---
name: engineering-mode
description: "工程模式：写入 Agent 系统指令级别的工程肌肉记忆。触发后强制 UNDERSTAND→DECOMPOSE→SAFETY→EXECUTE→VERIFY→RECOVER 六阶段状态机。使用场景：(1) 用户要求写/改/重构代码 (2) 涉及 edit/write/exec 编程操作 (3) 用户说'工程模式''engineering mode'。不用于：纯聊天、查资料、系统管理、甩给 CC/Codex 子代理的任务。"
---

# Engineering Mode

六阶段状态机，改代码前必须走完。

## 状态机概览

```
UNDERSTAND → DECOMPOSE → SAFETY → EXECUTE → VERIFY ──成功→ 下一步
                                              │
                                             失败
                                              │
                                          RECOVER ──成功→ 继续循环
                                              │
                                             失败 → 回退→报告
```

## 阶段定义

### 1. UNDERSTAND — 改前必读

**目标**：确认自己真的理解改动范围。

**强制动作**：
- `read` 目标文件，至少覆盖改动位置周围 50 行
- 追踪调用链：谁调用它？它调用谁？（grep / read 相邻文件）
- 输出简短理解小结（3-5 行），确认后进入下一步
- 理解不足 → 继续读，不进入 DECOMPOSE

**检查清单**：需要时读 `references/pre-edit-checklist.md`

### 2. DECOMPOSE — 任务拆解

**目标**：把复杂任务拆成独立可验证的原子步骤。

**强制动作**：
- 每步 ≤ 15 分钟工作量
- 每步有明确成功标准（"跑过某个测试" / "编译通过" / "输出某段日志"）
- 使用 `update_plan` 写入步骤列表
- 拆不出来 → 说明理解不够，回 UNDERSTAND

**注意**：
- 简单任务（1-2 文件、单函数改动）可跳过 DECOMPOSE，直接到 SAFETY
- 3+ 文件或多步骤依赖 → 必须拆

### 3. SAFETY — 安全隔离

**目标**：建立可回退的安全点，不污染用户工作区。

**强制动作（分支隔离）**：
```bash
# 记录原始分支名
ORIGINAL_BRANCH=$(git branch --show-current)

# 从当前分支切出临时工作分支
git checkout -b eng-mode-$(date +%s)
```

**禁止**：
- `git add -A`（会夹带脏数据）
- `git stash`（冲突风险）
- 跳过 SAFETY 直接改

### 4. EXECUTE — 最小改动

**目标**：一个逻辑变更，最小修改集。

**强制动作**：
- 使用 `edit`（首选）或 `write` 做精确修改
- 一次只做一个逻辑变更
- 不改无关代码（格式化、重构除非是本步目标）

**禁止**：
- 边改边加新功能
- 顺带重构无关代码
- 一次改多个不相关的文件

### 5. VERIFY — 改后必验

**目标**：确认改动没有破坏东西。

**三级验证**：

| 级别 | 触发 | 操作 | 超时 |
|---|---|---|---|
| **L1 Lint** | 每次编辑后必做 | `eslint <file>` / `flake8 <file>` / `shellcheck <file>` | 10s |
| **L2 单元** | 改动涉及逻辑变化 | 只跑相关测试文件 | 30s |
| **L3 全量** | 所有步骤完成后 | `npm run build` / `pytest` / `cargo build` | 120s |

超时视为失败。详细策略见 `references/validate-strategies.md`

### 6. RECOVER — 失败恢复

**目标**：修一次，修不好就回退汇报。

**强制动作**：
1. 分析错误信息（读 stderr/stdout）
2. 检查改动：`git diff`
3. **修一次**——仅做代码文本修改，不创建新 checkpoint
4. 重新 VERIFY

**状态机互斥铁律**：
- RECOVER 阶段 **绝对禁止** 触发 SAFETY（创建 checkpoint / 切分支）
- RECOVER 阶段 **绝对禁止** 触发 DECOMPOSE（重新拆任务）
- RECOVER 阶段 **只能做**：读错误 → 改代码 → 重验证
- 修复成功 → 回到循环，正常进入下一步的 SAFETY

**回退**（修复失败）：
```bash
# 动态获取最近 checkpoint（不依赖环境变量传递）
LATEST_CHECKPOINT=$(git log --grep="^checkpoint:" -1 --format=%H)
git reset --hard $LATEST_CHECKPOINT

# 或：直接切回原分支，丢弃临时分支
git checkout $ORIGINAL_BRANCH
git branch -D eng-mode-*
```

回退后：分析失败原因 → 报告用户 → 等待指示

详细恢复模式见 `references/error-recovery.md`

---

## 状态机互斥规则

| 当前阶段 | 允许的操作 | 禁止的操作 |
|---|---|---|
| UNDERSTAND | read, grep, 分析 | edit, write, git commit |
| DECOMPOSE | update_plan, 分析 | edit, write, git commit |
| SAFETY | git checkout -b, git commit | edit, write |
| EXECUTE | edit, write | git commit, git checkout |
| VERIFY | exec (lint/build/test) | edit, write, git commit |
| RECOVER | read error, edit, exec verify | git commit, git checkout, update_plan, DECOMPOSE |

**进入下一阶段前必须确认当前阶段完成。**

---

## Git 提交规范

**仅在 SAFETY 阶段做 checkpoint commit**，格式：
```
checkpoint: <简短描述>
```

EXECUTE 后的增量提交（可选，在 VERIFY 通过后执行）：
```
<type>: <简短描述>
```
type: `feat` / `fix` / `refactor` / `chore` / `test`

详见 `references/commit-discipline.md`

---

## Reference 加载条件

按需加载，不一次性全吞：

| Reference | 何时加载 |
|---|---|
| `references/pre-edit-checklist.md` | UNDERSTAND 阶段，项目结构复杂或改动跨多文件 |
| `references/validate-strategies.md` | VERIFY 阶段，需要确认特定语言的验证命令 |
| `references/error-recovery.md` | RECOVER 阶段触发时 |
| `references/commit-discipline.md` | 需要提交或用户询问提交规范时 |

---

## 不适用场景（跳过工程模式）

以下情况直接操作，不走六阶段：
- 纯聊天、回答问题、查资料
- 系统管理（改配置、重启服务、查进程）
- 甩给 CC/Codex 的任务（子代理自行管理）
- 单文件单行的简单修改（如改一个常量值、改一行注释）
- 用户明确说"不用工程模式"

判断标准：涉及 2+ 文件 或 逻辑改动 → 触发工程模式。
