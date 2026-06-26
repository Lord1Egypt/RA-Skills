#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch.py — 用 Serper 搜索设计领域最新内容
支持：岗位定制 / 时间过滤 / 实时发现热门设计师 / 用户自定义关注人物
"""

import os
import logging
import requests

SERPER_KEY = os.environ.get("SERPER_API_KEY", "")
SERPER_URL = "https://google.serper.dev/search"

# ── 时间范围 → Serper tbs 参数 ────────────────────────────────────────────────
TIME_RANGE_TBS = {
    "24h": "qdr:d",
    "2d" : "qdr:d2",
    "3d" : "qdr:d3",
    "1w" : "qdr:w",
    "2w" : "qdr:d14",
    "1m" : "qdr:m",
}

# ── 岗位 → 搜索词 ─────────────────────────────────────────────────────────────
ROLE_QUERIES = {
    "UI设计师": [
        "UI design trends latest",
        "Figma component design system update",
        "mobile UI pattern best practice",
    ],
    "UX设计师": [
        "UX design case study latest",
        "user experience research insight",
        "UX flow wireframe decision",
    ],
    "视觉设计师": [
        "visual design trend latest",
        "brand identity design case study",
        "typography color system design",
    ],
    "交互设计师": [
        "interaction design pattern latest",
        "microinteraction animation UX",
        "IxD prototyping tool update",
    ],
    "服务设计师": [
        "service design blueprint case study",
        "customer journey map tool latest",
        "service design system thinking",
    ],
    "设计系统工程师": [
        "design system token component latest",
        "Figma variables design token update",
        "design system engineering scalable",
    ],
    "动效设计师": [
        "motion design UI animation latest",
        "Lottie After Effects design workflow",
        "microanimation UX principle",
    ],
    "内容设计师": [
        "UX writing content design latest",
        "microcopy error message pattern",
        "content strategy product design",
    ],
    "可访问性设计师": [
        "accessibility design WCAG latest",
        "inclusive design tool update",
        "a11y UX audit best practice",
    ],
    "用户研究员": [
        "user research method latest",
        "UX research insight synthesis",
        "qualitative quantitative research design",
    ],
    "增长设计师": [
        "growth design conversion UX latest",
        "onboarding design funnel optimization",
        "A/B test design experiment",
    ],
    "产品设计师": [
        "product design decision latest",
        "top product UX breakdown analysis",
        "product designer AI workflow",
    ],
    "AI产品设计师": [
        "AI product design interaction latest",
        "prompt UI design LLM interface",
        "AI UX uncertainty design pattern",
    ],
    "设计工程师": [
        "design engineer frontend latest",
        "Vercel Linear design code intersection",
        "React component design system code",
    ],
    "零界面设计师": [
        "voice UI zero interface design latest",
        "gesture spatial interaction design",
        "conversational UX design pattern",
    ],
    "空间计算设计师": [
        "spatial computing design visionOS latest",
        "3D UI visionOS interface design",
        "AR VR UX design pattern",
    ],
    "产品经理": [
        "product management design collaboration latest",
        "PM UX decision making framework",
        "product strategy design thinking",
    ],
}

# ── 通用行业动态 ──────────────────────────────────────────────────────────────
COMMON_QUERIES = [
    "Figma major update announcement",
    "design tool ProductHunt launch",
    "design industry news",
]

# ── 固定的知名设计圈人物（国际 + 国内头部）───────────────────────────────────
# 这些人更新稳定、内容质量高，作为基础盘保留
KNOWN_INFLUENCER_QUERIES = [
    # 国际
    "Rasmus Andersson design Linear",
    "Frank Chimero design writing",
    "Maggie Appleton AI interface design",
    "Khoi Vinh design opinion",
    "Emil Kowalski design engineer",
    # 国内头部团队
    "腾讯 ISUX 设计",
    "Ant Design 更新",
    "字节跳动 design system",
    "饿了么 UX 设计",
]

# ── 实时发现热门设计师（动态搜索，不依赖硬编码名单）─────────────────────────
# 这组词专门用来找「最近在设计圈突然火了的人或作品」
TRENDING_DESIGNER_QUERIES = [
    # 国内设计圈热点发现
    "设计师 走红 作品 最近",
    "UI设计师 爆款 作品集",
    "国内设计师 刷屏 设计圈",
    "小红书 设计师 爆款",
    "站酷 设计 热门",
    # 国际设计圈热点发现
    "designer viral design community",
    "designer portfolio trending Twitter",
    "design work going viral Dribbble",
    "designer thread viral design Twitter",
    # 设计圈「大事件」发现
    "designer controversy design community debate",
    "design industry drama discussion",
    "设计圈 争议 讨论 热点",
]


# ── Serper 搜索 ───────────────────────────────────────────────────────────────

def serper_search(query: str, num: int = 5, tbs: str = "") -> list[dict]:
    if not SERPER_KEY:
        raise EnvironmentError("SERPER_API_KEY 未设置，请检查环境变量")

    payload = {"q": query, "num": num, "hl": "en", "gl": "us"}
    if tbs:
        payload["tbs"] = tbs

    resp = requests.post(
        SERPER_URL,
        headers={"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"},
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()

    results = []
    for item in resp.json().get("organic", []):
        title = item.get("title", "").strip()
        url   = item.get("link", "").strip()
        if title and url:
            results.append({
                "title"  : title,
                "url"    : url,
                "snippet": item.get("snippet", "").strip(),
                "source" : item.get("source", "").strip(),
            })
    return results


def _relax_tbs(tbs: str) -> str:
    """把时间范围放宽一档，用于人物/热门设计师搜索"""
    relaxed = {
        "qdr:d"  : "qdr:w",
        "qdr:d2" : "qdr:w",
        "qdr:d3" : "qdr:w",
        "qdr:w"  : "qdr:d14",
        "qdr:d14": "qdr:m",
        "qdr:m"  : "qdr:m",
    }
    return relaxed.get(tbs, "qdr:w")


def _build_favorite_queries(favorite_designers: list[dict]) -> list[dict]:
    """
    根据用户配置的关注设计师，生成搜索词 + 标注。
    每个 designer 可以是：
      { "name": "张三", "focus": "品牌设计" }
      { "url": "https://twitter.com/xxx", "focus": "交互设计" }
      { "name": "Diego Hernandez", "url": "https://...", "focus": "" }
    """
    queries = []
    for designer in favorite_designers:
        name  = designer.get("name", "").strip()
        url   = designer.get("url", "").strip()
        focus = designer.get("focus", "").strip()

        label = name or url  # 用于日志显示

        if name:
            # 用名字搜：中文名直接搜，英文名加 design 关键词
            if any('\u4e00' <= c <= '\u9fff' for c in name):
                queries.append({
                    "query": f"{name} 设计 作品 最新",
                    "label": label,
                    "focus": focus,
                })
                queries.append({
                    "query": f"{name} design",
                    "label": label,
                    "focus": focus,
                })
            else:
                queries.append({
                    "query": f"{name} design work latest",
                    "label": label,
                    "focus": focus,
                })
                queries.append({
                    "query": f"{name} designer portfolio",
                    "label": label,
                    "focus": focus,
                })

        if url:
            # 用 URL 域名/用户名提炼搜索词
            # 例如 twitter.com/xxx → 搜索 "xxx designer"
            import re
            handle = re.sub(r'https?://(www\.)?', '', url).rstrip('/')
            handle = handle.split('/')[-1]  # 取最后一段路径
            if handle and handle not in ('', '#'):
                queries.append({
                    "query": f"{handle} design latest",
                    "label": label,
                    "focus": focus,
                })

    return queries


# ── 主抓取函数 ────────────────────────────────────────────────────────────────

def fetch_all(
    roles              : list[str],
    items_per_day      : int  = 3,
    time_range         : str  = "1w",
    favorite_designers : list = None,
) -> list[dict]:
    """
    抓取所有来源的原始素材：
      1. 岗位相关搜索
      2. 通用行业动态
      3. 固定知名人物
      4. 实时热门设计师发现
      5. 用户自定义关注人物（最高优先级，结果置顶）
    """
    if favorite_designers is None:
        favorite_designers = []

    tbs             = TIME_RANGE_TBS.get(time_range, "qdr:w")
    influencer_tbs  = _relax_tbs(tbs)

    logging.info(f"⏱️  时间范围：{time_range}（tbs={tbs}）")

    seen_urls = set()
    all_items = []

    def add_items(items: list[dict], role_tag: str):
        for item in items:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                item.setdefault("role", role_tag)
                all_items.append(item)

    # ── ① 用户自定义关注人物（置顶，优先喂给 AI）────────────────────────────
    if favorite_designers:
        fav_queries = _build_favorite_queries(favorite_designers)
        logging.info(f"⭐ [关注设计师] 搜索 {len(fav_queries)} 组词")
        for q in fav_queries:
            try:
                results = serper_search(q["query"], num=3, tbs=influencer_tbs)
                for item in results:
                    item["role"]  = f"关注：{q['label']}"
                    item["focus"] = q.get("focus", "")
                    item["priority"] = True   # 标记高优先级，brief.py 可感知
                add_items(results, f"关注：{q['label']}")
            except Exception as e:
                logging.warning(f"   搜索失败 [{q['query']}]: {e}")

    # ── ② 岗位相关搜索 ───────────────────────────────────────────────────────
    queries_per_role = 2 if len(roles) > 4 else 3
    for role in roles:
        queries = ROLE_QUERIES.get(role, [])[:queries_per_role]
        logging.info(f"🔍 [{role}] 执行 {len(queries)} 组搜索")
        for query in queries:
            try:
                add_items(serper_search(query, num=4, tbs=tbs), role)
            except Exception as e:
                logging.warning(f"   搜索失败 [{query}]: {e}")

    # ── ③ 通用行业动态 ───────────────────────────────────────────────────────
    logging.info("🔍 [行业动态] 补充通用搜索")
    for query in COMMON_QUERIES:
        try:
            add_items(serper_search(query, num=3, tbs=tbs), "行业动态")
        except Exception as e:
            logging.warning(f"   搜索失败 [{query}]: {e}")

    # ── ④ 固定知名人物 ───────────────────────────────────────────────────────
    logging.info("🔍 [知名设计师] 搜索固定人物动态")
    for query in KNOWN_INFLUENCER_QUERIES:
        try:
            add_items(serper_search(query, num=2, tbs=influencer_tbs), "知名设计师")
        except Exception as e:
            logging.warning(f"   搜索失败 [{query}]: {e}")

    # ── ⑤ 实时热门设计师发现 ─────────────────────────────────────────────────
    # 只取前 5 条热门搜索词（控制 API 用量），覆盖国内外
    logging.info("🔥 [热门发现] 搜索最近在设计圈走红的人/作品")
    for query in TRENDING_DESIGNER_QUERIES[:5]:
        try:
            add_items(serper_search(query, num=3, tbs=influencer_tbs), "热门发现")
        except Exception as e:
            logging.warning(f"   搜索失败 [{query}]: {e}")

    logging.info(f"📦 共抓取 {len(all_items)} 条原始素材，供 AI 精选 {items_per_day} 条")
    return all_items
