---
name: feishu-card-sender
description: 通过飞书 OpenAPI 发送卡片消息（interactive card），支持模板化 JSON 卡片与变量替换。用于用户要求“发送飞书卡片/模板消息/互动卡片”时，或需要把结构化通知发到指定 open_id/chat_id 时。该技能只走 OpenAPI（appid/appsecret + tenant_access_token），不使用 message 通道。
---

# Feishu Card Sender

## 概览

用统一方式通过飞书 OpenAPI 发送卡片消息，避免每次手写 curl。
本技能固定使用 `scripts/send_feishu_card.py`（appid/appsecret 鉴权），不走 `message` 通道。

## 快速决策

1. **发送到当前会话用户** → 使用当前会话 `sender_id` 作为 `--receive-id`（open_id）
2. **发送到指定用户/群** → 显式传 `--receive-id` + `--receive-id-type`
3. **需要复用模板** → 把模板放到 `assets/templates/*.json`，再用 `--template` + 变量替换

## 发送方式：脚本发送（OpenAPI，唯一方式）

脚本：`scripts/send_feishu_card.py`

### 凭证

按以下优先级自动获取（从高到低）：
1. 命令参数：`--app-id` / `--app-secret`
2. 环境变量：`FEISHU_APP_ID` / `FEISHU_APP_SECRET`
3. OpenClaw 配置：`/root/.openclaw/openclaw.json` 的 `channels.feishu.accounts`
   - 可用 `--account-id` 指定账户（不传则取第一个）
   - 可用 `--account-id current` 自动读取会话上下文 account_id（从运行时环境变量 best-effort 获取）

### 常用命令

```bash
# 1) 列出内置模板
python3 scripts/send_feishu_card.py --list-templates

# 2) 用 movie 模板发送到 open_id（变量文件）
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
python3 scripts/send_feishu_card.py \
  --template movie \
  --receive-id ou_xxx \
  --receive-id-type open_id \
  --vars-file references/vars.example.env

# 3) 直接指定模板文件 + 行内变量
python3 scripts/send_feishu_card.py \
  --template-file assets/templates/movie.json \
  --receive-id ou_xxx \
  --var title='星际穿越' \
  --var rating='8.7'

# 4) 只有海报 URL 时，自动上传飞书并注入 poster_img_key
python3 scripts/send_feishu_card.py \
  --template movie-custom \
  --receive-id ou_xxx \
  --receive-id-type open_id \
  --poster-url 'https://image.tmdb.org/t/p/original/xxx.jpg' \
  --var title='星际穿越' \
  --var overview='...'
```

## 变量替换规则

- 模板中占位符写法：`${key}`
- 变量来源（后者覆盖前者）：
  1) `--vars-file`（`KEY=VALUE`）
  2) 多次 `--var key=value`
- 未提供的变量保持原样，不报错（便于渐进调试）

## 参数规范（必读）

发送前先读：
- `references/template-params.md`（movie-custom）
- `references/template-params-tv.md`（tv-custom）

- 文档定义了每个模板的必填参数、字段含义、示例命令。
- `cast`（演员）字段必须按 Markdown 多行列表字符串传递。

## 文件结构

- `scripts/send_feishu_card.py`：获取 token、渲染模板、发送消息
- `scripts/format_cast.py`：把演员 JSON 自动转为 `cast` 字段字符串
- `scripts/card_callback_router.py`：卡片回调统一路由入口
- `scripts/subscribe_callback_handler.py`：处理“立即订阅”回调并写入 MoviePilot（含幂等）
- `assets/templates/movie-custom.json`：电影详情模板（movie）
- `assets/templates/tv-custom.json`：剧集详情模板（tv）
- `assets/rules/*.rules.json`：通用规则（支持 require_non_empty / default_value / 条件删减区块）
- `references/vars.example.env`：变量文件示例
- `references/template-params.md`：模板参数与传参格式规范

## Card-Action 自动处理规则（方案 B）

当收到 Feishu 卡片回调消息时（`message_id` 形如 `card-action-c-...`，内容含 `{"action":"subscribe"...}`）：

1. 自动提取 `callback_token`（从 `message_id` 去掉 `card-action-` 前缀）
2. 自动执行：
   - 先延时更新卡片为“处理中...”并禁用
   - 执行 MoviePilot 订阅（幂等）
   - 再延时更新卡片为“✅ 已订阅”或“❌ 订阅失败，请重试”
3. 无需用户手动提供 token/account 参数

## 发送后回复约束

- 卡片发送成功后，默认不要再发“已发送 + message_id”的额外文本。
- 仅在用户明确要求回执时，才返回 `message_id`。

## 安全与约束

- 不在脚本里硬编码 App Secret
- 日志默认不打印密钥
- 失败时返回飞书原始错误码与错误信息，便于排障
