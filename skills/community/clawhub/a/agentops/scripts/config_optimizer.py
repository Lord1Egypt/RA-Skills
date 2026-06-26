#!/usr/bin/env python3
"""Agent配置优化 - 付费版

用法:
    python3 config_optimizer.py
    python3 config_optimizer.py --config-file ~/.openclaw/openclaw.json
    python3 config_optimizer.py --format markdown
"""

import argparse
import json
import os
import sys
from datetime import datetime


# 推荐配置模板
RECOMMENDED = {
    "gateway": {
        "bind": "127.0.0.1",
        "port": 3000,
    },
    "sessions": {
        "heartbeat": {
            "enabled": True,
            "interval_minutes": 15,
        },
        "memory": {
            "enabled": True,
            "auto_summary": True,
        },
    },
    "models": {
        "fallback_enabled": True,
        "max_context_tokens": 128000,
    },
    "security": {
        "exec_approvals": "on-miss",
        "sandbox_enabled": True,
    },
}


def load_config(config_path):
    """加载配置文件"""
    if not os.path.exists(config_path):
        return None, f"配置文件不存在: {config_path}"
    try:
        with open(config_path, "r") as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"JSON解析错误: {e}"


def check_config(config):
    """分析配置并生成优化建议"""
    suggestions = []

    # Gateway检查
    gateway = config.get("gateway", {})
    if gateway.get("bind") not in ("127.0.0.1", "localhost"):
        suggestions.append({
            "severity": "high",
            "category": "security",
            "issue": "Gateway绑定地址非localhost",
            "current": gateway.get("bind"),
            "recommendation": "建议绑定到 127.0.0.1 以确保安全",
        })

    if "port" not in gateway:
        suggestions.append({
            "severity": "info",
            "category": "config",
            "issue": "Gateway端口未显式配置",
            "recommendation": "建议显式设置 port: 3000",
        })

    # Heartbeat检查
    sessions = config.get("sessions", {})
    heartbeat = sessions.get("heartbeat", {})
    if not heartbeat.get("enabled", False):
        suggestions.append({
            "severity": "medium",
            "category": "reliability",
            "issue": "Heartbeat未启用",
            "recommendation": "启用heartbeat以支持后台定时任务",
        })

    # Memory检查
    memory_config = sessions.get("memory", {})
    if not memory_config.get("enabled", False):
        suggestions.append({
            "severity": "medium",
            "category": "functionality",
            "issue": "Memory未启用",
            "recommendation": "启用memory以支持Agent上下文记忆",
        })

    # Plugins检查
    plugins = config.get("plugins", {})
    if isinstance(plugins, dict) and not plugins.get("entries"):
        suggestions.append({
            "severity": "info",
            "category": "config",
            "issue": "Plugins未配置",
            "recommendation": "建议配置至少一个消息通道插件",
        })

    # Models检查
    models = config.get("models", {})
    if not isinstance(models, dict):
        suggestions.append({
            "severity": "info",
            "category": "config",
            "issue": "Models未配置",
            "recommendation": "建议配置模型fallback策略",
        })

    # 安全配置
    security = config.get("security", {})
    exec_setting = security.get("exec_approvals", "allowlist")
    if exec_setting == "full":
        suggestions.append({
            "severity": "high",
            "category": "security",
            "issue": "Exec审批模式为full（无审批）",
            "current": exec_setting,
            "recommendation": "建议使用 on-miss 或 allowlist 模式",
        })

    # 总体评分
    high = sum(1 for s in suggestions if s["severity"] == "high")
    medium = sum(1 for s in suggestions if s["severity"] == "medium")
    low = sum(1 for s in suggestions if s["severity"] == "info")
    score = max(0, 100 - high * 20 - medium * 10 - low * 5)

    return {
        "config_path": config_path,
        "timestamp": datetime.now().isoformat(),
        "score": score,
        "total_suggestions": len(suggestions),
        "severity_breakdown": {"high": high, "medium": medium, "info": low},
        "suggestions": suggestions,
    }


def format_text(result):
    """格式化文本输出"""
    lines = []
    lines.append("\n⚙️ 配置优化报告")
    lines.append("=" * 45)
    lines.append(f"  评分: {result['score']}/100")
    lines.append(f"  建议数: {result['total_suggestions']}")
    lines.append(f"  🔴 高: {result['severity_breakdown']['high']}")
    lines.append(f"  🟡 中: {result['severity_breakdown']['medium']}")
    lines.append(f"  🔵 低: {result['severity_breakdown']['info']}")
    lines.append("")

    if result["suggestions"]:
        lines.append("  📋 优化建议:")
        for i, s in enumerate(result["suggestions"], 1):
            sev_emoji = {"high": "🔴", "medium": "🟡", "info": "🔵"}[s["severity"]]
            lines.append(f"    {sev_emoji} [{i}] {s['issue']}")
            if "current" in s:
                lines.append(f"        当前: {s['current']}")
            lines.append(f"        建议: {s['recommendation']}")
    else:
        lines.append("  ✅ 配置看起来很好，暂无优化建议")

    return "\n".join(lines)


def format_markdown(result):
    """格式化为Markdown"""
    lines = []
    lines.append("# AgentOps 配置优化报告")
    lines.append("")
    lines.append(f"- **评分**: {result['score']}/100")
    lines.append(f"- **建议数**: {result['total_suggestions']}")
    lines.append(f"- **生成时间**: {result['timestamp']}")
    lines.append("")

    if result["suggestions"]:
        lines.append("## 优化建议")
        lines.append("")
        for i, s in enumerate(result["suggestions"], 1):
            lines.append(f"### {i}. {s['issue']}")
            lines.append(f"- **严重程度**: {s['severity']}")
            lines.append(f"- **类别**: {s['category']}")
            if "current" in s:
                lines.append(f"- **当前值**: `{s['current']}`")
            lines.append(f"- **建议**: {s['recommendation']}")
            lines.append("")
    else:
        lines.append("## ✅ 配置良好")
        lines.append("未发现需要优化的配置项。")

    return "\n".join(lines)


config_path = ""  # Set in main()


def main():
    global config_path
    parser = argparse.ArgumentParser(description="OpenClaw配置优化分析")
    parser.add_argument(
        "--config-file",
        default=os.path.expanduser("~/.openclaw/openclaw.json"),
        help="配置文件路径",
    )
    parser.add_argument(
        "--format", choices=["text", "markdown"], default="text",
        help="输出格式",
    )
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    config_path = args.config_file
    config, error = load_config(config_path)
    if error:
        print(f"❌ {error}")
        sys.exit(1)

    result = check_config(config)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(format_markdown(result))
    else:
        print(format_text(result))
        print(f"\n💡 AgentOps Pro 功能: 配置优化 | 其他: 健康检查、日志分析（免费）")


if __name__ == "__main__":
    main()
