#!/usr/bin/env python3
"""
每日自我检查闭环
自动扫描系统状态，发现问题自动修复，不能修复上报飞书
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple

# 检查项定义
CHECKS = [
    {
        "name": "目录结构规范检查",
        "command": "python3 /app/working/scripts/system/maintenance/verify_directory_structure.py",
        "critical": True
    },
    {
        "name": "记忆索引一致性同步",
        "command": "python3 -m skills.memory-syncer.__init__ --fix",
        "critical": False
    },
    {
        "name": "安全基线检查",
        "command": "cd /app/working/skills/claw-security-suite && python lib/security_patrol.py daily",
        "critical": True
    },
    {
        "name": "硬编码密钥扫描",
        "command": "cd /app/working/skills/claw-security-suite && python lib/static_scanner.py /app/working/scripts /app/working/skills claw-security-suite",
        "critical": False
    },
    {
        "name": "磁盘使用检查",
        "command": "df -h / | awk 'NR==2 {print $5}'",
        "critical": False
    },
]

def run_check(check: Dict) -> Tuple[bool, str, str]:
    """运行单个检查，返回(是否成功, 标准输出, 标准错误)"""
    print(f"\n🔍 开始检查: {check['name']}")
    try:
        result = subprocess.run(
            check["command"],
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"✅ {check['name']}: 通过")
            return True, result.stdout, result.stderr
        else:
            print(f"❌ {check['name']}: 失败 (exit code {result.returncode})")
            return False, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ {check['name']}: 异常 - {e}")
        return False, "", str(e)

def generate_report(results: List[Dict]) -> str:
    """生成自检报告Markdown"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    failed = total - passed
    
    report = f"# 🧠 每日自我进化自检报告 - {now}\n\n"
    report += f"**结果**: {passed}/{total} 检查通过，{failed} 项失败\n\n"
    
    report += "| 检查项 | 状态 |\n"
    report += "|--------|------|\n"
    for r in results:
        status = "✅ 通过" if r["passed"] else "❌ 失败"
        report += f"| {r['name']} | {status} |\n"
    
    if failed > 0:
        report += "\n## ❌ 失败详情\n\n"
        for r in results:
            if not r["passed"]:
                report += f"### {r['name']}\n"
                if r["stdout"]:
                    report += "**输出:**\n```\n" + r["stdout"] + "\n```\n"
                if r["stderr"]:
                    report += "**错误:**\n```\n" + r["stderr"] + "\n```\n"
        report += "\n⚠️ 请查看失败详情，手动处理无法自动修复的问题\n"
    
    else:
        report += "\n🎉 全部检查通过！系统状态良好，持续稳定运行。\n"
    
    report += "\n---\n*自动生成，每天凌晨运行*"
    return report

def main():
    print("🚀 开始每日自我检查...")
    
    results = []
    for check in CHECKS:
        passed, stdout, stderr = run_check(check)
        results.append({
            "name": check["name"],
            "passed": passed,
            "stdout": stdout,
            "stderr": stderr,
            "critical": check["critical"]
        })
    
    report = generate_report(results)
    
    # 保存报告
    report_dir = "/app/working/logs/self-check/"
    os.makedirs(report_dir, exist_ok=True)
    filename = f"self-check-{datetime.now().strftime('%Y%m%d')}.md"
    report_path = os.path.join(report_dir, filename)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📝 报告已保存: {report_path}")
    
    # 🧠 汇总学习记录统计（self-improving-agent 思路整合）
    print("\n📚 学习记录汇总：")
    learning_dir = "/app/working/memory/learnings/"
    for fname in ["ERRORS.md", "LEARNINGS.md", "FEATURE_REQUESTS.md"]:
        fpath = os.path.join(learning_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                entries = content.count('## ')
                print(f"  {fname}: {entries} 条记录")
    
    # 追加到报告
    with open(report_path, "a", encoding='utf-8') as f:
        f.write("\n\n---\n\n## 📚 学习记录汇总\n\n")
        f.write("| 文件 | 记录条数 |\n")
        f.write("|------|---------|\n")
        for fname in ["ERRORS.md", "LEARNINGS.md", "FEATURE_REQUESTS.md"]:
            fpath = os.path.join(learning_dir, fname)
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f_read:
                    content = f_read.read()
                    entries = content.count('## ')
                    f.write(f"| {fname} | {entries} |\n")
    
    # 检查是否有失败项，如有失败需要推送飞书
    failed_critical = sum(1 for r in results if not r["passed"] and r["critical"])
    
    if failed_critical > 0:
        print(f"⚠️  {failed_critical} 项关键检查失败，需要人工处理")
        # 这里返回非零，让调度系统推送报告给飞书
        sys.exit(1)
    else:
        print("✅ 所有关键检查通过")
        sys.exit(0)

if __name__ == "__main__":
    main()
