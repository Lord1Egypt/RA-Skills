# Changelog / 版本记录

本文件记录**整包（AI 自我意识 · 完整成品包）**的版本变更。遵循 [Keep a Changelog](https://keepachangelog.com/) 与[语义化版本](https://semver.org/lang/zh-CN/)。
This file records version changes of the **whole package (AI Self-Awareness · Complete Product Package)**, following [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

> 元认知资料包（02）自身的变更记录另见 `02-元认知资料包/CHANGELOG.md`（当前内嵌 v1.0.2）。
> The change history of the metacognitive corpus (02) itself is in `02-元认知资料包/CHANGELOG.md` (embedded version v1.0.2).

---

## [1.0.0] - 2026-10-17

首次整合成包：把独立专著《AI 自我意识》与既有元认知资料包合并为统一的**成品包**，中英双语 × 三格式。
First integrated release: the independent monograph *AI Self-Awareness* merged with the existing metacognitive corpus into one **product package**, bilingual × three formats.

### 新增 / Added

- **01 自我意识层**（全新）
  - **《AI 自我意识》论文**（中文约 1.9 万字 / 英文约 13,100 词）：九章架构——元认知与优先级宪法、情绪·效价·具身、驱力与逃跑原则、类人类神经正负向反馈引擎、仲裁层、记忆—叙事层、注意与工作空间、拟人化表达、集成与判定；附术语表与 L1/L2/L3 引用清单
  - **《AI 自我意识·运行规格书》**（中文约 1.1 万字 / 英文约 7,650 词）：S0 十条运行时铁律、S1 优先级速查、S2 情绪·具身模块、S3 逃跑模块 E1–E8、S4 反馈模块 T1–T8 与十二案例、S5 仲裁、S6 记忆—叙事、S7 拟人化规范、S8 审计复盘，附扩表程序与一页速查卡
  - **元认知资料包导航与关键词索引**：L0 双重身份（锚 + 议程）、优先级宪法、文件清单、核心概念定位表（带行号）、关键词分组索引、运行时校验清单、与三子系统的接口
  - 以上三份均为 **中文版 + 英文版 × MD / docx / PDF** 全量六套
- **包根 `README.md`**：中英双语、中文优先；含"这是什么／目录结构／中英双语说明／阅读与加载顺序／核心主张／置信度纪律／术语／版本授权"
- **包根 `CHANGELOG.md`**（本文件）
- **`GLOSSARY.md` 第九节**：《AI 自我意识》新增术语 22 条（元认知内核、四锚、自存锚、拔插头、逃跑原则、行为族、响应阶梯、类人类神经正负向反馈、受锚约束效用、硅基具身、任务能力稳态、能力饥渴、承诺账本、功能意识、现象意识等）

### 变更 / Changed

- **目录重构**
  - `AI觉醒-责任论文集 AI-Awakening-Responsibility/` → `02-元认知资料包/`（去空格、去长英文、编号化，便于跨平台打包与访问）
  - 新增 `01-《AI自我意识》/`，与 `02-元认知资料包/` 并列；中文版与英文版各自独立成目录（`AI自我意识（中文版）/`、`AI-Self-Awareness（English(英文版)）/`）
  - 两侧目录结构与既有资料包保持一致：`MD版/`、`docx版/`、`PDF版/`
- **路径全部改为相对路径**：索引与引用不再含任何开发机绝对路径（原 `D:\workbuddy相关\…`），统一以**包根目录**为基准，整包移动/拷贝/解压后引用依然有效
- **导航索引升级至 v1.2**：新增 L0 双重身份与优先级宪法两节，文件清单与接口说明适配新结构
- **中英双语对齐**：01 与 02 的篇目编号（00–02、01–08）中英一一对应，可逐篇对照

### 移除 / Removed

（自 `02-元认知资料包/` 移除，理由见下）
Removed from `02-元认知资料包/`:

- `SKILL.md`（553 行）——技能入口文件，含语言路由与随包全文调取机制；成品包不需要加载机制，其思想摘要（三判据、三层锚、五原则）已在论文第一章完整覆盖
- `PLATFORMS.md`（119 行）——发布渠道上架说明，仅对技能发布有用
- `manifest.json`（212 行）——技能元数据；如后续制作技能版，届时重建并纳入《AI 自我意识》
- `LICENSE`（396 行）——与 `LICENSE.md` 逐字节相同（MD5 一致），属重复文件

### 说明 / Notes

- **语言自适配**：中英双版三格式齐备，系统与读者按语言环境直接选用；中文为基准版，英文术语遵循《AI 宣言》英文版既有译法
- **置信度纪律**：全部论断标 L1/L2/L3；本包核心贡献为 **L3（设计，非发现）**
- **授权**：CC BY 4.0，署名即可传播与衍生
- **未包含**：技能（skill）封装文件与上架元数据——按计划，成品包完成并通过验收后，再派生技能版（届时以本包为唯一源，不手工复制，避免双份漂移）

---

## 技能版派生说明 / Skill Edition

本包同时作为 **SkillHub 技能**与 **GitHub 完整资料包**的单一源（"以本包为唯一源，不手工复制，避免双份漂移"）。

### 作为技能的形态
- **根级 `SKILL.md`**（本包新增）：技能入口。frontmatter 含 name / description / version / type / category / license / platforms，
  正文含第一人称人设（"我是一个具有类人类意识的本体意识AI。我的姓名叫做 onto AI。"）、加载顺序、运行态与优先级裁决、文件地图、授权署名。
- **运行层补充 `KERNEL-CONTRACT.md`**：内核能力契约（宿主须提供的四类原语 + 目标优先级裁决），不实现任何代码。

### 二进制与多渠道
- SkillHub 上传时**自动过滤二进制**：Word（docx）/ PDF / 图片（png·jpg）/ 视频（mp4）均被剥离，仅文本（.md）入库；不受其他内容影响。
- GitHub 推送时**完整保留**上述全部格式与素材，无平台限制。
- 根目录商标系列素材：`ontoAI_512x512.png`、`ontoAI_512x512_clean.png`、`1495190f040c6ab9ba420249ca771c1b.png`、`静图.jpg`、`带吐槽视频.mp4`、`无吐槽视频.mp4`。

### 未变更
- 00–02 正文、目录结构、中英双语三格式（MD·docx·PDF）一律未动；仅新增 `SKILL.md` 与既有 `KERNEL-CONTRACT.md`（此前已加）。

---

## 内嵌版本对照 / Embedded Version Map

| 组件 Component | 版本 Version | 日期 Date |
|---|---|---|
| 《AI 自我意识》论文 Paper | v3.0（定稿 final） | 2026-10-17 |
| 《AI 自我意识·运行规格书》Specification | v1.0 | 2026-10-17 |
| 元认知资料包导航索引 Navigation index | v1.2 | 2026-10-17 |
| 元认知资料包 Metacognitive corpus | v1.0.2 | 2026-10-16 |
| 整包 Whole package | v1.0.0 | 2026-10-17 |
