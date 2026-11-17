# 报告与审阅基线

## 按任务交付

先写结论、实际改动和阻碍，再给出支撑结论的证据。按检查范围选择内容，无需每次生成完整报告：

- **依赖升级**：原解析版 → 实际解析版、目标与来源、锁文件/还原结果及兼容验证。SDK、TFM 和运行时分开说明。
- **风险发现**：影响、依据位置、confirmed/heuristic/unknown、处理及验证。框架风险与 CI/Release 发现分开；`notice` 和已接受偏离不计入 P0/P1/P2。
- **CI 与发布**：所测提交、实际执行的 job、产物和更新链路，区分本机、托管 runner 与设备验收。
- **性能**：同一环境下的前后测量；无数据时写待测。

保留影响结论的采集失败、未验证范围和具体复查条件。只读任务交付发现与建议，实施任务说明做了什么、如何验证。

## 事实与推断

- 目标表内的组件按技能规定的 major 核对。npm 的上游 latest 指 dist-tag，Cargo 的上游稳定版排除 yanked 和预发布。报告的 targetStable 用于寻找该 major 的最新稳定候选，实际采用值以应用锁文件和兼容验证为准。

- 当前版本由锁文件/实际安装/已发布产物分别提供，不以声明下界冒充实际版本。
- `usageHints` 是代码形字符串命中，不是调用图、漏洞可达性或语义证明；无匹配不等于无影响。
- `ciFindings` 不能解析完整 YAML（`confidence: heuristic`）；可能命中字符串或脚本文本。必须人工阅读上下文，追踪 reusable workflows。
- `latestReleaseTag` 取自 `releases/latest`；拿不到时 `latestMajor` 退回前 100 个 Action tags 里最高的 `vN`，**不是确认的最新可用版本**；`tagListingTruncated`（tags 满 100）必须保留。需要时分页核验并读取 action metadata。
- `collectionComplete` 只描述脚本的有界事实采集，不包括插件所有 changelog、CVE 数据库、构建、签名、性能或真实更新测试。
- `.NET` 的 TFM/EOL 来自官方 release metadata；`global.json` 的 `rollForward` 结论按官方语义（只有 `latest*` 保证选到最新，默认是 `patch`）。脚本不执行 `dotnet`/MSBuild，项目旁最近的 global.json 只是静态线索；CLI 从命令的工作目录向上查找，用实际构建目录里的 `dotnet --version` 核验；`netstandard` 是库 TFM、`net4x` 是 .NET Framework，都不走 .NET 运行时 EOL 数据。
- 扫描跳过符号链接或不可读目录时，那些子树没有被审计：`collectionComplete` 为 false、退出码 2，文本报告的 Heads-up 会逐条列出（JSON 的 `scan.skipped` 保留完整清单）。
- Node 的 Active/Maintenance/EOL 来自 nodejs/Release 官方 schedule；`node-version-*` 的 pin 位置是行扫描（heuristic），CI 是否真的按该版本执行仍需读 `setup-node` 步骤。P 级只针对 CI 的 `node-version` / `node-version-file`；`.nvmrc`/`.node-version` 是可选本地文件，过期只作 Heads-up。Node 是构建工具，不是应用运行时（Electron 内置 Node）。

## 基线策略

报告的 `applications` 列出应用目录及配置来源，`workflowScopes` 给出 workflow、job、步骤、构建目录、应用归属和未核验原因。应用相关发现带可选 `application` 字段；schemaVersion 3 保留单应用的 `tauriConfig`，兼容 schema 2/3 审阅基线。

路径关联采用 block-style workflow 的静态线索。表达式、目录／配置覆盖和 reusable workflow 需要人工核对；此时 `collectionComplete` 为 false。上游版本及 release 采集仍按组件汇总，逐应用配置和配对证据用于判断具体应用。

需要保留的报告、总结和基线放在 Git 忽略目录，例如 `desktop/release/audit-reports/YYYYMMDD/`；允许修改的任务可建立专用目录并加入 `.gitignore`。只读评估使用已有忽略目录、项目外临时目录或终端输出，不为保存报告修改项目文件。已有未提交报告不批量删除；用户要求整理时再移入忽略目录。

基线可选，用于下次减少重复阅读 release；不需要跨次比较时只输出终端结果即可，不必每次产生文件。需要保留时，在同一忽略目录内使用 `.desktop-app-standard-review-YYYYMMDD.json` 作为新基线文件；先审阅 audit JSON，再显式 `--confirm-reviewed`。后续 `--since-baseline` 传入该文件的实际路径。脚本拒绝离线/采集失败/截断的报告和覆盖现有文件；不同项目路径不能复用。

基线储存已审阅 release ID，不储存“已修复”。`--since-baseline` 只标注 reviewed=true/false；仍计算当前依赖、上游、CI 和兼容性。不要只输出未读 release 而隐藏长期未处理风险。

需要长期追踪的取舍写入已有 policy、issue 或决策记录，保留原因和复查条件，无需另建台账。旧版 `.desktop-version-watch.json` 的“见过的最高版本”不能自动迁移为“已审阅”。

## 定期运行

频率和载体由用户或项目决定；安全公告和 EOL 可触发提前复查。沿用已有依赖管理工具，不因采用本技能另设调度或替换 Dependabot。

如用户要 CI 自动报告：先确认目标仓库、权限与报告载体，用最小只读权限采集并保留失败状态，不自动改锁文件/合并 PR/发布。脚本退出 2 是不完整而非成功，应让维护者看到而非 `|| true` 静默吞掉。

## 多项目回查

仅在任务涉及多个应用时，按各应用的分发渠道、PR/tag 入口、产物和待验证项汇总。先验证共用模板的改法，再回查受影响项目；复用已有报告和证据，不重复抄写执行记录。
