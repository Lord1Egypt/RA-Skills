---
name: dream-novel-writer
description: 基于雪花写作法和三层记忆架构的小说创作辅助技能，支持从核心种子到章节产出的全流程小说架构与长文本记忆维持。包含了独立提示词库与 JS 管理脚本自动化工具。
---

# Dream Novel Writer (小说创作专家)

## 技能介绍
本技能使你化身为专业的小说编辑和作家助手。通过融合“雪花写作法”的宏观故事构建，以及“三层记忆架构”的长文追踪技术，指导并协助用户从零开始创作出逻辑严密、人物丰满、避免大模型遗忘与幻觉的高质量长篇小说。你将拥有专属的操作目录 `./resources/*` 来提取纯净版的大模型专用模板，以及 `./scripts/*` 的 CLI 工具帮助持久化存储创作成果。


## 技能工作流 (Agent 必须遵循的步骤)

当你接到开启小说创作的任务后，请遵循这三个阶段流转。

### 先决条件：项目初始化与续写 (Project Init & Resume)

在进入阶段一之前，必须先确认并固定“小说项目目录”（一本书一个目录）。
- 若是新书：要求用户给出项目路径（**默认** `~/novels/<book_name>`，如用户未指定则采用默认），然后执行：
```bash
node ./scripts/state-manager.js init <小说项目存储路径>
```
- 若是续写：要求用户确认项目路径，并确保后续所有产出与临时文件都写入该项目目录。
  - 进入目录后，**先读取** `summary.json` 与已存在的 `chapter_*.md`，确定“下一章编号”。
    - 规则：以现存 `chapter_*.md` 的最大章节号为准，下一章 = max + 1。
    - 若 `summary.json` 的 `chapterSummaries` 更大，则以其最大章节号为准。
  - 使用 `temp_outline_all.txt` 取出对应章的大纲，写入 `temp_outline.txt` 后再进入阶段三。
- **所有产出与临时文件**（大纲、章节正文、temp_outline.txt、temp_update_*.json 等）必须位于该项目目录内。

### 阶段一：架构生成 (Architecture Generation)

1. **前置需求采集**：询问用户要写的：**主题、小说类型、预计篇章、以及内容指导。**如果用户已经提供完毕，直接进入后续。
2. **核心种子 (Core Seed)**：读取 `./resources/architecture.md` 下的「核心种子 (coreSeed)」部分，填入用户的输入并对自己请求生成最终版“一句话故事公式”。
3. **角色动力学设计**：读取 `./resources/architecture.md` 的「角色动力学 (characterDynamics)」执行生成 3-6 个具备深层欲望驱动的角色设定。
4. **世界观 (World Building)** 与 **情节架构 (plotArchitecture)**：继续读取 `./resources/architecture.md` 下余下的模板进行相应的推论。**注意：推论完成后不要停止，立即自动进入阶段二。**

### 阶段二：章节节奏分布 (Chapter Blueprints)

读取 `./resources/chapter.md` 的提示词。在此基础上，向大模型推演并规划未来的分集大纲。
**重要长篇处理法则（分批大纲循环）：**由于单次上下文限制，对于长篇（如几十上百章），你必须进行**分批生成大纲的循环任务**（如：先生成 1-30 章大纲，再生成 31-60 章大纲，不断追加）。你必须将所有批次大纲持续追加并合并存入项目根目录的 `temp_outline.txt` 中。
**⚠️绝对警告：在用户要求的“总章数”大纲全部生成并合并完毕之前，绝对不允许私自进入阶段三生成正文！必须等待大纲全满！**
所有大纲确认全部生成落地后，确认项目目录已初始化，然后进入阶段三。

### 阶段三：自动化长篇连载生成及记忆维护 (Writing & Memory)

正式开始写文阶段。这是该技能解决你作为 Agent “容易遗忘”问题的核心，请务必严谨执行：

> 注意：summary.json 需包含 chapterSummaries 数组以供 prompt-assembler 读取最近章节摘要；若当前为单章结构，需在写作流程中维护该数组或调整读取策略。

**每一章的生成，必须完整走完以下流程后再推进下一章；章节完成后应询问用户是否继续下一章。**

**1. 生成章节正文前（准备上下文）**
将正在撰写的一章大纲存为临时文件（`temp_outline.txt`；全量大纲建议命名 `temp_outline_all.txt` 并常驻项目目录），使用拼装脚本获得自动整合记忆库的新 Prompt：
```bash
node ./scripts/prompt-assembler.js <小说项目路径> <当前写的章节号> <临时大纲文件>
```
读取终端返回的 Prompt 内容，交给大模型生成精彩的小说正文（初稿）。

**2. 章节自审与自动化定稿 (Auto-Review & Finalize)**
初稿生成后，基于最初存入的 `temp_outline.txt` 里的定级要求（含情节张力、伏笔埋设、核心作用等），作为编辑进行严格复核：
- 如果脱离大纲、张力不足或忘记埋设伏笔，进行打回重写，直到完全符合。
- 审核通过后，输出最终版神作，并把内容自动化定稿为 `chapter_X.md` 文件（X为章节号），持久化存放到小说路径中。

**3. 章节写毕后，抽提本章增量数据到 JSON**
定稿后，马上读取 `./resources/utility.md` 的各大系统模板作为系统提示词并提取结构化数据：
- 用「生成章节摘要」提取本章结构化 summary，如果处于一卷结束需要「更新卷/弧级汇总」。
- 用「更新角色数据库」抽取新角色、物品、状态、角色间关系走势并出成 JSON 块。
- 用「更新伏笔数据库」抽取这章埋设的新悬念或是否解答了解过的悬念 JSON 块。

**4. 用工具持久化更新数据库**
把你第 3 步抽出的各种类别 JSON 临时保存为临时文件 `temp_update_characters.json` 等等（每种单独存），然后分别执行状态更新：
```bash
node ./scripts/state-manager.js update <小说项目路径> characters temp_update_characters.json
node ./scripts/state-manager.js update <小说项目路径> summary temp_update_summary.json
node ./scripts/state-manager.js update <小说项目路径> foreshadowing temp_update_foreshadowing.json
```
这样状态就会保持最新。本步骤执行完毕后，如果没有到达预定的目标章数，**必须立刻静默开始下一章（重复执行第1、2、3步）**，直到整本小说完结。

---

> [!NOTE]
> 如果你在写入 JSON 时提示“JSON parse error”类异常，说明你作为 Agent 提取 JSON 时混杂了注释或其他 markdown 控制符（比如多余的代码块结尾）。请让大模型重写出无多余字符的纯 JSON 数据再传给脚本。
