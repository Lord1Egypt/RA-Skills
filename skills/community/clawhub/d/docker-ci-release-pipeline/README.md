# Docker CI Release Pipeline

> 编排 docker-expert × github-actions-templates × testing-patterns × github，实现容器化应用的自动化构建、测试、安全扫描与镜像发布全链路闭环。

## 痛点分析

- **流程割裂**：Dockerfile 优化、CI 配置、安全扫描需要分别找不同资料或手动拼接
- **重复试错**：多阶段构建、安全加固、缓存优化需要专业知识积累
- **发布风险**：没有自动安全扫描的镜像发布存在漏洞暴露风险
- **版本混乱**：手动打标签、无法追溯构建来源

## 技能编排图谱

```
┌─────────────────────────────────────────────────────┐
│              Docker CI Release Pipeline             │
│                                                     │
│  ┌──────────────┐    ┌──────────────┐              │
│  │docker-expert│───→│testing-      │              │
│  │多阶段构建    │    │patterns      │              │
│  │安全加固      │    │容器内测试    │              │
│  └──────┬───────┘    └──────┬───────┘              │
│         │                   │                      │
│         ↓                   ↓                      │
│  ┌────────────────────────────────────┐           │
│  │   github-actions-templates         │           │
│  │   GitHub Actions CI/CD 工作流       │           │
│  └──────────────┬─────────────────────┘           │
│                 │                                │
│                 ↓                                │
│  ┌────────────────────────────────────┐          │
│  │   github                            │          │
│  │   验证CI状态 / 查看失败日志          │          │
│  └────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

## 输入输出

| 输入 | 输出 |
|------|------|
| 项目目录 + 语言/框架 | Dockerfile（生产级多阶段） |
| | docker-compose.yml（三环境） |
| | .github/workflows/build-push.yml |
| | .dockerignore |
| | 容器内集成测试文件 |

## 使用示例

**触发方式**：发送 `Docker构建` 或 `镜像发布` 或 `CI/CD`

**完整执行流程**：

1. **Dockerfile 生成**（docker-expert）
   - 分析项目结构，检测语言/框架
   - 生成多阶段 Dockerfile（deps → build → runtime）
   - 配置非root用户、只读文件系统、健康检查
   - 优化 .dockerignore 减少构建上下文

2. **测试文件生成**（testing-patterns）
   - 为容器环境编写集成测试
   - 使用工厂函数模式 mock 外部依赖
   - 配置 Jest supertest 或 pytest 测试框架

3. **CI 工作流生成**（github-actions-templates）
   - 构建矩阵：多架构（amd64/arm64）
   - 缓存策略：BuildKit + GHA 缓存
   - 安全扫描：Trivy + Snyk 双扫描
   - 发布策略：branch/PR/semver 自动标签

4. **CI 验证**（github）
   - 查看 workflow 运行状态
   - 定位失败步骤，查看详细日志
   - PR 检查通过后触发镜像发布

## 技术栈支持

- Node.js / TypeScript：`node:18-alpine` + `distroless/nodejs18`
- Python：`python:3.11-slim` + `python:3.11-alpine`
- Go：`golang:1.22-alpine` + `gcr.io/distroless/static`
- Java：`eclipse-temurin:21-jre-alpine`
- Rust：`rust:1.77-alpine` + `scratch`
