#!/usr/bin/env python3
"""维护 feature-retcon 的本地追平契约和可逆写前日志。"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import difflib
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import uuid


SCHEMA_VERSION = 1
CONTRACT_NAME = "RECONCILIATION.md"
JOURNAL_BEGIN = "<!-- feature-retcon:journal:begin -->"
JOURNAL_END = "<!-- feature-retcon:journal:end -->"
MAX_EMBEDDED_PAYLOAD = 10 * 1024 * 1024
STAGES = ("requirements", "design", "tasks", "implementation", "validation")
STATUSES = ("executing", "paused", "blocked", "restoring", "restored", "ready_to_close")
ENTRY_STATUSES = ("prepared", "applied", "restored")
STATUS_TRANSITIONS = {
    "executing": {"paused", "blocked", "restoring"},
    "paused": {"executing", "blocked", "restoring"},
    "blocked": {"executing", "restoring"},
    "restoring": {"blocked"},
    "restored": {"blocked", "restoring"},
    "ready_to_close": {"executing", "blocked", "restoring"},
}

SENSITIVE_NAME_PATTERNS = (
    ("dotenv-file", re.compile(r"(^|/)\.env(?:\.|$)", re.IGNORECASE)),
    ("private-key-file", re.compile(r"(^|/)(?:id_[^/]+|[^/]+\.(?:pem|key|p12|pfx))$", re.IGNORECASE)),
    ("credential-file", re.compile(r"(?:credential|secret|token|password)", re.IGNORECASE)),
)
SENSITIVE_CONTENT_PATTERNS = (
    ("private-key-material", re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("cloud-access-key", re.compile(rb"\bAKIA[0-9A-Z]{16}\b")),
    ("provider-token", re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,})\b")),
    ("jwt-token", re.compile(rb"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")),
    ("bearer-token", re.compile(rb"(?im)^\s*authorization\s*[:=]\s*bearer\s+\S+")),
    (
        "credential-assignment",
        re.compile(
            rb"(?im)^\s*(?:password|passwd|secret|client[_-]?secret|token|access[_-]?token|api[_-]?(?:key|token))\s*[:=]"
        ),
    ),
)


class ContractError(RuntimeError):
    """表示可安全报告、无需堆栈的契约错误。"""


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_scalar(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def read_regular_file(path: Path) -> tuple[bytes, int]:
    if path.is_symlink():
        raise ContractError(f"拒绝跟随符号链接：{path}")
    if not path.is_file():
        raise ContractError(f"只支持常规文件：{path}")
    return path.read_bytes(), stat.S_IMODE(path.stat().st_mode)


def snapshot(path: Path) -> dict[str, object]:
    if not path.exists() and not path.is_symlink():
        return {"exists": False, "sha256": None, "mode": None}
    data, mode = read_regular_file(path)
    return {"exists": True, "sha256": sha256(data), "mode": mode, "data": data}


def public_snapshot(value: dict[str, object]) -> dict[str, object]:
    return {key: value.get(key) for key in ("exists", "sha256", "mode")}


def same_snapshot(left: dict[str, object], right: dict[str, object]) -> bool:
    return public_snapshot(left) == public_snapshot(right)


def encode_payload(data: bytes) -> str:
    return base64.b64encode(gzip.compress(data, compresslevel=9, mtime=0)).decode("ascii")


def decode_payload(payload: str) -> bytes:
    try:
        return gzip.decompress(base64.b64decode(payload.encode("ascii"), validate=True))
    except (ValueError, OSError) as exc:
        raise ContractError("恢复载荷损坏，无法解码") from exc


def detect_sensitive(path: Path, data: bytes | None) -> list[str]:
    normalized = path.as_posix()
    signals = [label for label, pattern in SENSITIVE_NAME_PATTERNS if pattern.search(normalized)]
    if data is not None:
        signals.extend(label for label, pattern in SENSITIVE_CONTENT_PATTERNS if pattern.search(data))
    return sorted(set(signals))


def reverse_diff(path: Path, new_data: bytes, original_data: bytes, sensitive: bool) -> str:
    if sensitive:
        return "[敏感内容：省略可读差异；恢复使用精确载荷。]"
    if max(len(new_data), len(original_data)) > 1024 * 1024:
        return "[文件超过 1 MiB：省略可读差异；恢复使用精确载荷。]"
    try:
        new_text = new_data.decode("utf-8").splitlines(keepends=True)
        old_text = original_data.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        return "[二进制或非 UTF-8 文件：恢复使用精确载荷。]"
    return "".join(
        difflib.unified_diff(
            new_text,
            old_text,
            fromfile=f"{path}（追平后）",
            tofile=f"{path}（追平前）",
        )
    ) or "[内容未变化；仅文件模式可能变化。]"


def parse_frontmatter(text: str) -> tuple[dict[str, object], int, int]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ContractError("契约缺少 YAML frontmatter")
    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None:
        raise ContractError("契约 YAML frontmatter 未闭合")
    values: dict[str, object] = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise ContractError(f"无法解析 frontmatter 行：{raw.strip()}")
        key, value = raw.split(":", 1)
        value = value.strip()
        if value in {"", "null", "~"}:
            parsed: object = None
        else:
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                parsed = value
        values[key.strip()] = parsed
    return values, 0, end


def extract_journal(text: str) -> dict[str, object]:
    if text.count(JOURNAL_BEGIN) != 1 or text.count(JOURNAL_END) != 1:
        raise ContractError("契约必须且只能包含一个恢复日志区块")
    payload = text.split(JOURNAL_BEGIN, 1)[1].split(JOURNAL_END, 1)[0].strip()
    if payload.startswith("```json") and payload.endswith("```"):
        payload = payload[len("```json") : -len("```")].strip()
    try:
        journal = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ContractError("恢复日志不是有效 JSON") from exc
    if not isinstance(journal, dict):
        raise ContractError("恢复日志根节点必须是对象")
    return journal


def replace_journal(text: str, journal: dict[str, object]) -> str:
    rendered = json.dumps(journal, ensure_ascii=False, indent=2, sort_keys=True)
    before, remainder = text.split(JOURNAL_BEGIN, 1)
    _, after = remainder.split(JOURNAL_END, 1)
    return f"{before}{JOURNAL_BEGIN}\n```json\n{rendered}\n```\n{JOURNAL_END}{after}"


def set_frontmatter(text: str, key: str, value: object) -> str:
    lines = text.splitlines(keepends=True)
    _, _, end = parse_frontmatter(text)
    prefix = f"{key}:"
    replacement = f"{key}: {json_scalar(value)}\n"
    for index in range(1, end):
        if lines[index].startswith(prefix):
            lines[index] = replacement
            return "".join(lines)
    lines.insert(end, replacement)
    return "".join(lines)


def atomic_write(path: Path, data: bytes, mode: int) -> None:
    if path.parent.exists() and path.parent.is_symlink():
        raise ContractError(f"拒绝写入符号链接目录：{path.parent}")
    if not path.parent.is_dir():
        raise ContractError(f"父目录不存在：{path.parent}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def write_contract(path: Path, text: str) -> None:
    atomic_write(path, text.encode("utf-8"), 0o600)


def load_contract(path_arg: str) -> tuple[Path, str, dict[str, object], dict[str, object]]:
    raw_path = Path(path_arg).expanduser().absolute()
    if raw_path.is_symlink():
        raise ContractError(f"拒绝通过符号链接加载契约：{raw_path}")
    path = raw_path.resolve()
    if path.name != CONTRACT_NAME:
        raise ContractError(f"契约文件名必须为 {CONTRACT_NAME}")
    if not path.is_file() or path.is_symlink():
        raise ContractError(f"契约不存在或不是常规文件：{path}")
    text = path.read_text(encoding="utf-8")
    frontmatter, _, _ = parse_frontmatter(text)
    journal = extract_journal(text)
    return path, text, frontmatter, journal


def save_contract(path: Path, text: str, journal: dict[str, object]) -> None:
    write_contract(path, replace_journal(text, journal))


def resolve_target(path_arg: str, writable_roots: list[str]) -> Path:
    raw_path = Path(path_arg).expanduser().absolute()
    if raw_path.is_symlink():
        raise ContractError(f"拒绝跟随符号链接：{raw_path}")
    path = raw_path.resolve(strict=False)
    roots = [Path(root).expanduser().resolve() for root in writable_roots]
    if not any(path == root or path.is_relative_to(root) for root in roots):
        raise ContractError(f"目标不在已授权可写工作根内：{path}")
    if path.name == CONTRACT_NAME:
        raise ContractError("恢复脚本不为追平契约自身创建日志")
    return path


def run_git(repo_hint: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_hint), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise ContractError(f"Git 不可用：{exc}") from exc
    if check and result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise ContractError(f"Git 读取失败：{message or '未知错误'}")
    return result


def git_root(path: Path) -> Path:
    hint = path if path.is_dir() else path.parent
    result = run_git(hint, "rev-parse", "--show-toplevel")
    return Path(result.stdout.decode("utf-8").strip()).resolve()


def git_blob(repo: Path, reference: str, path: Path) -> tuple[bytes, str]:
    try:
        relative = path.relative_to(repo).as_posix()
    except ValueError as exc:
        raise ContractError(f"文件不在 Git 仓库内：{path}") from exc
    result = run_git(repo, "show", f"{reference}:{relative}")
    return result.stdout, relative


def git_commit(repo: Path, reference: str) -> str:
    if not reference or reference.startswith("-") or any(char in reference for char in "\r\n\x00"):
        raise ContractError("baseline_ref 非法")
    result = run_git(repo, "rev-parse", "--verify", f"{reference}^{{commit}}")
    commit = result.stdout.decode("ascii", errors="strict").strip().lower()
    if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit) is None:
        raise ContractError("baseline_ref 未解析为不可变 Git 提交")
    return commit


def contract_is_tracked(contract: Path, authority_root: Path) -> bool:
    repo = git_root(authority_root)
    try:
        relative = contract.relative_to(repo).as_posix()
    except ValueError as exc:
        raise ContractError(f"契约不在声明的 Git 仓库内：{contract}") from exc
    result = run_git(repo, "ls-files", "--stage", "--", relative, check=False)
    return result.returncode == 0 and bool(result.stdout.strip())


def require_snapshot(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ContractError(f"{label} 必须是对象")
    exists = value.get("exists")
    digest = value.get("sha256")
    mode = value.get("mode")
    if not isinstance(exists, bool):
        raise ContractError(f"{label}.exists 必须是布尔值")
    if exists:
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise ContractError(f"{label}.sha256 非法")
        if not isinstance(mode, int) or isinstance(mode, bool) or not 0 <= mode <= 0o7777:
            raise ContractError(f"{label}.mode 非法")
    elif digest is not None or mode is not None:
        raise ContractError(f"{label} 不存在时 sha256 和 mode 必须为 null")
    return value


def require_schema(frontmatter: dict[str, object], journal: dict[str, object]) -> None:
    if frontmatter.get("schema_version") != SCHEMA_VERSION:
        raise ContractError(f"仅支持 schema_version: {SCHEMA_VERSION}")
    if frontmatter.get("status") not in STATUSES:
        raise ContractError("契约 status 非法")
    if frontmatter.get("target_stage") not in STAGES:
        raise ContractError("契约 target_stage 非法")
    completion = frontmatter.get("completion_stage")
    if completion is not None and (
        completion not in STAGES or STAGES.index(completion) < STAGES.index(frontmatter["target_stage"])
    ):
        raise ContractError("completion_stage 必须覆盖 target_stage")
    if journal.get("journal_version") != 1:
        raise ContractError("恢复日志版本不受支持")
    roots = journal.get("writable_roots")
    if not isinstance(roots, list) or not roots or not all(isinstance(root, str) for root in roots):
        raise ContractError("恢复日志缺少 writable_roots")
    entries = journal.get("entries")
    if not isinstance(entries, list):
        raise ContractError("恢复日志缺少 entries")
    for index, entry in enumerate(entries, start=1):
        label = f"日志项 J{index:04d}"
        if not isinstance(entry, dict):
            raise ContractError(f"{label} 必须是对象")
        if not isinstance(entry.get("id"), str):
            raise ContractError(f"{label}.id 非法")
        if not isinstance(entry.get("path"), str) or not Path(str(entry["path"])).is_absolute():
            raise ContractError(f"{label}.path 必须是绝对路径")
        status_value = entry.get("status")
        if status_value not in ENTRY_STATUSES:
            raise ContractError(f"{label}.status 非法")
        signals = entry.get("sensitive_signals")
        if not isinstance(signals, list) or not all(isinstance(signal, str) for signal in signals):
            raise ContractError(f"{label}.sensitive_signals 必须是字符串数组")
        if not isinstance(entry.get("sensitive_authorized"), bool):
            raise ContractError(f"{label}.sensitive_authorized 必须是布尔值")
        original = require_snapshot(entry.get("original"), f"{label}.original")
        if original.get("exists"):
            recovery = original.get("recovery")
            if recovery == "embed" and not isinstance(original.get("payload"), str):
                raise ContractError(f"{label}.original.payload 非法")
            if recovery == "git" and not all(
                isinstance(original.get(key), str) for key in ("git_repo", "git_ref", "git_path")
            ):
                raise ContractError(f"{label}.original 的 Git 恢复来源非法")
            if recovery not in {"embed", "git"}:
                raise ContractError(f"{label}.original.recovery 非法")
        elif original.get("recovery") != "none":
            raise ContractError(f"{label}.original.recovery 非法")
        applied = entry.get("applied")
        if status_value == "applied" or applied is not None:
            require_snapshot(applied, f"{label}.applied")


def resolve_entry_targets(entries: list[dict[str, object]], writable_roots: list[str]) -> list[Path]:
    return [resolve_target(str(entry["path"]), writable_roots) for entry in entries]


def original_bytes(entry: dict[str, object]) -> bytes:
    original = entry["original"]
    assert isinstance(original, dict)
    if not original.get("exists"):
        return b""
    recovery = original.get("recovery")
    if recovery == "embed":
        data = decode_payload(str(original.get("payload", "")))
    elif recovery == "git":
        repo = Path(str(original["git_repo"]))
        result = run_git(repo, "show", f"{original['git_ref']}:{original['git_path']}")
        data = result.stdout
    else:
        raise ContractError(f"日志项 {entry.get('id')} 缺少恢复来源")
    if sha256(data) != original.get("sha256"):
        raise ContractError(f"日志项 {entry.get('id')} 的恢复内容哈希不匹配")
    return data


def expected_current(entries: list[dict[str, object]]) -> dict[str, object]:
    active = [entry for entry in entries if entry.get("status") != "restored"]
    if not active:
        return dict(entries[0]["original"])
    latest = active[-1]
    if latest.get("status") == "applied":
        return dict(latest["applied"])
    return dict(latest["original"])


def cmd_init(args: argparse.Namespace) -> dict[str, object]:
    if args.completion_stage and STAGES.index(args.completion_stage) < STAGES.index(args.target_stage):
        raise ContractError("completion_stage 必须覆盖 target_stage")
    authority_root = Path(args.authority_root).expanduser().resolve()
    if not authority_root.is_dir():
        raise ContractError(f"权威根不存在：{authority_root}")
    roots = [Path(root).expanduser().resolve() for root in args.writable_root]
    if not roots or any(not root.is_dir() for root in roots):
        raise ContractError("每个可写工作根都必须是已存在目录")
    if not any(authority_root == root or authority_root.is_relative_to(root) for root in roots):
        raise ContractError("权威根必须位于一个已确认可写工作根内")
    contract = authority_root / CONTRACT_NAME
    if contract.exists() or contract.is_symlink():
        raise ContractError(f"检测到未完成轮次：{contract}")
    if args.version_control == "git" and not args.baseline_ref:
        raise ContractError("version_control=git 时必须提供 baseline_ref")
    repository: Path | None = None
    try:
        repository = git_root(authority_root)
        observed_version_control = "git"
    except ContractError:
        observed_version_control = "none"
    if observed_version_control != args.version_control:
        raise ContractError(
            f"version_control 与实际权威根不一致：声明 {args.version_control}，实际 {observed_version_control}"
        )
    baseline_ref = args.baseline_ref
    if repository is not None:
        baseline_ref = git_commit(repository, str(args.baseline_ref))

    template = (Path(__file__).resolve().parents[1] / "assets" / CONTRACT_NAME).read_text(encoding="utf-8")
    created_at = now_iso()
    journal = {
        "journal_version": 1,
        "writable_roots": [str(root) for root in roots],
        "entries": [],
    }
    replacements = {
        "{{SCHEMA_VERSION}}": str(SCHEMA_VERSION),
        "{{ROUND_ID}}": json_scalar(args.round_id or str(uuid.uuid4())),
        "{{AUTHORITY_ROOT}}": json_scalar(str(authority_root)),
        "{{TARGET_STAGE}}": json_scalar(args.target_stage),
        "{{COMPLETION_STAGE}}": json_scalar(args.completion_stage),
        "{{CREATED_AT}}": json_scalar(created_at),
        "{{CONFIRMED_AT}}": json_scalar(args.confirmed_at or created_at),
        "{{VERSION_CONTROL}}": json_scalar(args.version_control),
        "{{BASELINE_REF}}": json_scalar(baseline_ref),
        "{{JOURNAL_JSON}}": json.dumps(journal, ensure_ascii=False, indent=2, sort_keys=True),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    if "{{" in template or "}}" in template:
        raise ContractError("契约模板仍含未替换占位符")
    write_contract(contract, template)
    return {"contract": str(contract), "status": "executing", "mode": "0600"}


def cmd_prepare(args: argparse.Namespace) -> dict[str, object]:
    contract, text, frontmatter, journal = load_contract(args.contract)
    require_schema(frontmatter, journal)
    if frontmatter["status"] != "executing":
        raise ContractError("仅 executing 状态可以登记写前日志")
    target = resolve_target(args.path, list(journal["writable_roots"]))
    entries = list(journal["entries"])
    for entry in reversed(entries):
        if entry.get("path") == str(target) and entry.get("status") == "prepared":
            raise ContractError(f"文件已有尚未 applied 的日志项：{target}")

    before = snapshot(target)
    data = before.get("data") if before.get("exists") else None
    assert data is None or isinstance(data, bytes)
    signals = detect_sensitive(target, data)
    if signals and not args.allow_sensitive:
        raise ContractError(f"检测到敏感候选，需逐文件确认后使用 --allow-sensitive：{target}；信号={','.join(signals)}")

    original: dict[str, object] = public_snapshot(before)
    if before["exists"]:
        assert isinstance(data, bytes)
        if args.recovery_mode == "git":
            if frontmatter.get("version_control") != "git":
                raise ContractError("只有 Git 基线契约可以使用 recovery-mode=git")
            repo = git_root(target)
            baseline, relative = git_blob(repo, str(frontmatter.get("baseline_ref")), target)
            if baseline != data:
                raise ContractError("当前文件与 baseline_ref 不一致，必须使用 embed 保存本轮真实基线")
            original.update(
                recovery="git",
                git_repo=str(repo),
                git_ref=str(frontmatter.get("baseline_ref")),
                git_path=relative,
            )
        else:
            payload = encode_payload(data)
            if len(payload.encode("ascii")) > MAX_EMBEDDED_PAYLOAD and not args.allow_large:
                raise ContractError(
                    f"恢复载荷超过 10 MiB，需选择 Git、缩小范围或确认后使用 --allow-large：{target}"
                )
            original.update(recovery="embed", payload=payload)
    else:
        original.update(recovery="none")

    entry = {
        "id": f"J{len(entries) + 1:04d}",
        "path": str(target),
        "prepared_at": now_iso(),
        "status": "prepared",
        "sensitive_signals": signals,
        "sensitive_authorized": bool(args.allow_sensitive),
        "original": original,
        "applied": None,
        "reverse_diff": None,
    }
    entries.append(entry)
    journal["entries"] = entries
    save_contract(contract, text, journal)
    return {"entry": entry["id"], "path": str(target), "status": "prepared", "sensitive_signals": signals}


def cmd_applied(args: argparse.Namespace) -> dict[str, object]:
    contract, text, frontmatter, journal = load_contract(args.contract)
    require_schema(frontmatter, journal)
    if frontmatter["status"] != "executing":
        raise ContractError("仅 executing 状态可以确认文件变更")
    target = resolve_target(args.path, list(journal["writable_roots"]))
    entries = list(journal["entries"])
    entry = next(
        (item for item in reversed(entries) if item.get("path") == str(target) and item.get("status") == "prepared"),
        None,
    )
    if entry is None:
        raise ContractError(f"找不到 prepared 日志项：{target}")
    after = snapshot(target)
    original = entry["original"]
    assert isinstance(original, dict)
    old_data = original_bytes(entry) if original.get("exists") else b""
    new_data = after.get("data") if after.get("exists") else b""
    assert isinstance(new_data, bytes)
    new_signals = detect_sensitive(target, new_data if after.get("exists") else None)
    all_signals = sorted(set(entry["sensitive_signals"]) | set(new_signals))
    entry["sensitive_signals"] = all_signals
    entry["applied"] = public_snapshot(after)
    entry["applied_at"] = now_iso()
    entry["reverse_diff"] = reverse_diff(target, new_data, old_data, bool(all_signals))
    entry["status"] = "applied"
    newly_sensitive = bool(new_signals) and not bool(entry.get("sensitive_authorized"))
    if newly_sensitive:
        text = set_frontmatter(text, "status", "blocked")
    save_contract(contract, text, journal)
    if newly_sensitive:
        raise ContractError(
            f"变更后检测到新的敏感候选，已安全记录并阻塞；需逐文件确认后继续：{target}；"
            f"信号={','.join(new_signals)}"
        )
    return {"entry": entry["id"], "path": str(target), "status": "applied", "sha256": after.get("sha256")}


def cmd_status(args: argparse.Namespace) -> dict[str, object]:
    contract, text, frontmatter, journal = load_contract(args.contract)
    require_schema(frontmatter, journal)
    if args.set_status:
        current = str(frontmatter["status"])
        requested = args.set_status
        if requested not in STATUS_TRANSITIONS[current]:
            raise ContractError(f"非法状态迁移：{current} -> {requested}")
        text = set_frontmatter(text, "status", requested)
        write_contract(contract, text)
        frontmatter["status"] = requested
    counts: dict[str, int] = {}
    for entry in journal["entries"]:
        state = str(entry.get("status"))
        counts[state] = counts.get(state, 0) + 1
    return {
        "contract": str(contract),
        "round_id": frontmatter.get("round_id"),
        "status": frontmatter.get("status"),
        "target_stage": frontmatter.get("target_stage"),
        "completion_stage": frontmatter.get("completion_stage"),
        "closure_recorded": bool(journal.get("closure")),
        "entries": counts,
    }


def cmd_scope(args: argparse.Namespace) -> dict[str, object]:
    contract, text, frontmatter, journal = load_contract(args.contract)
    require_schema(frontmatter, journal)
    if frontmatter["status"] not in {"executing", "paused", "blocked"}:
        raise ContractError("当前状态不能调整执行边界")
    completion = args.completion_stage or frontmatter.get("completion_stage")
    if completion not in STAGES or STAGES.index(completion) < STAGES.index(args.target_stage):
        raise ContractError("必须明确覆盖执行上限的 completion_stage")
    previous = frontmatter.get("completion_stage")
    if previous and STAGES.index(completion) < STAGES.index(previous):
        raise ContractError("不能降低原轮次的闭环终点；保留契约并处理剩余工作或恢复")
    if not args.confirmation.strip():
        raise ContractError("需要用户确认的原文或定位")
    roots = list(journal["writable_roots"])
    added_roots: list[str] = []
    for root_arg in args.writable_root or []:
        root = Path(root_arg).expanduser().resolve()
        if not root.is_dir():
            raise ContractError(f"可写工作根不存在：{root}")
        if str(root) not in roots:
            roots.append(str(root))
            added_roots.append(str(root))
    journal.setdefault("scope_changes", []).append({
        "at": now_iso(), "confirmation": args.confirmation,
        "previous_target": frontmatter["target_stage"], "target_stage": args.target_stage,
        "previous_completion": previous, "completion_stage": completion,
        "added_writable_roots": added_roots,
    })
    journal["writable_roots"] = roots
    text = set_frontmatter(text, "target_stage", args.target_stage)
    text = set_frontmatter(text, "completion_stage", completion)
    save_contract(contract, text, journal)
    return {"contract": str(contract), "target_stage": args.target_stage, "completion_stage": completion}


def restore_one(entry: dict[str, object], target: Path) -> None:
    current = snapshot(target)
    original = entry["original"]
    assert isinstance(original, dict)
    if same_snapshot(current, original):
        return
    status_value = entry.get("status")
    expected = entry.get("applied") if status_value == "applied" else entry.get("original")
    assert isinstance(expected, dict)
    if not same_snapshot(current, expected):
        raise ContractError(f"检测到外部漂移，停止恢复：{target}")
    if original.get("exists"):
        data = original_bytes(entry)
        mode = int(original["mode"])
        atomic_write(target, data, mode)
    elif current.get("exists"):
        if target.is_symlink() or not target.is_file():
            raise ContractError(f"拒绝删除非常规文件：{target}")
        target.unlink()
    restored = snapshot(target)
    if not same_snapshot(restored, original):
        raise ContractError(f"恢复后校验失败：{target}")


def cmd_restore(args: argparse.Namespace) -> dict[str, object]:
    contract, text, frontmatter, journal = load_contract(args.contract)
    require_schema(frontmatter, journal)
    if frontmatter["status"] == "ready_to_close":
        raise ContractError("契约已经 ready_to_close")
    entries = list(journal["entries"])
    targets = resolve_entry_targets(entries, list(journal["writable_roots"]))
    if frontmatter["status"] != "restoring":
        text = set_frontmatter(text, "status", "restoring")
        write_contract(contract, text)
    restored_ids: list[str] = []
    try:
        for entry, target in reversed(list(zip(entries, targets))):
            if entry.get("status") == "restored":
                continue
            restore_one(entry, target)
            entry["status"] = "restored"
            entry["restored_at"] = now_iso()
            restored_ids.append(str(entry["id"]))
            _, latest_text, _, _ = load_contract(str(contract))
            save_contract(contract, latest_text, journal)
    except ContractError:
        _, latest_text, _, _ = load_contract(str(contract))
        latest_text = set_frontmatter(latest_text, "status", "blocked")
        save_contract(contract, latest_text, journal)
        raise
    _, latest_text, _, _ = load_contract(str(contract))
    latest_text = set_frontmatter(latest_text, "status", "restored")
    journal.pop("closure", None)
    save_contract(contract, latest_text, journal)
    return {"contract": str(contract), "status": "restored", "restored": restored_ids}


def verify_entry_chains(entries: list[dict[str, object]], writable_roots: list[str]) -> list[str]:
    issues: list[str] = []
    grouped: dict[str, list[dict[str, object]]] = {}
    for index, entry in enumerate(entries, start=1):
        expected_id = f"J{index:04d}"
        if entry.get("id") != expected_id:
            issues.append(f"日志编号不连续：期望 {expected_id}")
        try:
            target = resolve_target(str(entry["path"]), writable_roots)
        except ContractError as exc:
            issues.append(str(exc))
            continue
        grouped.setdefault(str(target), []).append(entry)
    for path, path_entries in grouped.items():
        for previous, current in zip(path_entries, path_entries[1:]):
            if previous.get("applied") is None:
                issues.append(f"前序日志未 applied：{path}")
                continue
            if public_snapshot(dict(previous["applied"])) != public_snapshot(dict(current["original"])):
                issues.append(f"同一文件的日志链不连续：{path}")
        expected = expected_current(path_entries)
        try:
            actual = snapshot(Path(path))
        except ContractError as exc:
            issues.append(str(exc))
            continue
        if not same_snapshot(actual, expected):
            issues.append(f"当前文件状态与恢复日志不一致：{path}")
        for entry in path_entries:
            original = entry.get("original")
            if isinstance(original, dict) and original.get("exists"):
                try:
                    original_bytes(entry)
                except ContractError as exc:
                    issues.append(str(exc))
    return issues


def closure_fingerprint(text: str, journal: dict[str, object]) -> str:
    journal = dict(journal)
    journal.pop("closure", None)
    normalized = replace_journal(set_frontmatter(text, "status", "executing"), journal)
    return sha256(normalized.encode("utf-8"))


def closure_evidence(
    contract: Path, evidence_arg: str, frontmatter: dict[str, object], journal: dict[str, object]
) -> dict[str, object]:
    evidence_path = Path(evidence_arg).expanduser().absolute()
    data, _ = read_regular_file(evidence_path)
    if evidence_path.resolve() == contract:
        raise ContractError("关闭证据必须保存在契约之外的验收载体")
    try:
        evidence = json.loads(data)
    except (ValueError, UnicodeError) as exc:
        raise ContractError("关闭证据必须为 JSON") from exc
    if not isinstance(evidence, dict) or evidence.get("round_id") != frontmatter.get("round_id"):
        raise ContractError("关闭证据 round_id 不匹配")
    if evidence.get("remaining_work") != []:
        raise ContractError("关闭证据必须明确 remaining_work: []；有剩余工作时保留契约")
    outcome = evidence.get("outcome")
    entries = journal["entries"]
    if outcome == "completed":
        completion = frontmatter.get("completion_stage")
        if completion not in STAGES:
            raise ContractError("缺少闭环终点；先用 scope 登记确认的 completion_stage")
        if frontmatter["target_stage"] != completion:
            raise ContractError("只达到本次执行上限，尚未到闭环终点；暂停并保留契约")
        if evidence.get("completed_stage") != completion:
            raise ContractError("关闭证据 completed_stage 未达到闭环终点")
        if frontmatter["status"] not in {"executing", "ready_to_close"}:
            raise ContractError("当前状态不能完成轮次")
        if any(entry["status"] != "applied" for entry in entries):
            raise ContractError("完成轮次要求全部变更已 applied")
        required = list(STAGES[:STAGES.index(completion) + 1]) + ["residuals", "watermark", "absorption"]
    elif outcome == "restored":
        if frontmatter["status"] not in {"restored", "ready_to_close"}:
            raise ContractError("先运行 restore 并复验基线")
        if any(entry["status"] != "restored" for entry in entries):
            raise ContractError("仍有未恢复的日志项")
        required = ["baseline", "references", "absorption"]
    else:
        raise ContractError("关闭证据 outcome 必须为 completed 或 restored")
    checks = evidence.get("checks")
    if not isinstance(checks, dict):
        raise ContractError("关闭证据缺少 checks")
    files: dict[str, object] = {}
    for name in dict.fromkeys(required + list(checks)):
        check = checks.get(name)
        if not isinstance(check, dict) or check.get("result") != "pass":
            raise ContractError(f"关闭门槛未通过：{name}")
        references = check.get("evidence")
        if not isinstance(references, list) or not references:
            raise ContractError(f"关闭门槛缺少证据文件：{name}")
        for reference in references:
            if not isinstance(reference, str) or not Path(reference).is_absolute():
                raise ContractError(f"证据路径必须为绝对路径：{name}")
            path = Path(reference)
            if path.resolve() in {contract, evidence_path.resolve()}:
                raise ContractError("门槛证据必须指向独立的权威产物或验收记录")
            content, _ = read_regular_file(path)
            if not content.strip():
                raise ContractError(f"证据文件为空：{path}")
            files[str(path)] = public_snapshot(snapshot(path))
    return {"evidence_path": str(evidence_path), "evidence_sha256": sha256(data), "files": files}


def cmd_verify(args: argparse.Namespace) -> dict[str, object]:
    contract, text, frontmatter, journal = load_contract(args.contract)
    require_schema(frontmatter, journal)
    issues: list[str] = []
    mode = stat.S_IMODE(contract.stat().st_mode)
    if mode != 0o600:
        issues.append(f"契约权限必须为 0600，当前为 {mode:04o}")
    authority_root = Path(str(frontmatter["authority_root"]))
    if frontmatter.get("version_control") == "git":
        try:
            if contract_is_tracked(contract, authority_root):
                issues.append("追平契约已被 Git 跟踪或暂存")
        except ContractError as exc:
            issues.append(str(exc))
    entries = list(journal["entries"])
    issues.extend(verify_entry_chains(entries, list(journal["writable_roots"])))
    if any(entry.get("status") == "prepared" for entry in entries):
        issues.append("存在尚未 applied 的写前日志")
    closure_issues: list[str] = []
    if frontmatter["status"] == "ready_to_close":
        certificate = journal.get("closure")
        try:
            if not isinstance(certificate, dict):
                raise ContractError("缺少关闭证据登记；旧 ready_to_close 不能直接删除")
            if certificate.get("fingerprint") != closure_fingerprint(text, journal):
                raise ContractError("契约在关闭复核后发生变化，需重新复核")
            current = closure_evidence(contract, str(certificate.get("evidence_path")), frontmatter, journal)
            if any(certificate.get(key) != value for key, value in current.items()):
                raise ContractError("关闭证据发生漂移，需重新验证")
        except ContractError as exc:
            closure_issues.append(str(exc))
    if args.mark_ready:
        if issues:
            raise ContractError("机械校验未通过，不能标记 ready_to_close")
        if frontmatter["status"] not in {"executing", "restored"}:
            raise ContractError(f"当前状态不能标记 ready_to_close：{frontmatter['status']}")
        if not args.evidence:
            raise ContractError("需要 --evidence；机械 valid 不代表轮次完成")
        certificate = closure_evidence(contract, args.evidence, frontmatter, journal)
        certificate["fingerprint"] = closure_fingerprint(text, journal)
        journal["closure"] = certificate
        text = set_frontmatter(text, "status", "ready_to_close")
        save_contract(contract, text, journal)
        frontmatter["status"] = "ready_to_close"
    return {
        "contract": str(contract),
        "status": frontmatter.get("status"),
        "valid": not issues,
        "issues": issues,
        "close_ready": frontmatter["status"] == "ready_to_close" and not issues and not closure_issues,
        "closure_issues": closure_issues,
        "entry_count": len(entries),
    }


def cmd_close(args: argparse.Namespace) -> dict[str, object]:
    result = cmd_verify(argparse.Namespace(contract=args.contract, mark_ready=False))
    if not result["close_ready"]:
        raise ContractError("关闭门槛未满足，保留契约：" + "; ".join(result["issues"] + result["closure_issues"]))
    contract = Path(str(result["contract"]))
    contract.unlink()
    return {"contract": str(contract), "closed": True}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="创建权限为 0600 的追平契约")
    init_parser.add_argument("authority_root")
    init_parser.add_argument("--round-id")
    init_parser.add_argument("--target-stage", choices=STAGES, required=True)
    init_parser.add_argument("--completion-stage", choices=STAGES, help="整轮闭环终点；省略时禁止正常关闭")
    init_parser.add_argument("--confirmed-at")
    init_parser.add_argument("--version-control", choices=("git", "none"), required=True)
    init_parser.add_argument("--baseline-ref")
    init_parser.add_argument("--writable-root", action="append", required=True)
    init_parser.set_defaults(handler=cmd_init)

    prepare_parser = subparsers.add_parser("prepare", help="在文件变更前记录可逆基线")
    prepare_parser.add_argument("contract")
    prepare_parser.add_argument("--path", required=True)
    prepare_parser.add_argument("--recovery-mode", choices=("embed", "git"), default="embed")
    prepare_parser.add_argument("--allow-sensitive", action="store_true")
    prepare_parser.add_argument("--allow-large", action="store_true")
    prepare_parser.set_defaults(handler=cmd_prepare)

    applied_parser = subparsers.add_parser("applied", help="记录文件变更后的哈希与反向差异")
    applied_parser.add_argument("contract")
    applied_parser.add_argument("--path", required=True)
    applied_parser.set_defaults(handler=cmd_applied)

    status_parser = subparsers.add_parser("status", help="查看或更新机械状态")
    status_parser.add_argument("contract")
    status_parser.add_argument("--set", dest="set_status", choices=("executing", "paused", "blocked", "restoring"))
    status_parser.set_defaults(handler=cmd_status)

    scope_parser = subparsers.add_parser("scope", help="在同一轮次记录用户确认的执行上限和闭环终点")
    scope_parser.add_argument("contract")
    scope_parser.add_argument("--target-stage", choices=STAGES, required=True)
    scope_parser.add_argument("--completion-stage", choices=STAGES)
    scope_parser.add_argument("--confirmation", required=True)
    scope_parser.add_argument("--writable-root", action="append", help="追加本次已明确授权的可写根")
    scope_parser.set_defaults(handler=cmd_scope)

    restore_parser = subparsers.add_parser("restore", help="按逆序恢复本轮全部文件变更")
    restore_parser.add_argument("contract")
    restore_parser.set_defaults(handler=cmd_restore)

    verify_parser = subparsers.add_parser("verify", help="校验 schema、日志链、哈希、权限和 Git 状态")
    verify_parser.add_argument("contract")
    verify_parser.add_argument("--mark-ready", action="store_true")
    verify_parser.add_argument("--evidence", help="当前轮次的关闭证据 JSON 文件")
    verify_parser.set_defaults(handler=cmd_verify)

    close_parser = subparsers.add_parser("close", help="重新核验关闭证据后显式删除契约")
    close_parser.add_argument("contract")
    close_parser.set_defaults(handler=cmd_close)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
    except ContractError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
