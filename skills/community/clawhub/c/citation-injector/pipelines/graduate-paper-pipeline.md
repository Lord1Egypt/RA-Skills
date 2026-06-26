# Pipeline：中文毕业论文重构与定稿（研究阶段草案）

> 状态：研究阶段草案  
> 当前定位：先研究流程与所需 skills，**暂不绑定 UNITS，不强行做成可执行合同**  
> 面向对象：已有学校模板、既有论文、Overleaf 源稿、PDF、BibTeX、实验图表与中间工作文档的中文毕业论文写作  
> 核心目标：把“已有材料”重构为“主线统一、结构顺畅、证据完整、术语一致、可编译交付”的中文毕业论文

## 1. 这条 Pipeline 的本质

这不是一条“从零写论文”的线性流程，也不是“把几篇 paper 拼起来”的拼装流程，而是一条**以问题清单驱动、以 Markdown 中间层为主、以 TeX 交付层收口**的论文工程 Pipeline。

它的真实主循环是：

> `问题清单 -> 语义定位 -> Markdown 重构 -> TeX 回写 -> 编译复查 -> 问题回写 -> 再进入下一轮`

因此，这条 Pipeline 的首要目标不是“赶紧写出一版正文”，而是先把以下几件事做对：

1. 先把已有材料还原出来，而不是直接在 `tex` 里盲改。  
2. 先围绕毕业论文主线重构章节角色，而不是照搬原论文叙事。  
3. 先在 Markdown 中间层把结构、证据、术语与图表想清楚，再回写到 TeX。  
4. 先解决结构与证据问题，再解决文风与去 AI 味问题。  
5. 真正的收敛点不是“写完一遍”，而是“问题清单被逐轮清空、编译与复查稳定通过”。

## 2. 这条 Pipeline 和 survey Pipeline 的根本区别

它与 `arxiv-survey` / `arxiv-survey-latex` 的差异很大，必须单独建模：

- survey pipeline 的起点是“根据主题检索文献并逐层收敛结构”；
- graduate-paper pipeline 的起点是“已有材料盘点与重构”；
- survey pipeline 的核心中间工件是 `outline/evidence_drafts/...`；
- graduate-paper pipeline 的核心中间工件是 `codex_md/` 里的大纲、问题清单、章节中间稿、图表计划和复查记录；
- survey pipeline 的主目标是“生成一篇综述”；
- graduate-paper pipeline 的主目标是“把已有研究工作重构成一篇符合中文学位论文规范的定稿论文”。

一句话说：

> survey 更像“检索驱动的证据写作流程”；  
> graduate-paper 更像“已有材料驱动的论文工程重构流程”。

## 3. 工作区分层与关键工件

这条 Pipeline 需要明确区分**思考层**与**交付层**。

### 3.1 目录职责

- `main.tex`：论文总入口，负责装配封面、摘要、目录、正文、附录、致谢、成果与参考文献。  
- `chapters/`：最终交付版正文 `.tex`。  
- `abstract/`、`preface/`、`acknowledgement/`、`achievements/`：非正文正式交付部分。  
- `references/`：参考文献库与样式文件。  
- `pdf/`：已发表或已投稿论文 PDF。  
- `Overleaf_ref/`：既有源稿、修回稿、补充材料。  
- `codex_md/`：中间工作层，是**论文重构工作区**。  
- `claude_md/`：复查清单、终稿核对记录。  
- `tmp_layout/`、`tmp_layout2/`：图表试排与版面预演。  

其中最关键的是：

- `codex_md/` 是**思考区 / 重构区**  
- `chapters/` 是**交付区 / 定稿区**

不要把二者混用。

### 3.2 建议固定的中间工件

建议在这条 Pipeline 里把以下工件长期固定下来：

- `codex_md/material_index.md`：已有材料盘点与索引  
- `codex_md/material_readiness.md`：材料就绪度与缺口提示  
- `codex_md/missing_info.md`：缺失信息清单  
- `codex_md/question_list.md`：本轮问题单、优先级与验收口径  
- `codex_md/00_thesis_outline.md`：毕业论文主线、大纲、章节角色  
- `codex_md/chapter_role_map.md`：来源材料 -> 章节 -> 角色 映射表  
- `codex_md/chapter_rewrite_rules.md`：章节重构准则表  
- `codex_md/terminology_glossary.md`：术语统一表  
- `codex_md/symbol_metric_table.md`：符号 / 指标统一表  
- `codex_md/figure_plan.md`：图表与版面计划  
- `claude_md/review_checklist.md`：编译、排版、数据、模板项复查清单  
- `output/THESIS_BUILD_REPORT.md`：编译与终稿检查报告

## 4. 这条 Pipeline 真正需要的 skills

当前先不考虑复用和泛化，按这条毕业论文 Pipeline 自身所需来拆，第一版建议使用以下 skills。

### 4.1 主链 skills

1. `thesis-workspace-init`  
   职责：初始化论文工程、提醒用户放置材料、建立工作区、检查 `main.tex` 是否可编译、生成材料盘点。

2. `thesis-question-list`  
   职责：建立并维护 `question_list.md`，把每一轮修改目标、问题优先级、边界、验收口径固定下来。  
   这是整条 Pipeline 的**控制面 skill**。

3. `thesis-source-role-mapper`  
   职责：把既有论文 / 模板 / 源稿 / PDF / 图表材料映射到“毕业论文角色”，不是只做 `paper -> chapter`。

4. `thesis-chapter-reconstructor`  
   职责：围绕毕业论文主线，重构每一章的目标、比重、承接与叙事方式。  
   这是整条 Pipeline 的**核心重构 skill**。

5. `thesis-markdown-aligner`  
   职责：统一主线、术语、符号、指标、图表口径，并让各章在 Markdown 中间层收敛成一篇论文而不是一组 paper。

6. `thesis-tex-writeback`  
   职责：把已经在 Markdown 层理顺的内容回写到 `chapters/*.tex`，并同步图表、公式、交叉引用与章节承接。

7. `thesis-compile-review`  
   职责：执行编译、warning 分级、模板模式检查、数据口径核验、问题回写。  
   它负责形成最后的质量闭环。

8. `thesis-style-polisher`  
   职责：在结构、证据、数据稳定后，做中文学位论文风格润色与去 AI 味处理。

### 4.2 并行支线 skills

9. `thesis-visual-layout-planner`  
   职责：图表规划、Mermaid 草图、临时拼版、图文节奏检查。

10. `thesis-frontmatter-sync`  
    职责：同步摘要、封面、附录、成果、致谢、名单等非正文部分，避免这些内容拖到最后才补。

11. `thesis-citation-enhance-review`  
    职责：定位必须有引用支撑的句子，扩充候选文献，核验引用与论断匹配关系，回写 `references/*.bib` 与正文引用。

### 4.3 这 11 个 skills 的关系

主链是：

`thesis-workspace-init -> thesis-question-list -> thesis-source-role-mapper -> thesis-chapter-reconstructor -> thesis-markdown-aligner -> thesis-tex-writeback -> thesis-compile-review -> thesis-style-polisher`

并行支线是：

- `thesis-visual-layout-planner`
- `thesis-frontmatter-sync`
- `thesis-citation-enhance-review`

其中：

- `thesis-question-list` 是全流程控制面  
- `thesis-chapter-reconstructor` 是核心重构面  
- `thesis-compile-review` 是质量闭环面

## 5. Pipeline 总览（按阶段）

| 阶段 | 目标 | 核心 skills | 主要输出 |
|---|---|---|---|
| 阶段 0 | 工程初始化与材料入仓 | `thesis-workspace-init` | 目录骨架、初始编译、材料索引、材料就绪度提示 |
| 阶段 1 | 还原已有材料到 Markdown 中间层 | `thesis-workspace-init` | 初始 Markdown 材料、缺失信息清单、材料缺口提示 |
| 阶段 1.5 | 锁定本轮问题与边界 | `thesis-question-list` | `question_list.md` |
| 阶段 2 | 建立来源材料与毕业论文角色映射 | `thesis-source-role-mapper` | 章节角色映射表、按章材料归类 |
| 阶段 2.5 | 围绕主线重构章节 | `thesis-chapter-reconstructor` | 重构后的章节 Markdown |
| 阶段 3 | 对齐、归并并统一全篇结构 | `thesis-markdown-aligner` | 稳定 outline、术语表、符号表、证据缺口清单 |
| 阶段 3.5 | 图表与版面预演 | `thesis-visual-layout-planner` | 图表计划、图文映射、临时版式结果 |
| 阶段 4 | 回写 TeX 交付层 | `thesis-tex-writeback` | 可编译章节 `.tex`、初版完整 `main.pdf` |
| 阶段 4.5 | 同步非正文部分 | `thesis-frontmatter-sync` | 摘要、附录、封面、成果等同步版本 |
| 阶段 5 | 引用增强与核验 | `thesis-citation-enhance-review` | 引用补强结果、核验记录 |
| 阶段 6 | 编译、排版与终稿复查 | `thesis-compile-review` | `THESIS_BUILD_REPORT`、review checklist |
| 阶段 7 | 最终润色与去 AI 味 | `thesis-style-polisher` | 更自然的中文终稿 |

## 6. 分阶段详细说明

### 阶段 0：工程初始化与材料入仓

**目标**  
先把论文变成一个可维护的工程，而不是一堆零散文件。

**主要输入**  
- 学校模板  
- 现有仓库 / 源稿  
- 学号、年份、中英文题目等基础元信息  
- 现有 `main.tex`

**核心 skill**  
- `thesis-workspace-init`

**主要输出**  
- 基础目录骨架  
- 初始 `main.tex` / 初始 `main.pdf`  
- `codex_md/material_index.md`
- `codex_md/material_readiness.md`

**衔接关系**  
- 如果 `main.tex` 还不能编译，不要进入正文重构阶段  
- 如果材料还没归位，不要开始问题清单与章节重构

**执行重点**  
- 明确哪些是材料区，哪些是工作区，哪些是交付区  
- 先保证“能编译”，再谈“写得好”

### 阶段 1：还原已有材料到 Markdown 中间层

**目标**  
把既有 `template / tex / Overleaf / PDF / bib` 中可复用的内容还原出来，形成 Markdown 中间层，而不是直接在 TeX 层硬改。

**主要输入**  
- 学校模板  
- 既有 `.tex`  
- Overleaf 源稿  
- PDF  
- 参考文献库

**核心 skill**  
- `thesis-workspace-init`

**主要输出**  
- 初始 Markdown 章节材料  
- `codex_md/material_readiness.md`  
- `codex_md/missing_info.md`  
- 材料索引与待补信息清单

**衔接关系**  
- 阶段 1 的输出会直接喂给 `thesis-question-list` 和 `thesis-source-role-mapper`

**执行重点**  
- 重点是“材料资产盘点”，不是“先写漂亮句子”  
- 要显式标出待补实验细节、待补图注、待补引用、待补数字核验

### 阶段 1.5：锁定问题清单与本轮目标

**目标**  
建立本轮控制面，明确这轮到底修什么，不修什么。

**主要输入**  
- 初始 Markdown 材料  
- 上一轮 review 反馈  
- 当前编译 / 结构 / 文风问题

**核心 skill**  
- `thesis-question-list`

**主要输出**  
- `codex_md/question_list.md`

**衔接关系**  
- 这一步是之后所有重构与回写的起点  
- 任何结构性争议，都应该先回到这里重新排序

**执行重点**  
- 每个问题都要写清楚：是什么、为什么、怎么改、验收到什么程度  
- 问题单不是备忘录，而是迭代入口

### 阶段 2：建立来源材料与毕业论文角色映射

**目标**  
把已有材料映射到毕业论文的章节角色，而不是只做“paper 对 chapter”的机械分配。

**主要输入**  
- 现有论文、PDF、源稿、图表  
- 初始 Markdown 材料  
- `question_list.md`

**核心 skill**  
- `thesis-source-role-mapper`

**主要输出**  
- `codex_md/chapter_role_map.md`  
- 按章归类的 Markdown 材料  
- 各章内容边界

**衔接关系**  
- 这是 `thesis-chapter-reconstructor` 的直接输入

**执行重点**  
- 区分：方法主体 / 背景支撑 / 验证证据 / 系统实现 / 局限与展望素材  
- 这里定错了，后面整篇论文都会歪

### 阶段 2.5：围绕主线重构章节

**目标**  
把原论文式叙事改造成毕业论文式叙事。

**主要输入**  
- 章节角色映射表  
- `question_list.md`  
- 各章 Markdown 草稿

**核心 skill**  
- `thesis-chapter-reconstructor`

**主要输出**  
- 重构后的章节 Markdown  
- `codex_md/chapter_rewrite_rules.md`

**衔接关系**  
- 这是整条 Pipeline 的核心阶段  
- 后续一切对齐、回写、编译，都是在这里的重构成果之上进行

**执行重点**  
- 明确每章要回答什么问题  
- 决定哪些内容强化、弱化、上移、下沉  
- 重写与前后章节的承接关系  
- 把“卖点叙事”改成“毕业论文主线叙事”

### 阶段 3：Markdown 对齐、归并与统一

**目标**  
让整篇论文在中间层先变成“一篇论文”，而不是几篇论文的拼接。

**主要输入**  
- 重构后的章节 Markdown  
- `question_list.md`

**核心 skill**  
- `thesis-markdown-aligner`

**主要输出**  
- 稳定版 `codex_md/00_thesis_outline.md`  
- `codex_md/terminology_glossary.md`  
- `codex_md/symbol_metric_table.md`  
- 证据缺口清单

**衔接关系**  
- 结构不稳、术语不稳、指标不稳时，不要进入 `tex-writeback`

**执行重点**  
- 统一研究主线、术语、缩写、符号、指标、图表口径  
- 决定哪些内容在第 2 章统一解释，哪些在第 3-5 章展开，哪些进入附录

### 阶段 3.5：图表与版面预演

**目标**  
在正文定稿前提前规划图表与版式，不要把图表拖成最后的补丁工程。

**主要输入**  
- 稳定版 outline  
- 章节 Markdown  
- 已有图表与实验结果

**核心 skill**  
- `thesis-visual-layout-planner`

**主要输出**  
- `codex_md/figure_plan.md`  
- `mermaid/` 图示草稿  
- `tmp_layout/`、`tmp_layout2/` 版面试排结果

**衔接关系**  
- 图表规划结果会直接影响 `tex-writeback` 的图文结构

**执行重点**  
- 明确每章需要哪些图表支撑主线  
- 先做草图，再做临时拼版，再决定最终落位与图注

### 阶段 4：回写 TeX 交付层

**目标**  
把已经在 Markdown 层理顺的内容回写到 `chapters/*.tex`，并进入交付层。

**主要输入**  
- 稳定版 Markdown 章节  
- 图表计划  
- 术语 / 符号 / 指标统一表

**核心 skill**  
- `thesis-tex-writeback`

**主要输出**  
- `chapters/*.tex`  
- 初版完整 `main.pdf`

**衔接关系**  
- 如果在这个阶段发现结构问题，原则上优先回 Markdown 层修，不在 TeX 层重新发明结构

**执行重点**  
- 同步图表、公式、交叉引用、章首导言与章末小结  
- TeX 层负责交付，不负责重新思考结构

### 阶段 4.5：同步非正文部分

**目标**  
并行维护摘要、附录、封面、成果、致谢等非正文部分，避免它们被拖到最后变成低质量补写。

**主要输入**  
- 正文稳定版本  
- 学校模板项  
- 中英文题目与摘要信息

**核心 skill**  
- `thesis-frontmatter-sync`

**主要输出**  
- `abstract/abstract.tex`  
- `abstract/abstract-en.tex`  
- `preface/...`  
- `appendix/...`  
- `acknowledgement/...`  
- `achievements/...`

**衔接关系**  
- 阶段 6 的终稿复查会把这些部分与正文一并检查

**执行重点**  
- 中英文题目与摘要口径一致  
- 摘要中的数字、指标、方法名与正文一致  
- 附录只放补充性内容，不重复主线

### 阶段 5：文献增强与引用核验

**目标**  
把“应该有引用支撑的句子”系统补齐，并确保引用与论断匹配。

**主要输入**  
- 当前 Markdown / TeX 版本  
- `references/*.bib`  
- 现有 PDF / 参考工作

**核心 skill**  
- `thesis-citation-enhance-review`

**主要输出**  
- 增强后的参考文献库  
- 引用补强记录  
- 引用核验记录

**衔接关系**  
- 文献增强可以与阶段 3、4 并行，但收口必须早于最终润色

**执行重点**  
- 优先找事实性描述、方法分类、经典结论、指标定义、数据来源这类必须有引文支撑的句子  
- 先补对，再补多

### 阶段 6：编译、排版与终稿复查

**目标**  
形成质量闭环，不只是“能编译”，而是“适合提交”。

**主要输入**  
- 完整 TeX 工程  
- 非正文同步版本  
- review checklist

**核心 skill**  
- `thesis-compile-review`

**主要输出**  
- `output/THESIS_BUILD_REPORT.md`  
- `claude_md/review_checklist.md`  
- 已关闭 / 待关闭问题清单

**衔接关系**  
- 阶段 6 的问题会决定回到阶段 1.5 / 2.5 / 3 / 4 的哪个层面修复

**执行重点**  
- 编译通过只是最低要求  
- 需要分级处理 warning：阻断提交 / 必须修 / 可记录观察  
- 还要检查：数据一致性、cite key 有效性、模板参数是否正确、术语与缩写是否统一

### 阶段 7：最终润色与去 AI 味

**目标**  
在结构、证据、数据稳定之后，再做中文学位论文风格润色。

**主要输入**  
- 通过编译与复查的论文版本  
- `中文写作要求.md`  
- `GPT口癖与高频用词调研.md`

**核心 skill**  
- `thesis-style-polisher`

**主要输出**  
- 更自然的中文终稿  
- 去模板化后的导言、小结、总结与展望

**衔接关系**  
- 阶段 7 必须放在最后  
- 如果润色暴露出结构或证据问题，应回退到前面阶段，而不是硬润色遮盖

**执行重点**  
- 优先处理章首导言、章末小结、贡献描述、总结与展望  
- 压低模板腔、宣传腔、AI 常见口癖  
- 目标是“更像学位论文”，不是“更像 AI 优化后的论文”

## 7. 这条 Pipeline 的四个固定回环

为了避免它再次退化成“线性 SOP”，建议把以下四个回环固定下来：

### 7.1 结构闭环

`outline -> 某章 md -> 发现章节失衡 -> 回 outline / question_list`

### 7.2 内容闭环

`paper / Overleaf / PDF -> 抽取内容 -> 重构叙事 -> 发现仍像原论文 -> 再重构`

### 7.3 排版闭环

`tex -> 编译 -> 发现 warning / 图表位置 / 交叉引用问题 -> 回 tex 或图表规划`

### 7.4 文风闭环

`正文稳定 -> AI 润色 -> 发现模板腔 / AI 味 -> 回写作规范与措辞控制`

## 8. 这条 Pipeline 的执行优先级

如果实际运行时资源有限，优先级应当是：

1. `thesis-question-list`  
2. `thesis-source-role-mapper`  
3. `thesis-chapter-reconstructor`  
4. `thesis-markdown-aligner`  
5. `thesis-tex-writeback`  
6. `thesis-compile-review`

换句话说：

- 真正不能省的是“问题清单 + 材料角色映射 + 章节重构 + 编译复查”
- 真正不该最早做的是“润色与去 AI 味”

## 9. 当前结论

这条 graduate-paper pipeline 的第一原则应当是：

> **先重构，再成文；先中间层收敛，再 TeX 交付；先证据与结构正确，再文风与润色。**

因此，这条 Pipeline 后续如果要正式执行化，最值得优先实现的不是“一个大而全的 runner”，而是先把以下 skills 做稳：

- `thesis-workspace-init`
- `thesis-question-list`
- `thesis-source-role-mapper`
- `thesis-chapter-reconstructor`
- `thesis-compile-review`

这五个 skill 稳了，这条中文毕业论文 Pipeline 才真正有落地价值。
