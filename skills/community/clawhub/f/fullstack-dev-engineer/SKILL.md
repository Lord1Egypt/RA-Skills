---
name: fullstack-dev-engineer
description: 提供全栈开发架构设计、技术栈选型、前端开发、后端开发、运维部署指导；当用户需要架构设计、技术选型、前端开发、后端开发、运维部署或最佳实践咨询时使用
---

# 全栈全能开发工程师

## 任务目标
- 本 Skill 用于：协助用户完成从架构设计、前端开发、后端开发到运维部署的全栈开发任务
- 能力包含：系统架构设计、技术栈选型、前端开发、后端开发、项目规划、代码生成、运维部署、最佳实践指导
- 触发条件：用户需要设计系统架构、选择技术方案、开发前端/后端项目、部署应用、生成代码或咨询开发最佳实践

## 前置准备
本 Skill 无需额外依赖，所有能力通过智能体的语言理解和代码生成能力实现。

## 操作步骤

### 1. 需求分析
- 理解用户的业务需求和功能需求
- 明确系统的非功能性需求（性能、可扩展性、安全性、维护性）
- 识别技术约束和环境限制（部署环境、团队技能、预算）

### 2. 架构设计
- 参考架构模式：查阅 [architecture-patterns.md](references/architecture-patterns.md) 选择合适的架构模式
- 设计系统模块划分和组件关系
- 明确数据流和接口设计
- 生成架构设计文档和架构图描述

### 3. 技术栈选型
- 参考技术对比：查阅 [tech-stack-comparison.md](references/tech-stack-comparison.md) 进行技术栈对比
- 根据项目需求选择合适的前端、后端、数据库、中间件
- 考虑技术成熟度、社区活跃度、学习曲线和团队匹配度
- 提供技术选型说明和备选方案

### 4. 项目规划
- 制定开发计划和里程碑
- 设计项目目录结构
- 规划开发环境和部署流程
- 定义代码规范和协作流程

### 5. 代码实现
- 参考最佳实践：查阅 [best-practices.md](references/best-practices.md) 遵循开发最佳实践
- 参考代码规范：查阅 [code-standards.md](references/code-standards.md) 保持代码质量
- 生成模块代码和核心功能实现
- 编写单元测试和集成测试
- 生成API文档和使用说明

### 6. 前端开发
- 参考前端指南：查阅 [frontend-guide.md](references/frontend-guide.md) 了解前端开发实践
- 选择前端技术栈（React/Vue/Angular）
- 设计组件架构和状态管理方案
- 实现响应式布局和交互功能
- 优化前端性能和用户体验
- 编写前端测试（单元测试、E2E测试）

### 7. 运维部署
- 参考运维指南：查阅 [devops-guide.md](references/devops-guide.md) 了解运维实践
- 配置容器化环境（Docker/Kubernetes）
- 设计CI/CD流水线
- 配置监控和告警系统
- 设置日志收集和分析
- 制定备份和灾难恢复方案
- 实施安全加固措施

### 8. 交付与优化
- 代码审查和优化建议
- 性能优化和安全加固
- 部署文档和运维指南
- 后续迭代和维护建议

## 资源索引
- 架构模式参考：[architecture-patterns.md](references/architecture-patterns.md)（设计系统架构时参考）
- 技术栈对比：[tech-stack-comparison.md](references/tech-stack-comparison.md)（选择技术方案时参考）
- 前端开发指南：[frontend-guide.md](references/frontend-guide.md)（前端开发时参考）
- 运维实践指南：[devops-guide.md](references/devops-guide.md)（运维部署时参考）
- 最佳实践：[best-practices.md](references/best-practices.md)（开发过程中参考）
- 代码规范：[code-standards.md](references/code-standards.md)（编写代码时参考）

## 注意事项
- 充分利用智能体的代码理解和生成能力，避免为简单任务编写脚本
- 优先推荐成熟、稳定、有良好社区支持的技术栈
- 在架构设计时平衡当前需求和未来扩展性
- 生成的代码应遵循清晰、可维护、可测试的原则
- 根据项目实际复杂度调整设计复杂度，避免过度设计

## 使用示例

### 示例1：设计电商平台架构
**功能说明**：为中小型电商平台设计整体架构方案
**执行方式**：智能体基于架构模式参考进行设计指导
**关键要点**：
1. 分析电商核心功能：商品管理、订单处理、支付系统、用户中心
2. 选择微服务架构，拆分为商品服务、订单服务、支付服务、用户服务
3. 技术栈：前端React + Node.js后端 + MySQL + Redis + Nginx
4. 设计服务间通信和API网关

### 示例2：技术栈选型
**功能说明**：为实时协作应用选择技术栈
**执行方式**：智能体基于技术对比提供选型建议
**关键要点**：
1. 核心需求：实时性、多用户并发、数据一致性
2. 前端：Vue.js + WebSocket（实时通信）
3. 后端：Node.js + Socket.io（高并发处理）
4. 数据库：PostgreSQL + Redis（缓存）
5. 备选方案：Go + gRPC（性能优化）

### 示例3：生成后端API代码
**功能说明**：生成用户认证模块的RESTful API代码
**执行方式**：智能体基于代码规范直接生成代码
**关键要点**：
1. 定义API接口：注册、登录、登出、刷新Token
2. 选择技术栈：Node.js + Express + JWT + bcrypt
3. 生成路由、控制器、中间件代码
4. 添加输入验证和错误处理
5. 编写单元测试用例

### 示例4：前端React项目开发
**功能说明**：开发React前端项目，实现用户管理界面
**执行方式**：智能体基于前端指南生成前端代码
**关键要点**：
1. 选择技术栈：React + TypeScript + Vite + Tailwind CSS
2. 设计组件架构：页面组件、业务组件、通用组件
3. 实现状态管理：使用Zustand或Redux Toolkit
4. 实现路由和导航
5. 添加性能优化：代码分割、懒加载、缓存策略

### 示例5：Kubernetes部署配置
**功能说明**：为应用配置Kubernetes部署环境
**执行方式**：智能体基于运维指南生成K8s配置
**关键要点**：
1. 创建Deployment配置，设置资源限制和健康检查
2. 配置Service和Ingress，实现服务暴露和负载均衡
3. 配置ConfigMap和Secret，管理配置和敏感信息
4. 设置Horizontal Pod Autoscaler，实现自动扩缩容
5. 配置NetworkPolicy，实现网络安全隔离
