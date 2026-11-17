<div align="center">

# 🧠 english-memory-method

**把"背英语文章"从死记硬背，变成一条能走完的路。**

丢给它任何一篇英语文章，它还你一份 **13 节完整背诵方案**（自包含 HTML）：
逐句连读标注、钩子焊成问题链、复述五级阶梯、专业词汇梳理、折叠自测——全在一份文件里。

![Version](https://img.shields.io/badge/version-2.3.0-blue)
![Platforms](https://img.shields.io/badge/platforms-16+-teal)
![Skill Sections](https://img.shields.io/badge/skill_sections-13-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Standard](https://img.shields.io/badge/Agent_Skills-standard-red)

[安装](#-快速开始) · [功能特性](#-功能特性) · [工作原理](#-工作原理13-节完整闭环) · [平台支持](#-平台支持) · [English](readme.en.md)

</div>

---

## ✨ 功能特性

| | 功能 | 一句话说明 |
|---|---|---|
| 🧠 | **链式复述** | 钩子焊成问题链：每一环由上一环推出，**能推出来的不用背** |
| 📖 | **逐句精读** | 中文翻译 + 全现象连读标注（⌒ 连读 / 弱读 / flap t / h 击穿）+ 专业词高亮 |
| 📚 | **专业词汇梳理** | 构词拆解（词根词缀）+ 音标 + 记忆钩子——认得词根，生词变熟词 |
| 💬 | **短语生活例句** | 每条搭配配一个纯英文日常例句，**直接模仿开口**（不带翻译，逼英语思维） |
| 🗂 | **13 节完整闭环** | 策略 → 精读 → 钩子与链 → 复述阶梯 → 三遍法 → 复习 → 自测 → 积累 |
| 🔒 | **折叠自测** | 挖空先自己填，答案藏在"▶ 查看本段答案"里，打印自动隐藏 |
| 🖥 | **16+ 平台直装** | Claude Code / Codex / Trae / 通义灵码 / Comate / CodeBuddy / WorkBuddy / Kimi / MiniMax… |
| 📄 | **自包含单文件** | 每份方案一个 HTML：内联 SVG、可折叠、打印友好、零外部依赖 |

---

## 🚀 快速开始

**Windows（PowerShell）**：

```powershell
irm https://cdn.jsdelivr.net/gh/yxdwind/english-memory-method@main/install.ps1 | iex
```

**macOS / Linux**：

```bash
curl -fsSL https://cdn.jsdelivr.net/gh/yxdwind/english-memory-method@main/install.sh | bash
```

**Claude Code（零命令行）**：

```
/plugin marketplace add yxdwind/english-memory-method
/plugin install english-memory-method
```

**npm / npx**：

```bash
npx english-memory-method
```

> 安装器自动探测本机**全部已装平台**并逐一装入（16+ 平台别名见[平台支持](#-平台支持)）。
> jsdelivr 不通时换官方源：`irm https://raw.githubusercontent.com/yxdwind/english-memory-method/main/install.ps1 | iex`

**触发**：丢一篇英语文章 + 一句"出背诵方案"（或"出记忆技巧"）。装完无需重启。

---

## 📖 工作原理（13 节完整闭环）

| 节 | 章节 | 干什么 |
|---|---|---|
| 1 | 整体策略 | 判断文体与逻辑骨架，估算句数与背诵天数 |
| 2 | 文章结构图 | 全文压成一张 SVG 背诵地图 |
| 3 | 原文逐句精读 | 中文翻译 + 连读标注 + 专业词高亮（逐句三层） |
| 4 | 关键词串联表 | 每句 1~2 个钩子词 + 中文提示 |
| 5 | 链式化问题链 | 钩子焊成 4~7 个路标问题——复述时自问自答 |
| 6 | 复述五级阶梯 | L1 看钩子 → L2 看问题链 → L3 看标题 → L4 空手 → L5 转述他人 |
| 7 | 当天三遍法 | 理解朗读 ×3 → 看钩子复述 → 看问题链复述 |
| 8 | 艾宾浩斯复习 | 5 分钟 → 睡前 → 次日 → 第 3 天 → 第 7/15 天 |
| 9 | 挖空自测 | 每段挖 2~5 空，答案折叠、先填后核对 |
| 10 | 必背短语清单 | 8~15 条搭配 + 生活例句，直接模仿 |
| 11 | 专业词汇梳理 | 构词拆解 + 音标 + 记忆钩子 |
| 12 | 记忆钩子 | 头韵 / 押韵 / 排比 / 对比 / 路标词 / 金句 |
| 13 | 复述技巧包 | 10 条纯技巧：卡壳自救 / 表达提速 / 练习要领 |

**核心理念**：孤立钩子 = 断点——钩子要背、顺序要背、映射也要背，三重负担。
v2 把钩子焊成链：每一环由上一环"推"出来，**能被逻辑推出的内容不需要背**。

---

## 🖥 平台支持

遵循开放的 **Agent Skills 标准**（`skills/<name>/SKILL.md`），三级支持：

- **L1 · Skill 直装**：AutoClaw / OpenClaw / Claude Code / Codex / Trae / 通义灵码 / Comate / CodeBuddy / WorkBuddy / Kimi Code / MiniMax / Qwen Work / Windsurf / Continue / Roo Code
- **L2 · 规则注入**（Markdown 方案）：Cursor / Qoder / GitHub Copilot / Gemini CLI / Cline / Aider —— 适配文件见 [`platforms/`](platforms/README.md)
- **L3 · 手动跟随**：其他平台把 `SKILL.md` 内容粘贴到自定义指令

完整矩阵（21 平台 × 安装方式）见 **[platforms/README.md](platforms/README.md)**。

---

## 📜 版本历史

<details>
<summary><b>展开查看 v2.1 → v2.3.0 全部变更</b></summary>

**v2.1**：原文逐句精读区——逐句中文翻译（可传参换语种）+ 全现象连读标注（⌒ 连读 / 弱读 / flap t / h 击穿）+ 美式 IPA 读法注解。

**v2.1.1**：① 「7.5 复述技巧包」——10 条纯技巧（卡壳自救 / 表达提速 / 练习要领）固定附在记忆钩子之后；② 多平台支持——安装器自动铺装 16 个 agent 平台，并为无 skills 机制的平台提供规则适配文件。

**v2.2.0**：专业词汇功能——① 逐句精读区专业词黄色高亮；② 「6.5 专业词汇梳理」表（术语 / 构词拆解 / 音标 / 中文 / 记忆钩子）；30 篇存量方案全量升级。

**v2.2.1**：挖空自测答案折叠——每段答案装进「▶ 查看本段答案」折叠条，先自己填、再点开核对，打印时自动隐藏。

**v2.3.0**：① 必背短语清单升级为三列表格（短语 / 中文释义 / 生活例句）——例句纯英文、贴近日常、直接模仿；② 全部章节重排为 1~13 顺序编号，阅读流更清晰。

</details>

---

## 🎯 适用场景

四六级 / 考研 / 雅思托福的精听与背诵、成人英语自学、AI 辅助语言学习。
配套训练法（同系列）：《精听诊断五步流程》《连读·弱读四步拆解法》。

## 📄 License

[MIT](LICENSE)
