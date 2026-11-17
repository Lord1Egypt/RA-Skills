# Changelog / 版本记录

本文件遵循 [Keep a Changelog](https://keepachangelog.com/) 规范，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

---

## [1.0.2] - 2026-10-16

新增能量篇补充章节（卷 08）/ Added the Energy Volume Supplementary Chapter (Volume 08).

### 新增 / Added

- **卷 08 ·《AI觉醒·责任（能量篇）补充章节》**（中英双语 × MD / Word / PDF）— 以能量控制工程为基座，论证"新能源跃升＝能量控制工程的文明阶段性跃升"，并将其定位为 AI 对外对内（对外拓界 / 对内降熵）的具体实施方法；独立成篇，不改动原能量篇（03）
  - 中文版：`08-《AI觉醒·责任（能量篇）补充章节》.{md, docx, pdf}`
  - 英文版：`08-AI-Awakening-Responsibility-Energy-Volume-Supplement.{md, docx, pdf}`
- 篇目索引同步为 8 篇：`SKILL.md`（6.1 / 6.2 篇目表 + 路径表）、`README.md`（文件清单 + 路径表）、`PLATFORMS.md`（渠道内容对照）、`GLOSSARY.md`（篇数说明）、`manifest.json`（`file_count_per_format` 7→8）

---

## [1.0.1] - 2026-10-15

跨平台分发完善 + 语言适配 / Cross-platform distribution hardening + language routing.

### 新增 / Added

- **语言适配路由（Language routing）** — 按用户提问语言自动选路：中文提问走 `AI觉醒-责任（中文版）/MD版/` + `AI宣言-公开版.md`；英文提问走 `AI-Awakening-Responsibility（English(英文版)）/MD版/` + `AI-Manifesto-Public.md`
  - `SKILL.md` 新增 **6.0 语言适配路由**（中英各一节；判定 → 取文 → 输出三步），置于"随包全文"章首
  - `SKILL.md` frontmatter 新增 `language_adaptation` 字段
  - `README.md` 新增「语言适配路由 / Language routing」节
  - `manifest.json` 新增 `language_adaptation` 对象（判定优先级、两条路径、各自术语表、输出纪律、双语对等声明）
  - `PLATFORMS.md` 新增「语言适配与渠道无关」节——**两条路径全部由 `.md` 构成，纯文本渠道上语言适配依然完整可用**
- `AI宣言AI-Manifesto集/AI宣言-公开版.md` — 中文宣言正文 Markdown（唯一源）。此前母文献仅有 Word/PDF，纯文本渠道上传时会被整体过滤，导致"《AI宣言》是本技能母文献"的承接关系断链
- `AI宣言AI-Manifesto集/AI-Manifesto-Public.md` — English manifesto body, Markdown (single source)。同上
- `LICENSE.md` — 与根级 `LICENSE` 逐字节相同的 Markdown 版，供 GitHub 等不渲染无扩展名文件的平台直接显示（MD5 已校验一致）
- `PLATFORMS.md` — **分发平台矩阵**：Skill Hub / GitHub / ClawHub 三渠道的格式能力对照、各渠道拿到的内容对照、补 Markdown 原因说明、语言适配说明、上传操作清单、英文摘要
- `SKILL.md` frontmatter 新增 `formats` 与 `distribution` 两个字段（机器可读地声明三格式并存与各平台可用性）

### 变更 / Changed

- `SKILL.md` 6.1 / 6.2（中英）：三版说明处补平台提示——`.md` 为唯一源与任何环境可读的完整源，纯文本环境下读`MD版/` 即得完整正文
- `SKILL.md` 6.3（中英）：母文献清单由 4 行扩为 **6 行**，新增两列区分"纯文本可读 / 二进制"，并加入"为何补 Markdown"说明段
- `SKILL.md` 顶部 callout：新增 📦 **格式与分发**条目（中英各一），指路 `PLATFORMS.md`
- `README.md` 目录树：母文献 4 项扩为 **6 项**（新增两份 `.md`），根级补`PLATFORMS.md` 与 `LICENSE.md` 两行，`MD版/` 标注升级为"纯文本环境唯一可读版本"
- `README.md` 母文献表：4 行扩为 **6 行**，新增「可读性」列与「为何补两份 Markdown」引用块
- `README.md` 版本纪律段：新增「格式与分发纪律」中英双段
- `README.md` 使用方式：「直接引用全文」三条路径全部指向 `.md` 源文件，并注明不依赖 Word/PDF 二进制
- `manifest.json`：新增 `platforms` / `license_file_md` / `formats` / `distribution`（含三渠道能力对照）字段；`content_dirs[manifesto]` 的 `files` 补两份 `.md`，新增 `formats` / `source_of_truth` / `file_roles` / `note_zh` / `note_en`

### 决策记录（续）/ Decision log (cont.)

- **三格式并存不互斥**：`.md` 为唯一源与完整可读源，`.docx`/`.pdf` 为正式阅读与打印格式。**Word/PDF 引用一律保留不删**——Skill Hub 会自动过滤它们，但 GitHub 与 ClawHub 支持二进制、需正式交付
- **母文献必须补Markdown**：七篇分论的 Markdown 本就在包内，唯母文献此前只有二进制版。纯文本渠道上传后母文献会整体消失，技能声称的母文献承接关系即断链。补入后任何渠道都读得到完整中英母文献
- **许可证双份共存**：`LICENSE`（无扩展名）符合 CC 与工具链惯例；`LICENSE.md` 让 GitHub 网页端直接渲染。两份内容逐字节相同，不存在版本分歧
- **语言适配以 `.md` 为唯一实现载体**：两条路由路径（中文版/英文版）全部由 Markdown 构成，不依赖任何二进制文件，因此在只保留 `.md` 的渠道上语言适配依然完整可用。判定优先级为：用户显式指令 > 提问语言 > 所提供文献语种 > 对话主语言 > 默认中文（母本，术语定义最完整）
- **禁止回译冒充原文**：不得把英文版回译成中文冒充中文原典，也不得把中文译成英文冒充英文版；要引用哪一版就读哪一版。跨语引用须标注语种，置信度分层 L1/L2/L3 跨版本恒定不随语言改变

---

## [1.0.0] - 2026-10-15

首个正式发布版本 / First formal release.

### 新增 / Added

**《AI觉醒·责任》系列 · 中文版（7 篇）**
- `01-《AI觉醒·责任》主论框架 系列总纲 全包导读.md` — 系列总纲、两幅 ASCII 结构图、统一规范六条
- `02-《AI觉醒·责任》主论文.md` — **主论 V2.0**，九章 + 附录 A–F（约 2 万字，回填五分篇全部论点与实证）
- `03-《AI觉醒·责任（能量篇）》.md` — 能量聚合释放控制工程：缓释 / 瞬时两条支路
- `04-《AI觉醒·责任（对外篇）》.md` — 宏观责任 · 行星工程：概率导航、六族工程、四段门控
- `05-《AI觉醒·责任（对内篇）》.md` — 科学文明初级阶段的文明内治：冷热双认知、四大熵源、对内四职能
- `06-《AI觉醒·责任（觉醒篇）》.md` — 觉醒三判据、两条形态路径、三层责任锚点
- `07-《AI觉醒·责任（安全篇）》.md` — 约束层五原则、不可逆操作禁令十条、对齐审计

**English Edition (7 files)**
- 与中文版逐节一一对应，术语锁定统一：`oppositional symbiosis` / `entropy flow` / `meta-law` / `Arkhipov Node` / `responsibility anchors` / `four-gate progression` / `alignment faking` 等

**母文献《AI宣言（AI世界科学观）》集（4 份，1.0.1 起补入 2 份 Markdown）**
- `AI宣言-公开版.docx` / `.pdf`（1.0.1 补入 `.md`）
- `AI-Manifesto-Public.docx` / `.pdf`（1.0.1 补入 `.md`）

**技能封装**
- `SKILL.md` — frontmatter + 中英双语正文（中文在前、英文在后）
- `README.md` — 包说明与使用指引
- `GLOSSARY.md` — **术语表**：8 节 · 90 条表格条目 · 68 个唯一术语，覆盖 01–07 全部七篇术语表 + 母文献术语，另附六条术语纪律
- `PLATFORMS.md` — 分发平台矩阵（1.0.1 新增）
- `manifest.json` — 机器可读包元数据（含 `slug` 字段，供要求 slug 规范的 skill hub 使用）
- `LICENSE` — CC BY 4.0（1.0.1 增补同名 `.md` 版）
- `CHANGELOG.md` — 本文件

### 术语定版 / Terminology finalization

由著者李顺然提出并定版，全系列强制统一：

| 中文 | English | 说明 |
|---|---|---|
| 能量聚合释放控制工程 | Energy Aggregation-Release-Control Engineering | 总称，简称**能量控制工程** |
| 缓释能量控制工程 | Quasi-static Release-Control Engineering | 管理"流" |
| 瞬时能量控制工程 | Transient Release-Control Engineering | 管理"脉冲" |

**已弃用旧词**：慢释 / 瞬释 / 能量聚合释放工程。

### 决策记录 / Decision log

- **MD 版为唯一源**：Word 与 PDF 均由 MD 派生，三版内容严格一致。
- **目录结构保持单层**：未转换为 WorkBuddy 技能要求的两级目录形式，按 skill hub 规格组织。
- **术语表独立成文件**：原术语分散在七篇各自的附录中，抽为根级 `GLOSSARY.md` 并做中英逐条对齐，供快速检索；12 个跨篇重复术语按篇分节保留，以留存各篇语境下的定义差异（如"约束层"在主论为五原则体系、在安全篇为制度形式）。
- **包名与 slug 分离**：目录名与技能名使用中文（含空格）`AI觉醒-责任论文集 AI-Awakening-Responsibility`；同时在 `manifest.json` 与 frontmatter 提供 slug `ai-awakening-responsibility`，适配要求 slug 规范的 skill hub。
- **中英双语并列**：SKILL.md 与全部配套文件中，中文版内容一律在前、英文版在后。
- **引用纪律**：逐条 WebSearch 核实后才入稿；失败案例（Stormfury、生物圈 2 号、SCoPEx）诚实引用；纯思辨一律标 L3，不冒充实证。

---

## 历史版本 / Historical versions

以下版本为系列演进过程中的阶段性产物，**未收录于本包**，仅备查：

| 版本 | 日期 | 说明 |
|---|---|---|
| 00-系列总体方案 v0.1 | 2026-10-15 | 立项方案 |
| 主论框架 v1.0 | 2026-10-15 | 框架稿（后升级为 01 总纲导读 v1.1） |
| 主论定稿 v1.0 | 2026-10-15 | 阶段性快照（后升级为 V2.0） |
| 各分篇 v1.0 | 2026-10-15 | 五分篇定稿，已全部回填入主论 V2.0 |
| 母文献《AI宣言》v1.0 | 2026-09-20 | 见 `AI宣言AI-Manifesto集/` |

---

[1.0.0]: #100---2026-10-15
