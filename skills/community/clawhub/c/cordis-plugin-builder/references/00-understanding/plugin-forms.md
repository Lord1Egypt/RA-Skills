# 插件形态与完整模板

Cordis 接受三种插件形态（教程第 1 章）。默认用函数形态；需要公开服务时用类形态。

## 形态选择脑图

```
要写什么插件？
│
├─ 只是注册副作用/监听/工具（不需要被别处调用）→ 函数插件（默认）
│     export function apply(ctx) { ctx.on(...); ctx.tools.register(...) }
│
├─ 要公开 ctx.<service> 能力供其他插件调用 → Service 子类
│     声明合并 declare module + class Xxx extends Service
│     apply 里 ctx.plugin(XxxService)
│
└─ 特殊场景（无函数、无类，纯配置对象）→ 对象插件
       { name, apply(ctx) }
```

> 判断口诀：**能力要被"消费"才用 Service**；只"产生活动"用函数；其余不常用。
> Service 子类构造即注册（`super(ctx, 'name')`），消费方按名引用、不 import 提供方。

## 1. 函数插件（默认）

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'hello'

export function apply(ctx: Context) {
  // 注册你的副作用：ctx.on / ctx.effect / ctx.plugin ...
}
```

- `name` 是模块级导出（显示用），不要给函数对象赋 `name` 属性——ES 严格模式下函数 `name` 只读。
- loader 挂载时用上下文调用 `apply`；插件描述自己的贡献，`cordis.yml` 组合应用。

## 2. 对象插件（特殊场景）

```ts
export const objectPlugin = {
  name: 'object-plugin',
  apply(ctx: Context) {
    // ...
  },
}
```

## 3. Service 子类（公开 `ctx.<service>` 能力）

```ts
import { Service, type Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Context {
    greeter: GreeterService
  }
}

export class GreeterService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'greeter') // 以 'greeter' 注册到上下文
  }
  greet(who: string) {
    return `Hello, ${who}!`
  }
}

export const name = 'greeter'

export function apply(ctx: Context) {
  ctx.plugin(GreeterService) // Service 子类本身就是插件
}
```

两部分协同：
- **运行时**：`super(ctx, 'greeter')` 注册实例，任何插件经 `ctx.greeter` 访问；注册属于 effect，提供方卸载即移除。
- **编译时**：`declare module` 声明合并只提供类型，不产生运行时接线；缺失时服务仍工作但消费方失去类型安全。

## 带 Config schema 的可配置插件

```ts
import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'

export const name = 'config-demo'

export interface Config {
  greeting: string
  targets: string[]
}

// 类型与运行时 schema 同名导出：消费方得类型，Cordis 得验证器
export const Config: Schema<Config> = Schema.object({
  greeting: Schema.string().default('Hello'),
  targets: Schema.array(String).default(['world']),
})

export function apply(ctx: Context, config: Config) {
  for (const target of config.targets) {
    console.log(`${config.greeting}, ${target}!`)
  }
}
```

要点：
- `apply` 永远收到完整且校验过的 config（schema 默认值补齐缺省字段）。
- 无效配置 → `ValidationError: invalid config: ...`，fiber 进 FAILED，进程按启动器策略报错退出。
- `Config` 必须是 Standard Schema（schemastery 是仓库标准）；导出普通对象无效。
- schema 验证通过但引用的资源/提供方不可用时，插件应在能解析引用时立即拒绝。

## 消费服务：inject 与可选依赖

```ts
// 硬依赖：保持 PENDING 直到所有依赖就绪
export const name = 'consumer'
export const inject = ['greeter']

export function apply(ctx: Context) {
  console.log(ctx.greeter.greet('world'))
}
```

```ts
// 可选依赖：不 inject，运行时探测
export function apply(ctx: Context) {
  const greeter = ctx.get('greeter') // 无提供方时为 undefined
  console.log(greeter?.greet('maybe') ?? 'no greeter available')
}
```

- `inject` 是**持续**依赖跟踪：服务运行时消失（卸载/热替换）→ 依赖插件随之卸载，恢复后再加载。防止消费方持有失效引用。
- 这就是"配置可替换服务"的基础：卸载 `dsh-bash-local`、挂载另一个 `shell` 提供方，所有 `inject: ['shell']` 的插件自动切换到新实现。

## 服务命名

- 服务名共用**一个扁平命名空间**：加辨识前缀，避开已占用名称（`tools`/`llm`/`agents`/`sessions`/`skills`/`goals`/`fs`/`timer` 等）。
## 部署形态与配置文件对应关系

不同部署形态所需的配置文件差异很大，选型前快速对照：

| 部署形态 | 配置文件 | 说明 |
|---------|---------|------|
| 动态插件 (`cordis_define`) | 无 | 纯 JS 代码直接提交，不涉及磁盘文件 |
| 函数插件（声明式装配） | `package.json` + `Config schema` + `cordis.patch.yml` | `package.json` 需配置 `type: "module"` 和 `exports`；`Config` 用 schemastery 编写；`cordis.patch.yml` 定义装配位置 |
| Service 子类（声明式装配） | 同上 + `declare module` 声明合并 | 额外需声明合并文件提供类型安全 |
| 对象插件（声明式装配） | 同上 | 与函数插件一致 |

> 快速验证思路用动态插件，正式功能固化为声明式装配。
