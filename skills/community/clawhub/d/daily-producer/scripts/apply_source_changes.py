#!/usr/bin/env python3
"""
将用户确认的来源变更写入 config/profile.yaml，并标记审查完成。

读取 data/source_review_pending.json 中 confirmed: true 的变更：
- action: remove_suggestion → 从 sources.direct 移除对应 URL
- action: add_suggestion    → 将 add_url 追加到 sources.direct

采用字符串外科手术方式修改 profile.yaml，保留注释和格式。
操作完成后将 pending 文件的 reviewed 标记为 true。

用法：
    python3 scripts/apply_source_changes.py
    python3 scripts/apply_source_changes.py --dry-run   # 预览变更，不实际写入
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def resolve_root_dir() -> Path:
    env_root = os.environ.get("DAILY_ROOT") or os.environ.get("AI_DAILY_ROOT")
    candidates = []
    if env_root:
        candidates.append(Path(env_root).expanduser())

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "SKILL.md").exists() and (candidate / "config").is_dir():
            return candidate

    return script_dir.parent


def load_pending(pending_path: Path) -> dict:
    if not pending_path.exists():
        print(f"ERROR: pending 文件不存在: {pending_path}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(pending_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"ERROR: 读取 pending 文件失败: {e}", file=sys.stderr)
        sys.exit(1)


def extract_direct_urls_from_yaml(yaml_text: str) -> list[str]:
    """从 YAML 文本中提取 sources.direct 下的 URL 列表。"""
    urls = []
    in_direct = False
    for line in yaml_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "direct:":
            in_direct = True
            continue
        if in_direct:
            if stripped.startswith("- "):
                url = stripped[2:].strip().strip("'\"")
                if url:
                    urls.append(url)
            elif not stripped.startswith("#"):
                # 遇到非列表行，退出 direct 区域
                indent = len(line) - len(line.lstrip())
                if indent < 4:
                    in_direct = False
    return urls


def update_direct_section(yaml_text: str, new_urls: list[str]) -> str:
    """
    用外科手术方式替换 yaml_text 中 direct: 段落的内容。
    保留 direct: 行本身和之后其他字段，只替换列表条目。
    """
    lines = yaml_text.splitlines(keepends=True)
    result: list[str] = []
    in_direct = False
    direct_written = False

    for line in lines:
        stripped = line.strip()

        if stripped == "direct:":
            in_direct = True
            direct_written = False
            result.append(line)
            # 立即写入新 URL 列表
            for url in new_urls:
                result.append(f'    - "{url}"\n')
            direct_written = True
            continue

        if in_direct:
            if stripped.startswith("- ") and (len(line) - len(line.lstrip())) >= 4:
                # 跳过旧的列表条目
                continue
            else:
                # 离开 direct 区域
                in_direct = False
                result.append(line)
                continue

        result.append(line)

    return "".join(result)


def main() -> int:
    parser = argparse.ArgumentParser(description="将确认的来源变更写入 profile.yaml")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览变更内容，不实际写入文件",
    )
    args = parser.parse_args()

    root = resolve_root_dir()
    pending_path = root / "data" / "source_review_pending.json"
    profile_path = root / "config" / "profile.yaml"

    pending = load_pending(pending_path)

    if pending.get("reviewed"):
        print("INFO: 该审查已完成（reviewed: true），无需重复执行。")
        return 0

    if not profile_path.exists():
        print(f"ERROR: profile.yaml 不存在: {profile_path}", file=sys.stderr)
        return 1

    changes = pending.get("changes", [])
    confirmed_changes = [c for c in changes if c.get("confirmed") is True]

    if not confirmed_changes:
        print("INFO: 没有 confirmed: true 的变更，标记审查完成后退出。")
        if not args.dry_run:
            pending["reviewed"] = True
            pending["applied_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
            pending["applied_count"] = 0
            pending_path.write_text(
                json.dumps(pending, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        return 0

    yaml_text = profile_path.read_text(encoding="utf-8")
    current_urls = extract_direct_urls_from_yaml(yaml_text)

    # 收集需要移除和新增的 URL
    to_remove: set[str] = set()
    to_add: list[str] = []

    for change in confirmed_changes:
        action = change.get("action")
        if action == "remove_suggestion":
            url = change.get("url", "")
            if url:
                to_remove.add(url)
        elif action == "add_suggestion":
            add_url = change.get("add_url", "")
            if add_url and add_url not in current_urls:
                to_add.append(add_url)

    new_urls = [u for u in current_urls if u not in to_remove] + to_add

    # 打印预览
    if to_remove:
        print(f"移除 {len(to_remove)} 个来源:")
        for url in sorted(to_remove):
            print(f"  - {url}")
    if to_add:
        print(f"新增 {len(to_add)} 个来源:")
        for url in to_add:
            print(f"  + {url}")

    if args.dry_run:
        print("\n[dry-run] 未写入文件。")
        return 0

    updated_yaml = update_direct_section(yaml_text, new_urls)
    profile_path.write_text(updated_yaml, encoding="utf-8")
    print(f"profile.yaml 已更新: {profile_path}")

    # 标记审查完成
    pending["reviewed"] = True
    pending["applied_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    pending["applied_count"] = len(confirmed_changes)
    pending_path.write_text(
        json.dumps(pending, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"pending 文件已标记完成: {pending_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
