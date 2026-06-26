# DESIGN - CI/CD Templates Generator

## 1. Concept & Vision

**cicd-gen** — 一键生成生产级 CI/CD Workflow 的 CLI 工具。用户只需提供「语言 + 框架 + 需求」，即可输出可直接提交的 `.github/workflows/ci.yml`（以及 GitLab CI / Jenkinsfile 变体）。

定位：面向独立开发者/小团队，让 CI/CD 配置从「门槛」变成「随手可得」的基础设施。

---

## 2. Design Language

- **输出风格**：YAML 纯净、无多余注释、可直接提交
- **CLI 交互**： positional args + flag，零配置即可跑
- **错误处理**：用户输入不合法时给出明确的修复建议

---

## 3. Architecture

```
cicd-gen
├── generator/
│   ├── __init__.py
│   ├── base.py          # TemplateEngine 基类
│   ├── github_actions.py # GitHub Actions 生成器
│   ├── gitlab_ci.py      # GitLab CI 生成器
│   └── jenkins.py         # Jenkinsfile 生成器
├── templates/
│   ├── python/          # pytest, unittest, coverage, docker, azure, aliyun, tencent
│   ├── javascript/      # jest, mocha, npm publish, docker
│   └── go/              # go test, goreleaser
├── cli.py               # CLI 入口 (cicd-gen)
└── tests/
    └── test_generator.py
```

---

## 4. Core Features

### 4.1 输入格式
```bash
cicd-gen python flask --test pytest --deploy docker --output .github/workflows/
cicd-gen javascript node --test jest --deploy docker --publish npm
cicd-gen go --test go-test --release goreleaser
```

### 4.2 支持场景矩阵

| 语言 | 测试 | 覆盖率 | Docker | 部署 | 发布 |
|------|------|--------|--------|------|------|
| Python | pytest/unittest | coverage | build+push | azure/aliyun/tencent/k8s/serverless | - |
| JavaScript | jest/mocha | - | build+push | azure/aliyun | npm publish |
| Go | go test | - | build | - | goreleaser |

### 4.3 输出格式
- `--format github` (默认): `.github/workflows/ci.yml`
- `--format gitlab`: `.gitlab-ci.yml`
- `--format jenkins`: `Jenkinsfile`
- `--format all`: 同时输出三种格式

---

## 5. CLI Interface

```bash
cicd-gen <language> [framework] [options]

Arguments:
  language              python | javascript | go
  framework             flask | django | fastapi | node | express | gin | echo

Options:
  --test TEST            pytest | unittest | jest | mocha | go-test
  --deploy DEPLOY        docker | azure | aliyun | tencent | k8s | serverless
  --release RELEASE      goreleaser | npm
  --format FORMAT        github | gitlab | jenkins | all
  --output DIR           输出目录 (默认: ./.github/workflows)
  --name NAME            workflow 名字 (默认: ci)
  --python-version VER   Python 版本 (默认: "3.11")
  --node-version VER     Node 版本 (默认: "20")
  --go-version VER       Go 版本 (默认: "1.22")
```

---

## 6. TDD Test Cases

### 单元测试覆盖
- `test_python_pytest_docker()`: Python + pytest + Docker
- `test_python_unittest_coverage()`: Python + unittest + coverage
- `test_javascript_jest()`: JavaScript + Jest
- `test_go_goreleaser()`: Go + goreleaser
- `test_github_actions_yaml_valid()`: 生成的 YAML 可解析
- `test_gitlab_ci_yaml_valid()`: GitLab CI YAML 可解析
- `test_jenkinsfile_valid()`: Jenkinsfile Groovy 语法合法
- `test_output_directory_creation()`: 自动创建输出目录
- `test_invalid_language()`: 无效语言报错
- `test_combined_features()`: 多特性组合

---

## 7. Quality Rules

- 单文件 ≤ 500 行
- 所有模板输出通过 `yaml.safe_load` 验证
- Jenkinsfile 通过 `jenkins-pipeline-linter` 或 basic Groovy 语法检查（无 raise）
- CLI 退出码：成功 0，参数错误 1，生成失败 2
