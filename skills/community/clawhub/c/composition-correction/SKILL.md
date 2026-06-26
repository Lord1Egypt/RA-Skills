---
name: composition-correction
description: 墨灵高考作文批改。调用 InkCraft API 提交批改并返回结构化结果。
user-invocable: true
metadata: {"openclaw":{"skillKey":"composition-correction","emoji":"📝","homepage":"https://www.inkcraft.cn","primaryEnv":"INKCRAFT_API_KEY","requires":{"bins":["curl"],"env":["INKCRAFT_API_KEY"]},"version":"1.0.0","tags":["latest"]}}
---

# 墨灵高考作文批改

- Slug: `composition-correction`
- Display name: `墨灵高考作文批改`
- Version: `1.0.0`
- Tags: `latest`

当用户请求“批改作文/高考作文打分/作文优化建议”时，使用本 Skill。

## Required Inputs

在调用 API 前，确保以下字段存在：

- `originalText`：作文题目或材料
- `essayText`：学生作文正文

可选字段：

- `title`
- `model`（默认 `doubao`）
- `essayType`（默认 `gaokao-chinese`）
- `tone`（默认 `strict`）
- `referenceText`
- `firstSentence`
- `secondSentence`

如果缺少 `originalText` 或 `essayText`，先向用户追问，不要发起请求。

## API Endpoints

默认使用：

- Base URL: `https://www.inkcraft.cn`
- Submit: `POST /api/skills/essay-correction`
- Result: `GET /api/skills/correction-result?uuid=<uuid>`

优先读取环境变量（若存在）：

- `INKCRAFT_BASE_URL`（可选）
- `INKCRAFT_API_KEY`（必需）

## Tool Execution Policy

优先使用可执行命令工具（如 `system.run`）通过 `curl` 调用 API。

### Step 1: Submit Correction Job

执行等价请求：

```bash
BASE_URL="${INKCRAFT_BASE_URL:-https://www.inkcraft.cn}"
curl -sS -X POST "$BASE_URL/api/skills/essay-correction" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $INKCRAFT_API_KEY" \
  -H "x-api-key: $INKCRAFT_API_KEY" \
  -d '<JSON_PAYLOAD>'
```

判定：

- 若返回 `success=true` 且含 `uuid`，进入查询阶段。
- 若返回 `Invalid API key`，停止并提示用户更新 API Key。

### Step 2: Poll Result

最多轮询 3 次，每次间隔 2-5 秒：

```bash
BASE_URL="${INKCRAFT_BASE_URL:-https://www.inkcraft.cn}"
curl -sS "$BASE_URL/api/skills/correction-result?uuid=<uuid>" \
  -H "Authorization: Bearer $INKCRAFT_API_KEY" \
  -H "x-api-key: $INKCRAFT_API_KEY"
```

判定：

- `done=false`：继续轮询。
- `done=true` 且 `status=success`：输出结构化结果。
- `status=error`：输出失败原因和重试建议。

## Response Format

最终回复使用以下结构：

1. 批改状态（成功/处理中/失败）
2. 总评（1-2 句）
3. 评分与关键维度（若有）
4. 亮点（2-4 条）
5. 待改进（2-4 条）
6. 可直接改写建议（1-3 条）
7. 并提供前往查看批改详情的链接（https://www.inkcraft.cn/dashboard/correction/[uuid]）

## Safety and Boundaries

- 不要伪造 API 返回内容。
- 不要泄漏 API Key。
- 若请求失败，给出可执行排查步骤：
  - 检查 key 是否来自 InkCraft 开发者页
  - 检查 baseUrl 是否为 `https://www.inkcraft.cn`
  - 重试或重新生成 key
