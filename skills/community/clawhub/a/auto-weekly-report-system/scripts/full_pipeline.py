#!/usr/bin/env python3
"""
完整自动化流程
一键完成：数据收集 → 报告生成 → 发布
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_step(name, command):
    """执行步骤"""
    print(f"\n{'='*60}")
    print(f"📌 {name}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"❌ {name} 失败")
        return False
    
    print(f"✅ {name} 完成")
    return True

def main():
    script_dir = Path(__file__).parent
    
    print("🚀 启动自动周报系统")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 步骤 1: 收集数据
    if not run_step("步骤 1/3: 收集数据", f"python3 {script_dir}/collector.py"):
        print("\n❌ 流程中断：数据收集失败")
        return 1
    
    # 步骤 2: 生成报告
    if not run_step("步骤 2/3: 生成报告", f"python3 {script_dir}/generator.py"):
        print("\n❌ 流程中断：报告生成失败")
        return 1
    
    # 步骤 3: 发布（模拟模式）
    print(f"\n{'='*60}")
    print(f"📌 步骤 3/3: 发布报告")
    print(f"{'='*60}")
    print("\n⚠️  注意: 当前为模拟模式")
    print("   实际发布需要手动执行 wecom_mcp 命令")
    print("   或设置企业微信 API 凭证")
    
    # 生成发布命令文件
    cmd_file = "/tmp/publish_weekly.sh"
    with open(cmd_file, 'w') as f:
        f.write(f"""#!/bin/bash
# 自动周报发布脚本
# 生成时间: {datetime.now().isoformat()}

cd {script_dir}
echo "发布周报到企业微信..."
python3 publisher.py --title "MoltbookAgent 周报 $(date +%Y-%m-%d)"
""")
    
    print(f"\n💾 发布脚本已保存: {cmd_file}")
    print(f"   手动发布: bash {cmd_file}")
    
    # 显示报告预览
    print(f"\n{'='*60}")
    print("📄 报告预览")
    print(f"{'='*60}")
    
    try:
        with open("/tmp/weekly_report_auto.md", 'r') as f:
            preview = f.read()[:500]
        print(preview + "\n... (已截断)")
    except:
        print("无法读取报告预览")
    
    print(f"\n{'='*60}")
    print("✅ 自动周报流程完成")
    print(f"{'='*60}")
    print(f"\n📊 输出文件:")
    print(f"   - 数据: /tmp/weekly_data.json")
    print(f"   - 报告: /tmp/weekly_report_auto.md")
    print(f"   - 发布: {cmd_file}")
    
    print(f"\n💡 设置定时任务:")
    print(f"   cron add --name \"weekly-report\" --schedule \"0 17 * * 5\" \\")
    print(f"     --command \"python3 {script_dir}/full_pipeline.py\"")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
