# 打包 / cordis.yml / 部署 / 诊断

## 包结构（DSH checkout 内的插件包）

```
packages/<domain>/<name>/
├── package.json      # name: @deepseek-ai/dsh-<name>；依赖 @deepseek-ai/cordis
├── src/index.ts      # name / apply / Config / inject 导出
└── tests/*.spec.ts   # vitest 测试
```

- DSH 用 pnpm workspace：`vendor/cordis` 的包名是 `@deepseek-ai/cordis`（v4），`@deepseek-ai/schemastery` 也是 vendor 包。
- 真实样板：`vendor/timer/src/index.ts`（最小 Service 插件）、`vendor/group`、`packages/examples/agent-spine-demo/src/index.ts`（应用级组合）。
- 想要 Config schema 被 Loader 正确读取：**只导出命名导出**（`export function apply` / `export const Config`），不要默认导出插件——Loader 默认解包会丢弃 `Config` schema（见 docs/postmortem/0001-acp-default-export-drops-inject.zh.md）。

## cordis.yml：应用的插件树

```yaml
- id: greeter            # 稳定标识：HMR 对比的依据，必给
  name: './greeter.ts'   # 相对路径或 npm 包名
  config:                # 经插件 Config schema 校验
    greeting: 'Hi'
  disabled: true         # 保留条目但跳过挂载（改回即可重载）
```

条目元数据：`id` / `name` / `config` / `disabled` / `inject`（覆盖插件级 inject）。

### `!!js` 表达式（loader 扩展）

```yaml
- name: './config-demo.ts'
  config:
    greeting: !!js process.env.DEMO_GREETING ?? 'Hello'
```

- `!!js` 仅在 `config` 与条目 `disabled` 字段内有效；`disabled: !!js ...` 每次挂载决策时基于 loader 上下文求值，可做平台/环境门控。
- 其余元数据（`name`/`id`/`inject`）保持静态，其中表达式是普通真值。

### 组合原语

- **group**（`@deepseek-ai/cordis-plugin-group`）：嵌套一份条目子列表，作为单元加载/卸载。
- **isolate**：为组提供某项服务的独立实例——两个组各自看到配置不同的提供方，互不影响。
- **include**（`@deepseek-ai/cordis-plugin-include`）：YAML/JSON 配置文件 include，`!!js` 解析表达式节点。
- DSH 的部署用 overlay 修补 base 配置（见 `packages/bundle/base/cordis.patch.yml`）。

## 运行与部署路径

### 1. 教程/独立启动器（无 harness）

```sh
node --import tsx ../../vendor/cordis/bin.js   # 从 cwd 读 cordis.yml
```

### 2. DSH 应用（cordis.yml 由 loader 加载）

插件进入 `cordis.yml`（apps/cli、bundle 或用户配置），经 `@deepseek-ai/cordis-plugin-loader` 挂载。HMR 三件套：`cordis-plugin-logger-console` + `cordis-plugin-timer` + `cordis-plugin-hmr`。

### 3. 动态挂载（模型自写插件）

- `@deepseek-ai/dsh-tool-cordis`：自指工具集——检查运行时、**挂载/卸载模型写的插件**。
- `@deepseek-ai/dsh-cordis-host-runner` / `dsh-cordis-client-runner`：host 与浏览器两侧的插件运行时。
- `ui-cordis`（`@deepseek-ai/dsh-client-ui-cordis`）：GUI 里的动态插件定义卡片（cordis_define 工具行 + run/stop 开关）。

### 4. 打包成 bundle（profile 部署）

DSH 的正式部署单元是 **bundle + profile**（已验证于 `apps/cli/reference/README.md`、`docs/architecture.md`、`docs/user/develop/basic/publish.md`）：

- **bundle** = 一个 npm 包，其 `package.json` 声明：
  ```json
  { "dsh": { "bundle": { "patch": "./cordis.patch.yml" } } }
  ```
  实质是**一层 patch**（插入/覆盖插件行），可附带运行时胶水插件。内置 bundle：`@deepseek-ai/dsh-base`、`@deepseek-ai/dsh-web-app`、`@deepseek-ai/dsh-headless`。
- **profile** = `$DSH_HOME/profiles/<name>` 目录，含 `package.json`（树外插件依赖 + `dsh.profile` manifest 的有序 `bundles` 列表）+ 用户自己的 `cordis.patch.yml`。`web`/`headless` 是自带模板。
- **patch 层语法**：`cordis.patch.yml` 用 `- insert:` 插入新行（与普通 cordis.yml 的 `- id/name/config` 条目不同！）；patch **整行替换**目标行的 `config`（不深度合并键）。
- **叠加顺序**（后层优先）：各 bundle patch（按 `dsh.profile.bundles` 顺序）→ profile 的 `cordis.patch.yml` → `$DSH_HOME/cordis.patch.yml` → 各 `--patch <path>` overlay（argv 顺序）。
- **安装树外插件**：`dsh plugin --profile <name> add <package-or-git-spec>`（转发 pnpm）；成功后若该包声明 `dsh.bundle` 则自动加入 `dsh.profile.bundles`。从插件 checkout 里 `add .` 会安装当前 checkout。
- 启动：`dsh --profile <name>`；`dsh web` 是 `--profile web` 的别名。

## npm pack 本地打包（方式 B：tarball，实测 2026-08）

不依赖 registry 发布权限的正式打包路径：产出标准 `.tgz`，可被 `dsh plugin add` / `npm install` 消费，且能立即本地验证。

### 打包前 package.json 硬要求（逐项核对）

| 字段 | 要求 |
|---|---|
| `main` / `exports["."]` | 指向 ESM 入口（`types` + `default` 双出口） |
| `type` | `"module"` |
| `files` | **必须包含** `lib` + 运行时资产目录（如 `python`）；`README.md` 可选 |
| `dependencies` | **禁写 `workspace:^`**（pnpm 内部协议，npm publish 拒绝/无法解析）——发布前替换为真实 semver |
| **peerDependencies** | **cordis / dsh-tools 等宿主已有服务放这里**（对齐 DSH 生态惯例，见下） |

### peerDependencies 惯例（对照 `@deepseek-ai/dsh-tool-cordis`）

- 插件运行在 DSH 进程内，`@deepseek-ai/cordis`、`@deepseek-ai/dsh-tools` 等**宿主已挂载**的服务必须声明为 **peerDependencies**——否则 pnpm/npm 装独立副本，Service 基类分裂 → `ctx.memory` 等注册到另一套 Context 原型，行为诡异。
- 真·独立依赖（如 schemastery 用于 Config schema，宿主也可能有）视情况 peer 或 dependency；**以宿主是否已提供为准**。
- 发布版本声明：`@deepseek-ai/cordis: ^4.0.1` 等（registry 可解析的版本）。

### registry 版本对齐检查（易踩）

- 本地构建用的版本（如 `@deepseek-ai/dsh-tools@0.1.0-rc.5`）**可能不在 registry**——先 `npm view <pkg> versions --json` 查。
- 声明 `^0.1.0-rc.5` 会解析到 registry 最高的 `0.1.0-rc.6`（本地无 rc.5 时）；rc 版本号语义与 API 稳定性不保证一致，**打包后用真实 registry 版本重跑验证**。

### 打包 + 验证链路（实测 PASS）

```
改 package.json ──► npm pack ──► <pkg>.tgz
   │  workspace:^→真实版本     │
   │  宿主服务→peerDependencies│
   │  registry 版本对齐        │
   ▼                          ▼
   ┌─────────────────────────────────────────────┐
   │ 解包验证：tar -xzf → junction 宿主 node_modules│
   │ → 用 verify-loader.ts 加载 tarball 内 lib     │
   │ → 工具注册 / Service 就绪 / 桥接拉起           │
   └─────────────────────────────────────────────┘
```

```sh
npm pack                       # → kiwifruit-dsh-memory-0.1.3.tgz
# 解包验证（tarball 内无 node_modules 是预期的——peer 由宿主提供）
tar -xzf <pkg>.tgz -C $env:TEMP/verify
# junction 宿主依赖树，模拟真实安装后的解析
New-Item -ItemType Junction "$env:TEMP/verify/package/node_modules" -Target "<插件目录>/node_modules"
# 用 verify-loader.ts 语义加载 tarball 内的 lib/index.js（createRequire 从 harness apps/cli 解析）
```

验证通过 = tarball 产物 + 宿主依赖树可完整装配（工具注册、Service 就绪、桥接进程拉起）。

## 插件发布：npm 包（可被 `dsh plugin add` 安装）

要让插件能被 `dsh plugin add` 安装，需发布为遵循 DSH 约定的 npm 包。

### 核心要求：`package.json` 中声明 `dsh.bundle`

```json
{
  "name": "dsh-hello-plugin",
  "version": "0.1.0",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "cordis.patch.yml"],
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    }
  }
}
```

- `dsh.bundle.patch`：告诉 DSH 安装后应用哪个 patch 文件来挂载插件
- `files`：确保构建产物和 patch 文件被包含进 npm 包

### 发布版 cordis.patch.yml

```yaml
- insert:
  - id: hello
    name: dsh-hello-plugin
```

与本地开发用的 `cordis.yml` 类似，但 `name` 用 npm 包名而非 `file://` URL。

### 发布到 npm

```bash
npm login
npm publish --access public  # scoped 包需要 --access public
```

### 发布者验证

发布后，在另一个 profile 中测试安装确认：

```bash
dsh plugin --profile test add dsh-hello-plugin
dsh plugin --profile test list
```

## 发布包 cordis.patch.yml 自动应用机制（实测 DSH-Context-Pro）

> 当用户 `dsh plugin add` 你的包时，插件如何被激活？全链路如下。

### 自动应用全链路

| 步骤 | 触发动作 | 产物 |
|------|----------|------|
| 1 | 用户 `dsh plugin --profile <name> add <pkg>` | CLI 下载 tarball |
| 2 | 解压包 → 读取根目录 `cordis.patch.yml` | 包内 patch 内容 |
| 3 | 合并到 `~/.dsh/profiles/<name>/cordis.patch.yml` | Profile patch 更新 |
| 4 | 触发 HMR 热重载 | 插件即时激活，无需重启 |

**核心机制**：`dsh plugin add` 安装后，若包声明了 `dsh.bundle.patch` 才会被激活为 bundle 层；激活通过**读取包根目录 `cordis.patch.yml` 合并进 profile** 实现，经 HMR 热重载生效。

### 发布包内 cordis.patch.yml 模板

```yaml
# cordis.patch.yml（包根目录，随包分发）
- insert:
    - id: context-pro
      name: '@kiwifruit/dsh-context-pro'   # 必须用 npm 包名，不能用 file:///
      config:
        chains:
          enabled: true
```

### 发布包五个配置项自检（缺一不生效）

| 配置项 | 要求 |
|--------|------|
| 包内含 `cordis.patch.yml` | `npm pack --dry-run` 列表须见该文件 |
| `files` 数组包含它 | `package.json: "files": [..., "cordis.patch.yml", ...]` |
| `dsh.bundle.patch` 指向正确 | `"patch": "./cordis.patch.yml"` |
| `name` 用 npm 包名 | 发布包 patch 里写 `@scope/pkg`（非 `file:///`） |
| 默认配置开箱即用 | `<入口>.config` 提供可直接运行缺省值 |

### 发布包常见坑

| 坑 | 症状 | 规避 |
|----|------|------|
| 包内无 `cordis.patch.yml` | `dsh plugin add` 后不生效 | `npm pack --dry-run` 必看 tarball 列表 |
| `files` 漏包 patch 文件 | 发布后 tarball 无该文件 | `files` 必含 `cordis.patch.yml` |
| `name` 写 `file:///` | 用户装后加载本地路径报错 | 发布包 patch 必须用 npm 包名 |
| `config` 字段名拼写错 | 装了不生效 | 对照 `<入口>.Config` schema 核对 |
| 同名 `id` 冲突 | 其它包也用 `context-pro` | 用带命名空间的 id（如 `@scope/context-pro`） |

### 发布前验证命令（必跑）

```bash
# 1. 打包干跑
npm pack --dry-run
# 必见：cordis.patch.yml 在列表中

# 2. 解包实测
npm pack && 解包后 grep cordis.patch.yml
# 必见：package/cordis.patch.yml

# 3. 消费者回拉验证（publish 后必做）
npm pack <pkg>@<ver>   # 回拉真实 tarball
# 清单断言：必须项全在 / 排除项全无
```

### 消费者回拉验证法（方法论）

- `npm pack <pkg>@<ver>` 回拉真实 tarball + 清单断言：**必须项全在 / 排除项全无**。
- ⚠️ 中文文件名比对必须走 `npm pack --json` 的 path 数组——`tar -tzf` 文本比对在 Windows 控制台是编码假象（曾误报中文文档缺失）。

## 发布生效链（坑：改完不生效）

部署插件遇"构建了、重启了仍旧行为"时，按此链逐环核对：

```
build（产物更新） → 安装源（profile 装的是哪个物理位置的包） → 重启（DSH 进程）
```

- **双安装源陷阱**：工作区 `lib` 构建、重启了，但 profile 装的是 **npm registry 版**——两个物理位置，build 只救了一半。失效链缺一环都白改。
- **规避**：开发态用 `dsh plugin --profile <name> add file:<本地路径>` 切源（或发布后 add @version）；生效链 = **build → 安装源 → 重启**，缺一环都白改。

## 用户安装插件的方式

### 方式一：通过插件市场（GUI）

1. 先安装市场插件：`dsh plugin --profile web add dshmarket`（或 `@ace-zone/dsh-market`）
2. 重启 DSH Web
3. 进入 `设置 → 插件 → 插件市场`，浏览并一键安装

### 方式二：通过命令行（CLI）

```bash
dsh plugin --profile <配置名> add <插件标识>
```

| 来源类型 | 命令格式 | 示例 |
|---------|---------|------|
| npm 包（推荐） | `dsh plugin --profile web add <包名>` | `dsh plugin --profile web add @kiwifruit/dsh-context-pro` |
| GitHub 仓库 | `dsh plugin --profile web add github:所有者/仓库` | `dsh plugin --profile web add github:owner/repo` |
| 本地目录 | `dsh plugin --profile web add <绝对路径>` | `dsh plugin --profile web add /path/to/my-plugin` |

### 升级插件

与安装命令相同，**再次执行 `dsh plugin --profile <name> add <package>` 即升级**。

### 安全提醒

安装社区插件等同于运行第三方代码，具有与你本人相同的权限。建议：
- 安装前查看插件源码
- 不熟悉的插件在隔离环境中测试
- 选择知名或源码公开的插件
- 安装时指定具体版本号而非 `@latest`

## 多语言内核集成（JS/TS 外壳 + 任意语言内核）

```
DSH 插件(TS/JS) ── child_process ──→ Python/Rust/二进制内核
     │                                   │
     │ ctx.effect(disposer)              │ 常驻：stdin/stdout JSON 行协议
     │ 启动/停止生命周期                   │ 一次性：stdout 收集 + 退出码
     └── 路径绝对化 / 错误包装 / 配置映射  ←─┘
```

1. **路径绝对化**：`./script.py` 相对路径是相对 **Node CWD**，不是插件源码目录。用 `path.join(__dirname, './script.py')` 转绝对路径。
2. **子进程错误包装**：Python 报错不会自动转成 Node 异常。用 try-catch 包裹调用，把子进程 `stderr` 经 `ctx.logger` 格式化（最好转成 Cordis `Error`），否则底层崩溃会静默拖垮 Harness。
3. **常驻进程释放**：若底层启动常驻进程（WebSocket 服务等），释放逻辑必须放 `ctx.effect()`，否则 HMR 重载产生"僵尸进程"。
4. **运行环境在场证明**：Cordis 只管调用不管安装——目标机必须预装解释器/动态库（`.dll`/`.so`），否则 `ENOENT`。
5. **配置预留**：底层硬编码的路径/超时先用常量占位，封装时全部映射到 `Config` schema；接口草图（入参/出参/异常码）先行，避免底层写完参数传不进。

### 常驻内核通信协议（dsh-memory 实测）

- **stdio JSON-RPC**：请求 `{"id","method","params"}` → 响应 `{"id","result"|"error"}`，**每行一个 JSON**，UTF-8。
- **Windows 编码坑**：Python 默认 locale 是 GBK——必须 `sys.stdout/err.reconfigure(encoding='utf-8')` 强制 UTF-8，否则中文乱码/崩溃。
- **会话隔离**：`init(user_id, session_id)` 按会话缓存内核 orchestrator；跨会话不共享状态。
- **胶水转换**：TS camelCase ↔ Python snake_case 必须显式转换（见 [traps.md](../90-experience/traps.md) #23）；不透传裸 RPC 结果。
- **崩溃自动重启**：`waitReady` 探测 + 指数退避重启（`RESTART_BASE * 2^n`）；重启后重发未完成请求。
- **优雅关闭**：stop 时先 `end_session` 再 kill；验证脚本需显式 `process.exit(0)` 释放句柄（见 [traps.md](../90-experience/traps.md) #19）。

### 桥接层职责边界（红线）

- 胶水只做：类型转换、参数适配、协议转换、调用转发——**不承载业务逻辑**（见 CLAUDE.md 胶水规范）。
- 下游异常统一翻译为业务错误码；跨系统调用设超时 + 重试（注意幂等性）。
- 可观测：胶水日志含 caller/callee/req/res/cost_ms，链路可追踪。

## dsh plugin add 安装踩坑（实测）

> 来源：DSH-Context-Pro 项目实测

### 坑 1：`dsh` 命令不存在于 PATH

**现象**：`dsh: The term 'dsh' is not recognized`

**根因**：`dsh` CLI 是 `@deepseek-ai/dsh` 包，安装在 harness 的 `node_modules/.pnpm/node_modules/@deepseek-ai/dsh/lib/bin.js`，没有注册到系统 PATH。

**规避**：直接通过 node 调用：
```
node "D:\Git\github\deepseek-harness-master\node_modules\.pnpm\node_modules\@deepseek-ai\dsh\lib\bin.js" <command>
```

### 坑 2：`--profile <name>` 是必选参数

**现象**：`error: required option '--profile <name>' not specified`

**规避**：显式指定 `--profile web`（web profile 在 `~/.dsh/profiles/web`）。

### 坑 3：版本解析到坏版本，依赖冲突

**现象**：`[ERR_PNPM_NO_MATCHING_VERSION] No matching version found for @deepseek-ai/schemastery@^4.0.0`

**根因**：`dsh plugin --profile <name> add` 默认解析到**最新发布版**（npm `latest` tag），但最新版的依赖可能已损坏（如声明了不存在的版本范围）。

**规避**：显式指定版本号 `@0.2.0`；发布前在 `dependencies` 中确认版本范围在 registry 上可解析。

### 坑 4：`@latest` 抛出最小发布年龄（minimumReleaseAge）

**现象**：`dsh plugin --profile web add pkg@latest` 报 `ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION ... published within ... cutoff`，拒绝安装刚发布的包。

**根因**：pnpm 对 `latest` tag 有 24h 最小存活期冷却机制，防范刚发布的损坏版本被广泛拉取。

**规避**：
- **刚发版要立即装 → 写精确版本号** `pkg@0.5.3`（精确版本自动豁免冷却期）。
- README 的安装命令用「裸包名 = 最新版 + 24h 冷却期」说明，不写 `@latest`。

**发版 checklist 强制项**：每次 bump `package.json` 版本时，同步更新 README 里的安装命令版本脚注。

### 完整安装命令

```bash
node "D:\Git\github\deepseek-harness-master\node_modules\.pnpm\node_modules\@deepseek-ai\dsh\lib\bin.js" plugin add @kiwifruit/dsh-context-pro@0.2.0 --profile web
```

### 安装后验证

```bash
# 检查 profile 的 node_modules 中是否有该包
ls "C:\Users\<user>\.dsh\profiles\web\node_modules\@kiwifruit\dsh-context-pro"

# 检查 composition 是否包含插件条目
cat "C:\Users\<user>\.dsh\profiles\web\cordis.yml" | grep context-pro
```

## pnpm11 构建门禁：allowBuilds 专题（实测 DSH-Context-Pro）

> DSH 依赖 pnpm ≥ 11，其 **strictDepBuilds** 构建门禁是发布后安装失败的第一大隐形元凶，DRY 不发小 champion 也坑过。

### strictDepBuilds 硬错误机制

- pnpm ≥ 11 默认阻断任何**未在白名单**依赖的 install 脚本（postinstall 构建）。
- 软包（schemastery、genai 等 DLL 原生模块）与绑包（bundle patch）都在此列。
- 关键坑：**`allowBuilds` 占位符 `"@deepseek-ai/*": true`**——注释里建议它，但 `cordis-plugin-loader` 根本不发布 shell，导致 `allowBuilds` 恒空悬、阻断依旧。

### 标准解法（三场景）

```bash
# 场景①：新装（第一优先）
pnpm config set onlyBuiltDependencies '["subprocess-local","node-pty","koffi","genai","protobufjs"]'
pnpm install

# 场景②：补跑未授权的（存量项目）
pnpm rebuild @deepseek-ai/cordis-plugin-loader   # 解决"无法构建原生依赖"声明错误
# 若仍有 install 脚本未跑：pnpm approve-builds 手动放行

# 场景③：已装但某模块丢失（中途被阻断）
node_modules/@deepseek-ai/genai npm rebuild genai   # 关键：@deepseek-ai/genai 的构建子项
```

### 五包逐档（`onlyBuiltDependencies` 白名单）

| 包 | 类型 | 作用 |
|----|------|------|
| `subprocess-local` | 原生模块 | 子进程桥接二进制 |
| `node-pty` | 原生模块 | 伪终端（web/headless 必需） |
| `koffi` | 原生 FFI | 跨语言绑定 |
| `genai` | SDK | AI 能力绑定 |
| `protobufjs` | 序列化 | 协议编解码 |

### 自查清单

- [ ] `pnpm config list` 含 `onlyBuiltDependencies`
- [ ] `node_modules/<包>` 存在且 `lib/` 有内容（非空）
- [ ] `node_modules/.pnpm` 下无 `node_modules/<包>` 束之高阁的副本
- [ ] 卸载时 `reconcilePlugins` 正确摘除 layer（无残留）

## 诊断：插件加载失败/不工作

```ts
import { FiberState, type Context } from '@deepseek-ai/cordis'

export function apply(ctx: Context) {
  setTimeout(() => {
    for (const runtime of ctx.registry.values()) {
      for (const fiber of runtime.fibers) {
        if (fiber.state === FiberState.PENDING) {
          console.log(`${fiber.name} is PENDING — a required service is missing`)
        }
      }
    }
  }, 500)
}
```

排查顺序：
1. **不输出且进程静默退出** → 检查 fiber 状态：多半是 `inject` 的服务无人提供（PENDING 合法，不崩溃不报错）。
2. **配置错误** → `ValidationError: invalid config:` 指明字段与期望类型。
3. **HMR 不生效** → 确认 logger-console 与 timer 插件已挂载；条目带 `id`。
4. **插件似乎没运行** → 先查 `cordis.yml` 拼写（解析失败只走 logger，启动早期可能丢失）。
5. **FAILED 但原因不明** → `apply` 抛错会终止进程，检查 `apply` 内同步抛出的异常。
