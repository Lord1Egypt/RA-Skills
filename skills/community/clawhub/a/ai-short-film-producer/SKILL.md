---
name: ai-short-film-producer
description: AI短剧制作助手 | AI Short Film Producer — 低成本AI短剧/短片全流程制作技能。使用Grok Imagine生成视频镜头、TTS生成配音，配合FFmpeg+Python本地合成。适用于从零制作AI短片、短视频、短剧EP、预告片等场景。包含完整的分镜脚本创作、视频生成、配音生成、音频驱动剪辑、字幕叠加、最终合成、成本核算的全套SOP。
---

# AI短剧制作助手 | AI Short Film Producer

## 概述

本Skill提供一套完整的**低成本AI短剧制作流程**，从脚本创作到最终成片，总成本仅需**¥30-50/部**（128秒短片）。核心思路：用AI API生成素材 → 本地FFmpeg合成 → WorkBuddy编排调度。

**适用场景：**
- 用户说"帮我做一个短片/短剧/预告片"
- 用户说"把这段文案做成视频"
- 用户说"生成一个XX题材的短视频"
- 用户需要从零到一完成AI视频制作

**核心成本优势：**
- 视频生成：Grok Imagine（速创API，按秒计费）
- 配音生成：TTS（速创API，按字计费）
- 合成剪辑：本地FFmpeg免费
- AI编排：WorkBuddy Lite版

---

## 制作流程总览

```
Step 1: 脚本创作
  ├── 确定主题/时长/风格
  ├── 编写分镜脚本（镜头×台词×角色）
  └── 输出：分镜表 + TTS文本清单

Step 2: 视频镜头生成
  ├── 调用速创API Grok Imagine
  ├── 25个镜头批量异步生成
  └── 输出：ep1_shots/*.mp4

Step 3: TTS配音生成
  ├── 调用速创API audio_tts
  ├── 多角色多音色
  └── 输出：ep1_tts/*.mp3

Step 4: 音频驱动剪辑
  ├── 逐段按TTS时长裁剪/循环镜头
  ├── 短镜头自动stream_loop填充
  └── 输出：分段seg_*.mp4

Step 5: 字幕生成
  ├── Python Pillow生成透明PNG字幕
  ├── FFmpeg overlay叠加（因FFmpeg 8.x无drawtext）
  └── 输出：带字幕的分段视频

Step 6: 最终合成
  ├── concat拼接25段视频
  ├── concat拼接25段音频
  ├── 音视频合并
  └── 输出：最终成片.mp4

Step 7: 素材导出
  ├── 结构化桌面文件夹
  ├── 矩阵表 + JSON
  └── 成本核算
```

---

## 详细步骤

### Step 1: 脚本创作

**输入：** 用户需求（主题、风格、时长、参考素材）
**输出：** 分镜脚本文档 + TTS台词清单

**工作流程：**
1. 与用户确认主题方向（科幻/悬疑/科普/剧情等）
2. 编写分镜脚本，包含：
   - 镜头编号、画面描述、时长
   - 配音台词、角色分配、音色选择
   - 音效说明
3. 输出TTS台词清单（25段以内，每段2-20字最佳）
4. 角色音色分配表：

| 角色类型 | 推荐音色ID | 说明 |
|---------|-----------|------|
| 旁白/叙述者 | male-qn-jingying | 精英青年男声，通用 |
| 男主角 | male-qn-jingying | 精英青年男声 |
| 霸道/硬汉 | male-qn-badao | 霸道男声 |
| 反派/俊朗 | junlang_nanyou | 俊朗男声 |
| 成熟女性 | female-chengshu | 成熟女声 |
| 少女 | female-shaonv | 少女音 |
| 研究员/学生 | male-qn-daxuesheng | 大学生男声 |
| 醇厚长辈 | male-chunhou | 醇厚男声 |

### Step 2: 视频镜头生成（速创API Grok Imagine）

**API平台：** 速创API（详见 references/sucuang_api.md）
**模型：** Grok Imagine（xAI Aurora引擎）
**价格：** 按秒计费（具体见平台）

**API调用方式：**
- 鉴权：Authorization Header 传API Key（不带Bearer前缀）
- 接口：POST /api/async/video/grok_imagine
- 参数格式：扁平JSON
- 结果查询：GET /api/async/detail?id=xxx（轮询直到status=2）

**批量生成策略：**
1. 25个镜头同时提交（用ThreadPoolExecutor）
2. 每个镜头约10秒，生成耗时约30-60秒
3. 失败自动重试（平均重试3次）
4. 注意：Sora2接口已不可用（持续400错误），全部使用Grok Imagine

**Prompt编写要点：**
- 英文Prompt效果更稳定
- 包含：场景描述、光线、构图、镜头运动
- 示例：`"Deep space, Milky Way galaxy slowly rotating, cinematic wide shot, photorealistic, 4K quality"`

### Step 3: TTS配音生成（速创API audio_tts）

**API接口：** POST /api/async/audio_tts
**价格：** 按字计费（具体见平台）
**参数格式（重要）：** 扁平JSON，不要嵌套

```json
{
  "text": "台词内容",
  "voice_id": "male-qn-jingying",
  "speed": 1.0
}
```

**注意事项（踩坑经验）：**
- ❌ 不要传 format 参数（会报500"存在未绑定的参数"）
- ❌ 不要嵌套成 `{"model":"audio_tts","params":{...}}`
- ✅ 状态码判断：status=2 完成，status=0/1 处理中
- ⚠️ 部分任务会卡住（status一直=0），重试可换IP节点
- ✅ 返回tar包，需解压获取mp3

### Step 4: 音频驱动剪辑（核心节奏控制）

**核心理念：** 画面长度由语音旁白决定，而非固定时长。先录制/生成TTS配音，再让每段视频精确匹配对应配音的时长。这样保证音画天然同步，且节奏由配音自然驱动。

#### 4.1 节奏控制逻辑

```
每段（镜头, TTS）的处理流程：

1. 获取TTS音频实际时长 tts_dur（用ffprobe精确到毫秒）
2. 获取源视频时长 src_dur
3. 对比决策：
   ├── src_dur >= tts_dur + 0.5s  → 直接裁剪到tts_dur（视频多出的部分舍弃）
   ├── src_dur ≈ tts_dur（差<0.5s）→ 直接裁剪，不做额外处理
   └── src_dur < tts_dur           → stream_loop循环播放填满tts_dur
4. 输出：seg_NNN.mp4（时长=tts_dur，精确匹配配音）
```

**为什么用"音频驱动"而非"视频驱动"：**
- 传统剪辑：先定视频长度，再往里塞配音 → 配音节奏被画面绑架
- 音频驱动：先定配音节奏，再裁剪画面适配 → 叙事节奏由台词自然决定
- 效果：观众听到的每句话都有对应的画面时长，不会出现"话没说完画面就切了"

#### 4.2 短镜头循环填充（stream_loop）

当源视频时长不够时，用FFmpeg的stream_loop让视频循环播放：

```bash
# 循环播放直到填满tts_dur
/opt/homebrew/bin/ffmpeg -y -stream_loop -1 -i shot.mp4 -t {tts_dur} -c:v libx264 -preset fast seg.mp4
```

**实战经验（三体EP1）：**
- 25个镜头中有3个需要循环填充
- 最大修复：pan_han_02火鸡演讲（源视频10s → TTS需要19s，循环补9s）
- 循环填充的视觉重复感在1-2次循环内不明显，超过3次建议换镜头

#### 4.3 逐段精确裁剪避免累积漂移

```python
# 关键：每段独立裁剪，不整体缩放
cumulative = 0.0
for i, (tts_file, shot_file) in enumerate(segments):
    tts_dur = get_duration(tts_file)  # ffprobe获取
    # 精确裁剪到tts_dur，不依赖前一段的结束时间
    trim_video(shot_file, tts_dur, f"seg_{i:03d}.mp4")
    cumulative += tts_dur

# 最终验证：所有seg时长之和 ≈ audio_concat时长 ≈ 最终成片时长
```

**FFmpeg路径（Mac mini M4）：** `/opt/homebrew/bin/ffmpeg`

**已知限制：**
- FFmpeg 8.x 未编译drawtext/libass/freetype滤镜 → 不能直接加字幕
- anullsrc语法用 `cl=stereo` 而非 `c=stereo`
- shell转义用Python subprocess list模式避免zsh问题

### Step 5: 字幕生成

**方案：** Pillow生成透明PNG → FFmpeg overlay叠加

```python
from PIL import Image, ImageDraw, ImageFont

# 创建透明PNG
img = Image.new('RGBA', (1920, 160), (0,0,0,0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 48)

# 白色大字 + 黑色描边
draw.text((960, 80), "台词文本", fill='white', font=font, 
          anchor='mm', stroke_width=3, stroke_fill='black')

# FFmpeg overlay叠加
ffmpeg -i seg.mp4 -i sub.png -filter_complex "overlay=0:H-h" output.mp4
```

**字幕设计规范：**
- 底部居中，距底部约60px
- 白色大字 + 3px黑色描边
- 字号48-56px（PingFang SC字体）
- 可加角色标签（如"旁白："、"汪淼："）

### Step 6: 最终合成

**拼接视频：**
```bash
# 生成file list
for f in seg_*.mp4; do echo "file '$f'" >> video_list.txt; done
ffmpeg -f concat -safe 0 -i video_list.txt -c copy video_concat.mp4
```

**拼接音频：**
```bash
for f in audio_*.mp3; do echo "file '$f'" >> audio_list.txt; done
ffmpeg -f concat -safe 0 -i audio_list.txt -c copy audio_concat.aac
```

**音视频合并：**
```bash
ffmpeg -i video_concat.mp4 -i audio_concat.aac -c:v copy -c:a aac final.mp4
```

### Step 7: 素材导出与成本核算

**桌面文件夹结构：**
```
~/Desktop/项目名称/
├── 01_字幕/     → 字幕PNG文件
├── 02_配音/     → TTS音频MP3
├── 03_主图/     → 镜头缩略图JPG
├── 04_视频/     → 分段视频MP4
├── 05_矩阵表/   → 矩阵表.html + 素材结构.json
└── 最终成片.mp4
```

**成本核算模板：**

| 项目 | 计算方式 | 说明 |
|------|---------|------|
| Grok Imagine视频 | 总秒数 × 重试次数 × 单价 | 按秒计费 |
| TTS配音 | 总字数 × 单价 | 按字计费 |
| WorkBuddy算力 | 对话轮次 × 单价 | 按轮计费 |
| 硬件折旧 | Mac mini ¥3,999/3年寿命 | ¥3.65/天 |
| 电费 | 16h × 65W × ¥0.6/度 | ¥0.62/天 |

---

## 速创API平台速查

**平台地址：** 详见 references/sucuang_api.md
**文档中心：** 详见 references/sucuang_api.md

**常用模型及价格：**

| 模型/接口 | 价格 | 说明 |
|-----------|------|------|
| Grok Imagine 视频生成 | 按秒计费 | 文生视频/图生视频，6-15秒 |
| audio_tts 配音 | 按字计费 | 多音色TTS |
| video_digital_humans 数字人 | 按次计费 | 需公网音频URL+视频URL |
| Sora2（已弃用） | — | 持续400错误，不可用 |

**API Key传递：**
- ✅ Authorization Header（推荐，不带Bearer前缀）
- ❌ URL参数 ?key=xxx（会返回403）

---

## 三体EP1实战参考

**项目规模：** 25个镜头，127秒成片，8个角色
**总成本：** ¥44.17（含重试+硬件折旧）
**工具链：** Grok Imagine × 25 + TTS × 25 + FFmpeg + Python Pillow
**迭代版本：** v5min → v6 → v7 → v7.1 → v8（5个版本迭代）

**关键经验：**
1. Sora2不可用，全部切Grok Imagine
2. 源视频短于TTS时用stream_loop循环填充
3. FFmpeg 8.x无drawtext，用Pillow生成PNG替代
4. TTS部分任务卡住需重试
5. 逐段精确裁剪避免累积漂移

---

## 专业审核与迭代流程

AI生成的第一版通常不是最终版。必须经过"制作→审核→修改"的迭代循环才能达到交付标准。

### 审核维度

| 维度 | 检查内容 | 常见问题 |
|------|---------|---------|
| **音画同步** | 画面内容是否匹配配音台词 | 角色A说话但画面是角色B |
| **时长匹配** | 每段视频是否完整覆盖TTS | 短镜头被截断，话没说完画面就切 |
| **视觉重复** | 循环播放是否超过3次 | 火鸡演讲循环9s，观众能看出重复 |
| **字幕准确** | 字幕文本是否与TTS一致 | 错别字、标点错误 |
| **节奏感** | 整体叙事节奏是否流畅 | 某段太长拖沓，某段太短仓促 |
| **画面质量** | 是否有明显AI生成瑕疵 | 人物变形、闪烁、分辨率低 |

### 迭代流程

```
V1（初版合成）
  ↓
专业审核（逐段检查以上6个维度）
  ↓
问题清单 → 按严重程度排序
  ├── P0（必须修）：音画不匹配、字幕错误、画面截断
  ├── P1（建议修）：节奏拖沓、视觉重复感强
  └── P2（可优化）：画面质量、色调统一
  ↓
V2（修复P0问题）
  ↓
再次审核
  ↓
V3...（逐轮修复，直到P0=0、P1≤2）
  ↓
最终交付
```

### 实战案例：三体EP1迭代记录

| 版本 | 问题 | 修复方案 |
|------|------|---------|
| v5min | 252秒成片，但TTS只有127秒，大量空白 | 重新按TTS时长裁剪 |
| v6 | 音频驱动剪辑，但3个短镜头被截断 | 修复中 |
| v7 | 短镜头截断（火鸡演讲缺9s） | stream_loop循环填充 |
| v7.1 | 循环修复完成，但无字幕 | 加字幕 |
| v8 | 字幕+音画同步修复+矩阵表 | ✅ 最终交付 |

**审核工具：**
- 逐段对比：`ffprobe` 获取每段TTS和视频的精确时长
- 偏差检查：每段TTS vs 视频时长差 > 0.5s 即标记为问题段
- 画面检查：播放时逐段确认画面内容与台词匹配

---

## 资源文件

### references/
- `sucuang_api.md` — 速创API完整接口文档和踩坑经验
- `production_workflow.md` — 制作流程详细参考

### scripts/
- （按需添加：批量提交脚本、合成脚本模板等）

### assets/
- （按需添加：字幕模板、片头片尾素材等）
