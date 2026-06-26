#!/usr/bin/env python3
"""Check and update cross-platform installed skills."""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PROVIDER_DIRS = (".claude", ".cursor", ".agents", ".codex", ".github", ".gemini", ".opencode", ".openclaw")


@dataclasses.dataclass
class UpdateReport:
    provider_root: str
    skill_name: str
    source_type: str
    source_url: str
    status: str
    current_ref_or_hash: str
    latest_ref_or_hash: str
    message: str
    local_path: str = ""
    meta: dict[str, object] = dataclasses.field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)


def run_git(repo: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        text=True,
        capture_output=True,
    )


def git_output(repo: Path, args: list[str], check: bool = True) -> str:
    result = run_git(repo, args, check=check)
    if not check and result.returncode != 0:
        return ""
    return result.stdout.strip()


def provider_root_candidates(base: Path) -> list[Path]:
    candidates = [(base / name).resolve() for name in PROVIDER_DIRS]
    candidates.append((base / ".openclaw" / "workspace").resolve())
    return candidates


def default_provider_roots(workspace_root: Path | str | None = None, home_root: Path | str | None = None) -> list[Path]:
    workspace = Path(workspace_root or Path.cwd()).resolve()
    home = Path(home_root or Path.home()).resolve()
    seen: set[Path] = set()
    results: list[Path] = []
    for base in (workspace, home):
        for candidate in provider_root_candidates(base):
            if candidate in seen:
                continue
            if (candidate / "skills").exists() or (candidate / ".skill-lock.json").exists():
                seen.add(candidate)
                results.append(candidate)
    return results


def infer_provider_root(skill_path: Path) -> Path:
    for parent in skill_path.parents:
        if parent.name != "skills":
            continue
        provider_root = parent.parent
        if provider_root.name in PROVIDER_DIRS:
            return provider_root
        if provider_root.name == "workspace" and provider_root.parent.name == ".openclaw":
            return provider_root
    return skill_path.parent


def find_git_root(path: Path) -> Path | None:
    result = run_git(path, ["rev-parse", "--show-toplevel"], check=False)
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def current_branch(repo_root: Path) -> str:
    return git_output(repo_root, ["symbolic-ref", "--quiet", "--short", "HEAD"], check=False)


def exact_tag(repo_root: Path) -> str:
    return git_output(repo_root, ["describe", "--tags", "--exact-match"], check=False)


def latest_tag(repo_root: Path) -> str:
    tags = git_output(repo_root, ["tag", "--sort=-version:refname"]).splitlines()
    return next((tag for tag in tags if tag.strip()), "")


def remote_url(repo_root: Path) -> str:
    return git_output(repo_root, ["remote", "get-url", "origin"], check=False)


def is_dirty(repo_root: Path) -> bool:
    return bool(git_output(repo_root, ["status", "--porcelain"]))


def upstream_branch(repo_root: Path, branch: str) -> str:
    upstream = git_output(repo_root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], check=False)
    return upstream or f"origin/{branch}"


def fetch_origin(repo_root: Path) -> None:
    run_git(repo_root, ["fetch", "--tags", "--prune", "origin"])


def normalize_source_id(source_url: str) -> str:
    if source_url.endswith(".git"):
        source_url = source_url[:-4]
    for prefix in ("https://github.com/", "git@github.com:", "ssh://git@github.com/"):
        if source_url.startswith(prefix):
            return source_url[len(prefix) :]
    return source_url


def inspect_git_skill(skill_path: Path | str, fetch: bool = True) -> UpdateReport:
    skill = Path(skill_path).resolve()
    provider_root = infer_provider_root(skill)
    if not (skill / "SKILL.md").exists():
        return UpdateReport(str(provider_root), skill.name, "git", "", "unsupported", "", "", "目录缺少 SKILL.md。", str(skill))
    repo_root = find_git_root(skill)
    if not repo_root:
        return UpdateReport(str(provider_root), skill.name, "git", "", "unsupported", "", "", "目录不在 git 仓库内。", str(skill))

    source = remote_url(repo_root)
    if not source:
        return UpdateReport(str(provider_root), skill.name, "git", "", "unsupported", "", "", "仓库缺少 origin 远端。", str(skill))

    if fetch:
        try:
            fetch_origin(repo_root)
        except subprocess.CalledProcessError as exc:
            detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
            return UpdateReport(str(provider_root), skill.name, "git", source, "unsupported", "", "", f"获取 origin 失败：{detail}", str(skill))

    branch = current_branch(repo_root)
    tag = exact_tag(repo_root)
    if tag and not branch:
        latest = latest_tag(repo_root)
        if not latest:
            return UpdateReport(str(provider_root), skill.name, "git", source, "unsupported", tag, "", "未找到任何远端 tags。", str(skill))
        status = "dirty" if is_dirty(repo_root) else ("update-available" if tag != latest else "up-to-date")
        message = {
            "dirty": "仓库存在未提交改动，默认不更新。",
            "update-available": "存在更新的 tag。",
            "up-to-date": "已是最新 tag。",
        }[status]
        return UpdateReport(
            str(provider_root),
            skill.name,
            "git",
            source,
            status,
            tag,
            latest,
            message,
            str(skill),
            meta={"repo_root": str(repo_root), "tracking": "tag"},
        )

    if not branch:
        return UpdateReport(
            str(provider_root),
            skill.name,
            "git",
            source,
            "unsupported",
            git_output(repo_root, ["rev-parse", "HEAD"]),
            "",
            "当前仓库处于 detached HEAD 且没有精确 tag，无法安全判断更新策略。",
            str(skill),
            meta={"repo_root": str(repo_root), "tracking": "detached"},
        )

    upstream = upstream_branch(repo_root, branch)
    current_ref = git_output(repo_root, ["rev-parse", "HEAD"])
    latest_ref = git_output(repo_root, ["rev-parse", upstream], check=False)
    if not latest_ref:
        return UpdateReport(
            str(provider_root),
            skill.name,
            "git",
            source,
            "unsupported",
            current_ref,
            "",
            f"找不到上游分支 {upstream}。",
            str(skill),
            meta={"repo_root": str(repo_root), "tracking": "branch"},
        )

    behind_count = int(git_output(repo_root, ["rev-list", "--count", f"HEAD..{upstream}"]))
    ahead_count = int(git_output(repo_root, ["rev-list", "--count", f"{upstream}..HEAD"]))
    dirty = is_dirty(repo_root)
    if dirty:
        status = "dirty"
        message = "仓库存在未提交改动，默认不更新。"
    elif behind_count > 0 and ahead_count == 0:
        status = "update-available"
        message = "远端分支有新提交。"
    elif ahead_count > 0 and behind_count == 0:
        status = "ahead"
        message = "本地提交领先远端，跳过自动更新。"
    elif behind_count > 0 and ahead_count > 0:
        status = "diverged"
        message = "本地与远端已分叉，跳过自动更新。"
    else:
        status = "up-to-date"
        message = "已是最新。"

    return UpdateReport(
        str(provider_root),
        skill.name,
        "git",
        source,
        status,
        current_ref,
        latest_ref,
        message,
        str(skill),
        meta={
            "repo_root": str(repo_root),
            "tracking": "branch",
            "behind_count": behind_count,
            "ahead_count": ahead_count,
        },
    )


def update_git_skill(skill_path: Path | str) -> UpdateReport:
    report = inspect_git_skill(skill_path, fetch=True)
    repo_root = Path(report.meta.get("repo_root", report.local_path or "."))
    tracking = report.meta.get("tracking")
    if report.status in {"unsupported", "dirty", "ahead", "diverged", "up-to-date"}:
        return report
    if tracking == "branch":
        branch = current_branch(repo_root)
        run_git(repo_root, ["pull", "--ff-only", "origin", branch])
    elif tracking == "tag":
        run_git(repo_root, ["checkout", report.latest_ref_or_hash])
    refreshed = inspect_git_skill(skill_path, fetch=False)
    return dataclasses.replace(
        refreshed,
        status="updated",
        message=f"已更新到 {refreshed.latest_ref_or_hash or refreshed.current_ref_or_hash}。",
    )


def git_blob_hash(data: bytes) -> bytes:
    return hashlib.sha1(f"blob {len(data)}".encode() + b"\0" + data).digest()


def git_tree_hash(path: Path) -> str:
    entries: list[tuple[str, str, bytes]] = []
    for child in sorted(path.iterdir(), key=lambda p: p.name):
        if child.name == ".DS_Store":
            continue
        if child.is_symlink():
            target = os.readlink(child)
            entries.append(("120000", child.name, git_blob_hash(target.encode())))
        elif child.is_dir():
            entries.append(("40000", child.name, bytes.fromhex(git_tree_hash(child))))
        elif child.is_file():
            entries.append(("100644", child.name, git_blob_hash(child.read_bytes())))
    payload = b"".join(f"{mode} {name}".encode() + b"\0" + sha for mode, name, sha in entries)
    return hashlib.sha1(f"tree {len(payload)}".encode() + b"\0" + payload).hexdigest()


def clone_source(source_url: str, cache_root: Path) -> Path:
    repo_dir = cache_root / hashlib.sha1(source_url.encode()).hexdigest()
    if repo_dir.exists():
        run_git(repo_dir, ["fetch", "--tags", "--prune", "origin"])
        return repo_dir
    subprocess.run(
        ["git", "clone", "--depth=1", source_url, str(repo_dir)],
        check=True,
        text=True,
        capture_output=True,
    )
    return repo_dir


def resolve_local_skill_path(provider_root: Path, skill_path: str) -> Path:
    path = Path(skill_path)
    if path.is_absolute():
        return path
    anchor = provider_root.parent if provider_root.name.startswith(".") else provider_root
    return (anchor / path).resolve()


def load_lockfile(provider_root: Path) -> dict | None:
    lock_path = provider_root / ".skill-lock.json"
    if not lock_path.exists():
        return None
    return json.loads(lock_path.read_text(encoding="utf-8"))


def inspect_lockfile_provider(provider_root: Path | str, cache_root: Path | None = None) -> list[UpdateReport]:
    provider = Path(provider_root).resolve()
    lock = load_lockfile(provider)
    if not lock:
        return []
    cache_base = cache_root or Path(tempfile.mkdtemp(prefix="skill-updater-"))
    reports: list[UpdateReport] = []
    grouped: dict[str, Path] = {}
    clone_errors: dict[str, str] = {}
    for skill_name, entry in sorted(lock.get("skills", {}).items()):
        source_url = entry.get("sourceUrl", "")
        skill_path = entry.get("skillPath")
        locked_hash = entry.get("skillFolderHash", "")
        if not source_url or not skill_path or not locked_hash:
            reports.append(
                UpdateReport(
                    str(provider),
                    skill_name,
                    "lockfile",
                    source_url,
                    "lock-invalid",
                    "",
                    "",
                    "锁文件缺少必要字段。",
                    meta={"source": entry.get("source", "")},
                )
            )
            continue

        local_skill = resolve_local_skill_path(provider, skill_path).parent
        if not local_skill.exists():
            reports.append(
                UpdateReport(
                    str(provider),
                    skill_name,
                    "lockfile",
                    source_url,
                    "missing-local-skill",
                    locked_hash,
                    "",
                    "本地 skill 目录不存在。",
                    str(local_skill),
                    meta={"source": entry.get("source", "")},
                )
            )
            continue

        local_hash = git_tree_hash(local_skill)
        if local_hash != locked_hash:
            reports.append(
                UpdateReport(
                    str(provider),
                    skill_name,
                    "lockfile",
                    source_url,
                    "modified-locally",
                    locked_hash,
                    "",
                    "本地 skill 与锁文件记录不一致，跳过自动更新。",
                    str(local_skill),
                    meta={"source": entry.get("source", "")},
                )
            )
            continue

        if source_url not in grouped and source_url not in clone_errors:
            try:
                grouped[source_url] = clone_source(source_url, cache_base)
            except subprocess.CalledProcessError as exc:
                detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
                clone_errors[source_url] = detail
        if source_url in clone_errors:
            reports.append(
                UpdateReport(
                    str(provider),
                    skill_name,
                    "lockfile",
                    source_url,
                    "update-failed",
                    locked_hash,
                    "",
                    f"获取来源失败：{clone_errors[source_url]}",
                    str(local_skill),
                    meta={"source": entry.get("source", "")},
                )
            )
            continue
        repo_dir = grouped[source_url]
        remote_tree_path = str(Path(skill_path).parent).replace("\\", "/")
        latest_hash = git_output(repo_dir, ["rev-parse", f"HEAD:{remote_tree_path}"], check=False)
        if not latest_hash:
            reports.append(
                UpdateReport(
                    str(provider),
                    skill_name,
                    "lockfile",
                    source_url,
                    "missing-source",
                    locked_hash,
                    "",
                    "远端仓库中不存在该 skill 目录。",
                    str(local_skill),
                    meta={"source": entry.get("source", "")},
                )
            )
            continue

        status = "update-available" if latest_hash != locked_hash else "up-to-date"
        message = "远端 skill 有更新。" if status == "update-available" else "已是最新。"
        reports.append(
            UpdateReport(
                str(provider),
                skill_name,
                "lockfile",
                source_url,
                status,
                locked_hash,
                latest_hash,
                message,
                str(local_skill),
                meta={"source": entry.get("source", "")},
            )
        )
    return reports


def backup_provider(provider_root: Path, skill_names: list[str]) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_base = Path(tempfile.gettempdir()) / f"skill-updater-backup-{provider_root.name.strip('.')}-{stamp}"
    backup_dir = backup_base / "payload"
    backup_dir.mkdir(parents=True)
    lock_path = provider_root / ".skill-lock.json"
    if lock_path.exists():
        shutil.copy2(lock_path, backup_dir / ".skill-lock.json")
    for name in skill_names:
        src = provider_root / "skills" / name
        if src.exists():
            shutil.copytree(src, backup_dir / name)
    archive = backup_base.with_suffix(".tar.gz")
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(backup_dir, arcname="payload")
    return archive


def update_lockfile_provider(provider_root: Path | str, cache_root: Path | None = None) -> list[UpdateReport]:
    provider = Path(provider_root).resolve()
    lock_path = provider / ".skill-lock.json"
    lock = load_lockfile(provider)
    if not lock:
        return []
    reports = inspect_lockfile_provider(provider, cache_root=cache_root)
    update_targets = [r for r in reports if r.status == "update-available"]
    if not update_targets:
        return reports

    backup_archive = backup_provider(provider, [r.skill_name for r in update_targets])
    data = json.loads(lock_path.read_text(encoding="utf-8"))
    cache_base = cache_root or Path(tempfile.mkdtemp(prefix="skill-updater-"))
    source_cache: dict[str, Path] = {}
    clone_errors: dict[str, str] = {}
    updated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rewritten: list[UpdateReport] = []

    by_key = {(r.provider_root, r.skill_name): r for r in reports}
    for skill_name, entry in sorted(data.get("skills", {}).items()):
        report = by_key.get((str(provider), skill_name))
        if not report or report.status != "update-available":
            if report:
                rewritten.append(report)
            continue
        source_url = entry["sourceUrl"]
        if source_url not in source_cache and source_url not in clone_errors:
            try:
                source_cache[source_url] = clone_source(source_url, cache_base)
            except subprocess.CalledProcessError as exc:
                detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
                clone_errors[source_url] = detail
        if source_url in clone_errors:
            rewritten.append(
                dataclasses.replace(
                    report,
                    status="update-failed",
                    message=f"获取来源失败：{clone_errors[source_url]}",
                )
            )
            continue
        repo_dir = source_cache[source_url]
        local_skill = resolve_local_skill_path(provider, entry["skillPath"]).parent
        source_skill = repo_dir / Path(entry["skillPath"]).parent
        if local_skill.exists():
            shutil.rmtree(local_skill)
        shutil.copytree(source_skill, local_skill)
        entry["skillFolderHash"] = report.latest_ref_or_hash
        entry["updatedAt"] = updated_at
        rewritten.append(
            dataclasses.replace(
                report,
                status="updated",
                current_ref_or_hash=report.latest_ref_or_hash,
                message=f"已更新，备份位于 {backup_archive}。",
            )
        )

    with lock_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return rewritten


def discover_skill_dirs(provider_root: Path) -> list[Path]:
    skills_dir = provider_root / "skills"
    if not skills_dir.exists():
        return []
    return sorted(candidate for candidate in skills_dir.iterdir() if candidate.is_dir() and (candidate / "SKILL.md").exists())


def report_matches_source(report: UpdateReport, filters: list[str]) -> bool:
    if not filters:
        return True
    candidates = [
        report.source_url,
        normalize_source_id(report.source_url),
        str(report.meta.get("source", "")),
    ]
    return any(token and any(token in candidate for candidate in candidates if candidate) for token in filters)


def collect_reports(
    command: str,
    provider_roots: list[Path],
    source_filters: list[str] | None = None,
    cache_root: Path | None = None,
) -> list[UpdateReport]:
    filters = source_filters or []
    reports: list[UpdateReport] = []
    for provider_root in provider_roots:
        provider = provider_root.resolve()
        lock_reports = inspect_lockfile_provider(provider, cache_root=cache_root)
        lock_skill_names = {report.skill_name for report in lock_reports}
        if command == "update":
            reports.extend(report for report in update_lockfile_provider(provider, cache_root=cache_root) if report_matches_source(report, filters))
        else:
            reports.extend(report for report in lock_reports if report_matches_source(report, filters))

        for skill_dir in discover_skill_dirs(provider):
            if skill_dir.name in lock_skill_names:
                continue
            report = update_git_skill(skill_dir) if command == "update" else inspect_git_skill(skill_dir)
            if report_matches_source(report, filters):
                reports.append(report)
    return reports


def render_text(reports: list[UpdateReport]) -> str:
    lines: list[str] = []
    for report in reports:
        lines.append(f"[{report.status}] {report.skill_name}")
        lines.append(f"  provider_root={report.provider_root}")
        lines.append(f"  source_type={report.source_type} current={report.current_ref_or_hash or '-'} latest={report.latest_ref_or_hash or '-'}")
        if report.source_url:
            lines.append(f"  source={report.source_url}")
        if report.local_path:
            lines.append(f"  local_path={report.local_path}")
        if report.message:
            lines.append(f"  note={report.message}")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check and update skills installed from git or lockfiles.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "update"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--json", action="store_true", help="Print JSON output.")
        sub.add_argument("--source", action="append", default=[], help="Filter by source id or source URL.")
        sub.add_argument("--path", action="append", default=[], help="Provider root or skills directory to scan.")
    return parser.parse_args(argv)


def normalize_paths(path_args: list[str]) -> list[Path]:
    if not path_args:
        return default_provider_roots()
    paths: list[Path] = []
    for value in path_args:
        candidate = Path(value).expanduser().resolve()
        if candidate.name == "skills":
            paths.append(candidate.parent)
        elif (candidate / "skills").exists() or (candidate / ".skill-lock.json").exists():
            paths.append(candidate)
        elif (candidate / "SKILL.md").exists():
            paths.append(infer_provider_root(candidate))
        else:
            paths.append(candidate)
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            result.append(path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    provider_roots = normalize_paths(args.path)
    with tempfile.TemporaryDirectory(prefix="skill-updater-cache-") as temp:
        reports = collect_reports(args.command, provider_roots, source_filters=args.source, cache_root=Path(temp))
    if args.json:
        print(json.dumps([report.to_dict() for report in reports], indent=2, ensure_ascii=False))
    else:
        print(render_text(reports))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
