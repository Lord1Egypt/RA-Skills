# Login (wechat-article-ego)

This skill checks its own login on https://mp.weixin.qq.com/. Do not add a separate cookie-healthcheck skill. Do not read Channels (`channels.weixin.qq.com`); that is a different product.

## soft-fail

`login_required: true`, exit code `2`, plus `how_to_login` / `how_to_login_zh`. The agent stops. It does not type a password, automate a QR scan, or paste cookies.

Signals:

- Logged out: the page is the QR / sign-in wall, or the console says 登录超时 / 请重新登录.
- Logged in: the login wall is gone and exactly one Official Account nickname is visible.
- Several nicknames, or a switcher with more than one account: exit `4`. Print the names. Do not save.

## What the human does

1. Open **Ego Lite** (the same profile `ego-browser` drives).
2. Open https://mp.weixin.qq.com/ and scan the QR. Pick the Official Account yourself.
3. Re-run `node scripts/check-login.mjs`. Continue only after exit `0`.

The task space always closes with `finish({ keep: [] })`. There is no `--keep`.

## 登录说明

1. 打开 **Ego Lite**（和 `ego-browser` 同一个配置档）。
2. 打开 https://mp.weixin.qq.com/ ，自己扫码并选中公众号。
3. 重新跑 `check-login`。退出码 `0` 再继续。退出码 `2` 或 `4` 就停。
