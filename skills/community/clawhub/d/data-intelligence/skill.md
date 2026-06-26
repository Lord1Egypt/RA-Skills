---
name: data-intelligence
description: 综合数据智能平台 - 整合 Apify 云端爬虫、PinchTab 浏览器自动化、内容分析与数据工作流。支持 55+ 平台的网络爬虫、线索生成、电商情报、竞品分析、趋势研究，以及浏览器自动化测试和数据提取。
metadata:
  version: "1.0"
  origin: "Apify + PinchTab + Content Engine"
---

# Data Intelligence 数据智能平台

综合数据智能解决方案，整合云端爬虫、浏览器自动化和内容分析，构建完整的数据采集与分析工作流。

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Data Intelligence 平台                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   云端爬虫层      │  浏览器自动化层   │      内容分析层            │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ • Apify Actors  │ • PinchTab      │ • 内容工厂                  │
│ • 55+ 平台支持   │ • 多实例编排     │ • 趋势分析                  │
│ • 无服务器架构   │ • Token高效提取  │ • 竞品监测                  │
│ • 弹性扩展      │ • 自动化测试     │ • 数据可视化                │
└─────────────────┴─────────────────┴─────────────────────────────┘
         │                │                   │
         └────────────────┼───────────────────┘
                          ↓
              ┌─────────────────────┐
              │    数据工作流引擎     │
              │  • 数据采集          │
              │  • 清洗转换          │
              │  • 分析洞察          │
              │  • 报告生成          │
              └─────────────────────┘
```

---

## 一、云端爬虫层 (Apify)

### 1.1 支持的 55+ 平台

#### 社交媒体 (45 Actors)

| 平台 | Actor 数量 | 主要用途 |
|------|-----------|----------|
| **Instagram** | 12 | 个人资料、帖子、评论、标签、Reels |
| **Facebook** | 14 | 页面、帖子、评论、广告、群组、活动 |
| **TikTok** | 14 | 视频、评论、用户、标签、趋势、直播 |
| **YouTube** | 5 | 视频、频道、评论、Shorts |

#### 商业与本地 (10 Actors)

| 平台 | Actor 数量 | 主要用途 |
|------|-----------|----------|
| **Google Maps** | 4 | 商家信息、评论、邮箱提取 |
| **Booking.com** | 2 | 酒店数据、评论 |
| **TripAdvisor** | 1 | 评论分析 |
| **Google Search** | 1 | 搜索结果 |
| **Google Trends** | 1 | 趋势数据 |

### 1.2 核心 Actor 速查表

#### 线索生成

| 需求 | Actor ID | 输出 |
|------|----------|------|
| 本地商家 | `compass/crawler-google-places` | 名称、地址、电话、评分 |
| 邮箱提取 | `poidata/google-maps-email-extractor` | 邮箱列表 |
| 联系信息 | `vdrmota/contact-info-scraper` | 邮箱、电话、社交媒体 |
| Instagram 用户 | `apify/instagram-profile-scraper` | 个人资料、粉丝数 |
| TikTok 创作者 | `clockworks/tiktok-profile-scraper` | 创作者信息 |

#### 内容分析

| 需求 | Actor ID | 输出 |
|------|----------|------|
| Instagram 帖子 | `apify/instagram-post-scraper` | 内容、点赞、评论数 |
| TikTok 视频 | `clockworks/tiktok-scraper` | 视频、播放量、分享数 |
| YouTube 视频 | `streamers/youtube-scraper` | 标题、观看、点赞 |
| Facebook 页面 | `apify/facebook-pages-scraper` | 页面信息、帖子 |

#### 竞品监测

| 需求 | Actor ID | 输出 |
|------|----------|------|
| Google Maps 评论 | `compass/Google-Maps-Reviews-Scraper` | 评论、评分、情感 |
| Booking 评论 | `voyager/booking-reviews-scraper` | 住客评价 |
| TripAdvisor | `maxcopell/tripadvisor-reviews` | 旅游评论 |

### 1.3 Apify 使用工作流

**前置条件：**
```bash
# 1. 安装依赖
npm install -g @apify/mcpc

# 2. 配置 Token
echo "APIFY_TOKEN=your_token_here" > .env

# 3. 验证
export $(grep APIFY_TOKEN .env | xargs) && mcpc --version
```

**标准工作流：**

```markdown
## 数据采集任务清单

- [ ] 步骤 1: 明确目标 - 需要什么数据？从哪个平台？
- [ ] 步骤 2: 选择 Actor - 根据平台速查表选择
- [ ] 步骤 3: 获取 Schema - 了解输入参数
- [ ] 步骤 4: 配置参数 - 设置搜索关键词、数量等
- [ ] 步骤 5: 运行采集 - 执行 Actor
- [ ] 步骤 6: 数据清洗 - 处理缺失值、格式转换
- [ ] 步骤 7: 分析洞察 - 生成报告
```

**执行命令：**

```bash
# 快速预览（仅显示结果，不保存文件）
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call run-actor \
  actor:="compass/crawler-google-places" \
  input:='{"searchStrings": ["coffee shop"], "location": "New York"}'

# 导出 CSV
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call run-actor \
  actor:="compass/crawler-google-places" \
  input:='{"searchStrings": ["coffee shop"], "maxCrawledPlaces": 50}' \
  | jq -r '.content[0].text' > results.csv

# 导出 JSON
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call run-actor \
  actor:="apify/instagram-profile-scraper" \
  input:='{"usernames": ["example_user"]}' \
  | jq '.content[0].text | fromjson' > results.json
```

---

## 二、浏览器自动化层 (PinchTab)

### 2.1 与 Apify 的互补关系

| 场景 | 使用 Apify | 使用 PinchTab |
|------|-----------|---------------|
| 大规模数据采集 | ✅ 云端 Actor，并发高 | ❌ 本地运行，资源有限 |
| 需要登录/认证 | ⚠️ 需要 Cookie | ✅ 支持登录态保留 |
| 实时交互测试 | ❌ 不适合 | ✅ 点击、输入、验证 |
| 视觉回归测试 | ❌ 不支持 | ✅ 截图对比 |
| Token 敏感场景 | ❌ 成本高 | ✅ 文本提取省 Token |
| 动态内容渲染 | ✅ 云端渲染 | ✅ 本地渲染 |

### 2.2 混合工作流示例

**场景：监测竞品网站 + 分析其社交媒体**

```bash
# Step 1: 使用 PinchTab 访问竞品网站，提取关键信息
pinchtab nav https://competitor.com
sleep 3
pinchtab text > competitor-content.txt

# Step 2: 从网站提取社交媒体链接
grep -oE '(instagram|facebook|tiktok)\.com/[^" ]+' competitor-content.txt > social-links.txt

# Step 3: 使用 Apify 分析其社交媒体
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call run-actor \
  actor:="apify/instagram-profile-scraper" \
  input:='{"usernames": ["competitor_ig"]}' \
  > competitor-ig-data.json

# Step 4: 数据分析
node analyze-competitor.js competitor-ig-data.json
```

### 2.3 数据采集黄金组合

| 数据类型 | Apify Actor | PinchTab 补充 |
|----------|-------------|---------------|
| 商家信息 | Google Maps Actor | 官网详情验证 |
| 产品信息 | 电商 Actor | 价格实时监控 |
| 用户评论 | 平台评论 Actor | 情感分析可视化 |
| 社交媒体 | Instagram/TikTok Actor | 内容趋势监测 |

---

## 三、内容分析层

### 3.1 数据采集后的内容工作流

```
Apify 采集数据
    ↓
数据清洗 (Python/pandas)
    ↓
内容分析 (内容工厂技能)
    ↓
生成报告 / 发布内容
```

### 3.2 数据分析模板

**竞品分析报告模板：**

```markdown
---
title: 竞品分析报告 - {{competitor_name}}
date: {{date}}
tags: [competitor, analysis]
---

# {{competitor_name}} 竞品分析

## 数据来源
- 网站: {{website_url}}
- Instagram: {{ig_followers}} 粉丝
- 数据采集时间: {{date}}

## 核心指标

| 指标 | 数值 | 趋势 |
|------|------|------|
| 网站流量 | {{traffic}} | {{trend}} |
| 社媒粉丝 | {{followers}} | {{trend}} |
| 内容发布频率 | {{frequency}} | {{trend}} |
| 平均互动率 | {{engagement}} | {{trend}} |

## 内容策略

### 高表现内容类型
1. {{top_content_1}}
2. {{top_content_2}}
3. {{top_content_3}}

### 发布时机
- 最佳时间: {{best_time}}
- 发布频率: {{post_frequency}}

## 差异化建议
- [ ] 建议 1
- [ ] 建议 2
- [ ] 建议 3
```

---

## 四、实战案例

### 案例 1：本地商家线索挖掘

**目标：** 收集某城市所有咖啡店的信息和联系方式

```bash
#!/bin/bash
# coffee-shop-leads.sh

CITY="Los Angeles"
OUTPUT_FILE="coffee-shops-$(date +%Y%m%d).csv"

# Step 1: Apify 采集 Google Maps
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call run-actor \
  actor:="compass/crawler-google-places" \
  input:="{\"searchStrings\": [\"coffee shop\"], \"location\": \"$CITY\", \"maxCrawledPlaces\": 100}"

# Step 2: 提取有网站的数据，用 PinchTab 验证详情
# （可选：访问官网提取更多联系信息）

# Step 3: 数据清洗
cat raw-data.json | jq -r '.[] | [.title, .address, .phone, .website] | @csv' > "$OUTPUT_FILE"

echo "找到 $(wc -l < $OUTPUT_FILE) 家咖啡店，数据已保存到 $OUTPUT_FILE"
```

### 案例 2：竞品社交媒体监测

**目标：** 监测 3 个竞品的 Instagram 表现

```bash
#!/bin/bash
# competitor-monitoring.sh

COMPETITORS=("brand_a" "brand_b" "brand_c")
DATE=$(date +%Y%m%d)

for competitor in "${COMPETITORS[@]}"; do
  echo "分析 $competitor..."

  # Apify 采集数据
  export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com \
    --header "Authorization: Bearer $APIFY_TOKEN" \
    tools-call run-actor \
    actor:="apify/instagram-profile-scraper" \
    input:="{\"usernames\": [\"$competitor\"]}" \
    > "data/${competitor}-${DATE}.json"

  # 提取关键指标
  followers=$(cat "data/${competitor}-${DATE}.json" | jq -r '.[0].followersCount')
  posts=$(cat "data/${competitor}-${DATE}.json" | jq -r '.[0].postsCount')

  echo "$competitor: $followers 粉丝, $posts 帖子"
done

# 生成对比报告
node generate-report.js $DATE
```

### 案例 3：趋势研究 + 内容创作

**目标：** 发现 TikTok 趋势，快速创作相关内容

```bash
#!/bin/bash
# trend-to-content.sh

# Step 1: Apify 采集 TikTok 趋势
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call run-actor \
  actor:="clockworks/tiktok-trends-scraper" \
  input:='{"resultsLimit": 20}' \
  > trends.json

# Step 2: 提取热门标签
TOP_HASHTAG=$(cat trends.json | jq -r '.[0].hashtag.name')
TOP_VIEWS=$(cat trends.json | jq -r '.[0].stats.playCount')

echo "热门趋势: #$TOP_HASHTAG ($TOP_VIEWS 播放)"

# Step 3: 使用内容工厂技能创作文章
# /content-create "如何蹭 $TOP_HASHTAG 趋势涨粉"
```

---

## 五、安装与配置

### 5.1 安装依赖

```bash
# 1. Apify MCP CLI
npm install -g @apify/mcpc

# 2. PinchTab 浏览器自动化
curl -fsSL https://pinchtab.com/install.sh | bash

# 3. 配置环境变量
cat > .env << EOF
APIFY_TOKEN=your_apify_token_here
PINCHTAB_PORT=9867
EOF
```

### 5.2 验证安装

```bash
# 验证 Apify
export $(grep APIFY_TOKEN .env | xargs) && mcpc --version

# 验证 PinchTab
pinchtab --version

# 测试连接
pinchtab health
```

### 5.3 Claude Code 集成

在 `.claude/settings.json` 中添加：

```json
{
  "env": {
    "APIFY_TOKEN": "${APIFY_TOKEN}",
    "CLAUDE_PLUGIN_ROOT": "${workspaceFolder}"
  },
  "skills": [
    "data-intelligence"
  ]
}
```

---

## 六、命令速查

### 6.1 Apify 常用命令

```bash
# 搜索 Actor
mcpc tools-call search-actors keywords:="instagram" limit:=10

# 获取 Actor 详情
mcpc tools-call fetch-actor-details actor:="apify/instagram-profile-scraper"

# 运行 Actor
mcpc tools-call run-actor actor:="ACTOR_ID" input:='{}'

# 查看运行状态
mcpc tools-call get-run runId:="RUN_ID"
```

### 6.2 PinchTab 常用命令

```bash
# 启动服务
pinchtab

# 创建实例
pinchtab instances create --mode=headless

# 导航
pinchtab nav https://example.com

# 提取文本
pinchtab text

# 执行动作
pinchtab click e5
pinchtab fill e3 "text"
```

### 6.3 组合命令

```bash
# 数据采集 + 分析一站式
export $(grep APIFY_TOKEN .env | xargs) && \
mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call run-actor \
  actor:="compass/crawler-google-places" \
  input:='{"searchStrings": ["keyword"]}' | \
jq -r '.content[0].text' | \
python analyze.py
```

---

## 七、最佳实践

### 7.1 成本控制

| 工具 | 成本模式 | 适用场景 |
|------|----------|----------|
| Apify | 按结果付费 | 大规模数据采集 |
| PinchTab | 免费（本地） | 小批量、实时测试 |
| 组合 | 混合使用 | 大规模 + 实时验证 |

### 7.2 数据质量

- **验证样本**：大规模采集前，先用小样本验证数据质量
- **交叉验证**：同一数据用多个 Actor 采集，对比结果
- **时效性**：注意数据更新时间，避免使用过期数据

### 7.3 合规性

- 遵守各平台的服务条款
- 尊重 robots.txt
- 不采集个人隐私数据
- 合理使用频率，避免对目标网站造成压力

---

## 八、故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| APIFY_TOKEN not found | 环境变量未设置 | `export APIFY_TOKEN=xxx` |
| mcpc not found | CLI 未安装 | `npm install -g @apify/mcpc` |
| Actor not found | Actor ID 错误 | 检查拼写或搜索可用 Actor |
| Rate limit | 请求过快 | 增加延时或减少并发 |
| PinchTab timeout | 页面加载慢 | 增加 sleep 时间 |

---

## 九、参考资源

- [Apify 文档](https://docs.apify.com)
- [Apify Actor 市场](https://apify.com/store)
- [PinchTab 文档](https://pinchtab.com/docs)
- [内容工厂技能](../content-engine/skill.md)
- [浏览器自动化技能](../browser-automation/skill.md)

---

*让数据驱动决策，用智能提升效率。*
