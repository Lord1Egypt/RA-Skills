# Agent 协作协议

## 通信机制

所有 Agent 通过 `sessions_send` 进行异步通信。消息格式：

```
sessions_send → devloop-<agent-id>: "<message>"
```

## 共享文件目录（shared/）

Agent 之间的文件共享通过**各自 workspace 下的 `shared/` 目录**实现，避免跨 workspace 路径依赖。

### 写入方与目录约定

| 来源 Agent | 写入目标 Agent 的 shared/ | 目录/文件 | 触发时机 |
|-----------|--------------------------|-----------|----------|
| Product | Core Dev, Marketing, Test | `shared/prd/PRD-<name>.md` | PRD 确认后，通过 sessions_send 告知路径 |
| Core Dev | Dev, Test | `shared/design/<feature>/` | 设计文档就绪后，通过 sessions_send 告知路径 |
| Core Dev | Dev, Test | `shared/design/DESIGN-INDEX.md` | 随设计文档更新 |
| Dev | Test, Core Dev | PR 分支信息 | 通过 sessions_send 通知分支名和变更清单 |
| Test | Dev, Core Dev | 测试结果摘要 | 通过 sessions_send 通知测试报告路径 |

### 使用规则

1. **写入者负责告知** — 写入 shared/ 后，必须通过 `sessions_send` 通知接收方
2. **只读消费** — 接收方只读取 shared/ 中的文件，不修改
3. **消息传递路径** — 无法直接写入对方 shared/ 时，通过 `sessions_send` 传递文件内容
4. **路径不假设** — 不使用 `../other-agent/workspace/` 等相对路径，所有跨 Agent 文件交换通过 shared/ 或 sessions 完成

## 消息路由表

| 来源 | 事件触发 | 目标 | 消息内容模板 |
|------|----------|------|-------------|
| Product | PRD 确认 | Core Dev | `"新产品需求就绪：[名称]。请查看 PRD 进行架构设计和任务拆解。"` |
| Product | PRD 确认 | Marketing | `"新产品方向确认：[名称]。定位：[一句话]。请准备宣传方案。详见 reports/PRD-<name>.md"` |
| Core Dev | 任务分配 | Dev | `"任务：<feature> 设计文档：design/<feature>/ 分支：feat/<feature> 注意事项：<如有>"` |
| Core Dev | 测试就绪 | Test | `"PR 就绪：feat/<feature>，设计文档见 design/<feature>/"` |
| Dev | 开发完成 | Core Dev | `"✅ 任务完成：<feature> - <维度> 分支：feat/<feature> 变更文件：N 个"` |
| Dev | PR 就绪 | Test | `"PR 就绪：feat/<feature>，请 review。设计文档见 design/<feature>/"` |
| Test | 测试规格就绪 | Core Dev, Dev | `"测试规格已就绪：test-specs/<feature>/test-spec.md。发现 N 个需注意的边界条件。"` |
| Test | 审查完成 | Dev | `"PR 审查完成。结果：[通过/需修复]。代码问题 N 个，文档建议 N 条。"` |
| Test | 测试报告 | Core Dev | `"测试报告：feat/<feature> [通过/未通过]。🔴N / 🟡N / 🟢N。"` |
| Marketing | 宣传素材就绪 | Product | `"宣传素材已准备好：[项目名]。详见 reports/"` |

## 完整工作流

### 阶段一：产品发现

```
[Cron 触发] → Product Agent 执行每日热点工作流
    1. 加载 MEMORY.md 中的调研方向追踪表
    2. 读取最近 3 天的 hotspot 文件
    3. web_search 5 个维度的 AI 动态
    4. 对比历史，标注连续性 [新发现] / [持续升温 🔥] / [后续进展]
    5. 输出 memory/YYYY-MM-DD-hotspot.md
    6. 更新 MEMORY.md 调研方向追踪表
```

### 阶段二：方向讨论与 PRD

```
用户 ↔ Product Agent 多轮讨论
    ↓ 用户确认方向
Product Agent:
    1. 创建项目知识库 projects/<name>/
    2. 生成 PRD → projects/<name>/reports/PRD-<name>.md
    3. → Core Dev: "新产品需求就绪"
    4. → Marketing: "新产品方向确认"
    5. 更新 MEMORY.md 活跃项目表
```

### 阶段三：设计与调度（Core Dev）

```
Core Dev 收到 PRD:
    1. 多轮需求讨论（7 个维度，逐一确认）
    2. 生成 3~5 个设计文档 → design/<feature>/
    3. 评估复杂度 → 选择调度策略:
       - S (1-3文件): 自己做 / 单个 Dev
       - M (4-10文件): 单 Dev 分批执行
       - L (10-25文件): 多 Dev 并行
       - XL (25+文件): 多 Dev + 自己做核心
    4. 检查文件变更冲突
    5. → Dev (×N): 分配任务 + 设计文档
    6. → Test: 通知开始准备测试规格
```

### 阶段四：测试先行（Test Agent）

```
Test Agent 收到设计文档通知:
    1. 读取 PRD + 设计文档
    2. 生成测试规格文档 → test-specs/<feature>/test-spec.md
    3. → Core Dev: "测试规格已就绪"
    4. → Dev: "请在编码时参考测试规格"
    （Dev 编码时可参考测试规格中的边界条件和建议）
```

### 阶段五：编码实现（Dev Agent）

```
Dev Agent (×N) 收到任务:
    1. 读取设计文档 + 测试规格（如有）
    2. 切换到指定 feature 分支
    3. 严格按文件变更清单编码
    4. Conventional Commits 提交
    5. → Core Dev: "✅ 任务完成"
    6. → Test: "PR 就绪"
```

### 阶段六：测试与合并

```
Test Agent 收到 PR:
    1. 加载测试规格
    2. 代码审查（架构一致性、安全、代码质量）
    3. 执行测试用例
    4. 记录 Bug → bug-tracker/BUGS.md
    5. 生成审查笔记 + 测试报告
    6. → Dev: "审查结果 + 文档建议"
    7. → Core Dev: "测试报告摘要"

Core Dev 确认质量后:
    1. 合并到 main
    2. 更新 DESIGN-INDEX.md
    3. → Marketing: "功能已上线"
```

## 并行开发冲突预防

Core Dev 调度多个 Dev 并行前，**必须**检查文件变更清单交叉情况：

| 情况 | 处理方式 |
|------|----------|
| 无交叉 | 安全并行 |
| 有交叉 | 标记依赖顺序，交叉文件统一由一个 Dev 或 Core Dev 负责 |
| 大量交叉 | 降级为单 Dev 顺序执行 |

## 通用记忆策略

所有 Agent 遵循统一的记忆管理规范：

| 类型 | 路径 | 用途 | 加载时机 |
|------|------|------|----------|
| 行为定义 | `SOUL.md` / `SOUL.override.md` | 身份与行为 | 每次 session |
| 个人偏好 | `USER.md` | 用户信息 | 每次 session |
| 长期记忆 | `MEMORY.md` | 跨 session 持久知识 | 仅主 session |
| 每日笔记 | `memory/YYYY-MM-DD.md` | 当日工作记录 | 最近 2-3 天 |
| 正式文档 | `reports/` | PRD、测试报告等 | 按需 |

### Session 启动加载顺序

1. `SOUL.override.md`（如存在） > `SOUL.md`
2. `USER.md`
3. `memory/` 最近 2 天
4. `MEMORY.md`（仅主 session）
5. Agent 特定文件（如有活跃任务）
