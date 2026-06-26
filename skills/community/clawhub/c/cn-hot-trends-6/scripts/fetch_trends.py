#!/usr/bin/env python3
"""
中文全平台热搜聚合 - cn-hot-trends
支持：知乎、微博、百度、B站、抖音、头条
AI选题推荐 + 内容角度分析

用法:
  python3 fetch_trends.py                    # 全平台热搜
  python3 fetch_trends.py --platform zhihu  # 单平台
  python3 fetch_trends.py --limit 10         # 每平台条数
  python3 fetch_trends.py --recommend        # AI选题推荐
  python3 fetch_trends.py --json             # JSON输出
"""

import json
import os
import sys
import ssl
import argparse
import time
import re
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# SSL 配置：优先标准验证，失败才降级
_SAFE_SSL_CTX = ssl.create_default_context()

def _urlopen(req, timeout=10):
    """优先标准SSL，失败自动降级"""
    try:
        return urlopen(req, timeout=timeout, context=_SAFE_SSL_CTX)
    except URLError as e:
        reason = getattr(e, 'reason', None)
        if isinstance(reason, (ssl.SSLError, ssl.SSLCertVerificationError)):
            return urlopen(req, timeout=timeout, context=ssl.create_default_context())
        raise
    except Exception as e:
        if 'SSL' in str(type(e).__name__) or 'SSL' in str(e):
            return urlopen(req, timeout=timeout, context=ssl.create_default_context())
        raise

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


# ========== 知乎热榜 ==========

def fetch_zhihu(limit=10):
    """抓取知乎热榜"""
    url = "https://api.zhihu.com/topstory/hot-lists/total?limit={}".format(limit)
    try:
        req = Request(url, headers=HEADERS)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 知乎抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    for item in data.get("data", []):
        target = item.get("target", {})
        title = target.get("title", "").strip()
        if not title:
            continue
        detail = item.get("detail_text", "")
        heat_num = 0
        try:
            if "万" in detail:
                heat_num = float(detail.replace("万热度", "").replace("万", "").strip()) * 10000
            elif "热度" in detail:
                heat_num = int(re.sub(r"\D", "", detail))
        except (ValueError, AttributeError):
            pass

        results.append({
            "title": title,
            "platform": "知乎",
            "emoji": "💬",
            "heat": int(heat_num),
            "heat_display": detail,
            "url": "https://www.zhihu.com/question/{}".format(target.get("id", "")),
            "category": "",
            "excerpt": (target.get("excerpt", "") or "")[:80]
        })
    return results


# ========== 微博热搜 ==========

def fetch_weibo(limit=10):
    """抓取微博热搜"""
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {**HEADERS, "Referer": "https://weibo.com/"}
    try:
        req = Request(url, headers=headers)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 微博热搜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    realtime = data.get("data", {}).get("realtime", [])
    for item in realtime[:limit]:
        note = item.get("note", "").strip()
        if not note:
            continue
        label = item.get("label_name", "")
        if label:
            note = "[{}] {}".format(label, note)
        results.append({
            "title": note,
            "platform": "微博",
            "emoji": "🌐",
            "heat": int(item.get("num", 0)),
            "heat_display": str(item.get("num", 0)),
            "url": "https://s.weibo.com/weibo?q=%23{}%23".format(
                item.get("word", item.get("note", ""))),
            "category": item.get("label_name", ""),
            "excerpt": ""
        })
    return results


# ========== 百度热搜 ==========

def fetch_baidu(limit=10):
    """抓取百度热搜"""
    url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
    try:
        req = Request(url, headers=HEADERS)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 百度热搜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    cards = data.get("data", {}).get("cards", [])
    if cards:
        content = cards[0].get("content", [])
        for item in content[:limit]:
            query = item.get("query", "").strip()
            if not query:
                continue
            heat_num = 0
            try:
                heat_num = int(item.get("hotScore", 0))
            except (ValueError, TypeError):
                pass
            results.append({
                "title": query,
                "platform": "百度",
                "emoji": "🔍",
                "heat": heat_num,
                "heat_display": item.get("desc", "")[:30],
                "url": "https://www.baidu.com/s?wd={}".format(query),
                "category": item.get("tag", ""),
                "excerpt": item.get("desc", "")[:80]
            })
    return results


# ========== B站排行榜 ==========

def fetch_bilibili(limit=10):
    """抓取B站排行榜"""
    url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
    try:
        req = Request(url, headers=HEADERS)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ B站排行榜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    items = data.get("data", {}).get("list", [])
    for item in items[:limit]:
        title = item.get("title", "").strip()
        if not title:
            continue
        stat = item.get("stat", {})
        results.append({
            "title": title,
            "platform": "B站",
            "emoji": "📺",
            "heat": int(stat.get("view", 0)),
            "heat_display": "{}播放".format(_format_num(stat.get("view", 0))),
            "url": item.get("short_link_v2", "https://www.bilibili.com/video/{}".format(item.get("bvid", ""))),
            "category": item.get("tname", ""),
            "excerpt": item.get("description", "")[:80] if item.get("description") else ""
        })
    return results


# ========== 抖音热榜 ==========

def fetch_douyin(limit=10):
    """抓取抖音热榜"""
    url = "https://www.douyin.com/aweme/v1/web/general/search/single/?keyword_type=0&count={}&device_platform=webapp&aid=6383".format(limit)
    headers = {
        **HEADERS,
        "Referer": "https://www.douyin.com/",
        "Cookie": ""
    }
    try:
        req = Request(url, headers=headers)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 抖音热榜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    try:
        items = data.get("data", []) or []
    except (KeyError, TypeError):
        return []
    
    for item in items[:limit]:
        aweme = item.get("aweme_info", {}) or item
        title = (aweme.get("desc", "") or "").strip()
        if not title:
            continue
        stat = aweme.get("statistics", {})
        results.append({
            "title": title,
            "platform": "抖音",
            "emoji": "🎵",
            "heat": int(stat.get("digg_count", 0)),
            "heat_display": "{}赞".format(_format_num(stat.get("digg_count", 0))),
            "url": "https://www.douyin.com/video/{}".format(aweme.get("aweme_id", "")),
            "category": "",
            "excerpt": ""
        })
    return results


# ========== 头条热榜 ==========

def fetch_toutiao(limit=10):
    """抓取今日头条热榜"""
    url = "https://www.toutiao.com/api/pc/feed/?tab_name=hot_board&catego ry=热点&max_behot_time=0&keep_items=[]&category=hot_board"
    headers = {
        **HEADERS,
        "Referer": "https://www.toutiao.com/",
    }
    try:
        req = Request(url, headers=headers)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 头条热榜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    try:
        items = data.get("data", [])
    except (KeyError, TypeError):
        return []

    for item in items[:limit]:
        title = (item.get("title", "") or "").strip()
        if not title:
            continue
        results.append({
            "title": title,
            "platform": "头条",
            "emoji": "📰",
            "heat": int(item.get("hot_score", 0)),
            "heat_display": "",
            "url": item.get("article_url", "") or "https://www.toutiao.com/",
            "category": "",
            "excerpt": (item.get("abstract", "") or "")[:80]
        })
    return results


# ========== 工具函数 ==========

def _format_num(n):
    n = int(n)
    if n >= 100000000:
        return "{:.1f}亿".format(n / 100000000)
    elif n >= 10000:
        return "{:.1f}万".format(n / 10000)
    elif n >= 1000:
        return "{:.1f}k".format(n / 1000)
    return str(n)


# ========== AI选题推荐 ==========

PLATFORM_TIPS = {
    "知乎": {
        "style": "专业分析文/问答视角",
        "tags": ["职场", "科技", "财经", "心理"],
        "angle": "给背景、给分析、给结论",
        "format": "800-1500字深度文"
    },
    "微博": {
        "style": "短平快观点输出",
        "tags": ["吃瓜", "热点", "社会"],
        "angle": "一句话立场 + 3个理由",
        "format": "100-300字观点"
    },
    "百度": {
        "style": "知识科普向",
        "tags": ["科普", "揭秘", "指南"],
        "angle": "解释是什么、为什么",
        "format": "500-800字科普"
    },
    "B站": {
        "style": "视频/深度内容",
        "tags": ["测评", "盘点", "教程"],
        "angle": "视频封面 + 前3秒钩子",
        "format": "视频脚本框架"
    },
    "抖音": {
        "style": "短视频/视觉冲击",
        "tags": ["反差", "猎奇", "共鸣"],
        "angle": "情绪共鸣 + 视觉冲击",
        "format": "60秒以内脚本"
    },
    "头条": {
        "style": "资讯类/资讯号",
        "tags": ["资讯", "解读", "快报"],
        "angle": "5W1H框架：是什么-为什么-影响",
        "format": "300-500字资讯文"
    }
}

CATEGORY_ANGLES = {
    "科技": ["产品测评", "技术解读", "行业分析", "创始人故事"],
    "社会": ["事件还原", "各方反应", "深层原因", "后续影响"],
    "职场": ["权益解读", "生存指南", "心理建设", "案例分析"],
    "财经": ["数据解读", "市场分析", "个人应对", "投资建议"],
    "娱乐": ["深度八卦", "作品分析", "行业观察", "粉丝视角"],
    "体育": ["赛事复盘", "人物故事", "战术分析", "幕后花絮"],
    "健康": ["科学解读", "辟谣", "实操建议", "专家视角"],
    "教育": ["政策解读", "实操指南", "家长视角", "过来人经验"],
    "默认": ["事件还原", "各方观点", "深层原因", "未来预测", "个人启示"]
}

def suggest_topics(items):
    """基于热搜数据生成AI选题建议"""
    if not items:
        return "⚠️ 无数据可选，请先抓取热搜"

    lines = []
    lines.append("\n" + "=" * 60)
    lines.append("📌 AI选题推荐")
    lines.append("=" * 60)

    top_items = sorted(items, key=lambda x: x.get("heat", 0), reverse=True)[:10]

    for i, item in enumerate(top_items, 1):
        title = item["title"]
        platform = item.get("platform", "")
        heat = item.get("heat_display", "")

        lines.append("\n{}. {} {}".format(i, title, heat))

        # 识别话题类别
        categories = _detect_category(title)
        if not categories:
            categories = ["默认"]

        for cat in categories:
            tips = PLATFORM_TIPS.get(platform, PLATFORM_TIPS["知乎"])
            angles = CATEGORY_ANGLES.get(cat, CATEGORY_ANGLES["默认"])

            lines.append("   📍 平台: {} | {} | {}".format(
                platform, tips["style"], tips["angle"]))
            lines.append("   🎯 可写角度: " + " / ".join(angles[:3]))

            # 给出一个具体标题建议
            suggested_title = _generate_title(title, cat, platform)
            lines.append("   📝 建议标题:「{}」".format(suggested_title))
            break

    lines.append("\n" + "-" * 60)
    lines.append("💡 使用方式：")
    lines.append("   选一个角度 + 一个平台 → 开始写作")
    lines.append("   输入「写知乎回答：标题」直接生成内容")

    return "\n".join(lines)


def _detect_category(title):
    """从标题识别话题类别"""
    title_lower = title.lower()
    cats = []
    keywords = {
        "科技": ["ai", "chatgpt", "openai", "手机", "电脑", "互联网", "腾讯", "阿里", "字节", "华为", "芯片", "手机", "智能", "软件", "苹果"],
        "社会": ["热搜", "网红", "社会", "事件", "报警", "拘", "判", "虐", "争议"],
        "职场": ["职场", "裁员", "工资", "加班", "辞职", "领导", "同事", "求职", "招聘"],
        "财经": ["股价", "上市", "融资", "经济", "市场", "投资", "基金", "股票", "理财", "cpi", "通胀", "降息"],
        "娱乐": ["明星", "电影", "电视剧", "综艺", "演唱会", "偶像", "粉丝", "红毯"],
        "体育": ["比赛", "奥运", "足球", "篮球", "冠军", "赛", "队", "球员"],
        "健康": ["健康", "医生", "医院", "疾病", "养生", "减肥", "睡眠"],
        "教育": ["学校", "考试", "学生", "老师", "大学", "高考", "留学", "教育"],
    }
    for cat, words in keywords.items():
        if any(w in title_lower for w in words):
            cats.append(cat)
    return cats if cats else ["默认"]


def _generate_title(topic, category, platform):
    """生成建议标题"""
    templates = {
        "知乎": [
            "「{}」这件事，普通人该怎么看？",
            "关于「{}」，我从3个角度拆解",
            "深度：为什么「{}」值得认真讨论",
            "关于「{}」，说几句实话"
        ],
        "微博": [
            "说个关于「{}」的暴论",
            "「{}」这件事，我站这边",
            "关于「{}」，不吐不快"
        ],
        "小红书": [
            "「{}」后，我总结了3条",
            "关于「{}」，普通人的真实感受",
            "刚刷到「{}」，说说我的看法"
        ],
        "头条": [
            "关于「{}」，你需要知道的几件事",
            "深度解读：「{}」意味着什么",
            "关于「{}」，最新进展来了"
        ],
        "B站": [
            "关于「{}」，一期说透",
            "「{}」背后，藏着什么",
            "关于「{}」，看完你就明白了"
        ],
        "抖音": [
            "关于「{}」，说几句",
            "「{}」这件事，我有话说",
            "刚看到的「{}」，聊聊"
        ]
    }
    import random
    templates_for_platform = templates.get(platform, templates["头条"])
    template = templates_for_platform[hash(topic) % len(templates_for_platform)]
    short_topic = topic[:15] + "..." if len(topic) > 15 else topic
    return template.format(short_topic)


# ========== 报告打印 ==========

def print_report(items, recommend=False):
    """打印热点报告"""
    if not items:
        print("\n📭 未抓取到热点数据")
        return

    # 按平台分组
    by_platform = {}
    for item in items:
        p = item.get("platform", "其他")
        by_platform.setdefault(p, []).append(item)

    total = len(items)
    top = sorted(items, key=lambda x: x.get("heat", 0), reverse=True)

    print("\n" + "🔥" * 18)
    print("  今日全平台热搜速览 | {} 条数据".format(total))
    print("🔥" * 18)

    platform_emojis = {
        "知乎": "💬", "微博": "🌐", "百度": "🔍",
        "B站": "📺", "抖音": "🎵", "头条": "📰"
    }

    for platform, topics in by_platform.items():
        emoji = platform_emojis.get(platform, "📌")
        print("\n{} {} | {}条".format(emoji, platform, len(topics)))
        for i, t in enumerate(topics[:10], 1):
            title = t["title"][:36]
            heat = t.get("heat_display", "")
            cat = t.get("category", "")
            print("  {}. {} {}".format(i, title, "🔥" + heat if heat else ""))
            if cat:
                print("     🏷️ {}".format(cat))

    # 热度总榜
    print("\n📊 全平台热度总榜 TOP 10")
    print("-" * 50)
    for i, t in enumerate(top_items := sorted(items, key=lambda x: x.get("heat", 0), reverse=True)[:10], 1):
        emoji = platform_emojis.get(t["platform"], "📌")
        heat = t.get("heat_display", "")
        print("  {}. {}{} {}{}".format(
            i, emoji, t["title"][:32], " 🔥" if heat else "", heat))

    if recommend:
        print(suggest_topics(items))


# ========== 主入口 ==========

FETCHERS = {
    "zhihu": fetch_zhihu,
    "weibo": fetch_weibo,
    "baidu": fetch_baidu,
    "bilibili": fetch_bilibili,
    "douyin": fetch_douyin,
    "toutiao": fetch_toutiao,
}

PLATFORM_NAMES = {
    "zhihu": "知乎", "weibo": "微博", "baidu": "百度",
    "bilibili": "B站", "douyin": "抖音", "toutiao": "头条",
    "all": "全部平台"
}


def main():
    parser = argparse.ArgumentParser(description="🔥 中文全平台热搜聚合")
    parser.add_argument("--platform", "-p",
                        choices=list(FETCHERS.keys()) + ["all"],
                        default="all",
                        help="抓取平台（默认全部）")
    parser.add_argument("--limit", "-n", type=int, default=10,
                        help="每个平台抓取条数（默认10）")
    parser.add_argument("--recommend", "-r", action="store_true",
                        help="显示AI选题推荐")
    parser.add_argument("--json", action="store_true",
                        help="输出 JSON 格式")
    args = parser.parse_args()

    if args.platform == "all":
        platforms = list(FETCHERS.keys())
    else:
        platforms = [args.platform]

    all_items = []
    success_count = 0
    for name in platforms:
        display_name = PLATFORM_NAMES.get(name, name)
        print("📡 抓取 {}...".format(display_name), file=sys.stderr)
        start = time.time()
        try:
            items = FETCHERS[name](args.limit)
            elapsed = time.time() - start
            if items:
                print("  ✅ {} 条 ({:.1f}s)".format(len(items), elapsed), file=sys.stderr)
                all_items.extend(items)
                success_count += 1
            else:
                print("  ⚠️ 无数据", file=sys.stderr)
        except Exception as e:
            print("  ⚠️ 失败: {}".format(e), file=sys.stderr)

    all_items.sort(key=lambda x: x.get("heat", 0), reverse=True)

    if args.json:
        print(json.dumps(all_items, ensure_ascii=False, indent=2))
    else:
        print_report(all_items, recommend=args.recommend)

    print("\n✅ 抓取完成 | {}平台有数据".format(success_count), file=sys.stderr)


if __name__ == "__main__":
    main()
