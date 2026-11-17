# House style（默认做法）

以下是 Tauri/Electron 的默认选型；版本维护统一按[依赖升级流程](upgrade-dependencies.md)，沿用组件、包管理器或 pin 形式不代表冻结版本。用户明确选择、只读要求和已证实的兼容性约束优先。

## 优先级

1. 用户本次明确要求。
2. 本技能明确指定的[组件大版本](version-targets.json)。在该 major 内安装最新兼容稳定版本。
3. 项目有原因和复查条件的支持契约或 policy 偏离。与指定大版本冲突时，报告未对齐的原因并继续其他升级。
4. 其余项目按本 house style 及上游默认值处理。

新建和升级应用时，本次请求已涵盖范围内的本地改动和验证。对明确的支持契约记录约束及复查条件。只读巡检输出差距和证据。

默认做法统一由本文说明，policy 仅保留脚本读取的平台和偏离，不复制发布流程或签名规则。无需为每个项目创建 policy；确需记录取舍时再复制 [policy 模板](../templates/desktop-policy.example.json)，保留空的 `deviations`。有实际决定后再添加条目，例如限制平台时填写 `{"rule":"platforms","value":["windows-x64"],"reason":"首发仅支持 Windows x64","revisitWhen":"完成 ARM64 安装验收"}`；接受某个发现时用它的 id 作为 `rule`。

## 平台与产物

| 平台 | 架构 | 正式（可更新）产物 | 便捷产物 |
|---|---|---|---|
| Windows | x64、arm64 | NSIS 安装包（可自动更新） | portable zip / portable exe（免安装试用，标注不自动更新） |
| macOS | arm64、x64（Tauri 分架构；Electron 同一 job 双架构） | dmg；更新载体 Tauri `.app.tar.gz` / Electron zip | — |
| Linux | x64、arm64 | AppImage（自动更新载体）+ deb + rpm | Flathub/Snap 按需另议 |

- 默认覆盖全部 6 个目标。runner 不可用（如私有仓库没有 arm runner）时用交叉编译或在 policy 中声明偏离，不静默缩减。
- Linux 构建用 ubuntu-22.04（较旧 glibc，兼容面更广）；只有依赖要求时才升级。
- 安装包是正式产物；portable 只是便利。updater 指向的必须是可被替换的安装产物。
- **安装包界面语言**：安装和卸载向导统一英文，自定义页面、按钮与提示文案也使用英文。语言列表仅保留英文并关闭语言选择器，避免随系统或应用语言切换。Tauri 在 `bundle.windows.nsis` 设置 `"languages": ["English"]`、`"displayLanguageSelector": false`；electron-builder 在 `nsis` 设置 `"installerLanguages": ["en_US"]`、`"displayLanguageSelector": false`。已有自定义 NSIS 脚本或 hook 时，同步核对实际生效的语言及文案。发布验收在中文 Windows 上运行安装和卸载向导，确认均为英文。[Tauri 配置](https://v2.tauri.app/reference/config/#nsisconfig)、[electron-builder NSIS 配置](https://www.electron.build/docs/api/app-builder-lib.interface.nsisoptions/)
- **技术栈产物边界**：本表只适用于 Tauri/Electron；WPF 的安装范围、权限及分发矩阵统一由 `wpf-desktop` 规定。Tauri/Electron 的便携形态也不直接套用安装器更新链，按实际包型验收。

## 工具链

- **Node**：当前 Active LTS（按 nodejs/Release 官方 schedule 判定，不写死 major）。
  - CI 钉具体 major 以便复现；`audit.mjs` 会在该线进入 maintenance/EOL、落后于最新 LTS 时报出来。**不要写 `node`/`latest`**：那会跟到非 LTS 的 Current 线。
  - `engines.node` 与 CI 钉版是**两件事，不要混**：`engines` 表达「这段代码最低能在什么 Node 上跑」，CI 钉版表达「这次发版用什么版本构建」。`engines` 的下限应当**从工具链自己的 `engines` 约束里取**（如 ESLint 10 要求 `^20.19.0 || ^22.13.0 || >=24`、Vite 8 要求 `^20.19.0 || >=22.12.0`，取其交集并排除已 EOL 的线），而不是抄 CI 的 major——照抄会声明一个根本装不起来的下限（Vite 8 装不上 Node 18），也会让 Node 20 这类已 EOL 的线继续被声称支持。
  - `.nvmrc` / `.node-version` 是**可选**的便利件，给本地开发指个版本用；它不是契约，也不必与 `engines` 一致。**少一处要同步的东西。**
  - `audit.mjs` 的 P 级只针对 CI 的 `node-version` / `node-version-file`；本地 `.nvmrc` 过期只作 Heads-up。
  - Node 只是构建工具，不是应用运行时（Electron 内置 Node，版本由 Electron major 决定）。
- **npm**：默认包管理器。CI 用 `npm ci`（锁文件入库，按 `integrity` 校验），本地用 `npm i`。锁文件是唯一事实来源。
  - Yarn / pnpm / bun 项目不强迁：脚本照样能读它们的锁文件。存量 Yarn 1 项目 CI 必须 `--frozen-lockfile`；需要迁移包管理器时，独立验证安装、缓存和锁文件行为。
- **Rust（Tauri）**：stable toolchain；Cargo.lock 入库；遵守目标 crate 的 MSRV。

## 框架选择（新应用）

- **Tauri**：默认首选 Tauri 2，JS／Rust 兼容组合统一按[Tauri 配套规则](tauri.md#版本配套)选择。
- **Electron**：需要 Chromium 一致渲染、Node 生态或现有 Electron 代码时选用。打包用 **electron-builder + electron-updater**：它是三平台（含 Linux AppImage）都有自动更新的主流方案。Electron 官方默认推荐 Forge；已用 Forge 的项目继续用 Forge，不为风格迁移。
- Electron 使用[技能目标表](version-targets.json)指定的 major，安装该线最新稳定版。上游支持窗口用来核查该目标能否继续获得补丁。
- Electron、builder、updater 的版本独立。从实际使用的包源核对稳定通道，遇到 GitHub 标签领先时，确认目标包已发布且属于稳定线再安装。

## 版本与发布

- **git tag `vX.Y.Z` 是唯一版本源**。发版提交先改 package.json（Tauri 的 `tauri.conf.json` `version` 指向 `"../package.json"`），再打 tag；release workflow 断言一致，不一致即失败。
- 发布流采用校验和测试 → 构建/打包 → 直接公开。Tauri 使用官方 Action，Electron/WPF 使用 softprops 的 draft: false；审批、草稿、provenance 与额外证据按项目明确要求添加。
- 需要手动运行按钮时，将 workflow 放在默认分支；tag 运行的是**被打 tag 的提交里的 workflow 文件**，不要求源码只能来自默认分支。手动重建已有 tag 时选择该 tag ref，确保事件提交、验证提交和打包输入一致。
- 发布必须依赖所发提交的测试结果；模板使用 `needs: validate`，已有 reusable workflow 或外部门禁需核对实际依赖。
- immutable releases 按仓库已有配置及发布 Action 的实际支持适配。
- 多个应用共用一个发布仓库（release hub）时，tag 加应用前缀（如 `appA-v1.2.3`），两边都从 tag 推导名称和版本。

## 签名

| 层 | 默认 |
|---|---|
| Tauri updater 签名 | 必须；私钥只在 secrets；不随意轮换（旧客户端只信旧公钥） |
| Windows | 公开分发采用签名，首选 Azure Artifact Signing；未签名期间在 release 说明提示 SmartScreen |
| macOS | Developer ID + 公证；没有 Apple 账号时 Tauri 用 ad-hoc（`signingIdentity: "-"`）并写明打开方式；Electron 未签名则 macOS 只能手动更新 |
| Linux | 无系统签名；SHA256SUMS；attestation 按需 |

## winget

- winget 是 Windows 的次要渠道，GitHub Release 才是事实来源。
- **清单归 winget-manifests 仓管**：那边 `apps.json` 是唯一源，它自己巡检各发布仓的 release，重生成 manifest 并往 winget-pkgs 开 PR。发布仓**不提交清单**——加进 `apps.json` 即可。
- **一种机制**：两条路写同一个包，等于开两个 PR，第二个被当重复拒掉，看起来就像「winget 坏了」。
- 不在那个流水线里的发布者，才在发布工作流的最后一个 job（`needs: publish`，仅稳定版）用 winget-releaser（基于 Komac）提交；需要 classic PAT（`public_repo`、`workflow`）存为 `WINGET_TOKEN` 并做预检；首个版本手工提交。
- 不依赖 `on: release: published`：用 GITHUB_TOKEN 发布的 release 不触发其他 workflow。

## 依赖与 Action

- 新项目默认使用 Action 大版本标签。升级项目时阅读最新稳定 major 的迁移说明，调整工作流和 runner 后验证，并保留项目原有的 pin 策略。
  - 项目要求完整 SHA 或精确版本时，更新到已核实的稳定 release 对应的提交或版本。
  - 产物写入类 Action 使用可移动标签时，审计会记为 `action-moving-ref` 提示。核对 release 创建、attestation 与上传步骤的权限。
- 沿用既有仓库的 Dependabot 配置；已有自动更新配置不替代本次依赖升级和验证。

## 应用默认体验

- 不默认开机自启；关闭到托盘由产品需求决定；主题跟随系统；遥测默认关闭，开启需声明并获同意。
- Electron：`contextIsolation`、`sandbox`、禁用 `nodeIntegration`、严格 CSP、窄 IPC。Tauri：最小 capabilities，Rust command 边界校验输入。
- 常驻托盘应用创建拖放或剪贴板临时文件时，按实际保留期清理应用拥有的过期文件。运行期间也要触发清理，跳过仍在使用的文件。
- 有长译文的工具栏需在最窄支持尺寸验证主操作可达。项目可选换行、溢出菜单或带可访问名称的图标按钮，保留键盘操作和可发现性。

## 何时重新评估

上游改变推荐（如 Tauri pipeline 文档、electron-builder 签名方式、GitHub runner/attestation 变化）、平台签名政策变化、用户群出现新平台/架构需求、或某条偏离到了 revisitWhen。
