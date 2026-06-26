---
name: codex-cli-guardian
description: Codex CLI 会话守护者。管理 API Key、任务执行与结果摘要。提供后台模式运行、API Key 验证、会话锁定与PID追踪等功能。
---

# Codex-CLI-Guardian

> Codex CLI 会话守护者 — 管理 API Key、任务执行与结果摘要

---

## 技能职责

1. **API Key 管理** — 首次引导输入并验证，验证通过才写入（init-setup）；codex-call 直接读取 credentials.env，不重复验证
2. **任务执行** — 后台模式运行 Codex，主人可继续聊天
3. **结果摘要** — 使用 `-o` 输出文件，只保存 Codex 完成语
4. **并发控制** — PID 锁防止多任务同时执行
5. **状态追踪** — 实时记录任务状态，支持超时警告
6. **Worker 编排** — 提供标准化 Worker 模板和编排模式

**不是**：coding-agent 的替代品，是其底层基础设施。

---

## 调用方式（重要）

**必须使用 `background:true`**，否则主 agent 会等待 Codex 执行完毕才响应：

```bash
exec:
  command: bash bin/codex-call.sh "任务描述"
  background: true   # ← 必须加，默认行为
```

不加 `background:true` → 主 agent 阻塞 → 无法中途回复主人
加 `background:true` → 主 agent 立即返回 → 可以继续聊天

**标准调用方式**：
```bash
exec background:true command:"bash bin/codex-call.sh \"任务描述\""
```

**进度/状态查询（不走 exec，直接读文件）**：
```bash
# 读 state/current-task.json
# 读 state/tasks/ 最新任务历史
```
原因：进度查询走 exec 反而会产生新的 exec，形成嵌套，效率低。

---

## 多步骤任务编排

当主人描述的任务涉及多个阶段时，会自动加上步骤指引，引导 Codex 依次执行：

```
请按以下步骤执行：
1. 【侦察】先摸清现状和关键文件
2. 【评审】分析风险和可行方案
3. 【实施】执行核心工作
4. 【验证】确认结果正确

每步完成后简报。
```

常用步骤组合：
| 场景 | 步骤组合 |
|------|---------|
| 代码重构 | 侦察 → 评审 → 实施 → 验证 |
| 复杂开发 | 需求确认 → 搭建框架 → 核心功能 → 测试 |
| Bug 修复 | 复现 → 定位 → 修复 → 验证 |
| 批量修改 | 扫描 → 分析 → 执行 → 确认 |

---

## 触发场景

### 两层确认机制

**第一层：触发关键词**

主人说以下内容时，进入「意图确认」流程：

| 关键词 | 触发场景 |
|--------|---------|
| `写代码` | 「帮我写代码」 |
| `写个` | 「帮我写个爬虫」「写个脚本」 |
| `写一个` | 「写一个计算器」 |
| `开发` | 「帮我开发一个 API」 |
| `重构` | 「帮我重构这个模块」 |
| `Codex` | 「用 Codex 写」「用 Codex 跑」 |
| `脚本` | 「写个脚本处理数据」 |
| `程序` | 「写个程序」 |
| `/codex-guardian` | 管理命令前缀 |

**注意**：单独说「代码」「谢谢」等词不触发。

---

**第二层：确认流程**

检测到关键词后，回复确认：

```
🔍 检测到代码开发意图，要用 Codex 执行吗？

任务：帮我写一个爬虫

→ 直接回「是」/「好」/「执行」 → 执行
→ 回「不用」/「取消」 → 取消
```

主人确认后，执行 codex-call.sh，后台运行。

---

**触发短语（agent 识别后执行，无需确认）**

| 触发短语 | 执行动作 |
|----------|----------|
| `任务进度` | 读取 state/current-task.json 展示状态 |
| `终止任务` | 调用 session.sh kill |
| `任务历史` | 调用 session.sh list |
| `/codex-guardian status` | 调用 session.sh status |
| `/codex-guardian reset` | 调用 session.sh reset |

---

## 执行步骤

```
1. 主人发起任务
      ↓
2. codex-call.sh 加载 Key（文件不存在 → 触发 init-setup）
      ↓
3. 检查 PID 锁 → 被占用 → 拒绝
      ↓（空闲）
4. 生成 task_id（如 20260404-001）
      ↓
5. 写入 state/current-task.json（status: running）
      ↓
6. codex-call.sh 启动后台子进程执行 codex exec
      ↓
7. codex-call.sh 主进程立即返回 task_id（不阻塞）
      ↓
8. Codex 执行中（主人可继续聊其他事）
      ↓
9. Codex 完成 → 写 state/tasks/<task_id>.json（摘要）
      ↓
10. 通知主人任务完成
```

**超时策略**：不自动终止。超时后继续运行，主人可随时说「终止任务」。

---

## PID 锁逻辑

```
进入 → 检查 lock 文件 → PID 存在且进程存活 → 拒绝
                              → PID 不存在或进程已死 → 清理 → 继续
```

---

## 命令接口

### codex-call.sh

```bash
bash bin/codex-call.sh "<任务描述>"
```

- 返回：`{"task_id":"...","pid":...}`
- 始终后台执行，不阻塞

### session.sh

```bash
bash bin/session.sh status   # 健康检查（含超时警告）
bash bin/session.sh list     # 列出最近任务
bash bin/session.sh kill     # 终止当前任务
bash bin/session.sh reset    # 重置状态（不清历史）
```

### init-setup.sh

```bash
bash scripts/init-setup.sh        # 交互式设置向导
bash scripts/init-setup.sh check # 仅检查状态
```

- 首次引导：输入 Key → 验证通过才写入
- 已有 Key：询问是否重设

---

## 输出标准

### 任务完成

```
🚀 已启动任务 [20260404-001]：帮我写个爬虫
（后台执行中，你可以继续聊其他事情）

✅ 任务 [20260404-001] 完成：
spider.py 已创建完成，包含以下功能：
- 支持多页面爬取
- 自动去重
```

### 任务失败

```
❌ 任务 [20260404-001] 失败：
原因：API Key 无效或已过期
```

### 忙碌拒绝

```
⚠️ Codex 忙碌中，请稍后再试。
```

### 健康检查

```
=== Codex Guardian 状态 ===
任务状态   : idle
累计任务   : 5
最后使用   : 3 分钟前
当前任务   : 无
```

### 超时警告（>=25 分钟）

```
运行时长   : 25 分钟 / 30 分钟 ⚠️ 即将超时
如需终止任务，请说：「终止任务」
```

---

## 文件清单

| 路径 | 用途 |
|------|------|
| `credentials.env` | API Key（skill 目录内，600 权限） |
| `state/current-task.json` | 运行中任务 |
| `state/tasks/*.json` | 历史任务摘要 |
| `state/codex.lock` | PID 锁文件 |

---

## 安全原则

1. API Key 不落日志
2. `credentials.env` 权限 600
3. credentials.env 已被 .gitignore 忽略，不会被 git 提交
4. init-setup 验证 Key 通过才写入，失败不保存（codex-call 不验证 Key）

---

## 参见

- [REFERENCES.md](./REFERENCES.md) — 完整格式标准
- [CLI.md](./CLI.md) — Codex CLI 正确用法
- [workers/](./workers/) — Worker 模板
  - `standard-preamble.md` — Worker 前言
  - `reviewer.md` — 评审者
  - `researcher.md` — 研究者
  - `implementer.md` — 实现者
  - `verifier.md` — 验证者
  - `scout.md` — 侦察者
  - `context-pack.md` — Context Pack
  - `patterns.md` — 编排模式
