---
name: douyin-transcribe-lz
description: 
  抖音视频文案提取 / 本地音视频转文字 / 语音转文本。
  当用户分享抖音链接（v.douyin.com、douyin.com、iesdouyin.com 等）并提出以下任一意图时，必须使用此技能：
  - 提取文案 / 提取文字 / 提取字幕 / 提取内容 / 提取文本
  - 视频转文字 / 视频转文本 / 语音转录 / 音频转文字
  - "这个视频说了什么" / "帮我看看这个视频讲什么" / "总结这个抖音视频"
  - 复制打开抖音的分享口令（含链接的整段分享文案）
  当用户提供本地视频或音频文件并需要转文字时，也必须使用此技能：
  - 本地视频转文字 / 本地音频转文字 / 提取本地音视频文本
  - "把这段录音转成文字" / "这个视频里说了什么" / "提取这个文件的语音内容"
  - 提取字幕 / 生成逐字稿 / 听写 / 语音识别 / 整理成文字
  支持视频格式：MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V, TS
  支持音频格式：MP3, WAV, FLAC, M4A, OGG, AAC, WMA, OPUS
  底层使用 Playwright 绕过抖音登录墙捕获视频，Whisper medium 模型本地转录中文，无需云端 API，全程本地化，隐私零风险。
agent_created: true
---

# 抖音视频文案提取 & 本地音视频转录

## 一句话定位

从抖音链接或本地媒体文件提取语音 → Whisper 本地转录为中文文本 → agent 整理纠错 → 输出可读 Markdown。

## 触发场景（满足任一即命中）

### 抖音链接场景

| 用户输入特征 | 示例 |
|-------------|------|
| 抖音链接 + "提取文案/文字/字幕/内容/文本" | "帮我把这个抖音视频的文案提取出来" |
| 抖音链接 + "转文字/转录/转文本" | "这个抖音视频转成文字" |
| 抖音链接 + "说了什么/讲什么/总结" | "这个视频说了什么？帮我看看" |
| 抖音完整分享口令文本（含链接） | "0.23 复制打开抖音，看看… https://v.douyin.com/xxx" |
| 任何含 douyin.com 域名且意图是从视频中获取文本 | "帮我听一下这个视频在讲什么" |

### 本地媒体文件场景

| 用户输入特征 | 示例 |
|-------------|------|
| 提供视频文件路径 + "转文字/转录" | "把 D:/videos/talk.mp4 转成文字" |
| 提供音频文件路径 + "转文字/转录" | "帮我听一下这个录音 /path/to/meeting.mp3" |
| 媒体文件 + "字幕" 意图 | "帮我给这个视频加字幕" / "提取视频字幕" |
| 媒体文件 + "逐字稿/听写/语音识别" 意图 | "帮我把这段录音做成逐字稿" / "语音识别这个文件" |
| "提取这个文件里的语音内容" | "这个录屏里说了什么，提取出来" |
| 任意媒体文件 + 提取文本意图 | "把这段采访音频转成文本" |

> **关键判断逻辑**：用户消息中同时出现「抖音链接/分享文本」或「本地媒体文件路径」+「获取文本内容」的意图时触发。
> 文件路径可以是绝对路径（如 `D:\videos\test.mp4`）、相对路径（如 `./recording.wav`），或 WorkBuddy 的 `@"..."` 附件引用语法。

---

## Agent 执行指引

> **跨机器迁移注意**：`.env_config.json` 由 `setup_env.py` 自动生成，包含机器特定路径。
> 迁移到新机器后必须重新运行 `python scripts/setup_env.py`，不能直接复制配置文件。

执行此技能时，agent 必须按以下顺序确定 Python 解释器：

```python
import json, os
from pathlib import Path

SKILL_DIR = Path("{skill_install_dir}")  # 运行时替换为实际安装路径
config_file = SKILL_DIR / ".env_config.json"

if config_file.exists():
    config = json.loads(config_file.read_text())
    PYTHON_EXE = config["venv_python"]    # 如 /path/to/venv/bin/python
else:
    # 环境未配置，提示用户运行 setup_env.py
    print("请先运行: python scripts/setup_env.py")
    sys.exit(1)
```

**所有脚本必须用 `PYTHON_EXE` 运行**，不得使用系统默认 `python`。

---

## 快速开始

```bash
# 1. 首次使用：配置环境（仅需一次）
python scripts/setup_env.py

# 2a. 抖音链接 → 转录
python scripts/fetch_douyin_video.py <抖音短链接>

# 2b. 抖音链接 → 转录（指定输出目录）
python scripts/fetch_douyin_video.py <抖音短链接> --output ./result

# 2c. 本地文件 → 转录
python scripts/transcribe_local.py <视频或音频文件路径>

# 2d. 本地文件 → 转录（指定输出目录）
python scripts/transcribe_local.py audio.mp3 --output ./result
```

---

## 首次配置

`scripts/setup_env.py` 自动完成以下全部步骤：

1. **检测兼容的 Python**（需要 3.10–3.12，不兼容 3.13）
2. **创建独立 venv**（位于 `{skill_dir}/venv/`）
3. **按正确顺序安装依赖**：numpy<2 → requests/imageio[ffmpeg] → playwright → openai-whisper
4. **安装 Chromium 浏览器**（Playwright 使用）
5. **验证所有包可正常导入**
6. **保存配置到 `.env_config.json`**（后续脚本自动读取）

```bash
python scripts/setup_env.py
python scripts/setup_env.py --force           # 强制重建
python scripts/setup_env.py --mirror=pypi     # 使用官方源
```

### 环境要求

| 需求 | 说明 |
|------|------|
| Python | 3.10–3.12（**3.13 不兼容**，greenlet DLL 加载失败） |
| numpy | **必须 < 2.0**（>=2.0 会触发 `ImportError: cannot load module more than once`） |
| VC++ Redist | Windows 下 torch 需要（[下载](https://aka.ms/vs/17/release/vc_redist.x64.exe)） |
| 磁盘空间 | ~4GB（torch ~2GB + Whisper 模型 ~1.4GB + Chromium ~300MB） |

### 环境验证

```bash
python scripts/verify_env.py       # 检查所有依赖
python scripts/verify_env.py --fix # 检查并自动修复
python scripts/verify_env.py --json # JSON 输出（供程序调用）
```

---

## 工作流程

### 模式 A：抖音链接 → 转录

```
抖音短链接 → Playwright 捕获视频 URL → 下载视频 → Whisper 转录 → agent 整理 → 保存 Markdown
```

### 模式 B：本地文件 → 转录

```
本地文件路径 → 格式验证 → Whisper 转录 → agent 整理 → 保存 Markdown
```

两种模式共用 `scripts/transcribe.py` 中的转录和 MD 写入逻辑。

---

### 步骤 1（仅抖音模式）：Playwright 捕获视频 URL

无需登录即可提取。Chrome 无头模式下打开短链接，首次等待 8 秒让 JS 填充 `video.src`，如果未捕获则自动增加等待时间（13 秒）重试一次。Playwright 失败时自动回退到 Douyin API 方案获取视频 URL。

> **为什么不用网络拦截？** 登录模态框覆盖时网络拦截失效，但 DOM 中 `video.src` 已就绪。

### 步骤 2（仅抖音模式）：下载视频（文件名含时间戳）

所有产物共用同一个 `YYYYMMDD_HHMMSS` 时间戳，重复运行不会覆盖。

```python
from scripts.transcribe import make_timestamp
ts = make_timestamp()  # "20260618_112500"
video_path = f"douyin_video_{ts}.mp4"
```

### 步骤 3：Whisper 转录

使用 `medium` 模型（~1.4GB，首次自动下载后缓存于 `~/.cache/whisper/`）。

脚本内置**模型缓存损坏自动修复**：若检测到模型文件不完整或加载崩溃，自动删除缓存并重新下载。

### 步骤 4：整理纠错 → 保存 Markdown

脚本**不调用外部 LLM**。转录完成后输出原始文本，由 agent 自身完成整理：

| 允许 | 禁止 |
|------|------|
| ✅ 添加标点符号 | ❌ 删减内容 |
| ✅ 修正 ASR 错字 | ❌ 改写概括 |
| ✅ 语义分段断句 | ❌ 添加总结评论 |

agent 整理完毕后调用 `scripts/transcribe.py` 中的 `write_cleaned_md()` 写入 `.md` 文件。

**Agent 调用方式**（写入整理后的 MD）：

```bash
# 抖音来源
cd <工作目录> && <venv_python> -c "
import sys
sys.path.insert(0, '<skill_dir>/scripts')
from transcribe import write_cleaned_md

md_path = write_cleaned_md(
    cleaned_text='''<整理后的文本>''',
    source='<原始短链接>',
    source_type='douyin',
    timestamp='<时间戳>',
    output_dir='<工作目录>'
)
print(f'MD saved: {md_path}')
"

# 本地文件来源
cd <工作目录> && <venv_python> -c "
import sys
sys.path.insert(0, '<skill_dir>/scripts')
from transcribe import write_cleaned_md

md_path = write_cleaned_md(
    cleaned_text='''<整理后的文本>''',
    source='<源文件名>',
    source_type='local',
    timestamp='<时间戳>',
    output_dir='<工作目录>'
)
print(f'MD saved: {md_path}')
"
```

---

## 产物清单

| 文件 | 内容 | 适用模式 |
|------|------|---------|
| `douyin_video_{ts}.mp4` | 原始视频 | 仅抖音 |
| `transcript_{ts}.txt` | Whisper 原始转录（含时间轴） | 两者 |
| `transcript_{ts}.json` | Whisper 完整 JSON 输出 | 两者 |
| `transcript_{ts}.md` | 整理后可读 Markdown | 两者 |

所有文件存放在运行脚本时的当前目录。本地文件模式**不会复制或移动**原始媒体文件，直接读取源文件。

---

## 支持的媒体格式

### 视频格式
| 格式 | 扩展名 |
|------|--------|
| MPEG-4 | `.mp4` `.m4v` |
| AVI | `.avi` |
| Matroska | `.mkv` |
| QuickTime | `.mov` |
| Windows Media | `.wmv` |
| Flash Video | `.flv` |
| WebM | `.webm` |
| MPEG-TS | `.ts` |

### 音频格式
| 格式 | 扩展名 |
|------|--------|
| MP3 | `.mp3` |
| WAV | `.wav` |
| FLAC | `.flac` |
| AAC/MP4 Audio | `.m4a` |
| Ogg Vorbis | `.ogg` |
| AAC | `.aac` |
| Windows Media Audio | `.wma` |
| Opus | `.opus` |

---

## 常见问题排查

| 症状 | 原因 | 修复 |
|------|------|------|
| `DLL load failed: c10.dll` | VC++ Redist 缺失 | 安装 [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe) |
| `ImportError: greenlet` (Python 3.13) | greenlet 与 3.13 不兼容 | 使用 Python 3.10–3.12 |
| `cannot load module more than once` | numpy >= 2 冲突 | `pip install "numpy<2" --force-reinstall` |
| Whisper SIGABRT 崩溃 | 模型缓存损坏 | 删除 `~/.cache/whisper/medium.pt` 后重试 |
| `pip install` 清华源 SSL 失败 | 清华源偶发故障 | 换用阿里云 `--mirror=aliyun` |
| 视频 URL 为空（抖音模式） | 视频需要登录或 JS 未加载 | 脚本自动先 Playwright 再 API 备用；如仍失败，确认链接有效 |
| Douyin API 返回乱码 | API 响应编码异常 | `_fix_douyin_text` 自动检测并修复 latin1 编码，无需手动干预 |
| playwright 未安装 | 本地模式不需要，抖音模式自动走 API | 无影响，脚本自动降级到 API 方案 |
| Whisper 模型下载慢 | 网络问题 | 手动下载 [medium.pt](https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt) 放到 `~/.cache/whisper/` |
| `setup_env.py` `Invalid requirement` | pip 包名被多余引号包裹 | 检查 `packages_ordered` 列表中包名无多余引号，如 `'numpy<2'` 而非 `'"numpy<2"'` |
| `setup_env.py` `AttributeError: module 'playwright' has no attribute '__version__'` | playwright 模块无 `__version__` 属性 | 使用 `getattr(playwright, '__version__', 'installed')` 安全获取 |
| `setup_env.py` `UnicodeEncodeError` 含 emoji | Windows GBK 控制台无法编码 emoji | 避免在 `print()` 中使用 emoji，改用 ASCII 标识如 `[OK]` |
| 本地文件 "不支持的格式" | 文件扩展名不在支持列表中 | 检查文件扩展名是否在支持列表中，或用 FFmpeg 转换为 MP4/MP3 |
| 本地文件 "文件不存在" | 路径错误或文件已移动 | 使用绝对路径，确认文件存在 |
| 本地模式 playwright 缺失 | 本地转录不需要 playwright | `setup_env.py` 会安装全套依赖，但 `check_dependencies(require_douyin=False)` 不检查 playwright |
| 转录速度太慢（CPU） | 无 GPU 加速 | 安装 CUDA 版 torch 加速转录 |
| 中英混合识别不准确 | Whisper 对混合语言识别较弱 | `initial_prompt` 默认已设中文提示；可自定义提示词如 `"这是一段关于AI和编程的技术视频"` |

---

## 技术要点

1. **登录墙绕过（抖音模式）**：`video.src` 由 JS 在登录模态框出现前填充，直接 DOM 查询即可捕获
2. **API 备用方案（抖音模式）**：Playwright 捕获失败时，自动回退到 Douyin web aweme detail API 获取视频 URL，双重保障
3. **Playwright 延迟导入（抖音模式）**：playwright 不再硬导入，脚本在没有 playwright 时仍可运行（自动走 API 路径）
4. **Playwright 重试机制（抖音模式）**：首次捕获等待 8 秒，失败后自动增加等待时间（13 秒）重试一次
5. **CDN URL 有效期（抖音模式）**：抖音签名 URL（`v26-web.douyinvod.com/...`）有效约 24 小时，捕获后立即下载
6. **Douyin API 编码修复**：智能检测 API 返回的 latin1 编码问题，仅在确实存在乱码时才做二次解码，不破坏正常 UTF-8 文本
7. **video ID 多格式提取**：支持 `/video/`、`/note/`（图文笔记）、`/modal/`、`/share/video/`、`?modal_id=` 五种 URL 格式
8. **本地文件零拷贝**：`transcribe_local.py` 直接从源文件路径读取，不复制文件，节省磁盘空间
9. **模型选择**：硬编码 `medium`，中文最佳性价比（准确率与 `large` 差距小而速度快一倍）
10. **FFmpeg 来源**：`imageio[ffmpeg]` 自动提供，无需系统安装
11. **环境隔离**：所有依赖安装在 skill 目录下的独立 venv 中，不影响系统 Python
12. **代码复用**：转录和 MD 写入逻辑集中在 `scripts/transcribe.py`，两个入口脚本共享
13. **GPU 加速**：自动检测 CUDA，有 GPU 时使用 GPU 加速转录（速度提升 5-10 倍），无 GPU 时使用 CPU
14. **initial_prompt**：默认设置中文提示文本，提升中文+英文混合识别准确率
15. **依赖分层**：本地转录只需核心依赖（whisper、requests、ffmpeg），抖音模式额外需要 playwright
16. **Windows UTF-8**：脚本入口自动 `sys.stdout.reconfigure(encoding='utf-8')`，解决 GBK 控制台中文乱码
17. **进度与预估**：自动获取媒体时长，根据模型大小和 CPU/GPU 预估转录耗时；计时从模型加载完毕后开始（不含模型加载）；转录后输出实际耗时和速度倍率

---

## 文件结构

```
douyin-transcribe-lz/
├── SKILL.md                          # 本文件
├── .env_config.json                  # 机器特定配置（setup_env.py 自动生成，勿手动编辑）
├── scripts/
│   ├── transcribe.py                 # 共享模块：转录 + MD 写入（核心逻辑）
│   ├── fetch_douyin_video.py         # 抖音模式入口：捕获 → 下载 → 转录
│   ├── transcribe_local.py           # 本地模式入口：格式验证 → 转录
│   ├── setup_env.py                  # 环境自动配置（支持 Windows/macOS/Linux）
│   └── verify_env.py                 # 环境快速检测（支持 --fix 自动修复）
├── references/
│   └── whisper_usage.md              # Whisper 参数详解
└── venv/                             # 隔离 Python 环境（setup_env.py 自动创建，不提交到版本控制）
    └── ...
```

> `.env_config.json` 和 `venv/` 是运行时生成的文件，跨机器迁移后需重新运行 `setup_env.py` 生成。
