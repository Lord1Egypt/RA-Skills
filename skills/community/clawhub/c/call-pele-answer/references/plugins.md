# 扩展：八个积木

内置能力和第三方插件走同一个注册 API（`scripts/core/registry.mjs`）。一个插件是一个 ES 模块：

```js
export default {
  name: 'my-plugin',
  apiVersion: 1,            // 与核心不匹配时拒绝加载
  setup(api) { /* api.form / router / routerSpec / adapter / theme / output / rule / deriver */ },
};
```

在配置里登记（`~/.call-pele-answer/config.json` 或项目根目录的 `.call-pele-answer.json`）：

```json
{
  "plugins": ["./plugins/kpi.mjs", "some-npm-package"],
  "adapters": [{ "name": "my-proxy", "kind": "native", "url": "https://…/v1/systemone", "keyEnv": ["MY_KEY"] }],
  "routers":  [{ "name": "proxy-full", "strategy": "full", "adapter": "my-proxy", "fallback": "classifier" }],
  "router": "proxy-full",
  "theme": "pele",
  "policy": { "device": "desktop", "budget": { "interactive": 2 } }
}
```

优先级（后者覆盖前者）：内置默认 < 用户配置 < 项目配置 < 环境变量（`PE_ROUTER`、`PE_THEME`）< 命令行参数。`pe info` 列出当前加载的全部积木。

## 1. form：一种内容形式

```js
api.form({
  name: 'kpi',
  fences: ['kpi'],                     // 认领哪些围栏；后注册的覆盖先注册的
  routes: ['chart'],                   // 可选：它服务于哪些形式族（文档用途）
  parse(node, ctx) { node.data = … },  // 围栏正文 → IR；ctx.parseBody(lines, line) 解析嵌套内容，ctx.err/warn 报错
  render: {                            // 每个输出一个渲染函数；缺的输出自动降级为代码块/原围栏
    html: (n, r) => `…`,               // r.esc / r.inline / r.nodes(children)
    markdown: (n, r) => `…`,
  },
  lint(node, report) {},               // 可选：形式自己的检查
  assets: { css: '…', js: '…' },       // 可选：只在页面用到这个形式时内联
});
```

CSS 只用 `--pe-*` 令牌，换主题时自动适配。JS 运行在页面的 IIFE 里，`PE.reduce` 表示用户偏好减少动态效果。

## 2. adapter：谁来回答（System One 适配器）

```js
ask(states: string[], questions) → Promise<answers[]>   // answers 为 System One 形状
```

- `native`：线上说 System One 协议（每个 state 一次调用，问题在调用内并行）。TypeSafe 直连、classifier.dev 转发、自建代理。只需配置，不用写代码。
- `shim`：在只会“多文本 × 一组标签”的批量分类接口上模拟 System One（每个问题一次批量调用）。
- 自定义：本地小模型、规则引擎、LLM 调用，只要实现 `ask` 就能接入。

## 3. router / routerSpec：问什么

推荐声明式：`{ name, strategy: 'fast' | 'full' | 'hybrid' | 'local', adapter, gateAdapter?, fallback? }`。

- `fast`：形式族 + 图类型。
- `full`：再加门控问题（真实数字？来源？分支？多方案？复杂度？），用置信度门控改判。
- `hybrid`：`fast` 定形式，只对关键块用 `full` 复核。
- 失败沿 `fallback` 链降级，最后总有 `local`。

也可以直接注册 `api.router({ name, route(texts) → { blocks, by } })`。

## 4. deriver：不经模型直接生成形式

```js
api.deriver('chart', block => ({ label: '指标卡', md: '```kpi\n…\n```' }) ?? null);
```

同一块有两种以上派生结果时，脚手架把它们放进 ```` ```views ````，读者在页面上切换。内置派生器在前，插件派生器追加在后。

## 5. theme：令牌 + 页面 CSS

```js
api.theme({ name: 'my-theme', css: ':root{--pe-paper:…;--pe-ink:…} …', js: '' });
```

必须定义 `aesthetic.md` 里的全部 `--pe-*` 令牌（浅色和深色），这样所有形式（包括插件形式）都能被正确着色。

## 6. output：输出目标

```js
api.output({ name: 'slides', ext: 'html', write(doc, ctx) { … } });
```

输入是 IR v1（见 `scripts/core/markdown.mjs` 顶部注释）。用 `createRenderer(registry, '<target>')` 复用各形式的渲染函数；形式没有该目标的渲染函数时自动降级。

## 7. rule：检查规则

```js
api.rule({ id: 'finance/source', check(doc, report, ctx) { /* report(line, rule, message, fix) */ } });
```

规则 id 以 `route/` 开头的归为“形式选择”警告，其余归为“文字”警告。

## 契约与版本

- **IR v1**：只增不改字段。破坏性变更时 `IR_VERSION` 升到 2。
- **API v1**：注册 API。变化时 `API_VERSION` 升级，旧插件会被明确拒绝，而不是悄悄出错。
- 示例插件：`examples/plugins/kpi.mjs`（form + deriver + lint）。


## palette：调色器的页面预设与色板

```js
export default { name: 'my-palettes', apiVersion: 1, setup(api) {
  // 色板：一个色相的三档（浅 / 中 / 深）。放在组件上：中 → 强调色与第一系列色，浅 → 浅色模式底色，深 → 深色模式底色
  api.palette({ kind: 'swatch', name: 'sage', label: '鼠尾草', l: '#C9D8C0', m: '#5E7F52', d: '#24331F' });
  // 页面预设：覆盖 --pe-* token，浅色和深色各一套
  api.palette({ kind: 'page', name: 'night', label: '夜读', light: { '--pe-paper': '#F7F4EE' }, dark: { '--pe-paper': '#0B0B0C' } });
} };
```

同名后注册的覆盖先注册的。内置：页面 墨纸（默认）/ 暖纸 / 蓝图；色板 番茄 / 芥末 / 薄荷 / 钴蓝 / 腮红 / 青 / 紫 / 石墨。

## annotation：批注类型

```js
export default { name: 'my-notes', apiVersion: 1, setup(api) {
  // 读者给一块内容打的标签；color 用作标记色和底栏计数色，按钮上是白字，选中深一点的颜色
  api.annotation({ name: 'typo', label: '错字', color: '#C26A84' });
} };
```

内置：疑问（钴蓝）/ 建议（芥末）/ 认可（薄荷）/ 顾虑（番茄）。同名覆盖。复制出的批注写类型的 label，所以 Agent 读到的是「[错字]」。
