---
name: create-harness-docs
description: "智能分析项目结构，自动创建符合 Harness Engineering 要求的文档体系。支持 Spring Boot、React、Vue、NestJS、Express、Django、FastAPI、Go 等多种项目类型。"
---

# Create Harness Docs (智能版)

自动分析当前项目类型并创建对应的 Harness Engineering 文档体系。

## 功能

1. **智能检测** - 自动识别项目类型 (Spring Boot/React/Vue/NestJS 等)
2. **生成对应模板** - 根据项目类型生成相应的分层架构、CI 配置
3. **创建文档** - AGENTS.md、架构文档、质量评级等
4. **架构测试** - 为 Java 项目生成 ArchUnit 测试

## 支持的项目类型

| 类型 | 检测依据 | 分层架构 |
|------|----------|----------|
| Spring Boot | pom.xml | Entity→DAO→Service→Controller |
| React | package.json + react | Types→Components→Hooks→Pages |
| Vue | package.json + vue | Types→Components→Composables→Views |
| NestJS | @nestjs/core | Entities→Repositories→Services→Controllers |
| Express | express | Types→DAO→Service→Controller |
| Django | manage.py | Models→Views→Serializers→Urls |
| FastAPI | fastapi | Models→Schemas→Services→Routes |
| Gin | go.mod | Models→Repository→Service→Handler |

## 使用方法

```bash
# 在项目目录运行，自动检测类型并创建文档
node create-harness-docs.js --init

# 选项
# --init          创建所有文档
# --agents        仅创建 AGENTS.md
# --architecture  仅创建架构文档
# --quality       仅创建质量评级
# --validate      验证现有文档
```

## 创建的文件

```
项目目录/
├── AGENTS.md                     # 入口/索引
├── docs/
│   ├── architecture/
│   │   ├── ARCHITECTURE.md      # 架构总览
│   │   └── domains/             # 业务域详情
│   ├── plans/                   # 执行计划
│   └── quality/grades.md        # 质量评级
├── .github/workflows/
│   └── harness-ci.yml          # CI 配置
└── (Java) src/test/.../ArchitectureTest.java  # ArchUnit 测试
```

## 核心原则

遵循 OpenAI Harness Engineering:

1. **AGENTS.md 是目录，不是手册** - 知识放 docs/
2. **严格分层** - 根据项目类型定义的分层架构
3. **约束即代码** - 用 linter/ArchUnit 强制规则
4. **持续清理** - 定期处理技术债务
