# Language Policy / 双语语言策略

> This file is the detailed companion to the "Language" section in SKILL.md. Applicability: this policy applies to **ct- skills that are statistical-analysis related AND intended for GitHub publication** (e.g. ct-samplesize). The ct-base scaffold itself ships the bilingual setup for library consistency; ct- skills that are NOT published / for internal use only default to Chinese-only and need no bilingual content. / 本文件是 `SKILL.md` 中「Language / 语言」段的详版补充。适用范围：本策略适用于 **ct- 系列中统计分析相关、且准备发布到 GitHub 的技能**（如 ct-samplesize）。ct-base 作为库底座采用双语脚手架以保持一致；不发布、仅自用的 ct- 技能默认纯中文，无需双语。
>
> **Web 工作台（本地浏览器 UI）场景落地细则**：凡技能附带本地 Web 操作界面（如 ct-samplesize `workbench/`），界面文本双语化的完整方案见 `ct-base/references/workbench_ui.md` —— 静态 chrome 走 `data-i18n`+`localize()`、schema 反射的动态表单走「按请求 lang 生成 + 前端按 LANG 取 + `setLang` 重建」三段链路、JS 动态文案走 `T.*` 键、计数/单位后缀特例双语同显。本文件仍为总策略权威，二者不冲突。

## Three core rules / 三条核心规则

1. **English by default / 默认英文**: All user-facing prompt content (reports, explanations, menus, warning boxes) defaults to English. / 所有面向用户的提示内容（报告、解释、菜单、警告框）默认使用英文。
2. **Auto-switch on Chinese-OS / 中文环境自动切换**: When the OS is detected as Chinese (locale contains `zh`/`CN`), prompt content auto-switches to Chinese **without explicit user request**. / 检测到操作系统为中文环境（locale 含 `zh`/`CN`）时，给用户的提示内容**自动切换为中文**，**无需用户显式要求**。
3. **Code output unaffected / 代码输出不受影响**: R / Python code itself is always English, shown per `--show-code`; not affected by the language policy. / R / Python 代码本身始终为英文，按 `--show-code` 规则展示，不受上述语言策略影响。
4. **Separator convention / 分隔符规范**: In any bilingual skill doc, join the EN and ZH text on the same line with ` / ` (slash, spaces on both sides). Never use `|` — it is the Markdown table column delimiter and breaks layout if the content is later moved into a table cell. / 双语文档中，中英文一律用 ` / `（斜杠，两侧空格）连同一行；不要用 `|`——它是 Markdown 表格列分隔符，内容移入表格会崩排版。
5. **Remote compute = explicit-locale bilingual template, figures always English / 远程计算端：显式 locale 直出双语模板，图形一律英文（2026-08-20 定稿·混合方案）**: Skills that call a remote compute service (e.g. coze R engine) follow the **hybrid model** — the engine emits a **bilingual template** selected by an **explicit `locale` parameter** (`zh`/`en`), so numbers and standard labels come straight from the built-in dictionary, **never through a generative model** (numeric fidelity & terminology consistency are hard guarantees for statistical tools). Rules:
   - **Explicit locale only**: the request / workflow input / engine input may carry `locale` (`zh`/`en`) when the engine ships a complete bilingual dictionary; absent the parameter the engine defaults to **English (language-neutral)** — never detect the server OS locale (server env ≠ user env, non-deterministic). The **local** caller decides the locale from the user's OS or prompt.
   - **Numeric fidelity**: `stats` JSON values must be quoted verbatim by the local presentation layer — never rewritten / rounded / re-translated by the LLM.
   - **Figures are special-cased（图形特殊规则，凡调用 coze 端一律适用）**: the SVG returned by the remote engine is **always English**, regardless of `locale` — server headless environments have no CJK fonts, and a server-rendered bitmap containing Chinese would be tofu. R engine figure labels are hard-coded English. **If user-supplied text (e.g. a Chinese project name) appears in the SVG, the local LLM MUST fix the font for CJK runs before rendering**: detect CJK characters in the SVG text nodes and extend their `font-family` with a CJK font family (e.g. `"Microsoft YaHei"` / `"PingFang SC"` / `"Noto Sans CJK SC"`) so Chinese renders correctly client-side.
   - **Caption vs SVG content（2026-08-28 细化：图形名称可双语，SVG 矢量内容一律英文）**: `figures[].caption`（图名字段，供 HTML 报告/卡片展示的标题）**follows `locale` and is bilingual**（zh→中文 / en→英文）via the engine dictionary keys (`fig.*`); but the **SVG vector content itself** (in-SVG `main` title, axis labels) **stays English** — server has no CJK font, tofu otherwise; the local HTML layer renders captions with a CJK font. Concretely: captions come from `sprintf(t("fig.curve"), test)` (bilingual), SVG `main=` is hard-coded English. This refines (does not contradict) the "figures always English" rule: the JSON caption metadata is bilingual; the rendered vector is English.
   - Skills without a bilingual dictionary default to English-only output; the local presentation layer translates as usual (rules 1–2). / 调用远程计算服务（如 coze R 引擎）的技能遵循**混合模型**：引擎按**显式 `locale` 参数**（`zh`/`en`）输出**双语模板**——数值与标准标签经内置字典直出，**绝不经过生成式模型**（统计工具必须保证数值保真与术语一致）。规则：
   - **仅显式 locale**：当引擎自带完整双语字典时，请求/工作流入参/引擎入参可携带 `locale`（`zh`/`en`）；缺省该参数时引擎默认**英文（语言中立）**——**绝不**按服务器 OS 判 locale（服务器环境 ≠ 用户环境，跨部署不确定）。由**本地**调用方按用户 OS 或提示词决定 locale。
   - **数值保真**：本地呈现层对 `stats` JSON 数值**逐字引用**——LLM 不得改写/四舍五入/转述。
   - **图形特殊规则（凡调用 coze 端一律适用）**：远程引擎返回的 SVG **一律英文**，不随 `locale` 变化——服务器 headless 环境无 CJK 字体，服务器端位图含中文必出豆腐块；R 端图形标签硬编码英文。**若 SVG 出现用户输入的中文（如项目名），本地大模型渲染前必须处理中文字体**：检测 SVG 文本节点中的 CJK 字符，为其 `font-family` 追加 CJK 字体族（如 `"Microsoft YaHei"` / `"PingFang SC"` / `"Noto Sans CJK SC"`），保证客户端中文正常显示。
   - **caption 与 SVG 内容区分（2026-08-28 细化：图形名称可双语，SVG 矢量内容一律英文）**：`figures[].caption`（图名字段，供 HTML 报告/卡片展示的标题）**随 locale 双语化**（zh→中文 / en→英文），经引擎字典 `fig.*` 键渲染（如 `sprintf(t("fig.curve"), test)`）；但 **SVG 矢量内容本身**（图内 `main` 标题、轴标签）**保持英文**——服务器无 CJK 字体，否则必豆腐块；中文由本地 HTML 层用中文字体渲染。本规则是对「图形一律英文」的**细化**（不矛盾）：JSON caption 元数据可双语，渲染出的矢量始终英文。
   - 无双语字典的技能默认纯英文输出，由本地呈现层按规则 1–2 照常转换。

## Chinese-OS detection method / 中文环境检测方法

| Platform 平台 | Detection method 检测方式 |
|:---|:---|
| Linux / macOS | Read `LANG` / `LC_ALL` / `LANGUAGE`; check if the language code starts with `zh` (e.g. `zh_CN.UTF-8`) / 读取 `LANG` / `LC_ALL` / `LANGUAGE` 环境变量，判断语言代码是否以 `zh` 开头（如 `zh_CN.UTF-8`） |
| Windows | Use `Get-Culture` / `Get-WinSystemLocale` PowerShell cmdlets, or read `os` env to check if the language code starts with `zh` (e.g. `zh-CN`) / 用 `Get-Culture` / `Get-WinSystemLocale` PowerShell cmdlet，或读取 `os` 环境变量判断语言代码是否以 `zh` 开头（如 `zh-CN`） |

If judged "Chinese environment", generate prompts in Chinese automatically; otherwise use English. / 判定为「中文环境」即自动用中文生成提示内容；否则用英文。


## Content-level language detection (user input text) / 内容级语言检测（用户输入文本）

> **区分两类"语言判定"**：① **系统语言**（`is_chinese_os()` / `_current_lang()`，读 `LANG` / Windows 区域设置）—— 决定**本地运行期 UI 提示**语言，遵循上文"默认英文、中文环境自动切中文"；② **用户输入文本语言**（`detect_text_language()`，扫 CJK 字符）—— 决定**coze 计算端报告/图表**应使用的语言。两者解耦，不可混用。

`detect_text_language(text)` 按**输入文本内容**判定（含中文→`zh`，纯英文→`en`，空文本→`None` 回退系统 locale），解决"中文系统 + 英文输入"被系统 locale 误判 `zh` 的盲区（如中文系统下用户 query 写 "BCG vaccine meta analysis"，应判 `en`）。扫描范围：基本汉字 + 扩展 A + 兼容汉字 + CJK 标点 + 全角字符。中英混排按中文占比判定（中文占比 ≥5% 或中文字符 ≥2 → `zh`；否则 `en`）。

## `user_language` backup param for coze compute endpoints / coze 计算端 `user_language` 备用入参

凡 ct-* 技能**调用 coze 计算端点**（R 引擎等），应在请求 `params` 中注入 `user_language`（`zh` / `en`）作为**备用提示**，供 coze 端决定报告/图表文案语言。判定优先级由 `i18n.resolve_user_language(query, override)` 统一实现（三级）：

> **注**：`user_language` 的字段位置、与 `skill_version` 顶层信封的关系、以及整体 coze 入参 / 飞书日志契约，集中在 **`ct-base/references/coze_io_contract.md`**（§1.1 入参 / §2 飞书存储），本文件仅描述语言判定逻辑。

1. **显式 `override`（如 `--language en`）最高** —— 多写法归一化（中文语境→`zh`、英文→`en`、未知值原样小写透传）；
2. **否则按【输入 query 文本内容】判定**（内容级检测，见上）—— 中文系统 + 英文输入 → `en`，不被系统 locale 误判 `zh`；
3. **query 为空时回退系统 locale**（`_current_lang()`）。

要点：
- **`user_language` 是备用输入** —— coze 端有自身判定时可忽略，不强制覆盖。
- **与 rule 5 `locale` 的区别**：rule 5 的 `locale` 是引擎**输出开关**（携带时引擎按内置双语字典直出对应语言模板）；`user_language` 是**调用方提供的提示**（caller → coze），二者可并存 —— `user_language` 不替代 `locale` 的显式输出语义。若端点同时支持两者，优先用 `locale` 做确定性输出切换，`user_language` 作退化兜底。
- **不影响本地 UI 提示**：`user_language` 只进 coze 请求参数，本地运行期提示仍按上文"Chinese-OS detection"走 `i18n._current_lang()`。


## Doc language convention (for maintainers) / 文档语言约定（面向维护者）

- `README.md`: English only, with a top switch link to `README_zh-CN.md`. / 纯英文，顶部保留指向 `README_zh-CN.md` 的切换链接。
- `README_zh-CN.md`: Chinese only, with a top switch link to `README.md`. / 纯中文，顶部保留指向 `README.md` 的切换链接。
- `SKILL.md` / `AGENTS.md` / `references/*.md`: English-only and agent-facing; bilingual human-readable content lives in the two READMEs. / 仅英文、面向 Agent；双语可读内容统一放在两份 README 中。
- Runtime prompts (from `scripts/i18n.py`) switch to Chinese on a `zh-*` locale and English otherwise. / 运行期提示（`scripts/i18n.py`）在 `zh-*` 环境下自动切中文，否则英文。

## i18n module consumers / i18n 模块的消费者

`scripts/i18n.py` exposes the lookup API (`t()` / `set_lang()` / `is_chinese_os()`); the bilingual strings themselves live in **`scripts/i18n_messages.json`** (EN/ZH key-value pairs), which is the **single source of truth** for all user-facing strings in the ct- library. Beyond runtime prompts, it is also consumed by **Excel report export**:

- **ct-registry `export_xlsx.py`** injects `../ct-base/scripts` onto `sys.path` and calls `from i18n import t, set_lang`, then renders all UI-frame labels (sheet names, banners, KPIs, block titles, column headers, chart titles) via `xlsx.*` keys. The report is switched with `--lang {auto,zh,en}` (default `auto` = OS locale). / `export_xlsx.py` 把 `../ct-base/scripts` 注入 `sys.path` 后 `from i18n import t, set_lang`，所有界面框架标签（表单名、横幅、KPI、区块标题、列头、图表标题）均经 `xlsx.*` 键渲染；报告以 `--lang {auto,zh,en}` 切换（默认 auto=OS 语言）。

- **Data-fidelity rule (Excel) / 数据保真原则**：only UI-frame labels are translated; **raw data values are NEVER translated** — e.g. CDE Chinese recruitment status ("进行中") and Chinese conditions stay verbatim in the English report. New `xlsx.*` keys must therefore cover labels only. / 仅翻译界面框架标签，**原始数据值一律不翻译**（英文报告中 CDE 中文状态、中文适应症等原样保留）。新增 `xlsx.*` 键只需覆盖标签。

- When adding Excel labels, append them to the `xlsx.*` (or `xlsx.safety.*`) section of **`i18n_messages.json`** (EN+ZH pair), never hard-code Chinese/English inside the consumer script. / 新增 Excel 标签时，统一追加到 `i18n_messages.json` 的 `xlsx.*`（或 `xlsx.safety.*`）段（EN+ZH 双语），切勿在消费脚本内硬编码中/英文。

### R-software messages live in a separate optional file / R 软件相关消息单独存放（可选扩展）

R-related runtime strings (`install.*`, `header.r_code`, `header.install_cmd`,
`error.rscript_*`, `error.r_timeout`) are **not** part of `i18n_messages.json`. They live in
**`scripts/i18n_r_messages.json`**, which `i18n.py` loads only when the file is present
(merge; main-file keys win). Pure-Python skills (e.g. ct-literature) simply do not vendor
this file and are unaffected; only skills that actually invoke R carry it (alongside their
own `r_libs.py`, e.g. ct-samplesize keeps its own embedded copies). When a skill needs
R-install / Rscript messages, copy `ct-base/scripts/i18n_r_messages.json` into its
`scripts/` — **never re-add R keys to the main file**. / R 相关运行期消息（`install.*`、
`header.r_code`、`header.install_cmd`、`error.rscript_*`、`error.r_timeout`）**不放在**
`i18n_messages.json` 主文件，而是单独放在 **`scripts/i18n_r_messages.json`**；`i18n.py`
仅在文件存在时合并加载（主文件键优先）。纯 Python 技能（如 ct-literature）不 vendor 该
文件即不受影响；只有真正调用 R 的技能才连同自己的 `r_libs.py` 一起携带（如 ct-samplesize
自带内嵌副本）。技能需要 R 安装 / Rscript 消息时，复制 `ct-base/scripts/i18n_r_messages.json`
到技能 `scripts/` 即可——**切勿把 R 键加回主文件**。

## First-use / one-shot runtime prompts / 首次使用与一次性运行期提示（强制接 i18n）

**强制规则（在三条核心规则之上追加）**：所有「首次使用才出现 / 一次性触发」的用户提示——尤其是**出站授权确认**（如首次开放 Coze 云端精校）、运行期**依赖缺失**、**网络 / HTTP 错误**（如 401 鉴权拒绝）、**回退本地草稿**等——**必须**经 `t()` 从 `i18n_messages.json` 取词，**禁止**在消费脚本内硬编码中/英文、**禁止**中英双显（同一消息同时打 EN+ZH）、**禁止**中英混排（一句前半 EN 后半 ZH）、**禁止**依赖 agent 在运行期临场拼模板（一旦 agent 误判语言或换一个不严格照 SKILL.md 执行的 agent，提示可能只出单语或失真）。

- 底座已在 `i18n_messages.json` 预置通用 `auth.*` / `error.*` 标准词条：`auth.coze_outbound`（首次出站授权）、`auth.coze_outbound_denied`（拒绝说明）、`auth.serial_blocked`（串行拦截回退）、`error.requests_missing`（依赖缺失）、`error.coze_401`（鉴权拒绝）、`error.fallback_local`（回退本地）。子技能直接 `t("auth.coze_outbound", endpoint=...)` 引用，或按需扩展，**切勿自建重复词条**。
- 占位符约定：`{endpoint}` 出站地址、`{cmd}` 手动安装命令、`{reason}` 异常原因、`{timeout}` 超时秒数。
- 机器信号（如 `[AUTH-BLOCK]` / `[coze] AUTH_REJECTED`）与用户可读提示**分离**：信号写 stderr 供 agent / 开发者定位，用户提示走 `t()` 单语输出。

## Locale chain propagation & zh-leak checks / locale 链式传播与中文泄漏检查（2026-10-29 补充）

> 来源：meta-analysis 工作台 EN 模式实测——GRADE 页残留中文、过度声明页整页中文、
> `p value` 与数值粘连。逐条根因均为本节规则的缺失，特此补入规范。

1. **Chain propagation / locale 链式传播**：界面语言必须经**每一条后端调用边界**透传到底
   （server route → orchestrator（如 `run_fullflow` / `run_fastpath`）→ 各块驱动器 → 子模块）。
   禁止「只有部分块消费语言」——orchestrator 应把 locale 存入会话 cfg 并持久化，各块统一从
   cfg 取值（缺省 zh），而不是各自由请求参数断链。 / The UI locale must reach **every**
   backend stage boundary. Orchestrators store it in the session cfg (persisted); block drivers
   read it from cfg — never rely on per-request params that only some stages consume.

2. **Inherit, don't reset / 内层函数继承而非重置**：子模块函数的 `lang` 参数缺省值必须是
   `None`（= 继承当前上下文语言），**禁止**缺省 `"zh"` 并在函数体内无条件
   `_LANG.set(lang)`——那会在每次调用时把语言重置回中文（meta-analysis `interpret_result`
   的实际翻车点）。只有显式传入 lang 时才覆盖。 / Inner functions must default
   `lang=None` (inherit); an unconditional `_LANG.set("zh")` default silently resets the
   language on every call.

3. **Single language source / 单一语言上下文源**：同一进程内多个模块各自持有 `_LANG`
   ContextVar 时，**所有语言入口必须同步设置全部 ContextVar**（或抽取公共
   `set_lang()`）；只设一个就会出现「同一信封内部分中文部分英文」。 / When several
   modules each keep their own `_LANG` ContextVar, every language entry point must set
   **all** of them (or share one helper) — partial sync yields mixed-language envelopes.

4. **Whitespace-preserving DOM replace / 前端文本替换保留空白**：渲染后按文本节点整体
   替换的兜底层，必须用「在原串中替换裁剪键」（`node.nodeValue = t.replace(key, out)`），
   不得 `node.nodeValue = dict[key.trim()]` 直接覆盖——后者会吞掉标签尾随空格，与相邻
   内联值拼接（`p value0.0739` 粘连实例）。模板里内联 label/value span 之间必须写显式
   空白。 / Post-render text-node replacement must replace the trimmed key **within** the
   original node value (preserving surrounding whitespace); wholesale assignment swallows
   trailing spaces and glues the label to the adjacent inline value.

5. **Data vs copy / 数据与文案的判据（DOM 翻译层补充）**：命中片段、句子引文、正则模式、
   扫描预览等**来自用户输入/匹配器的字符串是数据**，即使含中文也保持逐字（与 Excel 数据
   保真原则同源）；DOM 翻译层用 skip 选择器豁免这些区域。只翻译**生成的叙述文案**。 /
   Matched fragments, quoted sentences, regex patterns and scan previews are **data** — keep
   them verbatim even when Chinese; only generated narrative copy is translated.

6. **Automated leak scan / 自动化泄漏扫描**：EN 模式回归必须包含一次机械扫描——遍历信封
   / 页面全部字符串，报告含 CJK 的键；数据字段（上条）列入豁免清单。人工目测不可靠
   （meta-analysis 此前多轮目测仍漏 `interpretation._LANG`）。 / EN-mode regression must
   include a mechanical CJK scan over all output strings with an explicit data-field
   exemption list.
