# Airline Info to Website — 示例手册

## 示例 1：抓取整个航司

```bash
# 新加坡航空
python scripts/scrape_seatmaps.py --airline "新加坡航空 Singapore Airlines SQ" --output FlightData/
node scripts/classify-images.js --base-dir "FlightData/新加坡航空 Singapore Airlines SQ"
node scripts/dedup-images.js --base-dir "FlightData/新加坡航空 Singapore Airlines SQ"
```

## 示例 2：抓取单个机型

```bash
python scripts/scrape_seatmaps.py "https://seatmaps.com/zh-CN/airlines/singapore-airlines-airbus-a350-900.html" --output FlightData/
```

## 示例 3：其他航司

```bash
# 阿联酋航空
python scripts/scrape_seatmaps.py --airline "阿联酋航空 Emirates EK" --output FlightData/

# 国泰航空
python scripts/scrape_seatmaps.py --airline "国泰航空 Cathay Pacific CX" --output FlightData/

# 日本航空
python scripts/scrape_seatmaps.py --airline "日本航空 Japan Airlines JL" --output FlightData/
```

## 示例 4：限制抓取数量

```bash
python scripts/scrape_seatmaps.py --airline "新加坡航空 Singapore Airlines SQ" --output FlightData/ --limit 3
```

## 示例 5：预览模式（不下载）

```bash
python scripts/scrape_seatmaps.py --airline "新加坡航空 Singapore Airlines SQ" --output FlightData/ --dry-run
```

## 输出示例

执行后会生成如下结构：

```
FlightData/
└── 新加坡航空 Singapore Airlines SQ/
    ├── Airbus A350-900/
    │   ├── 机型详情.md
    │   ├── 完整内容整理.md
    │   └── images/
    │       ├── 0-原始数据/
    │       ├── 1-座椅布局/
    │       ├── 2-座椅图片/
    │       ├── 3-机上餐食/
    │       ├── 4-娱乐设备/
    │       └── 5-其他信息/
    ├── Airbus A380/
    └── ...
```
