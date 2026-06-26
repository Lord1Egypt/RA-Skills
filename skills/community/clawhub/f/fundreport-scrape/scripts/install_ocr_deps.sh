#!/bin/bash
# fundreport-scrape v1.0.0 - OCR 依赖一键安装脚本
# Author: ymzhang
# 适用于 OpenCloudOS/CentOS 9

echo "========================================"
echo "基金月报技能 - OCR 依赖安装"
echo "========================================"
echo ""

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then
  echo "⚠️  请使用 sudo 运行此脚本"
  echo "用法：sudo ./install_ocr_deps.sh"
  exit 1
fi

# 步骤 1: 安装系统工具
echo "📦 步骤 1/2: 安装系统工具 (Tesseract + Poppler)..."
yum install -y tesseract tesseract-langpack-chi_simp tesseract-osd poppler-utils

if [ $? -eq 0 ]; then
  echo "✅ 系统工具安装成功"
else
  echo "❌ 系统工具安装失败"
  exit 1
fi

# 验证 Tesseract
echo ""
echo "🔍 验证 Tesseract 安装..."
tesseract --version
echo ""
echo "📋 可用语言包:"
tesseract --list-langs
echo ""

# 检查中文语言包
if tesseract --list-langs | grep -q "chi_sim"; then
  echo "✅ 中文语言包已安装"
else
  echo "❌ 中文语言包未安装，请检查 tesseract-langpack-chi_simp"
  exit 1
fi

# 步骤 2: 安装 Python 包
echo ""
echo "🐍 步骤 2/2: 安装 Python 包..."
pip install pdf2image Pillow opencv-python-headless

if [ $? -eq 0 ]; then
  echo "✅ Python 包安装成功"
else
  echo "❌ Python 包安装失败"
  exit 1
fi

# 验证 Python 包
echo ""
echo "🔍 验证 Python 包..."
python3 -c "import pdf2image; import pytesseract; import cv2; print('✅ 所有 Python 包加载成功')"

echo ""
echo "========================================"
echo "✅ OCR 依赖安装完成！"
echo "========================================"
echo ""
echo "使用方法："
echo "  python3 scripts/auto_update_two_months.py <模板.xlsx> <上月 PDF/> <本月 PDF/> <输出.xlsx>"
echo ""
