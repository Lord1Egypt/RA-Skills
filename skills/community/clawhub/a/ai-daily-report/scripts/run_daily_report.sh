#!/usr/bin/env bash
# 用于定时或手动触发 AI 每日报告
# 前置：确保 GITHUB_TOKEN、FEISHU_CHAT_ID 已在环境变量中
# 依赖：python3, pip 包 feedparser jinja2 (可选 cairosvg), rsvg-convert 或 ImageMagick
set -euo pipefail
SKILL_ROOT="$(dirname "$(dirname "$(realpath "$0")")")"
cd "$SKILL_ROOT"
# 1. 抓新闻
python3 scripts/fetch_news.py > news.json
# 2. 抓项目
python3 scripts/fetch_top_projects.py > projects.json
# 3. 生成报告文件
python3 scripts/generate_report.py news.json projects.json
# 4. SVG → PNG
python3 scripts/svg_to_png.py report.svg
# 5. 发送报告（依赖 FEISHU_CHAT_ID 环境变量）
python3 scripts/send_report.py
