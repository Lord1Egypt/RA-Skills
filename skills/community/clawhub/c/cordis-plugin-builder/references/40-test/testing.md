# Cordis 插件测试方法论（真实上下文单测范式）

> 蒸馏自 001/Cordis.md 测试章节（2026-08）。核心原则：**放弃重度 Mock，采用真实 Context 单测**。

## 测试层次

```
┌──────────────────────────────────────────────┐
│ ① 单测（真实 Context + 最小 Fake 依赖）        │  ← 主力
│    new Context() + FakeTools + ctx.plugin()   │
│    验证 Fiber 状态 + 功能 + 配置校验           │
├──────────────────────────────────────────────┤
│ ② 装配冒烟（cordis.yml 集成）                 │
│    dsh --dump-config 看树 / 单文件启动器拉起   │
│    验证组合与配置插值                          │
├──────────────────────────────────────────────┤
│ ③ 可逆性测试（Cordis 特有）                   │
│    反复 load/dispose + 幽灵状态检查           │
│    卸载后副作用必须全部撤销                    │
├──────────────────────────────────────────────┤
│ ④ 通信拦截测试（事件域）                      │
│    waterfall 的 next()/短路/veto 行为         │
└──────────────────────────────────────────────┘
```

## 1. 建立单测环境（单插件验证）

不要模拟整个宿主环境，直接在测试中创建真实 Cordis 上下文：

```ts
import { Context } from '@deepseek-ai/cordis'
const ctx = new Context()
// 插件依赖的服务：手动挂载最小实现（真实 DI 容器内验证）
class FakeTools extends Service {
  readonly list: { name: string }[] = []
  constructor(ctx: Context) { super(ctx, 'tools') }
  register(t: { name: string }): void { this.list.push(t) }
}
new FakeTools(ctx)
await ctx.plugin(myPlugin, { /* config 必须显式传 */ })
```

**状态验证**：观察插件 Fiber 状态机是否从 `PENDING` → `ACTIVE`。停在 `PENDING` = `inject` 服务未就绪或服务名拼写错误（静默等待，不报错）。

## 2. 装配级集成测试（cordis.yml 冒烟）

- 用 DSH 内置单文件启动器：`node --import tsx ../../vendor/cordis/bin.js` 拉起环境
- 写临时 `cordis.yml`，把插件路径加入并传测试配置
- 观察输出：`dsh --dump-config` 查看插件树是否按预期构建、配置是否正确插值

## 3. 副作用与可逆性测试（Cordis 特有，关键）

确保"资源安全"（HMR 的前提）：

- **重复加载/卸载**：不重启进程，反复 `ctx.plugin` / dispose（或触发 HMR）
- **幽灵状态检查**：卸载后验证副作用完全撤销——注册的指令消失、定时器停止、监听器移除。卸载后行为变混乱 = 有副作用未通过 `ctx.effect()` 托管
- 原生 `setInterval`/`setTimeout` 等非框架托管资源必须 `ctx.effect()` 返回 disposer

## 4. 通信与拦截测试（事件域）

- **Waterfall 拦截器**：分别测试调 `next()` 与不调 `next()`（短路/Veto）的表现——只读监听器必须无条件委托，决策监听器才能否决
- **emit 广播**：验证正确发出持久"事实"到会话日志

## 5. 专用调试工具

| 工具 | 用途 |
|------|------|
| `dsh --dump-config` | 插件树构建与配置插值验证 |
| `dsh-plugin-check` | 检查 Manifest / Patch 逻辑 / 常见构建陷阱 |
| Trajectory（轨迹视图） | Web UI 监控插件在 Agent 循环哪一步触发、Token 消耗、报错归属 |
| schemastery | 故意传错误类型参数，观察 Loader 是否精准拦截 |

## 6. 工程原则（发布级护栏）

> 来源：DSH-Context-Pro 项目实测

### 6.1 静默降级必须有暴露通道

任何"失败就静默降级"的逻辑，都必须有可观测的暴露通道，否则退化会被长期掩盖（fail-closed 优于 fail-open）。该被看见的退化必须被看见。

### 6.2 工程门禁：报警器常鸣等于没有报警器

- 手工验证不是验证：`CI(typecheck 零容忍 + lint)` + `eslint 入门禁` + `prepublish 制品断言` 才是可靠门。
- 先清零噪声地板（全项目 tsc 0 错误基线），再谈零容忍。
- 制品断言是发布前最后一道闸（见 packaging.md 消费者回拉验证）。

### 6.3 排除式断言（负向门禁）

断言不仅能测"该在的在场"，还能守"不该回来的别回来"——任何曾经删错/加错过的重要内容，都值得一条反向断言，把"不回潮"固化成可执行不变式。

## 测试清单（交付前）

1. **加载测试**：依赖满足？Fiber 状态 ACTIVE？
2. **功能测试**：服务调用正常？事件拦截未漏 `next()`？
3. **清理测试**：dispose 后无幽灵状态？
4. **配置测试**：Config Schema 校验与脱敏正常？
