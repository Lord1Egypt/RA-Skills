# agent-constraints

给 coding agent 设置和治理约束的技能。

**它解决的不是「AGENTS.md 怎么写」，而是「这条约束该用什么机制来实现」。**

真实场景里人遇到的是「agent 老是用 pip 装依赖」或者「它又把 `legacy/` 当死代码删了」，默认反应是往 CLAUDE.md 加一行。这个技能拦住这个默认反应，把问题走一遍分层判断——多数时候正确答案是 hook 或权限规则，不是加一行文字。

依据是三篇 2026 年的实证研究，核心结论：**上下文文件是行为杠杆，不是性能增强器**。无配置文件时目标指令执行率 0%，有文件时 67.7%——文件极其有效；但任务成功率变化不显著，推理成本必然上升约 20%。所以写下的每一条都会被真的执行，而执行不等于有帮助。数字见 `EVIDENCE.md`。

---

## 安装

在仓库根目录执行：

```bash
# 所有项目生效（推荐，这个技能是通用的）
mkdir -p ~/.claude/skills && cp -r skills/agent-constraints ~/.claude/skills/
```

```bash
# 只在当前项目生效
mkdir -p .claude/skills && cp -r skills/agent-constraints .claude/skills/
```

验证：**新开一个会话**，输入 `/agent-constraints`。刚装好的技能不在当前会话的技能索引里，调用会报 `Unknown skill`，要等索引刷新才出现。

改过 `SKILL.md` 之后也一样要新会话。正文走一个异步缓存，比磁盘落后一拍——实测改完立刻重调用拿到的是**上一版**内容，中间那次还会回一句 "instructions unchanged"。在旧会话里改一版调一次，你验的不是你刚写的东西。

可选：装上会话记录 hook，为定期复盘留数据。装法见 `hooks/README.md`。

---

## 什么时候会启动

**自动触发**（匹配对话内容）：

- 「帮我写个 AGENTS.md」「我的 CLAUDE.md 太长了」
- 「agent 老是犯这个错，该怎么办」「这条规则该放哪」
- 「怎么禁止它动 migrations 目录」「怎么强制它跑完测试再结束」

**手动**：`/agent-constraints`

**不会自动触发的**：agent 在编码过程中自己意识到「该加条约束了」。这是刻意的——这份技能自己的证据表明，指令层的自我监控不可靠。触发靠工作流 E 的记录 + 复盘。

---

## 四层模型

每条规则放在**能承载它的最低层**。

| 层 | 机制 | 性质 |
|---|---|---|
| **1 执行层** | 执行门：hooks、`permissions.deny`、CI required check、pre-commit；检查器：linter、formatter、类型系统、测试 | 执行门确定性；检查器须接入执行门 |
| **2 常驻层** | AGENTS.md / CLAUDE.md | 每会话付费；单次应用命中 45%–84%，主要看任务类型 |
| **3 按需层** | Skill、path-scoped rule | 只在相关时进上下文 |
| **4 会话层** | prompt、plan mode、SPEC.md、`/goal` | 一次性 |

核心判断：能被第 1 层强制的，绝不放第 2 层。

---

## 五个工作流

| | 场景 | 做什么 |
|---|---|---|
| **A** | 从零配约束 | 先建第 1 层（把已有 linter/测试接上 hook），再复制模板**先删后填**。劝阻 `/init` 一把梭。 |
| **B** | agent 犯了错 | 单条规则走六步定层流程。触发条件是**第二次**犯同一个错，不是「想到一条好规则」。 |
| **C** | 配置乱了 | 读全套配置逐条**重新定层**，带判定表；反向检查缺什么；检查文件间矛盾。输出建议，等确认再改。 |
| **D** | 委派编写 | 开子 agent 写第 1/3 层产物，**强制要求验证并带回证据**，附各类产物的验证方法与陷阱。 |
| **E** | 定期复盘 | 读会话日志 + auto memory 的 feedback 文件，**只挑出现两次以上的**，逐个定层。建议每周或每 15–20 个会话一次。 |

---

## 文件

```
SKILL.md                决策流程 + 四层落地要点（调用时加载）
LAYER1-ENFORCEMENT.md   hooks 与权限规则的实际写法
LAYER2-INSTRUCTIONS.md  AGENTS.md 写作规范、修剪判定表、反模式
LAYER3-ONDEMAND.md      Skill 与 path-scoped rule
EVIDENCE.md             支撑数字，自包含
templates/              AGENTS.md + CLAUDE.md 模板
hooks/                  SessionEnd 记录脚本 + 装法
```

常规使用只加载 SKILL.md，其余按需展开。

`LAYER1-ENFORCEMENT.md` 是最实的部分，全部核自官方文档，包含三个**会静默失效**的坑：

- `Write(docs/**)` 会被接受但**永不生效**——只有 `Edit(...)` 和 `Read(...)` 被文件权限检查读取
- `Bash(command:rm *)` 被忽略并告警，要写 `Bash(rm *)`
- 单个前导斜杠不是绝对路径，`/Users/x` 锚在 settings 作用域，绝对路径要写 `//Users/x`

---

## 它不做什么

**不替你判断项目该有哪些约束。** 提供的是判断程序，不是规则清单——规则必须绑定到你自己真实发生过的失败。

**不自动发现问题。** 记录是确定性的（hook），发现重复需要你发起复盘。这个分工是刻意的：能确定性执行的交给 hook，需要判断的不假装它是自动的。

**不保证 hook 一定挡住。** `Stop` hook 连续 8 次阻止后 Claude Code 会强制结束回合。

**结论不可移植。** 任务类型对合规率的影响达 39 个百分点、模型 12.8 个、代码库 11.0 个，都大于文件怎么写。要在你自己的模型和代码库上实测——但也要知道跑三次看不出 10 个百分点的差别，小规模验证只能筛掉完全无效的规则。

---

## 适用范围

第 1 层的语法（hooks、权限规则）是 **Claude Code 专有**的，其他 agent 机制不同，不要照搬。第 2 层的写作规范跨工具通用。第 3 层的 path-scoped rule 在 Copilot 里对应 `applyTo`。

支撑数据来自 Python 与 TypeScript 上的研究，对 Go、Rust、Java 的执行行为没有证据。两篇实验论文均为 arXiv 预印本，未见同行评审。每条结论的统计功效与适用边界见 `EVIDENCE.md`，原始论文链接在其文末。
