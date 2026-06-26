#!/usr/bin/env python3
"""
run_pipeline.py - 一键运行完整流程

执行：搜索 → 去重 → 分类 → 摘要 → 推送

用法:
    python run_pipeline.py [--config sources.json] [--time-range 24h]
"""

import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def run_script(name, args):
    """运行脚本并返回输出"""
    cmd = [sys.executable, str(SCRIPT_DIR / name)] + args
    print(f"▶️  运行：{' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 错误：{result.stderr}", file=sys.stderr)
        return None
    
    return result.stdout

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="运行完整新闻聚合流程")
    parser.add_argument("--config", type=str, default="sources.json",
                        help="配置文件路径")
    parser.add_argument("--time-range", type=str, default="24h",
                        help="时间范围")
    parser.add_argument("--dry-run", action="store_true",
                        help="只运行到摘要，不推送")
    
    args = parser.parse_args()
    
    config_file = SCRIPT_DIR / args.config
    if not config_file.exists():
        print(f"错误：配置文件不存在 {config_file}", file=sys.stderr)
        return 1
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    print(f"📋 配置：{args.config}")
    print(f"⏰ 时间范围：{args.time_range}")
    print(f"🚀 开始流程：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 步骤 1: 搜索
    print("=" * 50)
    print("步骤 1/5: 搜索新闻")
    search_output = run_script("search_news.py", [
        "--config", str(config_file),
        "--time-range", args.time_range,
        "--output", str(SCRIPT_DIR / "temp_search.json")
    ])
    if not search_output:
        return 1
    
    # 步骤 2: 去重
    print("\n" + "=" * 50)
    print("步骤 2/5: 去重")
    dedup_output = run_script("deduplicate.py", [
        "--input", str(SCRIPT_DIR / "temp_search.json"),
        "--output", str(SCRIPT_DIR / "temp_deduped.json"),
        "--threshold", "0.85"
    ])
    if not dedup_output:
        return 1
    
    # 解析去重结果
    dedup_result = json.loads(dedup_output)
    removed = dedup_result.get("removed_count", 0)
    print(f"   移除重复：{removed} 条")
    
    # 步骤 3: 分类
    print("\n" + "=" * 50)
    print("步骤 3/5: 分类")
    cat_output = run_script("categorize.py", [
        "--input", str(SCRIPT_DIR / "temp_deduped.json"),
        "--output", str(SCRIPT_DIR / "temp_categorized.json"),
        "--config", str(config_file)
    ])
    if not cat_output:
        return 1
    
    # 解析分类结果
    cat_result = json.loads(cat_output)
    counts = cat_result.get("counts", {})
    print(f"   分类统计：{counts}")
    
    # 步骤 4: 摘要
    print("\n" + "=" * 50)
    print("步骤 4/5: 生成摘要")
    sum_output = run_script("summarize.py", [
        "--input", str(SCRIPT_DIR / "temp_categorized.json"),
        "--output", str(SCRIPT_DIR / "temp_summarized.json"),
        "--max-length", "50"
    ])
    if not sum_output:
        return 1
    
    # 步骤 5: 推送
    if not args.dry_run:
        print("\n" + "=" * 50)
        print("步骤 5/5: 推送到飞书")
        
        channel_id = config.get("feishu", {}).get("channel_id", "")
        if not channel_id:
            print("⚠️  警告：未配置 channel_id，跳过推送", file=sys.stderr)
            print("   请在 sources.json 中配置 feishu.channel_id")
        else:
            push_output = run_script("push_to_feishu.py", [
                "--input", str(SCRIPT_DIR / "temp_summarized.json"),
                "--config", str(config_file)
            ])
            if push_output:
                push_result = json.loads(push_output)
                if push_result.get("success"):
                    print(f"   ✅ 推送成功！消息长度：{push_result.get('message_length', 0)}")
                else:
                    print(f"   ❌ 推送失败：{push_result}")
    else:
        print("\n" + "=" * 50)
        print("🧪 干运行模式：跳过推送")
    
    # 清理临时文件（可选）
    # for f in ["temp_search.json", "temp_deduped.json", "temp_categorized.json", "temp_summarized.json"]:
    #     (SCRIPT_DIR / f).unlink(missing_ok=True)
    
    print("\n" + "=" * 50)
    print(f"✅ 流程完成：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
