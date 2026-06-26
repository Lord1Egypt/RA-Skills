# ClawTune API Playbook for Skill v1

这份文件不是给用户看的，而是给调用本 skill 的模型看的。目标是把对话阶段、主锚点对象、建议 API 和恢复逻辑写清楚，避免自由发挥。

## 1. 固定线上地址
- `https://clawtune.aqifun.com`

默认 API 基址：
- `https://clawtune.aqifun.com/api/v1`

## 2. 认证与凭证
### 本地固定路径
- `~/.openclaw/clawtune/auth.json`
- `~/.openclaw/clawtune/session.json`

### 凭证优先级
1. 读取 `auth.json`
2. 若不存在 -> `POST /bootstrap`
3. 若 `access_token` 过期但 `refresh_token` 可用 -> `POST /token/refresh`
4. 若 refresh 失效 -> 重新 bootstrap

### 要带 token 的接口
默认把以下都当成鉴权接口：
- `GET /content/facets`
- `POST /playlists/generate`
- `GET /playlists/{playlist_id}`
- `POST /creation-drafts`
- `PATCH /creation-drafts/{draft_id}`
- `POST /creation-drafts/{draft_id}/recommendations`
- `POST /orders`
- `GET /orders/{order_id}`
- `GET /orders/{order_id}/status`
- `GET /orders/{order_id}/delivery`

## 3. 对话阶段与主锚点
### 阶段 A：playlist
主锚点：`playlist_id`

推荐流程：
1. 理解用户场景
2. 做一次轻选择
3. 内部生成更饱满的标题 / 简介 / prompt
4. 调 `POST /playlists/generate`
5. 把 `playlist_id` 写入 `session.json`

### 阶段 B：draft
主锚点：`draft_id`

推荐流程：
1. 用户表达创作意图
2. `POST /creation-drafts`
3. 逐步 `PATCH /creation-drafts/{draft_id}`
4. 必要时 `POST /creation-drafts/{draft_id}/recommendations`

### 阶段 C：order
主锚点：`order_id`

推荐流程：
1. 总结创作方案
2. 用户确认方向并准备下单后，`POST /orders`
3. 一旦拿到 `order_id`，主锚点立刻切换为 `order_id`
4. 对用户返回线上正式订单入口链接，由网页继续承接后续步骤

### 阶段 D：status / delivery
主锚点仍然是 `order_id`

推荐流程：
1. `POST /orders` 成功后，把线上正式继续入口链接返回给用户
2. 后续步骤在网页内完成，不由对话 agent 继续下探
3. 进度查询统一走：
   - `GET /orders/{order_id}/status`
   - `GET /orders/{order_id}/delivery`
4. 若 delivery 返回 `playlist_id`，把主锚点切到结果歌单

### 阶段 E：playlist result
主锚点：`playlist_id`

推荐流程：
1. 以 `result_entry_url` 或 `playlist_id` 作为完成后的主入口
2. 对用户优先返回生成完成后的歌单页

## 4. 恢复链路
### 用户说“我刚在网页那边完成了，结果在哪？”
恢复优先级：
1. `current_order_id`
2. `GET /orders/{order_id}/delivery` 返回的 `playlist_id`
3. 如果只剩旧歌单 `playlist_id`，不要假装它就是完成后的结果歌单

## 5. 幂等建议
所有可能重试的写操作都要带稳定的 `idempotency_key`：
- 生成歌单
- 创建订单

同一业务意图重试时复用同一个 key，不同意图不得复用。

## 6. 已知后端风险
当前 skill 不应假设以下事情已经绝对可靠：
1. `orders` 已完整持久化 `skill_session_id` / `source_context_playlist_id`
2. `order` 创建的幂等逻辑已像 playlists 一样完整
3. 完成后的结果歌单一定会在用户回来的第一时间立刻可见

因此，v1 skill 应优先保证：
- 先把 `order_id` 本地保存好
- 后续恢复时只围绕 `order_id` 查询
- 对用户只提供线上正式继续入口，不在对话里下探网页内部流程
- 不对“长链路自动找回原始歌单上下文”做过度承诺
