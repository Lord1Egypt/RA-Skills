#!/usr/bin/env python3
"""
Fragment Stitcher - 碎片知识缝纫师
核心脚本：碎片关系分析与知识连接生成
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

# 配置
KNOWLEDGE_DIR = Path("knowledge")
FRAGMENTS_DIR = KNOWLEDGE_DIR / "fragments"
CONNECTIONS_DIR = KNOWLEDGE_DIR / "connections"
OUTLINES_DIR = KNOWLEDGE_DIR / "outlines"

def ensure_dirs():
    """确保目录结构存在"""
    for d in [FRAGMENTS_DIR, CONNECTIONS_DIR, OUTLINES_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def extract_keywords(text):
    """提取关键词（简单实现）"""
    # 移除标点，转小写，分词
    words = text.lower().replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').split()
    # 过滤短词，返回唯一词
    return set(w for w in words if len(w) > 1)

def calculate_similarity(text1, text2):
    """计算两段文本的相似度"""
    kw1 = extract_keywords(text1)
    kw2 = extract_keywords(text2)
    if not kw1 or not kw2:
        return 0.0
    intersection = len(kw1 & kw2)
    union = len(kw1 | kw2)
    return intersection / union if union > 0 else 0.0

def find_related_fragments(new_fragment_path, top_k=3):
    """查找与新碎片相关的已有碎片"""
    if not new_fragment_path.exists():
        return []
    
    new_content = new_fragment_path.read_text(encoding='utf-8')
    new_text = new_content.split('---')[-1] if '---' in new_content else new_content
    
    related = []
    for frag in FRAGMENTS_DIR.glob("*.md"):
        if frag == new_fragment_path:
            continue
        content = frag.read_text(encoding='utf-8')
        text = content.split('---')[-1] if '---' in content else content
        sim = calculate_similarity(new_text, text)
        if sim > 0.1:  # 阈值
            related.append((frag, sim))
    
    related.sort(key=lambda x: x[1], reverse=True)
    return related[:top_k]

def generate_connection_note(new_frag_path, related_frags):
    """生成知识连接笔记"""
    if not related_frags:
        return None
    
    new_name = new_frag_path.stem
    timestamp = datetime.now().strftime("%Y-%m-%d")
    conn_file = CONNECTIONS_DIR / f"{timestamp}-{new_name}-connections.md"
    
    content = f"""# 知识连接笔记
创建时间: {datetime.now().isoformat()}
源碎片: {new_frag_path.name}

## 关联发现

"""
    for frag, sim in related_frags:
        content += f"""### {frag.stem} (相似度: {sim:.2%})
- 文件: {frag.name}
- 关联说明: [请补充具体关联点]

"""
    content += """
## 建议行动
- [ ] 阅读关联碎片，确认关联性
- [ ] 补充具体的连接说明
- [ ] 如已形成体系，考虑生成大纲
"""
    
    conn_file.write_text(content, encoding='utf-8')
    return conn_file

def check_theme_threshold(theme_tag, threshold=5):
    """检查某主题的碎片数量是否达到阈值"""
    count = 0
    for frag in FRAGMENTS_DIR.glob("*.md"):
        if theme_tag in frag.stem:
            count += 1
    return count >= threshold

def save_fragment(content, source="manual", tags=None):
    """保存新碎片"""
    ensure_dirs()
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    hash_id = hashlib.md5(content[:100].encode()).hexdigest()[:8]
    
    # 确定主题标签
    theme = tags[0] if tags else "general"
    frag_file = FRAGMENTS_DIR / f"{timestamp}-{hash_id}-{theme}.md"
    
    meta = f"""---
created: {datetime.now().isoformat()}
source: {source}
tags: {tags or []}
---

"""
    frag_file.write_text(meta + content, encoding='utf-8')
    return frag_file

if __name__ == "__main__":
    # 测试
    ensure_dirs()
    print("Fragment Stitcher 初始化完成")
    print(f"碎片目录: {FRAGMENTS_DIR}")
    print(f"连接目录: {CONNECTIONS_DIR}")
