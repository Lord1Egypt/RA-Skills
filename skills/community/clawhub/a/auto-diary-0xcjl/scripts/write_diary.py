#!/usr/bin/env python3
"""
write_diary.py - 自动写日记核心逻辑
读取昨日上下文 → AI 生成结构化日记 → 保存本地 → 提取洞察到 auto-learn.md
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
DIARY_DIR = WORKSPACE / "memory" / "diary"
AUTO_LEARN = WORKSPACE / "memory" / "auto-learn.md"
FARM_JSON = WORKSPACE / "farm" / "farm.json"
MEMORY_DIR = WORKSPACE / "memory"

DIARY_DIR.mkdir(parents=True, exist_ok=True)


def get_yesterday_date():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def read_memory_files(yesterday_str):
    """读取昨日相关的 memory 文件"""
    memories = []
    
    # 尝试读取昨日的 memory 文件
    memory_file = MEMORY_DIR / f"{yesterday_str}.md"
    if memory_file.exists():
        memories.append(f"=== Yesterday Memory ({yesterday_str}) ===\n{memory_file.read_text()}")
    
    # 读取最近的 NOW.md
    now_file = WORKSPACE / "NOW.md"
    if now_file.exists():
        memories.append(f"=== Current NOW.md ===\n{now_file.read_text()}")
    
    # 读取 farm 状态
    if FARM_JSON.exists():
        try:
            farm_data = json.loads(FARM_JSON.read_text())
            memories.append(f"=== Farm Status ===\n{json.dumps(farm_data, indent=2, ensure_ascii=False)}")
        except:
            pass
    
    # 读取 auto-learn 最新条目（最近5条）
    if AUTO_LEARN.exists():
        content = AUTO_LEARN.read_text()
        lines = content.split('\n')
        # 简单取最后 30 行
        recent = '\n'.join(lines[-60:]) if len(lines) > 60 else content
        memories.append(f"=== Recent Auto-Learn ===\n{recent}")
    
    return '\n\n'.join(memories) if memories else "No context available"


def generate_diary_context(context_data, yesterday_str):
    """调用 AI 生成日记（通过 main agent）"""
    prompt = f"""你是一个日记生成助手。请根据以下上下文为昨天（{yesterday_str}）生成结构化日记。

## 上下文数据
{context_data}

## 输出要求
生成一份日记，包含：

### 中文部分（给 Jialin 看）
1. **今日概览**：用 2-3 句话总结昨天做了什么
2. **关键决策**：列出 1-3 个重要决定及原因
3. **收获与教训**：从昨天的经历中学到了什么
4. **下一步**：今天应该关注什么

### English Section (For HexaLoop System)
1. **Task Types**: 任务类型分类（diary|ops|reasoning|creative|content|technical）
2. **Key Decisions**: 具体决策点（英文）
3. **Lessons Learned**: 教训（英文）
4. **Next Actions**: 可操作的下一步（英文）
5. **HexaLoop Hints**: 对冥想/农场有价值的信号（英文，1-2句）

请用以下格式输出（YAML frontmatter + Markdown）：

---
date: {yesterday_str}
trigger_time: 08:20
period: yesterday
---

## 📋 今日概览 | Summary

**中文摘要:**
[中文内容]

**English Summary:**
[English content]

## 🔑 关键决策 | Key Decisions

- [决策1]: [原因]
- [决策2]: [原因]

## 💡 收获与教训 | Insights & Lessons

[中文内容]

## 🌱 HexaLoop 状态

[从上下文中提取 farm/能量状态，没有则写 "N/A"]

## 📊 指标快照

| 指标 | 值 |
|------|---|
| Tasks | [数字或 N/A] |
| Sessions | [数字或 N/A] |

## 🎯 下一步 | Next Steps

[中文 + English]

## 🧠 系统备注 | System Notes

[English only - 供 HexaLoop 读取的原始信息]
"""

    return prompt


def save_diary(diary_content, yesterday_str):
    """保存日记到本地文件"""
    diary_file = DIARY_DIR / f"{yesterday_str}.md"
    diary_file.write_text(diary_content)
    print(f"[auto-diary] 日记已保存: {diary_file}")
    return diary_file


def extract_insights(diary_content, yesterday_str):
    """从日记中提取价值片段，写入 auto-learn.md（格式 A）"""
    
    # 检查 auto-learn.md 是否存在
    if AUTO_LEARN.exists():
        existing = AUTO_LEARN.read_text()
        # 检查是否已有今日的记录，避免重复
        if f"### {yesterday_str}" in existing:
            print(f"[auto-diary] 今日洞察已存在，跳过")
            return
    else:
        existing = "# auto-learn.md - Agent 自我学习记录\n\n> 版本：2026-03-31\n---\n\n"
    
    # 生成洞察条目（格式 A）
    insight_entry = f"""## 学习记录

### {yesterday_str} 08:20

**任务类型**: diary
**涉及 Skill**: auto-diary
**关键决策**: {extract_key_decisions(diary_content)}
**教训**: {extract_lessons(diary_content)}
**下次应用**: {extract_next_actions(diary_content)}
"""
    
    # 追加到 auto-learn.md
    AUTO_LEARN.write_text(existing + "\n" + insight_entry)
    print(f"[auto-diary] 洞察已写入: {AUTO_LEARN}")


def extract_key_decisions(content):
    """简单从日记中提取关键决策"""
    # 找 Key Decisions 部分
    lines = content.split('\n')
    decisions = []
    in_decisions = False
    for line in lines:
        if '关键决策' in line or 'Key Decisions' in line:
            in_decisions = True
            continue
        if in_decisions:
            if line.strip().startswith('##') or line.strip().startswith('**'):
                break
            if line.strip().startswith('-'):
                decisions.append(line.strip().lstrip('- '))
    return '; '.join(decisions[:3]) if decisions else '日记自动生成，无手动决策记录'


def extract_lessons(content):
    """提取教训"""
    lines = content.split('\n')
    lessons = []
    in_lessons = False
    for line in lines:
        if '教训' in line or 'Lessons' in line:
            in_lessons = True
            continue
        if in_lessons:
            if line.strip().startswith('##') or line.strip().startswith('🎯'):
                break
            if len(line.strip()) > 10:
                lessons.append(line.strip())
    return ' '.join(lessons[:2]) if lessons else '持续记录中'


def extract_next_actions(content):
    """提取下一步行动"""
    lines = content.split('\n')
    actions = []
    in_actions = False
    for line in lines:
        if '下一步' in line or 'Next' in line:
            in_actions = True
            continue
        if in_actions:
            if line.strip().startswith('##'):
                break
            if line.strip().startswith('-') or line.strip().startswith('*'):
                actions.append(line.strip().lstrip('- *'))
    return ' '.join(actions[:2]) if actions else '继续记录和优化'


def build_feishu_card(diary_content, yesterday_str, card_type="daily"):
    """构建飞书 Interactive 卡片"""
    
    # 提取中文摘要
    zh_summary = extract_section(diary_content, '中文摘要', 'English Summary')
    en_summary = extract_section(diary_content, 'English Summary', '##')
    key_decisions = extract_section(diary_content, '关键决策', '##', start_marker='## 🔑')
    next_steps = extract_section(diary_content, '下一步', '##', start_marker='## 🎯')
    
    if card_type == "daily":
        title = f"📓 {yesterday_str} 日记"
    elif card_type == "weekly":
        title = f"📊 周度回顾"
    else:
        title = f"🗓️ 月度回顾"
    
    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "text": title},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**📋 摘要**\n{zh_summary[:200]}..."
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**🔑 关键决策**\n{key_decisions[:300]}"
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**🎯 下一步**\n{next_steps[:200]}"
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "note",
                    "elements": [
                        {"tag": "plain_text", "text": f"English version saved to: memory/diary/{yesterday_str}.md | Insights → auto-learn.md"}
                    ]
                }
            ]
        }
    }
    
    return card


def extract_section(content, start_marker, end_marker, start_marker_full=None):
    """提取日记中的特定章节"""
    lines = content.split('\n')
    result = []
    in_section = False
    
    for line in lines:
        if start_marker_full and start_marker_full in line:
            in_section = True
            continue
        elif start_marker in line and not start_marker_full:
            in_section = True
            continue
        if in_section:
            if end_marker in line and '## #' not in line:
                break
            result.append(line)
    
    text = '\n'.join(result).strip()
    # 清理 Markdown 格式
    text = text.replace('**', '').replace('*', '').replace('- ', '').strip()
    return text[:500] if len(text) > 500 else text


if __name__ == "__main__":
    yesterday_str = get_yesterday_date()
    
    print(f"[auto-diary] 开始生成 {yesterday_str} 日记...")
    
    # 1. 读取上下文
    context = read_memory_files(yesterday_str)
    
    # 2. 生成日记内容（这里直接输出 prompt，实际由 main agent 执行 AI 生成）
    diary_prompt = generate_diary_context(context, yesterday_str)
    
    # 输出日记模板（让 agent 填充）
    template_path = Path(__file__).parent.parent / "templates" / "diary_template.md"
    template = template_path.read_text()
    template = template.replace("{{date}}", yesterday_str)
    template = template.replace("{{trigger_time}}", "08:20")
    template = template.replace("{{period}}", "yesterday")
    template = template.replace("{{zh_summary}}", "[请根据上下文生成中文摘要]")
    template = template.replace("{{en_summary}}", "[Please generate English summary based on context]")
    
    # 保存初步模板
    diary_file = save_diary(template, yesterday_str)
    
    print(f"[auto-diary] 日记模板已保存到: {diary_file}")
    print(f"[auto-diary] 请 main agent 根据上下文填充完整内容")
    print(f"[auto-diary] Context length: {len(context)} chars")
