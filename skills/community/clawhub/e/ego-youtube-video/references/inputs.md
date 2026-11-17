# 调用方提供的输入（通用）

本技能**不绑定**任何产品目录，也**不下载**视频（没有 yt-dlp）。调用方自己准备本地文件。发布前确认调用方有权发布该文件，并且真的要传到这个 YouTube 频道。

| 字段 | 必填 | 说明 |
|------|------|------|
| `video` | 是 | 本机视频路径，例如 `/absolute/path/to/video.mp4`。支持 mp4、mov、webm、mkv、m4v、avi 等常见容器 |
| `title` | 是 | 视频标题，最多 100 个字符。写完要回读 |
| `description` | 否 | 简介，最多 5000 个字符。不传就是空简介 |
| `tags` | 否 | 逗号分隔，例如 `one,two`。总长度不超过 500。不传就不填标签 |
| `visibility` | 否 | `private`（默认）、`unlisted`、`public`。没明确说就用 private，不要擅自公开 |
| `thumbnail` | 否 | 本机图片路径，jpg / jpeg / png / webp / gif。不传就用 Studio 自动封面 |
| `madeForKids` | 否 | 默认 `no`。只有调用方明确说面向儿童才传 `yes` |
| `spaceId` | 否 | 登录 handOff 或中断后续跑时传入。不要为了重试新开一个 space |
| `keep` | 否 | 加上 `--keep` 才保留浏览器页。默认关闭：`finish({ keep: [] })` |

系列栏目（播客、课程等）应在**自己的发布清单**里给出上表字段，不要把产品路径写进本技能。

公开范围默认 private，是为了避免脚本把视频直接公开。调用方要公开时必须自己传 `--visibility public`。
