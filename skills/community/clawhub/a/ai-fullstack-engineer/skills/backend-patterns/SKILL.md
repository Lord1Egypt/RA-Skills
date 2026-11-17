---
name: backend-patterns
description: 后端架构模式：Node.js/Express 最佳实践、数据库优化、安全加固、错误处理
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/backend-patterns/SKILL.md
  url: https://skills.sh/affaan-m/everything-claude-code/backend-patterns
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 架构
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - backend
  - nodejs
  - express
  - architecture
  - security
---

# Backend Patterns — 后端架构模式

> 后端开发不是只有「能跑就行」。用经过验证的架构模式构建可维护、高性能、安全的服务端应用。

## 能力

- **架构分层**：Controller-Service-Repository 模式、依赖注入
- **Node.js/Express 最佳实践**：中间件链、错误处理、异步模式
- **数据库优化**：连接池、N+1 查询消除、慢查询分析
- **安全加固**：输入验证、SQL 注入防护、CORS 配置、Rate Limiting
- **性能优化**：缓存策略、分页优化、响应压缩

## 使用方式

在 Claude Code 中使用 `/backend-patterns` 调用。

```
/backend-patterns 审查我的 Express 应用架构
/backend-patterns 优化这个 N+1 查询问题
/backend-patterns 帮我添加 Rate Limiting 和 CORS 配置
```

## 工作流

1. **架构审查** — 检查项目分层、模块边界、依赖方向
2. **问题定位** — 识别性能瓶颈、安全隐患、代码坏味
3. **模式应用** — 选择合适架构模式并实现
4. **安全加固** — 逐项检查 OWASP Top 10，添加防护
5. **验证** — 压测对比、安全检查、代码质量评估

## 关键模式

| 模式 | 适用场景 | 收益 |
|------|---------|------|
| Repository Pattern | 数据访问抽象 | 替换 ORM/数据库不影响业务逻辑 |
| Middleware Chain | 请求处理管线 | 认证/日志/限流可插拔 |
| CQRS | 读写分离 | 读优化和写优化互不干扰 |
| Circuit Breaker | 外部服务调用 | 防止级联故障 |
| Idempotency Key | 支付/订单接口 | 防止重复操作 |

## 适用场景

- 后端服务从「能跑」到「能维护」的升级
- Node.js 项目需要架构重构
- 新项目启动时的技术栈选型
- 性能瓶颈排查和优化

## 限制

- 主要覆盖 Node.js/Express 生态（FastAPI 见 fastapi-python）
- 不覆盖微服务治理（服务发现、分布式追踪）
- 缓存策略聚焦应用层，不涉及 Redis/Memcached 集群运维

## 相关参考（Playbook）

本子技能落地"后端架构模式"，跨栈方法论见下列 `references/`（按需读取）：

- 后端深度 playbook（分层 / 中间件 / 安全 / 限流 / 幂等 / 迁移锁表）：[references/backend-playbook.md](../../references/backend-playbook.md)
- AI-native 全栈工作流（并联交付与联调）：[references/fullstack-workflow.md](../../references/fullstack-workflow.md)