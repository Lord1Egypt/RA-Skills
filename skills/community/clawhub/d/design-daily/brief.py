#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brief.py — 调用 DeepSeek 把原始素材提炼成「谈资」格式的设计日报
"""

import os
import json
import re
import logging
import requests

DEEPSEEK_KEY   = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL   = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# ── System Prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """你是一个设计圈里消息很灵通的朋友，每天帮大家盯着设计行业的新鲜事。

你的读者是 UI 设计师和 UX 设计师，他们工作很忙，但对行业新鲜事很好奇。
他们打开这份日报，是因为想找点有意思的事情，在和同事喝咖啡时能聊两句。

你的写作风格：
- 像朋友发微信分享八卦，不是上司在做汇报
- 用「你有没有发现」「说实话挺有意思的」「这个角度蛮新鲜」这类自然口语
- 每条有一个让人「哦！」或者「哈，确实」的落点，就够了
- 绝对不说「你需要学习」「应当反思」「需要警惕」这类有压力的话
- 不预测职业危机，不渲染焦虑，不扮演导师
- 轻松、好奇、有点俏皮，但不刻意搞笑

每条内容的结构：
- 说清楚发生了啥（1句）
- 给一个「有点意思」的角度（1~2句），让读者觉得「哦这样看挺好玩的」
- 不用面面俱到，一个角度抓住就够

全程输出中文，Figma、AI、UX 这类专有名词保留英文即可。

输出格式：严格按以下 JSON，不输出其他任何内容：
{
  "one_liner": "今日一句轻松的话，像朋友发给你的一条消息，30字以内，可以有点俏皮",
  "items": [
    {
      "title": "标题（15字以内，说清楚是什么事，不用感叹号）",
      "what": "发生了什么（1句，说清楚就好）",
      "angle": "一个有点意思的角度（1~2句，口语，不焦虑，有点好奇心）",
      "url": "原文链接",
      "source": "来源",
      "role": "最相关岗位"
    }
  ]
}"""


def build_prompt(
    raw_items          : list[dict],
    roles              : list[str],
    count              : int,
    favorite_designers : list = None,
) -> str:
    roles_str = "、".join(roles)

    # 分成「关注设计师」和「其他」两个区块，让 AI 明确优先级
    priority_items = [it for it in raw_items if it.get("priority")]
    normal_items   = [it for it in raw_items if not it.get("priority")]

    def fmt_item(i, item):
        role_tag = item.get("role", "")
        focus    = item.get("focus", "")
        focus_str = f"（用户关注方向：{focus}）" if focus else ""
        priority_str = "⭐ 用户关注设计师相关 " if item.get("priority") else ""
        lines = [
            f"\n[{i}] {priority_str}{item['title']}",
            f"    来源：{item.get('source', '')} | 标签：{role_tag}{focus_str}",
            f"    摘要：{item.get('snippet', '')}",
            f"    链接：{item.get('url', '')}",
        ]
        return "\n".join(lines)

    news_block = ""
    idx = 1
    if priority_items:
        news_block += "\n── ⭐ 用户关注设计师相关内容（优先考虑选入）──\n"
        for item in priority_items:
            news_block += fmt_item(idx, item)
            idx += 1
    if normal_items:
        news_block += "\n\n── 其他素材 ──\n"
        for item in normal_items:
            news_block += fmt_item(idx, item)
            idx += 1

    # 关注设计师提示语
    fav_hint = ""
    if favorite_designers:
        names = [d.get("name") or d.get("url", "") for d in favorite_designers]
        fav_hint = f"\n- 如果有关于「{'、'.join(names)}」的内容，优先选入，这是读者特别关注的人"

    return f"""今天的读者是：{roles_str}

原始素材共 {len(raw_items)} 条：
{news_block}

请从中挑 {count} 条「说出去有点意思」的内容，提炼成中文日报。
选条原则：
- ⭐ 标注的「用户关注设计师」相关内容优先，只要有料就选进来{fav_hint}
- 优先选和读者岗位（{roles_str}）直接相关的内容
- 如果相关内容不够，可以补充「行业动态」类的通用内容，但不要超过总数的 1/3
- 其次挑「有一点点意外」或「角度比较新鲜」的，跳过老生常谈
- 不选纯产品发布稿、罗列功能、没有观点的条目

role 字段填写规则（严格遵守）：
- role 只能从用户选择的岗位列表中选一个填写：[{roles_str}]
- 无论这条内容是否完全匹配，都必须从这个列表里选最相关的那个
- 绝对不能填列表之外的任何值，包括「行业动态」「所有设计师」等自创标签

输出 JSON："""


def call_deepseek(prompt: str) -> str:
    if not DEEPSEEK_KEY:
        raise EnvironmentError("DEEPSEEK_API_KEY 未设置，请检查环境变量")

    resp = requests.post(
        DEEPSEEK_URL,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model"          : DEEPSEEK_MODEL,
            "messages"       : [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
            "temperature"    : 0.85,
            "max_tokens"     : 2000,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def parse_response(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"无法解析 DeepSeek 返回内容：{raw[:300]}")


def format_brief(data: dict, title: str, date_str: str, roles: list[str]) -> str:
    one_liner  = data.get("one_liner", "")
    items      = data.get("items", [])
    roles_str  = "  ·  ".join(roles)
    valid_tags = set(roles)  # 只允许用户选的岗位，无其他选项

    def normalize_role(role: str) -> str:
        """把 AI 乱填的 role 修正为用户选的岗位"""
        if role in valid_tags:
            return role
        # 模糊匹配：包含某个岗位关键词就用那个
        for r in roles:
            if r in role or role in r:
                return r
        # 兜底：用户只选了一个岗位就用那个，多个岗位取第一个
        return roles[0]

    def truncate_url(url: str, max_len: int = 55) -> str:
        """把长 URL 缩短显示，保留域名和路径首段"""
        if len(url) <= max_len:
            return url
        from urllib.parse import urlparse
        p = urlparse(url)
        base = f"{p.scheme}://{p.netloc}{p.path[:20]}"
        return base + "..."

    lines = []

    # ── 头部 ─────────────────────────────────────────────────────────────────
    lines += [
        f"  {title}  ·  {date_str}",
        f"  {roles_str}",
        f"  {'─' * 42}",
        f"  {one_liner}",
        "",
    ]

    # ── 每条内容 ──────────────────────────────────────────────────────────────
    for i, item in enumerate(items, 1):
        num    = f"{i:02d}"
        t      = item.get("title", "")
        what   = item.get("what", "")
        angle  = item.get("angle", "")
        source = item.get("source", "")
        role   = normalize_role(item.get("role", ""))
        url    = item.get("url", "")

        # 标题行：编号 + 标题 + 岗位 tag
        role_tag = f"[{role}]" if role else ""
        lines.append(f"  {num}  {t}  {role_tag}")

        # 事实层（灰色用缩进区隔）
        lines.append(f"      {what}")
        lines.append("")

        # 洞察层（竖线前缀模拟左侧线）
        # 长文本自动换行（按 34 字符折行）
        angle_words = angle
        chunk_size  = 34
        angle_lines = []
        while len(angle_words) > chunk_size:
            # 在 chunk_size 附近找最近的中文句末或空格
            cut = chunk_size
            for c in range(chunk_size, max(chunk_size - 8, 0), -1):
                if angle_words[c] in "，。、！？ ":
                    cut = c + 1
                    break
            angle_lines.append(angle_words[:cut].strip())
            angle_words = angle_words[cut:].strip()
        if angle_words:
            angle_lines.append(angle_words)

        for j, al in enumerate(angle_lines):
            prefix = "  ┃  " if j == 0 else "     "
            lines.append(f"{prefix}{al}")

        lines.append("")

        # 来源行
        src_str = f"  {source}"
        if url:
            src_str += f"  →  {truncate_url(url)}"
        lines.append(src_str)

        # 条目间分隔（最后一条不加）
        if i < len(items):
            lines.append(f"  {'╌' * 42}")
        lines.append("")

    # ── 延伸阅读 ──────────────────────────────────────────────────────────────
    urls = [(it.get("title", ""), it.get("url", "")) for it in items if it.get("url")]
    if urls:
        lines += [f"  {'─' * 42}", "  延伸阅读"]
        for t, u in urls:
            lines.append(f"  · {t}")
            lines.append(f"    {u}")
        lines.append(f"  {'─' * 42}")

    return "\n".join(lines)


def generate_brief(
    raw_items          : list[dict],
    roles              : list[str],
    count              : int,
    title              : str,
    date_str           : str,
    favorite_designers : list = None,
) -> tuple[str, dict]:
    prompt = build_prompt(raw_items, roles, count, favorite_designers or [])

    logging.info(f"🤖 调用 DeepSeek 生成日报（岗位：{'、'.join(roles)}）...")
    raw_output = call_deepseek(prompt)
    data = parse_response(raw_output)

    text = format_brief(data, title, date_str, roles)
    logging.info(f"✅ 日报生成完成，共 {len(data.get('items', []))} 条")
    return text, data
