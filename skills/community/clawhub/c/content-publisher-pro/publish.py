#!/usr/bin/env python3
"""
Content Publisher Pro
多平台一键发布工具 - 支持 GitHub Pages 和 Dev.to
"""

import argparse
import yaml
import os
import sys
from pathlib import Path

# 导入发布模块
from utils.github_publisher import GitHubPublisher
from utils.devto_publisher import DevToPublisher
from utils.content_processor import ContentProcessor
from utils.seo_optimizer import SEOOptimizer


def load_config(config_path):
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_article(article_path):
    """加载文章文件"""
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='内容多平台发布工具 (GitHub Pages + Dev.to)')
    parser.add_argument('-c', '--config', default='config.yaml',
                        help='配置文件路径 (默认: config.yaml)')
    parser.add_argument('-a', '--article', required=True,
                        help='文章文件路径 (必需)')
    parser.add_argument('-p', '--platforms', default='all',
                        help='发布平台: all / blog / devto (默认: all)')
    parser.add_argument('-m', '--mode', default='auto',
                        help='发布模式: full / summary / abstract / auto (默认: auto)')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='预览模式，不实际发布')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='详细输出')
    return parser.parse_args()


def main():
    args = parse_args()

    # 验证 platforms 参数
    valid_platforms = ['all', 'blog', 'devto']
    if args.platforms not in valid_platforms:
        print(f"错误: 不支持的平台 '{args.platforms}'，可选值: {', '.join(valid_platforms)}")
        sys.exit(1)

    # 验证 mode 参数
    valid_modes = ['auto', 'full', 'summary', 'abstract']
    if args.mode not in valid_modes:
        print(f"错误: 不支持的模式 '{args.mode}'，可选值: {', '.join(valid_modes)}")
        sys.exit(1)

    # 加载配置
    try:
        config = load_config(args.config)
        if args.verbose:
            print(f"[OK] 配置文件加载成功: {args.config}")
    except Exception as e:
        print(f"错误: 配置文件加载失败: {e}")
        sys.exit(1)

    # 加载文章
    try:
        article_content = load_article(args.article)
        if args.verbose:
            print(f"[OK] 文章加载成功: {args.article}")
    except Exception as e:
        print(f"错误: 文章加载失败: {e}")
        sys.exit(1)

    # 处理内容
    processor = ContentProcessor()
    article_data = processor.parse(article_content)

    # SEO 优化
    seo = SEOOptimizer()
    article_data = seo.optimize(article_data)

    # 根据模式处理内容
    if args.mode == 'summary':
        article_data = processor.generate_summary(article_data)
    elif args.mode == 'abstract':
        article_data = processor.generate_abstract(article_data)
    # mode == 'auto' 或 'full' 时使用原始内容

    # 发布到各平台
    results = []

    if args.platforms in ['all', 'blog']:
        try:
            github = GitHubPublisher(config['github'])
            if args.dry_run:
                print("[DRY RUN] 将发布到 GitHub Pages 博客")
            else:
                # 发布前去重检查
                if github.check_duplicate(article_data['title']):
                    print("[WARN] GitHub 上已存在相同标题的文章，将更新已有文章")

                url = github.publish(article_data, mode='full')
                results.append(('GitHub Pages', url))
                print(f"[OK] GitHub Pages: {url}")
        except Exception as e:
            print(f"[FAIL] GitHub Pages 发布失败: {e}")

    if args.platforms in ['all', 'devto']:
        try:
            devto = DevToPublisher(config['devto'])
            if args.dry_run:
                print("[DRY RUN] 将发布到 Dev.to")
            else:
                url = devto.publish(article_data, mode='summary')
                results.append(('Dev.to', url))
                print(f"[OK] Dev.to: {url}")
        except Exception as e:
            print(f"[FAIL] Dev.to 发布失败: {e}")

    # 输出汇总
    print("\n" + "=" * 50)
    print("发布完成汇总")
    print("=" * 50)
    if results:
        for platform, url in results:
            print(f"[OK] {platform}: {url}")
    else:
        print("没有文章被发布")

    if args.dry_run:
        print("\n[DRY RUN] 预览模式，未实际发布")


if __name__ == '__main__':
    main()
