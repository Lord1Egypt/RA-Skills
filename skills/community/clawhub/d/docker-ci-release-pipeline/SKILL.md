---
name: docker-ci-release-pipeline
description: Docker镜像构建测试与GitHub Actions发布全链路流水线，自动构建、测试、安全扫描并推送至镜像仓库
category: 开发
triggers: Docker构建, 镜像发布, CI/CD, 容器化部署, GitHub Actions
---

# Docker CI Release Pipeline

自动化 Docker 镜像构建、测试、安全扫描与发布全链路流水线。

## 业务场景

开发团队需要将应用容器化并通过 GitHub Actions 自动发布到镜像仓库。传统做法需要手动编写 Dockerfile、优化构建、配置 CI、设置安全扫描，流程割裂且容易出错。

本 Combo 编排 docker-expert、github-actions-templates、testing-patterns、github 四个 Skill，一次性完成从镜像优化到自动发布的完整闭环。

## 工作流程

1. **docker-expert** 分析项目结构，生成生产级 Dockerfile（含多阶段构建、安全加固、健康检查）
2. **testing-patterns** 生成容器内的集成测试用例（Jest + supertest 或 pytest）
3. **github-actions-templates** 生成完整的 GitHub Actions 工作流（构建→测试→扫描→推送）
4. **github** 验证工作流执行状态，处理失败的构建步骤

## 核心功能

- 多阶段构建：构建依赖与运行时分离，镜像体积最小化
- 安全加固：非root用户、只读文件系统、最小化基础镜像
- 依赖缓存：利用 BuildKit cache-mount 加速重复构建
- 安全扫描：Trivy 漏洞扫描 + Snyk 依赖扫描
- 多架构支持：linux/amd64 + linux/arm64 并行构建
- 镜像标签策略：branch / PR / semver 自动打标

## 使用方法

### 触发词

`Docker构建` 或 `镜像发布` 或 `CI/CD`

### 输入

提供待容器化的项目目录结构和语言/框架信息

### 输出

- 优化后的 `Dockerfile`（多阶段、安全加固）
- `docker-compose.yml`（dev/staging/prod 三环境）
- `.github/workflows/build-push.yml`（完整 CI 工作流）
- 测试文件（在 `tests/` 或 `__tests__/` 目录）
- `.dockerignore`（构建上下文优化）

### 示例工作流

```yaml
# 触发条件
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  tags: ['v*']

# 流程：Checkout → Setup Buildx → Build & Test → Security Scan → Push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build --target production -t app:${{ github.sha }} .
      - name: Run tests in container
        run: docker run --rm app:${{ github.sha }} npm test
      - name: Security scan
        uses: aquasecurity/trivy-action@master
      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: docker push ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## 技术细节

- 基础镜像推荐：Alpine / Distroless / Scratch（生产）
- 多架构构建：docker buildx（linux/amd64, linux/arm64）
- 构建缓存：GitHub Actions Cache（GHA）驱动
- 镜像仓库：GHCR（GitHub Container Registry）优先
- 安全扫描：Trivy（文件系统）+ Snyk（依赖）双扫描
