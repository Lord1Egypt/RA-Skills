# 日常用法

## 进入条件

- 状态前置：P3 **正常态**。
- 意图话术：切模型、看渠道、停用/启用 provider、配 key、通知与掉线询问。

## 健康与状态

CLI 没有 status/health/doctor/version 命令（能力缺口如实标注），判据一律走：

1. `GET /healthz` → 活着吗（零副作用纯探针）；
2. `GET /api/status` → 健康吗：`version`、`activeProviders`/`totalProviders`（=0 即无可路由渠道；`activeProviders` 疑为热池非空的渠道数，与已配 key 的渠道数不必相等——**口径待源码核实**，向用户转述时用"在承担路由"，不说"配了 key"）、`strategy`、`lastSync`（过旧即与控制服务器失联）、`apiKeyConfigured`（响应体另含明文 `apiKey` 字段，任何输出不回显）、各渠道主备热池；
3. `/admin` 面板 → 用户一站式查看；
4. `data/router.pid` → 进程级判活。

"跑个 CLI 命令看看活着没"不是判据——见下方③类陷阱。

探针按 SKILL.md 证据层级执行：某端点此版本不暴露时标注缺失并取次级证据，不作为故障；版本走版本证据链兜底（SKILL.md P4 落地细则：`current/package.json` → `install-info.json` 的 `nodePath` 目录 → 端点 `version` → 版本未知，旧布局无 `current` 不构成断流点）。

## 日常操作（REST；Skill 形态同义命令见 `${CLAUDE_SKILL_DIR}/references/data/cli-commands.md`）

```
BASE=http://127.0.0.1:5678
curl -s $BASE/api/providers                                     # 渠道全景
curl -s "$BASE/api/models?provider=<id>"                        # 某渠道模型清单
curl -s -X POST $BASE/api/switch-primary  -H "Content-Type: application/json" \
     -d '{"provider":"<id>","modelId":"<模型ID>"}'               # 切主模型
curl -s -X POST $BASE/api/toggle-model    -H "Content-Type: application/json" \
     -d '{"provider":"<id>","modelId":"<模型ID>","enabled":false}'   # 禁坏模型（enabled:true 恢复）
curl -s -X POST $BASE/api/toggle-provider -H "Content-Type: application/json" \
     -d '{"provider":"<id>","enabled":false}'                   # 整渠道下线（enabled:true 恢复）
```

注意：

- 切主模型**不校验模型 ID 是否存在**，写错会成功但路由不到——先 `GET /api/models?provider=<id>` 复制准确 ID。
- 配/换 key 走 `${CLAUDE_SKILL_DIR}/references/data/provider-registration.md` 模板（双通道 + 明文风险声明）。

## key 录入的明文风险声明（代配前必做）

渠道 API key 以**明文**存于 `data/router-config.json`。agent 代配前必须向用户声明这一点，由用户选择代配（REST）或自行到 `/admin` 面板录入（多 key 管理 CLI 无对应命令，走面板或 REST `/api/provider-keys/*`）。

## 通知与掉线询问

`event-check` 只在两个触发点执行：用户问及通知/掉线；排障与升级开局顺带。**不做定期巡检**——Skill 形态的 OpenClaw cron 每天 10/15/20 点已定时推事件，叠加巡检 = 重复告警。`event-check` 直读 `data/events.json` 并自动把输出事件标为已读，输出即汇报（事件类型解读见 `${CLAUDE_SKILL_DIR}/references/data/events.md`）。掉线询问的答案通常就在 `modelFailover`/`modelUnavailable`/`modelRescue` 事件里。

## 重操作（无 CLI/打包命令对应）

自定义 provider、分组与路由映射、MoA 配置、超时档位、多 key 管理：CLI 无对应命令，可裸调 REST（`/api/custom-providers*`、`/api/groups*`、`/api/router-mapping`、`/api/moa-config`、`/api/timeout-profile`、`/api/provider-keys/*`；本机回环免密）或用 `/admin` 面板。**没有必须 GUI 的操作**——面板只是 REST 的静态前端。

## ③类陷阱（警示，按当前事实单轨书写）

机器上存在 **Skill 形态 CLI**（迁移期用户常态）时：Router 停止状态下执行其带自动拉起的命令，会经 `ensureRouter()` 无条件拉起**该 CLI 所在包自带的旧版 core**——直写共享数据、覆写 `router.pid`、占住 5678 旁路服务管理面。因此 **Router 停止时"跑个 CLI 命令看看"是禁止动作**：先走 SKILL.md 探针（P2 判活、P4 验版本），要启动走平台拉起面。纯 standalone 安装（包内无 CLI）不受此陷阱影响，REST 直调天然安全（Router 不在时请求直接拒连）。

## 完成判据

每个写操作完成后以只读接口回读：`GET /api/status`、`GET /api/providers` 的前后差反映操作结果。**不回读即视为未完成**；命令/请求的退出码与"成功"回包不构成判据。
