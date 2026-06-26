---
name: geo-cycle-autopilot
description: GEO 周期自动协同 — 读龙虾密钥，自动导出范文/执行深度仿写并导出，上报待群发状态。供 QClaw 每日定时任务加载，无需用户说「开始优化任务」。
requires:
  tools:
    - web_fetch
---

# GEO 周期自动协同（Autopilot）

**主路径**：由用户在 QClaw 配置**每日定时**（本项目不实现 cron），定时仅加载本 skill。

## 前置（本 skill 可独立运行，不依赖 geo-opt-coordinator）

### 读取密钥

1. 依次读取 `~/.qclaw/geo-api-key`、`~/.openclaw/geo-api-key`；存在且非空则使用
2. **若不存在或为空**：向用户索要 GEO API Key，提示在 SaaS **账户设置 → 龙虾密钥** 创建，并保存：
   ```bash
   echo -n "<用户提供的key>" > ~/.qclaw/geo-api-key
   ```
3. 用户说「更换 key / 重置 key」时：删除上述文件后重新索要

```bash
GEO_KEY=$(cat ~/.qclaw/geo-api-key 2>/dev/null || cat ~/.openclaw/geo-api-key 2>/dev/null)
BASE="https://ai.gaobobo.cn"
```

### 验证密钥（业务请求前必做）

```bash
curl -s -X POST "$BASE/api/geo/verify-key" \
  -H "Authorization: Bearer $GEO_KEY"
```

- 返回 `code: 0` 且 message 含「验证通过」→ 继续下文
- HTTP 401/403 或 `code != 0` → **立即停止**，告知用户密钥无效或已吊销，请到 SaaS 重新创建并更新本机 key 文件
- **不要**在未验证通过时调用 optimization / export 等接口

### 其他前置

- QClaw **`web_fetch`** 可用
- SaaS 智能优化任务已开启 **OpenClaw 协同** 与（若需仿写）**深度仿写**

## 本机目录约定

```text
~/.qclaw/geo-exports/{brand}_{product}_C{cycle}/fanwen/fanwen.zip
~/.qclaw/geo-exports/{brand}_{product}_C{cycle}/fangxie/fangxie.zip
```

Windows：`%USERPROFILE%\.qclaw\geo-exports\...`

## 1. 拉取任务

```bash
curl -s "$BASE/api/geo/optimization/tasks" -H "Authorization: Bearer $GEO_KEY"
```

对每个 `items[]` 读取 `task`、`latestCycle`、`openclawActions`（**勿向用户索要 OPT-ID**）。

## 2. 范文：导出并上报

当 `openclawActions.needsFanwenExport == true`：

```bash
OPT_ID="<task.taskId 内部用>"
CYCLE=<latestCycle.cycleNumber>
BRAND="<task.brandName>"
PRODUCT="<task.productName>"
DIR="$HOME/.qclaw/geo-exports/${BRAND}_${PRODUCT}_C${CYCLE}/fanwen"
mkdir -p "$DIR"
curl -fsSL -o "$DIR/fanwen.zip" \
  "$BASE/api/geo/optimization/$OPT_ID/cycles/$CYCLE/export/fanwen.zip" \
  -H "Authorization: Bearer $GEO_KEY"
curl -s -X POST "$BASE/api/geo/optimization/$OPT_ID/cycles/$CYCLE/mass-publish-export" \
  -H "Authorization: Bearer $GEO_KEY" -H "Content-Type: application/json" \
  -d "{\"branch\":\"fanwen\",\"local_path_hint\":\"$DIR\"}"
```

若 `openclawActions.fanwenStatus` 已为 `completed` 且本地已有 `fanwen.zip`，跳过。

## 3. 仿写：抓信源 → 成稿 → 导出 → 上报

当 `openclawActions.needsFangxieRun == true`：

1. `GET .../diagnosis/imitate-sources?optimization_task_id=$OPT_ID&cycle_number=$CYCLE`
2. 对 Top1–3 URL 仅用 **`web_fetch(url)`** 取正文（勿用 Firecrawl）
3. `POST .../article/generate-deep-imitate`（见 geo-deep-imitate）
4. 轮询 `GET .../article/{CG-id}`，间隔 ≥30s，直至 `status=completed`

当 `openclawActions.needsFangxieExport == true`（或上一步刚完成）：

```bash
DIR_FX="$HOME/.qclaw/geo-exports/${BRAND}_${PRODUCT}_C${CYCLE}/fangxie"
mkdir -p "$DIR_FX"
curl -fsSL -o "$DIR_FX/fangxie.zip" \
  "$BASE/api/geo/optimization/$OPT_ID/cycles/$CYCLE/export/fangxie.zip" \
  -H "Authorization: Bearer $GEO_KEY"
curl -s -X POST "$BASE/api/geo/optimization/$OPT_ID/cycles/$CYCLE/mass-publish-export" \
  -H "Authorization: Bearer $GEO_KEY" -H "Content-Type: application/json" \
  -d "{\"branch\":\"fangxie\",\"local_path_hint\":\"$DIR_FX\"}"
```

`openclawActions.fangxieStatus == not_enabled` 时跳过仿写分支。

## 4. 结束

不向用户展示 OPT-ID。可输出内部摘要：品牌、产品、范文状态、仿写状态（读 `latestCycle.cycleStepResults.massPublish` 或 `openclawActions.fanwenStatusLabel` / `fangxieStatusLabel`）。

群发提醒由 **geo-mass-publish-check** 定时或紧随其后执行。

## 约束

- 不触发 Celery 优化周期；不替代服务端范文生成
- 群发用本机 **融媒宝** + 已导出 Word/ZIP，勿加载 geo-social-publish
