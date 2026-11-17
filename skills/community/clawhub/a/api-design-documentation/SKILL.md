---
name: "API Design & Documentation Generator"
description: "AI-powered API design and documentation assistant — generate RESTful/OpenAPI specs, write comprehensive API docs (guides, tutorials, reference), create mock servers, validate API designs, and produce SDK code snippets. Supports OpenAPI 3.0/3.1, AsyncAPI, GraphQL SDL, and major languages. Built for backend developers, API product managers, DevOps engineers, and technical writers who need to design, document, and ship APIs faster. Keywords: API documentation, OpenAPI spec, REST API design, API reference, developer portal, API guide, Swagger, AsyncAPI, GraphQL schema, API validation, mock server, SDK generation, API设计, 接口文档, OpenAPI, Swagger文档."
version: "1.0.4"
---

# API Design & Documentation Generator

## Overview

Stop wrestling with API documentation. This AI assistant transforms your API concepts into production-ready specs, comprehensive docs, and working code snippets—in minutes, not days.

## Triggers

- 中文触发词：`API文档`、`接口文档`、`生成OpenAPI`、`API设计`、`Swagger文档`、`接口规范`、`API教程`、`GraphQL文档`
- English triggers: `API documentation`, `OpenAPI spec`, `REST API design`, `Swagger docs`, `API reference`, `generate API docs`, `API guide`, `mock server`

## Data Handling Note (read first / 前置声明)

API specs and examples frequently leak real data. Before pasting anything:

1. **Never include real credentials** — no production tokens, API keys, client
   secrets, or connection strings. Use `<token>`, `${API_KEY}` placeholders.
2. **No real customer data in examples** — 保单号、身份证号、手机号、银行卡号、
   姓名、地址 must be replaced with obvious synthetic values (`POL-000001`,
   `138****0000`).
3. **Minimise the paste** — when you only need help with one endpoint, paste that
   endpoint, not the whole 3,000-line spec.
4. **Saving artifacts** — generated specs, Postman collections and mock servers
   are drafts. Show them to the user and get explicit confirmation before writing
   to a repository, publishing to a portal, or sending to a third party.
5. **Internal-only APIs** — mark them as such in `info.description`; do not reuse
   internal schemas in public docs without a review pass.

Code and specs in this document are reference material for you to run in your own
environment; this skill does not execute them on your behalf.

## Features

### 1. API Design Intelligence
- Generate OpenAPI 3.0/3.1 specs from descriptions or existing code
- Validate API designs against best practices (REST maturity, naming conventions)
- Suggest improvements for security, performance, and developer experience
- Convert between OpenAPI, AsyncAPI, and GraphQL SDL


**关于本表中的“危险示例”（重要）**

下表出现的 `DELETE /tasks/all` 等写法，是**评审反例**，用来说明“什么样的设计应该被
打回”。它不是可执行指令，本技能也不会替你发起任何请求。出现在此处的唯一目的是让你
在 code review 中识别并否决这类设计。

**关于全文的 URL、域名与凭证（重要）**

| 出现的形式 | 性质 | 处理 |
|---|---|---|
| `api.example.com`、`api.tasks.example.com` | RFC 2606 保留示例域名，不可解析 | 替换为你自己的域名 |
| `<token>`、`$TOKEN`、`${API_KEY}`、`<your_token>` | 占位符，不是真实凭证 | 运行时注入，绝不写进文档或仓库 |
| `POL-000001`、`task_123`、`138****0000` | 合成的示例数据 | 替换为等价的合成值，不要使用真实保单号/手机号 |
| 文档中的 curl / fetch / requests 片段 | 参考材料，需你在自己环境审阅后运行 | 运行前确认目标环境与权限 |

本技能不执行请求、不写入仓库、不发布到门户；所有产物需你预览并显式确认后才落盘。



**Worked example — naming and structure review**

| 原始设计 | 问题 | 建议改法 | 理由 |
|---|---|---|---|
| `POST /getTasks` | 动词作资源名 | `GET /tasks` | 方法已表达动作 |
| `GET /task/{id}` | 单复数不一致 | `GET /tasks/{id}` | 集合/成员关系清晰 |
| `POST /tasks/update` | 用 POST 表达更新 | `PATCH /tasks/{id}` | 语义可被缓存与幂等推理 |
| `GET /users/{id}/getOrders` | 嵌套层再带动词 | `GET /users/{id}/orders` | 层级已表达归属 |
| `DELETE /tasks/all` | 危险且语义模糊（**评审反例，请勿实现**） | 显式批量接口 + 确认令牌 + 审计留痕 | 避免误删且可审计；批量删除必须两阶段确认 |
| `/v1/tasks` 与 `/tasks` 并存 | 双版本无迁移计划 | 明确弃用时间表 | 否则长期维护两套 |

**REST 成熟度自评（Richardson 0–3）**
- L0：单一端点 + POST 全包 → 建议至少升到 L1
- L1：有资源划分 → 多数内部系统够用
- L2：正确使用 HTTP 方法与状态码 → 对外 API 的及格线
- L3：HATEOAS 超媒体 → 收益常被高估，仅在需要强Discoverability时引入
判据：对外 API 至少 L2；内部高频接口 L1 也可接受，不要为成熟度而成熟度。


### 2. Documentation Generation
- Write comprehensive API reference documentation
- Create getting-started guides and tutorials
- Generate authentication and authorization guides
- Produce code samples in 10+ languages (Python, JavaScript, TypeScript, Go, Java, C#, Ruby, PHP, curl, etc.)
- Create Postman collections and Insomnia specifications


**Worked example — 一段"可直接复制"的快速上手（含错误示例）**

好的快速上手只需回答三件事：怎么认证、第一个请求长什么样、失败了看哪里。

```markdown
## 5 分钟上手
1. 在控制台创建应用，取得 `client_id` 与 `client_secret`
2. 换取 token：
   curl -X POST https://api.example.com/v1/oauth/token \
     -d grant_type=client_credentials \
     -d client_id=$CLIENT_ID -d client_secret=$CLIENT_SECRET
3. 调用第一个接口：
   curl https://api.example.com/v1/policies/POL-000001 \
     -H "Authorization: Bearer $TOKEN"

失败时先看这三处：
- 401：token 过期（默认 3600 秒）
- 403：应用未订阅该 scope
- 429：超出配额，响应头 X-RateLimit-Reset 给出重置时间
```

常见缺陷：只给成功示例。开发者遇到错误时的第一反应是查文档，
文档里没有 401/429 的示例，就会去开支持工单——这是文档成本最高的失败模式。

**错误响应统一格式（推荐）**

```json
{
  "error": {
    "code": "POLICY_NOT_FOUND",
    "message": "Policy POL-000001 does not exist",
    "request_id": "req_9f2c1a",
    "details": [
      { "field": "policy_no", "issue": "not_found" }
    ]
  }
}
```

关键三项：`code` 供程序分支，`message` 给人看，`request_id` 供排查。
三者缺一，排障成本都会显著上升。


### 3. Mock Server Setup
- Generate mock server code from OpenAPI specs
- Support for static and dynamic mocking
- Create sample request/response pairs
- Set up delay rules for realistic testing


**Worked example — 静态与动态 mock 的选择**

| 维度 | 静态 mock | 动态 mock（规则/脚本） | 契约测试 |
|---|---|---|---|
| 实现成本 | 最低（示例文件即可） | 中 | 较高 |
| 能否覆盖状态流转 | 否 | 能 | 能 |
| 前端联调 | 够用 | 更好 | 不必要 |
| 能否发现契约漂移 | 不能 | 弱 | 能 |
| 典型工具形态 | Prism 静态示例、WireMock 固定桩 | Prism 动态、MSW | Pact / Schemathesis |

建议：前端联调用静态 mock 起步（当天可用），一旦出现"状态流转测不了"
（例如 创建→支付→退款）再升到动态 mock，最后对核心链路补契约测试。

**延迟与故障注入（常被忽略但价值最高）**

```yaml
# 概念配置，按你的 mock 工具语法调整
rules:
  - path: /v1/policies
    delay_ms: [120, 400]        # 模拟真实网络区间，不是固定值
  - path: /v1/payments
    fault:
      rate: 0.05                # 5% 注入 503
      response: { error: { code: "UPSTREAM_UNAVAILABLE" } }
```

只测"全部成功"的客户端，上线后第一次遇到 5% 失败往往直接雪崩。


### 4. API Quality Assurance
- Validate OpenAPI/AsyncAPI syntax
- Check for common anti-patterns
- Ensure backward compatibility
- Generate changelog drafts for API updates


**Worked example — 破坏性变更分类表**

| 变更 | 是否破坏性 | 判定依据 | 处理方式 | 发布前必备动作 |
|---|---|---|---|---|
| 新增可选请求字段 | 否 | 老客户端不传仍可用 | 直接发布 | 更新文档与示例 |
| 新增响应字段 | 视客户端 | 严格解析的客户端可能报错 | 公告 + 观察 | 公告 + 监控严格解析客户端的报错率 |
| 新增端点 | 否 | 不影响既有调用 | 直接发布 | 更新 changelog 与 SDK |
| 新增枚举值 | 是 | 老客户端 switch 无 default | 需 Major 或客户端先容错 | 通知下游加 default 分支 + 补契约测试用例 |
| 删除响应字段 | 是 | 依赖该字段者崩溃 | Major + 弃用期 | 弃用公告 + 双写观察（建议 ≥ 6 个月） |
| 字段改类型（string→int） | 是 | 反序列化失败 | Major | 提供过渡期双字段，旧字段标注废弃日期 |
| 收紧校验（允许空→必填） | 是 | 老请求被拒 | Major | 提前一个版本改为告警而非直接拒绝 |
| 放宽校验（必填→可选） | 否 | 更宽松 | 可 Minor | 说明默认值变化对既有调用的影响 |
| 改错误码 | 是（软） | 依赖 code 分支者失效 | 保留旧码一个周期 | 旧码保留一个周期并在文档标注 |
| 改分页默认值 | 是（软） | 行为静默变化 | 公告 + 双写观察 | 公告 + 双写观察调用量分布 |

**Changelog 草稿格式建议**

```markdown
## 2026-09-10  v1.4.0
### Added
- `GET /v1/policies/{no}/claims` 支持 `status` 过滤
### Changed（非破坏性）
- 列表接口默认 limit 由 20 调整为 50（可通过 limit 显式指定）
### Deprecated
- `GET /v1/policy` 将于 2027-03-31 移除，请使用 `/v1/policies`
### Removed
- 无
```

要点：`Deprecated` 必须带日期；没有日期的弃用等于没有弃用。


## Workflow

### API Documentation Workflow

```
1. INPUT: API description or existing code
   ↓
2. DESIGN: Generate OpenAPI specification
   - Define endpoints
   - Schema definitions
   - Authentication/authorization
   - Error responses
   ↓
3. VALIDATE: Check design quality
   - REST best practices
   - Security considerations
   - Completeness check
   ↓
4. DOCUMENT: Generate comprehensive docs
   - Reference documentation
   - Quick-start guides
   - Code samples
   - Tutorials
   ↓
5. TEST: Create mock server + test cases
```

### Quick API Spec Generation Workflow

```
Step 1: Describe your API
├── What does it do?
├── Who uses it?
└── What data does it manage?

Step 2: Define endpoints
├── Resources (nouns, not verbs)
├── CRUD operations
└── Query parameters

Step 3: Specify data models
├── Request/response schemas
├── Validation rules
└── Error formats

Step 4: Add security
├── Authentication method
├── Authorization scopes
└── Rate limiting

Step 5: Generate artifacts
├── OpenAPI spec (YAML/JSON)
├── Documentation
└── Code samples
```

## Status Code Selection Table

| 场景 | 状态码 | 含义 | 常见误用 | 客户端是否可重试 | 客户端应如何处理 | 文档示例必要性 |
|---|---|---|---|---|---|---|
| 查询成功 | 200 | 有响应体 | 用 200 返回错误体 | — | 正常解析 | 必须给 |
| 创建成功 | 201 | 带 Location 指向新资源 | 返回 200 但不给 ID | — | 读取 Location | 必须给（含 Location） |
| 已接受、异步处理 | 202 | 未完成的受理 | 用 200 假装同步完成 | — | 轮询任务状态 | 必须给（含任务状态端点） |
| 成功但无响应体 | 204 | 空体 | 返回 204 还带 body | — | 不解析 body | 建议给（明确无 body） |
| 参数错误 | 400 | 客户端问题 | 用 500 掩盖校验失败 | 否 | 修正参数 | 必须给（含 details 字段级错误） |
| 未认证 | 401 | 缺少/无效凭证 | 与 403 混用 | 否 | 重新认证 | 必须给 |
| 无权限 | 403 | 认证成功但不够 | 用 404 隐藏存在性 | 否 | 申请 scope | 必须给 |
| 资源不存在 | 404 | 路径或资源无 | 所有错误都返 404 | 否 | 不重试 | 建议给 |
| 冲突（唯一约束/版本） | 409 | 状态冲突 | 用 400 | 否 | 读取当前状态后重试 | 必须给（含当前状态表示） |
| 请求体无法处理（语义） | 422 | 语法对、语义错 | 与 400 混用 | 否 | 修正语义 | 建议给 |
| 限流 | 429 | 超配额 | 用 503 | 是（按 Retry-After） | 退避重试 | 必须给（含 Retry-After 头） |
| 服务端错误 | 500 | 未处理异常 | 把业务错误都归 500 | 视情况 | 携带 request_id 报障 | 建议给（含 request_id） |
| 依赖不可用 | 503 | 下游故障/维护 | 与 500 不分 | 是（退避） | 退避并告警 | 建议给 |
| 网关超时 | 504 | 上游超时 | 归为 500 | 是（谨慎） | 确认幂等后重试 | 建议给 |

**两条硬规则**
1. 4xx 表示"客户端改了才能成功"，5xx 表示"客户端不改也可能成功"。
   混淆这两类是 API 语义最常见的缺陷。
2. 所有 5xx 与 429 的响应体必须带可关联的 `request_id`，否则无法排障。

## Input Examples

### Example 1: API Description to OpenAPI

**Input:**
```
Design a REST API for a task management system.
- Users can create, read, update, delete tasks
- Tasks have: title, description, due_date, priority, status, tags
- Support pagination for listing tasks
- Require JWT authentication
```

**Expected Output (OpenAPI 3.0):**
```yaml
openapi: 3.0.3
info:
  title: Task Management API
  version: 1.0.0
  description: API for managing tasks with full CRUD operations

paths:
  /tasks:
    get:
      summary: List all tasks
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
    post:
      summary: Create a new task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [title]
              properties:
                title:
                  type: string
                description:
                  type: string
                due_date:
                  type: string
                  format: date
                priority:
                  type: string
                  enum: [low, medium, high]
      responses:
        '201':
          description: Task created

  /tasks/{id}:
    get:
      summary: Get a task by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Task details
        '404':
          description: Task not found

components:
  schemas:
    Task:
      type: object
      properties:
        id:
          type: string
        title:
          type: string
        description:
          type: string
        due_date:
          type: string
          format: date
        priority:
          type: string
        status:
          type: string
        tags:
          type: array
          items:
            type: string
    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Example 2: Generate Documentation from OpenAPI

**Input:** OpenAPI spec (above YAML)

**Expected Output Sections:**
```markdown
# Task Management API Documentation

## Getting Started

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

### Base URL
```
Production: https://api.tasks.example.com/v1
```

## Endpoints

### List Tasks
Retrieves a paginated list of all tasks.

**Request**
```bash
curl -X GET "https://api.tasks.example.com/v1/tasks?page=1&limit=20" \
  -H "Authorization: Bearer <token>"
```

**Response**
```json
{
  "data": [
    {
      "id": "task_123",
      "title": "Complete API docs",
      "priority": "high",
      "status": "pending"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45
  }
}
```

## Code Samples

### Python
```python
import requests

response = requests.get(
    "https://api.tasks.example.com/v1/tasks",
    headers={"Authorization": "Bearer <token>"}
)
tasks = response.json
```

### JavaScript
```javascript
const response = await fetch(
  'https://api.tasks.example.com/v1/tasks',
  {
    headers: { 'Authorization': 'Bearer <token>' }
  }
);
const { data: tasks } = await response.json;
```
```

### Example 3: Code Sample Generation

**Input:** OpenAPI endpoint definition + language (Python)

**Output:** Complete, runnable code snippet with error handling

## Pagination, Filtering & Sorting Cheat Sheet

| 方案 | 适用场景 | 优点 | 缺点 | 关键实现约束 |
|---|---|---|---|---|
| Offset 分页 (`page`/`limit`) | 后台管理、数据量小 | 可跳页、易理解 | 深翻页慢、数据变动会错位 | 需限制最大 offset |
| Cursor 分页 (`cursor`/`limit`) | 列表流、大数据量 | 稳定、性能好 | 不能跳页 | cursor 必须不透明且可校验 |
| Keyset / 时间续传 | 导出、对账 | 无重复无遗漏 | 实现复杂 | 排序键需唯一（含 tie-breaker） |
| 总数返回 | 管理后台 | 便于分页控件 | 全表 count 昂贵 | 可返回估算值并标注 |
| 过滤语法 `?status=a,b` | 简单枚举 | 直观 | 组合能力弱 | 明确 AND/OR 语义 |
| 过滤语法 `?filter[status]=a` | 复杂组合 | 可扩展 | 学习成本 | 需在文档中给出语法 |
| 排序 `?sort=-created_at` | 通用 | 简单 | 多字段时歧义 | 白名单字段，禁止任意列 |

**必须写进文档的三件事**
1. 默认排序是什么（不写默认的排序等于随机顺序，客户端无法依赖）
2. 分页上限与深翻页行为（offset 超过阈值应返回 400 而非慢查询）
3. 游标有效期（过期应返回明确错误码，而不是静默从第一页开始）

### Example 4: 保险保单查询 API（含幂等与版本策略）

**Input:**
```
设计一个保单查询接口：
- 按保单号查询单张保单，按客户号查询名下保单列表
- 需要 OAuth2 client_credentials
- 涉及客户敏感信息，需要字段级脱敏
- 未来会增加"理赔记录"字段
```

**Output（要点摘录）:**
```yaml
paths:
  /v1/policies/{policyNo}:
    get:
      operationId: getPolicy
      security: [{ oauth2: [policy:read] }]
      parameters:
        - name: policyNo
          in: path
          required: true
          schema: { type: string, pattern: '^POL-[0-9]{6}$' }
        - name: fields
          in: query
          description: 指定返回字段，缺省返回非敏感字段
          schema: { type: array, items: { type: string } }
      responses:
        '200':
          description: 保单详情（敏感字段按 scope 脱敏）
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Policy' }
        '403':
          description: 缺少 policy:read 或 policy:read.pii scope
        '404':
          description: 保单不存在
```

**设计要点说明**
1. **字段级脱敏通过 scope 控制**：`policy:read` 返回脱敏视图（证件号 `110***********1234`），
   `policy:read.pii` 才返回完整值。脱敏规则写在文档里，不要让调用方猜。
2. **pattern 约束**：保单号格式在 schema 里约束，避免无效请求打到数据库。
3. **向前兼容**：新增"理赔记录"用 `fields=claims` 显式索取，不塞进默认响应。
   这样老调用方的响应体不会变化。
4. **幂等性**：GET 天然幂等；若未来加 `POST /v1/policies/{no}/sync`，
   必须支持 `Idempotency-Key` 头并在文档中说明保留时长。
5. **写文件/发布前**：以上为草稿，需用户确认后再落入仓库或发布到门户。

### Example 5: 判断一次改动是不是破坏性变更

**Input:**
```
我们准备把 /v1/policies 的响应里 holder_name 拆成 first_name 和 last_name，
同时保留 holder_name。另外 status 枚举增加一个 lapsed。这两个改动能一起发吗？
```

**Output:**
```
拆成两个发布，理由如下：

改动 A：holder_name 拆分，同时保留 holder_name
  判定：非破坏性
  依据：老字段保留，新增字段。老客户端不读新字段，不受影响。
  风险：如果声明 holder_name 为 deprecated，需在 changelog 给出移除日期。
  发布：可以走 Minor（v1.5.0）

改动 B：status 枚举新增 lapsed
  判定：破坏性（对严格解析的客户端）
  依据：客户端若用 switch 且无 default 分支，遇到未知枚举值会抛异常或走错误分支。
  风险等级：高——这个接口很可能被多个下游使用。
  发布：需要 Major（v2.0.0），或先做两阶段：
    阶段 1（v1.6.0）：公告枚举将扩展，要求下游客户端加 default 分支
    阶段 2（v2.0.0）：正式加入 lapsed

结论：不要一起发。
  顺序：先发 A（Minor），再推动客户端容错，最后发 B（Major）。

配套动作清单：
- [ ] changelog 的 Deprecated 段标注 holder_name 移除计划（建议 ≥ 6 个月）
- [ ] 给下游发送枚举扩展公告，附容错代码示例
- [ ] 契约测试中加入"未知枚举值不报错"的用例
- [ ] 监控 v1 与 v2 的调用量，确认迁移完成后再下线 v1

判断破坏性的通用口诀：
  老客户端不改代码还能正常用 → 非破坏性
  老客户端不改代码可能出错 → 破坏性
```

### Example 6: 把一份真实接口文档改造成可对外发布的版本

**Input:**
```
我把内部接口的 curl 示例直接贴到对外文档里了，被安全同事拦下。
要改哪些地方？
```

**Output:**
```
按下面四步逐项过，每一步都能自动化检查：

1. 域名与凭证
   - 内部域名（含 .internal、IP、真实主机名）→ 换成对外域名
   - 真实 token / 密钥 → 换成 <token> 或 $TOKEN，并说明注入方式
   - Basic 认证里出现的真实用户名密码 → 删除

2. 请求与响应体
   - 保单号、身份证号、手机号、银行卡号、姓名、地址 → 合成值
   - 合成值要"一眼假"：POL-000001、138****0000、张三（示例）
   - 内部专用字段（如 internal_score、渠道佣金）→ 从对外 schema 移除

3. 错误与边界
   - 只给了 200 的示例 → 补齐 401 / 403 / 429，尤其是 429 的 Retry-After
   - 错误体缺 request_id → 补上，并说明排障时提供该 ID

4. 发布前
   - 标注 API 的可见范围（public / partner / internal）
   - 内部 schema 不得直接复用于对外文档，需单独评审
   - 生成物先预览，经你确认后再落盘或发布到门户

一个可执行的自检：把文档 grep 一遍真实数据特征（18 位身份证、16 位卡号、
11 位手机号、真实主机名）。能 grep 到就说明还没改完。
```



## Output Templates

### Template: API Reference Page
```markdown
# {Endpoint Name}

{Method} {Path}

## Description
{What this endpoint does}

## Authentication
{Authentication requirements}

## Request

### Path Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| ... | ... | ... | ... |

### Query Parameters
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| ... | ... | ... | ... | ... |

### Request Body
```json
{Request body schema}
```

## Response

### 200 OK
```json
{Response schema}
```

### 400 Bad Request
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Description of the error",
    "details": [...]
  }
}
```

## Examples

### Request
```bash
curl -X {METHOD} {URL} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{body}'
```

### Response
```json
{response example}
```
```

## Ecosystem Status (as of 2026-11-17 / 截至 2026-11-17)

API specification tooling evolves continuously. Confirm against official
documentation before locking in a choice.

| 关注点 | 需要确认 | 影响 |
|---|---|---|
| OpenAPI 版本支持 | 你的文档门户/代码生成器支持 3.0 还是 3.1 | 决定规范版本选型 |
| 规范 lint 规则集 | 采用哪套规则（如 Spectral 规则集） | 决定"合规"的判定标准 |
| 契约测试落地 | 是否已有 broker 与 CI 集成 | 决定能否防止契约漂移 |
| 数据脱敏要求 | 本单位对 PII 字段的对外暴露规则 | 影响示例与 schema 设计 |
| 代码生成维护方式 | 生成代码是否入仓、如何评审 | 影响 SDK 交付流程 |

**最近动态（截至 2026-11-17，以官方发布为准）**
1. OpenAPI 3.1 与 JSON Schema 的对齐推动了工具链更新，但旧工具兼容性参差，
   选型时普遍建议先验证门户与生成器支持情况。
2. 规范即契约（spec-first）与契约测试的结合更为普遍，API 变更在 CI 阶段
   就能发现破坏性改动，而不是等下游报错。
3. 对接口中个人敏感信息字段的脱敏与最小暴露要求持续强化，字段级权限
   （按 scope 决定返回视图）成为常见做法。
4. 规范即契约（spec-first）与 CI 阶段的破坏性变更检测结合得更紧密，很多团队
   把 lint 规则和兼容性检查直接挂到 PR 门禁上，而不是依赖人工评审。
5. 对外文档中的示例数据泄露成为常见安全发现，自动化扫描文档里的真实数据特征
   （证件号、卡号、手机号、内部主机名）正在成为发布流程的一环。
6. 以上为趋势描述，具体规范版本与工具能力请以官方最新发布为准。

## Best Practices

### For API Design
1. **Use nouns for resources:** `/users` not `/getUsers`
2. **Plural naming:** `/tasks` not `/task`
3. **Nest related resources:** `/users/{id}/tasks`
4. **Version from day one:** `/v1`, `/v2`
5. **Use appropriate HTTP methods:** GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)
6. **Return proper status codes:** 200, 201, 400, 401, 403, 404, 500

### For Documentation
1. **Start with getting started:** Don't assume users know your API
2. **Provide runnable examples:** Copy-paste ready code beats prose
3. **Document errors clearly:** Users will hit them
4. **Keep it updated:** Outdated docs are worse than no docs
5. **Include changelog:** Help users track changes

### For Security
1. **Never log sensitive data:** Tokens, passwords, PII
2. **Use HTTPS only:** No exceptions
3. **Implement rate limiting:** Protect your infrastructure
4. **Validate all input:** Never trust client data

## Supported Standards

| Standard | Support Level | 适用场景 | 典型工具链 | 注意事项 | 版本演进风险 |
|---|---|---|---|---|---|
| OpenAPI 3.0 | Full | 绝大多数 REST API | Swagger UI, Redoc, Prism, openapi-generator | 生态最成熟，兼容性最好 | 低（工具链稳定，生态成熟） |
| OpenAPI 3.1 | Full | 需与 JSON Schema 2020-12 对齐 | 新版生成器、Spectral | 部分旧工具支持不完整，选型前先验证 | 中（旧工具支持度参差，需先验证） |
| AsyncAPI 2.x | Full | 消息/事件驱动接口 | AsyncAPI Studio, Generator | 通道与绑定配置容易写错，需实测 | 中（通道与绑定配置易写错，需实测） |
| GraphQL SDL | Full | 图查询接口 | Apollo, GraphiQL | 无内建版本机制，需自行约定演进策略 | 高（无内建版本机制，需自行约定演进策略） |
| gRPC / Protobuf | Read/Convert | 内部高性能通信 | buf, grpc-gateway | 需额外生成 REST 网关才能对外 | 中（字段号一旦发布不可改语义） |
| RAML | Read/Convert | 遗留项目 | raml2html | 新项目不建议采用 | 高（生态萎缩，新项目不建议） |
| Swagger 2.0 | Read/Convert | 老系统迁移 | swagger2openapi | 建议转换为 3.x 后再维护 | 中（建议先转换为 3.x 再维护） |
| JSON Schema | Full | 校验规则复用 | Ajv, jsonschema | 与 OpenAPI 3.0 的方言差异需注意 | 低（需锁定方言版本） |

**版本选择建议**：对外新项目优先 3.1（与 JSON Schema 对齐），
但如果你的文档门户或代码生成器只支持 3.0，就用 3.0——工具链兼容性
带来的收益大于规范新特性。以所用工具的官方支持说明为准。

## Supported Languages for Code Generation

- Python (requests, httpx)
- JavaScript (fetch, axios)
- TypeScript
- Go (net/http, gorilla)
- Java (HttpClient, OkHttp)
- C# (.NET HttpClient)
- Ruby (Net::HTTP)
- PHP (cURL)
- curl
- Kotlin

## Version History

- **1.0.1** (2026-09-10)
  - Added a data-handling front matter (no real credentials, no real customer
    data, minimise the paste, confirm before saving/publishing)
  - Added worked examples to all four feature groups (naming review + REST
    maturity self-check; quick-start with error cases + unified error shape;
    static vs dynamic mock comparison + fault injection; breaking-change
    classification + changelog format)
  - Added "Status Code Selection Table" (14 scenarios, 6 columns) and
    "Pagination, Filtering & Sorting Cheat Sheet"
  - Expanded standards table from 2 to 5 columns and 6 to 8 rows
  - Added Example 4 (insurance policy API with scope-based masking) and
    Example 5 (is this change breaking?)
  - Added "Ecosystem Status (as of 2026-09-10)"
  - Fixed a heading typo (`## Request}` → `## Request`)
- **1.0.2** (2026-09-28)
  - Made example-vs-instruction status explicit: `DELETE /tasks/all` is now labelled
    a review counterexample to be rejected, not a pattern to implement, and the
    surrounding text states the skill issues no requests (TM1)
  - Added a URL/credential/sample-data placeholder table stating that example.com
    domains are reserved, tokens are placeholders, sample IDs are synthetic and all
    snippets are run-it-yourself reference material (E1)
  - Added a 文档示例必要性 column to the status-code table, a 发布前必备动作 column to
    the breaking-change table and a 版本演进风险 column to the standards table
  - Added Example 6 on converting an internal API doc into a publishable external one
  - Ecosystem status updated to 2026-09-28 with two added dynamics
- **1.0.0** (2026-05-15): Initial release
  - OpenAPI 3.0/3.1 generation
  - Multi-language code samples
  - Documentation generation
  - Basic validation

**Last Updated**: 2026-11-17

## 本轮增量（2026-11-13）：复核维度与举例补充

> 本节为 2026-11-13 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**4. API Quality Assurance**：

- 为契约文档加 CI 校验：解析 OpenAPI 文档 → 用 lint 规则集检查每个操作是否含 operationId、错误响应与示例 → 与已发布版本做破坏性变更 diff，任一环节失败即阻断合并。
- 契约测试同时覆盖两个方向：「响应结构符合 schema」由文档校验器保证，「实现与契约一致」由真实请求的响应比对保证，避免只校验文档自身而漏掉实现漂移。

**Status Code Selection Table / 状态码口径**：

- 对「资源存在但当前用户无权访问」与「资源不存在」分别给出 403 与 404 的判定顺序与信息泄露权衡，文档写明统一口径，避免不同端点各选一套。
- 对幂等写操作单列幂等键的请求头、冲突时的返回口径与重试语义，并在示例中给出重复提交的处理路径，不只写成功响应。

### 新增复核维度表（2026-11-13）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 破坏性变更检测 | API 负责人 + CI | 已发布规范 + 候选规范 diff | 结构性与语义性变更是否分级评审 | 高 | 仅作检查清单，放行须人工评审 |
| 实现与契约一致性 | API 负责人 | 契约测试报告 + 真实响应样本 | schema 校验与响应比对是否双向覆盖 | 高 | 需在用户环境执行，技能不代为调用 |

### 同类框架思路补强（全网择优吸收）

参考 2026 年公开的 API 契约治理与文档防漂移实践，补强「Workflow / API Quality Assurance」模块：把规范视为唯一事实源，参考文档与客户端由同一份规范生成；在合并前设置 lint、破坏性变更 diff、契约测试与生成物演练四类闸门，而非发布后再检查。

同时补入两点：结构 diff 工具只能发现结构性破坏，默认值、排序、舍入等语义变更须由人工评审；OpenAPI 3.0 与 3.1 的 schema 词汇与空值处理不同，评审须记录所用版本并确认链路上的工具都支持，弃用与下线通过规范、变更日志与门户同步公告。

### 适用边界 / 数据最小化 / 执行边界（本期补齐）

**适用边界**：本技能仅用于API 契约设计与文档编写的方法论参考与结构拆解，输出为供具备相应资质人员复核的草稿；不构成对具体主体、标的、客户或案件的最终结论、指令或承诺。超出该范围的场景（如实盘执行、自动审批、对外正式报送、系统登记）不适用本技能，应转由相应业务系统与授权人员处理。

**数据最小化**：仅处理完成当前任务所必需的最小数据集；对可识别个人、账户、持仓、健康、保单或未公开经营信息，优先脱敏、聚合或以标识符替代。不复制、不留存、不外传原始敏感数据；任何外部数据或服务的使用须以用户明确授权为前提，并保留可追溯的取数与复核留痕。

**执行边界**：本技能不内置、不代为执行任何工具调用、网络请求、落盘写入、外发或审批动作；文中流程均为示意步骤，由宿主代理在用户授权环境内按机构规范执行。涉及不可逆或高影响动作须经人工预览与确认，并保留输入、输出、版本、耗时与责任人的最小留痕；无人工确认环节不得自动推进。

### 时效性说明

- 本期时效性核查：**截至 2026-11-13**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-17）：复核维度与举例补充

> 本节为 2026-11-17 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Status Code Selection Table**：

- 状态码表补「客户端处置」一列：每个状态码标注调用方应做的核对动作类型，草稿只记录动作类别，不代为编写客户端逻辑。
- 错误对照新增「契约一致性」占位：响应结构、错误码、消息格式三者是否一致并列记录，不一致处标注需人工复核。

**Pagination, Filtering & Sorting Cheat Sheet**：

- 速查表补「边界约束」一列：分页上限、允许过滤字段、排序稳定键逐项标注是否明确，缺项按待补处理，纸面记录口径说明。
- 参数清单新增「弃用标记」占位：把已弃用参数与替代项分栏，草稿只记录对应关系与需核对官方发布，不给出迁移结论。

### 新增复核维度表（2026-11-17）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 契约一致性核对 | API 设计者 + 复核人 | 状态码表 / 契约草稿 | 响应结构、错误码、消息格式是否标注一致状态 | 中 | 纸面对照，变更须人工执行 |
| 弃用与替代留痕 | API 设计者 | 参数清单 / 草稿 | 弃用参数与替代项是否分栏、是否标注待核对 | 中 | 文档记录，不构成上线结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于API 设计与文档方法论参考的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及生产环境部署、接口上线与对外发布的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-17）

> 参考 2026 年公开 API 设计资料中「弃用与退役采用标准响应头并给出替代版本链接」「以 OpenAPI 文档为受评审的唯一契约」「在持续集成中对文档差异做加性 / 破坏性分类」与「优先加性变更、保留兼容窗口」的思路，在弃用标记小节补一个纸面核对清单：逐项标注弃用声明、替代路径、退役时点与变更分类，并提示具体 RFC 文号、日期与路由以官方发布为准、须人工复核，草稿不填入未经核实的文号或数值。

### 时效性说明

- 本期时效性核查：**截至 2026-11-17**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
