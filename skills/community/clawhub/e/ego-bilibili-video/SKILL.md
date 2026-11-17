---
name: bilibili-video
slug: ego-bilibili-video
displayName: Ego Bilibili Video
summary: Publish a local video to Bilibili with Ego Lite. Login-check first. Nothing is submitted without --yes.
description: Publish a local video to the Bilibili creator platform (member.bilibili.com) with Ego Lite via ego-browser. Login-check first. Bilibili wants TWO covers uploaded separately: --cover-4x3 (首页推荐) and --cover-16x9 (个人空间). Nothing is submitted without --yes: that run only prints a local plan and exits 3. --type selects a partition from the human-type list and reads it back; a missing name stops before 立即投稿. Success is 投稿成功 / 审核中, with a BV URL or identity unconfirmed. Bilibili has no private visibility on web upload: approved submissions go public. Use when the user asks to post to B站, 哔哩哔哩, B站投稿, or publish a video to bilibili.
version: "0.1.0"
license: MIT
homepage: https://github.com/terryso/ego-skills/tree/main/skills/bilibili-video
metadata:
  version: "0.1.0"
  requires:
    bins:
      - ego-browser
      - node
  ego:
    min_skill_guide: "2.1.0"

---

# bilibili-video

用 Ego Lite 会话把**本地视频**投到 [B 站创作中心](https://member.bilibili.com)。终点是**「投稿成功」且稿件进入审核**。

Publish a **local video file** to the Bilibili creator platform. The endpoint is 投稿成功 with the work under review. No download step.

## 先装 Ego

先装 **Ego Lite**,保证 `ego-browser` 在 `PATH`。非交互 shell 找不到时,再试 `~/.local/bin/ego-browser`。仍然缺失则 soft-fail(退出码 `2`),**不要**改用 Playwright、Puppeteer 或云端浏览器。

Install **Ego Lite** and put `ego-browser` on `PATH`. If missing, soft-fail with exit `2`. Do not switch stacks.

## 每次投稿前:登录闸门(必做)

```bash
node skills/bilibili-video/scripts/check-login.mjs
# 需要把窗口留给人扫码时:
node skills/bilibili-video/scripts/check-login.mjs --keep
```

| 退出码 | 含义 | Agent 做什么 |
|--------|------|----------------|
| `0` | 已登录 | 继续 |
| `2` | 未登录 / 无 ego-browser | 展示 `how_to_login`,**停**,请人在 Ego 扫码后重跑 |
| `1` | 其它错误 | 报告 JSON `error`,不要假装已投稿 |

## CLI

`ego-browser nodejs` 不继承 shell 环境变量,也不转发 argv,所以由 `publish.mjs` 把 JSON 写到 `/tmp` 再交给 ego。**参数全部走 flag**(key=value 也支持):

```bash
# 仓库根目录。没有 --yes 且没有 --stop-before-submit:只做本地校验并打印计划,exit 3,不打开浏览器
# 验收入口:真实上传并校验,但在「立即投稿」之前退出。和 --yes 同时出现也不会投稿
node skills/bilibili-video/scripts/publish.mjs \
  --video /absolute/path/to/video.mp4 \
  --title "标题" \
  --cover-4x3 /absolute/path/to/cover-4x3.png \
  --cover-16x9 /absolute/path/to/cover-16x9.png \
  --type "科技数码" \
  --stop-before-submit
node skills/bilibili-video/scripts/publish.mjs \
  --video /absolute/path/to/video.mp4 \
  --title "标题(≤80字)" \
  --desc "简介(≤2000字),话题写在正文里"

# 真实投稿:封面两张分开传(4:3 首页推荐 + 16:9 个人空间)
node skills/bilibili-video/scripts/publish.mjs \
  --video /absolute/path/to/video.mp4 \
  --title "标题" \
  --desc "简介" \
  --cover-4x3 /absolute/path/to/cover-4x3.png \
  --cover-16x9 /absolute/path/to/cover-16x9.png \
  --tags "标签1,标签2" \
  --declare ai \
  --yes

# 中断后用 spaceId 续跑,--keep 保留页面
node skills/bilibili-video/scripts/publish.mjs --video ... --title ... --yes --space-id 12
```

| 退出码 | 含义 |
|--------|------|
| `0` | 投稿成功,stdout 有 `{"ok":true,"status":"审核中","bvid","url","identity"}`;读不到稿件号时 `identity` 为 `unconfirmed`,`url` 为 null |
| `1` | 参数或流程错误(JSON 在 stderr) |
| `2` | 需要登录(脚本内遇登录墙会 `handOff()`) |
| `0` | `--stop-before-submit`:表单已填完并回读,`submitted` 为 false,没有点「立即投稿」。和 `--yes` 同时使用也停 |
| `3` | 没有 `--yes` 也没有 `--stop-before-submit` 的计划模式,未上传未投稿 |

## 硬性限制(先本地校验,超了直接 exit 1)

- 视频 ≤ 16G,推荐 MP4/MOV/MKV;竖屏横屏都可以传
- 标题必填 ≤ 80 字;简介 ≤ 2000 字;标签 ≤ 10 个(逗号分隔)
- 封面:png/jpg,4:3 与 16:9 **必须成对传入**(±8% 容差本地校验;比例差太多 B 站会裁切,不如自己给对的)

## 分区(分区必填)

投稿表单的分区是**必填**。不传 `--type` 时,沿用表单记住的分区并在结果里回读这个名字;分区为空则 exit 1。

传了 `--type` 时,打开 `.video-human-type` 的人选列表并点对应项,再读 chip。列表里没有这个名字,或点完回读不一致,就在「立即投稿」之前退出,不会留着旧分区继续投。

## 创作声明(必填,不传默认「内容无需标注」)

`--declare` 对应表单的**必填**创作声明下拉;为空时点「立即投稿」会被表单校验拦下(下拉被弹开,投稿不发生)。取值:

| flag 值 | 表单选项 |
|---------|----------|
| `none`(默认) | 内容无需标注 |
| `ai` | 含AI生成内容 |
| `fiction` | 含虚构演绎内容 |
| `marketing` | 内容含营销信息 |
| `opinion` | 个人观点,仅供参考 |
| `repost` | 内容为转载 |
| `original` | 内容为自制:未经作者允许,禁止转载 |

**Agent 必须向用户确认内容性质**:AI 生成(AI 配音/AI 生成画面等)要传 `--declare ai`,这是平台合规要求;转载内容传 `--declare repost`。不要默默用默认值绕过这个决定。

## 发布脚本在做什么

1. 打开投稿页前用 CDP 预授通知权限,避免系统弹窗打断 agent。
2. 登录闸门:shadow-DOM 文本里没有创作中心元素、或 URL 跳到 passport 登录页,exit 2 + `handOff()`。
3. 坐标点上传区 → `waitForFileChooser` → 交视频文件,轮询「上传完成 / 更换视频」(最长 15 分钟)。
4. 写标题(原生 setter + input 事件)并回读校验;清掉表单预填标签后逐个回车添加 `--tags` 并核对 chip;简介写入 Quill 编辑器并回读校验。
5. 封面:点「添加封面」→ 读 `.sync-checkbox-wrapper` 里可见勾选,连续两次未勾选后才上传。4:3 传「首页推荐」槽、16:9 传「个人空间」槽,每次选文件前再确认勾选是关的。成功回执里两槽各自带 `slot`、`width`、`height` 和 `match`。传完第二张再复核 4:3 槽仍是原来那张图,才点「完成」;表单 `.cover-img` 出现背景图才算落位。任何一步不确认就不投稿。
6. 分区按上面的规则回读确认 → 点「立即投稿」→ 轮询「投稿成功/审核中」。成功页文本里有 BV 号就写入 `url`;没有就按标题轮询创作中心稿件接口(进行中/已发布),直到读到或超时,最后再只读扫稿件管理。仍然没有则 `identity` 为 `unconfirmed`。

成功时默认 `finish({ keep: [] })`;`--keep` 才保留页面。

## B 站特有,必须告知用户

- **网页投稿没有「仅自己可见」**:投稿即进审核,过审后公开。
- 网页封面是 4:3 与 16:9 两个独立槽位。「双比例同步改动」开着时,上传 16:9 会把 4:3 换成同一张图。技能读勾选状态,确认关掉之后才选文件。
- 上传中的稿件在「内容管理 → 稿件管理」里能看到状态(审核中/已通过/未通过)。

## 避坑

完整清单在 `references/pitfalls.md`,选择器细节在 `references/selectors.md`。发布前先 login-check;exit 2 必须停。

## 手动兜底

`post-video.mjs` 报错后,JSON 里的 `spaceId` 可以回到原 space 排查,不要另开 space:

```bash
ego-browser nodejs <<'EOF'
const task = await taskSpace(12);
const page = task.page("p1");
console.log({ url: await page.url() });
EOF
```

把 `12` 换成实际 `spaceId`。

## 测试

```bash
npm test
```

单元测试不访问 bilibili.com;真实投稿冒烟用一张小视频 + 两张测试封面人工触发。
