#!/usr/bin/env python3
"""
DataWorks Task Instance Diagnostician - All-in-One Tool

Fetches task instance log and provides diagnostic recommendations.

Usage:
    python3 dataworks_diagnose.py <instance_id> [options]

Examples:
    python3 dataworks_diagnose.py 12345678
    python3 dataworks_diagnose.py 12345678 --region cn-shanghai
    python3 dataworks_diagnose.py 12345678 --auto-fix
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run_script(script_name, args, capture=True, input_text=None):
    """Run a helper script and return output"""
    script_path = Path(__file__).parent / script_name
    
    cmd = [sys.executable, str(script_path)] + args
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=60,
            input=input_text
        )
        
        if result.returncode != 0:
            return None, result.stderr
        
        return result.stdout, None
        
    except subprocess.TimeoutExpired:
        return None, "Script execution timed out"
    except Exception as e:
        return None, str(e)


def main():
    parser = argparse.ArgumentParser(
        description="DataWorks Task Instance Diagnostician",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 12345678
  %(prog)s 12345678 --region cn-shanghai
  %(prog)s 12345678 --json
  %(prog)s 12345678 --save-report report.txt
        """
    )
    
    parser.add_argument("instance_id", help="Task instance ID")
    parser.add_argument("--region", "-r", default='cn-hangzhou',
                       help="Alibaba Cloud region (default: cn-hangzhou)")
    parser.add_argument("--access-key", help="Access Key ID")
    parser.add_argument("--access-secret", help="Access Key Secret")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show full log")
    parser.add_argument("--save-log", metavar="FILE",
                       help="Save raw log to file")
    parser.add_argument("--save-report", metavar="FILE",
                       help="Save diagnostic report to file")
    
    args = parser.parse_args()
    
    print(f"🔍 开始诊断 DataWorks 任务实例：{args.instance_id}")
    print(f"📍 区域：{args.region}")
    print("-" * 60)
    
    # Step 1: Fetch log
    print("\n📥 步骤 1/2: 获取任务日志...")
    
    fetch_args = [
        args.instance_id,
        '--region', args.region,
    ]
    
    if args.access_key:
        fetch_args.extend(['--access-key', args.access_key])
    if args.access_secret:
        fetch_args.extend(['--access-secret', args.access_secret])
    if args.verbose:
        fetch_args.append('--verbose')
    
    log_output, error = run_script('fetch_instance_log.py', fetch_args + ['--json'])
    
    if error:
        print(f"❌ 获取日志失败：{error}")
        sys.exit(1)
    
    print("✅ 日志获取成功")
    
    # Save raw log if requested
    if args.save_log:
        Path(args.save_log).write_text(log_output)
        print(f"💾 原始日志已保存到：{args.save_log}")
    
    # Parse JSON response and extract log content
    try:
        response = json.loads(log_output)
        body = response.get('body', {})
        log_content = body.get('TaskInstanceLog', '')
        request_id = body.get('RequestId', 'N/A')
        
        # Print task info
        print(f"📋 RequestId: {request_id}")
        
        if not log_content:
            print("❌ 日志内容为空")
            sys.exit(1)
        
        # Extract and print task summary
        print("\n📊 任务摘要:")
        found_summary = False
        
        # Try to find DI task summary first
        for line in log_content.split('\n'):
            if 'DI Submit at' in line:
                print(f"   {line.strip()}")
                found_summary = True
            elif 'DI Start at' in line:
                print(f"   {line.strip()}")
            elif 'DI Finish at' in line:
                print(f"   {line.strip()}")
            elif 'DI job state' in line:
                print(f"   {line.strip()}")
                found_summary = True
            elif 'ErrorMessage:' in line:
                print(f"   {line.strip()}")
        
        # If not DI task, try to find ODPS/shell task status
        if not found_summary:
            for line in log_content.split('\n'):
                if 'Current task status' in line:
                    print(f"   {line.strip()}")
                    found_summary = True
                elif 'Exit code of the Shell command' in line:
                    print(f"   {line.strip()}")
                    found_summary = True
                elif 'Shell run failed' in line:
                    print(f"   ❌ {line.strip()}")
                    found_summary = True
                elif 'FAILED:' in line and 'ODPS' in line:
                    print(f"   ❌ {line.strip()[:200]}")
                    found_summary = True
        
        if not found_summary:
            print("   (未找到任务状态信息)")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        sys.exit(1)
    
    # Step 2: Diagnose with AI analysis
    print("\n🔬 步骤 2/2: AI 智能分析中...")
    
    # Pass log content via stdin to new analyzer
    analyze_args = ['--instance-id', args.instance_id]
    if args.json:
        analyze_args.append('--json')
    
    report_output, error = run_script('analyze_error.py', analyze_args, input_text=log_content)
    
    if error:
        print(f"❌ 诊断失败：{error}")
        sys.exit(1)
    
    print("✅ 诊断完成")
    print("\n" + "=" * 60)
    print("📋 诊断报告")
    print("=" * 60)
    print(report_output)
    
    # Save report if requested
    if args.save_report:
        Path(args.save_report).write_text(report_output)
        print(f"\n💾 诊断报告已保存到：{args.save_report}")


if __name__ == "__main__":
    main()
