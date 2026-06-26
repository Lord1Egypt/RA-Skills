---
name: geo-mass-publish-check
description: GEO 待群发 — 拉取范文/仿写状态，待导出时下载 ZIP 到本机并上报，可群发时提示用户。QClaw 定时只装本 skill 即可。
---

# GEO 待群发（拉状态 · 下 ZIP）

**只做三件事**（不触发周期、不成稿、不发帖）：

1. **拉取状态** — `GET /api/geo/optimization/tasks`（必要时 `mass-publish/pending`）
2. **符合条件则下载 ZIP** — `needsFanwenExport` / `needsFangxieExport` 为 true 时下载并 `POST mass-publish-export`
3. **回报用户** — 品牌/周期、范文·仿写 ZIP 导出状态、本机路径；可群发时提示用融媒宝导入

SaaS 任务须已配置国内 **范文** 和/或 **普通仿写**（协同 API 默认开启）。勿调用深度仿写、`web_fetch`、`generate-deep-imitate`。

## 密钥

1. 读 `~/.qclaw/geo-api-key` 或 `~/.openclaw/geo-api-key`；无则让用户在 QClaw 发送：`这是geo的api key：<SaaS 龙虾密钥>`
2. 业务请求前：`POST /api/geo/verify-key`，`code != 0` 则停止

```bash
GEO_KEY=$(cat ~/.qclaw/geo-api-key 2>/dev/null || cat ~/.openclaw/geo-api-key 2>/dev/null)
BASE="https://ai.gaobobo.cn"
```

## 本机路径

```text
~/.qclaw/geo-exports/{brand}_{product}_C{cycle}/fanwen/fanwen.zip
~/.qclaw/geo-exports/{brand}_{product}_C{cycle}/fangxie/fangxie.zip
```

## 1. 拉取状态并下载（主流程）

```bash
curl -s "$BASE/api/geo/optimization/tasks" -H "Authorization: Bearer $GEO_KEY"
```

对每个 `items[]` 看 `openclawActions`（**勿向用户索要 OPT-ID**）：

| 字段 | 动作 |
|------|------|
| `needsFanwenExport == true` | 下载 `.../export/fanwen.zip` → 本机 `fanwen/`，`POST mass-publish-export` `branch: fanwen` |
| `needsFangxieExport == true` | 下载 `fangxie.zip` → 本机 `fangxie/`，`branch: fangxie` |
| `fanwenStatus == completed` 且本地已有 zip | 跳过范文 |
| `fangxieStatus == not_enabled` | 跳过仿写 |

导出示例（范文；仿写改路径与 `branch`）：

```bash
OPT_ID="<task.taskId>"
CYCLE=<latestCycle.cycleNumber>
DIR="$HOME/.qclaw/geo-exports/${BRAND}_${PRODUCT}_C${CYCLE}/fanwen"
mkdir -p "$DIR"
curl -fsSL -o "$DIR/fanwen.zip" \
  "$BASE/api/geo/optimization/$OPT_ID/cycles/$CYCLE/export/fanwen.zip" \
  -H "Authorization: Bearer $GEO_KEY"
curl -s -X POST "$BASE/api/geo/optimization/$OPT_ID/cycles/$CYCLE/mass-publish-export" \
  -H "Authorization: Bearer $GEO_KEY" -H "Content-Type: application/json" \
  -d "{\"branch\":\"fanwen\",\"local_path_hint\":\"$DIR\"}"
```

## 2. 待群发列表（可选，用于提醒）

```bash
curl -s "$BASE/api/geo/optimization/mass-publish/pending" \
  -H "Authorization: Bearer $GEO_KEY"
```

`items[]` 含 `brandName`、`productName`、`cycleNumber`、`massPublishScopeLabel`、`fanwenStatusLabel`、`fangxieStatusLabel`、`fanwenLocalPath`、`fangxieLocalPath`。

**可群发**：任一侧 ZIP 导出状态为 `ready_to_export`（待导出）或 `completed`（已完成）。

## 3. 回报用户

```text
【GEO 待群发】{brandName} · {productName} · 第 {cycleNumber} 周期
范文 ZIP：{fanwenStatusLabel} · {fanwenLocalPath 或「—」}
仿写 ZIP：{fangxieStatusLabel} · {fangxieLocalPath 或「—」}
{若可群发}请用融媒宝批量导入上述目录中的 ZIP。
```

无 `items`：说明当前无待群发，或仍在生成中。

## 约束

- 勿要求用户输入 OPT-ID
- 不执行发帖、不回写发布结果
- 不触发 Celery 优化周期
