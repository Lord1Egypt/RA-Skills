# 快速开始

## 适用场景

- 在 Claude Code 中使用 Claude-Flow 智能体
- 组建蜂群处理复杂任务
- 查看和管理智能体状态

---

## 在 Claude Code 中直接使用（最简单）

安装完成后，Claude-Flow 通过 MCP 集成到 Claude Code。**你不需要学习所有命令**，直接在对话中描述任务即可：

```
帮我审查 src/auth/ 目录的代码安全性

帮我为 payments 模块写完整的测试套件

重构 database.ts，提高性能并改善错误处理
```

Claude-Flow 会自动路由到合适的专业智能体（security、tester、refactor 等）。

---

## 查看可用智能体

```bash
# 列出所有可用智能体
npx ruflo@latest agent list

# 查看特定智能体详情
npx ruflo@latest agent info coder
npx ruflo@latest agent info security
```

常用智能体类型：

| 智能体 | 职责 |
|--------|------|
| `coder` | 代码编写和实现 |
| `tester` | 测试编写和执行 |
| `reviewer` | 代码审查 |
| `architect` | 技术架构设计 |
| `security` | 安全扫描和审计 |
| `documenter` | 文档生成 |
| `optimizer` | 性能优化 |
| `researcher` | 技术调研 |

---

## 手动启动单个智能体

```bash
# 启动 coder 智能体处理特定任务
npx ruflo@latest agent spawn coder \
  --task "实现用户认证模块，包含 JWT 刷新机制"

# 启动 security 智能体审计代码
npx ruflo@latest agent spawn security \
  --task "审计 src/api/ 目录的安全性" \
  --files "src/api/"
```

---

## 启动蜂群（多智能体协作）

```bash
# 层级蜂群（Queen 协调 Worker）
npx ruflo@latest swarm start \
  --topology hierarchical \
  --agents coder,tester,reviewer,security \
  --task "实现并测试用户注册和登录 API"

# 网状蜂群（P2P 协作，适合研究任务）
npx ruflo@latest swarm start \
  --topology mesh \
  --agents researcher,architect,documenter \
  --task "设计微服务架构方案"

# 查看蜂群状态
npx ruflo@latest swarm status
```

---

## 常见任务模式

### 全链路代码实现

```bash
# 让多个智能体协作完成从设计到测试的完整流程
npx ruflo@latest swarm start \
  --topology hierarchical \
  --agents architect,coder,tester,reviewer \
  --task "设计并实现一个 RESTful API 用于用户管理（CRUD），包含完整测试"
```

### 代码质量审查

```bash
# 并行运行审查、安全、测试三个智能体
npx ruflo@latest swarm start \
  --topology mesh \
  --agents reviewer,security,tester \
  --task "全面审查 src/ 目录的代码质量、安全性和测试覆盖率"
```

### 紧急 Bug 修复

```bash
# 单个 coder 智能体快速处理
npx ruflo@latest agent spawn coder \
  --task "修复 payment.ts 中的竞态条件 bug，错误出现在 processPayment 函数"
```

---

## 查看学习记忆

Claude-Flow 会记住成功的任务模式，可以查询：

```bash
# 查看记忆系统状态
npx ruflo@latest hooks intelligence --status

# 搜索历史成功模式
npx ruflo@latest memory search "authentication"
```

---

## MCP 工具列表

在 Claude Code 中，Claude-Flow 暴露 310+ MCP 工具：

```
# 在 Claude Code 中查询可用工具
/mcp list

# 常用工具（自动调用，无需手动触发）
claude_flow_agent_spawn   — 启动智能体
claude_flow_swarm_start   — 启动蜂群
claude_flow_memory_search — 搜索历史模式
claude_flow_task_status   — 查看任务状态
```

---

## 完成确认检查清单

- [ ] Claude Code 中 Claude-Flow MCP 工具可用（`/mcp list` 可见）
- [ ] `npx ruflo@latest agent list` 显示可用智能体
- [ ] 简单任务通过对话自动路由到合适智能体
- [ ] 蜂群模式成功启动并完成任务

---

## 下一步

- [高级用法](03-advanced-usage.md) — 自定义智能体、多模型切换、向量记忆管理
