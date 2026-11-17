# 任务：为 DeepSeek Harness 构建可通用部署的桌面套壳（Electron）

## 目标

将运行于 `http://127.0.0.1:<port>` 的 DeepSeek Harness Web UI 包装为原生桌面应用
（Windows 优先，兼顾 macOS / Linux），让用户开箱即用，且**完整保留 Harness 的功能与
插件体系，尤其是插件 / 扩展能力**。

---

## 一、本地目录与配置通用化（重点）

所有路径、端口、启动参数**不得写死绝对路径**，改为「配置优先 + 自动发现」：

- 项目根提供 `config.json`（或 `.env`），字段：
  - `harnessHome`：harness 安装根目录（即内含 `apps/cli/lib/bin.js` 的目录）。
  - `port`：Harness Web 端口，默认 `3080`。
  - `autoLaunch`：是否由壳自动拉起 Harness（布尔值）。
  - `nodeBin`（可选）：指定 node 可执行文件路径；缺省用壳运行环境自带的 node。
- 解析顺序：`config.json` → 环境变量 `DEEPSEEK_HARNESS_HOME` / `DEEPSEEK_HARNESS_PORT`
  → 按相对布局推断（如壳可执行文件同级的 `Deepseek/` 或 `../Deepseek`）。
- 使用 `path` 与 `app.getPath` 做跨平台拼接，Windows / macOS / Linux 均可运行。
- 自动拉起时，用解析出的 `harnessHome` + `nodeBin` 拼出 CLI 命令：
  `NODE_OPTIONS="" "<nodeBin>" "<harnessHome>/apps/cli/lib/bin.js" web --port <port>`
  （保留 `NODE_OPTIONS=""` 以规避某些托管环境给 node 注入"安全删除"钩子、导致 Harness 写盘
  失败的问题；若该环境无此问题可省略，但需在 README 说明。具体钩子成因与边界见
  `deepseek-harness-windows-deploy` 技能的「安全与防护边界」。）
- 端口占用检测通用化：启动前探测 `port`，被占用则直接连接（视为已有 Harness 在跑），
  否则拉起。

---

## 二、完整保留 Harness 功能与插件（重点）

- 主窗口**完整加载** Harness Web UI，不裁剪、不替换任何页面逻辑；壳只做"容器"，
  不注入业务代码。
- `contextIsolation: true` + `nodeIntegration: false` 保持不变，但**绝不能阻断 Harness
  页面自身的脚本与插件**：Harness 及其插件均运行在 `http://127.0.0.1:<port>` 同源下，
  由 Harness 自身服务，壳不应拦截其请求 / 资源。
- preload 仅暴露最小桥接 API（如：窗口最小化 / 关闭、打开外部链接、读写壳自己的
  `config.json`、读取版本号），不得劫持或改写 Harness 逻辑。
- 插件可能打开新窗口 / 弹窗：拦截 `webContents` 的 `new-window` / `will-navigate`，
  对 Harness 自身的同源导航在壳内处理，对外部链接用系统浏览器打开，确保插件交互不丢失。
- 保持 Harness 运行环境原样：自动拉起时沿用其预期的 `DSH_HOME`（默认 `~/.dsh`）与
  用户级 node 环境，不改动、不沙箱化 Harness 的插件目录与配置，确保插件可被正常
  加载 / 启用。

---

## 三、尤其保障「插件扩展功能」

- 明确要求：桌面壳**不得削弱 Harness 的插件 / 扩展加载能力**。无论壳是"直连已有
  Harness"还是"内置拉起 Harness"，插件目录（用户级 `~/.dsh` 下的插件，以及 harness
  安装内的插件包）都必须可被 Harness 正常读取。
- 若 Harness 支持通过配置 / CLI 启用插件，壳不传递任何会禁用插件的参数；README 注明
  "插件在 Harness 侧照常管理，壳透明转发"。
- （可选增强，不强求）壳自身预留一个扩展点：允许通过 `config.json` 的 `extraPreload`
  / `injectedCss` 注入少量自定义样式 / 脚本，用于品牌化，但默认关闭，绝不默认改动
  Harness 行为。

---

## 四、其余工程要求

- 脚手架：package.json（name 建议 `deepseek-harness-desktop`）、Electron、electron-builder；
  入口 `main.js` / `preload.js` / `index.html`（加载失败兜底页）。
- 主窗口 1280x800；应用图标占位 + 替换说明。
- 桌面体验：单实例锁（`app.requestSingleInstanceLock`）、F12 开 DevTools（仅开发模式）、
  可选最小化到托盘。
- 打包：Windows 产出 nsis / portable 的 `.exe`；scripts 含 `start` / `pack` / `dist`。
- README：配置说明（harnessHome / port / autoLaunch）、运行与打包步骤、插件使用说明、
  图标替换方法。

---

## 验收标准

- 配置改为指向任意本地 harness 目录后，`npm start` 都能正确加载对应实例的 Web UI。
- Harness 的既有功能与插件在壳内全部可用（README 可列出验证过的插件清单）。
- 不修改 harness 源码目录，仅在本工作区新增文件。

## 执行方式

先给出项目结构与实现计划，再逐步写代码；每完成一个文件说明其作用与涉及的配置项。
高影响操作（安装依赖、执行打包、在用户目录新建/修改工程文件）前先向用户说明并确认。
