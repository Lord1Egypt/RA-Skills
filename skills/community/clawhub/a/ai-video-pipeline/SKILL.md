---
name: ai-video-pipeline
description: >
  对话式AI短视频创作工具。用户提出想法 → agent 设计脚本 → 人工确认 → 自动制作MP4。
  当用户提到：(1) 做个视频/短视频, (2) AI旁白视频, (3) 认知自述/播客风格视频, (4) 文稿转视频。
  不要在用户仅提到"视频"、"TTS"、"语音"等模糊词时激活（可能是其他需求）。
---

# AI短视频创作管线 v17

从想法到成片的全流程：**用户提出想法 → 脚本设计 → 人工确认 → 自动制作**。

用户只需关注内容创作，所有技术细节（分段、帧数、编码、片段铺满）由 agent 自动处理。

## 🎬 创作工作流（4阶段）

### Phase 1: 需求收集
用户提出想法后，agent 自行判断是否需要补充信息：

**自动判断需要补充的场景：**
- 用户只给了极简描述（"做个关于孤独的视频"）→ 需要补充内容方向、受众、时长偏好
- 用户未指定音色 → 默认使用大因先生（适合旁白/认知类），不用问
- 用户未指定风格 → 默认写实电影质感，不用问
- 用户明确说了完整文稿 → 跳过此阶段，直接进入 Phase 2

**不需要问的：** 音色（默认大因先生）、分辨率（默认720P）、帧率（默认24fps）、字幕样式（默认底部定位+四向描边）、视频片段（默认自动铺满）、**文稿风格（自动匹配，见下文）**
    y_ratio=0.85（底部85%位置，多行向上扩展）
**需要确认的：** 内容方向、目标受众、总时长预期、是否有特殊风格要求

### 📝 文稿风格系统

**目录：** `~/.openclaw/skills/ai-video-pipeline/styles/`

每个风格模板包含：人设、叙事结构、句式模板、范例片段、禁止事项。

**可用风格：**

| 标签 | 风格 | 适用场景 | 语速 |
|------|------|---------|------|
| `cognitive` | 认知拆解 | 职场/社会现象/权力结构/潜规则 | 200-220字/分 |
| `emotional` | 情感共鸣 | 人生感悟/关系/成长/内心独白 | 180-200字/分 |
| `deepread` | 深度解读 | 行业分析/政策/趋势/商业逻辑 | 210-230字/分 |

**自动匹配规则：** 根据用户话题中的关键词自动选择风格（匹配规则见各模板文件头部）。用户也可手动指定。

**使用流程：**
1. 用户给话题 → agent 读取匹配的风格模板
2. 按模板规则先整理「角度与痛点」（表面现象/痛点/角度/不敢说的话/突破方向），发用户确认
3. 确认后用模板的句式模板完全重写文稿（不基于旧稿改）
4. 用户标注哪里不像人话 → 针对性修改，通常2-3轮收敛

**⚠️ 重要：不要跳过角度整理直接写文稿。先整理后确认再写。**

### Phase 2: 脚本设计
agent 根据需求完成脚本设计，输出**完整的制作方案**供用户确认：

**方案格式：**
```
📋 制作方案

📹 整体：约 XX 秒，X 个段落
🎵 音色：大因先生（旁白风格）
🎞️ 动画：即梦AI自动铺满（每个段落一个动画片段）

📝 脚本：
---
[段落1]

[段落2]

[段落3]
---

💰 预估成本：约 ¥X（即梦AI ¥0.28/秒 × 预估总秒数）

确认后开始制作。有修改意见请直接说。
```

**脚本设计规则：**
- 每段 15-35 字（确保单段 ≤ 10s），段落间空行分隔
- 总时长控制在 30-90 秒（短视频最佳区间）
- **不要为每个段落手动写即梦AI prompt** — 自动铺满模式会用段落原文作为 prompt

### Phase 3: 人工确认
- 等待用户明确确认（"可以"、"开始"、"确认"等）
- 用户可提出修改：调整脚本内容、换音色、改风格、增减段落
- 修改后重新展示方案，再次等待确认
- **未确认前不执行任何制作操作**

### Phase 4: 自动制作
确认后，agent 调用 `build_video.py` 一键生成：

```bash
cd /tmp/video-poc && python3 -u ~/.openclaw/skills/ai-video-pipeline/scripts/build_video.py script.txt -o output.mp4
```

**管线自动执行（无需 agent 手动编排）：**
1. **TTS**：播客API 生成语音 + 字幕时间轴（自动缓存 subs.json，重跑跳过）
2. **BGM 混音**：自动选择 BGM（35% 音量，2s 淡入淡出），ffmpeg 混合
3. **即梦AI视频片段**：**每个段落自动生成一个动画片段，铺满整个时长**（用段落原文作 prompt）
4. **视频合成**：预提取帧 + frame_map + 字幕叠加 → MP4
5. 通过飞书发送 MP4 给用户

**⚠️ 耗时较长：即梦AI 串行生成 ~30s/clip，总耗时 = 30s × 段落数 + ~2min合成**

**agent 在制作期间的职责：**
- 执行 `build_video.py` 命令（后台运行）
- 定期 poll 进度，给用户反馈
- 完成后自动发送视频

**发送格式：**
```
🎬 视频制作完成！

时长：XX秒 | 段落：X个 | 大小：XXMB
视觉：即梦AI动画 × N（自动铺满）
成本：约 ¥X
```

## 技术参考

### 环境变量（`~/.config/openclaw/gateway.env`）

| 变量 | 用途 |
|------|------|
| `VOLC_APP_ID` | 火山播客API |
| `VOLC_ACCESS_KEY` | 火山播客API |
| `VOLC_APP_KEY` | 火山播客API |
| `VOLC_ACCESS_KEY_ID` | 即梦AI IAM |
| `VOLC_SECRET_KEY` | 即梦AI IAM |
| `MINIMAX_API_KEY` | MiniMax 音乐生成 |

### 模块结构

```
~/.openclaw/skills/ai-video-pipeline/
├── scripts/
│   ├── build_video.py      # 入口，一键构建（v17）
│   ├── tts.py              # 火山播客API TTS
│   ├── bgm.py              # BGM 选择 + ffmpeg 混音
│   ├── subtitle.py         # 字幕渲染（PIL 底部定位+四向描边）
│   ├── compose.py          # 视频合成（预提取帧 + frame_map）
│   ├── clips.py            # 即梦AI 片段生成编排（调用 jimeng_video）
│   ├── jimeng_video.py     # 即梦AI 文生视频 API 封装
│   └── asr.py              # FunASR 字幕时间轴对齐（原文标点分句）
├── styles/                 # 文稿风格模板（自动匹配）
│   ├── cognitive.md        # 认知拆解（职场/社会现象/潜规则）
│   ├── emotional.md        # 情感共鸣（人生感悟/关系/成长）
│   └── deepread.md         # 深度解读（行业分析/趋势/商业逻辑）
└── bgm/                    # BGM 背景音乐
```

### Python API

```python
from scripts.build_video import build

# ⭐ 推荐：自动铺满模式（每个段落一个动画片段）
output, subs = build(script_text, "output.mp4", work_dir="/tmp/video-poc")
# video_clip_configs 默认 "auto"，自动为每个段落生成即梦AI片段

# 手动指定片段配置（可选，一般不需要）
output, subs = build(
    script_text, "output.mp4",
    video_clip_configs=[
        {"prompt": "描述文字", "mode": "t2v_720p"},
    ]
)

# 仅 TTS + BGM + 字幕（不要动画片段）
output, subs = build(script_text, "output.mp4", video_clip_configs=[])
```

### CLI

```bash
# 自动铺满（默认）
python3 build_video.py script.txt -o output.mp4

# 不生成动画片段
python3 build_video.py script.txt -o output.mp4 --no-clips

# 仅生成音频
python3 build_video.py script.txt --tts-only
```

### 可用音色

| 名称 | ID | 风格 |
|------|----|------|
| **大因先生** | `zh_male_dayixiansheng_v2_saturn_bigtts` | 沉稳旁白（⭐ 默认） |
| 咪仔 | `zh_female_mizaitongxue_v2_saturn_bigtts` | 清新女声 |
| 刘飞 | `zh_male_liufei_v2_saturn_bigtts` | 活力男声 |

### BGM 背景音乐

**策略：本地优先 → MiniMax 动态生成 → 自动复用**

1. **优先本地**：检查 `bgm/` 目录，按风格关键词匹配已有 MP3
2. **无匹配则生成**：调用 MiniMax `music-2.5+` 生成纯音乐（`is_instrumental: true`）
3. **自动复用**：生成的 BGM 自动存入 `bgm/`，下次同风格直接复用

**支持的风格标签：**

| 标签 | 风格 | 默认 prompt |
|------|------|-------------|
| `lofi` | lo-fi chill / 咖啡馆 | lo-fi instrumental, chillhop beat |
| `calm` | 安静 / 沉思 | calm, 轻柔, 简单钢琴+轻鼓点 |
| `dark` | 暗调 / 深沉 / 紧张 | dark ambient, 电影氛围 |
| `uplifting` | 轻快 / 阳光 | 轻快, 阳光, 节奏明快 |
| `piano` | 简约钢琴 | minimal piano, 干净留白 |
| `corporate` | 商务 / 科技感 | 简洁现代 |

**使用方式：**
```python
# 指定风格（本地优先，无匹配则 MiniMax 生成）
output, subs = build(script_text, "output.mp4", bgm_style="lofi")
# 指定 BGM 风格标签（本地优先，无匹配则 MiniMax 生成）

# 自定义 prompt 生成
from bgm import generate_bgm
path = generate_bgm("暗调电子, 中等节奏, 紧张感", style_tag="dark")

# 手动添加本地 BGM
# 下载 MP3 → 放入 bgm/ 目录（文件名包含风格关键词即可自动匹配）
```

**混音参数（已锁定）：**
- 音量：35%（衬托旁白但不抢戏）
- 淡入/淡出：各 2 秒
- 循环播放至音频结束

**MiniMax API 说明：**
- 超时：500 秒（API 请求 + ffmpeg 混音）
- 模型：`music-2.5+`（纯音乐模式）
- API Key：`MINIMAX_API_KEY`（配置在 `gateway.env`）
- 生成耗时：约 30-60 秒
- 无水印记号：`aigc_watermark: false`

### 成本估算

| 时长 | 段落数 | 即梦AI成本 |
|------|--------|-----------|
| 30s | ~5-7 | ¥8-10 |
| 60s | ~10-14 | ¥17-24 |
| 90s | ~15-20 | ¥25-35 |

即梦AI 720P：¥0.28/秒（5秒=¥1.4/clip），串行生成。

### 限制
- 即梦AI帧数范围 121~241（单段 5~10 秒）
- 播客API每轮≤300字
- 即梦AI免费并发限制1（**串行生成**，~30s/clip）
- BGM 目前 2 首本地 + MiniMax 动态生成（本地优先）
