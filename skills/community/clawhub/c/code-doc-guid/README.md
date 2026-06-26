# code-doc-guid Skill - 轻量级代码导航助手

**code-doc-guid** 是一个轻量级、零依赖的代码库导航工具。它通过维护一个本地的 SQLite 知识图谱，帮助 AI 和开发者快速理解项目结构、文件层级和基础依赖关系。

设计为**“随用随走”**的脚本工具，特别适合在接手新项目时的快速侦察（Reconnaissance）。

## 🌟 核心理念

1.  **分层架构 (Layering)**：
    自动计算每个文件的“深度”。
    -   **Layer 0**: 基础工具（Utils, Config），不依赖项目内其他文件。
    -   **Layer N**: 业务逻辑，依赖底层组件。
    -   *Insight*: 修改 Layer 0 的文件风险极高，修改 Layer N 的文件相对安全。

2.  **双向索引**：
    -   **Used by**: 谁在用我？（影响面）
    -   **Depends on**: 我在用谁？（依赖项）

## 🛠️ 使用指南

本工具通过 `scripts/codebase_manager.py` 脚本执行。

### 1. 初始化/更新索引 (`update`)
在开始工作前，或修改代码后，务必运行此命令。它会扫描项目并更新本地 SQLite 数据库（默认存储在 `.trae/codebase.db`）。

```bash
python scripts/codebase_manager.py update
```
*特点：增量更新，速度极快 (<1s)。*

### 2. 检查文件 (`inspect`)
想了解一个文件的上下文？使用 `inspect`。

```bash
python scripts/codebase_manager.py inspect "AuthService"
```
*支持模糊匹配文件名。*

**输出示例**：
```text
File: src/services/AuthService.ts
Layer: 3
Used by (2): UserController.ts, ApiRoute.ts
Depends on (1): Database.ts
```

### 3. 搜索代码 (`search`)
查找类、函数或概念。

```bash
python scripts/codebase_manager.py search "login logic"
```

### 4. 导出全图 (`graph`)
生成项目的整体架构文档。

```bash
python scripts/codebase_manager.py graph
```
*生成 `architecture_layers.md` 和 `dependency_graph.json`。*

## 🔧 技术实现详解

### 1. 核心数据结构 (SQLite Schema)

本工具的核心是 `.trae/codebase.db` SQLite 数据库，包含三张主表和一张虚拟表。

*   **`files`**: 存储文件元数据。
    *   `id`, `path`, `mtime`, `checksum`, `layer` (拓扑层级), `scc_id` (强连通分量ID)。
*   **`symbols`**: 存储代码定义（类、函数）。
    *   `id`, `file_id`, `name`, `type`, `line_start`, `doc` (Docstring)。
*   **`dependencies`**: 存储文件间的引用关系。
    *   `source_file_id` -> `target_file_id`。
*   **`search_index` (FTS5)**: 虚拟表，用于全文检索。
    *   自动索引文件路径、符号名和 Docstring，支持自然语言查询。

### 2. 关键算法逻辑

#### A. 增量更新 (Incremental Update)
为了极致速度，`update` 命令执行以下流程：
1.  **扫描磁盘**: 遍历项目文件，获取 `mtime`。
2.  **差异对比**: 仅筛选出 `mtime` 变化的文件或新增文件。
3.  **原子解析**:
    *   解析文件内容（Python 使用 `ast`，JS/TS 使用正则）。
    *   在一个事务中 `DELETE` 旧的 Symbols/Dependencies 并 `INSERT` 新数据。
4.  **两阶段构建**:
    *   Phase 1: 写入所有节点（Files）。
    *   Phase 2: 解析 Imports 并通过 `ImportResolver` 映射到具体 File ID，建立边（Dependencies）。

#### B. 依赖解析 (Import Resolution)
`ImportResolver` 类负责将字符串形式的 import 转换为绝对路径：
*   **Python**: 模拟 `sys.path` 行为，处理相对导入 (`.`) 和包导入。
*   **TS/JS**: 解析 `tsconfig.json` 的 `paths` 配置，支持 Alias (`@/components/...`)，并尝试添加后缀 (`.ts`, `.tsx`, `/index.ts`) 进行匹配。

#### C. 图算法 (Graph Engine)
每次更新后，`GraphEngine` 会重算架构层级：
1.  **构建图**: 从数据库加载 Nodes 和 Edges。
2.  **检测循环依赖 (SCC)**: 使用 **Tarjan 算法** 识别强连通分量 (SCC)。循环依赖的文件被视为同一个“超级节点”。
3.  **拓扑排序**: 对 SCC 图进行拓扑排序，计算每个文件的 `layer` 值。
    *   **`search_index` (FTS5)**: 虚拟表，用于全文检索。
    *   自动索引文件路径、符号名和 Docstring，支持自然语言查询。

## 🚀 改进方向
-   优化正则解析或实现简易状态机解析，提升非 Python 语言的解析准确度（保持零依赖）。
-   支持 `.gitignore` 规则，动态过滤构建产物。
-   集成 Git Diff，实现“改动感知”的智能增量分析。
