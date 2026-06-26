---
name: douyin-downloader
description: 下载抖音视频或图集（图片）。当用户提供抖音 App 分享口令、v.douyin.com 短链、或 douyin.com 视频/图文页面 URL，并希望下载视频文件或图集中的所有图片时使用本 skill。支持自动识别图集 vs 视频；图集会把所有图片下载到一个以作品标题命名的目录中，可选打包为 zip。视频按原始（带水印）地址下载。
agent_created: true
---

# 抖音视频/图集下载器（douyin-downloader）

## 适用场景（触发条件）

当用户的请求**同时满足**以下两点时使用本 skill：

1. 输入中包含以下任一形式的抖音内容标识：
   - 抖音 App 复制的分享口令文本（包含 `v.douyin.com/xxx/` 短链 + 一段口令）
   - `https://v.douyin.com/xxx/` 短链
   - `https://www.douyin.com/video/<id>` 或 `https://www.douyin.com/note/<id>` 网页 URL
   - `https://www.iesdouyin.com/share/video|note/<id>/` 分享页 URL
2. 用户希望**下载/保存**视频或图集到本地（包含「下载」「保存」「拿到」「批量保存」「下载图片」等意图）。

## 能力概述

- **视频**：解析 aweme_detail，下载默认 CDN 上的视频文件（**原始带水印**版本，命名为 `<标题>_<aweme_id>.mp4`）。
- **图集**：识别图集（note）类型作品，把所有图片下载到 `<标题>_<aweme_id>/` 目录（命名为 `01.jpg`、`02.jpg` …）。可选 `--zip` 参数将该目录打包为 `<标题>_<aweme_id>.zip`。
- **输入容错**：自动从分享口令文本里提取链接，跟随短链重定向取出 `aweme_id`。
- **接口降级**：依次尝试 `video` 和 `note` 两种 share 路径解析，避免类型判错导致空数据。

## 用法

脚本路径：`scripts/douyin_dl.py`，依赖 Python 3 与 `requests`。

```bash
# 基本用法（视频或图集都用这一个命令）
python3 scripts/douyin_dl.py "<分享文本或链接>" -o ./downloads

# 图集自动打包成 zip
python3 scripts/douyin_dl.py "<分享文本或链接>" -o ./downloads --zip

# 短链
python3 scripts/douyin_dl.py "https://v.douyin.com/xxxxxx/"

# 直接的 douyin.com 网页 URL
python3 scripts/douyin_dl.py "https://www.douyin.com/note/7412345678901234567"

# 抖音 App 复制的整段分享口令（带换行也可以，记得用引号包起来）
python3 scripts/douyin_dl.py "7.99 复制打开抖音，看看【XXX的作品】https://v.douyin.com/abc123/"
```

参数：

| 参数 | 说明 |
|------|------|
| `input`（位置参数） | 必填。分享文本 / 短链 / 完整 URL，任选其一。 |
| `-o, --output` | 输出目录，默认 `./downloads`。 |
| `--zip` | 仅对图集有效：把图片目录打包为同名 zip 文件。 |

## 工作流（执行步骤）

1. 用 `Bash` 调用 `python3 scripts/douyin_dl.py "<input>" -o <dir>`。
2. 检查脚本输出：脚本以 `[douyin] ...` 前缀打印进度日志，结尾会汇报"完成，输出 N 个文件"或失败原因。
3. 失败时按以下顺序排查：
   - 提示"未识别到链接"：检查输入文本里是否真的包含 `v.douyin.com` 或 `douyin.com` 链接。
   - 提示"解析失败"或返回空 detail：抖音可能对该 IP 有风控/需要登录，可让用户在浏览器登录后导出 cookie，再写进脚本里的 headers（脚本预留了 `EXTRA_HEADERS` 入口）。
   - 视频可下载但图集报"未找到图片"：少数图集的 `images` 字段在另一个嵌套位置，脚本会自动递归查找；如仍失败，把整段 RENDER_DATA dump 出来人工定位字段。

## 已知限制

- 抖音 web 接口经常变动；脚本依赖 `iesdouyin.com/share` 页面里的 `RENDER_DATA` JSON。如果某天该接口变更，需要更新解析逻辑。
- 不支持登录后才能查看的私密作品。
- 视频是 CDN 上的**原始带水印**版本（按用户需求保留水印）。
- 不支持从主页批量抓取所有作品（仅单作品下载）。
- 长视频（合集）只下载第一段对应的 `play_addr`。

## 注意事项（合规）

- 仅限下载用户**有权访问/有合法用途**的内容；不要用于规模化采集、商业再分发或侵犯创作者权益。
- 抖音 ToS 对自动化访问有限制；本脚本面向个人留存场景。
