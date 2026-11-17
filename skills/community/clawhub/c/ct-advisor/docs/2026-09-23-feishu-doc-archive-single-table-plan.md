# 用户上传文档落库飞书：单表方案（写入既有 advisorlog 表）

- ⚠️ **本稿未采纳（作废标注，2026-09-25）**：最终落地**既非单表也非双表存正文**，而是**独立附件表 `filelog`**（`Source_ID`=advisorlog 自动编号 int 关联，存附件 file_token）。统一规范见 ct-base §20.16；实现 = coze v1.27–v1.36。本页保留作方案演进对照。
- **日期**：2026-09-23
- **状态**：评估稿，**尚未实施**（不含任何已生效的代码改动）
- **取代**：`2026-09-23-feishu-document-archive-plan.md`（双表方案）——本稿按「不新建数据表」口径重做
- **载体**：**既有的 advisorlog 表** `app_token = Pog0bGNMbaCWMIsGRNpckHcnn9f` / `table_id = tblA2mEaE7TJtI0u`
- **结论**：**可行**。列数已从初稿的 9 列压到 **最少 1 列 / 推荐 2 列**（推导见 §3.1）。
- **两个前置条件**：🔴 数据合规（§9.1）、🟠 权限探针（§9.2）；另有**一个必须权衡的硬风险**（行数预算共用，§4）。

---

## 0. 相对上一版（双表方案）的差异总览

| 维度 | 双表方案（上一版） | **单表方案（本稿）** |
|---|---|---|
| 表结构 | 新建 `doc_archive` + `doc_segments` 两张表 | **复用 advisorlog**，**最少新增 1 列 / 推荐 2 列**（§3.1） |
| 凭据 | 复用 `integration-feishu-base` | **同上**（同一 app_token，零新增集成） |
| 跨表关联 | 靠 `doc_fp` 跨表 join | **消除**——同一张表内直接按 `doc_id` 取值 |
| 正文载体 | 新表的 `doc_text` 列 | **既有 `final_answer` 列**（能力等价，见 §3.2） |
| 行数预算 | 文档行有**独立**预算 | 🔴 **与问答日志共用同一预算**（本稿头号风险） |
| 现有视图/统计 | 完全不受影响 | 🟡 P1 阶段完全不受影响；P2 起需加一条 `doc_id 为空` 筛选（§3.6） |
| 去重 | 误以为可用 `client_token` 长期幂等 | ✅ **改为写入前 `records/search`**（§7） |
| 超 10 万字文档 | 写入 `doc_segments` 分段表 | 同表 **多行**分段（功能等价，仍占行数；此时 +1 列） |
| 运维成本 | 多一张表要看 | **只维护一张表**（用户诉求） |

> 单表方案的真实收益是**运维面变窄**（一个表、一套视图、一套权限、零跨表 join）；真实代价是**行数预算被共用**。两者都要摊在桌面上。

---

## 1. 现状：链路与既有写入器

### 1.1 图顺序与两个写入点（本次核对的关键发现）

```
doc_ingest ──▶ cache_check ──▶ generate_organized_problems ──▶ full_analysis ──▶ tool_router
     │              │                                              │
     │              └─ 缓存命中 → async_feishu_write()  ← 写入点 ②  │
     │                               （cache_check_node.py:194）    │
     │                                                             │
     └─ 唯一在缓存闸之前运行的节点                          写入点 ①
                                       （full_analysis_node.py:458）
```

**这条顺序决定挂载点**：`async_feishu_write` 有**两个**调用点，缓存命中时**只走 `cache_check_node`**。因此任何归档设计都必须挂在 `doc_ingest` 上，**不能**挂在 `full_analysis`（否则缓存命中的请求会漏归档）。

而 `doc_ingest` 恰好也是**唯一持有 `doc_context` 原始载荷**的节点，且它每轮都执行（本地默认每轮随载荷携带正文）。

### 1.2 advisorlog 表结构（代码即单源真源）

`src/graphs/nodes/async_feishu_writer.py` 顶部两个常量定义了整张表：

```python
FEISHU_APP_TOKEN = "Pog0bGNMbaCWMIsGRNpckHcnn9f"
FEISHU_TABLE_ID  = "tblA2mEaE7TJtI0u"

ADVISORLOG_FIELDS = [            # 8 个固定列（2026-09-09 定稿，写前不查 schema）
    "difficulty", "category", "original_question", "organized_problems",
    "accuracy", "final_answer", "query_origin", "inittime",
]

ADVISORLOG_FIELDS_OPTIONAL = [   # 13 个「机会性写入」列（2026-09-20 起）
    "cache_hit", "similarity", "answer_len", "finish_reason",
    "kb_sections", "kb_terms_hit", "kb_evidence", "kb_route_pass", "scope_notice",
]
```

两个机制值得直接复用：

1. **`_supported_optional_fields()`**——进程内缓存一次 `GET /fields?page_size=100`，只写"表里真实存在"的列。**这正是新方案需要的列探测机制，不需要另写。**
2. **自愈降级**——带增强列的写入被拒 → 回退为基础列重试一次，并清缓存。新方案照抄。

> 🔑 **这 8 个固定列没有一个是空置的**——每个都在问答路径上服役（`difficulty`/`category`/`accuracy` 进统计，`query_origin` 是审计标识）。所以"借用既有列"必然要付语义代价，见 §2 变体 3。

### 1.3 `doc_meta` 已在信封里，但**不能**用来传正文

`final_answer` 列实际承载的是 JSON 信封：

```json
{"answer": "...", "skill_version": "...", "coze_version": "1.24",
 "cache_hit": false, "answer_len": 1234, "kb_evidence": 3,
 "doc_id": "doc_xxx", "doc_chars": 32000, "doc_chunks": 6,
 "doc_total_chunks": 41, "doc_fp": "a1b2...", "doc_mode": "full"}
```

⚠️ **`doc_meta` 参与缓存键**——`cache_fingerprint(conversation_history, doc_meta)` 取 `doc_meta["doc_fp"]`（`cache_manager.py:161`）。所以：

> **红线：绝不把全文写进 `doc_meta`。** 它会同时污染 `state`、缓存键与信封格式。这一条是本方案所有设计取舍的起点。

**副产品**：信封里已经有 `doc_id` / `doc_chars` / `doc_fp` / `doc_mode` / `doc_total_chunks`——**在问答行上**。这是"文档行可以极简"的根据之一（§3.1）。

---

## 2. 三个结构变体（先选结构，再谈实现）

### 变体 1 · 同表「文档行」（**推荐**）

文档作为**独立一行**写进 advisorlog，只填**新增的 2 个列**，正文进既有 `final_answer` 列，其余原列一律留空。

```
row 1  doc_id=""        original_question="样本量怎么算的？"  final_answer={...信封...}   ← 问答行（逐字节不变）
row 2  doc_id="doc_xxx" doc_name="方案_v3.docx"  final_answer="...文档正文..."            ← 文档行
row 3  doc_id=""        original_question="那脱落率呢？"      final_answer={...信封...}   ← 问答行
```

- ✅ **判别位由 `doc_id` 非空承担**——不需要单独的 `row_type` 列。
- ✅ **问答行零污染**：`difficulty`/`category`/`accuracy`/`organized_problems`/`query_origin` 对文档行留空，原列语义与统计不变。
- ✅ **1 文档 1 行**：`doc_id` 去重后行数 = 文档数，可预测。
- ✅ **独立可筛**：`doc_id 不为空` 一条筛选就是台账视图；`doc_id 为空` 即恢复今日语义。
- ⚠️ 行数与问答日志**共用预算**（§4 头号风险）。
- ⚠️ P2 起文档正文与"答案"同用 `final_answer` 列——**这是省列的代价**，见 §3.6。

### 变体 2 · 同行附带（备选，零新增行）

不新增行，把新列填在**带来该文档的那一次问答行**上。

- ✅ **零新增行**，现有视图与统计**完全不动**。
- ⚠️ 无独立台账视图；文档正文分散在历史行里。
- ⚠️ 容器回收后同一文档再次上传 → 会在**另一行**再写一份（跨会话无去重锚点）。
- ⚠️ 需要本地 `has_doc(doc_id)` 判断"是否首次见到"，而这个判断正是因为 G1 才不可靠。
- ⚠️ **同一行要同时装"出参信封"和"文档正文"** → 两者挤在 `final_answer` 一格，会撞 10 万字上限。

> 选它的唯一理由：**行数预算已经紧张，或现有视图不可改**。否则用变体 1。

### 变体 3 · 零 schema 变更（0 新增列）——**可行但检索降级**

连 1 列都不加，全靠既有列承载：

```python
{
  "query_origin":      "ct-advisor/doc",                        # ← 判别位（既有列，机器标识）
  "final_answer":      "[doc_id: doc_xxx]\n" + text[:100_000],  # ← 正文，检索键埋首行
  "original_question": "[文档] " + doc_name,                    # ← 可读性
  "inittime":          ms,
}
```

| 代价 | 说明 |
|---|---|
| **检索降级** | `doc_id` 只能埋进正文，filter 只能用 `contains`（子串匹配）而非 `is`（精确匹配）→ 可能误命中、性能差。**去重与读回退都建在沙子上** |
| **判别位不可靠** | 依赖改 `query_origin` 的值域；若该列有下游消费方（审计统计），会混入文档行 |
| **审计列被占用** | `final_answer` 在问答行是"出参"，在文档行是"正文"，同列双语义 |

> **变通（可恢复精确匹配）**：把**裸 `doc_id`**（不加 JSON 外壳）放进 `organized_problems` 列——该列在问答行存的是 JSON 数组字符串，文档行存裸 id 会让 filter 能用 `is` 精确匹配。代价是破坏该列的类型契约（消费方若 `json.loads` 会崩）。
>
> **结论**：只在"完全不允许改表结构"时使用。

---

## 3. 字段设计：为什么最少只需 2 列

### 3.1 逐列推导——9 列里只有 1 列不可省

判据只有一条：**这一列承载的信息，能否从别处得到？**

| 初稿提议列 | 必要性 | 替代方案 |
|---|---|---|
| `doc_id` | 🔴 **不可省** | 无。它是**判别位 + 精确检索键 + 去重键**三合一（filter 只能对"独立列"做 `is` 精确匹配） |
| `doc_name` | 🟢 **推荐加** | 不加就得塞进 `original_question`（污染该列语义）。1 列换可读性，值得 |
| `row_type` | ❌ **删** | **`doc_id` 非空 ⇔ 文档行**，判别位已有；再要一个就是冗余 |
| `doc_text` | ❌ **删** | 正文进既有 `final_answer` 列——同为自由文本、同为 **10 万字上限**，能力完全等价（§3.2） |
| `doc_preview` | ❌ **删** | preview 的意义是"长文档里看开头"；正文截断到 10 万字后开头**本来就在**，小文档则全文即 preview |
| `doc_chars` | ❌ **删** | 纯冗余：`doc_chars` 已在**问答行**的 `final_answer` 信封里（§1.3）。要按大小判断，看正文长度即可 |
| `doc_status` | ❌ **删** | 只在**失败**时才需要状态；而失败时**根本不写文档行**。"超大"由分段行的存在表达 |
| `seg_index` | 🟡 **P2b 才要** | 只有做 >10 万字分段时才需要（+1 列）。**不能**靠 `inittime` 排序替代（并发/补写会乱序） |
| `doc_file` | 🟡 **P3 才要** | 附件列**无法用任何既有列替代** → 要存原件就必须 +1 列 |

> **结论：最少 1 列（`doc_id`）；推荐 2 列（+ `doc_name`）。**
> 分期视角：**P1 与 P2 都只需这 2 列**；P2b 分段 +1；P3 原件 +1。

### 3.2 省列的关键：正文放进既有 `final_answer` 列

`final_answer` 是表里唯一"自由文本 + 10 万字上限"的既有列——**新建 `doc_text` 列的能力与它完全相同**，所以新建属于重复建设。

区别只在语义：问答行的 `final_answer` 是"本次出参"（JSON 信封或兜底纯文本），文档行是"文档正文"。**用 `doc_id` 是否为空即可区分。**

> ⚠️ **更正初稿的一处论断**：初稿在 §2 变体 3 里批评过"往 `final_answer` 塞正文会与 JSON 信封互相挤压、易撞 10 万字上限"。**那条批评只对"同行附带"（变体 2）成立**——那一行既要装出参信封、又要装正文。在"独立文档行"（变体 1）里，文档行**不需要出参信封**，一格只装正文，挤压不存在。

### 3.3 需新增的列（2 个）

| 列名 | 类型 | 类型码 | 用途 |
|---|---|---|---|
| `doc_id` | 文本 | 1 | **唯一不可省的列**：判别位（非空 = 文档行）+ 精确检索键（`operator: "is"`）+ 去重键 |
| `doc_name` | 文本 | 1 | `file_name`（`mode=file`）或 `title`，供人工识别。**可省**，但省了就得污染 `original_question` |

**已确认不加的列**：`doc_fp` / `doc_mode` / `doc_chars` / `doc_total_chunks` / `doc_selected_chunks` —— 已在**问答行**的 `final_answer` 信封里，加列就是第二份需要同步的真相。

> 💡 若筛选器不支持 `isNotEmpty` 操作符，退化用官方「常用筛选公式」表里的写法：`NOT(CurrentValue.[doc_id] ="")`。

### 3.4 主字段（primary field）的处理——**必须先探测**

飞书表有一个 `is_primary: true` 的索引字段。写入记录时**若主字段是文本类而留空，可能被拒**。所以：

```python
# 复用既有探针：GET /fields?page_size=100 的返回里同时能拿到 is_primary
# 实现上扩展 _supported_optional_fields()，让它一并返回 primary_field_name
```

| 主字段类型 | 处理 |
|---|---|
| 自动编号（`type=1005`）/ 创建时间（`1001`）| **不用管**，系统自动填 |
| 文本（`type=1`）| 文档行填 `"[文档] " + doc_name`，分段行填 `"[文档段] " + doc_name` |
| 日期（`type=5`）| 文档行填同一毫秒时间戳 |

> ⚠️ **必须在实施前用一次 `GET /fields` 实测确认。** 若主字段恰是 `original_question` 这类既有列，文档行会不可避免地在该列留下一个 `[文档] xxx` 值——这是单表方案里唯一无法完全避免的轻微污染，**需事先认可**。

### 3.5 文档行写入字段（示例）

```python
doc_record = {
    # —— 新增列（仅 2 个）——
    "doc_id":       meta["doc_id"],
    "doc_name":     file_name or meta.get("title") or "",
    # —— 既有列：正文进 final_answer（P2 起；P1 阶段留空）——
    "final_answer": text[:100_000],                 # ≤10 万字全文；超出部分交给分段行走
    "inittime":     int(time.time() * 1000),
    # —— 主字段（按 §3.4 探测结果决定是否填）——
}
# 注意：不写 difficulty / category / organized_problems / accuracy /
#       query_origin —— 这 5 个原列对文档行一律留空，零污染。
```

**问答行一行代码都不用改** —— 新列对它们是空值，`ADVISORLOG_FIELDS` 的 8 列取值逻辑与今天逐字节相同。

> 若做了 P2b 分段：`final_answer` 放第 0 段，其余段各自成行，靠 `seg_index` 列排序（此时才 +1 列）。

### 3.6 省列的代价（必须接受的两条）

| 代价 | 影响面 | 若不接受，怎么办 |
|---|---|---|
| ① `final_answer` 同列双语义（**仅 P2 起**）| 任何**按答案列做统计 / 导出 / 正则清洗**的现有动作会多出文档行 → 需加 `doc_id 为空` 过滤 | 加 1 列 `doc_text`（变 3 列），文档行的 `final_answer` 留空 → 现有消费方零影响 |
| ② 判别位是"空 / 非空"而非显式标签 | 可读性略降（要先看列值才知道是文档行）；将来若要区分更多行类型需再加列 | 加 1 列 `row_type`（单选，变 3 列），筛选条件更直白 |

> **一句话**：**2 列是"少加列"与"不动现有消费方"之间的平衡点**。
> **P1 阶段尤其划算**：只写 `doc_id` + `doc_name`、正文留空 → **连代价 ① 都不存在**，现有视图与消费方完全不受影响。
> 若"现有消费方不能动"是硬约束，则从 P2 起改用 3 列（`doc_id` + `doc_name` + `doc_text`）。

---

## 4. 🔴 头号风险：单表行数预算共用

### 4.1 官方行数事实（本次核对）

| 版本 | 单数据表行数上限 |
|---|---|
| 基础版（**免费**）/ 商业标准版 | **2,000 行** |
| 商业专业版 | 20,000 行 |
| 商业旗舰版 / 企业版 | 50,000 行 |
| 硬上限（购买扩容包后）| 单表 **200 万**行；单个多维表格文件总行数 ≤ **1,000 万**行 |

> 📌 **免费版与商业标准版可免费额外领取 1.8 万行权益**（数据表右侧 `︙` → 领取行数权益），即实际可按 **2 万行**规划。系统在通过表单/接口写入触顶时会**自动领取**该权益并通知所有者。

### 4.2 为什么这在单表方案里是风险，在双表方案里不是

> ⚠️ **官方原文：「超出行数上限的数据表将无法新增记录。」**

双表方案里，文档行写在 `doc_archive`，问答日志写在 advisorlog，**各有各的 2,000 行预算**——文档表满了，日志照写。

单表方案里两者共用一份预算。**一旦触顶，连问答日志都会写不进去** —— 这会让一个"归档功能"的故障升级为"审计留痕整体失效"。风险等级从局部升为全局。

### 4.3 缓解措施（缺一不可）

1. **先查数**：实施前记录 advisorlog 当前行数上限与实际行数，算出剩余预算。
2. **领权益**：若在免费/标准版，先领那免费的 1.8 万行（把预算从 2,000 拉到 20,000）。
3. **真去重**：`records/search` 拦住重复文档（§7）；否则同一文档在容器回收后会重复写入。
4. **行数告警**：达上限 80% 时告警（飞书仪表盘或人工周检）。
5. **兜底退路**：若文档量级可能与日志同量级，回退双表——**这条退路必须写进实施文档，否则等于没有**。

---

## 5. 挂载点与数据流

### 5.1 为什么挂在 `doc_ingest`（而不是复用现有写入器）

| 理由 | 依据 |
|---|---|
| 它是**唯一在缓存闸之前**执行的节点 | 缓存命中走 `cache_check_node` 的写入点，挂 `full_analysis` 会漏 |
| 它**独家持有 `doc_context`**（含 `file_b64`） | 原件字节只在这里可得 |
| 每轮都执行 | 本地默认每轮随载荷携带正文，故每轮都能触发（去重会拦住重复） |

### 5.2 全文怎么拿：**加一个可选回调**（关键设计）

问题：`ingest_and_select()` 只返回 `(evidence, meta)`，**正文 `text` 与 `file_info` 都在它的局部作用域里**。而 `meta` 不能扩（§1.3 红线）。

| 解法 | 评价 |
|---|---|
| 把全文塞进 `meta` | ❌ 违反 §1.3 红线（污染缓存键 / state / 信封） |
| 归档逻辑写进 `src/doc/__init__.py` | ❌ 让纯计算包依赖飞书，破坏分层 |
| **加可选回调参数 `on_ingest=None`** | ✅ **采用**：签名向后兼容，`src/doc/` 仍不知道飞书的存在 |

```python
# src/doc/__init__.py —— 仅新增一个可选参数，默认 None 时行为逐字节不变
def ingest_and_select(doc_context, question="", top_k=DEFAULT_TOP_K,
                      max_chars=None, on_ingest=None):
    ...
        if not stored:
            stored = save_doc(payload.doc_id, chunks, {...})
        # ↓ 新增：落盘之后回调（尽力而为；异常一律吞掉，绝不阻断）
        if on_ingest is not None:
            try:
                on_ingest(payload=payload, chunks=chunks, text=text, file_info=file_info)
            except Exception:
                pass
```

> ⚠️ **为什么不能从 `doc_store` 反查全文**：`save_doc()` 只存 **chunks**，不存原始 text；而 `split_chunks` 的 `OVERLAP=120` 让相邻块有重叠，**拼接块会产出约 15% 的重复文本**，不是原文。所以全文只能从回调拿。

### 5.3 节点侧接线（开关关闭时零开销）

```python
# src/graphs/nodes/doc_ingest_node.py
_hook = None
try:                                     # 延迟导入 + 开关判断
    from graphs.nodes.feishu_doc_archive import archive_hook_if_enabled
    _hook = archive_hook_if_enabled()    # 开关 off → 直接返回 None
except Exception:
    _hook = None

evidence, meta = ingest_and_select(doc_context, question, top_k=TOP_K, on_ingest=_hook)
```

开关关闭时：**不导入归档模块、不调用回调、零 HTTP** → 行为与今天一致（回归红线）。

### 5.4 闭环数据流

```
doc_ingest_node
  └─ ingest_and_select(..., on_ingest=hook)
        ├─ payload 解析 → chunks → save_doc(doc_store)
        └─ on_ingest(payload, chunks, text, file_info)
              └─ 守护线程：records/search(doc_id) ─命中─▶ 跳过
                                                 └─未命中─▶ batch_create(文档行)
                                                             └─ >10万字 ─▶ 追加分段行
```

**归档线程与主流程完全解耦**（守护线程 + 失败静默），不合并进问答日志的批次——理由是两条写入路径分处不同节点（§1.1），强行同批会把它们耦合，并引入"归档失败连带日志失败"的新故障模式。**独立 = 失败域隔离**，这比省一次后台 HTTP 重要得多。

---

## 6. 模块与代码改动清单

| 文件 | 动作 | 规模 | 说明 |
|---|---|---|---|
| `src/graphs/nodes/feishu_doc_archive.py` | **新增** | ~200 行 | 归档写入器；复用 `async_feishu_writer` 的鉴权与探针 |
| `src/doc/__init__.py` | 改 | ~8 行 | `ingest_and_select` 加 `on_ingest=None` 回调 |
| `src/graphs/nodes/doc_ingest_node.py` | 改 | ~12 行 | 开关开启时传回调 |
| `tests/test_feishu_doc_archive.py` | **新增** | ~180 行 | 离线测试，stub HTTP 层 |
| `docs/feishu-doc-archive.md` | 新增（实施后） | — | 转正式文档 |
| `config/full_analysis_cfg.json` | **不改** | — | — |
| `src/graphs/nodes/async_feishu_writer.py` | **不改** | — | 见 §6.1 |
| 飞书表结构 | 人工 | **+2 列** | `doc_id` / `doc_name`（后台手动加，约 2 分钟） |

### 6.1 刻意不改动在服役的日志写入器

```python
# feishu_doc_archive.py —— 复用，不复制
from graphs.nodes.async_feishu_writer import (
    _get_access_token,            # 同一套 coze_workload_identity 凭据
    _supported_optional_fields,   # 同一套列探测（含进程内缓存）
    FEISHU_APP_TOKEN, FEISHU_TABLE_ID,
)
```

理由：`async_feishu_writer.py` 是**每天在跑的审计主通道**，任何改动都有回归风险；而新功能只需要它的两个内部工具。**P1 先用私有名复用，不改它一行。**

---

## 7. 去重与幂等（本稿对上一版的实质纠错）

### 7.1 ❌ 上一版的错误

上一版写道：「`client_token = uuid5(NAMESPACE_URL, doc_id)` → 同一份文档重复上传 → 同一个 token → 飞书侧幂等，**不产生重复行**。」

**这是错的。** `client_token` 有明确时效（飞书开放平台通用语义）：

> 「client_token 有时效性。……如果接口实际成功了，**幂等行为会保持 5 分钟**。过期后同一个 client_token 也会被视作是全新的 token。」
> 「不能将 client_token 当作资源 ID 使用。」
> 并发同 token → 错误码 `1470422`。

即：`uuid5(doc_id)` 这种**确定性长期 token** 只能防"5 分钟内的重复提交"（重试、双击），**完全防不住"同一文档几天后再上传"**——而那正是 G1 场景下最常发生的。

### 7.2 ✅ 正确的去重：写入前 `records/search`

```
① POST /records/search
   body = {"filter": {"conjunction": "and",
                      "conditions": [{"field_name": "doc_id",
                                      "operator":   "is",
                                      "value":      [doc_id]}]}}
   → items 非空 → 已归档，跳过
   → items 为空 → ②
② POST /records/batch_create?client_token=<uuid5(doc_id)>
   → client_token 仍然带：不是为了长期去重，而是为了**防 5 分钟内的重试重复**
```

filter 语法要点（来自《记录筛选参数填写说明》）：
- `value` 必须是**字符串数组**（即使字段是数字类型）；
- 只支持**一层** `children`，不能嵌套多层；
- 精确匹配用 `operator: "is"`。

> 📌 这也是 `doc_id` **必须独立成列**的根本原因：只有独立列才能被 filter 精确匹配，`doc_id` 才能同时充当去重键与取回键。

### 7.3 成本控制

每轮带文档的请求会多 1 次 `search`（后台线程内，用户无感）。若一次会话对同一文档追问 10 轮 → 10 次 search。

**优化（建议纳入 P1）**：进程内 `set` 记忆已归档的 `doc_id`
`if doc_id in _archived: return` —— 同容器内零额外 HTTP；跨容器时由 `search` 权威兜底。

---

## 8. 分期落地

| 阶段 | 内容 | 需新增列 | 依赖 | 风险 | 可独立回滚 |
|---|---|---|---|---|---|
| **P0** | ① 合规确认（§9.1）② 权限探针（§9.2）③ **后台加 2 列** ④ **查行数上限/当前行数 + 领取免费行数权益** ⑤ **`GET /fields` 确认主字段** | — | 人工 | — | — |
| **P1** | 文档行落库：**只写 `doc_id` + `doc_name`**（**不含正文、不含附件**） | `doc_id` `doc_name` | P0 | 🟢 极低 | ✅ 关开关 |
| **P2** | 正文进 `final_answer`（≤ 10 万字） | **0**（复用既有列） | P1 | 🟡 暴露面扩大 | ✅ 关开关 |
| **P2b** | >10 万字：同表分段行（每段 ≤ 5 万字） | +`seg_index` | P2 | 🟢 低 | ✅ |
| **P3** | 附件列 `doc_file`（仅 `mode=file`）+ 读回退（治 G1） | +`doc_file` | P0 权限 / P2 | 🔴 较高（进关键路径） | ✅ 独立开关 |

**验收节奏**：P1 上线观察 2 周，用「advisorlog 中 `doc_id` 非空的记录数」对账「实际归档的文档数」——同一 `doc_id` 只应出现在一行。对账通过再推 P2。

> **P1 单独就解决了 G2（审计留痕）**，且几乎零风险、零新增列代价：因为 P1 不写正文，`final_answer` 对文档行留空，现有视图与消费方**完全不受影响**。

---

## 9. 风险、门禁与诚实边界

### 9.1 🔴 门禁一：数据合规（未变，且不因单表而减轻）

用户上传的多是**临床试验方案 / CSR / 伦理批件**，可能含患者数据或受 NDA 约束。写入飞书云文档意味着：数据离开原边界、该多维表格**全部协作者可见**、且**没有 TTL**（与 `doc_store` 的 30 天不同）。

> **今日飞书里只有"指针"（`doc_id`/`doc_chars`/`doc_fp`），没有正文。** 本方案是**实质性地扩大数据暴露面**，不是格式调整——单表双表都一样。

若不合规：**退化为只做 P1**（只写 `doc_id` + `doc_name`，正文一律不落）——审计价值（"哪次请求用了哪份文档"）仍然拿到，暴露面与今天持平。

### 9.2 🟠 门禁二：权限探针（约 30 分钟）

用一个最小脚本验证现有凭据：

1. 对 advisorlog **新增列后**能否 `batch_create` 写 1 行文档行（再删掉）→ 验列级写权限；
2. `POST drive/v1/medias/upload_all` 上传 1 个 <1 KB 文件 → 验**附件能力是否存在**；
3. 2 失败 → **P3 的附件列直接砍掉**，不留悬念。

> 没有这一步，任何"附件归档"的承诺都是猜的。

### 9.3 🟡 原件只有 `mode=file` 可得（认知边界，未变）

| mode | Coze 端手上有什么 | 能存原件吗 |
|---|---|---|
| `file` | **原始字节**（`file_b64`）| ✅ |
| `full` / `chunks` | 仅**解码后文本** | ❌ 原件从未上传 |
| `ref` | 无正文 | ❌ |

即 **"把所有上传原件都存下来"今天做不到**。要全覆盖需改本地协议（让本地在所有模式下都带原文件），建议**单独立项**，不混进本方案。

### 9.4 🟡 其他

| 项 | 说明 |
|---|---|
| `final_answer` 双语义 | P2 起文档行正文与问答行出参同列（§3.6 代价 ①）→ 下游统计需加 `doc_id 为空` 过滤 |
| 批量/限流口径 | 频率限制两版现已**一致 = 50 次/秒**；但单次条数仍**不一致**（中文页 1,000 / 英文页 500）→ 按保守值 500 实现，做成常量 |
| 请求体过大 | 单格 10 万字（中文 UTF-8 ≈ 300 KB）可能触发 `TooLargeResponse` → 拒则自动降级为分段行，不视为失败 |
| 单元格文本上限 | **100,000 字**/格；附件 ≤ 100 个/格；单表附件总数 ≤ 20,000 个 |
| 只增不减 | 归档行**只能累积**（P1 先不做删除）；一旦写错只能人工清 |

---

## 10. 测试计划

新增 `tests/test_feishu_doc_archive.py`（**离线，stub 掉 HTTP**），断言：

1. **开关 `off` → HTTP 调用次数 = 0**（最重要的一条，含"不导入归档模块"）。
2. `ingest_and_select(..., on_ingest=None)` 的返回值 `(evidence, meta)` 与改造前**逐字节相同**（回调不改变任何返回）。
3. 回调抛异常 → **不向 `ingest_and_select` 传播**，主链路结果不变。
4. 文档行 payload 形状：**只含** `doc_id` / `doc_name` / `final_answer`（P2）/ `inittime`（+ 主字段）；
   **不含** `difficulty` / `category` / `organized_problems` / `accuracy` / `query_origin`（防污染回归）。
5. **P1 模式**（正文开关关）：`final_answer` **不出现在 payload 里** → 证明现有消费方零影响。
6. 去重：`search` 命中 → **不发** `batch_create`；未命中 → 发 1 次。
7. `client_token` 由 `doc_id` 确定性派生（同 id 同 token），且位于 **URL 查询参数**而非请求体。
8. 正文边界 99,999 / 100,000 / 100,001 字 → 分别截断为原长 / 原长 / 转为分段行（P2b）。
9. 分段数学：200 万字 → 40 行，每段 ≤ 50,000，拼接后与原文逐字节相等。
10. 主字段为自动编号时文档行**不填**主字段；为文本时填 `[文档] xxx`。
11. `mode=file`：`upload_all` → `file_token` → 附件字段 payload 形状正确。

**回归红线**：`ingest_and_select` 的**签名兼容性与返回值**不得变；`config/full_analysis_cfg.json` 不得动。现有 coze 端 238 项（`test_doc_pipeline` 85 / `test_legacy_office` 94 / `test_deliverable_boundary` 59）与脚本侧八套须全绿。

---

## 11. 配置与开关

| 名称 | 形式 | 默认 | 说明 |
|---|---|---|---|
| `CT_FEISHU_DOC_ARCHIVE` | 环境变量 | `off` | **总开关**。`off` → 完全不导入归档模块、零 HTTP |
| `CT_FEISHU_DOC_ARCHIVE_NAME` | 环境变量 | `on` | 是否写 `doc_name`。关掉 → **1 列模式**（只写 `doc_id`） |
| `CT_FEISHU_DOC_ARCHIVE_BODY` | 环境变量 | `off` | 是否把正文写进 `final_answer`（P2）。关掉 = P1 行为 |
| `CT_FEISHU_DOC_ARCHIVE_SEG` | 环境变量 | `off` | 分段（P2b，需 `seg_index` 列） |
| `CT_FEISHU_DOC_ARCHIVE_ATTACH` | 环境变量 | `off` | 附件（P3，需 `doc_file` 列） |
| `CT_FEISHU_DOC_READ_FALLBACK` | 环境变量 | `off` | 读回退（P3） |
| `FEISHU_DOC_BODY_MAX` | 常量 | `100_000` | 单格正文上限（与 `final_answer` 同格上限） |
| `FEISHU_DOC_SEG_CHARS` | 常量 | `50_000` | 分段大小（P2b） |
| `FEISHU_BATCH_MAX` | 常量 | `500` | 单次批量（保守口径） |

---

## 12. 读回退（P3，治 G1）

```
load_doc(doc_id) ─未命中─▶ POST /records/search filter doc_id is <id>（timeout 3s）
                              ├ 命中文档行（final_answer 有正文）→ split_chunks 重建块
                              └ 命中分段行 → 按 seg_index 排序拼接后重建块
```

**三条硬约束**：
1. **仅在 `mode=ref` 且本地未命中时**触发——绝不为 `full`/`chunks` 打网络（正文已在手上）。
2. **严格 3s 超时**，失败即降级为现有"未取回"提示；绝不让飞书抖动变成用户侧 5xx。
3. **独立开关**，默认关。

> ⚠️ 已知副作用：从文本重建块后 `§N` 编号可能与原始会话不同（分段发生在服务端）。对"引用某段"的场景影响轻微，但**须写进文档**，避免日后误判为 bug。

---

## 13. 待用户决策的 4 个点

| # | 决策 | 影响 |
|---|---|---|
| 1 | **允许新增 2 个列吗？** | 不允许 → 走变体 3（0 列，检索降级为子串匹配）；或维持双表 |
| 2 | **"按答案列做统计/导出"的现有动作可否加过滤？** | 不可 → 从 P2 起改用 3 列（加 `doc_text`），文档行的 `final_answer` 留空 |
| 3 | **现有视图能否各加一条筛选？** | 不能 → 倾向变体 2（同行附带，零新增行） |
| 4 | **advisorlog 当前行数上限与已用行数？** | 决定 §4 风险等级；决定是否先领 1.8 万行权益 |

---

## 14. 建议的下一步

1. **今天可做**：跑 §9.2 权限探针 + `GET /fields` 看主字段与当前列清单（30 分钟，钉死"能做/不能做"）。
2. **同步确认**：§9.1 合规口径（唯一可能一票否决）。
3. **前两项都过** → 实施 **P1**（只加 2 列、只写两个字段、**正文不落**）。这一步**零风险、零现有影响**。
4. **2 周后对账** → 再决定 P2（正文）/ P3（附件 + 读回退）。

---

## 附 A：官方事实核对表（本稿新增/更正项）

| 事实 | 上一版记载 | **本稿核实** | 出处 |
|---|---|---|---|
| `client_token` 幂等时长 | 未提（默认长期有效）| 🔴 **仅 5 分钟**；不能当资源 ID；并发同 token → `1470422` | 开放平台接口概述 |
| `client_token` 位置 | 未提 | **URL 查询参数**（非请求体）| `batch_create` 文档 |
| 单表行数上限（免费/标准）| 5,000 行 | 🔴 **2,000 行**（可免费领 1.8 万 → 2 万）| 多维表格付费权益说明 |
| 行数超限后果 | 未提 | 🔴 **整表无法新增记录** | 多维表格行数扩容 |
| `batch_create` 限流 | 中文 50/s、英文 10 QPS | 🟠 **两版均 50 次/秒**（已一致）| 中/英文页 |
| `batch_create` 单次条数 | 中文 1,000 / 英文 500 | ⚠️ 仍不一致（按 500 实现）| 中/英文页 |
| 单元格文本上限 | 100,000 字 | ✅ 维持 | 帮助中心 |
| 字段类型码 | 未列 | 1 文本 / 2 数字 / 3 单选 / 5 日期 / 7 复选框 / 17 附件 / 1005 自动编号 | 字段编辑指南 |
| 主字段标识 | 未提 | `is_primary: true` | 字段编辑指南 |
| filter 语法 | 未列 | `{"conjunction","conditions":[{"field_name","operator":"is","value":[…]}]}`，`value` 为**字符串数组**，仅一层 `children` | 记录筛选参数填写说明 |

## 附 B：变体与列数选择速查

| 若你的约束是… | 选 | 新增列数 |
|---|---|---|
| 只是不想多一张表（**默认**）| **变体 1**：同表文档行，正文进 `final_answer` | **2**（P1/P2 均只需 2；P2b +1、P3 +1）|
| 想要最小的 schema 变更 | 变体 1 的 `doc_name` 也关掉 | **1** |
| 现有消费方不能动（按答案列统计）| 变体 1 改用 `doc_text` 独立列 | **3** |
| 现有视图不能改 / 行数预算紧张 | **变体 2**：同行附带，零新增行 | 2（或 3）|
| 连加列都不允许 | **变体 3**：0 列，检索降级 | **0** |
| 文档量级可能逼近日志量级 | **回退双表**（独立行数预算）| — |

> **一句话结论**：**最少 1 列，推荐 2 列**；9 列里 `row_type` / `doc_text` / `doc_preview` / `doc_chars` / `doc_status` 这 5 列都有现成替代，属于重复建设。
