# Login

Script: `scripts/login.py`

The user never leaves the chat: they give an email, (sometimes) type one image captcha, then the emailed code. That signs them up or logs them in, and the script saves an API key on this machine.

## Flow

```bash
# 1. Send the email code (new emails sign up, existing ones log in; the script decides)
python3 scripts/login.py start --email user@example.com

# 2. Only when step 1 returned "next": "enter_captcha": what the user read off the image
python3 scripts/login.py captcha --code 9139

# 3. The code the user received by email
python3 scripts/login.py verify --code 123456
```

Every step prints JSON on stdout; the `next` field tells you what to do:

| Output | Meaning | Next |
|---|---|---|
| `"next": "enter_captcha"` | The server wants an image captcha first | Show the user `captcha_url` (or the local `captcha_file`), then run `captcha` with what they type |
| `"next": "enter_email_code"` | The code was emailed | Ask the user to check their inbox (and spam), then run `verify` |
| `"ok": true, "api_key_tail"` | Logged in, key saved | Re-run the original command |
| `"error": "login_failed"` | Failed; `message` says why | Wrong captcha: run `start` again. Wrong email code: have the user re-check and run `verify` again |

The user must read and type the captcha themselves; the agent must never solve it for them.

## Where the key lives

- File: `~/.config/adsturbo/credentials.json` (mode 600), saved per site so the test and production sites never mix; set `ADSTURBO_CONFIG_DIR` to use another directory
- Every script reads it when `ADSTURBO_API_KEY` is unset; the environment variable wins
- If the account already has a key named `adsturbo-skill`, it is reused rather than duplicated
- Output only carries the key's last four characters; never echo the full key in a reply

## Other commands

```bash
python3 scripts/login.py status   # is a key available here, and for which email
python3 scripts/login.py logout   # forget the saved key on this machine (the key stays valid; delete it at https://adsturbo.ai/iris/api)
```

## Notes

- Re-running `start` for the same email within 30 seconds does not send a new code; the emailed one stays valid
- Closed email sign-up, deactivated accounts and similar cases are explained in `message`
- New accounts get no free credits; top up at https://adsturbo.ai/pricing before generating if needed

---

# 在对话里登录 / Login

脚本：`scripts/login.py`

用户不用离开对话：给邮箱、（偶尔）输一次图形验证码、再输邮箱验证码，就完成注册或登录，脚本自动拿到 API Key 存在本机。

## 流程

```bash
# 1. 发邮箱验证码（新邮箱走注册，老邮箱走登录，脚本自己判断）
python3 scripts/login.py start --email user@example.com

# 2. 仅当上一步返回 "next": "enter_captcha" 时：用户照图输入字符
python3 scripts/login.py captcha --code 9139

# 3. 用户输入邮箱里收到的验证码
python3 scripts/login.py verify --code 123456
```

每一步都在 stdout 输出 JSON，看 `next` 字段决定下一步：

| 返回 | 含义 | 下一步 |
|---|---|---|
| `"next": "enter_captcha"` | 服务端要求先过图形验证码 | 把 `captcha_url`（或本地 `captcha_file`）给用户看，用户输入后跑 `captcha` |
| `"next": "enter_email_code"` | 验证码已发到邮箱 | 请用户查邮箱（含垃圾箱），跑 `verify` |
| `"ok": true, "api_key_tail"` | 登录成功，Key 已保存 | 重跑原来的命令 |
| `"error": "login_failed"` | 失败，`message` 里有原因 | 图形验证码错了就重新 `start`；邮箱验证码错了让用户再核对后重跑 `verify` |

图形验证码必须让用户本人辨认输入，agent 不要自己识别代填。

## Key 存在哪

- 文件：`~/.config/adsturbo/credentials.json`（权限 600），按站点分别保存，测试站和正式站互不影响；可用环境变量 `ADSTURBO_CONFIG_DIR` 换目录
- 所有脚本在 `ADSTURBO_API_KEY` 没设置时自动读它；环境变量优先
- 账号里已有名为 `adsturbo-skill` 的 Key 就直接复用，不会重复创建
- 输出只带 Key 的末 4 位，回复里不要回显完整 Key

## 其他命令

```bash
python3 scripts/login.py status   # 本机有没有可用的 Key、是哪个邮箱
python3 scripts/login.py logout   # 删掉本机保存的 Key（Key 本身仍有效，可在 https://adsturbo.ai/iris/api 删除）
```

## 注意

- 同一邮箱 30 秒内重复 `start` 不会重发新码，邮件里的码仍然有效
- 邮箱注册被关闭、账号已注销等情况会在 `message` 里说明，按提示处理
- 新注册账号不送积分，生成前积分不够时到 https://adsturbo.ai/pricing 充值
