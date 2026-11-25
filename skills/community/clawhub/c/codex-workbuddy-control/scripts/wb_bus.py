#!/usr/bin/env python3
"""Portable file bus for Codex <-> WorkBuddy task and verification hand-offs.

Only the Python standard library is used. Runtime paths are supplied by CLI
arguments or WB_BUS_* environment variables; the skill package contains no
machine-specific paths.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
import time
from pathlib import Path
from typing import Iterator

SCRIPT = Path(__file__).resolve()
SKILL_ROOT = SCRIPT.parent.parent
TEMPLATES = SKILL_ROOT / "templates"
ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{8}-\d{3}$")
WB_RESULTS = {"WB_PASS", "WB_FAIL", "WB_PARTIAL"}
CANDIDATE_RESULTS = {"PASS", "FAIL"}


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def today() -> str:
    return dt.datetime.now().astimezone().date().isoformat()


def month_key() -> str:
    return today()[:7]


def one_line(value: object) -> str:
    return " ".join(str(value).split())


def cell(value: object) -> str:
    return one_line(value).replace("|", "/")


def bullet(values: list[str], empty: str) -> str:
    return "\n".join(f"- {one_line(item)}" for item in values) if values else empty


def numbered(values: list[str]) -> str:
    return "\n".join(f"{index}. `{one_line(item)}`" for index, item in enumerate(values, 1))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def changed_manifest(paths: list[str]) -> str:
    rows: list[str] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"改动文件不存在: {path}")
        rows.append(f"- `{path}`  \n  SHA-256：`{sha256_file(path)}`")
    return "\n".join(rows)


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(temporary)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def atomic_json(path: Path, payload: dict) -> None:
    atomic_text(path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def read_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON 对象无效: {path}")
    return payload


def validate_id(task_id: str) -> None:
    if not ID_RE.match(task_id):
        raise ValueError(f"无效编号: {task_id}（示例 WB-YYYYMMDD-NNN）")


def render(template_name: str, values: dict[str, str]) -> str:
    path = TEMPLATES / template_name
    text = path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)))
    if unresolved:
        raise ValueError(f"模板 {template_name} 存在未替换字段: {', '.join(unresolved)}")
    return text


def nonportable_commands(commands: list[str]) -> list[str]:
    errors: list[str] = []
    for index, command in enumerate(commands, 1):
        for segment in re.split(r"\s*(?:&&|\|\||[;|])\s*", command):
            try:
                tokens = shlex.split(segment)
            except ValueError:
                continue
            while tokens and (tokens[0] in {"env", "command"} or re.match(r"^[A-Za-z_]\w*=", tokens[0])):
                tokens.pop(0)
            if not tokens:
                continue
            executable = Path(tokens[0]).name
            if executable in {"rg", "codex"}:
                errors.append(
                    f"第 {index} 条复验命令依赖 WorkBuddy shell 不保证存在的 `{executable}`；"
                    "改用 Python、绝对路径工具或纯 shell。"
                )
    return errors


class Bus:
    def __init__(self, root: str, ledger: str | None = None, review_dir: str | None = None):
        self.root = Path(root).expanduser().resolve()
        config: dict = {}
        config_path = self.root / "bus.json"
        if config_path.is_file():
            try:
                config = read_json(config_path)
            except (OSError, ValueError, json.JSONDecodeError):
                config = {}
        self.ledger = Path(
            ledger or os.environ.get("WB_BUS_LEDGER") or config.get("ledger") or self.root / "shared" / "任务台账.md"
        ).expanduser().resolve()
        self.review_dir = Path(
            review_dir
            or os.environ.get("WB_BUS_REVIEW_DIR")
            or config.get("review_dir")
            or self.root / "shared" / "复盘"
        ).expanduser().resolve()
        self.tasks = self.root / "tasks"
        self.queue = self.root / "queue"
        self.pending = self.queue / "pending"
        self.claimed = self.queue / "claimed"
        self.completed = self.queue / "completed"
        self.failed = self.queue / "failed"
        self.candidates = self.root / "candidates"
        self.pending_verify = self.root / "待验证"
        self.verified = self.root / "已验证"
        self.rework = self.root / "返工"
        self.lock_path = self.queue / ".wb-bus.lock"

    def ensure(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        for directory in (
            self.tasks,
            self.pending,
            self.claimed,
            self.completed,
            self.failed,
            self.candidates,
            self.pending_verify,
            self.verified,
            self.rework,
            self.review_dir,
            self.ledger.parent,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        if not self.ledger.is_file():
            atomic_text(
                self.ledger,
                "# Codex × WorkBuddy 任务台账\n\n"
                "| 日期 | 编号 | 任务 | 主责 | 状态 | 证据 | 复盘 |\n"
                "|---|---|---|---|---|---|---|\n",
            )
        review = self.review_dir / f"{month_key()}.md"
        if not review.is_file():
            atomic_text(review, f"# Codex × WorkBuddy 复盘 {month_key()}\n\n")
        config = self.root / "bus.json"
        if not config.is_file():
            atomic_json(
                config,
                {
                    "schema": 1,
                    "created_at": now_iso(),
                    "ledger": str(self.ledger),
                    "review_dir": str(self.review_dir),
                },
            )

    def exists(self, task_id: str) -> bool:
        names = [f"{task_id}.json", task_id]
        for directory in (self.pending, self.claimed, self.completed, self.failed, self.candidates, self.tasks):
            if any((directory / name).exists() for name in names):
                return True
        for directory in (self.pending_verify, self.verified, self.rework):
            if (directory / f"{task_id}.md").exists():
                return True
        if self.ledger.is_file() and f"`{task_id}`" in self.ledger.read_text(encoding="utf-8"):
            return True
        return False

    def append_ledger(self, task_id: str, title: str, role: str, status: str, evidence: str) -> None:
        if f"`{task_id}`" in self.ledger.read_text(encoding="utf-8"):
            return
        row = (
            f"| {today()} | `{task_id}` | {cell(title)} | {cell(role)} | `{cell(status)}` | "
            f"{cell(evidence)} | - |\n"
        )
        with self.ledger.open("a", encoding="utf-8") as handle:
            handle.write(row)

    def update_ledger(self, task_id: str, status: str, evidence: str) -> bool:
        lines = self.ledger.read_text(encoding="utf-8").splitlines()
        changed = False
        for index, line in enumerate(lines):
            if not line.startswith("|") or f"`{task_id}`" not in line:
                continue
            cells = line.split("|")
            if len(cells) >= 8:
                cells[5] = f" `{cell(status)}` "
                cells[6] = f" {cell(evidence)} "
                cells[7] = f" {month_key()} "
                lines[index] = "|".join(cells)
                changed = True
                break
        if changed:
            atomic_text(self.ledger, "\n".join(lines) + "\n")
        return changed

    def append_review(self, task_id: str, title: str, result: str, evidence: str) -> Path:
        path = self.review_dir / f"{month_key()}.md"
        current = path.read_text(encoding="utf-8") if path.is_file() else f"# Codex × WorkBuddy 复盘 {month_key()}\n\n"
        heading = f"## {today()} `{task_id}` {one_line(title)}"
        if heading not in current:
            current = current.rstrip() + (
                f"\n\n{heading}\n\n"
                f"- 结果：`{one_line(result)}`\n"
                f"- 证据：{one_line(evidence)}\n"
                "- 风险：以任务包、回执和验证结果中的未完成项为准。\n"
                "- 后续：PASS/完成则归档；FAIL/PARTIAL 则返工或交用户决定。\n"
            )
            atomic_text(path, current.rstrip() + "\n")
        return path

    @contextlib.contextmanager
    def lock(self) -> Iterator[None]:
        self.queue.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + 10
        handle: int | None = None
        while handle is None:
            try:
                handle = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    age = time.time() - self.lock_path.stat().st_mtime
                    if age > 120:
                        self.lock_path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"等待队列锁超时: {self.lock_path}")
                time.sleep(0.05)
        try:
            os.write(handle, f"{os.getpid()} {now_iso()}\n".encode())
            yield
        finally:
            os.close(handle)
            try:
                self.lock_path.unlink()
            except FileNotFoundError:
                pass


def command_claim(bus: Bus) -> str:
    return (
        f"{shlex.quote(sys.executable)} {shlex.quote(str(SCRIPT))} "
        f"--root {shlex.quote(str(bus.root))} claim --worker workbuddy"
    )


def command_complete(bus: Bus, task_id: str) -> str:
    return (
        f"{shlex.quote(sys.executable)} {shlex.quote(str(SCRIPT))} "
        f"--root {shlex.quote(str(bus.root))} complete --id {shlex.quote(task_id)}"
    )


def cmd_init(bus: Bus) -> int:
    bus.ensure()
    print(
        json.dumps(
            {
                "status": "INITIALIZED",
                "root": str(bus.root),
                "ledger": str(bus.ledger),
                "review_dir": str(bus.review_dir),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_dispatch(bus: Bus, args: argparse.Namespace) -> int:
    bus.ensure()
    validate_id(args.id)
    if not args.id.startswith("WB-"):
        raise ValueError("dispatch 只接受 WB-YYYYMMDD-NNN")
    with bus.lock():
        if bus.exists(args.id):
            raise FileExistsError(f"编号已存在，禁止重复派发: {args.id}")
        task_dir = bus.tasks / args.id
        task_dir.mkdir(parents=True, exist_ok=False)
        package = task_dir / "任务包.md"
        content = render(
            "任务包.md",
            {
                "ID": args.id,
                "TITLE": args.title,
                "CREATED": now_iso(),
                "GOAL": args.goal,
                "WORKBUDDY_SCOPE": bullet(args.workbuddy, "- 按目标完成资料、报告、表格或明确指派的工作。"),
                "CODEX_SCOPE": bullet(args.codex, "- Codex 负责最终验收、修复和发布。"),
                "INPUTS": bullet(args.input, "- 无额外输入。"),
                "DELIVERABLES": bullet(args.deliverable, "- 按目标交付可编辑文件和回执。"),
                "ACCEPTANCE": bullet(args.acceptance, "- 交付物可打开；来源、未知项、风险和数据边界如实记录。"),
                "CONSTRAINTS": bullet(args.constraint, "- 不修改任务包、生产代码、共享台账或发布包。"),
                "CLAIM_COMMAND": command_claim(bus),
                "COMPLETE_COMMAND": command_complete(bus, args.id),
            },
        )
        atomic_text(package, content)
        receipt = task_dir / "回执包.md"
        payload = {
            "schema": 1,
            "task_id": args.id,
            "title": args.title,
            "kind": "task",
            "status": "QUEUED",
            "package_path": str(package),
            "receipt_path": str(receipt),
            "created_at": now_iso(),
        }
        atomic_json(bus.pending / f"{args.id}.json", payload)
        bus.append_ledger(
            args.id, args.title, "WorkBuddy 执行；Codex 验收", "QUEUED", f"任务包：{package}"
        )
    print(json.dumps({"status": "QUEUED", "id": args.id, "package": str(package)}, ensure_ascii=False, indent=2))
    return 0


def verify_values(bus: Bus, args: argparse.Namespace, manifest: str) -> dict[str, str]:
    return {
        "ID": args.id,
        "TITLE": args.title,
        "REQUEST_TYPE": "Codex 交付只读独立验收",
        "IMPLEMENTER": "Codex（实现与自测已完成）",
        "VERIFIER": "WorkBuddy",
        "FINAL_OWNER": "Codex",
        "CREATED": now_iso(),
        "GOAL": args.goal,
        "CANDIDATE_DIR": "- 无；直接对下方工作目录做只读验收。",
        "CHANGED_MANIFEST": manifest,
        "CWD": f"- `{Path(args.cwd).expanduser().resolve()}`",
        "COMMANDS": numbered(args.command),
        "EVIDENCE": bullet(args.evidence, "- Codex 未提供自测证据；独立验收应按 PARTIAL 风险处理。"),
        "ACCEPTANCE": bullet(args.acceptance, "- 所有复验命令有真实 EXIT、关键输出，且满足本次目标。"),
        "RISKS": bullet(args.risk, "- 未发现额外风险；以实际命令输出为准。")
        + "\n- WorkBuddy 不得修改代码、修复、格式化、合并或发布。",
        "CLAIM_COMMAND": command_claim(bus),
        "COMPLETE_COMMAND": command_complete(bus, args.id),
    }


def cmd_verify(bus: Bus, args: argparse.Namespace) -> int:
    bus.ensure()
    validate_id(args.id)
    with bus.lock():
        if bus.exists(args.id):
            raise FileExistsError(f"编号已存在，禁止重复登记: {args.id}")
        if args.id.startswith("WBC-"):
            if not args.candidate_dir:
                raise ValueError("WBC 候选验收必须提供 --candidate-dir")
            candidate_dir = Path(args.candidate_dir).expanduser().resolve()
            request = candidate_dir / "验证请求.md"
            if not candidate_dir.is_dir():
                raise FileNotFoundError(f"候选目录不存在: {candidate_dir}")
            if not request.is_file():
                raise FileNotFoundError(f"候选目录缺少 验证请求.md: {request}")
            marker = bus.pending_verify / f"{args.id}.md"
            atomic_text(marker, request.read_text(encoding="utf-8"))
            metadata = {
                "schema": 1,
                "task_id": args.id,
                "title": args.title,
                "kind": "candidate",
                "status": "WAITING_VERIFY",
                "candidate_dir": str(candidate_dir),
                "request_path": str(request),
                "marker_path": str(marker),
                "created_at": now_iso(),
            }
            atomic_json(bus.candidates / f"{args.id}.json", metadata)
            bus.append_ledger(
                args.id,
                args.title,
                "WorkBuddy 候选；Codex 最终验收",
                "WAITING_VERIFY",
                f"候选请求：{request}",
            )
            print(
                json.dumps(
                    {"status": "WAITING_VERIFY", "id": args.id, "request": str(request), "marker": str(marker)},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        if not args.id.startswith("WBV-"):
            raise ValueError("verify 接受 WBV-* 正向验收或 WBC-* 候选")
        if not args.goal:
            raise ValueError("WBV 验收必须提供 --goal")
        if not args.changed_file:
            raise ValueError("WBV 验收至少提供一个 --changed-file")
        if not args.command:
            raise ValueError("WBV 验收至少提供一个可复跑 --command")
        cwd = Path(args.cwd).expanduser().resolve()
        if not cwd.is_dir():
            raise FileNotFoundError(f"cwd 不存在: {cwd}")
        errors = nonportable_commands(args.command)
        if errors:
            raise ValueError("\n".join(errors))
        manifest = changed_manifest(args.changed_file)
        values = verify_values(bus, args, manifest)
        content = render("验证请求.md", values)
        task_dir = bus.tasks / args.id
        task_dir.mkdir(parents=True, exist_ok=False)
        package = task_dir / "任务包.md"
        request = task_dir / "验证请求.md"
        atomic_text(package, content)
        atomic_text(request, content)
        receipt = task_dir / "回执包.md"
        payload = {
            "schema": 1,
            "task_id": args.id,
            "title": args.title,
            "kind": "verification",
            "status": "QUEUED",
            "package_path": str(package),
            "request_path": str(request),
            "receipt_path": str(receipt),
            "created_at": now_iso(),
        }
        atomic_json(bus.pending / f"{args.id}.json", payload)
        bus.append_ledger(
            args.id,
            args.title,
            "Codex 实现；WorkBuddy 独立验收",
            "QUEUED",
            f"验收请求：{request}",
        )
    print(
        json.dumps(
            {"status": "QUEUED", "id": args.id, "package": str(package), "receipt": str(receipt)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_status(bus: Bus) -> int:
    if not bus.root.is_dir():
        raise FileNotFoundError(f"总线根不存在，请先 init: {bus.root}")

    def entries(directory: Path) -> list[dict]:
        rows: list[dict] = []
        for path in sorted(directory.glob("*.json")):
            try:
                payload = read_json(path)
                rows.append(
                    {
                        "id": payload.get("task_id", path.stem),
                        "status": payload.get("status", "UNKNOWN"),
                        "kind": payload.get("kind", ""),
                        "queue_file": str(path),
                    }
                )
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                rows.append({"id": path.stem, "status": "INVALID", "error": str(exc), "queue_file": str(path)})
        return rows

    payload = {
        "root": str(bus.root),
        "ledger": str(bus.ledger),
        "review_dir": str(bus.review_dir),
        "pending": entries(bus.pending),
        "claimed": entries(bus.claimed),
        "completed_recent": entries(bus.completed)[-20:],
        "failed_recent": entries(bus.failed)[-20:],
        "waiting_verify": [path.stem for path in sorted(bus.pending_verify.glob("*.md"))],
        "verified": [path.stem for path in sorted(bus.verified.glob("*.md"))],
        "rework": [path.stem for path in sorted(bus.rework.glob("*.md"))],
    }
    payload["counts"] = {
        "pending": len(payload["pending"]),
        "claimed": len(payload["claimed"]),
        "completed_recent": len(payload["completed_recent"]),
        "failed_recent": len(payload["failed_recent"]),
        "waiting_verify": len(payload["waiting_verify"]),
        "verified": len(payload["verified"]),
        "rework": len(payload["rework"]),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def cmd_claim(bus: Bus, args: argparse.Namespace) -> int:
    bus.ensure()
    with bus.lock():
        candidates: list[tuple[str, Path, dict]] = []
        for path in bus.pending.glob("*.json"):
            try:
                payload = read_json(path)
                candidates.append((str(payload.get("created_at", "")), path, payload))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
        for _, path, payload in sorted(candidates):
            task_id = str(payload.get("task_id", ""))
            validate_id(task_id)
            package = Path(str(payload.get("package_path", ""))).expanduser()
            receipt = Path(str(payload.get("receipt_path", ""))).expanduser()
            if not package.is_file():
                error = f"任务包缺失: {package}"
                payload.update(status="FAILED", failed_at=now_iso(), error=error)
                target = bus.failed / path.name
                os.replace(path, target)
                atomic_json(target, payload)
                evidence = f"失败记录：{target}"
                bus.update_ledger(task_id, "FAILED", evidence)
                bus.append_review(task_id, str(payload.get("title", "")), "FAILED", evidence)
                continue
            if receipt.is_file() and receipt.stat().st_size > 0:
                payload.update(status="RECEIPT_EXISTS", receipt_path=str(receipt))
                target = bus.claimed / path.name
                os.replace(path, target)
                atomic_json(target, payload)
                payload["queue_file"] = str(target)
                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
                return 0
            payload.update(
                status="IN_PROGRESS",
                claimed_at=now_iso(),
                claimed_by=args.worker,
                attempt=int(payload.get("attempt", 0)) + 1,
            )
            target = bus.claimed / path.name
            os.replace(path, target)
            atomic_json(target, payload)
            payload["queue_file"] = str(target)
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
    print(json.dumps({"status": "EMPTY", "root": str(bus.root)}, ensure_ascii=False, indent=2))
    return 0


def declared_results(text: str, allowed: set[str]) -> list[str]:
    found: set[str] = set()
    result_line = re.compile(r"(?:最终结论|验收结论|结论)\s*[：:]")
    for line in text.splitlines():
        if not result_line.search(line):
            continue
        for result in allowed:
            if re.search(rf"(?<![A-Z_]){re.escape(result)}(?![A-Z_])", line):
                found.add(result)
    return sorted(found)


def compatible_result(text: str, requested: str | None, allowed: set[str], label: str) -> str:
    found = declared_results(text, allowed)
    if not found:
        found = [
            result
            for result in sorted(allowed)
            if re.search(rf"(?<![A-Z_]){re.escape(result)}(?![A-Z_])", text)
        ]
    if requested and requested not in allowed:
        raise ValueError(f"{label} 结论无效: {requested}")
    if len(found) > 1:
        raise ValueError(f"回执包含多个 {label} 结论: {', '.join(found)}")
    if requested and found and requested not in found:
        raise ValueError(f"参数结论 {requested} 与回执中的 {found[0]} 不一致")
    if requested and not found:
        raise ValueError(f"回执没有写明参数结论 {requested}")
    if not requested:
        if not found:
            raise ValueError(f"回执缺少 {label} 结论")
        return found[0]
    return requested


def write_candidate_result(
    metadata: dict,
    result: str,
    evidence: list[str],
    receipt: Path,
) -> None:
    marker = Path(str(metadata["marker_path"])).expanduser().resolve()
    values = {
        "ID": str(metadata["task_id"]),
        "TITLE": str(metadata["title"]),
        "FINAL_OWNER": "Codex",
        "CREATED": now_iso(),
        "RESULT": result,
        "NEXT_ACTION": "允许进入合并/发布评审；仍需用户授权与脱敏检查。"
        if result == "PASS"
        else "留在返工目录，由候选方或用户决定返工。",
        "EVIDENCE": bullet(evidence, "- 待补充：未提供实际复跑证据。"),
        "RECEIPT": f"- 候选请求入口：`{marker}`\n- 验证结果：`{receipt}`",
    }
    atomic_text(receipt, render("验证结果.md", values))


def cmd_complete(bus: Bus, args: argparse.Namespace) -> int:
    bus.ensure()
    validate_id(args.id)
    with bus.lock():
        claimed = bus.claimed / f"{args.id}.json"
        if claimed.is_file():
            payload = read_json(claimed)
            receipt = Path(args.receipt).expanduser().resolve() if args.receipt else Path(
                str(payload["receipt_path"])
            ).expanduser()
            if not receipt.is_file() or receipt.stat().st_size == 0:
                raise FileNotFoundError(f"回执不存在或为空，禁止完成: {receipt}")
            text = receipt.read_text(encoding="utf-8", errors="ignore")
            kind = str(payload.get("kind", "task"))
            if kind == "verification":
                result = compatible_result(text, args.result, WB_RESULTS, "WB")
            else:
                result = args.result or "COMPLETED"
            payload.update(
                status=result,
                completed_at=now_iso(),
                receipt_path=str(receipt),
                receipt_sha256=sha256_file(receipt),
            )
            target = bus.completed / claimed.name
            os.replace(claimed, target)
            atomic_json(target, payload)
            evidence = f"回执：{receipt}"
            updated = bus.update_ledger(args.id, result, evidence)
            review = bus.append_review(args.id, str(payload.get("title", "")), result, evidence)
            print(
                json.dumps(
                    {
                        "status": "COMPLETED",
                        "id": args.id,
                        "result": result,
                        "receipt": str(receipt),
                        "queue_file": str(target),
                        "ledger_updated": updated,
                        "review": str(review),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        marker = bus.pending_verify / f"{args.id}.md"
        metadata_path = bus.candidates / f"{args.id}.json"
        if marker.is_file() and metadata_path.is_file():
            metadata = read_json(metadata_path)
            candidate_dir = Path(str(metadata["candidate_dir"])).expanduser().resolve()
            receipt = Path(args.receipt).expanduser().resolve() if args.receipt else candidate_dir / "验证结果.md"
            if receipt.is_file() and receipt.stat().st_size > 0:
                result = compatible_result(
                    receipt.read_text(encoding="utf-8", errors="ignore"),
                    args.result,
                    CANDIDATE_RESULTS,
                    "候选",
                )
            elif args.result:
                if args.result not in CANDIDATE_RESULTS:
                    raise ValueError(f"候选结论无效: {args.result}")
                result = args.result
                if not args.evidence:
                    raise ValueError("候选 PASS/FAIL 必须提供实际复跑 --evidence")
                write_candidate_result(metadata, result, args.evidence, receipt)
            else:
                raise FileNotFoundError(f"验证结果不存在: {receipt}")
            destination = bus.verified if result == "PASS" else bus.rework
            target_marker = destination / marker.name
            if target_marker.exists():
                raise FileExistsError(f"目标验证入口已存在: {target_marker}")
            os.replace(marker, target_marker)
            metadata.update(
                status=result,
                verified_at=now_iso(),
                result_path=str(receipt),
                marker_path=str(target_marker),
            )
            atomic_json(metadata_path, metadata)
            evidence = f"验证结果：{receipt}"
            updated = bus.update_ledger(args.id, result, evidence)
            review = bus.append_review(args.id, str(metadata.get("title", "")), result, evidence)
            print(
                json.dumps(
                    {
                        "status": "VERIFIED" if result == "PASS" else "REWORK",
                        "id": args.id,
                        "result": result,
                        "result_path": str(receipt),
                        "ledger_updated": updated,
                        "review": str(review),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
        raise FileNotFoundError(f"领取队列和待验证入口中都没有任务: {args.id}")


def cmd_fail(bus: Bus, args: argparse.Namespace) -> int:
    bus.ensure()
    validate_id(args.id)
    with bus.lock():
        source = bus.claimed / f"{args.id}.json"
        if not source.is_file():
            raise FileNotFoundError(f"领取队列中不存在任务: {args.id}")
        payload = read_json(source)
        payload.update(status="FAILED", failed_at=now_iso(), error=args.error[:4000])
        target = bus.failed / source.name
        os.replace(source, target)
        atomic_json(target, payload)
        evidence = f"失败记录：{target}"
        updated = bus.update_ledger(args.id, "FAILED", evidence)
        review = bus.append_review(args.id, str(payload.get("title", "")), "FAILED", evidence)
    print(
        json.dumps(
            {
                "status": "FAILED",
                "id": args.id,
                "queue_file": str(target),
                "ledger_updated": updated,
                "review": str(review),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def add_common(parser: argparse.ArgumentParser, suppress_defaults: bool = False) -> None:
    default_root = argparse.SUPPRESS if suppress_defaults else os.environ.get("WB_BUS_HOME", ".wb-bus")
    default_ledger = argparse.SUPPRESS if suppress_defaults else None
    default_review = argparse.SUPPRESS if suppress_defaults else None
    parser.add_argument("--root", default=default_root, help="总线数据根目录")
    parser.add_argument("--ledger", default=default_ledger, help="共享台账路径；默认在 root/shared")
    parser.add_argument("--review-dir", default=default_review, help="固定复盘目录；默认在 root/shared")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Codex <-> WorkBuddy 文件任务总线")
    add_common(p)
    sub = p.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="初始化目录和台账")
    add_common(init, suppress_defaults=True)
    init.set_defaults(func=lambda bus, args: cmd_init(bus))

    status = sub.add_parser("status", help="只读查看总线状态")
    add_common(status, suppress_defaults=True)
    status.set_defaults(func=lambda bus, args: cmd_status(bus))

    dispatch = sub.add_parser("dispatch", help="创建 WB 执行任务")
    add_common(dispatch, suppress_defaults=True)
    dispatch.add_argument("--id", required=True)
    dispatch.add_argument("--title", required=True)
    dispatch.add_argument("--goal", required=True)
    dispatch.add_argument("--workbuddy", action="append", default=[])
    dispatch.add_argument("--codex", action="append", default=[])
    dispatch.add_argument("--input", action="append", default=[])
    dispatch.add_argument("--deliverable", action="append", default=[])
    dispatch.add_argument("--acceptance", action="append", default=[])
    dispatch.add_argument("--constraint", action="append", default=[])
    dispatch.set_defaults(func=cmd_dispatch)

    verify = sub.add_parser("verify", help="创建 WBV 验收包或登记 WBC 候选")
    add_common(verify, suppress_defaults=True)
    verify.add_argument("--id", required=True)
    verify.add_argument("--title", required=True)
    verify.add_argument("--goal")
    verify.add_argument("--changed-file", action="append", default=[])
    verify.add_argument("--cwd", default=str(Path.cwd()))
    verify.add_argument("--command", action="append", default=[])
    verify.add_argument("--evidence", action="append", default=[])
    verify.add_argument("--acceptance", action="append", default=[])
    verify.add_argument("--risk", action="append", default=[])
    verify.add_argument("--candidate-dir")
    verify.set_defaults(func=cmd_verify)

    claim = sub.add_parser("claim", help="原子领取最早任务")
    add_common(claim, suppress_defaults=True)
    claim.add_argument("--worker", default="workbuddy")
    claim.set_defaults(func=cmd_claim)

    complete = sub.add_parser("complete", help="凭回执/验证结果完成")
    add_common(complete, suppress_defaults=True)
    complete.add_argument("--id", required=True)
    complete.add_argument("--receipt")
    complete.add_argument("--result")
    complete.add_argument("--evidence", action="append", default=[])
    complete.set_defaults(func=cmd_complete)

    fail = sub.add_parser("fail", help="流程失败时移入 failed")
    add_common(fail, suppress_defaults=True)
    fail.add_argument("--id", required=True)
    fail.add_argument("--error", required=True)
    fail.set_defaults(func=cmd_fail)
    return p


def main() -> int:
    try:
        args = parser().parse_args()
        bus = Bus(args.root, args.ledger, args.review_dir)
        return args.func(bus, args)
    except (FileNotFoundError, FileExistsError, TimeoutError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
