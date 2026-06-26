# 论文项目初始化脚手架

当用户要求按该技能启动一个具体论文项目时，默认创建如下结构：

```text
<project>-paper/
├── MEGA_PROMPT.md
├── RESTRICTS.yaml
├── PROGRESS.md
├── plans/
├── code/
│   └── README.md
├── data/
│   └── README.md
├── docs/
│   ├── overall-outline.md
│   ├── experiment-plan.md
│   └── literature-notes.md
├── results/
│   └── README.md
└── paper/
    └── mypaper/
        ├── main.tex
        ├── figures/
        └── sections/
            ├── introduction.tex
            ├── related_work.tex
            ├── method.tex
            ├── experiments.tex
            ├── results.tex
            ├── discussion.tex
            ├── limitations.tex
            ├── conclusion.tex
            └── appendix.tex
```

## 初始化规则

1. 项目目录名默认用 `<project>-paper`。
2. `MEGA_PROMPT.md` 来自项目定制版，而不是直接把 skill 的大模板原样塞进去。
3. `RESTRICTS.yaml` 以 `templates/RESTRICTS.example.yaml` 为起点，再补充会议、页数、实验轮次等具体值。
4. `PROGRESS.md` 必须预置：
   - stage checklist
   - v1 / v2 循环记录区
   - risk / blocker 区
   - git 提交记录区
5. `paper/mypaper/main.tex` 必须只负责组织结构，正文拆分到 `sections/`。

## 最小可用文件建议

### `code/README.md`
- 记录运行方式
- 记录环境
- 记录实验入口脚本

### `data/README.md`
- 记录数据来源
- 记录预处理规则
- 记录不可伪造要求

### `results/README.md`
- 记录结果文件格式
- 记录每轮实验编号
- 记录图表与表格来源

### `PROGRESS.md`
至少包含：
- Topic
- Target venue
- Deadline
- Stage progress table
- Current decision: PROCEED / REFINE / PIVOT
- Evidence summary
- Next actions

## 可复用模板

技能目录中已提供这些可复用模板：

- `templates/PROGRESS.template.md`
- `templates/MEGA_PROMPT.project.md`
- `templates/RESTRICTS.example.yaml`
- `templates/main.tex`
- `templates/sections/*.tex`

## 使用方式

当用户给出论文题目、会议、路径、摘要、实验文档后，按此脚手架实例化项目，并优先从 `templates/` 复制模板文件，再做项目特定替换。
