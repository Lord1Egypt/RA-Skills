# 登录 / Login

## 检查方式

`check-login.mjs` 打开 `https://member.bilibili.com/platform/upload/video/frame` 并做三级判断:

1. URL 跳到 `passport.bilibili.com/login` 或含 `/login` → 未登录
2. shadow-DOM 文本含「扫码登录 / 请登录」且没有创作中心导航 → 未登录
3. 文本含「创作中心 / 投稿 / 内容管理 / 上传视频」→ 已登录

`document.cookie` 里的 `DedeUserID` 只作参考信号,不单独作为登录依据。

## 退出码

| code | 含义 |
|------|------|
| 0 | 已登录,`login_tip` 说明可继续 |
| 2 | 未登录或 ego-browser 缺失。JSON 含 `how_to_login` / `how_to_login_zh` |
| 1 | 打开页面或探测异常 |

## 让用户登录

`--keep` 会让 check-login 停在登录页并 `handOff()` 把窗口交给用户;用户在 Ego Lite 里打开 `bilibili.com` 或 `member.bilibili.com` 扫码即可。登录态存在 Ego 的浏览器 profile 里,不需要单独的 cookie 文件。

`publish.mjs` 在投稿中途遇到登录墙也会输出同样的 `login_required` JSON 并 `handOff()`(退出码 2),登录后用 `--space-id` 回到原 space 续跑。
