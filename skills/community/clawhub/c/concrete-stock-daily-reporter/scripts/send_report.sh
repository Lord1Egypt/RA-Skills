#!/bin/bash
# 每日自选股报告 - 自动发送脚本
# 用法：bash send_report.sh "代码1:名称1,代码2:名称2,..."
# 示例：bash send_report.sh "1A0001:上证指数,600036:招商银行,000858:五粮液"

cd /root/.openclaw/workspace/skills/stock-daily-report/scripts
OPENCLAW="/opt/node-v24.13.0-linux-x64/bin/openclaw"

# 从命令行参数获取股票列表
STOCKS_STR="${1:-}"

if [ -z "$STOCKS_STR" ]; then
    echo "错误：请提供股票列表"
    echo "用法：bash send_report.sh \"代码1:名称1,代码2:名称2,...\""
    echo "示例：bash send_report.sh \"1A0001:上证指数,600036:招商银行\""
    exit 1
fi

# 生成报告
REPORT=$(python3 daily_report.py "$STOCKS_STR")

# 发送飞书消息
$OPENCLAW message send \
  --channel feishu \
  --target ou_624ec10057e782149ded8bc7040ea7b9 \
  --message "$REPORT" >> /tmp/stock_report.log 2>&1

echo "报告已发送"