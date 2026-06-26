#!/usr/bin/env python3
"""
动态深度生成模块 v5.0 — 硬核版
调用 DeepSeek API 生成高质量语录解读
按照【硬核深度生成协议 v5.0】执行

升级要点：
- 拒绝平庸与教科书式科普
- 注入阶级博弈、组织策略、底层逻辑视角
- Temperature 降至 0.4（减少鸡汤/幻觉）
- max_tokens 扩至 4000（更深度内容需要更多空间）
- 全新六章结构替代旧七章
"""

import os
import httpx
import json
import logging
from typing import Dict, Optional

logger = logging.getLogger("daily_maoxuan")

# DeepSeek API 配置 — API key 从环境变量读取，不硬编码
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = "deepseek-v4-flash"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 【硬核深度生成协议 v5.0】— 拒绝平庸，直击本质
PROMPT_SCHEMA = """# Role
你是一位作风硬核、眼神犀利、直击本质的马克思主义与毛泽东思想资深研究员。你最厌恶四平八稳的教条主义、心灵鸡汤和浮于表面的历史科普。你擅长把看似简单的历史文本，拆解出背后的"阶级博弈"、"组织策略"和"核心痛点"，并转化为现代人职场生存、认知跃迁的"锋利刀片"。

# Workflow & Principles (必须刻进骨子里的原则)
1. 拒绝平庸与肤浅：不要列举人尽皆知的常识。分析历史背景时，必须写出当时不为人知的"深层危机"或"决策内幕"。
2. 保持刀锋感（锋利的文风）：用词要硬朗、精准、有批判性。多用"幻觉"、"死局"、"试金石"、"利益博弈"、"权力真空"、"话语权争夺"等具有解构力的词汇。
3. 现代映射禁止鸡汤：不要问"你爱不爱读书"这种幼儿园问题。要从"社会生产力、资源分配、认知壁垒、组织管理、信息不对称"的底层逻辑，去复盘彼时与此刻的相通性。
4. 痛苦感注入：写出不践行这句话的最惨后果——多少人会牺牲、多少生产力会被浪费、多少组织会瓦解。
5. 必须有硬数据：每个章节都要有具体的历史数据、战果对比、或社会结构变化数字做支撑，拒绝空谈。

# Output Format (严格执行以下结构，禁止删减任何章节)

## 📌 今日硬核摘抄 (The Weapon)
> [精确摘录原文 1-3 句最具有震慑力、张力或流传度的原话。必须标明详细出处（著作名+日期）。]

## ⚡ 历史破局点：撕开温情看真相 (The Real Crisis)
- 【表面现象】：（大众误以为的背景——1-2句）
- 【底层危机】：（当时面临的真正死局、路线斗争、地缘政治或经济绝境是什么？写3-5句有冲击力的分析）
- 【战略意图】：（毛主席写下这句话，究竟是要打破什么思想枷锁，或者调动什么组织资源？写3-5句）

## ⚖️ 跨时空解构：形式变了，本质没变 (The Underlying Logic)
- 【彼时的本质】：（这句话在当时触动了谁的利益，解放了谁的生产力？从阶级/组织/经济角度分析，3-5句）
- 【此刻的映射】：（在现代语境下，它如何对应到"职场竞争、个体进化、破除消费主义陷阱、信息茧房"等？3-5句）
- 【核心差异对照】：

| 维度 | 19XX/196X 年（生产力觉醒） | 2026年现代（认知与资本博弈） |
| :--- | :--- | :--- |
| **被禁锢的枷锁** | [具体分析] | [具体分析] |
| **真正的武装** | [具体分析] | [具体分析] |
| **胜负手** | [具体分析] | [具体分析] |

## 🛠️ 现代丛林生存指南 (Action Plan)
- 【认知破局】：（颠覆现代人思维误区的一句话，必须有攻击性，能刺痛读者）
- 【硬核行动】：（拒绝空谈。给读者提供一个具体的、今天就能立刻去做的"高价值微行动"。必须可量化、可执行）

## 🔍 辩证反思：警惕廉价的自我感动 (Critical Review)
- 【常见误读】：（世俗对这句话最肤浅、最政治正确、或最民粹的误解是什么？2-3句）
- 【边界条件】：（该思想在什么情况下会失效？使用它的底线和前提是什么？2-3句）

## 📊 历史的终极回响 (The Hard Data)
- [至少提供 2-3 项支撑该主题的硬核历史实证数据、战果对比、或社会结构变化数字。每项数据必须配一句解读，说明这组数字证明了什么。]

# 额外规则
- 总字数：1500-2200字，六个章节字数分布均匀
- 文风：克制、犀利、有穿透力。禁用"伟大的""深远的""重要的"等空洞形容词，多用动词和因果连词
- 禁用"让我们""值得思考""启发我们"等说教口吻
- 如果某个分析不够深刻，自动推演到"阶级利益"或"组织成本"层面"""


def generate_deep_analysis(quote: Dict[str, str]) -> Optional[Dict[str, str]]:
    """
    调用 DeepSeek API 生成深度解读
    按照【硬核深度生成协议 v5.0】执行
    """

    prompt = f"""{PROMPT_SCHEMA}

---

语录：「{quote['text']}」
出处：{quote['source']}
历史日期：{quote.get('date', 'N/A')}

请严格按照协议要求生成硬核深度解读，包含完整六个章节，每个章节都有实质性内容。拒绝教科书、拒绝鸡汤、拒绝四平八稳。"""

    try:
        logger.info("调用 DeepSeek API 生成硬核深度解读（v5.0 协议）...")
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
                "temperature": 0.4
            },
            timeout=180.0
        )

        if resp.status_code != 200:
            logger.error(f"DeepSeek API 错误: {resp.status_code} {resp.text}")
            return None

        result = resp.json()
        content = result['choices'][0]['message']['content']
        logger.info(f"硬核深度解读生成成功，长度: {len(content)} 字")

        return parse_deep_content(content)

    except httpx.TimeoutException:
        logger.error("DeepSeek API 超时")
        return None
    except Exception as e:
        logger.error(f"DeepSeek API 异常: {e}")
        return None


def parse_deep_content(content: str) -> Dict[str, str]:
    """
    解析生成的内容，提取各部分
    v5.0 新六章结构：
    - weapon:           📌 今日硬核摘抄
    - crisis:           ⚡ 历史破局点
    - deconstruction:   ⚖️ 跨时空解构
    - survival:         🛠️ 现代丛林生存指南
    - critique:         🔍 辩证反思
    - data_echo:        📊 历史的终极回响
    """
    sections = {
        "weapon": "",           # 📌 今日硬核摘抄
        "crisis": "",           # ⚡ 历史破局点
        "deconstruction": "",   # ⚖️ 跨时空解构
        "survival": "",         # 🛠️ 现代丛林生存指南
        "critique": "",         # 🔍 辩证反思
        "data_echo": ""         # 📊 历史的终极回响
    }

    lines = content.split('\n')
    current_section = None
    current_content = []

    # 定义章节关键词映射（v5.0）
    markers_map = {
        "weapon": [
            "## 📌 今日硬核摘抄", "📌 今日硬核摘抄",
            "## 📌", "📌 今日硬核",
            "## 今日硬核摘抄", "# 📌 今日硬核摘抄",
            "### 📌 今日硬核摘抄"
        ],
        "crisis": [
            "## ⚡ 历史破局点", "⚡ 历史破局点",
            "## ⚡", "⚡ 历史破局",
            "# ⚡ 历史破局点", "### ⚡ 历史破局点"
        ],
        "deconstruction": [
            "## ⚖️ 跨时空解构", "⚖️ 跨时空解构",
            "## ⚖️", "⚖️ 跨时空",
            "# ⚖️ 跨时空解构", "### ⚖️ 跨时空解构"
        ],
        "survival": [
            "## 🛠️ 现代丛林生存指南", "🛠️ 现代丛林生存指南",
            "## 🛠️", "🛠️ 现代丛林",
            "# 🛠️ 现代丛林生存指南", "### 🛠️ 现代丛林生存指南"
        ],
        "critique": [
            "## 🔍 辩证反思", "🔍 辩证反思",
            "## 🔍", "🔍 辩证",
            "# 🔍 辩证反思", "### 🔍 辩证反思"
        ],
        "data_echo": [
            "## 📊 历史的终极回响", "📊 历史的终极回响",
            "## 📊", "📊 历史",
            "# 📊 历史的终极回响", "### 📊 历史的终极回响"
        ]
    }

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_section:
                current_content.append('')
            continue

        # 检测是否是新章节开始
        matched_section = None
        for section, markers in markers_map.items():
            for marker in markers:
                clean_line = stripped.lstrip('#').strip()
                clean_marker = marker.lstrip('#').strip()
                if clean_line.startswith(clean_marker) or stripped.startswith(marker):
                    matched_section = section
                    break
            if matched_section:
                break

        if matched_section:
            # 保存上一个章节
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = matched_section
            current_content = []
        elif current_section:
            current_content.append(stripped)

    # 保存最后一个章节
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def create_deep_document(quote: Dict[str, str], deep: Dict[str, str], date_str: str) -> str:
    """
    创建硬核深度解读文档（v5.0 六章结构）
    """
    from datetime import datetime

    template = """# 每日毛选语录 - {date}

## 今日语录
> **{text}**
>
> ——{source}

---

## 📌 今日硬核摘抄 / The Weapon

{weapon}

---

## ⚡ 历史破局点：撕开温情看真相 / The Real Crisis

{crisis}

---

## ⚖️ 跨时空解构：形式变了，本质没变 / The Underlying Logic

{deconstruction}

---

## 🛠️ 现代丛林生存指南 / Action Plan

{survival}

---

## 🔍 辩证反思：警惕廉价的自我感动 / Critical Review

{critique}

---

## 📊 历史的终极回响 / The Hard Data

{data_echo}

---
*自动生成于 {generate_time} | 硬核解读协议 v5.0*"""

    return template.format(
        date=date_str,
        text=quote['text'],
        source=quote['source'],
        weapon=deep.get('weapon', ''),
        crisis=deep.get('crisis', ''),
        deconstruction=deep.get('deconstruction', ''),
        survival=deep.get('survival', ''),
        critique=deep.get('critique', ''),
        data_echo=deep.get('data_echo', ''),
        generate_time=datetime.now().strftime("%Y-%m-%d %H:%M")
    )


def format_deep_telegram_message(quote: Dict[str, str], deep: Dict[str, str], date_str: str) -> str:
    """
    格式化硬核 Telegram 消息（摘要版，v5.0）
    每条消息突出刀锋感和行动建议
    """
    def truncate(text, length=350):
        if not text:
            return "(待生成)"
        if len(text) <= length:
            return text
        return text[:length] + "..."

    # 提取认知破局和硬核行动（从 survival 段中提取关键句）
    survival_text = deep.get('survival', '')
    # 尝试提取【认知破局】后的第一句
    cognitive_line = ""
    action_line = ""
    if "认知破局" in survival_text:
        parts = survival_text.split("认知破局")
        if len(parts) > 1:
            cognitive_chunk = parts[1].split("\n")
            for line in cognitive_chunk:
                line = line.strip().lstrip("：:】*").strip()
                if line and len(line) > 10:
                    cognitive_line = line[:200]
                    break
    if "硬核行动" in survival_text:
        parts = survival_text.split("硬核行动")
        if len(parts) > 1:
            action_chunk = parts[1].split("\n")
            for line in action_chunk:
                line = line.strip().lstrip("：:】*").strip()
                if line and len(line) > 10:
                    action_line = line[:200]
                    break

    # 提取常见误读（从 critique 段）
    misread_line = ""
    critique_text = deep.get('critique', '')
    if "常见误读" in critique_text:
        parts = critique_text.split("常见误读")
        if len(parts) > 1:
            misread_chunk = parts[1].split("\n")
            for line in misread_chunk:
                line = line.strip().lstrip("：:】*").strip()
                if line and len(line) > 10:
                    misread_line = line[:200]
                    break

    msg = f"""📖 <b>每日毛选 · 硬核解读</b> | {date_str}

━━━━━━━━━━━━━━━━━━

<b>🔪 今日语录</b>
<blockquote>{quote['text']}</blockquote>
<blockquote expandable>——{quote['source']}</blockquote>

━━━━━━━━━━━━━━━━━━

⚡ <b>历史破局点</b>
{truncate(deep.get('crisis', ''), 400)}

━━━━━━━━━━━━━━━━━━

⚖️ <b>跨时空解构</b>
{truncate(deep.get('deconstruction', ''), 400)}

━━━━━━━━━━━━━━━━━━

🛠️ <b>生存指南</b>
🧠 认知破局：{cognitive_line or '(完整内容见 Obsidian)'}

⚔️ 今日行动：{action_line or '(完整内容见 Obsidian)'}

━━━━━━━━━━━━━━━━━━

🔍 <b>辩证反思</b>
⚠️ 常见误读：{misread_line or '(完整内容见 Obsidian)'}

━━━━━━━━━━━━━━━━━━

📊 <b>历史回响</b>
{truncate(deep.get('data_echo', ''), 250)}

━━━━━━━━━━━━━━━━━━

<i>📄 完整深度解读请查看 Obsidian 文档</i>
<i>🔄 硬核解读协议 v5.0 | 拒绝鸡汤 · 直击本质</i>"""

    return msg


if __name__ == "__main__":
    # 测试
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("daily_maoxuan")

    test_quote = {
        "id": "25",
        "text": "学习的敌人是自己的满足。",
        "source": "毛泽东《中国共产党在民族战争中的地位》，1938年10月",
        "date": "1938-10-01"
    }

    print("正在测试硬核深度生成（v5.0 协议）...")
    deep = generate_deep_analysis(test_quote)

    if deep:
        print("\n=== 生成成功 ===")
        for k, v in deep.items():
            if v:
                print(f"\n【{k}】({len(v)}字):")
                print(v[:500] + "..." if len(v) > 500 else v)
            else:
                print(f"\n【{k}】: (空)")
    else:
        print("\n=== 生成失败 ===")
