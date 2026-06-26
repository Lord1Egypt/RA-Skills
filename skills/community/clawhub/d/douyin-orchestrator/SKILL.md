---
name: douyin-orchestrator
description: 抖音视频转录工作流编排。从抖音链接下载视频、转录语音、分析内容，输出结构化成果。编排调用 douyin-fetcher、douyin-transcriber、douyin-analyzer 三个独立模块。
---

# Douyin Transcribe - 工作流编排

**
完整的抖音视频转录工作流，按顺序调用三个独立模块：

1. **douyin-fetcher** - 获取视频
2. **douyin-transcriber** - 转录音频
3. **douyin-analyzer** - 分析内容

---

## 架构

```
用户发送抖音链接
    ↓
[Step 0] 判断输入类型
    ↓
[Step 1] fetcher: 解析链接 → 下载视频
    ↓
[Step 2] transcriber: 提取音频 → 转录文字
    ↓
[Step 3] analyzer: 清理文本 → 分析要点
    ↓
[Step 4] 保存成果 → 更新索引
```

---

## 完整工作流

### Step 0: 判断输入类型

| 输入类型 | 处理方式 |
|----------|----------|
| 视频链接（`/video/`） | 完整工作流 |
| 图文链接（`/note/`） | 浏览器 snapshot 提取文字 |
| 本地视频文件 | 从 Step 2 开始 |
| 文本内容 | 从 Step 3 开始 |

---

### Step 1: 下载视频

**调用模块**：`douyin-fetcher`

详见 `~/.openclaw/skills/douyin-fetcher/SKILL.md`

⚠️ **注意**：Step 1 的 browser act 调用必须用 `request={"kind": "evaluate", "fn": "..."}` 嵌套格式。

**输出**：视频流 + 音频流（DASH）或完整视频文件

---

### Step 2: 转录音频

**调用模块**：`douyin-transcriber`

详见 `~/.openclaw/skills/douyin-transcriber/SKILL.md`

⚠️ **注意**：如果 Step 1 下载了 DASH 分离流，直接用 `audio.mp4` 转 WAV 转录，不需要先合并

**输出**：转录文本

---

### Step 3: 分析内容

**调用模块**：`douyin-analyzer`

详见 `~/.openclaw/skills/douyin-analyzer/SKILL.md`

**做法**：转录后由 agent 直接分析（语义分段、修正错误、提取要点）

---

### Step 4: 保存成果

#### 转录稿（/path/to/knowledge\transcripts\）

| 文件 | 说明 |
|------|------|
| `{主题}-完整转录.md` | 包含标题、作者、链接、转录时间、完整内容 |

#### 视频文件（/path/to/videos\）

| 文件 | 说明 |
|------|------|
| `{主题}.mp4` | 原始视频（可选保存）|

#### 更新索引

保存文件后，更新：
- `/path/to/knowledge\transcripts\data_structure.md`
- `/path/to/knowledge\data_structure.md`（主索引）
- `/path/to/videos\data_structure.md`（如保存视频）

---

## 部分工作流

| 用户请求 | 执行步骤 |
|----------|----------|
| "帮我转录这个抖音视频" | Step 1 → 2 → 3 → 4 |
| "只下载这个视频，不转录" | Step 1 → 保存到 /path/to/videos\ |
| "我已经有视频文件了，帮我转录" | Step 2 → 3 → 4 |
| "帮我分析这段文本" | Step 3 → 4 |

---

## 异常处理汇总

| 阶段 | 问题 | 处理 |
|------|------|------|
| Step 1 | 短链解析失败 | 检查链接完整性，去掉分享文案干扰字符 |
| Step 1 | JS 返回空数组 | 等待 15-20 秒后重试，或扩大搜索范围 |
| Step 1 | 下载 403 | URL 过期，重新获取 |
| Step 1 | 浏览器不可用 | 提示用户手动下载 |
| Step 2 | ffmpeg 未安装 | `winget install Gyan.FFmpeg` |
| Step 2 | Whisper 服务未运行 | `docker start whisper-asr` |
| Step 2 | 转录超时 | 长视频需要更多时间，10分钟视频约需 15-20 分钟 |
| Step 2 | 转录乱码 | 语言识别问题，可后续手动修正 |
| Step 4 | 索引更新失败 | 手动更新 data_structure.md |

---

## 图文笔记处理

图文链接（`/note/`）无需下载，直接提取：

```
1. browser(action='open', profile='openclaw', url='图文链接')
2. browser(action='snapshot')
3. 从 snapshot 提取文字内容
4. 保存到 /path/to/knowledge\transcripts\
```

---

## 前置条件

| 工具 | 用途 | 检查命令 |
|------|------|----------|
| curl | 下载文件 | `curl --version` |
| ffmpeg | 视频合并/格式转换 | `ffmpeg -version` |
| Docker Whisper | 转录服务（内含 ffmpeg 7.1）| `docker ps --filter "name=whisper-asr"` |
| 浏览器 | 抓取视频 | openclaw profile 可用 |

**说明**：宿主机 ffmpeg 8.1 用于视频合并等任务，Whisper ASR 容器内 ffmpeg 7.1 用于转录处理，两者并存。

---

## 已知限制

1. **视频 URL 有时效性** — 获取后立即下载
2. **长视频转录耗时** — 10分钟视频约需 15-20 分钟
3. **需要浏览器** — openclaw profile 必须可用
4. **图文笔记** — 部分需要登录才能查看完整内容
5. **部分视频无分离流** — 直接是完整 MP4，无需合并