#!/usr/bin/env python3
"""
User Profile Generator - Phase 3
从分析报告生成用户画像 JSON
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 路径配置
SKILL_DIR = Path(__file__).parent.parent
ANALYSIS_FILE = SKILL_DIR / "data" / "analysis_report.json"
PROFILE_FILE = SKILL_DIR / "data" / "user-profile.json"

def load_analysis():
    if ANALYSIS_FILE.exists():
        with open(ANALYSIS_FILE, 'r') as f:
            return json.load(f)
    return {}

def generate_profile(analysis):
    """基于分析报告生成用户画像"""
    
    # 沟通习惯
    comm = analysis.get('communication', {})
    active_hours = comm.get('peak_hours', ['20:00'])[0] if comm.get('peak_hours') else '20:00'
    channels = comm.get('channels', {})
    top_channel = max(channels.keys(), default='feishu') if channels else 'feishu'
    
    # 工作风格
    work = analysis.get('work_style', {})
    completion_rate = work.get('completion_rate', 0.66)
    
    # 行为模式
    patterns = analysis.get('behavior_patterns', {})
    impatience_signals = patterns.get('impatience_count', 0)
    
    # 话题
    topics = analysis.get('topics', {})
    top_topics = list(topics.keys())[:5] if topics else ['OpenClaw', 'Agent']
    
    # 生成画像
    profile = {
        "communication": {
            "style": "direct_no_bullshit",
            "active_hours": active_hours,
            "preferred_channel": top_channel,
            "avg_message_length": comm.get('avg_message_length', 200),
            "question_ratio": comm.get('question_ratio', 0.3)
        },
        "work_style": {
            "planning": "adaptive",
            "execution": "prototype_first",
            "risk_tolerance": "medium",
            "completion_rate": completion_rate,
            "abandonment_triggers": []
        },
        "learning_mode": {
            "approach": "concept_oriented",
            "documentation_style": "minimal",
            "code_style": "pragmatic"
        },
        "patterns": {
            "impatience_signals": impatience_signals,
            "abandonment_triggers": [],
            "investment_triggers": []
        },
        "preferences": {
            "top_topics": top_topics,
            "tech_stack": ["OpenClaw", "Python", "AI Agent"],
            "work_rhythm": "evening_peak"
        },
        "insights": [
            f"Prefers {top_channel} for communication",
            f"Most active around {active_hours}",
            f"Project completion rate: {completion_rate*100:.0f}%",
            "Likes direct, concise responses",
            "Prefers prototypes over documentation"
        ],
        "confidence": min(0.5 + completion_rate * 0.3, 0.85),
        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "analysis_window_days": 30,
        "total_messages_analyzed": analysis.get('total_messages', 0)
    }
    
    return profile

def main():
    print("Generating user profile from analysis...")
    
    analysis = load_analysis()
    if not analysis:
        print("No analysis data found. Run analyzer.py first.")
        return
    
    profile = generate_profile(analysis)
    
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Profile saved to {PROFILE_FILE}")
    print(f"   Confidence: {profile['confidence']:.0%}")
    print(f"   Top topics: {', '.join(profile['preferences']['top_topics'][:3])}")
    print(f"   Active hours: {profile['communication']['active_hours']}")

if __name__ == "__main__":
    main()
