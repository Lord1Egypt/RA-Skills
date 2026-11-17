---
name: debugging
description: Use when encountering any bug, test failure, or unexpected behavior, BEFORE proposing fixes. Enforces a four-phase root-cause investigation (root cause investigation, pattern analysis, hypothesis testing, implementation) before any code change. Iron law: no fixes without root cause investigation first.
license: MIT
version: 1.0.0
agent_created: true
allowed-tools: Read Grep Glob Bash
---

# Systematic Debugging / 系统化调试

A four-phase discipline for finding the root cause of any bug before attempting fixes. / 在尝试修复前，用四阶段纪律找到任何 Bug 的根因。

## The Iron Law / 铁律

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.
没有根因调查，就不能修复。
```

If you haven't completed Phase 1, you cannot propose fixes. Symptom fixes are failure. / 如果没完成 Phase 1，就不能提修复。症状修复 = 失败。

**Violating the letter of this process is violating the spirit of debugging.** / **违反字面也违反精神**。

## When to use / 何时使用

Use for ANY technical issue: / 任何技术问题都用：

- Test failures / 测试失败
- Bugs in production / 生产 Bug
- Unexpected behavior / 意外行为
- Performance problems / 性能问题
- Build failures / 构建失败
- Integration issues / 集成问题
- User says "bug", "broken", "not working", "why", "出错", "挂了", "失败", "有问题" / 用户说 "bug"、"broken"、"not working"、"why"、"出错"、"挂了"、"失败"、"有问题"

**Use this ESPECIALLY when** / **尤其在这些情况**：
- Under time pressure (emergencies make guessing tempting) / 时间压力（紧急让人想猜）
- "Just one quick fix" seems obvious / 「就一个小修复」看起来明显
- You've already tried multiple fixes / 已试过多个修复
- Previous fix didn't work / 上次修复没生效
- You don't fully understand the issue / 没完全理解问题

**Don't skip when** / **不要跳过**：
- Issue seems simple (simple bugs have root causes too) / 问题看起来简单（简单 Bug 也有根因）
- You're in a hurry (rushing guarantees rework) / 你赶时间（赶时间保证返工）
- Manager wants it fixed NOW (systematic is faster than thrashing) / 经理要立刻修（系统化比瞎试更快）

## The Four Phases / 四阶段

You MUST complete each phase before proceeding to the next. / 必须按顺序完成每个阶段。

### Phase 1: Root Cause Investigation / 根因调查

**BEFORE attempting ANY fix** / **尝试任何修复之前**：

#### 1.1 Read error messages carefully / 仔细读错误信息

- Don't skip past errors or warnings / 不要跳过错误或警告
- They often contain the exact solution / 它们常常包含精确解法
- Read stack traces completely / 完整读 stack trace
- Note line numbers, file paths, error codes / 注意行号、文件路径、错误码

#### 1.2 Reproduce consistently / 稳定复现

- Can you trigger it reliably? / 能稳定触发吗？
- What are the exact steps? / 精确步骤是什么？
- Does it happen every time? / 每次都发生吗？
- If not reproducible → gather more data, don't guess / 如果不能复现 → 收集更多数据，别猜

#### 1.3 Check recent changes / 检查最近变更

- What changed that could cause this? / 什么变更可能引发？
- `git log --since="2 weeks ago" --oneline` / git log
- `git diff HEAD~10 -- path/to/file` / git diff
- New dependencies, config changes / 新依赖、配置变更
- Environmental differences / 环境差异

#### 1.4 Gather evidence in multi-component systems / 多组件系统收集证据

**WHEN system has multiple components** (CI → build → signing, API → service → database) / **当系统有多组件**：

**BEFORE proposing fixes, add diagnostic instrumentation** / **提修复之前，加诊断埋点**：

```
For EACH component boundary:
  - Log what data enters component
  - Log what data exits component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence showing WHERE it breaks
THEN analyze evidence to identify failing component
THEN investigate that specific component
```

**Example (CI → build → signing pipeline)** / **示例（CI → 构建 → 签名流水线）**：

```bash
# Layer 1: Workflow / 工作流
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script / 构建脚本
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"

# Layer 3a: macOS keychain / macOS 钥匙串
echo "=== macOS keychain state: ==="
security list-keychains
security find-identity -v

# Layer 3b: Windows certificate store / Windows 证书存储
echo "=== Windows certificate store: ==="
certutil -store My

# Layer 3c: Linux GPG / Linux GPG
echo "=== Linux GPG keys: ==="
gpg --list-secret-keys

# Layer 4: Actual signing / 实际签名
codesign --sign "$IDENTITY" --verbose=4 "$APP"           # macOS
signtool sign /fd SHA256 /a "$APP.exe"                    # Windows
gpg --detach-sign --armor "$APP.tar.gz"                  # Linux
```

This reveals: which layer fails. / 这揭示：哪一层挂了。

#### 1.5 Trace data flow / 追踪数据流

**WHEN error is deep in call stack** / **当错误在调用栈深处**：

Backward trace technique: / 反向追踪技术：
- Where does bad value originate? / 错误值从何而来？
- What called this with bad value? / 谁用错误值调用了它？
- Keep tracing up until you find the source / 继续往上追直到找到源
- Fix at source, not at symptom / 在源头修，不要在症状

### Phase 2: Pattern Analysis / 模式分析

**Find the pattern before fixing** / **修复前先找模式**：

#### 2.1 Find working examples / 找到工作中的例子

- Locate similar working code in same codebase / 在同一代码库找相似工作中代码
- What works that's similar to what's broken? / 什么工作中代码和坏掉的相似？

#### 2.2 Compare against references / 与参考实现对比

- If implementing pattern, read reference implementation COMPLETELY / 如果实现模式，完整读参考实现
- Don't skim — read every line / 不要略读——每行都读
- Understand the pattern fully before applying / 完整理解模式再应用

#### 2.3 Identify differences / 识别差异

- What's different between working and broken? / 工作中 vs坏的不同
- List every difference, however small / 列出每个差异，无论多小
- Don't assume "that can't matter" / 不要假设「那不重要」

#### 2.4 Understand dependencies / 理解依赖

- What other components does this need? / 需要哪些其他组件？
- What settings, config, environment? / 什么设置、配置、环境？
- What assumptions does it make? / 做了什么假设？

### Phase 3: Hypothesis and Testing / 假设与测试

**Scientific method** / **科学方法**：

#### 3.1 Form single hypothesis / 形成单一假设

- State clearly: "I think X is the root cause because Y" / 清晰表述：「我认为 X 是根因，因为 Y」
- Write it down / 写下来
- Be specific, not vague / 具体，不要模糊

#### 3.2 Test minimally / 最小化测试

- Make the SMALLEST possible change to test hypothesis / 做最小变更测假设
- One variable at a time / 一次一个变量
- Don't fix multiple things at once / 不要一次修多个

#### 3.3 Verify before continuing / 继续前验证

- Did it work? Yes → Phase 4 / 生效？→ Phase 4
- Didn't work? Form NEW hypothesis / 没生效？形成新假设
- DON'T add more fixes on top / 不要叠加加更多修复

#### 3.4 When you don't know / 当你不知道

- Say "I don't understand X" / 说「我不理解 X」
- Don't pretend to know / 不要装懂
- Ask for help / 求助
- Research more / 多研究

### Phase 4: Implementation / 实施

**Fix the root cause, not the symptom** / **修根因，不修症状**：

#### 4.1 Create failing test case / 创建失败测试用例

- Simplest possible reproduction / 最简复现
- Automated test if possible / 可能就用自动化测试
- One-off test script if no framework / 没框架就一次性脚本
- MUST have before fixing / 必须有再修

#### 4.2 Implement single fix / 实施单一修复

- Address the root cause identified / 针对已识别根因
- ONE change at a time / 一次一个变更
- No "while I'm here" improvements / 不要「顺便」改进
- No bundled refactoring / 不要捆绑重构

#### 4.3 Verify fix / 验证修复

- Test passes now? / 测试过了？
- No other tests broken? / 其他测试没坏？
- Issue actually resolved? / 问题真解决了？

#### 4.4 If fix doesn't work / 如果修复不生效

- STOP / 停
- Count: how many fixes have you tried? / 数：试过几个修复？
- If `< 3`: Return to Phase 1, re-analyze with new information / 回到 Phase 1，用新信息重新分析
- **If `≥ 3`: STOP and question the architecture** / **问架构问题**
- DON'T attempt Fix #4 without architectural discussion / 不要在架构讨论前做第 4 次修复

#### 4.5 If 3+ fixes failed: Question architecture / 3+ 修复失败：问架构

**Pattern indicating architectural problem** / **架构问题的信号**：
- Each fix reveals new shared state/coupling/problem in different place / 每次修复在不同地方暴露新共享状态/耦合/问题
- Fixes require "massive refactoring" to implement / 修复需要「巨大重构」才能实施
- Each fix creates new symptoms elsewhere / 每次修复在别处产生新症状

**STOP and question fundamentals** / **停下来问根本问题**：
- Is this pattern fundamentally sound? / 这模式根本合理吗？
- Are we "sticking with it through sheer inertia"? / 我们是「凭惯性坚持」吗？
- Should we refactor architecture vs. continue fixing symptoms? / 应该重构架构还是继续修症状？

**Discuss with your human partner before attempting more fixes.** / **继续修前与人类伙伴讨论**。

This is NOT a failed hypothesis — this is a wrong architecture. / 这不是失败的假设——是错的架构。

## Quick Reference / 速查表

| Phase | Key Activities / 关键活动 | Success Criteria / 成功标准 |
|---|---|---|
| **1. Root Cause** / 根因 | Read errors, reproduce, check changes, gather evidence / 读错误、复现、检查变更、收集证据 | Understand WHAT and WHY / 理解是什么、为什么 |
| **2. Pattern** / 模式 | Find working examples, compare / 找工作中示例、对比 | Identify differences / 识别差异 |
| **3. Hypothesis** / 假设 | Form theory, test minimally / 形成理论、最小测试 | Confirmed or new hypothesis / 确认或新假设 |
| **4. Implementation** / 实施 | Create test, fix, verify / 建测试、修、验证 | Bug resolved, tests pass / Bug 解决、测试过 |

## Red Flags — STOP and follow process / 红旗 — 停下走流程

If you catch yourself thinking / 如果你发现自己在想：
- "Quick fix for now, investigate later" / 「现在先快速修，之后查」
- "Just try changing X and see if it works" / 「改 X 试试」
- "Add multiple changes, run tests" / 「加多个变更，跑测试」
- "Skip the test, I'll manually verify" / 「跳过测试，我手动验证」
- "It's probably X, let me fix that" / 「可能是 X，修一下」
- "I don't fully understand but this might work" / 「不完全懂但可能行」
- "Pattern says X but I'll adapt differently" / 「模式说 X 但我变通」
- "Here are the main problems: [lists fixes without investigation]" / 「主要问题是：[列修复没调查]」
- Proposing solutions before tracing data flow / 追数据流前提方案
- **"One more fix attempt" (when already tried 2+)** / **「再试一次」（已试过 2+）**
- **Each fix reveals new problem in different place** / **每次修复在不同地方暴露新问题**

→ **STOP. Return to Phase 1.** / **停止。回到 Phase 1。**

**If 3+ fixes failed: Question the architecture** (Phase 4.5) / **3+ 修复失败：问架构**

## Signals you're doing it wrong / 走偏的信号

Watch for these redirections from your human partner: / 注意人类伙伴这些反向信号：

- "Is that not happening?" — You assumed without verifying / 「那没发生？」——你假设了没验证
- "Will it show us...?" — You should have added evidence gathering / 「能展示……？」——你应该加证据收集
- "Stop guessing" — You're proposing fixes without understanding / 「别猜」——你提修复没理解
- "Ultra-think this" — Question fundamentals, not just symptoms / 「深度想」——问根本，不只症状
- "We're stuck?" (frustrated) — Your approach isn't working / 「卡住了？」（烦躁）——你的方法没在用

**When you see these: STOP. Return to Phase 1.** / **看到这些：停。回到 Phase 1。**

## Common Rationalizations / 常见合理化借口

| Excuse / 借口 | Reality / 真相 |
|---|---|
| "Issue is simple, don't need process" / 「简单问题，不要流程」 | Simple issues have root causes too. Process is fast for simple bugs. / 简单问题也有根因。流程对简单 Bug 很快。 |
| "Emergency, no time for process" / 「紧急，没时间走流程」 | Systematic debugging is FASTER than guess-and-check thrashing. / 系统化调试比瞎试返工更快。 |
| "Just try this first, then investigate" / 「先试试，之后查」 | First fix sets the pattern. Do it right from the start. / 第一次修复定模式。一开始就做对。 |
| "I'll write test after confirming fix works" / 「确认修好再写测试」 | Untested fixes don't stick. Test first proves it. / 没测的修复站不住。测试先证。 |
| "Multiple fixes at once saves time" / 「一次修多个省时间」 | Can't isolate what worked. Causes new bugs. / 不能隔离哪个生效。会引入新 Bug。 |
| "Reference too long, I'll adapt the pattern" / 「参考太长，我变通」 | Partial understanding guarantees bugs. Read it completely. / 部分理解保证有 Bug。完整读。 |
| "I see the problem, let me fix it" / 「我看到问题，修」 | Seeing symptoms ≠ understanding root cause. / 看症状 ≠ 理解根因。 |
| "One more fix attempt" (after 2+ failures) / 「再试一次」（2+ 失败后） | 3+ failures = architectural problem. Question pattern, don't fix again. / 3+ 失败 = 架构问题。问模式，不要再修。 |

## When process reveals "no root cause" / 当流程揭示「无根因」

If systematic investigation reveals issue is truly environmental, timing-dependent, or external: / 如果系统化调查发现真是环境、时序、或外部问题：

1. You've completed the process / 你完成了流程
2. Document what you investigated / 记录你调查的内容
3. Implement appropriate handling (retry, timeout, error message) / 实施合适处理（重试、超时、错误消息）
4. Add monitoring/logging for future investigation / 加监控/日志便于将来调查

**But:** 95% of "no root cause" cases are incomplete investigation. / **但是**：95% 的「无根因」案例是调查不彻底。

## Supporting Techniques (inlined) / 支持技术（已内联）

These are part of systematic debugging. Read the inline guidance below before reaching for them. / 这些是系统化调试的一部分。下面的内联指南在使用前先读。

### Root cause tracing / 根因追踪

When error is deep in call stack: / 当错误在调用栈深处：

1. Start at the error site / 从错误点开始
2. Identify the bad value / 识别错误值
3. Walk up the call stack: who passed this value? / 沿调用栈往上：谁传的这个值？
4. Continue until you find where the value originated / 继续直到找到值起源
5. Fix at origin, not at error site / 在起源修，不在错误点

### Defense in depth / 纵深防御

After finding root cause, add validation at multiple layers: / 找到根因后，在多层加验证：

- Input boundary validation / 输入边界验证
- Pre-condition assertions / 前置条件断言
- Internal invariant checks / 内部不变性检查
- Output boundary validation / 输出边界验证

One layer catches what another misses. / 一层抓另一层漏的。

### Condition-based waiting / 条件等待

Replace arbitrary timeouts with condition polling: / 用条件轮询替换任意超时：

```js
// BAD: arbitrary timeout / 任意超时
await sleep(5000)

// GOOD: poll for condition / 轮询条件
while (!(await checkReady())) {
  await sleep(100)
}
```

## Output expectations / 输出期望

When you finish debugging, you have: / 完成调试后，你拥有：

- ✅ Root cause identified and stated clearly / 根因识别并清晰表述
- ✅ Failing test that reproduces it / 复现它的失败测试
- ✅ Single fix at root cause / 根因处的单一修复
- ✅ Test now passes, no other tests broke / 测试现在过，其他测试没坏
- ✅ Optional: monitoring/logging if "no root cause" / 可选：监控/日志（如果「无根因」）

## Cross-platform notes / 跨平台说明

Debugging commands differ per OS. The systematic process is identical; the diagnostic commands adapt. / 调试命令因 OS 而异。系统化过程相同；诊断命令适配。

| OS | File listing | Process list | Logs | Network |
|---|---|---|---|---|
| **macOS** | `ls`, `find` | `ps aux`, `lsof -i` | `log show --last 5m` | `lsof -iTCP -sTCP:LISTEN` |
| **Linux** | `ls`, `find` | `ps aux`, `ss -tlnp` | `journalctl -u <svc> --since "5m ago"` | `ss -tlnp` |
| **Windows** | `dir`, `Get-ChildItem` | `Get-Process`, `tasklist` | `Get-EventLog -LogName Application -Newest 50` | `netstat -ano` |

Pick the row for your OS. / 选你 OS 那一行。

## Compatibility notes / 兼容性说明

- **No project requirement**: works in any repo, single-file script, or no-repo directory. / 无项目要求：任何仓库、单文件脚本或无仓库目录都用得上。
- **No tool dependency**: process uses whatever tools you have (git, debugger, IDE, print statements). / 无工具依赖。
- **No API cost**: methodology, not LLM-bound. / 无 API 成本：方法论，不绑 LLM。