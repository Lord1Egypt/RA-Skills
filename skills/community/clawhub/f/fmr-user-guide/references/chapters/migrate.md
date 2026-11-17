# 从 Skill 模式迁移

## 进入条件

- 用户自述旧 Skill 模式 / OpenClaw 存量（`openclaw.json` 留有 `free-model-router` provider 条目）。
- 意图话术："我是老版本""从 Skill 模式迁过来""换成新的装法"。

> 术语说明（仅本章面向 Skill 模式存量用户）：旧安装形态称 **Skill 模式**（OpenClaw 技能），新装形态称 **Standalone 模式**（便携包 + 平台服务）。

## 背景（陈述，不教操作）

Skill 模式的官方升级 = `stop` + `setup`（技能文件更新后重启进程）。该形态已逐渐弃用，本章不展开其操作细节；迁移目标是装上 standalone 形态。

## 迁移原理

两种形态**共享同一数据目录** `~/.free-model-router/`，且 Skill 形态的 CLI 卸载不清数据目录。因此迁移 = 直接按 install 章安装 standalone——渠道 key、主备模型、路由策略、autoUpdate 配置全部自然继承，无数据迁移步骤。

## 流程

1. **记录现状**：Router 在跑则 `GET /api/status` 留底；找到旧 Skill 目录位置（通常 `~/.openclaw/skills/free-model-router`）。
2. **装 standalone**：走 `${CLAUDE_SKILL_DIR}/references/chapters/install.md`。
3. **核对继承**：`data/router-config.json` 的渠道 key 与主备模型仍在；`current` 指针指向新版本目录（新旧同血统：`versions/` 目录结构与文件时间戳可观测；旧布局安装则看数据目录未被重建）。
4. **主备角色确认**：Skill 形态的 `configureModelRole primary` 曾把原主模型移入 `openclaw.json` 的 `fallbacks`，且卸载/迁移**不自动回滚**——检查 `agents.defaults.model.primary` 现指向何处，按用户意愿确认（保留指向 FMR 虚拟名，或改回原模型）。
5. **接入层指向**：`openclaw.json` 的 provider `baseUrl` 仍指 `127.0.0.1:5678`，standalone 起来后继续有效；其余 harness 按 access 章接入。
6. **清理告知**：旧 Skill 技能与它的 OpenClaw cron 任务（`free-model-router-event-check` 等）在 OpenClaw 技能管理界面移除技能时清理；standalone 自身无 cron。

**迁移期专属陷阱**：机器上留存的 Skill 形态 CLI 在 Router 停止时会误拉其自带旧版 core（写共享数据、覆写 `router.pid`）——Router 停止时勿"跑个 CLI 命令看看"，判活走探针（见 usage 章 ③类陷阱）。

## 完成判据

1. standalone P2/P3 通过（healthz 200 + `/api/status` 正常）；
2. 数据目录未被重建：渠道 key 仍在、`current` 血统/文件时间戳早于本次安装时刻；
3. 接入层指向新服务面（healthz + 一轮虚拟名请求，移交 access 章验证话术）；
4. 已向用户交代：哪些配置沿用（渠道 key、主备、路由策略、autoUpdate），哪些需确认/重配（openclaw.json 主备角色、旧 cron 清理）。

## 收尾：能力速览一屏

完成判据全过后，按 `${CLAUDE_SKILL_DIR}/references/chapters/capabilities.md` 附**能力速览一屏**（standalone 已是正常态，走 `/api/features` 主通道）；对 Skill 形态存量用户，这一屏顺带回答"换到新装法后多了什么"。
