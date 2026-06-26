# Daily Income Logger

自动记录每日各平台收入，生成收入报告和趋势分析。

## 功能

- **多平台支持**: 支持手动录入各平台收入（自媒体、广告、电商等）
- **每日汇总**: 自动生成每日收入汇总报告
- **趋势分析**: 按周/月统计收入趋势
- **数据导出**: 支持导出 CSV/JSON 格式报告

## 使用方式

```
用户: 今天各平台收入是多少？
助手: 使用 daily-income-logger 查询今日收入汇总

用户: 记录今日B站收入500元
助手: 使用 daily-income-logger 记录收入

用户: 这周收入趋势如何？
助手: 使用 daily-income-logger 分析本周趋势
```

## 执行脚本

### 1. 查询今日收入汇总
```bash
#!/bin/bash
# daily-income-logger query today
DATA_DIR="$HOME/.daily-income-logger"
TODAY=$(date +%Y-%m-%d)
mkdir -p "$DATA_DIR/data"

if [ -f "$DATA_DIR/data/income.json" ]; then
  cat "$DATA_DIR/data/income.json" | jq -r --arg date "$TODAY" '
    .records[] | select(.date == $date) | 
    "平台: \(.platform) | 金额: ¥\(.amount) | 备注: \(.note)"'
else
  echo "今日暂无收入记录"
fi
```

### 2. 记录收入
```bash
#!/bin/bash
# daily-income-logger record <platform> <amount> [note]
DATA_DIR="$HOME/.daily-income-logger"
mkdir -p "$DATA_DIR/data"

PLATFORM=$1
AMOUNT=$2
NOTE=${3:-""}
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date -Iseconds)

INCOME_FILE="$DATA_DIR/data/income.json"

# 初始化或读取现有数据
if [ ! -f "$INCOME_FILE" ]; then
  echo '{"records":[]}' > "$INCOME_FILE"
fi

# 添加新记录
jq --arg date "$TODAY" --arg ts "$TIMESTAMP" --arg platform "$PLATFORM" \
   --arg amount "$AMOUNT" --arg note "$NOTE" \
   '.records += [{"date":$date,"timestamp":$ts,"platform":$platform,"amount":($amount | tonumber),"note":$note}]' \
   "$INCOME_FILE" > tmp.json && mv tmp.json "$INCOME_FILE"

echo "已记录: $PLATFORM +¥$AMOUNT"
```

### 3. 生成周报
```bash
#!/bin/bash
# daily-income-logger weekly-report
DATA_DIR="$HOME/.daily-income-logger"
START_DATE=$(date -d "7 days ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

echo "===== 周收入报告 ====="
echo "时间: $START_DATE ~ $END_DATE"
echo ""

if [ -f "$DATA_DIR/data/income.json" ]; then
  cat "$DATA_DIR/data/income.json" | jq -r --arg start "$START_DATE" --arg end "$END_DATE" '
    [.records[] | select(.date >= $start and .date <= $end)] |
    group_by(.platform) |
    .[] | 
    "【\.[0].platform】总计: ¥\(map(.amount) | add)"'
else
  echo "暂无数据"
fi
```

## 数据存储

收入数据存储在本地 JSON 文件中:
- `~/.daily-income-logger/data/income.json` - 收入记录
- `~/.daily-income-logger/data/reports/` - 生成的报告

## 配置

首次使用需要配置收入类别:
```json
{
  "categories": [
    "bilibili", "youtube", "xiaohongshu", 
    "advertising", "affiliate", "freelance"
  ]
}
```

## 权限

需要读写本地文件系统权限，用于存储收入数据。

## 版本

1.0.0