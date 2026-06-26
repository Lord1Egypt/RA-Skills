---
name: china-company-search-wendaoyun
description: 问道云企业信息查询工具，支持通过问道云 API 查询企业基本信息、经营信息、财务信息、舆情信息、企业各类风险指标等功能，当用户需要查询企业相关信息时触发。
---

# 问道云 (WenDaoYun) 企业信息查询


## 核心流程

**所有接口调用前**，请先阅读下方 [API 请求组装](#API请求组装) 章节，了解 Base URL、认证方式和 URL 拼接规则。

所有查询必须按以下顺序执行：

**第 1 步：搜索企业**
1. 检查环境变量 `WENDAOYUN_API_KEY` 是否有值
   - **无值** → 返回下方 [配置说明](#配置说明) 章节的完整内容，引导用户配置 API Key，**停止后续所有操作**
   - **有值** → 继续执行步骤 2

2. 调用 `fuzzy-search-org` 搜索企业
   - 入参：`searchKey` = 用户提供的企业名称或关键词
   - 展示前 5 条结果（企业ID、企业全称、法定代表人、成立日期、状态）
   - 如果总数超过 5 条，提示用户"查下一页或指定页码"

**第 2 步：用户确认（必须等待，不可跳过！）**
- 必须等待用户选择具体企业（通过序号或名称）
- 未确认前，**禁止**调用任何详细信息接口

**第 3 步：查询对应接口**
- 用户确认后，根据用户意图从「接口路由表」中找到对应接口
- 参数详情查阅 `references/` 目录下对应的接口文件


## 配置说明

1. 获取 API KEY：访问 https://open.wintaocloud.com/home → 【个人中心-ApiKey】
2. 设置环境变量：`export WENDAOYUN_API_KEY=你的API KEY`
3. 每日调用额度：200 次

> ⚠️ API KEY 属于敏感信息，请妥善保管。发现泄露请在问道云开放平台及时作废。


## API请求组装

- **Base URL**: `https://h5.wintaocloud.com/prod-api/api/invoke`
- **认证**: Header `Authorization: Bearer {WENDAOYUN_API_KEY}`
- **请求方式**: GET
- **URL 拼接**: `Base URL + / + 接口名称 + ? + 参数`
  - 示例：`https://h5.wintaocloud.com/prod-api/api/invoke/fuzzy-search-org?searchKey=腾讯&pageNum=1&pageSize=5`


## 通用规则

- **⚠️ API 调用错误处理（所有接口通用）**：
  - 任何接口调用返回的错误信息中，如果包含 `apiKey`关键词 → **立即停止所有操作**，将错误信息原文返回给用户，并引导用户重新获取 API KEY（参考上方[配置说明](#配置说明) 章节）
- **⚠️ 接口入参规则**：
  - 入参为 `searchKey`：取 `fuzzy-search-org` 搜索结果中的 `orgName`（企业全称）
  - 入参为 `orgId`：取 `fuzzy-search-org` 搜索结果中的 `orgId`（企业ID）
- ⚠️ 金额字段（`punishAmount`、`executeAmount` 等）单位为**分**，展示时必须 **÷100 换算为元**
- ⚠️ 返回 `null` 时显示"未知"
- ⚠️ `code=200` 但数据为空时，展示"暂无数据"，而非直接显示原始返回
- 📖 所有接口的详细参数和响应字段，请查阅 `references/` 目录下对应的接口文件


## 接口路由表

| 用户意图 | 接口名称 | 详细文档 |
|---------|---------|---------|
| 搜索/查询企业 | `fuzzy-search-org` | `references/fuzzy-search-org.md` |
| 行政处罚 | `get-punishments` | `references/get-punishments.md` |
| 经营异常 | `get-abnormal` | `references/get-abnormal.md` |
| 股权质押 | `get-equity-pledge` | `references/get-equity-pledge.md` |
| 环保处罚 | `get-environmental-penalties` | `references/get-environmental-penalties.md` |
| 欠税公告 | `get-tax-notice` | `references/get-tax-notice.md` |
| 简易注销 | `get-simple-cancel` | `references/get-simple-cancel.md` |
| 土地抵押 | `get-land-mortgage` | `references/get-land-mortgage.md` |
| 公示催告 | `get-public-inform` | `references/get-public-inform.md` |
| 送达报告（劳动仲裁） | `get-labour-arb` | `references/get-labour-arb.md` |
| 担保信息 | `get-gua-info` | `references/get-gua-info.md` |
| 开庭公告（劳动仲裁） | `get-open-court-arb` | `references/get-open-court-arb.md` |
| 债券信息 | `get-bond-info` | `references/get-bond-info.md` |
| 海关进出口信用 | `get-import-export-credit` | `references/get-import-export-credit.md` |
| 被执行信息 | `get-execute-info` | `references/get-execute-info.md` |
| 失信被执行信息 | `get-dishonest-debtors` | `references/get-dishonest-debtors.md` |
| 股权冻结 | `get-share-blocking` | `references/get-share-blocking.md` |
| 限制高消费 | `get-consumption-limits` | `references/get-consumption-limits.md` |
| 裁判文书 | `get-judge-doc` | `references/get-judge-doc.md` |
| 破产重整 | `get-bankruptcy-regroup` | `references/get-bankruptcy-regroup.md` |
| 司法拍卖 | `get-judicial-sale` | `references/get-judicial-sale.md` |
| 开庭公告 | `get-open-court` | `references/get-open-court.md` |
| 立案信息 | `get-case-filing` | `references/get-case-filing.md` |
| 诉前调解 | `get-pre-mediate` | `references/get-pre-mediate.md` |
| 询价评估 | `get-inq-eval` | `references/get-inq-eval.md` |
| 送达公告 | `get-deliver-notice` | `references/get-deliver-notice.md` |
| 终本案件 | `get-cases-terminated` | `references/get-cases-terminated.md` |
| 限制出境 | `get-exit-ban` | `references/get-exit-ban.md` |
| 法院公告 | `get-judicial-notice` | `references/get-judicial-notice.md` |
| 企业风险信息 | `get-risk` | `references/get-risk.md` |
| 清算信息 | `get-clear-info` | `references/get-clear-info.md` |
| 客户查询信息 | `get-customer` | `references/get-customer.md` |
| 供应商查询 | `get-supplier` | `references/get-supplier.md` |
| 企业招聘信息 | `get-employment-info` | `references/get-employment-info.md` |
| 企业招聘信息详情 | `get-employment-detail` | `references/get-employment-detail.md` |
| 企业风险指数 | `get-risk-index` | `references/get-risk-index.md` |
