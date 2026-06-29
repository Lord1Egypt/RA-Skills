# 高考志愿研究 Skill

`gaokao-volunteer-research` 是一个面向中国高考志愿研究的 Codex/Avatanel skill。它的目标不是“替你填志愿”，而是把志愿相关问题转成一套可查证、可复核、可交付的研究流程。

它适合用于：

- 高考志愿、大学志愿、选大学、选专业、冲稳保垫研究。
- 一分一段、分数对应位次、本科线、专科线、批次线核对。
- 招生章程、院校/专业信息、政策文档、高考真题来源整理。
- 志愿参考前的口径校验和风险点整理。
- 生成 `sources.md`、`data-check.md`、`candidate-matrix.md`、`family-brief.md`、`risk-notes.md` 等研究包文件。

## 核心边界

- 必须优先使用官方、当年、可追溯资料。
- 缺少省份、年份、位次等关键口径时，不得直接给具体候选矩阵。
- 不承诺录取结果，不预测录取概率，不声称掌握内部数据，不代替用户提交官方志愿系统。
- 非官方榜单、短视频、截图、家长群表格只能作为线索，必须回到省考试院、阳光高考/阳光志愿、高校招生章程等来源核验。
- 真题资料只整理来源、入口、年份、科目、卷别和授权状态，不大段转载非官方或未授权题面/答案解析。

## 目录结构

```text
gaokao-volunteer-research/
├── SKILL.md
├── CHANGELOG.md
├── README.md
├── data/
│   └── official-source-index.json
├── examples/
│   └── sample-run.md
├── references/
│   ├── source-policy.md
│   ├── test-scenarios.md
│   └── tooling.md
├── scripts/
│   └── gaokao_toolkit.py
├── templates/
│   ├── candidate-matrix.md
│   ├── data-check.md
│   └── family-brief.md
└── tests/
    ├── fixtures/
    └── regression-cases.json
```

## 快速使用

在支持 skill 的 agent 中直接说：

```text
使用 gaokao-volunteer-research。
2026 年广东物理类 612 分，我不知道位次。先不要推荐学校，先帮我做 data-check：查一分一段、分数对应位次、本科线/专科线/批次线，并列出官方来源和下一步核验路径。
```

资料查证示例：

```text
使用 gaokao-volunteer-research。
帮我整理 2026 年江苏高考真题、答案或官方试卷资料来源。不要转载题面，只列来源、URL、年份、科目/卷别和是否官方。
```

完整研究包示例：

```text
使用 gaokao-volunteer-research。
2026 年广东，物理类，位次 18000，本科批，偏计算机/电子信息，公办优先，城市优先广州深圳珠三角。请生成 sources.md、data-check.md、candidate-matrix.md、family-brief.md 和 risk-notes.md。
```

## 工具层

确定性工具入口是：

```bash
python3 scripts/gaokao_toolkit.py --help
```

常用命令：

```bash
python3 scripts/gaokao_toolkit.py index lookup --province 广东
python3 scripts/gaokao_toolkit.py index verify --province 广东 --timeout 10
python3 scripts/gaokao_toolkit.py parse-table --input tests/fixtures/guangdong-score-table.md --out /tmp/gaokao-score-table.json --kind score --province 广东 --year 2026 --category 物理类
python3 scripts/gaokao_toolkit.py validate-package --dir tests/fixtures/sample-package --province 广东 --year 2026 --category 物理类
python3 scripts/gaokao_toolkit.py regression --cases tests/regression-cases.json
```

工具能力：

- `index`：查询和验证省级考试院、阳光高考等官方入口。
- `snapshot`：保存政策、章程、PDF、真题来源页面等快照和 metadata。
- `parse-table`：解析 CSV、TSV、Markdown、简单 HTML 表格。
- `validate-package`：检查研究包文件、URL、口径和禁止表达。
- `regression`：检查 skill 文档是否保留关键触发词和回归样例。

## 推荐研究包

默认研究包包含：

```text
sources.md
data-check.md
candidate-matrix.md
family-brief.md
risk-notes.md
raw/
```

其中：

- `sources.md` 记录来源、URL、发布日期、适用年份和用途。
- `data-check.md` 记录分数、位次、一分一段、批次线、本科线/专科线和口径风险。
- `candidate-matrix.md` 记录候选院校/专业组、计划数、限制条件、证据链接、风险层级和待核验问题。
- `family-brief.md` 面向学生和家长总结决策摘要、冲稳保垫分层、重大风险和电话确认清单。
- `risk-notes.md` 记录不能直接下结论的来源冲突、缺失数据和下一步核验路径。

## 验证

在仓库根目录运行：

```bash
python3 scripts/gaokao_toolkit.py regression --cases tests/regression-cases.json
python3 scripts/gaokao_toolkit.py validate-package --dir tests/fixtures/sample-package --province 广东 --year 2026 --category 物理类
python3 scripts/gaokao_toolkit.py parse-table --input tests/fixtures/guangdong-score-table.md --out /tmp/gaokao-score-table.json --kind score --province 广东 --year 2026 --category 物理类
python3 -m py_compile scripts/gaokao_toolkit.py
```

预期：命令返回 `ok: true` 或正常退出。

## 注意

`data/official-source-index.json` 是官方入口种子，不等于当年正式数据。正式研究必须进入当年省考试院发布页、阳光高考/阳光志愿、高校招生章程或其他官方材料做最终核验。
