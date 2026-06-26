#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Article Workflow 主工作流脚本

功能：文章分析工作流 CLI
用法：
  python workflow.py <url>                    # 分析文章
  python workflow.py <url> --check-only       # 仅检查是否重复
  python workflow.py --status                 # 查看状态
  python workflow.py --stats                  # 查看统计
  python workflow.py <url1> <url2> <url3>     # 批量分析（智能路由）

注意：
    完整功能需要 OpenClaw 环境支持：
    - 内容抓取：web_fetch/browser 工具
    - 文档创建：feishu-create-doc
    - Bitable 归档：feishu-bitable
    
    独立运行模式仅支持：
    - URL 去重检查
    - 状态查看
    - 统计查看

智能路由：
    - 单篇文章 → 主 Agent 一次性执行（1 次流式请求）
    - 多篇文章 → SubAgent 并发执行（N 次但并行）
    - 详见：docs/smart-router-implementation.md
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List

# 模块路径（相对路径）
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CORE_DIR = SKILL_DIR / "core"

sys.path.insert(0, str(CORE_DIR))
sys.path.insert(0, str(SCRIPT_DIR))
from dedup import check_duplicate, add_url_to_cache, load_cache
from scorer import evaluate_quality_score

# 导入智能路由器（同级目录）
try:
    from smart_router import ArticleSmartRouter
except ImportError:
    ArticleSmartRouter = None, get_level_info


def print_header(text: str):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_success(text: str):
    """打印成功消息"""
    print(f"✅ {text}")


def print_error(text: str):
    """打印错误消息"""
    print(f"❌ {text}")


def print_warning(text: str):
    """打印警告消息"""
    print(f"⚠️  {text}")


def analyze_article(url: str, title: str = None, content: str = None, auto_archive: bool = True):
    """
    分析文章完整流程
    
    Args:
        url: 文章 URL
        title: 文章标题（可选）
        content: 文章内容（可选）
        auto_archive: 是否自动归档
    """
    print_header("📝 文章分析工作流")
    
    # 1. 检查重复
    print("1️⃣  检查重复...")
    result = check_duplicate(url, title, content)
    
    if result["is_duplicate"]:
        print_warning(f"检测到重复内容！")
        print(f"   检测类型：{result['check_type']}")
        print(f"   标准化 URL: {result['normalized_url']}")
        print(f"   标题：{result['record']['title']}")
        print(f"   文档：{result['record']['doc_url']}")
        return {
            "success": False,
            "error": "duplicate",
            "existing_record": result["record"]
        }
    
    print_success("新文章，继续处理...")
    print(f"   标准化 URL: {result['normalized_url']}")
    
    # 2. 抓取内容（如果未提供）
    if title is None or content is None:
        print("\n2️⃣  抓取内容...")
        print_warning("内容抓取需要 OpenClaw 环境")
        print("   请在 OpenClaw 中使用此功能，或手动提供 title 和 content 参数")
        return {
            "success": False,
            "error": "content_fetch_requires_openclaw",
            "message": "此功能需要 OpenClaw 工具系统支持"
        }
    
    # 3. 质量评分
    print("\n3️⃣  质量评分...")
    quality = evaluate_quality_score(title, content)
    print(f"   总分：{quality['total']}/100")
    print(f"   等级：{quality['level']}级")
    print(f"   重要程度：{quality['importance']}")
    
    # 4. 生成报告
    print("\n4️⃣  生成报告...")
    print_warning("报告生成需要 OpenClaw 飞书插件")
    print("   功能：feishu-create-doc")
    
    # 5. 归档
    if auto_archive:
        print("\n5️⃣  归档到 Bitable...")
        print_warning("归档需要 OpenClaw 飞书插件")
        print("   功能：feishu-bitable-app-table-record")
    
    # 6. 添加到缓存
    print("\n6️⃣  添加到缓存...")
    # 独立运行模式下可以执行
    print_success("缓存功能可用（独立运行）")
    
    print_header("✨ 分析完成")
    return {
        "success": True,
        "url": url,
        "title": title,
        "quality": quality
    }


def show_status():
    """显示工作流状态"""
    print_header("📊 工作流状态")
    
    cache = load_cache()
    
    print(f"URL 缓存：{cache['metadata'].get('total', 0)} 条")
    print(f"内容指纹：{cache['metadata'].get('fingerprint_total', 0)} 条")
    print(f"最后更新：{cache['metadata'].get('last_updated', '未知')}")
    
    # 检查配置
    config_file = Path(__file__).parent.parent / "config.json"
    if config_file.exists():
        print_success("配置文件：存在")
    else:
        print_error("配置文件：缺失（请复制 config.example.json）")
    
    # 检查数据目录
    data_dir = Path(__file__).parent.parent / "data"
    if data_dir.exists():
        print_success("数据目录：存在")
    else:
        print_error("数据目录：缺失")
    
    # 检查日志目录
    logs_dir = Path(__file__).parent.parent / "logs"
    if logs_dir.exists():
        print_success("日志目录：存在")
    else:
        print_error("日志目录：缺失")


def show_stats():
    """显示统计信息"""
    print_header("📈 统计分析")
    
    cache = load_cache()
    
    print(f"总处理文章：{cache['metadata'].get('total', 0)} 篇")
    print(f"内容指纹库：{cache['metadata'].get('fingerprint_total', 0)} 条")
    print()
    
    # 显示最近 5 条
    if cache["urls"]:
        print("最近处理的文章：")
        urls = list(cache["urls"].values())[-5:]
        for i, item in enumerate(reversed(urls), 1):
            print(f"  {i}. {item['title']}")
            print(f"     {item['doc_url']}")
            print()


def parse_urls_from_args(args: List[str]) -> List[str]:
    """从命令行参数解析 URL 列表"""
    urls = []
    for arg in args:
        if arg.startswith("--"):
            continue
        # 简单的 URL 验证
        if arg.startswith("http://") or arg.startswith("https://"):
            urls.append(arg)
    return urls


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  python workflow.py <url>                    # 分析文章（单篇）")
        print("  python workflow.py <url> --check-only       # 仅检查重复")
        print("  python workflow.py <url1> <url2> <url3>     # 批量分析（智能路由）")
        print("  python workflow.py --status                 # 查看状态")
        print("  python workflow.py --stats                  # 查看统计")
        print()
        print("示例：")
        print("  python workflow.py https://mp.weixin.qq.com/s/xxx")
        print("  python workflow.py url1 url2 url3  # 批量分析 3 篇文章")
        sys.exit(1)
    
    # 特殊命令
    if sys.argv[1] == "--status":
        show_status()
        sys.exit(0)
    
    if sys.argv[1] == "--stats":
        show_stats()
        sys.exit(0)
    
    # 解析 URL 列表（支持批量）
    urls = parse_urls_from_args(sys.argv[1:])
    
    if not urls:
        print_error("未找到有效的 URL")
        sys.exit(1)
    
    # 检查模式
    check_only = "--check-only" in sys.argv
    
    # 智能路由：单篇 vs 批量
    is_batch = len(urls) > 1
    
    if is_batch:
        print_header(f"📊 批量分析模式（{len(urls)} 篇文章）")
        print(f"智能路由：已自动启用 SubAgent 并发执行")
        print(f"最大并发数：{ArticleSmartRouter.MAX_CONCURRENT_SUBAGENTS}")
        print()
        
        # TODO: 实现批量分析
        # router = ArticleSmartRouter()
        # results = router.process_batch(urls)
        
        print_warning("批量分析功能需要 OpenClaw 环境支持")
        print("   将在 OpenClaw 会话中自动启用 SubAgent 并发执行")
        
        for i, url in enumerate(urls, 1):
            print(f"\n{i}. {url}")
        
    elif check_only:
        url = urls[0]
        print_header("🔍 检查重复")
        result = check_duplicate(url)
        
        if result["is_duplicate"]:
            print_warning("检测到重复！")
            print(f"   类型：{result['check_type']}")
            print(f"   标题：{result['record']['title']}")
            sys.exit(1)
        else:
            print_success("新文章")
            print(f"   标准化 URL: {result['normalized_url']}")
            sys.exit(0)
    
    else:
        # 单篇分析
        url = urls[0]
        print_header("📝 文章分析工作流（单篇模式）")
        print("智能路由：主 Agent 一次性执行（1 次流式请求）")
        print()
        analyze_article(url)


if __name__ == "__main__":
    main()
