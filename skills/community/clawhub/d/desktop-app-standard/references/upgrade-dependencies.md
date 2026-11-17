# 实施依赖升级

按[任务入口](../SKILL.md)确定范围。新建或整体升级覆盖应用、工具链和 CI；局部任务在下节建议依赖之外，只处理解决问题所需的包及配套依赖。只读评估从仓库文件、已有解析结果和包源采集版本并输出差距，不执行安装、升级或应用测试。

先找到应用所属 workspace、构建和发布入口。新项目在脚手架生成后检查依赖；已有项目在允许实施的范围内，升级前从原锁文件建立构建／测试基线，可复用当前会话同一代码状态的结果。

## 已采用的建议依赖必须升级

建议依赖以[目标大版本表](version-targets.json)、[起手步骤](bootstrap.md)及框架指南为准。仓库已经采用时，必须查询配置源并将低版本升级到所选目标，包含开发依赖、workspace 共享声明及必要的配套迁移；未采用的组件按实际需求引入。

| 已采用的组件 | 升级目标 |
| --- | --- |
| `electron`、`electron-builder`、`electron-updater` | 目标大版本表指定 major 内的最新兼容稳定版；已有 Forge 继续使用并升级兼容的 Forge。 |
| `@tauri-apps/api`、`@tauri-apps/cli`、Rust `tauri`、`tauri-cli`、`tauri-build` | 目标大版本表指定 major 内的最新兼容稳定组合，遵守 JS／Rust 配对规则。 |
| 已使用的 Tauri 官方插件及 Electron 原生模块 rebuild 工具 | 满足目标框架、ABI 和平台的最新兼容稳定版；插件同步核对 JS／Rust 两端。 |

这项要求适用于维护和局部任务，也包含达到目标所需的跨 major 更新。不能因为当前 pin、声明范围、开发依赖分类或与本次故障无关而仅给出升级建议。用户明确锁版、只读要求或已证实的兼容性阻碍优先；未能升级时记录当前版本、目标版本、具体阻碍和复查条件，并继续其余可完成的升级。

## 查出目标版本

每次检查已采用的建议依赖，以及新建或整体升级时，按[目标大版本表](version-targets.json)选择该 major 的最新兼容稳定版。旧 pin、脚手架输出和上游更高 major 都只作为对照，用户指定的版本优先。迁移时记录方向并验证实际版本，包括新建或整体对齐时原版本高于目标的回迁；低版本必须升级的规则本身不要求局部任务回退更高版本。采用本技能发布模板时，将目标表同步到应用的 `.github/desktop-version-targets.json`，让 tag 构建核对同一提交中的安装结果。

- 从应用、前端、测试、打包及 CI 的 manifest 收集直接依赖，包括开发和可选依赖。读取 workspace 共享版本、overrides、私有源、git/path 依赖及现有包管理器。对私有包使用项目配置的源，保留别名、workspace 协议和 fork 身份。
- npm 项目在对应工作区运行 `npm outdated --long`，逐项比较 current、wanted、latest。wanted 受当前声明范围限制。用 `npm view <包> dist-tags --json` 核对发布通道，用 `npm view <包>@<目标版本> engines peerDependencies --json` 核对兼容要求。latest 是发布者设置的标签，结合上游稳定发行说明确认目标。跨 major、0.x 的破坏性更新和旧精确 pin 都要纳入。其他包管理器用仓库所用版本的对应命令。[npm outdated](https://docs.npmjs.com/cli/v11/commands/npm-outdated/)
- 对表内 npm 包查询 `npm view <包> versions --json`，按指定 major 筛出数值最大的正式版本，排除弃用版本和预发布通道；Cargo 在同一 major 内排除预发布和 yanked 版本。在线审计的 `latestStable` 是上游参考，技能大版本与该线候选值分别在 `targetMajor`、`targetStable`。安装前再核对配套依赖、平台和项目使用的源。未指定 major 的直接依赖取满足目标栈的最新稳定版。Node 和 Rust 按 house style 的 Active LTS / stable 通道核对，Actions 按工作流的 pin 规则核对。

## 修改并解析

1. 在拥有声明的文件里写入已核实的版本，保留依赖分组和仓库的精确或范围风格。npm 项目可分组执行 `npm install <运行时包>@<目标版本>` 和 `npm install -D <开发包>@<目标版本>`。集中管理、peer、optional 或 workspace 声明宜就地编辑，再在锁文件所属根目录运行原包管理器的安装命令。单跑 `npm update` 可能停在旧 major。
2. Tauri 同时检查 Cargo workspace 的直接依赖及各应用的 JS 依赖。到配置的 crate 源查可用稳定版本，在实际拥有版本的 Cargo.toml 更新 requirements，保留 features、条件依赖与来源。在 Cargo workspace 中运行 `cargo update`，或用 `cargo update -p <crate>` 更新限定范围。核对两边锁文件，Tauri v2 API/core 取双方都提供的最高兼容 major.minor。使用 JS 绑定的官方插件取两端都已发布且兼容目标框架的同一稳定版本。CLI 和 build crate 各按自己的稳定线。[Cargo update](https://doc.rust-lang.org/cargo/commands/cargo-update.html) · [Tauri 依赖配对](https://v2.tauri.app/develop/updating-dependencies/)
3. Electron 使用目标表指定的运行时、builder 和 updater 大版本，已有 Forge 的项目继续使用兼容该 Electron 线的 Forge。按目标 ABI 重建原生模块。同步更新受影响的 CI、API、配置和测试。
4. 遇到冲突先更新配套包并迁移代码。若目标 major 尚无兼容组合或已停止支持，保留已验证的工作状态，列出未达成的目标、具体阻碍及复查条件，并继续其他升级。网络失败要记录受影响的源和包。

## 安全告警与间接依赖

- 把受影响包条目归并到实际安全公告，沿锁文件追到消费方调用。分别记录触发条件、构建期或运行时用途；开发依赖也可能处理不可信输入，不能仅凭分类排除风险。
- 不把 `audit fix --force` 建议当实施方案；先核对它是否降级父工具或改变框架。无合适修复版时记录影响边界和复查条件，不为审计清零回退旧主版本。
- 上游范围未放行修复版时，可对具体消费链和受影响版本使用定向 overrides/resolutions。跨范围升级前核对实际使用的导出、CommonJS/ESM、Node 下限与匹配语义，并用消费方集成测试验证。父级覆盖可能传到更深子依赖，必须检查最终解析树，保留仍需不同接口的无关分支。
- 用锁文件干净安装并检查依赖树，防止本机残留掩盖问题。去重或 peer 解析顺带改变 SDK 配对、插件共用实例或原生模块位置时，恢复本轮既定组合或纳入明确的升级验收；核对生成的原生工程路径。
- 保留仍未修复的告警及原因。父包升级后检查是否可移除覆盖，避免形成长期无人维护的额外版本约束。

## 验收

从更新后的锁文件干净安装（npm 用 `npm ci`），跑项目既有的类型检查、测试、生产构建和桌面启动。Tauri 在 Cargo workspace 跑 `cargo check --locked` 及项目测试。涉及 native 模块、插件、签名或 updater 时，在打包产物上验证受影响功能，记录实际测试的平台。

重新查询包源并复跑审计。逐项核对锁文件的解析值是否等于目标 major 内选定的稳定版。上游有更高 major 时可以保留在报告中。交付实际版本变化、验证结果和未达成的目标。
