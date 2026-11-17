# Fiber / effect / 生命周期

## Fiber 状态机

```
        ctx.plugin(plugin, config)
                 │
                 ▼
             ┌────────┐  依赖未就绪   ┌─────────┐
             │ PENDING │────────────►│ LOADING │
             │ (等待依赖)│             └─────────┘
             └────────┘                  │ 依赖就绪
                 │                        ▼
                 │                 ┌──────────┐
                 │  config 校验失败/│  ACTIVE  │◄── apply() 已执行
                 ▼   apply 抛错    └──────────┘
             ┌────────┐                 │ dispose()/HMR
             │ FAILED │                 ▼
             └────────┘           ┌───────────┐
                                  │ UNLOADING │──effect 回卷──► 结束
                                  └───────────┘
```

## Fiber：插件的生命周期单元

- `ctx.plugin(plugin, config?)` 返回一个 **Fiber**（可 await 其加载完成）。
- Fiber 拥有自己的 effect 作用域：插件注册的所有监听器、服务、effect 都挂在它名下。
- `fiber.dispose()`（或根上下文的 `root.fiber.dispose()`）卸载插件：**先回卷全部 effect（含 disposer），再报告完成**。
- 每个插件每次 `ctx.plugin()` 调用对应一个 fiber；同一插件的多次挂载 = 多个 fiber。

## Fiber 状态

| 状态 | 含义 |
|---|---|
| `PENDING` | 等待 `inject` 依赖就绪（合法状态，不报错；提供方可能稍后挂载） |
| `ACTIVE` | 依赖就绪，`apply` 已执行 |
| `FAILED` | 配置校验失败或 `apply` 抛错 |
| `UNLOADING` | 卸载中（disposer 回卷） |

## effect：可逆副作用的唯一入口

```ts
ctx.effect(() => {
  // 安装阶段：注册资源
  const timer = setInterval(...)
  return () => clearInterval(timer) // disposer：卸载阶段回卷
}, 'effect-label') // label 用于 fiber 诊断
```

纪律（primer 明确要求）：
1. **每个注册都有 disposer**：要么从 `ctx.effect()` 返回，要么用框架辅助方法自动处理。
2. **teardown 顺序敏感的工作放同一 effect**：保证资源按预期顺序释放（后注册先回卷）。
3. 事件监听用 `ctx.on()`（自动注册/回卷）；一次性定时用 `@deepseek-ai/cordis-plugin-timer` 的 `ctx.timeout()` / `ctx.interval()`（随 fiber 清理）。

## 依赖驱动的生命周期（重要）

- `inject` 不是一次性启动检查：应用运行期间若依赖服务消失（提供方被卸载/热替换），**依赖插件自动卸载，服务恢复后自动重载**。
- 加载顺序由依赖图推导，与 `cordis.yml` 文件顺序无关。
- 消费方绝不会持有失效的服务引用——依赖消失时其注册同时撤销。

## HMR 行为

`@deepseek-ai/cordis-plugin-hmr` 监视文件，保存时执行"先卸载旧实例（effect 全回卷）→ 加载新代码 → 再跑 apply"。

- HMR 依赖 `timer` 服务（去抖）与 logger 控制台导出器，否则静默不工作且永远 PENDING。
- **cordis.yml 自身变更也触发更新**：loader 按 `id` 对比条目，只挂载/卸载/重配变化部分。
- **条目不带 `id` → 每次读文件都生成新 id → 任何编辑都被视为删除+新增，全量重挂**。务必给稳定 `id`。

## 进程退出语义

- PENDING 的 fiber 不保持 Node 事件循环活跃：组合中若没有其它运行项，进程会以状态码 0 **静默退出**（不是崩溃）。
- 插件 `apply` 抛错 → 进程以错误终止（加载失败明确报错，不静默跳过）。
- 模块解析失败（路径/包名拼错）→ logger 报告，不崩溃；启动阶段可能被吞，先查拼写。
