#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
beautify.py v3.3.0 - 智能 UI 美化脚本
功能：
1. 智能检测项目类型（静态 HTML / Vite / Next.js / Nuxt.js / Remix / SvelteKit）
2. 自动推荐最适合的风格
3. 智能注入样式（支持多种注入策略）
4. 生成实时预览页（对比前后效果）
5. 30 种风格库（教育/创意/工具/商务/社交/电商/中国厂商）
6. Design Tokens 导出功能
7. 组件代码片段生成
8. A/B 风格对比
"""

import os
import sys
import json
import re
import shutil
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Windows 编码设置
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ========== 扩展风格库（30 种）==========
DESIGN_TEMPLATES = {
    # 教育/文档类
    "notion": {
        "name": "Notion",
        "description": "温暖简约，适合文学、教育类",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F7F7F5", "text": "#37352F", "textSecondary": "#9B9A97", "link": "#0066E0", "border": "#E1E1E0", "primary": "#0066E0", "hover": "#EFEFED"},
        "typography": {"heading": "Georgia, serif", "body": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", "code": "'SFMono-Regular', 'Consolas', monospace"},
        "radius": "4px", "shadow": "0 1px 3px rgba(0,0,0,0.08)",
        "suitable_for": ["教育", "文学", "阅读", "文档"], "category": "教育文档"
    },
    "figma": {
        "name": "Figma",
        "description": "活泼多彩，适合互动学习",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F5", "text": "#1E1E1E", "textSecondary": "#737373", "link": "#0C8CE9", "border": "#E5E5E5", "primary": "#0C8CE9", "secondary": "#FF725C", "accent": "#7ED321"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "'JetBrains Mono', monospace"},
        "radius": "8px", "shadow": "0 4px 12px rgba(0,0,0,0.1)",
        "suitable_for": ["互动", "创意", "年轻", "设计"], "category": "创意设计"
    },
    "linear": {
        "name": "Linear",
        "description": "极简精准，适合工具类",
        "colors": {"background": "#0D0D0D", "backgroundSecondary": "#1A1A1A", "text": "#E0E0E0", "textSecondary": "#8A8A8A", "link": "#5E6AD2", "border": "#2A2A2A", "primary": "#5E6AD2"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "'JetBrains Mono', monospace"},
        "radius": "6px", "shadow": "0 2px 8px rgba(0,0,0,0.2)",
        "suitable_for": ["工具", "逻辑", "效率", "数据"], "category": "工具效率"
    },
    "vercel": {
        "name": "Vercel",
        "description": "黑白科技感",
        "colors": {"background": "#000000", "backgroundSecondary": "#111111", "text": "#FFFFFF", "textSecondary": "#888888", "link": "#0070F3", "border": "#333333"},
        "typography": {"heading": "'Geist Sans', sans-serif", "body": "'Geist Sans', sans-serif", "code": "'Geist Mono', monospace"},
        "radius": "5px", "shadow": "0 4px 14px rgba(0,0,0,0.3)",
        "suitable_for": ["技术", "开发者", "文档", "API"], "category": "技术文档"
    },
    "stripe": {
        "name": "Stripe",
        "description": "专业优雅",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F6F9FC", "text": "#1A1F36", "textSecondary": "#697386", "link": "#635BFF", "border": "#E3E8EE", "primary": "#635BFF"},
        "typography": {"heading": "'Söhne', sans-serif", "body": "'Söhne', sans-serif", "code": "'Söhne Mono', monospace"},
        "radius": "8px", "shadow": "0 13px 27px -5px rgba(50,50,93,0.25)",
        "suitable_for": ["商务", "金融", "企业", "专业"], "category": "商务金融"
    },
    # 新增风格
    "claude": {
        "name": "Claude",
        "description": "温暖陶土色，简洁编辑风格",
        "colors": {"background": "#FAFAF9", "backgroundSecondary": "#F5F5F4", "text": "#1C1917", "textSecondary": "#78716C", "link": "#B91C1C", "border": "#E7E5E4", "primary": "#B91C1C"},
        "typography": {"heading": "Georgia, serif", "body": "system-ui, sans-serif", "code": "monospace"},
        "radius": "6px", "shadow": "0 1px 2px rgba(0,0,0,0.05)",
        "suitable_for": ["阅读", "写作", "博客"], "category": "教育文档"
    },
    "elevenlabs": {
        "name": "ElevenLabs",
        "description": "暗黑电影感，音频波形美学",
        "colors": {"background": "#0A0A0A", "backgroundSecondary": "#1A1A1A", "text": "#FFFFFF", "textSecondary": "#A0A0A0", "link": "#FF4D00", "border": "#333333", "primary": "#FF4D00"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "monospace"},
        "radius": "12px", "shadow": "0 4px 20px rgba(0,0,0,0.4)",
        "suitable_for": ["音频", "媒体", "创意"], "category": "创意设计"
    },
    "ollama": {
        "name": "Ollama",
        "description": "终端优先，单色简约",
        "colors": {"background": "#000000", "backgroundSecondary": "#111111", "text": "#FFFFFF", "textSecondary": "#666666", "link": "#00FF00", "border": "#333333", "primary": "#00FF00"},
        "typography": {"heading": "monospace", "body": "system-ui", "code": "monospace"},
        "radius": "0px", "shadow": "none",
        "suitable_for": ["开发者", "极客", "终端"], "category": "技术文档"
    },
    "cursor": {
        "name": "Cursor",
        "description": "流畅暗黑，渐变点缀",
        "colors": {"background": "#1E1E1E", "backgroundSecondary": "#2A2A2A", "text": "#FFFFFF", "textSecondary": "#A0A0A0", "link": "#007ACC", "border": "#404040", "primary": "#007ACC"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "'JetBrains Mono'"},
        "radius": "8px", "shadow": "0 4px 12px rgba(0,0,0,0.3)",
        "suitable_for": ["编辑器", "IDE", "开发"], "category": "技术文档"
    },
    "raycast": {
        "name": "Raycast",
        "description": "流畅暗铬，渐变强调",
        "colors": {"background": "#0D0D0D", "backgroundSecondary": "#1A1A1A", "text": "#FFFFFF", "textSecondary": "#888888", "link": "#FF6363", "border": "#2A2A2A", "primary": "#FF6363"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "monospace"},
        "radius": "8px", "shadow": "0 4px 16px rgba(0,0,0,0.4)",
        "suitable_for": ["工具", "效率", "启动器"], "category": "工具效率"
    },
    "superhuman": {
        "name": "Superhuman",
        "description": "高级暗黑，键盘优先",
        "colors": {"background": "#1A1A1A", "backgroundSecondary": "#262626", "text": "#FFFFFF", "textSecondary": "#A0A0A0", "link": "#7C3AED", "border": "#404040", "primary": "#7C3AED"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "monospace"},
        "radius": "6px", "shadow": "0 2px 8px rgba(0,0,0,0.3)",
        "suitable_for": ["邮件", "效率", "专业"], "category": "工具效率"
    },
    "airbnb": {
        "name": "Airbnb",
        "description": "温暖珊瑚色，摄影驱动",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F7F7F7", "text": "#222222", "textSecondary": "#717171", "link": "#FF5A5F", "border": "#DDDDDD", "primary": "#FF5A5F"},
        "typography": {"heading": "'Circular', sans-serif", "body": "'Circular', sans-serif", "code": "monospace"},
        "radius": "12px", "shadow": "0 4px 12px rgba(0,0,0,0.08)",
        "suitable_for": ["旅行", "摄影", "生活"], "category": "电商生活"
    },
    "spotify": {
        "name": "Spotify",
        "description": "鲜艳绿黑，专辑封面驱动",
        "colors": {"background": "#121212", "backgroundSecondary": "#181818", "text": "#FFFFFF", "textSecondary": "#B3B3B3", "link": "#1DB954", "border": "#282828", "primary": "#1DB954"},
        "typography": {"heading": "'Circular', sans-serif", "body": "'Circular', sans-serif", "code": "monospace"},
        "radius": "8px", "shadow": "0 4px 12px rgba(0,0,0,0.4)",
        "suitable_for": ["音乐", "媒体", "娱乐"], "category": "创意设计"
    },
    "tesla": {
        "name": "Tesla",
        "description": "激进减法，全屏摄影",
        "colors": {"background": "#000000", "backgroundSecondary": "#111111", "text": "#FFFFFF", "textSecondary": "#A0A0A0", "link": "#E31937", "border": "#333333", "primary": "#E31937", "secondary": "#FFFFFF", "accent": "#E31937"},
        "typography": {"heading": "'Gotham', sans-serif", "body": "'Gotham', sans-serif", "code": "monospace"},
        "radius": "0px", "shadow": "none",
        "suitable_for": ["汽车", "科技", "未来"], "category": "商务金融"
    },
    "apple": {
        "name": "Apple",
        "description": "高级留白，电影感",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F7", "text": "#1D1D1F", "textSecondary": "#86868B", "link": "#0066CC", "border": "#D2D2D7", "primary": "#0066CC"},
        "typography": {"heading": "'SF Pro Display', sans-serif", "body": "'SF Pro Text', sans-serif", "code": "'SF Mono', monospace"},
        "radius": "12px", "shadow": "0 4px 16px rgba(0,0,0,0.08)",
        "suitable_for": ["高端", "零售", "科技"], "category": "商务金融"
    },
    "github": {
        "name": "GitHub",
        "description": "开发者友好，清晰高效",
        "colors": {"background": "#0D1117", "backgroundSecondary": "#161B22", "text": "#E6EDF3", "textSecondary": "#8B949E", "link": "#58A6FF", "border": "#30363D", "primary": "#238636", "secondary": "#8957E5", "accent": "#F78166"},
        "typography": {"heading": "-apple-system, BlinkMacSystemFont, sans-serif", "body": "-apple-system, BlinkMacSystemFont, sans-serif", "code": "'SF Mono', Consolas, monospace"},
        "radius": "6px", "shadow": "0 4px 12px rgba(0,0,0,0.3)",
        "suitable_for": ["开发者", "代码", "开源"], "category": "技术文档"
    },
    "discord": {
        "name": "Discord",
        "description": "社交娱乐，活力社区",
        "colors": {"background": "#36393F", "backgroundSecondary": "#2F3136", "text": "#FFFFFF", "textSecondary": "#B9BBBE", "link": "#5865F2", "border": "#404040", "primary": "#5865F2", "secondary": "#57F287", "accent": "#FEE75C"},
        "typography": {"heading": "gg sans, sans-serif", "body": "gg sans, sans-serif", "code": "Consolas, monospace"},
        "radius": "4px", "shadow": "0 2px 8px rgba(0,0,0,0.2)",
        "suitable_for": ["社区", "社交", "聊天"], "category": "社交娱乐"
    },
    "slack": {
        "name": "Slack",
        "description": "协作办公，色彩丰富",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F4F4F4", "text": "#1D1C1D", "textSecondary": "#616061", "link": "#4A154B", "border": "#E1E1E1", "primary": "#4A154B", "secondary": "#36C5F0", "accent": "#2EB67D"},
        "typography": {"heading": "Slack Sans, sans-serif", "body": "Slack Sans, sans-serif", "code": "monospace"},
        "radius": "8px", "shadow": "0 1px 3px rgba(0,0,0,0.08)",
        "suitable_for": ["办公", "团队", "协作"], "category": "商务金融"
    },
    "telegram": {
        "name": "Telegram",
        "description": "简洁快速，蓝色为主",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F5", "text": "#000000", "textSecondary": "#8E8E93", "link": "#0088CC", "border": "#E5E5E5", "primary": "#0088CC", "secondary": "#0077B5", "accent": "#25C2A0"},
        "typography": {"heading": "Roboto, sans-serif", "body": "Roboto, sans-serif", "code": "Consolas, monospace"},
        "radius": "10px", "shadow": "0 2px 8px rgba(0,0,0,0.1)",
        "suitable_for": ["通讯", "消息", "快速"], "category": "社交娱乐"
    },
    # 中国厂商风格
    "alibaba": {
        "name": "Alibaba Cloud",
        "description": "阿里云风格，橙色科技感",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F6F8FA", "text": "#1F2328", "textSecondary": "#656D76", "link": "#FF6A00", "border": "#D0D7DE", "primary": "#FF6A00", "secondary": "#0366D6", "accent": "#F78166"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "'JetBrains Mono', monospace"},
        "radius": "6px", "shadow": "0 1px 3px rgba(0,0,0,0.06)",
        "suitable_for": ["云服务", "企业", "技术"], "category": "技术文档"
    },
    "bytedance": {
        "name": "ByteDance",
        "description": "字节跳动风格，渐变活力",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F4F5F5", "text": "#1C1C1C", "textSecondary": "#666666", "link": "#FE2853", "border": "#E5E5E5", "primary": "#FE2853", "secondary": "#00F5C4", "accent": "#FFD100"},
        "typography": {"heading": "'PingFang SC', sans-serif", "body": "'PingFang SC', sans-serif", "code": "'SF Mono', monospace"},
        "radius": "8px", "shadow": "0 4px 12px rgba(0,0,0,0.08)",
        "suitable_for": ["社交", "短视频", "年轻"], "category": "创意设计"
    },
    "tencent": {
        "name": "Tencent",
        "description": "腾讯风格，蓝色社交",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F7F7F7", "text": "#1A1A1A", "textSecondary": "#999999", "link": "#07C160", "border": "#E5E5E5", "primary": "#07C160", "secondary": "#198964", "accent": "#FF6D00"},
        "typography": {"heading": "'Tencent Sans', sans-serif", "body": "'Tencent Sans', sans-serif", "code": "'SF Mono', monospace"},
        "radius": "4px", "shadow": "0 2px 8px rgba(0,0,0,0.06)",
        "suitable_for": ["社交", "即时通讯", "企业"], "category": "社交娱乐"
    },
    "antdesign": {
        "name": "Ant Design",
        "description": "企业级设计，蚂蚁金服",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#FAFAFA", "text": "#262626", "textSecondary": "#8C8C8C", "link": "#1677FF", "border": "#D9D9D9", "primary": "#1677FF", "secondary": "#52C41A", "accent": "#FAAD14"},
        "typography": {"heading": "'PingFang SC', 'Microsoft YaHei', sans-serif", "body": "'PingFang SC', 'Microsoft YaHei', sans-serif", "code": "'SFMono-Regular', Consolas, monospace"},
        "radius": "6px", "shadow": "0 2px 8px rgba(0,0,0,0.1)",
        "suitable_for": ["企业", "后台", "中台"], "category": "商务金融"
    },
    # 电商风格
    "shopify": {
        "name": "Shopify",
        "description": "简洁专业电商风，适合在线商店",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#FBF7F4", "text": "#1A1A1A", "textSecondary": "#6B7177", "link": "#008060", "border": "#E3E5E4", "primary": "#008060", "secondary": "#004C3F", "accent": "#FFB800"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "'SF Mono', monospace"},
        "radius": "8px", "shadow": "0 2px 8px rgba(0,0,0,0.08)",
        "suitable_for": ["电商", "商店", "零售"], "category": "电商生活"
    },
    "amazon": {
        "name": "Amazon",
        "description": "橙黑电商风，信任感强",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F5", "text": "#0F1111", "textSecondary": "#565959", "link": "#007185", "border": "#D5D9D9", "primary": "#FFA41C", "secondary": "#E77600", "accent": "#00A8E1"},
        "typography": {"heading": "'Amazon Ember', sans-serif", "body": "'Amazon Ember', sans-serif", "code": "monospace"},
        "radius": "4px", "shadow": "0 2px 4px rgba(0,0,0,0.1)",
        "suitable_for": ["电商", "零售", "市场"], "category": "电商生活"
    },
    "taobao": {
        "name": "Taobao",
        "description": "淘宝风格，活力橙色",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F5", "text": "#3C3C3C", "textSecondary": "#9E9E9E", "link": "#FF5000", "border": "#E8E8E8", "primary": "#FF5000", "secondary": "#FF7034", "accent": "#F5C200"},
        "typography": {"heading": "'PingFang SC', sans-serif", "body": "'PingFang SC', sans-serif", "code": "monospace"},
        "radius": "4px", "shadow": "0 2px 6px rgba(0,0,0,0.08)",
        "suitable_for": ["电商", "购物", "拍卖"], "category": "电商生活"
    },
    # 中国厂商新风格
    "huawei": {
        "name": "Huawei",
        "description": "华为企业级，红色科技感",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F5", "text": "#1F1F1F", "textSecondary": "#828282", "link": "#CF0A2C", "border": "#E0E0E0", "primary": "#CF0A2C", "secondary": "#8B0000", "accent": "#FFD700"},
        "typography": {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "code": "monospace"},
        "radius": "4px", "shadow": "0 2px 8px rgba(0,0,0,0.1)",
        "suitable_for": ["企业", "云服务", "科技"], "category": "中国厂商"
    },
    "xiaomi": {
        "name": "Xiaomi",
        "description": "小米风格，橙色活力",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F5", "text": "#1F1F1F", "textSecondary": "#8E8E8E", "link": "#FF6900", "border": "#E5E5E5", "primary": "#FF6900", "secondary": "#00F5C4", "accent": "#FFB800"},
        "typography": {"heading": "'MiSans', sans-serif", "body": "'MiSans', sans-serif", "code": "monospace"},
        "radius": "8px", "shadow": "0 4px 12px rgba(0,0,0,0.08)",
        "suitable_for": ["科技", "硬件", "智能"], "category": "中国厂商"
    },
    "jd": {
        "name": "JD",
        "description": "京东风格，红白信任",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F5", "text": "#1F1F1F", "textSecondary": "#8C8C8C", "link": "#E2231A", "border": "#E8E8E8", "primary": "#E2231A", "secondary": "#C91623", "accent": "#FFD800"},
        "typography": {"heading": "'PingFang SC', sans-serif", "body": "'PingFang SC', sans-serif", "code": "monospace"},
        "radius": "4px", "shadow": "0 2px 6px rgba(0,0,0,0.08)",
        "suitable_for": ["电商", "数码", "家电"], "category": "中国厂商"
    },
    "meituan": {
        "name": "Meituan",
        "description": "美团风格，黄色生活服务",
        "colors": {"background": "#FFFFFF", "backgroundSecondary": "#F5F5F5", "text": "#333333", "textSecondary": "#999999", "link": "#FFCC00", "border": "#E5E5E5", "primary": "#FFCC00", "secondary": "#FF6633", "accent": "#00C777"},
        "typography": {"heading": "'PingFang SC', sans-serif", "body": "'PingFang SC', sans-serif", "code": "monospace"},
        "radius": "8px", "shadow": "0 2px 8px rgba(0,0,0,0.08)",
        "suitable_for": ["生活服务", "外卖", "旅游"], "category": "中国厂商"
    },
}

DESIGN_MD_TEMPLATE = """# DESIGN.md - {name}
{description}

## 色彩系统
{colors}

## 字体规范
- 标题：{heading}
- 正文：{body}
- 代码：{code}

## 组件样式
- 圆角：{radius}
- 阴影：{shadow}
"""


def detect_project_type(project_path: str) -> Dict[str, Any]:
    """智能检测项目类型（增强版）"""
    result: Dict[str, Any] = {
        'type': 'static',
        'has_tailwind': False,
        'has_css_modules': False,
        'has_styled_components': False,
        'has_emotion': False,
        'has_scss': False,
        'has_less': False,
        'content_type': 'general',
        'html_files': [],
        'js_files': [],
        'css_files': [],
        'scss_files': [],
        'less_files': []
    }

    package_json_path = os.path.join(project_path, 'package.json')
    if os.path.exists(package_json_path):
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                deps = package_data.get('dependencies', {})
                devDeps = package_data.get('devDependencies', {})
                all_deps = {{**deps, **devDeps}}

                if 'next' in all_deps: result['type'] = 'nextjs'
                elif 'nuxt' in all_deps: result['type'] = 'nuxt'
                elif '@remix-run/react' in all_deps or 'remix' in all_deps: result['type'] = 'remix'
                elif '@sveltejs/kit' in all_deps or 'svelte' in all_deps: result['type'] = 'sveltekit'
                elif 'vite' in all_deps: result['type'] = 'vite'
                elif 'react-scripts' in all_deps: result['type'] = 'cra'

                if 'tailwindcss' in all_deps: result['has_tailwind'] = True
                if 'styled-components' in all_deps: result['has_styled_components'] = True
                if '@emotion/react' in all_deps or '@emotion/styled' in all_deps: result['has_emotion'] = True
                if 'sass' in all_deps or 'node-sass' in all_deps: result['has_scss'] = True
                if 'less' in all_deps: result['has_less'] = True

                desc = package_data.get('description', '').lower()
                if any(k in desc for k in ['教育', '学习', 'student', 'education']): result['content_type'] = 'education'
                elif any(k in desc for k in ['文档', 'doc', 'api']): result['content_type'] = 'docs'
                elif any(k in desc for k in ['电商', 'shop', 'store', '商城', '购物']): result['content_type'] = 'ecommerce'
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ 读取 package.json 失败: {{e}}")

    for root, dirs, files in os.walk(project_path):
        if 'node_modules' in root or '.git' in root: continue
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith('.html'): result['html_files'].append(full_path)
            elif file.endswith(('.js', '.jsx', '.ts', '.tsx')): result['js_files'].append(full_path)
            elif file.endswith('.scss'): result['scss_files'].append(full_path)
            elif file.endswith('.less'): result['less_files'].append(full_path)
            elif file.endswith(('.css', '.module.css')):
                result['css_files'].append(full_path)
                if file.endswith('.module.css'): result['has_css_modules'] = True

    return result


def recommend_style(project_info: Dict[str, Any]) -> Tuple[str, List[str]]:
    """推荐风格"""
    content_type = project_info.get('content_type', 'general')
    recommendations = {'education': 'notion', 'docs': 'vercel', 'ecommerce': 'stripe', 'general': 'linear'}
    style_key = recommendations.get(content_type, 'linear')
    return style_key, DESIGN_TEMPLATES[style_key]['suitable_for']


def generate_design_md(style_key: str, output_path: str) -> bool:
    """生成 DESIGN.md"""
    if style_key not in DESIGN_TEMPLATES: return False
    style_data = DESIGN_TEMPLATES[style_key]
    colors_md = "\n".join([f"- {k}: `{v}`" for k, v in style_data["colors"].items()])
    content = DESIGN_MD_TEMPLATE.format(name=style_data["name"], description=style_data["description"], colors=colors_md,
        heading=style_data["typography"]["heading"], body=style_data["typography"]["body"], 
        code=style_data["typography"]["code"], radius=style_data["radius"], shadow=style_data["shadow"])
    with open(output_path, "w", encoding="utf-8") as f: f.write(content)
    return True


def generate_tailwind_config(style_key: str, project_info: Dict[str, Any], output_path: str) -> bool:
    """生成 Tailwind 配置"""
    if style_key not in DESIGN_TEMPLATES: return False
    style_data = DESIGN_TEMPLATES[style_key]
    colors = style_data["colors"]
    
    tailwind_config = f"""/** @type {{
  config = {{
    content: [
      './index.html',
      './src/**/*.{{vue,js,ts,jsx,tsx}}',
    ],
    theme: {{
      extend: {{
        colors: {{
          primary: '{colors.get('primary', colors.get('link', '#0070F3'))}',
          secondary: '{colors.get('secondary', colors.get('backgroundSecondary', '#F5F5F5'))}',
          accent: '{colors.get('accent', colors.get('primary', '#0070F3'))}',
          background: '{colors.get('background', '#FFFFFF')}',
          foreground: '{colors.get('text', '#1E1E1E')}',
          muted: '{colors.get('textSecondary', '#737373')}',
          border: '{colors.get('border', '#E5E5E5')}',
          link: '{colors.get('link', '#0070F3')}',
        }},
        fontFamily: {{
          heading: [{_format_font_family(style_data["typography"]["heading"])}],
          body: [{_format_font_family(style_data["typography"]["body"])}],
          mono: [{_format_font_family(style_data["typography"]["code"])}],
        }},
        borderRadius: {{
          DEFAULT: '{style_data["radius"]}',
        }},
        boxShadow: {{
          DEFAULT: '{style_data["shadow"]}',
        }},
      }},
    }},
    plugins: [],
  }}
}} */
module.exports = {{
  content: ['./index.html', './src/**/*.{{vue,js,ts,jsx,tsx}}'],
  theme: {{
    extend: {{
      colors: {{
        primary: '{colors.get('primary', colors.get('link', '#0070F3'))}',
        secondary: '{colors.get('secondary', colors.get('backgroundSecondary', '#F5F5F5'))}',
        accent: '{colors.get('accent', colors.get('primary', '#0070F3'))}',
        background: '{colors.get('background', '#FFFFFF')}',
        foreground: '{colors.get('text', '#1E1E1E')}',
        muted: '{colors.get('textSecondary', '#737373')}',
        border: '{colors.get('border', '#E5E5E5')}',
        link: '{colors.get('link', '#0070F3')}',
      }},
      fontFamily: {{
        heading: [{_format_font_family(style_data["typography"]["heading"])}],
        body: [{_format_font_family(style_data["typography"]["body"])}],
        mono: [{_format_font_family(style_data["typography"]["code"])}],
      }},
      borderRadius: {{
        DEFAULT: '{style_data["radius"]}',
      }},
      boxShadow: {{
        DEFAULT: '{style_data["shadow"]}',
      }},
    }},
  }},
  plugins: [],
}}
"""
    with open(output_path, "w", encoding="utf-8") as f: f.write(tailwind_config)
    return True


def _format_font_family(font_family_str):
    """格式化字体家族字符串为 Tailwind 格式"""
    fonts = []
    for f in font_family_str.split(','):
        cleaned = f.strip().strip("'\"`")
        fonts.append(f"'{cleaned}'")
    return ', '.join(fonts)


def generate_css_content(style_key: str, project_info: Dict[str, Any]) -> str:
    """生成智能 CSS"""
    if style_key not in DESIGN_TEMPLATES: return ""
    style_data = DESIGN_TEMPLATES[style_key]
    colors = style_data["colors"]
    typo = style_data["typography"]
    
    css = f"""/* {style_data['name']} 风格 - 智能生成 */
:root {{
  --bg-primary: {colors.get('background', '#FFFFFF')};
  --bg-secondary: {colors.get('backgroundSecondary', '#F5F5F5')};
  --text-primary: {colors.get('text', '#1E1E1E')};
  --text-secondary: {colors.get('textSecondary', '#737373')};
  --link-color: {colors.get('link', '#0070F3')};
  --border-color: {colors.get('border', '#E5E5E5')};
  --primary: {colors.get('primary', colors.get('link', '#0070F3'))};
  --radius: {style_data['radius']};
  --shadow: {style_data['shadow']};
}}

body {{ background-color: var(--bg-primary) !important; color: var(--text-primary) !important; font-family: var(--font-body) !important; }}
h1, h2, h3, h4, h5, h6 {{ font-family: var(--font-heading) !important; color: var(--text-primary) !important; }}
a {{ color: var(--link-color) !important; }}
button, .btn {{ border-radius: var(--radius) !important; background: var(--primary) !important; color: #fff !important; }}
.card {{ background: var(--bg-secondary) !important; border: 1px solid var(--border-color) !important; border-radius: var(--radius) !important; }}
"""
    return css


def generate_preview_html(project_path: str, style_key: str, project_info: Dict[str, Any]) -> Optional[str]:
    """生成实时预览页（增强版）"""
    if style_key not in DESIGN_TEMPLATES: return None

    style_data = DESIGN_TEMPLATES[style_key]
    colors = style_data["colors"]
    primary_color = colors.get('primary', colors.get('link', '#0070F3'))

    preview_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{style_data['name']} - 实时预览 v3.3.0</title>
    <style>
        :root {{
            --bg-primary: {colors.get('background', '#FFFFFF')};
            --bg-secondary: {colors.get('backgroundSecondary', '#F5F5F5')};
            --text-primary: {colors.get('text', '#1E1E1E')};
            --text-secondary: {colors.get('textSecondary', '#737373')};
            --link-color: {colors.get('link', '#0070F3')};
            --border-color: {colors.get('border', '#E5E5E5')};
            --primary: {primary_color};
            --secondary: {colors.get('secondary', colors.get('backgroundSecondary', '#F5F5F5'))};
            --accent: {colors.get('accent', colors.get('primary', '#0070F3'))};
            --radius: {style_data['radius']};
            --shadow: {style_data['shadow']};
        }}
        [data-theme="dark"] {{
            --bg-primary: #1a1a1a;
            --bg-secondary: #262626;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --border-color: #404040;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            padding: 40px;
            margin: 0;
            transition: all 0.3s ease;
        }}
        .preview-container {{ max-width: 1200px; margin: 0 auto; }}
        .toolbar {{
            position: fixed;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
            z-index: 1000;
        }}
        .theme-toggle, .responsive-toggle {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 10px 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s ease;
        }}
        .theme-toggle:hover, .responsive-toggle:hover {{ background: var(--primary); color: #fff; }}
        .style-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 30px;
            margin: 20px 0;
            box-shadow: var(--shadow);
        }}
        .section-title {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
        }}
        .color-swatches {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .color-swatch {{
            width: 80px;
            height: 80px;
            border-radius: var(--radius);
            border: 1px solid rgba(0,0,0,0.1);
            display: flex;
            align-items: flex-end;
            justify-content: center;
            padding-bottom: 8px;
            font-size: 11px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
            color: #fff;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .color-swatch:hover {{ transform: scale(1.05); }}
        .color-swatch.light-text {{ color: #333; text-shadow: 0 1px 2px rgba(255,255,255,0.8); }}
        .btn {{
            background: var(--primary);
            color: #fff;
            border: none;
            border-radius: var(--radius);
            padding: 12px 24px;
            font-size: 16px;
            cursor: pointer;
            margin: 8px 4px;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }}
        .btn-secondary {{ background: transparent; color: var(--text-primary); border: 1px solid var(--border-color); }}
        .btn-accent {{ background: var(--accent); }}
        .btn-group {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-top: 20px; }}
        .card {{ background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius); padding: 24px; transition: all 0.2s ease; }}
        .card:hover {{ transform: translateY(-4px); box-shadow: var(--shadow); }}
        .card h3 {{ margin: 0 0 12px 0; font-size: 18px; }}
        .card p {{ margin: 0; color: var(--text-secondary); font-size: 14px; line-height: 1.6; }}
        .input-demo {{ display: flex; flex-direction: column; gap: 16px; max-width: 400px; }}
        .input-field {{ padding: 12px 16px; border: 1px solid var(--border-color); border-radius: var(--radius); background: var(--bg-primary); color: var(--text-primary); font-size: 14px; transition: all 0.2s ease; }}
        .input-field:focus {{ outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px {primary_color}22; }}
        .input-field::placeholder {{ color: var(--text-secondary); }}
        .nav-demo {{ display: flex; align-items: center; gap: 24px; padding: 16px 24px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius); }}
        .nav-logo {{ font-weight: 700; font-size: 18px; color: var(--primary); }}
        .nav-links {{ display: flex; gap: 20px; margin-left: auto; }}
        .nav-link {{ color: var(--text-secondary); text-decoration: none; font-size: 14px; transition: color 0.2s; }}
        .nav-link:hover {{ color: var(--primary); }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; background: var(--primary); color: #fff; }}
        .badge-secondary {{ background: var(--secondary); color: var(--text-primary); }}
        .badge-outline {{ background: transparent; border: 1px solid var(--border-color); color: var(--text-secondary); }}
        .tags {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .tag {{ padding: 6px 14px; background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: var(--radius); font-size: 13px; color: var(--text-secondary); }}
        .comparison {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 40px 0; }}
        .comparison-item {{ padding: 20px; border-radius: var(--radius); }}
        .original {{ background: #f5f5f5; color: #333; }}
        .preview-demo {{ background: var(--bg-secondary); color: var(--text-primary); }}
        h1 {{ font-family: Georgia, serif; font-size: 36px; margin-bottom: 10px; }}
        h2 {{ font-size: 20px; margin: 0 0 16px 0; }}

        /* Table Styles */
        .table-demo {{ width: 100%; border-collapse: collapse; }}
        .table-demo th, .table-demo td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border-color); }}
        .table-demo th {{ font-weight: 600; background: var(--bg-secondary); }}
        .table-demo tr:hover {{ background: var(--bg-secondary); }}

        /* Tabs Styles */
        .tabs {{ border-bottom: 1px solid var(--border-color); margin-bottom: 20px; }}
        .tab-list {{ display: flex; gap: 20px; }}
        .tab {{ padding: 12px 0; border: none; background: none; color: var(--text-secondary); font-size: 14px; cursor: pointer; border-bottom: 2px solid transparent; transition: all 0.2s; }}
        .tab:hover {{ color: var(--text-primary); }}
        .tab.active {{ color: var(--primary); border-bottom-color: var(--primary); }}
        .tab-content {{ padding: 20px 0; }}

        /* Progress Styles */
        .progress-demo {{ display: flex; flex-direction: column; gap: 16px; max-width: 400px; }}
        .progress-item {{ }}
        .progress-label {{ display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; }}
        .progress-bar {{ height: 8px; background: var(--bg-primary); border-radius: 4px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: var(--primary); border-radius: 4px; transition: width 0.3s ease; }}
        .progress-fill.striped {{ background: repeating-linear-gradient(45deg, var(--primary), var(--primary) 10px, var(--accent) 10px, var(--accent) 20px); }}

        /* Date Picker Styles */
        .date-demo {{ display: flex; gap: 16px; flex-wrap: wrap; }}
        .date-input {{ padding: 12px 16px; border: 1px solid var(--border-color); border-radius: var(--radius); background: var(--bg-primary); color: var(--text-primary); font-size: 14px; }}

        /* Color Picker Styles */
        .color-picker-demo {{ display: flex; flex-direction: column; gap: 16px; max-width: 300px; }}
        .color-picker-row {{ display: flex; align-items: center; gap: 12px; }}
        .color-picker-row label {{ width: 80px; font-size: 14px; }}
        .color-picker-row input[type="color"] {{ width: 50px; height: 36px; border: 1px solid var(--border-color); border-radius: var(--radius); cursor: pointer; }}
        .color-picker-row input[type="text"] {{ flex: 1; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: var(--radius); background: var(--bg-primary); color: var(--text-primary); font-size: 14px; font-family: monospace; }}

        /* Responsive Preview */
        .responsive-frame {{ border: 2px solid var(--border-color); border-radius: var(--radius); overflow: hidden; margin: 20px 0; }}
        .responsive-viewport {{ transition: all 0.3s ease; }}
        .responsive-viewport.mobile {{ max-width: 375px; margin: 0 auto; }}
        .responsive-viewport.tablet {{ max-width: 768px; margin: 0 auto; }}
        .responsive-viewport.desktop {{ max-width: 100%; }}
        .responsive-label {{ font-size: 12px; color: var(--text-secondary); margin-bottom: 8px; }}
    </style>
</head>
<body>
    <div class="toolbar">
        <button class="theme-toggle" onclick="toggleTheme()">切换暗色模式</button>
        <button class="responsive-toggle" onclick="cycleResponsive()">桌面端</button>
    </div>
    <div class="responsive-viewport desktop" id="responsiveViewport">
    <div class="preview-container">
        <h1>{style_data['name']} - 实时预览 v3.3.0</h1>
        <p style="color: var(--text-secondary); font-size: 16px;">{style_data['description']}</p>

        <div class="style-card">
            <h2 class="section-title">交互式色彩系统</h2>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">点击颜色块或修改下方颜色值实时预览效果</p>
            <div class="color-picker-demo">
                <div class="color-picker-row">
                    <label>Primary</label>
                    <input type="color" id="primaryPicker" value="{primary_color}" onchange="updateColor('primary', this.value)">
                    <input type="text" id="primaryText" value="{primary_color}" onchange="updateColorFromText('primary', this.value)">
                </div>
                <div class="color-picker-row">
                    <label>Accent</label>
                    <input type="color" id="accentPicker" value="{colors.get('accent', primary_color)}" onchange="updateColor('accent', this.value)">
                    <input type="text" id="accentText" value="{colors.get('accent', primary_color)}" onchange="updateColorFromText('accent', this.value)">
                </div>
                <div class="color-picker-row">
                    <label>Link</label>
                    <input type="color" id="linkPicker" value="{colors.get('link', '#0070F3')}" onchange="updateColor('link', this.value)">
                    <input type="text" id="linkText" value="{colors.get('link', '#0070F3')}" onchange="updateColorFromText('link', this.value)">
                </div>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">色彩系统</h2>
            <div class="color-swatches">
                <div class="color-swatch light-text" style="background: {colors.get('background', '#FFFFFF')};">Background</div>
                <div class="color-swatch" style="background: {colors.get('backgroundSecondary', '#F5F5F5')};">Secondary</div>
                <div class="color-swatch light-text" style="background: {colors.get('text', '#1E1E1E')};">Text</div>
                <div class="color-swatch light-text" style="background: {colors.get('textSecondary', '#737373')};">Muted</div>
                <div class="color-swatch" style="background: var(--primary);" onclick="updatePrimaryFromSwatch(this)">Primary</div>
                <div class="color-swatch" style="background: var(--link-color);" onclick="updatePrimaryFromSwatch(this)">Link</div>
                <div class="color-swatch" style="background: var(--accent);" onclick="updatePrimaryFromSwatch(this)">Accent</div>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">响应式断点预览</h2>
            <div class="responsive-label">当前视图：<span id="responsiveLabel">桌面端</span></div>
            <div style="background: var(--bg-secondary); padding: 20px; border-radius: var(--radius);">
                <p>在工具栏点击"响应式切换"按钮查看不同设备尺寸下的效果。</p>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">按钮组件</h2>
            <div class="btn-group">
                <button class="btn">主要按钮</button>
                <button class="btn btn-secondary">次要按钮</button>
                <button class="btn btn-accent">强调按钮</button>
            </div>
            <h2 class="section-title" style="margin-top: 30px;">按钮尺寸</h2>
            <div class="btn-group">
                <button class="btn" style="padding: 8px 16px; font-size: 14px;">小按钮</button>
                <button class="btn">中按钮</button>
                <button class="btn" style="padding: 16px 32px; font-size: 18px;">大按钮</button>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">导航栏</h2>
            <div class="nav-demo">
                <div class="nav-logo">{style_data['name']}</div>
                <div class="nav-links">
                    <a href="#" class="nav-link">产品</a>
                    <a href="#" class="nav-link">解决方案</a>
                    <a href="#" class="nav-link" style="color: var(--primary);">定价</a>
                    <a href="#" class="nav-link">文档</a>
                </div>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">卡片组件</h2>
            <div class="card-grid">
                <div class="card">
                    <span class="badge">新功能</span>
                    <h3 style="margin-top: 12px;">卡片标题</h3>
                    <p>这是卡片的描述文本，展示了内容的呈现效果。</p>
                </div>
                <div class="card">
                    <span class="badge badge-secondary">推荐</span>
                    <h3 style="margin-top: 12px;">另一个卡片</h3>
                    <p>第二个卡片的描述内容，用于展示不同的信息。</p>
                </div>
                <div class="card">
                    <span class="badge badge-outline">标签</span>
                    <h3 style="margin-top: 12px;">第三个卡片</h3>
                    <p>第三个卡片展示了不同样式徽章的组合使用效果。</p>
                </div>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">表单组件</h2>
            <div class="input-demo">
                <input type="text" class="input-field" placeholder="请输入用户名">
                <input type="email" class="input-field" placeholder="请输入邮箱地址">
                <input type="password" class="input-field" placeholder="请输入密码">
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">表格组件</h2>
            <table class="table-demo">
                <thead>
                    <tr>
                        <th>产品名称</th>
                        <th>分类</th>
                        <th>价格</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>化学试剂 A</td>
                        <td>工业原料</td>
                        <td>¥299.00</td>
                        <td><span class="badge">在售</span></td>
                    </tr>
                    <tr>
                        <td>化学试剂 B</td>
                        <td>实验室用品</td>
                        <td>¥599.00</td>
                        <td><span class="badge badge-secondary">待货</span></td>
                    </tr>
                    <tr>
                        <td>化学试剂 C</td>
                        <td>工业原料</td>
                        <td>¥899.00</td>
                        <td><span class="badge">在售</span></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="style-card">
            <h2 class="section-title">标签页组件</h2>
            <div class="tabs">
                <div class="tab-list">
                    <button class="tab active" onclick="switchTab(this)">产品介绍</button>
                    <button class="tab" onclick="switchTab(this)">规格参数</button>
                    <button class="tab" onclick="switchTab(this)">用户评价</button>
                </div>
            </div>
            <div class="tab-content">
                <p>这是产品介绍的内容。展示了标签页切换的基本效果。</p>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">进度条组件</h2>
            <div class="progress-demo">
                <div class="progress-item">
                    <div class="progress-label">
                        <span>项目进度</span>
                        <span>75%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 75%;"></div>
                    </div>
                </div>
                <div class="progress-item">
                    <div class="progress-label">
                        <span>销售额</span>
                        <span>90%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill striped" style="width: 90%;"></div>
                    </div>
                </div>
                <div class="progress-item">
                    <div class="progress-label">
                        <span>完成率</span>
                        <span>45%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 45%; background: var(--accent);"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">日期选择器</h2>
            <div class="date-demo">
                <input type="date" class="date-input">
                <input type="time" class="date-input">
                <input type="datetime-local" class="date-input">
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">标签与徽章</h2>
            <div class="tags" style="margin-bottom: 20px;">
                <span class="tag">技术</span>
                <span class="tag">产品</span>
                <span class="tag">设计</span>
                <span class="tag">运营</span>
            </div>
            <div class="tags">
                <span class="badge">主要</span>
                <span class="badge badge-secondary">次要</span>
                <span class="badge badge-outline">轮廓</span>
            </div>
        </div>

        <div class="comparison">
            <div class="comparison-item original">
                <h3>原始效果</h3>
                <p>这是原始样式，未经任何美化处理。</p>
            </div>
            <div class="comparison-item preview-demo">
                <h3>{style_data['name']} 效果</h3>
                <p>应用 {style_data['name']} 风格后的效果展示。</p>
            </div>
        </div>

        <div class="style-card">
            <h2 class="section-title">适合场景</h2>
            <p>{', '.join(style_data['suitable_for'])}</p>
            <p style="margin-top: 16px; color: var(--text-secondary);">分类：{style_data['category']}</p>
        </div>
    </div>
    </div>
    <script>
        function toggleTheme() {{
            const body = document.body;
            const btn = document.querySelector('.theme-toggle');
            if (body.getAttribute('data-theme') === 'dark') {{
                body.removeAttribute('data-theme');
                btn.textContent = '切换暗色模式';
            }} else {{
                body.setAttribute('data-theme', 'dark');
                btn.textContent = '切换亮色模式';
            }}
        }}

        let responsiveModes = ['desktop', 'tablet', 'mobile'];
        let currentResponsiveIndex = 0;

        function cycleResponsive() {{
            currentResponsiveIndex = (currentResponsiveIndex + 1) % responsiveModes.length;
            const mode = responsiveModes[currentResponsiveIndex];
            const viewport = document.getElementById('responsiveViewport');
            const btn = document.querySelector('.responsive-toggle');
            const label = document.getElementById('responsiveLabel');

            viewport.className = 'responsive-viewport ' + mode;
            btn.textContent = mode === 'desktop' ? '桌面端' : mode === 'tablet' ? '平板端' : '移动端';
            label.textContent = btn.textContent;
        }}

        function updateColor(colorVar, value) {{
            document.documentElement.style.setProperty('--' + colorVar, value);
            document.getElementById(colorVar + 'Text').value = value;
        }}

        function updateColorFromText(colorVar, value) {{
            if (/^#[0-9A-Fa-f]{{6}}$/.test(value)) {{
                document.documentElement.style.setProperty('--' + colorVar, value);
                document.getElementById(colorVar + 'Picker').value = value;
            }}
        }}

        function updatePrimaryFromSwatch(el) {{
            const bgColor = el.style.backgroundColor;
            const rgb = bgColor.match(/\\d+/g);
            if (rgb) {{
                const hex = '#' + rgb.slice(0, 3).map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
                updateColor('primary', hex);
            }}
        }}

        function switchTab(btn) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            btn.classList.add('active');
        }}
    </script>
</body>
</html>"""

    preview_path = os.path.join(project_path, f"preview-{style_key}.html")
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(preview_content)

    return preview_path


def generate_design_tokens_json(style_key: str, project_info: Dict[str, Any], output_path: str) -> bool:
    """生成 Design Tokens JSON"""
    if style_key not in DESIGN_TEMPLATES: return False
    style_data = DESIGN_TEMPLATES[style_key]
    colors = style_data["colors"]

    tokens = {
        "name": style_data["name"],
        "description": style_data["description"],
        "category": style_data["category"],
        "colors": {
            "background": {"primary": colors.get("background", "#FFFFFF"), "secondary": colors.get("backgroundSecondary", "#F5F5F5")},
            "text": {"primary": colors.get("text", "#1E1E1E"), "secondary": colors.get("textSecondary", "#737373")},
            "brand": {"primary": colors.get("primary", colors.get("link", "#0070F3")), "secondary": colors.get("secondary", ""), "accent": colors.get("accent", "")},
            "border": colors.get("border", "#E5E5E5"),
            "link": colors.get("link", "#0070F3")
        },
        "typography": style_data["typography"],
        "spacing": {"radius": style_data["radius"], "shadow": style_data["shadow"]},
        "suitable_for": style_data["suitable_for"]
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
    return True


def generate_design_tokens_js(style_key: str, project_info: Dict[str, Any], output_path: str) -> bool:
    """生成 Design Tokens JS"""
    if style_key not in DESIGN_TEMPLATES: return False
    style_data = DESIGN_TEMPLATES[style_key]
    colors = style_data["colors"]

    js_content = f"""// Design Tokens - {style_data['name']}
// Generated by beautify-ui v3.3.0
export const tokens = {{
  name: '{style_data["name"]}',
  description: '{style_data["description"]}',
  colors: {{
    background: {{
      primary: '{colors.get("background", "#FFFFFF")}',
      secondary: '{colors.get("backgroundSecondary", "#F5F5F5")}'
    }},
    text: {{
      primary: '{colors.get("text", "#1E1E1E")}',
      secondary: '{colors.get("textSecondary", "#737373")}'
    }},
    brand: {{
      primary: '{colors.get("primary", colors.get("link", "#0070F3"))}',
      secondary: '{colors.get("secondary", "")}',
      accent: '{colors.get("accent", "")}'
    }},
    border: '{colors.get("border", "#E5E5E5")}',
    link: '{colors.get("link", "#0070F3")}'
  }},
  typography: {{
    heading: '{style_data["typography"]["heading"]}',
    body: '{style_data["typography"]["body"]}',
    code: '{style_data["typography"]["code"]}'
  }},
  spacing: {{
    radius: '{style_data["radius"]}',
    shadow: '{style_data["shadow"]}'
  }},
  suitableFor: {style_data["suitable_for"]}
}};

export default tokens;
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    return True


def generate_component_snippets(style_key: str, project_info: Dict[str, Any], output_dir: str) -> bool:
    """生成组件代码片段"""
    if style_key not in DESIGN_TEMPLATES: return False
    style_data = DESIGN_TEMPLATES[style_key]
    colors = style_data["colors"]

    os.makedirs(output_dir, exist_ok=True)

    button_snippet = f'''<button class="btn btn-primary">
  Click me
</button>

<style>
.btn {{
  background: {colors.get('primary', colors.get('link', '#0070F3'))};
  color: #fff;
  border: none;
  border-radius: {style_data['radius']};
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}}
.btn:hover {{
  transform: translateY(-2px);
  box-shadow: {style_data['shadow']};
}}
.btn-secondary {{
  background: transparent;
  color: {colors.get('text', '#1E1E1E')};
  border: 1px solid {colors.get('border', '#E5E5E5')};
}}
</style>'''

    card_snippet = f'''<div class="card">
  <h3 class="card-title">Card Title</h3>
  <p class="card-text">Card content goes here.</p>
</div>

<style>
.card {{
  background: {colors.get('backgroundSecondary', '#F5F5F5')};
  border: 1px solid {colors.get('border', '#E5E5E5')};
  border-radius: {style_data['radius']};
  padding: 24px;
  box-shadow: {style_data['shadow']};
}}
.card-title {{
  margin: 0 0 12px 0;
  font-size: 18px;
  color: {colors.get('text', '#1E1E1E')};
}}
.card-text {{
  margin: 0;
  color: {colors.get('textSecondary', '#737373')};
  font-size: 14px;
}}
</style>'''

    form_snippet = f'''<div class="form-group">
  <label for="username">Username</label>
  <input type="text" id="username" class="input-field" placeholder="Enter username">
</div>

<style>
.form-group {{
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}}
.input-field {{
  padding: 12px 16px;
  border: 1px solid {colors.get('border', '#E5E5E5')};
  border-radius: {style_data['radius']};
  background: {colors.get('background', '#FFFFFF')};
  color: {colors.get('text', '#1E1E1E')};
  font-size: 14px;
}}
.input-field:focus {{
  outline: none;
  border-color: {colors.get('primary', colors.get('link', '#0070F3'))};
  box-shadow: 0 0 0 3px {colors.get('primary', colors.get('link', '#0070F3'))}22;
}}
</style>'''

    with open(os.path.join(output_dir, "button.html"), "w", encoding="utf-8") as f:
        f.write(button_snippet)
    with open(os.path.join(output_dir, "card.html"), "w", encoding="utf-8") as f:
        f.write(card_snippet)
    with open(os.path.join(output_dir, "form.html"), "w", encoding="utf-8") as f:
        f.write(form_snippet)

    return True


def generate_compare_html(project_path: str, style_key_a: str, style_key_b: str, project_info: Dict[str, Any]) -> Optional[str]:
    """生成 A/B 风格对比页"""
    if style_key_a not in DESIGN_TEMPLATES or style_key_b not in DESIGN_TEMPLATES:
        return None

    style_a = DESIGN_TEMPLATES[style_key_a]
    style_b = DESIGN_TEMPLATES[style_key_b]

    compare_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A/B 风格对比 - {{style_a['name']}} vs {{style_b['name']}}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
        .toolbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #333;
            color: #fff;
            padding: 16px 24px;
            display: flex;
            justify-content: center;
            gap: 40px;
            z-index: 1000;
        }}
        .toolbar button {{
            background: transparent;
            border: 1px solid #666;
            color: #fff;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
        }}
        .toolbar button.active {{
            background: #0070F3;
            border-color: #0070F3;
        }}
        .compare-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2px;
            margin-top: 60px;
            min-height: calc(100vh - 60px);
        }}
        .compare-pane {{
            padding: 40px;
            overflow: auto;
        }}
        .pane-a {{
            background: {style_a['colors'].get('background', '#FFFFFF')};
            color: {style_a['colors'].get('text', '#1E1E1E')};
        }}
        .pane-b {{
            background: {style_b['colors'].get('background', '#FFFFFF')};
            color: {style_b['colors'].get('text', '#1E1E1E')};
        }}
        .style-label {{
            position: fixed;
            top: 70px;
            font-size: 14px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 4px;
        }}
        .label-a {{
            left: 40px;
            background: {style_a['colors'].get('primary', style_a['colors'].get('link', '#0070F3'))};
            color: #fff;
        }}
        .label-b {{
            right: 40px;
            background: {style_b['colors'].get('primary', style_b['colors'].get('link', '#0070F3'))};
            color: #fff;
        }}
        .card {{
            background: {'var(--bg-secondary)' if False else style_a['colors'].get('backgroundSecondary', '#F5F5F5')};
            border: 1px solid {style_a['colors'].get('border', '#E5E5E5')};
            border-radius: {style_a['radius']};
            padding: 24px;
            margin-bottom: 20px;
        }}
        .card h3 {{ margin-bottom: 12px; font-size: 18px; }}
        .card p {{ color: {style_a['colors'].get('textSecondary', '#737373')}; font-size: 14px; }}
        .btn {{
            background: {style_a['colors'].get('primary', style_a['colors'].get('link', '#0070F3'))};
            color: #fff;
            border: none;
            border-radius: {style_a['radius']};
            padding: 12px 24px;
            font-size: 16px;
            cursor: pointer;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        .btn-outline {{
            background: transparent;
            color: {style_a['colors'].get('text', '#1E1E1E')};
            border: 1px solid {style_a['colors'].get('border', '#E5E5E5')};
        }}
        .input-field {{
            width: 100%;
            padding: 12px 16px;
            border: 1px solid {style_a['colors'].get('border', '#E5E5E5')};
            border-radius: {style_a['radius']};
            margin-bottom: 16px;
            font-size: 14px;
        }}
        h1 {{ font-size: 32px; margin-bottom: 16px; }}
        h2 {{ font-size: 24px; margin-bottom: 12px; }}
        p {{ margin-bottom: 12px; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="toolbar">
        <button onclick="showBoth()">并排对比</button>
        <button onclick="showOnlyA()">只看 A</button>
        <button onclick="showOnlyB()">只看 B</button>
        <button onclick="showSideBySide()">左右切换</button>
    </div>
    <span class="style-label label-a">{style_a['name']}</span>
    <span class="style-label label-b">{style_b['name']}</span>
    <div class="compare-container" id="compareContainer">
        <div class="compare-pane pane-a" id="paneA">
            <h1>{style_a['name']}</h1>
            <p style="color: {style_a['colors'].get('textSecondary', '#737373')};">{style_a['description']}</p>
            <h2>按钮组件</h2>
            <button class="btn">主要按钮</button>
            <button class="btn btn-outline">次要按钮</button>
            <h2 style="margin-top: 24px;">卡片组件</h2>
            <div class="card">
                <h3>卡片标题</h3>
                <p>这是卡片的描述文本，展示了内容的呈现效果。</p>
            </div>
            <h2 style="margin-top: 24px;">表单组件</h2>
            <input type="text" class="input-field" placeholder="请输入用户名">
            <input type="email" class="input-field" placeholder="请输入邮箱">
        </div>
        <div class="compare-pane pane-b" id="paneB">
            <h1>{style_b['name']}</h1>
            <p style="color: {style_b['colors'].get('textSecondary', '#737373')};">{style_b['description']}</p>
            <h2>按钮组件</h2>
            <button class="btn" style="background: {style_b['colors'].get('primary', style_b['colors'].get('link', '#0070F3'))}; border-radius: {style_b['radius']};">主要按钮</button>
            <button class="btn btn-outline" style="border-color: {style_b['colors'].get('border', '#E5E5E5')}; color: {style_b['colors'].get('text', '#1E1E1E')}; border-radius: {style_b['radius']};">次要按钮</button>
            <h2 style="margin-top: 24px;">卡片组件</h2>
            <div class="card" style="background: {style_b['colors'].get('backgroundSecondary', '#F5F5F5')}; border-color: {style_b['colors'].get('border', '#E5E5E5')}; border-radius: {style_b['radius']};">
                <h3 style="color: {style_b['colors'].get('text', '#1E1E1E')};">卡片标题</h3>
                <p style="color: {style_b['colors'].get('textSecondary', '#737373')};">这是卡片的描述文本，展示了内容的呈现效果。</p>
            </div>
            <h2 style="margin-top: 24px;">表单组件</h2>
            <input type="text" class="input-field" style="border-color: {style_b['colors'].get('border', '#E5E5E5')}; border-radius: {style_b['radius']}; background: {style_b['colors'].get('background', '#FFFFFF')}; color: {style_b['colors'].get('text', '#1E1E1E')};">
            <input type="email" class="input-field" style="border-color: {style_b['colors'].get('border', '#E5E5E5')}; border-radius: {style_b['radius']}; background: {style_b['colors'].get('background', '#FFFFFF')}; color: {style_b['colors'].get('text', '#1E1E1E')};">
        </div>
    </div>
    <script>
        function showBoth() {{
            document.getElementById('compareContainer').style.gridTemplateColumns = '1fr 1fr';
            document.getElementById('paneA').style.display = 'block';
            document.getElementById('paneB').style.display = 'block';
        }}
        function showOnlyA() {{
            document.getElementById('compareContainer').style.gridTemplateColumns = '1fr';
            document.getElementById('paneA').style.display = 'block';
            document.getElementById('paneB').style.display = 'none';
        }}
        function showOnlyB() {{
            document.getElementById('compareContainer').style.gridTemplateColumns = '1fr';
            document.getElementById('paneA').style.display = 'none';
            document.getElementById('paneB').style.display = 'block';
        }}
        let showingA = true;
        function showSideBySide() {{
            document.getElementById('compareContainer').style.gridTemplateColumns = '1fr 1fr';
            document.getElementById('paneA').style.display = showingA ? 'block' : 'none';
            document.getElementById('paneB').style.display = showingA ? 'none' : 'block';
            showingA = !showingA;
        }}
    </script>
</body>
</html>"""

    compare_path = os.path.join(project_path, f"compare-{style_key_a}-vs-{style_key_b}.html")
    with open(compare_path, "w", encoding="utf-8") as f:
        f.write(compare_content)
    return compare_path


def show_help():
    """显示帮助信息"""
    help_text = """🎨 beautify-ui - 智能 UI 美化脚本 v3.3.0

用法：
  py beautify.py <项目路径> [风格名称] [--auto] [--preview] [--dry-run] [--config <path>] [--help]

参数：
  <项目路径>          项目目录路径（必需）
  [风格名称]          可选：指定风格，如 notion、linear、github 等
  --auto              自动检测项目类型并推荐最佳风格
  --preview           生成预览页（不修改原项目）
  --dry-run           预览更改但不应用
  --config <path>     使用自定义配置文件
  --tokens            导出 Design Tokens
  --snippets          生成组件代码片段
  --compare           A/B 风格对比模式
  --help              显示本帮助信息

可用风格（{}种）：
  教育文档类：notion, vercel, claude, cursor
  创意设计类：figma, elevenlabs, spotify, airbnb, bytedance
  工具效率类：linear, raycast, superhuman, ollama
  商务金融类：stripe, tesla, apple, github, antdesign
  社交娱乐类：discord, slack, telegram, tencent
  中国厂商类：alibaba, bytedance, tencent, antdesign, huawei, xiaomi, jd, meituan
  电商生活类：shopify, amazon, taobao

示例：
  py beautify.py C:\\projects\\my-site notion
  py beautify.py C:\\projects\\my-site --auto
  py beautify.py C:\\projects\\my-site github --preview
  py beautify.py C:\\projects\\my-site shopify --preview
  py beautify.py C:\\projects\\my-site huawei --dry-run
""".format(len(DESIGN_TEMPLATES))
    print(help_text)


def main():
    if '--help' in sys.argv or len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    project_path = sys.argv[1]
    style_key = sys.argv[2].lower() if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    is_preview = '--preview' in sys.argv
    is_dry_run = '--dry-run' in sys.argv
    is_tokens = '--tokens' in sys.argv
    is_snippets = '--snippets' in sys.argv
    is_compare = '--compare' in sys.argv

    if is_dry_run:
        print("🔍 DRY-RUN 模式：预览更改但不应用")

    if not os.path.exists(project_path):
        print(f"❌ 路径不存在：{project_path}")
        sys.exit(1)

    print("\n🔍 分析项目...")
    project_info = detect_project_type(project_path)
    framework_info = []
    if project_info['type'] != 'static':
        framework_info.append(project_info['type'].upper())
    if project_info['has_tailwind']:
        framework_info.append('Tailwind')
    if project_info['has_styled_components']:
        framework_info.append('Styled Components')
    if project_info['has_emotion']:
        framework_info.append('Emotion')
    if project_info['has_scss']:
        framework_info.append('SCSS')
    if project_info['has_less']:
        framework_info.append('Less')
    framework_str = ', '.join(framework_info) if framework_info else 'Static HTML'
    print(f"📦 检测到：{framework_str}")

    if is_compare:
        compare_styles = [s for s in sys.argv[sys.argv.index('--compare') + 1:] if not s.startswith('--')]
        if len(compare_styles) >= 2:
            style_key_a, style_key_b = compare_styles[0], compare_styles[1]
        else:
            print("❌ --compare 需要指定两种风格：--compare <风格A> <风格B>")
            sys.exit(1)
        print(f"\n🔄 A/B 风格对比：{DESIGN_TEMPLATES[style_key_a]['name']} vs {DESIGN_TEMPLATES[style_key_b]['name']}")
        if not is_dry_run:
            compare_path = generate_compare_html(project_path, style_key_a, style_key_b, project_info)
            if compare_path:
                print(f"✅ {compare_path}")
                try:
                    webbrowser.open(f"file://{compare_path}")
                    print("🌐 已打开浏览器预览")
                except Exception:
                    pass
        print("\n✨ 完成！")
        sys.exit(0)

    if style_key == '--auto' or style_key is None:
        style_key, suitable = recommend_style(project_info)
        print(f"💡 推荐：{DESIGN_TEMPLATES[style_key]['name']}")
    elif style_key not in DESIGN_TEMPLATES:
        print(f"❌ 风格不存在：{style_key}")
        print(f"可用：{', '.join(DESIGN_TEMPLATES.keys())}")
        sys.exit(1)

    style_data = DESIGN_TEMPLATES[style_key]
    print(f"\n🎨 风格：{style_data['name']} - {style_data['description']}")

    if is_dry_run:
        print("\n📋 DRY-RUN - 以下是将被生成的文件：")
        print(f"   - DESIGN.md")
        print(f"   - styles/theme-override.css")
        if project_info['has_tailwind']:
            print(f"   - tailwind.config.js")
        if project_info['type'] in ['vite', 'nextjs', 'cra', 'nuxt', 'remix', 'sveltekit']:
            print(f"   - assets/theme-override.css")
        if is_preview:
            print(f"   - preview-{style_key}.html")
        if is_tokens:
            print(f"   - tokens.json")
            print(f"   - tokens.js")
        if is_snippets:
            print(f"   - snippets/button.html")
            print(f"   - snippets/card.html")
            print(f"   - snippets/form.html")
        print("\n✨ DRY-RUN 完成！")
        sys.exit(0)

    design_md_path = os.path.join(project_path, "DESIGN.md")
    if generate_design_md(style_key, design_md_path):
        print("✅ DESIGN.md")

    styles_dir = os.path.join(project_path, "styles")
    if not os.path.exists(styles_dir):
        os.makedirs(styles_dir)
    css_path = os.path.join(styles_dir, "theme-override.css")
    css_content = generate_css_content(style_key, project_info)
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print("✅ styles/theme-override.css")

    if project_info['has_tailwind']:
        tailwind_path = os.path.join(project_path, "tailwind.config.js")
        if generate_tailwind_config(style_key, project_info, tailwind_path):
            print("✅ tailwind.config.js")

    if project_info['type'] in ['vite', 'nextjs', 'cra', 'nuxt', 'remix', 'sveltekit']:
        assets_dir = os.path.join(project_path, "assets")
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
        shutil.copy(css_path, os.path.join(assets_dir, "theme-override.css"))
        print("✅ assets/theme-override.css")

    if is_tokens:
        tokens_json_path = os.path.join(project_path, "tokens.json")
        tokens_js_path = os.path.join(project_path, "tokens.js")
        if generate_design_tokens_json(style_key, project_info, tokens_json_path):
            print(f"✅ tokens.json")
        if generate_design_tokens_js(style_key, project_info, tokens_js_path):
            print(f"✅ tokens.js")

    if is_snippets:
        snippets_dir = os.path.join(project_path, "snippets")
        if generate_component_snippets(style_key, project_info, snippets_dir):
            print(f"✅ snippets/button.html")
            print(f"✅ snippets/card.html")
            print(f"✅ snippets/form.html")

    if is_preview or '--preview' in sys.argv:
        print("\n📺 生成预览页...")
        preview_path = generate_preview_html(project_path, style_key, project_info)
        if preview_path:
            print(f"✅ {preview_path}")
            try:
                webbrowser.open(f"file://{preview_path}")
                print("🌐 已打开浏览器预览")
            except Exception:
                print(f"📄 预览路径：{preview_path}")

    print("\n✨ 完成！")


if __name__ == "__main__":
    main()
