#!/usr/bin/env python3
"""
毛泽东文章深度生成模块 v2
调用 DeepSeek API 生成高质量文章解读
OpenClaw 专用版：结构化提取 + 深度对齐 + 核心摘抄
"""

import os
import httpx
import json
import logging
from typing import Dict, Optional

logger = logging.getLogger("daily_maoxuan_article")

# DeepSeek API 配置 — API key 从环境变量读取
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = "deepseek-v4-flash"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"


# 【OpenClaw 专用文章协议】
ARTICLE_PROMPT_SCHEMA = """你是精通毛泽东思想的研究员，擅长将历史文献转化为具备现代行动指南意义的结构化报告。

请针对以下《毛泽东选集》文章进行深度解析。

【输出格式 - 严格遵守】

## 1. 📑 核心摘抄 (The Source)
从原文中精选 3-5 段最具震慑力、最核心的论点原话。

## 2. ⚡ 破局点 (Historical Context)
- 当时面临的"死局"是什么？
- 毛主席通过这篇文章要拆解哪个具体的矛盾？
- 如果不写这篇文章，后果推演（量化代价）

## 3. 🎯 唯一判定标准 (The Key Logic)
提取文中定义的"试金石"或"分水岭"逻辑。

## 4. 🛠️ 现代行动指南 (Modern Action)
拒绝空谈，将文章逻辑映射到：职场进阶、团队管理或个人成长。
提供 1 条具体的"今日行动清单"。

## 5. 🔍 辩证反思 (Critical Thinking)
- 纠正对本文最常见的"廉价误读"
- 阐述该理论在现代应用时的边界条件

## 6. 📊 结果验证 (Results)
列举该思想落地后的历史实证数据（可量化）

【输出要求】
- 字数：1500-2500字
- 必须包含原文摘抄（3-5段）
- 史料密度：必须包含具体人物、事件、数据
- 每章必须有实质性内容（至少50字）"""


def generate_article_deep_analysis(title: str, date: str, background: str) -> Optional[Dict[str, str]]:
    """调用 DeepSeek API 生成文章深度解读"""

    prompt = f"""{ARTICLE_PROMPT_SCHEMA}

---

文章标题：{title}
写作日期：{date}

原文背景简述：
{background}

请按协议要求生成深度解读，包含完整6个章节，每章至少50字。"""

    try:
        logger.info(f"调用 DeepSeek API 生成文章深度解读（OpenClaw版）：{title}")
        resp = httpx.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000,
                "temperature": 0.7
            },
            timeout=120.0
        )

        if resp.status_code != 200:
            logger.error(f"DeepSeek API 错误: {resp.status_code} {resp.text}")
            return None

        result = resp.json()
        content = result['choices'][0]['message']['content']
        logger.info(f"文章深度解读生成成功，长度: {len(content)} 字")

        return parse_article_content(content)

    except httpx.TimeoutException:
        logger.error("DeepSeek API 超时")
        return None
    except Exception as e:
        logger.error(f"DeepSeek API 异常: {e}")
        return None


def parse_article_content(content: str) -> Dict[str, str]:
    """
    解析生成的文章内容，提取各部分
    健壮版本：按顺序匹配章节标题
    """
    sections = {
        "quotes": "",
        "breakthrough": "",
        "key_logic": "",
        "modern_action": "",
        "reflection": "",
        "results": ""
    }

    # 定义章节关键词（按优先级排序）
    section_keywords = {
        "quotes": ["核心摘抄", "摘抄"],
        "breakthrough": ["破局点", "死局"],
        "key_logic": ["唯一判定标准", "判定标准", "试金石"],
        "modern_action": ["现代行动指南", "行动指南", "今日行动"],
        "reflection": ["辩证反思", "反思", "误读"],
        "results": ["结果验证", "验证", "数据"]
    }

    lines = content.split('\n')
    current_section = None
    current_content = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # 只有以 ## 开头的行才可能是章节标题
        is_header = line_stripped.startswith('##') and not line_stripped.startswith('-') and not line_stripped.startswith('*')
        
        if not is_header:
            if current_section:
                current_content.append(line_stripped)
            continue

        # 检测章节标题
        clean_line = line_stripped.lstrip('#').strip()
        matched_section = None

        for section_name, keywords in section_keywords.items():
            for keyword in keywords:
                if keyword in clean_line:
                    matched_section = section_name
                    break
            if matched_section:
                break

        if matched_section:
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = matched_section
            current_content = []

    # 保存最后一个章节
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def create_article_document(title: str, date: str, background: str,
                             deep: Dict[str, str], output_date: str) -> str:
    """创建文章深度解读文档"""
    from datetime import datetime

    template = """# 每日毛选文章 - {output_date}

## 文章信息
- **标题**：{title}
- **写作日期**：{date}
- **标签**：#毛选研读 #每日推送

## 原文背景
{background}

---

## 1. 📑 核心摘抄
{quotes}

---

## 2. ⚡ 破局点
{breakthrough}

---

## 3. 🎯 唯一判定标准
{key_logic}

---

## 4. 🛠️ 现代行动指南
{modern_action}

---

## 5. 🔍 辩证反思
{reflection}

---

## 6. 📊 结果验证
{results}

---
*自动生成于 {generate_time}*
*由 OpenClaw + DeepSeek 提供支持*
"""

    return template.format(
        title=title,
        date=date,
        background=background,
        output_date=output_date,
        quotes=deep.get('quotes', ''),
        breakthrough=deep.get('breakthrough', ''),
        key_logic=deep.get('key_logic', ''),
        modern_action=deep.get('modern_action', ''),
        reflection=deep.get('reflection', ''),
        results=deep.get('results', ''),
        generate_time=datetime.now().strftime("%Y-%m-%d %H:%M")
    )


def format_article_telegram_message(title: str, date: str, deep: Dict[str, str], output_date: str) -> str:
    """格式化文章 Telegram 消息"""
    def truncate(text, length=280):
        if len(text) <= length:
            return text
        return text[:length] + "..."

    msg = f"""📚 <b>每日毛选文章</b> | {output_date}

━━━━━━━━━━━━━━━━━━

<b>{title}</b>
📅 {date}

━━━━━━━━━━━━━━━━━━

📑 <b>核心摘抄</b>
{truncate(deep.get('quotes', ''))}

━━━━━━━━━━━━━━━━━━

⚡ <b>破局点</b>
{truncate(deep.get('breakthrough', ''))}

━━━━━━━━━━━━━━━━━━

🎯 <b>唯一判定标准</b>
{truncate(deep.get('key_logic', ''))}

━━━━━━━━━━━━━━━━━━

🛠️ <b>今日行动</b>
{truncate(deep.get('modern_action', ''))}

━━━━━━━━━━━━━━━━━━

🔍 <b>辩证反思</b>
{truncate(deep.get('reflection', ''))}

━━━━━━━━━━━━━━━━━━

📊 <b>结果验证</b>
{truncate(deep.get('results', ''))}

━━━━━━━━━━━━━━━━━━

<i>完整深度解读请查看 Obsidian 文档</i>"""

    return msg


if __name__ == "__main__":
    # 测试解析
    logging.basicConfig(level=logging.INFO)

    test_content = """
## 1. 📑 核心摘抄
- "集中优势兵力、各个歼灭敌人的原则，是我军从开始建军起十余年以来的优良传统。"
- "在战役的部署方面，当着敌人使用许多个旅（或团）分路前进的时候，我军必须集中绝对优势的兵力。"

## 2. ⚡ 破局点
破局点在于打破"均衡对抗"的惯性思维，将"力"的分配从"均分"转向"局部绝对优势"。

## 3. 🎯 唯一判定标准
唯一判定标准是：是否实现了"全歼"和"速决"的双重效果。

## 4. 🛠️ 现代行动指南
在个人项目管理中，列出当前所有任务，识别出最关键的"一个旅"。

## 5. 🔍 辩证反思
常见的误读是：将"集中优势兵力"等同于"盲目大兵团作战"。

## 6. 📊 结果验证
- 淮海战役第一阶段：华东野战军以10个纵队约30万人集中攻击黄百韬兵团约10万人。
- 解放战争头8个月：我军共歼敌正规军66个旅（约71万人）。
"""

    result = parse_article_content(test_content)
    print("=== 解析测试 ===")
    for k, v in result.items():
        print(f"{k}: {len(v)}字")
        if v:
            print(f"  内容: {v[:60]}...")