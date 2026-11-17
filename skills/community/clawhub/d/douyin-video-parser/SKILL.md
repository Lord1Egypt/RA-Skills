---
name: douyin-video-parser
slug: douyin-video-parser
displayName: 抖音视频解析
version: 1.4.4
summary: 把抖音视频链接转成中文字幕稿，并自动生成结构化 HTML 分析报告。需要联网下载视频和 whisper 模型，免费、不需要任何 API key。抖音 2026-08 反爬后自动走浏览器直连通道（CDP），无需手动 cookie。
description: 抖音视频解析-把抖音视频链接（v.douyin.com 短链或 douyin.com/video/<id> 长链）转成中文字幕稿和交互式 HTML 报告。原理：多级 fallback 拿 mp4 直链（iesdouyin share API → CDP 浏览器方案 → yt-dlp）-> 下载视频 -> 本地 faster-whisper（base 模型、CPU、int8）转写 -> 本地规则提取分析 -> 生成交互式 HTML 报告。免费，不依赖任何 API key。一条命令出逐字稿（带时间戳）+ 连贯稿（无时间戳）+ 可视化 HTML 报告（含一句话总结、金句卡片、核心观点、结构拆解、内容判断、内容亮点六大模块）。
license: MIT
author: 斑斑（在小黑人 × 斑斑项目里固化）
---

# 抖音视频解析（本地版）

## 这条 skill 解决什么

经常需要"读"抖音视频里的内容——判断对账号有没有用、提炼观点、做素材库。
但 AI 模型本身不能听音频，必须借工具。这条 skill 就是那套工具的固化。

核心做法：

1. 从抖音链接拿到 `video_id`
2. 拿 mp4 直链（按顺序尝试，任一级成功即继续）：
   - **一级：iesdouyin share API**（正则抠 `play_addr`，快路径，无外部依赖）
   - **二级：CDP 浏览器方案**（2026-08 抖音反爬后的主通道）——启动 headless Edge/Chrome，让抖音前端 JS 自己完成签名和种 cookie，再用调试协议（CDP）从 `Network.loadingFinished` 事件后截获 `aweme/v1/web/aweme/detail` 接口响应，提取标题和 mp4 直链。零手动操作、不需要登录。
     - **SSR 页面兜底**：部分视频（如 AI 短片）的页面数据走服务端直出，不发 detail XHR——此时直接截获 `<video>` 元素请求的 CDN 直链（`douyinvod.com`）。抖音对这类视频常用 DASH 分离（视频流/音频流是两个文件），脚本会逐个下载探测，挑**带音轨**的那个用于转写。
   - **三级：yt-dlp 兜底**（最后手段，需 `--cookies` 指定 cookies.txt）
3. 用 Python 标准库 `urllib` 下载 mp4 到系统临时目录（不依赖外部 curl）
4. 用 `faster-whisper`（CPU、int8、base 模型）转写
5. 输出逐字稿（带时间戳）+ 连贯稿（无时间戳）
6. **本地规则提取**：无 API Key 时通过关键词密度、段落结构和数字线索提取分析
7. **生成 HTML 报告**：始终生成一份交互式 HTML 报告，含六大模块

**不需要**：z-ai、ffmpeg 外部命令、curl、登录、API key、手动 cookie。
`faster-whisper` 自带的 PyAV 已经能读 mp4 抽音轨。
CDP 方案需要本机装有 Edge/Chrome（Windows 一般自带 Edge），并安装 `websocket-client` 库。

## Required Capabilities（权限声明）

> 以下权限均为**执行抖音链接解析任务所必需的最小权限**。仅在用户明确提供抖音链接（v.douyin.com / douyin.com / iesdouyin.com）时才触发，不执行任何与本任务无关的系统操作。

| 能力 | 用途 | 触发条件 | 最小化说明 |
|------|------|----------|-----------|
| 网络请求 | 访问 iesdouyin.com 获取视频直链；访问抖音视频 CDN 下载 mp4 | 用户提供抖音链接时 | 仅访问抖音/iesdouyin 域名，不向任何第三方发送数据 |
| 浏览器子进程 | CDP 方案：启动 headless Edge/Chrome 截获抖音详情接口 | iesdouyin API 失效时 | 仅访问 douyin.com，使用独立临时 profile（不碰用户浏览器数据），用后即杀 |
| 网络请求（模型） | 首次运行时从 HuggingFace 下载 whisper base 模型（~74 MB） | 首次转写、模型未缓存时 | 下载到系统临时目录后缓存，之后不再重复下载 |
| Python 子进程 | 运行 faster-whisper 转写脚本（CPU、int8） | 转写步骤 | 仅调用 faster-whisper 库，无外部命令行调用 |
| 文件读写 | 保存逐字稿/连贯稿 txt 文件、写入 HTML 报告 | 转写完成后 | 输出到脚本 work/ 目录（可用 --out-dir 指定受控目录） |
| 临时文件 | 在系统 temp 目录存放 mp4 和 whisper 模型 | 下载/转写期间 | mp4 转写完成后自动删除（--keep-mp4 可保留） |

**不执行的操作**：不读取用户本地任意文件、不访问抖音以外的任意 URL、不发送数据到任何第三方服务、不上传用户数据。

## 环境准备（AI 执行前必须检查）

收到抖音链接后，**第一步不是直接跑脚本**，而是先检查环境：

### 1. 检查 Python
```bash
python3 --version
```

### 2. 检查 faster-whisper 是否已安装
```bash
python3 -c "import faster_whisper; print('ok')"
```

如果报 ImportError，立即安装：
```bash
pip3 install faster-whisper
```
> 首次运行脚本时会自动从 HuggingFace 下载 base 模型（~74 MB）到系统临时目录，之后不再重复下载（模型已缓存）。

### 3. curl 检查
不需要。脚本全部使用 Python 标准库 urllib，不依赖外部 curl。

### 4. 浏览器（CDP 兜底用）
抖音 2026-08 反爬升级后，iesdouyin share API 不再返回视频数据，脚本会自动切换 CDP 浏览器方案。需要：
- 本机装有 Edge 或 Chrome（Windows 一般自带 Edge，无需安装）
- 安装 websocket-client：`pip3 install websocket-client`

### 5. whisper 模型
脚本优先使用本地模型目录 `~/.whisper-models-local`（存在且完整时直接加载，避免反复下载）；否则自动从 HuggingFace 下载 base 模型（~74 MB）到系统临时目录并缓存。

## 一行命令用法

环境就绪后，直接跑：

```bash
python3 scripts/transcribe.py "https://www.douyin.com/video/7634579290163531035"
# 或短链
python3 transcribe.py "https://v.douyin.com/xa-wFiDUUvVs/"
```

脚本会输出：
- `MMDD-<video_id>-逐字稿.txt`（带时间戳）
- `MMDD-<video_id>-连贯稿.txt`（无时间戳）
- `MMDD-<video_id>-报告.html`（交互式 HTML 报告）
- **连贯稿前 500 字摘要**（打印到终端，完整内容见连贯稿文件；如需全文打印加 `--print-transcript`）

## HTML 报告内容

报告为单文件 HTML，打开即可直接浏览，包含六大模块：

| 模块 | 说明 |
|------|------|
| Hero 区 | 视频标题 + 平台 + 时长 |
| 一句话总结 | 智能提取核心观点，关键词高亮 |
| 金句卡片 | 最多 8 句适合二次传播的金句（有金句就留，不设下限）。点击卡片弹出 3:4 竖版大卡片弹窗，适合直接截图分享 |
| 深度解析（胶囊书架） | 点击展开四张胶囊卡片 |
| - 核心观点 | 3-6 条核心观点，编号列表 |
| - 结构拆解 | 开场/核心/结尾分区 |
| - 内容判断 | 立场/可信度/可借鉴点 |
| - 内容亮点 | 观点排行列表 |

> 报告使用系统字体栈（不依赖外部字体 CDN），所有用户内容均经 HTML 转义防止 XSS。

## 转写后的后处理（AI 必须执行）

**拿到连贯稿和 HTML 报告后，AI 不要只甩出文件就结束。** 先读取 `MMDD-<video_id>-连贯稿.txt` 文件的完整内容（终端默认只打印前 500 字摘要，不要依赖终端输出），再按以下结构输出分析：

### 一句话总结
> 用一句话概括这个视频在讲什么。

### 核心观点（3-5 条）
- 提取视频中表达的 3-5 个核心观点，每条一句话

### 结构拆解
根据视频类型，选择对应的结构框架来拆：

**如果是口播/观点类：**
| 结构 | 内容 |
|------|------|
| 开头钩子 | 视频前 5 秒用了什么话术抓住注意力 |
| 核心论点 | 主要在讲什么 |
| 论据/案例 | 用了什么例子支撑 |
| 结尾/CTA | 最后怎么收的，有没有引导行动 |

**如果是营销/带货类：**
| 结构 | 内容 |
|------|------|
| 痛点切入 | 开头怎么戳中用户痛点 |
| 产品卖点 | 列出提到的卖点 |
| 信任背书 | 用了什么方式建立信任（数据/案例/权威） |
| 转化路径 | 怎么引导用户下单/关注/点击 |

**如果是知识/教程类：**
| 结构 | 内容 |
|------|------|
| 主题 | 这期在教什么 |
| 步骤拆解 | 按顺序列出教学步骤 |
| 关键提醒 | 有没有强调注意事项 |
| 适用场景 | 适合什么人/什么场景用 |

### 金句提取
> 挑出最多 8 句适合二次传播的金句（有传播力、有观点、有情绪；有金句就留，不设下限）

### 内容判断
- **立场分析**：说话的人站在什么立场（创作者/消费者/平台/品牌方）
- **可信度**：观点有没有数据支撑，还是纯主观判断
- **可借鉴点**：对我们的内容生产有没有参考价值，具体能借鉴什么

## 已知限制

- whisper base 模型对**中文繁简**会随机选——常见错别字示例："护身符"被识别成"护成盒"。
  - 内容理解不受影响，但写最终稿前要人工修。
  - 如果要更准，把模型换成 `small` 或 `medium`（更慢、更准）：
    ```bash
    python3 scripts/transcribe.py "<链接>" --model small
    ```
- **抖音反爬状态（2026-08）**：iesdouyin share API 已不返回视频数据；CDP 浏览器方案是当前主通道，成功率已实测通过。若 CDP 也失败（抖音风控/要求登录），可提供 cookies.txt 走 yt-dlp 兜底：
  ```bash
  python3 scripts/transcribe.py "<链接>" --cookies cookies.txt
  ```
  cookies.txt 可用浏览器扩展（如 "Get cookies.txt LOCALLY"）从浏览器导出。
- 抖音短链（v.douyin.com）有反爬，长链（douyin.com/video/xxx）更稳。短链失败时手动从浏览器拷贝长链。
- 视频大于 10 分钟时建议改用 `medium` 模型，base 在长视频上准确率会掉。
- 脚本已支持跨平台（Windows/macOS/Linux），临时文件使用系统 temp 目录，不依赖 `/tmp/`。
- HTML 报告的本地规则提取不如 LLM 精准，如需更深分析建议 AI 结合连贯稿做后处理。
- **金句卡片（2026-08-20 修复）**：旧版金句规则只匹配书面句式（"说过/名言/不是…而是"），且回退逻辑要求句子含 4 个以上连续英文字母，对中文口播视频几乎必挂 → 金句卡片常显示"暂无金句数据"。新版改为观点强度打分（转折/反问/强情绪词/因果词），并修复 whisper 无标点文本的句子切分（超长块按逗号/空格二次切分）。金句上限 8 句（有金句就留，不设下限）。**注意：本地规则捞出的金句是"候选句"，质量一般（可能是切碎短句），AI 后处理时务必人工精选带标点、适合传播的金句，数量按实际有多少留多少（最多 8 句）。**

## 调用提醒

收到抖音视频链接时，第一反应不是去浏览器截图、不是去硬装 yt-dlp。
直接：

```bash
python3 scripts/transcribe.py "<链接>"
```

然后读输出目录里的连贯稿文件（完整内容在文件里，终端只打印摘要），按"先看说话的人站在哪儿（立场）→ 再看跟我们阶段/数据对不对得上 → 最后才说能不能用"的顺序判断。
不要直接跳进内容里去结构化。

## 安全声明

- **联网行为（如实声明）**：本技能**需要联网**——首次运行从 HuggingFace 下载 whisper 模型（~74 MB），每次运行访问 iesdouyin.com / douyin.com 获取视频信息、下载 mp4 文件。**不是纯离线工具**
- **浏览器调用（CDP 兜底）**：iesdouyin API 失效时会启动一次 headless Edge/Chrome 访问 douyin.com 视频页，用独立临时 profile（不读取用户浏览器数据），进程用完即终止。浏览器只访问 douyin.com 域名
- **隐私提醒**：转写内容会写入本地 txt/HTML 文件，且视频链接、标题会出现在终端输出中。**请勿在共享/受监控环境中解析隐私敏感视频**；如需控制输出位置，用 `--out-dir` 指定目录
- **终端输出**：默认只打印连贯稿前 500 字摘要，不打印全文，避免敏感语音内容进入终端回滚和日志；确需全文打印时显式加 `--print-transcript`
- **网络边界**：仅访问 iesdouyin.com / douyin.com（获取视频信息）和视频 CDN（下载 mp4），不发送任何数据到第三方服务
- **无 API Key**：整个流程不需要任何 API key、cookie 或登录态（yt-dlp 兜底时可选提供 cookies.txt）
- **HTML 安全**：生成的 HTML 报告中所有从视频内容提取的文本均经过 `html.escape()` 转义，使用 data-* 属性 + 事件委托替代 inline onclick，防止 XSS
- **无外部字体**：HTML 报告使用系统字体栈，不依赖 Google Fonts 或其他外部字体 CDN
- **临时文件清理**：mp4 文件在转写完成后自动删除（除非 `--keep-mp4`）
