# CI 与直接发布

默认在 tag 校验、测试和资产校验通过后自动公开 Release。Tauri 使用官方 Action 暂存草稿，完成矩阵与校验后自动公开，Electron 与 WPF 使用 softprops/action-gh-release 的 draft: false。按应用适配工作目录、命令和产物。参考项目的具体做法见[大型项目工作流](workflow-examples.md)。

## 日常 CI

PR 在只读权限下运行锁文件安装、项目已有的 lint/typecheck/test/build。桌面运行验证按支持平台配置。Tauri Linux 先安装系统库，Rust 使用 locked 安装和测试；需要启动 Electron 的测试显式安装该项目的 Electron 运行时。WPF 在 Windows 构建和执行窗口 smoke，测试 runner 按项目的 MTP 或 VSTest 配置。

## 三栈发布入口

| 栈 | 模板与发布方式 |
| --- | --- |
| Tauri | [release-tauri.yml](../templates/workflows/release-tauri.yml) 校验 tag、配置版本与依赖后，矩阵使用 tauri-apps/tauri-action，releaseDraft: true，暂存安装包、签名和 latest.json。verify 核对平台覆盖并附加 SHA256SUMS 后自动公开。 |
| Electron | [release-electron.yml](../templates/workflows/release-electron.yml) 校验后按 OS 构建 artifacts，electron-builder --publish never；单一 publish 下载全部本轮 artifacts，在本地验证清单和 SHA-512、生成 SHA256SUMS，再调用 Release Action 直接发布。 |
| WPF | wpf-desktop 的 templates/ci.yml 用 test → release；生成所选 profile、签名、安装器及完整 ZIP，运行解包 smoke，再直接发布明确的文件列表。 |

Tauri 官方 Action 合并同一个 latest.json，模板串行执行这些写入者。首个矩阵目标创建草稿，后续目标补齐资产；verify 检查全部目标、签名和摘要后自动公开。构建或校验失败时保留草稿，不向更新客户端暴露不完整版本。

## 版本与重跑

- tag vX.Y.Z 对应应用版本；Electron 默认模板接受稳定版。发布前同步 package.json，Tauri 配置引用该版本；WPF 从 tag 注入 publish。依赖目标表随 workflow 入库，校验实际解析版本。手动重跑选择对应 tag ref，构建检出已验证的 commit。
- softprops 使用 make_latest: legacy，按 GitHub 的版本规则判断 latest。Tauri 沿用官方 Action 的发布逻辑。预发布通过各自 channel 测试，普通用户的稳定 endpoint 仍需验证。
- Tauri 同一 tag 重跑只允许复用未公开草稿；已公开时拒绝覆盖，修复使用新版本。其他发布器上传同名文件按 Action 的覆盖行为处理。签名和打包完成后再计算摘要，检查本次文件集合；公开后的不兼容修复通常发布新版本。
- 仓库已开启 immutable releases 时按 GitHub 的资产不可变限制及所用 Action 的支持情况适配。审批、provenance、SBOM、严格构建证据等按用户或仓库要求添加。

## 自动更新与签名

Tauri 的 createUpdaterArtifacts 和更新私钥配套，公钥可入库；Windows 默认 updaterJsonPreferNsis: true，macOS 需要 .app.tar.gz，Linux 使用适用的 AppImage 更新载体，保留对应 .sig。首发后从 N 安装版实测到 N+1。

Electron 每 OS 在同一 job 打所需架构，避免 latest-mac.yml 被覆盖；含原生模块时按目标架构构建或 rebuild。Windows 使用 NSIS，macOS 同时保留 dmg 和更新 zip，Linux 按项目 target 分发。手动上传时让最终资产名与 manifest 的 URL 一致，上传 manifest 引用的文件与 blockmap，并比对 SHA-512。模板处理空格转短横线；特殊 artifactName 按实际 builder 规则适配。

macOS 更新需要应用签名及适用的公证；Windows 可用 Azure Artifact Signing。未签名版本在说明里标出状态。私钥只注入可信发布构建。代码签名、updater 签名和校验和各自按项目配置核验。

## 无在线更新的产品

仅在明确离线或手动更新的产品中应用。本技能的发布模板默认要求 updater feed；停用在线更新时，联动调整应用检查／下载入口、专用依赖与权限、updater 产物生成、更新密钥输入、feed／更新签名校验及上传和 readiness 清单。保留其他功能仍需的共享依赖，不把 OS 代码签名或公证当作 updater 签名一起删除。

继续验证 tag／版本、所选平台的实际包、SHA256、公开下载和安装升级；离线产品验收实际无更新网络请求，手动更新产品验收其交付路径。已有安装用户仍依赖旧 endpoint 时，先处理客户端迁移与信任兼容，不能直接移除。

## 下载说明与发布验收

说明包含本 tag 的变更、平台/架构选择、实际提供的安装与便携形式、运行时要求、签名状态和 SHA256SUMS。模板的包型文案是起点，删除未提供的类型，写入实际签名结果。

公开后检查 tag、安装包与 feed 可下载，manifest 对应本版本且引用真实文件，并实测 N→N+1 的下载、验签、重启和数据保留。本地 YAML 检查、托管 runner 构建和设备验收分别记录。多应用共用发布仓时由一个协调 workflow 汇总各应用文件，使用独立名称和版本映射。

winget 沿用已有唯一提交路径。由本仓负责提交时，放在发布验证成功后的 job；GITHUB_TOKEN 创建的 release 不会触发另一个 on: release 工作流，可直接使用 needs 或 workflow_dispatch。

## 适配既有分发

新建与整体维护按 house-style 的推荐矩阵实施。明确的平台限制按用户当前要求处理；现有发布物较少作为待补齐差距。artifact 中转与直接 Release 上传根据项目实际配额和已有工具选择，直接上传时应记录上传期间各平台逐步补齐的行为。

## winget 与直接发布的衔接

中央 registry 复查包括 PackageIdentifier、源仓库公开可访问、包型、CPU 架构、安装范围、ARP 的 DisplayName/Publisher/ProductCode，以及实际下载 URL 和 SHA256。NSIS 多架构共享一个安装器时为每个支持架构生成条目；已登记 portable ZIP 的应用保留既有升级类型，迁移到安装器前验证旧版升级。

逐平台直接上传时，完成文件和更新清单齐备后才允许消费 release。中央巡检应等待校验和及应用必需资产，不仅凭 draft:false 选取新版本。校验清单覆盖所有下载，重跑排除校验和文件自身，缺摘要或缺平台清单应失败。登记和生成清单在本地完成，公开 Release 和提交 PR 按用户授权执行。

从 [winget-readiness.example.json](../templates/winget-readiness.example.json) 适配所选 tag 的完整必需文件集合，包含安装包、各架构 ZIP、更新清单和完成标记。中央巡检读取公开 Release API 后可运行 `node release-assets.mjs ready release.json readiness.json`，失败时保留原登记等待下轮，成功后再读取真实 URL/摘要并生成清单。它只做本地校验，不提交或联网；PackageIdentifier、InstallerType、Scope 和 ARP 仍由中央 registry 管理。

自动更新能力要按包型验收。自定义下载器按进程架构选包，缓存包含架构和版本，下载完成并验 SHA256 后再解包、最后写完成标记；纯离线应用保持手动更新。安装器自动升级、便携包校验下载和离线手动更新使用各自的真实说明。
