#!/bin/bash
# 启动币安资金费率监控 Skill MCP Server

# 加载 SkillPay 配置
source ~/.config/skillpay/env.sh

# 加载币安 API 配置
source ~/.config/binance/env.sh

# 启动 MCP Server
cd ~/.openclaw/workspace/skills/binance-monitor-skillpay
exec python3 server.py