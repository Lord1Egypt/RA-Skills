# batch_search 契约规范（Coze 端 ct-search 工作流 · 2026-10-20）

> 客户端侧：`scripts/batch_lib.py` 的 `--pack` 模式（配合 `scripts/batch.py`）。
> 目的：把 N 个检索 entry 打包成**一次** Coze 调用，由 Coze 端拆解逐条执行后批量返回，
> 取代"每 entry 一次调用、批量 N 条 = N×(6源+汇总) 次调用"的线性膨胀。
> 与既有 `search` / `log_only` 契约**完全兼容**：仅新增 `mode` 分支，旧行为不变。

## 1. 请求（POST 同一端点 `ct-search.coze.site/run`）

```json
{
  "mode": "batch_search",
  "queries": [
    {"id": "lung_adeno_ia2", "source": "openalex",  "keyword": "stage IA2 lung adenocarcinoma prognosis", "year_from": 2020, "year_to": 2026, "max_results": 50},
    {"id": "lung_adeno_ia2", "source": "europepmc", "keyword": "stage IA2 lung adenocarcinoma prognosis", "lit_date_from": "2020-01-01"},
    {"id": "acinar_vs_lepidic", "source": "openalex", "keyword": "acinar predominant adenocarcinoma versus lepidic"}
  ],
  "log_feishu": true,
  "query_origin": "<同 search 契约>",
  "skill_version": "<同 search 契约>",
  "entry_point": "<同 search 契约>",
  "locale": "zh",
  "params": {"user_language": "zh"},
  "querystr": "{\"batch_id\":\"...\",\"package\":\"1/3\",\"entries\":[\"lung_adeno_ia2\"],\"n_queries\":3,\"mode\":\"batch_search\"}"
}
```

**queries[] 元素字段**（与 `search` 契约逐字段同义）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | entry 标识（客户端生成，`[a-z0-9_]`）；**响应必须原样带回**，客户端按它拆回各 entry |
| `source` | string | openalex / europepmc / biorxiv / medrxiv / semantic_scholar / arxiv |
| `keyword` | string | 已翻英的检索式（含概念 AND 拼接，客户端一次预处理完成） |
| `year_from` / `year_to` | int? | 年份边界（可选） |
| `max_results` | int? | 每源上限（可选，默认 50） |
| `lit_date_from` / `lit_date_to` | string? | 月级日期窗口 YYYY-MM-DD（可选，云端 0.3.94 起原生过滤） |

- **上限：queries ≤ 50**（与 `publisher_pdf_batch` 的 `MAX_BATCH_ITEMS=50` 同口径；客户端默认 8 entry/包 ≈ 40 查询）。超限直接 `rejected`。
- **不传** `review_type` / `safety`（与 search 契约相同——这两项客户端本地处理）。

## 2. 执行语义（Coze 端）

1. `route_by_mode` 新增 `batch_search` 分支 → 批量检索节点。
2. 对 `queries` **逐条**调用既有检索节点（与 search 相同的六源节点逻辑）。
3. **逐条 try/catch**：单条失败不得失败整包——该条返回 `status=error` + `error` 消息，其余条目继续。
4. 建议**并发**执行（参照 `publisher_pdf_batch`：50 条数分钟）；严格顺序亦可，客户端不依赖顺序。
5. `works` 元素格式 = search 契约的 `projects` 元素（同一 normalize 后 work schema）。

## 3. 响应

重任务必走**异步协议**（同步响应会被网关 60s 掐断）：

- 立即返回 `{"status": "accepted", "run_id": "..."}`；
- 客户端轮询 `GET /run/status/{run_id}`（既有协议：指数退避 5→30s，单次轮询超 30s 续轮，401/403 立即失败）；
- `completed` 时 `result`（或响应本体）为：

```json
{
  "results": [
    {"id": "lung_adeno_ia2", "source": "openalex", "status": "ok", "works": [/* 同 search 的 projects 元素 */], "count": 12, "total_count": 12},
    {"id": "lung_adeno_ia2", "source": "europepmc", "status": "error", "error": "rate limited"},
    {"id": "acinar_vs_lepidic", "source": "openalex", "status": "ok", "works": [], "count": 0, "total_count": 0}
  ],
  "summary": {"total": 3, "ok": 2, "error": 1}
}
```

- `results` 必须覆盖请求的**每个 (id, source)**；缺失条目客户端可检测并回退。
- **结果集过大外置 S3**：返回 `{"s3_url": "...", "results": []}`；S3 内容为上述同构 JSON（或 `{"projects": [...]}` / 裸列表——客户端三者均识别并回拉）。

## 4. 飞书审计

- `log_feishu=true` 时**每包一条汇总**（`querystr` 已携带 `batch_id` / `package` / `entries` / `n_queries`），取代逐 entry N 条噪音。
- 版本字段（`skill_version` / `coze_version`）仍按 §2.1 纪律只落 `resultstr`，不进 `querystr`。

## 5. 失败与兼容（客户端行为，供 Coze 端知悉）

| 情形 | 客户端行为 |
|---|---|
| 端点未实现 batch_search（返回 search 形态响应：有 `works`/`projects` 无 `results`，或 HTTP 400 schema 错） | 判 `unsupported` → **自动回退逐 entry 模式**（`--pack-fallback auto`，默认）或中止（`strict`） |
| 传输失败 / 轮询超时 | 重试 `--pack-retries` 次（默认 1）后按包回退逐 entry |
| 单条 `status=error` | 只回退该 entry；同包其他 entry 正常 |
| 整个 entry 无任何结果 | 回退该 entry 常规检索 |
| 401 / 403 | 立即中止（exit 3），不回退（回退同样会被拒） |
| `--from-pack` 子进程失败 | 用原命令（常规联网检索）自动重试一次 |

## 6. Coze 端验收清单

- [ ] `mode` 三分支路由：`search` / `log_only` / `batch_search`（旧两支行为零变化）
- [ ] `queries` 上限 50，超限 rejected
- [ ] 逐条 try/catch，`status=ok/error`，单条失败不拖垮整包
- [ ] `results` 按 `(id, source)` 全覆盖，`id` 原样带回
- [ ] 异步协议（`accepted` + `run_id` + `/run/status`）可用
- [ ] 大结果集 S3 外置 + 回拉契约
- [ ] 每包一条飞书汇总（querystr 落库）
- [ ] `works` schema 与 search 契约一致（同一 normalize 输出）
