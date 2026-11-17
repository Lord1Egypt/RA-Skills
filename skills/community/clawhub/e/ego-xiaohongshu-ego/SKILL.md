---
name: xiaohongshu-ego
slug: ego-xiaohongshu-ego
displayName: Ego Xiaohongshu Notes
summary: Publish one Xiaohongshu video or image-text note via Ego Lite; --yes required; cover must confirm
description: >
  Publish one Xiaohongshu (小红书) note — video or image-text — through the creator web UI in Ego Lite.
  Login-check first. Soft-fail when ego-browser is missing, logged out, or --expect-account mismatches.
  Nothing uploads without --yes. Video notes accept --cover and click 发布 only after the 编辑封面 dialog
  changes the main-cover preview. Image-text notes take 1-18 images via --images. Notes cannot contain links.
  Ego Lite only, not MCP.
version: "0.2.0"
license: MIT
homepage: https://github.com/terryso/ego-skills/tree/main/skills/xiaohongshu-ego
metadata:
  version: "0.2.0"
  requires:
    bins:
      - ego-browser
      - node
  ego:
    min_skill_guide: "2.1.0"
---

# xiaohongshu-ego

用 Ego Lite 里已经登录的创作者会话，发**一条**小红书笔记：视频笔记或图文笔记。只走 creator 网页，不走 MCP。

Publish **one** note — a video note or an image-text note — through the logged-in creator site. Ego Lite and `ego-browser` only. Not MCP.

成功标准是 stdout 打出 `https://www.xiaohongshu.com/explore/<noteId>`，页面曾出现「发布成功」。没有这条链接就不算成功。

Success is `https://www.xiaohongshu.com/explore/<noteId>` after 「发布成功」.

## 先装 Ego

先装 **Ego Lite**，保证 `ego-browser` 在 `PATH`。非交互 shell 找不到时，再试 `~/.local/bin/ego-browser`。仍然缺失则 soft-fail（退出码 `2`），**不要**改用 Playwright、Puppeteer 或云端浏览器。

Install **Ego Lite** and put `ego-browser` on `PATH`. A non-interactive shell also tries `~/.local/bin/ego-browser`. If it is still missing, soft-fail with exit `2`. Do not switch to Playwright, Puppeteer, or a cloud browser.

## 封面

传 `--cover` 才会换主封面（例如 `cover-3x4.png`）。2026-11-05 改版后走「编辑封面」弹窗：悬停主封面卡片（`.cover--column .default.column`）让「编辑封面」（`.cover-edit-entry`）显现并点击，把图片传进弹窗里的 `.upload-btn input.upload-input`，等「完成」按钮变为可用后点它。主封面预览（卡片 background-image）必须发生变化，才点「发布」。确认失败就退出，不要带着视频首帧发布。

PK 封面槽不能代替主封面。只上传 PK 时，主封面和笔记管理缩略图仍是视频首帧，角标「封面待PK」，要等约 72 小时 PK 结束才会换。因此 `--cover` 不走 PK 槽。

不传 `--cover` 时，平台默认就是视频首帧。技能不会自己造一张封面。

图文笔记没有 `--cover`：第一张图就是封面，传了 `--cover` 直接校验失败。图文走「上传图文」tab，见下面的图文一节。

Pass `--cover` to set the **main** cover (for example `cover-3x4.png`) through the cover editor dialog, verified on 2026-11-05: hover the 主封面 card (`.cover--column .default.column`) to reveal 编辑封面 (`.cover-edit-entry`), click it, `setInputFiles` the image into `.upload-btn input.upload-input`, wait for the 完成 button to enable, then click it. Click 发布 only after the main-cover preview (the card's background-image) changes. If that confirmation fails, the run fails and does not publish the first frame.

PK slots are not this path. Uploading only a PK cover leaves the main cover and the note-manager thumbnail as the video's first frame (badge 封面待PK) until the 72-hour PK ends. `--cover` does not use the PK slots.

Without `--cover`, Xiaohongshu keeps the first frame. This skill does not invent a cover.

Image-text notes have no `--cover`: the first image is the cover, and passing `--cover` fails validation. Image-text publishes through the 上传图文 tab, see the image-text section below.

## 图文笔记

`--images` 接受逗号分隔的绝对路径（1–18 张，`.jpg` `.jpeg` `.png` `.webp`，单张不超过 32MB），和 `--video` 互斥。发布走「上传图文」tab：

1. 点文案恰好为「上传图文」的叶子元素。切过去之后 URL 会带 `target=image`。
2. 找到图片上传框。它和视频上传框**同类名** `input.upload-input`，只能靠 `accept` 区分：图文是 `.jpg,.jpeg,.png,.webp` 且 `multiple`，视频是 `.mp4,...`。绝不能把视频 accept 的输入当图片输入。
3. 一次 `setInputFiles` 传入全部路径（数组）。
4. 等所有缩略图出现（`blob:` 或 `sns-img` 的 `img` 数量 ≥ 张数，或计数 N/18 ≥ 张数），且没有「上传中 N%」「上传失败」，才继续。
5. 图文页的「发布」按钮在 **closed shadow root** 里，DOM 选择器摸不到，要用无障碍快照里的 `button [ref=N]`（精确文本「发布」）点 `ref=N`。**不要**点 `.btn-wrapper`——那是侧边栏「发布笔记」菜单，点了会把草稿存进草稿箱。详见 `references/imagetext-flow.md`。
6. 之后与视频相同：标题、正文、账号闸门、发布成功。

第一张图就是封面，没有确认环节。`--cover` 在图文模式下校验直接失败。

`--images` takes comma-separated absolute paths (1-18 images, `.jpg` `.jpeg` `.png` `.webp`, max 32MB each) and is mutually exclusive with `--video`. The flow clicks the 上传图文 tab (the URL gains `target=image`), finds the upload input — same class `input.upload-input` as the video input, told apart only by the accept `.jpg,.jpeg,.png,.webp` with `multiple` — sets all files in one `setInputFiles` call, waits until every thumbnail is counted (blob:/sns-img images ≥ count, or the N/18 counter ≥ count) with no 上传中/上传失败 text, then continues like a video: title, body, account gate, 发布, 发布成功. The first image is the cover; `--cover` fails validation on this mode.

## 不能带链接

小红书笔记不能出现链接。`--title`、`--desc`、`--topics` 里的 `http(s)://`、`www.`、裸域名（如 `github.com/xxx`、`x.com/xxx`）和 `t.co` 默认直接失败，退出码 `4`，并列出片段。不要发布。把链接从文案里删掉，或加 `--strip-links`：删掉链接，并去掉同一行上因此悬空的「项目地址：」「链接：」，收掉多余空行，同时打印删了什么。没有 `--yes` 的预检也做同样的检查。

Xiaohongshu notes must not contain links. By default, `http(s)://`, `www.`, bare domains such as `github.com/xxx` or `x.com/xxx`, and `t.co` in `--title`, `--desc`, or `--topics` fail with exit `4` and the offending fragments. Delete them from the copy, or pass `--strip-links` to remove the links, drop a dangling label such as `项目地址：` or `链接：` on that line, trim leftover blank lines, and print what was removed. The dry run without `--yes` uses the same check.

已经发出的笔记可以事后改封面，但那是尽力而为：`edit-cover.mjs`。保存可能重新进入「审核中」，并出现「封面PK中」。笔记管理里找不到、或更新页「加载失败」时不要重试。优先在第一次发布前换封面。

## 每次发布前：登录闸门

```bash
node scripts/check-login.mjs
node scripts/check-login.mjs --expect-account "听懂AI"
node scripts/check-login.mjs --keep
```

| 退出码 | 含义 | Agent 做什么 |
|--------|------|----------------|
| `0` | 已登录，且昵称匹配（若传了 `--expect-account`） | 把 `login_tip` 告诉用户，继续 |
| `2` | 未登录 / 昵称不符 / 无 ego-browser | 展示 `how_to_login`，**停** |
| `4` | 文案里有链接 | 把片段给人看。删掉链接，或改用 `--strip-links` 后再跑。不要加 `--yes` 硬发 |
| `1` | 其它错误 | 报告 JSON `error`，不要假装已经发出 |

`www.xiaohongshu.com` 上的账号可能和创作者平台不是同一个。只看创作者页眉昵称。不要代填密码，不要粘贴 Cookie。

默认 `finish({ keep: [] })`。`--keep` 才把页面留着并 `handOff()`。

## 确认规则

没有 `--yes`：只检查登录并打印计划 JSON（`cover_mode` 为 `main-cover`，`cover_selector` 为「编辑封面」，并带上封面路径），退出码 `3`。这一步不上传视频，也不点「发布」。

有 `--yes`：才会上传。如果带了 `--cover`，必须走「编辑封面」弹窗设置主封面，并且主封面预览发生变化，才点「发布」。预览没变就失败退出，不发布。PK 槽不算主封面。

Without `--yes` the command only inspects login and prints the plan JSON (`cover_mode=main-cover`, `cover_selector=编辑封面`, plus the cover path), then exits `3`. It does not upload and it does not click 发布.

With `--yes` it uploads. When `--cover` is set, it must set the main cover through the 编辑封面 dialog and click 发布 only after the main-cover preview changes. If the preview does not change, the run fails and does not publish. PK slots do not count as the main cover.

## 命令

仓库根目录。每次只发一条。调用方传绝对路径，不要写死产品目录。

```bash
node skills/xiaohongshu-ego/scripts/check-login.mjs --expect-account "听懂AI"
node skills/xiaohongshu-ego/scripts/post-video.mjs \
  --video /absolute/path/to/video.mp4 \
  --title "标题" \
  --desc "正文" \
  --topics "#话题1 #话题2" \
  --cover /absolute/path/to/cover-3x4.png \
  --expect-account "听懂AI"
node skills/xiaohongshu-ego/scripts/post-video.mjs \
  --video /absolute/path/to/video.mp4 \
  --title "标题" \
  --desc "正文" \
  --topics "#话题1 #话题2" \
  --cover /absolute/path/to/cover-3x4.png \
  --expect-account "听懂AI" \
  --yes --json
node skills/xiaohongshu-ego/scripts/post-images.mjs \
  --images /absolute/path/to/1.jpg,/absolute/path/to/2.jpg,/absolute/path/to/3.jpg \
  --title "标题" \
  --desc "正文" \
  --topics "#话题1 #话题2" \
  --expect-account "听懂AI"
node skills/xiaohongshu-ego/scripts/post-images.mjs \
  --images /absolute/path/to/1.jpg,/absolute/path/to/2.jpg \
  --title "标题" \
  --desc "正文" \
  --topics "#话题1 #话题2" \
  --expect-account "听懂AI" \
  --yes --json
node skills/xiaohongshu-ego/scripts/edit-cover.mjs \
  --note-id <noteId> --cover /absolute/path/to/cover-3x4.png
node skills/xiaohongshu-ego/scripts/cleanup.mjs
```

| 退出码 | 含义 |
|--------|------|
| `0` | 已登录，或已发出并打印 explore 链接，或 cleanup 关掉了本机空间 |
| `3` | 计划已打印，拒绝上传 |
| `2` | 未登录、昵称不符，或没有 `ego-browser` |
| `4` | 标题、正文或话题里有链接。没有 `--strip-links` 时不上传 |
| `1` | 参数、封面未确认、或浏览器错误 |

`--json` 打出摘要 JSON。不加 `--json` 且发布成功时，stdout 只有 explore 链接。

`cleanup` 关掉名称以 `xiaohongshu-ego` 开头的任务空间。它不删笔记。

## 不做

定时发布、一次跑多条、MCP、删笔记。图文只支持一次性传齐 1–18 张，不支持追加、排序或删图。发布后改封面不是主路径。

## 测试

```bash
npm test
```

`npm test` 用 c8 统计 `scripts/lib/**/*.mjs`（不含 `ego-deps.mjs`），行覆盖率不低于 80%。单测不访问小红书。

界面步骤见 `references/publish-flow.md`（视频）与 `references/imagetext-flow.md`（图文）。登录见 `references/login.md`。
