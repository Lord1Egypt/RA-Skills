# 输入

调用方提供绝对路径和文案。本技能不下载视频，也不写死任何产品目录。

| 参数 | 必填 | 说明 |
|------|------|------|
| `--video` | 视频笔记必填 | 本地视频绝对路径。扩展名：`.mp4 .mov .flv .f4v .mkv .rm .rmvb .m4v .mpg .mpeg .ts`。与 `--images` 互斥 |
| `--images` | 图文笔记必填 | 逗号分隔的图片绝对路径，1–18 张，`.jpg .jpeg .png .webp`，单张最大 32MB。与 `--video` 互斥。第一张图就是封面 |
| `--title` | 发布时必填 | 笔记标题。界面建议大约 20 个字，超长只警告 |
| `--desc` | 发布时必填 | 正文 |
| `--topics` | 否 | 例如 `#话题1 #话题2`，会空一行后接到正文后面 |
| `--strip-links` | 否 | 删掉标题、正文、话题里的链接，以及同一行上悬空的「项目地址：」「链接：」。不加这个参数时，发现链接就退出码 `4` |
| `--cover` | 否 | `.jpg` `.jpeg` `.png` 绝对路径，例如 `cover-3x4.png`。仅视频笔记可用：有 `--yes` 时走「编辑封面」弹窗换主封面；预览没变就不点发布。没有 `--yes` 只写进计划，不上传。图文笔记传了会校验失败 |
| `--expect-account` | 否 | 创作者页眉昵称。不一致则退出码 `2`，不点发布 |
| `--yes` | 真正发布时必填 | 没有它只打印计划，退出码 `3`，不上传 |
| `--json` | 否 | 成功时也打印完整 JSON |
| `--keep` | 否 | 保留页面。默认 `finish({ keep: [] })` |
| `--task-name` | 否 | 任务空间名。建议以 `xiaohongshu-ego` 开头，cleanup 才能按前缀关掉 |
| `--note-id` | 仅 `edit-cover` | explore URL 里的笔记 id |

`--video` 和 `--images` 必须二选一。视频笔记不传 `--cover` 时，计划里的 `cover` 是 `null`，`cover_mode` 是 `platform-default-first-frame`。技能不会另找一张图。图文笔记的 `cover_mode` 是 `first-image`。

`edit-cover.mjs` 必须带 `--note-id` 和 `--cover`。它是尽力而为，见 `publish-flow.md`。
