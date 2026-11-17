---
name: x-post
description: >
  Post on X (x.com / twitter.com) through the logged-in Ego Lite session.
  Login-check first and soft-fail with exit 2 when ego-browser is missing or
  x.com is logged out. Sends only with --yes after the draft is shown.
  Uses page.fetch CreateTweet, not the composer click path. Optional --image
  uploads up to 4 png/jpeg/webp files only after --yes. Reply is best-effort.
  Use when the user asks to tweet, post, reply, or attach images on X or Twitter from Ego.
metadata:
  version: "0.2.0"
  requires:
    bins:
      - ego-browser
      - node
  ego:
    min_skill_guide: "2.1.0"
---

# x-post

用 Ego Lite 里已经登录的 Chromium 会话往 X 发帖。主路径是 `page.fetch` 的 **CreateTweet**，不点「发帖」。

Post to X through the logged-in Ego Lite session. The primary path is `page.fetch` **CreateTweet**. Do not click the composer.

成功标准是 stdout 打出 `https://x.com/<screen_name>/status/<id>`。没有这条链接就不算成功。不要顺手点其它确认框。

Success is the status URL on stdout: `https://x.com/<screen_name>/status/<id>`. Do not click unrelated confirmations.

## 先装 Ego

先装 **Ego Lite**，保证 `ego-browser` 在 `PATH`。缺失则 soft-fail（退出码 `2`），**不要**改用 Playwright、Puppeteer 或云端浏览器。

Install **Ego Lite** and put `ego-browser` on `PATH`. If it is missing, soft-fail with exit `2`. Do not switch to Playwright, Puppeteer, or a cloud browser.

## 每次发帖前：登录闸门（必做）

```bash
node scripts/check-login.mjs
node scripts/check-login.mjs --keep
```

| 退出码 | 含义 | Agent 做什么 |
|--------|------|----------------|
| `0` | 已登录 | 把 `login_tip` 告诉用户，继续 |
| `2` | 未登录 / 无 ego-browser | 展示 `how_to_login` / `how_to_login_zh`，**停** |
| `1` | 其它错误 | 报告 JSON `error`，不要假装已经发出 |

`auth_token` 是 HttpOnly，只存在于浏览器 Cookie 罐。不要打印 Cookie，不要粘贴 Cookie，不要代填密码。

默认 `finish({ keep: [] })`。`--keep` 才把页面留着并 `handOff()`。

## 确认规则

没有 `--yes` 只打印草稿并退出码 `3`，**不发送**。Agent 必须把草稿给人看，等人确认后再加 `--yes`。

Without `--yes` the command prints the draft and exits `3`. It does not send. Show that draft to the user. Add `--yes` only after they confirm.

## 命令

仓库根目录：

```bash
node skills/x-post/scripts/check-login.mjs
node skills/x-post/scripts/post.mjs --text "..."
node skills/x-post/scripts/post.mjs --text "..." --yes
node skills/x-post/scripts/post.mjs --text "..." --reply-to <statusId> --yes
node skills/x-post/scripts/post.mjs --text "..." --yes --json
node skills/x-post/scripts/post.mjs --text "..." --image /absolute/path/to/image.png
node skills/x-post/scripts/post.mjs --text "..." --image /absolute/path/to/image.png --image /absolute/path/to/other.webp --yes --json
node skills/x-post/scripts/cleanup.mjs
```

已安装的技能目录里用 `node scripts/...`。

| 退出码 | 含义 |
|--------|------|
| `0` | 已登录，或已发出并打印状态链接，或 cleanup 关掉了本机空间 |
| `3` | 草稿已打印，拒绝发送 |
| `2` | 未登录，或没有 `ego-browser` |
| `1` | 参数、HTTP、GraphQL 或浏览器错误 |

`--json` 打出摘要 JSON。不加 `--json` 且发送成功时，stdout 只有状态链接。

`cleanup` 只对任务空间 `x-post` 执行 `finish({ keep: [] })`。它不删帖。

## 回复

`--reply-to` 会在同一条 mutation 上加 `variables.reply`。2026-11-04 的实页 `page.fetch` 回复返回 GraphQL **226**，**没有**验证成功。当尽力而为：失败就把错误给人，不要改去点回复框，不要重试。

## 短帖和长文

加权长度用 twitter-text v3 的 `maxWeightedTweetLength`（280）。不超过就发 **CreateTweet**。超过，或显式 `--long`，就发 **CreateNoteTweet**（2026-11-04 捕获）。普通 `/compose/post` 的长文就会走这条，不必打开 Articles。

CreateTweet 和 CreateNoteTweet 都带现算的 `x-client-transaction-id`。verification key 和 `loading-x-anim` 从 x.com 文档读。`ondemand.s` 和 `main.*.js` 的地址从文档或 performance 发现。字节谁先返回用谁：页面里已经加载的脚本；**并行**的 Node HTTPS（`ECONNRESET` 等中断会退避重试）和 Ego 浏览器网络。浏览器这条走 CDP `Network.loadNetworkResource`；该方法没有正文时，把 `<script src>` 插进当前 x.com 页面，再用 script 文本、performance resource、`Page.getResourceContent` 和 `Network.getResponseBody` 读取。check-login 刚结束时主页常常还没有 `ondemand.s`，所以短帖也会主动让浏览器去拉，而不是只读空缓存。`page.fetch` 不用于 `abs.twimg.com`（CORS 会得到 0 字节），也不为了热身去点作曲框。query id 来自这份 `main.*.js`。不要复用别的 GraphQL 请求上的 transaction id。长文仍在材料齐了之后打开 `https://x.com/compose/post`，等两秒，再发。两边都拿不到字节就退出码 `1`、`sent: false`，错误里写明缺什么。也可以传 `--transaction-id`。不要编一个假的。

成功仍然是 `https://x.com/<screen_name>/status/<id>`。长文的完整正文在 `note_tweet.note_tweet_results.result.text`；`legacy.full_text` 会被截断，不当成全文。

## 接口

`queryId` 会随 `main.*.js` 轮换。先从当前包里读对应的 `operationName`，读不到再用 2026-11-04 的捕获值：CreateTweet `l4hk8uVGvR-a8kzQ4nOhPA`，CreateNoteTweet `seOZkIS8AysCGfPo6yYPVA`。不要发明其它 query id。字段见 `references/create-tweet.md`。坑见 `references/pitfalls.md`。

没有 `--image` 时 `media.media_entities` 仍是 `[]`。私信、点赞、关注不做。GraphQL **186** 表示这条文本对短帖太长。

## 图片

`--image <路径>` 可重复，最多 4 张。只接受 png、jpeg、webp，每张不超过 5 MiB（5242880 字节）。GIF 不支持。文件是否存在、类型、大小和张数都在任何网络请求之前检查；不合格是退出码 `1`。没有 `--yes` 时草稿列出路径、字节数和 md5，不上传。加上 `--yes` 之后，在已登录的 x.com 页面里用 `page.evaluate` 走 upload.x.com 的 INIT → APPEND → FINALIZE，再把 `media_id_string` 放进 CreateTweet 或 CreateNoteTweet。不点「发帖」。细节见 `references/media-upload.md`。

## Images

`--image <path>` is repeatable, up to 4 files. png, jpeg, and webp only, each at most 5 MiB (5242880 bytes). GIF is rejected. Existence, type, size, and count are checked before any network call; a bad file exits `1`. Without `--yes` the draft lists path, bytes, and md5, and nothing is uploaded. With `--yes`, `page.evaluate` runs INIT → APPEND → FINALIZE on upload.x.com, then CreateTweet or CreateNoteTweet receives `media_id_string`. The script does not click Post. See `references/media-upload.md`.

## Pro 冒烟（公告原文）

先 `check-login`（退出码 0）。把下面这段原文给人看，确认后再加 `--yes`。成功时 stdout 是 `https://x.com/<screen_name>/status/<id>`。不要删这条公告。

```text
ego-skills x-post: post on X from a logged-in Ego Lite session (page.fetch CreateTweet). Login-check first. Nothing sends without --yes. https://github.com/terryso/ego-skills
```

```bash
node skills/x-post/scripts/post.mjs --text "ego-skills x-post: post on X from a logged-in Ego Lite session (page.fetch CreateTweet). Login-check first. Nothing sends without --yes. https://github.com/terryso/ego-skills"
node skills/x-post/scripts/post.mjs --text "ego-skills x-post: post on X from a logged-in Ego Lite session (page.fetch CreateTweet). Login-check first. Nothing sends without --yes. https://github.com/terryso/ego-skills" --yes
```

## 测试

```bash
npm test
```

`npm test` 用 c8 统计 `scripts/lib/**/*.mjs`（不含 `ego-deps.mjs`），行覆盖率不低于 80%。单测不访问 x.com。

## Changelog

- **0.2.0** — `--image` 可附最多 4 张 png/jpeg/webp（每张 ≤ 5 MiB）。上传按 2026-11-04 捕获的 upload.x.com INIT → APPEND → FINALIZE，在 `page.evaluate` 里执行。没有 `--yes` 不上传。GIF 不支持。
