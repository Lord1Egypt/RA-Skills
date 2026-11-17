---
slug: ego-douyin-video
displayName: Ego Douyin Video
summary: "Publish a local video to the Douyin creator center (creator.douyin.com) with Ego Lite via ego-browser. Login-check first. Title is a separate field of at most 30 characters. Success is a redirect t..."
license: MIT
homepage: https://github.com/terryso/ego-skills/tree/main/skills/douyin-video
name: douyin-video
description: Publish a local video to the Douyin creator center (creator.douyin.com) with Ego Lite via ego-browser. Login-check first. Title is a separate field of at most 30 characters. Success is a redirect to content management or a publish-success message. The caller supplies a local video file. This skill does not download video. Use when the user asks to post to 抖音, 抖音发视频, 发布到抖音创作者中心, or creator.douyin.com.
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

# douyin-video

用 Ego Lite 会话把**本地视频**发到 [抖音创作者中心](https://creator.douyin.com)。终点是跳到**内容管理**（`content/manage`）或页面出现**「发布成功」**。

Publish a **local video file** to the Douyin creator center. Success is a redirect to content management or the text 发布成功. This skill does not download video and does not call yt-dlp.

搬运他人内容前，确认调用方拥有相应权利。平台会打击未授权搬运。

## 先装 Ego

先装 **Ego Lite**，保证 `ego-browser` 在 `PATH`。缺失则 soft-fail / 告知用户去装，**不要**硬调浏览器。

Install **Ego Lite** and put `ego-browser` on `PATH`. If either is missing, soft-fail and tell the user. Do not hard-require the browser.

在 Ego 里已经登录抖音时效果更好。每次发布前把这句话告诉用户。

Being logged into Douyin inside Ego works better. Say that to the user before every publish.

## 每次发布前：登录闸门（必做）

Agent **在上传之前**必须跑：

```bash
node scripts/check-login.mjs
# 需要把窗口留给人扫码时：
node scripts/check-login.mjs --keep
```

| 退出码 | 含义 | Agent 做什么 |
|--------|------|----------------|
| `0` | 已登录 | 把 `login_tip` 告诉用户，继续发布 |
| `2` | 未登录 / 无 ego-browser | 展示 `how_to_login` / `how_to_login_zh`，**停**。请人在 Ego 扫码后再跑 check-login |
| `1` | 其它错误 | 报告 JSON `error`，不要假装已发布 |

详见 `references/login.md`。不要另做 cookie-healthcheck 技能。

默认 `finish({ keep: [] })`。`--keep` 才把登录页留着并 `handOff()`。

## 输入（通用，无本机产品路径）

调用方提供本地文件和文案。见 `references/inputs.md`。本技能**不**绑定任何产品系列、播客或业务目录，也**不**下载视频。

最少需要：本机 `video` 路径、`title`（独立输入框，最多 30 个 Unicode 码位）、`desc`（话题写在简介里）。

默认设置即合理：公开、允许保存、立即发布。不要额外去改这些开关。

## CLI

`ego-browser nodejs` 不继承 shell 环境变量，也不转发 shell argv。`publish.sh` 先把 JSON 写到 `/tmp/douyin-video-publish.json`，再交给 ego。

```bash
# 仓库根目录
node skills/douyin-video/scripts/check-login.mjs
node skills/douyin-video/scripts/check-login.mjs --keep
bash skills/douyin-video/scripts/publish.sh /absolute/path/to/video.mp4 "标题" "简介 #话题"
# 登录 handOff 或位置权限弹窗中断后，第 4 个参数传 spaceId。第 5 个参数 1 才保留浏览器页。
bash skills/douyin-video/scripts/publish.sh /absolute/path/to/video.mp4 "标题" "简介" 6
bash skills/douyin-video/scripts/publish.sh /absolute/path/to/video.mp4 "标题" "简介" 6 1
```

已安装的技能目录里用相对路径：`node scripts/check-login.mjs`、`bash scripts/publish.sh …`。

| 退出码 | 含义 |
|--------|------|
| `0` | 成功。stdout 含 `{"ok":true,"manageUrl":"https://creator.douyin.com/creator-micro/content/manage",...}` |
| `1` | 参数或流程错误。位置权限打断时 JSON 带 `resume: true` 和 `spaceId` |
| `2` | 需要登录。发布脚本会 `handOff()` 并把 space 留着，方便扫码后带 spaceId 续跑 |

创作者表单没有 wujie。Agent 不要另写一套填表脚本，除非脚本报了 flow error 并留下 `spaceId`。

## 发布脚本在做什么

1. 若当前 URL 已是 `/content/post/video`（带 `spaceId` 续跑），跳过上传。
2. 否则打开 `https://creator.douyin.com/creator-micro/content/upload`。
3. 用正文判断登录：出现「扫码登录 / 二维码登录 / 请登录」，或没有「点击上传 / 上传视频」，则 exit 2 并 `handOff()`。文档标题里的产品名不算已登录。
4. 先 `waitForFileChooser`，再点去空白后文本恰好是「上传视频」的按钮（文本可能被拆成「上传」「视频」）。
5. 等到 URL 含 `/content/post/video`，并且正文出现「作品描述」或「添加作品简介」。
6. 用 native setter 写标题（占位含「作品标题」），回读必须和传入标题一致。超过 30 个码位直接失败。
7. 用 `execCommand('insertText')` 写简介（contenteditable，占位「添加作品简介」），回读必须一致。
8. 用 TreeWalker 找 `<button>`，其**自身文本**恰好是「发布」（不是「立即发布 / 定时发布 / 同时发布」），`scrollIntoView` 后坐标点击。
9. 成功：URL 含 `content/manage`，或正文出现「发布成功」。

成功时默认 `finish({ keep: [] })`。其它流程错误也会关掉 space。登录墙和位置权限打断**不关**，以便用同一个 `spaceId` 续跑。第 5 个参数 `1` 才在成功后保留页面。

## 位置权限打断

首次点击上传时，抖音可能申请地理位置。ego 会以 user-control 错误停掉这次调用。让用户在浏览器里处理（建议拒绝），然后用打印的 `spaceId` 重跑。点击通常已经生效，脚本看到发布表单就跳过重复上传。

## 评论

评论管理还没有脚本。需要发评论时走人工，或先探测页面再操作。不要在本技能里发明评论步骤。说明见 `references/pitfalls.md`。

## 避坑

完整清单在 `references/pitfalls.md`。发布前先 login-check；exit 2 必须停。

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
