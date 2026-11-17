---
name: dead-code-cleaner
description: 基于 codebase-memory-mcp 知识图谱的多阶段死代码检测与安全清理。当用户要求清理无用代码、查找并删除死代码、消除未被引用的文件、进行项目代码清理、或运行基于知识图谱的死代码分析时使用。支持所有编程语言（JS/TS/Vue/React/Python/Java/Go/Rust/C/C++/PHP/C# 等有精确验证模式，其他语言使用通用层验证）。同时处理单仓库与 monorepo。
---

# 死代码清理器

## 概述

基于 codebase-memory-mcp 知识图谱的 11 阶段工作流，安全地识别并移除未被引用的代码。每个候选文件在删除前均通过 N 层验证，级联死代码检测会捕获在其唯一消费者被移除后成为孤儿文件的代码。

以下引用的所有 MCP 工具均属于 `codebase-memory-mcp` 服务，通过标准 MCP 工具调用约定使用（如 `mcp__codebase-memory-mcp__index_repository`）。

## 快速开始

用户通过以下短语触发此 skill：
- "清理死代码"
- "移除项目中的无用文件"
- "查找并删除 <项目> 中的死代码"
- "运行死代码分析和清理"

### 参数解析

三个参数驱动整个工作流。全部自动检测；仅在检测结果有二义性时询问用户。

**repo-path** — 项目在磁盘上的根目录。

默认值：当前工作目录（`pwd`）。如果用户指定了项目名，从已知的工作区路径解析。仅在两者都不明确时询问。

**index-name** — codebase-memory-mcp 中使用的项目标识符。

检测顺序（使用第一个成功的）：
1. `package.json` → `name` 字段
2. `go.mod` → module 路径（`module ` 后的第一行）
3. `Cargo.toml` → `[package]` 下的 `name`
4. `pom.xml` → `<artifactId>`（第一个匹配）
5. `composer.json` → `name` 字段（PHP 项目）
6. `.csproj` / `.sln` → 项目文件名（C# 项目，取第一个匹配的 `.csproj` 文件名去掉扩展名）
7. `Gemfile` → 目录名（Ruby 项目）
8. `setup.py` / `pyproject.toml` → `name` 字段
9. 回退到 `repo-path` 的目录名

**app-name** — 总结文档中使用的可读名称。

检测顺序（使用第一个成功的）：
1. `package.json` → `description` 或 `name`
2. `composer.json` → `description` 或 `name`（PHP 项目）
3. `.csproj` 所在目录名（C# 项目）
4. 与 `index-name` 相同
5. `repo-path` 目录名的 Title Case 格式

### Monorepo 处理

通过检查是否存在各自包含独立构建清单（`package.json`、`go.mod`、`Cargo.toml`、`composer.json`、`.csproj`、`pom.xml` 等）的子目录来检测 monorepo 结构。常见模式：`microapps/`、`packages/`、`apps/`、`services/`、`modules/`。

当检测到 monorepo 时：

- **单个子项目**（用户明确指定了某一个）：仅作用于该子项目，直接在当前 agent 中执行完整流程（阶段 0–10）。

- **多个子项目**（用户选择了多个，或说了"全部"/"整个工作区"）：
  1. **全局索引**（主 agent）：先对所有涉及的子项目逐个执行 `index_repository mode=full`，再执行一次 `index_repository mode=cross-repo-intelligence target_projects=["*"]`，建立完整的跨项目引用图谱。此步完成后，每个子项目的 L-cross 验证都有了准确的跨项目引用基线。

  2. **派发子 agent**：主 agent 检测当前环境可用的子 agent 能力，**自动选用**下表第一种可用方式；不可用时直接串行，不报错停滞。**禁止使用 fork_thread**（会继承主 agent 上下文，导致多项目污染）。

     | 优先级 | 环境能力 | 派发方式 |
     |--------|----------|----------|
     | 1 | 内置并行子 agent 派发工具 | 每个子项目派发一个子 agent，同批并行 |
     | 2 | 独立会话创建工具（干净会话，非 fork） | 每个子项目创建一个独立会话 |
     | 3 | 以上均不可用 | 主 agent 对各子项目**串行**执行阶段 0–10 |

     各子 agent 传入**相同的 prompt**（`<...>` 替换为实际值）：

     ```
     清理以下单个子项目的死代码。必须 @ dead-code-cleaner，先完整读取 SKILL.md 再执行——与主 agent 跑单个子项目时相同的阶段 0–10 流程，逐步执行，不可凭记忆省略或只输出分析结论。
     不要处理其他子项目，不要运行 monorepo 检测逻辑。

     子项目路径：<子项目路径>（即 repo-path）
     索引名：<index-name>
     应用名：<app-name>

     全局索引已完成，阶段 1.1/1.2 跳过。其余阶段与 SKILL.md 正文完全一致：
     0 → 1.3 → 1.4 → 1.5 → 1.6 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10

     阶段 1.4 的 Cypher 结果须按子项目路径过滤（仅保留 path 以「<子项目路径>/」开头的节点）。
     阶段 6 必须实际删除文件（rm/git rm），不可只列清单。
     rg 命令与验证层详见 references/verification-patterns.md。
     完成后按 references/output-template.md 输出完整清理总结。
     ```

     **分批执行**：若子项目超过 5 个，每批 3–5 个并行派发，等本批全部完成后再派下一批。

     **兜底**：派发第一批后抽查一个子 agent 的输出。若未按上述流程执行（如跳过阶段、只分析不删除、未读 SKILL.md），则放弃子 agent，改由主 agent 对各子项目串行执行相同流程。

  3. **并发执行**：同批次的子 agent 并行运行，主 agent 等待全部完成后汇总，不介入各子 agent 的执行过程。

  4. **汇总结果**：主 agent 执行跨仓库索引更新（阶段 7.3），再按 [output-template.md](references/output-template.md) 格式输出合并总结（各项指标按子项目分列，末尾加总计行）。

- **用户未指定**：列出检测到的子项目，询问用户要清理哪一个（或多个）。


## 前置检查：环境准备

在开始分析之前，确认工具链就绪。

### 1. 检查 codebase-memory-mcp 是否可用

检查二进制文件是否存在：
```bash
which codebase-memory-mcp && codebase-memory-mcp --version
```

如果未找到，告知用户按照官方指南安装。二进制文件必须位于 `$PATH` 中。

### 2. 确认 MCP 服务已配置

通过调用一个轻量工具来验证 MCP 服务连接：
```
mcp__codebase-memory-mcp__list_projects
```

- **调用成功** → 继续。
- **调用失败** → 运行 `codebase-memory-mcp install` 尝试修复，然后重新验证。
- **仍失败** → **终止流程**。提示用户：codebase-memory-mcp MCP 服务不可用，请检查配置是否正确。修复后重新运行本 skill。

### 3. 启用 3D 图谱可视化

设置 UI 标志（持久化，重启后仍生效）：
```bash
codebase-memory-mcp --ui=true
```
默认端口为 9749。验证其是否响应：
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:9749
```
如果端口被占用，更换端口：`codebase-memory-mcp --port=<备选端口>`。

### 4. 保存当前状态

建议用户在继续之前提交或暂存当前更改。工作流会删除文件但不会自动提交——用户自行控制版本管理生命周期。


## 阶段 0：语言栈识别

0.1 扫描项目文件扩展名分布（不限语言，扫描实际文件系统中的源文件。codebase-memory-mcp 索引的是文件系统而非 git，二者需保持一致）：
```bash
find <repo-path> -type f \
  -not -path '*/node_modules/*' \
  -not -path '*/vendor/*' \
  -not -path '*/.git/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  -not -path '*/target/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/bin/*' \
  -not -path '*/obj/*' \
  -not -name '*.json' \
  -not -name '*.yaml' -not -name '*.yml' \
  -not -name '*.md' -not -name '*.txt' -not -name '*.rst' \
  -not -name '*.lock' \
  -not -name '*.svg' -not -name '*.png' -not -name '*.jpg' \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -30
```
常见映射参考：`.vue/.ts/.js/.jsx/.tsx` → JS/TS 系列，`.py` → Python，`.go` → Go，`.java` → Java，`.rs` → Rust，`.c/.cpp/.h` → C/C++，`.rb` → Ruby，`.php` → PHP，`.swift` → Swift，`.kt` → Kotlin，`.cs` → C#，`.scala` → Scala。

0.2 根据主导扩展名映射到语言栈：
- **在表中**：参见[语言参考模式表](references/verification-patterns.md)，使用对应的精确验证层。
- **不在表中**：codebase-memory-mcp 的图谱索引本身是语言无关的，阶段 1 的孤立节点检测仍然有效。进入阶段 2 时使用[通用验证层](references/verification-patterns.md#通用验证层表外语言)。

0.3 对于多语言混合项目：所有识别到的语言（表内 + 表外）的验证层都必须执行。



## 阶段 1：全量索引

1.1 全量重建当前项目索引：
```
mcp__codebase-memory-mcp__index_repository mode=full repo_path="<repo-path>"
```

1.2 跨仓库智能索引（仅 monorepo；单仓库跳过）：
```
mcp__codebase-memory-mcp__index_repository mode=cross-repo-intelligence target_projects=["*"] repo_path="<repo-path>"
```

1.3 通过 `mcp__codebase-memory-mcp__get_architecture` 获取架构全貌。记录：节点数、边数、路由、入口点、语言分布。

1.4 通过 `mcp__codebase-memory-mcp__query_graph` 查找未被任何文件引用的 File 节点（入度为 0）。注意：不要求出度为 0——一个文件即使导入了其他模块，只要没有任何文件引用它，它就是死代码：
```cypher
MATCH (f:File) WHERE f.in_degree = 0 RETURN f.path
```
此结果构成候选集。

1.5 从候选集中排除以下文件：
- 构建配置文件（`webpack.config.*`、`vite.config.*`、`Makefile`、`CMakeLists.txt` 等）
- 包管理文件（`package.json`、`go.mod`、`Cargo.toml`、`pom.xml`、`composer.json`、`Gemfile`、`requirements.txt` 等）
- 入口文件（`main.*`、`index.*`、`app.*`、`__init__.py` 等——根据项目约定调整）
- 测试文件（`*.test.*`、`*.spec.*`、`*_test.*`、`test_*` 等）
- 类型声明文件（`*.d.ts`、`*.pyi` 等）
- barrel/重导出索引文件（需人工核实）
- 数据/配置文件（`*.json`、`*.yaml`、`*.yml`、`*.xml`、`*.toml`、`*.lock`——这些文件可能被图谱索引但通常不是代码入口）
- 文档文件（`*.md`、`*.txt`、`*.rst`）

1.6 **重复文件候选扩展**：项目迭代中常见将代码复制到新位置而忘记删除原版。字节级相同的文件意味着至少一份是废弃副本，但图谱可能因"两份文件互相无引用"而漏掉其中一份。

```bash
# 查找字节级相同的文件对（语言无关，扩展名使用阶段 0 的结果）
find <source-dir> -type f \( -name '*.js' -o -name '*.ts' -o -name '*.vue' -o -name '*.py' -o -name '*.go' -o -name '*.java' -o -name '*.php' -o -name '*.cs' \) -exec md5 -q {} \; | sort | uniq -d
```

对每组重复文件：
- 如果至少一份已在候选集中 → 将组内所有文件加入候选集
- 如果组内所有文件均不在候选集中 → 同样全部加入候选集（两份完全相同且都未被引用，均为死代码嫌疑）

加入后不重复执行 1.5 的排除规则（重复文件不受"非代码文件"排除影响）。

**约束**：候选集以图谱查询结果为基础，1.6 的 md5 重复检测是对图谱盲区的补充——两份字节级相同的文件互相无引用关系时，图谱无法发现它们之间的关联。除此例外，禁止手动挑选子集。

**如果候选集为空**（1.5 排除和 1.6 扩展后均无文件）：
- 项目代码引用关系完整，未发现可疑死代码。
- 直接跳到阶段 10，输出空报告（清理效果表各项均为 0）。
- 仍然打开 3D 图谱供用户可视化确认。


## 阶段 2：逐文件 N 层验证

根据阶段 0 的语言识别结果，对候选集中每个文件 F 选择验证策略：

- **语言在参考表中**：执行[验证模式参考](references/verification-patterns.md)中该语言对应的所有精确验证层。不适用的层跳过（标记 N/A）。
- **语言不在参考表中**：执行[通用验证层](references/verification-patterns.md#通用验证层表外语言)。核心思路是利用图谱已经证明"无入边"的事实，加上文件名全文搜索和相对路径搜索作为最终确认。


验证层一览：
- **L-import-abs**：绝对路径/别名路径导入
- **L-import-rel**：相对路径导入（`./` 和 `../`）
- **L-dynamic**：动态加载（`import()`、`require()`、`Class.forName()` 等）
- **L-cross**：跨项目/跨仓库引用（仅 monorepo）
- **L-template-tag**：模板标签引用（Vue/React/Angular）
- **L-component-reg**：组件注册（Vue/Angular）
- **L-reflection**：反射/运行时引用（Python/Java/PHP/C#/Go）
- **L-config-ref**：配置文件中的引用（.yaml、.json、.xml、.properties）

**同名校验**：当 `{basename}` 在项目中存在多个同名文件时（如 `check-list.vue` 在 `baseline-check/` 和 `cloud-baseline-check/` 各有一个），L-import-abs 模式 B、L-template-tag、L-component-reg 的裸 basename 命中无法区分来源。必须执行精确路径反查——仅当命中的 import/标签路径包含正确的 `{parent_dir}/{basename}` 时才计入有效命中。详见 [verification-patterns.md](references/verification-patterns.md)「同名校验」节。


各语言每层对应的精确 `rg` 模式见 [verification-patterns.md](references/verification-patterns.md)。使用 `rg` 时，根据需要添加 `--no-ignore` 以搜索包括被 git 忽略的目录，添加 `-l` 仅列出匹配文件。

**Python f-string 正则陷阱**：在 Python 中使用 f-string 构建 `rg` 正则时，`{` 和 `}` 是 Python 格式化占位符。如需在 f-string 中表示字面量 `{` 或 `}`，必须写为 `{{` 和 `}}`。**更推荐的做法是避免在 Python 中构建正则**，直接用 shell 变量或裸 `rg` 命令：

```bash
# 推荐：直接用 shell 变量
rel_path="dialogs/upload-certificate"
rg -l "from ['"]@/${rel_path}['"]" src/

# 不推荐：Python f-string 中容易出错
# f"rg "from ['\"]@/{{{rel_path}}}['\"]""
#                       ^^^             ^^^  三重花括号极易写错
```

**阶段 2 验证必须逐个文件输出结果**：对每个候选文件，输出各层的命中数。零命中的层标记为 0。结果必须人类可审计——不可仅在脚本内部静默判断。


## 阶段 3：汇总与交叉验证

3.1 对每层命中结果（L-*），人工逐条核实：
- **子串误匹配**：如 `vul-list` 包含 `ul-list`。用 `grep -v "vul-list"` 排除。
- **同名异文件**：如 `a/foo.vue` 被误判为引用了 `b/foo.vue`。此问题主要在阶段 2 的「同名校验」步骤中解决——当检测到同名文件时，必须用精确路径反查替换裸 basename 匹配（见 verification-patterns.md 同名校验节）。阶段 3 交叉验证时再次确认：逐一检查每个命中的 import/标签路径，确保其引用的文件路径与候选文件完全一致，排除指向同名异文件的所有命中。
- **注释/文档引用**：注释或文档中的引用不是代码引用。
- **HTML 注释排除（Vue/React 必做）**：`<!-- <Component /> -->` 中的组件标签不算代码引用。L-template-tag 层命中后必须用 `grep -v "<!--.*<"` 排除被 HTML 注释包裹的行。详见 verification-patterns.md L-template-tag 节。

3.2 标记规则：
- 任一层的任一命中经核实为**有效引用** → 标记 ALIVE，退出该文件的验证
- 所有层均无命中或所有命中均为误报 → 标记 DEAD


## 阶段 4：级联死代码检查（递归）

4.1 对每个 DEAD 文件 F，通过 `mcp__codebase-memory-mcp__trace_path`（出向）分析 F 的依赖图：F 导入了哪些目标 T？

4.2 对每个 T：
  a. 通过 `trace_path`（入向）列出 T 的所有消费者 → 集合 C
  b. 若 C ⊆ 当前 DEAD 集合，则 T 也标记为 DEAD
  c. 递归对 T 执行步骤 4.1
  d. **导出级死代码检测**（当 T 文件级检查为 ALIVE 时执行）：

    当 F 从 T 中导入了具名导出，但 T 整体仍被其他文件引用（因此不能标记为 DEAD）时，
    需进一步分析：这些具名导出是否还有其他消费者？

    i. 从 F 的源码中提取所有从 T 导入的具名导出 → 集合 E：
       ```bash
       # 如果 F 仍在本地（尚未删除），直接用 rg 提取
       rg "from ['\"].*{T_basename}" <path-to-F>
       # 如果 F 已被删除，从 git 历史恢复
       git show HEAD:<path-to-F> | grep "from ['\"].*{T_basename}"
       ```

    ii. 对每个 e ∈ E，搜索项目中是否有其他活代码从 T 导入了 e：
       ```bash
       # JS/TS/Vue：搜索 import { ..., e, ... } from '...T'
       rg -l "import\s*\{[^}]*\b{e}\b[^}]*\}\s*from\s*['\"].*{T_rel_path}['\"]" <source-dir>/
       ```
       各语言对应的精确模式见 verification-patterns.md L-export-dead 节。

    iii. 若 e 的所有消费者均来自当前 DEAD 集合（包括已删除的 F），标记 e 为 DEAD_EXPORT。
       记录到 DEAD_EXPORT 清单中（供阶段 6.2 执行清理）。

    iv. **注意**：
       - 默认导出（`export default`）视为整个文件，不适用导出级检测——已在文件级检查中覆盖
       - 重导出（`export { X } from './Y'`）需递归跟踪至最终定义文件
       - TypeScript 类型导出（`export type`、`export interface`）同理适用


4.3 终止条件：无新增 DEAD 文件。


## 阶段 5：预删除构建验证（门禁）

**在删除任何文件之前，必须先运行一次构建验证。这是最后一道安全网。**

5.1 执行构建（根据项目类型选择对应的验证方式）：
- 前端项目（JS/TS）：运行 `npm run build` 或 `yarn build`，确认 exit code 为 0
- Go 项目：`go build ./...`
- Rust 项目：`cargo build`
- Java 项目：`mvn compile` 或 `gradle build`
- C# 项目：`dotnet build`
- PHP 项目：运行 `php -l` 语法检查或 `composer run-script lint`（若有配置）；若无构建步骤，改为运行完整 L-* 层验证并逐层报告结果
- Python 项目：`python -m compileall .`
- 如果构建命令因环境限制无法执行（如 Node 版本不兼容），则**必须**对每个标记为 DEAD 的文件，重新手动执行完整的 L-* 层验证，并逐层报告结果

5.2 如果构建失败：
- **终止流程。** 此时尚未删除任何文件，构建失败说明项目本身存在预存问题，与死代码分析无关。
- 告知用户先修复构建错误，再重新运行本 skill。
- **不得**在构建失败的情况下继续删除文件——门禁的意义正在于此。

5.3 如果构建通过（0 error）：继续阶段 6。


## 阶段 6：资源文件与空目录清理

6.1 代码文件：`.vue` `.js` `.ts` `.jsx` `.tsx` `.py` `.java` `.go` `.rs` `.php` `.cs` `.c` `.cpp` `.h` `.rb` `.swift` `.kt` `.scala` 等。以阶段 0 识别到的扩展名为准，此处仅列出常见项。


6.2 **导出级清理**：对阶段 4 标记的每个 DEAD_EXPORT，从源文件中删除该导出的声明代码。

  - 删除 `export const/function/class/let/var NAME = ...` 声明块。保留文件内其他活导出。
  - 若被删除的导出是文件内其他活导出的依赖（如内部工具函数），不可一并删除——仅移除无消费者且无内部使用者的导出。
  - 级联清理顶层 import：若被删除的导出声明依赖了文件顶层的 `import` 语句，且该 import 仅被此导出使用（未被文件内其他活导出或活代码使用），一并移除该 import 语句。
  - 清理后若文件仅剩注释和空行（无任何可执行代码或导出），标记整个文件为 DEAD，按 6.1 处理。


6.3 样式文件：`.scss` `.css` `.less` `.styl`

6.4 资源文件：`.svg` `.png` `.jpg` `.gif` `.ico` `.woff` `.ttf` `.pdf`
  - 检查方法：在整个项目中 `rg` 搜索资源文件名
  - 若仅被 DEAD 文件引用，标记 DEAD

6.5 空目录：删除文件后，仅清理因本次删除变为空的目录。自底向上逐级检查：对每个被删除文件的父目录，若该目录下所有文件均已被删除（即目录为空），则删除该目录；递归向上直到非空目录为止。**不要**使用 `find -type d -empty -delete` 全量扫描——这会误删项目中预存的空目录（如空的 `__tests__/` fixture 目录）。


## 阶段 7：增量更新索引

7.1 确认所有删除已正确执行：
- `git diff --stat` 确认删除行数是否与 DEAD 清单一致
- 逐一检查每个 DEAD 文件是否已从文件系统中移除

7.2 重建索引：
```
mcp__codebase-memory-mcp__index_repository mode=full repo_path="<repo-path>"
```

7.3 跨仓库索引（多项目场景）：
- **主 agent / 单项目场景**：如果是 monorepo 且当前 agent 负责全局协调，执行以下命令更新跨项目引用索引：
  ```
  mcp__codebase-memory-mcp__index_repository mode=cross-repo-intelligence target_projects=["*"] repo_path="<repo-path>"
  ```
- **子 agent 场景**：跳过此步骤。主 agent 在所有子 agent 完成后统一执行跨仓库索引更新。

7.4 记录索引变化：节点数 before → after，边数 before → after。


## 阶段 8：编译与运行验证

8.1 构建验证（与阶段 5 使用相同的构建命令，确保删除后项目仍能通过编译）：
- 前端项目（JS/TS）：运行 `npm run build` 或 `yarn build`，确认 exit code 为 0
- Go 项目：`go build ./...`
- Rust 项目：`cargo build`
- Java 项目：`mvn compile` 或 `gradle build`
- C# 项目：`dotnet build`
- PHP 项目：`php -l` 语法检查或 `composer run-script lint`
- Python 项目：`python -m compileall .`
- 脚本语言（无编译步骤）：运行 linter/类型检查（`mypy`、`tsc --noEmit`）→ exit code 0

8.2 若有测试：运行测试套件（如 `npm test`、`go test ./...`、`cargo test`、`pytest`）并确认全部通过。

8.3 **如果构建或测试失败（且阶段 5 已通过）**——说明删除操作引入了问题：
- 从构建错误日志中定位缺失的引用（如 `Module not found: Error: Can't resolve '...'`）
- 用 `git checkout -- <被引用的文件>` 恢复这些文件
- 将这些文件从 DEAD 列表移除，标记为 ALIVE
- 重新对剩余候选执行阶段 4-8（无需重做阶段 3 的人工核实）


## 阶段 9：变更影响评估

9.1 运行变更检测：
```
mcp__codebase-memory-mcp__detect_changes project="<index-name>"
```

9.2 确认 `impacted_symbols` 为空列表 `[]`。

9.3 通过比较删除前后的 `get_architecture` 验证路由/入口点完整性。


## 阶段 10：输出总结文档

按照 [output-template.md](references/output-template.md) 中的模板生成总结文档。必须包含以下章节：

- 清理效果表（按类型分组的删除文件数、删除行数、清理率、图谱节点/边变化、受影响符号）
- 删除清单（如有文件被删除）
- 修改清单（如有文件被修改但未删除；无内容则不展示）
- 验证方法（列出实际使用的阶段 2 验证层 + 阶段 4 级联检查）
- 安全原则（列出本次清理遵循的所有验证原则）
- 建议人工复核（若涉及表外语言，列出需人工复核的文件；无则不展示）
- 风险评估（风险等级 + 影响面分析）

## 清理后：打开 3D 图谱可视化

在交付总结文档后，打开浏览器访问 3D 知识图谱：

```bash
open http://localhost:9749
```
如果前置检查中更改了端口，使用对应端口。`codebase-memory-mcp --ui=true` 已在前置检查阶段启用了 HTTP 图谱服务，无需额外安装浏览器插件。用户现在可以可视化地探索清理后的代码库，验证没有遗留的孤立节点，图谱结构完整。

## 安全护栏

- **必须完成所有验证层才能删除文件。** 每个 DEAD 标记必须在所有适用的 L-* 检查中零有效命中。
- **初始 DEAD 标记后必须运行级联检查（阶段 4）。** 一个看起来未被引用的文件，可能在其消费者被确认为 DEAD 后才成为级联受害者。
- **确认清理完成前必须运行构建验证（阶段 8）。** 通过构建是最后的安全网。
- **开始前先 commit 或 stash。** 在阶段 1 之前提醒用户。工作流会删除文件但不会自动提交——用户自行控制版本管理生命周期。
- **尊重 `.gitignore`**：绝不删除被 git 追踪但被项目忽略的文件（如生成代码、vendor 依赖）。删除前用 `git ls-files` 确认文件被追踪。
- **多项目并发清理**：按环境能力派发子 agent（并行派发工具 → 独立会话 → 串行兜底）；禁止 fork_thread。各子 agent 传入相同 prompt，完整执行阶段 0–10（仅 1.1/1.2 由主 agent 预先完成）。执行异常时回退为主 agent 串行。
- **L-template-tag 必须排除 HTML 注释**：Vue/React 模板中的组件标签可能被 `<!-- -->` 注释包裹。`rg "<ComponentName>"` 的裸匹配会命中注释中的标签，导致误判为 ALIVE。必须用 `grep -v "<!--.*<"` 做二次过滤。详见 verification-patterns.md L-template-tag 节的「注释排除（必做）」。
- **禁止用 Python/脚本批量运行验证层。** 阶段 2 的每一层必须直接用 `rg` 命令执行，输出必须可见可审计。不得在 Python f-string 中使用 `{` `}` 嵌套——这会与 Python 格式化语法冲突导致 pattern 被吞掉。如需在 Python 中构建正则，`{` 和 `}` 必须写为 `{{` 和 `}}`。
- **删除前必须运行构建验证（门禁）。** 在阶段 4（级联检查）完成后、阶段 6（删除文件）执行前，必须先运行阶段 5（预删除构建验证）。只有构建通过（0 error）才能继续删除。如果构建失败，终止流程，告知用户先修复预存问题。
