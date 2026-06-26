---
name: geo-opt-coordinator
description: GEO 智能优化龙虾 — 对话入口、密钥验证、任务列表。主自动化请用 geo-cycle-autopilot 定时；群发状态用 geo-mass-publish-check。勿要求 OPT-ID。
---

# GEO 智能优化龙虾（Coordinator）

**主路径（推荐）**：在 QClaw 配置每日定时，加载 **geo-cycle-autopilot** + **geo-mass-publish-check**，无需用户说「开始优化任务」。

本 skill 用于：首次配置 **龙虾密钥**、查看任务列表、口语触发单次仿写（兼容）。

**自媒体群发**：本机 **融媒宝** + 已导出 Word/ZIP。勿用 `geo-social-publish`（已废弃）。

## API 与密钥

- **生产基址**：`https://ai.gaobobo.cn`
- **GEO_KEY**：`~/.qclaw/geo-api-key` 或 `~/.openclaw/geo-api-key`
- 创建密钥：SaaS **账户设置 → 龙虾密钥**

```bash
GEO_KEY=$(cat ~/.qclaw/geo-api-key 2>/dev/null || cat ~/.openclaw/geo-api-key 2>/dev/null)
curl -s "https://ai.gaobobo.cn/api/geo/optimization/tasks" -H "Authorization: Bearer $GEO_KEY"
```

`openclawActions` 字段：

- `needsFanwenExport` / `needsFangxieRun` / `needsFangxieExport`
- `fanwenStatusLabel` / `fangxieStatusLabel` / `canMassPublish`
- `needsDeepImitate`（兼容旧逻辑）

`latestCycle.cycleStepResults.massPublish`：范文/仿写双状态。

---

## 子 skill

| 能力 | Skill |
|------|--------|
| **每日自动（主路径）** | **geo-cycle-autopilot** |
| **待群发检查与话术** | **geo-mass-publish-check** |
| 深度仿写步骤 | **geo-deep-imitate**（autopilot 内联） |
| 品牌诊断 | **geo-brand-optimization** |

---

## 路径零：龙虾密钥

读取或索要密钥 → `POST /api/geo/verify-key` → 保存到 `~/.qclaw/geo-api-key`。

---

## 路径一（兼容）：开始优化任务

等同对 `needsDeepImitate` 项执行 **geo-deep-imitate**；新部署优先用 **geo-cycle-autopilot** 定时。

---

## 路径二：列表 / 按品牌产品仿写

展示品牌、产品、`fanwenStatusLabel`、`fangxieStatusLabel`；匹配后调用 **geo-deep-imitate**。

---

## 回写与 SaaS

- `cycleStepResults.deepImitate`、`massPublish`
- 群发结果不回写 SaaS
