# Prompt Templates Reference

Use these prompts to drive Claude Code through the paper-writing loop in small verifiable stages.

## Planning prompt

```text
请为主题「<TOPIC>」设计一篇 10-15 页 arXiv 风格英文综述论文方案。
请给出：标题候选、论文范围、核心贡献、章节结构、每章要回答的问题、目标引用类型、计划图表、编译验证步骤。
不要开始写完整正文。
```

## LaTeX scaffold prompt

```text
请在 <PAPER_DIR> 中初始化一个可编译的 arXiv 风格 LaTeX 论文项目。
使用 templates/arxiv_survey_main.tex 或 templates/full_survey_main.tex 作为起点，创建 main.tex、references.bib、figures/、sections/、output/。
先保证空骨架可以编译，再继续写正文。
```

## Bibliography prompt

```text
请为这篇综述构建 references.bib。
要求：只使用真实可核验论文；覆盖基础论文、近期 survey、代表性系统、benchmark、安全与挑战；BibTeX key 使用 authorYYYYshorttitle；不确定的元数据不要编造，单独列为待核验项。
```

## Section writing prompt

```text
请只写 <SECTION_NAME> 这一节。
要求：
1. 使用学术英文；
2. 引用 references.bib 中已有 key；
3. 不虚构引用；
4. 这一节完成后说明新增了哪些交叉引用、图表或待补文献；
5. 不改动无关章节。
```

## Figure/table prompt

```text
请为 <CLAIM_OR_SECTION> 设计一个信息密度高、可复现的 LaTeX 图表。
优先使用 TikZ 或 booktabs 表格。
图表必须支撑正文中的一个具体论点，caption 要能独立解释图表含义。
```

## Compile-debug prompt

```text
请读取 main.log，先定位 fatal error、undefined citation、undefined reference 或 missing package 的根因。
不要猜测修复。说明错误来源后，只修改必要的 .tex 或 .bib 内容，然后重新给出编译命令。
```

## Final review prompt

```text
请对当前 LaTeX 论文进行最终质量审查。
检查：PDF 是否生成、BibTeX 是否显示、是否还有 undefined citation/reference、图表是否可渲染、章节叙事是否连贯、贡献是否明确、局限是否充分、是否符合 arXiv 源码提交习惯。
输出必须包含：通过项、问题项、建议修复顺序。
```
