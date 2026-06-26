# 债券资讯 (Bond Information)

基于 FEEDAX API 的债券资讯与信用风险监测技能，提供全面的债券舆情查询能力。

## 📊 功能概述

支持查询债券市场相关新闻资讯，包括：
- **违约风险**: 债券违约、信用风险、评级下调
- **城投债**: 城投公司舆情、区域分化、债务压力
- **公司债**: 上市公司债券、信用利差、发行人动态
- **债券发行**: 申购、配售、发行利率
- **政策动态**: 监管政策、货币政策、财政政策

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
bond-information/
├── SKILL.md                          # 技能说明文档
├── README.md                         # 本文件
└── scripts/
    ├── query_bond_information.py     # 查询脚本
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
python scripts/query_bond_information.py --api-key "your-api-key" --keyword "城投债"
```

**方式 2: 环境变量**
```bash
export FEEDAX_API_KEY="your-api-key"
python scripts/query_bond_information.py --keyword "城投债"
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
# 查询负面债券资讯
python scripts/query_bond_information.py --keyword "违约" --sentiments 负面 --days 7

# 查询特定债券
python scripts/query_bond_information.py --keyword "20 万科 01" --days 14

# 查询城投债
python scripts/query_bond_information.py --keyword "城投债" --sentiments 负面 --days 30

# 按热度排序
python scripts/query_bond_information.py --keyword "公司债" --sort-by heat_scores
```

---

## 参数说明

### 必填参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--keyword` | `-k` | 搜索关键词（债券名称/类型/发行人） |

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

- **文件名**: `bond_information_<时间戳>.csv`
- **字段**: 发布时间、标题、摘要、内容、来源、债券名称、债券类型、发行人、重要程度、热度得分、浏览数、转发数、URL

### MD 说明文件

- **文件名**: `bond_information_<时间戳>.md`
- **内容**: 查询统计、债券类型分布、情感分布、重要程度分布、债券标签等

---

## 数据字段说明

| 字段 | 说明 |
|------|------|
| `title` | 新闻标题 |
| `content` | 新闻正文 |
| `summary` | 摘要 |
| `source` | 新闻来源 |
| `url` | 原文链接 |
| `publishDate` | 发布时间（13 位时间戳） |
| `sentiment` | 情感倾向（正面/负面/中性） |
| `newsImportanceLevel` | 重要程度（高/中/低） |
| `heatScores` | 资讯热度得分 |
| `viewNum` | 浏览数 |
| `forwardedNum` | 转发数 |
| `sseBondResults` | 债券信息列表 |

### 债券信息 (sseBondResults)

| 字段 | 说明 |
|------|------|
| `bondName` | 债券名称 |
| `bondType` | 债券类型 |
| `bondIssuer` | 发行人名称 |
| `companySentimentScore` | 情感得分（>0 正面，=0 中性，<0 负面） |
| `relevance` | 新闻与债券的相关性 |
| `importantArea` | 重要区域（产业/绿色/创新/城投等） |

---

## 债券类型分类

| 债券类型 | 说明 |
|---------|------|
| **国债** | 中央政府发行的债券 |
| **地方政府债** | 地方政府发行的债券 |
| **政策性金融债** | 政策性银行发行的金融债券 |
| **企业债** | 企业发行的债券 |
| **公司债** | 上市公司发行的债券 |
| **中期票据** | 银行间市场发行的中期债务工具 |
| **短期融资券** | 短期债务融资工具 |
| **ABS** | 资产支持证券 |
| **可转债** | 可转换公司债券 |
| **REIT** | 不动产投资信托基金 |
| **城投债** | 城投公司发行的债券 |

---

## 常见债券标签

- **风险类**: 违约风险、信用评级下调、负面舆情
- **评级类**: 信用评级、评级调整、评级展望
- **发行类**: 债券发行、申购、配售
- **交易类**: 债券交易、收益率、利差
- **政策类**: 监管政策、货币政策、财政政策
- **行业类**: 城投、房地产、金融、产业债

---

## 示例输出

```
共找到 20 条资讯:

================================================================================
1. [2026-04-02 14:30] 🔴 负面
   标题：城投债信用利差走阔，关注区域分化风险
   来源：新浪财经 | 热度：85.3
   债券名称：20 万科 01
   债券类型：公司债
   发行人：万科企业股份有限公司
   重要程度：高
--------------------------------------------------------------------------------
```

---

## 示例对话

**用户**: 搜索最近 7 天城投债的负面新闻，按热度排序

**执行命令**:
```bash
python scripts/query_bond_information.py \
    --keyword "城投债" \
    --sentiments 负面 \
    --days 7 \
    --sort-by heat_scores
```

---

## 注意事项

1. **时间参数**: 使用 Unix 时间戳（毫秒），脚本会自动计算
2. **页码**: 从 0 开始计数
3. **情感倾向**: 正面、负面、中性，不传表示全部
4. **债券类型**: 支持 11 种债券类型筛选
5. **API Key**: 必须提供，支持三种配置方式
6. **输出文件**: 默认生成 CSV 和 MD 文件，可使用 `--no-output` 禁用

---

## 接口信息

- **接口地址**: `221.6.15.90:18011`
- **接口 URI**: `/data-service/v1/news/bond/external/query`
- **请求方式**: `POST`
- **Content-Type**: `application/json; charset=UTF-8`

---

**数据来源**: FEEDAX 债券资讯监测平台  
**数据范围**: 新闻、微信公众号、微博等多种信源

---

*最后更新：2026-04-02*
