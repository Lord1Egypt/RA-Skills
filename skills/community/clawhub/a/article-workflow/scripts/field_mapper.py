#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字段映射增强工具 - 优化 Bitable 字段填充

功能：
1. 自动填充负责人（使用当前用户）
2. 来源平台映射（今日头条→微信等）
3. 封面图片提取
4. 附件管理
5. 批量更新已有记录
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_FILE = SKILL_DIR / "config.json"


def load_config() -> dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_current_user_id() -> str:
    """获取当前用户 ID（从环境变量或配置）"""
    # 优先从环境变量获取
    user_id = os.environ.get('FEISHU_USER_ID')
    if user_id:
        return user_id
    
    # 从配置获取
    config = load_config()
    return config.get('auto_assign', {}).get('default_assignee', '')


def map_source_platform(platform: str, config: dict) -> str:
    """
    映射来源平台到 Bitable 选项
    
    Args:
        platform: 原始平台名称
        config: 配置文件
    
    Returns:
        Bitable 中的选项值
    """
    mapping = config.get('bitable_field_mapping', {}).get('source_platform', {})
    return mapping.get(platform, "微信")


def format_person_field(user_id: str, name: str = "") -> List[Dict]:
    """
    格式化人员字段
    
    Args:
        user_id: 用户 open_id
        name: 用户姓名（可选）
    
    Returns:
        Bitable 人员字段格式
    """
    if not user_id:
        return []
    
    return [{
        "id": user_id,
        "name": name or "用户",
        "type": "user"
    }]


def format_date_field(date_str: str = None) -> int:
    """
    格式化日期字段为毫秒时间戳
    
    Args:
        date_str: 日期字符串（YYYY-MM-DD）
    
    Returns:
        毫秒时间戳
    """
    if date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        dt = datetime.now()
    
    return int(dt.timestamp() * 1000)


def format_tags_field(tags: List[str]) -> List[str]:
    """
    格式化标签字段
    
    Args:
        tags: 标签列表
    
    Returns:
        Bitable 多选字段格式
    """
    return tags if tags else []


def extract_cover_image_url(content: str) -> Optional[str]:
    """
    从内容中提取封面图片 URL
    
    Args:
        content: 文章内容
    
    Returns:
        图片 URL 或 None
    """
    import re
    # 匹配 Markdown 图片语法 ![alt](url)
    pattern = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(pattern, content)
    
    if matches:
        return matches[0]  # 返回第一张图片
    return None


def create_bitable_record_fields(
    title: str,
    url: str,
    summary: str = "",
    source: str = "微信",
    tags: List[str] = None,
    importance: str = "中",
    doc_url: str = "",
    assignee_id: str = None,
    read_date: str = None,
    config: dict = None
) -> Dict[str, Any]:
    """
    创建 Bitable 记录字段
    
    Args:
        title: 标题
        url: URL
        summary: 摘要
        source: 来源平台
        tags: 标签列表
        importance: 重要程度
        doc_url: 详细报告链接
        assignee_id: 负责人 ID
        read_date: 阅读日期
        config: 配置文件
    
    Returns:
        Bitable 字段字典
    """
    if config is None:
        config = load_config()
    
    if assignee_id is None:
        assignee_id = get_current_user_id()
    
    # 映射来源平台
    mapped_source = map_source_platform(source, config)
    
    fields = {
        config['bitable_fields']['title']: title,
        config['bitable_fields']['url']: url,
        config['bitable_fields']['summary']: summary,
        config['bitable_fields']['read_date']: format_date_field(read_date),
        config['bitable_fields']['source']: mapped_source,
        config['bitable_fields']['tags']: format_tags_field(tags or []),
        config['bitable_fields']['importance']: importance,
        config['bitable_fields']['doc_url']: doc_url,
        config['bitable_fields']['status']: "已完成",
        config['bitable_fields']['creation_method']: "自动分析",
    }
    
    # 添加负责人（如果有）
    if assignee_id:
        fields[config['bitable_fields']['assignee']] = format_person_field(assignee_id)
    
    return fields


def print_field_mapping_demo():
    """打印字段映射演示"""
    config = load_config()
    
    print("\n" + "="*60)
    print("  📊 Bitable 字段映射演示")
    print("="*60 + "\n")
    
    print("配置字段映射：")
    for key, value in config.get('bitable_fields', {}).items():
        print(f"  {key:20} → {value}")
    
    print("\n来源平台映射：")
    for original, mapped in config.get('bitable_field_mapping', {}).get('source_platform', {}).items():
        print(f"  {original:15} → {mapped}")
    
    print("\n示例记录：")
    example = create_bitable_record_fields(
        title="测试文章标题",
        url="https://example.com/article",
        summary="这是测试摘要",
        source="今日头条",
        tags=["OpenClaw", "AI"],
        importance="高",
        doc_url="https://feishu.cn/docx/xxx",
        assignee_id=get_current_user_id(),
        config=config
    )
    
    for field, value in example.items():
        if isinstance(value, list):
            print(f"  {field:20} : [{len(value)} 项]")
        else:
            print(f"  {field:20} : {value}")
    
    print()


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  python field_mapper.py demo      # 查看字段映射演示")
        print("  python field_mapper.py check     # 检查配置")
        print("  python field_mapper.py test      # 测试字段生成")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "demo":
        print_field_mapping_demo()
    
    elif command == "check":
        config = load_config()
        print("\n✅ 配置检查")
        print(f"   Bitable App Token: {config.get('bitable', {}).get('app_token', '未配置')[:10]}...")
        print(f"   Table ID: {config.get('bitable', {}).get('table_id', '未配置')}")
        print(f"   默认负责人：{get_current_user_id()}")
        print()
    
    elif command == "test":
        print("\n🧪 测试字段生成")
        fields = create_bitable_record_fields(
            title="OpenClaw 智能路由优化",
            url="https://example.com/article",
            summary="智能路由优化方案测试",
            source="今日头条",
            tags=["OpenClaw", "智能路由", "性能优化"],
            importance="高",
            doc_url="https://feishu.cn/docx/xxx"
        )
        print("\n生成的字段：")
        for field, value in fields.items():
            print(f"  {field}: {value}")
        print()
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
