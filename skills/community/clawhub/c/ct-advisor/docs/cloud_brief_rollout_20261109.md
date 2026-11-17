# ct-advisor 调用三技能：能力接口上移修改计划与部署说明

日期：2026-11-09 · 契约 `config/brief_contract.json` v1.0.0 · ct-search 端点 0.5.00
状态：**本地代码已落地并自检通过；Coze 云端包待手动重新发布，未发布前线上行为不变**

---

## 🔴 2026-11-09 晚间架构重评（当前有效状态，优先于下文）

用户裁定：客户端已解决调用 ct-safety / ct-registry 等兄弟技能的问题，可直接调用。
因此本文 15:51 拍板的「本地直连 brief 为默认主链路」**已被覆盖**：

| 项 | 本文 15:51 版 | 当前（晚间重评后） |
|---|---|---|
| 默认主路径 | cloud brief 直连 ct-search | **handoff**：代码产出 `@skill:<slug>` 卡片，客户端直接调用技能本体 |
| `CT_ADVISOR_CLOUD_BRIEF` | 默认启用 | **默认关闭**，仅显式 `=1` 时启用速览 |
| 回滚开关 | 设 `0` 关闭 | 新增 `CT_ADVISOR_HANDOFF=0`，可整条关回原执行卡 |
| 理由 | 免除「为一句速览先装三个技能」 | 技能本体已可直接调用；brief 只给非审计级速览、不产文件，默认启用反而把用户挡在完整交付物之外 |

同步位置：`config/brief_contract.json`（`switch.enabled_default=false`）·
`scripts/tool_mapping.json`（顶层 `handoff` 段、`cloud_brief.default=false`）·
`scripts/handle_need_tool.py::_client_callable()` ·
`scripts/refine_answer.py::_merge_answer(status=handoff)` ·
`scripts/orchestrate.py::build_output` · `scripts/route_tool.py::suggest_footer`。
**HARD GATE、B 档涉密边界、F33 出域红线、Coze 云端零凭据均不变。**
下文保留 15:51 的决策轨迹；凡「默认启用 / 主链路」表述一律以本表为准。

---

## 🔴 性能优化（2026-11-09 16:52 · ct-search **0.5.01**）

用户确认「频繁更新问题不大」，按 P0 + P1-1/2/3/4 全量落地，P2（换 CT.gov
REST 主源 / `async_run` 轮询）暂缓。**凭据架构完全不变**：仍在本地技能，
Coze 云端零凭据、零需鉴权外部调用；**advisor 包不用动**。

### 实测基线（优化前，串行稳态）

| source | 稳态 | 观测波动 | 瓶颈 |
|---|---|---|---|
| `advisor_literature_brief` | 17.8–18.0s | 7.7 / 13.7 / 45.7s | OpenAlex + EuropePMC **串行**；底层 `timeout=60` / `retries=3` / 指数退避 |
| `advisor_registry_brief` | 22–26s | 24 / 37 / 62s | WHO 普通 keyword 路径**必启 Playwright**（Chromium + ASP.NET 首屏 ~23s） |
| `advisor_safety_brief` | ~0.4s（端点缓存） | 11.7s | FAERS REST，非瓶颈 |

Coze 网关 stgw 有 **60s 硬顶**（ct-base §20.17）；曾观测 62s / 45.7s 已贴边。
另外 `orchestrate._fire_prefetch` 与 Coze 回答并行，用户感知是 `max(8s, brief)` 而非相加。

### 改动清单

| 层 | 项 | 做法 |
|---|---|---|
| 端点 | P1-1 并发 | `advisor_brief_nodes.py` 两源 `ThreadPoolExecutor` 并发；每任务独立 `contextvars.copy_context()` 保证 `runtime.context` 跨线程可读 |
| 端点 | P1-2 WHO 快路径 | registry 子 state 设 `who_condition`（与 keyword 同值）+ `max_pages=1`，命中 `who_search_node` **既有** `_try_http_fast_path` 纯 HTTP 路径、不启浏览器。两条路径都映射到 `txtCondition`（`who_search_node.py:674` / `:399`），语义对齐。`WHO_FAST_PATH_ENABLED=False` 可整体回退 |
| 端点 | P1-3 软预算 | `BRIEF_DEADLINE_SEC` 按 source 分档 **18 / 15 / 12s**，超时只标 `partial_sources`、保留已完成源，绝不伪装 0 命中。⚠ 线程不强杀、池有界 `max_workers=4`，属软预算；硬防线是本地分档超时 + 网关 60s |
| 端点 | P1-4 缩放 | `max_results` 由固定 `max(cap*2,30)` 改 `max(cap,10)` |
| 本地 | P0-1 分档超时 | 契约 `endpoint.per_source_timeout_sec` = 20 / 35 / 40s，取代统一 90s；超时立即回落本地执行卡 |
| 本地 | P0-2 短 TTL 缓存 | 契约 `cache` 段 TTL 600s，key = `sha256(source + 规范化 keyword JSON)`（不含每次变化的 `query_origin`）；落系统临时目录、原子覆盖不删历史；只缓存 `status=ok` 且 `partial_sources` 为空。`CT_ADVISOR_BRIEF_CACHE=0` 关闭 |

🔴 **护栏 1 未破**：所有裁剪在节点内部固定，白名单仍锁死 **8/6/6、零新增入参**；
`disclaimer` / `suggest_footer` 文案逐字未动。响应 `brief` 内新增 `perf` 诊断字段
（`mode` / `deadline_sec` / `elapsed_sec`）供部署后 A/B 确认新版本生效。

> 关于「12s 软预算」的一处工程细化：原设计写单源 12s，但 registry 走 HTTP
> 快路径标称 1–15s、literature 并发后稳态约 9–12s，一刀切 12s 会误伤稳态。
> 实装改为按 source 分档 18/15/12s，目的是**熔断 45–62s 长尾**而非砍正常请求。
> 部署后按 `--only perf` 的 `partial_sources` 出现率校准，调 `BRIEF_DEADLINE_SEC`
> 一个常量后重发包即可。

### 验证（改包前）

离线 dry-run **18/18**：并发 0.30s（非 0.60s）、contextvars 继承、超预算标 partial
且不阻塞、三 brief stub 端到端、`who_condition`/`max_pages=1`/`fetch_cap=10` 到位、
护栏常量未漂移。`test_cloud_brief` 全过、`selfcheck` **44/44**、
`cloud_brief --self-test` **26/26**。真实链路缓存对照：关闭 8.01s → 端点缓存
0.31s → 本地缓存 0.01s，结果逐字一致。

### 部署与 A/B（**必须重发 ct-search 包**）

1. 发布 `coze_deploy_bundle_<时间戳>.zip`（`COZE_VERSION=0.5.01`）；
2. 跑 `python scripts/canary_cloud_brief.py --only all` 确认全量功能回归（含 P0-2 缓存命中）全绿；
3. 跑 `python scripts/canary_cloud_brief.py --only perf` 做耗时 A/B：
   应看到 `perf.mode=parallel`（证明新包生效）、三源 `status=ok`、
   `partial_sources` 为空，且 registry/literature 耗时低于 24s / 18s 基线；
4. 若 `partial_sources` 偏高 → 调大 `BRIEF_DEADLINE_SEC` 对应档位后重发包；
   若 WHO 快路径结果集语义异常 → 置 `WHO_FAST_PATH_ENABLED=False` 回退原路径后重发包。

**回滚**：重新发布 0.5.00 包即可；本地 P0 改动与新包解耦，可独立保留或
设 `CT_ADVISOR_BRIEF_CACHE=0` 关闭缓存。

---

## 🔴 0. 最终架构（2026-11-09 15:51 用户拍板，覆盖下文 1–8 节的云端直连旧说明）

**Coze 云端只保留单纯的代码调用，不持有任何共享凭据、不发起需凭据的外部调用；
凭据与调用点全部收敛到本地技能 / 工作台。** 这是家族既有范式：本地技能持
`ct_advisor_coze` 调用 advisor Coze 端点，Coze 包内并不持有该凭据。

| 项 | 最终形态 |
|---|---|
| 凭据位置 | **仅** `ct-advisor/adapters/coze_token_embedded.py::EMBEDDED_SECRETS["ct_search_coze"]`（工作台同理）；真源 `ct-registry/adapters/endpoint_token.py::coze_unified` |
| Coze 包内 | 零凭据 blob、零混淆密钥、零 token 读取、零需鉴权外部 HTTP；`src/search_token.py` 与 `cloud_brief_node.py` 已移入 `_archive/`（可逆，pack.py 排除该目录） |
| graph.py | `tool_router` 命中后一律 `need_tool → END`，回到纯代码判定路径 |
| 主链路（15:51 版，已被文首重评覆盖） | 本地 `scripts/cloud_brief.py` 直连 ct-search（当时默认启用），`handle_need_tool` 分流 + `orchestrate._fire_prefetch` 并行预取，本地确定性缝合；**当前默认主路径为 handoff** |
| 开关（已被文首重评覆盖） | `CT_ADVISOR_CLOUD_BRIEF` 当时默认启用；**当前默认关闭**，仅 `=1` 显式开启。云端开关 `cloud_brief_enabled` 已作废 |
| 平台配置 | **无需任何 Coze 控制台环境变量或输入变量**（此前卡住的 `cloud_brief_enabled` 开始节点声明问题自然消失） |
| 凭据轮换 | 只改本地技能 + 更新本地发布物，**无需重打包 / 重发 Coze 包**；SOP 见契约 `credential_governance` 段与源码注释 |

> 下文 1–8 节记录的是 15:51 之前的「云端直连」方案，作为决策沿革保留；
> 与本节冲突处一律以本节为准。

---

## 1. 结论与架构决策

**需要调整的是 ct-advisor 的调用层，不是三个技能本体。** 现状链路是 2026-08-14 的
`need_tool` 执行卡：Coze 判定工具 → 落回本地技能 CLI → 本地 CLI 再上云取数 →
结果回本地计算/写文件/读产物 → 缝合。而三个技能的取数层与部分计算层在这半年里
已陆续上移到 `ct-search.coze.site`，advisor 的调用路径没跟上，形成四次跨域与
「必须本地安装三个技能」的隐含依赖。

本次把 **执行位置** 上移到 Coze，分两层：

| 层 | 内容 | 归属 |
|---|---|---|
| L1 能力层 | `ct-search` 端点内新增 3 个聚合 source，进程内复用既有节点取数 | ct-registry/adapters/coze |
| L2 产品层 | 三个技能保留交付物 / 确认门 / 独立发布 / 合规边界；advisor 只做路由 + 综合成文 | 原样不动 |

**共享实现 ≠ 产品替代。** 三条护栏确保 brief 只暴露「单轮、确定性、无状态、纯文本可表达」的
速览切面；需要 XLSX/HTML、SAFE PREVIEW 确认门、多轮协商、批量、本地数据导入、审计留痕的
场景仍归三个技能，并由 `suggest_footer` 明确导流。

治理依据：`ct-base §20.19.5` 范畴说明「检索族端点内 source 级上移 ≠ 跨族后端合并」；
`§20.19.7` 红线 2「合并不取消本地引擎」；红线 3「新增节点必须同步契约 + 版本归因 +
CHANGELOG」。`§20.19.5` 实例表「不合：ct-registry / advisor / literature / safety」否决的是
**跨族后端合并**，本次是端点内扩展 + 端点间调用，不触碰该判定。

---

## 2. 改动清单

### 2.1 新增文件

| 文件 | 作用 |
|---|---|
| `ct-advisor/config/brief_contract.json` | **契约单一真相源**：3 个 source 的参数白名单、响应 schema、三条护栏文案、开关、回落链、出域边界 |
| `ct-advisor/scripts/cloud_brief.py` | 本地薄客户端：信封构造 / 白名单过滤 / HTTP / 三护栏校验 / 确定性渲染 / `--self-test` |
| `ct-advisor/scripts/test_cloud_brief.py` | 跨仓一致性自检（AST 断言契约 ⇄ 云端内嵌副本 ⇄ tool_mapping 逐字一致） |
| `ct-advisor/adapters/coze/src/graphs/nodes/cloud_brief_node.py` | advisor 云端工作流直连节点：开关 + 白名单 → 调 ct-search → 缝合；失败 pass-through |
| `ct-registry/adapters/coze/src/graphs/nodes/advisor_brief_nodes.py` | 3 个 brief 聚合节点：进程内复用 `who` / `chinadrugtrials` / `faers` / `openalex` / `europepmc`，纯 stdlib 聚合，零重复取数实现 |
| `ct-advisor/docs/cloud_brief_rollout_20261109.md` | 本文档 |

### 2.2 修改文件（均为增补，无删除、无裁剪）

| 文件 | 改动 |
|---|---|
| `ct-registry/adapters/coze/src/graphs/sources.py` | 白名单登记 3 个 `advisor_*_brief` |
| `ct-registry/adapters/coze/src/graphs/nodes/search_node.py` | 3 个懒加载分支（fail-closed 由既有 `normalize_source` 承担） |
| `ct-registry/tests/coze_cases/_contract_index.json` | 3 条契约 + `coze_version` 0.5.00 + 版本历史 + 新增红线 |
| `ct-registry/adapters/coze/coze_contract.md` | 由 `gen_contract_doc.py` 重新生成（禁手改） |
| `ct-registry/adapters/coze/src/graphs/nodes/_version.py` | `COZE_VERSION` 0.4.02 → 0.5.00，顺带收敛索引/代码版本漂移 |
| `ct-registry/adapters/coze/AGENTS.md` | 版本常量处 `0.4.00` → `0.5.00` |
| `ct-registry/CHANGELOG.md` / `ct-advisor/CHANGELOG.md` | 版本归因 |
| `ct-advisor/adapters/coze_token_embedded.py` | 新增 `ct_search_coze` 共享公开凭据 blob + `get_search_token()`；本地不再依赖 ct-registry 已安装 |
| `ct-advisor/scripts/tool_mapping.json` | 新增顶层 `cloud_brief` 路由/开关段；**三个 `engine: local` 原样保留** |
| `ct-advisor/scripts/handle_need_tool.py` | `execute_card` 在档位门之前加 cloud brief 分流；失败回落原执行卡 |
| `ct-advisor/adapters/coze/src/graphs/state.py` | `GraphInput` / `GlobalState` 加 `cloud_brief_enabled`（默认 false）；新增 `CloudBriefInput/Output` |
| `ct-advisor/adapters/coze/src/graphs/graph.py` | import 新节点；`route_after_tool_router` 加 `cloud_brief` 出口；`add_edge("cloud_brief", END)` |

---

## 3. 三条护栏（可执行约束）

| # | 约束 | 落点 |
|---|---|---|
| 1 | **参数白名单锁死 8/6/6 键**，禁止扩张到 L0–L4 / PICO / batch / 本地导入 / 文件产出 | 契约 `param_allowlist`；云端节点未知键 `PARAM_NOT_ALLOWLISTED` fail-closed；本地发送前二次过滤；`test_cloud_brief.py` 断言与 `tool_mapping.json` 三方一致 |
| 2 | **速览、非审计级**：只回结构化 JSON，不产 XLSX/HTML，响应强制 `disclaimer` | 云端 `_guard_fields()` 对 ok/error 信封都写；本地 `validate_response()` 缺失即判违约回落 |
| 3 | **suggest_footer 导流**：响应强制 `suggest_skill` + `suggest_text` | 同上；渲染时原样附在答案末尾，把要文件/审计/多轮的用户送回三个技能 |

---

## 4. 开关与回落链

两个开关**相互独立、默认都关**，便于灰度：

| 开关 | 位置 | 控制 |
|---|---|---|
| `CT_ADVISOR_CLOUD_BRIEF` | 本地 env | `handle_need_tool` 是否走本地直连速览通道（**当前默认关闭 / opt-in**）。另见 `CT_ADVISOR_HANDOFF`（默认开，设 `0` 回到原执行卡） |
| `cloud_brief_enabled` | advisor 云端 `GraphInput` | `tool_router` 命中后是否路由到云端 `cloud_brief` 节点 |

回落链（任何一环失败都不伪造数据、不静默降级）：

```
cloud brief status=ok 且三护栏齐备 → 缝合交付
  ↓ 开关关闭 / 未部署 / 无凭证 / query_origin 缺失 / 超时 / async accepted /
    status=error / 契约违约
本地 need_tool 执行卡（§20.19.7 红线 2）
  ↓ 技能未安装 / 执行失败
Coze 草稿 + 明确标注「未取数」（既有行为，未改动）
```

**出域红线**：`doc_context` 只走 `ct-advisor.coze.site`，绝不进入 ct-search 信封；
`query_origin` 由本地客户端生成并两层透传，服务端禁止兜底生成（ct-base §8.6）。

---

## 5. 部署顺序（必须由维护者在 Coze 控制台执行）

> 🔴 **本地代码改动不会自行生效。** 两个 Coze 云端包需要手动重新打包发布；
> 在步骤 1–3 完成前，所有开关默认关闭，线上行为与改造前逐字一致。

1. **部署 ct-search 0.5.00**：`ct-registry/adapters/coze` 打干净 zip + MD5 校验后重新发布。
   先 canary 三个新 source（各发一个最小 `keyword` JSON 请求），确认返回
   `status=ok` 且 `brief` / `disclaimer` / `suggest_*` 齐备。
2. **部署 ct-advisor 云端工作流**：`ct-advisor/adapters/coze` 重新发布即可。
   包内**不含任何凭据**、不发起需凭据的外部调用；无需配 `CT_SEARCH_TOKEN`、
   无需在「开始节点」声明 `cloud_brief_enabled`。取数由本地技能完成。
3. **灰度云端开关**：少量请求把 `cloud_brief_enabled=true` 放进 `query_meta` 同级入参，
   观察 `final_answer` 末尾速览段与 `need_tool=None`；异常时直接关开关即回滚。
4. **可选灰度本地开关**：`CT_ADVISOR_CLOUD_BRIEF=1`，验证本地兜底直连通道。

打包纪律见 `ct-registry/adapters/coze/scripts/pack.sh` 与 `ct-advisor/adapters/coze/scripts/pack.py`；
`coze_contract.md` 必须经 `gen_contract_doc.py` 重生成，禁手改。

---

## 6. 验收清单

```bash
# 跨仓一致性（AST 断言 + 语法编译 + 薄客户端离线自测）
C:/Tools/Anaconda3/python.exe ct-advisor/scripts/test_cloud_brief.py

# 薄客户端离线自测（单独跑）
C:/Tools/Anaconda3/python.exe ct-advisor/scripts/cloud_brief.py --self-test

# 只看信封，不触网
C:/Tools/Anaconda3/python.exe ct-advisor/scripts/cloud_brief.py --dry-run \
    --tool ct-safety --params '{"drug":"aspirin","event":"hepatic failure"}'

# ct-search 端点离线自检：A1/A2 断言白名单 ⇄ 分支严格一致
C:/Tools/Anaconda3/python.exe ct-registry/adapters/coze/scripts/selfcheck.py

# 重生成契约文档（禁手改）
C:/Tools/Anaconda3/python.exe ct-registry/tests/coze_cases/gen_contract_doc.py
```

部署后线上 canary：三个 source 各一次最小请求；确认 `brief_kind` 正确、
`param_allowlist` 回显一致、`disclaimer` 与 `suggest_text` 逐字一致；
再模拟「关开关 / 断凭证 / 强制 error」三种回落，确认 `need_tool` 执行卡仍原样返回。

---

## 7. 回滚

| 场景 | 动作 |
|---|---|
| 只想停新链路 | **当前默认即关闭**；若显式开过 `CT_ADVISOR_CLOUD_BRIEF=1`，unset 即可回到 handoff（设 `CT_ADVISOR_HANDOFF=0` 再回到原执行卡），**无需改代码** |
| 云端包有问题 | 回滚 Coze 控制台上一版本部署包；本地代码不需要动 |
| 需要彻底移除 | 三个技能 `engine: local` 与 `handle_need_tool` 原路径完整保留，删掉 `cloud_brief` 分流块 + 两个开关 + 三个 source 即可；无需迁移数据 |

---

## 8. 明确不做 / 待拍板

| 项 | 说明 |
|---|---|
| 不删本地引擎 | 按 §20.19.7 红线 2 保留。但 `ct-safety v0.9.9` 曾按用户要求移除本地降级路径，与红线 2 口径不一致；**本次按红线 2 执行，若需改为无回退请单独拍板** |
| 不做跨族后端合并 | §20.19.5 已判「不合」；本次是端点内 source 级扩展 + 端点间调用 |
| 不重构两套路由规则表 | `check_route_drift.py` 检出的本地 `route_tool.py` ⇄ 云端 `tool_router_node.py` 漂移属独立行为变更工作项，需人工决策；本次只新增 brief 白名单一致性门禁 |
| 不产文件 | advisor 交付边界仍是纯文本；XLSX/HTML 归三个技能 |
| 不做异步轮询 | 本地/云端 brief 通道遇 `status=accepted` 直接回落执行卡；长任务仍走既有 `ct-safety/adapters/coze_dispatch.py` 的轮询链路 |
| 无法代发布 | 两个 Coze 云端包的重新发布、环境变量配置与线上 canary 必须由维护者在 Coze 控制台完成 |
