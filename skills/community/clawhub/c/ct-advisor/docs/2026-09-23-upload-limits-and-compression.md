# 上传体积门、格式覆盖与传输压缩（2026-09-23）

> ## 🔴 读前必看 · 2026-09-23 修订：传输压缩方案**已下线**
>
> 本文 §4（正文压缩 `zip=zlib` + `text_b64`）及 §6/§7 中与之相关的条目**已作废**：
> 实测收益不足以承担两端复杂度，而且它**压不进 5 MB 体积门**，所以
> 本地 `doc_memory.build_doc_payload()` 不再产出该字段、Coze 端也不再解压；
> 老本地若仍发送该形态，Coze 端会**显式提示「请升级技能」**，不会静默当成无文档。
>
> **§4.1 / §4.2 的流量实测数据依然有效**——它们正是「决定不做压缩」的依据，请照旧阅读。
>
> 老格式（`.doc` / `.xls` / `.ppt`）的处理已另立专文：
> **`adapters/coze/docs/legacy-office-decoding.md`**。结论是「本地只搬运、Coze 端纯标准库解码」，
> **不再**要求用户安装 antiword / word-reader。

> 触发：用户三问 —— ① 超 5 MB 是否拒收；② 能否先 ZIP 压缩以减少流量；③ Word/Excel/PPT 是否都已能在客户端正常解码。
> 结论先行：① 已实现硬门；② **ZIP 原始文件无效**，有效杠杆是压缩「提取正文」与 `doc_id` 引用；③ Word/PPT 本就支持，**Excel 原先缺失，本次已补齐**。

---

## 1. 结论速览

| 问题 | 结论 | 依据 |
|---|---|---|
| ① 超 5 MB 拒收 | **已实现**（`check_upload`，硬门，`UploadRejected` 继承 `ValueError`） | §2 |
| ② 先 ZIP 减流量 | **无效**（实测仅省 0.9%~24.5% 且不稳定）；应改为压缩正文 / 传 `doc_id` | §4 |
| ③ 三种格式可解码 | `.docx` ✅、`.pptx` ✅、**`.xlsx` 原先缺 → 本次补齐** ✅ | §3 |

---

## 2. 5 MB 体积门

**落点**：`scripts/office_to_md.py::check_upload()` —— 本地 Office 上传的**唯一门禁**，任何调用 `office_to_md()` 的路径都会先经过它。

**行为**：

| 情形 | 结果 |
|---|---|
| 恰好 5 MB | 放行（`>` 而非 `>=` 判定） |
| 5 MB + 1 字节 | 拒绝 |
| `> 5 MB` | 拒绝，消息含体积、上限与 4 条可执行修正建议 |
| `.doc` / `.xls` / `.ppt` | 拒绝，指引「另存为」新格式 |
| `.pdf` | 拒绝，指引调用 pdf 技能（扫描件需 OCR） |
| `.zip` | 拒绝，说明对 OOXML 再压缩收益极低 |
| 其他扩展名 | 拒绝，列出支持的格式 |
| 文件不存在 / 不可读 | 拒绝 |

**兼容性**：`UploadRejected` 继承 `ValueError`，既有 `except ValueError` 调用方无需改动。

**为何在「客户端」设门而不是下游补**：超大正文会挤爆提示词预算（表现为答案截断 / 为空），且解析与传输成本随体积线性上升——在上传点拦截比在下游补救更省。

> ⚠️ 该门是**在技能内**执行的第一道闸；用户对话层（WorkBuddy 附件）可能有各自的限制，二者互不冲突。

---

## 3. 格式覆盖（客户端解码能力）

| 格式 | 改造前 | 改造后 | 实现 |
|---|---|---|---|
| `.docx` | ✅ | ✅ | `docx_to_md`：段落 + 表格按文档序交错 |
| `.pptx` | ✅ | ✅ | `pptx_to_md`：`### Slide N` 分节 + 表格 |
| **`.xlsx`** | **❌ 缺失** | **✅ 新增** | `xlsx_to_md`：每表一节 `## Sheet N: 名称` + md 表格 |
| `.doc` / `.xls` / `.ppt` | ⛔ 抛错 | ⛔ 抛错（改为**可执行**的「另存为」指引） | — |
| `.pdf` | ⛔ 抛错 | ⛔ 抛错（指引 pdf 技能） | — |

### 3.1 `xlsx_to_md` 实现要点（stdlib-only）

- **共享字符串**（`xl/sharedStrings.xml`）：聚合 `si/t` 与富文本 `si/r/t`，并**跳过 `rPh`（拼音注音）**——否则中文表格会混入注音文本。
- **表名与顺序**：读 `xl/workbook.xml` + `xl/_rels/workbook.xml.rels` 还原真实表名与声明顺序；失败则按 `sheetN.xml` 数字序兜底。
- **稀疏列还原**：按单元格 `ref`（如 `C5`）的列字母还原 0 基列号，**避免中间空列导致整行左移串位**。
- **单元格类型**：`s`（共享串索引）/ `inlineStr`（内联串）/ `str`（公式缓存串）/ `b`（布尔→TRUE/FALSE）/ 数值（原样保留）。
- **全空行跳过**；首行为空则不用它当表头。
- **截断护栏**：单表最多 300 行 / 30 列，超出即截断并在表后**显式标注**（防止超大表格吃光提示词预算）。
- **已知限制**：数值型日期**不做序列→日期换算**（原样保留数字），以免猜测格式导致错误；需要日期语义时请用户在提问中说明。

---

## 4. 传输压缩（回答「先 ZIP 再上传」）

### 4.1 为什么 ZIP 原始文件无效

`.docx / .xlsx / .pptx` **本身就是 ZIP + deflate 容器**。对已压缩容器再套一层 ZIP，收益来自「容器内本就未压缩的部分」，因此**不稳定**。真实文件实测：

| 文件 | 原始 | 再 ZIP(-6) | 再 ZIP(-9) | 收益 |
|---|---|---|---|---|
| CTDB_advisorlog (5).xlsx | 139.6 KB | 137.6 KB | 137.6 KB | 1.4% |
| CTDB_searchlog (2).xlsx | 10.0 KB | 7.7 KB | 7.7 KB | 22.7% |
| 工作簿1.xlsx | 9.6 KB | 7.2 KB | 7.2 KB | 24.5% |
| JJ销量统计（7月）-0801_processed.xlsx | 4999.0 KB | 4402.4 KB | 4402.4 KB | 11.9% |
| SanDisk_PtP_Topline_v1.1.docx | 45.8 KB | 43.6 KB | 43.6 KB | 4.8% |
| 课程委托创作协议（共有）-模板 (1).docx | 32.5 KB | 28.8 KB | 28.8 KB | 11.4% |
| Buddy案例.pptx | 5450.2 KB | 5400.2 KB | 5400.1 KB | **0.9%** |

**关键反证**：5.45 MB 的 pptx 压完仍是 5.40 MB —— **照样超出 5 MB 门**。因此「压缩包直传」不能作为超限的解法，规范上一律要求解压后上传原件。

### 4.2 有效的三个杠杆（按收益排序）

**① `doc_id` 引用（收益最高，已实现）** —— 同一文档的追问不再重传正文：

| 文件 | 每轮节省 |
|---|---|
| CTDB_advisorlog (5).xlsx | 100.0%（315,143 → 57 字符） |
| JJ销量统计.xlsx | 99.7% |
| SanDisk_PtP_Topline_v1.1.docx | 99.4% |
| CTDB_searchlog (2).xlsx | 99.3% |
| 课程委托协议.docx | 98.5% |
| 工作簿1.xlsx | 85.8% |

**② 压缩「提取后的正文」（本次新增，可选）** —— 跨端流动的是正文文本，deflate 效果显著：

| 文件 | 正文字符 | 明文 JSON | zlib | zlib+base64 | 净省 |
|---|---|---|---|---|---|
| JJ销量统计（7月）.xlsx | 20,674 | 31.7 KB | 2.9 KB | 3.9 KB | **87.7%** |
| CTDB_searchlog (2).xlsx | 7,271 | 7.8 KB | 1.0 KB | 1.3 KB | **83.0%** |
| CTDB_advisorlog (5).xlsx | 307,286 | 402.9 KB | 140.9 KB | 187.8 KB | **53.4%** |
| SanDisk_PtP_Topline.docx | 9,452 | 19.1 KB | 8.0 KB | 10.6 KB | 44.2% |
| 课程委托协议.docx | 3,510 | 9.5 KB | 4.1 KB | 5.5 KB | 41.5% |
| 工作簿1.xlsx | 365 | 0.5 KB | 0.3 KB | 0.4 KB | 21.9% |

> 注：base64 会吃掉约 33% 收益（二进制 → ASCII），故表中「净省」已扣除该开销。正文极短时（如 365 字符）开销占比高，收益自然低。

**③ 本地分块、只外发相关片段（已实现）** —— 超过 12 万字符的文档退化为本地粗选 top-30 块。

### 4.3 如何开启正文压缩（🔴 已作废 · 2026-09-23 整体下线）

**默认关闭**（老 Coze 镜像不认 `zip` 字段时，压过的载荷会被当作「无正文」→ 有降级风险）。

| 开启方式 | 用法 |
|---|---|
| 环境变量 | `CT_ADVISOR_DOC_ZIP=1` |
| 函数入参 | `doc_memory.build_doc_payload(text, compress=True)` |

载荷形态（契约真源：`adapters/coze/src/doc/payload.py`）：

```json
{"v":1, "doc_id":"doc_…", "instruction":"…", "mode":"full",
 "zip":"zlib", "text_b64":"…", "total_chars":12345, "source":"local_doc_memory"}
```

Coze 侧 `payload.py::_from_mapping` **透明解压**；解压失败则安全降级为「无正文」，**不抛错、不阻断**。压缩失败（zlib 异常）自动回退明文 `text`。

**启用建议顺序**：先部署携带该解码逻辑的 Coze 包，再在本地开启 `CT_ADVISOR_DOC_ZIP=1`。

---

## 5. 测试

`scripts/test_office_ingest.py` —— **38 项全部通过**（纯离线）：

- 体积门：边界（恰好 5 MB 放行 / +1 字节拒绝）、拒绝消息可执行、`ValueError` 兼容、6 类拒绝路径、真实 5.3 MB 文件。
- 格式覆盖：内存构造最小 docx/xlsx/pptx 夹具（含富文本共享串、rPh 跳过、稀疏列、内联串、布尔）+ 真实 xlsx 回归。
- 压缩往返：本地压缩 → Coze 解压正文一致、`doc_id` 一致、坏载荷安全降级、环境变量开关、zlib 交叉验证。

回归（无新增破坏）：`route.py --self-test` 29/29、`test_local_guards.py` ALL PASS、`test_local_doc_payload.py` 32/32、Coze `test_doc_pipeline.py` 60/60、`shared_sync_check.py` 全部一致 ✓。

---

## 6. 变更文件

| 文件 | 变更 |
|---|---|
| `scripts/office_to_md.py` | 新增 5 MB 门（`check_upload` / `UploadRejected`）、`xlsx_to_md`、老格式可执行指引；**同步至 ct-base 单一真源** |
| `scripts/doc_memory.py` | `build_doc_payload` 增 `compress` 参数 + `_attach_full_text`（zlib+base64） |
| `adapters/coze/src/doc/payload.py` | `_inflate_b64` + 透明解压（坏载荷安全降级） |
| `scripts/test_office_ingest.py` | 新增（38 项） |
| `SKILL.md` | 附件章节：5 MB 规则 + 格式覆盖表 + 测试入口 |
| `ct-base/scripts/office_to_md.py` | 单一真源同步（md5 与叶子一致） |
| `ct-base/docs/03-interaction-constraints.md` | §6.7.1 加入 5 MB 硬门、ZIP 无效性说明与减流量杠杆 |

---

## 7. 后续可选

- **日期语义**：如确需把 xlsx 数值型日期还原为日期串，可加 `numFmt` 解析（需读 `xl/styles.xml`），当前刻意不做以避免误判。
- ~~**压缩默认开启**~~：**已作废**（2026-09-23 压缩方案整体下线，开关与参数一并移除，不再翻转任何默认值）。
- **`.csv` / `.tsv`**：本次未纳入（用户仅问 Word/Excel/PPT）；如需可直接走同一解析族扩展。
