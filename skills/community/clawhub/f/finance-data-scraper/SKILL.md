---
name: finance-data-scraper
description: |
  完整的财经数据抓取Skill，包含：
  1. 每日财经新闻（Chrome插件抓取）
  2. 每日财经新闻（无头浏览器抓取）
  3. 每日大盘数据
  4. 每日热门板块数据
  5. 每日涨停个股数据
  6. Chrome浏览器Tab清理（防止内存溢出）
  包含所有入库表配置、定时任务配置、去重规则等
---

# 财经数据抓取Skill（完整版）

完整的财经数据抓取解决方案，包含多种抓取方式、入库配置、定时任务、内存清理等功能！

---

## 🚨 前置条件（必须满足！）
1. **OpenClaw浏览器扩展已安装并连接**（用于Chrome插件抓取）
2. **NocoDB配置已提供**（BASE_URL、TOKEN、各表ID）
3. **sshpass已安装**（如果需要上传文件到服务器，可选）
4. **Python 3.7+已安装**

---

## 📋 抓取任务总览

| 任务编号 | 任务名称 | 抓取内容 | 入库表ID | 建议定时配置 | 抓取方式 |
|---------|---------|---------|---------|-------------|---------|
| 1 | 每日财经新闻（Chrome插件） | 东方财富财经导读、财联社等新闻 | 需用户提供（示例：`m2w****33m`） | `30 9,12,15,18 * * *`（每天4次） | Chrome浏览器插件（OpenClaw browser API） |
| 2 | 每日财经新闻（无头浏览器） | 东方财富财经导读等新闻 | 需用户提供 | `0 9,12,15,18 * * *`（每天4次） | 无头浏览器（Playwright/Puppeteer） |
| 3 | 每日大盘数据 | 每日大盘指数数据 | 需用户提供（示例：`mhmt****ibzo`） | `0 15:05 * * *`（每日收盘后） | 东方财富数据接口 |
| 4 | 每日热门板块数据 | 每日一级行业板块涨幅TOP3 | 需用户提供（示例：`mcit****je27`） | `10 15 * * *`（每日15:10） | 东方财富数据接口 |
| 5 | 每日涨停个股数据 | 每日涨停个股（代码/名称/涨幅/成交额/封单/连板数/行业等） | 需用户提供（示例：`mq8****ct7`） | `05 15 * * *`（每日15:05） | 东方财富数据接口 |
| 6 | Chrome浏览器Tab清理 | 保留1个东方财富tab，关闭其他所有tab | 无 | `20,50 * * * *`（每小时20分和50分） | `scripts/cleanup_tabs.py` |

---

## 🔧 NocoDB统一配置（必须提供！）
| 配置项 | 说明 | 示例值 |
|-------|------|--------|
| `BASE_URL` | NocoDB API基础URL | `https://nocodb.*****.com/api/v2` |
| `TOKEN` | NocoDB API Token | 需用户提供 |
| `TABLE_ID_NEWS` | 财经新闻入库表ID | 需用户提供 |
| `TABLE_ID_MARKET` | 每日大盘数据入库表ID | 需用户提供 |
| `TABLE_ID_PLATES` | 每日热门板块数据入库表ID | 需用户提供 |
| `TABLE_ID_LIMIT_UP` | 每日涨停个股数据入库表ID | 需用户提供 |

---

## 📁 使用前准备

### 步骤1：确认前置条件已满足
- OpenClaw浏览器扩展已安装并连接
- NocoDB配置信息已准备好

### 步骤2：配置NocoDB
复制 `config-examples/nocodb-config.example.json` 为 `nocodb-config.json`，填入你的配置：
```bash
cp config-examples/nocodb-config.example.json nocodb-config.json
```

### 步骤3：配置定时任务
参考 `config-examples/cron-configs/` 目录下的示例配置，创建你的定时任务配置文件！

---

## 🔨 脚本使用说明

### 1. Chrome浏览器Tab清理脚本
**路径**：`scripts/cleanup_tabs.py`
**功能**：防止浏览器tab过多造成内存溢出
**策略**：
- 保留**1个**东方财富标签页（必须有至少1个）
- 关闭其他所有多余的东方财富标签页
- 关闭所有非东方财富标签页
**使用**：
```bash
python scripts/cleanup_tabs.py
```

### 2. NocoDB导入脚本
**路径**：`scripts/import_to_nocodb.py`
**功能**：批量导入财经新闻到NocoDB
**去重规则**：按 `source` + `content` 组合去重
**使用**：
```bash
# 使用最新的JSON文件
python scripts/import_to_nocodb.py

# 指定文件
python scripts/import_to_nocodb.py /path/to/data.json
```

---

## 📚 参考文档
- `config-examples/`：配置示例（NocoDB配置、Cron配置）
- `references/`：抓取规范文档（待补充）

---

## ⚠️ 注意事项
1. **定时任务配置**：请根据你的实际情况调整定时时间（考虑交易时间）
2. **内存管理**：务必配置Chrome浏览器Tab清理任务，防止内存溢出
3. **去重规则**：财经新闻按 `source` + `content` 组合去重
4. **板块数据规则**：仅保留一级行业，排除地域板块、细分行业和概念板块
