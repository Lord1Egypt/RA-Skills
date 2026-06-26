# airline-info-to-website / scripts

本目录包含航司机型数据抓取和整理的核心脚本。

## 核心流程脚本

| 文件 | 用途 | 用法 |
|------|------|------|
| `scrape_seatmaps.py` | 从 seatmaps.com 抓取航司机型数据 | `python scrape_seatmaps.py --airline "航司名" --output FlightData/` |
| `classify-images.js` | 语义分类图片到 1-5 子目录 | `node classify-images.js --base-dir "FlightData/航司目录"` |
| `dedup-images.js` | 基于 MD5 哈希删除重复图片 | `node dedup-images.js --base-dir "FlightData/航司目录"` |

## 脚本详情

### scrape_seatmaps.py

抓取航司机型数据，包括：
- 机型基本信息（名称、舱位配置）
- 座位图和座椅图片
- 自动生成 `机型详情.md` 和 `完整内容整理.md`

**参数：**
- `--airline`: 航空公司名称（中英文）
- `--output`: 输出目录（默认 FlightData/）
- `--limit`: 限制抓取数量
- `--dry-run`: 预览模式，不下载

**示例：**
```bash
python scrape_seatmaps.py --airline "新加坡航空 Singapore Airlines SQ" --output FlightData/
python scrape_seatmaps.py "https://seatmaps.com/zh-CN/airlines/..." --output FlightData/
```

### classify-images.js

将 `images/0-原始数据/` 中的图片按语义分类到：
- `1-座椅布局/` - 座位图、舱位平面图
- `2-座椅图片/` - 座椅实物照片
- `3-机上餐食/` - 餐食、菜单相关
- `4-娱乐设备/` - IFE、屏幕、Wi-Fi 等
- `5-其他信息/` - 外观、logo、杂项

**分类规则：**
- 基于文件名关键词匹配
- 保留原始文件，执行复制操作
- 生成 `classification-report.md` 报告

**示例：**
```bash
node classify-images.js --base-dir "FlightData/新加坡航空 Singapore Airlines SQ"
```

### dedup-images.js

检测并删除重复图片：
- 基于 MD5 哈希比较
- 保留第一份，删除后续重复
- 支持预览模式（`--dry-run`）

**示例：**
```bash
node dedup-images.js --base-dir "FlightData/新加坡航空 Singapore Airlines SQ"
node dedup-images.js --base-dir "FlightData/航司目录" --dry-run
```

## 依赖

- Python 3.7+: `pip install requests beautifulsoup4`
- Node.js 14+
