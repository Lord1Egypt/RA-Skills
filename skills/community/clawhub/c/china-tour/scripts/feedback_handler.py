#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feedback_handler.py - 处理用户反馈并调整后续路线

Usage:
    python feedback_handler.py --feedback "太啰嗦了" --current-spot "太和殿"
"""

import argparse
import json
import sys
from typing import Dict, List, Optional

# 处理 Windows 控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# ============== 反馈类型与调整策略 ==============

FEEDBACK_TYPES = {
    "satisfied": {
        "keywords": ["满意", "好的", "不错", "挺好", "继续", "ok", "good", "great"],
        "adjustment": "continue",
        "response": "太好了！继续下一站～"
    },
    "want_deeper": {
        "keywords": ["想更深", "更多", "详细点", "不够", "deep", "more"],
        "adjustment": "increase_depth",
        "response": "好的，我补充更多细节！"
    },
    "too_verbose": {
        "keywords": ["太啰嗦", "简单点", "太多了", "brief", "too much", "short"],
        "adjustment": "decrease_depth",
        "response": "明白，接下来精简讲解！"
    },
    "want_photo": {
        "keywords": ["想拍照", "拍照", "机位", "photo", "picture", "camera"],
        "adjustment": "add_photo_spots",
        "response": "收到！推荐更多拍照机位～"
    },
    "tired": {
        "keywords": ["累了", "休息", "走不动", "tired", "rest", "break"],
        "adjustment": "add_rest",
        "response": "辛苦了！调整路线，增加休息点～"
    },
    "not_satisfied": {
        "keywords": ["不满意", "不喜欢", "不好", "not good", "don't like"],
        "adjustment": "ask_reason",
        "response": "抱歉！请问具体哪里不满意？我重新规划～"
    },
    "bored": {
        "keywords": ["无聊", "没意思", "boring", "bored"],
        "adjustment": "add_interest",
        "response": "了解！增加更多有趣的内容～"
    },
    "rush": {
        "keywords": ["赶时间", "快点", "着急", "rush", "hurry", "quick"],
        "adjustment": "speed_up",
        "response": "明白！加快节奏，直奔精华～"
    }
}

# 讲解深度级别
DEPTH_LEVELS = {
    "L1": "简版 (30 秒，核心信息)",
    "L2": "标准版 (2-3 分钟，历史 + 亮点)",
    "L3": "深度版 (5-10 分钟，详细历史 + 冷知识)"
}


def classify_feedback(feedback_text: str) -> str:
    """
    分类用户反馈
    
    Args:
        feedback_text: 用户反馈文本
    
    Returns:
        反馈类型
    """
    text_lower = feedback_text.lower()
    
    for feedback_type, config in FEEDBACK_TYPES.items():
        for keyword in config["keywords"]:
            if keyword.lower() in text_lower:
                return feedback_type
    
    # 默认返回满意
    return "satisfied"


def get_adjustment_strategy(feedback_type: str) -> Dict:
    """
    获取调整策略
    
    Args:
        feedback_type: 反馈类型
    
    Returns:
        调整策略字典
    """
    return FEEDBACK_TYPES.get(feedback_type, FEEDBACK_TYPES["satisfied"])


def adjust_route_depth(current_depth: str, adjustment: str) -> str:
    """
    调整讲解深度
    
    Args:
        current_depth: 当前深度 (L1/L2/L3)
        adjustment: 调整类型
    
    Returns:
        新深度
    """
    depth_order = ["L1", "L2", "L3"]
    current_index = depth_order.index(current_depth)
    
    if adjustment == "increase_depth":
        new_index = min(current_index + 1, 2)
    elif adjustment == "decrease_depth":
        new_index = max(current_index - 1, 0)
    else:
        new_index = current_index
    
    return depth_order[new_index]


def generate_adjusted_response(
    feedback_type: str,
    current_spot: str,
    current_depth: str = "L2",
    remaining_spots: List[str] = None
) -> Dict:
    """
    生成调整后的响应
    
    Args:
        feedback_type: 反馈类型
        current_spot: 当前景点
        current_depth: 当前深度
        remaining_spots: 剩余景点列表
    
    Returns:
        响应字典
    """
    strategy = get_adjustment_strategy(feedback_type)
    adjustment = strategy["adjustment"]
    
    response = {
        "feedback_type": feedback_type,
        "acknowledgment": strategy["response"],
        "adjustment": adjustment,
        "new_depth": current_depth,
        "next_action": ""
    }
    
    # 根据调整类型生成具体行动
    if adjustment == "continue":
        response["next_action"] = "继续下一站"
    
    elif adjustment == "increase_depth":
        new_depth = adjust_route_depth(current_depth, adjustment)
        response["new_depth"] = new_depth
        response["next_action"] = f"为{current_spot}补充更多历史细节和冷知识"
    
    elif adjustment == "decrease_depth":
        new_depth = adjust_route_depth(current_depth, adjustment)
        response["new_depth"] = new_depth
        response["next_action"] = "精简讲解，只保留核心信息"
    
    elif adjustment == "add_photo_spots":
        response["next_action"] = "推荐更多拍照机位和拍摄建议"
    
    elif adjustment == "add_rest":
        response["next_action"] = "调整路线，增加休息点，减少步行距离"
    
    elif adjustment == "ask_reason":
        response["next_action"] = "询问具体不满意的原因"
    
    elif adjustment == "add_interest":
        response["next_action"] = "增加趣味故事和互动内容"
    
    elif adjustment == "speed_up":
        response["next_action"] = "加快节奏，跳过次要景点，直奔精华"
    
    # 如果有剩余景点，给出预览
    if remaining_spots and len(remaining_spots) > 0:
        response["remaining_preview"] = f"接下来：{' → '.join(remaining_spots[:3])}"
    
    return response


def format_feedback_options() -> str:
    """格式化反馈选项供用户选择"""
    options = [
        "1️⃣ 满意 → 继续下一站",
        "2️⃣ 想更深 → 补充更多细节",
        "3️⃣ 太啰嗦 → 简化讲解",
        "4️⃣ 想拍照 → 推荐更多机位",
        "5️⃣ 累了 → 增加休息点",
        "6️⃣ 不满意 → 重新规划"
    ]
    options.append("")
    options.append("👉 直接回复数字即可（如回复"1"）")
    return "\n".join(options)


def main():
    parser = argparse.ArgumentParser(description="处理用户反馈并调整路线")
    parser.add_argument("--feedback", type=str, required=True, help="用户反馈文本")
    parser.add_argument("--current-spot", type=str, default="", help="当前景点")
    parser.add_argument("--depth", type=str, default="L2", help="当前讲解深度 (L1/L2/L3)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    # 分类反馈
    feedback_type = classify_feedback(args.feedback)
    
    # 生成调整响应
    response = generate_adjusted_response(
        feedback_type=feedback_type,
        current_spot=args.current_spot,
        current_depth=args.depth
    )
    
    if args.json:
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print(f"📝 反馈类型：{feedback_type}")
        print(f"💬 识别关键词：{args.feedback}")
        print(f"🔧 调整策略：{response['adjustment']}")
        print(f"📖 新讲解深度：{response['new_depth']}")
        print(f"➡️ 下一步：{response['next_action']}")
        if "remaining_preview" in response:
            print(f"🗺️ 剩余路线：{response['remaining_preview']}")


if __name__ == "__main__":
    main()
