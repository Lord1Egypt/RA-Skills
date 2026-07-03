---
name: agentsmd-creator
description: >
  为项目仓库生成 AGENTS.md — AI 面向的项目 README。告诉 AI Coding Agent：项目是什么、怎么构建和测试、代码规范、编程原则等。
  触发场景：用户需要创建 AGENTS.md、生成项目 AI 指南、为仓库写 AI 上下文文件、或提到「给 AI 看的 README」、agentsmd-creator、AI 代码指南。
  输出：200 行以内的 AGENTS.md，采用 6 章结构（项目概述 → 快速开始 → 系统架构 → 代码规范与编程原则 → 本地开发及验证 → 文档导航）。
---

# AI 代码指南（agentsmd-creator）

为项目仓库生成 AGENTS.md，让 AI Coding Agent「打开即理解、改完即验证」。

## 核心原则

- **地图，不做手册** — 控制在 200 行以内，超了考虑拆分到 `docs/`
- **渐进式披露** — 前 10 行建立心智模型，详细内容用链接指向 `docs/`
- **实操导向** — 每条命令都是可直接跑的，不是描述性的

## 生成流程

### 0. 项目状态扫描（前置步骤）

生成 AGENTS.md 前，先快速扫描检查项目状态。

#### 0.1 统计文件数量

排除三方包及构建缓存路径后统计项目源文件总数（涵盖各语言常见三方包目录）：

```bash
find . -type f \
  -not -path './.git/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/vendor/*' \
  -not -path '*/__pycache__/*' \
  -not -path './.venv/*' -not -path './venv/*' \
  -not -path '*/target/*' -not -path '*/build/*' -not -path '*/dist/*' \
  -not -path './.gradle/*' -not -path './.idea/*' -not -path './.vscode/*' \
  -not -path './.m2/*' -not -path './Pods/*' -not -path './.dart_tool/*' \
  -not -path '*/coverage/*' -not -path '*/.svelte-kit/*' \
  -not -path '*/.next/*' -not -path './out/*' \
  -not -path '*/.egg-info/*' -not -path './.cache/*' \
  -not -path '*/bin/*' -not -path '*/obj/*' \
  -not -path '*/site-packages/*' -not -path '*/.bundle/*' \
  -not -path '*/.terraform/*' -not -path '*/.serverless/*' \
  -not -path '*/.cargo/*' -not -path '*/.nuget/*' \
  | wc -l
```

> 排除路径涵盖：Git、npm/Node.js、Go vendor、Python __pycache__/venv/site-packages/egg-info、Java/Maven/Gradle target/.m2/.gradle、IDE 配置、CocoaPods、Flutter/Dart、.NET bin/obj/.nuget、Rust target/.cargo、构建产物、Terraform、Serverless、系统缓存等。

**判断规则：** ≥ 10 个文件视为已有项目，< 10 个文件视为新项目。

#### 0.2 识别主语言与技术栈

通过特征文件判断主语言，匹配社区规范：

| 特征文件 | 主语言 | 社区规范 |
|----------|--------|----------|
| `go.mod` / `*.go` | Go | [Effective Go](https://go.dev/doc/effective_go) |
| `package.json` / `*.ts` / `*.js` | JavaScript/TypeScript | [Airbnb Style Guide](https://github.com/airbnb/javascript) |
| `requirements.txt` / `pyproject.toml` / `*.py` | Python | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) |
| `pom.xml` / `build.gradle` / `*.java` | Java | [Alibaba Java 规约](https://github.com/alibaba/p3c) |
| `CMakeLists.txt` / `*.cpp` / `*.h` | C++ | [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) |
| `*.csproj` / `*.sln` / `*.cs` | C# | [Microsoft .NET 命名约定](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/) |

完整社区规范列表 → 见 [references/community-standards.md](references/community-standards.md)

#### 0.3 编码规范处理

**已有项目（≥ 10 文件）：从代码全面分析编码规范**
- 按场景分类选取典型源文件，抽样数量尽量多，上限 128 个文件：
  - **入口/启动文件**：如 `main.go`、`index.ts`、`app.py` 等
  - **核心业务逻辑**：控制器、服务层、处理函数等
  - **数据模型/类型定义**：实体类、DTO、schema 定义等
  - **工具/辅助函数**：utils、helpers、common 模块
  - **中间件/拦截器**：filter、middleware、interceptor
  - **配置/常量**：config、constants、env 相关
  - **测试文件**：单元/集成测试，验证测试规范
  - **异常/错误处理**：error handler、exception 定义
  - **API 层**：路由定义、接口契约
- 按模块/包/目录分层，每层取代表性文件
- 分析维度：命名约定、缩进风格、注释格式、错误处理模式、import/using 组织、函数/类组织风格、目录结构惯例
- **规范冲突处理**：若同一维度发现多种规范（如多种日志规范），通过比较源文件修改时间，以最新修改的文件所遵循的规范为准
- 将分析结果写入 `docs/CODING_STYLE.md`

**新项目（< 10 文件）：使用社区标准**
- 根据 0.2 识别的技术栈，引用对应社区规范
- 生成默认 `docs/CODING_STYLE.md`

#### 0.4 检查 docs/ARCHITECTURE.md

- **不存在** → 分析项目结构生成架构描述，写入 `docs/ARCHITECTURE.md`
- **已存在** → 读取现有内容，merge 并更新

#### 0.5 检查 AGENTS.md

- **不存在** → 全新生成
- **已存在** → 读取现有内容，保留用户手动修改部分，merge 并更新

### 1. 收集项目信息

- 项目定位与技术栈
- 仓库目录结构（`tree -L 2` 或等价命令）
- 构建/测试/格式化命令（从 Makefile、package.json、pom.xml 等提取）
- 已有文档索引

### 2. 按 6 章模板生成

读取 [references/template.md](references/template.md)，按模板结构填充。

**编程原则内容：**
- 原则正文：直接引用 [references/principles.md](references/principles.md) 全文，不做压缩改写。
- 示例：将 [references/examples.md](references/examples.md) 中的示例作为补充，外链到 `docs/programming-principles-examples.md` 以保持 AGENTS.md ≤ 200 行。

**代码规范引用：**
- 第 4 章引用 `docs/CODING_STYLE.md`（步骤 0.3 生成/分析）
- 第 3 章引用 `docs/ARCHITECTURE.md`（步骤 0.4 生成/更新）

**关键约束：**
- 总行数 ≤ 200
- 第 1 章前 10 行内说清「项目是什么 + 技术栈 + 仓库结构」
- 详细内容用 `→ 见 docs/xxx.md` 链接外置
- 第 5 章给出完整的「改 → 构建 → 启动 → 验证」闭环命令
- 第 6 章列出所有详细文档索引表

### 3. Git 提交约定

在 AGENTS.md 中注明：Git 提交优先使用 `git-commit-helper` skill；如不使用，可采用社区标准语义化 Git Commit 协议（Conventional Commits）。

### 4. 输出与确认

按顺序输出：
- `docs/CODING_STYLE.md` — 新建或 merge 更新
- `docs/ARCHITECTURE.md` — 新建或 merge 更新
- `AGENTS.md` — 仓库根目录，新建或 merge 更新
- **CLAUDE.md 兼容** — 生成 AGENTS.md 后，在仓库根目录创建软链接指向 AGENTS.md：
  ```bash
  ln -sf AGENTS.md CLAUDE.md
  ```

告知用户各文件行数及操作类型（新建 / merge）。如 AGENTS.md > 200 行建议拆分。

## 注意事项

- 不要编造项目中不存在的命令或文件
- 如果不确定某个命令，用占位符 `TODO: 补充 xxx 命令` 标记
- 对于 monorepo，可以为每个 package 生成独立的 AGENTS.md 并在根目录放总索引
- Merge 更新时保留用户手动修改的内容，只更新 AI 可自动分析的部分
