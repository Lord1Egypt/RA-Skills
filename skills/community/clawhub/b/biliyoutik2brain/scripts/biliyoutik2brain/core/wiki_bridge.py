"""
wiki_bridge.py — biliyoutik2brain × karpathy-wiki 双向桥接

功能:
  1. wiki_ingest: 视频加工后，以karpathy-wiki格式写入实体页面
  2. wiki_query: 纠错前，从wiki读取相关领域知识注入prompt
  3. 自动维护 index.md + log.md

格式对齐 karpathy-llm-wiki 实体页面规范。
"""

import os, re, json, time
from typing import List, Dict, Optional

# ── wiki路径 ──
WIKI_DIR = os.path.expanduser("~/wiki/wiki")
INDEX_FILE = os.path.join(WIKI_DIR, "index.md")
LOG_FILE = os.path.join(WIKI_DIR, "log.md")
os.makedirs(WIKI_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# 写入：视频加工后同步到wiki
# ═══════════════════════════════════════════════════════════════

def wiki_ingest(
    speaker: str,
    summary: str,
    keywords: list,
    domain: str,
    video_title: str,
    video_url: str,
    analysis: dict = None,
) -> None:
    """以karpathy-wiki格式将视频知识写入实体页面"""
    slug = _make_slug(speaker)
    page_path = os.path.join(WIKI_DIR, f"{slug}.md")
    today = time.strftime("%Y-%m-%d")
    kw_str = ", ".join(keywords[:8]) if keywords else ""
    domain_label = domain or "综合"
    analysis_text = analysis.get("analysis", "") if analysis else ""
    
    # 构造新条目
    entry = f"""### {video_title[:80]}
> 日期: {today} | 来源: {video_url}

{summary}

"""
    if analysis_text:
        entry += f"**分析**: {analysis_text[:500]}\n"

    entry += f"**关键词**: {kw_str}\n---\n\n"

    if os.path.exists(page_path):
        # 追加条目
        with open(page_path) as f:
            existing = f.read()
        if summary[:80] in existing:
            print(f"  [Wiki入库] 摘要已存在，跳过 ({slug}.md)")
            return
        with open(page_path, "a") as f:
            f.write(entry)
        print(f"  [Wiki入库] ✅ 追加 ({slug}.md)")
    else:
        # 新建实体页（karpathy格式兼容 + 与已有b2b页面风格一致）
        page = f"""# {speaker}

> 来源: {video_url} | 领域: {domain_label}

## 概述

{summary}

**关键词**: {kw_str}

---

## 视频条目

{entry}"""
        with open(page_path, "w") as f:
            f.write(page)
        print(f"  [Wiki入库] ✅ 新建 ({slug}.md)")
        _update_index(slug, speaker, domain_label, today)

    _update_log(slug, speaker, video_title[:60], today)


# ═══════════════════════════════════════════════════════════════
# 读取：纠错时获取wiki上下文
# ═══════════════════════════════════════════════════════════════

def wiki_query(topic: str, uploader: str = "", domain: str = "", top_n: int = 3) -> str:
    """从wiki读取相关领域知识，返回结构化文本供LLM prompt注入
    
    Args:
        topic: 视频标题/主题
        uploader: up主名称
        domain: 领域过滤（如"trading"/"coding"），跨up主查询时不跨领域
        top_n: 最多返回几个页面的知识
    
    Returns:
        格式化文本（空字串表示无相关wiki内容）
    """
    if not os.path.exists(INDEX_FILE):
        return ""
    
    # 1. 读index找到相关页面
    with open(INDEX_FILE) as f:
        index_content = f.read()
    
    # 2. 收集关键词
    search_terms = set()
    for t in [uploader, topic]:
        if t:
            terms = re.split(r'[^\w\u4e00-\u9fff]', t)
            for term in terms:
                term = term.strip()
                if len(term) > 1:
                    search_terms.add(term.lower())
    
    if not search_terms:
        return ""
    
    # 3. 从index匹配页面（过滤同领域）
    candidates = []
    for line in index_content.split("\n"):
        m = re.findall(r'\[\[([^\]]+)\]\]', line)
        for page_name in m:
            score = _match_score(page_name, search_terms)
            if score > 0:
                # 领域过滤：index行含领域括号，如 "xxx（trading）"
                if domain:
                    domain_markers = [f"（{domain}", f"({domain}", f"/{domain}"]
                    passes_domain = any(marker in line.lower() for marker in domain_markers)
                    if not passes_domain:
                        # 当前speaker自己的页面不按领域过滤
                        page_lower = _make_slug(uploader.lower())
                        if page_lower not in page_name.lower():
                            score = 0
                if score > 0:
                    candidates.append((page_name, score))
    
    candidates.sort(key=lambda x: -x[1])
    candidates = candidates[:top_n]
    
    if not candidates:
        return ""
    
    # 4. 读取页面内容
    parts = []
    for page_name, _ in candidates:
        page_file = os.path.join(WIKI_DIR, _page_filename(page_name))
        if not os.path.exists(page_file):
            continue
        with open(page_file) as f:
            content = f.read()
        
        # 提取概述和关键事实
        overview = _extract_section(content, "概述", "##")
        key_facts = _extract_section(content, "Key facts", "##")
        # 提取视频条目中最新的2个
        video_section = _extract_section(content, "视频条目", "##")
        recent_videos = ""
        if video_section:
            entries = re.findall(r'### (.*?)\n>.*?\n(.*?)(?=\n###|\n---|\Z)', video_section, re.DOTALL)
            for title, body in entries[-2:]:
                body_trim = body.strip()[:300]
                recent_videos += f"- {title.strip()}: {body_trim}\n"
        
        ctx = f"— {page_name} —\n"
        if overview:
            ctx += f"{overview[:500]}\n"
        if key_facts:
            ctx += f"{key_facts[:500]}\n"
        if recent_videos:
            ctx += f"\n最新视频:\n{recent_videos}"
            ctx += f"{key_facts[:500]}\n"
        parts.append(ctx.strip())
    
    return "\n---\n".join(parts) if parts else ""


# ═══════════════════════════════════════════════════════════════
# 内部维护
# ═══════════════════════════════════════════════════════════════

def _make_slug(name: str) -> str:
    """名字 → wiki文件名slug"""
    name = re.sub(r'[^\w\u4e00-\u9fff]', '_', name)
    return name.lower()


def _page_filename(page_name: str) -> str:
    """页面名 → 文件名（处理大小写差异）"""
    # 优先精确匹配
    exact = f"{page_name}.md"
    exact_path = os.path.join(WIKI_DIR, exact)
    if os.path.exists(exact_path):
        return exact
    # 降级用小写slug
    slug = _make_slug(page_name)
    return f"{slug}.md"


def _match_score(page_name: str, search_terms: set) -> int:
    """页面与搜索词的相关度打分"""
    page_lower = page_name.lower()
    score = 0
    for term in search_terms:
        if term in page_lower:
            score += 2
        # 词根匹配
        if len(term) > 3 and term[:-1] in page_lower:
            score += 1
    return score


def _extract_section(content: str, section_name: str, end_marker: str) -> str:
    """从markdown页面提取指定section的文本"""
    # 支持中英文section名
    patterns = [
        rf"##\s*{section_name}\s*\n(.*?)(?=\n##\s|\Z)",
        rf"##\s*{section_name}\s*\n(.*?)(?=\n---|\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, content, re.DOTALL)
        if m:
            return m.group(1).strip()
    return ""


def _update_index(slug: str, speaker: str, domain: str, today: str) -> None:
    """index.md 添加新条目"""
    if not os.path.exists(INDEX_FILE):
        return
    with open(INDEX_FILE) as f:
        content = f.read()
    
    # 找"交易方法/理念库"章节
    section_marker = "## 💹 交易方法/理念库"
    idx = content.find(section_marker)
    if idx == -1:
        section_marker = "## 交易方法"
        idx = content.find(section_marker)
    if idx == -1:
        # 找不到合适章节，追加在末尾
        new_row = f"\n| [[{slug}]] | {speaker}（{domain}） | {today} |\n"
        content += new_row
    else:
        section_end = content.find("\n##", idx + 5)
        if section_end == -1:
            content += f"\n| [[{slug}]] | {speaker}（{domain}） | {today} |\n"
        else:
            new_row = f"| [[{slug}]] | {speaker}（{domain}） | {today} |\n"
            content = content[:section_end] + new_row + content[section_end:]
    
    with open(INDEX_FILE, "w") as f:
        f.write(content)
    print(f"  [Wiki入库] ✅ 索引已更新 ({slug})")


def _update_log(slug: str, speaker: str, video_title: str, today: str) -> None:
    """log.md 追加操作记录"""
    entry = f"""
## [{today}] ingest | {video_title}
Source: <biliyoutik2brain auto-archive>
Pages affected: {slug}.md (updated)
---

"""
    with open(LOG_FILE, "a") as f:
        f.write(entry)


# ================================================================
# 移植自 ZIP v1.x: wiki_bridge.py 扩展内容
# ================================================================

def _find_cross_references(speaker: str, keywords: List[str], domain: str) -> str:
    """
    扫描 knowledge/ 下同领域的其他 UP 主文章，
    用关键词命中做观点对比，输出共鸣/对立/补充/你的观点。
    """
    from .paths import KNOWLEDGE_DIR
    knowledge_dir = KNOWLEDGE_DIR
    if not os.path.exists(knowledge_dir):
        return ""
    
    this_slug = _make_slug(speaker)
    matches = []
    
    # 扫所有 knowledge 文件
    for fname in os.listdir(knowledge_dir):
        if not fname.endswith(".md"):
            continue
        other_slug = fname[:-3]  # 去 .md
        if other_slug == this_slug:
            continue
        
        fpath = os.path.join(knowledge_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue
        
        # 同领域过滤: 检查文件中的领域标签
        if domain:
            domain_in_file = False
            for line in content.split("\n")[:20]:
                if f"领域: {domain}" in line or f"/{domain}" in line:
                    domain_in_file = True
                    break
            # 找不到明确领域标签时，用关键词相似度代替
            if not domain_in_file:
                # 放宽：只要有任何关键词重叠就算相关
                pass
        
        # 计算关键词命中
        score = 0
        hit_words = []
        for kw in keywords[:10]:
            if kw.lower() in content.lower():
                score += 1
                hit_words.append(kw)
        
        if score >= 2:  # 至少命中2个关键词才算相关
            # 提取该 UP 主的核心观点
            other_speaker = fname[:-3].replace("_", " ")
            views = _extract_views(content)
            matches.append((other_speaker, score, hit_words, views[:300]))
    
    if not matches:
        return ""
    
    matches.sort(key=lambda x: -x[1])
    
    # 拼接对比结果
    lines = []
    for i, (other, score, words, views) in enumerate(matches[:3]):  # 最多3个
        lines.append(f"  - **{other}** (命中 {', '.join(words[:3])}): {views}")
    
    return "\n".join(lines)



def _extract_views(content: str) -> str:
    """从 knowledge 文件中提取 UP 主的核心观点"""
    # 提取摘要行和核心行
    views = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("**摘要**:"):
            views.append(line.replace("**摘要**:", "").strip()[:200])
        elif line.startswith("**核心**:"):
            views.append(line.replace("**核心**:", "").strip()[:200])
        elif line.startswith("**应用**:"):
            views.append(line.replace("**应用**:", "").strip()[:200])
    
    return " | ".join(views[:2]) if views else "（暂无详细观点摘要）"

