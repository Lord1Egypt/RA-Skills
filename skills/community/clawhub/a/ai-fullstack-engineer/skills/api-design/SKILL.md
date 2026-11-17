---
name: api-design
description: API 与接口设计：REST/GraphQL 稳定性策略、版本管理、错误处理、契约测试
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/api-design/SKILL.md
  url: https://skills.sh/addyosmani/agent-skills/api-and-interface-design
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 设计
  platform: API
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - api
  - rest
  - graphql
  - interface-design
  - versioning
---

# API Design — 接口设计

> API 改不动、前端不敢升级、每次发布都是灾难——根本原因是接口设计阶段没有定好契约。本技能帮你建立稳定的 API 设计流程。

## 能力

- **API 风格选择**：REST vs GraphQL vs gRPC 决策指南
- **接口稳定性**：版本策略（URL/path/header）、向后兼容、弃用流程
- **契约设计**：请求/响应格式、状态码规范、分页/过滤/排序标准
- **错误处理**：统一错误响应格式、错误码体系、调试信息分级
- **文档驱动**：OpenAPI/Swagger 规范、API 文档自动生成

## 使用方式

在 Claude Code 中使用 `/api-design` 调用。

```
/api-design 帮我设计一个用户管理模块的 REST API
/api-design 审查这个 API 设计是否向后兼容
/api-design 从 REST 迁移到 GraphQL 的策略建议
```

## 工作流

1. **需求梳理** — 资源模型、CRUD 操作、权限层级
2. **端点设计** — URL 命名、HTTP 方法选择、查询参数
3. **契约定义** — 请求/响应 JSON Schema、状态码映射
4. **版本策略** — 选择版本方案、制定弃用时间表
5. **文档输出** — OpenAPI 3.0 规范文件、示例请求

## API 设计原则

| 原则 | 做法 | 反例 |
|------|------|------|
| 名词复数 | `/users` `/orders` | `/getUser` `/createOrder` |
| HTTP 语义 | GET=查询 POST=创建 PUT=全量更新 PATCH=部分更新 DELETE=删除 | 全部用 POST |
| 状态码准确 | 200/201/400/401/403/404/409/500 | 全部返回 200 + code 字段 |
| 分页统一 | `?page=1&limit=20` + Link header | 每端点不同分页方式 |
| 错误可调试 | `{"error": {"code": "INVALID_EMAIL", "message": "..."}}` | 返回 HTML 或纯文本 |

## 适用场景

- 从零设计新 API（REST 或 GraphQL）
- API 需要做不兼容变更，规划迁移路径
- 现有 API 风格混乱，需要统一规范
- 需要为外部开发者提供 API 文档

## 限制

- 不涉及 gRPC/WebSocket 的详细实现
- 不替代 API 网关/Kong 等基础设施配置
- 接口安全（OAuth2/JWT）建议配合 security-guardian 使用

## 相关参考（Playbook）

本子技能落地"接口契约怎么设计"，跨栈方法论见下列 `references/`（按需读取）：

- 后端深度 playbook（API + 架构 + FastAPI 踩坑速查）：[references/backend-playbook.md](../../references/backend-playbook.md)
- AI-native 全栈工作流（契约优先 → 前后端并行 → 类型安全）：[references/fullstack-workflow.md](../../references/fullstack-workflow.md)（类型生成见 [scripts/gen_types_from_openapi.py](../../scripts/gen_types_from_openapi.py)）