#!/bin/bash
# API Key 轮换提醒脚本
# 每3个月提醒一次

echo "🔐 API Key 轮换提醒"
echo "================================"
echo "时间: $(date '+%Y-%m-%d %H:%M')"
echo ""
echo "请轮换以下敏感 Key:"
echo "  1. 阿里云 AccessKey (重要!)"
echo "  2. 火山引擎 AccessKey"
echo ""
echo "查看余额: python3 ~/.openclaw/workspace/scripts/query_aliyun_balance.py"
echo "查看余额: python3 ~/.openclaw/workspace/scripts/query_volc_balance.py"
echo "================================"
