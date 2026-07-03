#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_publish.py - 批量发布脚本
从JSON文件读取发布列表，批量发布到多平台
"""

import json
import argparse
import logging
from auto_publish import AutoPublisher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BatchPublish')

def load_publish_list(list_path):
    """加载发布列表"""
    try:
        with open(list_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"❌ 发布列表文件未找到: {list_path}")
        return None
    except json.JSONDecodeError:
        logger.error(f"❌ 发布列表文件格式错误: {list_path}")
        return None

def save_results(results, output_path):
    """保存发布结果"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ 发布结果已保存: {output_path}")
    except Exception as e:
        logger.error(f"❌ 保存结果失败: {str(e)}")

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='批量发布脚本')
    parser.add_argument('--list', required=True, help='发布列表JSON文件路径')
    parser.add_argument('--config', default='scripts/config.json', help='配置文件路径')
    parser.add_argument('--output', default='publish_results.json', help='结果输出文件路径')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行（不实际发布）')
    
    args = parser.parse_args()
    
    # 加载发布列表
    publish_list = load_publish_list(args.list)
    if not publish_list:
        return 1
    
    logger.info(f"📋 加载发布列表: {len(publish_list)} 个任务")
    
    # 初始化发布器
    if not args.dry_run:
        publisher = AutoPublisher(config_path=args.config)
    
    # 执行批量发布
    results = []
    
    for i, item in enumerate(publish_list, 1):
        logger.info(f"📤 [{i}/{len(publish_list)}] 正在发布: {item.get('title', 'N/A')}")
        
        if args.dry_run:
            # 模拟运行
            result = {
                "success": True,
                "dry_run": True,
                "item": item,
                "message": "模拟运行，未实际发布"
            }
            logger.info(f"🧪 [模拟] 将发布到 {item['platform']}: {item['title']}")
        else:
            # 实际发布
            result = publisher.publish(
                platform=item["platform"],
                video_path=item["video"],
                title=item["title"],
                description=item.get("desc", ""),
                tags=item.get("tags", []),
                publish_time=item.get("publish_time", "now")
            )
        
        results.append({
            "index": i,
            "item": item,
            "result": result,
            "timestamp": str(__import__('datetime').datetime.now())
        })
        
        # 输出进度
        status = "✅" if result.get("success") else "❌"
        logger.info(f"{status} [{i}/{len(publish_list)}] 完成: {item.get('title', 'N/A')}")
    
    # 统计结果
    success_count = sum(1 for r in results if r["result"].get("success"))
    failed_count = len(results) - success_count
    
    logger.info("="*60)
    logger.info(f"📊 发布完成: 成功 {success_count}/{len(results)}, 失败 {failed_count}/{len(results)}")
    logger.info("="*60)
    
    # 保存结果
    save_results(results, args.output)
    
    return 0 if failed_count == 0 else 1

if __name__ == '__main__':
    exit(main())
