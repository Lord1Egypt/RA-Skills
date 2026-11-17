# 经验总结

## Markdown 图文上传

统一调用 `upload-markdown-to-lexiang`。公共上传器负责：

- 按本地图片切分 Markdown，并按原文顺序交替写入文字和图片。
- 每张图片独立申请上传会话并创建 image block。
- 长正文分段、页面写入和富元素渲染全部由 uploader 处理。
- 上传前检查全部图片，上传后核对标题、正文锚点、图片和公式。

调用方必须先下载重要外链图片，并保持标准 Markdown 相对路径。

## 内容加工

- 非中文原文必须全文保留并逐段翻译，不能摘要替代。
- 标题使用 `English / 中文` 单行格式。
- 将标准工作包交给 `trans-doc-to-md` Prepared Markdown Package 模式。
- 本 Skill 和当前 Agent 不直接实现翻译。
- 翻译后的覆盖上传仍调用公共上传器 `--entry-id`。

## YouTube

- 使用较新的 `yt-dlp`，YouTube 反爬变化时优先更新工具。
- DASH 分片出现 403 时优先选择 HLS。
- Whisper 输入预处理为 16kHz、单声道 WAV。
- 相邻短 segment 按时间间隔和标点合并为自然段。
- Markdown 文字稿上传为 page；视频使用 VOD 文件上传。

## 播客

- 小宇宙等页面通常可通过 generic extractor 获取音频直链。
- 中文 Whisper 输出可能偏繁体，转录后用 OpenCC `t2s` 统一简体。
- 中文播客无需翻译，但必须保留 Show Notes 和章节时间线。
- Markdown 文字稿调用公共上传器；音频继续使用 VOD 专用脚本。

## 微信公众号

- WebFetch 无法保证懒加载图片完整，图文必须使用 `fetch_article.py`。
- 优先读取 `data-src`，慢速滚动触发懒加载。
- 图片下载请求需要正确 Referer。
- Markdown 转换不能 strip `img`，否则会丢失图片位置。

## CDP 登录态

- 日常 Chrome、CDP Chrome、Testing Chrome 是三个独立实例。
- 付费内容只复用 9222 端口的持久化 CDP Profile。
- CDP 连接失败时禁止静默回退到无登录态 Testing Chrome。
