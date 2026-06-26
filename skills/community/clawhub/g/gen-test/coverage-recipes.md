# 覆盖率工具配方

Phase 4 使用本文档为目标项目选择和配置覆盖率工具。
按语言/框架索引，每个配方包含：检测、安装、运行、解析报告。

---

## 自动检测与安装逻辑

按以下优先级检测项目语言和已有的覆盖率配置。
**如果检测到缺失，执行对应的自动安装命令（需用户确认）。**

```
1. package.json 存在 → JavaScript/TypeScript 生态
   - 检查 jest.config / vitest.config / .nycrc / .c8rc
   - Jest: 内置 --coverage，无需额外安装
   - Vitest: 检查 @vitest/coverage-v8 或 @vitest/coverage-istanbul
     → 缺失则: npm install -D @vitest/coverage-v8
   - Mocha/其他: 检查 c8 / nyc
     → 缺失则: npm install -D c8

2. go.mod 存在 → Go
   - 内置 go test -cover，无需安装

3. pyproject.toml / setup.py / requirements.txt 存在 → Python
   - 检查 pytest-cov / coverage 是否在依赖中
   - 检查方式: pip show pytest-cov 2>/dev/null
     → 缺失则: pip install pytest-cov
   - 如项目使用 pyproject.toml 的 [project.optional-dependencies]
     → 同时将 pytest-cov 追加到 dev 依赖列表

4. pom.xml / build.gradle 存在 → Java/Kotlin
   - 检查 jacoco 配置
   - Maven: 检查 pom.xml 中是否有 jacoco-maven-plugin
     → 缺失则: 在 <build><plugins> 中添加 JaCoCo 插件配置
   - Gradle: 检查 build.gradle 中是否有 id 'jacoco'
     → 缺失则: 在 plugins 块中添加

5. Cargo.toml 存在 → Rust
   - 检查 cargo-llvm-cov: cargo llvm-cov --version 2>/dev/null
     → 缺失则: cargo install cargo-llvm-cov

6. *.sln / *.csproj 存在 → C#/.NET
   - 检查 coverlet: 搜索 *.csproj 中是否有 coverlet.collector
     → 缺失则: dotnet add package coverlet.collector
```

---

## JavaScript / TypeScript

### Jest

```bash
# 基础运行
npx jest --coverage --coverageReporters=text --coverageReporters=lcov

# 指定目录
npx jest --coverage --collectCoverageFrom='src/**/*.{ts,tsx,js,jsx}'

# 使用阈值（从 coverage_thresholds 读取）
npx jest --coverage \
  --coverageThreshold='{"global":{"lines":80,"branches":70,"functions":80}}' \
  --coverageThreshold='{"./src/**/*.ts":{"lines":60,"branches":50}}'
```

Jest 原生支持全局和按文件 pattern 的阈值 (`coverageThreshold` in jest.config)。

覆盖率报告位置：`coverage/lcov-report/index.html`

解析文本输出（stdout）中的摘要表格：

```
----------|---------|----------|---------|---------|
File      | % Stmts | % Branch | % Funcs | % Lines |
----------|---------|----------|---------|---------|
```

### Vitest

```bash
npx vitest run --coverage --coverage.reporter=text --coverage.reporter=lcov
```

需要安装 coverage provider：

```bash
# v8 (推荐，无需额外依赖)
npm install -D @vitest/coverage-v8

# 或 istanbul
npm install -D @vitest/coverage-istanbul
```

vitest.config 中配置（含阈值）：

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      include: ['src/**'],
      exclude: ['**/*.test.*', '**/*.spec.*'],
      thresholds: {
        lines: 80,       // coverage_thresholds.overall.line
        branches: 70,    // coverage_thresholds.overall.branch
        functions: 80,   // coverage_thresholds.overall.function
        perFile: true,   // 启用单文件阈值检查
      },
    },
  },
});
```

### c8 (Node.js 原生)

```bash
npx c8 --reporter=text --reporter=lcov node your-script.js
# 或配合其他测试运行器
npx c8 --reporter=text --reporter=lcov npx mocha
```

---

## Go

Go 覆盖率工具为内置，无需额外安装。

### 基础用法

```bash
# 运行测试并生成覆盖率
go test -coverprofile=coverage.out ./...

# 查看文本摘要
go tool cover -func=coverage.out

# 生成 HTML 报告
go tool cover -html=coverage.out -o coverage.html
```

### 解析摘要

`go tool cover -func` 输出格式：

```
package/file.go:42:    FunctionName    85.7%
...
total:                 (statements)    72.3%
```

提取最后一行的 total 作为总覆盖率。

### 按包查看

```bash
go test -cover ./...
# 输出每个包的覆盖率百分比
```

### 阈值检查

Go 没有内置的 `--fail-under`。解析 `go tool cover -func` 的 total 行，
与 `coverage_thresholds.overall.line` 阈值比对。

```bash
TOTAL=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | tr -d '%')
THRESHOLD=80
if [ "$(echo "$TOTAL < $THRESHOLD" | bc)" -eq 1 ]; then
  echo "!! 覆盖率 ${TOTAL}% 低于阈值 ${THRESHOLD}%"
fi
```

**单文件覆盖率检查**：解析 `go tool cover -func` 输出中每个文件的覆盖率，
与 `per_file.line` 阈值逐一比对。

---

## Python

### pytest-cov

```bash
# 安装
pip install pytest-cov

# 运行
pytest --cov=src --cov-report=term-missing --cov-report=html

# 使用阈值（从 coverage_thresholds.overall.line 读取）
pytest --cov=src --cov-fail-under=80
```

**单文件覆盖率检查**：`--cov-report=term-missing` 输出中逐行解析每个文件的 Cover 列，
与 `per_file.line` 阈值比对，列出未达标文件。

`--cov-report=term-missing` 输出格式：

```
Name                 Stmts   Miss  Cover   Missing
----------------------------------------------------
src/module.py           42      5    88%   23-25, 31, 45
```

### coverage.py (不使用 pytest 时)

```bash
# 安装
pip install coverage

# 运行
coverage run -m unittest discover
coverage report -m
coverage html
```

---

## Java / Kotlin

### JaCoCo (Maven)

pom.xml 中添加：

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
    </executions>
</plugin>
```

```bash
mvn test
# 报告位置: target/site/jacoco/index.html
```

### JaCoCo (Gradle)

```groovy
plugins {
    id 'jacoco'
}

jacocoTestReport {
    reports {
        xml.required = true
        html.required = true
    }
}
```

```bash
./gradlew test jacocoTestReport
# 报告位置: build/reports/jacoco/test/html/index.html
```

---

## Rust

### cargo-tarpaulin

```bash
# 安装
cargo install cargo-tarpaulin

# 运行
cargo tarpaulin --out Html --out Stdout
```

### cargo-llvm-cov (更精确)

```bash
# 安装
cargo install cargo-llvm-cov

# 运行
cargo llvm-cov --html
cargo llvm-cov --text
```

---

## C# / .NET

### coverlet

```bash
# 安装（通常随 xunit/nunit 模板自动安装）
dotnet add package coverlet.collector

# 运行
dotnet test --collect:"XPlat Code Coverage"

# 使用 reportgenerator 生成 HTML
dotnet tool install -g dotnet-reportgenerator-globaltool
reportgenerator -reports:"**/coverage.cobertura.xml" -targetdir:"coveragereport"
```

---

## 覆盖率报告统一摘要格式

无论使用哪种工具，Phase 4 产出的覆盖率摘要使用以下格式。
阈值从 `.test-gen.yaml` 或 `pyproject.toml` / `package.json` 中读取，
未配置时使用默认值（overall: 80/70/80, per_file: 60/50, delta: 90）。

```markdown
## 覆盖率报告

**工具**: [使用的覆盖率工具名]
**运行命令**: `[实际执行的命令]`
**阈值来源**: [.test-gen.yaml / pyproject.toml / 默认值]

### 总体覆盖率

| 指标 | 覆盖率 | 目标 | 达标 |
|------|--------|------|------|
| 行覆盖率 (Line) | XX.X% | 80% | YES / !! NO (-X.X%) |
| 分支覆盖率 (Branch) | XX.X% | 70% | YES / !! NO (-X.X%) |
| 函数覆盖率 (Function) | XX.X% | 80% | YES / !! NO (-X.X%) |

### 单文件覆盖率（未达标文件）

仅列出低于 per_file 阈值的文件：

| 文件 | 行覆盖率 | 目标 | 差距 | 分支覆盖率 | 目标 | 差距 |
|------|----------|------|------|------------|------|------|

如所有文件均达标，显示: "所有文件均达到单文件覆盖率阈值 (line: 60%, branch: 50%)"

### 模块覆盖率明细

| 模块/文件 | 行 | 分支 | 函数 |
|-----------|-----|------|------|

### 未覆盖的关键路径

| 文件 | 行号 | 描述 |
|------|------|------|

### 详细报告
完整的 HTML 覆盖率报告位于: `[路径]`
```

---

## 变更行覆盖率（Delta Coverage）

变更行覆盖率只关注**本次变更（相对于基准分支）的代码行**是否被测试覆盖。
对于"给已有项目补测试"的场景，这比全量覆盖率更有指导意义。

### 通用流程（适用于所有语言）

```
1. 获取变更行
   git diff --unified=0 <base_branch>...HEAD -- '*.py' '*.go' '*.ts' '*.js' ...
   解析输出，提取每个文件的变更行号集合

2. 生成覆盖率数据（使用各语言的工具，输出 lcov 或等效格式）

3. 交集计算
   对每个变更文件：
   - 变更行集合 ∩ 已覆盖行集合 = 已覆盖的变更行
   - delta_coverage = len(已覆盖的变更行) / len(变更行)

4. 产出报告
```

### Python: diff-cover

```bash
# 安装
pip install diff-cover

# 先生成覆盖率 XML
pytest --cov=src --cov-report=xml

# 基于 git diff 计算变更行覆盖率
diff-cover coverage.xml --compare-branch=main --html-report delta-coverage.html

# 使用阈值（从 coverage_thresholds.delta.line 读取）
diff-cover coverage.xml --compare-branch=main --fail-under=90
```

`diff-cover` 输出格式：

```
-------------
Diff Coverage
Diff: main...HEAD, staged and unstaged changes
-------------
src/tracker/sync/engine.py (85.7%): Missing lines 42-45, 78
src/tracker/analysis/llm.py (100%)
-------------
Total:   90.2% (37 of 41 lines)
```

### Go: 手动交集

Go 没有官方的 delta coverage 工具，使用脚本实现：

```bash
# 1. 生成覆盖率
go test -coverprofile=coverage.out ./...

# 2. 获取变更文件列表
git diff --name-only main...HEAD -- '*.go' > changed_files.txt

# 3. 过滤覆盖率数据中的变更文件
# coverage.out 格式: package/file.go:startLine.col,endLine.col count
# 与 git diff 的行号做交集
go tool cover -func=coverage.out | grep -f changed_files.txt
```

更精确的方案：使用 `git diff --unified=0` 提取具体行号，与 coverage.out 的行范围做交集。

### JavaScript/TypeScript: diff-cover 或手动

**方案 1**：生成 lcov 格式后使用 diff-cover（需要 Python 环境）

```bash
# Jest 生成 lcov
npx jest --coverage --coverageReporters=lcov
# 使用 diff-cover
diff-cover coverage/lcov.info --compare-branch=main
```

**方案 2**：使用 lcov-diff（纯 Node.js）

```bash
npx lcov-diff coverage/lcov.info --branch main
```

### Rust: cargo-llvm-cov + diff-cover

```bash
cargo llvm-cov --lcov --output-path lcov.info
diff-cover lcov.info --compare-branch=main
```

### Java: JaCoCo + diff-cover

```bash
mvn test  # 生成 JaCoCo 报告
# 转换 JaCoCo XML 为 Cobertura 格式后使用 diff-cover
# 或直接使用 JaCoCo 的 XML 报告
diff-cover target/site/jacoco/jacoco.xml --compare-branch=main
```

### 变更行覆盖率报告格式

```markdown
### 变更行覆盖率（Delta Coverage）

**基准分支**: main
**对比**: main...HEAD
**工具**: [diff-cover / 手动计算]
**运行命令**: `[实际执行的命令]`
**目标**: 90% (来自 coverage_thresholds.delta.line)

| 文件 | 变更行 | 已覆盖 | 未覆盖 | 覆盖率 | 达标 |
|------|--------|--------|--------|--------|------|

**总变更行覆盖率**: XX.X% (M/N 行) — 目标: 90% — YES / !! NO (-X.X%)

#### 未覆盖的变更行
| 文件 | 行号 | 上下文 |
|------|------|--------|
```

---

## Makefile targets 生成

如果项目使用 Makefile，在 Phase 4 末尾生成以下 targets（跳过已存在的同名 target）。

### 生成前检查

```bash
# 检查 Makefile 是否存在
test -f Makefile

# 检查已有 targets，避免冲突
grep -E '^(test|test-unit|test-e2e|test-cov|test-cov-delta|test-cov-html)\s*:' Makefile
```

### 各语言的 Makefile 模板

**Python (pytest)**

```makefile
COV_LINE ?= 80
COV_BRANCH ?= 70
COV_DELTA ?= 90

.PHONY: test test-unit test-e2e test-cov test-cov-delta test-cov-html

test: test-unit test-e2e

test-unit:
	python -m pytest tests/ -v

test-e2e:
	python -m pytest e2e/ -v

test-cov:
	python -m pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=$(COV_LINE)

test-cov-delta:
	python -m pytest tests/ --cov=src --cov-report=xml
	diff-cover coverage.xml --compare-branch=main --fail-under=$(COV_DELTA)

test-cov-html:
	python -m pytest tests/ --cov=src --cov-report=html
	@echo "Coverage report: htmlcov/index.html"
```

**Go**

```makefile
.PHONY: test test-unit test-e2e test-cov test-cov-delta test-cov-html

test: test-unit test-e2e

test-unit:
	go test ./... -v

test-e2e:
	go test ./e2e/... -v

test-cov:
	go test -coverprofile=coverage.out ./...
	go tool cover -func=coverage.out

test-cov-delta:
	go test -coverprofile=coverage.out ./...
	go tool cover -func=coverage.out | grep -f <(git diff --name-only main...HEAD -- '*.go')

test-cov-html:
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report: coverage.html"
```

**JavaScript/TypeScript (Jest)**

```makefile
.PHONY: test test-unit test-e2e test-cov test-cov-delta test-cov-html

test: test-unit test-e2e

test-unit:
	npx jest

test-e2e:
	npx jest --config jest.e2e.config.js

test-cov:
	npx jest --coverage --coverageReporters=text

test-cov-delta:
	npx jest --coverage --coverageReporters=lcov
	diff-cover coverage/lcov.info --compare-branch=main

test-cov-html:
	npx jest --coverage --coverageReporters=html
	@echo "Coverage report: coverage/lcov-report/index.html"
```

**JavaScript/TypeScript (Vitest)**

```makefile
.PHONY: test test-unit test-e2e test-cov test-cov-delta test-cov-html

test: test-unit test-e2e

test-unit:
	npx vitest run

test-e2e:
	npx vitest run --config vitest.e2e.config.ts

test-cov:
	npx vitest run --coverage --coverage.reporter=text

test-cov-delta:
	npx vitest run --coverage --coverage.reporter=lcov
	diff-cover coverage/lcov.info --compare-branch=main

test-cov-html:
	npx vitest run --coverage --coverage.reporter=html
	@echo "Coverage report: coverage/index.html"
```

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 覆盖率工具未安装 | 自动检测并安装（见自动检测与安装逻辑） |
| 覆盖率包含测试文件自身 | 配置 exclude 排除 `*test*` / `*spec*` |
| 覆盖率包含第三方代码 | 配置 include 只包含 src 目录 |
| 分支覆盖率远低于行覆盖率 | 正常现象，复杂条件需更多测试用例 |
| 覆盖率 100% 但仍有 bug | 覆盖率不等于正确性，关注断言质量 |
| diff-cover 未安装 | `pip install diff-cover`（Python 工具，可跨语言使用 lcov 格式） |
| 非 git 仓库无法做 delta coverage | 跳过变更行覆盖率，仅产出全量报告 |
| Makefile 已有同名 target | 跳过该 target，不覆盖用户已有配置 |
