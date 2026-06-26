#!/usr/bin/env python3
"""
AutoDream-Core CLI — 通用记忆整理引擎命令行入口

用法 | Usage:
    python scripts/run.py [--force] [--workspace PATH] [--dry-run]

选项 | Options:
    --force, -f      强制运行，忽略时间/会话阈值 | Force run, ignore thresholds
    --workspace, -w  指定工作目录 | Specify workspace path
    --dry-run, -d    干运行，不实际修改 | Dry run, no actual modifications
    --help, -h       显示帮助信息 | Show help

示例 | Examples:
    # 基础运行 | Basic run
    python scripts/run.py

    # 强制运行 | Force run
    python scripts/run.py --force

    # 指定工作目录 | Specify workspace
    python scripts/run.py --workspace ~/.openclaw/workspace-research

    # 干运行 | Dry run
    python scripts/run.py --dry-run
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# 添加核心模块路径
script_dir = Path(__file__).parent
core_dir = script_dir.parent / "core"
sys.path.insert(0, str(core_dir.parent))

from core import AutoDreamEngine
from adapters import OpenClawAdapter


def parse_args():
    """解析命令行参数 | Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="AutoDream-Core — 通用记忆整理引擎 | Universal Memory Consolidation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 | Examples:
  python run.py --force
  python run.py --workspace ~/.openclaw/workspace-research
  python run.py --dry-run
        """
    )
    
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="强制运行，忽略时间/会话阈值 | Force run, ignore thresholds"
    )
    
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        default=None,
        help="指定工作目录 | Specify workspace path (default: ~/.openclaw/workspace-research)"
    )
    
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="干运行，不实际修改 | Dry run, no actual modifications"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出 | Verbose output"
    )
    
    return parser.parse_args()


def main():
    """主函数 | Main function"""
    args = parse_args()
    
    # 确定工作目录 | Determine workspace
    if args.workspace:
        workspace = Path(args.workspace).expanduser()
    else:
        workspace = Path("~/.openclaw/workspace-research").expanduser()
    
    if not workspace.exists():
        print(f"❌ 工作目录不存在 | Workspace does not exist: {workspace}")
        sys.exit(1)
    
    print(f"🔧 AutoDream-Core v1.0.0")
    print(f"📁 工作目录 | Workspace: {workspace}")
    print(f"⏰ 时间 | Time: {datetime.now(timezone.utc).isoformat()}")
    print()
    
    # 初始化适配器 | Initialize adapter
    try:
        adapter = OpenClawAdapter(workspace=workspace)
        print(f"✅ 适配器初始化成功 | Adapter initialized")
    except Exception as e:
        print(f"❌ 适配器初始化失败 | Adapter initialization failed: {e}")
        sys.exit(1)
    
    # 创建引擎 | Create engine
    engine = AutoDreamEngine(
        adapter,
        max_memory_lines=200,
        stale_days=30,
        enable_analytics=True,
    )
    
    # 运行整理 | Run consolidation
    try:
        print(f"🚀 开始整理 | Starting consolidation...")
        print()
        
        result = engine.run(
            force=args.force,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )
        
        # 输出结果 | Output results
        print()
        print("=" * 50)
        print("📊 整理结果 | Consolidation Results")
        print("=" * 50)
        
        if "orientation" in result:
            print(f"📁 记忆文件 | Memory files: {result['orientation'].get('memory_files', 0)}")
            print(f"📝 总条目数 | Total entries: {result['orientation'].get('total_entries', 0)}")
        
        if "gather" in result:
            print(f"🔍 新信号 | New signals: {result['gather'].get('new_signals', 0)}")
            print(f"💬 扫描会话 | Sessions scanned: {result['gather'].get('session_scanned', 0)}")
        
        if "consolidation" in result:
            print(f"🔗 合并条目 | Merged: {result['consolidation'].get('merged', 0)}")
            print(f"🗑️  删除过期 | Removed stale: {result['consolidation'].get('removed_stale', 0)}")
            print(f"✅ 最终条目 | Final count: {result['consolidation'].get('final_count', 0)}")
        
        if "prune" in result:
            print(f"📏 行数变化 | Lines: {result['prune'].get('lines_before', 0)} → {result['prune'].get('lines_after', 0)}")
        
        print()
        print("✨ 整理完成 | Consolidation complete!")
        
        # 返回状态码 | Return status code
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 整理失败 | Consolidation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
