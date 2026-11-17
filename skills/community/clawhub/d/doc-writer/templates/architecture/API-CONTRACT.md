---
doc-type: API-CONTRACT
layer: project
doc-class: to-be
contract-version: v1    # 只升不改；breaking change 必升主版本并留迁移期（第 6 节）
status: draft           # draft | frozen
frozen-date:            # 仅 status: frozen 时填写
base-url: /api/v1
owner:
---

# API-CONTRACT：〈系统/服务名〉接口契约（v〈1〉）

> **产出者**：架构师——起草草案并主持冻结；冻结前开放讨论，冻结后改动只走第 6 节变更规则
> **受众**：后端（实现依据）、前端（对接依据）、测试（验证依据）+ AI 编程智能体（按本契约直接生成实现与用例）
> **归档**：`docs/project/api-contract.md`；一份契约覆盖一个 base-url，多版本并存时旧版本只读归档
> **真值源**：接口规格本身；端点承载的需求链 `./req-spec.md`；全局约定基线以 `./dev-standards.md` 为准，本契约只记差异；与实现漂移即缺陷
> **质量门禁**：① 每条 FR-NNN 有承载端点或明确缺口（第 4 节） ② 每个端点含可复制 curl 示例且带认证头 ③ 错误表覆盖全部非 2xx 状态码 ④ 冻结后无未经变更流程的改动

## 1. 契约头

〈填写指引：认证方式写清取 token 的端点与刷新机制；服务间调用若用独立凭证（API Key/mTLS）单独一行说明；公开接口在端点目录"认证"列与端点详情中显式标注"公开"，不依赖读者推断。〉

| 项 | 值 |
|---|---|
| 契约版本 | v〈1〉（与 frontmatter contract-version 一致） |
| 状态 | 〈draft / frozen（补日期，与 frontmatter 一致）〉 |
| Base URL | `/api/v1` |
| 认证方式 | 〈如 `Authorization: Bearer <JWT>`，token 获取端点与刷新机制〉 |

## 2. 端点目录

〈填写指引：全量列出，目录即接口总账；路径全小写 kebab-case、资源名复数；"认证"列三值：公开 / Bearer / 〈服务间凭证名〉。〉

| 方法 | 路径 | 说明 | 认证 |
|---|---|---|---|
| 示例：POST | /auth/login | 〈登录换取 token〉 | 公开 |
| 示例：POST | /orders | 〈创建订单〉 | 〈Bearer〉 |
| 示例：GET | /orders | 〈分页查询订单〉 | 〈Bearer〉 |

## 3. 逐端点模板

〈填写指引：目录中每个端点按本模板展开一小节，标题 = "方法 路径"；请求/响应 JSON 用行内注释写"字段-类型-说明-校验规则"；错误表覆盖该端点全部非 2xx 响应；curl 示例必须可直接复制执行——$BASE/$TOKEN 环境变量、认证头、Content-Type、幂等键（如有）齐全。〉

### 〈POST〉 〈/orders〉 —— 〈一句话说明〉

- **用途**：〈谁在什么场景调用、产生什么副作用；承载的 FR-NNN〉
- **请求**：

```json
{
  "customer_id": "string — 客户 ID — 必填，存在性由服务端校验",
  "items": "array<{sku, qty}> — 订单行 — 必填，1–50 项，qty ∈ [1,99]"
}
```

- **响应 201**：

```json
{
  "data": { "id": "string — 订单号，格式 ORD-<13位数字>" },
  "Idempotency-Replayed": "响应头 — 命中幂等键时为 true"
}
```

- **错误**：

| 状态码 | code | message | 场景 |
|---|---|---|---|
| 示例：422 | FIELD_INVALID | 〈参数校验失败〉 | 〈字段缺失/超长/格式错〉 |
| 示例：409 | ORDER_DUPLICATED | 〈幂等键重复且载荷不一致〉 | 〈同 Idempotency-Key 不同 body〉 |

- **示例**（可复制粘贴，含认证头）：

```bash
curl -X POST "$BASE/api/v1/orders" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $UUID" \
  -d '{"customer_id":"CUS-001","items":[{"sku":"SKU-A","qty":2}]}'
```

## 4. FR↔端点覆盖映射

〈填写指引：`./req-spec.md` 每条 FR-NNN 必须在此有承载端点或明确缺口——缺口写原因与补齐计划（ROADMAP 条目号）；本表是需求可追溯性的验收表，评审时逐行核对。〉

| FR | 端点 | 缺口说明 |
|---|---|---|
| 示例：FR-001 | POST /orders、GET /orders/{id} | — |
| 示例：FR-009 | — | 〈暂由后台任务承载，端点待补，ROADMAP BK-032〉 |

## 5. 全局约定（只记差异）

〈填写指引：错误响应结构、分页（page/page_size/total）、排序（sort=-created_at）、过滤、幂等键的基线统一见 `./dev-standards.md`；本节只写与基线的差异（如"分页上限 100，基线为 50"），无差异写"无差异"两字。〉

## 6. 变更规则

〈填写指引：契约冻结后的改动必须走变更流程——新增端点/新增可选字段 → 小版本（v1.1）+ 通知消费方；breaking change（删端点/改字段语义/可选转必填）→ 升主版本（v2）+ 双版本并存迁移期（≥1 个迭代）+ 通知所有消费方；每次变更追加一行记录。〉

| 日期 | 版本 | 变更 | 类型（兼容/breaking） | 通知对象 |
|---|---|---|---|---|
| 示例：YYYY-MM-DD | v1.1 | 〈GET /orders 新增 filter=status〉 | 兼容 | 〈前端组〉 |

## 红线自查（一票否决，提交前逐条勾选）

- [ ] `./req-spec.md` 每条 FR 有承载端点或明确缺口说明（第 4 节逐行核对）
- [ ] 每个端点含可复制执行的 curl 示例（含认证头）
- [ ] 每个端点错误表覆盖全部非 2xx 状态码与业务错误码
- [ ] 公开接口在目录与端点详情中均显式标注"公开"
- [ ] 冻结后无未经变更流程的改动；breaking change 均已升版本、留迁移期、通知消费方
- [ ] 全局约定只记差异，未复制 `./dev-standards.md` 基线全文

## 追踪链

| 方向 | 对象 | 说明 |
|---|---|---|
| 上游（本文消费） | 〈`./req-spec.md` FR-NNN / `./design.md` 第 3 节对外契约 / ADR-NNNN〉 | 契约的输入依据 |
| 下游（消费本文） | 〈`./ddd-design.md` 第 4 节 API 合同 / 前端接口层 / 测试用例 / `./reverse-analysis/` 5b 协议规格〉 | 按本契约实现与验证的对象 |
