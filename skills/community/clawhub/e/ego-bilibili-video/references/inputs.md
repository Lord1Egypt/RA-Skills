# 输入 / Inputs

调用方提供本地文件与文案;本技能**不**绑定任何业务目录,也**不**下载视频。

| flag | 必填 | 限制 | 说明 |
|------|------|------|------|
| `--video` | ✅ | ≤16G,MP4/MOV/MKV 等 | 本地绝对路径;横屏竖屏都可以 |
| `--title` | ✅ | ≤80 字 | B 站超长会拒 |
| `--desc` | – | ≤2000 字 | 简介;话题写在正文,如 `描述 #话题` |
| `--cover-4x3` | –* | png/jpg,≈4:3 | 首页推荐封面槽 |
| `--cover-16x9` | –* | png/jpg,≈16:9 | 个人空间封面槽 |
| `--tags` | – | ≤10 个,逗号分隔 | 每个标签 ≤20 字 |
| `--yes` | – | flag | 真实点「立即投稿」。不传且没有 `--stop-before-submit`:只做本地校验,exit 3 |
| `--stop-before-submit` | – | flag | 上传并校验标题、简介、标签、分区、双封面后退出。即使同时有 `--yes` 也不点「立即投稿」 |
| `--keep` | – | flag | 保留页面不 finish |
| `--space-id` | – | 正整数 | 回到已有 space 续跑 |
| `--type` | – | 字符串 | 从人选列表点选并回读;不在列表里就停止,不沿用旧分区。不传则使用表单记住的分区 |
| `--declare` | – | 枚举,默认 `none` | 创作声明(必填项):`none`/`ai`/`fiction`/`marketing`/`opinion`/`repost`/`original`。AI 配音、AI 生成画面要传 `ai` |

\* 封面要么两张都传,要么都不传;比例容差 ±8%,超出本地直接 exit 1(B 站自己会裁切,不如给对的)。

## 封面从哪来

技能不管素材来源。常见做法:从视频抽帧或设计稿导出两个比例各一张;只有一张 3:4 竖版图时,可先用 `sips -c <h> <w>` 居中裁出 4:3 与 16:9 再传入(注意竖版裁横版两侧信息损失大,建议专用封面稿)。

## 文件传递机制

`ego-browser nodejs` 不继承 shell 环境变量、不转发 argv。`publish.mjs` 先把 JSON 写到 `/tmp/bilibili-video-publish.json`,`post-video.mjs`(在 ego 内运行)再读它。视频与封面文件通过 `waitForFileChooser` + `chooser.setFiles()` 交给页面,路径必须是绝对路径。
