#!/usr/bin/env python3
"""
Behavior Persona - Phase 2: Pattern Analyzer

Analyzes collected user behavior data and identifies patterns.
"""

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# 配置
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
COLLECTED_FILE = DATA_DIR / "collected_data.json"
REPORT_FILE = DATA_DIR / "analysis_report.json"

# 分析维度
ANALYSIS_DIMENSIONS = {
    "communication": {
        "active_hours": {},
        "channel_usage": {},
        "message_length": {},
        "question_frequency": 0.0,
    },
    "work_style": {
        "task_creation_rate": 0.0,
        "task_completion_rate": 0.0,
        "task_abandon_rate": 0.0,
        "avg_turns_per_topic": 0.0,
    },
    "patterns": {
        "abandon_keywords": [],
        "engagement_triggers": [],
        "frustration_signals": [],
    },
    "topics": {},
}


def load_collected_data() -> dict:
    """加载收集的数据"""
    if COLLECTED_FILE.exists():
        with open(COLLECTED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"messages": [], "events": []}


def parse_timestamp(ts: str) -> Optional[datetime]:
    """解析时间戳"""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except:
        return None


def analyze_time_distribution(messages: list) -> dict:
    """
    分析活跃时间分布
    
    Args:
        messages: 消息列表
        
    Returns:
        时间分布字典 {"09:00": 15, "10:00": 23, ...}
    """
    hour_counts = Counter()
    
    for msg in messages:
        ts = msg.get("timestamp", "")
        dt = parse_timestamp(ts)
        if dt:
            # 转换为本地时间 (假设 Asia/Shanghai)
            hour = dt.hour
            hour_counts[f"{hour:02d}:00"] += 1
    
    # 转换为排序的字典
    active_hours = dict(sorted(hour_counts.items()))
    
    # 计算高峰时段
    if hour_counts:
        peak_hour = hour_counts.most_common(1)[0][0]
    else:
        peak_hour = None
    
    return {
        "distribution": active_hours,
        "peak_hour": peak_hour,
        "total_hours": len(hour_counts),
    }


def analyze_channel_usage(messages: list) -> dict:
    """
    分析渠道使用
    
    Args:
        messages: 消息列表
        
    Returns:
        渠道使用字典 {"feishu": 80, "imessage": 20, ...}
    """
    channel_counts = Counter()
    
    for msg in messages:
        sender = msg.get("sender", "")
        # 只分析 Roger 的消息来确定偏好
        if sender == "Roger":
            channel = msg.get("channel", "unknown")
            channel_counts[channel] += 1
    
    return dict(channel_counts)


def analyze_message_length(messages: list) -> dict:
    """
    分析消息长度
    
    Args:
        messages: 消息列表
        
    Returns:
        消息长度统计
    """
    roger_lengths = []
    
    for msg in messages:
        if msg.get("sender") == "Roger":
            content = msg.get("content", "")
            roger_lengths.append(len(content))
    
    if not roger_lengths:
        return {"avg": 0, "min": 0, "max": 0, "total": 0}
    
    return {
        "avg": round(sum(roger_lengths) / len(roger_lengths), 1),
        "min": min(roger_lengths),
        "max": max(roger_lengths),
        "total": len(roger_lengths),
    }


def analyze_question_frequency(messages: list) -> float:
    """
    分析问句占比
    
    Args:
        messages: 消息列表
        
    Returns:
        问句占比 (0.0 - 1.0)
    """
    question_patterns = [
        r"\?$",
        r"吗[？?]",
        r"怎么[?？]",
        r"为什么[?？]",
        r"什么[?？]",
        r"如何[?？]",
        r"能否[?？]",
        r"可以[?？]",
        r"是不是",
    ]
    
    roger_count = 0
    question_count = 0
    
    for msg in messages:
        if msg.get("sender") == "Roger":
            roger_count += 1
            content = msg.get("content", "")
            
            for pattern in question_patterns:
                if re.search(pattern, content):
                    question_count += 1
                    break
    
    if roger_count == 0:
        return 0.0
    
    return round(question_count / roger_count, 3)


def analyze_task_patterns(events: list) -> dict:
    """
    分析任务模式（创建/完成/放弃）
    
    Args:
        events: 事件列表
        
    Returns:
        任务模式统计
    """
    task_created = 0
    task_completed = 0
    task_abandoned = 0
    question_asked = 0
    
    for event in events:
        event_type = event.get("type", "")
        if event_type == "task_created":
            task_created += 1
        elif event_type == "task_completed":
            task_completed += 1
        elif event_type == "task_abandoned":
            task_abandoned += 1
        elif event_type == "question_asked":
            question_asked += 1
    
    total = task_created + task_completed + task_abandoned
    
    return {
        "task_creation_count": task_created,
        "task_completion_count": task_completed,
        "task_abandon_count": task_abandoned,
        "question_count": question_asked,
        "task_creation_rate": round(task_created / max(total, 1), 3),
        "task_completion_rate": round(task_completed / max(total, 1), 3),
        "task_abandon_rate": round(task_abandoned / max(total, 1), 3),
    }


def analyze_turns_per_topic(messages: list) -> float:
    """
    分析每个话题的平均轮数
    
    Args:
        messages: 消息列表
        
    Returns:
        平均轮数
    """
    # 按会话分组
    sessions = defaultdict(list)
    
    for msg in messages:
        session_key = msg.get("session_key", "unknown")
        sessions[session_key].append(msg)
    
    if not sessions:
        return 0.0
    
    # 计算每个会话的轮数
    total_turns = sum(len(msgs) for msgs in sessions.values())
    return round(total_turns / len(sessions), 1)


def extract_topics(messages: list) -> list:
    """提取消息中的主题关键词"""
    topics = []
    
    topic_patterns = [
        (r"OpenClaw|openclaw", "OpenClaw"),
        (r"EvoMap|evomap", "EvoMap"),
        (r"iMessage|imessage", "iMessage"),
        (r"飞书|feishu", "Feishu"),
        (r"memory|MEMORY", "Memory"),
        (r"cron|Cron", "Cron"),
        (r"skill|Skill", "Skill"),
        (r"API|api", "API"),
        (r"model|Model", "Model"),
        (r"gateway|Gateway", "Gateway"),
        (r"session|Session", "Session"),
        (r"agent|Agent", "Agent"),
        (r"Go[语程]?|go", "Go语言"),
        (r"PMP|项目经理", "PMP"),
        (r"waoowaoo", "waoowaoo"),
        (r"The Machine|machine", "The Machine"),
    ]
    
    for msg in messages:
        if msg.get("sender") == "Roger":
            content = msg.get("content", "")
            
            for pattern, topic_name in topic_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    topics.append(topic_name)
    
    return topics


def analyze_topics(messages: list) -> dict:
    """
    分析话题分布
    
    Args:
        messages: 消息列表
        
    Returns:
        话题分布字典
    """
    topics = extract_topics(messages)
    topic_counts = Counter(topics)
    
    return dict(topic_counts.most_common(20))


def detect_abandon_keywords(events: list, messages: list) -> list:
    """
    检测放弃时的关键词
    
    Args:
        events: 事件列表
        messages: 消息列表
        
    Returns:
        放弃关键词列表
    """
    abandon_events = [e for e in events if e.get("type") == "task_abandoned"]
    
    if not abandon_events:
        return []
    
    # 分析放弃消息的内容
    content_samples = []
    for event in abandon_events:
        task = event.get("task", "")
        if task:
            content_samples.append(task)
    
    # 提取常见词
    keywords = []
    for content in content_samples:
        # 简单分词
        words = re.findall(r"[\u4e00-\u9fa5]{2,}|[\w]+", content)
        keywords.extend(words[:5])
    
    # 返回最常见的关键词
    keyword_counts = Counter(keywords)
    return [kw for kw, _ in keyword_counts.most_common(5)]


def detect_engagement_triggers(events: list, messages: list) -> list:
    """
    检测投入时的触发词
    
    Args:
        events: 事件列表
        messages: 消息列表
        
    Returns:
        投入触发词列表
    """
    task_events = [e for e in events if e.get("type") == "task_created"]
    
    if not task_events:
        return []
    
    triggers = []
    for event in task_events:
        task = event.get("task", "")
        if task:
            # 提取有意义的开始词
            if task.startswith(("帮我", "做个", "写个", "创建", "实现", "研究", "分析")):
                # 取前10个字符作为触发词
                triggers.append(task[:10])
    
    # 返回出现次数最多的
    trigger_counts = Counter(triggers)
    return [t for t, _ in trigger_counts.most_common(5)]


def detect_frustration(messages: list) -> list:
    """
    检测不耐烦信号
    
    Args:
        messages: 消息列表
        
    Returns:
        不耐烦信号列表
    """
    frustration_keywords = [
        "算了",
        "不做了",
        "不用了",
        "不需要",
        "别说了",
        "好了",
        "就这样",
        "不用管",
        "先这样",
        "重做",
        "不对",
        "错了",
        "不是这样",
        "需要修改",
    ]
    
    signals = []
    
    for msg in messages:
        if msg.get("sender") == "Roger":
            content = msg.get("content", "")
            
            for keyword in frustration_keywords:
                if keyword in content:
                    signals.append({
                        "keyword": keyword,
                        "context": content[:100],
                        "timestamp": msg.get("timestamp", ""),
                    })
    
    # 只返回最近的5个
    return signals[:5]


def detect_frustration_signals(messages: list) -> list:
    """
    检测不耐烦信号关键词
    
    Args:
        messages: 消息列表
        
    Returns:
        不耐烦关键词列表
    """
    frustration_keywords = [
        "算了",
        "不做了",
        "不用了",
        "不需要",
        "别说了",
        "好了",
        "就这样",
        "不用管",
        "先这样",
        "重做",
        "不对",
        "错了",
        "不是这样",
        "需要修改",
    ]
    
    found_keywords = []
    
    for msg in messages:
        if msg.get("sender") == "Roger":
            content = msg.get("content", "")
            
            for keyword in frustration_keywords:
                if keyword in content:
                    found_keywords.append(keyword)
    
    # 去重并排序
    keyword_counts = Counter(found_keywords)
    return [kw for kw, _ in keyword_counts.most_common(10)]


def generate_analysis_report(analysis: dict) -> str:
    """
    生成分析报告
    
    Args:
        analysis: 分析结果字典
        
    Returns:
        Markdown 格式报告
    """
    report = []
    report.append("# 行为分析报告")
    report.append("")
    report.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # 沟通习惯
    report.append("## 📊 沟通习惯")
    report.append("")
    
    comm = analysis.get("communication", {})
    
    # 时间分布
    time_dist = comm.get("active_hours", {})
    if time_dist.get("peak_hour"):
        report.append(f"**活跃时段**: 主要在 {time_dist['peak_hour']}")
    if time_dist.get("distribution"):
        hours = list(time_dist["distribution"].keys())
        if hours:
            report.append(f"**活跃小时数**: {time_dist.get('total_hours', 0)} 小时")
    
    # 渠道使用
    channel = comm.get("channel_usage", {})
    if channel:
        report.append(f"**常用渠道**: {', '.join(f'{k}({v})' for k, v in list(channel.items())[:3])}")
    
    # 消息长度
    msg_len = comm.get("message_length", {})
    if msg_len.get("avg"):
        report.append(f"**平均消息长度**: {msg_len['avg']} 字符")
    
    # 问句占比
    question_freq = comm.get("question_frequency", 0.0)
    if question_freq > 0:
        report.append(f"**问句占比**: {question_freq * 100:.1f}%")
    
    report.append("")
    
    # 工作风格
    report.append("## 🛠️ 工作风格")
    report.append("")
    
    work = analysis.get("work_style", {})
    
    report.append(f"**任务创建**: {work.get('task_creation_count', 0)} 个")
    report.append(f"**任务完成**: {work.get('task_completion_count', 0)} 个")
    report.append(f"**任务放弃**: {work.get('task_abandon_count', 0)} 个")
    report.append(f"**完成率**: {work.get('task_completion_rate', 0) * 100:.1f}%")
    report.append(f"**放弃率**: {work.get('task_abandon_rate', 0) * 100:.1f}%")
    report.append(f"**平均会话轮数**: {work.get('avg_turns_per_topic', 0)} 轮")
    report.append("")
    
    # 模式
    report.append("## 🔍 行为模式")
    report.append("")
    
    patterns = analysis.get("patterns", {})
    
    abandon = patterns.get("abandon_keywords", [])
    if abandon:
        report.append(f"**放弃关键词**: {', '.join(abandon)}")
    
    engage = patterns.get("engagement_triggers", [])
    if engage:
        report.append(f"**投入触发**: {', '.join(engage)}")
    
    frustration = patterns.get("frustration_signals", [])
    if frustration:
        report.append(f"**不耐烦信号**: {len(frustration)} 次")
    
    report.append("")
    
    # 话题
    report.append("## 📚 热门话题")
    report.append("")
    
    topics = analysis.get("topics", {})
    if topics:
        for topic, count in list(topics.items())[:10]:
            report.append(f"- **{topic}**: {count} 次")
    else:
        report.append("_暂无数据_")
    
    report.append("")
    report.append("---")
    report.append("_由 Nova 分析器生成_")
    
    return "\n".join(report)


def run_analysis() -> dict:
    """
    运行完整分析
    
    Returns:
        分析结果字典
    """
    print("📊 加载数据...")
    data = load_collected_data()
    
    messages = data.get("messages", [])
    events = data.get("events", [])
    
    print(f"  - 消息数: {len(messages)}")
    print(f"  - 事件数: {len(events)}")
    
    print("📈 分析时间分布...")
    time_dist = analyze_time_distribution(messages)
    
    print("📡 分析渠道使用...")
    channel_usage = analyze_channel_usage(messages)
    
    print("📏 分析消息长度...")
    message_length = analyze_message_length(messages)
    
    print("❓ 分析问句占比...")
    question_freq = analyze_question_frequency(messages)
    
    print("📋 分析任务模式...")
    task_patterns = analyze_task_patterns(events)
    
    print("💬 分析会话轮数...")
    avg_turns = analyze_turns_per_topic(messages)
    
    print("📚 分析话题分布...")
    topics = analyze_topics(messages)
    
    print("⚠️ 检测放弃关键词...")
    abandon_keywords = detect_abandon_keywords(events, messages)
    
    print("🎯 检测投入触发...")
    engagement_triggers = detect_engagement_triggers(events, messages)
    
    print("😤 检测不耐烦信号...")
    frustration_signals = detect_frustration_signals(messages)
    
    # 组装分析结果
    analysis = {
        "communication": {
            "active_hours": time_dist,
            "channel_usage": channel_usage,
            "message_length": message_length,
            "question_frequency": question_freq,
        },
        "work_style": {
            **task_patterns,
            "avg_turns_per_topic": avg_turns,
        },
        "patterns": {
            "abandon_keywords": abandon_keywords,
            "engagement_triggers": engagement_triggers,
            "frustration_signals": frustration_signals,
        },
        "topics": topics,
    }
    
    return analysis


def save_analysis_report(analysis: dict):
    """保存分析报告"""
    # 确保目录存在
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存 JSON 格式
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 分析报告已保存: {REPORT_FILE}")
    
    # 生成 Markdown 报告
    md_report = generate_analysis_report(analysis)
    md_file = REPORT_FILE.with_suffix(".md")
    
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_report)
    
    print(f"✅ Markdown 报告已保存: {md_file}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Behavior Persona - Pattern Analyzer")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (don't save)")
    
    args = parser.parse_args()
    
    print("🚀 开始行为模式分析...")
    
    analysis = run_analysis()
    
    if args.dry_run:
        print("\n--- Dry run results ---")
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        save_analysis_report(analysis)
        print("\n📄 生成报告文本...")
        print(generate_analysis_report(analysis))


if __name__ == "__main__":
    main()