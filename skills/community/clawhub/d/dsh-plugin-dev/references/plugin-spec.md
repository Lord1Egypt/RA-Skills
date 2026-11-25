# DSH 插件技术规范（基于官方文档 dsh-v0.1.1-rc.2 实证）

> 来源：deepseek-harness.github.io（cordis-primer / cordis-tutorial / develop/basic 系列）
> 与社区实证指南 github.com/anweat/dsh-plugin-dev-guide。

## 1. 插件是什么

插件 = 一个导出 `apply` 函数的 ES 模块。框架加载时调用 `apply(ctx)`，通过 `ctx` 注册能力。
注册都是可逆副作用：插件卸载/HMR 时自动撤销，无需手动 removeListener/clearInterval。

三种形态（多数情况用函数形式）：

```js
// 函数形式（推荐）
export const name = 'my-plugin'        // 可选，插件标识
export const inject = ['tools']        // 可选，依赖的服务 key
export function apply(ctx) { /* ... */ }

// 对象形式
export default { name: 'my-plugin', inject: ['tools'], apply(ctx) { /* ... */ } }

// 类形式（需要对外提供服务时）
import { Service } from '@deepseek-ai/cordis'
export default class MyService extends Service {
  static inject = ['tools']
  constructor(ctx) { super(ctx, 'myService') }
}
```

需要手动清理的资源用 `ctx.effect(() => { ...; return () => cleanup() })`。

## 2. 核心概念

- **ctx = 服务容器**：`ctx.tools`、`ctx.llm`、`ctx.sessions`…按 key 取服务，不 import 具体实现。
- **inject 声明依赖**：框架等依赖就绪后才调用 `apply`。加载顺序由服务依赖表达，不按配置行序。
- **配置**：`export interface Config` + 同名 Schemastery schema；`apply(ctx, config)` 拿到校验并填好默认值的配置。不要导出普通对象当 `Config`（不满足 Standard Schema 接口）。

```js
import Schema from '@deepseek-ai/schemastery'
export const Config = Schema.object({
  endpoint: Schema.string().required(),
  timeoutMs: Schema.number().default(30000),
})
```

设计原则：**可调参数一律进 Config**（检验标准：能否不改代码在 cordis.yml 里改值）；配置错误要响亮（加载即失败）。

## 3. 注册工具（最常见插件类型）

```js
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'greet-tool'
export const inject = ['tools']

export function apply(ctx) {
  ctx.tools.register(defineTool({
    name: 'greet',
    description: 'Greet someone by name.',
    parameters: { name: { type: 'string', required: true, description: 'Who to greet' } },
    output: {
      schema: { type: 'string' },                                    // execute 返回的规范值
      render: (_args, value) => [{ type: 'text', text: value }],     // 转成面向模型的内容
    },
    async execute(args) { return `Hello, ${args.name}!` },
  }))
}
```

- `defineTool` 把 `parameters` 规约为给模型看的 JSON Schema，并在 `execute` 前校验模型实参。
- 注册 disposer 自动附着到插件，卸载即注销。
- 组合时需要 `@deepseek-ai/dsh-system-prompt` 在场（工具要向系统提示词贡献 schema），缺提供方则插件一直 PENDING。
- 观察工具结果：`ctx.on('tools/result', (exec, result) => { ... })`（`import type {} from '@deepseek-ai/dsh-tools'` 引入事件类型）。
- 更丰富能力（嵌套 schema、后台工作、策略钩子、UI 卡片）见官方 `docs/cookbook/adding-a-tool.md`。

## 4. 事件分发（五种模式）

| 模式 | await？ | 顺序 | 返回值 |
|---|---|---|---|
| `emit` | 否 | 按注册序观察 | 无 |
| `waterfall` | 否 | 按注册序，环绕中间件 | 有（逐层包装） |
| `parallel` | 是 | 并行扇出 | 无 |
| `serial` | 是 | 按序执行 | 有 |
| `bail` | 否 | 直到某监听器返回 bail 值 | 有 |

waterfall 短路语义：监听器收到 `(...args, next)`；调 `next()` 委托下游，不调直接返回即短路。
策略类监听器拥有决策权时可短路；仅观察/标注的监听器必须委托。

## 5. bundle manifest（发布包的硬门槛）

可安装的**组合包（bundle）**由 package.json 声明：

```json
{
  "name": "dsh-hello-plugin",
  "version": "0.1.0",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "cordis.patch.yml"],
  "dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
}
```

`cordis.patch.yml` 是标准补丁行，**`name` 写包名**（Node 模块解析），不是源码路径：

```yaml
- insert:
    - id: hello
      name: dsh-hello-plugin
      # scoped 包名必须加引号（@ 是 YAML 保留字符）：name: '@scope/dsh-hello-plugin'
```

规则：

- **没有 `dsh.bundle` 的包仍可安装，但只作为普通依赖**：`dsh plugin` 打印警告，不激活任何层。
- `patch` 可为有序文件列表 `["./base.patch.yml", "./web.patch.yml"]`，相对路径按各文件所在目录解析。
- 可选 `"engines": { "dsh": ">=0.2.0 <0.3.0" }` 声明兼容范围；不满足则安装/启动拒绝。
  （注意 SemVer 预发布版本的匹配规则，拿不准就省略 engines.dsh，让 peer 依赖范围兜底。）
- `files` 必须包含入口文件与 patch 文件，否则 npm 包缺件。
- patch 也接受 `config:` 键，随行传给插件的 Config schema。

## 6. 层顺序（谁覆盖谁）

生效配置 = 空根之上按序叠加：

1. profile 的 `dsh.profile.bundles` 各组合包层（按加入顺序，`@deepseek-ai/dsh-base` 在前）
2. profile 自己的 `cordis.patch.yml`
3. home 级 `$DSH_HOME/cordis.patch.yml`
4. 各 `--patch` overlay（按 argv 顺序）

后层按行（id）胜出；**`config` 整块替换，不是深度合并**——覆盖一行必须重述该行全部键。
用户可在自己 profile 里覆盖你的行，所以默认值给用户大概率保留的，其余交给 schema。

## 7. 依赖规则

- `@deepseek-ai/*` 必须是**已发布版本**，禁止 `workspace:*`。
- 与宿主共享实例的包（cordis、dsh-tools 等）声明为 **optional peerDependencies**（精确范围最佳），devDependencies 镜像一份供独立测试；不要装成插件私有运行时副本。
- Cordis 服务按全局 symbol key 品牌化，插件自带的 `@deepseek-ai/cordis` 副本与 harness 内副本天然互操作。
- 无状态第三方依赖放 `dependencies`。

## 8. 原生行为陷阱（实测确认）

1. **激活顺序按服务可用性，不按行序**：`inject` 的服务一就位插件即激活。`apply()` 里读全局注册表多半是空的；要全局视图得等 boot 之后。
2. **撞名即抛错**：路由、RPC 通道、工具名、`single`/`keyed` 槽位撞名一律抛错（只有 `list`/`chain` 槽相加）。把包名放进路径/命名前缀，跨包撞车几乎不可能。
3. **entry list 不是全部**：插件可在自己 `apply` 里挂子插件，这些包名不会出现在组合配置里。判断"装了什么"要按 `peerDependencies` 闭包展开。
4. **git 安装拉的是源码不是产物**：TS 包必须给自包含 `prepare` 脚本；且 pnpm ≥10 要求用户把包 key 加进 profile 的 `pnpm-workspace.yaml` `allowBuilds:` 白名单。**纯 JS 包无此坑**。
5. **`!!js` 表达式**在注入就绪后基于插件上下文插值；`--help` 时提供方不发布服务，相关行不激活。
6. YAML 中 `@` 开头的纯标量非法——scoped 包名在 patch 里必须加引号。

## 9. 环境基线

- Node ^22.19 || >=24；Corepack + pnpm（基线 `pnpm@11.7.0`）
- DSH 源码运行：克隆 deepseek-ai/deepseek-harness → `corepack pnpm install && corepack pnpm run build` → `corepack pnpm dsh ...`
- 开发期加载本地插件：`pnpm dsh web --patch ./your-plugin/cordis.yml`（patch 里 name 用**绝对路径**指向 TS/JS 源码；bundle 包才用包名）
