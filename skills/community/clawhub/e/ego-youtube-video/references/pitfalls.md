# 避坑（YouTube Studio）

Studio 上传向导是 Polymer 组件，标题和简介的 `#textbox` 在 **open shadow** 里。脚本用 `queryDeep` 穿过 shadow，再用 `execCommand('insertText')` 写入并回读。Agent 重试时不要另写一套填表。

1. **先装 Ego Lite，`ego-browser` 要在 PATH 上。** 缺失是 soft-fail（退出码 2），不要硬调浏览器。
2. **每次发布前先 `check-login`。** 退出码 2 必须停。在 Ego 里登录 YouTube 效果最好，把 `login_tip` 告诉用户。
3. **文档标题 “YouTube Studio” 不是登录成功。** 登录墙在 `accounts.google.com` 或 “Choose an account / Sign in to YouTube”。空白页只重画一次。
4. **先布防文件选择器，再点选择文件。** 视频按钮是 `#select-files-button`。点击会弹出原生文件框。不要用脚本去下载视频，调用方给什么本地文件就传什么。
5. **创建菜单再进上传。** 先点 `#create-icon`，再点 `test-id="upload-beta"` 或正文恰好是 “Upload videos” / “上传视频” 的菜单项。已经停在选择文件页就不要再点创建。
6. **标题在 `#title-textarea` 的 shadow `#textbox` 里。** Studio 会先填文件名。写完回读必须和传入标题一致，否则当失败。简介同理，但简介允许为空。
7. **不选观众，Next 会一直禁用。** 默认点 `VIDEO_MADE_FOR_KIDS_NOT_MFK`（不是面向儿童）。只有调用方明确要求才点 `VIDEO_MADE_FOR_KIDS_MFK`。
8. **标签在 “Show more / 显示更多”（`#toggle-button`）下面。** 输入框是 `#tags-container` 里的 `#text-input`。每个标签回车提交。没看到 chip 或正文里的标签就是失败，不要当成功。
9. **缩略图走文件选择器。** 先等 chooser，再点 `#file-loader`。点不到再试 “Upload thumbnail” / “上传缩略图”。不要把图片 base64 塞进页面。
10. **公开范围默认 Private。** 单选的 `name` 是 `PRIVATE` / `UNLISTED` / `PUBLIC`。private 和 unlisted 的最后一颗按钮是 Save；public 才是 Publish。调用方没说 public 就不要选公开。
11. **成功不要等 HD 处理完。** 点完 Save/Publish 后，读到 11 位视频 ID（`youtu.be`、`watch?v=` 或 `/video/<id>`）以及处理状态即可。状态可以是 Uploading、Upload complete、Processing、Checks complete、Saved、Published。
12. **上传上限和版权弹层不要替用户点掉。** 正文出现 daily upload limit / 上传次数已达上限就失败退出。不要自动勾选版权声明。
13. **ego 内嵌 Node 不继承 shell 环境变量。** 参数由 `publish.sh` 写入 `/tmp/youtube-video-publish.json`。不要裸跑 `publish.js`，也不要指望 `VAR=x ego-browser nodejs` 能读到 `VAR`。
14. **默认关掉 space。** 成功、失败、未登录（没带 `--keep`）都 `finish({ keep: [] })`。只有人还要看页面时才传 `--keep`。
15. **中英文界面都要认。** 菜单和按钮同时匹配英文和中文文案。选择器优先用稳定的 id 和 `name`，不要只靠一种语言的坐标。
