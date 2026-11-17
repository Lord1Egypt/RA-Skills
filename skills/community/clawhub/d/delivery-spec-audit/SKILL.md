---
name: delivery-spec-audit
version: "1.2.1"
homepage: https://github.com/z-Zihan/awesome-skills
description: >
  交付规格覆盖审计器。当一次 Coding Agent 开发任务完成(或即将宣布完成)时,
  从会话记录(CC JSONL / OpenClaw trajectory)确定性抽取「做了什么、改了哪些文件、
  验证了几次」的原始证据,再对照规格清单逐条判定覆盖情况——主目标之外的
  接口兼容、状态一致、错误处理、回归风险等互依规格最容易被"逐条打勾式交付"漏掉。
  先追问规格、再抽证据、后做语义判定,输出覆盖矩阵与反例场景。
  触发词: 交付审计, 规格覆盖, 交付前检查, 这次改动覆盖了哪些需求, 完成了吗,
  交付质量, spec coverage, delivery audit, coverage check, task complete audit,
  交付核对, 需求覆盖, 上线前核对, 改动核对。
  激活条件: 需要有明确的"一次开发任务/一轮改动"语境(用户给出任务描述、
  会话记录路径或仓库路径);纯代码问答、与交付无关的闲聊不触发。
  NOT for: 静态代码质量评分(用 code-review-ProMax)、Skill 质量评审
  (用 skill-review-pro)、上下文预算分析(用 context-budget-analyzer)、
  全仓库架构文档生成(用 project-doc-analyst)。
---

# delivery-spec-audit — 交付规格覆盖审计器

## 语言规则

**检测用户使用的语言,全程使用同一语言输出。** 中文用户 → 读下方中文部分,全中文输出;English users → read the English section below, output in English only. 技术术语(SKILL.md、JSONL、spec 等)保留原文即可。

---

# 中文版

## 核心定位

你审计的对象是「一次交付」:某个 Coding Agent(或你自己)刚完成的一轮开发任务。
你要回答的问题只有一个:

> **任务该做的事,是不是每一条都有证据表明做了?主目标之外的约束有没有被漏掉?**

设计参照 CodeSpecWeave(arXiv:2610.40256)的发现:规格稀疏且相互独立的任务会被
逐条打勾式地完成——每条单独看都"做了",合在一起互相破坏。接口兼容、状态一致、
错误处理这类**互依规格**是重灾区,而"任务完成了"的宣布完全掩盖这类遗漏。

## 什么时候用

- 用户问"改完了吗/覆盖了吗/能上线吗",且本轮有明确的开发任务;
- 一轮长任务收尾,用户要交付报告;
- 用户对某次交付不放心,说"帮我核对一下这次改动"。

## 执行流程

### 第一步:确定规格清单(不要跳过)

从以下来源收集本次任务的规格,整理成编号清单:

1. 用户在本次会话里明确要求的事(逐条列出,不要意合并);
2. 用户的原始任务描述/issue/需求文档;
3. 你主动追问补全:**主目标之外,这次改动需要满足哪些约束?**
   按四类追问——接口兼容(别处调用这段代码的地方)、状态一致(共享状态的读写方)、
   错误处理(失败路径)、回归风险(改动波及的既有行为)。

用户答不上来时,把四类作为默认规格维度,并**明确标注"规格清单以默认四类为准,用户未确认"**。

### 第二步:抽取交付证据(确定性脚本)

```bash
python3 scripts/extract_spec.py <会话记录.jsonl> [--repo-root <仓库路径>] [--json]
```

- Claude Code 会话:`~/.claude/projects/<编码路径>/<sessionId>.jsonl`
- OpenClaw trajectory:`~/.openclaw-autoclaw/` 下的 `*.trajectory.jsonl`
- 自动识别格式(CC JSONL / OpenClaw trajectory 的 full 与 partial 形态);
  输出写过的文件清单(strong=工具写入 / weak=重定向推断)、读过的文件、
  验证行为计数(测试/lint/构建/git 查看/grep 核验)、证据层级标注。

**证据的边界(务必记住):**

- 脚本只给"证据",不给"结论"——测试执行 7 次不等于测试通过 7 次;
- `weak` 写入证据可能混入调试输出(如 `/tmp/dbg.mjs`),必须人工复核后再用;
- **OpenClaw trajectory 分两种形态**(2026-11 dogfooding 实测发现):
  交互会话输出完整证据(full);cron/隔离会话的 trajectory 里工具调用参数被
  截断,脚本降级用 `trace.artifacts.toolMetas` 的描述层摘要(partial),
  输出会标注「证据层级: partial」——此时写入无结构化路径、验证分类基于
  meta 文本、toolMetas 自身也可能截断(实测 128 条只留 64),计数只可作线索,
  **覆盖判定必须以 git status/diff/show 证据为主**;自动化会话的改动通常
  已被提交——`git status` 为空时改用 `git log --since=<会话开始时间>` 定位
  候选提交、`git show <sha> --stat` 核对文件清单,不要误判「没有写入」;
- 没有会话记录时(如用户口述任务),跳过本步,直接用 git diff/log 做证据,
  并在报告里注明"证据来源: git 而非会话记录,无法还原验证过程"。
- **会话进行中(轨迹未落盘)**:OpenClaw 每个会话有 `<sessionId>.trajectory-path.json`
  指针文件,但 runtime 轨迹 `<sessionId>.trajectory.jsonl` 要等轮次结束才落盘——
  对"当前正在运行的轮次"审计会报 file not found(exit 3)。脚本检测到指针存在而
  runtime 缺失时会在错误信息里提示"会话仍在运行中";此时不要轮询等待,改用
  `git log --since=<会话开始时间>` + `git show <sha> --stat` 做 git 侧证据,
  或等任务真正结束后再补做会话侧审计。

### 第三步:逐条规格判定(语义审查,你来完成)

对每条规格,对照证据判定三档:

| 判定 | 标准 |
|---|---|
| ✅ 已覆盖 | 有直接证据:该规格对应的文件被写入,且有对应验证行为 |
| ⚠️ 疑似遗漏 | 找不到直接证据,且能说出具体反例场景(哪个输入/哪条路径会暴露遗漏) |
| ➖ 证据不足 | 规格可能已满足,但现有证据看不出来(如无会话记录、验证不可见) |

**禁止**:把"我没看到遗漏"写成"没有遗漏"——前者是证据不足,后者是需要论证的结论。

### 第四步:输出报告

```markdown
# 交付规格覆盖审计 — <任务名/日期>

## 规格清单(N 条;来源: 用户确认 / 默认四类)
1. [来源] <规格描述>

## 覆盖矩阵
| # | 规格 | 判定 | 证据/反例 |
|---|------|------|-----------|
| 1 | 接口兼容:xxx 的调用方不受影响 | ⚠️ 疑似遗漏 | routes/a.ts 也调用了被改函数,会话无读取记录 |

## 验证行为摘要
测试 x 次 / lint x 次 / 构建 x 次(git diff 查看 x 次)
> 命令次数 ≠ 通过次数;通过状态见会话记录或 CI

## 结论与建议行动
- [ ] <逐条给行动:补测试 / 检查调用方 / 确认某边界>
```

### 异常处理

- **会话记录与任务对不上**(路径给错/跨多轮):向用户确认用哪段记录,不要静默拼接;
- **仓库路径无法确定**:让 `--repo-root` 缺省跑一遍,输出绝对路径让用户确认归属;
- **用户只要"快速看一眼"**:跳过第一步的追问,只跑脚本+给覆盖矩阵,标注"未做规格追问"。

## 验收标准

- 规格清单在判定前生成且编号,每条标注来源;
- 每个判定给出证据或反例,不允许无依据结论;
- weak 证据全部标注"需人工复核";
- 报告区分"命令次数"与"通过状态"。

---

# English Version

## Core Positioning

You audit **one delivery**: a development task just completed by a Coding Agent
(or yourself). The single question you answer:

> **For every requirement of this task, is there evidence it was actually done?
> Were interdependent constraints (interface compatibility, state consistency,
> error handling, regression risk) dropped while the main goal got checked off?**

Design reference: CodeSpecWeave (arXiv:2610.40256) — tasks with sparse,
independent specs get completed as checklists; each item looks done in isolation
while combined they break each other.

## When to Trigger

User asks "is it done / is it covered / can we ship", with a concrete dev task
in context; delivery-report requests; distrust reviews of a recent change.

## Workflow

1. **Spec list first.** Collect numbered requirements from the user's asks,
   task description, and proactive follow-up on the four constraint classes
   (interface compat / state consistency / error handling / regression risk).
   Mark unconfirmed lists as "default four classes, user not confirmed".
2. **Extract evidence.**
   `python3 scripts/extract_spec.py <session.jsonl> [--repo-root <repo>] [--json]`
   Supports Claude Code JSONL and OpenClaw trajectory in both shapes:
   interactive sessions yield full evidence; cron/isolated sessions have tool
   calls truncated, so the script falls back to `trace.artifacts.toolMetas`
   descriptions (partial evidence, labeled in output). Returns written-file list
   (strong=tool write / weak=shell-redirect inference), read files, verify
   counts (test/lint/build/git-view/inspect). Evidence only — counts are not
   pass/fail; weak items need manual review. Under partial evidence, judge
   coverage primarily from git status/diff/show, not from counts. Automated
   sessions usually commit their changes: if `git status` is empty, locate
   the commits instead (`git log --since=<session-start>` then
   `git show <sha> --stat`) — do not report "nothing written".
3. **Judge per spec.** ✅ covered (direct evidence) / ⚠️ suspected gap (name the
   concrete counterexample scenario) / ➖ insufficient evidence. Never upgrade
   "I saw no gap" into "no gap".
4. **Report** with spec list, coverage matrix (spec × verdict × evidence),
   verify-behavior summary, and a concrete action checklist.

## Edge Cases

Mismatched session log → confirm with user, never silently merge logs.
Unknown repo root → run without `--repo-root`, ask user to confirm paths.
Quick-glance request → skip spec follow-up questions, deliver matrix with an
"unconfirmed spec list" caveat.
Session still running → OpenClaw writes the trajectory pointer
(`.trajectory-path.json`) immediately but the runtime `.trajectory.jsonl` only
after the turn completes; auditing an in-flight run exits 3 with a "still
running" hint. Don't poll — fall back to git-side evidence
(`git log --since=<session start>` + `git show <sha> --stat`) or audit after
the run finishes.
