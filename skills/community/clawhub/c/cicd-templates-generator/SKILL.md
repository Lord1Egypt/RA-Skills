# SKILL.md — CI/CD Templates Generator

## Identity

**Name**: CI/CD Templates Generator (`cicd-gen`)
**Type**: CLI Tool + OpenClaw Skill
**Purpose**: 一键生成生产级 CI/CD workflow 文件（GitHub Actions / GitLab CI / Jenkins）
**Author**: kay
**Version**: 1.0.0

---

## Triggers

```
cicd-gen <language> [framework] [options]
```
触发词示例：
- "生成 Python Flask CI/CD workflow"
- "创建 GitHub Actions workflow for pytest + Docker"
- "GitLab CI for Node.js + Jest"
- "Generate Jenkinsfile for Go + goreleaser"
- "多平台 CI/CD: Python + pytest + Docker"
- "帮我创建一个 CI/CD workflow"
- "CI/CD 模板生成"

---

## Capabilities

### 支持的语言与框架

| 语言 | 框架 | 测试框架 | 部署选项 | 发布 |
|------|------|----------|----------|------|
| Python | flask, django, fastapi | pytest, unittest | docker, azure, aliyun, tencent, k8s, serverless | — |
| JavaScript | node, express | jest, mocha | docker, azure, aliyun, tencent | npm publish |
| Go | gin, echo | go-test | docker | goreleaser |

### 支持的场景

- **定时任务** (cron): 集成于 GitHub Actions `on.schedule`
- **PR 测试**: 集成于 `on.pull_request`
- **自动发布**: goreleaser / npm publish
- **多平台矩阵**: 同时输出 GitHub Actions + GitLab CI + Jenkinsfile
- **Docker 构建推送**: docker build + push 到 Docker Hub
- **云部署**: Azure Web App / 阿里云 ECS / 腾讯云 / Kubernetes / Serverless

---

## CLI Usage

```bash
# 基本用法
cicd-gen python flask --test pytest --output ./.github/workflows/

# Python + pytest + Docker
cicd-gen python flask --test pytest --deploy docker

# Python + pytest + Docker + Azure 部署
cicd-gen python flask --test pytest --deploy docker --cloud azure

# Python + unittest + 覆盖率
cicd-gen python django --test unittest --coverage

# JavaScript + Jest
cicd-gen javascript node --test jest

# JavaScript + Jest + Docker + npm 发布
cicd-gen javascript node --test jest --deploy docker --release npm

# Go + goreleaser
cicd-gen go gin --test go-test --release goreleaser

# 多平台输出
cicd-gen python flask --test pytest --format all

# 仅打印不写文件
cicd-gen python flask --test pytest --print-only

# 自定义版本
cicd-gen python flask --test pytest --python-version 3.10 --name "My CI"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `language` | python / javascript / go | 必填 |
| `framework` | flask / django / node / gin / echo 等 | 可选 |
| `--test, -t` | 测试框架 | 自动检测 (pytest/jest/go-test) |
| `--deploy, -d` | 部署目标 | 无 |
| `--release, -r` | 发布工具 (npm/goreleaser) | 无 |
| `--coverage, -c` | 启用覆盖率报告 | False |
| `--cloud` | 云服务商 (azure/aliyun/tencent) | 无 |
| `--format, -f` | github / gitlab / jenkins / all | github |
| `--output, -o` | 输出目录 | ./.github/workflows |
| `--name, -n` | workflow 名称 | CI |
| `--python-version` | Python 版本 | 3.11 |
| `--node-version` | Node 版本 | 20 |
| `--go-version` | Go 版本 | 1.22 |
| `--print-only` | 仅打印，不写文件 | False |

---

## Installation

```bash
pip install cicd-gen
# 或本地安装
cd cicd-templates-generator && pip install -e .
```

---

## Technical Details

- **语言**: Python 3.8+
- **依赖**: `pyyaml`
- **CLI 入口**: `cicd-gen`
- **代码行数**: 单文件 ≤ 500 行（generator 模块各自独立）
- **测试**: 25 个单元测试，全部通过

---

## 输出示例

### GitHub Actions (`.github/workflows/ci.yml`)

```yaml
name: CI
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt pytest
      - name: Run tests
        run: pytest
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/app:latest
```

---

## 文件结构

```
cicd-templates-generator/
├── cicd_gen/
│   ├── __init__.py
│   ├── cli.py                    # CLI 入口
│   └── generator/
│       ├── __init__.py           # BaseGenerator
│       ├── github_actions.py     # GitHub Actions 生成器
│       ├── gitlab_ci.py          # GitLab CI 生成器
│       └── jenkins.py            # Jenkinsfile 生成器
├── tests/
│   └── test_cicd_gen.py          # 单元测试
├── setup.py
├── SKILL.md
└── DESIGN-cicd-templates-generator.md
```

---

## Integration with OpenClaw

当用户请求创建 CI/CD workflow 时：

1. 解析用户意图（语言、框架、需求）
2. 调用 `cicd-gen` CLI 生成对应 workflow
3. 展示生成结果（`--print-only` 模式）
4. 可选：写入项目目录

```bash
# 示例调用
cicd-gen python flask --test pytest --deploy docker --print-only
```
