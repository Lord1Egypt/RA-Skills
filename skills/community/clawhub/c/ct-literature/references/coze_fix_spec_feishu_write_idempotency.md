# Coze 端修复规格：feishu_write 幂等去重（含 B 类写入路径）

> 状态：**已落地（Coze 端源码 0.5.08，2026-11-13）｜待部署**
> 适用技能：ct-literature（同契约适用于全部 ct-* 技能）
> 关联：`coze_fix_spec_publisher_pdf_batch.md`（假成功 / s3 漏登 / 重试退避）
> 代码位置：`ct-registry/adapters/coze/`

---

## 0. 本轮修订说明（重要）

初版规格（同日早些时候）在「本地看不到 Coze 代码」的前提下推断
**「云端 `feishu_write` 没有幂等约束，需要按本文伪代码新建」**。用户随后给出
Coze 端代码路径，只读侦察后**该推断被推翻**：

- `feishu_write_node.py` 早已迭代到 **0.5.07**，包含 `field_name` 修正、列名
  大小写不敏感解析、缺列自动补建、前置 `_dedup_probe`、`dedup=` 诊断写进
  `resultstr.log`、TOCTOU 单飞、写后收敛、确定性 keeper。伪代码里的能力**全部已存在**。
- 真正缺的是**另一条写入路径**：`publisher_pdf_batch_node` 自建 record 直接
  `add_records`，完全绕过上述机制。
- 还有一处与历史事故同根的缺陷：`SearchNodeInput` 未声明 `request_id`。
- 以及一个初版规格**没有预见到**的风险：A/B 两类共享 `(request_id, skillname)`，
  直接复用裸键会互合并成一行。

所以本文由「待实现规格」改为「已落地清单 + 实测修正」。§1 实证数据保留。

---

## 1. 实证问题（保留）

数据窗口：2026-10-15 → 2026-11-13（飞书 `searchlog`，ct-literature，650 行）。
取数口径：`ct-update/scripts/feishu_log_fetch.py --skill literature` 的 §3.6。

| 指标 | 实测 |
|---|---|
| 总写入行数 | 650 |
| 结构性双写（同载荷 Δt < 2s 的第二行） | **264 行 = 40.6%** |
| 日双写率 | 10-15～11-11 多日精确 **50.0%** |
| 双写间隔 | min 172ms / p50 **385ms** / p75 531ms / max 1933ms |
| 双写行类型 | `literature_summary` 260 / `publisher_pdf_batch` 4 |
| 两行 `resultstr` | 245 对仅 `runtime_sec` 不同 → 两次真实独立执行 |
| 跨时间重复提交 | 去双写后 386 行 / 唯一载荷 306 组 → 80 行重复 |
| 理论可压缩 | 344 行 = **52.9%** |

> 50% 稳定 + 亚秒级间隔 + runtime 不同，排除人工重复提交与退避重试，指向
> **同一次用户请求触发了两轮完整执行**。

---

## 2. 根因链（修订）

| 层 | 问题 | 状态 |
|---|---|---|
| 上游 | 同一次用户请求触发两轮，各生成新 `uuid4`（`CT_REQUEST_ID` 未贯穿） | 遗留，属编排层 |
| 客户端 | 4 个调用点传 `request_id=`，但 `dispatch()` / `fetch_source()` 签名不接受、payload 从未携带 | **已修**（本轮客户端 5 文件） |
| 云端 A 类 | `feishu_write_node` 幂等 | **早已实现**（0.5.02→0.5.07），无需改 |
| 云端 B 类 | `publisher_pdf_batch_node` 裸 `add_records`，无 ID 列、无查重/收敛 | **本轮修复**（0.5.08） |
| 字段投影 | `SearchNodeInput` 未声明 `request_id` → `extra='ignore'` 静默丢弃 | **本轮修复**（0.5.08） |
| 部署包 | 根目录 `coze_deploy_bundle.zip` 仍是 **0.4.02（11-05）**，不含任何去重代码 | **本轮重新出包**，待人工部署 |

---

## 3. Coze 端已落地改动（0.5.08）

### 3.1 字段契约（客户端已补齐，云端按此读取）

顶层信封新增 `request_id`（string，客户端 `uuid4().hex` 或继承 `CT_REQUEST_ID`），
非嵌套、不进 `querystr` / `resultstr`。一次用户请求内 6 源检索 + 末尾汇总 +
批量下载共享同一 ID。

落点（客户端侧，本轮已改）：
- `ct-literature/adapters/fetch_coze_unified.py` → `dispatch()` / `dispatch_stream()` 参数 + payload
- `ct-literature/adapters/source_registry.py` → `fetch_source()` 参数 + `_kw` 透传
- `ct-literature/adapters/pdf_download.py` → `PdfDownloader(request_id=...)` + `publisher_pdf_batch` payload
- `ct-literature/scripts/ct_literature.py` → 汇总 `querystr` 内 `request_id` + 4 个调用点

> 旧云端 `extra='ignore'` 静默忽略未知字段，客户端改动向后兼容。

### 3.2 `state.py::SearchNodeInput` 补声明

`GraphInput` / `GlobalState` / `FeishuWriteInput` 三处早已声明 `request_id`，
唯独 `SearchNodeInput` 漏了 → `/run` 投影到搜索节点时被 `extra='ignore'` 丢弃，
`publisher_pdf_batch_node` 恒拿到 `None`。与 0.3.93（`date_from/date_to`）、
0.3.94（`lit_date_*`）、0.5.03（`FeishuWriteInput`）完全同根：
**入口声明 ≠ 节点内可见**。同时补齐 `entry_point` 声明（同款漏声明）。

### 3.3 B 类节点复用幂等写入

`publisher_pdf_batch_node._fire_and_forget_feishu_log()`：

| 改动前 | 改动后 |
|---|---|
| record 无 `request_id` 键 | 落 `request_id` 独立列（飞书列名解析/自动补建由写入侧统一处理） |
| `bitable.add_records(records=[record])` | `_write_to_feishu(record, dedup_scope='publisher_pdf_batch')` |
| 无查重、无收敛、无字段被拒重试 | 全部复用 `feishu_write_node` 单一真源 |
| `resultstr` 无路径标记 | 增 `dedup_scope` 观测键，验收时一次取数即可区分新旧路径 |

**降级纪律**：`from graphs.nodes.feishu_write_node import _write_to_feishu`
失败（打包遗漏 / 运行期 import 异常）时回退裸写入，并**剥离 `request_id` 键**
——旧表无该列时整行会被拒，不剥离就会丢审计记录。守住
「宁可不重，不可不留痕」。仍是 fire-and-forget daemon 线程，不阻塞主响应。

### 3.4 `dedup_scope`：调用类别隔离（初版规格未预见到）

`_write_to_feishu()` 新增可选参数 `dedup_scope: str = ""`，在 `_dedup_key()`
结果后追加 `|<scope>`：

```
A 类 log_only 汇总      key = <request_id>
B 类 publisher_pdf_batch key = <request_id>|publisher_pdf_batch
```

**为什么必须隔离**：ct-literature 一次用户请求里，A 类汇总与 B 类批量下载共享
同一 `request_id` 和 `skillname='ct-literature'`。若共用裸 `(request_id, skillname)`
键，`_find_by_request_id` 会互命中，`_merge_prefer_richer` 会把 `hits_merged`
与 `ok/total/s3` 混进同一行 —— 两类日志同时失真，比双写更难发现。

- A 类不传 scope（默认空串），**行为逐字节不变**，零回归风险；
- scope 改变键后，节点内基于裸键缓存的 `existing`/`note` 结论强制作废，线程内重查；
- 去重规则仍只留一份，调用方只声明「我是哪一类」，不复制第二套白名单。

### 3.5 关于 `write_count`（取舍）

初版 §3.3 建议新增 `write_count` 独立列以区分「云端去重生效」与「上游仍触发两次」。
**本轮不新增列**，理由：云端 0.5.05 的 `dedup=hit/miss/+wait` 诊断、
0.5.06 的 `recon=delN` 已写进 `resultstr.log`，信息等价；再加一列需要改飞书表结构，
收益不抵风险。验收直接读 `resultstr.log` 的 `dedup=` 即可。

---

## 4. 云端既有能力盘点（无需重写，`AGENTS.md` 有完整事故史）

| 版本 | 能力 |
|---|---|
| 0.5.02 | 按 `(request_id, skillname)` 精确 upsert；`_merge_prefer_richer` 防「秒空热命中」覆盖真结果 |
| 0.5.03 | filter 键改 `field_name`（首发用 `field` 导致查重恒 miss）；列名大小写不敏感解析；死代码降级改 `try/except` |
| 0.5.04 | 补漏 import 的 `Optional`（注解 def 期求值会让容器起不来）；`build_bundle.py` 增加 `preflight()` 静态体检 |
| 0.5.05 | `_dedup_probe` 把 `dedup=` 结论写进 `resultstr.log`；缺列自动 `create_field` 补建；无 ID 时退化 `auto:sha256` 指纹 + 5 分钟窗 |
| 0.5.06 | TOCTOU 竞态：`_claim_inflight` 单飞 + `_reconcile_dups` 写后收敛（跨容器唯一保证） |
| 0.5.07 | 收敛改**确定性 keeper**（按 `(inittime, record_id)` 升序），修 0.5.06 互删至 0 行的回归 |
| **0.5.08** | **本轮：B 类路径接入 + 字段投影修复 + scope 隔离 + 重新出包** |

---

## 5. 编排层配合（P1，非本技能可改）

一次用户请求进入时，由编排层（ct-advisor / 工作台 `server.py`）生成并注入：

```
CT_REQUEST_ID=<uuid4().hex>
```

要求：同一用户请求内**所有**兄弟技能 / 端点 / 重试调用共享同一值；
`ct_literature.run()` 已实现 `os.environ.get("CT_REQUEST_ID") or uuid.uuid4().hex`。
缺失时客户端各自生成 → 云端按 ID 去重无法覆盖跨轮双写，只能靠客户端护栏兜底。

---

## 6. 客户端本轮已落地（无需云端配合即可部分生效）

| 层次 | 改动 | 效果 |
|---|---|---|
| P0 | `request_id` 接口闭环（5 个文件） | 云端首次真正收到 ID；消除 4 处 `TypeError` 隐患 |
| P2 | `feishu_summary_skipped_cache_hit`：整次 run 全命中缓存 → 跳过 `log_only` 汇总写入（**2026-11-14 已改口径，见 §11**） | 当时抑制跨时间重复提交（最多 -80 行）；`CT_LIT_LOG_ON_CACHE_HIT=1` 可回退 |
| P3 | `adapters/feishu_write_guard.py`：业务载荷指纹 + 5s 窗口原子 claim | 云端改造前即可挡住同机双写；排他锁 + 原子写 + 失败 `release()` |
| 诊断 | `ct-update/scripts/feishu_log_fetch.py` 新增 §3.6 + JSON `duplicate_writes` | 双写率可量化、可验收 |

**刻意不做的两件事**：
1. **不给 B 类接本地写前护栏**：B 类日志与真实下载是同一次 Coze 调用，本地无法
   只抑制日志而不抑制下载；实测 `ok==0` 占 50.9%，盲目抑制会挡掉失败重试。
   B 类交给云端按 ID 去重解决（本轮 §3.3）。
2. **不做语义查询归一化**：实测 215 个唯一 topic 无损归一后 214，收益≈0；
   临床检索自动合并 `omega-3` 与 `omega-3 fatty acids` 会返回错误文献集。

---

## 7. 验收口径（部署后必跑）

```bash
cd ~/.workbuddy/skills/ct-update
python scripts/feishu_log_fetch.py --skill literature --days 14
```

| 检查项 | 期望 | 不达标含义 |
|---|---|---|
| §3.6 `duplicate_rows` / `duplicate_rate` | **0 / 0.0%** | 云端 upsert 未生效，或上游仍在 append |
| §3.6 按日双写率 | 全 0.0% | 部分日期仍双写 → 版本灰度未铺开 |
| §6 `request_id` 覆盖率 | 显著 > 0%（A/B 两类都要有） | 独立列未落，或旧客户端仍占主导 |
| B 类 `resultstr.dedup_scope` | `publisher_pdf_batch` | 仍是旧写入路径（部署包没换） |
| `resultstr.log` 的 `dedup=hit` / `recon=delN` | 可见 | 云端去重生效但**上游仍触发两次**，需查编排层 |
| §3.5 `no_artifact` / `zero_fetch` | 下降 | 属 `coze_fix_spec_publisher_pdf_batch.md` 范畴 |

> ⚠️ 窗口建议 ≥14 天且覆盖新版本流量。历史窗口（10-15～11-13）全是修复前数据，
> 用它验收必然仍是 40.6%，**不能据此判定修复失败**。
> ⚠️ 部署前先核对包内 `_version.py::COZE_VERSION == "0.5.09"` 且
> `feishu_write_node.py` 含 `_reconcile_dups` —— 历史欠账就是「源码改了、包没换」。
> （0.5.08 包已被 0.5.09 替换；验收新增字段见 `audit_requests_and_log_content.md` §9。）

---

## 8. 可逆开关速查（客户端）

| 环境变量 | 默认 | 作用 |
|---|---|---|
| `CT_LIT_WRITE_GUARD=0` | 开 | 关闭 P3 写前护栏，恢复旧写入行为 |
| `CT_LIT_WRITE_GUARD_WINDOW` | 5.0s | 调整去重时间窗（实测双写 max 1933ms） |
| `CT_LIT_WRITE_GUARD_DIR` | `~/.cache/ct-literature` | 自定义护栏 ledger 目录 |
| `CT_LIT_LOG_ON_CACHE_HIT=1` | 关 | **语义已变（0.5.09）**：缓存命中时改回写**全量 A 汇总**；默认已是轻量 `cache_hit` 行，不再是「是否留痕」开关 |
| `CT_LIT_CACHE_LOCAL=1` | 关 | 回退缓存到每次唯一的 `<out_dir>`（不推荐） |
| `CT_LIT_CACHE_DIR` | 用户级共享目录 | 自定义缓存位置 |

---

## 9. 合规说明（P2 取舍已获用户确认）

用户于 2026-11-13 明确选择「全部（含缓存命中抑制留痕）」，即接受：
**整次 run 全部命中本地缓存时，该次调用不再产生飞书审计留痕**。
保留的可观测性：本地 `--progress json` 事件流仍发
`feishu_summary_skipped_cache_hit`；若后续合规要求「每次调用必留痕」，
设 `CT_LIT_LOG_ON_CACHE_HIT=1` 即可全量恢复，无需改代码。

---

## 10. 唯一剩余待办

**部署**：已在本机重新生成 **0.5.09** 部署包并完成静态体检（0.5.08 包已备份），但按项目红线
**不自动推送 / 不自动部署**。需人工把 `coze_deploy_bundle.zip` 上传到 Coze 端点后，
再按 §7 跑验收。历史重复行按 2026-11-11 决定不做清理，只保证新请求不再双写。

---

## 11. 2026-11-14 修订（0.5.09，用户确认后）——本文为 0.5.08 历史档，口径以此节为准

用户确认了综合审计报告 §8 的两项待确认项，两项均已落地，故本档 §6 P2、§8 开关、
§9 合规说明的**原始描述已过时**，保留作为历史留痕：

| 原口径（0.5.08） | 现口径（0.5.09） |
|---|---|
| 缓存全命中完全不写飞书（`feishu_summary_skipped_cache_hit`） | 改发一条轻量 `cache_hit` 行（`feishu_summary_cache_hit`），恢复「每需求至少一条记录」 |
| `CT_LIT_LOG_ON_CACHE_HIT=1` = 是否留痕的开关 | = 是否写**全量 A 汇总**的回退开关（默认已有轻量行） |
| B 类 `resultstr` 只有 `ok/total/s3/dedup_scope` | 新增 `ok_urls`（成功产物 URL 列表）+ `failures`（逐 link 失败原因）+ 异常路径 `status=error` 留痕 |

**关键保证**：轻量行与 A 汇总共用 P3 稳定键白名单 `type/call_type/topic/query/params`，
离线实测首轮 `claim=True`、第二轮 `claim=False (duplicate_in_window)`，故同请求两轮 run
**仍恒 1 行**，恢复留痕不放大双写。代价：缓存全命中从 0 次 Coze 请求回到 1 次纯 `log_only`
留痕（0 次检索），属用户明确接受的合规取舍。

回归 `selfcheck_pdf_dedup.py` 由 24 项扩至 **43 项全通过**；0.5.09 包 79 files /
513,636 B / md5 `0db706647d0c014f6f238a0cd8559468`，**仍未部署**。完整改动与验收字段见
`references/audit_requests_and_log_content.md` §10。
