from __future__ import annotations

import json
from pathlib import Path

import gitea_api as g
import kb_schema as schema

COMMON_MODULE_VERSION = "paperkb-v3.0"
EMPTY = {"documents": [], "concepts": [], "resources": [], "people": [], "projects": [], "reviews": [], "imports": []}


def read(owner: str, repo: str) -> dict:
    result = g.get_file(owner, repo, "catalog.json")
    if not result:
        return json.loads(json.dumps(EMPTY))
    try:
        data = json.loads(result[0])
    except json.JSONDecodeError:
        data = json.loads(json.dumps(EMPTY))
    for key in EMPTY:
        data.setdefault(key, [])
    return data


def write(owner: str, repo: str, data: dict) -> None:
    g.put_file(owner, repo, "catalog.json", json.dumps(data, ensure_ascii=False, indent=2), "paper-kb: update catalog")


def upsert_document(cat: dict, entry: dict) -> bool:
    docs = cat.setdefault("documents", [])
    for i, old in enumerate(docs):
        same_source = entry.get("source_id") and old.get("source_id") == entry.get("source_id") and old.get("source_path") == entry.get("source_path")
        same_title = old.get("title") == entry.get("title") and old.get("type_key") == entry.get("type_key")
        if same_source or same_title:
            docs[i] = entry
            return True
    docs.append(entry)
    return False


def regen_index(owner: str, repo: str, title: str, cat: dict) -> None:
    lines = [f"# {title}", "", "## 文档", ""]
    for key, meta in schema.DOC_TYPES.items():
        group = [d for d in cat.get("documents", []) if d.get("type_key") == key]
        if not group:
            continue
        lines += [f"### {meta['cn']}"]
        for doc in group:
            stem = Path(doc.get("file", "")).stem
            lines.append(f"- [[{stem}]] — {doc.get('brief', '')}")
        lines.append("")
    for section, label in [("concepts", "概念"), ("resources", "资源"), ("people", "人物"), ("projects", "项目"), ("reviews", "综述")]:
        items = cat.get(section, [])
        if not items:
            continue
        lines += [f"## {label}", ""]
        for item in items:
            name = item.get("name") or item.get("title") or item.get("project_id")
            file = item.get("file") or item.get("folder", "")
            lines.append(f"- [[{Path(file).stem or name}]] — {item.get('brief', '')}")
        lines.append("")
    g.put_file(owner, repo, "index.md", "\n".join(lines).rstrip() + "\n", "paper-kb: regenerate index")
