---
name: desktop-app-standard
description: Build, maintain or audit Tauri/Electron desktop apps, including dependencies, packaging, updates and CI. Next.js shell migration uses the corresponding nextjs-to-tauri or nextjs-to-electron Skill. 支持只读巡检，以及明确请求的 .NET SDK/TFM 静态审计；局部修复也检查已采用的建议依赖升级。

metadata:
  version: "0.9.22"
  openclaw:
    homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/desktop-app-standard
    emoji: "📐"
    requires:
      bins: ["node"]
    files:
      - scripts/audit.mjs
      - scripts/core.mjs
      - scripts/app-context.mjs
      - scripts/ci-traps.mjs
      - scripts/delivery-checks.mjs
      - scripts/dotnet.mjs
      - scripts/review-baseline.mjs
      - scripts/checksums.mjs
      - scripts/release-assets.mjs
      - references/house-style.md
      - references/bootstrap.md
      - references/upgrade-dependencies.md
      - references/version-targets.json
      - references/release-flow.md
      - references/workflow-examples.md
      - references/ci-traps.md
      - references/tauri.md
      - references/electron.md
      - references/adopt-checklist.md
      - references/report-and-baseline.md
      - references/verification-performance.md
      - references/sources.md
      - templates/workflows/ci.yml
      - templates/workflows/release-tauri.yml
      - templates/workflows/release-electron.yml
      - templates/desktop-policy.example.json
      - templates/release-plan.md
      - templates/winget-readiness.example.json
      - templates/performance-record.md
---

# Desktop App Standard

从应用所属 workspace、锁文件和构建入口确认框架及实际版本。范围由用户目标决定，用户指定的组件、平台、版本和只读要求优先。`.NET --dotnet` 仅作静态审计，不套用 Tauri/Electron 的依赖与产物标准；WPF 实施使用 `wpf-desktop`。

## 按目标选择入口

| 用户目标 | 检查、实施与验收 |
| --- | --- |
| 只给技能与仓库，或笼统要求维护 | 先运行在线审计，再按 [Tauri](references/tauri.md) 或 [Electron](references/electron.md) 检查框架配对、安全配置、启动与资源、打包和更新链路，并对照 [CI 模板](templates/workflows/ci.yml) 检查实际测试矩阵和门禁。用代码、锁文件或产物核实发现，落实范围内可验证的修复与 CI 缺口；其余差距说明阻碍和复查条件。 |
| 新建、整体升级或按本技能全面改造 | 新项目先按[起手步骤](references/bootstrap.md)生成骨架。按[依赖升级](references/upgrade-dependencies.md)覆盖框架、前端、构建、测试和 CI，验证更新后的锁文件、启动及适用的发布产物。 |
| 局部功能或故障 | 沿故障路径及下述建议依赖升级涉及的配套迁移实施，其余改动限于任务所需；按[验证与优化](references/verification-performance.md)验收受影响路径。 |
| 只读巡检、评估或计划 | 从仓库文件、现有产物与上游版本采集证据。交付差距、影响和验证办法，保持项目文件及锁文件原样。 |
| 排查 CI、草稿、更新清单、签名或 winget | 运行 `--ci-only`，按 [CI 陷阱](references/ci-traps.md) 核对命中的 job，按[发布流程](references/release-flow.md)检查实际送达。 |
| 查 .NET 的 TFM 支持期、SDK 下限、rollForward 或 CI 配置 | 运行 `--dotnet`。WPF 的 XAML、DPI、托盘、安装包与单文件发布实现见独立技能 `wpf-desktop`。 |
| 测启动速度、内存或体积 | 先按[性能验证](references/verification-performance.md)记录相同环境下的基准，再测改动。 |

## 已采用的建议依赖升级

Tauri/Electron 每次任务都按[建议依赖升级规则](references/upgrade-dependencies.md#已采用的建议依赖必须升级)检查已采用组件；允许修改时，低于所选目标必须升级，包含局部任务和必要配套迁移。版本选择、阻碍处理及其他依赖范围统一由该页规定，未采用的组件按需引入。

## CI 与发布的日常检查

新建和全面维护时先确认实际分发渠道，再分别报告 PR 测试和 tag 交付的证据。GitHub Releases 项目采用下表的发布链；商店、内部或人工分发项目记录其现有交付入口与验收。已有工作流达到同等结果时沿用其结构。维护时按推荐的平台与产物矩阵补齐缺口；历史发布类型较少本身不构成缩减目标。用户当前明确要求和实际兼容性约束优先。相同可执行文件已打入便携 ZIP 时通常只发布 ZIP，更新协议必需的载体、签名和清单仍需保留。局部任务按故障修复及建议依赖升级影响的路径检查；只读任务给出差距与改法。

| 应用 | 推荐入口 | 构建与发布责任 |
| --- | --- | --- |
| Tauri | [release-tauri.yml](templates/workflows/release-tauri.yml) | 官方 tauri-apps/tauri-action 使用 releaseDraft: true 暂存全部平台，核对 updater 覆盖和摘要后自动公开。 |
| Electron builder/updater | [release-electron.yml](templates/workflows/release-electron.yml) | 平台构建显式 --publish never；单一 publish 检查本地更新清单和摘要后用 softprops/action-gh-release 直接公开。示例只接受稳定版，beta 项目按真实 channel 生成和校验清单。 |
| PR 检查 | [ci.yml](templates/workflows/ci.yml) | 使用实际应用工作目录、锁文件和 scripts；覆盖承诺的平台及受影响的打包运行路径。 |

复制和改造按[模板适配步骤](references/bootstrap.md#适配已有应用的-workflow)，实际交付与重跑按[发布流程](references/release-flow.md)。默认自动发布；Tauri 草稿仅用于构建暂存，校验后自动公开，不增加人工审批。provenance 与额外证据按项目要求配置。reusable workflow 追到被调用文件和固定版本核实，大型项目参考见[工作流实例](references/workflow-examples.md)。

默认 Tauri 模板调用 release-assets.mjs 的 verify-draft，在公开前检查资产归属、六平台 feed、签名对应和真实 SHA256；Electron 在 tag 校验中调用 delivery-checks.mjs 检查有效 NSIS 英文配置。随模板复制所声明脚本，按[适配清单](templates/release-plan.md)核对外置文件、缓存架构、实际更新方式与中央 winget 完整资产门禁。audit.mjs 也输出已知源码分发陷阱，静态候选需结合实际入口验证。

## 运行审计

从任意目录调用随附脚本，替换并引用实际路径。未指定 `--out` 时只输出终端；保存报告及基线时按[报告策略](references/report-and-baseline.md#基线策略)选用忽略目录，只读任务不为此修改 `.gitignore`。在线模式可读取 `GH_TOKEN` 或 `GITHUB_TOKEN`。

```sh
node "{SKILL_DIR}/scripts/audit.mjs" "<repo>" --out "<report-dir>/audit.json"
node "{SKILL_DIR}/scripts/audit.mjs" "<repo>" --ci-only
node "{SKILL_DIR}/scripts/audit.mjs" "<repo>" --dotnet
node "{SKILL_DIR}/scripts/audit.mjs" "<repo>" --offline --json
```

审计只读项目，不运行应用脚本。`--out` 只创建指定的新文件。退出码 **0** 表示范围内采集完整，**2** 表示离线、限流、无法解析或范围受限，其他非零码表示调用失败。先读 warnings/errors，再判断优先级；离线结果仍可用于定位本地问题。

## 判断与交付

- [House style](references/house-style.md) 统一规定平台矩阵、英文安装／卸载界面、工具链与 Action 策略，并说明支持契约和 policy 的优先级；不将历史未验证状态当作跳过 CI 的理由。
- 按[验证与优化](references/verification-performance.md)选择本次范围内的检查。只读评估不运行会改动状态的安装、构建或应用测试；配置、本机、远程 runner 与设备结果分别报告。
- 用锁文件、仓库代码及[上游原文](references/sources.md)核实审计线索。`usageHints` 和 CI 字符串只是线索，按[升级采用清单](references/adopt-checklist.md)筛选本项目用到的变更。整体升级时用包管理器补查框架审计未覆盖的依赖。
- 按[报告与基线](references/report-and-baseline.md)交付证据、实际改动、版本差距、验证结果及复查条件；性能结论使用可比测量，缺环境记为待验。需要跨次复查时再保存已审阅 release 基线。
- 应用内更新按[发布验收](references/release-flow.md#下载说明与发布验收)从已安装 N 走通 N+1。远程 tag、公开 release、secrets 与 winget 按用户授权处理。
