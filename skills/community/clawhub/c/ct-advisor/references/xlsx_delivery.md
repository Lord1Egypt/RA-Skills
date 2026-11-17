# Excel 结果文件交付规范 / XLSX Delivery Contract（ct- 全库共享）

> 单一真源：`ct-base/scripts/xlsx_delivery.py`（流程契约层）+ `ct-base/scripts/excel_style.py`（视觉层）
> 上位规范：`BASE.md §16.8` 共享件单一真源 / 发布包自包含；`references/excel_style.md` 视觉标准
> 适用范围：所有产出 `.xlsx` 交付物的 `ct-` 技能（当前 ct-registry / ct-literature / ct-safety / ct-pipeline / ct-tlf 等）
> 确立日期：2026-11-06（三技能横向事故归纳）

---

## A. 为什么要这份规范

2026-11-06 连续排查三个技能后发现**同一个缺陷在三条链路各自独立出现**：

| 技能 | 线上表现 | 直接成因 |
|---|---|---|
| ct-registry | `README / Search Results Summary / Trial Master Table / Raw Details` 全英文；超时兜底 xlsx 表头中英混排、列表值写成 `['United States', 'China']` | `--lang auto` → OS locale（云端 en_US）；兜底报告手写极简 OOXML 无样式 |
| ct-literature | Excel 四表全英文，且 `lit_report.html` / Markdown 同步全英文 | xlsx / html / md 三处各自按 OS locale 判 `auto`；前端 `#f_lang=auto` 时主 CLI 不传语言 |
| ct-safety | 同日两次任务一份英文一份中文 | 工作台 `defaultLang="en"`（全家族唯一异常值）+ `report_xlsx` 用 `sys.platform == "win32"` 判语言 |

**共性根因**：把「交付物语言」当成「运行期控制台提示语言」，交给宿主机 OS locale 决定；且三个技能各写了一份几乎相同的 `resolve_report_lang()`（仅环境变量名不同）。

**已有基础**：`excel_style.py` 早已把视觉层（调色板/字体/表头/斑马纹/KPI/图表/列宽）统一，本次事故全部发生在它**之外**的流程层。因此本规范补齐 L2，不重复 L1。

---

## B. 三层边界（核心结论：可归纳，但只能上移 L2）

| 层 | 内容 | 归属 | 能否上移 |
|---|---|---|---|
| **L1 视觉层** | 调色板 `PALETTES`、CJK 字体探测、表头 24px、斑马纹、KPI 卡、封面 banner / logo、图表自适应、列宽 CJK 感知、`join/safe/year_of` | `ct-base/scripts/excel_style.py` | ✅ 已完成（2026-07-30 起） |
| **L2 流程契约层** | 交付语言解析、sheet 契约声明、CLI `--lang` 契约、交付物机检、工作台语言注入约定、文件名/下载契约 | `ct-base/scripts/xlsx_delivery.py` + 本文档 | ✅ **本规范确立** |
| **L3 业务层** | 记录 schema（试验记录 / 文献 works / FAERS 个例）、分布维度与聚合、sheet 数量与编排、技能私有词条、超时兜底报告、主 CLI 业务参数 | 各技能 `scripts/export_xlsx.py` | ❌ **不上移**（差异是领域本质，强行抽象会产生上帝基类） |

**L3 的真实差异（不要抹平）**

| | ct-registry | ct-literature | ct-safety |
|---|---|---|---|
| 输入 | `recs` 归一化试验记录 list | `data` = `.merged.json`（works / evidence_log / verification） | `rows` FAERS 个例 + `dists` 预聚合 |
| sheet 数 | 4（说明/概要/总表/原始明细） | 5（说明/概览/文献总表/安全性相关/证据溯源） | 3（说明/概要/原始计数） |
| 分布维度 | 分期/状态/来源/适应症/国家/年份/申办方/样本量/交叉矩阵 | 年份/来源/类型/高被引 | 严重性/性别/年龄/国家/报告类型/PT |
| i18n 键空间 | `xlsx.*`（通用主表） | `_LOCAL` 私有字典 + `xlsx.*` | `xlsx.safety.*` + `xlsx.*` |
| 导出入口 | `export_workbook(recs, out, *, title, meta, lang)` | `export_workbook(data, out, lang, safety, decisions…)` | `export_workbook(rows, out, meta, lang, dists)` |
| CLI | `--in/--out/--title/--meta/--lang` | `--in-json/--out/--topic/--safety/--lang` | `--in-csv/--out/--drug/--total/--lang` |
| 兜底 | `_write_partial_xlsx()` 超时手写 OOXML | 无 | 无 |

> 结论：**统一"契约"，不统一"实现"**。用可组合的 helper + 声明式 `WorkbookSpec`，而不是基类继承 / 模板方法强制重构三份 700–1150 行且已稳定的脚本。

---

## C. 标准七步流程（所有技能必须遵守的顺序）

```
1 resolve_lang    resolve_report_lang(lang, skill=..., title=...) → 'zh' | 'en'
                  → 技能调用自己的 vendored i18n.set_lang()  ← 只此一次，贯穿全流程
2 coerce_input    归一化输入为技能 schema（L3）；原始数据值不做任何翻译
3 open_workbook   xlsxwriter.Workbook(out) + set_properties(title/author)
4 make_formats    excel_style.make_formats(wb, PALETTES["<skill>"])
5 build_sheets    封面(说明) → 概要/分布(带原生图表) → 明细总表 → 溯源/原始明细
                  每张表：freeze_panes(1,0) + autofilter + repeat_rows(0,0)
6 verify          xlsx_delivery.verify_workbook(out, expected_lang=lang)
7 close_return    wb.close() → 返回 sheet 数 → 交付 report.xlsx
```

`DELIVERY_CONTRACT` 字典是上述流程的机器可读版本，供回归用例断言。

**步骤 1 的优先级（🔴 硬红线，见 §D）**

```
显式 --lang zh|en
  > CT_<SKILL>_LANG  →  CT_LANG            （工作台注入当前界面语言）
  > 技能根 config.json 的 language         （持久用户选择）
  > 封面标题含 CJK → zh                   （对话式 CLI 的输入语言信号）
  > 默认 zh                               （中文用户优先）
```

**步骤 5 的最低结构要求**（与 `excel_style.md §3` 对齐）：表头首行、冻结首行、自动筛选、CJK 感知列宽、状态色、图表浮于右侧。任何"兜底/部分结果"报告同样适用——不得因为走的是降级路径就退化为无样式裸表。

---

## D. 交付语言红线（本次事故的归纳，全库强制）

1. 🔴 **交付物语言禁止回退到服务器 OS locale**。`is_chinese_os()` / `getdefaultlocale()` / `sys.platform == "win32"` 一律不得作为 `.xlsx` 语言判据；云端容器普遍为 `en_US`。
2. **`auto` 的语义是"按调用上下文解析"，不是"按操作系统解析"**。上下文 = 显式参数 > 工作台界面语言 > 持久配置 > 用户输入语言信号 > 默认中文。
3. **一次解析、全程复用**：主 CLI 在入口解析成具体 `zh|en` 后传给所有下游导出器（xlsx / html / md / 引用文件），禁止每个导出模块各自再判一次 `auto`（ct-literature 事故的直接形态）。
4. **工作台必须把当前 UI 语言下发到导出子进程**：前端 `lang` 字段 → 后端 `CT_<SKILL>_LANG` 环境变量或 `--lang`；界面切 EN 才出英文交付物。
5. **原始数据值绝不翻译**（试验标题、状态枚举、申办方、PT 术语、国别码）；本地化的只有界面 chrome。此条同时是 `excel_style.md §8` 的既有红线。
6. **i18n 键空间分层**：通用 `xlsx.*` 放 `scripts/i18n_messages.json`；技能专属用 `xlsx.<skill>.*` 或 `i18n_skill_messages.json` 覆盖；禁止把私有词条写回共享主表。
7. **键名不得泄漏进单元格**：`t()` 找不到键时回退键名，会把 `xlsx.field.xxx` 写进交付物。`verify_workbook()` 必须把这一项作为硬失败。
8. **中文词条不得留英文**：新增/修改词条须双语齐备；`zh` 值仍是 `Primary Outcome(s)` 这类英文属缺陷（ct-registry 已修一例）。
9. 🔴 **英文交付物不得残留中文界面文案**（阶段 2 新增）：`lang=en` / 工作台切 EN 时，sheet 名、表头行、封面标签、KPI 标签、字段字典、图例、注意事项、兜底报告表头必须**纯英文**。禁止 `"Run config / 运行配置"` 这类中英混排硬编码；封面若展示中英并列的检索主题，英文模式只保留英文片段。
   - **边界**：明细数据区里的中文（中文试验标题、CDE 中文状态、中文申办方、中文检索词作为数据值）属 **§8 数据保真红线**，保留原文，不算缺陷；`verify_workbook()` 只把表头行 / A 列短标签判为 chrome 硬失败，其余中文进 `cjk_cells` 报告供人工审阅。

---

## E. 文件 / CLI / 工作台契约

| 项 | 标准 |
|---|---|
| 交付文件名 | `report.xlsx`（技能可用 `<skill>_report.xlsx`，但须在 SKILL.md 与前端文案一致） |
| CLI 语言参数 | `--lang {auto,zh,en}`，用 `xlsx_delivery.add_lang_argument(parser)` 统一 help 文本 |
| 导出 API | `export_workbook(data, out_path, *, lang="auto", **skill_specific)`；`lang` 恒为关键字参数，返回 sheet 数 |
| 工作台下载 | `GET /api/download?task=<id>`（或 `/api/file?dir=&name=`），`Content-Type` 为 xlsx MIME，`Content-Disposition: attachment` |
| 工作台语言注入 | 前端表单带 `lang`（当前 `WB_LANG`）；后端子进程 env 写 `CT_<SKILL>_LANG`（默认 zh） |
| 工作台默认界面语言 | `workbench.config.json` 的 `i18n.defaultLang` 统一为 **zh**（ct-safety 曾是 `en`，已对齐） |
| 发布包自包含 | 共享件经 `publish_inject.py` 注入；发布包内不得出现 ct-base sibling fallback |

---

## F. 交付物机检清单（`verify_workbook()`）

| # | 检查项 | 失败级别 |
|---|---|---|
| F1 | 文件为合法 OOXML zip、`xl/workbook.xml` 可解析 | ERROR |
| F2 | sheet 数 ≥ 2、表名无非法字符且 ≤ 31 字符 | ERROR |
| F3 | 期望 zh 时至少一张表名为中文；期望 en 时无中文表名 | ERROR |
| F4 | 单元格/sharedStrings 无 `xlsx.*` 等键名残留 | ERROR |
| F5 | 至少一张表带冻结窗格或自动筛选 | ERROR |
| F6 | 显式 `--lang en` 仍可产出英文（双语能力不得被"默认中文"抹掉） | 回归用例 |
| F7 | 同一份数据在 zh / en 两种语言下记录数、图表数、sheet 数一致 | 回归用例 |
| F8 | 原始数据值在两种语言下逐格一致（只换 chrome） | 回归用例 |
| F9 | 期望 en 时界面 chrome（sheet 名 / 表头行 / A 列短标签）零中文；`cjk_cells` 只报告数据区 | ERROR |

`python scripts/xlsx_delivery.py --selfcheck` 跑内置语言解析回归；
`python scripts/xlsx_delivery.py --verify <file.xlsx> --expect-lang zh|en` 校验单个交付物
（返回 `cjk_cells` / `cjk_cell_count`，便于区分 chrome 缺陷与数据保真值）。

---

## G. 现状对照与迁移路线（不破坏现网的分阶段落地）

| 阶段 | 动作 | 风险 |
|---|---|---|
| **阶段 1（已完成）** | 底座新增 `scripts/xlsx_delivery.py` + 本文档；登记进 `publish_inject.py::SHARED_ASSETS`；`excel_style.md` / BASE 双视图索引互链 | 零：未改生产代码 |
| **阶段 2（✅ 2026-11-06 已完成）** | 三个技能删除本地 `resolve_report_lang()`，改为 `from xlsx_delivery import resolve_report_lang` 并传 `skill=`；`ct_literature.py` / `export_html.py` / `report.py` / `report_xlsx.py` 引用点同步；共享件物理注入 3 个主 `scripts/` + 3 个发布包 `scripts/`（逐文件一致）；修复英文模式中文残留（文献混排标签 / 封面中英并列主题 / 兜底报告硬编码中文表头） | 中：已完成全量回归，**线上三个应用仍待重新部署** |
| **阶段 3（✅ 2026-11-06 已完成）** | `xlsx_delivery.py` 纳入 `shared_sync_check.py::_PY_STRICT` + `_REF_KW`（消费者契约：引用未携带 / 携带漂移均判 ERROR，未引用技能零噪声）；补 `ctqa` W1_CLI 套件 `xlsx_delivery_cases.py` 断言 F1–F9（四技能实跑 9/9 PASS）；`ct-pipeline` 接入共享件（删本地 `_LANG="en"` 恒英文回退，改 import；框架 chrome 全面双语化，英文版 CJK 数据单元格全为原始简报值、机检 `ok=true`）；`ct-sdtm` 仅注入资产并登记技术规格类边界 | 低 |

> ⚠️ 阶段 2 已验收的行为差异：统一版**不读 OS locale**，纯英文标题 + 英文 OS 的旧行为是 `en`，新行为是 `zh`；英文用户须显式 `--lang en` 或工作台切 EN（后端注入 `CT_<SKILL>_LANG=en`）。这是刻意选择——中文用户优先，且工作台已显式下发界面语言。
>
> ⚠️ ct-base 永不发布：阶段 2 已把 `xlsx_delivery.py` 实际复制进每个技能的主目录与发布包；后续新增产出 xlsx 的技能必须同样物理注入，否则线上 `ModuleNotFoundError`。
>
> ✅ 阶段 2 验收：4 个导出器（registry / literature / safety / pipeline）× 2 语言，英文版**界面 chrome（sheet 名 / 表头 / A 列短标签）零中文**；中文版 sheet 名与表头全中文；`--lang en` 与 `CT_<SKILL>_LANG=en` 均产出英文；英文表头注入中文的反例被 `verify_workbook()` 准确判失败；发布包脚本独立运行自包含。
>
> ✅ 阶段 3 验收（2026-11-06）：闸门 `_PY_STRICT` / `_REF_KW` 对「引用未携带」「携带漂移」判 ERROR、未引用技能零噪声；`ctqa` W1_CLI 的 `xlsx_delivery_cases.py` 九项 F1–F9 在四技能实跑 **9/9 PASS**；`ct-pipeline` 删除本地恒英文回退、接入共享件，框架 chrome 全面双语化，英文版 21 个 CJK 单元格**全部是简报原始数据值**（机检 `ok=true`）。
>
> ⚠️ **数据保真红线（用户 2026-11-06 明确）**：英文模式下，**检索到的原始中文数据值保持原状，不得为追求"零中文"而刻意翻译成英文**。中英文切换只作用于**界面 chrome**（sheet 名、表头、字段标签、KPI / 图例、说明文字、图表标题、封面元信息）；明细数据区（中文试验名、CDE 中文状态、中文申办方、FAERS 原始字段、生成叙述中的原始中文引用）一律保留原文。`verify_workbook()` 的 F9 仅约束 chrome，数据区中文只进 `cjk_cells` 报告、不阻断——这正是该红线的机检体现。

---

## H. 接线清单（改本规范时必须同步）

- `scripts/publish_inject.py` → `SHARED_ASSETS` 登记 `scripts/xlsx_delivery.py` 与 `references/xlsx_delivery.md`
- `scripts/shared_sync_check.py` → 阶段 3 前**仅注入表登记，不入 `_PY_STRICT`**（口径同 `wb_detail_check.py` / `doc_comments.py`，避免对未引用该件的 16 个技能产生无谓 WARN）；阶段 2 已由 `publish_inject` 的登记 + 6 处物理注入保证自包含
- `references/excel_style.md §9` → 互链到本文档
- `BASE.md` 与 `docs/00-index.md` → 双视图索引逐字同步（F31 闸门为逐字比较）
- `CHANGELOG.md` → 按 §9 版本纪律登记
