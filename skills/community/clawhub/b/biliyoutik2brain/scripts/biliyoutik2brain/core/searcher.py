"""
BiliYouTik2Brain — 快链检索 (v1.0)

一句话功能：输入关键词，返回所有相关视频片段+来源。
搜三个地方：transcript文件、knowledge档案、说话人知识库。

设计原则：
  - 零依赖：只用标准库，不装Elasticsearch/Whoosh
  - 即时可用：不建索引，每次实时搜索（30+视频体量够用）
  - 渐进增强：未来体量变大时可换SQLite FTS5
"""

import os, re, json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

# ── 存储路径 ──
from .paths import TRANSCRIPTS_DIR
from .paths import KNOWLEDGE_DIR
SPEAKERS_FILE   = os.path.expanduser("~/.biliyoutik2brain_speakers.json")


@dataclass
class SearchResult:
    """一条搜索结果"""
    score: float                    # 相关性分数 (0-1)
    keyword: str                    # 匹配关键词
    source: str                     # "transcript" / "knowledge" / "speaker"
    uploader: str                   # UP主名
    title: str                      # 视频标题
    snippet: str                    # 匹配上下文片段 (最多200字)
    bvid: str = ""                  # BV号/视频ID
    file_path: str = ""             # 源文件路径
    date: str = ""                  # 处理日期
    url: str = ""                   # 原始视频链接


# ═══════════════════════════════════════════════════════════════
#  搜索逻辑
# ═══════════════════════════════════════════════════════════════

def _tokenize(text: str) -> List[str]:
    """简易中文分词：按非文字字符切分，保留2字以上"""
    if not text:
        return []
    tokens = re.findall(r'[\u4e00-\u9fff]{2,}|\w+', text)
    return [t for t in tokens if len(t) >= 2]


def _score_snippet(keyword: str, text: str, position: str = "body") -> float:
    """计算匹配分数

    关键词出现次数 × 位置权重 × 片段独特性
    - position: "title"=3.0, "summary"=2.0, "body"=1.0
    """
    if not keyword or not text:
        return 0.0

    text_lower = text.lower()
    kw_lower = keyword.lower()

    # 出现次数
    count = text_lower.count(kw_lower)
    if count == 0:
        return 0.0

    # 位置权重
    position_weight = {"title": 3.0, "summary": 2.0, "body": 1.0}.get(position, 1.0)

    # 基础分: 0.3 min + count 加成
    base = 0.3 + min(count, 10) * 0.07

    return min(base * position_weight, 1.0)


def _extract_snippet(text: str, keyword: str, context_chars: int = 100) -> str:
    """提取关键词周围的文本片段"""
    if not text or not keyword:
        return ""

    text_lower = text.lower()
    kw_lower = keyword.lower()
    idx = text_lower.find(kw_lower)

    if idx == -1:
        return text[:context_chars * 2]

    start = max(0, idx - context_chars)
    end = min(len(text), idx + len(keyword) + context_chars)

    snippet = text[start:end].strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"

    return snippet


# ═══════════════════════════════════════════════════════════════
#  transcript 搜索
# ═══════════════════════════════════════════════════════════════

def _parse_transcript(filepath: str) -> Optional[Dict]:
    """解析一个 transcript markdown 文件，返回结构化数据"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return None

    # 提取标题（第一行 # 开头）
    title = ""
    m = re.search(r'^# (.+)', content, re.MULTILINE)
    if m:
        title = m.group(1).strip()

    # 提取元信息
    uploader = ""
    source = ""
    bvid = ""
    date = ""

    m = re.search(r'\*\*UP主\*\*:\s*(.+)', content)
    if m:
        uploader = m.group(1).strip()

    m = re.search(r'\*\*来源\*\*:\s*(.+)', content)
    if m:
        source = m.group(1).strip()
        # 从URL提取BV号
        bv_match = re.search(r'(BV[\w]+|v=([\w-]+))', source)
        if bv_match:
            bvid = bv_match.group(1) or bv_match.group(2)

    # 转录用文字
    transcript_text = ""
    m = re.search(r'## 转录文本\s*\n+(.+)', content, re.DOTALL)
    if m:
        transcript_text = m.group(1).strip()
        # 截断分析部分
        analysis_pos = transcript_text.find("## 结构化分析")
        if analysis_pos > 0:
            transcript_text = transcript_text[:analysis_pos].strip()

    # 分析摘要
    summary = ""
    m = re.search(r'## 结构化分析\s*\n+(.+)', content, re.DOTALL)
    if m:
        json_str = m.group(1).strip()
        try:
            analysis = json.loads(json_str)
            summary = analysis.get("summary", "")
        except (json.JSONDecodeError, TypeError):
            pass

    return {
        "title": title,
        "uploader": uploader,
        "bvid": bvid,
        "url": source,
        "date": date,
        "transcript": transcript_text,
        "summary": summary,
        "file_path": filepath,
    }


def search_transcripts(keyword: str, max_results: int = 10) -> List[SearchResult]:
    """在 transcript 文件中搜索关键词"""
    if not keyword or not os.path.exists(TRANSCRIPTS_DIR):
        return []

    results = []
    files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith(".md")]

    for fname in files:
        filepath = os.path.join(TRANSCRIPTS_DIR, fname)
        data = _parse_transcript(filepath)
        if not data:
            continue

        # 快速过滤：关键词是否出现在文件中
        combined = f"{data['title']} {data['summary']} {data['transcript'][:5000]}"
        if keyword.lower() not in combined.lower():
            continue

        title_score = _score_snippet(keyword, data["title"], "title")
        summary_score = _score_snippet(keyword, data["summary"], "summary")
        body_score = _score_snippet(keyword, data["transcript"], "body")

        # 总分
        score = title_score * 0.4 + summary_score * 0.35 + body_score * 0.25
        if score < 0.1:
            continue

        # 取最佳匹配片段
        snippet = ""
        if title_score > 0:
            snippet = _extract_snippet(data["title"], keyword, 30)
        elif summary_score > 0:
            snippet = _extract_snippet(data["summary"], keyword, 80)
        else:
            snippet = _extract_snippet(data["transcript"], keyword, 100)

        results.append(SearchResult(
            score=round(score, 3),
            keyword=keyword,
            source="transcript",
            uploader=data["uploader"],
            title=data["title"],
            snippet=snippet,
            bvid=data["bvid"],
            file_path=filepath,
            date=data["date"],
            url=data["url"],
        ))

    # 按分数排序，取前N条
    results.sort(key=lambda r: r.score, reverse=True)
    return results[:max_results]


# ═══════════════════════════════════════════════════════════════
#  knowledge 档案搜索
# ═══════════════════════════════════════════════════════════════

def search_knowledge(keyword: str, max_results: int = 5) -> List[SearchResult]:
    """在 knowledge 档案中搜索关键词"""
    if not keyword or not os.path.exists(KNOWLEDGE_DIR):
        return []

    results = []
    files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith(".md")]

    for fname in files:
        filepath = os.path.join(KNOWLEDGE_DIR, fname)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            continue

        if keyword.lower() not in content.lower():
            continue

        # knowledge 文件按 ## 标题分节
        uploader = fname.replace(".md", "")

        for section in content.split("\n## "):
            if keyword.lower() not in section.lower():
                continue

            lines = section.strip().split("\n")
            if not lines:
                continue

            title = lines[0].replace("## ", "").strip()[:60]

            # 解析元信息
            bvid = ""
            date = ""
            url = ""
            for line in lines[:5]:
                m = re.search(r'来源:\s*(.+)', line)
                if m:
                    url = m.group(1).strip()
                    bv = re.search(r'(BV[\w]+|v=([\w-]+))', url)
                    if bv:
                        bvid = bv.group(1) or bv.group(2)
                m = re.search(r'处理日期:\s*(.+)', line)
                if m:
                    date = m.group(1).strip()

            score = _score_snippet(keyword, section, "body")
            snippet = _extract_snippet(section, keyword, 80)

            results.append(SearchResult(
                score=round(score * 0.8, 3),  # knowledge 档案权重略低于 transcript
                keyword=keyword,
                source="knowledge",
                uploader=uploader,
                title=title,
                snippet=snippet,
                bvid=bvid,
                file_path=filepath,
                date=date,
                url=url,
            ))

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:max_results]


# ═══════════════════════════════════════════════════════════════
#  说话人知识库搜索
# ═══════════════════════════════════════════════════════════════

def search_speakers(keyword: str, max_results: int = 5) -> List[SearchResult]:
    """在说话人知识库中搜索关键词"""
    if not keyword or not os.path.exists(SPEAKERS_FILE):
        return []

    try:
        with open(SPEAKERS_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    results = []

    for speaker_name, profile in db.items():
        display_name = profile.get("real_name", speaker_name)

        # 搜常讲话题
        topics = profile.get("common_topics", [])
        for topic in topics:
            if keyword.lower() in topic.lower():
                results.append(SearchResult(
                    score=0.6,
                    keyword=keyword,
                    source="speaker",
                    uploader=display_name,
                    title=f"常讲话题: {topic}",
                    snippet=f"{display_name} 常讲内容包含「{topic}」（共 {len(topics)} 个话题）",
                    bvid="",
                    file_path=SPEAKERS_FILE,
                ))
                break  # 一个说话人只加一条

        # 搜已知规律
        patterns = profile.get("known_patterns", [])
        for pattern in patterns:
            if keyword.lower() in pattern.lower():
                results.append(SearchResult(
                    score=0.7,
                    keyword=keyword,
                    source="speaker",
                    uploader=display_name,
                    title=f"核心观点",
                    snippet=_extract_snippet(pattern, keyword, 60),
                    bvid="",
                    file_path=SPEAKERS_FILE,
                ))
                break

        # 搜历史视频标题
        videos = profile.get("processed_videos", [])
        for v in videos:
            title = v.get("title", "")
            insight = v.get("key_insight", "")
            if keyword.lower() in title.lower() or keyword.lower() in insight.lower():
                results.append(SearchResult(
                    score=0.5,
                    keyword=keyword,
                    source="speaker",
                    uploader=display_name,
                    title=title,
                    snippet=insight[:100] if insight else f"由 {display_name} 讲解",
                    bvid=v.get("bvid", ""),
                    date=v.get("date", ""),
                    file_path=SPEAKERS_FILE,
                ))
                break

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:max_results]


# ═══════════════════════════════════════════════════════════════
#  统一搜索入口
# ═══════════════════════════════════════════════════════════════

def search(keyword: str, max_results: int = 10) -> List[SearchResult]:
    """统一搜索：transcript + knowledge + speaker

    返回按分数排序的合并结果。
    """
    if not keyword:
        return []

    all_results = []
    all_results.extend(search_transcripts(keyword, max_results))
    all_results.extend(search_knowledge(keyword, max_results // 2))
    all_results.extend(search_speakers(keyword, max_results // 2))

    # 按分数排序，去重
    seen = set()
    deduped = []
    for r in sorted(all_results, key=lambda x: x.score, reverse=True):
        key = (r.uploader, r.title[:40])
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    return deduped[:max_results]


def search_all(keywords: List[str], max_results: int = 15) -> List[SearchResult]:
    """多关键词搜索"""
    if not keywords:
        return []

    all_results = []
    for kw in keywords:
        all_results.extend(search(kw, max_results // len(keywords) + 3))

    # 按分数排序去重
    seen = set()
    deduped = []
    for r in sorted(all_results, key=lambda x: x.score, reverse=True):
        key = (r.uploader, r.title[:40])
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    return deduped[:max_results]
