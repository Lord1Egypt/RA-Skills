> ⚠️ **本稿已被取代（2026-09-23）**——按「不新建数据表」口径重做的方案见
> [`2026-09-23-feishu-doc-archive-single-table-plan.md`](./2026-09-23-feishu-doc-archive-single-table-plan.md)；
> 而**最终实现**为独立附件表 `filelog`（coze v1.27+，2026-09-25 生产闭环；规范见 ct-base §20.16）。
>
> 本稿保留作**双表方案**的对照记录，但**其中两处事实已更正，请勿据此实施**：
> 1. `client_token` 的幂等**只维持 5 分钟**，**不能**作为跨会话去重手段（本稿 §5.5 的说法有误）→ 长期去重必须靠写入前 `records/search`；
> 2. 单表行数上限**免费/标准版为 2,000 行**（不是本稿 §4.1 所写的 5,000），且**超限后整表无法新增记录**。
>
> 完整更正清单见新稿「附 A：官方事实核对表」。

---

# 用户上传文档落库飞书：实施方案（评估稿）

- **日期**：2026-09-23
- **状态**：评估稿，**尚未实施**（不含任何已生效的代码改动）
- **结论**：**可行**，且多维表格（Bitable）几乎是唯一合理载体。建议分 4 期落地，**P1 即拿到最痛的价值**且风险极低。
- **两个前置门禁**（未过之前不应写生产代码）：
  1. 🔴 **数据合规**：是否允许把用户上传的**原文**写入飞书云文档？（见 §10.1）
  2. 🟠 **权限探针**：现有 `integration-feishu-base` 凭据对新表是否有写权限，尤其**云空间素材上传**权限（附件列的前置）。（见 §10.2）

---

## 1. 现状与缺口

### 1.1 今天的链路

```
本地 (doc_memory)                 Coze 端
  ├ mode=full   正文全文 ────────▶ payload.parse ──▶ split_chunks ──▶ doc_store(SQLite, TTL 30d)
  ├ mode=chunks 已切块   ────────▶ 同上                                    │
  ├ mode=ref    仅 doc_id ───────▶ load_doc ◀────────────────────────────┘
  └ mode=file   原始字节 ────────▶ office_reader 解码为 md ──▶ 同上
                                                                    │
                                                    select_chunks(question)
                                                                    ▼
                                              doc_evidence(`[文档 §N]`) + doc_meta
                                                                    ▼
                                              full_analysis ──▶ advisorlog(飞书 Bitable)
                                                                （信封里带 doc_id / doc_fp /
                                                                  doc_chars / doc_mode）
```

关键代码位置：

| 环节 | 文件 |
|---|---|
| 载荷契约（单一真源） | `src/doc/payload.py` |
| 管线唯一高层入口 | `src/doc/__init__.py::ingest_and_select` |
| 服务端文档库 | `src/doc/doc_store.py`（SQLite → /tmp → 内存） |
| 入口节点 | `src/graphs/nodes/doc_ingest_node.py` |
| 已存在的飞书写入器 | `src/graphs/nodes/async_feishu_writer.py` |

### 1.2 三个缺口

| # | 缺口 | 今天的后果 |
|---|---|---|
| G1 | **文档只活在容器里**。`doc_store` 是容器本地 SQLite（TTL 30 天，`MAX_DOCS=5000`），容器回收 / 换 worker 即丢 | `mode=ref` 的追问在回收后必然失败 → 用户看到「本轮未能取回此前上传的文档内容」 |
| G2 | **没有审计留痕**。飞书里只有「哪次问答用了文档」的**元数据**，文档本身不在 | 运营/QA 无法复核「这条结论是基于哪份文档、文档长什么样」 |
| G3 | **跨会话复用为零**。doc_id 与内容的绑定随容器消失 | 用户重复上传同一份文档时，服务端无法识别"已存过" |

> **注意**：`final_answer` 的 JSON 信封里已经带 `doc_id` / `doc_fp` / `doc_chars` / `doc_chunks` / `doc_total_chunks` / `doc_mode`。**这为跨表关联提供了现成主键，不需要改 advisorlog 的 schema。**

---

## 2. 目标与非目标

**目标**
- 把上传的文档**持久化**到飞书，使其不再依赖容器生命周期（治 G1/G2/G3）。
- 保持"用户上传 → 得到答案"主链路的**延迟与失败语义完全不变**。

**非目标**
- ❌ 不做向量检索 / 语义搜索（本次只做持久化与可读）。
- ❌ 不改变 `doc_context` 契约的**必填**字段（保持两端可独立升级）。
- ❌ 不把飞书做成文档的**主存储**。`doc_store`（本地、快、零网络）仍是一线；飞书是**持久化副本 + 审计面**。

---

## 3. 载体选型：为什么是多维表格

| 载体 | 长文本 | 附件 | 记录级 API | 能否复用现有凭据 | 结论 |
|---|---|---|---|---|---|
| **多维表格 Bitable** | 单格 ≤ **10 万字** | ✅ 有附件字段 | ✅ records CRUD | ✅ 同一 app_token | **推荐** |
| 电子表格 Sheets | 单元格模型，长文本能力弱 | ❌ | ❌ | ❌ 另一套 API/权限 | 不推荐 |
| 云文档 Docs | ✅ | ✅ | ❌ 无结构化查询 | ❌ 需 drive 建文档权限 | 只适合草稿，不作主方案 |

### 3.1 必须先知道的硬限制（官方数字）

| 限制项 | 数值 | 出处 |
|---|---|---|
| 单元格**文本**上限 | **100,000 字** | 帮助中心《多维表格常见上限》+《记录数据结构》两处一致 |
| 单元格附件数 | ≤ 100 个 | 同上 |
| 单表附件总数 | ≤ 20,000 个 | 同上 |
| 单个多维表格内数据表数 | ≤ 300 | 同上 |
| `records/batch_create` 单次条数 | 中文页 **1,000** / 英文页与 SDK 注释 **500** ⚠️ | 官方文档口径不一致 |
| `records/batch_create` 频率 | 中文页 **50 次/秒** / 英文页与 SDK 注释 **10 QPS** ⚠️ | 同上 |
| 附件大小 | ≤ 2 GB | 帮助中心 |

> ⚠️ **限流/批量口径官方两版文档不一致**（中文页比英文页宽松 2~5 倍）。**实现一律按保守值**（500 条/次、10 QPS），并把它们做成常量：一旦实测发现可按宽松值跑，改常量即可，不动逻辑。

---

## 4. 数据模型

两张新表，**建在现有的同一个多维表格 app 内**（`app_token = Pog0bGNMbaCWMIsGRNpckHcnn9f`），这样能直接复用 `integration-feishu-base` 凭据。

### 表 1：`doc_archive`（文档台账，**1 行 / 文档**）

| 列名 | 类型 | 说明 |
|---|---|---|
| `doc_id` | 文本 | 主键。本地内容哈希，跨轮稳定 |
| `doc_fp` | 文本 | 指纹。**与 advisorlog 信封的 `doc_fp` 同名同义 → 跨表关联键** |
| `title` | 文本 | `payload.title` |
| `file_name` | 文本 | 原始文件名（仅 `mode=file` 有） |
| `mode` | 单选 | `full` / `chunks` / `ref` / `file` |
| `format` | 文本 | `docx`/`xlsx`/`pptx`/`doc`/`xls`/`ppt`/`pdf`/`txt` |
| `doc_chars` | 数字 | 正文字符数 |
| `doc_total_chunks` | 数字 | 分块总数 |
| `doc_selected_chunks` | 数字 | 本轮命中块数 |
| `answer_mode` | 单选 | `survey`（梳理型）/ `qa`（问答型） |
| `decode_ok` | 复选框 | 解码是否成功 |
| `decode_error` | 文本 | 失败原因（**面向用户的那段文案**，便于运营直接复述） |
| `query_origin` | 文本 | 机器标识，与 advisorlog 同义 |
| `first_question` | 文本 | 首次触发上传的问题 |
| `preview` | 文本 | 正文前 **20,000 字**（供人工速览，不依赖附件） |
| `doc_text` | 文本 | 正文全文，**仅当 ≤ 100,000 字**时写（见 §5.4） |
| `file` | 附件 | 原始文件，**仅 `mode=file`** 可得（见 §10.6） |
| `hits` | 数字 | 后续被引用次数（`mode=ref` 命中时 +1） |
| `created_at` | 日期 | 毫秒时间戳 |
| `status` | 单选 | `ok` / `file_error` / `oversize` / `missing` |

### 表 2：`doc_segments`（全文分段，**仅超大文档**，1 行 / 段）

| 列名 | 类型 | 说明 |
|---|---|---|
| `doc_id` | 文本 | 关联表 1 |
| `seg_index` | 数字 | 段序，从 0 起 |
| `text` | 文本 | 段正文，每段 ≤ **50,000 字** |
| `chars` | 数字 | 段字符数 |
| `created_at` | 日期 | ms |

### 4.1 容量测算（诚实版）

| 项目 | 测算 |
|---|---|
| 表 1 行数 | 1 行/文档。**免费版单表 5,000 行 → 上限 5,000 份文档**，需监控 |
| 表 2 行数 | 仅 >10 万字的文档才写；按 5 万字/段，**200 万字上限也只 = 40 行/文档** |
| 典型场景 | 用户实际反馈的 3.2 万字文档 → **表 1 一行、`doc_text` 一格装下、表 2 零行** ✅ |

> 结论：**绝大多数文档就是 1 行**；分段表只在极端大文档时启用，行数成本可控。

---

## 5. 写入链路设计

### 5.1 挂载点：`ingest_and_select` 内部（落盘之后）

**唯一能同时拿到"全文 + 原始字节"的位置**就在这里：

```python
# src/doc/__init__.py :: ingest_and_select  （示意，尚未实施）
        if not stored:
            stored = save_doc(payload.doc_id, chunks, {...})
            # ↓ 新增：落盘成功后异步归档到飞书（尽力而为，绝不阻断）
            _maybe_archive(payload, chunks, text, file_info, meta_hint)
```

为什么**不**把全文/字节塞进返回的 `meta`？
- `meta` 会进 `state`、进缓存键、进 advisorlog 信封 —— 塞全文会让它们全部膨胀，并可能破坏现有缓存语义与信封格式。
- 保持 `meta` 轻量是现有设计（`doc_meta` 只放指针类字段），不应破坏。

### 5.2 模块与签名

新增 `src/graphs/nodes/feishu_doc_writer.py`，**完全对齐 `async_feishu_writer.py` 的工程风格**：

```python
def async_feishu_archive(
    doc_meta: dict,            # doc_id / doc_fp / mode / total_chars / n_total / n_selected ...
    *,
    text: str = "",            # 全文（mode=chunks 时用 "\n".join(chunks) 还原）
    chunks: list | None = None,
    file_b64: str = "",        # 仅 mode=file
    file_name: str = "",
    question: str = "",
    query_meta: dict | None = None,
) -> None:
    """后台线程异步归档到飞书多维表格。永不抛异常、永不阻塞主链路。"""
```

**共用鉴权**：把 `_get_access_token()`（`coze_workload_identity.Client().get_integration_credential("integration-feishu-base")`）抽到 `src/graphs/nodes/feishu_auth.py`，两个写入器共享，避免复制粘贴。

### 5.3 三条硬性工程约定（与现有写入器一致）

1. **异步 + 守护线程**：`threading.Thread(daemon=True).start()`，主链路立即返回。
2. **失败静默**：任何异常只 `logger.warning`，绝不影响答案产出。
3. **开关默认关**：见 §8；关闭时**零 HTTP 调用**、行为与今天逐字节一致。

### 5.4 截断与分段规则

| 正文字符数 | 落法 |
|---|---|
| ≤ 20,000 | `doc_text` 全文 + `preview` 同文 |
| 20,000 < n ≤ 100,000 | `doc_text` 全文（单格上限内）+ `preview` 前 20,000 |
| > 100,000 | **不写** `doc_text`；改写表 2 `doc_segments`（每段 ≤ 50,000 字）+ `preview` 前 20,000 |

> 规则刻意简单：**能一格装下就一格**，装不下才分段。避免为"小文档"引入不必要复杂度。

### 5.5 幂等：确定性 `client_token`

`batch_create` 支持 `client_token`（"uuidv4，用于幂等更新；非空即幂等操作"）。

做法：`client_token = uuid5(NAMESPACE_URL, doc_id)`  → **由 doc_id 确定性派生**。
- 同一份文档重复上传 → 同一个 token → 飞书侧幂等，**不产生重复行**。
- 进程重启 / 重试 → token 不变 → 依然幂等。
- 需要累计 `hits` 时，另走 `records/batch_update`（按返回的 `record_id`）。

### 5.6 附件上传（两步，仅 `mode=file`）

```
① POST drive/v1/medias/upload_all   (multipart)      → file_token
② POST bitable/.../records/batch_create  {"file":[{"file_token": "..."}]}
```
- ⚠️ `file_token` **只在当前多维表格内有效**，换表需重传。
- ⚠️ 需云空间上传权限；权限不足会返回 `1254027 UploadAttachNotAllowed`。→ **正是 §10.2 探针要验的东西。**

---

## 6. 读回退（可选 · P4）

**目的**：治 G1 —— 容器回收后，`mode=ref` 的追问仍能取回文档。

```
load_doc(doc_id)  ─未命中─▶  查飞书 doc_archive（timeout 3s）
                                 ├ 命中 doc_text      → split_chunks 重建块
                                 └ 命中 doc_segments  → 拼接后重建块
```

**必须遵守的三条**：
1. **仅在 `mode=ref` 且 SQLite 未命中时**触发 —— 绝不为 `full`/`chunks`（正文已在手上）去打网络。
2. **严格超时**（建议 3s）+ 失败即降级为现有的"未取回"提示；**绝不**让飞书抖动变成用户侧 5xx 或长等待。
3. **默认关闭**，单独开关控制。

> ⚠️ 已知副作用：从文本重建块后，`§N` 的编号可能与原始会话不同（因为分段发生在服务端而非本地）。对"引用某段"的场景影响轻微，但**需在文档里写明**，避免日后误判为 bug。

---

## 7. 分阶段落地计划

| 阶段 | 内容 | 依赖 | 风险 | 是否可独立回滚 |
|---|---|---|---|---|
| **P0** | 合规确认（§10.1）+ 权限探针（§10.2）+ UI 手工建表 1 | 人工 | — | — |
| **P1** | 台账落库：`doc_archive` **元数据 + preview**（不含全文、不含附件） | P0 | 🟢 极低 | ✅ 关开关 |
| **P2** | 全文列：`doc_text`（≤10 万字） | P1 | 🟡 数据暴露面扩大 | ✅ |
| **P3** | 超大文档分段表 `doc_segments` | P2 | 🟢 低 | ✅ |
| **P4** | 附件列（原件）+ 读回退 | P0 权限 / P2 | 🔴 较高（进关键路径） | ✅ |

**建议的验收节奏**：P1 上线后观察 2 周，确认「台账能覆盖全部文档请求」（用 advisorlog 的 `doc_id` 非空记录数 vs `doc_archive` 行数做对账），再决定是否推进 P2+。

> **P1 单独就已经解决了 G2（审计留痕）**，且几乎零风险 —— 这是投入产出比最高的一步。

---

## 8. 配置与开关

| 名称 | 形式 | 默认 | 说明 |
|---|---|---|---|
| `CT_FEISHU_DOC_ARCHIVE` | 环境变量 | `off` | 总开关。`off` → 零 HTTP 调用 |
| `CT_FEISHU_DOC_ARCHIVE_TEXT` | 环境变量 | `off` | 是否写全文列（P2） |
| `CT_FEISHU_DOC_ARCHIVE_ATTACH` | 环境变量 | `off` | 是否传附件（P4） |
| `CT_FEISHU_DOC_READ_FALLBACK` | 环境变量 | `off` | 读回退（P4） |
| `FEISHU_DOC_TABLE_ID` | 常量 | — | 表 1 的 `table_id`（建表后回填） |
| `FEISHU_DOC_TEXT_MAX` | 常量 | `100_000` | 单格全文上限 |
| `FEISHU_DOC_SEG_CHARS` | 常量 | `50_000` | 分段大小 |
| `FEISHU_BATCH_MAX` | 常量 | `500` | 单次批量（取官方保守口径） |

---

## 9. 测试计划

新增 `tests/test_feishu_doc_archive.py`（**离线，stub 掉 HTTP 层**），断言：

1. 开关 `off` → **HTTP 调用次数为 0**（最重要的一条）。
2. 全文边界：99,999 / 100,000 / 100,001 字 → 分别落在 `doc_text` / `doc_text` / `doc_segments`。
3. 分段数学：200 万字 → 40 段，每段 ≤ 50,000，拼接后与原文逐字节相等。
4. `client_token` 由 `doc_id` 确定性派生（同 id 两次调用 token 相同；不同 id 不同）。
5. 写入器内部抛异常 → **不向外传播**，且答案链路结果不变。
6. `mode=file`：`upload_all` → `file_token` → 附件字段 payload 形状正确。
7. `mode=ref`：不新增行，只 `batch_update`（`hits` +1）。

**回归红线**：不得改动 `ingest_and_select` 的**签名与返回值**（`(evidence, meta)`），确保 `tests/test_doc_pipeline.py`（85 项）与 `tests/test_deliverable_boundary.py`（59 项）原样通过。

---

## 10. 风险、未知与门禁

### 10.1 🔴 门禁一：数据合规（**必须先过**）

用户上传的是**临床试验方案 / CSR / 伦理批件**这类文件，可能包含**患者数据、申办方保密信息、或处于 NDA 之下**。写入飞书云文档意味着：

- 数据离开原有边界，进入飞书云（可能涉及**数据出境**）；
- 该多维表格的**全部协作者**可见；
- **没有 TTL**（与 `doc_store` 的 30 天不同）→ 一旦写入即长期留存。

> **口径对照**：今天飞书里**没有**文档正文，只有 `doc_id`/`char`/`fp` 这类**指针**。本方案是**实质性地扩大数据暴露面**，不是格式调整。

**建议**：先拿到明确许可；若不可，则**只做 P1（元数据 + 20,000 字 preview 也可关掉）**——审计价值的大部分仍在，暴露面与今天基本持平。同时补上保留策略与访问控制。

### 10.2 🟠 门禁二：权限探针（实施前 30 分钟可完成）

用一个最小脚本验证现有凭据能做什么：

1. 对**新表** `batch_create` 写 1 行、再删掉 → 验表级写权限；
2. 上传 1 个 <1 KB 的测试文件到 `drive/v1/medias/upload_all` → 验**附件能力是否存在**；
3. 若 2 失败 → **P4 的附件列直接砍掉**，不起负面作用。

> 这一步没有做之前，任何关于"附件归档"的承诺都是猜的。

### 10.3 🟡 限流与批量口径不一致

官方中文页（1,000 条/次、50 QPS）与英文页/SDK（500 条/次、10 QPS）不一致。→ 按保守值实现，常量可调。

### 10.4 🟡 请求体过大

单格 10 万字（中文 UTF-8 约 300 KB）可能触发 `1254030 TooLargeResponse`。→ 策略：全文列**单请求**写入；若被拒，**自动降级为分段写**（复用 §5.4 的分段逻辑），不视为失败。

### 10.5 🟡 免费版单表行数

台账表 5,000 行上限。→ 加监控（`doc_archive` 行数），超 80% 告警；必要时归档冷数据到表 2 之外的年度表。

### 10.6 🟡 原件只对 `mode=file` 可得（**重要认知**）

| mode | Coze 端手上有什么 | 能否存原件 |
|---|---|---|
| `file` | **原始字节**（`file_b64`） | ✅ |
| `full` / `chunks` | 仅**解码后的文本** | ❌ 原件从未上传 |
| `ref` | 无正文 | ❌ |

即：**"把用户上传的原件都存下来"这个目标，今天拿不到** —— 只有走老格式转发路径（`mode=file`）的才有字节。要做到全覆盖，需要**改本地协议**（让本地在所有模式下都带原文件），属于更大的改动，建议**单独立项**，不混进本方案。

---

## 11. 工作量与文件清单

| 文件 | 动作 | 规模 |
|---|---|---|
| `src/graphs/nodes/feishu_auth.py` | 新增（从 writer 抽出鉴权） | ~30 行 |
| `src/graphs/nodes/feishu_doc_writer.py` | 新增（归档写入器） | ~180 行 |
| `src/doc/__init__.py` | 改（落盘后加 `_maybe_archive` 调用） | ~10 行 |
| `tests/test_feishu_doc_archive.py` | 新增 | ~150 行 |
| `docs/feishu-doc-archive.md` | 新增（实施后转正式文档） | — |
| `config/full_analysis_cfg.json` | 不改 | — |

---

## 12. 建议的下一步（最小可验证路径）

1. **今天就能做**：跑 §10.2 的权限探针（30 分钟），把"能做/不能做"钉死。
2. **同步确认**：§10.1 的合规口径（这是唯一可能一票否决的事项）。
3. **两项都过** → 实施 **P1**（台账 + 元数据，不写全文、不传附件），2 周后对账。
4. **对账通过** → 再决定 P2（全文）与 P4（读回退）。

---

## 附：被否决的备选方案

| 方案 | 否决理由 |
|---|---|
| 用**电子表格**存 | 单元格模型对长文本不友好；无附件字段、无记录级 API；需要另开一套 API 与权限 |
| 用**云文档**每份文档建一个文件 | 无结构化查询/统计能力；需 drive 建文档权限；无法与 advisorlog 便捷关联 |
| 把飞书当**主存储**（替掉 doc_store） | 把网络 IO 放进关键路径，延迟与可用性都劣化。飞书应是**副本 + 审计面**，不是一线 |
| 把全文塞进 advisorlog 的 `final_answer` 信封 | 会污染现有信封格式、膨胀缓存与表格；且已回答 `doc_id`，另表存正文更干净 |
