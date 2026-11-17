# Electron 核验与采用清单

## 支持窗口与依赖边界

Electron 官方支持最新三个稳定 major，且每条受支持稳定线只维护最新 minor；不能把“仍属受支持 major 的旧 minor”视作补丁覆盖完整。用本次官方 schedule 确认支持情况和日期。[Electron 支持时间线](https://www.electronjs.org/docs/latest/tutorial/electron-timelines)

- 查询 Electron 精确目标 release，列出 Chromium/Node/V8、最低 OS、架构变化；系统 Node 与 Electron 内置 Node 不是同一运行时。
- 保持现有 Forge/builder 方案。分别查询 Electron、打包器、updater 的稳定发行，按兼容区间更新每个已用组件。
- 对原生模块检查 Node/Electron ABI、N-API 支持、目标架构、`@electron/rebuild`（旧名 `electron-rebuild` 已弃用）和 ASAR unpack；不能把 `npm test` 在系统 Node 下成功当作原生模块在 Electron 中可用。
- Electron 42 起不再在 postinstall 下载二进制（首次运行时下载，`ELECTRON_SKIP_BINARY_DOWNLOAD` 已移除）；CI 与打包前显式 `node node_modules/electron/install.js`（Yarn：`yarn run install-electron`）。后续版本仍以目标包与官方文档为准。[Electron 42 发布说明](https://www.electronjs.org/blog/electron-42-0)
- 目标架构以所选 Electron 版本的官方发布资产为准；house style 默认 x64 + arm64，不以旧版本的架构支持推断当前仍可构建。
- 从配置的 npm 源安装[技能指定大版本](version-targets.json)内的最新兼容稳定版。遇到上游移除目标架构等限制时，记录受影响的包和未达成的目标。迁移时按[升级采用清单](adopt-checklist.md)筛选受影响能力。
- 较旧应用可先到受支持的安全过渡线，再逐 major 处理适用 breaking changes；明确最终目标及暂缓期限。

安装二进制时，npm 优先直接调用已安装 electron 包的 `install.js`，路径按 workspace
实际安装位置调整，避免本地 bin 缺失时 npx 回落到 registry 上同名的 `install-electron` 包。
Yarn PnP 等不使用 `node_modules` 的项目沿用包管理器的本地 bin 调用。

## 安全基线

默认采用 `nodeIntegration:false`、`contextIsolation:true`、`sandbox:true`，保持 webSecurity、限制 CSP、远程内容隔离和导航/新窗口/权限处理。对每个特权 IPC 校验 sender origin、输入 schema 和授权；通过 contextBridge 暴露窄接口，不暴露整个 ipcRenderer、文件系统或任意命令执行。[Electron 安全指南](https://www.electronjs.org/docs/latest/tutorial/security)

- 45.x 起 sandboxed preload 不再有 `Buffer`、`events`、`timers`、`url`、`setImmediate`、`clearImmediate`；用 polyfill 或把工作移到 contextBridge/main 边界，不要用 `sandbox: false` 修缺模块。target release 改变 preload 能力时按官方迁移方案处理。
- 45.1+ 可用 `session.registerPreloadScript` 的 URL/origin 过滤（`matches`/`excludeMatches`/`includeGlobs`/`excludeGlobs`）把 preload 限制到需要的页面，比一条全局 preload 更小权限面。
- 外链只允许明确协议与可信 URL；深链参数按不可信数据处理。
- 审查 fuses、打包完整性与调试入口；适用时启用，并验证实际打包产物。
- 新能力与受实验开关保护的能力分开；不为了恢复旧 API 全局启用不安全 Blink 特性。
- 凭证使用操作系统安全存储；45 起 `safeStorage` 同步 API 弃用、46 移除，改用 async，并检查平台后端与失败模式；不要假设所有平台加密保障一致。
- 屏幕/窗口/标签捕获在权限处理器里是 `display-capture`（不是 `media`）；同时实现 `setPermissionRequestHandler` 与 `setPermissionCheckHandler`，默认拒绝。

## 支持窗口的自动判定

`audit.mjs` 从 `releases.electronjs.org/releases.json` 计算当前受支持的 3 个 major：已落出 = P0，处于最旧一条 = P1（下一个 major 发布即落出）。只升到最新 minor 才有补丁。

## 自动更新与分发

不要混淆 Electron 内置 `autoUpdater` 与 `electron-updater`。先查现有 app 使用哪一种及其 provider，再应用对应规则。[electron-builder 自动更新](https://www.electron.build/docs/features/auto-update)

对于 electron-builder + electron-updater，当前官方文档列出：Windows NSIS；macOS DMG 分发且 Squirrel.Mac 更新需要 zip；Linux 有 AppImage、DEB、RPM、Pacman 等受支持 target。**不是仅 Windows 可用**。macOS 自动更新需要应用签名。目标与更新行为仍应按所用版本验证。[electron-builder 自动更新](https://www.electron.build/docs/features/auto-update)

- Windows 常见 `latest.yml`、macOS `latest-mac.yml`、Linux `latest-linux.yml`；beta 等使用对应 channel。provider 可能有其他布局，不能只 grep 一个文件名断定没有更新。
- 上传 manifest 指向的全部真实产物和所需 blockmap；核验 `files[].url`/散列/大小、架构、版本和权限。不同架构不要互相覆盖同名清单。
- macOS 打包/更新通常需要 dmg+zip，不是“只有 dmg 即更新完整”。
- Windows portable exe/zip 不能直接套用 NSIS 安装更新链；要么明确不支持自更新，要么验证实际便携更新实现。
- 核对 electron-builder 与 electron-updater 各自的 npm dist-tags、版本和 release notes，使用已经发布到源的稳定版本。
- 检查 provider、updater metadata schema 与已发布旧 updater 的兼容范围；新 builder 生成了新字段不代表旧安装版能读。
- 不把 PAT/CI token 打包给终端用户。私有更新使用适当的用户认证/代理/受控签名 URL，并验证跨源凭证处理。
- 大版本升级、签名身份变化、安装路径变化和 schema 迁移都要从 N 安装版实测，不只在开发模式检查更新事件。

## 多平台打包（house style）

- 每个 OS 一个 job，同一 job 内 `--x64 --arm64`；`--publish never`；唯一 publish job 上传。
- Windows `nsis`（双架构合一安装包 + 单一 `latest.yml`）；macOS `dmg` + `zip`；Linux `AppImage` + `deb` + `rpm`。
- electron-builder 的命令行 target 会覆盖配置中的 target 列表。目标统一放在配置中，命令行只选平台与架构；需要临时指定 target 时核对最终产物，避免漏掉 portable 等配置目标。
- 原生模块：交叉架构需在对应 runner 上 rebuild（如 Linux arm64 用 `ubuntu-22.04-arm`），不能只在 x64 上交叉打包。
- 签名见 [发布流程](release-flow.md)；electron-builder 大版本升级时按实际安装版本核对签名配置，不照搬预发布计划。
