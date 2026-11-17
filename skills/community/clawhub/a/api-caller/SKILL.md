---
name: api-caller
description: |
  REST API 调用助手。覆盖鉴权（Bearer/API Key/基本认证）、指数退避重试、超时与限流处理、JSON 解析与错误分类、分页与速率控制。当用户需要"调用接口""拉取 API 数据""对接某开放平台""写个请求脚本"时调用。
agent_created: true
visibility: "public"
---

# REST API 调用助手

帮用户稳健地调用任意 HTTP API：从简单 GET 到带鉴权、重试、分页的复杂拉取。核心原则：**网络不可靠，调用必须可重试、可观测、可分类错误**。

## 适用场景
- 拉取开放平台数据（行情、天气、搜索、AI 推理）
- 对接需要鉴权的内部/外部服务
- 批量分页抓取、限速下的稳定采集
- 把 API 响应转成结构化数据（接 `structured-extraction`）

## 调用黄金法则
1. **鉴权统一走 Header**：`Authorization: Bearer <token>` 或 `X-API-Key: <key>`，token 从环境变量注入，不落盘。
2. **重试 + 退避**：5xx / 429（限流）自动重试，指数退避（1s→2s→4s），带 `jitter` 抖动避免惊群。
3. **尊重限流**：读 `Retry-After` 头；无头时按 429 退避；长批量用令牌桶限速。
4. **超时**：connect/read 都设上限（默认 30s），避免挂死。
5. **错误分类**：
   - 4xx → 客户端错（参数/鉴权），不重试，直接报
   - 5xx / 429 / 网络超时 → 服务端/限流，可重试
   - 解析失败 → 响应非预期格式，记录原始体便于排查
6. **结构化落地**：成功响应用 `structured-extraction` 的 `json_repair.py` 修复再解析。

## 标准工作流
使用 `scripts/api_call.py`：
```bash
python scripts/api_call.py \
  --method GET \
  --url "https://api.example.com/v1/data" \
  --header "Authorization: Bearer $API_TOKEN" \
  --retry 3 --timeout 30 \
  --out result.json
```
- `--header` 可重复；`--body` 传 JSON 字符串（POST/PUT）。
- 支持 `--paged` 自动翻页直到 `next` 为空或达到 `--max-pages`。
- 退出码：0 成功，2 客户端错（4xx），3 重试耗尽，4 解析失败。

## 常见平台鉴权速查
- **OpenAI / 兼容**：`Authorization: Bearer $OPENAI_API_KEY`
- **ClawHub**：`Authorization: Bearer <token>`
- **GitHub**：`Authorization: Bearer <token>` 且 `Accept: application/vnd.github+json`
- **微信/企微**：access_token 先用 `GET /cgi-bin/token` 换，再附带

## 质量门禁
- [ ] token 来自环境变量（不写进脚本/日志）
- [ ] 重试仅针对 5xx/429/网络错，4xx 不重试
- [ ] 批量调用有限速，避免被封
- [ ] 大响应落地到文件而非全量打印

## 自进化学习系统
```bash
python scripts/learner.py record . --capability "API调用" [--fail --error <类型> --note <说明>]
python scripts/learner.py insight .
python scripts/learner.py reflect .
```
- 某接口反复 401 → 记录 `error=auth`，reflect 提示"检查 token 有效期/作用域"
- 反复 429 → 记录 `error=ratelimit`，reflect 建议下调并发/加 `Retry-After` 尊重

## 安全边界
- 不把响应中的密钥/PII 写进公开日志
- 不绕过对方服务的鉴权或速率限制用于滥用
