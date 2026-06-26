#!/usr/bin/env python3
"""
Agent Security Skill Scanner - 统一扫描入口
功能:
    一站式安全扫描解决方案
    
用法:
    python3 scanner_cli.py scan <directory>     # 扫描目录
    python3 scanner_cli.py collect             # 采集真实样本
    python3 scanner_cli.py evaluate             # 评估检测能力
    python3 scanner_cli.py report               # 生成 HTML 报告
    python3 scanner_cli.py dynamic <file>       # 动态行为分析
    python3 scanner_cli.py full                 # 完整扫描流程
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name, args=None):
    """运行脚本"""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        log(f"❌ 脚本不存在: {script_name}")
        return False
    
    cmd = ["python3", script_path]
    if args:
        cmd.extend(args)
    
    result = subprocess.run(cmd)
    return result.returncode == 0

def cmd_scan(args):
    """扫描目录"""
    log(f"🔍 扫描目录: {args.directory}")
    
    cmd = [
        "python3", 
        os.path.join(SCRIPTS_DIR, "parallel_scanner.py"),
        "--dir", os.path.abspath(args.directory),
        "--threads", str(args.threads or 8),
        "--output", args.output or "scan_result.json"
    ]
    subprocess.run(cmd)

def cmd_collect(args):
    """采集真实样本"""
    log("📦 采集真实 Skill 样本...")
    keywords = args.keywords.split() if args.keywords else ["security", "agent"]
    run_script("real_skill_collector.py", [
        "--keywords"
    ] + keywords + [
        "--limit", str(args.limit or 50),
        "--parallel", str(args.parallel or 8)
    ])

def cmd_evaluate(args):
    """评估检测能力"""
    log("📊 评估检测能力...")
    run_script("evaluation_metrics.py", [
        "--malicious-dir", args.malicious or "samples/external/malicious",
        "--benign-dir", args.benign or "samples/external/benign",
        "--output", args.output or "evaluation_report.json"
    ])

def cmd_report(args):
    """生成报告"""
    log("📈 生成 HTML 报告...")
    run_script("html_report_generator.py", [
        "--scan-result", args.scan_result or "scan_result.json",
        "--output", args.output or "security_report.html"
    ])

def cmd_dynamic(args):
    """动态行为分析"""
    log(f"🔬 动态分析: {args.file}")
    run_script("dynamic_detector.py", [
        "--file" if os.path.isfile(args.file) else "--dir",
        args.file,
        "--output", args.output or "dynamic_result.json"
    ])

def cmd_full(args):
    """完整扫描流程"""
    log("🚀 开始完整扫描流程...")
    
    # 1. 采集样本
    log("\n[1/5] 采集样本...")
    keywords = args.keywords.split() if args.keywords else ["security", "agent"]
    cmd_collect(argparse.Namespace(
        keywords=" ".join(keywords),
        limit=30,
        parallel=8
    ))
    
    # 2. 扫描
    log("\n[2/5] 扫描分析...")
    cmd_scan(argparse.Namespace(
        directory="samples/real_skills",
        threads=8,
        output="full_scan_result.json"
    ))
    
    # 3. 动态检测
    log("\n[3/5] 动态行为检测...")
    cmd_dynamic(argparse.Namespace(
        file="samples/real_skills",
        output="full_dynamic_result.json"
    ))
    
    # 4. 评估
    log("\n[4/5] 能力评估...")
    cmd_evaluate(argparse.Namespace(
        malicious="samples/external/malicious",
        benign="samples/external/benign",
        output="full_eval_result.json"
    ))
    
    # 5. 报告
    log("\n[5/5] 生成报告...")
    cmd_report(argparse.Namespace(
        scan_result="full_scan_result.json",
        output="full_security_report.html"
    ))
    
    log("\n✅ 完整扫描完成!")
    log("📁 报告: full_security_report.html")

def main():
    parser = argparse.ArgumentParser(
        description="Agent Security Skill Scanner - 统一扫描入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 scanner_cli.py scan ./my_skills
    python3 scanner_cli.py collect --keywords security agent
    python3 scanner_cli.py evaluate
    python3 scanner_cli.py report --scan-result scan_result.json
    python3 scanner_cli.py full
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # scan
    scan_parser = subparsers.add_parser("scan", help="扫描目录")
    scan_parser.add_argument("directory", help="扫描目录")
    scan_parser.add_argument("--threads", type=int, help="线程数")
    scan_parser.add_argument("--output", help="输出文件")
    
    # collect
    collect_parser = subparsers.add_parser("collect", help="采集真实样本")
    collect_parser.add_argument("--keywords", help="关键词 (空格分隔)")
    collect_parser.add_argument("--limit", type=int, help="采集数量")
    collect_parser.add_argument("--parallel", type=int, help="并行数")
    
    # evaluate
    eval_parser = subparsers.add_parser("evaluate", help="评估检测能力")
    eval_parser.add_argument("--malicious", help="恶意样本目录")
    eval_parser.add_argument("--benign", help="良性样本目录")
    eval_parser.add_argument("--output", help="输出文件")
    
    # report
    report_parser = subparsers.add_parser("report", help="生成 HTML 报告")
    report_parser.add_argument("--scan-result", help="扫描结果文件")
    report_parser.add_argument("--output", help="输出 HTML")
    
    # dynamic
    dynamic_parser = subparsers.add_parser("dynamic", help="动态行为分析")
    dynamic_parser.add_argument("file", help="文件或目录")
    dynamic_parser.add_argument("--output", help="输出文件")
    
    # full
    subparsers.add_parser("full", help="完整扫描流程")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    commands = {
        "scan": cmd_scan,
        "collect": cmd_collect,
        "evaluate": cmd_evaluate,
        "report": cmd_report,
        "dynamic": cmd_dynamic,
        "full": cmd_full,
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        log(f"未知命令: {args.command}")

if __name__ == "__main__":
    main()
