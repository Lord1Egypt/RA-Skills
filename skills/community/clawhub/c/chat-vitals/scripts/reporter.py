#!/usr/bin/env python3
"""
Chat Vitals - Reporter
生成监控报告
"""

import json
import os
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path.home() / ".openclaw" / "skills" / "chat-vitals"
DATA_DIR = SKILL_DIR / "data"
SESSION_DIR = DATA_DIR / "sessions"
REPORT_DIR = DATA_DIR / "reports"
CONFIG_PATH = SKILL_DIR / "config.json"

def ensure_report_dir():
    """确保报告目录存在"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    """加载配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_all_sessions(days=7):
    """加载会话"""
    sessions = []
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    for sf in SESSION_DIR.glob("*.json"):
        with open(sf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            start_time = datetime.fromisoformat(data.get("start_time", "2000-01-01"))
            if start_time >= cutoff:
                sessions.append(data)
    
    return sessions

def get_status_emoji(status):
    """状态表情"""
    return {
        "excellent": "🟢",
        "good": "🟡",
        "warning": "🟠",
        "danger": "🔴"
    }.get(status, "⚪")

def get_status_label(score):
    """状态标签"""
    if score >= 85:
        return "高效协作"
    elif score >= 70:
        return "偶有摩擦"
    elif score >= 50:
        return "需要关注"
    else:
        return "严重告警"

def generate_session_report(session_id):
    """生成单个会话报告"""
    # 调用 analyzer 分析
    import subprocess
    result = subprocess.run(
        ["python3", str(SKILL_DIR / "scripts" / "analyzer.py"), "session", session_id],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return None
    
    analysis = json.loads(result.stdout)
    
    # 生成 Markdown 报告
    report = f"""# 📊 LLM 会话监控报告

## 会话概览

| 项目 | 内容 |
|------|------|
| 会话ID | `{analysis['session_id']}` |
| 使用模型 | {analysis['model']} |
| 总轮次 | {analysis['total_turns']} |
| 总Token | {analysis['total_tokens']:,} |

## 健康评分

{get_status_emoji(analysis['status'])} **{analysis['health_score']}/100** - {get_status_label(analysis['health_score'])}

```
{generate_score_bar(analysis['health_score'])}
```

## 核心指标

### 1️⃣ 一次做对能力

| 指标 | 数值 | 状态 |
|------|------|------|
| 首通率 | {analysis['first_try_success_rate']:.1f}% | {'✅ 一次做对' if analysis['first_try_success'] else '⚠️ 需要返工'} |
| 返工次数 | {analysis['rework_count']} | {'✅ 无返工' if analysis['rework_count'] == 0 else '⚠️ 有返工'} |

### 2️⃣ 承诺兑现能力

| 指标 | 数值 | 状态 |
|------|------|------|
| 承诺次数 | {analysis['promise_count']} | - |
| 兑现率 | {analysis['promise_fulfillment_rate']:.1f}% | {'✅' if analysis['promise_fulfillment_rate'] >= 80 else '⚠️' if analysis['promise_fulfillment_rate'] >= 60 else '🔴'} |
| 计划膨胀指数 | {analysis['plan_inflation_index']:.2f}x | {'✅' if analysis['plan_inflation_index'] <= 1.3 else '⚠️' if analysis['plan_inflation_index'] <= 2.0 else '🔴'} |

### 3️⃣ 对话效率

| 指标 | 数值 |
|------|------|
| Token效率 | {analysis['token_efficiency']:.4f} |
| 平均每轮Token | {analysis['total_tokens'] // analysis['total_turns'] if analysis['total_turns'] > 0 else 0:,} |

## 诊断建议

{generate_diagnosis(analysis)}

---
*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    return report

def generate_score_bar(score):
    """生成ASCII进度条"""
    filled = int(score / 5)
    empty = 20 - filled
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {score}%"

def generate_diagnosis(analysis):
    """生成诊断建议"""
    suggestions = []
    
    if not analysis['first_try_success']:
        suggestions.append("💡 **优化建议 - 提升首通率**：\n   - 初始提示词更详细具体\n   - 明确输出格式要求\n   - 提供示例参考")
    
    if analysis['promise_fulfillment_rate'] < 80:
        suggestions.append("💡 **优化建议 - 减少过度承诺**：\n   - 要求模型每步完成后确认\n   - 设定明确的完成标准\n   - 复杂任务拆分为子任务")
    
    if analysis['plan_inflation_index'] > 1.5:
        suggestions.append("💡 **优化建议 - 控制计划膨胀**：\n   - 要求模型先给出完整计划\n   - 设定最大轮次限制\n   - 定期确认进度与计划一致性")
    
    if analysis['rework_count'] > 2:
        suggestions.append("💡 **优化建议 - 减少返工**：\n   - 建立检查清单\n   - 关键节点要求确认\n   - 记录常见误解模式")
    
    if not suggestions:
        return "✨ 本次会话表现优秀，继续保持！"
    
    return "\n\n".join(suggestions)

def generate_daily_report():
    """生成日报"""
    import subprocess
    
    # 获取趋势数据
    result = subprocess.run(
        ["python3", str(SKILL_DIR / "scripts" / "analyzer.py"), "trend", "1"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0 or not result.stdout.strip():
        return "今日暂无会话数据"
    
    trend = json.loads(result.stdout)
    if not trend:
        return "今日暂无会话数据"
    
    today = trend[0]
    
    report = f"""# 📈 LLM 监控日报 - {today['date']}

## 今日概览

| 指标 | 数值 |
|------|------|
| 会话数 | {today['session_count']} |
| 总Token消耗 | {today['total_tokens']:,} |
| 平均健康分 | {today['avg_health_score']:.1f} |
| 首通率 | {today['first_try_rate']:.1f}% |
| 总返工次数 | {today['total_rework']} |

## 健康状态

{get_status_emoji(get_health_status(today['avg_health_score']))} **{get_status_label(today['avg_health_score'])}**

```
{generate_score_bar(int(today['avg_health_score']))}
```

---
*日报生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    return report

def get_health_status(score):
    """获取状态"""
    if score >= 85:
        return "excellent"
    elif score >= 70:
        return "good"
    elif score >= 50:
        return "warning"
    else:
        return "danger"

def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: reporter.py <command> [args...]")
        print("Commands:")
        print("  session <session_id>  - 生成会话报告")
        print("  daily                - 生成日报")
        print("  save <type>         - 保存报告到文件")
        return
    
    cmd = sys.argv[1]
    ensure_report_dir()
    
    if cmd == "session":
        if len(sys.argv) < 3:
            print("Usage: session <session_id>")
            return
        sid = sys.argv[2]
        report = generate_session_report(sid)
        if report:
            print(report)
        else:
            print(f"Failed to generate report for session {sid}")
    
    elif cmd == "daily":
        report = generate_daily_report()
        print(report)
    
    elif cmd == "save":
        report_type = sys.argv[2] if len(sys.argv) > 2 else "daily"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if report_type == "daily":
            report = generate_daily_report()
            filename = f"daily_{datetime.now().strftime('%Y%m%d')}.md"
        else:
            print(f"Unknown report type: {report_type}")
            return
        
        report_path = REPORT_DIR / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()
