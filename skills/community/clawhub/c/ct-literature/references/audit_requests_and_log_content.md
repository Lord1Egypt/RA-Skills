# ct-literature 请求数与飞书写入内容综合审计

> 审计日期：2026-11-14 · 范围：技能本地代码（`ct-literature/scripts`、`adapters`）
> + Coze 远端代码（`ct-registry/adapters/coze/src/graphs`）
> 实证窗口：飞书 searchlog 2026-10-15 → 2026-11-13，650 行（全部为治理前数据）
> 本文是**评估 + 本轮补齐说明**；代码改动见第 6 节，验收口径见第 9 节。
> **0.5.09 收尾（2026-11-14，用户确认后落地）**：第 8 节两项待确认项已全部闭环——
> ① Coze 端 B 类补 `ok_urls` / `failures` 逐项明细 + 异常路径留痕；
> ② 本地缓存命中由「完全不留痕」改为「一条轻量 `cache_hit` 行」，恢复每需求至少一条。
> 本轮改动与验证见第 10 节；**0.5.09 部署包已重打，仍未部署**。

---

## 1. 结论先行

| 问题 | 判定 |
|---|---|
| 本地重复发起请求 / Coze 端快速反复写入是否已被抑制？ | **基本是**。结构性双写 264 行（40.6%）已从三层（客户端护栏 / request_id 透传 / 云端 upsert）堵住；本轮又补掉「缓存全命中仍发 1 次纯计算请求」的最后一处放大点。 |
| 每个需求是否只发起尽量少的客户端请求？ | **首次 7 次 → 其中 5 次功能必需、2 次可优化；重复需求 0 次**。本轮把 1 次可优化（lit_prisma）消除；剩 `log_only` 纯留痕 1 次（缓存命中时已跳过）。 |
| 是否写入尽量完整的一条记录？ | **条数上达标**：一次需求 1 行汇总（若下载 PDF 再 1 行下载记录，按 `request_id` 关联、`dedup_scope` 隔离防误合并），缓存命中也恒有 1 行轻量记录；**内容上原本严重不足**，A 类已补 11 类字段，B 类 0.5.09 补逐项明细。 |
| 飞书写入内容是否足够有效信息？ | **治理前判定「信息稀薄」**：单条平均 9.9 个有效字段、仅 17.2% 记录含任一关键信号；检索参数、答案/产物引用、缓存信号、结构化错误码覆盖率**全为 0%**。A 类已补 11 类字段；B 类 0.5.09 补成功产物 URL 与逐 link 失败原因。 |

一句话：**条数治理与信息治理均已闭环；第 8 节两项待确认项按用户确认并入 0.5.09 落地，剩余未闭环项只剩部署与编排层。**

---

## 2. 一次用户需求的完整请求链路（默认 online 配置）

按 `ct_literature.py` 551–581 的默认开关离线复刻（5 个源启用：`OpenAlex / EuropePMC / bioRxiv / medRxiv / PubMed`；`semantic_scholar / arxiv / prospero` 默认关闭）：

| # | 出站点 | 次数 | 是否功能必需 | 治理后状态 |
|---|---|---|---|---|
| 1 | 各源检索 `fetch_source → dispatch`（并行） | **5** | ✅ 必需，每源一个端点 | 缓存全命中时 0 次（`resolve_cache_file` 跨运行共享） |
| 2 | `lit_prisma` 机器初筛 | 1 | ❌ 纯计算、零 IO，本地等价 | **本轮修复**：缓存命中 run 强制走本地 → 0 次 |
| 3 | `lit_rrf` 跨源融合 | 0 | ❌ 纯计算（默认 `rank=cited` 不触发） | 同上，`--rank rrf` 且缓存命中时走本地 |
| 4 | `log_only` 汇总留痕 | 1 | ✅ 「每需求至少一条记录」所需 | 首次写全量 A 汇总；**0.5.09 起缓存命中改写一条轻量 `cache_hit` 行** |
| 5 | `publisher_pdf_batch` | 0（默认 `download_pdf=False`） | ✅ 按需，一次批量只发 1 次 | 开启时 1 次，不再逐 link 发 |
| | **合计** | **7** | | **缓存全命中 → 1 次 Coze 端点请求（纯留痕，0 次检索）** |

> 口径说明：`verify_citations.verify_one` 仍会访问 DOI / PMID / OpenAlex 等**外部数据源 API**（反幻觉正确性所需），不计入上表的 Coze 端点请求数。缓存命中时这部分依然执行——这是「客户端请求」与「Coze 端点请求」的区别，不能混为一谈。
>
> 附带发现（未改，待核实）：`ct_literature.py:574-577` 的注释称 PubMed「`coze_routable=False`、独立车道」，但 `SOURCE_REGISTRY['PubMed']` 实测为 `coze_routable=True`，因此默认遍历已挂载 PubMed 一次；577 行 `if with_pubmed` 是冗余的二次挂载条件。云端 0.3.97 确有 pubmed 节点，故注册表取值合理，属**注释与分支过时**，不影响本轮结论，但应另行清理以免误判请求数。

### 请求数收敛矩阵

| 场景 | 治理前 | 上一轮治理后 | 本轮治理后 |
|---|---|---|---|
| 首次需求 | 7 次 Coze + 全量外部 API | 7 次 Coze | 7 次 Coze（5 必需 + 1 prisma 已本地化 + 1 留痕）→ 实际 **6 次** |
| 同需求重复（TTL 内，隔时重跑） | 7 次全部重跑（缓存绑 `out_dir`，从不跨运行命中） | 5 源跳过，但 `lit_prisma` 仍发 1 次 → 1 次 | **1 次 Coze**（0.5.09：纯留痕 `cache_hit` 行，0 次检索） |
| 上游同请求触发两轮 run | 2×7 = 14 次 | 第二轮全缓存命中 → 1 次 ×2 | 第二轮 **0 次 Coze**（P3 护栏 5s 窗口抑制） |
| 编排层 `CT_REQUEST_ID` 贯穿 | 未落地 | 未落地 | 仍未落地（属 ct-advisor / 工作台，见第 8 节） |

> **0.5.09 口径修正必须讲清**：把「缓存命中 0 次请求 / 0 行」改成「1 次请求 / 1 行」是用户 2026-11-14 明确确认的合规取舍——**用 1 次纯留痕请求换「每需求至少一条记录」**。请求数从 0 回到 1，但仍是理论最小（本地无飞书凭据，任何落库都必须经 Coze `log_only`）；且两类 payload 共用 P3 稳定键护栏，同请求两轮 run 仍恒 1 行，**不放大存储**。

---

## 3. 飞书写入条数收敛评估

| 层次 | 机制 | 落点 | 效果 |
|---|---|---|---|
| 上游双写 | 同请求触发两轮、各生成新 `uuid4` | 编排层 | 实测日双写率多日精确 50.0%，间隔 p50 385ms |
| P0 | `request_id` 接口闭环 | 本地 `dispatch` / `dispatch_stream` / `fetch_source` / `PdfDownloader` + payload 顶层 | 此前签名不接受该参数、payload 从未携带 → 已修，云端真正收得到 ID |
| P2（0.5.09 修正） | 缓存命中改**轻量留痕** | `ct_literature.py` `_fresh_fetches` / `_n_jobs` / `_cache_only` | 全命中 run 写 1 条 `cache_hit` 行而非全量 A 汇总，恢复「每需求至少一条」；`CT_LIT_LOG_ON_CACHE_HIT=1` 可改回全量 |
| P3 | 本地写前幂等护栏 | `adapters/feishu_write_guard.py` | 业务载荷指纹 + 5s 窗口原子 claim、排他锁、失败 `release()` 允许重试、fail-open |
| 云端 A 类 | `feishu_write_node` 0.5.07 已完整 | Coze 端 | `field_name` 修正 / 自动建列 / `_dedup_probe` / TOCTOU 单飞 / 确定性 keeper 收敛 |
| 云端 B 类 | 0.5.08 纳入去重 | `publisher_pdf_batch_node` | 原先裸 `add_records`，112 行全部绕过去重；现 `_write_to_feishu(..., dedup_scope="publisher_pdf_batch")` |
| A/B 隔离 | `dedup_scope` | `feishu_write_node` | 防同 `request_id` 的 A 汇总与 B 下载被 `_merge_prefer_richer` 混进一行 |

**量化结论**：治理前 650 行 → 结构性双写 264 行（40.6%）+ 跨时间重复提交 80 行；理论可压缩 344 行（52.9%）→ 306 行。修复后一次需求写 **1 行 A 汇总或 1 行轻量 `cache_hit`（+1 行 B 下载，若启用 PDF）**；同请求两轮 run 由 P3 护栏 + 云端 upsert 收敛为 1 行。隔时同参重跑按 0.5.09 新口径写 1 行 `cache_hit`，不再 0 行。

> ⚠️ 一个必须讲清的修正：上一轮的「缓存跨运行共享」**不减少飞书写入**——`_cache_wrap` 只包住检索 `jobs`，汇总留痕在 `run()` 末尾 `if online:` 独立执行。缓存省的是 Coze 检索配额与延迟，不是行数；真正压行数的是 P2 / P3 / 云端 upsert。

---

## 4. 飞书写入内容完备性评估（本轮核心）

### 4.1 治理前实测（`stat_field_coverage`，650 行）

| 指标 | 实测 | 判定 |
|---|---|---|
| 单条记录平均有效字段 | **9.9 个** | 稀薄 |
| 含任一关键信号的记录 | **17.2%** | 稀薄 |
| 分级 | **信息稀薄** | — |

分桶：

| call_type | 行数 | 平均有效键 | querystr 键数 | resultstr 键数 |
|---|---|---|---|---|
| `literature_summary`（A） | 534 | **9.0** | 6 | 4 |
| `publisher_pdf_batch`（B） | 112 | 14.0 | 8 | 7 |
| unknown | 4 | 5.5 | 3 | 3 |

**A 类（占 82.8% 流量）最成问题**：`querystr` 只有 `type / topic / query / sources_ok / sources_fail / hits_merged`；`resultstr` 只有 `runtime_sec / skill_version / coze_version`（`log_only` 被 Coze 端刻意不写 `status/ok/total/s3`，避免谎报 0 命中）。也就是说，**主记录里没有任何结果侧信息**。

### 4.2 四类关键缺口（覆盖率全为 0%）

| 类别 | 缺失字段 | 后果 |
|---|---|---|
| 检索可复现性 | 年份窗口、`review_type`、`safety`、`max_results`、`cochrane`、`rank`、`verify_mode`、启用源列表 | 审计表无法回答「这次用了什么条件」，记录不可复现、结果差异无法解释 |
| 结果可回溯性 | `answer_hash`、`artifact_ref`、`answer_text`、`_coze_full`、真实产物 URL | 无法回答「给用户返回了什么」；重复调用是否同答无从判定；`s3` 有效率 0%（17.2% 只是布尔 False 占位） |
| 治理可观测性 | `cache_hits`、`fresh_fetches`、`token_usage` | 前几轮做的缓存治理与写放大治理**无法从飞书验证收益** |
| 失败可归因 | `error_type`、`error_code`、失败源明细 | 失败信号只能靠 `querystr` 数值反推（见 §3.5 指标型失败），无法自动聚类 |

另有 `call_type`（0%，A/B 混算稀释统计）、`request_id` / `entry_point` 独立列（0%，0.5.08 部署后才有）、`memo`（100% 空，应从 schema 移除或真正启用）。

### 4.3 判定

**条数收敛 ≠ 记录可用。** 治理前的一条 A 类记录，既不能复现检索、也不能回溯答案、更不能验证本轮所有治理措施的真实收益——只够回答「谁在什么时候查了一个什么主题、大概命中几条」。对临床文献检索这种需要可追溯、可复盘的技能，这是明显不足。

---

## 5. 本轮补齐的信息字段（A 类，本地可控、纯增量）

`_summary_payload` 新增（不新增飞书列、不改 Coze 端契约、不影响 `resultstr`）：

| 字段 | 用途 |
|---|---|
| `params` | 完整检索参数组：`year_from/year_to/date_from/date_to/review_type/safety/max_results/cochrane/include_reviews/rank/prisma/verify_mode/sources_enabled` |
| `sources_requested` / `sources_failed` | 请求源数 + **失败源名列表**（原来只有数字，无法定位哪个源挂了） |
| `cache_hits` / `fresh_fetches` | 缓存治理效果的直接观测位 |
| `answer_hash` | `works` 内容 md5 前 16 位，判定同参重跑是否同答 |
| `artifact_ref` | 主产物文件名，可回溯交付物 |
| `summary_status` | `ok / empty / partial / error`（补 `log_only` 刻意留空的 `status`） |
| `error_type` / `error_code` | `source_fetch_failed` + `LIT_SRC_ALL_FAILED / LIT_SRC_PARTIAL` |

配合新增的诊断能力：`feishu_log_fetch.py` §3.7「写入内容信息完备性」把上述 12 个关键信号做成可量化、可落 JSON 快照的巡检指标（`grade` 分为信息稀薄 / 基本可用 / 较完整）。

### 🔴 一个必须同步处理的连带风险（已修）

P3 护栏原先用「`_summary_payload` 全量减 `request_id`」做业务载荷指纹。新字段里 `cache_hits` / `fresh_fetches` 在两轮重复 run 中必然不同（第一轮 fresh=5、第二轮 fresh=0），`artifact_ref` 也可能因带时间戳的 `out_dir` 而变——若沿用旧口径，**两次 run 指纹不同 → 护栏失效 → 40.6% 结构性双写复发**。

故把护栏指纹改为**稳定键白名单**：`type / call_type / topic / query / params`（用户输入 + 检索参数 + 常量，两轮必然相同）。这是「补信息」与「防双写」之间的必要耦合，单独改任一侧都会出事。

---

## 6. 本轮代码改动清单

| 文件 | 改动 |
|---|---|
| `ct-literature/scripts/ct_literature.py` | `import hashlib`；A 类汇总补 11 类上下文字段；护栏指纹改稳定键白名单；新增 `_pure_local_on_cache` 判定；**0.5.09**：缓存全命中改写轻量 `cache_hit` 行（源成败取真实 `_p_ok`/`_p_fail`） |
| `ct-literature/adapters/_coze_lit_pipeline.py` | `rrf_fuse` / `prisma_screen` 增 `prefer_local`，缓存命中 run 直接走本地纯计算引擎 |
| `ct-update/scripts/feishu_log_fetch.py` | 新增 `stat_field_coverage()`、§3.7 章节、JSON 快照 `field_coverage`；**0.5.09**：SIGNAL_FIELDS 补 `cache_hit` / `ok_urls` / `failures` |
| `coze .../publisher_pdf_batch_node.py` | **0.5.09**：`_build_item_details()` 投影 `ok_urls` / `failures`；`_fire_and_forget_feishu_log` 增 `items`；正常 + 异常两处调用点 |
| `coze .../nodes/_version.py` | **0.5.09**：末尾追加本轮说明（保留并行改动线段落，未覆盖） |
| `coze .../scripts/selfcheck_pdf_dedup.py` | **0.5.09**：扩至 43 项，含跨技能静态断言 T14a–d |
| `coze .../AGENTS.md` | 版本表 / 回归清单 / 部署包欠账 / 两条改动线验收提示 |
| `ct-literature/references/audit_requests_and_log_content.md` | 本文 |

**Coze 端代码在最早的评估轮（0.5.08 之前）确未改动**，理由见第 8 节；但用户
2026-11-14 确认两项待办后，0.5.09 已改 Coze 端（上表 4 行）。因此本节清单以
**0.5.09 最终态**为准，§8 第 1 项的删除线即指此。

---

## 7. 关于「写入尽量完整的一条记录」的设计权衡

用户期望「一次需求 → 一条完整记录」，当前实际是 **最多两条语义不同的记录**：

| 记录 | 时机 | 内容 | 为何不合并 |
|---|---|---|---|
| A `literature_summary` | 检索汇总完成后 | 检索参数 + 命中统计 + 答案指纹 + 产物引用 | 检索阶段结果 |
| B `publisher_pdf_batch` | PDF 批量下载完成后（可晚数分钟） | `ok/total/s3` + `dedup_scope` + **0.5.09 新增 `ok_urls` / `failures` 逐项明细** | 下载阶段结果 |

两者共享同一 `request_id`，但 0.5.08 起用 `dedup_scope` **刻意隔离**：若直接复用裸 `(request_id, skillname)` 去重键，`_merge_prefer_richer` 会把 `hits_merged` 与 `ok/total/s3` 混进一行，字段语义互相污染。合并成一行需要「先写后 update 回填」，会引入异步回填与失败补偿复杂度。

因此本轮采用的口径是：**一次需求 → 一组按 `request_id` 可归因的少量记录，且每条记录自身信息完整**（A 行本轮已补齐，作为主记录）。若确实要求物理上严格一行，需另立需求设计回填链路。

另一个张力：**P2「缓存命中不写留痕」与「每个需求都有一条记录」冲突**。

> ✅ **0.5.09 已按用户 2026-11-14 确认解决**：缓存命中不再完全跳过，改写一条
> **轻量 `cache_hit` 行**（`cache_hit=true` / `served_from=local_cache`，只带稳定键、
> 诊断口径必需键与缓存观测键，不重复全量检索统计）。两类 payload 共用同一
> P3 稳定键白名单 `type/call_type/topic/query/params`，离线实测：首轮 A 汇总
> `claim=True`、第二轮 cache_hit `claim=False (duplicate_in_window)`、`release`
> 后可重试 → **同请求两轮 run 仍恒 1 行**，恢复留痕不放大存储。
> 代价是缓存全命中从 0 次 Coze 请求回到 1 次（纯 `log_only` 留痕、0 次检索），
> 属用户明确接受的取舍。`CT_LIT_LOG_ON_CACHE_HIT=1` 现语义为「缓存命中也写
> **全量** A 汇总」（回退开关），不再是「是否留痕」开关。

---

## 8. 仍未闭环 / 待确认项

| # | 事项 | 归属 | 说明 |
|---|---|---|---|
| 1 | ~~Coze 端 B 类失败明细~~ | Coze 端 | ✅ **0.5.09 已闭环**：`resultstr` 新增 `ok_urls`（成功产物 URL 列表）/ `failures`（逐 link 失败原因）+ 各自 count/truncated；节点异常分支补 `status=error` 留痕。详见第 10 节 |
| 2 | 0.5.09 部署包未部署 | 人工 | 主包已重打为 **0.5.09**（79 files / 513,636 B / md5 `0db706647d0c014f6f238a0cd8559468`），0.5.08 首包已备份为 `coze_deploy_bundle.zip.bak_20261114_075659_pre_0509`。**源码改对、包未换**仍是「线上没效果」的独立来源，按红线未自动部署 |
| 3 | 编排层 `CT_REQUEST_ID` 贯穿 | ct-advisor / 工作台 | 上游两轮 run 各生成新 `uuid4`，靠缓存 + 护栏 + 云端 upsert 抑制了后果，但双轮触发本身未根治。 |
| 4 | `log_only` 纯留痕请求 | 本地 | 首次需求仍为写 1 行审计多发 1 次 Coze 请求。若要省掉，需把汇总统计挂到某次已有检索请求由云端合并写入，属架构级改动。 |
| 5 | 版本碎片化 | 部署 | 72%（468/650）流量仍在 `1.4.7`，需先判别「多端点并存 / 灰度未铺开」再动作，不宜直接推定。 |
| 6 | 引文验证外部 API | 本地 | 缓存命中 run 仍访问 DOI/PMID/OpenAlex 等外部源（反幻觉所需），不在「Coze 端点请求」统计内。 |
| 7 | PubMed 注释/分支过时 | 本地 | 见第 2 节附注，待清理。 |
| 8 | `coze_contract.md` 版本漂移 | 文档（自动生成物） | 文件头标「**禁手改**」，仍写「端点 / 当前 `0.5.05`」，版本表也止于 0.5.05，与 `_version.py` 的 0.5.09 不符。属 0.5.06–0.5.09 多版本既有欠账、非本轮引入；按红线**未手改**，需改 `tests/coze_cases/_contract_index.json` 后跑 `gen_contract_doc.py` 重渲染。 |

> 第 1 项与第 7 节张力均已于 **2026-11-14 经用户确认后落地 0.5.09**；离线回归从 24 项扩至 **43 项全通过**，详见第 10 节。
> ⚠️ **本包含两条独立改动线**：本轮（B 类明细 / `cache_hit`）与并行改动线（飞书「降级·回退」结构化信号 `who_status` / `fallback_used` / `cde_retried` / `cde_zero_hit_unverified`）。两者共用 0.5.09 版本号但互不涉及，验收时按字段区分，不要因某一侧缺失误判整包没换。

---

## 9. 验收口径（须用修复后 ≥14 天新窗口）

历史 30 天窗口全是治理前数据，跑出来必然仍是「双写 40.6% / 信息稀薄」，**不能据此判定失败**。

| 检查项 | 期望 |
|---|---|
| §3.6 双写率 | 归零，按日全 0.0% |
| §6 `request_id` 覆盖率 | 显著 >0%（A/B 两类都要有） |
| B 类 `resultstr.dedup_scope` | == `"publisher_pdf_batch"`（没有 → 部署包没换） |
| **B 类 `ok_urls` / `failures`** | 0.5.09 部署后应出现；`ok==0` 的行必须能读到 `failures[].error`，`ok>0` 的行应能读到 `ok_urls[].url`（有 URL 才算可回溯） |
| **A 类 `cache_hit=true`** | 缓存命中调用应各留 1 行轻量记录；同 `request_id` 下不应同时出现 A 汇总 + cache_hit 两行（护栏应抑制） |
| **B 类异常留痕** | 节点抛异常时应有 `status=error` 行（此前完全无记录） |
| §3.7 `grade` | 从「信息稀薄」上移；`params / answer_hash / cache_hits / call_type / request_id` 覆盖率显著上升 |
| `resultstr.log` 的 `dedup=hit` / `recon=delN` | 若仍大量出现，说明云端去重生效但**上游仍在触发两次** → 查编排层 |
| 平均有效键数 | A 类从 9.0 升至 20+；B 类从 14.0 再上移（新增明细键） |
| §3.7 新增信号键 | `cache_hit` / `ok_urls` / `failures` 覆盖率应 >0%（0.5.09 已加入 SIGNAL_FIELDS，否则 grade 反映不出新增信息） |

> ⚠️ **§3.6 工具的已知盲点（0.5.09 复核发现，未改口径）**：`detect_duplicate_writes()`
> 按 `(query_origin, querystr 全文)` 分组判双写。轻量 `cache_hit` 行与全量 A 汇总的
> querystr **内容不同**（前者带 `cache_hit:true` 且字段更少），因此「同 `request_id`
> 同时出现 A 汇总 + cache_hit 两行」这种护栏失效情形**不会被 §3.6 判为双写**。
> 同时 A/B 两类本就是 `dedup_scope` 隔离的合法两行，也不能简单按 `request_id` 一刀切
> 合并计数。故验收必须额外做一次**按 `(request_id, call_type=literature_summary)` 分组**
> 的复核：同组 ≥2 行即护栏失效。上表「A 类 `cache_hit=true`」一项即此用途，
> 不要只看 §3.6 双写率归零就判定收敛。

> 仍须用**修复后 ≥14 天新窗口**；历史 30 天窗口全是治理前数据，跑出来必然仍是「双写 40.6% / 信息稀薄」，不能据此判定失败。

### 可逆开关

| 环境变量 | 作用 |
|---|---|
| `CT_LIT_LOG_ON_CACHE_HIT=1` | **语义已变（0.5.09）**：缓存命中时改回写**全量 A 汇总**（默认已是轻量 `cache_hit` 行，不再是「是否留痕」开关） |
| `CT_LIT_PURE_LOCAL_ON_CACHE=0` | 恢复纯计算节点云端优先（canary 比对用） |
| `CT_LIT_WRITE_GUARD=0` / `WINDOW` / `DIR` | 关闭 / 调窗 / 改 ledger 目录 |
| `CT_LIT_CACHE_LOCAL=1` / `CT_LIT_CACHE_DIR` | 恢复旧缓存作用域 / 自定义位置 |
| `CT_LIT_NO_CACHE=1` | 完全停用搜索缓存 |

---

## 10. 0.5.09 收尾（2026-11-14，用户确认后落地）

### 10.1 两项确认项的落地方式

| # | 确认项 | 落点 | 做法 |
|---|---|---|---|
| 1 | B 类缺逐 link 失败原因 / 成功产物 URL | Coze `publisher_pdf_batch_node.py` | 新增 `_build_item_details(items)`，把主链路**已算好**的 `_do_batch` 逐项结果投影进 `resultstr`；不额外发请求、不新增飞书列 |
| 2 | 「每需求一条」vs P2 完全不留痕 | 本地 `ct_literature.py` | 缓存全命中改写一条轻量 `cache_hit` 行；仍走 P3 稳定键护栏 |

**B 类新增字段**（仅正常完成路径传 `items`，`rejected` / 异常 / 老调用不传 → resultstr 与 0.5.08 逐字节一致）：

| 字段 | 内容 | 体量控制 |
|---|---|---|
| `ok_urls` | `[{key, url, via}]`，`url` 取已验证的 `pdf_url` / `pdf_s3_url` | ≤12 条；key 100 / url 160 字符截断 |
| `failures` | `[{key, status, error}]`，逐 link 失败原因 | ≤12 条；error 120 字符截断 |
| `*_count` / `*_truncated` | 未截断总数 + 是否截断标记 | 50 篇批次仍可定位前 12 条 |

划分口径用 `url and status=="ok"` 双向确认：`_sanitize_record` 会把「伪 ok 但无直链」降级为 `pdf_failed`，该分支不得混进成功列表。**节点异常分支补一条 `status=error` 轻量留痕**（此前 0 条记录，是「每需求至少一条」的漏洞）。

**本地轻量行**：`cache_hit=true` / `served_from=local_cache`，只带稳定键、诊断口径必需键（`hits_merged` / `sources_fail` / `zero_hits`，防取数工具把缺键误判零命中）与缓存观测键；`type` / `call_type` 刻意保持 `literature_summary`，避免给 `record_call_type` 制造第三分桶稀释统计。

### 10.2 验证（全部离线，未触碰线上）

| 项 | 结果 |
|---|---|
| `py_compile`（4 个改动 .py + ct_literature.py） | 通过（Anaconda `C:\Tools\anaconda3\python.exe`） |
| `selfcheck_pdf_dedup.py` | **43 项 ALL PASSED**（原 24 项 + T10g / T11a–f / T12a–d / T13a–c / T14a–d） |
| P3 护栏离线实测 | A 汇总与 cache_hit 两类 payload 稳定键**相同**；首轮 `claim=True`、第二轮 `claim=False (duplicate_in_window)`、`release` 后可重试 → 同请求恒 1 行 |
| `build_bundle.py preflight` | 66 个 .py 语法 + 注解 import 体检通过 |
| 新包反查 | `COZE_VERSION=0.5.09`；含 `_build_item_details` / `items=results` / `T14a` / `_reconcile_dups`；`testzip()` 无损坏 |

### 10.3 改动文件与产物

| 文件 | 改动 |
|---|---|
| `coze .../publisher_pdf_batch_node.py` | 常量 4 个 + `_build_item_details()` + `_fire_and_forget_feishu_log(items=)` + 正常/异常两处调用点 |
| `coze .../nodes/_version.py` | 追加 0.5.09 续说明（保留并行改动线原有 0.5.09 段落，未覆盖） |
| `coze .../scripts/selfcheck_pdf_dedup.py` | 扩至 43 项，含跨技能静态断言 T14 |
| `coze .../AGENTS.md` | 版本表、回归清单、部署包欠账段、两条改动线验收提示 |
| `ct-literature/scripts/ct_literature.py` | 缓存命中轻量行 + 统一护栏/dispatch 分支 + 3 处注释口径同步 |
| `ct-literature/references/audit_requests_and_log_content.md` | 本文（§1/2/3/7/8/9 口径同步 + 本节） |

**部署包**：`coze_deploy_bundle.zip` = 79 files / 513,636 B / md5 `0db706647d0c014f6f238a0cd8559468`；旧 0.5.08 首包备份 `coze_deploy_bundle.zip.bak_20261114_075659_pre_0509`。🔴 **按红线未部署**，需人工上传后按第 9 节新窗口验收。

### 10.4 执行中发现的并发写入（需知悉）

本轮侦察后、编辑期间（07:46–07:49）检测到 Coze 目录另一进程写入了 `state.py` / `who_search_node.py` / `feishu_write_node.py` / `cde_search.py` / `_version.py`，内容为「飞书降级·回退结构化信号」，并已把版本常量置为 `0.5.09`。处理原则：**不覆盖对方任何文件**，只在 `_version.py` 末尾追加本轮说明，版本沿用 0.5.09（与用户「并入 0.5.09」的口径一致）。因此本包**同时含两条独立改动线**，验收按字段区分（见第 8 节尾注）；若要求单线验收，可另出 0.5.10 拆分。

### 10.5 复核修正（2026-11-14 08:04–08:12，用户「再检查一下」）

不复用上一轮结论，重读落盘代码、重跑回归、反查部署包后，发现并修正 4 处：

| # | 发现 | 判定 | 修正 |
|---|---|---|---|
| 1 | 首包打于 07:57，另一进程 08:00:38 又改了 `search_node.py`（`_do_search_cached` 短 TTL 缓存 + `cde_zero_hit_unverified`）与 `who_search_node.py`（续行缩进），首包仍是 296 行旧版 | **真缺陷**：§8 尾注声称本包含两条改动线，实际降级信号线有一半没进包 | 按「包 = 磁盘」重新出包；逐文件字节比对 **DIFF = 0**，`_do_search_cached` / `cde_zero_hit_unverified` 已入包 |
| 2 | 轻量 `cache_hit` 行把 `sources_ok` 硬编码 `_n_jobs`、`sources_fail` 硬编码 `0`，而同函数上方已算出真实 `_p_ok` / `_p_fail` | **真缺陷**：缓存里若存着失败源，诊断侧会把该次调用判成全成功，与「写入有效信息」相悖 | 改用真实 `_p_ok` / `_p_fail`，补 `sources_failed` / `error_type` / `error_code`，与全量 A 汇总同口径；新增 T14d 静态断言锁死 |
| 3 | §6 仍写「Coze 端代码本轮未改动」，改动清单也未列 0.5.09 的 Coze 文件 | 文档过期 | §6 表格补 4 行 Coze 文件 + ct-update 信号键，末句改为按 0.5.09 最终态表述 |
| 4 | `detect_duplicate_writes()` 按 `(query_origin, querystr 全文)` 分组；轻量行与 A 汇总 querystr 不同 | 验收工具盲点（非缺陷，A/B 两行本就合法，不宜一刀切合并） | 不改工具口径，§9 增加「按 `(request_id, call_type=literature_summary)` 分组 ≥2 行即护栏失效」的人工复核项与盲点说明 |

**同时补齐可验收性**：`ct-update/feishu_log_fetch.py` 的 `stat_field_coverage` SIGNAL_FIELDS 加入 `cache_hit` / `ok_urls` / `failures`，否则 0.5.09 新增的有效信息即使写全，§3.7 `grade` 也反映不出来；§9 同步加检查项。

**复核后最终态**：`py_compile` 9 个改动 `.py` 通过；`selfcheck_pdf_dedup.py` **43 项 ALL PASSED**；`build_bundle.py preflight` 66 个 `.py` 通过；包指纹 79 files / 513,636 B / md5 `0db706647d0c014f6f238a0cd8559468`，`testzip()` 无损坏、包=磁盘差异 0。07:57 首版 0.5.09 包已备份为 `coze_deploy_bundle.zip.bak_20261114_081058_pre_repack`（08:10 二次包另备份为 `coze_deploy_bundle.zip.bak_20261114_081337_pre_final`）。**仍未部署**。

> 误报排除：复核脚本曾按裸串 `dedup_scope=""` 反查 `feishu_write_node.py` 未命中，实际源码为带类型注解的 `dedup_scope: str = ""`，磁盘与包内字节一致、T2 回归通过，非缺陷。

