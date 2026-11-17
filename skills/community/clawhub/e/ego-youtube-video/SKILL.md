---
slug: ego-youtube-video
displayName: Ego YouTube Video
summary: "Publish a local video to YouTube Studio (studio.youtube.com) with Ego Lite via ego-browser. Login-check first. Default visibility is private and Made for kids is No. Success is a video URL or ID pl..."
license: MIT
homepage: https://github.com/terryso/ego-skills/tree/main/skills/youtube-video
name: youtube-video
description: Publish a local video to YouTube Studio (studio.youtube.com) with Ego Lite via ego-browser. Login-check first. Default visibility is private and Made for kids is No. Success is a video URL or ID plus a processing status. The caller supplies a local video file. This skill does not download video. Use when the user asks to upload or publish a video to YouTube, YouTube Studio, or 发布到 YouTube.
metadata:
  version: "0.1.0"
  requires:
    bins:
      - ego-browser
      - node
  ego:
    min_skill_guide: "2.1.0"
version: "0.1.0"
---

# youtube-video

用 Ego Lite 会话把**本地视频**发到 [YouTube Studio](https://studio.youtube.com/)。成功是拿到**视频链接 / 视频 ID**，并读到处理状态（Uploading、Upload complete、Processing、Checks complete、Saved 或 Published）。

Publish a **local video file** to YouTube Studio. Success is a **video URL or ID** plus a processing status. This skill does not download video and does not call yt-dlp.

## 先装 Ego

先装 **Ego Lite**，保证 `ego-browser` 在 `PATH`。缺失则 soft-fail / 告知用户去装，**不要**硬调浏览器。

Install **Ego Lite** and put `ego-browser` on `PATH`. If either is missing, soft-fail and tell the user. Do not hard-require the browser.

在 Ego 里已经登录 YouTube 时效果最好。每次发布前把这句话告诉用户。

Being logged in to YouTube inside Ego gives the best results. Say that to the user before every publish.

## 每次发布前：登录闸门（必做）

Agent **在上传之前**必须跑：

```bash
node scripts/check-login.mjs
# 需要把窗口留给人登录时：
node scripts/check-login.mjs --keep
```

| 退出码 | 含义 | Agent 做什么 |
|--------|------|----------------|
| `0` | 已登录 | 把 `login_tip` 告诉用户，继续发布 |
| `2` | 未登录 / 无 ego-browser | 展示 `how_to_login` / `how_to_login_zh`，**停**。请人在 Ego 登录 YouTube 后再跑 check-login |
| `1` | 其它错误 | 报告 JSON `error`，不要假装已发布 |

详见 `references/login.md`。不要另做 cookie-healthcheck 技能。

默认 `finish({ keep: [] })`。`--keep` 才把登录页留着并 `handOff()`。

## 输入（通用，无本机产品路径）

调用方提供本地文件和文案。见 `references/inputs.md`。本技能**不**绑定任何产品系列、播客或业务目录，也**不**下载视频。

最少需要：本机 `video` 路径、`title`。`description` 可空。`tags`、`thumbnail` 可选。`visibility` 默认 `private`（`unlisted` / `public` 必须调用方明确要求）。Made for kids 默认 **No**。

## CLI

`ego-browser nodejs` 不继承 shell 环境变量，也不转发 shell argv。`publish.sh` 先把 JSON 写到 `/tmp/youtube-video-publish.json`，再交给 ego。

```bash
# 仓库根目录
node skills/youtube-video/scripts/check-login.mjs
node skills/youtube-video/scripts/check-login.mjs --keep
bash skills/youtube-video/scripts/publish.sh /absolute/path/to/video.mp4 "Title" "Description"
bash skills/youtube-video/scripts/publish.sh \
  --video /absolute/path/to/video.mp4 \
  --title "Title" \
  --description "Description" \
  --tags "one,two" \
  --visibility private \
  --thumbnail /absolute/path/to/thumbnail.jpg \
  --made-for-kids no \
  --space-id 4 \
  --keep
```

已安装的技能目录里用相对路径：`node scripts/check-login.mjs`、`bash scripts/publish.sh …`。

| 退出码 | 含义 |
|--------|------|
| `0` | 成功。stdout 含 `{"ok":true,"videoId":"…","videoUrl":"https://youtu.be/…","status":"Processing",…}` |
| `1` | 参数或流程错误 |
| `2` | 需要登录，或本机没有 `ego-browser` |

不要为了排查再开一个上传。登录 handOff 或中断后，用 `--space-id` 回到原来的 space。

## 发布脚本在做什么

1. 打开 `https://studio.youtube.com/`。
2. 用正文判断登录。跳到 `accounts.google.com` / `/signin`，或正文是 Google 登录 / 选择账号，则 exit 2。文档标题里的 “YouTube Studio” 不算已登录。
3. 点创建（`#create-icon`），再点「Upload videos / 上传视频」，直到出现 `#select-files-button`。
4. 先 `waitForFileChooser`，再点选择文件，把调用方的本地视频交给文件选择器。
5. 等到进度或 `youtu.be` 链接出现。
6. 写入标题和简介（可空）。标题在 shadow DOM 的 `#textbox` 里，写完要回读，必须和传入标题一致。
7. 有缩略图时，再用文件选择器点 `#file-loader`（或 Upload thumbnail / 上传缩略图）。
8. 有标签时先点 Show more / 显示更多，再写入 `#tags-container`。
9. 观众设置默认点 **No, it's not made for kids**（`VIDEO_MADE_FOR_KIDS_NOT_MFK`）。只有调用方明确要求才点 Yes。
10. 点三次 Next，直到公开范围单选出现。默认点 **Private**。`public` 只有调用方传入才选，按钮文案这时是 Publish；private / unlisted 是 Save。
11. 点 `#done-button`。
12. 成功：从页面链接抽出 11 位视频 ID，并读到处理状态。不等到 HD 处理结束。

成功和失败默认都 `finish({ keep: [] })`。只有 `--keep` 才把页面留着。

## 避坑

完整清单在 `references/pitfalls.md`。发布前先 login-check；exit 2 必须停。不要把未登录当成已发布。

## 手动兜底

`publish.js` 报错后，JSON 里的 `spaceId` 可以回到原 space。不要为了排查再开一个 space。

```bash
ego-browser nodejs <<'EOF'
const task = await taskSpace(4);
const page = task.page("p1");
console.log({ url: await page.url() });
console.log(await page.snapshot());
EOF
```

把 `4` 换成实际 `spaceId`。看完执行 `finish({ keep: [] })`。

## 测试

```bash
npm test
```
