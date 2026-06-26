#!/usr/bin/env python3
"""
extract_entities.py — Claude-Obsidian 实体提取工具
从输入文件中提取实体，并与 vault 比对
"""

import re, sys
from pathlib import Path

def extract_entities_markdown(content):
    entities = []
    for line in content.split('\n'):
        headings = re.findall(r'^#{1,3}\s+(.+)$', line, re.MULTILINE)
        for h in headings:
            entities.append({"text": h.strip(), "source": "heading", "weight": 3})
        emphasis = re.findall(r'\*\*([^*]+)\*\*|\*([^*]+)\*', line)
        for e in emphasis:
            for part in e:
                if part:
                    entities.append({"text": part.strip(), "source": "emphasis", "weight": 2})
        if line.startswith('# ') and len(line) < 100:
            entities.append({"text": line[2:].strip(), "source": "title", "weight": 5})
    return entities

def build_vault_index(vault_path):
    vault = Path(vault_path)
    if not vault.exists():
        return {}
    index = {}
    for f in vault.rglob("*.md"):
        if any(p.startswith('.') for p in f.parts): continue
        try:
            content = f.read_text(encoding='utf-8')
        except Exception:
            continue
        tm = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        title = tm.group(1).strip().lower() if tm else (re.search(r'^#\s+(.+)$', content, re.MULTILINE) or type('',(),{'group':lambda s,x:''})()).group(1).strip().lower() if re.search(r'^#\s+(.+)$', content, re.MULTILINE) else f.stem.lower()
        index[title] = f.relative_to(vault)
    return index

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--vault", default=None)
    args = parser.parse_args()
    p = Path(args.input_file)
    if not p.exists(): print(f"File not found: {p}"); sys.exit(1)
    content = p.read_text(encoding='utf-8')
    entities = extract_entities_markdown(content)
    entities.sort(key=lambda x: -x["weight"])
    print(f"Extracted {len(entities)} entities from {p.name}:")
    vault_index = build_vault_index(args.vault) if args.vault else {}
    for e in entities[:20]:
        if vault_index:
            found = any(e["text"].lower() in k for k in vault_index)
            mark = "✅ exists" if found else "🆕 new"
            print(f"  {mark}: {e['text']} [weight={e['weight']}]")
        else:
            print(f"  • {e['text']} [weight={e['weight']}, {e['source']}]")
