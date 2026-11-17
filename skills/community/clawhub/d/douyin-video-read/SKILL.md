---
name: douyin-video-read
description: 读取抖音视频的内容——元信息、官方 AI 章节要点，以及通过逐帧截图 + 字幕 OCR 得到完整口播讲稿。用户分享抖音链接（v.douyin.com / douyin.com/video/xxx）并希望了解视频讲了什么、提取文案、拿到文字稿时使用。触发词：抖音链接、抖音视频、这个视频讲了什么、提取视频文案、抖音视频转文字、视频字幕、看看这个视频、视频内容。
agent_created: true
---

# 读取抖音视频内容

两级能力，按需选择：

| 级别 | 能拿到 | 耗时 | 用什么 |
| --- | --- | --- | --- |
| **L1 摘要** | 标题、作者、发布时间、互动数据、**抖音官方 AI 章节要点**（带时间戳的逐章摘要）、评论、推荐流 | 约 30-60 秒 | `scripts/read_douyin.py` |
| **L2 全文** | 画面关键帧 + **逐句口播讲稿**（来自画面硬字幕 OCR，带时间戳） | 约 3-5 分钟 | `scripts/capture_frames.py` + `scripts/ocr_subtitles.py` |

**先用 L1**。用户只是问"这视频讲了什么"，L1 的官方章节要点就够，没必要跑 L2。只有需要逐句原文、要引用具体表述、或视频没有 AI 章节要点时，才上 L2。

## 核心原理

**L1**：抖音视频页渲染后，`document.body.innerText` 里含抖音**官方 AI 生成的分章要点**。直接读文本，不解析 DOM 选择器（类名被混淆且频繁变更）。

**L2**：不下载视频文件，而是让真实浏览器播放视频，再用 `canvas.drawImage(video)` 在任意时间点取帧 —— 可以精确按时间轴采样，且完全避开预加载污染。这类知识讲解视频通常是**双层文字**：顶部章节标题条 + 底部口播字幕，裁切时两块都要。

## 环境准备

```bash
pip install playwright requests Pillow
python -m playwright install chromium   # 可跳过：会优先复用系统已装的 Edge / Chrome
```

OCR 后端三选一（脚本 `auto` 会按 winrt → tesseract → none 自动挑）：

```bash
# A. Windows 内置 OCR（推荐：离线、免费、中文好）
pip install winrt-runtime winrt-Windows.Media.Ocr winrt-Windows.Globalization \
    winrt-Windows.Graphics.Imaging winrt-Windows.Storage \
    winrt-Windows.Storage.Streams winrt-Windows.Foundation \
    winrt-Windows.Foundation.Collections
# 另需系统中文 OCR 语言包：设置 → 时间和语言 → 语言 → 中文(简体) → 语言选项 → 光学字符识别

# B. 跨平台
#   macOS:  brew install tesseract tesseract-lang
#   Ubuntu: sudo apt install tesseract-ocr tesseract-ocr-chi-sim
pip install pytesseract   # 可选，装了会自动优先走 Python 接口

# C. 都不装：用 --backend none，把裁好的字幕图交给具备视觉能力的 agent 自己读
```

- 浏览器**优先复用系统已装的 Edge / Chrome**（`--browser auto` 会依次尝试
  msedge → chrome → chromium），都没有才回落到 Playwright 自带 Chromium，省 500MB 下载。
  想强制指定用 `--browser msedge` / `--browser chrome`。

## 使用方式

本 skill 放在**用户级 skills 目录**里，任何项目、任何任务都能直接调用，与工作目录无关。

```bash
SK=<本 skill 的绝对路径>/scripts

# L1：元信息 + 官方章节要点（约 30-60 秒）
python "$SK/read_douyin.py" "<分享文本或链接>"
python "$SK/read_douyin.py" "<链接>" --json        # 结构化输出

# L2 第一步：逐帧截图（约 1-2 分钟，不下载视频）
python "$SK/capture_frames.py" "<链接>" --out "<输出目录>" --interval 1.5

# L2 第二步：裁字幕区 + OCR + 生成讲稿（约 30 秒）
python "$SK/ocr_subtitles.py" --dir "<输出目录>"

# 没有可用 OCR 引擎时：只出图，交给具备视觉能力的 agent 直接读
python "$SK/ocr_subtitles.py" --dir "<输出目录>" --backend none
```

**用装了依赖的那个解释器**——如果依赖装在虚拟环境里，就把 `python` 换成该环境的解释器路径，
或先激活环境。系统全局 Python 里通常没装 playwright / Pillow。

L2 输出目录内容：`frames/*.jpg`（关键帧）、`frames.json`（时间轴+时长）、`subtitles/*.jpg`（裁好的字幕条）、`ocr_raw.txt`（OCR 原始输出）、`transcript.md`（讲稿）、`transcript.json`（带时间戳的结构化分段）、`manifest.md`（`--backend none` 时的读图清单）

采样间隔建议 **1.5 秒**（字幕约 2-3 秒换一次，1.5 秒能保证每条至少被采到一次）。长视频可放宽到 2-3 秒省时间。

## 关键实现要点（改脚本前必读）

1. **先预热 `https://www.douyin.com/`** 拿匿名 cookie（ttwid 等），再跳视频页，成功率显著提高。
2. **必须处理登录弹窗**（「登录后免费畅享高清视频」会遮住内容）：`Escape` + 点关闭按钮（PC 布局 1600×900 下约 `x=763, y=167`），反复几轮直到 `<video>` 出现。
3. **`wait_until` 用 `domcontentloaded`**，绝不用 `networkidle`——抖音页面永不 idle，会一直挂到超时。
4. **`page.goto` 要 `try/except` 包住**：超时不致命，等 3-5 秒页面通常已渲染完，继续读文本/取帧即可。
5. **用视频时长校验是否拿到了正确视频**：`video.duration` 应与页面显示时长一致（本例 284.887s ≈ 4:45）。这是 L2 里唯一可靠的"身份校验"。
6. **OCR 需要 BGRA8 格式**，必须显式转换，否则抛异常。

## 已知的坑（都是实测踩出来的）

### 别用 yt-dlp 下抖音
yt-dlp 的抖音提取器调 `aweme/v1/web/aweme/detail/`，抖音现在要求 `a_bogus` 签名（源码里写着 `TODO: Run verification challenge code to generate signature cookies`），因此**加任何 cookie 都失败**，报 `Fresh cookies (not necessarily logged in) are needed`。自己造匿名 ttwid（`ttwid.bytedance.com/ttwid/union/register/` + callback）也无效。

### 别解析 iesdouyin 分享页
`https://www.iesdouyin.com/share/video/{id}` 的 `window._ROUTER_DATA` 还在，但 `loaderData["video_(id)/page"]` 里**已没有 `videoInfoRes` 字段**（抖音改版），基于它的解析方案（如 `yzfly/douyin-mcp-server` 的 douyin-video skill）全部失效。

### 别靠捕获 .mp4 下载视频
抖音播放器会预加载推荐流的其他视频，网络里抓到的 `*.douyinvod.com` 的 mp4 **很可能不是目标视频**（实测下到一个 270MB 的隔壁游戏视频）。用 canvas 取帧就没这个问题。

### Windows PowerShell 5.1 的编码陷阱（所以本 skill 不碰 PowerShell）
无 BOM 的 `.ps1` 会被当 ANSI/GBK 解码，脚本里**任何中文都会破坏语法**（报"缺少右 }"之类的怪异错误）。而且本环境安全策略会拦截 PowerShell 脚本执行和 `Add-Type`。
→ **OCR 走 Python 的 winrt 绑定，完全不碰 PowerShell**。如果你要写 ps1，必须保证文件是**纯 ASCII**。
（曾有一个 `ocr_batch.ps1` 实现，已删除——在这套环境里跑不起来。）

### winrt-py 的重载参数个数与文档不一致
实测（winrt 3.2.1）：
- `decoder.get_software_bitmap_async()` → 必须 **0 参**
- `decoder.get_software_bitmap_converted_async(fmt, alpha)` → 必须 **2 参**

传错个数会在**调用时同步抛** `TypeError: Invalid parameter count`（不是 await 时）。

### Windows OCR 会插入空格，且对艺术字体有形近字误差
- 中文之间会被插空格 → 必须 `normalize()` 去掉所有空白再比对/去重
- 形近字误差是**字体风格导致的，无法靠预处理消除**：实测 `autocontrast` / 二值化(140/180) / `SHARPEN` 对识别结果**没有提升**，原图就是最好的。常见错例：标准→标推、解决→解块、核心→核弋/核答
- → 生成讲稿后应人工扫一遍改掉高频形近字错误，或用上下文校正

## 相关第三方 skill（调研记录，本 skill 未依赖）

- `yzfly/douyin-mcp-server` 的 `douyin-video`：解析 iesdouyin 分享页取无水印地址 —— **已失效**
- `douyin-zh` / `douyin-dl`（SkillHub）：用 Playwright / agent-browser 取 `<video>` src 下载 —— 方法方向对，但受预加载污染影响可能下错视频
- `douyin-orchestrator`（SkillHub）：引用了三个不存在的子 skill，空壳

## 实测验证记录

| 日期 | 视频 | 结果 |
| --- | --- | --- |
| 2026-09-12 | 7681979274496183552《大厂AI Agent面试题：自驱执行架构》4:45 | L1 ✅；L2：190 帧 @1.5s → 380 次 OCR（29 秒）→ 去重 143 条字幕，覆盖全片 |
| 2026-09-12 | 7683485349322169075《Agent项目做到什么程度…》3:25 | L1 ✅；L2：137 帧 @1.5s → 去重 95 条字幕。**全程无需改代码**，证明可复用 |
| 2026-09-12 | 同上 | **跨目录调用验证**：从任意工作目录调用（脚本用绝对路径、`--out` 传相对路径），L1/L2 均正常，产出落到当前 cwd |

两个视频都是 1080p 或 720p，`video.duration` 校验与页面显示时长一致（284.887s / 205.034s）。

