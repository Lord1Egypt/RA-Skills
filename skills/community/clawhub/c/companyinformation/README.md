# 企业舆情 (Company Information)

基于 FEEDAX API 的企业舆情监测与风险预警技能，提供全面的企业资讯查询能力。

## 📊 功能概述

支持查询特定上市公司的新闻资讯和舆情动态，包括：
- **公司新闻**: 万科、宁德时代、比亚迪、腾讯、茅台等
- **舆情监测**: 负面新闻、风险预警、口碑分析
- **投资研究**: 公司动态、行业对比、投资价值
- **风险预警**: 负面事件、信用评级、经营风险

## ⚠️ 前置条件：配置 API Key

**使用本技能前，必须先配置 API Key。**

### API Key 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| GE1003 | 未配置 API Key | 前往 https://www.feedax.cn 申请 |
| GE1004 | API Key 已失效 | 检查 API Key 有效性，或重新申请 |
| GE1005 | API Key 已过期 | 前往 https://www.feedax.cn 重新申请 |
| GE1006 | API Key 无效 | 前往 https://www.feedax.cn 重新申请 |
| GE1007 | 账户余额不足 | 前往 https://www.feedax.cn 充值 |

### 服务错误处理

| HTTP 状态码 | 错误提示 |
|------------|----------|
| 400 | 请求参数错误，请检查输入 |
| 401/403 | API Key 可能无效或已过期 |
| 429 | 请求过于频繁，请稍后再试 |
| 500 | 服务器内部错误 |
| 502 | 服务暂时不可用，请稍后再试 |
| 503 | 服务维护中，请稍后再试 |
| 504 | 网关超时，请稍后再试 |

---

## 文件结构

```
company-information/
├── SKILL.md                          # 技能说明文档
├── README.md                         # 本文件
└── scripts/
    ├── query_company_information.py  # 查询脚本
    └── config.json                   # API Key 配置文件（可选）
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API Key（三选一）

**方式 1: 命令行参数（推荐）**
```bash
python scripts/query_company_information.py --api-key "your-api-key" --company "万科"
```

**方式 2: 环境变量**
```bash
export FEEDAX_API_KEY="your-api-key"
python scripts/query_company_information.py --company "万科"
```

**方式 3: 配置文件**
在 `scripts/` 目录创建 `config.json` 文件：
```json
{
  "api_key": "your-api-key"
}
```

### 3. 基本用法

```bash
# 查询公司负面资讯
python scripts/query_company_information.py --company "万科" --sentiments 负面 --days 7

# 查询关键词
python scripts/query_company_information.py --keyword "恒大集团" --days 14

# 查询公司正面资讯
python scripts/query_company_information.py --company "宁德时代" --sentiments 正面 --days 30

# 按热度排序
python scripts/query_company_information.py --company "比亚迪" --sort-by heat_scores
```

---

## 参数说明

### 必填参数（二选一）

| 参数 | 简写 | 说明 |
|------|------|------|
| `--company` | `-c` | 公司名称 |
| `--keyword` | `-k` | 搜索关键词 |

### 情感筛选

| 参数 | 简写 | 可选值 |
|------|------|--------|
| `--sentiments` | `-s` | 正面 / 负面 / 中性（可多选） |

### 分页与排序

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--days` | `-d` | 7 | 查询天数 |
| `--page` | `-p` | 0 | 页码（从 0 开始） |
| `--size` | `-n` | 20 | 每页数量 |
| `--sort-by` | | `publish_date` | 排序字段：publish_date / heat_scores |
| `--sort-type` | | `DESC` | 排序方式：ASC / DESC |

### 输出控制

| 参数 | 简写 | 说明 |
|------|------|------|
| `--verbose` | `-v` | 显示详细内容（摘要） |
| `--output-dir` | | 输出目录（默认当前目录） |
| `--no-output` | | 不生成输出文件，仅显示结果 |
| `--api-key` | | FEEDAX API Key |

---

## 输出文件

### CSV 文件

- **文件名**: `company_information_<时间戳>.csv`
- **字段**: 发布时间、标题、摘要、内容、来源、公司名称、情感倾向、情感得分、重要程度、热度得分、浏览数、转发数、URL

### MD 说明文件

- **文件名**: `company_information_<时间戳>.md`
- **内容**: 查询统计、情感分布、重要程度分布、公司情感得分等

---

## 数据字段说明

| 字段 | 说明 |
|------|------|
| `articleTitle` | 新闻标题 |
| `articleContent` | 新闻正文 |
| `articleSummary` | 摘要 |
| `infoSource` | 新闻来源 |
| `articleUrl` | 原文链接 |
| `releaseDate` | 发布时间（13 位时间戳） |
| `articleSentiment` | 情感倾向（正面/负面/中性） |
| `articleImportanceLevel` | 重要程度（高/中/低） |
| `publicOpinionHeatScore` | 舆情热度得分 |
| `viewCount` | 浏览数 |
| `shareCount` | 转发数 |
| `golaxyCompanyTagResults` | 公司资讯标签结果 |

### 公司信息 (golaxyCompanyTagResults)

| 字段 | 说明 |
|------|------|
| `compName` | 公司名 |
| `compSentimentScore` | 公司情感得分（>0 正面，=0 中性，<0 负面） |
| `isMajorComp` | 是否为主要公司 |
| `newsRelevance` | 新闻与公司的相关性 |
| `stockInfo` | 上市信息（股票代码、简称） |

---

## 示例输出

```
共找到 20 条资讯:

================================================================================
1. [2026-04-02 14:30] 🟢 正面
   标题：万科发布 2025 年业绩预告，净利润同比增长
   来源：新浪财经 | 热度：85.3
   公司：万科企业股份有限公司
   情感得分：0.6
   重要程度：高
--------------------------------------------------------------------------------
```

---

## 示例对话

**用户**: 搜索万科最近 7 天的负面新闻，按热度排序

**执行命令**:
```bash
python scripts/query_company_information.py \
    --company "万科" \
    --sentiments 负面 \
    --days 7 \
    --sort-by heat_scores
```

---

## 注意事项

1. **时间参数**: 使用 Unix 时间戳（毫秒），脚本会自动计算
2. **页码**: 从 0 开始计数
3. **情感倾向**: 正面、负面、中性，不传表示全部
4. **公司名称**: 公司名称和关键词至少填写一个
5. **API Key**: 必须提供，支持三种配置方式
6. **输出文件**: 默认生成 CSV 和 MD 文件，可使用 `--no-output` 禁用

---

## 接口信息

- **接口地址**: `221.6.15.90:18011`
- **接口 URI**: `/data-service/v1/news/company/external/query`
- **请求方式**: `POST`
- **Content-Type**: `application/json; charset=UTF-8`

---

**数据来源**: FEEDAX 企业舆情监测平台  
**数据范围**: 新闻、微信公众号、微博等多种信源

---

*最后更新：2026-04-02*
