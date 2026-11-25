---
subdomain: vite-tooling
version: 11
updated: 2026-11-17
---
# Vite 工具链

## 定位与心智模型

Vite（当前 **8.3.8**，npm registry 复核 2026-11-17）是前端构建工具：**dev 用原生 ESM 按需转换（毫秒级冷启）、build 用 Rolldown 驱动**——advanced tree-shaking、内置 minification、fine-grained chunking [官方文档](https://vite.dev)。心智模型一句话：**dev 与 build 是两条管线**（v8：dev 原生 ESM+Oxc / build Rolldown；esbuild 与 Rollup 已被整体替换），"dev 好的 build 崩"多源于插件只在一条管线生效。

理解三条主线：**配置分层**（vite.config + `.env.[mode]` + 插件）、**模式机制**（mode ≠ NODE_ENV）、**插件钩子**（Rollup 接口扩展 + Vite 特有 apply/enforce）。

## 法则

[VT-1] **MUST**: 生成 Vite 配置前确认版本（当前 8.3.8，Rolldown+Oxc 构建）（全局宪法 LAW-1）；v7→v8 升级先过「版本注意」的 breaking 清单。
- 违反后果: 按 5/6/7 时代记忆盲写，配置不生效或构建失败（如 manualChunks 对象形式 v8 已移除）。
- 溯源: [官方迁移指南](https://vite.dev/guide/migration)

[VT-2] **MUST**: 客户端可见环境变量必须 `VITE_` 前缀；密钥 NEVER 进 `VITE_` 变量（全局宪法 LAW-6）。
- 违反后果: 无前缀取不到值；有前缀的密钥全量打进客户端 bundle（泄漏）。
- 溯源: [模型经验]

[VT-3] **MUST**: vite.config 用 ESM（.ts/.mjs + import）。
- 违反后果: `require is not defined`。
- 溯源: [模型经验]

[VT-4] **NEVER**: 不要期望 `server.proxy` 在生产生效——生产代理由反向代理承担。
- 违反后果: 部署后接口跨域 404。
- 溯源: [模型经验]

[VT-5] **MUST**: 懒加载场景的 `import.meta.glob` 显式 `{ eager: false }`。
- 违反后果: 默认 eager 全量进主包。
- 溯源: [模型经验]

[VT-6] **MUST**: 分包策略依赖默认动态 import 分包；精细控制用 Rolldown `codeSplitting`（v8）或 manualChunks 函数形式（v7-）——NEVER 按包名全量分组；v8 已移除 manualChunks 对象形式。
- 违反后果: 按包名全量分组导致 chunk 交叉重复、缓存失效放大；v8 下对象形式配置直接失效。
- 溯源: [官方迁移指南](https://vite.dev/guide/migration) + [模型经验]

[VT-7] **MUST**: 启用 React Compiler 时 plugin-react 必须用 Babel 模式（与 SWC 互斥）。
- 违反后果: 编译产物未 memo 化，Compiler 静默失效。
- 溯源: [模型经验]

[VT-8] **MUST**: tsconfig 含 `"types": ["vite/client"]`；子路径部署配置 `base`。
- 违反后果: `import.meta.env` TS 报错；资产 404。
- 溯源: [模型经验]

[VT-9] **MUST**: 源码引用的静态资源一律 import（进管线：build 哈希/内联阈值优化）；public 仅放不可哈希、必须保留原名或运行时才知道路径的资源，引用一律**根绝对路径**。
- 违反后果: public 资产相对路径/import 引用 404；src 资产失去缓存优化。
- 溯源: [官方文档](https://vite.dev/guide/assets)

[VT-10] **MUST**: 获取 CSS 内容用 `?inline`（CSS 文件默认/具名导入 Vite 5 起已移除）；局部作用域样式用 `.module.css`。
- 违反后果: `import css from './x.css'` 得到 undefined/编译报错。
- 溯源: [官方文档](https://vite.dev/guide/features)

[VT-11] **MUST**: HMR API 使用必须 `if (import.meta.hot)` 条件守卫（生产靠 tree-shake 剔除）；`import.meta.hot.accept(` 必须源码原样出现（静态分析空白敏感，不能存变量再调）。
- 违反后果: 生产构建内联 HMR 代码或报错；非字面量 accept 不生效（HMR 边界丢失→整页刷新）。
- 溯源: [官方文档](https://vite.dev/guide/api-hmr)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| mode | development/production/自定义，配 `.env.[mode]` 与 `import.meta.env.MODE` |
| import.meta.env | 客户端环境变量，**仅 `VITE_` 前缀暴露** |
| define | 编译期常量替换 |
| server.proxy | **仅 dev 生效**的接口代理；生产交反向代理 |
| 插件 | 扩展 Rollup 接口 + Vite 特有选项（apply/enforce）[官方文档](https://vite.dev) |
| Rolldown | v8 构建引擎（替代 Rollup）：tree-shaking/minify/chunking 内置 |
| assetsInlineLimit | 内联阈值（默认 4096 字节）：以下资产转 base64 data URI（Git LFS 占位文件除外） |
| publicDir | 原样拷贝目录：不进管线、不哈希，**必须根绝对路径引用** [VT-9] |
| CSS Modules | `.module.css` 类名局部作用域；`localsConvention: 'camelCaseOnly'` 具名导入 [VT-10] |
| import.meta.hot | HMR API：data/accept/dispose/prune/invalidate/on/send；使用必须 if 守卫（生产 tree-shake）[VT-11] |
| 插件钩子 | Rolldown 接口扩展（v8）+ Vite 特有钩子（config/configureServer/transformIndexHtml/handleHotUpdate）；enforce/apply 控制生效域 |

## 最佳实践

### 场景：环境变量（[VT-2]）

推荐路径：`.env.[mode]` 分层 + `VITE_` 前缀 + `vite-env.d.ts` 类型；密钥放服务端（BFF/Nest），客户端只拿公开配置。

```bash
# .env.staging
VITE_API_BASE=/api   # do：前缀 VITE_
# SECRET_KEY=xxx     # don't：客户端拿不到；VITE_SECRET 更是泄漏 [VT-2]
```

```ts
// do：模式区分 + 类型（vite-env.d.ts 已含 vite/client）
const apiBase = import.meta.env.VITE_API_BASE ?? '/api';
```

### 场景：接口代理（[VT-4]）

推荐路径：dev 用 server.proxy，生产同路径交 nginx/网关——代码零感知。

```ts
// do：dev 代理 + 生产 nginx 同路径
server: { proxy: { '/api': { target: 'http://localhost:3000', changeOrigin: true } } }
```

### 场景：代码分割（[VT-5]/[VT-6]）

推荐路径：依赖默认分包策略（动态 import 自动分）→ 路由级懒加载 `() => import('./pages/X')` → 确需精细控制：**v8 用 `build.rolldownOptions` 的 Rolldown `codeSplitting` 选项**（manualChunks 函数形式已弃用）；v7 及以前用 manualChunks **函数形式**且只收确实跨路由的稳定大库（echarts/monaco 单独 chunk）。

```ts
// don't：按包名全量分组（交叉重复、hash 全变；且 v8 已移除对象形式）
manualChunks: { vendor: ['react', 'react-dom', 'lodash', ...] }

// do（v7-）：函数形式，只收稳定大库
manualChunks: (id) => { if (id.includes('echarts')) return 'charts'; }

// do（v8）：Rolldown codeSplitting（见版本注意 v8 breaking 清单）
build: { rolldownOptions: { output: { /* codeSplitting 策略 */ } } }
```

```ts
// 懒加载 glob：显式 eager: false（默认 eager 全量打包）
const pages = import.meta.glob('./pages/*.tsx', { eager: false });
```

### 场景：静态资源导入（[VT-9]）

推荐路径：源码引用的资源一律 import——dev 得 `/src/...`、build 得 `/assets/xxx.hash.ext`（改内容才失效缓存，可 immutable 长缓存）；public 仅放不可哈希/须保留原名/运行时拼接路径的资源，引用一律根绝对路径 `/icon.png`。

```ts
import img from './assets/logo.png';      // build → /assets/logo.hash.png
import wasm from './assets/x.wasm?url';   // ?url 强制取 URL
import raw from './shader.glsl?raw';      // ?raw 取字符串
```

边界条件：`assetsInlineLimit`（默认 4096 字节）以下内联 base64（**Git LFS 占位文件除外**；CSP 场景 `build.assetsInlineLimit: 0` + `html.cspNonce`）；`?inline`/`?no-inline` 覆盖阈值；`new URL(url, import.meta.url)` 三态——dev 原生可用、build 仅静态/模板字面量（一层深）被转换、**完全动态字符串不转换；SSR 下不适用**；TS 需 `"types": ["vite/client"]`（[VT-8]）。

### 场景：Web Worker

推荐路径（[官方文档](https://vite.dev/guide/features)）：v8 标准写法 `new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' })`——仅**直接内联于 new Worker() 调用**的 `new URL(...)` 被构建器识别；后缀式 `import MyWorker from './worker?worker'`（得到构造器）/`?sharedworker`/`?worker&inline`（base64 内联）亦可。

边界条件：dev 依赖浏览器原生 module worker 支持；worker 内 import 走独立依赖图；`?worker&inline` 产物自包含。

### 场景：CSS 工程面（[VT-10]）

推荐路径：局部作用域用 `.module.css`（类名哈希局部化）；取 CSS 内容用 `?inline`（返回字符串、**不注入页面**）；`@import` 由 postcss-import 自动内联（支持 alias 与 url 重写）。

```ts
import styles from './Button.module.css';   // CSS Modules：类名 → 哈希映射
import css from './global.css?inline';      // 取内容（默认/具名导入 Vite 5 起已移除）[VT-10]
```

边界条件：预处理器需自装 **sass-embedded/sass/less/stylus**（Vite 不内置）；`css.transformer: 'lightningcss'` 整体接管（**v8 起 Lightning CSS 是默认 CSS 压缩器**，见版本注意）；CSP 配 `html.cspNonce`；MPA：根目录 HTML 皆可访问（root/index.html → /），多入口 `build.rolldownOptions.input`。

### 场景：React Compiler 集成（[VT-7]）

推荐路径：需要 Compiler 时 plugin-react 切 **Babel 模式**（SWC 模式不走 Babel，Compiler 静默失效）；对构建速度敏感且不用 Compiler 的项目才用 SWC。详见 `kb/react-core.md` Compiler 节。

### 场景：子路径部署（[VT-8]）

推荐路径：`base: '/app/'`（vite.config 或构建时 `--base`）+ tsconfig `"types": ["vite/client"]`；History 路由的 SPA 配置回退（nginx `try_files`）。动态拼接资源路径用 `import.meta.env.BASE_URL`（**构建期静态替换**——`import.meta.env['BASE_URL']` 动态键访问无效）。

### 场景：依赖预构建与 monorepo 联调

推荐路径：预构建仅 dev 生效（CJS/UMD→ESM + 性能合并），v8 由 Rolldown 执行。**monorepo linked 依赖自动视为源码不预构建**（要求 ESM 导出，否则 `optimizeDeps.include`）；**linked 依赖改动后须 `--force` 重启 dev server 才生效**。插件 transform 产生的不可发现导入：大/含 CJS → `optimizeDeps.include`；小且纯 ESM → `optimizeDeps.exclude`。缓存失效条件：lockfile 内容/patches 目录 mtime/vite.config 相关字段/NODE_ENV——疑难杂症先 `--force` 重建 `node_modules/.vite`。

### 场景：库模式构建（build.lib）

推荐路径：`build.lib`（entry/formats）；**单入口产物 es+umd、多入口 es+cjs**；CSS 打成单文件并在 package.json exports 暴露；**库模式 `import.meta.env.*` 静态替换但 `process.env.*` 不替换**（消费者可动态改）——需固化用 define 或 esm-env。非浏览器库/高级构建直接用 tsdown 或 Rolldown。

### 场景：部署后动态 import 报错（旧 chunk 失效）

推荐路径：新部署删除旧资产后，存量用户页面动态 import 旧 chunk 报错——监听 **`vite:preloadError`** 事件 `preventDefault()` 后 reload；HTML 文件配 `Cache-Control: no-cache` 确保拿到新资产引用。

### 场景：插件开发（Plugin API）

推荐路径：插件 = **Rolldown 插件接口的扩展**（v8，非纯 Rollup）——工厂函数返回 `{ name, ...hooks }`；falsy 返回跳过、数组 preset 自动拍平；命名约定 `vite-plugin-*`。性能敏感 transform 用 **hook filters**（`transform: { filter: { id }, handler }`——id 支持字符串/includes/regex/函数及 `!` 否定数组；@rolldown/pluginutils 提供 exactRegex/prefixRegex；兼容旧版须在 handler 内重复 filter 判断）。

```ts
function myPlugin(): Plugin {
  return {
    name: 'vite-plugin-my',
    enforce: 'pre',                        // 顺序链：Alias → pre → Vite core → normal → Vite build → post → post-build
    apply: 'serve',                        // 'build' / 'serve' / (config) => boolean
    transform: {
      filter: { id: '**/*.svg' },          // hook filter 预过滤（性能）
      handler(code, id) { return transformSvg(code, id); },
    },
  };
}
```

边界条件：**dev 钩子映射**——options/buildStart 启动一次、resolveId/load/transform 每模块、buildEnd/closeBundle 关闭；**moduleParsed dev 不调用**（dev 不做完整 AST 解析）；除 closeBundle 外 Output Generation Hooks dev 均不调用；Vite 特有钩子——config（建议返回 partial 深合并、避免直接 mutate）/configResolved（command/mode/isProduction 载体）/configureServer（**返回函数 = 后置中间件**，不返回 = 前置）/transformIndexHtml（order pre/post + HtmlTagDescriptor injectTo）/handleHotUpdate（HmrContext：收窄 modules、返回 [] 强制整页刷新、发自定义 ws 事件）/closeServer（reason: restart|close）；`this.meta.viteVersion`/`rolldownVersion` 环境探测（v8+）；产物引用 emitFile + `import.meta.ROLLDOWN_FILE_URL_<ref>`（JS）/`__VITE_ASSET__<ref>__`（CSS/HTML）；build-only 插件注册进 `build.rolldownOptions.plugins`（≡ enforce: 'post' + apply: 'build'，此形态下 Vite 特有钩子不可用）；Rolldown/Rollup 插件兼容判据：无 moduleParsed、无 transform.inject、不强耦合 bundle 输出钩子；跨平台路径用 `normalizePath`（from 'vite'）。排障：vite-plugin-inspect（.inspect/ 面板查每插件 transform 输入输出与耗时）。

### 场景：HMR API（import.meta.hot，[VT-11]）

推荐路径：所有 HMR 代码包 `if (import.meta.hot)` 守卫；self-accept 即 HMR 边界——**原模块引用不被替换**，re-export 须 `let` + accept 内重赋值；清理副作用用 dispose/prune；跨实例状态用 data。

```ts
// do：守卫 + self-accept + dispose 清理
export let data = await loadData();
if (import.meta.hot) {                            // [VT-11] 生产 tree-shake
  import.meta.hot.accept(async (newModule) => {   // 静态分析：import.meta.hot.accept( 须原样出现
    if (!newModule) return;                       // 更新模块语法错误时为 undefined
    data = newModule.data;
  });
  import.meta.hot.dispose(() => cleanup());       // 替换前清理副作用
  import.meta.hot.on('vite:beforeUpdate', (p) => log(p));
}
```

边界条件：accept 三形参（无参 self / 单 deps / 数组 deps）；**更新模块语法错误时 newModule 为 undefined**（回调仍触发，判空）；静态分析空白敏感；dispose（模块替换前清理监听/定时器）、prune（模块不再被导入时——CSS 注入清理用此）；data **按模块路径持久化、跨 HMR 实例存活**（仅可变属性、不可整体重赋值；prune 后清空）；invalidate(message?) 向 importer 传播失效（推荐在 accept 回调内调用；仍须先 accept 否则整页刷新）；内建事件：vite:beforeUpdate/afterUpdate/beforeFullReload/beforePrune/invalidate/error/ws:disconnect/ws:connect；客户端→服务端 `hot.send`（连接建立前缓冲）；服务端→客户端 `server.ws.send` + `import.meta.hot.on`（事件名加前缀防撞；TS 类型 CustomEventMap，'vite/types/customEvent.d.ts'）；decline 为向后兼容 noop。

### 场景：Tailwind CSS v4（v3→v4 迁移与集成）

推荐路径：Vite 项目用专用插件 `@tailwindcss/vite`（4.3.5，与 tailwindcss 同版本）；CSS 入口 `@import "tailwindcss"`；升级用 `npx @tailwindcss/upgrade`（Node ≥20，新分支跑）。确认版本线：**v4 latest=4.3.5，v3-lts=3.4.19**；v4 依赖现代 CSS（@property/color-mix()），浏览器门槛 Safari 16.4+/Chrome 111+/Firefox 128+，老浏览器停留 v3.4 [官方文档](https://tailwindcss.com/docs/upgrade-guide)。**包拆分**：PostCSS 插件 → `@tailwindcss/postcss`、CLI → `@tailwindcss/cli`（Vite 项目用 `@tailwindcss/vite` 性能最佳）；v4 自动处理 import 与 vendor prefixing——可删 postcss-import/autoprefixer。

- **视觉静默漂移高危改名**（不报错但样式变）：`shadow-sm→shadow-xs`、`shadow→shadow-sm`；`rounded/blur/backdrop-blur/drop-shadow` 同套；**`outline-none→outline-hidden`**（新 `outline-none` 真设 `outline-style: none`）；**`ring→ring-3`**（默认环宽 3px→1px、色 blue-500→**currentColor**）；**默认 border 色 gray-200→currentColor**
- **配置面**：CSS-first（`@theme { --color-*: ... }`）；JS 配置不自动检测——显式 `@config` 指令加载（`corePlugins`/`safelist`/`separator` 不支持；safelist → `@source inline()`）；`resolveConfig` 移除 → CSS 变量 + getComputedStyle
- **语法面**：重要修饰符 `!` 移到类名**末尾**（`flex!`）；变体堆叠顺序改**左到右**；任意值变量速写 `bg-(--brand)`（原 `bg-[--brand]`）；自定义工具类用 **`@utility`** API（`@layer utilities` 不再识别）；`@tailwind` 三指令移除
- **行为面**：`space-y-*`/`divide-y-*` 选择器改 `> :not(:last-child)`（inline 元素/子元素额外 margin 时漂移，推荐 flex/grid+gap）；hover 仅 `(hover: hover)` 生效（tap 不触发）；`transform-none` 不再重置 rotate/scale/translate；v4 **不兼容 Sass/Less/Stylus**；Vue/Svelte/CSS Modules 里 `@apply` 须 `@reference` 主 CSS
- 来源：[官方文档](https://tailwindcss.com/docs/upgrade-guide)

### 场景：Lint/Format 选型（Biome 2 vs ESLint+Prettier）

推荐路径（**@biomejs/biome 2.6.8**，2026-11-15 锚定）：新项目 Rust 单二进制 Biome 2（format+lint+assist 一体；JS/TS/JSON/CSS/GraphQL/HTML/Markdown/YAML 全覆盖；GritQL 插件自定义规则）替代 Prettier+ESLint 双链；存量 ESLint 生态（typescript-eslint 深度规则）维护成本高时保留。安装必 `-E` 精确锁版；`biome init` → `biome check --write`（格式化+安全修复一遍过）。

- **v1→v2 断裂速查**（迁移 `biome migrate --write`）：`ignore`/`include` → **`includes`**（glob 引擎重写：不再自动前置 `**/`；`*` 不再匹配 `/`）；路径/glob **相对配置文件**（非 cwd）；linter `all` 移除 → recommended + `domains: { next/react/test/project: "all" }`（react 与 solid 域冲突勿同开）；**style 组默认不报 error**；package.json 默认多行展开（`expand: "auto"` 恢复）；`organizeImports` 字段 → **assist action `source.organizeImports`**（新排序：`node:` 不再置顶）；抑制注释 `// biome-ignore lint/<GROUP>/<RULE>: <reason>`；VS Code 扩展 v3 升级须完全重启 + 杀残留 biome 进程
- 来源：[官方文档](https://biomejs.dev/guides/getting-started/) + [官方文档](https://biomejs.dev/installation/upgrade-to-biome-v2/)

### 场景：构建工具替代线（Rspack / Rsbuild，Rstack 生态）

选型定位：**@rspack/core 2.3.2**（2026-11-17 锚定，**v2 大版本**；Node ^20.19.0 || >=22.12.0——与 Vite 8 门槛一致；peer @swc/helpers/@module-federation/runtime-tools）是 **webpack 兼容的 Rust bundler**——modernized webpack API，**兼容社区 webpack 插件与 loaders 生态**（迁移存量 webpack 项目不重写配置面）；**@rsbuild/core 2.3.2**（与 Rspack 同版本号同步发版；peer core-js ≥3；`create-rsbuild` 脚手架）是其上 batteries-included 构建工具——零配置 + 插件体系 + framework agnostic（React/Vue/Svelte），定位 **Vite 竞品**，含 `/guide/migration/webpack` 迁移指南。

- **官方 benchmark**（rspack.rs 首页，build-tools-performance 仓库）：dev 1.36s / build 3.35s / HMR 160ms——vs Vite 6.50s dev / **1.98s build** / 130ms HMR vs webpack 21.40s/28.10s/2.78s——**dev 冷启远快于 Vite，但 build 与 HMR 略慢**；选型按痛点：webpack 存量迁移/超大项目 dev 冷启选 Rstack，新项目追求 build 速度与 ESM 原生管线仍选 Vite 8
- **Rstack 全家桶**（ByteDance，MIT）：Rspack（bundler）/ Rsbuild（应用构建）/ Rslib 0.0.10（库开发，早期）/ Rspress 1.47.2（SSG 文档站）/ Rsdoctor（**AI 友好构建分析器**，包名 @rsdoctor/core）/ **@rstest/core 0.12.6**（Rspack 驱动 Jest 兼容测试框架，peer jsdom/happy-dom 可选）/ Rslint（ESLint 兼容高性能 linter，**npm 尚无 latest——未正式发布**）
- **域名迁移**：官方域名 **rspack.dev → rspack.rs**（文档索引 rspack.rs/llms.txt、rsbuild.rs/llms.txt——AI 抓取友好）；**全家桶域名均迁 .rs**：rspack.rs / rsbuild.rs / rslib.rs / rspress.rs / rsdoctor.rs / **rstest.rs** / rslint.rs + **Rstack CLI rstack.rs**（One CLI 覆盖 dev/build/test/lint/format）；**rstest.dev 为域名抢注垃圾站勿访问**（2026-11-17 验证）
- 来源：[官方文档](https://rspack.dev) + [官方文档](https://rsbuild.rs) + [官方文档](https://rstest.rs/) + registry 锚定（2026-11-17）

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | `import.meta.env.MY_VAR` 为 undefined | 环境变量忘 `VITE_` 前缀 | [VT-2] |
| 2 | 本地 dev 正常，部署后接口跨域 404 | `server.proxy` 仅 dev 生效 | [VT-4] |
| 3 | `require is not defined` | vite.config 用 CJS | ESM [VT-3] |
| 4 | 本想按需加载，产物含所有匹配模块 | `import.meta.glob` 默认 eager | `{ eager: false }` [VT-5] |
| 5 | 公共 chunk 与路由 chunk 交叉重复 | manualChunks 按包名全量分组 | [VT-6] |
| 6 | v7 项目升 v8 后分包配置失效/报错 | v8 移除 manualChunks 对象形式、弃用函数形式 | codeSplitting [VT-6] |
| 7 | 配了 Compiler 但产物未 memo 化 | plugin-react SWC 模式不走 Babel | Babel 模式 [VT-7] |
| 8 | `import.meta.env` TS 报错 | tsconfig 缺 `"types": ["vite/client"]` | [VT-8] |
| 9 | 部署到 `/app/` 子路径后资产 404 | 忘配 `base` | [VT-8] |
| 10 | monorepo linked 依赖改动不生效 | 预构建缓存未失效 | `--force` 重启 dev server |
| 11 | 新部署后存量用户白屏/动态 import 报错 | 旧 chunk 被删，页面仍引用旧 hash | 监听 `vite:preloadError` 后 reload |
| 12 | 原生装饰器构建报错/不转换 | **Oxc 不支持原生装饰器降级** | @rolldown/plugin-babel 或 @rollup/plugin-swc |
| 13 | public 资产 import 或相对路径引用 404 | public 不进管线，仅根绝对路径可访问 | [VT-9] |
| 14 | `import css from './x.css'` 为 undefined | Vite 5 起移除 CSS 默认/具名导入 | `?inline` [VT-10] |
| 15 | new Worker 传变量路径 build 后 404 | 仅 new Worker(new URL(...)) 内联形态被识别 | 标准写法（见场景：Web Worker） |
| 16 | new URL(url, import.meta.url) SSR 报错/全动态 build 后 404 | SSR 不支持；完全动态字符串不转换 | 静态/模板字面量路径或改 import |
| 17 | CSP 阻断内联资源 | assetsInlineLimit 把小资产转 data: URI | `build.assetsInlineLimit: 0` + `html.cspNonce` |
| 18 | 插件 moduleParsed 钩子 dev 不触发 | dev 不做完整 AST 解析 | 改用 resolveId/load/transform |
| 19 | configureServer 中间件想拦内部中间件之后却在前执行 | 不返回函数 = 前置中间件 | 返回函数注入后置中间件 |
| 20 | import.meta.hot.accept 不生效（整页刷新） | 静态分析空白敏感：import.meta.hot.accept( 须原样出现 | 保持字面量调用 [VT-11] |
| 21 | HMR 更新回调里 newModule 为 undefined 未处理 | 更新模块语法错误时回调仍触发 | 回调内判空 [VT-11] |
| 22 | HMR 后导入方拿到的导出还是旧值 | self-accept 不替换原模块引用 | re-export 用 let + accept 内重赋值 |
| 23 | 生产包含 HMR 代码/报错 | 缺 if (import.meta.hot) 守卫 | 条件守卫 [VT-11] |

## API/配置速查表

| 配置 | 要点 | 易错点 |
|---|---|---|
| defineConfig | `defineConfig({...})` 类型安全入口 | — |
| resolve.alias | `@` → src；用 `path.resolve` | 手写相对路径 Windows 分隔符问题 |
| define | `'process.env.X': JSON.stringify(v)` | 与 import.meta.env 双轨混乱 |
| server.proxy | `'/api': { target, rewrite }` | 仅 dev；生产反向代理 [VT-4] |
| build.target | `'es2022'` 等按浏览器矩阵（v8 默认 Baseline：Chrome 111/Edge 111/Firefox 114/Safari 16.4） | legacy 用 plugin-legacy 按需 |
| build.rolldownOptions | v8 现行键（`rollupOptions` 弃用）；`codeSplitting` 分包 | manualChunks 对象形式 v8 已移除 [VT-6] |
| optimizeDeps.rolldownOptions | v8 现行键（`esbuildOptions` 弃用） | 沿用旧键静默失效 |
| envDir/envPrefix | `.env` 目录与前缀 | 前缀改了忘了同步 CI 变量 |
| 插件 enforce | `'pre'`/`'post'` 排序 | 顺序链：Alias→pre→core→normal→build→post→post-build |
| 插件 apply | `'build'`/`'serve'`/函数 | dev 专用插件漏 apply 进 build |
| hook filter | `transform: { filter: { id }, handler }`（Rolldown 特性） | 兼容旧版须 handler 内重复判断 |
| configureServer | dev server 中间件注入；返回函数 = 后置 | 不返回 = 前置中间件 [坑点 19] |
| handleHotUpdate | HmrContext：收窄 modules / 返回 [] 整页刷新 / 自定义 ws 事件 | moduleParsed dev 不调用 [坑点 18] |
| import.meta.hot | data/accept(三形参)/dispose/prune/invalidate/on/send | if 守卫 [VT-11]；newModule 可 undefined；accept 字面量 |
| vite-plugin-inspect | `.inspect/` 可视化面板 | 插件 transform 排障第一入口 |
| build.lib | entry/formats；单入口 es+umd、多入口 es+cjs | import.meta.env 静态替换、process.env 不替换 |
| assetsInlineLimit | 内联阈值（默认 4096 字节） | Git LFS 占位除外；CSP 场景置 0 [坑点 17] |
| publicDir | 原样拷贝目录 | 仅根绝对路径引用 [VT-9] |
| ?url / ?raw / ?inline | 资产后缀：强制 URL / 取字符串 / 覆盖内联阈值 | TS 需 vite/client [VT-8] |
| ?worker / ?sharedworker / ?worker&inline | Worker 后缀式导入 | 标准写法 new Worker(new URL(...)) 优先（可静态分析） |
| html.cspNonce | CSP nonce 注入 | 与 assetsInlineLimit 内联冲突 [坑点 17] |
| new URL(url, import.meta.url) | 运行时资产路径 | 全动态不转换；SSR 不适用 [坑点 16] |
| optimizeDeps.include/exclude | 不可发现导入显式声明 | linked 依赖改动须 `--force` |
| vite:preloadError | 动态 import 加载失败事件 | preventDefault + reload；HTML 配 no-cache |
| environments（RC） | 多环境显式配置；顶层 `ssr` 属性将在 API 稳定后弃用 | RC 阶段——暂不推荐全面切换 |

## 版本注意

- 当前最新：**Vite 8.3.8**（npm registry 复核 2026-11-17；8.3.7 为 2026-11-15 官网 footer 锚定；**8.4.0-beta.1 通道推进中**——2026-11-17 巡检，8.4 minor 未 stable 前生成基线仍 8.3）[官方文档](https://vite.dev)
- **v8 相对 v7 breaking 清单**（[官方迁移指南](https://vite.dev/guide/migration)，2026-11-15 抓取）：
  - **环境**：Node 20.19+/22.12+；默认浏览器目标 Baseline Widely Available——Chrome/Edge 111、Firefox 114、Safari 16.4
  - **引擎替换**：Rolldown+Oxc 取代 esbuild+Rollup；提供 **rolldown-vite**（带 Rolldown 的 Vite 7）渐进迁移
  - **配置改名/弃用**：`build.rollupOptions`→`build.rolldownOptions`；`worker.rollupOptions`→`worker.rolldownOptions`；`optimizeDeps.esbuildOptions`→`optimizeDeps.rolldownOptions`；顶层 `esbuild`→`oxc`；`transformWithEsbuild`→`transformWithOxc`；`build.commonjsOptions` 成 no-op
  - **分包**：**manualChunks 对象形式已移除**；函数形式弃用 → Rolldown `codeSplitting` 选项（[VT-6]）
  - **压缩**：JS 默认 Oxc minifier（`build.minify:'esbuild'` 弃用；不支持属性混淆）；CSS 默认 Lightning CSS
  - **模块语义**：CJS 互操作 dev/build 统一（旧行为临时用 `legacy.inconsistentCjsInterop: true`）；移除模块解析格式嗅探；外部化模块 `require()` 保留（配套 `esmExternalRequirePlugin`）；UMD/IIFE 不再 polyfill `import.meta.url`；`build()` 失败抛 `BundleError`
  - **移除/不支持**：`build.rollupOptions.watch.chokidar`；`output.format:'system'/'amd'`；部分 Rollup hooks；plugin-legacy 的 ES5 降级
  - **Oxc 转换/压缩限制** [官方文档](https://vite.dev/guide/migration)：**原生装饰器不支持降级**（规范未定——用 @rolldown/plugin-babel + @babel/plugin-proposal-decorators（version '2023-11'）或 @rollup/plugin-swc 替代）；`esbuild.supported` 不支持；Oxc minifier **不支持 mangleProps/reserveProps**；esbuild 变可选依赖
- SSR 一等支持（ssr.noExternal/ssr.target）；**Environment API（v6+）处于 Release Candidate**——大版本间稳定、部分 API 仍 experimental；多环境用 `environments` 显式配置（dev 期 client+ssr 恒存在；环境继承顶层配置）；**顶层 `ssr` 属性将在 API 稳定后弃用**；官方建议暂不全面切换 [官方文档](https://vite.dev/guide/api-environment)
- **静态资源与 CSS 工程锚定**（[官方文档](https://vite.dev/guide/assets) + [官方文档](https://vite.dev/guide/features)，2026-11-17）：资产后缀全家桶（?url/?raw/?inline/?no-inline/?worker/?worker&inline）、assetsInlineLimit 与 Git LFS 排除、publicDir 规则、new URL 三态、CSS Modules 约定与 localsConvention、**Vite 5 起移除 CSS 默认/具名导入**（取内容 ?inline）、预处理器自装、**Lightning CSS 默认 CSS 压缩**、TS 转译仅（isolatedModules；paths 需 resolve.tsconfigPaths: true）、MPA 入口
- **官方插件版本锚定**（npm registry，2026-11-15）：**@vitejs/plugin-react 6.3.0**（**peer 仅 vite ^8**——锁 Vite 8 线；React Compiler 走 babel-plugin-react-compiler ^1.0.0 可选 peer；Node 20.19+/22.12+）；**@vitejs/plugin-legacy 8.2.4**（peer vite ^8 + **terser ^5.16**——legacy 双构建靠 terser 压 ES5 包；systemjs/core-js 内置）
- **配置加载语义** [官方文档](https://vite.dev/config/)：configLoader 默认 `bundle`（Rolldown 打包 config 到 node_modules/.vite-temp）；`--configLoader native`（Node 22.18+ 原生执行）计划成默认；条件配置 `isSsrBuild`/`isPreview` **可能 undefined**（显式比较 true/false）；**.env* 文件在 config 解析后才加载——config 运行时 process.env 无 .env 变量，需影响 config 用 `loadEnv(mode, cwd, '')` 手动加载**
- **Biome 2.6.8**（2026-11-15；v1 线末版 1.9.4）[官方文档](https://biomejs.dev/installation/upgrade-to-biome-v2/)：format+lint+assist 一体化（Rust 单二进制）；v1→v2 用 `biome migrate --write` 迁移
- **Vite 插件 API 与 HMR API 锚定**（2026-11-17）：插件 = Rolldown 接口扩展（hook filters 性能预过滤/dev 钩子映射——moduleParsed 不调用、Output Hooks 除 closeBundle dev 不调用/configureServer 前后置中间件/transformIndexHtml/handleHotUpdate HmrContext/emitFile 产物引用/插件顺序链/this.meta 探测/Rolldown-Rollup 兼容三判据/build.rolldownOptions.plugins 等价性）[官方文档](https://vite.dev/guide/api-plugin)；import.meta.hot 全 API（accept 三形参/静态分析空白敏感/newModule 可 undefined/data 跨实例持久/invalidate 传播/内建事件族/hot.send 连接前缓冲）[官方文档](https://vite.dev/guide/api-hmr)
- 来源：[官方文档](https://vite.dev) + [官方迁移指南](https://vite.dev/guide/migration)

## 与其他子领域的集成要点

- **react-core**：React Compiler 需 Babel 模式 plugin-react（与 SWC 互斥）[VT-7] → 见 `kb/react-core.md`
- **Testing**：Vitest 复用 Vite 配置与管线（同源 transform）→ 见 `kb/testing.md`
- **monorepo**：monorepo 下 Vite 项目作为 workspace 包；根配置复用 `mergeConfig` → 见 `kb/monorepo.md`
- **Next.js**：Next 自带 Turbopack，**不要**在 Next 项目里套 Vite；Vite 适合纯 SPA/库 → 见 `kb/nextjs.md`

## 来源索引

- Vite 官网（定位/插件生态/Rolldown 特性/版本 8.3.8）：https://vite.dev [官方文档]
- Vite 官方迁移指南（v7→v8 breaking 全清单）：https://vite.dev/guide/migration [官方文档]
- 生产构建指南（codeSplitting/多页/库模式/vite:preloadError）：https://vite.dev/guide/build [官方文档]
- 依赖预构建指南（自动发现/monorepo linked/缓存失效）：https://vite.dev/guide/dep-pre-bundling [官方文档]
- Tailwind CSS v4 升级指南（v3→v4 改名表/@theme CSS-first/@utility/hover 行为/包拆分）：https://tailwindcss.com/docs/upgrade-guide [官方文档]
- npm registry（tailwindcss 4.3.5 / v3-lts 3.4.19 / @tailwindcss/vite 4.3.5 锚定）：https://registry.npmjs.org [官方文档]
- Environment API 指南（RC 状态/environments 配置）：https://vite.dev/guide/api-environment [官方文档]
- 静态资源指南（资产导入语义/assetsInlineLimit/publicDir/new URL 三态/Git LFS 排除）：https://vite.dev/guide/assets [官方文档]
- 特性指南（CSS Modules/?inline/预处理器/Lightning CSS/Worker 标准写法/MPA/CSP nonce/TS 转译仅）：https://vite.dev/guide/features [官方文档]
- Vite Plugin API（Rolldown 接口扩展/hook filters/dev 钩子映射/Vite 特有钩子/插件顺序链/emitFile 引用/兼容判据/this.meta 探测）：https://vite.dev/guide/api-plugin [官方文档]
- Vite HMR API（import.meta.hot 全 API/accept 静态分析/data 持久化/invalidate/内建事件/hot.send）：https://vite.dev/guide/api-hmr [官方文档]
- [模型经验]：坑点 1-9 的故障模式与修复、代理/env/glob 实践——适用 Vite 5~8 长期稳定面
- 法则条款来源：corpus/react/vite-tooling/elicited/05-laws.md（法则化萃取）

- **Biome 快速开始（init/check --write/锁版/语言面/GritQL 插件/domains）**：https://biomejs.dev/guides/getting-started/ [官方文档]
- **Biome v1→v2 升级（includes glob 重写/domains/assist action organizeImports/style 不报错/VS Code 重启）**：https://biomejs.dev/installation/upgrade-to-biome-v2/ [官方文档]
## 冲突消解记录

| 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|
| Vite 当前大版本为 7（Rolldown 实验中） | **8.3.8**，Rolldown 已是 v8 构建引擎（官网锚定） | 采用文档：版本锚定 8.3.8 |
| Vite = esbuild(dev) + Rollup(build) | v8 全链 Rolldown+Oxc（dev 转换 Oxc、预优化/构建 Rolldown、压缩 Oxc+Lightning CSS） | 采用文档：引擎记忆整体更新 |
| manualChunks 对象形式是标准分包配置 | v8 **移除对象形式**，函数形式弃用 → Rolldown `codeSplitting` | 采用文档（迁移指南）：[VT-6] 修订 |
| 所有插件两条管线等效 | 插件 apply/enforce 决定生效域 | 保留：dev 好的 build 崩优先查插件管线 |
| CSS import 默认导出返回样式内容（v4 时代习惯） | Vite 5 起移除默认/具名导入——取内容用 `?inline` | 采用文档 [VT-10] |
| Worker 必须用 `?worker` 后缀导入 | v8 推荐标准构造器 `new Worker(new URL(...), {type:'module'})`（后缀式仍可用） | 采用文档：标准写法优先（构建器仅识别内联形态） |
| assetsInlineLimit 只影响 JS 引用 | CSS url() 同样受阈值内联 | 采用文档 |
| Vite 插件 = Rollup 插件接口扩展 | v8 起 = **Rolldown** 插件接口扩展（Rollup 插件兼容有判据：无 moduleParsed/无 transform.inject/不耦合输出钩子） | 采用文档 |
| moduleParsed 钩子 dev/build 均可用 | dev 不调用；除 closeBundle 外 Output Generation Hooks dev 均不调用 | 采用文档 [坑点 18] |
| configureServer 返回的中间件运行在内部中间件之后 | 默认**之前**；返回函数才注入之后 | 采用文档 [坑点 19] |
| HMR 替换原模块引用 | self-accept 不替换原引用——re-export 须 let + accept 内重赋值；更新模块语法错误时 newModule 为 undefined | 采用文档 [VT-11] |
| import.meta.hot 可直接使用（生产自动移除） | 必须 if (import.meta.hot) 守卫——生产靠 tree-shake 剔除 | 采用文档 [VT-11] |
