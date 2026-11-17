"""
BiliYouTik2Brain — 知识库查询接口

职责单一：
  1. 提供 `query()` 接口供 enhance_engine 调用
  2. 检索已有知识（按 UP主/领域/关键词）
  3. 不负责知识写入（由 node_save.py 归档）
  4. 纯确定性查询，不涉及 LLM

数据来源：
  - storage/knowledge/*.md — 已归档的说话人知识
  - ~/wiki/wiki/*.md — Karpathy wiki 同步
"""

import os, re, json, glob
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class KnowledgeEntry:
    """单条知识条目"""
    speaker: str = ""
    summary: str = ""
    keywords: List[str] = field(default_factory=list)
    domain: str = ""
    date: str = ""
    source_url: str = ""
    file_path: str = ""
    similarity: float = 0.0


# ── 路径 ──
from .paths import KNOWLEDGE_DIR
WIKI_DIR = os.path.expanduser("~/wiki/wiki")


def _ensure_dirs():
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    os.makedirs(WIKI_DIR, exist_ok=True)


def query(speaker: str = "", domain: str = "", keywords: Optional[List[str]] = None,
          max_results: int = 5) -> List[KnowledgeEntry]:
    """知识库查询
    
    Args:
        speaker: UP主名（模糊匹配）
        domain: 领域过滤
        keywords: 关键词过滤
        max_results: 最大返回条数
    
    Returns:
        匹配的知识条目列表，按相关性降序
    
    使用示例:
        entries = query(speaker="张聚贤", max_results=3)
        entries = query(domain="交易", keywords=["孕线", "Pinbar"])
    """
    _ensure_dirs()
    
    if not keywords:
        keywords = []
    
    results: List[KnowledgeEntry] = []
    
    # 1. 搜索 knowledge/ 目录
    for fname in os.listdir(KNOWLEDGE_DIR):
        if not fname.endswith(".md"):
            continue
        filepath = os.path.join(KNOWLEDGE_DIR, fname)
        entries = _parse_knowledge_file(filepath, speaker, domain, keywords)
        results.extend(entries)
    
    # 2. 搜索 wiki/*.md（补充）
    if os.path.exists(WIKI_DIR):
        for fname in os.listdir(WIKI_DIR):
            if not fname.endswith(".md") or fname == "index.md":
                continue
            filepath = os.path.join(WIKI_DIR, fname)
            entries = _parse_wiki_file(filepath, speaker, domain, keywords)
            results.extend(entries)
    
    # 3. 去重（按source_url去重）
    seen_urls = set()
    deduped = []
    for e in results:
        key = e.source_url or e.summary
        if key in seen_urls:
            continue
        seen_urls.add(key)
        deduped.append(e)
    
    # 4. 排序（按关键词匹配数降序）
    deduped.sort(key=lambda e: -e.similarity)
    
    return deduped[:max_results]


def query_by_uploader(uploader: str, max_results: int = 3) -> str:
    """快速获取UP主已有知识（返回纯文本，直接供prompt拼接）"""
    entries = query(speaker=uploader, max_results=max_results)
    if not entries:
        return ""
    
    parts = ["## 已有知识记录"]
    for e in entries:
        parts.append(f"- {e.summary}")
        if e.keywords:
            parts.append(f"  关键词: {', '.join(e.keywords[:5])}")
        if e.speaker:
            parts.append(f"  UP主: {e.speaker}")
        parts.append("")
    
    return "\n".join(parts).strip()


def _parse_knowledge_file(filepath: str, speaker: str, domain: str,
                          keywords: List[str]) -> List[KnowledgeEntry]:
    """解析 knowledge/ 目录下的知识文件"""
    entries = []
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except Exception:
        return entries
    
    speaker_from_file = os.path.splitext(os.path.basename(filepath))[0]
    
    # 说话人过滤
    if speaker and not _fuzzy_match(speaker_from_file, speaker):
        return entries
    
    # 解析 ## 标题段落
    blocks = re.split(r'\n(?=##\s)', content)
    for block in blocks:
        if not block.strip():
            continue
        
        # 提取摘要
        m_summary = re.search(r'\*\*摘要\*\*:\s*(.+?)(?:\n|$)', block)
        summary = m_summary.group(1).strip() if m_summary else ""
        
        # 提取关键词
        m_kw = re.search(r'\*\*关键词\*\*:\s*(.+?)(?:\n|$)', block)
        block_keywords = [k.strip() for k in (m_kw.group(1).split(',') if m_kw else [])]
        
        # 提取领域
        m_domain = re.search(r'领域:\s*(.+?)(?:\||\n)', block)
        block_domain = m_domain.group(1).strip() if m_domain else ""
        
        # 提取日期
        m_date = re.search(r'日期:\s*(\d{4}-\d{2}-\d{2})', block)
        block_date = m_date.group(1) if m_date else ""
        
        # 来源
        m_url = re.search(r'来源:\s*(https?://[^\s]+)', block)
        source_url = m_url.group(1).strip() if m_url else ""
        
        # 领域过滤
        if domain and block_domain and domain.lower() not in block_domain.lower():
            continue
        
        # 关键词匹配度
        similarity = 0.0
        if keywords:
            all_text = block.lower()
            matches = sum(1 for kw in keywords if kw.lower() in all_text)
            similarity = matches / len(keywords)
            if similarity == 0:
                continue
        
        if summary:
            entries.append(KnowledgeEntry(
                speaker=speaker_from_file,
                summary=summary,
                keywords=block_keywords,
                domain=block_domain,
                date=block_date,
                source_url=source_url,
                file_path=filepath,
                similarity=similarity,
            ))
    
    return entries


def _parse_wiki_file(filepath: str, speaker: str, domain: str,
                     keywords: List[str]) -> List[KnowledgeEntry]:
    """解析 wiki/ 目录下的知识页面"""
    entries = []
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except Exception:
        return entries
    
    slug = os.path.splitext(os.path.basename(filepath))[0]
    
    if speaker and not _fuzzy_match(slug, speaker):
        return entries
    
    # 提取顶级标题
    m_title = re.search(r'^#\s+(.+?)\s*$', content, re.MULTILINE)
    page_title = m_title.group(1).strip() if m_title else slug
    
    # 提取概述段落
    m_overview = re.search(r'## 概述\s*\n\s*(.+?)(?:\n##|\n---|$)', content, re.DOTALL)
    overview = m_overview.group(1).strip()[:200] if m_overview else ""
    
    # 提取视频条目
    video_blocks = re.findall(r'###\s+(.+?)\n>(.+?)\n([\s\S]*?)(?=\n###|\n---|$)', content)
    
    if overview and not video_blocks:
        entries.append(KnowledgeEntry(
            speaker=page_title,
            summary=overview,
            file_path=filepath,
        ))
    
    for title, date_line, body in video_blocks:
        m_url = re.search(r'https?://[^\s]+', date_line)
        source_url = m_url.group(0) if m_url else ""
        
        m_date = re.search(r'\d{4}-\d{2}-\d{2}', date_line)
        block_date = m_date.group(0) if m_date else ""
        
        body_text = body.strip()[:200] if body else ""
        
        all_text = f"{title} {body_text}".lower()
        similarity = 0.0
        if keywords:
            matches = sum(1 for kw in keywords if kw.lower() in all_text)
            similarity = matches / len(keywords) if keywords else 0
            if similarity == 0:
                continue
        
        entries.append(KnowledgeEntry(
            speaker=page_title,
            summary=title[:80],
            keywords=[],
            date=block_date,
            source_url=source_url,
            file_path=filepath,
            similarity=similarity,
        ))
    
    return entries


def _fuzzy_match(name_a: str, name_b: str) -> bool:
    """说话人名模糊匹配"""
    a = name_a.strip().lower().replace("_", "").replace(" ", "")
    b = name_b.strip().lower().replace("_", "").replace(" ", "")
    return a == b or a in b or b in a
