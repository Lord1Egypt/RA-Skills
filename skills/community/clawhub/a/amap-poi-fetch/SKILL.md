---
name: amap-poi-fetch
description: 高德地图POI数据采集技能。通过关键词抓取城市的医疗美容和生活美容机构分布数据，输出JSON原始数据和Excel汇总文件。触发词：「采集XX城市医美数据」「抓取POI」「导出医美机构Excel」「XX市医美机构分布」。
---

# amap-poi-fetch · 高德POI医美机构采集

## 快速使用

```bash
# 基本用法
python3 scripts/poi_fetch.py <城市名>

# 示例：采集成都数据
python3 scripts/poi_fetch.py 成都

# 跳过Excel（只采集JSON）
python3 scripts/poi_fetch.py 上海 --skip-excel

# 指定KEY
python3 scripts/poi_fetch.py 深圳 --key <YOUR_KEY>
```

## 工作流程

```
城市名输入
  ↓
获取城市区划adcode（高德行政区划API）
  ↓
逐区采集：
  ① 医疗美容 → ② 生活美容
  每词翻页（每页20条，上限200条）
  ↓
保存JSON到 ~/.openclaw/workspace/data/<城市>_poi/
  ↓
生成Excel（含3个Sheet：汇总 + 医疗美容明细 + 生活美容明细）
```

## 输出文件

| 文件类型 | 位置 |
|---------|------|
| JSON原始数据 | `~/.openclaw/workspace/data/<城市>_poi/*.json` |
| Excel汇总 | `~/.openclaw/workspace/data/<城市>_poi/<城市>医美生活美容数据_YYYYMMDD.xlsx` |

## Excel结构

- **汇总**：各区医疗美容/生活美容数量统计
- **医疗美容明细**：机构名称、电话、地址、评分、人均、商圈、坐标
- **生活美容明细**：同上字段

## 已知限制

| 限制 | 说明 |
|------|------|
| API硬上限 | 每词每区最多返回200条 |
| QPS限制 | 并发需间隔≥1秒 |
| KEY | 默认使用主人已申请的KEY（`0c166a2bf61c1e4e6c96e3b645233e54`） |

## 脚本参数

| 参数 | 说明 |
|------|------|
| `<城市名>` | 必填，城市/省份名称（支持"成都""成都市"） |
| `--skip-excel` | 仅采集JSON，不生成Excel |
| `--key <KEY>` | 使用指定高德KEY |

## 依赖

```bash
pip install openpyxl
```

## 执行路径

脚本位置：`~/.openclaw/workspace/skills/amap-poi-fetch/scripts/poi_fetch.py`
