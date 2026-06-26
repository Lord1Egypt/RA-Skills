#!/usr/bin/env python3
"""
目标提取脚本
从上下文历史中提取核心目标和当前阶段
"""

import json
import re
import sys
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


# 目标相关关键词
GOAL_KEYWORDS = [
    "要", "需要", "请", "帮", "开发", "创建", "实现", "做", "写", "构建",
    "build", "create", "make", "implement", "do", "need", "want", "please"
]

# 完成状态关键词
COMPLETION_KEYWORDS = [
    "完成", "好了", "完成", "done", "finished", "completed", "完成啦", "搞定"
]

# 阶段过渡关键词
PHASE_KEYWORDS = [
    "首先", "然后", "接下来", "下一步", "之后", "最后",
    "first", "then", "next", "after", "finally", "now"
]


@dataclass
class Goal:
    """目标项"""
    content: str
    completed: bool = False
    phase: str = "unknown"
    source: str = ""


def extract_initial_goal(messages: List[Dict]) -> Tuple[str, str]:
    """从开头提取初始目标"""
    if not messages:
        return "", ""

    # 找前几条用户消息
    for msg in messages[:5]:
        if msg.get("role") != "user":
            continue

        content = msg.get("content", "")

        # 尝试找到完整的任务描述
        # 查找包含目标关键词的句子
        for keyword in GOAL_KEYWORDS:
            if keyword in content:
                # 找到关键词所在句子
                sentences = re.split(r'[。.!?]', content)
                for sent in sentences:
                    if keyword in sent and len(sent) > 5:
                        return sent.strip(), "initial"

        # 如果没找到完整句子，返回整个消息
        if len(content) > 10:
            return content[:200], "initial"

    return "", ""


def normalize_text(text: str) -> str:
    """标准化文本用于去重比较"""
    # 移除空格、标点，转小写
    normalized = re.sub(r'[\s\u3000，。、！？；：""''（）【】《》]', '', text.lower())
    return normalized


def is_duplicate(new_content: str, existing_goals: List[Goal], threshold: float = 0.5) -> bool:
    """检查是否与已有目标重复 - 更严格的去重
    
    只要内容高度相似就认为是重复，避免提取子集目标
    """
    # 清理新内容 - 移除常见前缀
    new_clean = re.sub(r'^(用户[:：]|助手[:：]|user[:：]|assistant[:：])', '', new_content.lower()).strip()
    new_clean = re.sub(r'[\s\u3000，。、！？；：""''（）【】《》]', '', new_clean)
    
    if not new_clean or len(new_clean) < 2:
        return True
    
    # 提取核心关键词
    new_keywords = set(re.findall(r'[\u4e00-\u9fa5]{2,}', new_clean))
    new_words = set(re.findall(r'[a-zA-Z]{3,}', new_clean))
    new_keywords.update(new_words)

    for goal in existing_goals:
        # 同样清理
        existing_clean = re.sub(r'^(用户[:：]|助手[:：]|user[:：]|assistant[:：])', '', goal.content.lower()).strip()
        existing_clean = re.sub(r'[\s\u3000，。、！？；：""''（）【】《》]', '', existing_clean)
        
        if not existing_clean or len(existing_clean) < 2:
            continue

        # 1. 完全相同
        if new_clean == existing_clean:
            return True

        # 2. 子集检查 - 如果新内容是已有内容的子集，或者是已有内容的超集，都认为是重复
        # 只要长度差异小于50%，就认为是重复
        if len(new_clean) > 2 and len(existing_clean) > 2:
            if new_clean in existing_clean or existing_clean in new_clean:
                len_ratio = min(len(new_clean), len(existing_clean)) / max(len(new_clean), len(existing_clean), 1)
                if len_ratio > threshold:
                    return True

        # 3. 关键词重叠检查 - 降低阈值，只要有一个共同关键词就认为是重复
        existing_keywords = set(re.findall(r'[\u4e00-\u9fa5]{2,}', existing_clean))
        existing_words = set(re.findall(r'[a-zA-Z]{3,}', existing_clean))
        existing_keywords.update(existing_words)
        
        if new_keywords and existing_keywords:
            overlap = len(new_keywords & existing_keywords)
            # 只有一个共同关键词但有重叠内容也认为是重复
            if overlap >= 1:
                # 额外检查：是否有实质性的内容重叠
                # 把关键词转回原文中检查
                for kw in (new_keywords & existing_keywords):
                    if kw in new_clean and kw in existing_clean:
                        return True

    return False


def extract_sub_goals(messages: List[Dict]) -> List[Goal]:
    """提取子目标 - 改进版，增强去重"""
    sub_goals = []

    all_text = "\n".join(msg.get("content", "") for msg in messages if msg.get("content"))

    # 模式1: 编号列表 (1) (2) 或 1. 2. - 只提取单个明确目标，避免列表
    numbered_patterns = [
        r'[（\(](\d+)[）\)][\s:：]*([^\d\(]{4,30})',  # (1) 单个目标
        r'^(\d+)[.、]\s*([^\d\.]{4,30})',  # 1. 单个目标
    ]

    for pattern in numbered_patterns:
        matches = re.finditer(pattern, all_text, re.MULTILINE)
        for match in matches:
            num, goal_text = match.groups()
            goal_text = goal_text.strip()
            # 过滤：太短或包含多个编号
            if len(goal_text) > 4 and len(goal_text) < 30 and not re.search(r'\d+[).、]', goal_text):
                if not is_duplicate(goal_text, sub_goals):
                    completed = any(kw in goal_text for kw in COMPLETION_KEYWORDS)
                    sub_goals.append(Goal(
                        content=goal_text[:100],
                        completed=completed,
                        phase=f"step_{num}",
                        source="numbered"
                    ))

    # 模式2: 待办事项风格 [ ] ( )
    todo_patterns = [
        r'[●○]\s*\[?\s*\]?\s*(.+?)(?=\n|[●○])',
        r'TODO:?\s*(.+?)(?=\n|TODO)',
    ]

    for pattern in todo_patterns:
        matches = re.findall(pattern, all_text, re.IGNORECASE)
        for match in matches:
            if len(match) > 3 and not is_duplicate(match, sub_goals):
                completed = any(kw in match for kw in COMPLETION_KEYWORDS)
                sub_goals.append(Goal(
                    content=match.strip()[:100],
                    completed=completed,
                    phase="todo",
                    source="todo"
                ))

    # 模式3: 明确的需求描述 - 更严格，避免提取列表
    # 需要...、要...、实现...（但排除编号列表）
    requirement_patterns = [
        (r'需要([^\n，。.0-9)）]{4,30})(?![0-9])', 'need'),  # 不匹配数字编号
        (r'需要完成([^\n，。.]{4,20})', 'need'),
        (r'要([^\n，。.0-9)）]{4,30})(?![0-9])', 'want'),  # 不匹配数字编号
        (r'实现([^\n，。.]{4,20})', 'implement'),
        (r'添加([^\n，。.]{4,20})', 'add'),
        (r'完成([^\n，。.]{4,20})', 'complete'),
    ]

    for pattern, ptype in requirement_patterns:
        matches = re.findall(pattern, all_text)
        for match in matches:
            # 过滤噪音：太短、太长、或包含数字编号
            if 3 < len(match) < 35 and not re.search(r'\d+[).、]', match) and not is_duplicate(match, sub_goals):
                # 检查是否包含完成关键词
                completed = any(kw in match for kw in COMPLETION_KEYWORDS)
                content = match.strip()[:100]
                sub_goals.append(Goal(
                    content=content,
                    completed=completed,
                    phase="requirement",
                    source=ptype
                ))

    # 模式4: 从用户消息中提取需求（更广泛的匹配）
    for msg in messages:
        if msg.get("role") != "user":
            continue

        content = msg.get("content", "")

        # 查找包含动词的句子
        verb_patterns = [
            r'(?:帮我|请|需要|要|想|帮我|给我)[^\n。.]{5,80}',
            r'(?:开发|创建|实现|制作|构建|写)[^\n。.]{5,80}',
        ]

        for pattern in verb_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) > 8 and not is_duplicate(match, sub_goals):
                    sub_goals.append(Goal(
                        content=match.strip()[:100],
                        completed=False,
                        phase="user_request",
                        source="user_message"
                    ))

    # 最终去重 - 与 is_duplicate 保持一致的逻辑
    final_goals = []
    final_seen = []  # 存储已见过目标的标准化形式
    
    for g in sub_goals:
        norm = normalize_text(g.content)
        if not norm or len(norm) < 2:
            continue
        
        # 提取关键词（2-4个字）
        keywords = set(re.findall(r'[\u4e00-\u9fa5]{2,4}', norm))
        
        is_dup = False
        for existing_norm in final_seen:
            # 完全相同
            if norm == existing_norm:
                is_dup = True
                break
            
            # 包含关系 - 无论长度差异多大，只要一个是另一个的子集就认为是重复
            if norm in existing_norm or existing_norm in norm:
                is_dup = True
                break
            
            # 关键词重叠 - 只要有1个共同关键词就认为是重复（更严格）
            existing_keywords = set(re.findall(r'[\u4e00-\u9fa5]{2,4}', existing_norm))
            if keywords and existing_keywords:
                overlap = len(keywords & existing_keywords)
                if overlap >= 1:
                    is_dup = True
                    break
        
        if not is_dup:
            final_seen.append(norm)
            final_goals.append(g)

    return final_goals[:10]


def detect_current_phase(messages: List[Dict]) -> str:
    """检测当前阶段"""
    if not messages:
        return "start"

    # 分析最近的消息
    recent = messages[-5:] if len(messages) >= 5 else messages
    recent_text = " ".join(msg.get("content", "") for msg in recent)

    # 检测阶段关键词
    phase_indicators = {
        "planning": ["计划", "设计", "规划", "方案", "plan", "design"],
        "implementation": ["实现", "开发", "写", "编码", "implement", "code", "write"],
        "testing": ["测试", "验证", "debug", "test", "verify"],
        "reviewing": ["检查", "审查", "review", "检查", "确认"],
        "finishing": ["完成", "结束", "finish", "done", "完成"],
    }

    for phase, keywords in phase_indicators.items():
        for kw in keywords:
            if kw in recent_text.lower():
                return phase

    # 尝试从对话数量推断
    if len(messages) < 5:
        return "start"
    elif len(messages) < 15:
        return "implementation"
    else:
        return "ongoing"


def identify_completed_items(messages: List[Dict]) -> List[str]:
    """识别已完成的项目"""
    completed = []

    for msg in messages:
        content = msg.get("content", "")

        # 检查是否包含完成状态
        if any(kw in content for kw in COMPLETION_KEYWORDS):
            # 提取完成的内容
            sentences = re.split(r'[。.!?]', content)
            for sent in sentences:
                if any(kw in sent for kw in COMPLETION_KEYWORDS) and len(sent) > 5:
                    # 清理
                    cleaned = re.sub(r'^(已经|已|完成|好了)', '', sent).strip()
                    if len(cleaned) > 5:
                        completed.append(cleaned[:80])

    # 去重
    return list(dict.fromkeys(completed))[:7]


def identify_pending_items(messages: List[Dict]) -> List[str]:
    """识别待完成的项目"""
    pending = []

    all_text = "\n".join(msg.get("content", "") for msg in messages if msg.get("content"))

    # 模式1: 还没、尚未、未
    pending_patterns = [
        r'还没[^\n。.]{10,50}',
        r'尚未[^\n。.]{10,50}',
        r'还未[^\n。.]{10,50}',
    ]

    for pattern in pending_patterns:
        matches = re.findall(pattern, all_text)
        pending.extend(matches)

    # 模式2: 需要...、应该...
    need_patterns = [
        r'需要[^\n。.]{10,50}',
        r'应该[^\n。.]{10,50}',
    ]

    for pattern in need_patterns:
        matches = re.findall(pattern, all_text)
        pending.extend(matches)

    # 清理
    cleaned = []
    seen = set()
    for p in pending:
        p = p.strip()[:80]
        if p and p not in seen:
            seen.add(p)
            cleaned.append(p)

    return cleaned[:7]


def extract_goals(context: Any) -> Dict[str, Any]:
    """
    提取目标信息

    Args:
        context: 上下文内容（字符串或消息列表）

    Returns:
        包含 main_goal, sub_goals, current_phase, completed, pending 的字典
    """

    # 处理不同类型的输入
    if isinstance(context, str):
        text = context
        # 将字符串转换为消息格式
        if text.strip():
            # 按行分割，每行作为一个用户消息
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            messages = [{"role": "user", "content": line} for line in lines]
        else:
            messages = []
    elif isinstance(context, list):
        messages = context
        text = ""
    else:
        messages = []
        text = str(context)

    # 1. 提取主目标
    main_goal, goal_source = extract_initial_goal(messages)

    # 2. 提取子目标
    sub_goals = extract_sub_goals(messages)

    # 3. 检测当前阶段
    current_phase = detect_current_phase(messages)

    # 4. 识别已完成项
    completed = identify_completed_items(messages)

    # 5. 识别待完成项
    pending = identify_pending_items(messages)

    # 阶段映射
    phase_labels = {
        "start": "起始阶段",
        "planning": "规划阶段",
        "implementation": "实现阶段",
        "testing": "测试阶段",
        "reviewing": "审查阶段",
        "finishing": "收尾阶段",
        "ongoing": "进行中"
    }

    return {
        "main_goal": main_goal,
        "goal_source": goal_source,
        "sub_goals": [
            {
                "content": g.content,
                "completed": g.completed,
                "phase": g.phase
            }
            for g in sub_goals
        ],
        "current_phase": current_phase,
        "current_phase_label": phase_labels.get(current_phase, "未知"),
        "completed": completed,
        "pending": pending,
        "summary": {
            "total_sub_goals": len(sub_goals),
            "completed_count": sum(1 for g in sub_goals if g.completed),
            "completed_items": len(completed),
            "pending_items": len(pending)
        }
    }


def format_goals_markdown(goals: Dict[str, Any]) -> str:
    """格式化目标为 Markdown"""
    output = "## 目标提取\n\n"

    # 主目标
    if goals["main_goal"]:
        output += f"### 🎯 核心目标\n{goals['main_goal']}\n\n"

    # 当前阶段
    output += f"### 📍 当前阶段\n{goals['current_phase_label']}\n\n"

    # 子目标
    if goals["sub_goals"]:
        output += "### 📋 子目标\n"
        for i, g in enumerate(goals["sub_goals"], 1):
            status = "✓" if g["completed"] else "○"
            output += f"- {status} {g['content']}\n"
        output += "\n"

    # 已完成
    if goals["completed"]:
        output += "### ✅ 已完成\n"
        for c in goals["completed"]:
            output += f"- {c}\n"
        output += "\n"

    # 待完成
    if goals["pending"]:
        output += "### ⏳ 待完成\n"
        for p in goals["pending"]:
            output += f"- {p}\n"
        output += "\n"

    # 统计
    s = goals["summary"]
    output += f"---\n📊 统计: {s['completed_count']}/{s['total_sub_goals']} 子目标完成, {s['pending_items']} 项待处理"

    return output


def main():
    """测试用主函数"""
    # 模拟测试数据
    test_messages = [
        {"role": "user", "content": "请帮我开发一个 Python 博客网站"},
        {"role": "assistant", "content": "好的，我来帮你开发博客网站。先确定一下需求。"},
        {"role": "user", "content": "需要用户登录、文章发布、评论功能，还有标签系统"},
        {"role": "assistant", "content": "明白了。我们需要：1) 用户系统 2) 文章CRUD 3) 评论系统 4) 标签管理"},
        {"role": "user", "content": "使用 Flask 框架和 SQLite 数据库"},
        {"role": "assistant", "content": "好的，我已创建项目结构。实现了用户模型和认证功能。"},
        {"role": "user", "content": "很好，接下来实现文章发布功能"},
        {"role": "assistant", "content": "正在实现文章CRUD，还没完成评论功能"},
        {"role": "user", "content": "记得加上 Docker 支持"},
    ]

    goals = extract_goals(test_messages)

    print(format_goals_markdown(goals))

    if "--json" in sys.argv:
        print("\n--- JSON ---")
        print(json.dumps(goals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
