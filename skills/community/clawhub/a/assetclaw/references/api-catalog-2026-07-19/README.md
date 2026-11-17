# AssetHub API 目录快照 — 2026-07-19

> 数据来源：实时抓取自 `http://localhost:13579` 后端（生成时间 2026-07-19T15:12:38.578Z）
>
> 本目录存放本次技能文档升级所依据的 3 份原始 API 数据快照。

## 文件清单

| 文件 | 大小 | 用途 |
|------|------|------|
| `api-tools-scale.json` | OpenAI function-calling 格式（schema v1），**1709 个 tool**，**97 个模块** | 模型工具描述 / MCP 风格调用 |
| `api-catalog.json` | 按模块分组的 endpoint 目录 | 路由速查 / diff 比对 |
| `API接口总览.md` | 人类可读 Markdown 总览（含 curl 模板、高危网关说明） | 文档撰写参考 |

## 数据规模对比

| 指标 | 本次快照（2026-07-19） | 旧文档（v1.5.9，截至 2026-04-22） |
|------|------------------------|----------------------------------|
| 端点总数 | **1709** | ~688（估算） |
| 模块数 | **97** | 60+ |
| 数据来源 | server.js route mounts + recursive regex scan | 人工维护 |
| 高危网关 | `Idempotency-Key` + `X-Risk-Confirm-Token` 双重保护 | 仅 `Idempotency-Key` |

## 关键变更点（更新到 SKILL.md / references/）

1. **新增模块（节选）**：`acceptance-management`、`adverse-reaction`、`agent-mesh`、`asset-ai-analysis`、`asset-ai-assistant`、`asset-allocation`、`asset-depreciation`、`asset-usage`、`contracts`、`dashboard-configs`、`emergency-allocation`、`feishu`、`form-customization`、`inspection`、`intelligent-alerts`、`inventory-discrepancies`、`inventory-plans`、`inventory-reports`、`inventory-tasks`、`knowledge-base`、`large-equipment`、`maintenance-management`、`maintenance-temporary`、`metrology`、`module-configs`、`pdca`、`poct-quality-control`、`quality-assurance`、`recipient-strategies`、`safety-inspection`、`spare-parts`、`special-equipment`、`staff`、`supplier`、`tenant-role-config`、`tendering`、`warranty`、`wechat-mp`、`wx-cloud` 等
2. **认证约定**：
   - Header 名：`Authorization: Bearer <JWT>` + `X-Tenant-Id: <id>`（**旧文档写的是 `X-Tenant-ID`，本次以官方为准改为 `X-Tenant-Id`**）
   - 高危操作：`Idempotency-Key` + `X-Risk-Confirm-Token` 双重保护
3. **统一响应结构**：增加 `pagination` 顶层字段（旧文档只在 data 内嵌）
4. **公开接口例外**：`/api/health`、`/api/alive`、`/api/ready` 等无 `/api` 前缀的根路径检查项
