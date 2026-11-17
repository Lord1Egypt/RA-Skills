---
name: chukonu-web-search
description: "通过 Chukonu remote MCP 的 search 与 research 获取网页、学术、专利、金融和中国法律法规证据。用于需要外部、实时、可引用信息的搜索任务，以及财经新闻与金融研究、法律法规检索、事实核验、反证检索、PDF 全文深读、覆盖评估或持久化多轮研究；依据结构化 evidence、retrieval_assessment 与 research dossier 作答。"
---

# Chukonu Search + Research

通过 Chukonu remote MCP 调用公开的 `search` 和 `research` 工具。无需本地二进制、API key 或静态 token；不要调用内部工具、上游服务或内部端口。法律法规检索是服务内部接入的 FY MCP provider，客户端不要单独配置它、传入其凭据或尝试调用其工具。

## 一次性接入

使用 `https://search.houdutech.cn/web/mcp/` streamable-http 端点。该端点通过标准 OAuth 2.0 保护，采用动态客户端注册、授权码、PKCE(S256) 和 refresh token，scope 为 `search:read`。让 MCP host 自动发现并注册，不要手工填写 client ID 或 client secret。

OpenClaw：

```bash
openclaw mcp add chukonu-web-search \
  --url https://search.houdutech.cn/web/mcp/ \
  --transport streamable-http \
  --auth oauth
openclaw mcp login chukonu-web-search
```

Claude Code：

```bash
claude mcp add chukonu-web-search https://search.houdutech.cn/web/mcp/ \
  --scope user --transport http
# 然后在会话中：/mcp → chukonu-web-search → Authenticate
```

Codex：

```bash
codex mcp add chukonu-web-search --url https://search.houdutech.cn/web/mcp/
codex mcp login chukonu-web-search
codex mcp list
```

在 Codex TUI 中用 `/mcp` 查看连接状态。若 OAuth 浏览器与 Codex 不在同一主机，先为 Codex 配置可回调的 `mcp_oauth_callback_url`，再登录；不要输出或持久化授权码、回调 URL、access token 或 refresh token。

不要为该服务器配置静态 `Authorization` 头或 `CHUKONU_SEARCH_API_TOKEN`。静态 Authorization 头会使 host 禁用 OAuth 回退，并可能导致 `401 invalid_token`。把 OAuth token 完全交给 host 保管，不要在日志、回答、示例或错误信息中泄露。

## 选择工具与来源

- 用 `search` 处理秒级发现、法规定位和获取后续研究所需的 `research_seed.search_id`。
- 用 `research` 处理关键主张核验、反证、跨来源冲突、全文定位或证据覆盖评估。必须先 `search`，再用返回的 `search_id` 启动任务。
- 本技能使用的 `source_types` 为 `web`、`academic`、`patent`、`legal` 和 `financial`。省略时服务自动路由；财经新闻归入 `financial`，法律意图可在法律 provider 启用时与通用网页并行召回。
- 用 `source_types: ["legal"]` 只检索中国法律法规；用 `source_types: ["legal", "web"]` 同时获取法条和通用网页背景。
- 用 `source_types: ["financial"]` 检索财经新闻和金融文档；宁夏服务已接入 `nws_news` 新闻库，其他金融来源取决于服务端配置。仅查金融时显式指定来源；需要网页原文或背景时用 `["financial", "web"]`。
- 金融问题需要进一步研究时，用 `research` 的 `profile: "financial_research"`；结构化股票数据是否可用要检查返回的 `financial_plan`，不能仅凭 profile 已接受就认定已启用行情查询。
- 对法律问题尽量写明法名和条号，例如 `《中华人民共和国民法典》第1084条`；仅把原始法条证据用于法律效力或条文结论。
- 不要把搜索相关性分数解释为事实置信度，也不要把检索结果或本技能当作法律意见。

## `search`

### 请求

最小调用：

```json
{
  "query": "固态电池硫化物电解质近五年的关键路线"
}
```

只检索现行有效的中国法规：

```json
{
  "query": "《中华人民共和国民法典》第1084条",
  "limit": 10,
  "source_types": ["legal"],
  "filters": {
    "legal_status": "现行有效",
    "jurisdictions": ["CN"]
  }
}
```

混合检索法条和网页解读：

```json
{
  "query": "劳动合同解除的法定情形和近期解读",
  "source_types": ["legal", "web"],
  "filters": {
    "legal_status": "现行有效",
    "languages": ["zh"]
  }
}
```

只检索财经新闻和金融文档：

```json
{
  "query": "贵州茅台 分红",
  "source_types": ["financial"],
  "filters": {
    "published_from": "2026-08-01",
    "published_to": "2026-08-31"
  }
}
```

遵守以下边界：

- `query` 必填；保持简洁、具体。`limit` 是最终全局返回数，范围为 1–20。
- 本技能使用的 `filters` 包括 `published_from`、`published_to`、`languages`、`jurisdictions`、`legal_status` 和 `patent`。`legal_status` 仅接受 `尚未生效`、`现行有效`、`已被修改`、`失效`、`待核实`。
- 日期、语言和法域过滤是否真正生效取决于来源。法律 provider 是中国法规来源，当前实际执行的是 `legal_status`；非中国法域和其他未支持过滤器会在响应中标明。不要仅因请求中带有过滤器就声称过滤已应用。
- 不要发送请求级模型、重排、PDF 或 trust 开关；未知字段会被拒绝。

### 金融垂直搜索

- 查询中写明公司名称或已知证券代码，并加上具体主题，如分红、经营业绩、并购或行业政策；命中公司名称可能只是正文提及，需核对事件主体。
- `published_from/published_to` 按新闻发布日期过滤，不代表财报报告期、交易日期或事件发生日期。示例日期须按用户问题调整；“最新”结论以实际 `published_date` 为准，空结果只说明本次检索未找到证据。
- 当前宁夏新闻来源返回 `financial.dataset="nws_news"`、`document_type="news"`。它是新闻文档检索；不能据此宣称已接入完整公告、券商研报、财务指标、基金持仓或债券行情。客户端无需知道 RDS 表名，也不要自行添加 `filters.financial`、股票代码或指标等未在工具 schema 中定义的参数。
- 当金融候选全部来自 NWS 新闻库时，服务在相关候选内按发布日期降序排序，同一时点再按检索相关性排序。靠前不代表更可信，也不保证是全库最新或完整的新闻集合。
- 金融证据使用下文的字段与质量标记解释；需要验证关键数值或公司事件时，补查公告、交易所披露等原始材料，或从 `search_id` 启动研究。正文很长、有 URL 或检索评估为 `usable`，都不等于已读取并核验原文。

### 解读搜索结果

按以下顺序检查响应：

1. 检查 `failures[]`，确认是否有来源或阶段失败。
2. 检查 `result_set.counts_by_stage` 中 `web`、`academic`、`patent`、`legal`、`financial` 的 `recalled/ranked/assembled/selected` 计数，定位候选丢失阶段。
3. 检查 `retrieval_assessment.status` 与 `retrieval_assessment.gaps[]`，判断证据是否足够。
4. 检查 `query.filter_execution`，确认每项过滤器实际 `applied`、`unsupported` 或 `not_applicable` 的状态。
5. 对法律证据读取 `type: "legal"`、`passage`、`legal.law_type`、`legal.status`、`legal.department`、`legal.directory` 与 `legal.item`。引用时保留法规标题和条号。
6. 法律证据可能没有公开 URL，且 `access.is_open` 为 `false`。不要臆造官方链接、发布日期、法规效力或全文定位；原文被截断时遵守 `diagnostics` 中的限制。
7. 金融证据读取 `type: "financial"`、`financial.dataset/document_type/vendor_record_id/tool`、`published_date`、`citation` 和 `passage.text`；检查 `quality.can_support_key_claim` 与 `diagnostics`。`PROVIDER_EXTRACT_NOT_ORIGINAL`、`NO_STABLE_LOCATOR` 或 `TRUNCATED_EVIDENCE` 表明摘录、定位或完整性限制，不能单独证明关键金融主张。缺少公开链接时保留标题、媒体、日期和记录 ID，不臆造 URL；有链接也不代表 `access.is_open=true`。
8. 仅用 `evidence[].scores.relevance` 排序，不将其视为可信度或法律效力判断。

`status` 只表示搜索执行是否完整，不代表证据充分性。`research_seed.search_id` 指向服务端保存的不可变 evidence 与检索边界快照；不要构造、修改或回传该快照。

## `research`

`research` 是持久化研究任务的统一生命周期工具，支持 `start`、`get`、`feedback` 和 `cancel`。

### 启动任务

从搜索响应取得 `research_seed.search_id` 后调用：

```json
{
  "operation": "start",
  "search_id": "srch_...",
  "idempotency_key": "agent-run-20260811-001",
  "profile": "technology_validation",
  "depth": "standard",
  "objective": {
    "question": "硫化物电解质的关键路线是什么，哪些已形成专利布局？",
    "claims": [
      {
        "text": "硫化物电解质已形成较完整的专利布局",
        "importance": "key"
      }
    ],
    "required_features": ["离子电导率", "界面稳定性", "制备方法"]
  }
}
```

- 必须提供 `search_id` 和全局 `idempotency_key`。为同一个逻辑请求的重试复用同一个 key；只有请求实质改变时才换 key。
- 选择 `profile`：`literature_review`、`technology_validation`（默认）、`prior_art_landscape`、`technology_landscape` 或 `financial_research`；选择 `depth`：`quick`、`standard` 或 `deep`。
- 把问题写入 `objective.question`，已知待核验陈述写入 `objective.claims`，必须覆盖的维度写入 `objective.required_features`。
- 仅在要收紧预设上限时提供 `budget`；不要用它扩大预设预算。

### 金融研究

先检索目标公司取得真实 `search_id`，再启动金融研究，例如：

```json
{
  "operation": "start",
  "search_id": "srch_...",
  "idempotency_key": "financial-research-20260909-001",
  "profile": "financial_research",
  "depth": "standard",
  "objective": {
    "question": "查询贵州茅台（600519.SH）的最新成交价，并说明交易日期、交易时间和数据来源。",
    "required_features": ["最新成交价", "交易日期与时间", "数据来源"]
  }
}
```

- `financial_research` 是显式研究入口。服务端规划器可选择文档（`documents`）、股票行情（`price`）、K 线（`kline`）、基本面（`fundamentals`）、公司档案（`profile`）、公司事件（`events`）或 `unsupported`。这些是返回计划中的操作，不是客户端可直接调用的工具；股票代码、时间范围和所需指标写入 `objective.question`。
- 结构化股票能力依赖服务端规划器和数据网关启用；不能把宁夏新闻搜索可用当作 Wind 股票数据已启用。当前结构化网关仅支持受限股票操作；行情与 K 线需明确 A 股代码（如 `600519.SH`），K 线还需日期区间和日/周/月周期。不要推断已支持基金、债券、宏观、全球股票或任意指标查询。
- 读取 `resolved.financial_plan` 或最终 `dossier.financial_plan` 的 `intent_status`、`execution_status`、`operation`、`failure_code`。只有执行为 `ready` 且实际返回 `data` 时，才使用其结构化结果；`documents` 不执行股票数据查询。
- 结构化结果位于 `financial_plan.data`，包括 `provider`、`tool`、`retrieved_at` 和 `tables[].columns/rows/units`；它们与 `evidence_index` 中的新闻文档分别引用。数值说明须保留证券主体、交易日或报告期、单位与来源；抓取时间不是行情时间，缺值不是零，不为表格臆造公开 URL。
- 计划为 `disabled`、`failed` 或 `unsupported` 时，结合原因说明未取得哪些数据；可以使用仍可用的文档继续研究。`clarification_questions` 是待澄清信息，不能替用户补造证券代码、日期或口径。

### 读取、补充与取消

读取任务：

```json
{
  "operation": "get",
  "research_id": "rsch_...",
  "detail": "full"
}
```

- 当 `state` 为 `queued` 或 `running` 时，等待响应中的 `retry_after_ms` 再读取；不要高频轮询。
- 仅在 `needs_input` 时提交 `feedback`。先读取最新任务，再以当前 `task_revision` 提交真实的 `answers` 或 `note`；不要替用户虚构答案。
- 取消任务时使用最新的 `task_revision`。终态包括 `completed`、`partial`、`needs_input`、`failed` 与 `cancelled`。
- `state="completed"` 只表示流程正常停止。用 `dossier.assessment.overall` 判断结论充分性，并从 finding 的 evidence ID 解引用 `dossier.evidence_index`；同时检查 `dossier.coverage.gaps` 和顶层 `stop`。

## 作答规则

- 让每个关键结论对应具体 evidence，并保留 finding、evidence 和 locator 的关系。区分搜索片段、法规条文、PDF 原文和研究结论。
- 法律问题先说明适用法域、检索时点、法条状态和证据缺口；将法条内容、事实适用和结论明确分开。对于个案、争议或跨法域问题，提示用户咨询合格的法律专业人士。
- 学术结论优先使用可定位的原始论文；专利结论优先使用专利文献，并区分申请、公开、授权和未知状态。
- 对时效性问题检查证据日期、`legal.status` 和 `filter_execution`。日期陈旧、状态待核实、过滤未执行或证据缺少公开链接时，明确披露限制。
- 当 `retrieval_assessment.status` 为 `limited`，有实质 `failures[]`，或法律/研究证据为 `partial`、`insufficient`、`conflicted`、`needs_expert_review` 时，不要给出无保留的确定性结论。
- 不要生成或声称接口提供单一 `trust_score`，不要臆造来源、法规元数据、引文、申请人、发明人、日期、许可证或 URL。

## 错误处理

- `401 invalid_token` 或未授权：重新执行 `openclaw mcp login chukonu-web-search`、`codex mcp login chukonu-web-search`，或在 Claude Code 中通过 `/mcp → chukonu-web-search → Authenticate` 重新完成 OAuth；同时检查并移除误配的静态 Authorization 头。
- `search` 参数被拒绝：移除未知字段，确认 `limit`、`source_types`、日期和 `legal_status` 的格式。
- 金融来源不可用或无结果：检查 `failures[]`、`query.filter_execution` 和日期范围；如改用网页补查，明确标明来源变化和金融数据缺口。`FINANCIAL_RESEARCH_PLANNER_DISABLED`、`WIND_STOCK_DATA_DISABLED` 等错误表示结构化能力未启用；不要把文档研究完成解释为行情查询成功，也不要要求用户配置上游凭据或绕过公开 MCP。
- 法律 provider 不可用：阅读 `failures[]` 和 `retrieval_assessment.gaps[]`；只有在普通网页证据仍覆盖主张时才以明确限制继续作答。
- `research start` 幂等冲突：若逻辑请求未变则恢复原请求并复用原 key；若请求变了才用新 key。
- `research` 返回 `needs_input`：读取 `input_request`，向用户取得答案后用最新 revision 提交。返回 `failed`、`partial` 或 `cancelled`：读取 `failures[]`、`stop` 和 coverage gaps，并说明已完成部分与限制。
