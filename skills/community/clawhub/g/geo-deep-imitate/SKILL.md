---
name: geo-deep-imitate
description: GEO 深度仿写 — web_fetch 爬信源、深度成稿、导出 ZIP 并上报仿写已完成。由 geo-cycle-autopilot 或 coordinator 调用。
requires:
  tools:
    - web_fetch
---

# GEO 深度仿写（仿写龙虾）

由 **geo-cycle-autopilot**（`needsFangxieRun`）或 **geo-opt-coordinator**（`needsDeepImitate`）调用。`taskId` 从任务列表内部取得，**勿向用户索要 OPT-ID**。

## 前置（本 skill 可独立运行，不依赖 geo-opt-coordinator）

### 读取密钥

1. 依次读取 `~/.qclaw/geo-api-key`、`~/.openclaw/geo-api-key`；存在且非空则使用
2. **若不存在或为空**：向用户索要 GEO API Key，提示在 SaaS **账户设置 → 龙虾密钥** 创建，并保存：
   ```bash
   echo -n "<用户提供的key>" > ~/.qclaw/geo-api-key
   ```

```bash
GEO_KEY=$(cat ~/.qclaw/geo-api-key 2>/dev/null || cat ~/.openclaw/geo-api-key 2>/dev/null)
BASE="https://ai.gaobobo.cn"
```

### 验证密钥（信源/成稿/导出前必做）

```bash
curl -s -X POST "$BASE/api/geo/verify-key" \
  -H "Authorization: Bearer $GEO_KEY"
```

- 返回 `code: 0` → 继续下文
- HTTP 401/403 或 `code != 0` → **立即停止**，告知用户密钥无效或已吊销，请到 SaaS 重新创建并更新本机 key 文件

### 其他前置

- QClaw 内置 **`web_fetch`** 可用（无需 Firecrawl 或 `FIRECRAWL_API_KEY`）

## 1. 信源列表

```bash
OPT_ID="<由协调器匹配到的 task.taskId>"
CYCLE=<latestCycle.cycleNumber>
curl -s "https://ai.gaobobo.cn/api/geo/diagnosis/imitate-sources?optimization_task_id=$OPT_ID&cycle_number=$CYCLE" \
  -H "Authorization: Bearer $GEO_KEY"
```

取 Top1–3 条带 `url` 的条目。

## 2. 爬全文

对每条信源 URL **只用** `web_fetch(url)` 获取页面内容：

- 将结果整理为 markdown（去掉导航、页脚、广告，保留正文；单篇目标长度建议 ≤50000 字符）
- 正文过短（仅标题、登录墙、验证码页）→ 换下一条 URL；仍不行则用该条 `summary` 并注明「已降级为摘要」
- **不要**要求用户配置 Firecrawl；**不要**调用 `firecrawl_scrape`

## 3. 提交成稿

```bash
curl -s -X POST "https://ai.gaobobo.cn/api/geo/article/generate-deep-imitate" \
  -H "Authorization: Bearer $GEO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "optimization_task_id": "OPT-XXX",
    "cycle_number": 1,
    "brand_name": "<task.brandName>",
    "keyword": "<核心词>",
    "reference_url": "https://...",
    "reference_markdown": "...",
    "reference_outline": {"sections": ["..."]}
  }'
```

## 4. 轮询

```bash
# 间隔 ≥30 秒
curl -s "https://ai.gaobobo.cn/api/geo/article/$TASK_ID" \
  -H "Authorization: Bearer $GEO_KEY"
```

`status=completed` 且正文非空即成功；`deepImitate` 由服务端回写。

## 5. 导出并上报（autopilot / 成稿后）

```bash
BASE="https://ai.gaobobo.cn"
DIR="$HOME/.qclaw/geo-exports/<brand>_<product>_C<cycle>/fangxie"
mkdir -p "$DIR"
curl -fsSL -o "$DIR/fangxie.zip" \
  "$BASE/api/geo/optimization/$OPT_ID/cycles/$CYCLE/export/fangxie.zip" \
  -H "Authorization: Bearer $GEO_KEY"
curl -s -X POST "$BASE/api/geo/optimization/$OPT_ID/cycles/$CYCLE/mass-publish-export" \
  -H "Authorization: Bearer $GEO_KEY" -H "Content-Type: application/json" \
  -d "{\"branch\":\"fangxie\",\"local_path_hint\":\"$DIR\"}"
```

## 约束

- 与 Celery 浅仿写（`imitate_enabled`）互斥
- 不自动创建三方媒体发稿任务
