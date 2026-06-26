# 从 Index 到 Detail：候选池深抓流程说明

## 概述

日报采集分两个阶段：

```
第一阶段：广撒网建候选池
  build_queries.py → collect_sources_with_opencli.py → filter_index.py
  输出：{date}_index.txt → {date}_index_filtered.txt

第二阶段：对高价值条目深抓正文
  collect_detail.py
  输��：{date}_detail.txt
```

## 为什么要分两阶段

第一阶段（index）从 20+ 个信息源快速拉取标题级信息，建立候选池。但不同来源返回的信息量不同：

| 来源类型 | 返回内容 | 是否需要深抓 |
|---------|---------|------------|
| **平台类**（微博/Twitter/Reddit/小红书等） | 已有完整内容（title + text 全文） | ❌ 不需要，直接用 |
| **网站类**（机器之心/量子位/TechCrunch 等） | 只有标题 + URL（来自 Google site: 搜索） | ✅ 需要，抓正文 |

所以 detail 阶段的核心工作是：**对网站类条目用 `opencli web read` 抓取正文**。

## 脚本说明

### collect_detail.py

```bash
# 基本用法
python3 scripts/collect_detail.py --date 2026-04-05

# dry-run（只看要抓哪些 URL，不实际执行）
python3 scripts/collect_detail.py --date 2026-04-05 --dry-run

# 限制最多深抓 20 个 URL
python3 scripts/collect_detail.py --date 2026-04-05 --max-fetch 20
```

### 输入

读取 `output/raw/{date}_index_filtered.txt`（由 filter_index.py 生成）。

### 处理逻辑

1. **解析 filtered index**，按 `time_status` 字段分为两类：
   - `time_status: in_window` → 平台类，已有完整内容
   - `time_status: google_filtered` → 网站类，需要深抓

2. **平台类条目**：直接复制到 detail 输出，不做额外请求

3. **网站类条目**：
   - 提取所有 URL，去重
   - 逐个执行 `opencli web read --url "<URL>"`
   - 每次请求间隔 3 秒
   - 正文截取前 2000 字符保存（避免文件过大）
   - 标记 `fetch_status: success / FAILED`

### 输出

`output/raw/{date}_detail.txt`，分两部分：

```
# ━━ 第一部分：平台类条目（已有完整内容）━━

--- [微博] (cn) ---
type: platform
keyword: 大模型
title: 大模型编程能力排名，Claude断崖领先...
author: 黄鱼Veda
time: 今天01:32
hot: ...
url: https://weibo.com/...

# ━━ 第二部分：网站类条目（深抓正文）━━

--- [量子位] (website) ---
type: website_detail
keyword: 大模型
title: OpenAI发布最新模型...
url: https://www.qbitai.com/2026/04/396346.html
fetch_status: success
fetched_content:
  （正文 Markdown 内容，最多 2000 字符）
```

## 完整流程

```bash
# 1. 生成查询
python3 scripts/build_queries.py --date 2026-04-05

# 2. 采集候选池
python3 scripts/collect_sources_with_opencli.py --date 2026-04-05 --max-keywords 5 --max-results 5

# 3. 时间筛选
python3 scripts/filter_index.py --date 2026-04-05 --window 3

# 4. 深抓正文
python3 scripts/collect_detail.py --date 2026-04-05

# 产出文件：
# output/raw/2026-04-05_queries.txt          ← 查询列表
# output/raw/2026-04-05_index.txt            ← 原始候选池
# output/raw/2026-04-05_index_filtered.txt   ← 筛选后候选池
# output/raw/2026-04-05_detail.txt           ← 深抓详情
```

## 后续：detail → 日报 JSON

detail.txt 包含了所有候选的完整信息，下一步由 AI 读取后：
1. 按 profile 画像筛选最相关的 15 条
2. 按优先级排序（官方发布 > 社区热议 > 背景报道）
3. 生成结构化 JSON（`output/daily/{date}.json`）
4. 渲染 HTML（`scripts/render_daily.py`）
