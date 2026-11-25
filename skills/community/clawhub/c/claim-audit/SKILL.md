---
name: claim-audit
display_name: Claim Audit
display_name_zh: 声明审计
description: Use when a skill package, README or report states numbers such as "9/9 PASS", "N files", "100/100" or file paths, and you need to know whether those numbers were actually produced by running the code. Re-runs the package's own test runner, counts real files, re-scores with the reviewer, and checks declared paths exist. Read-only, never edits the document.
description_zh: 当技能包、README 或报告里写了「9/9 PASS」「N 个文件」「100/100」或某个文件路径，需要确认这些数字是不是真跑出来的，用本技能。它重跑包自带的自检、数真实文件、复跑评测器、核对声明的路径是否存在；只读，不改文档。
version: 1.0.0
license: MIT
author: zhaoxinghua09-cell
tags:
- audit
- claims
- verification
- evidence
---

# Claim Audit · 把文档里的数字拉回去重跑一遍

文档里最容易写错、也最容易被读者默认相信的，是数字。`9/9 PASS` 可能是三天前跑的；`12 个文件`可能是加了 references 之前的；`100/100` 可能是在改口径之前量的。本技能只做一件事：**把每个能验的数字重新跑一遍，然后告诉你哪个对不上。**

## 三条坚决不做

1. **不判断"这句话说得对不对"**，只判断"这个数字跑出来是不是这个数"。语义判断不归本工具，越界就是假装有判断力。
2. **不替作者改数字**。对不上是人的事，工具只负责把它摆到台面上。自动改数字比不改更危险，因为读者会以为有人核过。
3. **不把"验不了"当"错"**。没有命令、没有 runner 的声明标 `UNVERIFIABLE`，默认不算失败；需要严格时才加 `--strict`。

**不编**。本工具输出的每个 `实际` 值都来自当场执行：跑出来的通过数、数出来的文件数、复跑出来的分数。算不出来就写 `UNVERIFIABLE`，绝不填一个看着合理的数。

## 判定流程

先分流，再动手。不同来源的声明走不同的核验路径。

| 情形 | 走哪条路 |
|---|---|
| 若声明是 `N/M PASS` 这类自检结果 | 重跑 `tests/run_golden.py`（或 `tests/run_tests.py`），比对通过数 |
| 若声明是文件数（`12 个文件` / `files=12`） | 按真实文件树计数，跳过 `__pycache__`、`.git` |
| 若声明是 `X/100` 分数 | 找同级 `lgd-skill-review/scripts/review.py` 复跑，带 `--run` |
| 若声明是包内路径 | 只核列表项、表格行、链接行里的路径；正文举例不算声明 |
| 若以上都不是（无 runner、无评测器） | 标 `UNVERIFIABLE`，不臆断对错 |
| 若同一份文档里既有当前值又有历史轨迹 | 只看当前值；`46/100 → 67/100`、`基线 46/100` 属过程记录，跳过 |

## 快速开始

审计一个包，看它文档里的数字对不对得上：

```bash
python scripts/audit.py check D:\path\to\some-skill
```

只想看它声明了什么、不跑任何东西：

```bash
python scripts/audit.py list D:\path\to\some-skill
```

要机器可读结果（接 CI 或报表）：

```bash
python scripts/audit.py check D:\path\to\some-skill --json
```

## 输出长什么样

```text
审计对象：D:\doubao\_matrix_v3\evidence-anchor
类型         结论       实际           声明原文
path       OK       存在           - 判定细则与退出码：`references/rules.md`
tests      OK       9/9          python tests/run_golden.py     # 9/9 PASS

声明 7 条：对上 7，对不上 0，验不了 0
```

对不上时是这一行，并且进程退出码为 1：

```text
tests      MISMATCH 7/9          自检全部通过（9/9 PASS）
```

## 退出码

| 退出码 | 含义 |
|---|---|
| 0 | 所有声明都对上（或只有 `UNVERIFIABLE` 且未加 `--strict`） |
| 1 | 至少一条 `MISMATCH`；加 `--strict` 时 `UNVERIFIABLE` 也算失败 |
| 2 | 参数错误或根目录不存在 |

## 硬规则

1. NEVER 把正文举例里的路径当成本包声明。因为举例的 `scripts/review.py:157` 属于别的包，算进来会造出一堆假阳性。
2. NEVER 跳过 `--run` 去复跑分数。因为不带 `--run` 会少掉实跑分，README 的 `100/100` 会被误判成对不上。
3. NEVER 只看 `pass` 不看 `PASS` 的大小写。因为不少 runner 输出是大写，漏判等于放行。
4. NEVER 把 `结构制 100/100 PASS` 当成自检条数。因为那是分数声明，混淆后必然报错。
5. NEVER 把历史轨迹的数字当当前值。因为 `46/100 → 67/100` 记录的是过程，按当前值比对一定失败。
6. NEVER 自动改写文档里的数字。因为读者会误以为有人核过，比不核更危险。
7. NEVER 因为找不到 runner 就判失败。因为缺 runner 是能力缺口，标 `UNVERIFIABLE` 才是诚实。
8. NEVER 让工具写出被审对象的任何文件。因为审计要只读，写一次就毁了证据链。
9. NEVER 在没有路径分隔符归一的情况下核路径。因为反斜杠与正斜杠混用会让存在的文件被判不存在。
10. NEVER 拿 `git` 忽略清单之外的目录当文件数。因为 `__pycache__` 会把 `12 个文件` 变成 19 个。

## 失败时的处理

- runner 跑不起来（超时、缺依赖）：该条标 `UNVERIFIABLE`，并在输出里写清原因，**不要**降级成 `OK`。
- 评测器路径找不到：分数类声明一律 `UNVERIFIABLE`，并提示"同级没有 lgd-skill-review"。
- 根目录不存在：直接退出码 2，不进入抽声明阶段。
- 文档里一条声明都没抽到：正常退出，打印"共 0 条声明"，这不是错误，是这份文档没有可验的数字。

## 复测口径

本包自己的自检覆盖 9 条用例，改动 `audit.py` 后必须复跑 `tests/run_golden.py`，再复跑一次真实包（`evidence-anchor` 与 `skill-improver`）确认没有假阳性。判据是**假阳性为零**：宁可漏判，不可冤枉。

## 细节与边界

- 抽声明的规则、正负例与已知误报：`references/rules.md`
- 为什么只做三件事、拒绝清单：`references/limits.md`
- 三种用法与真实输出：`references/usage.md`
- 9 条自检覆盖表：`references/selfcheck.md`
- 端到端演示：`demo/run_demo.py`（造一个写了假数字的包，跑一遍看它被抓出来）

## Triggers

- 用户问"这个包文档里写的 9/9 是不是真的"、"README 的数字对不对"
- 发布前自查：确认文档里的自检条数、文件数、分数没漂
- 接手别人的技能包，想先知道它声明了什么、哪些能验
- 交接或验收：需要对"文档说的"与"实际跑的"出一份对照表

## 同系列技能

| 技能 | 管什么 |
|---|---|
| `lgd-skill-review` | 出分数：结构制 100 分 + 语义制 120 分 |
| `evidence-anchor` | 核锚点：结论挂的文件与行号还存不存在 |
| `claim-audit`（本包） | 核数字：文档里写的数，跑出来是不是这个数 |

三者合起来是一条证据链：**分数可复现 → 锚点可打开 → 数字可重跑**。
