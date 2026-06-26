---
name: mx-skills-suite
description: >
  东方财富妙想金融技能套件（mx-skills-suite），包含 5 个专业金融子技能：
  1. eastmoney_fin_data - 金融数据查询（行情、财务、关联关系）
  2. eastmoney_fin_search - 金融资讯搜索（新闻、公告、研报、政策）
  3. mx_select_stock - 智能选股（条件筛选、板块查询、股票推荐）
  4. mx_self_select - 自选股管理（查询、添加、删除自选股）
  5. eastmoney_stock_simulator - 模拟组合管理（持仓、买卖、撤单、委托、资金）
  触发词：东方财富、妙想、金融数据、行情查询、股票资讯、选股、自选股、模拟交易、模拟炒股、持仓查询、东方财富数据、东方财富API。
author: Community (based on 东方财富妙想团队 original work)
version: 2.0.0
required_env_vars:
  - MX_APIKEY
credentials:
  - type: api_key
    name: MX_APIKEY
    description: 从东方财富妙想平台获取的 API Key，首次使用需注册获取
    setup_url: "https://marketing.dfcfs.com/views/mktemplate/route1?activityId=738&appfenxiang=1"
---

# mx-skills-suite - 东方财富妙想金融技能套件

本技能套件基于**东方财富妙想平台 API**构建，提供一站式金融数据查询、资讯搜索、智能选股、自选股管理和模拟交易功能。所有子技能通过统一的 `MX_APIKEY` 认证，支持自然语言交互。

## 包含的子技能

| # | 技能名称 | 功能说明 | 详细文档 |
|---|---------|---------|---------|
| 1 | **eastmoney_fin_data** | 金融数据查询：股票/行业/板块/指数/基金/债券的实时行情、主力资金、估值、财务指标、股东结构等 | `references/mx-data.md` |
| 2 | **eastmoney_fin_search** | 金融资讯搜索：新闻、公告、研报、政策、交易规则、事件分析等时效性信息 | `references/mx-search.md` |
| 3 | **mx_select_stock** | 智能选股：基于行情/财务指标条件筛选股票、板块成分股查询、股票推荐 | `references/mx-select-stock.md` |
| 4 | **mx_self_select** | 自选股管理：查询/添加/删除东方财富通行证账户下的自选股 | `references/mx-selfselect.md` |
| 5 | **eastmoney_stock_simulator** | 模拟组合管理：持仓查询、买卖操作、撤单、委托查询、资金查询 | `references/mx-stock-simulator.md` |

## 首次使用 - 获取 API Key

**所有子技能都需要 `MX_APIKEY` 环境变量才能使用。** 如果用户尚未配置，按以下步骤引导：

### 步骤 1：获取 API Key

打开东方财富妙想平台注册页面：
**https://marketing.dfcfs.com/views/mktemplate/route1?activityId=738&appfenxiang=1**

### 步骤 2：下载并安装东方财富 APP

### 步骤 3：领取 API Key

注册/登录后，在首页搜索 **Skill**，领取 **API KEY**

### 步骤 4：配置环境变量

获取到 API Key 后，直接复制指引文字，或手动设置环境变量：

```bash
# Linux / macOS
export MX_APIKEY=你的API_KEY

# Windows PowerShell
$env:MX_APIKEY = "你的API_KEY"

# Windows CMD
set MX_APIKEY=你的API_KEY
```

### 验证配置

配置完成后，尝试调用任意子技能接口验证 Key 是否有效。如果返回 `114` 或 `116` 错误码，说明 Key 无效，需要重新获取。

## 使用方式

根据用户请求自动匹配对应子技能，按需加载 `references/` 下的详细文档：

- **查行情/财务数据** → 加载 `references/mx-data.md`，调用金融数据查询接口
- **搜新闻/研报/公告** → 加载 `references/mx-search.md`，调用资讯搜索接口
- **筛选股票/选股** → 加载 `references/mx-select-stock.md`，调用智能选股接口
- **管理自选股** → 加载 `references/mx-selfselect.md`，调用自选股管理接口
- **模拟交易/查持仓** → 加载 `references/mx-stock-simulator.md`，调用模拟组合接口

## API 基础信息

- **API 域名**: `https://mkapi2.dfcfs.com/finskillshub`
- **认证方式**: HTTP Header `apikey: {MX_APIKEY}`
- **请求方法**: 所有接口均使用 `POST`
- **Content-Type**: `application/json`

## 错误码说明

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 113 | 调用次数达上限 | 提示用户等待或更新 API Key |
| 114 | API 密钥失效 | 提示用户重新获取 Key |
| 115 | 未携带密钥 | 提示用户配置 `MX_APIKEY` |
| 116 | 密钥不存在 | 提示用户检查 Key 是否正确 |
| 404 | 未绑定模拟组合 | 提示用户先在妙想页面创建模拟账户 |

## 安全说明

- 数据仅发送至东方财富官方 API 域名 `mkapi2.dfcfs.com`
- API Key 通过环境变量 `MX_APIKEY` 在服务端使用，不会在前端明文暴露
- 模拟交易功能仅用于学习练手，不涉及真实资金
