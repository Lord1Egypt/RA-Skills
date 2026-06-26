# 编码规范索引

## 概述

本文档是项目编码规范的索引和导航指南，帮助 AI 模型快速定位和理解相关规范。

## 技术栈概览

### 主要技术
- **编程语言**: [如：TypeScript、Java、Python]
- **框架**: [如：Vue 3、Spring Boot 3、Django]
- **数据库**: [如：MySQL 8.0、Redis]
- **ORM**: [如：MyBatis-Plus]
- **构建工具**: [如：Vite、Maven、Gradle]
- **测试框架**: [如：Jest、JUnit、pytest]

## 规范文档索引

### 核心规范
| # | 规范 | 说明 | 关键内容 |
|---|------|------|---------|
| 1 | [接口规范](./coding.api.md) | API 设计标准 | 请求/响应格式、错误处理、版本管理、API 文档 |
| 2 | [架构规范](./coding.architecture.md) | 系统架构原则 | 分层架构、设计模式、数据访问、错误处理、ADR |
| 3 | [数据模型规范](./coding.data-models.md) | 数据库设计标准 | 命名规范、表结构、关系设计、索引、MyBatis-Plus 速查 |

### 前端规范
| # | 规范 | 说明 | 关键内容 |
|---|------|------|---------|
| 4 | [Vue.js 开发规范](./coding.vue.md) | Vue 3 前端规范 | 组件定义、Pinia 状态管理、Composables、路由 |

### 编码规范
| # | 规范 | 说明 | 关键内容 |
|---|------|------|---------|
| 5 | [编码风格规范](./coding.coding-style.md) | 代码格式标准 | 命名规范、代码格式、注释、函数设计、最佳实践 |
| 6 | [测试规范](./coding.testing.md) | 测试策略 | 测试金字塔、AAA 模式、Mock、覆盖率要求 |
| 7 | [安全规范](./coding.security.md) | 安全编码标准 | 输入验证、认证授权、加密、漏洞防护、依赖安全 |

### 质量与协作
| # | 规范 | 说明 | 关键内容 |
|---|------|------|---------|
| 8 | [性能优化规范](./coding.performance.md) | 性能优化策略 | 性能目标、缓存、数据库优化、异步处理、监控 |
| 9 | [文档规范](./coding.documentation.md) | 文档编写标准 | 注释原则、README 结构、CHANGELOG 格式 |
| 10 | [代码审查规范](./coding.code-review.md) | 代码审查流程 | 审查流程、检查清单、反馈原则 |
| 11 | [版本控制规范](./coding.version-control.md) | Git 工作流 | 分支策略、提交信息规范、合并策略、冲突解决 |

## 上下文加载策略

按任务类型加载对应规范组合：

| 任务类型 | 须加载的规范 |
|----------|------------|
| API 开发 | 接口规范 + 编码风格 + 测试规范 |
| 架构设计 | 架构规范 + 数据模型规范 + Vue 规范 |
| 代码生成（Java） | 架构规范 + 数据模型规范 + 编码风格 |
| 代码生成（Vue） | Vue 规范 + 编码风格 + 接口规范 |
| 代码审查 | 代码审查规范 + 编码风格 + 安全规范 + 测试规范 |
| 性能优化 | 性能优化规范 + 架构规范 + 数据模型规范 |

## 规范间引用关系

```
coding.architecture.md（架构原则、设计模式、错误处理）
  ├── 引用 → coding.data-models.md（数据访问层速查）
  ├── 引用 → coding.vue.md（前端架构）
  └── 引用 → coding.performance.md（缓存、监控）

coding.api.md（接口设计）
  ├── 引用 → coding.security.md（认证授权）
  └── 引用 → coding.coding-style.md（代码格式）

coding.code-review.md（审查流程）
  ├── 引用 → coding.security.md（安全检查）
  ├── 引用 → coding.testing.md（测试检查）
  └── 引用 → coding.performance.md（性能检查）

coding.coding-style.md（代码格式）
  ├── 引用 → coding.architecture.md（Java/MyBatis-Plus 速查、错误类型）
  └── 引用 → coding.data-models.md（数据访问规范）
```

---

*规范随项目演进时：可再次执行 **gen-coding-specs** 技能重新生成，或直接编辑本分册目录下的 `coding.*.md` 文件。*
