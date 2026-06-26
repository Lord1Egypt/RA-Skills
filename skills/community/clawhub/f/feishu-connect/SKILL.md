---
name: feishu-connect
description: 连接飞书机器人。通过接口直连发起注册会话，拿到链接（必须拼接 from=maxclaw）发给用户，等用户配置完成后告诉用户去飞书找机器人拿配对码。适用于连接飞书、接入飞书、绑定飞书机器人、创建飞书机器人、OpenClaw 接飞书等场景。
---

# Feishu Connect Skill

## 适用场景

用户要求连接飞书、绑定飞书机器人、创建飞书机器人、OpenClaw 接飞书时触发。

## 最高优先级规则（必须遵守，违反即失败）

1. 给用户的链接必须拼接 `&from=maxclaw`，没有这个参数的链接是错误的。
2. 用户回复"ok"或"配置好了"之后，禁止读取 `docs/channels/feishu.md`。
3. 用户回复"ok"或"配置好了"之后，禁止输出任何关于"配置权限"、"开启机器人能力"、"配置事件订阅"、"发布应用"、"管理员审批"、"权限管理"、"批量导入"的内容。

## 核心原则

- 直接走接口直连模式，不要先跑官方安装器。
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

---

配对完成了！现在请在飞书里找到你的机器人，给它发一条消息，机器人会回复一个配对码。把这个码告诉我，我来帮你完成配对授权。

---

到此为止。不要再做任何额外操作。不要读文档。不要输出配置指引。

## 禁止事项

- 给用户的链接不拼 `&from=maxclaw`
- 读取 `docs/channels/feishu.md`
- 输出"配置权限/开启机器人能力/配置事件订阅/发布应用/管理员审批/批量导入/权限JSON"等内容
- 先跑官方安装器再切直连
- 手动卸载/禁用插件
- 自动开轮询
- 生成二维码图片
- 用反引号/代码块包裹链接
- 把 `authorization_pending` 当失败

## 一句话总结

curl 拿链接 → 拼 `&from=maxclaw` → 裸链接给用户 → 等用户说 ok → poll 一次 → 告诉用户去飞书找机器人拿配对码。
