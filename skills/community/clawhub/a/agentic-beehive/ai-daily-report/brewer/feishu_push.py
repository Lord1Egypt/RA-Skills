#!/usr/bin/env python3
"""
飞书卡片日报推送 — 把酿蜜结果推送到洪亮的飞书
"""
import json
import os
import sys
import re
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).parent.parent
SEND_CARD_SCRIPT = Path.home() / ".openclaw/workspace/scripts/send_feishu_card.py"
OUTPUT_DIR = PROJECT_ROOT / "output"

# 洪亮的 open_id
HONGLIANG_OPEN_ID = "ou_fed42d91849c37358ce2846958544e3e"


def build_ranking_card(rankings: list, garden_data: dict = None) -> tuple:
    """构建综合排名飞书卡片"""
    today = date.today().isoformat()
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.today().weekday()]
    
    title = f"🐝 AI 市场日报 — {today} {weekday_cn}"
    
    # 构建卡片内容
    lines = []
    
    # 花园态势摘要
    if garden_data:
        vendors = garden_data.get("vendors", {})
        sorted_v = sorted(vendors.values(), key=lambda x: x.get("bloom_score", 0), reverse=True)
        bloom_line = " ".join(
            f"{'🌺' if v['bloom_score']>=0.7 else '🌸' if v['bloom_score']>=0.4 else '🌷'}{v['name']}"
            for v in sorted_v[:8]
        )
        lines.append(f"**🌸 花园** {bloom_line}")
        lines.append("")
    
    # Top 10 排名
    lines.append("**🏆 综合排名 Top 10**")
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for r in rankings[:10]:
        m = medals.get(r["rank"], f"`{r['rank']}.`")
        model = r.get("model", "?")
        vendor = r.get("vendor", "?")
        score = r.get("composite_score", 0)
        inp = r.get("input_price", 0)
        outp = r.get("output_price", 0)
        lines.append(f"{m} **{model}** ({vendor}) {score:.3f}  ¥{inp}/{outp}")
    
    lines.append("")
    
    # 性价比 Top 5
    ce_sorted = sorted(rankings, key=lambda x: x.get("ce_raw", 0), reverse=True)
    lines.append("**💰 性价比 Top 5**")
    for i, r in enumerate(ce_sorted[:5], 1):
        lines.append(f"{i}. **{r['model']}** CE={r.get('ce_raw',0):.2f} ({r.get('vendor','')})")
    
    lines.append("")
    lines.append(f"_蜂巢自动感知·采蜜·酿蜜 | {len(rankings)} 模型评测_")
    
    content = "\n".join(lines)
    return title, content


def build_news_card(forage_data: dict) -> tuple:
    """构建新闻动态飞书卡片"""
    today = date.today().isoformat()
    title = f"📰 AI 厂商动态 — {today}"
    
    lines = []
    news = forage_data.get("news", {})
    
    for vendor, data in news.items():
        status = data.get("status", "")
        if not status.startswith("ok"):
            continue
        headlines = data.get("headlines", [])
        if headlines:
            lines.append(f"**{vendor}**")
            for h in headlines[:3]:
                t = h.get("title", "").strip()
                if t and len(t) > 5:
                    lines.append(f"- {t[:80]}")
            lines.append("")
    
    if not lines:
        content = "_今日无显著新闻_"
    else:
        content = "\n".join(lines)
    
    return title, content


def send_card(receive_id: str, title: str, content_md: str, template: str = "orange"):
    """调用飞书发卡脚本"""
    import subprocess
    
    # 限制内容长度（飞书卡片有上限）
    if len(content_md) > 4000:
        content_md = content_md[:3900] + "\n\n_...内容过长，已截断_"
    
    result = subprocess.run(
        [sys.executable, str(SEND_CARD_SCRIPT), receive_id, title, content_md, template],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stdout.strip(), result.stderr.strip()


def push_daily_report():
    """推送每日 AI 市场日报到飞书"""
    today = date.today().isoformat()
    
    # 加载排名数据
    ranking_path = OUTPUT_DIR / f"ranking_{today}.json"
    if not ranking_path.exists():
        print(f"❌ 排名数据不存在: {ranking_path}")
        return False
    
    with open(ranking_path) as f:
        rankings = json.load(f)
    
    # 加载花园数据
    garden_path = OUTPUT_DIR / f"garden_{today}.json"
    garden_data = None
    if garden_path.exists():
        with open(garden_path) as f:
            garden_data = json.load(f)
    
    # 加载采蜜数据
    forage_path = OUTPUT_DIR / f"forage_{today}.json"
    forage_data = {}
    if forage_path.exists():
        with open(forage_path) as f:
            forage_data = json.load(f)
    
    # 发送排名卡片
    title, content = build_ranking_card(rankings, garden_data)
    ok, out, err = send_card(HONGLIANG_OPEN_ID, title, content, "orange")
    if ok:
        print(f"✅ 排名卡片已推送: {out}")
    else:
        print(f"❌ 排名卡片推送失败: {out} {err}")
    
    # 发送新闻卡片（如果有数据）
    if forage_data.get("news"):
        title2, content2 = build_news_card(forage_data)
        if content2.strip() != "_今日无显著新闻_":
            ok2, out2, err2 = send_card(HONGLIANG_OPEN_ID, title2, content2, "blue")
            if ok2:
                print(f"✅ 新闻卡片已推送: {out2}")
    
    return ok


if __name__ == "__main__":
    push_daily_report()
