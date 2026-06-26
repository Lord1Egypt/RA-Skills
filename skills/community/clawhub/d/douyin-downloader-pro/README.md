# douyin-downloader

抖音视频/图集（图片）下载 skill。一次解析、自动判别视频或图集、按作品标题命名。

## 安装

把整个 `douyin-downloader/` 目录放到任一位置：

- 用户级（所有项目可用）：`~/.workbuddy/skills/douyin-downloader/`
- 项目级（仅当前项目）：`<project>/.workbuddy/skills/douyin-downloader/`

依赖：

```bash
pip install requests
```

Python 3.9+ 即可。

## 快速使用

```bash
# 视频
python3 scripts/douyin_dl.py "https://v.douyin.com/abcdef/"

# 整段分享口令（用引号包起来）
python3 scripts/douyin_dl.py "7.99 复制打开抖音，看看【XXX】https://v.douyin.com/abcdef/"

# 图集，集中下载到一个目录
python3 scripts/douyin_dl.py "https://www.douyin.com/note/7412345678901234567" -o ./out

# 图集打包为 zip
python3 scripts/douyin_dl.py "<分享文本>" -o ./out --zip
```

输出：

- 视频：`<output>/<标题>_<aweme_id>.mp4`
- 图集：`<output>/<标题>_<aweme_id>/01.jpg ... NN.jpg`
- 图集（--zip）：`<output>/<标题>_<aweme_id>.zip`

## 实现要点

1. 用正则从分享文本中提取链接（短链 / pc 网页 url / iesdouyin share url）。
2. requests 跟随重定向得到最终 url，提取 `aweme_id`。
3. 请求 `https://www.iesdouyin.com/share/{video|note}/{aweme_id}/`，取出 `<script id="RENDER_DATA">` 里的 URL-encoded JSON。
4. 递归找出 `aweme_detail`，根据 `images` 是否存在分流：
   - 有 `images`：图集，逐张下载，命名 `01.jpg / 02.jpg / ...`。
   - 否则：视频，下载 `video.play_addr.url_list[0]`。
5. 文件名用 `desc`（作品标题）做安全化处理，最长 80 字符。

## 常见问题

- **解析失败 / 拿不到 RENDER_DATA**：极可能是 IP 被风控。在 `scripts/douyin_dl.py` 顶部 `EXTRA_HEADERS` 写入浏览器登录后的 Cookie 即可。
- **图集只下了几张**：查看日志 `[NN] 全部 url 都失败`；可能是单张图被 CDN 拒绝，重试或换网络即可。
- **下载下来的视频带水印**：本工具按需保留原始带水印版本；如要无水印需要使用 `playApi`/wrap 域名替换的方案，本工具未做。
