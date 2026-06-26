#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════
# build-capsule-index.py — 话题胶囊元数据索引构建器
# 扫描 memory/topics/ 下所有 .md 文件，生成结构化索引
# 输出: .capsule-index.json (供 Adaptive RAG 预筛选使用)
# ═══════════════════════════════════════════════════════

import os
import json
import re
from datetime import datetime
from pathlib import Path

TOPICS_DIR = Path(os.path.expanduser("~/.openclaw/workspace/memory/topics"))
OUTPUT_FILE = TOPICS_DIR / ".capsule-index.json"

# 胶囊分类规则（基于文件名关键词）
CATEGORY_RULES = {
    "medical": ["互联网医院", "医疗", "双向转诊", "联合病房", "中医", "CHIMA", "健康"],
    "tech": ["Claude", "OpenClaw", "Harness", "TurboQuant", "架构", "技术", "本地AI", "autoskill", "Hooks"],
    "research": ["科研", "论文", "学术", "TriAttention", "kdense", "研究", "量表", "self-evolving", "research"],
    "doc": ["公文", "办公", "事业", "微信文章", "数字院区", "素材", "写作", "AI观点"],
    "personal": ["命理", "炒股", "金融", "古籍", "个人"],
    "collab": ["CEO-CTO", "协作", "openai-harness"],
}


def classify_capsule(name):
    """根据名称自动分类"""
    tags = []
    for cat, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in name:
                tags.append(cat)
                break
    if not tags:
        tags.append("general")
    return tags


def extract_summary(filepath, max_chars=200):
    """提取胶囊摘要：优先取第一个标题或前几行"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000)
        
        lines = content.strip().split('\n')
        
        # 跳过开头的标题行（# 开头）
        summary_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('#'):
                continue  # 跳过标题行
            summary_lines.append(stripped)
            if len(' '.join(summary_lines)) > max_chars:
                break
        
        summary = ' '.join(summary_lines)[:max_chars]
        return summary if summary else "(空胶囊)"
    except Exception:
        return "(读取失败)"


def build_index():
    """扫描所有胶囊，构建索引"""
    capsules = []
    
    md_files = sorted(TOPICS_DIR.glob("*.md"))
    
    for f in md_files:
        name = f.stem
        size = f.stat().st_size
        mtime = datetime.fromtimestamp(f.stat().st_mtime).isoformat()
        summary = extract_summary(f)
        tags = classify_capsule(name)
        
        capsules.append({
            "id": name,
            "name": name,
            "size_bytes": size,
            "modified": mtime,
            "summary": summary,
            "tags": tags,
            "path": str(f.relative_to(Path(os.path.expanduser("~/.openclaw/workspace")))),
        })
    
    index = {
        "version": "1.0",
        "built_at": datetime.now().isoformat(),
        "total_capsules": len(capsules),
        "categories": {
            "medical": [c["id"] for c in capsules if "medical" in c["tags"]],
            "tech": [c["id"] for c in capsules if "tech" in c["tags"]],
            "research": [c["id"] for c in capsules if "research" in c["tags"]],
            "doc": [c["id"] for c in capsules if "doc" in c["tags"]],
            "personal": [c["id"] for c in capsules if "personal" in c["tags"]],
            "collab": [c["id"] for c in capsules if "collab" in c["tags"]],
        },
        "capsules": capsules,
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 索引构建完成!")
    print(f"   胶囊总数: {len(capsules)}")
    for cat, ids in index["categories"].items():
        print(f"   {cat}: {len(ids)} 个")
    print(f"   输出: {OUTPUT_FILE}")
    
    return index


if __name__ == "__main__":
    build_index()
