---
slug: ego-kuaishou-video
displayName: Ego Kuaishou Video
summary: "Publish a local video to the Kuaishou creator platform (cp.kuaishou.com) with Ego Lite via ego-browser. Login-check first. Success means the work shows 审核中. Optional comment from the creator commen..."
license: MIT
homepage: https://github.com/terryso/ego-skills/tree/main/skills/kuaishou-video
name: kuaishou-video
description: Publish a local video to the Kuaishou creator platform (cp.kuaishou.com) with Ego Lite via ego-browser. Login-check first. Success means the work shows 审核中. Optional comment from the creator comment manager. The caller supplies a local video file and a description. This skill does not download video. Use when the user asks to post to 快手, 快手发视频, 发布到快手创作者平台, or comment on a Kuaishou work from the creator backend.
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

# kuaishou-video

用 Ego Lite 会话把**本地视频**发到 [快手创作者服务平台](https://cp.kuaishou.com)。终点是作品进入**「审核中」**。

Publish a **local video file** to the Kuaishou creator platform. The endpoint is **审核中**. This skill does not download video.

## 先装 Ego

先装 **Ego Lite**，保证 `ego-browser` 在 `PATH`。缺失则 soft-fail / 告知用户去装，**不要**硬调浏览器。

Install **Ego Lite** and put `ego-browser` on `PATH`. If it is missing, soft-fail and tell the user. Do not hard-require the browser.

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

最少需要：本机 `video` 绝对路径、`desc`（话题写在描述字符串里，如 `描述 #话题1 #话题2`）。

## CLI

`ego-browser nodejs` 不继承 shell 环境变量，也不转发 shell argv。`publish.sh` / `comment.sh` 先把 JSON 写到 `/tmp`，再交给 ego。

```bash
# 仓库根目录
node skills/kuaishou-video/scripts/check-login.mjs
node skills/kuaishou-video/scripts/check-login.mjs --keep
bash skills/kuaishou-video/scripts/publish.sh /absolute/path/to/video.mp4 "描述 #话题1 #话题2"
# 登录 handOff 或中断后，用 spaceId 续跑；最后一个 1 表示保留浏览器页
bash skills/kuaishou-video/scripts/publish.sh /absolute/path/to/video.mp4 "描述" 4 1

# 可选：后台评论管理（不是 www 公开页）
bash skills/kuaishou-video/scripts/comment.sh "评论内容"
bash skills/kuaishou-video/scripts/comment.sh "评论内容" "标题片段" 4 1
```

已安装的技能目录里用相对路径：`node scripts/check-login.mjs`、`bash scripts/publish.sh …`。

| 退出码 | 含义 |
|--------|------|
| `0` | 成功。发布 stdout 含 `{"ok":true,"status":"审核中",...}` |
| `1` | 参数或流程错误 |
| `2` | 需要登录。发布/评论脚本在登录墙上会 `handOff()` |

创作者表单没有 wujie，所以上传、描述、点击发布由 `publish.js` 做完。Agent 不要另写一套填表脚本，除非脚本报了 flow error 并留下 `spaceId`。

## 发布脚本在做什么

1. 打开 `https://cp.kuaishou.com/article/publish/video`。
2. 用正文判断登录：出现「扫码登录 / 二维码登录 / 请登录」且没有创作者后台，则 exit 2 并 `handOff()`。
3. 先 `waitForFileChooser`，再点 `loc=role:button[name='上传视频']`。
4. 等到「重新上传」，再等到「上传中」消失并隔 2 秒复核。
5. 写入 contenteditable 描述，回读 `innerText`，必须和 `desc` 一致。
6. 用元素**自身文本精确等于「发布」**定位（不是「立即发布 / 定时发布」），`scrollIntoView` 后坐标点击。
7. 成功：URL 含 `article/manage/video`，且页面有「审核中」。

成功时默认 `finish({ keep: [] })`。第 4 个参数 `1` 才保留页面。

## 评论（可选）

`comment.sh` 打开 `https://cp.kuaishou.com/article/comment`。该页默认选中最新作品。占位是「有爱评论，说点儿好听的」，发送按钮用精确文本「发送」。

成功：toast「发送成功」，且评论出现在列表里。标题片段对不上就 exit 1，不要发错作品。

`cp.kuaishou.com` 和 `www.kuaishou.com` **不共享登录态**。不要去公开页评论。

## 避坑

完整清单在 `references/pitfalls.md`。发布前先 login-check；exit 2 必须停。

## 手动兜底

`publish.js` / `comment.js` 报错后，JSON 里的 `spaceId` 可以回到原 space。不要为了排查再开一个 space。

```bash
ego-browser nodejs <<'EOF'
const task = await taskSpace(4);
const page = task.page("p1");
console.log({ url: await page.url() });
console.log(await page.snapshot());
EOF
```

把 `4` 换成实际 `spaceId`。

## 测试

```bash
npm test
```
