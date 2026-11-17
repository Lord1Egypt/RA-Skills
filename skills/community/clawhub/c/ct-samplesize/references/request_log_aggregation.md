# 请求级日志聚合 / Request-level log aggregation（v5.15.0 · 2026-11-15）

> 驱动数据：ct-update 只读端口 `feishu_log_fetch.py --skill ct-samplesize --days 30`，
> 2026-10-17 19:53 ～ 11-12 14:45 CST，252 行 searchlog / 52 会话 / 50 个来源。
> 分析见工作区 `ct_samplesize_usage/ct-samplesize_使用行为分析与改进建议.md`。

## 1. 问题

| 现象 | 实测 |
|---|---|
| 一次用户需求被拆成多个 Coze 请求 | 45/45 的 `power` 调用在 2 分钟内紧接同检验的 `n` 调用；`meta_planning` 单会话 40 次 / 27.8 分钟、37 次 / 9.2 分钟的参数扫描 |
| 每个 POST 各写一行飞书 | 252 行 / 52 会话；60s 内同签名重复 25 行（9.9%），浪费 91.8s |
| 失败后被盲目重试 | `correlation effect=2.0` 越界，一个来源 2 分钟内逐字节重试 4 次，全部 `f.lower = f(lower) is NA` |
| 一个 POST 内部还可能追加写行 | 批量已合并为 1 行，但 `/run_upload` 附件归档走 filelog 另表；老客户端胖信封（136 键）把单行撑到 ~2.8KB |

根因：日志以「Coze 请求」为建档单位，而不是以「用户需求」为单位。

## 2. 设计

**客户端**：`adapters/coze_client.py`

- `request_scope()`：一次需求的所有子调用共享一个 `request_id`，`call_seq` 递增。CLI
  `scripts/samplesize_power.py::main()` 已自动包裹整条命令；工作台/编排层可自行包裹。
- `call_paired(test, params)`：一次 POST 同时返回「所需 n」与「该 n 下实际 power」
  （服务端 `mode="paired"` 在 `samplesize_node` 内连算两向）。替代 45 组成对调用。
- `call_grid(test, base, variants)` / `call_batch(specs)`：参数扫描一次 POST 返回全部，
  服务端 `ThreadPoolExecutor` 并行（替代逐项串行，实测批量 p50 10.39s ≈ 2×单条）。
- `call()` 内置 60s 同签名成功结果本地复用（`CTSS_LOCAL_DEDUP_TTL`）：不新开 POST、
  不新写飞书行；失败结果不缓存，用户修正后可立即重试。
- `validate_domain()`：出站前按契约 `ranges` 拦截越界参数（如 `correlation |r|<1`），
  返回双语可行动错误信封，**零网络往返**。
- `normalize_legacy_params()`：兼容 `delta/sd/sides` 等 5.8.0 老参数名。

**Coze 端**：`adapters/coze/src/graphs/nodes/log_aggregator.py`

- `aggregate_log()`：同一 `request_id` 首次 `add_records` 建行，后续 `update_records`
  更新同一行；行内聚合 `call_count` / `calls[]`（前 5 次保留裁剪后 params，之后只存
  sha256 摘要）/ `statuses` / `errors` / `total_runtime_sec` / `last_result`。
- 超过 `CTSS_LOG_AGGREGATE_WINDOW`（默认 300s）或 `CTSS_LOG_MAX_CALLS`（默认 20）
  才另起一行 → 一次需求通常 **1 行**，长会话也只产生「很少数几行」。
- 兼容红线：无 `request_id` → `delegate` 回原 `write_feishu_log`（老客户端零行为变化）；
  `log_mode=skip` 不写；`log_mode=always` 强制逐次追加；`update` 失败自动降级追加，
  绝不丢日志、绝不阻断主流程；进程重启从新行重新聚合（最多多一行，不覆盖历史）。
- `CTSS_LOG_REQUEST_ID_COLUMN=1` 时额外把 `request_id` 写入独立列，便于按需求检索/治理。

`main.py::/run` 在客户端未带时按 `x-ctss-request-id` / `x-request-id` / `x-run-id`
顺序补 `request_id`，让老客户端也能通过网关头参与合并。

### 契约加载：为什么不放「兜底副本」

初版曾让 Coze 侧按 `Path(__file__).parents[N] / "config" / "log_contract.json"`
探测文件，于是担心「Coze 可能只把 `src/` 挂到 sys.path」而想再加一份 `src/config/`
兜底 —— 这是用副本掩盖布局假设，每多一份就多一处漂移与部署故障点。已彻底改为：

- `scripts/build_log_contract.py` 把契约**烘焙成 Python 常量模块**
  `src/graphs/nodes/log_contract_data.py`，与 `log_aggregator.py` 同属 `graphs.nodes` 包；
- `log_aggregator` 顶部 `from graphs.nodes.log_contract_data import CONTRACT`，
  **零文件 IO、零路径探测、零 `parents[N]` 假设**；部署目录怎么挂都不影响加载；
- 漏带模块 → 启动时立即 `ImportError`（可发现的部署错误），不再静默降级；
- 生成期用 `ast.literal_eval` 自检常量与本地 JSON 语义一致，单测断言
  「Coze 侧无任何 JSON 冗余副本」。

三个产物分别属于三个**不同部署单元**（本地技能 / 工作台 / Coze 服务端），
各自只带一份；同一单元内绝无第二份。

## 3. 同步落地的 9 项改进

| 编号 | 改动 | 位置 |
|---|---|---|
| P0-1 | 契约按消费者加载方式各产出一份：本地客户端 `config/log_contract.json`、工作台 `workbench/publish/config/log_contract.json`、Coze 运行时 `src/graphs/nodes/log_contract_data.py`（Python 常量，`log_aggregator` 直接 import，**零路径探测 / 零防御性副本**）；契约缺失时客户端按默认值表 fail-closed 裁剪；服务端落库前二次裁剪 | `scripts/build_log_contract.py`、`adapters/coze_client.py`、`log_contract_data.py`、`log_aggregator.trim_params` |
| P0-2 | 客户端 + 服务端双端参数域校验；R 端 `.translate_engine_error`（v5.13.31+）保留为最后防线 | `validate_domain()` ×2、`feishu_save_node` |
| P1-3 | `call_paired` / 服务端 `mode="paired"` | `coze_client.py`、`samplesize.py` |
| P1-4 | `cache_hit` 镜像进 `resultstr`、批量 `cache_hits`、默认组合懒预热（`CTSS_PREWARM=1`）、本地 60s 去重 | `samplesize.py`、`coze_client.py` |
| P1-5 | 批量项并行（`CTSS_BATCH_WORKERS`，默认 4）+ `call_grid` | `samplesize.py`、`coze_client.py` |
| P1-6 | `entry_point` / `call_type` / `call_seq` / `cache_hit` / `error_type` / `request_id` / `is_qa` 镜像进 `resultstr` 顶层（绕过 download 不投影独立列的限制） | `feishu_save_node.py`、`state.py` |
| P2-7 | `scripts/route_intent.py`：方案段落 → 候选检验、`handoff_hint()`（ct-advisor 交接）、按真实频次排序的 `menu_order()` | `route_intent.py`、SKILL.md |
| P2-8 | `assumption_block()`：关键假设 + 来源 + `unverified` 提示写入日志与 paired 结果 | `log_aggregator.py` |
| P2-9 | 版本落后非阻塞提示、旧参数名兼容、未知 `test` 跨域脏流量不写主表 | `upgrade_hint()`、`normalize_legacy_params()`、`is_known_test()` |

## 4. 验证

- `python -m py_compile` 全量 11 个改动文件通过。
- `python tests/test_request_log_aggregation.py` → **37/37 PASS**（含 FakeBitable 离线断言
  「5 次子调用 = 1 行 add + 4 次 update」「3 次且上限 2 → 2 行」「无 request_id 零行为变化」
  「130 键 → 11 键」「correlation effect=2.0 被拦」「request_scope 同 ID / seq 递增」）。
- `python scripts/build_log_contract.py` 重建三份产物（两个 JSON + 一个 Python 常量模块），生成期 `ast.literal_eval` 自检常量与 JSON 语义一致；单测断言 Coze 侧无任何 JSON 冗余副本。
- CLI `--help`、`route_intent.py` 实跑通过（无网络、无写入）。

## 5. 未做（需单独授权）

- **未部署 Coze 端点**、**未写回飞书**、**未 git commit / push / 三平台发布**。
  服务端改动须重新打包部署后才在线上生效；在此之前线上仍是旧行为。
- 未清理历史 252 行日志（治理写回默认 dry-run，且需明确授权）。
- `download` 端口的 `entry_point` / `request_id` 列投影属 ct-update 侧，本技能只做
  `resultstr` 镜像，未改 ct-update 文件。

## 6. English summary

One user request used to fan out into many Coze POSTs (n→power pairs, grid sweeps, blind
retries), and each POST wrote a Feishu row. v5.15.0 attaches a `request_id` to all sub-calls
of one demand; the Coze `feishu_save` node merges them via `update_records` into a single row
(first `add_records`, then in-place updates). `call_paired` / `call_grid` collapse common
workflows into one POST; a 60-second local dedup cache and pre-flight domain validation remove
redundant and doomed requests entirely. Legacy clients without `request_id` keep the exact
old behaviour. All edits are local-only: nothing was deployed, published, or written back to
Feishu.
