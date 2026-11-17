# 事件分发模式与 waterfall 语义

事件是插件间无需共享服务即可通信的通道。**分发模式是事件公开契约的一部分**——新的 harness 事件通过 `@mode` 标签记录模式，生成目录交叉校验声明与调用点。

## 注册：`ctx.on` / `ctx.once`

- 监听器用 `ctx.on(name, listener, options?)` 注册；`options` 布尔值简写为 `prepend`。
- 注册属于 effect：fiber 卸载自动移除监听器。
- `ctx.once` 首次触发后自毁。

## 五种分发模式（只能通过对应方法分发）

```
选哪种分发模式？
│
├─ 广播事实，无返回值          → emit（ctx.emit）        最常用：状态/创建/结束
├─ 并行扇出，全部 await        → parallel（ctx.parallel） 持久化检查点，互不干扰
├─ 顺序执行，失败即停          → serial（ctx.serial）     有顺序依赖的串联处理
├─ 同步短路，首个真值返回       → bail（ctx.bail）        取第一个"有决定"的监听器
└─ 环绕链，改值/否决/包装       → waterfall（ctx.waterfall）★最易踩坑
      监听器: (...args, next) => next() 并 return
```

| 模式 | 方法 | 是否 await | 顺序 | 返回值 |
|---|---|---|---|---|
| `emit` | `ctx.emit(name, ...args)` | 否 | 注册顺序观察 | 无 |
| `parallel` | `ctx.parallel(...)` | 是 | 并行扇出 | 无（聚合成 AggregateError） |
| `serial` | `ctx.serial(...)` | 是 | 注册顺序 | 首个 bail 值 |
| `bail` | `ctx.bail(...)` | 否 | 注册顺序 | 首个 bail 值（同步） |
| `waterfall` | `ctx.waterfall(...)` | 否 | 注册顺序（外层优先） | 最外层监听器返回值 |

## waterfall 语义（最容易踩坑）

**分发签名**：`ctx.waterfall(name, ...args, innerNext)` —— 最后一个参数是内层 `next`。

**监听器签名**：`(...args, next)`，用 `ctx.on` 注册（`ctx.waterfall(name, fn)` 不是注册！那是分发，`fn` 会被当作内层 next）。

**核心语义**（实测自 vendor/cordis v4 源码）：
- 监听器收到 `(...args, next)`；`next()` 执行下游（更内层的监听器，最后是 `innerNext`）。
- **`next(新值)` 传参被忽略**——`next` 闭包捕获的是原始 args 数组，你传给 `next` 的参数不会传给下游。
- **正确包装姿势**：`const result = next(); return 包装(result)`。
- **短路（veto）**：不调用 `next()` 直接返回 → 下游全部跳过，返回值为该监听器的返回值。

```ts
// ✅ 正确：取下游返回值再包装
ctx.on('decorate', (text, next) => {
  const result = next()
  return `${result}!`
})

// ❌ 错误：传参给 next() 会被静默忽略，下游收到的是原始 args
ctx.on('decorate', (text, next) => next(`${text}!`))
```

```ts
// 分发：最后一个参数是内层 next
const out = await ctx.waterfall('decorate', 'hello', (v) => v) // -> 'hello!'
```

**协作模式**：监听器修改共享的请求/决策对象后委托 `next()`（对象引用共享，修改对下游可见）；单决策事件中，拥有决策权的策略监听器可以短路返回，仅观察的监听器必须委托。

**顺序控制**：`prepend: true` 只在必须早于普通注册运行时使用。

## 内置框架事件（internal/*，扩展点）

- `internal/plugin(fiber)` / `internal/status(fiber, old)`：fiber 生命周期观察。
- `internal/config`（waterfall）：插件配置解析前拦截。
- `internal/service(ctx, name, value)`：服务绑定拦截。
- `internal/update`（waterfall）：fiber 配置更新，跳过 `next()` 可否决。
- `internal/get` / `internal/set`（waterfall）：上下文代理读写拦截（服务隔离/拦截的底层）。
- `internal/listener`（bail）：监听器注册拦截，非空返回值可替换注册。
- `internal/dispatch`（emit）：任何非 internal 事件分发前触发（事件总线诊断）。

## 类型化事件（TS 声明合并）

```ts
declare module '@deepseek-ai/cordis' {
  interface Events {
    'app/ready'(message: string): void
    'internal/config'(this: Fiber, config: any, next: () => any): any // @mode waterfall
  }
}
```

事件名建议带命名空间前缀（如 `app/`、`internal/`），避免与其它插件冲突。

## 7. 实战沉淀：waterfall 监听器标准模板

> 来源：DSH-Context-Pro 项目实测

监听 waterfall 事件（如 `agent/pre-step`）的标准三段式代码模板：

```ts
import '@deepseek-ai/dsh-agent'   // ① 副作用导入触发 Events 声明合并
import type { PreStepDecision } from '@deepseek-ai/dsh-agent'

ctx.on('agent/pre-step', async (
  payload: { agent: unknown; messages: UserMessage[]; turn: number; step: number; signal: AbortSignal },
  next: () => Promise<PreStepDecision>,
): Promise<PreStepDecision> => {
  const decision = await next()                      // ② 先委托下游（取返回值，不传参）
  if (decision.kind !== 'enter') return decision      // 只处理 enter 类型
  const messages = decision.messages.flat() as UserMessage[]  // ③ 展平拓宽类型
  // ... 注入后返回 —— ⚠️ 返回的 messages 必须扁平：
  return { ...decision, messages: appendContextToMessages(messages, injected) } as PreStepDecision
  // 错误写法：[...messages, appendContextToMessages([], injected)] 会嵌套数组，模型无法应答
})
```

**关键纪律**：
1. **副作用导入**：`import '@deepseek-ai/dsh-agent'` 触发 `declare module` 的 Events 合并——只 `import type` 不触发合并。
2. **先委托后包装**：`const decision = await next()` 取下游返回值，传参给 `next()` 会被静默忽略。
3. **返回扁平数组**：messages 必须是一维数组，每元素是 `{role, content}` 对象——嵌套数组会被写入 session 作为单条"消息"，导致模型无法应答。
4. **`ctx.provide` 非 Service 不可 await**：只有 `Service` 子类注册才是可等待服务；普通对象 provide 走 Proxy 惰性解析，`await ctx.serviceName` 永远 undefined。注册服务用 `Service` 子类（构造即注册）。
