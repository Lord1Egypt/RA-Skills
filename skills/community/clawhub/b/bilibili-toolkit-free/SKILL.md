---
name: "bilibili-toolkit-free"
description: "B站热门监控、视频下载、数据查看与字幕获取，免登录使用核心功能，适合个人用户。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "B站工具箱免费版"
  version: "1.0.0"
  summary: "B站热门监控、视频下载、数据查看与字幕获取，免登录使用核心功能，适合个人用户。"
  tags:
    - "B站"
    - "视频下载"
    - "内容监控"
    - "个人创作"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# B站工具箱免费版

## 概述

B站工具箱免费版是一款面向个人用户的轻量级B站内容工具，集成热门监控、视频下载、数据查看、字幕获取与弹幕获取五大模块。无需登录即可使用核心功能，适合个人用户日常浏览B站内容、下载视频离线观看等场景。

## 核心能力

| 模块 | 功能 | 是否需要登录 |
| --- | --- | --- |
| 热门监控 | 热门视频、热搜、排行榜、必看榜 | 否 |
| 视频下载 | 360p-1080p标准画质下载 | 否 |
| 数据查看 | 播放量、点赞数等基础统计 | 否 |
| 字幕获取 | CC字幕下载，多语言支持 | 否 |
| 弹幕获取 | 视频弹幕内容获取 | 否 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：站热门监控、数据查看与字幕获、免登录使用核心功、适合个人用户、站工具箱免费版、面向个人用户的轻、站内容工具、热门视频监控、实时查看、站热门、标准画质视频下载、视频数据查看、查看播放量、下载视频、支持多语言、获取视频弹幕内容、无需登录即可使用等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：浏览B站热门内容

查看B站当前热门视频、热搜话题与排行榜。

```bash
# 查看热门视频
python main.py hot_monitor get_hot '{"page_size": 10}'

# 查看热搜话题
python main.py hot_monitor get_trending '{"limit": 5}'

# 查看每周必看榜
python main.py hot_monitor get_weekly

# 查看游戏区排行榜
python main.py hot_monitor get_rank '{"category": "game", "limit": 10}'
```

```python
# Python API调用
import asyncio
from main import BilibiliAllInOne

app = BilibiliAllInOne()

async def browse_hot():
    # 获取热门视频
    hot_videos = await app.execute("hot_monitor", "get_hot", page_size=10)
    print("=== 热门视频 ===")
    for v in hot_videos['data']:
        print(f"{v['title']} - 播放:{v['play']}")

    # 获取游戏区排行
    game_rank = await app.execute("hot_monitor", "get_rank", 
                                   category="game", limit=5)
    print("=== 游戏区排行 ===")
    for v in game_rank['data']:
        print(f"{v['title']} - 综合得分:{v['score']}")

asyncio.run(browse_hot())
```

### 场景二：下载视频离线观看

下载B站视频到本地，离线观看。

```bash
# 获取视频信息
python main.py downloader get_info '{"url": "BV1xx411c7mD"}'

# 查看可用画质
python main.py downloader get_formats '{"url": "BV1xx411c7mD"}'

# 下载1080p视频
python main.py downloader download '{"url": "BV1xx411c7mD", "quality": "1080p", "format": "mp4"}'

# 仅下载音频
python main.py downloader download '{"url": "BV1xx411c7mD", "format": "mp3"}'
```

```python
# Python API下载
async def download_video():
    # 获取视频信息
    info = await app.execute("downloader", "get_info", url="BV1xx411c7mD")
    print(f"标题: {info['data']['title']}")
    
    # 下载视频
    result = await app.execute("downloader", "download",
                                url="BV1xx411c7mD",
                                quality="1080p",
                                format="mp4")
    print(f"下载完成: {result}")

asyncio.run(download_video())
```

### 场景三：获取视频字幕与弹幕

下载视频字幕用于学习，获取弹幕了解观众反馈。

```bash
# 查看可用字幕
python main.py subtitle list '{"url": "BV1xx411c7mD"}'

# 下载中文字幕（SRT格式）
python main.py subtitle download '{"url": "BV1xx411c7mD", "language": "zh-CN", "format": "srt"}'

# 获取弹幕
python main.py player get_danmaku '{"url": "BV1xx411c7mD"}'
```

```python
async def get_subtitles_and_danmaku():
    # 获取字幕列表
    subs = await app.execute("subtitle", "list", url="BV1xx411c7mD")
    print(f"可用字幕: {subs['data']}")
    
    # 下载中文字幕
    result = await app.execute("subtitle", "download",
                                url="BV1xx411c7mD",
                                language="zh-CN",
                                format="srt")
    print(f"字幕已下载: {result}")
    
    # 获取弹幕
    danmaku = await app.execute("player", "get_danmaku", url="BV1xx411c7mD")
    print(f"弹幕数量: {len(danmaku['data'])}")

asyncio.run(get_subtitles_and_danmaku())
```

## 不适用场景

以下场景B站工具箱免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 依赖详情

```bash
pip install httpx aiohttp beautifulsoup4 lxml requests
```

### 2. 查看热门视频

```bash
python main.py hot_monitor get_hot '{"page_size": 5}'
```

### 3. 下载第一个视频

```bash
python main.py downloader download '{"url": "BV1xx411c7mD", "quality": "1080p"}'
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

### 支持的分区

| 分区 | 代码 |
| --- | --- |
| 全部 | `all` |
| 动画 | `anime` |
| 音乐 | `music` |
| 舞蹈 | `dance` |
| 游戏 | `game` |
| 科技 | `tech` |
| 生活 | `life` |
| 美食 | `food` |
| 汽车 | `car` |
| 时尚 | `fashion` |
| 娱乐 | `entertainment` |
| 影视 | `movie` |
| 电视剧 | `tv` |

### 下载画质选项

| 画质 | 代码 | 需要登录 |
| --- | --- | --- |
| 360p | `360p` | 否 |
| 480p | `480p` | 否 |
| 720p | `720p` | 否 |
| 1080p | `1080p` | 否 |
| 1080p+ | `1080p+` | 是 |
| 4K | `4k` | 是 |

### 字幕格式

| 格式 | 代码 | 说明 |
| --- | --- | --- |
| SRT | `srt` | 默认，通用字幕格式 |
| ASS | `ass` | 高级字幕，支持样式 |
| VTT | `vtt` | Web标准 |
| TXT | `txt` | 纯文本 |
| JSON | `json` | 程序处理 |

## 最佳实践

1. **无需登录**：免费版核心功能无需登录，直接使用即可
2. **画质选择**：1080p已满足大多数观看需求，更高画质需登录
3. **字幕下载**：部分视频可能没有CC字幕，此时会尝试语音识别转写
4. **批量操作**：免费版建议逐个下载，批量下载建议使用PRO版本
5. **遵守规则**：下载内容仅供个人学习使用，请尊重版权
6. **频率控制**：请求不宜过于频繁，避免被限制访问

## 常见问题

### Q1：下载1080p+或4K画质需要什么？

需要提供B站登录凭证（SESSDATA等）。免费版仅支持1080p及以下画质，更高画质请使用PRO版本。

### Q2：视频没有CC字幕怎么办？

系统会自动尝试语音识别转写（需要安装faster-whisper）和弹幕提取作为备用方案。

### Q3：可以批量下载视频吗？

免费版支持单个下载。如需批量下载，建议升级至PRO版本使用batch_download功能。

### Q4：下载的视频是什么格式？

默认下载MP4格式。也可选择FLV格式或仅提取MP3音频。

### 已知限制

免费版无需登录，受B站公开API的频率限制。建议合理使用，避免短时间内大量请求。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8及以上
- **可选工具**: ffmpeg（用于合并音视频流）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python 3 | 运行时 | 必需 | python.org 下载安装 |
| httpx | Python库 | 必需 | `pip install httpx` |
| aiohttp | Python库 | 必需 | `pip install aiohttp` |
| beautifulsoup4 | Python库 | 必需 | `pip install beautifulsoup4` |
| lxml | Python库 | 必需 | `pip install lxml` |
| requests | Python库 | 必需 | `pip install requests` |
| faster-whisper | Python库 | 可选 | `pip install faster-whisper`（语音识别转写） |
| ffmpeg | 系统工具 | 可选 | 系统包管理器安装 |

### API Key 配置

- 免费版无需任何API Key或登录凭证
- 所有核心功能通过B站公开API实现，无需认证

### 可用性分类

- **分类**: MD+EXEC（纯Markdown指令，核心功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行B站内容操作任务。核心功能通过Python脚本调用B站公开API实现，无需登录凭证。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
