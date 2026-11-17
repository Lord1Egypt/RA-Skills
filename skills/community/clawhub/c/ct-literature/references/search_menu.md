# 检索细节确认菜单框架 / Search Confirmation Menu (ct-literature 定制版)

> **框架归属 / Framework**：本文件 = ct- 家族 **「检索型交互框架（Type-Search）」** 规范在 **ct-literature** 的落地（确认后才执行）。
> 本文件基于 ct- 家族共享的「检索型交互框架（Type-Search）」规范，按 ct-literature 参数清单定制；
> 与之并列的 **「计算型交互框架（Type-Compute）」** 见 `references/compute_menu.md`（meta-analysis / ct-samplesize）。
> 选哪套看 `references/interaction_frameworks.md`；跨轮连续性统一见 `references/continuity.md`。

> 本文件定义自然语言对话中，AI Agent 引导用户确认检索参数的通用交互流程。
> **covers every confirmation node from "user request" to "execute search"**——含参数确认、关键字体系确认门、预览确认与跨轮连续性。

---

## 1. 对话状态机 / Dialogue State Machine

```
       ┌──────────────────────────────┐
       │  Triage: BASE.md §6.2 三分类   │◄──────────────┐
       └──────────────────────────────┘               │
用户请求 ──►│                                          │（grill-me 理清后
   ├─ Simple  → 直接回复，不进入本框架（不弹菜单）      │  重新 Triage）
   ├─ Vague   → grill-me 逐分支追问 ───────────────────┘
   └─ Complex → [识别意图] → 收集参数 → [预览确认] → 执行检索 → 展示结果
                                 ↑________↓              ↑________↓
                                 (参数缺失时追问)         (用户可修改后重跑)

> **Citation-Expand 子意图（B.2）**：Complex 分支下，若用户以**某篇具体论文**（DOI / PMID / OpenAlex ID / 题名）为起点要求"追溯引用/被引/引文网络"，进入**种子驱动 snowball** 子意图——解析种子为 OpenAlex work ID，按方向（`references`=后向参考文献 / `cited_by`=前向被引 / `both`）扩展 1-hop 引文网络，并入语料。详见 §14。
```

> **前置门控（必读）**：本框架（状态机 + §4 菜单模板 + §12 关键字门）**仅适用于已 triage 为 Complex 的检索请求**。
> - **Simple**（具体、单一意图，topic + 参数基本齐，知识包/公开 API 可直接答）→ 直接回复，**不弹任何菜单**。
> - **Vague**（没说清要什么 / 用户自述不确定）→ 进入 **grill-me 逐分支追问**模式（每轮 1–3 个带默认的分支问题，硬上限 ≤2–3 轮，理清后给出「需求画像 + 推荐检索参数」摘要确认），**不甩菜单**，理清后再 triage。
> - 仅当请求被判定为 **Complex**（需选工作流 / 结论依赖多参数）→ 才进入下方的参数收集与确认菜单。
> - 任何 ct- 技能在调用本框架前，**必须先完成 §6.2 triage**；原子技能被独立调用时同样适用此门控。

## 2. 参数收集清单 / Parameter Checklist (ct-literature)

| 参数 | 必填 | 默认值 | 追问话术 |
|------|:----:|--------|----------|
| `--topic` | ✅ | — | "请告诉我检索主题（药物名 / 疾病 / 方法），例如：semaglutide、osimertinib、PD-1 inhibitor" |
| `--review-type` | ❌ | `all` | "需要限定文献类型吗？可选：系统综述 / Meta 分析 / RCT / 病例报告" |
| `--year-from` | ❌ | — | "需要限定起始年份吗？" |
| `--year-to` | ❌ | — | "需要限定截止年份吗？" |
| `--safety` | ❌ | off | "是否需要偏向安全性 / 不良事件文献（CSM 定性子集）？" |
| `--max` | ❌ | 50 | "每源最多检索多少篇？（默认 50）" |
| `--with-europepmc` | ❌ | **ON** | "是否关闭 Europe PMC（MeSH 精准，默认开启）？"（⚠ 默认开：`--no-with-europepmc` 关闭） |
| `--with-semantic-scholar` | ❌ | off | "是否开启 Semantic Scholar（引用排序增强，可能 429）？" |
| `--with-biorxiv` / `--with-medrxiv` | ❌ | **ON** | "是否关闭预印本（bioRxiv / medRxiv，默认开启）？"（⚠ 默认开：`--no-with-biorxiv` / `--no-with-medrxiv` 关闭） |
| `--with-arxiv` | ❌ | off | "是否纳入 arXiv 预印本？" |
| `--with-guidelines` | ❌ | off | "是否叠加临床指南本地语料库（12+ 源，零联网）？" |
| `--verify` | ❌ | all | "检索后做引用验证吗？（`all`/`top` 防幻觉，P0，耗时增加；默认开）" |
| `--depth` | ❌ | —（旧 `--max`） | "检索深度预算？quick=快速定位 / standard=标准（默认档位）/ deep=广覆盖。决定每源上限与是否弱化结果救援（非证据质量评级）" |
| `--concept` | ❌ | — | "结构化 PICO 概念（可重复）？如 `--concept intervention=osimertinib --concept comparator=chemotherapy --concept outcome=overall-survival`，干预/对照/结局分轴，做 MeSH 归一化审计" |

> 数据源：OpenAlex（主源，免 key）+ Europe PMC（默认开，含预印本 SRC:PPR）+ bioRxiv/medRxiv（默认开，预印本直连）+ Semantic Scholar（引用增强）+ arXiv（预印本，opt-in）+ 指南语料库（本地）。

## 3. 快速模式 / Quick Mode

当用户请求已包含 ≥2 个明确参数时，**跳过逐项追问**，直接进入预览确认。

**触发示例**：
- "检索 semaglutide 的系统综述，2020 年至今" → 直接进入预览
- "查一下 osimertinib 的安全性文献" → 直接进入预览
- "帮我查 PD-1 抑制剂的 RCT，近 5 年，要 Europe PMC" → 直接进入预览

## 4. 菜单选项模板 / Menu Templates

### 4.1 初始确认菜单（参数不足时）

```
📚 文献检索准备

当前已识别：
- 主题：{topic}
- 类型：{review_type}
- 年份：{year_range}

还需要确认：
1. 文献类型 — 全部 / 系统综述 / Meta分析 / RCT / 病例报告
2. 年份范围 — 全部 / 自定义
3. 安全性偏向 — 是 / 否
4. 数据源 — 主源(OpenAlex) / + Europe PMC(默认) / + Semantic Scholar / + 预印本 / + 指南语料库
5. 引用验证 — 不做 / 仅 Top / 全部

请回复编号选择，或直接说"默认"使用推荐配置。
```

### 4.2 预览确认菜单（参数齐全后）

```
📚 检索预览

| 参数 | 值 |
|------|-----|
| 主题 | {topic} |
| 类型 | {review_type} |
| 年份 | {year_range} |
| 安全性 | {safety} |
| 检索深度 | {depth} |
| 结构化概念 | {concepts} |
| 数据源 | {sources} |
| 每源上限 | {max} |
| 引用验证 | {verify} |

确认执行？
1. ✅ 直接执行
2. ✏️ 修改参数（回复编号）
3. ❌ 取消
4. 🔗 引导式检索剧本（读→扩→链，需 PDF 下载权限）
5. 🔍 以某篇论文为种子扩展引文网络（Citation-Expand，见 §14）
```

### 4.3 修改子菜单（用户选择修改时）

```
修改哪项？
1. 主题（当前：{topic}）
2. 类型（当前：{review_type}）
3. 年份（当前：{year_range}）
4. 安全性（当前：{safety}）
5. 数据源（当前：{sources}）
6. 每源上限（当前：{max}）
0. 返回上级

回复编号 + 新值，例如："2 meta-analysis"
```

### 4.4 选型犹豫时的「解释差异」入口（全库统一）

当用户在 Complex 路由菜单前/中对某个选型犹豫（如"系统综述 vs 快速证据扫描""加不加 Semantic Scholar""要不要做引用验证"），菜单应提供一个**独立选项**，触发「先讲清差异、再决策」，而非替用户拍板或直接甩全量菜单：

- 中文标注：`③ 还拿不准？→ 说「详细解释这些选择之间的差异」，我先讲清临床与统计含义再让你决定`
- 英文标注：`③ Can't decide? → say "explain the differences between these choices in detail", and I'll clarify the clinical/statistical meaning before you choose`

**适用**：所有 ct- 技能在 Complex 分支弹出的路由/选型菜单。与 `BASE.md §6.2` Complex 行「内置解释差异入口」要求一致。

## 5. 推荐配置策略 / Recommended Presets

| 场景 | 推荐配置 |
|------|----------|
| 快速了解某药证据格局 | `all` + 近 5 年 + OpenAlex + Europe PMC |
| 系统综述 / Meta 分析 | `systematic-review` + `meta-analysis` + 近 10 年 + 全源 |
| 安全性评估（CSM 定性） | `--safety` + `case-report` + 全部年份 |
| 竞品情报 | `all` + 近 3 年 + Semantic Scholar（引用排序） |
| 临床方案背景 | `rct` + `systematic-review` + 近 5 年 |
| 指南支持 | 默认参数 + `--with-guidelines`（本地语料库） |

## 6. 追问策略 / Follow-up Strategy

### 6.1 优先级

1. **topic 缺失** → 必须追问，无法继续
2. **year 缺失** → 推荐"近 5 年"，等用户确认
3. **review_type 缺失** → 默认 `all`，预览时提醒
4. **数据源缺失** → 默认"Europe PMC 开 + 其余按需"，预览时提醒

### 6.2 追问上限（有界追问）

- 连续追问不超过 **2 轮**（与 compute_menu §4「有界 grill-me」同源：LLM 自计数轮次，超限即收敛）
- 第 2 轮仍缺参数 → 使用默认值 + 预览提醒
- Vague 分支的 grill-me 同理：硬上限 2–3 轮，结束时给「需求画像 + 推荐检索参数」摘要确认

### 6.3 追问话术示例

```
# topic 缺失
"请告诉我检索主题（药物名 / 疾病 / 方法），例如：semaglutide、osimertinib、PD-1 inhibitor"

# year 缺失
"需要限定年份吗？比如'2020 年至今'、'近 5 年'，还是全部年份？"

# review_type 确认
"当前检索全部文献类型。需要限定吗？可选：系统综述 / Meta分析 / RCT / 病例报告"

# 数据源确认
"当前开启 OpenAlex + Europe PMC（默认）。需要加 Semantic Scholar（引用排序）/ 预印本 / 指南语料库吗？"
```

## 7. 输出确认 / Output Confirmation

检索完成后，展示结果摘要 + 后续选项，**并固定追加回显块**（见 §13）：

```
📚 检索完成！

- 主题：{topic}
- 检索到：{count} 篇唯一文献（{source_count} 个数据源）
- 开放获取：{oa_count} 篇（{oa_pct}%）
- 引用验证率：{verified}/{total}（若 --verify）
- 高被引 Top 3：
  1. {title_1}（{cited_1} 次）
  2. {title_2}（{cited_2} 次）
  3. {title_3}（{cited_3} 次）

## 当前检索设定：topic={topic} | type={review_type} | year={year_range} | safety={safety} | depth={depth} | concepts={concepts} | sources={sources} | max={max} | verify={verify}

后续操作：
1. 📄 查看完整报告（HTML / xlsx / bib）
2. 📥 下载 merged.json
3. 🔄 调整参数重新检索
4. 🔗 串联 ct-pipeline 生成情报简报（由 ct-pipeline 消费本技能 JSON 做聚合）
```

## 8. 异常处理 / Error Handling

| 异常 | 处理 |
|------|------|
| 无结果 | "未找到文献。建议：扩大主题词 / 放宽年份 / 切换 review-type" |
| Europe PMC 返回 0 | 静默跳过，不提示用户（已修复为 PUB_YEAR） |
| Semantic Scholar 429 | 静默跳过，结果中注明"未包含 S2" |
| 网络超时 | "网络连接超时。请检查网络后重试，或仅使用 OpenAlex 主源" |
| 主题词拼写异常 | "未找到结果。您是否想检索：{suggestion}？" |
| 引用验证失败（P0 防幻觉） | 结果标注 `unresolved/mismatch`，报告给出验证率，不静默丢弃 |

## 9. 多语言支持 / i18n

- 中文环境 → 中文菜单 + 中文报告
- 英文环境 → 英文菜单 + 英文报告
- 混合模式 → 菜单中文，报告双语（默认）
- 用户可见字符串经 `scripts/i18n.py`（en/zh 成对）按 locale 切换；**不硬编码裸字符串**。模板为结构参考，实际措辞走 i18n。

## 10. 对话示例 / Dialogue Examples（few-shot）

### 示例 1 · Simple：topic + 参数齐 → 直接预览确认（不逐项追问）

**You say:**
> 检索 osimertinib 的系统综述，2020 年至今

**Assistant replies (sketch):**
> 已识别：主题 osimertinib、类型 systematic-review、年份 2020-now（≥2 参数 → 快速模式）。
> 📚 检索预览：| 主题 osimertinib | 类型 systematic-review | 年份 2020-now | 安全性 off | 数据源 OpenAlex+Europe PMC | 每源 30 |
> 确认执行？（1 执行 / 2 修改 / 3 取消）——默认 SAFE PREVIEW，带 `--run` 才真正检索。

**📌 说明：** Simple / 快速模式直接进预览确认，不弹 4.1 初始菜单。

### 示例 2 · Complex：参数不足 → 初始确认菜单 + 预览 + 关键字门

**You say:**
> 帮我查一下 PD-1 抑制剂的安全性文献，但我不确定要不要加 Semantic Scholar，也不知道要不要做引用验证

**Assistant replies (sketch):**
> 已识别：主题 PD-1 inhibitor、安全性偏向开。还有 2 个关键选择，我来帮你理清：
>
> **① 要不要加 Semantic Scholar？**
> - (a) 不加 — OpenAlex + Europe PMC 已够，速度更快（推荐）
> - (b) 加 — 引用排序增强竞品情报，但可能 429 被跳过
>
> **② 要不要做引用验证？**
> - (a) 不做 — 快（默认）
> - (b) 做 `--verify top` — 防幻觉（§17.1 P0），耗时 +1–3 分钟
>
> **③ 还拿不准？** → 说「详细解释这些选择之间的差异」，我先讲清临床与统计含义再让你决定
>
> （确认后：参数预览 → **§12 关键字体系确认门**（PD-1 inhibitor 的中英扩展词）→ `--run` 检索）

**📌 说明：** Complex 分支弹能力路由菜单（(a)/(b) + rationale + ③ 解释差异入口），不替用户拍板；参数确认后强制过关键字门。

### 示例 3 · Vague：不确定要什么 → 有界 grill-me（不甩菜单）

**You say:**
> 我想查点文献，但不确定具体查什么方向，你能帮我梳理一下吗？

**Assistant replies (sketch):**
> 好的，我们先把需求理清楚。每轮问 1–3 个聚焦问题，每个带推荐默认（最多 2–3 轮）：
>
> **第 1 轮（2 题）：**
> 1. 你关注的是**药物 / 疾病 / 方法**哪一类？（如某药安全性、某适应症证据格局、某统计方法应用）
> 2. 用途是？— 临床方案背景 / 安全性核查 / 竞品情报 / 系统综述
>
> （回答后继续追问锁定主题与范围，结束时回显「需求画像 + 推荐检索参数」摘要确认，再进入预览。）

**📌 说明：** Vague 用 grill-me 逐分支理清（有界、带画像收尾），不甩全量菜单。

## 11. 与 AGENTS.md §6、BASE.md §6.2 的关系 / Relation

本文件在 ct- 交互规范体系中处于「**菜单模板实现层**」，承接两层上游约束：

- **AGENTS.md §6** 定义的是**图形界面 / 菜单导航**的 UX 基线（非互斥树）→ 本文件是其**自然语言对话**场景的具体实现。
- **BASE.md §6.2（Triage 三分类）** 定义的是**弹不弹菜单、怎么弹**的总规则（Simple 不弹 / Complex 弹 / Vague 用 grill-me）→ 本文件**仅适用于其中 Complex 分支**的参数确认菜单；Simple 与 Vague 不进入本框架（门控见 §1）。

> 简言之：**§6.2 决定"进不进菜单"，本文件 + AGENTS.md §6 决定"菜单怎么跑"**。

---

## 12. 关键字体系确认门 / Keyword-System Confirmation Gate

> 检索型技能的**核心确认门**：凡用户提供了可解析的检索词，构建关键字 Manifest（自动扩展 + 中英互译）后**强制弹确认门**，让用户过目技能替 TA 扩展的词。
> - 引擎：`scripts/kw_localize.py`（`expand_keyword` / `render_kw_system_menu` / `render_kw_system_menu_multi`）
> - 词库：`scripts/kw_lexicon.json` + `references/term_map.json`；双语框架标签：`scripts/i18n.py` 的 `kw_gate.*` 键
> - 完整 Manifest schema 与扩展维度见 `references/keyword_expand.md`

### 12.1 插入位置

对话状态机的「参数齐全后、执行检索前」之间：

```
用户请求 → [识别意图] → 构建 Manifest(扩展+互译) → 【关键字体系确认门】(强制)
         → 执行检索 → 展示结果
```

- **总是强制**：只要用户提供了可解析的检索词，就先构建 Manifest 并弹确认门（扩展词是技能替用户加的，必须让用户过目）。
- 例外：用户显式 `--no-expand` 或声明「不要扩展」时才跳过，直接进检索。

### 12.2 菜单模板（由 `render_kw_system_menu` 生成，i18n 双语）

```
🔍 关键字体系（自动扩展 + 中英互译）— 请确认 / 补充后再检索

原文：{base} ｜ 意图：{intent_label}
【中文候选】{zh 逗号分隔}
【英文候选】{en 逗号分隔}

【按源分配】
  · en_exact 源（英文·精确）：{per_source.en_exact.keywords}
  · zh_substring 源（中文·子串）：{per_source.zh_substring.keywords}
⚠ 风险提示：{risks 逐条}
📝 推测词（建议留意/可删）：{confidence.speculative 或 "无"}

请确认：
  1. ✅ 采用以上关键字体系（推荐）
  2. ✏️ 删除某些词（回复：删 <词>）
  3. ➕ 补充我自己的词（回复：加 <词>）
  4. 🔄 改用更窄 / 更宽范围
  0. ❌ 取消

（确认后才进入检索 → 正式检索）
```

- 框架标签经 i18n `kw_gate.*` 按 OS 语言切换；**候选词（药名、中文类别后缀、用户所输词）永远不翻译**（数据保真原则）。
- 多轴（如 disease + intervention 同时检索）用 `render_kw_system_menu_multi`，每块复用单轴模板，末尾共用一个动作菜单。

### 12.3 与既有机制的关系

- 与 §4 参数确认菜单**并存**：§4 确认「检索参数」，本门确认「实际会搜哪些词」，二者不冲突。
- 沿用 `_confirm_foreign_gate` 的「STOP 等确认」内存标志模式；标志位不落盘、不跨轮。

---

## 13. 跨轮连续性（回显当前检索设定块）/ Cross-turn Continuity

> 多轮追问时，前轮已确认的参数（topic / year / review_type / sources / safety …）必须无损继承，不能只凭 LLM 记忆。
> 家族标准见 `references/continuity.md` 模式 A（Type-Search 自动继承）。

### 13.1 规则

1. **每次执行后回显「当前检索设定」块**：在 §7 输出确认里，固定追加一个紧凑设定块，例如
   `## 当前检索设定：topic=osimertinib | type=systematic-review | year=2020-now | safety=off | sources=openalex+europepmc | max=30 | verify=none`
2. **追问时只改变化字段**：用户说"只看近 5 年"或"换成 semaglutide"时，LLM **必须读取对话中最近一个设定块**，只覆盖变化字段（year / topic），其余原样继承，再进 §12 关键字门或执行。
3. **确定性兜底（可选）**：担心漏带时，用 `scripts/merge_spec.py` 合并（上一轮 spec JSON + 本轮 partial，经 stdin 传入），输出完整 merged spec；状态仅经对话线程传入，不落盘、不跨轮缓存。

### 13.2 与既有机制的关系

- 本节的设定块是**对话线程内状态**，模型可见、可引用、可校验；不替代 §4 参数确认菜单，也不落盘。
- 红线：不用本地正则猜"是不是追问"；无状态远端计算的连续性必须在本地解决。

---

## 14. Citation-Expand 种子驱动 snowball（B.2）

> 以**某篇具体论文**为起点扩展其引文网络，而非从主题检索结果里挑种子。适用于"这篇 pivotal 论文还被谁引用、它又引了谁"这类诉求。

### 14.1 触发识别
- 用户给出明确种子（DOI / PMID / OpenAlex `W...` ID / 题名）+ "追溯引用/被引/前后向文献/引文网络/citation expand/snowball"。
- 与"主题检索 + 自动 snowball"（默认关、关键词后附加步）区分：本意图**种子来自用户指定文献**，不依赖主题检索结果。

### 14.2 参数收集（精简版）
| 参数 | 必填 | 默认 | 说明 |
|------|:----:|------|------|
| 种子 `seed` | ✅ | — | DOI / PMID / OpenAlex ID / 题名（题名模糊匹配取 top-1，置信度低时提示用户确认） |
| 方向 `direction` | ❌ | `both` | `references`=后向参考文献 / `cited_by`=前向被引 / `both` |
| 每方向上限 `max` | ❌ | 10 | 单方向扩展文献数上限（≤50） |

### 14.3 执行映射（CLI）
```
python scripts/ct_literature.py --snowball-seed "<DOI/PMID/题名>" \
    [--snowball-direction references|cited_by|both] [--snowball-max 10] --run --out-dir ./out
```
- 解析器 `fetch_openalex.resolve_seed_to_oa_id`：OpenAlex ID → 直出；DOI → `/works/doi:`；PMID → `/works/pmid:`；题名 → `/works?search=` 取 top-1。
- 解析失败：如实回报"无法解析为 OpenAlex work ID"，不编造文献。
- 种子文献经与主题检索相同的去重 / 引用验证（反幻觉）/ 报告流程；种子驱动文献在报告中带 `snowball_seed` / `snowball_direction` 溯源标记。

### 14.4 轻量可视化（可选）
复用 PRISMA 的 inline-SVG 能力：种子居中，前向/后向分两环，节点标注 `cited_by_count` 与相关性，生成轻量引文关系图嵌入 `lit_report.html`。

---

## 15. 引导式检索剧本（读→扩→链，C 项）

> 把现有零件串成"先读全文 → 再扩摘要 → 沿引用链扩展"的分段节奏，对应文章演示的 workflow。

### 15.1 三段节奏
1. **读**：`--download-pdf --anchor` 拉开放全文、落段落级溯源（需机构/本地 PDF 访问权限）。
2. **扩**：`--depth standard/deep` 扩摘要；必要时 `--snowball` 补网络。
3. **链**：以高相关种子走 §14 Citation-Expand。

### 15.2 开关
- CLI：`--guided` 一次性开启 `--download-pdf --anchor` 与标准深度（`--depth standard`），并打印剧本提示。
- 预览确认菜单见 §4.2 选项 ④。默认关，避免打扰简单查询。
