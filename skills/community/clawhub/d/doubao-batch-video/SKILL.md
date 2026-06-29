---
name: doubao-batch-video
description: 豆包网页视频批量生成技能。基于豆包网页端批量生成推广视频，自动完成文案创作、视频生成、拼接混音的完整流水线。触发词：豆包批量生成视频、帮我用豆包做视频、批量生成短视频。
agent_created: true
---

# 豆包网页视频批量生成技能

基于豆包网页端（doubao.com）批量生成推广短视频，自动完成从文案创作到成片输出的完整流水线。

---

## 技术框架

```
┌─────────────────────────────────────────────────────────┐
│           豆包网页视频批量生成技能 v1.0                 │
├─────────────────────────────────────────────────────────┤
│  输入：主题 / 条数 / 画幅 / 风格                       │
│  ↓                                                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Layer 1 · 登录管理（第零步）                    │   │
│  │  检测登录态 → 引导登录（手机号/扫码）              │   │
│  │  保持会话（OpenCLI profile / 持久化用户数据）       │   │
│  └────────────────┬────────────────────────────────┘   │
│                   ↓                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Layer 2 · 文案创作                            │   │
│  │  AI 生成 N 条文案（标题/描述/提示词/配音文本）    │   │
│  │  ⚠️ 提示词确认节点（人机协作，必须用户确认）      │   │
│  └────────────────┬────────────────────────────────┘   │
│                   ↓                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Layer 3 · 视频生成（二选一）                    │   │
│  │  ┌──────────────┐  ┌──────────────────────┐  │   │
│  │  │ 方式A：豆包    │  │ 方式B：多模态云端      │  │   │
│  │  │ (推荐，画质好) │  │ (备用，无需登录)       │  │   │
│  │  │ OpenCLI/      │  │ 多模态内容生成技能      │  │   │
│  │  │ Playwright    │  │ 并发限制：2条同时      │  │   │
│  │  └──────────────┘  └──────────────────────┘  │   │
│  └────────────────┬────────────────────────────────┘   │
│                   ↓                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Layer 4 · 后期处理                            │   │
│  │  ① ffmpeg 拼接（concat，N × 10s）             │   │
│  │  ② 生成 BGM（lavfi sine + afade）             │   │
│  │  ③ 混音（amix，原声 + BGM）                   │   │
│  │  ④ 压缩（libx264，用于平台上传）               │   │
│  └────────────────┬────────────────────────────────┘   │
│                   ↓                                     │
│  输出：final.mp4（完整版）+ final-sm.mp4（压缩版）     │
├─────────────────────────────────────────────────────────┤
│  支撑配置：                                          │
│  • ffmpeg + ffprobe（必备，视频处理）                  │
│  • OpenCLI + Browser Bridge（可选，浏览器自动化）       │
│  • Playwright（可选，CDP 接管）                       │
│  • Python3（必备，运行拼接脚本）                       │
└─────────────────────────────────────────────────────────┘
```

### 各层说明

| 层 | 名称 | 核心功能 | 输出 |
|----|------|----------|------|
| Layer 1 | 登录管理 | 检测/引导豆包登录，保持会话 | 已登录的浏览器会话 |
| Layer 2 | 文案创作 | AI 生成 N 条提示词，用户确认 | 已确认的视频提示词列表 |
| Layer 3 | 视频生成 | 调用豆包/云端 API 生成视频 | N 个 .mp4 文件（各10秒） |
| Layer 4 | 后期处理 | 拼接 + BGM + 混音 + 压缩 | 最终成片（完整版 + 上传版） |

---

## 工作流概览

```
理解需求
  ↓
【首次使用】引导登录豆包
  ↓
生成视频文案（N条）
  ↓
⚠️ 提示词确认（展示给用户，等待确认）
  ↓
生成视频（每条10秒，豆包网页端 / 多模态云端）
  ↓
ffmpeg 拼接 → 背景音乐混音
  ↓
输出最终视频（含压缩版）
```

---

## 第零步：登录管理

> **首次使用必须完成此步**。如果已登录可跳过。

### 检测登录态

```bash
opencli browser doubao open "https://www.doubao.com/"
opencli browser doubao eval "document.body?.innerText?.includes('登录')"
```

返回 `true` 说明需要登录。

### 登录方式

| 方式 | 适用场景 | 引导步骤 |
|------|----------|----------|
| 手机号（推荐） | 有国内手机号 | 打开 doubao.com → 登录 → 手机号 → 验证码 |
| 微信/抖音扫码 | 无手机号 | 打开 doubao.com → 登录 → 选微信/抖音 → 扫码 |
| 豆包App扫码 | 手机已装豆包 | 打开 doubao.com → 扫码登录 → 豆包App扫一扫 |

### 登录态保持

- **OpenCLI**：用同一个 profile（如 `doubao`），不要每次新建
- **Playwright**：使用 `launchPersistentContext` + 固定用户数据目录
- **手动**：不要用无痕模式

---

## 第一步：理解需求

向用户确认以下参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 主题 | 必填 | 视频核心主题 |
| 条数 | `5` | 生成几条（每条10秒） |
| 画幅 | `16:9` | `16:9` 横屏 / `9:16` 竖屏 |
| 风格 | `科技感` | 画面风格关键词 |
| 背景音乐 | `是` | 是否合成 BGM |
| 上传平台 | `否` | 需要则生成压缩版 |

---

## 第二步：文案创作

根据用户主题，生成 N 条短视频文案。

每条文案包含：
- **标题**（20字内）
- **描述**（50字内，含2-3个话题标签）
- **视频提示词**（中文，描述画面+风格+质量关键词，50字内）
- **配音文本**（80字内，对应10秒口播时长）

### 文案生成提示词模板

```
请为「{主题}」生成 {N} 条短视频文案，每条包含：
1. 标题（20字内）
2. 描述（50字内，含 # 话题标签）
3. 视频提示词（用于AI生成视频，中文描述画面+风格，50字内）
4. 配音文本（口播文案，80字内，对应10秒视频时长）

要求：风格多样，涵盖科普/对比/案例/趋势/行动五种角度。
```

---

## ⚠️ 第三步：提示词确认（必做）

文案生成后，**必须先将所有视频提示词展示给用户确认**，不得直接提交生成！

### 操作流程

**1. 以表格形式展示给用户：**

```
以下是为「{主题}」生成的 {N} 条视频提示词，请确认：

| 序号 | 标题 | 视频提示词（将用于AI生成） | 配音文本 |
|------|------|--------------------------|----------|
| 1 | XXX | XXX | XXX |
| 2 | XXX | XXX | XXX |
| ... | ... | ... | ... |

如果需要修改某条的提示词，请直接告诉我；
如果确认无误，请回复「确认/OK/可以」。
```

**2. 等待用户响应：**
- 用户说「确认/OK/可以/没问题」→ 继续进入「第四步：生成视频」
- 用户提出修改 → 修改对应提示词，再次展示确认

**3. 确认通过后才进入视频生成。**

---

## 第四步：生成视频

### 方式A：豆包网页端（推荐，画质好）

> 前提：已完成登录（见第零步）。

#### A1：OpenCLI Browser Bridge（推荐）

```bash
# 打开豆包（用已登录的 profile）
opencli browser doubao open "https://www.doubao.com/"

# 等待加载
opencli browser doubao wait time 3

# 查看页面交互元素（找到视频生成入口的索引）
opencli browser doubao state

# 点击"视频生成"入口
opencli browser doubao click <index>

# 输入提示词并提交
opencli browser doubao type <index> "提示词，科技感，16:9"
opencli browser doubao click <index>   # 提交生成

# 等待生成完成（30-60秒）
opencli browser doubao wait time 60

# 下载视频
opencli browser doubao click <index>   # 下载按钮
```

#### A2：Playwright CDP（豆包自动化技能）

```bash
node ~/.workbuddy/skills/doubao-automation/scripts/doubao-automation.js \
  --action generate-video \
  --prompt "视频提示词" \
  --aspect-ratio "16:9"
```

#### A3：手动引导（自动化失败时的兜底）

1. 用户在浏览器打开 `https://www.doubao.com/`（已登录）
2. 找到"视频生成"功能
3. 逐条输入提示词，点击生成
4. 生成完成后下载，将文件路径告诉 AI

---

### 方式B：多模态云端生成（备用）

使用 **多模态内容生成** 技能（`Skill` 工具，命令：`多模态内容生成`）。

每次调用生成一条视频：
```json
{
  "operation": "text-to-video",
  "prompt": "<视频提示词>",
  "duration": 10,
  "aspect_ratio": "16:9"
}
```

> **注意**：并发限制2条同时，每条间隔至少30秒。

---

## 第五步：视频拼接（ffmpeg）

将 N 个视频文件拼接为一条长视频。

### 使用内置脚本

```bash
python ~/.workbuddy/skills/doubao-batch-video/scripts/combine_videos.py \
  --input-dir ./video-output \
  --output ./video-output/final-concat.mp4
```

### 手动拼接

创建 `concat-list.txt`：
```
file 'video-1.mp4'
file 'video-2.mp4'
file 'video-3.mp4'
file 'video-4.mp4'
file 'video-5.mp4'
```

执行拼接：
```bash
ffmpeg -f concat -safe 0 -i concat-list.txt -c copy final-concat.mp4
```

---

## 第六步：生成背景音乐

用 ffmpeg 生成电子合成风格 BGM（无需外部音频文件）。

```bash
# 获取视频总时长
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 final-concat.mp4)

# 生成正弦波 BGM（淡入淡出）
ffmpeg -f lavfi -i "sine=frequency=440:duration=$DURATION" \
  -af "volume=0.15,afade=t=in:st=0:d=2,afade=t=out:st=$(echo "$DURATION - 2" | bc):d=2" \
  bgm.wav
```

---

## 第七步：混音

将拼接后的视频与背景音乐混合。

```bash
ffmpeg -i final-concat.mp4 -i bgm.wav \
  -filter_complex "[1:a]volume=0.15,afade=t=in:st=0:d=2,afade=t=out:st=<总时长-2>:d=2[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy -shortest final-combined.mp4
```

---

## 第八步：压缩（用于上传）

视频号等平台对文件大小有限制（通常50MB），需要压缩：

```bash
ffmpeg -i final-combined.mp4 \
  -c:v libx264 -crf 26 -preset medium \
  -c:a aac -b:a 128k \
  final-combined-sm.mp4
```

---

## 输出文件

| 文件 | 说明 |
|------|------|
| `video-output/video-1~N-<id>.mp4` | 原始生成视频（每条10秒） |
| `video-output/final-concat.mp4` | 拼接后视频（无声） |
| `video-output/final-combined.mp4` | 最终成片（有背景音乐） |
| `video-output/final-combined-sm.mp4` | 压缩版（用于平台上传） |

---

## 依赖检查

运行前确保以下工具可用：
- `ffmpeg` + `ffprobe`：视频拼接和混音（**必备**）
- `python3`：运行拼接脚本（**必备**）
- OpenCLI + Browser Bridge 扩展（可选，浏览器自动化）
- 多模态内容生成技能（可选，云端视频生成备用）

---

## 常见问题

**Q：新用户第一次怎么登录豆包？**
A：见「第零步」，推荐手机号登录。登录后保持同一浏览器会话。

**Q：视频生成失败？**
A：豆包网页端有频率限制（每日约10条）。如遇限制，切换至多模态云端生成。

**Q：拼接后视频时长不对？**
A：检查 `concat-list.txt` 中的文件路径，建议使用绝对路径。用 `ffprobe` 检查各视频时长。

**Q：背景音乐太吵？**
A：调整 `volume` 参数，推荐 `0.1~0.2` 之间。

**Q：想每条视频有不同的配音？**
A：在文案阶段生成「配音文本」，用 TTS 工具生成音频，再用 ffmpeg 将音频与视频合成。
