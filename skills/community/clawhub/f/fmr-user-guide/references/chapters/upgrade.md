# 升级 / 回退 / 卸载

## 进入条件

- 意图话术：升级、版本、回退、卸载、"更新没生效/更新失败"。
- 分发进入：SKILL.md 版本门 P4 拦截写操作时；install 章完成后版本核对不一致时。
- 开局顺带：执行 `event-check` 一次（upgrade 章是其触发点之一；输出解读见 `${CLAUDE_SKILL_DIR}/references/data/events.md`）。

## 版本判定（先于一切）

用版本门 P4 文件比对法：CLI 所在 zip 根 `package.json` 版本 vs 安装目录 `current` 指针指向版本的 `package.json`（落地细则见 SKILL.md：无 CLI 的 standalone 安装即比对版本目录根）。Router 活着时以 `GET /api/status` 的 `version` 字段交叉核对。

- 一致 → 用户问"什么版本"就直接回答，无升级动作；
- 不一致 → 版本漂移（自动更新已切指针而进程未重启，或工具链滞后），按下方路径处理。

## 两条升级正路

1. **自动更新**（默认开启）：Router 每 8h±1h 检查新版本（周期为时点观测，以所装版本实测为准）；SHA256 校验通过才下载，落 `versions/{ver}/` 后切换 `current` 指针；失败自动回滚并有连续失败熔断；manifest 版本 ≤ 当前版本拒绝（降级保护）；docker 容器不自动应用。三档模式 `autoUpdate.mode`：`auto`（默认，空闲窗口自动应用）/ `notify` / `disabled`（无对应 REST 端点，变更走 data-map.md 配置手改白名单，改前护栏见其"改法"；热更新生效）。
   - 手动触发/查看（REST，本机免密）：`GET /api/version-info`（当前 vs 最新）、`POST /api/apply-update`、`GET /api/update-status`（只读核对用）。
2. **重跑一键安装**（install 章同一命令）：检测到既有安装按升级处理——先停旧服务再动文件，新目录完整落盘后才切 `current`。`--force` 才允许重装/降级；非 semver 版本同样要 `--force`。

## "更新没生效"

症状"升级了还是旧行为"：按版本判定。文件已是新版而 `/api/status` 的 `version` 仍旧 → 旧进程还在跑：**平台拉起面重启服务**（勿用 CLI 拉起——Skill 形态 CLI 会误拉旧版 core，见 usage 章陷阱）。

## 持久边界

| 操作 | 丢什么 | 一定不丢 |
|---|---|---|
| 自动更新 / 重跑一键安装 | `versions/` 旧目录按 retainVersions=3 修剪 | `data/router-config.json`（含 `server.host/port`、渠道 key、主备模型）——数据目录原封 |
| 卸载脚本（无参数） | **整个 `~/.free-model-router/` 含数据** | 无 |
| 卸载脚本 `-k` / `-KeepData` | 应用目录、服务面、自启项 | `data/` 与 `logs/` |

## 卸载

- **standalone**：安装目录内 `uninstall.sh` / `uninstall.ps1`。默认删整个数据目录；保数据加 `-k` / `-KeepData`。执行前向用户确认数据去留，确认结果决定参数。
- **Skill 形态背景（迁移期用户）**：CLI `uninstall` 语义不同——只停进程 + 删 `openclaw.json` 的 FMR provider 条目；`~/.free-model-router/data` 原样保留、cron 不删、主备模型角色不回滚（`agents.defaults.model.primary` 可能仍指向已删条目，需人工改回）。包内 `_meta.json` 声称"卸载后 OpenClaw 配置自动回滚"——实际行为是删除 provider 条目而非恢复原文件，以此处为准。

## 完成判据

- 升级/回退：`current` 指向目标版本，且 `GET /api/status` 的 `version` 与之相等；`GET /api/update-status` 无未消化回滚记录（只读核对）。
- 失败：向用户报告已回滚至旧版本 + 失败原因，以事件（`announce` 的版本公告）与日志为佐证；随后转 troubleshoot 章。
- 卸载：以用户确认的数据去留为准核对目录现状（删/留与选择一致）。

## 收尾：能力速览一屏

升级/回退完成后，按 `${CLAUDE_SKILL_DIR}/references/chapters/capabilities.md` 重给**能力速览一屏**：新版本可能新增特性、组合或变更 `lifecycle`，一律以升级后实测的 `/api/features` 为准，与升级前的差异点出一二即可。卸载路径无此收尾。
