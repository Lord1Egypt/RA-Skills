# Bootstrap：新桌面应用

目标：第一天就具备多平台发布、自动更新和持续版本跟进，而不是“先做功能，发布以后再说”。
先查已安装的 `nextjs-to-tauri` / `nextjs-to-electron` 技能：若用户从 Next.js 迁移，用它们完成前端改造，本文件只负责版本、CI 与发布骨架。

## 1. 选框架（见 house-style.md）

默认选 Tauri 2。需要 Chromium 一致性或 Node 原生生态时选 Electron + electron-builder，组件大版本见[技能目标表](version-targets.json)。

## 2. 脚手架（npm）

```bash
# Tauri
# 从 create-tauri-app 的发布说明选仍生成目标框架大版本的脚手架，将实际版本赋给 scaffoldVersion
npm create "tauri-app@${scaffoldVersion:?先设置脚手架版本}"
# Electron：选一个带 electron-builder 的模板，或在现有前端中加入：
# 从目标大版本表和包源取三个实际稳定版本，分别赋给以下变量
npm i -D "electron@${electronVersion:?}" "electron-builder@${builderVersion:?}"
npm i "electron-updater@${updaterVersion:?}"
node node_modules/electron/install.js # Electron ≥ 42 不再在 postinstall 下载运行时
# 保留生成的 package-lock.json，CI 用 npm ci
```

Electron 新项目需要可执行入口：在 package.json 指定主进程文件，为开发启动和打包配置 scripts，在主进程创建 BrowserWindow 并加载项目的页面。先启动生成的应用，再接发布模板。已有 Yarn/pnpm 项目沿用其锁文件和包管理器，复制模板时同步调整安装和缓存步骤。

脚手架生成后，按[依赖升级](upgrade-dependencies.md)逐项更新应用、前端和打包工具，核对并保留锁文件。Electron 原生模块按目标版本使用配套的 rebuild 工具。

`create-electron-app` 生成的是 Electron Forge 项目；要按 house style 用 electron-builder，就不要用它，或在第一天迁移。

## 3. 安全默认

- **Tauri**：capabilities 按窗口最小授权；只启用需要的插件；CSP 明确；Rust command 校验输入与路径。
- **Electron**：`contextIsolation: true`、`sandbox: true`、`nodeIntegration: false`；preload 用 `contextBridge` 暴露窄 API；限制导航/新窗口；启用适用的 fuses。

## 4. 自动更新

新应用默认接入在线更新；明确离线或手动更新的产品保留其选择，不安装无用 updater 或新增网络请求。已有应用沿用实际 provider、渠道与已安装客户端的信任链。

禁用在线更新时，按[离线／手动更新的发布适配](release-flow.md#无在线更新的产品)同步修改模板；仅删除前端检查或插件会留下不匹配的 feed 门禁。

- **Tauri**：`npm run tauri -- signer generate -w ~/.tauri/<app>.key`；公钥写入 `plugins.updater.pubkey`，endpoint 用 `https://github.com/<owner>/<repo>/releases/latest/download/latest.json`；`bundle.createUpdaterArtifacts: true`；私钥与密码存入 secrets `TAURI_SIGNING_PRIVATE_KEY(_PASSWORD)`，离线备份——丢了旧用户就无法再更新。
- **Electron**：electron-builder 配置 `publish: { provider: github }`；Windows target `nsis`，macOS `dmg`+`zip`，Linux `AppImage`+`deb`+`rpm`；主进程 `autoUpdater.checkForUpdatesAndNotify()`（electron-updater）。

## 5. 版本单一来源

- package.json `version` 为准；Tauri `tauri.conf.json` 写 `"version": "../package.json"`。
- 发版：`npm pkg set version=x.y.z`（与包管理器无关，只改 package.json）→ 提交 → `git tag vX.Y.Z` → 推送 tag。

## 6. 复制 CI 文件

| 模板 | 放到 |
|---|---|
| [references/version-targets.json](version-targets.json) | `.github/desktop-version-targets.json`，与工作流一起纳入版本控制 |
| templates/workflows/ci.yml | `.github/workflows/ci.yml` |
| templates/workflows/release-tauri.yml 或 release-electron.yml | `.github/workflows/release.yml` |
| templates/desktop-policy.example.json | 仅需记录偏离时创建 `.desktop-policy.json` |

模板里的 Action 标签和 Node 版本来自编写时的环境。复制后核实当前的稳定 release、Active LTS 及 runner 要求，实际更新工作流。随后执行 `node "{SKILL_DIR}/scripts/audit.mjs" "<repo>" --ci-only` 复查。直接发布和 token 权限见[发布流程](release-flow.md)。

## 7. 首次发布检查

以下外部发布步骤按用户授权执行；本地迁移或只读评估不自动授权推送 tag、公开 Release 或配置 secrets。

1. 运行审计，核对框架和 CI 发现。确认 tag 的版本源与测试门禁。
2. 推送可信 tag，检查托管构建和直接发布结果。Tauri 矩阵逐平台补齐草稿，latest.json 覆盖全部支持目标且校验成功后自动公开；Electron 单一发布器等待所有平台构建完成。
3. 匿名下载安装包与 feed，核对版本、摘要、签名和真实更新载体。
4. 在目标 OS 安装 N，再发布 N+1，验证下载、验签、重启与数据保留，记录实际环境。
5. 发布说明列出签名状态、平台/架构和下载选择。winget 沿用已有唯一提交渠道。

## 适配已有应用的 workflow

1. 从应用入口和锁文件确定 app root、Cargo root、包管理器、Node/Rust 与构建脚本。monorepo 逐应用列出这些值，版本读取和发布路径使用同一应用。
2. 对 run 步骤设置实际 working-directory；checkout、setup-node 的 cache-dependency-path、rust-cache workspaces、tauri-action projectPath、artifact path 和版本读取分别设置。Action 的路径输入独立于 defaults.run.working-directory。
3. npm 使用 npm ci；pnpm 先安装项目指定版本，再设置 setup-node 的 pnpm cache 和 lockfile 路径，执行 pnpm install --frozen-lockfile。Yarn 按现有版本安装并冻结锁文件，Corepack 在缓存步骤前准备好。根目录 npm 和子目录 pnpm 都要验证干净安装。
4. 把 lint/typecheck/test/build 换成已核实的项目命令。测试已含类型检查时复用它。承诺的检查缺失时明确补齐或报告缺口。需要启动 Electron 的测试先安装该应用实际解析到的 Electron 运行时。
5. 核对输出目录、各架构命名、provider 与 channel。Electron 默认示例仅支持稳定版；采用 beta 时同步修改 tag 校验、清单生成、上传 glob、验证文件名和公开端点，确认稳定用户和 beta 用户各自能更新。
6. 上传前生成发布说明，使用本 tag 的变更和实际资产列表，说明平台、推荐下载包、便携版更新方式、签名状态及校验入口。沿用已有 changelog 时链接真实存在的版本段。
7. 从安装后的 skill 复制模板及声明的脚本，在目标应用检查 YAML、安装、构建、测试和公开下载。随后按授权范围验收托管 runner 与真实安装升级。

Tauri 同时复制 `scripts/release-assets.mjs` 到 `.github/scripts/release-assets.mjs`。默认 verify-draft 在公开前核对草稿全部资产和更新 feed，不需要可选的构建证据。Electron 复制 `scripts/delivery-checks.mjs` 到 `.github/scripts/delivery-checks.mjs`，将模板中的 `electron-builder.yml` 换成真正生效的配置路径；NSIS 设置 installerLanguages: [en_US]、displayLanguageSelector: false。YAML 校验复用应用已安装的解析器（含 electron-builder 的依赖），不另装技能依赖；继承或动态配置先提供实际生效的 builder JSON。运行模板实际调用的检查，缺文件应先适配。

Tauri 模板串行更新共享 latest.json。需缩短耗时时先记录各目标与总耗时，再试验并行构建独立 artifacts、单一汇总 job 生成 feed；覆盖缺架构、错误签名和部分重跑后再替换当前流程。
