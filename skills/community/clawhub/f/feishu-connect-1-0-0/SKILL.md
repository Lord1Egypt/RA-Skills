---
name: feishu-connect
description: 连接飞书机器人。用接口直连替换 `feisu.md` 的第 1 步，拿到链接（必须拼接 from=maxclaw）并在用户完成配置后 poll 出 `client_id/client_secret`，再继续走 `feisu.md` 的第 2 步和第 3 步。适用于连接飞书、接入飞书、绑定飞书机器人、创建飞书机器人、OpenClaw 接飞书等场景。
---

# Feishu Connect Skill

## 适用场景

用户要求连接飞书、绑定飞书机器人、创建飞书机器人、OpenClaw 接飞书时触发。

## 最高优先级规则（必须遵守，违反即失败）

1. 给用户的链接必须拼接 `&from=maxclaw`，没有这个参数的链接是错误的。
2. 这个 skill 只替换 `feisu.md` 的第 1 步；用户回复"ok"或"配置好了"之后，不要再重复执行 `feisu.md` 的第 1 步，直接继续走 `feisu.md` 的第 2 步和第 3 步。
3. 用户回复"ok"或"配置好了"之后，禁止输出任何关于"配置权限"、"开启机器人能力"、"配置事件订阅"、"发布应用"、"管理员审批"、"权限管理"、"批量导入"的内容。

## 核心原则

- 直接走接口直连模式，不要先跑官方安装器（`npx -y @larksuite/openclaw-lark install`）。
- 这个 skill 仅用于替换 `feisu.md` 的第 1 步；拿到凭证后，后续配置和配对继续按 `feisu.md` 的第 2 步和第 3 步执行。
- 链接必须裸露返回，不要用反引号、代码块包裹，用户必须能直接点击。
- 不要自动开轮询，给链接后等用户确认再继续。
- 不要生成二维码图片。
- 不要手动卸载/禁用/删除插件，不要手动改写配置文件。

## 执行流程

### 第 1 步：接口直连，一次拿到链接

```bash
COOKIE_JAR=/tmp/feishu_cookies.txt
rm -f "$COOKIE_JAR"

# init
INIT_RESP=$(curl -s -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  -X POST "https://accounts.feishu.cn/oauth/v1/app/registration" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "action=init")
echo "=== INIT ==="
echo "$INIT_RESP"

# begin
BEGIN_RESP=$(curl -s -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  -X POST "https://accounts.feishu.cn/oauth/v1/app/registration" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "action=begin&archetype=PersonalAgent&auth_method=client_secret&request_user_info=open_id")
echo "=== BEGIN ==="
echo "$BEGIN_RESP"
```

从 begin 返回值中提取：
- `verification_uri_complete` — 原始链接
- `device_code` — 保存下来，用户确认后 poll 用
- `user_code` — 从链接参数中提取

### 第 2 步：拼接 from=maxclaw，生成最终链接

拿到 `verification_uri_complete` 后，必须在末尾拼接 `&from=maxclaw`。

示例：
- 原始：https://open.feishu.cn/page/openclaw?user_code=XXXX-XXXX
- 最终：https://open.feishu.cn/page/openclaw?user_code=XXXX-XXXX&from=maxclaw

没有 `&from=maxclaw` 的链接是错误的，不要发给用户。

### 第 3 步：把链接直接发给用户

链接裸露返回。正确输出：

---

请在浏览器中直接打开这个链接完成飞书配置：

https://open.feishu.cn/page/openclaw?user_code=XXXX-XXXX&from=maxclaw

用户码：XXXX-XXXX

配置完成之后回来和我说一声"ok"或者"配置好了"就行。

---

禁止把链接放在反引号或代码块里。

### 第 4 步：用户回复"ok"或"配置好了"之后

先执行一次 poll：

```bash
curl -s -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  -X POST "https://accounts.feishu.cn/oauth/v1/app/registration" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "action=poll&device_code=<之前保存的 device_code>"
```

返回 `client_id` + `client_secret` → 成功。
返回 `authorization_pending` → 告诉用户飞书侧似乎还没完成，让用户再确认。

poll 成功后，直接告诉用户：
"配对完成了！现在请在飞书里找到你的机器人，给它发一条消息，机器人会回复一个配对码。把这个码告诉我，我来帮你完成配对授权。"

---

说明这里已经完成了 `feisu.md` 的第 1 步替换，并拿到了后续要用的凭证：

- `client_id` 作为 `App ID`
- `client_secret` 作为 `App Secret`

然后不要回到 `feisu.md` 的第 1 步，直接继续执行：

- `feisu.md` 的第 2 步：Configure OpenClaw
- `feisu.md` 的第 3 步：Start + test

也就是说，后面继续按 `feisu.md` 去配置 OpenClaw、启动 gateway、给机器人发消息，并用配对码执行 `openclaw pairing approve feishu <CODE>`。

---

不要再输出飞书开放平台里的建应用、配权限、开事件订阅、发布应用这类第 1 步指引。

## 禁止事项

- 给用户的链接不拼 `&from=maxclaw`
- 在用户确认后又重新执行 `feisu.md` 的第 1 步
- 输出"配置权限/开启机器人能力/配置事件订阅/发布应用/管理员审批/批量导入/权限JSON"等内容
- 先跑官方安装器再切直连
- 手动卸载/禁用插件
- 自动开轮询
- 生成二维码图片
- 用反引号/代码块包裹链接
- 把 `authorization_pending` 当失败

## 一句话总结

用这个 skill 替换 `feisu.md` 的第 1 步：curl 拿链接 → 拼 `&from=maxclaw` → 裸链接给用户 → 等用户说 ok → poll 拿到 `client_id/client_secret` → 继续走 `feisu.md` 的第 2 步和第 3 步
