#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译模块 - 预留接口
功能：将英文AI资讯翻译成中文
"""

import sys
import io
import json
import os

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "user_config")
CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "translator_config.json")
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "translator_config.json.default")


def load_translator_config():
    """加载翻译配置（优先用户配置）"""
    # 优先读取用户配置目录
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 读取用户配置失败: {e}")
    
    # 读取默认配置
    if os.path.exists(DEFAULT_CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                print("[INFO] 使用默认翻译配置，请复制到 user_config 目录进行自定义")
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] 无法加载默认配置: {e}")
            return None
    
    return {"config": {"enabled": False}}


def translate_text(text, target_lang='zh', config=None):
    """
    翻译文本
    注意：需要配置API才能使用
    """
    if config is None:
        config = load_translator_config()
    
    cfg = config.get('config', {})
    
    if not cfg.get('enabled', False):
        return text  # 返回原文
    
    # TODO: 实现具体翻译逻辑
    # 可以接入百度翻译API、Google Translate API等
    return text


def translate_articles(articles, target_lang='zh'):
    """翻译文章列表"""
    config = load_translator_config()
    
    if not config.get('config', {}).get('enabled', False):
        print("  ℹ️ 翻译未启用，跳过")
        return articles
    
    print(f"  🌐 翻译文章到中文...")
    
    for article in articles:
        # 翻译标题和摘要
        if article.get('title'):
            article['title_zh'] = translate_text(article['title'], target_lang, config)
        if article.get('summary'):
            article['summary_zh'] = translate_text(article['summary'][:500], target_lang, config)
    
    print(f"  ✅ 完成 {len(articles)} 篇文章的翻译")
    
    return articles


def test_translator():
    """测试翻译配置"""
    config = load_translator_config()
    
    print("=" * 50)
    print("翻译配置检查")
    print("=" * 50)
    print(f"启用状态: {'✅ 已启用' if config.get('config', {}).get('enabled') else '❌ 未启用'}")
    print(f"服务商: {config.get('config', {}).get('provider', '未选择')}")
    print("=" * 50)
    
    if not config.get('config', {}).get('enabled'):
        print("\n请编辑 translator_config.json 设置 enabled: true")


if __name__ == "__main__":
    test_translator()