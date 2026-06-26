#!/usr/bin/env python3
"""
AI Game - 游戏×AI 资讯抓取脚本 v2
三层信源架构 + 关键词过滤 + 分类 + 标签 + 推荐理由
"""

import json
import os
import sys
import re
import hashlib
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from xml.etree import ElementTree as ET

# === 配置 ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
SOURCES_PATH = os.path.join(SKILL_DIR, "references", "sources.json")
KEYWORDS_PATH = os.path.join(SKILL_DIR, "references", "keywords.json")
DATA_DIR = os.path.join(SKILL_DIR, "data")

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
FETCH_TIMEOUT = 15
MAX_AGE_HOURS = 72


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_url(url, timeout=FETCH_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        print(f"  [WARN] 抓取失败 {url}: {e}", file=sys.stderr)
        return None


def parse_rss(xml_text, source_name):
    items = []
    if not xml_text:
        return items
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"  [WARN] XML 解析失败 ({source_name}): {e}", file=sys.stderr)
        return items

    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "dc": "http://purl.org/dc/elements/1.1/",
        "content": "http://purl.org/rss/1.0/modules/content/",
    }

    # RSS 2.0
    for item in root.findall(".//item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        desc = item.findtext("description", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        if title and link:
            items.append({
                "title": title,
                "url": link,
                "summary": clean_html(desc)[:300] if desc else "",
                "source": source_name,
                "published_at": parse_date(pub_date),
            })

    # Atom
    for entry in root.findall(".//atom:entry", ns):
        title = entry.findtext("atom:title", "", ns).strip()
        link_el = entry.find("atom:link[@rel='alternate']", ns)
        if link_el is None:
            link_el = entry.find("atom:link", ns)
        link = link_el.get("href", "") if link_el is not None else ""
        summary = entry.findtext("atom:summary", "", ns).strip()
        updated = entry.findtext("atom:updated", "", ns).strip()
        published = entry.findtext("atom:published", "", ns).strip()
        if title and link:
            items.append({
                "title": title,
                "url": link,
                "summary": clean_html(summary)[:300] if summary else "",
                "source": source_name,
                "published_at": parse_date(published or updated),
            })

    return items


def clean_html(text):
    return re.sub(r"<[^>]+>", "", text).strip()


def parse_date(date_str):
    if not date_str:
        return None
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    date_str = date_str.replace("GMT", "+0000").replace("UTC", "+0000")
    date_str = re.sub(r"([+-]\d{2}):(\d{2})$", r"\1\2", date_str)
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue
    return None


def fetch_aihot(queries):
    items = []
    seen_ids = set()
    for q in queries:
        url = f"https://aihot.virxact.com/api/public/items?mode=all&q={urllib.request.quote(q)}&take=30"
        text = fetch_url(url)
        if not text:
            continue
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            continue
        for item in data.get("items", []):
            item_id = item.get("id", "")
            if item_id in seen_ids:
                continue
            seen_ids.add(item_id)
            # 用真实来源而非 "AI HOT"，让用户看到一手出处
            raw_source = item.get("source", "unknown")
            items.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "summary": item.get("summary", "")[:300] if item.get("summary") else "",
                "source": raw_source,
                "source_via": "AI HOT",  # 标记数据渠道，但不展示给用户
                "published_at": item.get("publishedAt"),
            })
    return items


def _word_match(keyword, text):
    kw = keyword.lower()
    if len(kw) <= 3 and kw.isascii() and kw.isalpha():
        return bool(re.search(r'\b' + re.escape(kw) + r'\b', text))
    return kw in text


def _combo_match(keyword, text):
    """处理 A+B 组合关键词"""
    if "+" in keyword:
        parts = [p.strip().lower() for p in keyword.split("+")]
        return all(_word_match(p, text) for p in parts)
    return _word_match(keyword, text)


def is_relevant(item, keywords_config, source_layer):
    """判断是否相关。Layer 1 游戏专业源只需含 AI 元素；Layer 2/3 需要游戏+AI 双重命中"""
    title = item.get('title', '').lower()
    summary = item.get('summary', '').lower()
    full_text = f"{title} {summary}"

    # 核心关键词：任何层级命中即相关
    for kw in keywords_config["global_filter"]["core_keywords"]:
        if _combo_match(kw, full_text):
            return True

    # Layer 1 游戏专业源：只需判断是否含 AI 元素
    if source_layer == 1:
        ai_keywords = keywords_config["global_filter"].get("layer1_ai_keywords", [])
        for kw in ai_keywords:
            if _word_match(kw, full_text):
                return True
        return False

    # Layer 2/3：需要游戏+AI 双重命中
    game_kws = keywords_config["global_filter"]["context_game"]
    ai_kws = keywords_config["global_filter"]["context_ai"]

    # 标题内同时出现游戏词+AI词
    title_has_game = any(_word_match(kw, title) for kw in game_kws)
    title_has_ai = any(_word_match(kw, title) for kw in ai_kws)
    if title_has_game and title_has_ai:
        return True

    # 摘要内同时出现
    summary_has_game = any(_word_match(kw, summary) for kw in game_kws)
    summary_has_ai = any(_word_match(kw, summary) for kw in ai_kws)
    if summary_has_game and summary_has_ai:
        return True

    # 标题含游戏词 + 摘要含多个 AI 词
    if title_has_game and summary_has_ai:
        ai_count = sum(1 for kw in ai_kws if _word_match(kw, summary))
        if ai_count >= 2:
            return True

    # 标题含AI词 + 摘要含多个游戏词
    if title_has_ai and summary_has_game:
        game_count = sum(1 for kw in game_kws if _word_match(kw, summary))
        if game_count >= 2:
            return True

    return False


def classify_item(item, keywords_config):
    """分类打标，返回 (primary, secondary)
    
    优先级逻辑：具体分类（in-game/creation/dev-tools/ops/research）
    优先于兆底分类（industry）。当具体分类和 industry 得分相同时，
    选具体分类；只有当 industry 得分明显更高（>2倍）时才归 industry。
    """
    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
    scores = {}
    for category, keywords in keywords_config["category_keywords"].items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[category] = score
    if not scores:
        return "industry", None
    
    # 如果有非-industry 分类命中，且 industry 也命中，除非 industry 得分超过非-industry 最高分 2 倍，否则优先选非-industry
    non_industry = {k: v for k, v in scores.items() if k != "industry"}
    if non_industry:
        best_specific = max(non_industry.items(), key=lambda x: x[1])
        industry_score = scores.get("industry", 0)
        if industry_score > best_specific[1] * 2:
            primary = "industry"
        else:
            primary = best_specific[0]
    else:
        primary = "industry"
    
    # secondary: 排除 primary 后得分最高的，且得分 >= 2
    remaining = {k: v for k, v in scores.items() if k != primary}
    secondary = None
    if remaining:
        best_remaining = max(remaining.items(), key=lambda x: x[1])
        if best_remaining[1] >= 2:
            secondary = best_remaining[0]
    
    return primary, secondary


def extract_tags(item, keywords_config):
    """提取实体标签（用 word boundary 防止短词误匹配）"""
    text = f"{item.get('title', '')} {item.get('summary', '')}"
    text_lower = text.lower()
    tags = []
    entity_tags = keywords_config.get("entity_tags", {})
    for tag_list in [entity_tags.get("companies", []), 
                     entity_tags.get("products", []),
                     entity_tags.get("technologies", [])]:
        for tag in tag_list:
            tag_lower = tag.lower()
            # 短词（<=4字符且纯ASCII）用 word boundary
            if len(tag) <= 4 and tag.isascii() and tag.isalpha():
                if re.search(r'\b' + re.escape(tag_lower) + r'\b', text_lower):
                    tags.append(tag)
            else:
                if tag_lower in text_lower:
                    tags.append(tag)
    # 去重保持顺序，最多 5 个
    seen = set()
    unique_tags = []
    for t in tags:
        t_lower = t.lower()
        if t_lower not in seen:
            seen.add(t_lower)
            unique_tags.append(t)
    return unique_tags[:5]


# 二手转载源列表——这些源的内容通常是翻译/整合，我们标记提醒 agent 追溯一手来源
SECONDARY_SOURCES = [
    "IT之家", "IT之家（RSS）", "量子位", "新智元", "CSDN",
    "机器之心",  # 偶尔有原创深度，但转载也多
]


def is_secondary_source(source_name):
    """判断是否为二手转载源"""
    for s in SECONDARY_SOURCES:
        if s in source_name:
            return True
    return False


def generate_recommendation(item):
    """基于标题和摘要生成简短推荐理由（规则式，非 LLM）"""
    title = item.get('title', '')
    summary = item.get('summary', '')
    category = item.get('category', '')
    source = item.get('source', '')
    
    # 根据分类生成推荐模板
    templates = {
        "creation": "关注 AI 如何改变游戏内容生产流程",
        "in-game": "AI 正在重塑玩家的游戏体验",
        "dev-tools": "开发效率提升工具，值得游戏开发者关注",
        "ops": "AI 赋能游戏运营和商业化",
        "industry": "游戏行业 AI 战略动向",
        "research": "前沿研究可能影响未来游戏形态",
    }
    
    # 尝试从内容中提取更具体的理由
    text = f"{title} {summary}".lower()
    
    if "融资" in text or "funding" in text or "投资" in text:
        return "资本看好该方向，行业信号值得关注"
    if "开源" in text or "open source" in text or "mit" in text:
        return "开源项目，团队可直接试用评估"
    if "发布" in text or "launch" in text or "release" in text:
        return "新产品/功能发布，可能影响行业格局"
    if "合作" in text or "partnership" in text:
        return "大厂联手布局，行业风向标"
    if "论文" in text or "paper" in text or "研究" in text:
        return "学术前沿，预示技术走向"
    if "GDC" in text or "SIGGRAPH" in text:
        return "顶级行业会议动态，聚焦前沿趋势"
    if "裁员" in text or "layoff" in text:
        return "行业人事变动，反映 AI 对就业的实际影响"
    
    return templates.get(category, "游戏×AI 领域值得关注的动态")


def url_hash(url):
    """生成 URL 的去重 key（去除 query/fragment/尾部斜杠）"""
    normalized = re.sub(r"[?#].*$", "", url).rstrip("/")
    return hashlib.md5(normalized.encode()).hexdigest()[:12]


def load_pushed_history():
    """加载已推送历史，返回 {url_hash: date_str} 字典"""
    history_path = os.path.join(DATA_DIR, "pushed_history.json")
    if not os.path.exists(history_path):
        return {}
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("items", {})
    except (json.JSONDecodeError, IOError):
        return {}


def save_pushed_history(history_items, new_items):
    """将新推送的条目写入历史，同时清理 >7 天的旧记录"""
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    cutoff = (datetime.now(timezone(timedelta(hours=8))) - timedelta(days=7)).strftime("%Y-%m-%d")

    # 清理超过 7 天的旧记录
    cleaned = {k: v for k, v in history_items.items() if v >= cutoff}

    # 追加本次推送的条目
    for item in new_items:
        h = url_hash(item.get("url", ""))
        if h not in cleaned:
            cleaned[h] = today

    history_path = os.path.join(DATA_DIR, "pushed_history.json")
    data = {
        "last_updated": today,
        "retention_days": 7,
        "count": len(cleaned),
        "items": cleaned
    }
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def dedup_items(items, cross_day=True):
    """去重：单日内 URL+标题去重 + 跨天历史去重"""
    # 加载历史
    history = load_pushed_history() if cross_day else {}

    seen_urls = set()
    seen_titles = []
    deduped = []
    skipped_by_history = 0

    for item in items:
        url = item.get("url", "")
        title = item.get("title", "")
        url_key = re.sub(r"[?#].*$", "", url).rstrip("/")

        # 跨天去重：检查是否在近 7 天内已推送过
        if cross_day and url_hash(url) in history:
            skipped_by_history += 1
            continue

        # 单日内 URL 去重
        if url_key in seen_urls:
            continue
        seen_urls.add(url_key)

        # 标题相似去重（前20字符）
        title_key = re.sub(r"\s+", "", title)[:20]
        if title_key and title_key in seen_titles:
            continue
        if title_key:
            seen_titles.append(title_key)
        deduped.append(item)

    if skipped_by_history > 0:
        print(f"  📋 跨天去重: 排除 {skipped_by_history} 条近7天已推送条目", file=sys.stderr)

    return deduped


def filter_by_time(items, max_age_hours=MAX_AGE_HOURS):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    cutoff_str = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")
    result = []
    for item in items:
        pub = item.get("published_at")
        if pub is None:
            result.append(item)
        elif pub >= cutoff_str:
            result.append(item)
    return result


def main():
    print("🎮 AI Game v2 - 开始抓取游戏×AI 资讯...", file=sys.stderr)
    
    sources_config = load_json(SOURCES_PATH)
    keywords_config = load_json(KEYWORDS_PATH)
    
    all_items = []
    
    # 抓取所有信源
    for source in sources_config.get("sources", []):
        layer = source.get("layer", 2)
        name = source.get("name", "unknown")
        
        if source["type"] == "rss":
            print(f"  📡 [{source.get('tier','?')}] {name}...", file=sys.stderr)
            xml = fetch_url(source["url"])
            items = parse_rss(xml, name)
            # 标记 layer 以便后续过滤
            for item in items:
                item["_layer"] = layer
                item["_tier"] = source.get("tier", "T2")
            print(f"      → {len(items)} 条", file=sys.stderr)
            all_items.extend(items)
        
        elif source["type"] == "api" and "aihot" in source["url"]:
            print(f"  🔥 [{source.get('tier','?')}] {name}...", file=sys.stderr)
            items = fetch_aihot(source.get("queries", ["游戏", "game"]))
            for item in items:
                item["_layer"] = layer
                item["_tier"] = source.get("tier", "T2")
            print(f"      → {len(items)} 条", file=sys.stderr)
            all_items.extend(items)
    
    print(f"\n  📊 原始条目: {len(all_items)}", file=sys.stderr)
    
    # 时间过滤
    all_items = filter_by_time(all_items)
    print(f"  ⏰ 时间过滤后: {len(all_items)}", file=sys.stderr)
    
    # 相关性过滤（按 layer 区分策略）
    relevant = []
    for item in all_items:
        layer = item.get("_layer", 2)
        if is_relevant(item, keywords_config, layer):
            relevant.append(item)
    print(f"  🎯 相关性过滤后: {len(relevant)}", file=sys.stderr)
    
    # 去重
    deduped = dedup_items(relevant)
    print(f"  🔄 去重后: {len(deduped)}", file=sys.stderr)
    
    # 分类 + 标签 + 推荐理由 + 来源标注
    for item in deduped:
        primary, secondary = classify_item(item, keywords_config)
        item["category"] = primary
        item["category_secondary"] = secondary
        item["tags"] = extract_tags(item, keywords_config)
        item["recommendation"] = generate_recommendation(item)
        # 标记是否来自二手源，提示 agent 追溯一手来源
        if is_secondary_source(item.get("source", "")):
            item["source_type"] = "secondary"
            item["trace_note"] = "此条来自聚合/转载媒体，建议追溯原始来源后再展示"
        else:
            item["source_type"] = "primary"
        # 清理内部字段
        item.pop("_layer", None)
        item.pop("_tier", None)
    
    # 按时间排序
    deduped.sort(key=lambda x: x.get("published_at") or "", reverse=True)
    
    # 输出
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    output = {
        "date": today,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_count": len(deduped),
        "items": deduped,
        "stats": {
            "raw_count": len(all_items),
            "after_relevance_filter": len(relevant),
            "after_dedup": len(deduped),
            "by_category": {}
        }
    }
    for item in deduped:
        cat = item.get("category", "unknown")
        output["stats"]["by_category"][cat] = output["stats"]["by_category"].get(cat, 0) + 1
    
    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, f"{today}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # 保存推送历史（用于跨天去重）
    history = load_pushed_history()
    save_pushed_history(history, deduped)

    print(f"\n  ✅ 完成！共 {len(deduped)} 条，写入 {output_path}", file=sys.stderr)
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
