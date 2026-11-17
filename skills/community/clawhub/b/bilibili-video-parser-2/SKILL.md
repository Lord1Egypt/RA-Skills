---
name: bilibili-video-parser
slug: bilibili-video-parser
displayName: B站视频解析
version: 1.0.0
summary: 把B站视频链接转成连贯稿，并自动生成结构化 HTML 分析报告。支持CC字幕优先（跳过转写），无字幕时用 faster-whisper 本地转写。需要联网下载视频和 whisper 模型，免费、不需要任何 API key。
description: B站视频解析-把B站视频链接（bilibili.com/video/BVxxx 长链或 b23.tv 短链）转成中文字幕连贯稿和交互式 HTML 报告。原理：B站公开 API 获取元数据+cid -> 优先尝试CC字幕API（有字幕直接用，跳过转写）-> 无字幕时下载音频流 -> 本地 faster-whisper（base 模型、CPU、int8）转写 -> 本地规则提取分析 -> 生成交互式 HTML 报告（含一句话总结、金句卡片、核心观点、结构拆解、内容判断、内容亮点六大模块）。免费，不依赖任何 API key 或 cookie 登录。一条命令出连贯稿（无时间戳）+ 可视化 HTML 报告。
license: MIT
author: zhouq2039-lang
---

# B站视频解析（本地版）

## 这条 skill 解决什么

经常需要"读"B站视频里的内容——判断对账号有没有用、提炼观点、做素材库。
但 AI 模型本身不能听音频，必须借工具。这条 skill 就是那套工具的固化。

核心做法：

1. 从B站链接提取 `BV号`
2. 走 `api.bilibili.com/x/web-interface/view` 公开 API 获取元数据（标题/UP主/时长/cid）
3. **优先尝试CC字幕**：走 `api.bilibili.com/x/player/v2` 获取CC字幕，有则直接用，跳过转写（秒出）
4. 无CC字幕时：走 `playurl` API 拿 DASH 音频流直链，用 Python 标准库 `urllib` 下载（不依赖外部 curl）
5. 用 `faster-whisper`（CPU、int8、base 模型）转写
6. 输出连贯稿（无时间戳）
7. **本地规则提取**：无 API Key 时通过关键词密度、段落结构和数字线索提取分析
8. **生成 HTML 报告**：始终生成一份交互式 HTML 报告，含六大模块

**不需要**：ffmpeg 外部命令、yt-dlp、curl、cookie、登录、API key。
`faster-whisper` 自带的 PyAV 已经能读 m4a 抽音轨。
B站CC字幕可直接从 API 获取时，完全跳过转写，速度极快。

## Required Capabilities（权限声明）

> 以下权限均为**执行B站链接解析任务所必需的最小权限**。仅在用户明确提供B站链接（bilibili.com / b23.tv）时才触发，不执行任何与本任务无关的系统操作。

| 能力 | 用途 | 触发条件 | 最小化说明 |
|------|------|----------|-----------|
| 网络请求 | 访问 api.bilibili.com 获取视频元数据、CC字幕、音频流直链 | 用户提供B站链接时 | 仅访问 bilibili.com 域名，不向任何第三方发送数据 |
| 网络请求（下载） | 下载音频流文件（DASH格式，仅音频） | 视频无CC字幕时 | 仅下载音频流，不下载视频画面；请求头含 Referer: bilibili.com |
| 网络请求（模型） | 首次运行时从 HuggingFace 下载 whisper base 模型（~74 MB） | 首次转写、模型未缓存时 | 下载到系统临时目录后缓存，之后不再重复下载 |
| Python 子进程 | 运行 faster-whisper 转写脚本（CPU、int8） | 无CC字幕、需转写时 | 仅调用 faster-whisper 库，无外部命令行调用 |
| 文件读写 | 保存连贯稿 txt 文件、写入 HTML 报告 | 转写/字幕获取完成后 | 输出到脚本 work/ 目录（可用 --out-dir 指定受控目录） |
| 临时文件 | 在系统 temp 目录存放音频文件和 whisper 模型 | 下载/转写期间 | 音频转写完成后自动删除（--keep-audio 可保留） |

**不执行的操作**：不读取用户本地任意文件、不访问B站以外的任意 URL（HuggingFace 模型下载除外）、不发送数据到任何第三方服务、不上传用户数据。

## 环境准备（AI 执行前必须检查）

收到B站链接后，**第一步不是直接跑脚本**，而是先检查环境：

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

## 一行命令用法

环境就绪后，直接跑：

```bash
python3 scripts/transcribe.py "https://www.bilibili.com/video/BV1Mu3y6NEzT"
# 或短链
python3 scripts/transcribe.py "https://b23.tv/xxx"
# 或直接传 BV号
python3 scripts/transcribe.py "BV1Mu3y6NEzT"
```

脚本会输出：
- `MMDD-<BV号>-连贯稿.txt`（无时间戳，纯文本）
- `MMDD-<BV号>-报告.html`（交互式 HTML 报告）
- **连贯稿前 500 字摘要**（打印到终端，完整内容见连贯稿文件；如需全文打印加 `--print-transcript`）

> 如果视频有CC字幕，会直接使用字幕数据，跳过 Whisper 转写，速度极快（秒出）。

### AI 深度分析注入（推荐）

脚本内置的本地规则提取（`local_analysis`）只是兜底，**质量有限**。AI Agent 跑完脚本后，应自己读连贯稿做深度分析，再用 `--analysis-json` 注入，重新生成高质量报告：

```bash
# 1. AI 读连贯稿 → 产出 analysis.json（结构见下）
# 2. 注入 AI 分析，重建 HTML（跳过下载/转写，秒出）
python3 scripts/transcribe.py "<链接>" \
  --from-transcript "MMDD-<BV号>-连贯稿.txt" \
  --analysis-json "MMDD-<BV号>-analysis.json"
```

`analysis.json` 结构（与 `local_analysis` 返回一致）：

```json
{
  "summary": "一句话总结",
  "key_points": ["观点1", "观点2"],
  "structure": {
    "type": "口播科普",
    "breakdown": {"开头钩子": "...", "核心论点": "...", "论据案例": "...", "结尾收束": "..."}
  },
  "quotes": [{"text": "金句1", "context": ""}],
  "judgment": {"stance": "立场", "credibility": "可信度", "takeaway": "可借鉴点"},
  "highlights": [{"name": "亮点名", "desc": "说明", "tag": "标签"}]
}
```

> 注意：whisper 转写文本常**没有中文标点**（空格分隔），`local_analysis` 已内置无标点降级切分，但 AI 深度分析仍建议基于连贯稿文件人工阅读后再写。

## HTML 报告内容

报告为单文件 HTML，打开即可直接浏览，包含六大模块：

| 模块 | 说明 |
|------|------|
| Hero 区 | 视频标题 + UP主 + 时长 |
| 一句话总结 | 智能提取核心观点，关键词高亮 |
| 金句卡片 | 2-3 句适合二次传播的金句 |
| 深度解析（胶囊书架） | 点击展开四张胶囊卡片 |
| - 核心观点 | 3-6 条核心观点，编号列表 |
| - 结构拆解 | 开场/核心/结尾分区 |
| - 内容判断 | 立场/可信度/可借鉴点 |
| - 内容亮点 | 观点排行列表 |

> 报告使用系统字体栈（不依赖外部字体 CDN），所有用户内容均经 HTML 转义防止 XSS。

## 转写后的后处理（AI 必须执行）

**拿到连贯稿和 HTML 报告后，AI 不要只甩出文件就结束。** 先读取 `MMDD-<BV号>-连贯稿.txt` 文件的完整内容（终端默认只打印前 500 字摘要，不要依赖终端输出），再按以下结构输出分析，**并把分析写成 JSON 注入回 HTML**（`--analysis-json`，见上节，这样报告才是可发布级的，不要留脚本的兜底分析）：

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

**如果是知识/教程类：**
| 结构 | 内容 |
|------|------|
| 主题 | 这期在教什么 |
| 步骤拆解 | 按顺序列出教学步骤 |
| 关键提醒 | 有没有强调注意事项 |
| 适用场景 | 适合什么人/什么场景用 |

**如果是测评/推荐类：**
| 结构 | 内容 |
|------|------|
| 痛点切入 | 开头怎么戳中用户痛点 |
| 产品卖点 | 列出提到的卖点 |
| 信任背书 | 用了什么方式建立信任（数据/案例/权威） |
| 转化路径 | 怎么引导用户下单/关注/点击 |

### 金句提取
> 挑出 2-3 句适合二次传播的金句（有传播力、有观点、有情绪）

### 内容判断
- **立场分析**：UP主站在什么立场（创作者/消费者/平台/品牌方）
- **可信度**：观点有没有数据支撑，还是纯主观判断
- **可借鉴点**：对我们的内容生产有没有参考价值，具体能借鉴什么

## 已知限制

- whisper base 模型对**中文繁简**会随机选——常见错别字示例："护身符"被识别成"护成盒"。
  - 内容理解不受影响，但写最终稿前要人工修。
  - 如果要更准，把模型换成 `small` 或 `medium`（更慢、更准）：
    ```bash
    python3 scripts/transcribe.py "<链接>" --model small
    ```
- b23.tv 短链偶尔有反爬，长链（bilibili.com/video/BVxxx）更稳。短链失败时手动从浏览器拷贝长链。
- 视频大于 20 分钟时建议改用 `medium` 模型，base 在长视频上准确率会掉。
- 部分视频可能无CC字幕，此时走 Whisper 转写，耗时与视频时长成正比（base 模型约 1:1 速度）。
- 大会员专享/付费视频无法下载音频流，脚本会报错退出。
- 脚本已支持跨平台（Windows/macOS/Linux），临时文件使用系统 temp 目录，不依赖 `/tmp/`。
- HTML 报告的本地规则提取不如 LLM 精准，如需更深分析建议 AI 结合连贯稿做后处理。

## 调用提醒

收到B站视频链接时，第一反应不是去浏览器截图、不是去硬装 yt-dlp。
直接：

```bash
python3 scripts/transcribe.py "<链接>"
```

然后读输出目录里的连贯稿文件（完整内容在文件里，终端只打印摘要），按"先看UP主站在哪儿（立场）→ 再看跟我们阶段/数据对不对得上 → 最后才说能不能用"的顺序判断。
不要直接跳进内容里去结构化。

## 安全声明

- **联网行为（如实声明）**：本技能**需要联网**——每次运行访问 api.bilibili.com 获取视频信息和（可选）CC字幕；无CC字幕时从B站 CDN 下载音频流；首次运行从 HuggingFace 下载 whisper 模型（~74 MB）。**不是纯离线工具**
- **隐私提醒**：转写内容会写入本地 txt/HTML 文件，且视频链接、标题会出现在终端输出中。**请勿在共享/受监控环境中解析隐私敏感视频**；如需控制输出位置，用 `--out-dir` 指定目录
- **终端输出**：默认只打印连贯稿前 500 字摘要，不打印全文，避免敏感语音内容进入终端回滚和日志；确需全文打印时显式加 `--print-transcript`
- **网络边界**：仅访问 api.bilibili.com（获取视频信息/字幕/音频直链）和B站 CDN（下载音频流），HuggingFace（首次模型下载），不发送任何数据到第三方服务
- **无 API Key**：整个流程不需要任何 API key、cookie 或登录态
- **HTML 安全**：生成的 HTML 报告中所有从视频内容提取的文本均经过 `html.escape()` 转义，使用 data-* 属性 + 事件委托替代 inline onclick，防止 XSS
- **无外部字体**：HTML 报告使用系统字体栈，不依赖 Google Fonts 或其他外部字体 CDN
- **临时文件清理**：音频文件在转写完成后自动删除（除非 `--keep-audio`）
