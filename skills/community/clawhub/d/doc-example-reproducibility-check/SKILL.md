---
name: doc-example-reproducibility-check
description: "Verify that example commands and their documented outputs in a technical document, tutorial, README, or skill package are actually reproducible. Use this when a doc contains runnable command examples, before publishing a doc or package whose examples must be trustworthy, when you need to change sample data inside a document (e.g. de-identify real birth dates, account numbers, or customer names) without introducing false claims, or when a document claims a script emits specific fields/values and you need to confirm it does. Covers: extracting every runnable example, separating mutable sample data from immutable factual tables, re-deriving every claimed value by actually running the tool instead of computing it by hand, bulk replacement with a change-count audit trail, and a per-example PASS/FAIL regression run. Trigger phrases: 'verify the examples in this doc', 'are these commands still correct', 'check the doc examples', 'replace the sample data in the docs', 'the docs claim X, does it really output X'."
description_zh: "文档示例可复算性核验"
description_en: "Doc Example Reproducibility Check"
disable: false
agent_created: true
version: "1.0.0"
---

# 文档示例可复算性核验

把文档里**声称能跑**的示例逐条跑一遍，确认文档写的输出是真的；并在必须改动示例数据时，保证「改数据」不引入「假结论」。

## When to use

- 文档／README／教程／skill 包**含可运行示例命令**，且这些示例被读者当作事实依据。
- 需要**替换文档内的样本数据**（去标识化：真实生辰、账号、客户名、内部编号）。
- 文档声称某脚本会输出某字段／某数值，需要实证。
- 发布前复核：文档示例与当前代码是否已经漂移。

## Steps

### 1. 清点全部示例，建立清单

对目标目录提取两类位置：**代码块**与**行内反引号命令**。

- 用 Grep 按代码围栏语言筛（如 ` ```powershell ` / ` ```bash `），再逐文件通读含命令的段落——**行内示例与注释里的示例最容易漏**（脚本头部注释、`--help` 文本、报错文案里的格式示例都算）。
- 同时按**数据形态**做第二遍扫描，不要只扫日期：年份、日期、时刻、编号、四柱／ID 之类的字面量要分别扫（例：`(19[0-9]{2}|20[0-9]{2})[-年]` 抓年份，`[甲-癸][子-亥]` 之类的领域符号抓结构化样本）。
- 输出一张表：`文件 : 行号 : 示例原文 : 所属类别`。

### 2. 分类：可改 vs 不可改（最关键的一步）

对每个字面量判定归属，**两类混改必出错**：

| 类别 | 判据 | 处置 |
|---|---|---|
| **示例／样本数据** | 为了演示而写的，换掉不影响结论 | **可改**，改了要重跑该示例 |
| **事实性数据** | 客观事实、算法常量、领域对照表 | **绝对不改**，改了就变成假话 |

事实性数据的典型形态（本轮实测踩到）：政策／历史时间窗口表、换算系数表（均时差、温差）、算法基准日（`new Date('2024-01-01')`）、法规生效日、领域字典的键（如按「月柱→用神」索引的对照表）。**这些即使长得像日期也一律不动。**

→ 把「不改」的那批**逐条列出来并写明理由**，作为审计留痕。只给「改了什么」而不给「故意没改什么」，事后无法复核。

### 3. 逐字复算，不要改写命令

- **照文档原文抄命令**跑，包括怪异的前缀与引号（例：`"@query.example.json"` 的 `@` 在 PowerShell 里不加引号会变 splatting，导致整个脚本块一条不执行）。
- 若某条失败，**先怀疑自己的调用形式**，不要立刻判定「文档写错了」。区分清楚是「文档有误」还是「我抄漏了」。
- 命令**写文件而非打印**时，判定标准是「退出码 + 目标文件内容同时命中」，只看退出码会放过空文件。
- 文档若声称「该命令同时输出三件事」，就**逐项去找这三件**，而不是看到命令成功就算过。

### 4. 任何要改的判断，必须由工具重新产出

**禁止手算／推算**替换后的值。经度差、时差修正、跨年周期这类量手算极易错，且错了无人能发现。

- 先把新样本喂给工具，拿到真实输出（例：真太阳时 `14:34:17`、四柱 `庚辰 辛巳 癸酉 己未`、交节翻转点落在哪个小时区间）。
- 再拿真实输出回填文档表格与结论。
- **等价证据要重新构造**：旧结论引用的是旧样本的实测值，换样本后要么重跑出新样本的等价实测，要么删掉该结论——不能保留旧数字。

### 5. 批量替换 + 改动留痕

- 用**一次脚本**做替换，输出 `文件: 旧串 -> 新串 x次数` 的报告，总次数与文件数写进记录。
- **顺序敏感**：长串先替（`1990-05-15T14:30:00` 先于 `1990-05-15`），否则短串会把长串切坏。
- **锚点不要含 shell 元字符**：`&`（如 `& $NODE ...` 行首）在部分工具层会被转义成 `&amp;` 而匹配失败；改用不含元字符的子串做锚点。
- 替换后**再全量扫一遍残留**，并明确「残留中哪些是允许保留的事实性数据」。

### 6. 全量回归

改动后把文档示例**整批重跑**，逐条给 PASS/FAIL 与期望串，最后给汇总数（例：`PASS 16 / FAIL 0`）。

- 清理临时产物（依赖联接、临时目录），并**核验已清理干净**（例：残留 `node_modules` 目录数 = 0、文件数与清单一致）。

## Pitfalls

- **把事实性表格和样本数据一起替换** —— 最常见也最难察觉的错误，直接制造假结论。
- **手算代替运行** —— 尤其涉及时区／夏令时／历法换算时。
- **改动样本后沿用旧实测数字** —— 旧证据与新样本不匹配，结论变成捏造。
- **自动替换把已经改过的内容再改一次** —— 幂等性：同一规则重复运行不应产生第二次变化。
- **工具层假象被当成文档缺陷**：shell 元字符转义、stdout 被吞（先落盘再读）、原生命令非零退出中断整个脚本（`$ErrorActionPreference='Continue'`）、慢命令撞默认超时（表现为「零输出 + 非零退出」但实际成功）。
- **只看退出码** —— 命令成功但产物为空／缺字段是常态。
- **自己实现一遍解析／计算逻辑去「等价复算」** —— 简易实现往往少了正规实现的规范化步骤（如剥引号、字段展开），会报出**假警报**。能用真函数就用真函数。

## Verification

- 清单覆盖：文档内每一处可运行示例都有 PASS/FAIL 记录，无遗漏（含注释与 `--help` 文本里的示例）。
- 事实性数据：有独立的「保持不变」清单 + 理由。
- 无残留：全量扫描后，剩余旧字面量逐条归类且均可解释。
- 幂等：再跑一次替换脚本，改动数为 0。
- 副作用归零：临时挂载／临时目录已清除并核验。
