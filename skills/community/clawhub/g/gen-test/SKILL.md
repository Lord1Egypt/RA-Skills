---
name: test-gen
description: >-
  为已有项目生成单元测试和 E2E 测试。分析设计文档和函数签名（黑盒），
  评审可测试性设计缺陷，生成测试代码并产出覆盖率报告。
  Use when: "generate tests", "add tests", "补测试", "生成单测",
  "write unit tests", "add e2e tests", "测试覆盖率"。
  Proactively suggest when user has an existing project with insufficient
  test coverage and asks about quality or stability.
disable-model-invocation: true
---

# Test Gen: 为已有项目生成测试

## Overview

本 skill 面向**代码已存在、需要补充测试**的场景（区别于 TDD 先写测试再写代码）。
通过五个阶段，从项目理解到测试交付，系统性地为已有项目生成高质量测试。

**核心理念：**
- **黑盒优先** — 从函数签名和接口契约出发，不偷看实现
- **诚实评审** — 设计有问题就直接说，不生成低质量测试来掩盖
- **覆盖率可量化** — 每次生成后产出覆盖率数据作为质量基线

## 安装

支持两种安装方式，使用 AskQuestion 让用户选择：

**项目级安装**（推荐协作项目，跟随 git 提交，团队共享）：

```bash
mkdir -p .cursor/skills && cp -r /path/to/test-gen .cursor/skills/test-gen
# 同时安装斜杠命令
mkdir -p .cursor/commands && cp /path/to/test-gen.md .cursor/commands/test-gen.md
```

**用户级安装**（个人全局使用，跨项目可用）：

```bash
mkdir -p ~/.cursor/skills && cp -r /path/to/test-gen ~/.cursor/skills/test-gen
```

> 项目级安装的 skill 优先于用户级。如果两处都存在，项目级生效。
> 用户级安装时不支持斜杠命令（命令只能放在项目的 `.cursor/commands/` 下）。

## 前置检测

在开始前，自动检测项目环境：

```
检测清单：
1. 语言 — 扫描文件后缀和配置文件（package.json / go.mod / pyproject.toml / pom.xml / Cargo.toml 等）
2. 测试框架 — 检查已有依赖（jest / vitest / pytest / go test / JUnit / RSpec 等）
3. 已有测试 — 搜索 *_test.* / *.test.* / *.spec.* / test_*.* 文件
4. 覆盖率工具 — 检查是否已配置（nyc / c8 / coverage.py / go cover 等）
5. 设计文档 — 搜索 README / ARCHITECTURE / docs/ / DESIGN.md
6. 构建系统 — 检查 Makefile / Taskfile / justfile 是否存在
7. VCS 状态 — 检查 git 是否可用（用于后续变更行覆盖率）
```

### 自动安装缺失的覆盖率工具

如果检测到项目**有测试框架但没有覆盖率工具**，自动安装：

| 语言 | 条件 | 安装命令 |
|------|------|----------|
| Python | 有 pytest 但无 pytest-cov | `pip install pytest-cov` |
| JS/TS (Jest) | 无 --coverage 配置 | 已内置，无需安装 |
| JS/TS (Vitest) | 无 @vitest/coverage-* | `npm install -D @vitest/coverage-v8` |
| Go | — | 内置 `go test -cover`，无需安装 |
| Rust | 无 cargo-tarpaulin/llvm-cov | `cargo install cargo-llvm-cov` |
| Java (Maven) | 无 JaCoCo 插件 | 在 pom.xml 中添加 JaCoCo 插件配置 |
| Java (Gradle) | 无 jacoco 插件 | 在 build.gradle 中添加 `id 'jacoco'` |
| C#/.NET | 无 coverlet | `dotnet add package coverlet.collector` |

安装前使用 AskQuestion 确认：

```
检测到项目缺少覆盖率工具。建议安装：
- [工具名] (安装命令: `xxx`)
是否立即安装？
```

详细的安装配方见 [coverage-recipes.md](coverage-recipes.md)。

将检测结果汇报给用户，确认无误后进入覆盖率阈值加载。

---

## 覆盖率阈值配置

在前置检测完成后、进入 Phase 1 之前，加载覆盖率阈值。

### 阈值定义

三层阈值，各自独立判定：

```yaml
coverage_thresholds:
  overall:             # 全项目总体阈值
    line: 80           # 行覆盖率 %
    branch: 70         # 分支覆盖率 %
    function: 80       # 函数覆盖率 %
  per_file:            # 单文件阈值（任何单文件不低于此值）
    line: 60
    branch: 50
  delta:               # 变更行覆盖率阈值
    line: 90           # 新增/修改的代码行覆盖率
```

### 配置来源优先级

按顺序查找，找到即停：

1. **项目配置文件** `.test-gen.yaml`（项目根目录）

   ```yaml
   coverage_thresholds:
     overall:
       line: 85
       branch: 75
       function: 85
     per_file:
       line: 70
       branch: 60
     delta:
       line: 95
   ```

2. **项目包管理配置中的嵌入字段**
   - Python `pyproject.toml`：`[tool.test-gen.coverage_thresholds]`
   - Node.js `package.json`：`"test-gen": { "coverage_thresholds": { ... } }`

3. **默认值**（上方定义的 80/70/80、60/50、90）

加载后向用户展示当前生效的阈值及来源。

### 阈值在流程中的使用

- **Phase 4 步骤 4**（全量覆盖率）：将实际值与 `overall` + `per_file` 阈值逐项对比
- **Phase 4 步骤 5**（变更行覆盖率）：将实际值与 `delta` 阈值对比
- 将阈值传递给底层工具的 `--fail-under` 参数（如工具支持）
- 未达标指标在报告中标注 `!! NO` 并给出与目标的差距

---

## Phase 1: 设计文档分析

**目标**：理解项目的设计意图、模块划分和数据流。

### 步骤

1. **搜索设计文档**
   - 优先级：ARCHITECTURE.md > DESIGN.md > README.md > docs/ 目录 > 代码注释头
   - 也检查：API 文档（OpenAPI/Swagger）、proto 文件、GraphQL schema

2. **提取关键信息**
   - 项目目标和核心功能
   - 模块/包划分及职责
   - 核心数据流（输入 → 处理 → 输出）
   - 外部依赖（数据库、第三方 API、消息队列等）
   - 预期的行为约束和业务规则

3. **无文档时的降级策略**
   - 从目录结构推断模块划分
   - 从 import/require 关系推断依赖图
   - 从 package/module 配置推断项目类型
   - 从已有测试推断预期行为

4. **产出项目理解摘要**

格式：

```markdown
## 项目理解摘要

### 项目类型
[Web 应用 / API 服务 / CLI 工具 / 库 / ...]

### 模块划分
| 模块 | 职责 | 核心文件 |
|------|------|----------|

### 核心数据流
[描述主要数据流向]

### 外部依赖
[列出所有外部依赖及其用途]

### 业务规则与约束
[从文档中提取的关键业务规则]
```

详细指南见 [design-analysis-guide.md](design-analysis-guide.md)。

### STOP — 与用户确认

使用 AskQuestion 向用户展示项目理解摘要，确认：
- 模块划分是否准确
- 是否遗漏了关键模块或业务规则
- 测试范围的优先级（哪些模块最需要测试）

用户确认后进入 Phase 2。

---

## Phase 2: 函数签名黑盒分析

**目标**：从公开 API 的角度理解每个函数的契约，不看实现。

### 铁律

```
禁止读取函数体。只看签名、类型定义、文档注释。
```

违反这条规则就失去了黑盒视角，测试会不自觉地追随实现细节。

### 步骤

1. **识别公开 API**
   - 扫描导出的函数、类、方法
   - 排除内部/私有符号（_前缀、unexported、private 等）
   - 关注 Phase 1 中用户标记为高优先级的模块

2. **提取签名信息**（仅以下内容）
   - 函数名
   - 参数名和类型
   - 返回值类型
   - 关联的类型/接口定义（struct、interface、type alias）
   - 函数上方的文档注释（doc comment）
   - 是否为 async / 是否抛异常

3. **推断测试维度**

   对每个函数，基于签名推断：

   | 维度 | 说明 |
   |------|------|
   | 正常输入 | 典型合法输入 |
   | 边界值 | 空值、零值、最大/最小值、空集合 |
   | 异常输入 | 类型不匹配、nil/null/undefined、非法格式 |
   | 异常路径 | 基于返回的 error/exception 类型推断 |
   | 并发安全 | 如果签名暗示并发使用（channel、mutex、sync 相关） |

4. **产出签名清单**

按模块分组，每个函数一行：

```markdown
### 模块: [name]

| 函数 | 参数 | 返回值 | 推断的测试维度 |
|------|------|--------|----------------|
| CreateUser | (name string, email string) | (User, error) | 正常/空字符串/重复email/非法格式 |
```

---

## Phase 3: 可测试性评审

**目标**：判断每个函数是否适合直接编写测试，不适合的直接指出设计缺陷。

这是本 skill 的**关键差异化阶段**。大多数测试生成工具会为所有函数无脑生成测试，
导致大量 mock 堆砌和脆弱测试。本阶段的职责是**诚实评估**。

### 评审维度

详细清单和示例见 [testability-checklist.md](testability-checklist.md)。

核心维度：

| 维度 | 好的设计 | 坏的设计 |
|------|----------|----------|
| 纯度 | 相同输入 → 相同输出 | 依赖全局状态或隐式输入 |
| 依赖注入 | 外部依赖通过参数传入 | 函数内部硬编码 new/connect |
| 接口隔离 | 参数各自独立，职责清晰 | God Object 参数，一个 struct 传所有 |
| 确定性 | 不依赖时间、随机数 | 内部调用 time.Now() 或 Math.random() |
| 可观测性 | 行为可通过返回值验证 | 关键行为只通过副作用发生 |
| 函数粒度 | 单一职责，逻辑聚焦 | 一个函数做五件事 |

### 三种判定

对每个函数给出判定：

**可测 (TESTABLE)**
- 可以直接生成高质量测试
- 进入 Phase 4

**需重构 (NEEDS_REFACTOR)**
- 指出具体设计缺陷
- 给出建议的重构方向（如"将 DB 连接抽为接口参数"）
- **不自动重构** — 这超出了本 skill 的职责范围
- 不为这类函数生成测试

**跳过 (SKIP)**
- 说明原因：trivial getter/setter、纯委托/胶水代码、已有充分测试
- 不生成测试

### 产出

```markdown
## 可测试性报告

### 统计
- 可测: X 个函数
- 需重构: Y 个函数
- 跳过: Z 个函数

### 需重构的函数

#### [函数名]
- **问题**: [具体的设计缺陷]
- **影响**: [为什么这会导致测试困难]
- **建议**: [具体的重构方向]

### 跳过的函数
| 函数 | 跳过原因 |
|------|----------|
```

### STOP — 与用户确认

使用 AskQuestion 展示可测试性报告：
- 用户确认"需重构"的判定是否合理
- 用户决定是否先处理重构再继续
- 用户可以覆盖判定（强制为某个函数生成测试）

---

## Phase 4: 单元测试生成 + 覆盖率

**目标**：为所有"可测"函数生成高质量单元测试，并产出覆盖率报告。

### 测试设计原则

1. **一个测试一个行为** — 测试名即文档
2. **命名规范**：`test_<行为>_when_<条件>_should_<预期>`
3. **等价类划分**：正常输入 / 边界值 / 异常输入
4. **真实对象优先** — mock 仅用于不可控的外部依赖（网络、DB、文件系统）
5. **断言明确** — 每个测试有且仅有一个核心断言
6. **测试隔离** — 测试之间无顺序依赖，无共享可变状态

### 步骤

1. **确定测试文件位置**
   - 遵循项目已有的测试文件组织惯例
   - 如无惯例，同目录 `*_test.*` 或 `__tests__/` 目录

2. **按模块生成测试**
   - 对 Phase 2 签名清单中每个"可测"函数：
     - 生成正常路径测试（至少 1 个）
     - 生成边界值测试（基于 Phase 2 推断的边界条件）
     - 生成异常路径测试（基于 Phase 2 推断的异常路径）
   - 使用项目已有的测试框架和断言库

3. **运行测试**
   - 执行全部新生成的测试
   - 全部通过则继续
   - 如有失败：分析失败原因，修复测试代码（不修改被测代码）
   - 如失败源于被测代码 bug — 报告给用户，保留失败测试作为 bug 文档

4. **生成覆盖率报告**

   使用项目对应的覆盖率工具（参见 [coverage-recipes.md](coverage-recipes.md)）。

   产出摘要（阈值从覆盖率阈值配置中读取）：

   ```markdown
   ## 覆盖率报告

   ### 总体覆盖率

   | 指标 | 覆盖率 | 目标 | 达标 |
   |------|--------|------|------|
   | 行覆盖率 | XX.X% | 80% | YES / !! NO (-X.X%) |
   | 分支覆盖率 | XX.X% | 70% | YES / !! NO (-X.X%) |
   | 函数覆盖率 | XX.X% | 80% | YES / !! NO (-X.X%) |

   ### 单文件覆盖率（未达标文件）

   | 文件 | 行覆盖率 | 目标 | 差距 |
   |------|----------|------|------|
   | [仅列出低于 per_file 阈值的文件] |

   ### 未覆盖的关键路径
   [列出仍未覆盖的重要代码路径]
   ```

5. **变更行覆盖率（Delta Coverage）**

   除全量覆盖率外，计算**仅针对本次变更代码**的覆盖率。
   这对于"给已有项目补测试"的场景尤为重要 — 关注新增测试是否覆盖了目标代码。

   步骤：
   - 使用 `git diff` 获取相对于基准分支（main/master）的变更行
   - 将覆盖率数据与变更行做交集
   - 产出变更行覆盖率摘要

   详细工具配方见 [coverage-recipes.md](coverage-recipes.md) 中的"变更行覆盖率"章节。

   追加到覆盖率报告中（阈值从 `delta` 配置读取）：

   ```markdown
   ### 变更行覆盖率（Delta Coverage）

   **基准分支**: main
   **变更文件数**: N
   **变更行数**: M
   **目标**: 90%

   | 文件 | 变更行 | 已覆盖 | 覆盖率 | 达标 |
   |------|--------|--------|--------|------|

   **总变更行覆盖率**: XX.X% (目标: 90%) — YES / !! NO
   ```

6. **生成 Makefile targets（如项目使用 Makefile）**

   如果前置检测发现项目有 `Makefile`，生成测试相关 make targets
   （`test`, `test-unit`, `test-e2e`, `test-cov`, `test-cov-delta`, `test-cov-html`）。

   生成规则：
   - 检查 Makefile 中是否已有同名 target，有则跳过
   - 命令内容根据项目语言和测试框架填充（模板见 [coverage-recipes.md](coverage-recipes.md)）
   - 覆盖率阈值作为 Makefile 变量传入（如 `COV_LINE ?= 80`）
   - 使用 AskQuestion 确认后再写入 Makefile

### STOP — 与用户确认

使用 AskQuestion 展示：
- 测试运行结果
- 全量覆盖率报告 + 变更行覆盖率报告（含阈值达标状态）
- 未达标项的具体差距和建议
- Makefile targets（如已生成）
- 是否继续生成 E2E 测试

---

## Phase 5: E2E 测试生成

**目标**：基于用户故事和数据流，生成端到端集成测试。

### 步骤

1. **识别关键用户路径**

   基于 Phase 1 的项目理解，识别核心 E2E 场景：

   | 项目类型 | 典型路径 |
   |----------|----------|
   | Web 应用 | 用户注册 → 登录 → 核心操作 → 验证结果 |
   | API 服务 | 认证 → CRUD 操作 → 状态验证 → 错误处理 |
   | CLI 工具 | 参数解析 → 执行 → stdout/stderr 验证 → 退出码 |
   | 库 | 公开 API 的集成调用链 |

2. **选择 E2E 框架**

   | 项目类型 | 推荐框架 |
   |----------|----------|
   | Web 前端 | Playwright（首选）/ Cypress |
   | API 服务 (Node) | supertest |
   | API 服务 (Go) | net/http/httptest |
   | API 服务 (Python) | httpx + pytest |
   | CLI 工具 | 子进程调用 + 断言 stdout/stderr/exit code |

3. **生成 E2E 测试**
   - 每个测试覆盖一条完整的用户路径
   - 包含 setup（准备测试数据/环境）和 teardown（清理）
   - 测试数据与测试代码分离（fixture 文件或 factory 函数）
   - 处理异步操作（等待、重试、超时）

4. **运行 E2E 测试**
   - 执行全部 E2E 测试
   - 如需启动服务，提示用户或使用项目已有的启动脚本
   - 报告结果

### 产出

```markdown
## E2E 测试报告

### 测试场景
| 场景 | 覆盖的用户路径 | 状态 |
|------|----------------|------|

### 测试数据管理
[描述 setup/teardown 策略]
```

---

## 输出规范

### 测试代码质量标准

生成的测试代码必须满足：

- **可独立运行** — 不依赖其他测试的执行顺序或副作用
- **失败信息清晰** — 断言失败时能定位到具体的预期 vs 实际差异
- **无硬编码路径** — 使用相对路径或环境变量
- **无 sleep/delay** — 使用轮询或事件等待代替固定延迟
- **符合项目代码风格** — lint 规则、命名惯例与项目一致

### 文件组织

遵循项目已有惯例。如无惯例：单元测试同目录 `*_test.*`，E2E 测试放 `e2e/` 目录。

---

## 异常处理

| 情况 | 处理方式 |
|------|----------|
| 无设计文档 | Phase 1 降级为目录结构分析，明确告知用户信息来源 |
| 无类型信息（纯 JS/Python） | Phase 2 从 doc comment 和变量名推断类型 |
| 函数全部"需重构" | 暂停流程，给用户一份完整的重构建议清单 |
| 测试框架未安装 | 提示安装命令，等用户确认后继续 |
| 覆盖率工具未安装 | 自动检测并提示安装（见前置检测章节），用户确认后安装 |
| 测试发现被测代码 bug | 保留失败测试，在报告中标记为"疑似 bug" |
| 非 git 仓库 | 跳过变更行覆盖率，仅产出全量覆盖率 |
| Makefile 已有同名 target | 跳过该 target，不覆盖已有配置 |
| 无 .test-gen.yaml 配置 | 使用默认阈值（80/70/80、60/50、90），告知用户可创建配置文件自定义 |
| 覆盖率未达标 | 报告中标注差距，不阻塞流程，由用户决定是否补充测试 |
