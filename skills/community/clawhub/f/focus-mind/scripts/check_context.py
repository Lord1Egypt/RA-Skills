#!/usr/bin/env python3
"""
上下文健康度检测脚本
评估当前上下文的健康状态，返回评分和建议
"""

import json
import re
import sys
from typing import Dict, List, Any, Optional


def count_tokens(text: str) -> int:
    """估算 token 数量 (中文约1字1token, 英文约1词1token)
    
    更准确的估算:
    - 中文: 每个汉字约 1-1.5 tokens
    - 英文: 每个单词约 1-2 tokens
    - 标点和空格: 不计入或少量计入
    """
    if not text:
        return 0
    
    # 中文 tokens
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词 tokens
    english_words = re.findall(r'[a-zA-Z]+', text)
    english_tokens = sum(max(1, len(word) // 3 + 1) for word in english_words)
    # 代码片段 (更精细的估算)
    code_blocks = len(re.findall(r'```[\s\S]*?```', text))
    code_chars = len(re.findall(r'[{}()\[\];]', text))
    # 数字
    numbers = len(re.findall(r'\d+', text))
    
    return chinese_chars + english_tokens + code_chars // 2 + numbers // 2


def calculate_repetition_ratio(text: str) -> float:
    """计算重复信息比例"""
    if not text:
        return 0.0
    
    # 简单实现：检查重复的句子/短语
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if len(lines) <= 1:
        return 0.0
    
    # 统计重复行
    unique_lines = set(lines)
    repetition = 1 - (len(unique_lines) / len(lines))
    return max(0.0, min(1.0, repetition))


def analyze_goal_clarity(messages: List[Dict]) -> Dict[str, Any]:
    """分析目标清晰度"""
    if not messages:
        return {"score": 50, "level": "medium", "reason": "无上下文"}
    
    # 尝试从开头找到明确的任务描述
    first_user_msg = None
    for msg in messages:
        if msg.get("role") == "user":
            first_user_msg = msg.get("content", "")[:200]
            break
    
    if not first_user_msg:
        return {"score": 50, "level": "medium", "reason": "无用户消息"}
    
    # 检查是否有明确的任务关键词
    task_keywords = ["帮", "做", "开发", "写", "创建", "实现", "请", "需要", "要", "修复", "build", "create", "make", "implement", "fix", "do"]
    has_task = any(kw in first_user_msg.lower() for kw in task_keywords)
    
    if has_task:
        return {"score": 85, "level": "high", "reason": "目标明确"}
    else:
        return {"score": 60, "level": "medium", "reason": "目标较模糊"}


def analyze_time_span(messages: List[Dict]) -> Dict[str, Any]:
    """分析时间跨度"""
    if not messages or len(messages) < 2:
        return {"score": 100, "level": "short", "reason": "对话刚开始"}
    
    # 简单估算：消息数量
    msg_count = len(messages)
    if msg_count < 10:
        return {"score": 90, "level": "short", "reason": f"对话较短 ({msg_count}条消息)"}
    elif msg_count < 30:
        return {"score": 70, "level": "medium", "reason": f"对话中等 ({msg_count}条消息)"}
    else:
        return {"score": 50, "level": "long", "reason": f"对话较长 ({msg_count}条消息)"}


def get_level_info(token_count: int) -> Dict[str, str]:
    """获取健康度等级信息
    
    可配置阈值以适应不同场景:
    - 短任务: 3000 tokens
    - 中等任务: 5000 tokens  
    - 长任务: 10000 tokens (默认)
    """
    if token_count < 5000:
        return {
            "level": "green",
            "emoji": "🟢",
            "label": "健康",
            "recommendation": "当前状态良好，无需清理"
        }
    elif token_count < 10000:
        return {
            "level": "yellow",
            "emoji": "🟡",
            "label": "警告",
            "recommendation": "建议生成摘要以保持清晰"
        }
    else:
        return {
            "level": "red",
            "emoji": "🔴",
            "label": "危险",
            "recommendation": "强烈建议立即清除脑雾"
        }


# ===== 扩展功能 =====

class HealthChecker:
    """健康度检查器类，支持更高级的功能"""
    
    def __init__(self, threshold: int = 10000):
        self.threshold = threshold
        self.history = []  # 历史记录
    
    def check(self, context: Any) -> Dict[str, Any]:
        """执行检查"""
        result = analyze_context_health(context, self.threshold)
        
        # 记录历史
        self.history.append({
            "timestamp": __import__("time").time(),
            "score": result["score"],
            "level": result["level"],
            "token_count": result["details"]["token_count"]
        })
        
        # 只保留最近20条记录
        if len(self.history) > 20:
            self.history = self.history[-20:]
        
        return result
    
    def get_trend(self) -> str:
        """获取趋势分析"""
        if len(self.history) < 2:
            return "stable"
        
        recent = self.history[-5:]
        scores = [h["score"] for h in recent]
        
        if all(scores[i] >= scores[i+1] for i in range(len(scores)-1)):
            return "declining"
        elif all(scores[i] <= scores[i+1] for i in range(len(scores)-1)):
            return "improving"
        else:
            return "stable"
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.history:
            return {}
        
        scores = [h["score"] for h in self.history]
        tokens = [h["token_count"] for h in self.history]
        
        return {
            "checks": len(self.history),
            "avg_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "avg_tokens": sum(tokens) / len(tokens),
            "trend": self.get_trend()
        }


def analyze_context_health(context: Any, threshold: int = 10000) -> Dict[str, Any]:
    """
    分析上下文健康度
    
    Args:
        context: 可以是字符串或消息列表
        threshold: token 阈值，默认10000
    
    Returns:
        包含 score, level, details, recommendations 的字典
    """
    
    # 处理不同类型的输入
    if isinstance(context, str):
        text = context
        # 将字符串转换为消息格式
        if text.strip():
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            messages = [{"role": "user", "content": line} for line in lines]
        else:
            messages = []
    elif isinstance(context, list):
        # 假设是消息列表
        messages = context
        text = "\n".join(msg.get("content", "") for msg in messages if msg.get("content"))
    else:
        # 尝试转换为字符串
        text = str(context)
        messages = []
    
    # 1. 计算 token 数量
    token_count = count_tokens(text)
    
    # 2. 计算重复比例
    repetition_ratio = calculate_repetition_ratio(text)
    
    # 3. 分析目标清晰度
    goal_clarity = analyze_goal_clarity(messages)
    
    # 4. 分析时间跨度
    time_span = analyze_time_span(messages)
    
    # 5. 额外分析维度
    # 5.1 代码密度分析
    code_density = analyze_code_density(text)
    # 5.2 对话质量分析
    dialogue_quality = analyze_dialogue_quality(messages)
    # 5.3 分散度分析
    focus_dispersion = analyze_focus_dispersion(messages)
    
    # 6. 计算综合评分
    # 权重: token长度35%, 重复度15%, 目标清晰度20%, 时间跨度10%, 代码密度10%, 对话质量5%, 分散度5%
    token_score = max(0, 100 - (token_count / threshold) * 50) if threshold > 0 else 100
    repetition_score = max(0, 100 - repetition_ratio * 100)
    
    total_score = (
        token_score * 0.35 +
        repetition_score * 0.15 +
        goal_clarity["score"] * 0.20 +
        time_span["score"] * 0.10 +
        code_density["score"] * 0.10 +
        dialogue_quality["score"] * 0.05 +
        focus_dispersion["score"] * 0.05
    )
    total_score = int(max(0, min(100, total_score)))
    
    # 7. 获取等级
    level_info = get_level_info(token_count)
    
    # 8. 生成建议
    recommendations = []
    if token_count >= threshold:
        recommendations.append("上下文超过阈值，建议运行摘要生成")
    if repetition_ratio > 0.3:
        recommendations.append("检测到较多重复内容，建议精简")
    if goal_clarity["level"] == "low":
        recommendations.append("目标不够清晰，建议明确当前任务")
    if time_span["level"] == "long":
        recommendations.append("对话时间较长，建议整理思路")
    if code_density["score"] < 50:
        recommendations.append("代码密度较高，可能需要分段处理")
    if dialogue_quality["score"] < 60:
        recommendations.append("对话中有较长的等待/思考时间")
    if focus_dispersion["level"] == "scattered":
        recommendations.append("思维较分散，建议聚焦核心目标")
    
    if not recommendations:
        recommendations.append(level_info["recommendation"])
    
    return {
        "score": total_score,
        "level": level_info["level"],
        "emoji": level_info["emoji"],
        "label": level_info["label"],
        "details": {
            "token_count": token_count,
            "repetition_ratio": round(repetition_ratio * 100, 1),
            "goal_clarity": goal_clarity,
            "time_span": time_span,
            "threshold": threshold,
            "code_density": code_density,
            "dialogue_quality": dialogue_quality,
            "focus_dispersion": focus_dispersion
        },
        "recommendations": recommendations
    }


def analyze_code_density(text: str) -> Dict[str, Any]:
    """分析代码密度"""
    if not text:
        return {"score": 100, "level": "low", "ratio": 0}
    
    # 检测代码块
    code_blocks = len(re.findall(r'```[\s\S]*?```', text))
    inline_code = len(re.findall(r'`[^`]+`', text))
    code_chars = len(re.findall(r'[{}()\[\];=]', text))
    
    total_chars = len(text)
    code_ratio = (code_blocks * 200 + inline_code * 20 + code_chars) / max(1, total_chars)
    
    # 代码占比高可能导致理解困难
    if code_ratio < 0.05:
        return {"score": 90, "level": "low", "ratio": round(code_ratio, 3)}
    elif code_ratio < 0.15:
        return {"score": 75, "level": "medium", "ratio": round(code_ratio, 3)}
    else:
        return {"score": 50, "level": "high", "ratio": round(code_ratio, 3)}


def analyze_dialogue_quality(messages: List[Dict]) -> Dict[str, Any]:
    """分析对话质量"""
    if not messages or len(messages) < 2:
        return {"score": 90, "level": "good", "avg_length": 0}
    
    # 计算平均消息长度
    total_length = sum(len(msg.get("content", "")) for msg in messages)
    avg_length = total_length / len(messages)
    
    # 过短的消息可能表示碎片化对话
    # 过长的消息可能表示一次性输入大量信息
    if 50 < avg_length < 500:
        return {"score": 85, "level": "good", "avg_length": avg_length}
    elif 20 < avg_length < 1000:
        return {"score": 70, "level": "medium", "avg_length": avg_length}
    else:
        return {"score": 50, "level": "poor", "avg_length": avg_length}


def analyze_focus_dispersion(messages: List[Dict]) -> Dict[str, Any]:
    """分析思维分散度"""
    if not messages or len(messages) < 3:
        return {"score": 90, "level": "focused", "topics": 1}
    
    # 简单主题检测: 提取每条消息的关键名词/关键词
    topics = []
    for msg in messages[:10]:  # 只看前10条
        content = msg.get("content", "")[:200]
        # 提取潜在的关键词
        words = re.findall(r'[A-Z][a-zA-Z]{3,}', content)  # 大写开头的词
        topics.extend(words[:2])
    
    # 统计不同主题数
    unique_topics = len(set(topics))
    
    if unique_topics <= 3:
        return {"score": 85, "level": "focused", "topics": unique_topics}
    elif unique_topics <= 6:
        return {"score": 60, "level": "moderate", "topics": unique_topics}
    else:
        return {"score": 40, "level": "scattered", "topics": unique_topics}


def format_health_report(health: Dict[str, Any]) -> str:
    """格式化健康度报告"""
    d = health["details"]
    
    # 翻译等级
    level_trans = {
        "low": "低", "medium": "中", "high": "高",
        "good": "良好", "poor": "较差",
        "focused": "聚焦", "moderate": "分散", "scattered": "较分散"
    }
    
    def tr(level):
        return level_trans.get(str(level).lower(), str(level))
    
    report = f"""
🧠 上下文健康度: {health["emoji"]} {health["score"]}/100 ({health["label"]})

📊 基础分析:
• 上下文长度: {d["token_count"]} tokens ({health["label"]})
• 重复信息: {d["repetition_ratio"]}% ({'低' if d['repetition_ratio'] < 10 else '中等' if d['repetition_ratio'] < 30 else '高'})
• 目标清晰度: {tr(d['goal_clarity']['level'])} ({d["goal_clarity"]["reason"]})
• 时间跨度: {tr(d['time_span']['level'])} ({d['time_span']['reason']})

📊 扩展分析:
• 代码密度: {tr(d.get('code_density', {}).get('level', 'low'))} ({d.get('code_density', {}).get('ratio', 0)})
• 对话质量: {tr(d.get('dialogue_quality', {}).get('level', 'good'))}
• 思维聚焦: {tr(d.get('focus_dispersion', {}).get('level', 'focused'))} ({d.get('focus_dispersion', {}).get('topics', 1)} 个主题)

💡 建议:
"""
    for i, rec in enumerate(health["recommendations"], 1):
        report += f"{i}. {rec}\n"
    
    return report


def main():
    """测试用主函数"""
    # 模拟测试
    test_context = """
    用户: 请帮我开发一个网站
    Agent: 好的，我可以帮你开发网站。你需要什么类型的网站？
    用户: 一个博客网站
    Agent: 博客网站很好。我来帮你设计一下结构。
    用户: 好的
    Agent: 首先我需要确定你的技术栈。你想用什么技术？
    用户: 用 Python 吧
    Agent: Python 很好，可以用 Flask 或 Django。你想用哪个？
    用户: Flask 吧，比较轻量
    Agent: 好的，Flask 是个不错的选择。我们开始吧。
    """ * 5  # 重复5次模拟长上下文
    
    health = analyze_context_health(test_context)
    print(format_health_report(health))
    
    # 也支持 JSON 输出
    if "--json" in sys.argv:
        print("\n--- JSON ---")
        print(json.dumps(health, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
