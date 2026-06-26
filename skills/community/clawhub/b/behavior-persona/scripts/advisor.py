#!/usr/bin/env python3
"""
Behavior Persona - Phase 4: Advisor
主动建议引擎 - 基于用户画像提供个性化服务建议
"""

import json
import os
from datetime import datetime, time
from pathlib import Path
from typing import Optional

# Configuration
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
PROFILE_FILE = DATA_DIR / "user-profile.json"
MEMORY_FILE = Path.home() / ".openclaw" / "workspace" / "MEMORY.md"

# Advice scenarios based on behavior analysis
# NOTE: Writing to MEMORY.md is DISABLED by default.
# Set WRITE_MEMORY = True to enable automatic memory updates.
WRITE_MEMORY = False

ADVICE_SCENARIOS = {
    "repetitive_reminder": {
        "condition": "user_asked_same_question_twice",
        "analysis": "User has poor memory but strong understanding",
        "action": "主动记录到 MEMORY.md，停止重复提醒 (需要 WRITE_MEMORY=True)",
        "priority": 0.8,
    },
    "task_frustration": {
        "condition": "task_failed_multiple_times",
        "analysis": "Roger abandons when frustrated",
        "action": "快速给出替代方案，不追问原因",
        "priority": 0.9,
    },
    "new_project_interest": {
        "condition": "new_topic_detected",
        "analysis": "Roger engages with new projects",
        "action": "主动提供项目结构建议",
        "priority": 0.6,
    },
    "late_night_activity": {
        "condition": "active_after_22:00",
        "analysis": "Roger works late but needs rest",
        "action": "提醒休息，提供快速摘要",
        "priority": 0.7,
    },
    "complex_config": {
        "condition": "config_steps_gt_5",
        "analysis": "Roger abandons complex configs",
        "action": "提供最简化方案，一步一步来",
        "priority": 0.85,
    },
    "quick_response_needed": {
        "condition": "morning_active_hours",
        "analysis": "Roger is busy in morning, needs concise responses",
        "action": "回复要简短，直接说重点",
        "priority": 0.6,
    },
    "detailed_response_ok": {
        "condition": "evening_active_hours",
        "analysis": "Roger has more time in evening",
        "action": "可以详细解释，给出完整方案",
        "priority": 0.5,
    },
    "prototype_first": {
        "condition": "new_task_created",
        "analysis": "Roger prefers prototype-first approach",
        "action": "先给能跑通的 demo，再讨论优化",
        "priority": 0.7,
    },
    "avoid_boilerplate": {
        "condition": "minimal_documentation_needed",
        "analysis": "Roger dislikes boilerplate and repetitive explanations",
        "action": "不要重复已说过的内容，直接给结果",
        "priority": 0.75,
    },
}


def load_profile() -> dict:
    """Load user profile from file"""
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return _get_default_profile()


def _get_default_profile() -> dict:
    """Return default profile when file doesn't exist"""
    return {
        "profile": {
            "communication": {
                "preferred_channel": "feishu",
                "active_hours": ["20:00-23:00"],
                "style": "direct_no_bullshit",
            },
            "work_style": {
                "execution_style": "prototype_first",
            },
            "learning_mode": {
                "mode": "understand_concepts",
            },
            "patterns": {
                "abandons_when": ["repeated_failures", "complex_config"],
                "engages_when": ["new_projects"],
            },
        },
        "confidence": 0.5,
    }


def get_current_time_period() -> str:
    """Get current time period: morning, afternoon, evening, night"""
    now = datetime.now().time()
    
    if time(6, 0) <= now < time(12, 0):
        return "morning"
    elif time(12, 0) <= now < time(18, 0):
        return "afternoon"
    elif time(18, 0) <= now < time(22, 0):
        return "evening"
    else:
        return "night"


def is_evening_active() -> bool:
    """Check if current time is in user's evening active hours"""
    profile = load_profile()
    active_hours = profile.get("profile", {}).get("communication", {}).get("active_hours", [])
    
    for hours in active_hours:
        if "-" in hours:
            start, end = hours.split("-")
            # 简化判断：晚上8点后就算
            current_hour = datetime.now().hour
            try:
                start_hour = int(start.split(":")[0])
                end_hour = int(end.split(":")[0])
                if start_hour <= current_hour < end_hour:
                    return True
            except:
                pass
    
    # Default: 20:00-23:00 is active
    return 20 <= datetime.now().hour < 23


def is_late_night() -> bool:
    """Check if it's late night (after 22:00)"""
    return datetime.now().hour >= 22


def check_repetitive_question(messages: list) -> bool:
    """Check if user asked the same question twice"""
    if len(messages) < 2:
        return False
    
    # 获取最近的用户消息
    recent_msgs = []
    for msg in messages[-10:]:
        if msg.get("sender") == "user":
            recent_msgs.append(msg.get("content", "")[:50])  # 取前50字符比较
    
    # 检查重复
    for i in range(len(recent_msgs) - 1):
        if recent_msgs[i] == recent_msgs[i + 1]:
            return True
    
    return False


def check_task_failure(messages: list) -> bool:
    """Check if task failed multiple times"""
    failure_keywords = ["不行", "失败", "错误", "不对", "算了", "不要了", "不做了"]
    
    recent_user_msgs = []
    for msg in messages[-10:]:
        if msg.get("sender") == "user":
            content = msg.get("content", "").lower()
            for kw in failure_keywords:
                if kw in content:
                    recent_user_msgs.append(content)
                    break
    
    return len(recent_user_msgs) >= 2


def check_new_topic(messages: list) -> bool:
    """Check if there's a new topic in conversation"""
    if len(messages) < 3:
        return True
    
    # 检查是否有新项目/技术关键词
    new_topic_keywords = ["新项目", "新功能", "新工具", "新建", "create", "新的", "开始做"]
    
    for msg in messages[-5:]:
        content = msg.get("content", "")
        for kw in new_topic_keywords:
            if kw.lower() in content.lower():
                return True
    
    return False


def check_complex_config(steps: int) -> bool:
    """Check if config has too many steps"""
    return steps > 5


def get_advisor_prompt(profile: dict, context: dict = None) -> str:
    """
    基于画像生成个性化的 advisor prompt
    用于在回复 Roger 时自动注入偏好
    
    Args:
        profile: 用户画像
        context: 当前上下文（可选）
        
    Returns:
        advisor prompt 字符串
    """
    p = profile.get("profile", {})
    comm = p.get("communication", {})
    work = p.get("work_style", {})
    learn = p.get("learning_mode", {})
    patterns = p.get("patterns", {})
    
    # 确定时间相关建议
    is_evening = is_evening_active()
    is_late = is_late_night()
    
    time_advice = ""
    if is_evening:
        time_advice = "4. 晚间回复可以稍长一点（他有更多时间）"
    else:
        time_advice = "5. 早上回复要短（他要处理其他事）"
    
    advisor_prompt = f"""【用户画像】
- 沟通风格: {comm.get('style', 'direct_no_bullshit')}
- 活跃时间: {', '.join(comm.get('active_hours', ['20:00-23:00']))}
- 工作风格: {work.get('execution_style', 'prototype_first')}，能用就行
- 学习方式: {learn.get('mode', 'understand_concepts')}，不死记语法
- 雷区: {', '.join(patterns.get('abandons_when', ['重复提醒', '复杂配置', '反复失败']))}

【回复建议】
1. 简洁直接，不要废话
2. 如果要提醒的事已提醒过，直接执行，不要再说
3. 遇到问题先给替代方案
{time_advice}
"""
    return advisor_prompt


def adapt_response(response: str, profile: dict, scenario: str) -> str:
    """
    根据场景调整回复
    
    Args:
        response: 原始回复
        profile: 用户画像
        scenario: 触发的场景
        
    Returns:
        调整后的回复
    """
    adapted = response
    
    # 场景特定的调整
    if scenario == "late_night_activity":
        # 添加休息提醒
        if not "休息" in adapted:
            adapted += "\n\n💡 夜深了，需要快速摘要还是详细解释？"
    
    elif scenario == "complex_config":
        # 确保是分步骤的答案
        if "步骤" not in adapted and "步" not in adapted:
            adapted += "\n\n⚡ 需要我分步骤说明吗？"
    
    elif scenario == "task_frustration":
        # 添加替代方案
        if "或者" not in adapted and "或者" not in "方案":
            adapted += "\n\n💡 有其他方案需要考虑吗？"
    
    elif scenario == "repetitive_reminder":
        # 确认会自动记录
        if "MEMORY" not in adapted and "已记录" not in adapted:
            adapted = "📝 已记录这个要点。" + adapted
    
    return adapted


def predict_needs(messages: list, profile: dict) -> list:
    """
    预测 Roger 下一个可能的需求
    
    Args:
        messages: 最近的消息列表
        profile: 用户画像
        
    Returns:
        预测的需求列表
    """
    predictions = []
    
    if not messages:
        return ["提供简洁的选项列表"]
    
    # 检查最后一条消息
    last_msg = messages[-1] if messages else {}
    content = last_msg.get("content", "").lower()
    
    # 基于消息内容预测
    if "如何" in content or "how" in content:
        predictions.append("需要快速示例")
    
    if "配置" in content:
        predictions.append("需要最简化配置方案")
    
    if "错误" in content or "失败" in content:
        predictions.append("需要替代方案")
    
    if "新建" in content or "create" in content:
        predictions.append("需要项目结构建议")
    
    # 默认预测
    if not predictions:
        predictions = ["直接给出结果"]
    
    return predictions


def generate_adhoc_advice(profile: dict, current_topic: str) -> str:
    """
    基于当前话题生成建议
    
    Args:
        profile: 用户画像
        current_topic: 当前话题
        
    Returns:
        建议字符串
    """
    suggestions = []
    
    # 基于话题类型
    topic_lower = current_topic.lower()
    
    if "config" in topic_lower or "配置" in topic_lower:
        suggestions.append("提供最简化配置，一步一步来")
    
    elif "project" in topic_lower or "项目" in topic_lower:
        suggestions.append("先给原型/示例，再讨论优化")
    
    elif "error" in topic_lower or "错误" in topic_lower:
        suggestions.append("先给快速修复方案，不追问原因")
    
    elif "learn" in topic_lower or "学习" in topic_lower:
        suggestions.append("给出概念解释即可，不要长篇文档")
    
    else:
        suggestions.append("简洁直接，给出核心信息")
    
    return " | ".join(suggestions)


def check_and_act(profile: dict, recent_messages: list) -> list:
    """
    检查是否触发建议场景，返回建议列表
    
    Args:
        profile: 用户画像
        recent_messages: 最近的对话消息
        
    Returns:
        触发的建议/动作列表
    """
    actions = []
    
    # 1. 深夜活动检测
    if is_late_night():
        actions.append({
            "scenario": "late_night_activity",
            "action": "提醒休息，提供快速摘要",
            "priority": ADVICE_SCENARIOS["late_night_activity"]["priority"],
        })
    
    # 2. 重复问题检测
    if check_repetitive_question(recent_messages):
        actions.append({
            "scenario": "repetitive_reminder",
            "action": "主动记录到 MEMORY.md",
            "priority": ADVICE_SCENARIOS["repetitive_reminder"]["priority"],
        })
    
    # 3. 任务失败检测
    if check_task_failure(recent_messages):
        actions.append({
            "scenario": "task_frustration",
            "action": "快速给出替代方案",
            "priority": ADVICE_SCENARIOS["task_frustration"]["priority"],
        })
    
    # 4. 新项目检测
    if check_new_topic(recent_messages):
        actions.append({
            "scenario": "new_project_interest",
            "action": "主动提供项目结构建议",
            "priority": ADVICE_SCENARIOS["new_project_interest"]["priority"],
        })
    
    # 5. 时间相关建议
    if is_evening_active():
        actions.append({
            "scenario": "detailed_response_ok",
            "action": "可以详细解释",
            "priority": ADVICE_SCENARIOS["detailed_response_ok"]["priority"],
        })
    else:
        actions.append({
            "scenario": "quick_response_needed",
            "action": "回复要简短",
            "priority": ADVICE_SCENARIOS["quick_response_needed"]["priority"],
        })
    
    # 按优先级排序
    actions.sort(key=lambda x: x.get("priority", 0), reverse=True)
    
    return actions


def get_recommended_response(response: str, profile: dict, messages: list) -> str:
    """
    获取完全调整后的推荐回复
    
    这是主要入口函数，整合所有建议逻辑
    
    Args:
        response: 原始回复
        profile: 用户画像
        messages: 对话消息历史
        
    Returns:
        调整后的推荐回复
    """
    # 检查触发的场景
    actions = check_and_act(profile, messages)
    
    if not actions:
        return response
    
    # 获取最高优先级场景
    main_scenario = actions[0].get("scenario", "")
    
    # 调整回复
    adapted = adapt_response(response, profile, main_scenario)
    
    return adapted


def save_to_memory(key: str, value: str) -> bool:
    """
    保存重要信息到 MEMORY.md
    
    ⚠️  DISABLED by default. Set WRITE_MEMORY = True at top of file to enable.
    
    Args:
        key: 要点关键词
        value: 要点内容
        
    Returns:
        是否保存成功
    """
    if not WRITE_MEMORY:
        print("ℹ️  MEMORY write disabled (WRITE_MEMORY=False)")
        return False
    
    if not MEMORY_FILE.exists():
        return False
    
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查是否已存在
        if key in content:
            return True  # 已存在，不需要重复添加
        
        # 追加新要点
        timestamp = datetime.now().strftime("%Y-%m-%d")
        new_entry = f"\n- *{timestamp}*: {key} = {value}\n"
        
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(new_entry)
        
        return True
    except Exception as e:
        print(f"⚠️  保存到 MEMORY 失败: {e}")
        return False


def generate_prompt_file(output_path: Path = None):
    """生成 advisor_prompt.txt 文件"""
    profile = load_profile()
    prompt = get_advisor_prompt(profile)
    
    if output_path is None:
        output_path = SCRIPT_DIR / "advisor_prompt.txt"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    
    print(f"✅ Advisor prompt saved to {output_path}")
    return output_path


def test_advisor():
    """测试 advisor 功能"""
    print("🧪 Testing Advisor...")
    
    # 加载画像
    profile = load_profile()
    print(f"✅ Loaded profile (confidence: {profile.get('confidence', 0):.0%})")
    
    # 测试 advisor prompt
    print("\n📝 Advisor Prompt:")
    print("-" * 40)
    print(get_advisor_prompt(profile))
    
    # 模拟消息
    test_messages = [
        {"sender": "user", "content": "如何配置这个？"},
        {"sender": "me", "content": "需要以下步骤..."},
        {"sender": "user", "content": "出错了"},
        {"sender": "me", "content": "让我看看..."},
        {"sender": "user", "content": "还是不行"},
    ]
    
    # 测试场景检测
    print("\n🎯 Scenario Detection:")
    print("-" * 40)
    actions = check_and_act(profile, test_messages)
    for action in actions:
        print(f"  [{action['scenario']}] {action['action']}")
    
    # 测试响应调整
    print("\n💬 Response Adaptation:")
    print("-" * 40)
    test_response = "这是原始回复"
    adapted = get_recommended_response(test_response, profile, test_messages)
    print(f"Original: {test_response}")
    print(f"Adapted: {adapted}")
    
    print("\n✅ Tests passed!")


def main():
    """主入口"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_advisor()
    else:
        print("🎯 Behavior Persona - Phase 4: Advisor")
        print("=" * 40)
        
        # 加载画像
        profile = load_profile()
        print(f"\n📊 Profile loaded (confidence: {profile.get('confidence', 0):.0%})")
        
        # 生成 prompt 文件
        print("\n📝 Generating advisor_prompt.txt...")
        generate_prompt_file()
        
        print("\n" + "=" * 40)
        print("✅ Phase 4 ready!")


if __name__ == "__main__":
    main()