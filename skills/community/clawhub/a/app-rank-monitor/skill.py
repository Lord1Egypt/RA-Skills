#!/usr/bin/env python3
"""
App Monitor Skill - OpenClaw 入口
处理用户自然语言命令，调用底层 CLI 工具
"""

import subprocess
import sys
import os
from pathlib import Path

SKILL_DIR = Path(__file__).parent
SRC_DIR = SKILL_DIR / "src"
TOOLS_DIR = SKILL_DIR / "tools"

# 设置 Python 路径
os.environ["PYTHONPATH"] = str(SRC_DIR)


def run_command(cmd: list, cwd: Path = None) -> str:
    """运行 CLI 命令"""
    if cwd is None:
        cwd = SRC_DIR
    
    env = {**os.environ, "PYTHONPATH": str(SRC_DIR)}
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            env=env,
            timeout=300  # 5 分钟超时
        )
        output = result.stdout + result.stderr
        return output.strip() if output else "命令执行完成"
    except subprocess.TimeoutExpired:
        return "⚠️ 命令执行超时（超过 5 分钟），任务可能仍在后台运行"
    except Exception as e:
        return f"❌ 执行失败：{e}"


def extract_url(text: str) -> str:
    """从文本中提取 URL"""
    import re
    urls = re.findall(r'https?://[^\s]+', text)
    return urls[-1] if urls else ""


def handle_task(task: str) -> str:
    """处理用户任务"""
    task_lower = task.lower()
    
    # 1. 爬取榜单
    if any(kw in task_lower for kw in ["榜单", "爬取", "排行榜"]):
        if "苹果" in task_lower or "ios" in task_lower:
            return run_command(["main.py", "apple-rank", "--detect-offline"])
        elif "点点" in task_lower:
            return run_command(["main.py", "rank", "--platform", "diandian"])
        else:
            # 默认爬取所有
            return run_command(["main.py", "rank", "--send-report"])
    
    # 2. 发送日报/报告
    elif any(kw in task_lower for kw in ["日报", "报告", "发送"]):
        return run_command(["main.py", "report"])
    
    # 3. 清理数据
    elif "清理" in task_lower:
        return run_command(["python", str(TOOLS_DIR / "cleanup_apple_data.py"), "--execute"])
    
    # 4. 查看统计
    elif any(kw in task_lower for kw in ["统计", "数据"]):
        return run_command(["python", str(TOOLS_DIR / "show_stats.py")])
    
    # 5. 下架检测
    elif "下架" in task_lower:
        return run_command(["main.py", "offline", "--platform", "all"])
    
    # 6. 帮助
    elif any(kw in task_lower for kw in ["帮助", "help", "用法"]):
        return """
📊 **App Monitor Skill 帮助**

**可用命令**:
- 爬取苹果榜单 - 获取 iOS 榜单数据并检测下架
- 爬取点点榜单 - 获取第三方榜单数据
- 发送日报 - 生成并发送榜单报告
- 查看统计 - 显示数据统计
- 清理数据 - 删除过期数据
- 查看下架应用 - 显示下架记录

**示例**:
- "查看今天的苹果榜单"
- "爬取点点榜单"
- "发送日报"
- "查看下架应用"
- "清理过期数据"

**支持平台**:
🍎 苹果（官方 RSS） | 📈 点点数据
"""
    
    # 默认：显示帮助
    else:
        return """👋 我是应用榜单监控助手！

我可以帮你：
- 📊 爬取应用榜单（苹果/点点）
- 🔍 检测下架应用并通知
- 📧 发送钉钉通知（文字 + 文件）
- 🧹 自动清理过期数据（保留 7 天）

**试试这样说**:
- "查看今天的苹果榜单"
- "爬取点点榜单"
- "发送日报"
- "查看下架应用"

输入"帮助"查看更多命令
"""


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(handle_task(""))
        return
    
    task = " ".join(sys.argv[1:])
    result = handle_task(task)
    print(result)


if __name__ == "__main__":
    main()
