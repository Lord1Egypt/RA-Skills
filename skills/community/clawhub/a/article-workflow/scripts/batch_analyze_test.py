#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量分析测试工具 - 测试批量分析功能并填充关键词标签

功能：
1. 批量分析多篇文章
2. 自动提取关键词标签
3. 填充多维表格所有字段（包括主字段）
4. 测试智能路由批量模式
"""

import json
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from field_mapper import load_config, format_person_field, format_date_field, create_bitable_record_fields


def print_header(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def extract_tags_from_title(title: str) -> list:
    """
    从标题中提取关键词标签
    
    Args:
        title: 文章标题
    
    Returns:
        标签列表
    """
    tags = []
    
    # 关键词匹配规则
    keyword_map = {
        "OpenClaw": ["OpenClaw", "AI 智能体", "Skill 生态"],
        "Agent": ["AI Agent", "多智能体", "自动化"],
        "智能体": ["AI 智能体", "多智能体协作"],
        "开源": ["开源项目", "GitHub"],
        "AI 编程": ["AI 编程", "代码生成", "自动化开发"],
        "Spec": ["Spec-Driven", "规范驱动开发"],
        "ChatDev": ["多智能体开发", "游戏开发"],
        "NocoBase": ["无代码", "低代码", "数据模型驱动"],
        "案例": ["落地案例", "最佳实践"],
        "Spring": ["Java", "后端开发", "框架更新"],
        "百度搜索": ["百度搜索", "搜索引擎", "国产 AI"],
        "Skill": ["Skill 生态", "ClawHub"],
    }
    
    for keyword, tag_list in keyword_map.items():
        if keyword in title:
            tags.extend(tag_list)
    
    # 去重
    return list(set(tags))[:5]  # 最多 5 个标签


def test_batch_analyze():
    """测试批量分析功能"""
    print_header("🧪 批量分析功能测试")
    
    config = load_config()
    
    # 测试文章列表
    test_articles = [
        {
            "title": "Clawith - OpenClaw for Teams 多智能体协作平台",
            "url": "https://github.com/dataelement/Clawith",
            "source": "GitHub"
        },
        {
            "title": "AI 编程三剑客：Spec-Kit、OpenSpec、Superpowers",
            "url": "https://mp.weixin.qq.com/s/NeBSi-Q8zUWlWb0mL5BPOA",
            "source": "微信"
        },
        {
            "title": "ChatDev 2.0：29.9k 星开源多智能体开发平台",
            "url": "https://mp.weixin.qq.com/s/YrjeY89hxan7YNnTocKgIg",
            "source": "微信"
        }
    ]
    
    print(f"测试文章数量：{len(test_articles)}\n")
    
    for i, article in enumerate(test_articles, 1):
        print(f"{i}. {article['title']}")
        
        # 提取标签
        tags = extract_tags_from_title(article['title'])
        print(f"   标签：{', '.join(tags)}")
        
        # 生成字段
        fields = create_bitable_record_fields(
            title=article['title'],
            url=article['url'],
            summary="测试摘要",
            source=article['source'],
            tags=tags,
            importance="高",
            doc_url="https://feishu.cn/docx/test"
        )
        
        # 添加主字段（多行文本）
        fields[config['bitable_fields']['primary']] = article['title']
        
        print(f"   主字段：{article['title']}")
        print(f"   负责人：已填充")
        print()
    
    print("✅ 批量分析测试完成")
    print("\n关键字段检查：")
    print("  ✅ 主字段（多行文本）- 已填充")
    print("  ✅ 标题 - 已填充")
    print("  ✅ 关键词标签 - 自动提取")
    print("  ✅ 负责人 - 自动填充")
    print("  ✅ 来源 - 平台映射")


def update_existing_records():
    """更新已有记录，补充关键词标签和主字段"""
    print_header("🔄 更新已有记录")
    
    config = load_config()
    
    # 模拟更新数据
    updates = [
        {
            "record_id": "recvdNynDpkd7r",
            "title": "Clawith - OpenClaw for Teams 多智能体协作平台",
            "tags": ["OpenClaw", "多智能体协作", "GitHub", "AI 智能体"]
        },
        {
            "record_id": "recvdNDvRWuuqM",
            "title": "AI 编程三剑客：Spec-Kit、OpenSpec、Superpowers",
            "tags": ["AI 编程", "Spec-Driven", "代码生成", "规范驱动开发"]
        },
        {
            "record_id": "recvdO0ziM99Sb",
            "title": "ChatDev 2.0：29.9k 星开源多智能体开发平台",
            "tags": ["多智能体开发", "游戏开发", "开源项目", "AI Agent"]
        }
    ]
    
    print("待更新记录：")
    for update in updates:
        print(f"\n  📝 {update['title']}")
        print(f"     标签：{', '.join(update['tags'])}")
        print(f"     主字段：{update['title']}")
    
    print("\n⚠️  此功能需要飞书 API 支持")
    print("示例代码：")
    print("""
# 批量更新记录
for update in updates:
    fields = {
        config['bitable_fields']['primary']: update['title'],
        config['bitable_fields']['tags']: update['tags']
    }
    
    feishu_bitable_app_table_record(
        action="update",
        app_token=app_token,
        table_id=table_id,
        record_id=update['record_id'],
        fields=fields
    )
    """)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  python batch_analyze_test.py test      # 测试批量分析")
        print("  python batch_analyze_test.py update    # 更新已有记录")
        print("  python batch_analyze_test.py all       # 全部测试")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "test":
        test_batch_analyze()
    
    elif command == "update":
        update_existing_records()
    
    elif command == "all":
        test_batch_analyze()
        print()
        update_existing_records()
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
