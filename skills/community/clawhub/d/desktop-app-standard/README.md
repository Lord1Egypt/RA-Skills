# desktop-app-standard

> Tauri / Electron 桌面应用的**新建骨架、版本巡检、升级与多平台发布检查**，以及 **.NET 运行时/SDK 审计**（`--dotnet`）Skill。

只给项目时，先巡检版本、安全配置、启动与资源、打包和发布，再修复有证据且能验证的问题。新建或整体升级按[目标大版本表](references/version-targets.json)实际更新依赖与锁文件。维护和局部修复也必须检查已采用的建议依赖，将低版本升级到目标并验证必要的配套迁移；其余改动限于任务所需范围。只读评估交付发现与证据。

## 安装

解压后把整个 `desktop-app-standard/` 目录放进代理宿主的 Skill 目录（保持 scripts/references/templates 结构）。.NET 运行时/SDK 生命周期用 `--dotnet` 审计；WPF 的 XAML/DPI/托盘与构建发布实现由 `wpf-desktop` 负责。

## 常用提示词

```text
用 desktop-app-standard 检查并维护 /path/to/app。
```
```text
用 desktop-app-standard 巡检 /path/to/app：最新稳定版、支持窗口、配对、上游变更是否影响本应用，以及 GitHub Actions 发布链路。只读，不改代码。
```
```text
用 desktop-app-standard 给新的 Tauri 应用搭发布骨架：多平台、自动更新、发布校验。
```
```text
用 desktop-app-standard 升级 /path/to/app，包括前端、桌面框架、测试和构建依赖。
```
```text
用 desktop-app-standard 审计 /path/to/wpf-app 的 .NET 运行时/SDK：TFM 支持期、EOL，以及 global.json 的 SDK pin/rollForward。只读，不改代码。
```

## 直接运行

需要 Node.js 22+（脚本自身要求；桌面项目按 house style 用当前 Active LTS）。审计脚本无需安装第三方依赖，不执行项目代码。NSIS 发布门禁在应用构建环境中复用已安装的 YAML 解析器；静态审计对 YAML 仅报告未验证提示。

```bash
GH_TOKEN=$(gh auth token) node scripts/audit.mjs /path/to/app --out /tmp/audit.json
node scripts/audit.mjs /path/to/app --ci-only        # 查 CI / 发布，读取本地依赖和打包配置辅助判断
node scripts/audit.mjs /path/to/app --dotnet         # .NET TFM/SDK/支持期 + CI 检查
node scripts/audit.mjs /path/to/app --offline --json # 无网络
node --test tests/*.test.mjs
```

- 读取 npm / Yarn classic / Yarn berry / pnpm / bun 锁文件与 Cargo.lock，按 governing lock 报告实际解析版本。
- 在线：npm/crates 最新版、Electron 支持窗口（releases.json）、Node 工具链（nodejs/Release schedule，CI pin 是否仍为 LTS；`.nvmrc` 过期只作提示）、Tauri 插件 JS⇄Rust 配对与 CHANGELOG 段落、electron-builder/updater release notes、Action 最新 release 与 `suggestedPin`（最新大版本标签）、.NET release metadata（TFM 支持期/EOL、latest SDK/runtime）。
- `--dotnet`：扫 `.csproj/.fsproj/.vbproj` 与 `Directory.Build.props`，解析 `TargetFramework(s)`（含旧式 `TargetFrameworkVersion`）和最近的 `global.json`；按官方 `rollForward` 语义判断 pin 能否到最新。报告 `dotnet`（projects/globalJson/channels）与 `dotnet-*` 发现；不执行 `dotnet`/MSBuild。
- `ciFindings`：38 条 workflow 陷阱 + 5 条仓库级发现 + 3 条在线 Node 工具链发现（[references/ci-traps.md](references/ci-traps.md)），另有 `--dotnet` 的 .NET SDK 来源检查（two-sources / shadow / setup 缺失）；`notice`（符合 house style 的提示）与 `.desktop-policy.json` 接受的偏离单列，不计入 P0/P1/P2。
- 退出码：0 完整；2 不完整（离线/限流/不可读）；其他为执行错误。只有 `--out` 会写文件，且拒绝覆盖。

多应用仓库新增 `applications`，逐应用保存目录、依赖来源及 Tauri 配置。多个应用的工作流通过字面量 `projectPath`、步骤或 defaults.run 的 `working-directory` 关联到具体应用；后者只作用于 run 步骤。应用相关发现增加 `application` 目录，文本输出也显示该目录。无法解析的矩阵路径、目录／配置覆盖参数、自定义 checkout 或 reusable workflow 标记为未核验，采集不完整并退出 2，可按应用子目录重跑及人工核对。JSON 保持 schemaVersion 3，单个有效 Tauri 配置继续提供原有 `tauriConfig`，旧审阅基线可继续读取。

## 模板（templates/）

| 文件 | 用途 |
|---|---|
| [references/version-targets.json](references/version-targets.json) | 随 release 工作流复制到应用的 `.github/desktop-version-targets.json`，用于校验实际依赖 |
| `workflows/ci.yml` | PR 检查，只读、无 secrets（Tauri 步骤按 `src-tauri/Cargo.toml` 自动跳过） |
| `workflows/release-tauri.yml` | Tauri 六目标矩阵 + 官方 Action 暂存草稿 + 全部资产校验后自动公开 |
| `workflows/release-electron.yml` | Electron 每 OS 一 job 双架构 + 单一直接发布 job |
| `desktop-policy.example.json` | 仅存放审计读取的平台与偏离；默认做法见 [house style](references/house-style.md) |

模板中的 Action 标签在采用时核对当前支持情况；模板默认 npm，存量 Yarn/pnpm 仓库按注释换安装行（漏改会报 `npm-ci-without-lockfile`）。模板的 Node major 是 bootstrap 起点，不是永久值：复制后跑 `audit.mjs --ci-only`，`node-version-*` 会指出它是否已落后于 LTS。首次使用前跑 `audit.mjs --ci-only`（.NET 项目用 `--dotnet`），并在真实仓库中跑一次完整发布与 N→N+1 更新。

Tauri 默认模板使用官方 Action 暂存草稿，并调用 `release-assets.mjs verify-draft` 核对全部资产、更新清单和摘要后自动公开。采用模板时一并复制该脚本。脚本中的 `record` / `verify` 构建证据命令仅用于明确需要该验证的工作流。

## 从旧版升级

替换整个技能目录。0.3.x 使用的名称为 `desktop-version-watch`。报告仍使用 schemaVersion 3，旧的 schema 2/3 审阅基线可继续读取。迁移旧工作流时，按本项目的平台与锁文件验证模板。日常升级使用[依赖升级](references/upgrade-dependencies.md)，只读脚本见上文。
