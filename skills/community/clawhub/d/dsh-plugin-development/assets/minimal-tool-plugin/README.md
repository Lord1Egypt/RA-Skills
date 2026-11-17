# dsh-tool-greet

最小工具插件骨架（T3 形态）。给模型注册一个可调用的工具。

## 目录结构

```
minimal-tool-plugin/
├── package.json
├── cordis.patch.yml
├── README.md
└── index.js           # 插件本体（命名导出 name / inject / apply）
```

**这份骨架是零构建的**：`index.js` 是可直接加载的产物，`package.json` 里 `main` / `exports` / `files` 声明的每个路径都真实存在，复制后**开箱即可安装**。

> 为什么不做成 `src/index.ts` + 构建：
> **「发布前必须构建好产物，因为 dsh 不会跑你的 build」**。给一份只含 `src/` 却把 `main` 指向 `index.js` 的骨架，等于让复制者先撞一次 `Cannot find module` 才知道要去补构建链。需要 TypeScript 时按下面「升级到 TS」自行加一步即可。

## 开发期：用 overlay 挂载（不用先打包）

在 profile 目录旁边建 `cordis.yml`：

```yaml
- insert:
    - id: dsh-tool-greet
      name: './index.js'
```

`name` 支持相对路径、绝对路径、npm 包名三种。相对路径会被**锚定到补丁文件所在目录**（源码 `packages/boot/app-boot/src/index.ts` 的 `anchorInsertedPluginNames()` 行为，且有单测固定）。

启动并确认工具已注册：

```bash
dsh --dump-config        # 看组装后的配置树
```

然后在会话里让模型调用 `greet`。**必须看到实际输出**才算跑通 —— 「装上了」不等于「生效了」。

## 交付期：按包名安装

```bash
dsh plugin --profile <profile 名> add .
# 或已发布到 npm
dsh plugin --profile <profile 名> add dsh-tool-greet
```

## 升级到 TS（可选）

如果你确实想要类型检查：

1. 把 `index.js` 改名为 `src/index.ts`，给 `ctx` 加类型标注（`import type { Context } from '@deepseek-ai/cordis'`）。
2. 加 `tsconfig.json`（`rootDir: "src"`、`outDir: "."`）与 `"scripts": {"build": "tsc"}`。
3. **构建产物必须叫 `index.js` 且在包根**——`main` 与 `exports['.']` 指向的就是它。
4. ⚠️ **不要把 `@deepseek-ai/*` 写进 `dependencies`**（DSH profile 已提供）。独立工程里 `tsc` 可能因此报「找不到模块」，那是**类型解析**问题不是运行期问题；别用「声明一个假依赖」去消掉它。

## 显示元数据与图标（`0.2.1-alpha.1` 起的官方检查清单）

即便是**纯工具插件**（没有 UI），Plugin Manager 也会在**不激活它**的前提下读 `locale/*.json` 的 `meta.title` / `meta.description` 与 `./icon` 来渲染插件行。缺字段**优雅回落**到 `package.json` 的 `name` / `description`、缺图用默认美术 —— 非硬报错，但要让插件可辨识就该补：

1. `locale/en.json`：`{"meta":{"title":"…","description":"…"}}`（再给 `locale/zh.json`）。
2. 一枚图标：SVG / PNG / JPEG / WebP，**≤ 256 KiB**，原创或许可允许再分发，留在包内。
3. `exports` 补 `"./locale/*.json"` 与 `"./icon"`，并同步进 `files` 白名单。

完整清单与验证方法：`references/02b-official-templates.md` §「显示元数据与图标」。

## 四条必须遵守的规则

1. **不要写 `export default`。** 函数式插件用命名导出 `name` / `inject` / `apply`；有 default 会被当成服务类解析，命名空间被丢弃。
2. **`inject` 里要写 `'tools'`。** 否则 `ctx.tools` 是 `undefined`，插件直接报错。可选服务不要写在 `inject`，用 `ctx.get('x')`。
3. **`parameters` 的 `required` 写在属性级**（`required: true`）。这是 `defineTool` 的 DSH 自有 DSL；裸 `ctx.tools.register` 才是对象级 `required: ['a']`。两条路径规则相反，套错会静默失效或直接报错。
4. **`dsh.bundle.patch`、`files`、`exports` 都不能漏。** 前者漏了 `dsh plugin add` 只打警告不生效；`files` 漏了补丁文件不会进 npm 包；`exports` 少了 `'./cordis.patch.yml'` / `'./package.json'` 就偏离官方 bundle 的约定。

## 🔴 `0.2.2-alpha.2` 起：注册成功 ≠ 能被调用

`ctx.tools` 服务（`@deepseek-ai/dsh-tools`）现在**只是注册表**，真正的执行本体搬到了独立的执行器插件：
`@deepseek-ai/dsh-tool-executor-native`（默认）或 `-ptc`。所以：

- **完整 dsh**：base overlay 自带 `tool-executor-native` 行（`packages/bundle/base/cordis.patch.yml:497`），你不用管。
- **自建最小 bundle**：必须显式加执行器行，否则本骨架注册的工具**能注册、`--dump-config` 也看得到，但模型一调就抛** `ToolExecutorUnavailableError`（`packages/core/tools/src/index.ts:365`，类定义 `executor.ts:97`）。

要补的就一行（base overlay 里同款）：

```yaml
- insert:
    - id: tool-executor-native
      name: '@deepseek-ai/dsh-tool-executor-native'
```

`tools.mode` / `tools.maxParallelSubCalls` 也已从 `dsh-tools` 的 Config 移除（该插件里它们被标成 `z.never()`），要调并行度请改执行器自己的配置。完整症状与排查见 `references/05-pitfalls.md` 坑 P23。

## 验证清单

- [ ] `dsh --dump-config` 里能看到这一行
- [ ] 部署里有执行器（缺了就报 `ToolExecutorUnavailableError`，见上一节）
- [ ] 插件没有停在 PENDING（PENDING = 注入的服务没到位）
- [ ] 模型能实际调用工具并拿到正确输出
- [ ] 卸载后工具消失（`ctx.tools.register` 是副作用，不需要手动清理）

## 参考

- 完整字段表与两条注册路径对比：`references/03-api-cookbook.md`
- 模板库 T3 / T4：`references/02-templates.md`
- 官方最小范本逐字源码：`references/02b-official-templates.md`（官方模板 3）
- 出问题先查：`references/05-pitfalls.md`、`references/06-workflow.md` 第 ④ 部分（调试与排错）
