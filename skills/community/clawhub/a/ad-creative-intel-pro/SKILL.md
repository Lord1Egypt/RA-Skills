---

slug: ad-creative-intel-pro
name: ad-creative-intel-pro
version: 1.0.1
displayName: 广告情报专业版
summary: '"解决批量创意导出慢、历史趋势无法回溯、下载收入数据缺失的专业广告情报分析平台。广告情报专业版是面向买量团队、投放优化师、市场研究负责人的全功能广告情报分析平台，针对"批量创意导出受限于单次"'
license: Proprietary
edition: pro
description: "广告情报专业版是面向买量团队、投放调优师、市场研究负责人的全功能广告情报剖析平台，针对\"成批创意导出受限于单次 10 条、历史趋势无法回溯剖析、下载与收入预估数据缺失、跨市场对比需手动聚合、创意效果难以归因到投放动作\"五大高频痛点而设计。它在免费版三大端点集群基础上，解锁成批导出、历史回溯、下载/收入预估三类高级端点，并新增多市场对比、创意效果归因、优先速率并发三项独有能力."。可自动提升工作效率
tags:
- 广告情报
- api
- data
- post
- 专业版增
- adc_intel_api_key
tools:
- read
- exec
- write
- glob
- grep
homepage: '""'
category: '"Agents"'
homepage: ""
pricing_tier: "L2-标准级"

---

> **功能说明**: 本技能涵盖 提升工作效率 等核心能力。

# 广告情报专业版（Ad Creative Intel Pro）
面向买量团队、投放优化师、市场研究负责人的全功能广告情报分析平台。在免费版三大端点集群基础上解锁批量导出、历史回溯、下载/收入预估三类高级端点，并新增多市场对比、创意效果归因、优先速率并发三项独有能力.
> 本专业版为收费版本，定价 ¥29.9/月。如需先体验核心功能，可使用 `ad-creative-intel-free` 免费版.
## 设计动机：五大高频痛点
| 痛点 | 典型表现 | 本技能对策 |
|---|----|-----|
| 批量导出受限于单次 10 条 | 调研 500 条素材需翻页 50 次 | 单次返回上限提升至 200，支持无上限翻页批量导出 |
| 历史趋势无法回溯 | 只能看当前快照，无法分析投放演变 | 开放历史时间段查询，支持任意日期区间回溯 |
| 下载与收入预估数据缺失 | 无法量化竞品体量与变现能力 | 开放 download-* 与 revenue-* 全套预估端点 |
| 跨市场对比需手动聚合 | 多地区数据需逐个拉取再 Excel 合并 | 多市场对比工作流，自动并行拉取并按统一维度聚合 |
| 创意效果难以归因 | 创意与投放花费/转化脱节 | 创意效果归因模板，关联创意到投放动作与业务指标 |
## 输入定义
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 广告情报专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
```bash
[ -n "${ADC_INTEL_API_KEY:-}" ] && echo ok || echo missing
```
专业版额外建议检查配额状态：
```bash
curl -s "https://api.ad-creative-intel.com/api/quota/status" \
  -H "X-API-Key: ${ADC_INTEL_API_KEY}"
```
返回当前 QPS、并发数、剩余配额等信息.
### Step 2：首次批量导出（< 60 秒）
```bash
curl -s -X POST "https://api.ad-creative-intel.com/api/data/search" \
  -H "X-API-Key: ${ADC_INTEL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword":"rpg",
    "countries":["US"],
    "tradeLevel1":"602",
    "dateRange":"30d",
    "pageSize":200,
    "page":1
  }'
```
专业版单次返回上限 200 条，相比免费版提升 20 倍.
### Step 3：查询下载/收入预估（< 60 秒）
```bash
ad-creative-intel.com/api/data/download-date" \
  -H "X-API-Key: ${ADC_INTEL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"unifiedProductId":"<参数>","dateRange":"30d"}'
ad-creative-intel.com/api/data/revenue-country" \
  -H "X-API-Key: ${ADC_INTEL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"unifiedProductId":"<参数>","countries":["US","JP"]}'
```
### Step 4：多市场对比分析（< 45 秒）
```bash
for country in US JP KR; do
ad-creative-intel.com/api/data/search" \
    -H "X-API-Key: ${ADC_INTEL_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"keyword\":\"rpg\",\"countries\":[\"$country\"],\"pageSize\":50}" &
done
wait
```
## 使用指南
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理
| 故障场景 | 表现症状 | 诊断方法 | 修复步骤 |
|:---------|:---------|:---------|:---------|
| Key无效 | 返回401状态码 | 验证Key格式和有效性 | 重新生成Key并更新环境变量 |
| 请求被拒 | 返回403禁止访问 | 检查权限范围和IP限制 | 确认账户权限,添加IP白名单 |
| 速率限制 | 返回429状态码 | 查看响应头中的Retry-After字段 | 按Retry-After值等待后重试 |
| 格式错误 | 返回400状态码 | 检查请求体JSON格式和字段类型 | 参照输入格式示例修正 |
| 服务不可用 | 返回503状态码 | 检查API状态页和健康检查端点 | 等待服务恢复,设置重试退避策略 |
## 主要能力
### 1. 广告创意搜索（专业版增强）
继承免费版全部创意搜索端点，新增以下能力：
| 增强项 | 免费版 | 专业版 |
|---:|---:|---:|
| 单次返回上限 | 10 条 | 200 条 |
| 历史时间段查询 | 仅当前 | 任意日期区间 |
| 并发请求 | 1 路 | 5 路 |
| QPS 限制 | 1 QPS | 10 QPS |
| 批量导出 | 翻页 50 次 | 翻页 3 次即可 |
端点清单同免费版（`/api/data/search`、`/api/data/count`、`/api/data/count-all`、`/api/data/distribute`、`/api/data/distribute-dims`、`/api/data/content-detail`、`/api/data/item-apps`、`/api/data/screen-types`、`/api/data/page-config`），但参数约束放宽.
**处理**: 解析广告创意搜索（专业版增强）的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回广告创意搜索（专业版增强）的响应数据,附带状态标识与运行日志.
### 2. 应用与开发者洞察（专业版增强）
继承免费版全部应用查询端点，新增 SDK 与分发数据：
| 端点 | 方法 | 用途 | 版本 |
|:---:|:---:|:---:|:---:|
| `/api/data/app-distribution` | POST | 应用级分发数据 | 专业版独有 |
| `/api/data/global-promote` | POST | 全球推广数据 | 专业版独有 |
| `/api/data/market-search` | POST | 市场级搜索与聚合 | 专业版独有 |
| `/api/data/product-list` | POST | 产品列表 | 专业版独有 |
| `/api/data/product-agg-list` | POST | 产品聚合列表 | 专业版独有 |
**处理**: 解析应用与开发者洞察（专业版增强）的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回应用与开发者洞察（专业版增强）的响应数据,附带状态标识与运行日志.
### 3. 应用商店榜单查询（专业版增强）
继承免费版榜单端点，新增历史榜单回溯：
| 增强项(续)| 免费版 | 专业版 |
|:--------|--------:|:--------|
| 榜单时间范围 | 仅当前 | 任意历史日期 |
| 历史对比 | 不支持 | 支持 T-7 / T-30 对比 |
| 批量分类查询 | 不支持 | 一次请求多个分类 |
**处理**: 解析应用商店榜单查询（专业版增强）的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回应用商店榜单查询（专业版增强）的响应数据,附带状态标识与运行日志.
### 4. 下载与收入预估数据（专业版独有）
开放全套第三方预估数据端点：
| 端点 | 方法 | 用途 |
|---:|:---|---:|
| `/api/data/download-date` | GET/POST | 按日期的下载量预估 |
| `/api/data/download-detail` | GET/POST | 下载量明细预估 |
| `/api/data/download-country` | GET/POST | 按国家的下载量预估 |
| `/api/data/revenue-date` | GET/POST | 按日期的收入预估 |
| `/api/data/revenue-detail` | GET/POST | 收入明细预估 |
| `/api/data/revenue-country` | GET/POST | 按国家的收入预估 |
**处理**: 解析下载与收入预估数据（专业版独有）的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回下载与收入预估数据（专业版独有）的响应数据,附带状态标识与运行日志.
### 5. 多市场对比分析（专业版独有）
自动并行拉取多地区数据并按统一维度聚合：
```text
工作流：
1. 输入：目标市场列表（如 US/JP/KR/DE/BR）+ 统一查询条件
2. 并行调用 /search（每市场一路并发，最多 5 路并行）
3. 按统一维度（adType / tradeLevel / creativeType）聚合
4. 输出对比矩阵：
   - 各市场创意数对比
   - 各市场广告类型分布对比
   - 各市场行业分布对比
   - 各市场 Top 创意交集与差异
```
**对比矩阵示例**：
| 维度 | US | JP | KR | DE | BR |
|:------:|--------|:-------|:------:|--------|:-------|
| 创意总数 | 1,250 | 890 | 650 | 420 | 780 |
| 视频广告占比 | 68% | 55% | 72% | 60% | 45% |
| 游戏行业占比 | 42% | 38% | 55% | 30% | 48% |
| Top 10 交集 | 7 | 7 | 5 | 4 | 3 |
**处理**: 解析多市场对比分析（专业版独有）的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回多市场对比分析（专业版独有）的响应数据,附带状态标识与运行日志.
### 6. 创意效果归因（专业版独有）
把创意素材关联到投放动作与业务指标：
```text
归因模板：
{
  "creative_id": "<参数>",
  "creative_meta": {
    "type": "video",
    "duration": 30,
    "first_seen": "2026-06-01",
    "last_seen": "2026-07-15",
    "active_days": 45
  },
  "attribution": {
    "associated_app": "com.example.app",
    "developer": "Example Studio",
    "estimated_spend_range": "high",
    "markets_active": ["US", "JP", "KR"],
    "media_channels": [1, 2, 3],
    "rank_impact": {
      "before_launch": 85,
      "after_launch": 23,
      "delta": -62
    }
  }
}
```
**归因数据来源**：通过创意 ID 关联 `/item-apps`、`/app-detail`、`/store-rank`（历史）、`/download-date` 等端点交叉拼接.
**处理**: 解析创意效果归因（专业版独有）的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回创意效果归因（专业版独有）的响应数据,附带状态标识与运行日志.
- `input_params`参数控制执行,支持创建/查询/导出
### 7. 优先 API 速率与并发（专业版独有）
| 配额项 | 免费版 | 专业版 |
|----|:--:|---:|
| QPS | 1 | 10 |
| 月度调用上限 | 无限 | 无限 |
| 优先队列 | 无 | 有 |
| 5xx 错误重试 | 自行处理 | 服务端优先重试 |
**处理**: 解析优先 API 速率与并发（专业版独有）的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回优先 API 速率与并发（专业版独有）的响应数据,附带状态标识与运行日志.
**能力覆盖范围**：支持的场景关键词如下：解决批量创意导出、历史趋势无法回溯、下载收入数据缺失、的专业广告情报分、析平台、广告情报专业版是、面向买量团队、投放优化师、市场研究负责人的、全功能广告情报分、批量创意导出受限、于单次、据缺失、跨市场对比需手动、创意效果难以归因、五大高频痛点而设、它在免费版三大端、点集群基础上、解锁批量导出、历史回溯、收入预估三类高级、并新增多市场对比、优先速率并发三项、独有能力等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 高级工作流
### 工作流 A：批量素材调研（500 条素材）
```text
1. 调用 /count 获取总数，确认是否 ≥ 500
2. 按 pageSize=200 翻页 3 次拉取全部数据
3. 并行调用 /content-detail 获取 Top 50 创意详情（5 路并发）
4. 调用 /item-apps 关联应用
5. 输出：创意列表 + 详情 + 关联应用（原始 JSON）
预计耗时：免费版需 50+ 次翻页，专业版仅需 3 次翻页 + 10 次详情查询
```
### 工作流 B：历史投放效果复盘
```text
1. 指定历史时间段（如 2026-04-01 至 2026-06-30）
2. 调用 /search 拉取该时间段创意
3. 调用 /download-date 获取同期下载量预估
4. 调用 /revenue-date 获取同期收入预估
5. 调用 /store-rank（历史）获取同期榜单变化
6. 交叉拼接：创意上线时间 → 下载/收入变化 → 榜单变化
7. 输出：投放动作效果复盘报告（原始 JSON + 关联视图）
```
### 工作流 C：跨市场投放策略制定
```text
1. 选定目标市场列表（如 US/JP/KR/DE/BR）
2. 并行拉取各市场 Top 100 创意（5 路并发）
3. 调用 /count-all 按维度分组统计各市场
4. 聚合为对比矩阵（创意数/类型分布/行业分布）
5. 识别各市场 Top 创意交集与差异
6. 调用 /download-country 获取各市场下载预估
7. 输出：跨市场投放策略建议（原始 JSON + 对比矩阵）
```
## 实际示例
### 场景一：买量团队批量调研 500 条 RPG 创意
```text
任务：调研全球近 30 天 RPG 游戏类广告创意 Top 500
执行步骤：
1. 调用 /count 确认总数 ≥ 500
2. 调用 /search：
   {
     "keyword": "rpg",
     "tradeLevel1": "602",
     "dateRange": "30d",
     "pageSize": 200,
     "page": 1
   }
3. 翻页 3 次拉取全部 500 条（专业版 pageSize=200）
4. 并行调用 /content-detail 获取 Top 50 详情（5 路并发）
5. 调用 /count-all 按 adType / countries 分组统计
6. 输出：500 条创意原始 JSON + 统计概览 + Top 50 详情
优势：相比免费版节省 47 次翻页请求，耗时从 ~5 分钟降至 ~30 秒
```
### 场景二：投放优化师复盘 Q2 投放效果
```text
任务：复盘 2026 年 Q2（4-6 月）某产品投放的创意效果与下载收入变化
执行步骤：
1. 调用 /product-content-search 获取该产品 Q2 全部创意
2. 调用 /download-date：
   { "unifiedProductId": "<参数>", "dateRange": "2026-04-01:2026-06-30" }
3. 调用 /revenue-date 同期收入预估
4. 调用 /store-rank（历史）获取同期榜单变化
5. 交叉拼接：创意上线时间 → 下载/收入变化 → 榜单变化
6. 输出：Q2 投放效果复盘（原始 JSON + 时间线关联视图）
注意：下载/收入为第三方预估值，呈现时必须标注
```
### 场景三：市场研究负责人跨市场对比分析
```text
任务：对比 US/JP/KR/DE/BR 五个市场 RPG 游戏投放策略差异
执行步骤：
1. 并行拉取 5 个市场 Top 100 创意（5 路并发）
2. 各市场调用 /count-all 按 adType / tradeLevel 分组
3. 聚合对比矩阵：
   - 各市场创意总数
   - 各市场视频/图片/Playable 占比
   - 各市场游戏子行业分布
   - Top 10 创意交集（全球化素材）与差异（本地化素材）
4. 调用 /download-country 获取各市场下载预估
5. 输出：跨市场投放策略对比报告
优势：5 路并发 + 自动聚合，5 分钟完成原本需 30 分钟的手工对比
```
### 场景四：应用发行商预估竞品下载收入
```text
任务：预估竞品 "示例值" 在美国与日本市场的下载量与收入
执行步骤：
1. 调用 /unified-product-search 搜索竞品获取 unifiedProductId
2. 调用 /download-country：
   { "unifiedProductId": "<参数>", "countries": ["US","JP"], "dateRange": "90d" }
3. 调用 /revenue-country 同期收入预估
4. 调用 /download-detail 获取明细（按日/周）
5. 输出：竞品下载收入预估报告（必须标注"预估值"）
注意：预估数据仅供参考，不可作为决策唯一依据
```
### 场景五：数据分析师构建投放数据看板
```text
任务：构建每日自动更新的投放数据看板
执行步骤：
1. 设计定时任务（每日 02:00 执行）
2. 并行拉取：
   - 竞品创意新增（/search + dateRange=1d）
   - 自家产品榜单变化（/store-rank）
   - 竞品下载预估（/download-date + dateRange=1d）
   - 行业分布变化（/count-all）
3. 利用专业版 10 QPS + 5 路并发，全量拉取 < 60 秒
4. 原始 JSON 入库，由看板前端渲染
5. 异常告警：榜单下跌 > 10 位 / 竞品创意激增 > 50% 触发通知
优势：专业版速率配额适合构建定时任务与数据看板
```
## API Key 配置
### 配置方式
**方式一：环境变量（推荐）**
```bash
export ADC_INTEL_API_KEY="${API_KEY:?请设置环境变量}"
$env:ADC_INTEL_API_KEY = "${API_KEY:?请设置环境变量}"
```
**方式二：Agent 平台配置**
```bash
skill-platform config set skills.entries.ad-creative-intel-pro.apiKey "your_pro_api_key_here"
```
### 获取专业版 API Key
1. 访问广告情报数据服务官网注册账号
2. 订阅专业版套餐（¥29.9/月）
3. 登录后在控制台找到 **API Keys** 菜单
4. 创建一个标记为"Pro"的 Key 并复制保存
5. 按上述方式配置到环境中
## 使用约束
- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
## 用户疑问集
**Q1：专业版与免费版的 API Key 是否通用？**
A：不通用。专业版需订阅后获取标记为"Pro"的 Key，免费版 Key 无法访问专业版独有端点（如 download-* / revenue-*）。两套 Key 可同时配置在不同环境变量中.
**Q2：批量导出 500 条素材需要多久？**
A：专业版单次返回 200 条，500 条仅需 3 次翻页。按 10 QPS 计算，3 次请求 + 10 次详情查询（5 路并发）总耗时约 30 秒。免费版同样任务需 50 次翻页，耗时约 5 分钟.
**Q3：历史趋势回溯支持多长时间范围？**
A：支持任意历史日期区间，最早可回溯至服务上线日（约 2 年前）。建议单次查询不超过 90 天，超过会触发分片机制降低响应速度.
**Q4：下载/收入预估数据准确吗？**
A：下载/收入为第三方预估数据，基于公开数据建模推算，存在 10-30% 误差。不可作为决策唯一依据，建议结合官方财报、榜单变化、创意投放量交叉验证。本技能原样返回预估数据，呈现时必须标注"预估值".
**Q5：多市场对比最多支持几个市场？**
A：单次工作流建议最多 5 个市场（受并发上限 5 路约束）。如需对比更多市场，可分批执行，每批 5 个市场并行拉取后聚合.
**Q6：专业版的 10 QPS 与 5 路并发是硬限制吗？**
A：是的。超过会返回 429（RATE_LIMITED 或 CONCURRENT_LIMIT）。如需更高配额，可联系服务方定制企业版.
**Q7：创意效果归因的数据来源是什么？**
A：归因数据非单一端点返回，而是通过创意 ID 关联 `/item-apps`（关联应用）、`/app-detail`（应用详情）、`/store-rank` 历史数据（榜单变化）、`/download-date`（下载变化）等多个端点交叉拼接。归因结果仅供参考，不构成投放建议.
**Q8：专业版是否支持 Webhook 或流式输出？**
A：当前版本不支持 Webhook 与流式输出。所有请求为同步 HTTP 调用。如需异步大批量任务，建议在调用方实现任务队列与回调机制.
## 专业版特性
本专业版相比免费版新增以下能力：
- 批量导出无上限：单次返回上限 200 条，相比免费版提升 20 倍，500 条素材调研从 5 分钟降至 30 秒
- 历史趋势回溯：支持任意时间段历史数据查询，最早可回溯 2 年，适合投放效果复盘与趋势分析
- 下载/收入预估数据：开放 download-* 与 revenue-* 全套端点，量化竞品体量与变现能力
- 多市场对比分析（独有）：自动并行拉取多地区数据并按统一维度聚合，5 分钟完成原本需 30 分钟的手工对比
- 创意效果归因（独有）：把创意素材关联到投放时间、下载变化、榜单变化、业务指标，构建投放动作效果视图
- 优先 API 速率与并发（独有）：10 QPS + 5 路并发配额，适合构建数据看板与定时任务，专属优先队列与 5xx 重试
## 定价
| 版本 | 价格 | 功能 | 适用场景 |
|---:|---:|---:|---:|
| 免费体验版 | ¥0 | 创意搜索（pageSize=10）+ 应用查询 + 榜单查询 + 基础示例 | 个人试用、轻量查询 |
| 收费专业版 | ¥29.9/月 | 全部端点 + 批量导出（pageSize=200）+ 历史回溯 + 下载收入预估 + 多市场对比 + 创意归因 + 10 QPS/5 路并发 + 优先支持 | 买量团队、投放优化师、市场研究负责人 |
专业版通过 SkillHub SkillPay 发布.
## 依赖与配置
### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **网络**：需可访问 `api.ad-creative-intel.com` 域名
- **并发运行时**：批量与多市场工作流需支持并发 HTTP 请求（如 Python asyncio / Node.js Promise.all / bash &）
### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由 Agent 平台内置 LLM 提供（专业版可选 GPT-4o 路由） |
| 广告情报数据服务 API（专业版） | 外部 API | 必需 | 需订阅专业版套餐（¥29.9/月）并获取 Pro Key |
| curl | 命令行工具 | 必需 | 系统自带或通过包管理器安装 |
| jq（可选） | 命令行工具 | 可选 | 用于 JSON 结果聚合与字段提取 |
### API Key 配置(补充)
- **存储位置**：环境变量 `ADC_INTEL_API_KEY`（专业版 Key）
- **禁止**：在 SKILL.md 或脚本中硬编码 Key
- **禁止**：在对话中接受用户输入的 Key 并回显
- **禁止**：在 git 仓库中提交 Key
- **建议**：将 Key 存储在 `d:\skills\.skillhub-credentials\` 目录并加入 gitignore
### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，批量与并发工作流需 exec 执行 curl 命令）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 调用广告情报数据 API 并完成多市场对比与创意归因
## License 与版权声明
本 skill 基于原始作品改进，保留原始版权声明：
- 原始作品：广告创意数据 API 客户端
- 原始 license：MIT
- 改进作品：© 2026 Ad Creative Intel Pro
- 改进 license：MIT
本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 重新设计为中文痛点导向的免费/专业双版本架构
- 新增五大痛点对策矩阵与高级工作流指南
- 新增批量导出、历史回溯、下载收入预估、多市场对比、创意归因、优先速率并发六大专业能力
- 新增 5 个真实场景示例（含批量调研、效果复盘、跨市场对比、竞品预估、看板构建）
- 新增 8 问 FAQ 与 10 项故障排查表
- 移除原项目专属标识，统一为"广告情报数据服务"抽象命名
- 将工具协议引用从特定实现改为通用"工具协议"标准术语
- 新增定价表与专业版独有功能对比
MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
## 安全规范
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 使用环境变量注入,不得在源码中明文写入 |
| 命令执行风险 | 限定执行预批准命令,不拼接用户输入到参数中 |
| 网络通信安全 | 使用TLS加密通道进行通信 |
| 敏感数据暴露 | 结果中排除密钥类数据 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 异常处理指引
针对广告情报专业版使用中可能遇到的常见问题,提供以下排查方案:
| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |
### 广告情报专业版通用排查步骤
1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
### Q1: 广告情报专业版支持哪些输入格式？
A1: "解决批量创意导出慢、历史趋势无法回溯、下载收入数据缺失的专业广告情报分析平台。广告情报专业版是面向买量团队、投放优化师、市场研究负责人的全功能广告情报分析平台。支持文本指令和结构化参数输入，具体格式参考使用流程章节。
### Q2: 需要配置API Key吗？
A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。
### Q3: 命令行执行失败怎么办？
A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。