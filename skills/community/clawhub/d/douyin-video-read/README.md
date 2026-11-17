# douyin-video-read

读取抖音（Douyin）视频内容的 Agent Skill。两级能力：

| 级别 | 能拿到 | 耗时 | 依赖 |
| --- | --- | --- | --- |
| **L1 摘要** | 标题、作者、发布时间、互动数据、**抖音官方 AI 章节要点**（带时间戳的逐章摘要）、评论、推荐流 | 30–60 秒 | 只要浏览器 |
| **L2 全文** | 画面关键帧 + **逐句口播讲稿**（画面硬字幕 OCR，带时间戳） | 3–5 分钟 | + OCR 后端 |

An Agent Skill for reading Douyin (Chinese TikTok) video content. Two levels:
**L1** = metadata + the platform's own AI-generated chapter summary.
**L2** = key frames + a full timestamped transcript from burnt-in subtitles.

---

## 为什么不用现成方案

调研过生态里所有能找到的抖音 skill / 工具，**全部失效**：

- **yt-dlp 的抖音提取器已坏**：它调用 `aweme/v1/web/aweme/detail/`，抖音现在要求 `a_bogus`
  签名（yt-dlp 源码里写着 `TODO: Run verification challenge code to generate signature cookies`），
  因此**加任何 cookie 都会失败**，报 `Fresh cookies (not necessarily logged in) are needed`。
  自己伪造匿名 `ttwid`（`ttwid.bytedance.com/ttwid/union/register/` + callback）同样无效。
- **不能解析 iesdouyin 分享页**：`window._ROUTER_DATA` 还在，但
  `loaderData["video_(id)/page"]` 里**已没有 `videoInfoRes` 字段**（抖音改版），
  基于它的方案（如 `yzfly/douyin-mcp-server` 的 douyin-video skill）全部失效。
- **不能靠捕获 `.mp4` 请求下载视频**：播放器会预加载推荐流里的其他视频，
  网络请求里抓到的 `*.douyinvod.com` 很可能**不是目标视频**（实测下到一个 270MB 的隔壁游戏视频）。

## 本项目的做法

**L1**：真实浏览器渲染后，直接读 `document.body.innerText`。
抖音页面文本里含官方 AI 生成的「章节要点」——等于一份现成的逐讲大纲，比下载视频做 ASR 都快。

**L2**：不下载视频，而是让浏览器播放视频后用 `canvas.drawImage(video)` **在任意时间点取帧**。
绕开了预加载污染，还能按精确时间轴采样。

---

## 安装

### 1. 装依赖

```bash
pip install playwright requests Pillow
python -m playwright install chromium   # 或跳过：直接用系统已装的 Edge / Chrome
```

OCR 后端三选一：

```bash
# A. Windows 内置 OCR（推荐，离线免费）
pip install winrt-runtime winrt-Windows.Media.Ocr winrt-Windows.Globalization \
            winrt-Windows.Graphics.Imaging winrt-Windows.Storage \
            winrt-Windows.Storage.Streams winrt-Windows.Foundation \
            winrt-Windows.Foundation.Collections

# B. 跨平台 OCR
#    macOS: brew install tesseract tesseract-lang
#    Ubuntu: sudo apt install tesseract-ocr tesseract-ocr-chi-sim
#    pip install pytesseract   # 可选，装了会自动优先用

# C. 什么都不装 —— 用 --backend none，把裁好的字幕图交给具备视觉能力的 Agent 自己读
```

### 2. 装 skill

```bash
# WorkBuddy / Claude Code（用户级，所有项目可用）
git clone https://github.com/<your-name>/douyin-video-read.git \
  ~/.workbuddy/skills/douyin-video-read

# Claude Code 项目级
git clone https://github.com/<your-name>/douyin-video-read.git \
  .claude/skills/douyin-video-read

# Codex / 其他支持 SKILL.md 的 agent
git clone https://github.com/<your-name>/douyin-video-read.git \
  <你的 skills 目录>/douyin-video-read
```

只要 agent 支持读 `SKILL.md` 的约定（`name` + `description` frontmatter），就能自动发现本 skill。

---

## 用法

```bash
SK=<skill 目录>/scripts

# L1：元信息 + 官方章节要点
python "$SK/read_douyin.py" "https://v.douyin.com/xxxx/"
python "$SK/read_douyin.py" "https://v.douyin.com/xxxx/" --json

# L2a：逐帧截图（不下载视频）
python "$SK/capture_frames.py" "https://v.douyin.com/xxxx/" --out ./out --interval 1.5

# L2b：裁字幕 + OCR + 生成讲稿
python "$SK/ocr_subtitles.py" --dir ./out

# 没有 OCR 引擎？交给 Agent 读图
python "$SK/ocr_subtitles.py" --dir ./out --backend none   # 产出 manifest.md
```

### 常用参数

| 参数 | 说明 |
| --- | --- |
| `--interval 1.5` | 采样间隔。字幕约 2–3 秒换一次，1.5 秒能保证不漏；长视频可放宽到 2–3 秒 |
| `--browser auto` | 浏览器选择：`auto`(默认，依次试 Edge/Chrome/Chromium) \| `msedge` \| `chrome` \| `chromium` |
| `--headed` | 显示浏览器窗口，用于站点有反爬或需要人工观察时 |
| `--selector video` | 视频元素选择器，适配非标准页面 |
| `--backend none` | 不做 OCR，产出图片清单交给多模态 Agent 读 |
| `--variants n` | 只输出原图（不做反色变体），速度翻倍 |
| `--top 0.22 --bottom 0.24` | 顶部标题条 / 底部字幕的裁剪比例，按实际版式调 |

### 输出文件

```
<out>/
├── frames/*.jpg        关键帧（文件名 = 毫秒时间戳）
├── frames.json         时间轴、时长、分辨率、所用浏览器
├── subtitles/*.jpg     裁好的字幕条（_n 原图 / _i 反色）
├── ocr_raw.txt         OCR 原始输出
├── transcript.md       讲稿（带时间戳）
├── transcript.json     结构化分段
└── manifest.md         backend=none 时的读图清单
```

---

## 通用性

`capture_frames.py` 与 `ocr_subtitles.py` **不限于抖音**——任何页面只要有一个 HTML5 `<video>`
元素就能用（传任意 URL 即可）。抖音只是内置了一个适配层（短链解析 + 登录弹窗处理）。

平台支持：

| 平台 | L1 | L2 |
| --- | --- | --- |
| Windows | ✅ winrt / tesseract / none | ✅ |
| macOS | ✅（正文提取） | ✅ tesseract / none |
| Linux | ✅（正文提取） | ✅ tesseract / none |

---

## 已知限制

- **L1 依赖抖音的官方 AI 章节要点**：冷门或刚发布的视频可能没有，只能拿到标题和描述。
- **OCR 形近字误差无法靠预处理消除**：实测 `autocontrast` / 二值化 / `SHARPEN` 对识别率**没有提升**，
  原图最好。误差来自艺术字体的形近字（标准→标推、解决→解块、核心→核弋），需人工校正。
- **Windows OCR 会在中文字间插空格**，比对前要去空白（脚本已处理）。
- 未登录状态可读标题 / 章节要点 / 评论 / 推荐；不能点赞、发评论。
- 部分视频有插播广告画面，OCR 结果会是噪声，需要人工剔除。

---

## License

MIT
