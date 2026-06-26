#!/usr/bin/env python3
"""
Feishu Wiki → Obsidian Sync (feishu-sync-obsidian)

纯路径构建 + 文件写入工具。
内容获取由 Agent 通过 feishu_fetch_doc 工具完成，脚本不直接调用飞书 API。

从 vault 根目录的 SYNC-RULES.md 读取数据源配置，
保留飞书 Wiki 的目录层级结构，增量同步（按 feishu_doc_token 去重）。

Usage:
    # Step A：节点遍历（脚本只返回待写入列表，不调用 API）
    echo '[{"title":"...","obj_token":"...","obj_type":"docx","node_token":"...",
          "parent_node_token":"...","wiki_name":"个人成长","space_id":"..."}]' \
      | python3 sync.py --stdin --plan

    # Step B：内容写入（Agent fetch 完内容后，再次调用于写入）
    echo '[{"title":"...","obj_token":"...","content":"..."}]' \
      | python3 sync.py --stdin --write [--dry-run]

Environment:
    VAULT_DIR   - Obsidian vault 路径（默认：/home/ink/个人知识库）
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── 路径配置 ──────────────────────────────────────────────────────────────
VAULT_DIR  = Path(os.environ.get("VAULT_DIR", "/home/ink/个人知识库"))
CACHE_DIR  = Path("/tmp/feishu-sync-obsidian")
SYNC_RULES = VAULT_DIR / "SYNC-RULES.md"

# ── 缓存 ─────────────────────────────────────────────────────────────────
_config_cache: Optional[Tuple[List[Tuple[str, str, str]], Dict[str, str]]] = None


# ── lark-table → Markdown ─────────────────────────────────────────────────

def convert_lark_tables(text: str) -> str:
    """将飞书 <lark-table> 标签转换为 Markdown 表格。"""
    def replace_table(match):
        table_content = match.group(0)
        rows_content: List[List[str]] = []

        for row_match in re.finditer(r'<lark-tr>(.*?)</lark-tr>', table_content, re.DOTALL):
            row_text = row_match.group(1)
            cells: List[str] = []
            for cell_match in re.finditer(r'<lark-td>(.*?)</lark-td>', row_text, re.DOTALL):
                cell = cell_match.group(1)
                # 字面 \n（反斜杠+n）→ 空格（飞书 API 编码的换行）
                cell = re.sub(r'\\+n', ' ', cell)
                # 移除所有 HTML 标签
                cell = re.sub(r'<[^>]+>', '', cell)
                cell = cell.strip()
                cells.append(cell)
            if cells:
                rows_content.append(cells)

        if not rows_content:
            return ""

        md_lines = []
        for i, row in enumerate(rows_content):
            md_lines.append("| " + " | ".join(row) + " |")
            if i == 0:
                md_lines.append("| " + " | ".join(["---"] * len(row)) + " |")

        return "\n".join(md_lines)

    return re.sub(r'<lark-table[^>]*>.*?</lark-table>', replace_table, text, flags=re.DOTALL)


# ── SYNC-RULES.md 解析 ──────────────────────────────────────────────────

def _parse_sync_rules() -> Tuple[List[Tuple[str, str, str]], Dict[str, str]]:
    """解析 vault/SYNC-RULES.md，提取数据源配置。"""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    if not SYNC_RULES.exists():
        print(f"[WARN] SYNC-RULES.md not found at {SYNC_RULES}", file=sys.stderr)
        _config_cache = ([], {})
        return _config_cache

    text = SYNC_RULES.read_text(encoding="utf-8")
    wiki_spaces: List[Tuple[str, str, str]] = []
    fallback_map: Dict[str, str] = {}
    in_datasource_section = False

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("##"):
            in_datasource_section = "数据源" in stripped
            continue
        if not in_datasource_section:
            continue
        if not stripped.startswith("|") or stripped.startswith("|---") or stripped.startswith("| Wiki"):
            continue
        parts = [p.strip() for p in stripped.split("|")]
        if len(parts) < 4:
            continue
        wiki_name, space_id, target_path = parts[1], parts[2], parts[3]
        if wiki_name and space_id and target_path:
            wiki_spaces.append((wiki_name, space_id, target_path))

    if not wiki_spaces:
        print(f"[WARN] No data source found in SYNC-RULES.md", file=sys.stderr)
        _config_cache = ([], {})
        return _config_cache

    _config_cache = (wiki_spaces, fallback_map)
    return wiki_spaces, fallback_map


def get_wiki_spaces() -> List[Tuple[str, str, str]]:
    return _parse_sync_rules()[0]


# ── 路径构建 ───────────────────────────────────────────────────────────────

def sanitize_filename(title: str, suffix: str = "") -> str:
    """标题转为安全文件名。"""
    s = re.sub(r'[\\/:*?"<>|]', "", title)
    s = re.sub(r'\s+', "-", s.strip())
    if suffix:
        max_len = 80 - len(suffix) - 1
        s = s[:max_len] + suffix
    return s + ".md"


def build_path_from_nodes(
    node: dict,
    wiki_name: str,
    token_to_info: Dict[str, Tuple[str, str]],
    parent_of: Dict[str, bool]
) -> Tuple[str, str]:
    """
    根据节点及其父节点链，构建 Obsidian 中的完整相对路径。

    返回 (relative_path, filename)
    - relative_path: wiki_name/父节点1/父节点2/...
    - filename: 当前节点文件名

    冲突处理：has_child=true 且 obj_type=docx 的节点，
    文件名加 _index 后缀，避免「软考笔记/软考笔记.md」歧义。
    """
    node_token = node.get("node_token", "")
    parent_token = node.get("parent_node_token", "")
    title = node.get("title", "未命名")

    is_container_with_content = (
        parent_of.get(node_token, False) and node.get("obj_type") == "docx"
    )

    path_parts: List[str] = []
    current_token = node_token
    visited: set = set()

    while current_token:
        if current_token in visited:
            break
        visited.add(current_token)

        if current_token == node_token:
            path_parts.append(sanitize_filename(title).replace(".md", ""))
            current_token = parent_token
        else:
            if current_token in token_to_info:
                parent_title, _ = token_to_info[current_token]
                path_parts.append(sanitize_filename(parent_title).replace(".md", ""))
                _, current_parent = token_to_info[current_token]
                current_token = current_parent
            else:
                break

    path_parts.reverse()
    parent_parts = path_parts[:-1]
    relative = wiki_name + ("/" + "/".join(parent_parts) if parent_parts else "")
    filename = (
        sanitize_filename(title, "_index")
        if is_container_with_content
        else sanitize_filename(title)
    )
    return relative, filename


# ── Obsidian 写入 ─────────────────────────────────────────────────────────

def ensure_obsidian_folder(relative_path: str) -> Path:
    dest_dir = VAULT_DIR / relative_path
    dest_dir.mkdir(parents=True, exist_ok=True)
    return dest_dir


def build_frontmatter(doc_token: str, node_token: str, wiki_name: str,
                      date: Optional[str] = None) -> str:
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    return f"""---
date: {date}
lastmod: {date}
draft: false
categories: []
tags: [来源/飞书同步]
feishu_doc_token: {doc_token}
feishu_wiki: {wiki_name}
feishu_node_token: {node_token}
---"""


def find_existing_by_doc_token(doc_token: str) -> Optional[Path]:
    """按 feishu_doc_token 查重（排除 .trash）。"""
    if not doc_token:
        return None
    for md_file in VAULT_DIR.rglob("*.md"):
        if '.trash' in md_file.parts:
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
            if not text.startswith("---"):
                continue
            end = text.find("\n---", 3)
            if end < 0:
                continue
            for fline in text[3:end].splitlines():
                if fline.strip().startswith("feishu_doc_token:"):
                    if fline.split(":", 1)[1].strip() == doc_token:
                        return md_file
        except Exception:
            continue
    return None


def write_obsidian_file(relative_path: str, filename: str, title: str, content: str,
                        doc_token: str, node_token: str, wiki_name: str,
                        dry_run: bool = False) -> Optional[str]:
    """写入 Obsidian 文件，返回路径（已存在则返回 None）。"""
    content = convert_lark_tables(content)

    existing = find_existing_by_doc_token(doc_token)
    if existing:
        print(f"  [SKIP] {title} → 已存在 ({existing.name})")
        return None

    dest_dir = ensure_obsidian_folder(relative_path)
    dest_path = dest_dir / filename

    counter = 1
    while dest_path.exists() and counter < 100:
        base, ext = filename.rsplit(".", 1)
        dest_path = dest_dir / f"{base}-{counter}.{ext}"
        counter += 1

    if dry_run:
        print(f"  [DRY-RUN] {title} → {relative_path}/{filename}")
        return str(dest_path)

    frontmatter = build_frontmatter(doc_token, node_token, wiki_name)
    dest_path.write_text(f"{frontmatter}\n\n{content}", encoding="utf-8")
    print(f"  [SYNCED] {title} → {relative_path}/{dest_path.name}")
    return str(dest_path)


# ── 两种运行模式 ───────────────────────────────────────────────────────────

def mode_plan(nodes: List[dict]):
    """
    模式A：分析节点，返回待写入文件列表（plan）。
    Agent 根据此列表决定 fetch 哪些文档。
    """
    wiki_spaces = get_wiki_spaces()
    if not wiki_spaces:
        print("[ERROR] No wiki spaces in SYNC-RULES.md", file=sys.stderr)
        sys.exit(1)

    space_id_to_info: Dict[str, Tuple[str, str]] = {
        sid: (name, path) for name, sid, path in wiki_spaces
    }
    token_to_info: Dict[str, Tuple[str, str]] = {}
    for n in nodes:
        if n.get("node_token"):
            token_to_info[n["node_token"]] = (n.get("title", "未命名"), n.get("parent_node_token", ""))

    parent_of: Dict[str, bool] = {}
    for n in nodes:
        if n.get("parent_node_token"):
            parent_of[n["parent_node_token"]] = True

    todo: List[dict] = []
    for node in nodes:
        obj_type = node.get("obj_type", "")
        obj_token = node.get("obj_token", "")
        wiki_name = node.get("wiki_name", "")
        space_id = node.get("space_id", "")
        node_token = node.get("node_token", "")

        if space_id and space_id in space_id_to_info:
            resolved_wiki_name, target_path = space_id_to_info[space_id]
        elif wiki_name:
            resolved_wiki_name, target_path = wiki_name, None
            for name, sid, path in wiki_spaces:
                if name == wiki_name:
                    target_path = path
                    break
            if target_path is None:
                continue
        else:
            continue

        # relative_path = target_path/父节点链/当前节点
        # build_path_from_nodes 返回的是 wiki_name/父节点/...，需拼 target_path 前缀
        relative_no_target, filename = build_path_from_nodes(node, resolved_wiki_name, token_to_info, parent_of)
        relative = (
            (target_path + "/" + relative_no_target)
            if relative_no_target
            else target_path
        )

        if obj_type != "docx":
            todo.append({
                "title": node.get("title", "未命名"),
                "obj_token": obj_token,
                "obj_type": obj_type,
                "node_token": node_token,
                "wiki_name": resolved_wiki_name,
                "relative_path": relative,
                "filename": filename,
                "need_fetch": False,
                "content": f"[飞书 {obj_type} 文档](https://vcndmev90kwz.feishu.cn/wiki/{node_token})"
            })
        else:
            todo.append({
                "title": node.get("title", "未命名"),
                "obj_token": obj_token,
                "obj_type": obj_type,
                "node_token": node_token,
                "wiki_name": resolved_wiki_name,
                "relative_path": relative,
                "filename": filename,
                "need_fetch": True
            })

    # 输出 plan JSON
    plan = {
        "wiki_spaces": [{"name": n, "sid": s, "path": p} for n, s, p in wiki_spaces],
        "total_nodes": len(nodes),
        "need_fetch": [t for t in todo if t.get("need_fetch")],
        "no_fetch_needed": [t for t in todo if not t.get("need_fetch")],
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    # 同步状态缓存
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    (CACHE_DIR / "plan.json").write_text(
        json.dumps({"todo": todo, "timestamp": datetime.now().isoformat()}, ensure_ascii=False, indent=2)
    )


def mode_write(nodes: List[dict], dry_run: bool = False):
    """
    模式B：写入文件（Agent fetch 完内容后调用）。
    nodes 格式：[{"title":"...","obj_token":"...","content":"...",
                  "node_token":"...","wiki_name":"...","relative_path":"...","filename":"..."}]
    """
    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Feishu → Obsidian Write")
    print(f"Vault: {VAULT_DIR}")
    print()

    todo = json.loads((CACHE_DIR / "plan.json").read_text())["todo"]
    todo_map: Dict[str, dict] = {t["obj_token"]: t for t in todo}

    all_synced, skipped, failed = [], 0, []

    for node in nodes:
        title = node.get("title", "未命名")
        obj_token = node.get("obj_token", "")
        content = node.get("content", "")
        node_token = node.get("node_token", "")
        wiki_name = node.get("wiki_name", "")
        relative_path = node.get("relative_path", wiki_name)
        filename = node.get("filename", sanitize_filename(title))

        if not content:
            skipped += 1
            continue

        try:
            path = write_obsidian_file(
                relative_path, filename, title, content,
                obj_token, node_token, wiki_name,
                dry_run=dry_run
            )
            if path:
                all_synced.append(path)
            else:
                skipped += 1
        except Exception as e:
            print(f"  [ERROR] {title} → {e}")
            failed.append((title, str(e)))

    print(f"\n[OK] {len(all_synced)} written, {skipped} skipped, {len(failed)} failed.")
    if failed:
        for ftitle, err in failed:
            print(f"  - {ftitle}: {err}")
    if dry_run:
        print("(dry run - no files written)")


def main_stdin():
    """解析命令行参数，从 stdin 读取 JSON。"""
    dry_run = "--dry-run" in sys.argv
    if "--plan" in sys.argv:
        mode_plan(json.loads(sys.stdin.read()))
    elif "--write" in sys.argv:
        mode_write(json.loads(sys.stdin.read()), dry_run=dry_run)
    else:
        print("[ERROR] 缺少模式参数：--plan（分析） 或 --write（写入）", file=sys.stderr)
        print("示例：echo '[...]' | python3 sync.py --stdin --plan", file=sys.stderr)
        print("示例：echo '[...]' | python3 sync.py --stdin --write", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if "--stdin" in sys.argv:
        main_stdin()
    else:
        print("[ERROR] 请使用 --stdin 模式", file=sys.stderr)
        print("示例：echo '[...]' | python3 sync.py --stdin --plan", file=sys.stderr)
        sys.exit(1)
