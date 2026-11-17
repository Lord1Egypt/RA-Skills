# Tauri 核验与采用清单

先用本次运行核验的官方版本与目标 tag 文档。不要把此文件当作固定版本号或完整迁移说明。

## 版本配套

官方 Updating Dependencies 当前说明：`@tauri-apps/api` 与 Rust `tauri` 保持相同 minor（含 major）；官方插件 JS/Rust 配套保持相同完整版本。`@tauri-apps/cli` 对应 CLI；core、build、CLI、macros 独立发版，不要求所有数字相等。每次升级重新核验该政策与例外。[Tauri 依赖配对](https://v2.tauri.app/develop/updating-dependencies)

- 同时读 Cargo.toml/Cargo.lock、JS manifest/锁文件、Rust toolchain、项目所用插件。
- 把 npm 声明范围、Cargo 声明范围与锁定解析值分开。检查 workspace 继承、同名多版本、git/path override 与目标平台条件依赖。
- 记录目标 crate 的 MSRV 和 Linux WebKitGTK、Windows WebView2、macOS 部署目标；不要把当前系统浏览器版本当作所有用户 WebView 版本。
- 调整 JS/Rust 兼容组后，更新对应锁定依赖；避免无关全量 `cargo update` 导致难以复盘。

## 安全与体验

- 按窗口/webview 最小化 capabilities、命令权限、路径/URL scope；检查 shell/opener/fs/http 等插件。
- 在 Rust command 边界校验输入、路径规范化和权限；不把“前端是本地文件”当作可信输入保证。
- 不通过 wildcard capability、关闭 CSP 或直接开放任意 shell 绕过集成问题。
- 对新原生能力检查插件初始化、JS 绑定、capability 三者；只升级包而不授权或初始化会出现运行时失败。
- 核验协议/深链、拖放、菜单/托盘、快捷键、多屏状态恢复和应用退出；基于使用场景选择新官方 API 替代手写实现。

## 自动更新

Tauri updater 的更新签名不能关闭；更新公钥、私钥与 OS 代码签名是不同信任层。`bundle.createUpdaterArtifacts` 控制产物生成；在使用官方 action 时还需核验它实际收集和上传的文件。[Tauri 更新器](https://v2.tauri.app/plugin/updater/)

- 在 app 初始化 updater 插件，核验 capability、endpoint HTTPS、pubkey 内容和更新 UI。
- 静态 JSON 核验 `version`、`platforms[os-arch].url`、`signature`；signature 是 `.sig` 内容，不是链接。检查所有已列平台，不只本机平台。
- 安装包、updater payload 与 updater `.sig` 分清。Windows 常复用 NSIS/MSI，macOS updater 常为 `.app.tar.gz`，Linux 常为 AppImage；按目标版本官方文档确认。
- 动态服务可返回 204 表示无更新；不要把 204 判成失败。自定义平台/渠道以应用配置为准，不强制名为 latest.json。
- 不自行轮换或覆盖更新密钥；评估旧安装版信任的公钥和桥接升级方案。
- 旧用户必须能验证新产物；生成 N+1 并从实际安装的 N 做下载、验证、安装、重启和数据保留测试。
- Windows 安装更新可能导致应用退出；先处理未保存数据，不盲目自动重启。

## 多平台构建（house style）

- 6 个目标：`x86_64/aarch64-pc-windows-msvc`、`aarch64/x86_64-apple-darwin`、`x86_64/aarch64-unknown-linux-gnu`。macOS 交叉架构要在 rust-toolchain 安装对应 target；Windows ARM64 可在 x64 runner 交叉编译（NSIS），首次需实测。
- Linux 依赖按官方 prerequisites：`libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev`；AppImage 另需 `patchelf`，打开外链等场景按需 `xdg-utils`。缺包时编译失败或 AppImage 打包失败。
- rust-cache `workspaces: './src-tauri -> target'`，不要把整个源码树当缓存。
- tauri-action 按 tag 创建或复用唯一 Release，默认 `releaseDraft: true` 暂存，完整验证后自动公开；`updaterJsonPreferNsis: true`；不设 `tauriScript`（按锁文件自动选 `npm run tauri`/`npm exec tauri`，npm 的 `--` 由 action 自己补）。串行合并共享的 latest.json，全部平台完成后校验覆盖、签名与摘要，再自动公开。
- updater endpoint 指向 `releases/latest/download/latest.json`；publish 后按平台 key 全量校验。

## 插件变更

`audit.mjs` 在线模式读取 `tauri-apps/plugins-workspace` 分支 `v2` 的 `plugins/<name>/CHANGELOG.md`，截取 `(已解析版, 最新版]` 的段落并分类（breaking / security / feature）。Rust crate 与 JS 包版本不一致是 P0（运行时才失败，通常表现为缺命令）。

官方 GitHub pipeline 用于核对参数；草稿用作内部暂存，由 verify job 校验后自动公开。[Tauri GitHub Actions 指南](https://v2.tauri.app/distribute/pipelines/github)
