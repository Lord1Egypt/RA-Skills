---
name: ai-short-film-studio
version: 3.0.0
description: 低成本AI短剧/短片全流程制作技能。三套制作路线：①速创API+Grok Imagine直出视频（¥30-50/部）；②可灵Kling V3+Gemini Image图生视频（¥80-120/部）；③Google Flow Omni Flash免费批量文生视频（¥0/部，Chrome CDP自动化）。包含分镜脚本创作、角色参考图生成、Chrome CDP网页自动化批量生产、五层Prompt公式、视觉一致性管理、音频驱动剪辑、三层音频(旁白+SFX+BGM)、字幕叠加、审片迭代的全套SOP。适用于AI短片、短剧EP、预告片、科普视频等场景。
agent_created: true
---

# AI Short Film Studio — 低成本AI短剧制作工坊 v3.0

## 概述

本Skill提供三套完整的**低成本AI短剧制作流程**，覆盖从脚本到成片的全链路。

### 三套制作路线

| 路线 | 视频方案 | 出图 | TTS | 成本 | 适用 |
|------|---------|------|-----|------|------|
| **路线A: 速创直出** | Grok Imagine 文生视频 | 无独立出图 | 速创TTS | ¥30-50/部 | 快速出片、试验性内容 |
| **路线B: 可灵精制** | 可灵Kling V3 图生视频 | Gemini Image | edge-tts 免费 | ¥80-120/部 | 连续剧集、高质量要求 |
| **路线C: Flow免费** | Google Flow Omni Flash 文生视频 | Nano Banana 2 | edge-tts 免费 | **¥0/部** | 免费、Chrome CDP自动化 |

**触发词：**
- "帮我做一个短片/短剧/预告片"
- "把这段文案做成视频"
- "生成一个XX题材的短视频"
- "制作XX系列第N集"

---

## 制作流程总览（不可跳步⚠️）

```
Step 0: 世界观管理（系列剧必做）
  ├── world-bible.md（世界状态变化）
  └── characters.md（角色设定存档）

Step 1: 剧本与分镜创作
  ├── 确定主题/风格/时长
  ├── 旁白文本写作（每段≤15秒）
  ├── 详细分镜表（narration.json格式）
  └── 用户审旁白+分镜

Step 2: 素材生成（路线A/B/C三选一）
  ├── 路线A: Grok Imagine直出视频
  ├── 路线B: Gemini Image出图 → 可灵图生视频
  └── 路线C: Google Flow Omni Flash免费文生视频（Chrome CDP自动化）⭐

Step 3: TTS配音生成
  ├── 路线A: 速创API audio_tts
  ├── 路线B: edge-tts（免费）
  └── 逐段试听，修复断词

Step 4: 音频驱动剪辑
  ├── 逐段按TTS时长裁剪/适配画面
  └── 输出分段视频

Step 5: 字幕生成
  ├── Pillow透明PNG → FFmpeg overlay
  └── 输出带字幕分段

Step 6: 三层音频合成
  ├── 旁白(1.0) + SFX(0.8-2.0) + BGM(0.18)
  └── 音视频合并

Step 7: 审片迭代
  ├── 用户审片 → 逐点修改 → 增量迭代
  └── 至P0=0, P1≤2 → 交付

Step 8: 素材导出与成本核算
```

⚠️ **铁律：不可跳步。** 跳过Step 2分镜和Step 7审片环节，质量会崩塌，返工成本远超正规流程。

---

## Step 0: 世界观管理（系列剧必须）

连续剧集项目必须维护两个核心文件：

### world-bible.md
记录每集发生后的世界状态变化。用于后续集数出图时保证世界观一致性。

```markdown
# 世界观圣经

## 当前集数: E03
## 时间线状态
- 地球已启程XX年
- 太阳状态: [膨胀期/红巨星/氦闪后]
- 地表状态: [冰冻/解冻/...]

## 关键事件记录
- E01: ...
- E02: ...
```

### characters.md
角色设定存档，每集更新角色状态和prompt锚定词。

```markdown
# 角色设定

## 主角
- 锚定词: "Chinese man in his 20s, round face, large dark eyes, short black hair"
- E01状态: ...
- E02状态: ... 
- 标杆图: references/char_main_v3.png
```

**锚定词使用：** 每张涉及人物的出图prompt必须包含characters.md的锚定词，防止AI画出不同长相。

---

## Step 1: 剧本与分镜创作

### 1.1 旁白写作规则

- 每段旁白控制在 **15秒以内**（约60字）
- 超过15秒必须拆段，每段配独立画面
- 避免TTS容易断错的词组：
  - ❌ "小行星带的战斗" → ✅ "小行星带，的战斗"
  - ❌ "天体物理学家" → ✅ "天体物理，学家"

### 1.2 分镜表格式（narration.json）

每段必须包含完整的叙事信息：

```json
{
  "id": "S05",
  "type": "narration",
  "text": "旁白文本（≤15秒）",
  "shots": [
    {
      "id": "05a",
      "type": "大远景",
      "desc": "具体画面描述",
      "motion": "slow push in",
      "mode": "single",
      "duration": "5s",
      "ref": "references/earth.png"
    }
  ],
  "note": "叙事意图"
}
```

**段落类型：**
| 类型 | 用途 |
|------|------|
| `text_card` | 黑底白字，开场/结语/标题 |
| `pause` | 黑屏静默，情绪过渡 |
| `narration` | 旁白+画面，正文 |

### 1.3 分镜设计原则

- **每段旁白至少2个镜头**（<5s的短段除外）
- **相邻镜头不共用插画**
- **景别要有变化**：远景→中景→特写交替，避免连续3个同景别
- **每个镜头有明确叙事任务**——不是为了好看，是为了推进故事
- **长旁白（>8s）必须拆成多段**，每段配独立画面

### 1.4 景别速查

| 景别 | 用途 | 示例 |
|------|------|------|
| 大远景 | 环境交代、渺小感 | 地球在太空中 |
| 远景 | 场景全貌 | 地下城广场 |
| 中景 | 人物+环境 | 父子在餐桌旁 |
| 近景 | 人物表情 | 面部特写 |
| 特写 | 情感聚焦/细节 | 勋章、手 |

---

## Step 2: 素材生成（双路线）

### 路线A: 速创API — Grok Imagine直出视频（快速低成本）

**适用：** 快速出片、试验性内容、预算敏感项目

**API平台：** https://api.wuyinkeji.com
**注册链接：** https://api.wuyinkeji.com/user/register?cps=UXPjoCgN

**价格：** ¥0.05/秒（按生成视频时长计费）

**API调用方式：**
- 鉴权：Authorization Header 传API Key（不带Bearer前缀）
- 接口：POST /api/async/video/grok_imagine
- 参数：扁平JSON
- 查询：GET /api/async/detail?id=xxx（轮询直到status=2）

**批量生成策略：**
1. 所有镜头同时提交（ThreadPoolExecutor）
2. 每个镜头约10秒，生成约30-60秒
3. 失败自动重试（平均3次）
4. ⚠️ Sora2接口已弃用（持续400错误）

**Prompt要点：** 英文效果更稳定，包含场景、光线、构图、镜头运动。

---

### 路线B: 可灵Kling V3 — 图生视频（高质量精制）

**适用：** 连续剧集、高质量要求项目

**工具链：** Gemini Image (Nano Banana Pro) 出图 → 可灵Kling V3 图生视频

**API：** https://api-beijing.klingai.com/v1/videos/image2video
**鉴权：** JWT (HS256, iss=AK, exp=30min)
**并发限制：** 3个任务同时

#### B.1 五层Prompt公式（出图/运镜通用）

每张图/每个运镜prompt必须包含五层，缺一不可：

```
① 通用风格前缀（style-bible.md 的风格描述）
② 一致性约束（视觉一致性清单中对应元素的描述，逐条写入）
③ 叙事意境（镜头在故事中的位置、情节背景、角色情绪）
④ 画面描述（构图、机位、光影、材质、色彩）
⑤ 情绪/氛围关键词
```

⚠️ **踩坑教训：** 只写①④⑤跳过②③ → 发动机比例错、防护服缺失、人种错。五层缺一不可。

#### B.2 视觉一致性管理

出图前必须检查：

**一致性清单（逐条对照）：**

| 元素 | 标杆图 | Prompt约束 | 常见错误 |
|------|--------|-----------|---------|
| 人物 | characters.md或标杆图 | 必须含"Chinese"（日本角色用"Japanese"） | 出西方面孔 |
| 核心场景 | 前集标杆图 | 外观/比例/材质必须一致 | 发动机比例错 |
| 关键道具 | 前集标杆图 | 形状/颜色/尺寸 | 勋章画成铁十字 |
| 环境特征 | world-bible.md | 时间线对应的环境状态 | 冰冻地球画成绿地 |

**出图执行流程：**
1. 读分镜表该镜头描述
2. 查一致性清单：画面涉及哪些元素？
3. 找到对应标杆参考图路径
4. 组装五层prompt
5. 用 `-i` 传入标杆参考图（最多2-3张）
6. 生成3版，自审时逐条对照清单
7. 不达标的不发用户，直接重做

**Prompt示例（完整五层）：**
```
[①风格] Cinematic photorealistic, 2K, 16:9, cold blue-gray palette
[②一致性] Five-pointed star medal with flat broad points, hammer and sickle emblem, aged dark gunmetal, ~4cm, short frayed olive ribbon
[③叙事] Father silently pins his medal on his son's chest before the final mission — a wordless passing of duty
[④画面] Extreme close-up, father's weathered hands holding the medal, son's dark blue jumpsuit collar visible, soft side lighting casting half-shadow
[⑤关键词] solemn, intimate, bittersweet
```

#### B.3 运镜Prompt规范

必须包含三层信息：

```
[叙事情境] 旁白在说什么，观众应该感受什么
[具体动作] 镜头具体怎么动，什么元素在变化  
[情绪关键词] contemplative / epic / intimate / terrifying
```

**方向敏感必须写明：**
- 物体移动：LEFT / RIGHT / UP / DOWN / TOWARD / AWAY
- 镜头运动：push in / pull back / pan left / tilt up

**禁止通用prompt：**
- ❌ "Slow cinematic camera movement"
- ✅ "Camera slowly pushes in from medium shot of father to close-up of face. Side lamp half-shadow. His lips move, speaking about hope."

#### B.4 首尾帧 vs 单图决策

**问：两张图之间有没有明确的状态变化？**

- 有（门开/关、人跑/停、物体出现/消失）→ 🔴 **单图模式**，绝不用首尾帧
- 无（镜头推进、视角旋转、气氛渐变）→ ✅ 可用首尾帧模式

**时长档位：** 单图 5s/10s | 首尾帧 5s/10s/15s
**选档原则：** 选≥旁白时长的最近档，多出的裁剪。

**时长匹配策略（逐镜头决策）：**

| 情况 | 方案 | 
|------|------|
| 视频 > 旁白 | 裁剪（从开头或结尾） |
| 差 < 15% | 微减速（0.85x-0.96x） |
| 差 > 15% | 微加速(1.1x) + 裁开头 |
| 段落 > 15s | 拆成2-3个独立单图拼接 |
| ❌ 冻结帧 | 禁止 |
| ❌ 循环播放 | 禁止（可灵路线） |

**首尾帧禁忌：**
- ❌ 不能在中间硬切（画面会跳回）
- ❌ 不能用于状态变化场景
- ✅ 可完整播放+微减速匹配旁白

---

### 路线C: Google Flow — Omni Flash 免费文生视频（Chrome CDP自动化）⭐

**适用：** 免费、全自动化、Chrome CDP 网页自动化批量生产

**工具链：** Chrome CDP (port 9222) → Google Flow (labs.google/fx/tools/flow) → Nano Banana 2 出图 + Omni Flash 文生视频

**成本：** ¥0（仅需 Google Flow 免费积分，Omni Flash 15 credits/镜头）

**依赖skill：** `google-flow-automation`（提供 generate-image.js / generate-one.js 核心脚本）

#### C.1 启动 Chrome（CDP 远程调试，一次性）

```bash
pkill -9 "Google Chrome"; sleep 2
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default" \
  "https://labs.google/fx/tools/flow" &
sleep 5
# 手动登录 Google 账号
```

#### C.2 角色参考图生成（Nano Banana 2 文生图）

```bash
cd ~/.workbuddy/skills/google-flow-automation

# 生成角色参考图（每个年龄段生成2张，用户选最佳）
node generate-image.js \
  --prompt "Portrait of a young Chinese man in his 20s, broad face, large dark eyes, short black hair, wearing late Qing dynasty peasant clothing, 1890s era, photorealistic, cinematic lighting" \
  --aspect 16:9 \
  --count x2 \
  --output ./characters
```

⚠️ **角色审核是全流程唯一手工环节。** 用户确认脸型、眼镜、服装、气质后才进入批量视频生成。

#### C.3 分镜脚本格式 (storyboard.json)

```json
[
  {
    "id": 1,
    "title": "片头-厦门大学全景",
    "prompt": "Video of a cinematic aerial view of a historic Chinese university campus at dawn, golden sunlight, photorealistic, cinematic",
    "narration": "在东南沿海的鹭岛，有一座大学，它的故事，要从一个人说起。"
  }
]
```

**关键字段：**
- `id` — 镜头编号（1开始，用于文件命名排序）
- `title` — 镜头标题（中文，用于文件命名 `XX-标题.mp4`）
- `prompt` — **英文**视频提示词，**必须以 `Video of` 开头**（否则生成图片！）
- `narration` — 中文旁白（TTS用）

**角色锚定词（每个涉及人物的镜头必须包含）：**
- 青年：`young Chinese man with broad face, short black hair`
- 中年：`middle-aged Chinese man with broad face and round metal-rimmed glasses`
- 老年：`elderly Chinese man with broad face, white hair and round metal-rimmed glasses`

#### C.4 批量视频生成（核心自动化）

**技术架构：**
```
batch-generate.js (批量调度)
    │
    ├── 逐镜头调用 generate-one.js (google-flow-automation skill)
    │       ├── Chrome CDP 连接 (port 9222)
    │       ├── 页面状态诊断 (DOM检测，非URL判断)
    │       ├── 空状态检测 → 返回主页 → New project
    │       ├── 进入 Scenes 模式 → New session
    │       ├── Agent Settings: Omni Flash + 16:9 + 10s
    │       ├── 填入提示词并提交
    │       ├── 自动点击积分确认 (Yes)
    │       ├── 轮询等待视频生成 (8分钟超时)
    │       ├── page.evaluate fetch 下载 (带Cookie认证)
    │       └── process.exit(0) 强制退出 ★关键
    │
    ├── 断点续传 (检查已完成的 XX-标题.mp4)
    ├── 自动重命名 (video-xxx.mp4 → XX-标题.mp4)
    ├── 写入 progress.json
    └── 失败重试 (最多2次/镜头)
```

**使用模板脚本：**

```bash
# 批量生成（断点续传）
cd ~/.workbuddy/skills/ai-short-film-studio/scripts
NODE_OPTIONS="" node batch-generate.js \
  --script /path/to/storyboard.json \
  --output /path/to/videos \
  --name "我的短剧"

# 持续重试直到全部完成（最多10轮）
NODE_OPTIONS="" node retry-until-complete.js \
  --script /path/to/storyboard.json \
  --output /path/to/videos \
  --name "我的短剧"
```

#### C.5 关键踩坑与修复（v6 → v8.2，血泪经验）

| 问题 | 修复方案 | 版本 |
|------|---------|------|
| 提示词不以 `Video of` 开头 → 生成图片 | 脚本自动添加前缀 | v6 |
| DOM搜索找不到模型按钮 | 用坐标点击 `page.mouse.click(825, 868)` | v6 |
| 提示词被当聊天消息 | 每次生成前点 New session | v6 |
| 内联模型选择器不存在（Scenes模式由Settings控制） | 步骤⑤.5自动跳过 | v7 |
| 生成超时6分钟不够 | 增加到8分钟 | v7 |
| **CDP WebSocket导致进程不退出** ★ | `finally` 块末尾 `process.exit(0)` | v7→v8 |
| URL不含 `/project/` 误判页面状态 | 用DOM状态（导航栏/输入框）判断 | v8 |
| Chrome被重定向到其他网站 | 自动导航回 Flow | v8.1 |
| 空状态页面 "doesn't seem to be anything here" | 检测→返回主页→创建项目 | v8.2 |
| `--use-system-ca is not allowed` 错误 | `NODE_OPTIONS=""` 清空环境变量 | — |
| `execSync` 输出被缓冲 | 改用 `spawnSync` + `stdio: 'inherit'` | — |

#### C.6 Google Flow 队列机制

- 高需求时视频排队：`"scheduled and is waiting in the queue due to high demand"`
- 排队时间不可预测（30秒~5分钟）
- **超时后视频可能仍会生成完成** → 超时后必须检查新文件
- **应对策略：** batch-generate.js 超时后检查文件 + retry-until-complete.js 持续重试

#### C.7 路线C的TTS/字幕/合成

路线C使用与路线B相同的 TTS（edge-tts）和字幕（Pillow）方案，但通过 `compose-video.py` 模板脚本一键完成：

```bash
python3 ~/.workbuddy/skills/ai-short-film-studio/scripts/compose-video.py \
  --base /path/to/project \
  --storyboard /path/to/storyboard.json \
  --output /path/to/最终成片.mp4 \
  --voice zh-CN-YunjianNeural \
  --rate -5%
```

该脚本自动完成5步：TTS生成 → 字幕PNG → 逐段合成 → 背景音乐 → 最终混音。

---

## Step 3: TTS配音生成

### 路线A: 速创API audio_tts

**接口：** POST /api/async/audio_tts
**价格：** ¥0.0006/字

```json
{
  "text": "台词内容",
  "voice_id": "male-qn-jingying",
  "speed": 1.0
}
```

**注意事项：**
- ❌ 不传 format 参数（500错误）
- ❌ 不嵌套 `{"model":"audio_tts","params":{...}}`
- ✅ status=2 完成
- ⚠️ 卡住重试换IP节点
- ✅ 返回tar包需解压

### 路线B: edge-tts（免费）

```python
import edge_tts
comm = edge_tts.Communicate(text, "zh-CN-YunjianNeural", rate="0%")
await comm.save(output_path)
```

### TTS断词修复技巧

| 方法 | 场景 | 示例 |
|------|------|------|
| 加逗号 | 复合名词 | "小行星带，的战斗中" |
| 加顿号 | 并列词 | "绕着太阳、转十五个圈" |
| 改措辞 | 逗号也不行时 | "绕着太阳转"→"围绕太阳飞行" |
| 出3版选 | 不确定时 | 3种标点各出，听完选 |

### 音色速查表

| 角色类型 | 速创API | edge-tts |
|---------|---------|----------|
| 旁白/叙述者 | male-qn-jingying | zh-CN-YunjianNeural |
| 男主角 | male-qn-jingying | zh-CN-YunxiNeural |
| 霸道/硬汉 | male-qn-badao | — |
| 反派/俊朗 | junlang_nanyou | — |
| 成熟女性 | female-chengshu | zh-CN-XiaoxiaoNeural |
| 少女 | female-shaonv | zh-CN-XiaoyiNeural |
| 学生 | male-qn-daxuesheng | — |
| 醇厚长辈 | male-chunhou | — |

---

## Step 4: 音频驱动剪辑

**核心理念：** 画面长度由语音旁白决定。先确定TTS节奏，再裁剪画面适配。叙事节奏由台词自然驱动。

### 节奏控制逻辑

```
每段(镜头, TTS)的处理：

1. ffprobe获取TTS实际时长 tts_dur
2. ffprobe获取源视频时长 src_dur
3. 决策：
   ├── src_dur ≥ tts_dur+0.5s  → 直接裁剪到tts_dur
   ├── src_dur ≈ tts_dur       → 直接裁剪
   └── src_dur < tts_dur       → stream_loop循环（路线A）/ 减速+冻结末帧（路线B）
4. 输出：seg_NNN.mp4（精确匹配配音时长）
```

### 路线A专用：stream_loop循环填充

```bash
ffmpeg -y -stream_loop -1 -i shot.mp4 -t {tts_dur} -c:v libx264 -preset fast seg.mp4
```
循环1-2次视觉重复感不明显，超过3次建议换镜头。

### 路线B专用：逐镜头适配策略

- **减速拉伸**：适合本身该慢的镜头，setpts调速
- **冻结末帧**：`tpad=stop_mode=clone:stop_duration=Xs`，适合末尾自然静止
- **两段拼接**：拆成两个独立视频，各有自己的运动
- ❌ 禁止循环播放（观感差）
- ❌ 尾帧静止超过2s（观众感知"卡住了"）

### 逐段精确裁剪（避免累积漂移）

```python
cumulative = 0.0
for i, (tts_file, shot_file) in enumerate(segments):
    tts_dur = get_duration(tts_file)
    trim_video(shot_file, tts_dur, f"seg_{i:03d}.mp4")
    cumulative += tts_dur
# 验证：sum(seg) ≈ audio_concat ≈ final
```

**FFmpeg路径：** `/opt/homebrew/bin/ffmpeg`
**已知限制：** FFmpeg 8.x 无drawtext/libass，用Pillow替代字幕

---

## Step 5: 字幕生成

**方案：** Pillow生成透明PNG → FFmpeg overlay叠加

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGBA', (1920, 160), (0,0,0,0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 48)

draw.text((960, 80), "台词文本", fill='white', font=font, 
          anchor='mm', stroke_width=3, stroke_fill='black')

ffmpeg -i seg.mp4 -i sub.png -filter_complex "overlay=0:H-h" output.mp4
```

**字幕设计规范：**
- 底部居中，距底部60px
- 白色 + 3px黑色描边，字号48-56px
- STHeiti Medium字体（macOS: `/System/Library/Fonts/STHeiti Medium.ttc`）
- 按句号（。！？）拆分，超20字自动换行
- 可加角色标签（"旁白："、"汪淼："）

---

## Step 6: 最终合成

### 三层音频设计

| 层级 | 音量 | 说明 |
|------|------|------|
| 旁白 | 1.0 | 最上层，永远最清晰 |
| SFX | 0.8-2.0 | 中层，按场景调整 |
| BGM | 0.18 | 底层，fade in 4s / fade out 5s |

### 视频参数

- 帧率：统一24fps（`-r 24`）
- 编码：libx264, CRF 22, yuv420p
- 分辨率：1920x1080
- 音频：AAC 128kbps 44100Hz stereo

### 拼接与合并

```bash
# 拼接视频
for f in seg_*.mp4; do echo "file '$f'" >> video_list.txt; done
ffmpeg -f concat -safe 0 -i video_list.txt -c copy video_concat.mp4

# 拼接音频
for f in audio_*.mp3; do echo "file '$f'" >> audio_list.txt; done
ffmpeg -f concat -safe 0 -i audio_list.txt -c copy audio_concat.aac

# 合并
ffmpeg -i video_concat.mp4 -i audio_concat.aac \
  -c:v copy -c:a aac final.mp4
```

### BGM处理

- 视频比BGM长时：用volumedetect找高潮段
- BGM衰减前用3s交叉淡入淡出（acrossfade）接回高潮起点
- 接缝在同能量自然节拍处
- 片尾让BGM自然衰减

---

## Step 7: 审片迭代流程

### 7.1 审核维度

| 维度 | 检查内容 | 常见问题 |
|------|---------|---------|
| **音画同步** | 画面匹配配音 | 角色A说话但画面是角色B |
| **时长匹配** | 视频完整覆盖TTS | 话没说完画面就切 |
| **视觉一致性** | 人物/场景/道具一致性 | 同角色不同集长相不同 |
| **字幕准确** | 字幕与TTS一致 | 错别字、标点 |
| **节奏感** | 叙事节奏流畅 | 某段拖沓/仓促 |
| **画面质量** | 无AI瑕疵 | 人物变形、闪烁 |
| **物理方向** | 运动方向正确 | 发动机喷射方向错 |
| **视觉重复** | 无明显循环 | 超过3次循环 |

### 7.2 物理方向检查清单（科幻/动作类必查🔴）

- [ ] 发动机喷射朝太阳方向（推地球远离太阳）
- [ ] 地球飞行远离太阳（太阳在背后变小）
- [ ] 传送带向内输送
- [ ] 人物移动方向符合场景逻辑
- [ ] 镜头运动方向一致

### 7.3 迭代规则

```
V1（初版合成）
  ↓
逐段审核（8个维度）
  ↓
问题清单按严重程度排序
  ├── P0（必须修）：音画不匹配、字幕错误、一致性崩塌
  ├── P1（建议修）：节奏拖沓、视觉重复>3次
  └── P2（可优化）：色调、画面质量
  ↓
V2（修复P0）→ 再次审核 → V3...
  ↓ 直到 P0=0, P1≤2
最终交付
```

### 7.4 增量迭代（关键效率技巧）

- 每个版本视频片段独立存储（`v7_S05.mp4`, `v8_S05.mp4`）
- 维护两个集合：`MUST_REGEN`（需重做）和 `REUSE`（可复用）
- MUST_REGEN优先级高于REUSE
- 每轮只改几段，其余复用，几分钟出新版
- **铁律：** 用户确认OK的段落不再动；不自作主张改其他段落

### 7.5 提交给用户的材料

- 压缩版视频预览（<50MB）
- 完整分镜时间线表（时间→段落→画面→改动标注）
- 高清版路径

---

## Step 8: 素材导出与成本核算

### 桌面文件夹结构

```
~/Desktop/项目名称/
├── 01_字幕/     → 字幕PNG
├── 02_配音/     → TTS音频
├── 03_主图/     → 镜头缩略图
├── 04_视频/     → 分段视频
├── 05_矩阵表/   → 矩阵表.html + 素材结构.json
└── 最终成片.mp4
```

### 项目文件结构（连续剧集）

```
项目根目录/
├── scripts/E{XX}/
│   ├── narration.json           # 分镜叙事结构
│   ├── motion_prompts.json      # 运镜prompt
│   ├── produce_e{XX}_v{N}.py   # 生产脚本（每版一个）
│   └── generate_tts.py          # TTS批量生成
├── images/E{XX}/                # 插画（所有版本+标杆图）
├── audio/E{XX}/
│   ├── narration_v{N}/          # TTS + durations.json
│   └── bgm-*.mp3
├── output/E{XX}/                # 视频片段（按版本前缀）
├── storyboard/E{XX}/            # 分镜表
├── references/                  # 标杆参考图
├── style-bible.md               # 风格圣经
├── characters.md                # 角色设定
├── world-bible.md               # 世界观圣经
└── PRODUCTION_HANDBOOK.md       # 本手册
```

### 成本核算

**路线A（速创直出）：**

| 项目 | 计算方式 | 参考单价 |
|------|---------|---------|
| Grok Imagine视频 | 总秒数 × 重试 × ¥0.05 | ¥0.05/秒 |
| TTS配音 | 总字数 × ¥0.0006 | ¥0.0006/字 |
| 合计 | — | **¥30-50/部** |

**路线B（可灵精制）：**

| 项目 | 计算方式 | 参考单价 |
|------|---------|---------|
| Gemini Image出图 | ~70张 × 2版 = 140张 | ~$0.134/张 |
| 可灵视频 | ~35个片段 | ~¥3/个 |
| BGM (Suno等) | — | ~¥10 |
| TTS | 免费(edge-tts) | ¥0 |
| 合计 | — | **¥80-120/部** |

**路线C（Google Flow免费）：**

| 项目 | 计算方式 | 参考单价 |
|------|---------|---------|
| Nano Banana 2 出图 | ~3张角色参考图 | ~5 credits/张 |
| Omni Flash 视频 | 25镜头 × 15 credits | 15 credits/镜头 |
| TTS | edge-tts 免费 | ¥0 |
| BGM | FFmpeg 生成 | ¥0 |
| 合计 | — | **¥0**（仅需Google Flow免费积分） |

---

## 关键设计原则

### 叙事意境驱动Prompt（核心方法论）

不只是描述画面，要把故事背景+情节+情绪融入prompt。这是出图质量飞跃的关键。

### 分镜设计是专业活

运镜、画面动态、镜头语言这些专业决策要主动做好，不能等用户指出。

### 极简有时更强

不要堆砌。简单有力的画面比复杂冗余的画面更有情感冲击力。

### 用户认可的版本别再改

过度优化是陷阱。用户确认OK → 不动。

### 每个镜头有自己的叙事任务

不套模板，不用一张好图的风格去套另一张。

---

## 平台速查

### 速创API
- 平台：https://api.wuyinkeji.com
- 注册：https://api.wuyinkeji.com/user/register?cps=UXPjoCgN
- 文档：https://api.wuyinkeji.com/doc
- 鉴权：Authorization Header (无Bearer前缀)

| 模型 | 价格 | 说明 |
|------|------|------|
| Grok Imagine 视频 | ¥0.05/秒 | 文生/图生视频，6-15秒 |
| audio_tts | ¥0.0006/字 | 多音色TTS |
| video_digital_humans | 按次 | 数字人视频 |
| ~~Sora2~~ | — | 已弃用(400错误) |

### 可灵Kling V3
- API：https://api-beijing.klingai.com/v1/videos/image2video
- 鉴权：JWT (HS256, iss=AK, exp=30min)
- 域名：api-beijing.klingai.com（国内版）
- 并发：3任务同时

| 模式 | 时长 | 适用 |
|------|------|------|
| 单图 | 5s/10s | 短镜头、静态场景 |
| 首尾帧 | 5-15s | 有叙事连续感 |

### Google Flow（路线C，免费）
- 网址：https://labs.google/fx/tools/flow
- 鉴权：Google 账号登录（Chrome CDP 自动化）
- 依赖skill：`google-flow-automation`（generate-image.js / generate-one.js）

| 模型 | 用途 | 积分 | 说明 |
|------|------|------|------|
| Nano Banana 2 | 文生图 | ~5 credits/张 | 角色参考图 |
| Omni Flash | 文生视频 | 15 credits/条 | 10秒/条，16:9或9:16 |

**关键限制：**
- Chrome 必须以 `--remote-debugging-port=9222` 启动
- 提示词必须以 `Video of` 开头（否则生成图片）
- 每次生成前必须 New session（否则提示词被当聊天）
- 高需求时排队等待（30秒~5分钟）
- `process.exit(0)` 必须加（CDP WebSocket不释放）

---

## 实战案例

### 案例1：三体EP1（路线A）
- 25镜头，127秒成片，8角色
- 成本：¥44.17
- 工具链：Grok Imagine × 25 + 速创TTS × 25 + FFmpeg + Pillow
- 迭代：v5min → v6 → v7 → v7.1 → v8（5版）
- 关键经验：Sora2不可用、stream_loop循环、FFmpeg 8.x无drawtext

### 案例2：流浪地球E01（路线B）
- 迭代：v6→v11（6轮），用户满意
- 经验：走完全流程的质量远超跳步流程
- 核心差异：E01每段2.1镜头(87%多镜头) vs E02只有1个(100%单镜头)

### 案例3：《阿公的故事》陈嘉庚（路线C）⭐
- 25镜头，2分42秒成片，3个年龄段角色
- 成本：¥0（Google Flow 免费积分，约540 credits含重试）
- 工具链：Chrome CDP → Nano Banana 2 出图 + Omni Flash 文生视频 × 25 + edge-tts × 25 + FFmpeg + Pillow
- 全自动化：仅角色参考图审核为手工，其余全部自动化
- 关键修复历程：v6（模型选择失败）→ v7（内联选择器不存在）→ v8（URL误判）→ v8.1（Chrome被重定向）→ v8.2（空状态页面）
- 最关键修复：`process.exit(0)` 解决 CDP WebSocket 导致进程不退出
- 文件：`scripts/batch-generate.js`、`scripts/retry-until-complete.js`、`scripts/compose-video.py`

---

## 资源文件

### references/
- `sucuang_api.md` — 速创API完整接口文档和踩坑经验
- `production_workflow.md` — 制作流程详细参考

### scripts/（路线C模板脚本）
- `batch-generate.js` — Google Flow 批量视频生成（断点续传+自动重试+自动重命名）
- `retry-until-complete.js` — 持续重试包装脚本（最多10轮，应对Flow队列拥堵）
- `compose-video.py` — TTS+字幕+背景音乐一键合成（edge-tts + Pillow + FFmpeg）

### assets/
- 按需添加：字幕模板、片头片尾素材
