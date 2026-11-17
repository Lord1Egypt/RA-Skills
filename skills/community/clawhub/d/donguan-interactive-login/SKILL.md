---
name: donguan-interactive-login
description: "动环综合网管（温湿度监控平台）交互式登录工具。自动识别图片验证码(RSA-OAEP-SHA256加密密码)并触发短信下发，用户仅需手动输入手机短信验证码即可完成登录，保存Cookie供脚本/定时任务复用。触发场景：登录动环系统、获取动环Cookie、动环网管2FA登录、刷新动环Session、动环登录验证码、dh login、动环综合网管登录。"
agent_created: true
---

# 动环综合网管 交互式登录

## Overview

动环综合网管（温湿度监控平台）登录需要 **三要素**：用户名 + 密码（RSA加密）+ 图片验证码 + 手机短信验证码（2FA）。
本 skill 封装交互式登录流程：脚本自动识别图片验证码并 RSA 加密密码，**主动调用 `/login/sendPhoneCode` 触发短信下发**，用户只需查收手机、输入短信码即可完成登录，最后把 `WEB_SESSION_ID_KEY` Cookie 写入指定文件，供定时任务/监控脚本复用。

> 关键经验：登录接口 `/login/go` **不会自动下发短信**，必须先单独调用 `/login/sendPhoneCode`（带图片验证码）触发短信，否则会一直返回"动态码失效"。这是本 skill 与"直接调 login/go"的本质区别。

## 环境依赖

- `curl`：用于 HTTP 请求（脚本已 `-k` 忽略自签名证书）
- `openssl`：用于 RSA-OAEP-SHA256 加密密码
- `ddddocr`：用于图片验证码 OCR（自动识别算术题），需提前安装：
  ```bash
  pip install ddddocr
  ```

## 用法

### 基本用法

```bash
python <skill_dir>/scripts/donguan_login.py \
  --username 05310480 \
  --password 'XZ$ua98E#dYO' \
  --cookie-file dh_session_cookie.txt
```

执行后终端交互流程：
```
=== 动环系统交互式登录 ===
用户名: 05310480
验证码图片已保存: .../_captcha.png
[OCR识别] 算式: 5x0=9  答案: 0
（请确认图片中的算式答案，如有偏差请手动输入正确值）
请输入图片验证码算式答案: 0          <- 脚本已OCR，回车即可
[OK] 短信已发送！，请查收手机
请输入手机短信验证码（动态码）: 361823   <- 用户查收手机输入
[成功] 登录成功! Cookie 已保存到: dh_session_cookie.txt
```

### 指定动环系统地址

```bash
python <skill_dir>/scripts/donguan_login.py \
  --base-url https://172.20.251.9:30666 \
  --username 05310480 \
  --password 'XZ$ua98E#dYO' \
  --cookie-file /path/to/dh_session_cookie.txt
```

### 在 Python 中直接调用

```python
import sys
sys.path.insert(0, '<skill_dir>/scripts')
from donguan_login import interactive_login

cookie = interactive_login(
    base='https://172.20.251.9:30666',
    username='05310480',
    password='XZ$ua98E#dYO',
    cookie_file='dh_session_cookie.txt',
    workdir='.',   # 临时文件（_captcha.png/_login_cookies.txt等）目录
)
if cookie:
    print('登录成功, Cookie=', cookie[:12], '...')
```

## 登录流程详解（已验证）

1. 建立会话：`GET /` 并保存会话 Cookie 到临时文件 `_login_cookies.txt`
2. 下载验证码：`GET /login/getVerifyCode?sign=1` → 保存 `_captcha.png`
3. OCR 识别：`ddddocr` 解析算术题（如 `5×0=?`），输出答案供确认
4. 获取公钥：`POST /login/getPublicKey` → RSA-OAEP-SHA256 加密密码
5. **触发短信**：`POST /login/sendPhoneCode`（参数含用户名/密文/图片验证码）→ 返回"短信已发送！"
6. 用户输入短信码（终端 `input`）
7. 完成登录：`POST /login/go`（含短信码）→ code=200 成功
8. 保存 Cookie：`WEB_SESSION_ID_KEY` 写到 `--cookie-file`

## 注意事项

- 图片验证码会随会话消耗，**每次登录都需重新下载**（脚本自动处理）
- 短信码有效期约 180 秒，倒计时结束后需重新触发发送
- Cookie 写入文件后，监控脚本 `acquire_session()` 会优先读取该文件，实现定时任务全自动运行
- 密码以明文作为参数传入，请确保执行环境安全（不要在共享终端暴露命令历史）
- ddddocr 对 `?` 常误识为 `9`、`×` 误识为 `x`，脚本已做算术后处理，答案通常正确，但建议用户看 `_captcha.png` 图片二次确认
- 自签名证书使用 `curl -k` 跳过校验，仅限内网可信环境使用
