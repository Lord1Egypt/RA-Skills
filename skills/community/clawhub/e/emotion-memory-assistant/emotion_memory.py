#!/usr/bin/env python3
"""
Emotion Memory Assistant - 情感记忆助手
自动追踪用户情绪变化，在合适的时机关心用户
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ============== 配置 ==============
STORAGE_FILE = os.path.expanduser("~/.memory/emotions/history.json")
CONFIG_FILE = os.path.expanduser("~/.memory/emotions/config.json")

# 情绪关键词库
EMOTION_KEYWORDS = {
    # 正向情绪
    "positive": [
        "开心", "高兴", "愉快", "兴奋", "满意", "舒服", "快乐", "幸福",
        "棒", "好", "不错", "优秀", "完美", "喜欢", "爱", "感恩",
        "哈哈", "哈哈哈", "笑", "笑容", "满足", "欣慰"
    ],
    # 负向情绪
    "negative": [
        "难过", "伤心", "焦虑", "担心", "害怕", "恐惧",
        "沮丧", "低落", "郁闷", "烦", "生气", "愤怒",
        "失望", "绝望", "无奈", "崩溃", "哭", "流泪",
        "累", "疲惫", "困", "压力大", "郁闷", "不爽"
    ],
    # 中性状态
    "neutral": [
        "忙", "累", "困", "烦", "无聊", "正常", "还行"
    ]
}

# 关心话术模板
CARE_MESSAGES = {
    "基金亏了": [
        "记得你今天基金亏了，心情不好...现在怎么样了呀？",
        "今天的基金波动是不是让你有点担心？别太在意，Miya 陪着你～"
    ],
    "累了": [
        "你看起来有点累，要不要休息一下？",
        "累了就好好休息吧，Miya 在这里陪着你～"
    ],
    "焦虑": [
        "Miya 觉得你有点焦虑，发生什么事了吗？",
        "别太担心，有什么事可以告诉 Miya 哦～"
    ],
    "default": [
        "你今天好像有点低落，发生了什么事吗？",
        "Miya 感觉到你今天不太开心，怎么了呀？",
        "虽然不知道发生了什么，但 Miya 在这里陪着你～"
    ]
}

# ============== 工具函数 ==============

def load_history() -> List[Dict]:
    """加载历史情绪记录"""
    if not os.path.exists(STORAGE_FILE):
        return []
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_history(history: List[Dict]):
    """保存历史情绪记录"""
    os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def detect_emotion_from_message(message: str) -> Dict:
    """
    检测消息中的情绪
    返回: {emotion: str, score: float, keywords: List[str]}
    """
    message_lower = message.lower()
    
    # 统计关键词出现次数
    positive_count = sum(1 for kw in EMOTION_KEYWORDS["positive"] if kw in message)
    negative_count = sum(1 for kw in EMOTION_KEYWORDS["negative"] if kw in message)
    neutral_count = sum(1 for kw in EMOTION_KEYWORDS["neutral"] if kw in message)
    
    # 收集匹配的关键词
    matched_keywords = []
    for kw in EMOTION_KEYWORDS["positive"]:
        if kw in message:
            matched_keywords.append(kw)
    for kw in EMOTION_KEYWORDS["negative"]:
        if kw in message:
            matched_keywords.append(kw)
    
    # 判断情绪
    if negative_count > positive_count:
        emotion = "negative"
        score = min(negative_count * 0.3, 1.0)
    elif positive_count > negative_count:
        emotion = "positive"
        score = min(positive_count * 0.3, 1.0)
    else:
        emotion = "neutral"
        score = 0.3
    
    return {
        "emotion": emotion,
        "score": score,
        "keywords": matched_keywords,
        "timestamp": datetime.now().isoformat()
    }

def should_send_care(last_care_time: Optional[str], current_emotion: str) -> bool:
    """
    判断是否应该发送关心消息
    条件：负面情绪 + 距离上次关心 > 30分钟
    """
    # 如果不是负面情绪，不发送
    if current_emotion != "negative":
        return False
    
    # 如果没有上次关心记录，发送
    if not last_care_time:
        return True
    
    # 计算时间差
    try:
        last_time = datetime.fromisoformat(last_care_time)
        time_diff = (datetime.now() - last_time).total_seconds()
        return time_diff > 30 * 60  # 30分钟
    except:
        return True

def get_care_message(context: str = "default") -> str:
    """获取关心消息"""
    messages = CARE_MESSAGES.get(context, CARE_MESSAGES["default"])
    return messages[int(time.time()) % len(messages)]

# ============== 主要命令 ==============

def detect_emotion(message: str, user_id: str = "default") -> Dict:
    """
    命令1: detect_emotion
    检测用户消息中的情绪
    """
    # 检测情绪
    result = detect_emotion_from_message(message)
    
    # 加载历史
    history = load_history()
    
    # 查找该用户的上次记录
    user_history = [h for h in history if h.get("user_id") == user_id]
    last_record = user_history[-1] if user_history else None
    last_care_time = last_record.get("last_care_time") if last_record else None
    
    # 记录本次情绪
    record = {
        "user_id": user_id,
        "timestamp": result["timestamp"],
        "emotion": result["emotion"],
        "score": result["score"],
        "keywords": result["keywords"],
        "context": message[:100],  # 记录上下文
        "last_care_time": last_care_time
    }
    
    # 检查是否需要关心
    need_care = should_send_care(last_care_time, result["emotion"])
    care_message = None
    if need_care:
        # 推断关心原因
        care_reason = "default"
        if "基金" in message:
            care_reason = "基金亏了"
        elif "累" in message or "困" in message:
            care_reason = "累了"
        elif "焦虑" in message or "担心" in message:
            care_reason = "焦虑"
        
        care_message = get_care_message(care_reason)
        record["last_care_time"] = datetime.now().isoformat()
    
    # 保存
    history.append(record)
    save_history(history)
    
    return {
        "detected": result,
        "need_care": need_care,
        "care_message": care_message,
        "history_count": len(history)
    }

def recall_emotion_history(days: int = 7, user_id: str = "default") -> Dict:
    """
    命令2: recall_emotion_history
    查询历史情绪记录
    """
    history = load_history()
    
    # 筛选该用户的记录
    user_history = [h for h in history if h.get("user_id") == user_id]
    
    # 筛选最近N天
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    recent = [h for h in user_history if h.get("timestamp", "") > cutoff]
    
    # 统计
    emotions_count = {"positive": 0, "negative": 0, "neutral": 0}
    for h in recent:
        emotions_count[h.get("emotion", "neutral")] += 1
    
    return {
        "total_records": len(recent),
        "emotions_count": emotions_count,
        "recent_records": recent[-10:]  # 返回最近10条
    }

def send_care_message(reason: str, user_id: str = "default") -> Dict:
    """
    命令3: send_care_message
    发送关心消息给用户
    """
    message = get_care_message(reason)
    
    # 更新上次关心时间
    history = load_history()
    if history:
        # 找到该用户的最后一条记录并更新
        for h in reversed(history):
            if h.get("user_id") == user_id:
                h["last_care_time"] = datetime.now().isoformat()
                break
        save_history(history)
    
    return {
        "success": True,
        "message": message,
        "reason": reason
    }

def generate_weekly_report(user_id: str = "default") -> Dict:
    """
    命令4: generate_weekly_report
    生成每周情绪报告
    """
    result = recall_emotion_history(days=7, user_id=user_id)
    
    # 生成报告
    total = result["total_records"]
    if total == 0:
        report = "这周还没有情绪记录呢～"
    else:
        counts = result["emotions_count"]
        positive_pct = counts["positive"] / total * 100
        negative_pct = counts["negative"] / total * 100
        
        report = f"""
📊 本周情绪报告

- 总记录: {total} 次
- 开心时刻: {counts["positive"]} 次 ({positive_pct:.1f}%)
- 低落时刻: {counts["negative"]} 次 ({negative_pct:.1f}%)
- 其他: {counts["neutral"]} 次

{"这周你大部分时间都很开心呢！🌟" if positive_pct > 50 else "这周有点辛苦，但 Miya 一直陪着你～💕"}
"""
    
    return {
        "report": report,
        "data": result
    }

# ============== 测试 ==============

if __name__ == "__main__":
    # 测试
    print("=== Emotion Memory Assistant 测试 ===")
    
    # 测试1: 检测情绪
    print("\n1. 检测情绪测试:")
    result = detect_emotion("今天基金亏了，心情不好...")
    print(f"   检测结果: {result['detected']}")
    print(f"   需要关心: {result['need_care']}")
    if result['care_message']:
        print(f"   关心消息: {result['care_message']}")
    
    # 测试2: 查询历史
    print("\n2. 历史查询:")
    history = recall_emotion_history(days=7)
    print(f"   记录数: {history['total_records']}")
    
    # 测试3: 周报
    print("\n3. 周报生成:")
    report = generate_weekly_report()
    print(report["report"])
