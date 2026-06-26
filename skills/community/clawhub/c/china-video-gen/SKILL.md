---
name: china-video-gen
description: 国内可用的AI视频生成技能。Create videos from text — generates script, images, voiceover, and merges into MP4. No time limit, full control. 视频生成、短视频制作。
version: 1.1.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🎬", "requires": {"bins": ["python3"], "env": ["SILICONFLOW_API_KEY"]}, "primaryEnv": "SILICONFLOW_API_KEY"}}
---

# 国内 AI 视频生成 China Video Gen

将文字描述转化为完整视频：自动生成分镜脚本 → 图片序列 → 配音 → 合成 MP4。
无时长限制，完全可控，国内直连，无需翻墙。

## 触发时机

- "帮我做一个30秒的[产品]宣传视频"
- "生成一个介绍[主题]的短视频"
- "做一个[品牌]的广告视频"
- "把这段文字做成视频"
- "生成适合小红书/抖音发布的视频"

---

## Step 0：环境检查

**每次执行前必须先检查依赖，缺失则提示用户手动安装。**

### 检查 ffmpeg

```
检查 ffmpeg 是否已安装：
- macOS:   brew install ffmpeg
- Ubuntu:  sudo apt install ffmpeg
- Windows: 从 https://ffmpeg.org/download.html 下载
```

### 检查依赖 Skills

```
需要安装以下 skills：
- china-image-gen：文生图技能
- china-tts：文字转语音技能

安装方法：clawhub install china-image-gen
```

### 检查 API Key

```
需要配置 SILICONFLOW_API_KEY：
1. 访问 cloud.siliconflow.cn 注册
2. 进入「API密钥」页面创建 Key
3. export SILICONFLOW_API_KEY='sk-xxxxxxxx'
```

---

## Step 1：理解用户需求

从用户描述中提取关键信息：

```
视频主题：产品宣传 / 知识科普 / 品牌故事 / 教程演示 / 其他
目标时长：15秒 / 30秒 / 60秒 / 更长（无限制）
画面风格：写实 / 插画 / 科技感 / 温暖 / 商务
音色选择：见 china-tts 音色列表
目标平台：小红书(1:1或3:4) / 抖音(9:16) / B站/YouTube(16:9) / 通用(16:9)
语言：中文 / 英文 / 中英混合
```

---

## Step 2：生成分镜脚本

根据用户需求，设计分镜脚本。每个分镜包含：

```
分镜N：
  时长：X 秒
  画面描述（英文 prompt，用于 FLUX 文生图）
  解说词（中文，用于 TTS 配音）
  运镜效果：静止 / Ken Burns 缩放 / 平移
  转场效果：淡入淡出 / 擦除 / 无
```

### 时长分配原则

```
总时长 30秒，建议分镜数量：5-8个
  开场：2-3秒（Logo/主题/吸引眼球）
  主体：每个分镜3-5秒
  结尾：2-3秒（CTA/联系方式/品牌）

总时长 60秒，建议分镜数量：10-15个
  节奏：前10秒最关键，必须抓住注意力

字数与时长对照（TTS朗读速度约4字/秒）：
  3秒 ≈ 12字
  5秒 ≈ 20字
  10秒 ≈ 40字
```

---

## Step 3：生成图片序列

调用 china-image-gen skill，为每个分镜生成对应图片。

### 分辨率与比例

```
小红书(1:1)：1024x1024
小红书(3:4)：768x1024
抖音/竖版(9:16)：720x1280
B站/横版(16:9)：1280x720
```

### 图片生成

对每个分镜执行：
1. 使用 china-image-gen 生成图片
2. 保存到工作区 frames 目录
3. 图片 URL 有效期1小时，必须立即下载

---

## Step 4：生成配音音频

调用 china-tts skill，将所有解说词合并为一个音频文件。

1. 合并所有分镜解说词
2. 调用 TTS 生成 MP3
3. 保存到工作区 audio 目录

---

## Step 5：合成视频

使用 ffmpeg 将图片序列和音频合成为 MP4 视频。

### 方案A：简单合成（静止图片+音频）

- 使用 ffmpeg concat 功能
- 每张图片显示指定时长
- 合并音频

### 方案B：Ken Burns 效果（推荐）

- 为每张图片添加缓慢缩放效果
- 模拟镜头推进
- 更有质感

### 方案C：淡入淡出转场

- 两张图片之间添加淡入淡出
- 使用 xfade filter

---

## Step 6：输出结果

```
视频生成完成
━━━━━━━━━━━━━━━━━━━━
视频文件：{工作区}/output.mp4
总时长：约 XX 秒
分镜数：X 张
画面比例：16:9（1280x720）

文件结构：
  video_xxx/
  ├── output.mp4          ← 最终视频
  ├── frames/             ← 各分镜图片
  ├── audio/
  │   └── voiceover.mp3  ← 配音文件
  └── concat.txt          ← 合成配置
```

---

## 视频类型预设

### 产品宣传（30秒，16:9）

```
分镜数：6个
图片模型：FLUX.1-dev（高质量）
音色：alex（沉稳男声）或 claire（温柔女声）
效果：Ken Burns
转场：淡入淡出
```

### 知识科普（60秒，16:9）

```
分镜数：12个
图片模型：FLUX.1-schnell（快速）
音色：anna（沉稳女声）
效果：静止图片
转场：无
```

### 小红书竖版（30秒，3:4）

```
分辨率：768x1024
分镜数：6个
图片模型：Kolors（中文理解最好）
音色：diana（欢快女声）
效果：Ken Burns
```

### 抖音竖版（15秒，9:16）

```
分辨率：720x1280
分镜数：4个（节奏快）
图片模型：FLUX.1-schnell
音色：bella（激情女声）
效果：Ken Burns
```

---

## 注意事项

- 图片 URL 有效期仅1小时，生成后立即下载
- Ken Burns 效果处理较慢，每张图约需10-30秒
- 视频文件保存至 OpenClaw 工作区，长期保留
- 建议先用 FLUX.1-schnell 快速预览，满意后换 FLUX.1-dev 出高质量版
- 不要在短时间内大批量请求，避免触发 API 限速