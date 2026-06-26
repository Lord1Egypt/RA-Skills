#!/usr/bin/env python3
"""
AutoDream Core 示例脚本

展示如何使用 autodream-core 库。
"""

from pathlib import Path
import sys

# 添加库路径
CORE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(CORE_DIR))

from core import AutoDreamEngine
from adapters import OpenClawAdapter


def main():
    # 配置工作区路径
    workspace = Path("~/.openclaw/workspace-research").expanduser()
    
    print("🚀 AutoDream Core 示例")
    print("=" * 50)
    print(f"工作区：{workspace}")
    print()
    
    # 初始化适配器
    adapter = OpenClawAdapter(workspace=workspace)
    
    # 自定义配置（可选）
    config = {
        "hours_since_last_run": 24,
        "min_sessions_since_last": 5,
        "memory_md_max_lines": 200,
        "enable_analytics": True,
    }
    
    # 创建引擎
    engine = AutoDreamEngine(adapter, config=config)
    
    # 检查是否应该触发
    should_run = engine.should_trigger()
    print(f"触发条件：{'满足' if should_run else '不满足'}")
    
    if not should_run:
        print("使用 --force 强制运行")
        print()
    
    # 运行整理
    result = engine.run(force=True)
    
    if result.get("skipped"):
        print(f"⏭️  跳过：{result.get('reason')}")
        return
    
    # 打印结果
    print("✅ 整理完成！")
    print()
    print(f"📊 统计信息:")
    print(f"   原始条目：{result['consolidation']['original_count']}")
    print(f"   最终条目：{result['consolidation']['final_count']}")
    print(f"   删除过时：{result['consolidation']['pruned_count']}")
    print(f"   合并重复：{result['consolidation']['merged_count']}")
    print()
    print(f"   MEMORY.md: {result['prune']['memory_md_lines_before']} → {result['prune']['memory_md_lines_after']} 行")
    print(f"   耗时：{result['duration_seconds']:.2f}s")
    print()
    
    # 查看状态
    state = engine.get_state()
    print(f"📝 状态：{state.status}")
    print(f"   阶段：{state.phase}")
    print(f"   处理条目：{state.entries_processed}")
    
    # 查看 Analytics
    stats = engine.analytics.get_stats()
    print()
    print(f"📈 Analytics:")
    print(f"   总运行次数：{stats['total_runs']}")
    print(f"   成功次数：{stats['successful_runs']}")
    print(f"   失败次数：{stats['failures']}")
    print(f"   平均耗时：{stats['avg_duration_seconds']:.2f}s")


if __name__ == "__main__":
    main()
