# Phase 3: 工具系统

## 目标

构建模块化、可扩展的工具注册和执行机制，让 Agent 能调用各类工具完成任务。Claude Code 实际部署了 43+ 个工具，按类别组织为 agent、workflow、task、plan、advanced 五类。

---

## 设计原理

### 1. 工具即 Prompt

工具描述（Description）本质上是**写给 LLM 看的 Prompt**。描述越详细，LLM 调用参数越准确。每个工具的 description 应当包含：

- **功能说明**：工具做什么，一句话概括
- **适用场景**：什么情况下应该选用此工具（而非另一个相似工具）
- **参数语义**：每个参数的含义、格式、约束、默认值
- **返回结果说明**：返回值的数据结构和含义
- **反面示例**：常见误用场景（可选但强烈推荐）

Schema 验证是把第二道关——即便描述不够好，Schema 也能在运行时拦截参数类型错误。但描述好 + Schema 严才是最佳实践。

### 2. 工具分区算法（Tool Partitioning）

只读工具可并发执行，写入工具需串行化：

```
分区原则：
  只读（Read）  = 文件读取搜索、网络GET请求、只读DB查询    → 可并发
  副作用（Write）= 文件写入/删除、Shell执行、POST/PUT/DELETE → 串行队列
  
算法伪代码：
  function partition(tool_calls):
    reads = [t for t in tool_calls if t.is_concurrency_safe]
    writes = [t for t in tool_calls if not t.is_concurrency_safe]
    
    results = {}
    // 阶段1: 所有只读工具并发
    for each batch in chunk(reads, max_concurrent=5):
      results += parallel_execute(batch)
    
    // 阶段2: 写入工具按序串行
    for tool in writes:
      results += execute(tool)
    
    return results
```

**为什么需要分区**：上下文窗口资源有限，若 LLM 一次返回 10 个 tool_call，其中 3 个写文件 + 7 个读文件，先并发跑完 7 个读操作能提前释放网络/IO 等待，再串行处理 3 个写操作避免数据竞争。

### 3. 工具结果截断策略（Result Truncation）

工具返回结果可能非常长（如读取 5000 行日志、Git diff 全文），直接全量存入上下文会浪费 token。截断策略：

```
截断算法：
  function truncate(result, max_chars=8000):
    if len(result) <= max_chars:
      return result
    
    head = result[:max_chars * 0.4]      // 保留前 40%
    tail = result[-max_chars * 0.4:]     // 保留后 40%
    middle_summary = summarize(result[max_chars*0.4 : -max_chars*0.4])
    
    return f"""{head}
    ... [省略 {省略行数} 行，摘要如下] ...
    {middle_summary}
    ... [继续] ...
    {tail}"""
```

核心思路：首尾保留完整内容（开头定义、结尾结论最有价值），中间压缩为摘要。摘要内容由一个小型 LLM 调用生成，或使用行数统计 + 关键词频次。

### 4. 工具依赖声明

某些工具之间存在前置依赖——工具 A 的输出是工具 B 的输入：

```
依赖声明接口：
  interface ToolDependency:
    tool_name: string          // 当前工具名
    depends_on: string[]       // 依赖的工具名称列表
    resolver: function         // 如何从依赖结果中提取参数

示例：
  Tool("generate_report") depends_on ["user_query_analysis", "data_fetch"]
  → 先执行 user_query_analysis 和 data_fetch，取其结果传给 generate_report
```

执行调度时，依赖图决定调用顺序：无依赖的工具可并发，有依赖的需等待上游完成。

### 5. 工具延迟加载策略

不要每次请求都发送所有 43+ 个工具定义给 LLM——上下文窗口是稀缺资源。

```
策略分类：

  A. 静态分类加载
     将工具分为核心组（必发）和扩展组（按需发）
     核心组：read_file, write_file, search, execute_command
     扩展组：preview_url, deploy, database_query ...
     每次请求只带核心组 + 最近使用过的 5 个扩展工具

  B. 动态相关性加载
     根据用户输入做关键词匹配，选择相关工具子集
     用户说"部署"  → 加载 deploy 组（git, docker, cloud）
     用户说"查日志" → 加载 diagnose 组（grep, log_parse, tail）

  C. 上下文自适应
     跟踪工具使用频率，高频工具常驻，低频工具按需请求
     维护 LRU 缓存：最近 10 次对话中未使用的工具延迟到下次请求
```

### 6. MCP 工具适配器

MCP（Model Context Protocol）定义了工具发现和调用的标准协议。项目需提供适配层将外部 MCP Server 的工具映射为内部 Tool 接口：

```
MCP适配器抽象：
  interface MCPAdapter:
    connect(server_config)        → 建立与 MCP Server 的连接
    list_tools()                  → 获取 MCP Server 的工具清单
    call_tool(name, arguments)    → 调用远程工具
    disconnect()                  → 断开连接

  // MCP 工具包装为内部 Tool：
  class MCPToolWrapper implements Tool:
    inner_tool: MCPRemoteTool    // 远端工具定义
    adapter: MCPAdapter           // 连接句柄
    
    execute(args):
      return adapter.call_tool(inner_tool.name, args)
```

关键差异：**
- **内置工具**在 LLM 沙箱/隔离环境中执行，受安全策略控制
- **自定义工具**（含 MCP 工具）在客户端侧执行，拥有真实系统权限

---

## 抽象接口层

> **以下仅定义接口契约和设计意图，不包含可执行的代码实现。AI 应根据这些契约构建具体代码。**

### Tool 接口

```
interface Tool:
    name: string
        // 工具唯一标识，LLM 通过此名调用
    description: string
        // 写给 LLM 的 Prompt 级描述：
        //   - 功能说明（做什么）
        //   - 使用时机（何时用，何时不用）
        //   - 参数说明（每个参数的含义、类型、约束）
        //   - 返回值说明（数据结构、字段含义）
        //   - 常见误用提示
    input_schema: JSONSchema
        // 参数 JSON Schema，定义：
        //   - type（参数类型）
        //   - properties（参数字段定义）
        //   - required（必填字段）
        //   - 每个属性的 type, description, enum, minimum, maximum
    category: ToolCategory
        // 分类：FILE | NETWORK | SHELL | DATABASE | EXTERNAL | CUSTOM
    concurrency_mode: enum { READ_ONLY, WRITE, MIXED }
        // 并发模式标记，决定分区算法如何处理此工具
    dependencies: ToolDependency[]
        // 前置依赖声明，为空则无依赖
    execute(args: Dict) → ToolResult
        // 执行工具逻辑，返回统一结构

interface ToolResult:
    success: bool
    data: any            // 成功时的数据
    error: string?       // 失败时的错误信息
    truncated: bool      // 结果是否被截断
    truncated_info: {    // 截断信息（仅被截断时有）
      original_length: int
      truncated_length: int
    }
```

### ToolRegistry 接口

```
interface ToolRegistry:
    register(tool: Tool)
        // 注册工具，重名时抛出或覆盖
    unregister(name: string)
        // 注销工具
    get(name: string) → Tool
        // 按名获取工具
    list_all() → Tool[]
        // 返回所有已注册工具
    get_for_llm(context_hint: string?, limit: int?) → ToolDefinition[]
        // 返回发给 LLM 的工具定义子集
        // context_hint: 上下文提示（用户意图），用于动态筛选
        // limit: 最大返回数量，默认核心组大小
        // 内部执行延迟加载策略
    execute_batch(calls: ToolCall[]) → ToolResult[]
        // 批量执行工具调用
        // 内部执行分区算法：只读并发 + 写入串行
        // 内部执行依赖解析：检查依赖图并排序
```

### 工具分区调度器（Scheduler）

```
interface ToolScheduler:
    schedule(calls: ToolCall[], config: ConcurrencyConfig) → SchedulePlan
        // 输入：LLM 返回的一批工具调用
        // 输出：调度计划（执行顺序 + 并发分组）
        // 
        // 步骤：
        //   1. 构建依赖图（DAG）
        //   2. 拓扑排序确定层级
        //   3. 每层内按 concurrency_mode 分区
        //   4. 只读组 → 并发执行（上限 max_concurrent）
        //   5. 写入组 → 串行队列
        //   6. 所有结果集会合并返回

    truncate_results(results: ToolResult[]) → ToolResult[]
        // 对超长结果应用截断策略
```

---

## AI 构建提示

构建此 Phase 时，AI 应按以下优先级决策：

### 优先级 1：Schema 定义先于实现

工具 Schema 是合约。先定义所有工具的 Schema（名称、描述、参数、返回结构），再逐个实现处理函数。描述质量直接决定 LLM 调用准确率——花 60% 时间在描述上，40% 在实现上。

### 优先级 2：工具分类

按 Claude Code 的分类体系组织工具：

| 类别 | 职责 | 示例工具 |
|------|------|---------|
| **agent** | Agent 自身控制 | task, delegate, abort |
| **workflow** | 流程与协作 | plan, verify, ask_user |
| **task** | 通用任务执行 | read_file, write_file, bash, search, grep, glob |
| **plan** | 计划与分析 | think, analyze, research |
| **advanced** | 高级/集成 | web_fetch, mcp_delegate, memory, database |

### 优先级 3：错误处理协议

所有工具必须遵循统一错误协议：捕获异常 → 包装为标准 ToolResult（含 error 字段）→ 绝不向上抛出未处理异常。Agent 核心循环依赖这一协议判断是否继续。

### 优先级 4：输出格式化

工具返回数据若为结构化对象，应格式化为 Markdown 或人类可读文本后再存入上下文。LLM 对结构化 Markdown 的理解优于 raw JSON。

---

## 规模适应性指南

### Minimal（原型/小项目）
- **工具数量**：3-5 个基础工具（read_file, write_file, search, bash, web_fetch）
- **注册表**：简单 Dict/map 结构，无需 Tool 类抽象
- **并发**：不需要分区，所有工具串行执行
- **截断**：简单按字符数硬截断，无摘要
- **MCP**：不接入

### Professional（团队项目/正式产品）
- **工具数量**：10-20 个，覆盖文件、网络、Shell、数据库
- **注册表**：ToolRegistry 类 + Tool 接口，Schema 验证
- **并发**：实现分区算法，只读 > 5 个时并发
- **截断**：头尾保留 + 中部摘要
- **MCP**：MCPAdapter 接口 + 基础实现，支持 1-2 个外部工具
- **延迟加载**：静态分类加载（核心组 vs 扩展组）
- **工具分类**：按 Category 枚举组织

### Enterprise（高可用/多租户/多 Agent）
- **工具数量**：50+，含 MCP 接入的外部工具生态
- **注册表**：支持动态注册/注销、工具版本管理
- **并发**：完整依赖图 + 并发调度器 + 最大并发数可配
- **结果缓存**：相同参数 + 短时间内重复调用的只读工具，缓存结果
- **工具热重载**：不重启 Agent 即可加载新工具定义
- **延迟加载**：上下文自适应 + 相关性动态加载
- **MCP**：多适配器实例，连接池管理，断线重连
- **安全沙箱**：内置工具限制文件系统访问范围，自定义工具记录审计日志

---

## 检查清单

- [ ] 每个工具的 description 是否按 Prompt 标准撰写（功能 + 场景 + 参数 + 返回说明）？
- [ ] 每个工具的 input_schema 是否完整（type, properties, required, 各属性描述）？
- [ ] 是否标记了每个工具的 concurrency_mode（READ_ONLY / WRITE）？
- [ ] 工具依赖是否显式声明（如有）？
- [ ] ToolRegistry 是否实现了分区调度逻辑（只读并发 + 写入串行）？
- [ ] 是否有结果截断机制（头尾保留 + 中部摘要）？
- [ ] 是否实现了延迟加载（不全量发送给 LLM）？
- [ ] 所有工具是否遵循统一错误协议（捕获 → 包装 → 返回 ToolResult）？
- [ ] 工具注册/注销是否线程安全（如需要）？
- [ ] MCP 适配器是否抽象了 connect / list_tools / call_tool 接口？

---

## 常见陷阱

### 陷阱 1：工具描述太简略 → LLM 参数错误频发

**症状**：LLM 调用工具时缺少 required 参数、参数类型不匹配、选错工具。
**根因**：描述只有一句话，没有说明参数语义和使用场景。
**解法**：工具描述按 "功能 → 时机 → 参数 → 返回 → 反面示例" 结构撰写，每个参数单独说明类型、格式、约束、默认值。

### 陷阱 2：所有工具全量发送 → 上下文超限

**症状**：工具太多（40+），每次请求上下文被工具定义占去 30%+。
**根因**：ToolRegistry.get_for_llm() 直接返回全量列表，无筛选。
**解法**：实现延迟加载策略——核心组常驻，扩展组按需；或基于用户意图做关键词匹配筛选。

### 陷阱 3：写入工具并发 → 数据竞争

**症状**：LLM 一次返回 3 个 write_file 调用，并发执行导致同文件被覆盖或部分写入。
**根因**：未对工具做并发安全标记，所有工具一律并发。
**解法**：实现分区算法，标记每个工具的 concurrency_mode，写入类工具强制进入串行队列。

### 陷阱 4：工具结果未截断 → Token 浪费

**症状**：read_file 返回 8000 行代码，全量存入上下文，后续对话 token 严重不足。
**根因**：没有结果截断策略，或简单硬截断丢失关键信息。
**解法**：头尾保留 + 中部摘要的截断策略，保留开头定义和结尾结论，中部用行数统计或关键词摘要替代。

### 陷阱 5：忽略工具依赖 → 执行顺序错误

**症状**："生成报告"工具在"获取数据"工具之前执行，拿到空数据报错。
**根因**：工具由 LLM 并行返回，但注册表不关心依赖关系，直接并发全部。
**解法**：支持 Tool.dependencies 声明，调度器构建依赖图，拓扑排序后再分区执行。

### 陷阱 6：沙箱 vs 客户端权限混淆

**症状**：自定义工具在客户端侧拥有完整系统权限，导致误删文件或执行危险命令。
**根因**：未区分内置工具（沙箱执行）和自定义/MCP 工具（客户端执行）的权限边界。
**解法**：内置工具限制文件系统访问范围（如 workdir 白名单），自定义工具添加权限确认（如 ask_user 确认危险操作）和审计日志。

### 陷阱 7：Schema 与实现不一致

**症状**：Schema 定义了 param_X，但 execute 实现里读取的是 param_x（大小写不匹配）。
**根因**：Schema 定义和代码实现各自维护，未做一致性校验。
**解法**：编写 Schema 一致性测试——对每个工具用 Schema 生成 mock 参数，调用 execute 验证不报错。

---

## 下一步

完成 Phase 3 后，进入 **Phase 4: Agent 核心循环**（参考 `references/04-phase-agent-loop.md`）