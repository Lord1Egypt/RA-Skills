---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100eebc155dae2d5c8f31401b642391494516d5208bf8e92735508c06634d9e28e3022100be14e766a0954c64fb0118ca6a5f8ca12f0b92ca82b2fe91921ba67bb07d1a6e
    ReservedCode2: 3046022100a06382f12975c56bcbbec487df626f5a3317e7af7489d0b1288152357461dfe1
description: FMT肠菌移植科普视频制作工具（视频合成+字幕+SRT+配音TTS+片头片尾）。将静态图片/动态视频素材合成为完整科普视频，支持中文字幕、旁白配音、片头片尾合成。触发词：合成视频/添加字幕/视频配音/制作FMT视频。
name: fmt-video-production
version: 1.0.0
---

# FMT视频制作技能 v1.0

> 将图片素材合成为完整FMT科普视频
> **v1.0（2026-05-12）：视频合成+字幕+配音+片头片尾全流程**

---

## 工具说明

| 工具 | 用途 |
|------|------|
| `gen_videos`（T2V模式）| 根据Prompt生成片头/片尾视频片段 |
| `batch_text_to_video` | 批量生成短视频片段（片头/过渡/片尾） |
| `tts` | 中文旁白配音（文字转语音） |
| `exec`（ffmpeg）| 视频合成、字幕烧录、音画同步 |

---

## 一、输入素材规范

### 标准输入格式
```
/workspace/fmt_pages/p[NN]_[主题]/
├── static.png          ← 4K静态插画（原图）
├── HD.mp4              ← 1080P动态视频（已有字幕）
└── metadata.json       ← 页面元数据
```

### 素材文件检查清单
```
[ ] static.png 存在且 ≥ 4K分辨率
[ ] HD.mp4 存在且为1080P/6秒
[ ] 有对应解说词文本（用于配音）
[ ] 有字幕内容（用于SRT）
[ ] 片头视频已生成（用于合成）
```

---

## 二、片头视频生成（可选，推荐使用）

**片头规格：6秒，1080P，统一风格**

**生成命令（gen_videos T2V模式）：**
```javascript
gen_videos({
  video_requests: [{
    duration: 6,
    output_file: "/workspace/fmt_video_intro.mp4",
    prompt: "A dramatic medical science intro animation. Soft blue-white gradient background. Large Chinese characters '肠菌移植' slowly fade in with golden glow effect. Animated medical icons (DNA helix, gut cross-section, bacteria) twinkle and rotate gently. Warm friendly atmosphere, high quality 1080P. Subtle light particles float upward. Duration 6 seconds, cinematic feel.",
    resolution: "1080P"
  }]
})
```

**片头Prompt库（直接使用）：**
```
[片头A - 主题引入型]
A gentle fade-in opening. Blue gradient background. Chinese title "肠菌移植" in elegant white font fades in with golden glow. Animated gut icon rotates slowly. Medical bacteria icons float gently. Warm scientific atmosphere. 1080P, 6 seconds.

[片头B - 人物引入型]
A chibi doctor character waves and smiles at camera. City hospital background fades in. Title "肠菌移植科普" appears with soft bounce animation. Bubbles and light particles rise. Friendly educational tone. 1080P, 6 seconds.
```

---

## 三、中文配音（TTS）

**工具**：`tts` — 直接生成音频，自动发送

### 配音生成命令
```javascript
tts({ text: "[完整解说词，最多500字/段]" })
```
> 音频自动生成并发送，回复写 NO_REPLY

### 分段配音规则
- 每段 ≤ 500字（中文），超过则自动分段
- 段间停顿：约1秒（自动处理）
- 语速：正常（1.0x）
- 推荐每张图配一段（6秒视频对应约80-120字配音）

### 解说词编写规范
```
[原则]
- 每句话 ≤ 20字，便于TTS自然表达
- 医学术语加停顿："肠 | 菌 | 移 | 植" 而非 "肠菌移植"
- 避免歧义读音："重于" vs "终于" → 明确写"不同于"
- 数字读法：10% → "百分之十"，3期 → "第三期"

[示例 - 页面1肠菌移植概述]
"欢迎来到肠菌移植科普。今天我们了解一种创新的治疗方法。它通过重建肠道菌群，帮助恢复健康。让我们开始吧。"
```

---

## 四、字幕文件制作（SRT格式）

### SRT格式说明
```
序号
开始时间 --> 结束时间
字幕内容

（空行）

序号
开始时间 --> 结束时间
字幕内容
```

**时间码格式**：`时:分:秒,毫秒`（例如 `00:01:23,456`）

### 自动生成SRT脚本

在 `/workspace/scripts/fmt_make_srt.py`：
```python
#!/usr/bin/env python3
"""自动生成SRT字幕文件"""
import sys

def make_srt(time_start, time_end, index, text):
    """生成单条字幕"""
    def fmt(t):
        ms = int((t - int(t)) * 1000)
        s = int(t) % 60
        m = (int(t) // 60) % 60
        h = int(t) // 3600
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{index}\n{fmt(time_start)} --> {fmt(time_end)}\n{text}\n\n"

# 示例：为6秒视频生成3条字幕
# 每条字幕持续2秒
lines = [
    make_srt(0.0, 2.0, 1, "肠菌移植"),
    make_srt(2.0, 4.0, 2, "重建肠道健康"),
    make_srt(4.0, 6.0, 3, "苏州市立医院"),
]
srt_content = "".join(lines)
with open("/workspace/fmt_01.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)
print("SRT生成完成: /workspace/fmt_01.srt")
```

### 实际SRT生成命令
```bash
# 方式A：用Python脚本生成
cd /workspace
python3 -c "
def fmt(t):
    ms = int((t - int(t)) * 1000)
    s = int(t) % 60
    m = (int(t) // 60) % 60
    h = int(t) // 3600
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

subtitle_lines = [
    (0.0, 2.0, '欢迎了解肠菌移植'),
    (2.0, 4.0, '重建肠道微生态平衡'),
    (4.0, 6.0, '苏州市立医院肠菌移植医学中心'),
]

with open('/workspace/fmt_s01.srt', 'w', encoding='utf-8') as f:
    for i, (s, e, text) in enumerate(subtitle_lines, 1):
        f.write(f'{i}\n{fmt(s)} --> {fmt(e)}\n{text}\n\n')
print('Done')
"
```

---

## 五、ffmpeg视频合成命令

### 检查ffmpeg是否可用
```bash
ffmpeg -version 2>&1 | head -1
```
- 输出版本号 → 可用
- command not found → 切换备选方案（见降级策略）

### 场景1：视频+字幕合成（推荐）
```bash
ffmpeg -i /workspace/fmt_pages/p01_肠菌移植概述/HD.mp4 \
  -vf "subtitles=/workspace/fmt_s01.srt:force_style='FontName=Noto Sans CJK SC,FontSize=36,PrimaryColour=\&HFFFFFF,Outline=2,Bold=1'" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a copy \
  /workspace/fmt_pages/p01_肠菌移植概述/final.mp4
```
> ⚠️ 若视频已有内置音轨，使用 `-c:a aac -b:a 192k` 重新编码

### 场景2：视频+配音合成（音画同步）
```bash
ffmpeg -i /workspace/fmt_pages/p01_肠菌移植概述/HD.mp4 \
  -i /workspace/fmt_01_audio.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  /workspace/fmt_pages/p01_肠菌移植概述/final_with_audio.mp4
```

### 场景3：视频+字幕+配音全合成
```bash
ffmpeg -i /workspace/fmt_pages/p01_肠菌移植概述/HD.mp4 \
  -i /workspace/fmt_01_audio.mp3 \
  -vf "subtitles=/workspace/fmt_s01.srt:force_style='FontName=Noto Sans CJK SC,FontSize=36,PrimaryColour=\&HFFFFFF,Outline=2,Bold=1'" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  -shortest \
  /workspace/fmt_pages/p01_肠菌移植概述/final_complete.mp4
```

### 场景4：片头+内容视频拼接
```bash
# 先检查片头和内容视频时长
ffprobe -v error -show_entries format=duration -of csv=p=0 /workspace/fmt_video_intro.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 /workspace/fmt_pages/p01_肠菌移植概述/final_complete.mp4

# 拼接（需先安装mkvmerge或用ffmpeg concat）
ffmpeg -f concat -safe 0 -i <(echo "file '/workspace/fmt_video_intro.mp4'"
echo "file '/workspace/fmt_pages/p01_肠菌移植概述/final_complete.mp4'") \
  -c copy \
  /workspace/fmt_pages/p01_肠菌移植概述/full_with_intro.mp4
```

### 字幕样式自定义
```
force_style 参数说明：
FontName=Noto Sans CJK SC     ← 字体（系统需有Noto Sans CJK）
FontSize=36                   ← 字号（1080P推荐36-48）
PrimaryColour=&HFFFFFF        ← 文字颜色（白色&HFFFFFF，十六进制）
Outline=2                     ← 描边宽度（2-3px防遮挡）
Bold=1                        ← 加粗
Alignment=2                   ← 底部居中（2=下方中间）
MarginV=20                    ← 距底部边距（px）
```

---

## 六、工作流程（完整版）

### 标准流程：单页视频制作

```
[输入] 用户提供：页面编号+主题+解说词文本+字幕内容

Step 1: 检查素材
  检查 HD.mp4 是否存在
  检查 static.png 是否存在

Step 2: 生成/确认配音
  调用 tts({ text: "[解说词]" })
  音频保存路径：/workspace/fmt_pages/p[N]_[主题]/narration.mp3
  回复 NO_REPLY

Step 3: 生成SRT字幕
  用Python脚本自动生成SRT文件
  保存路径：/workspace/fmt_pages/p[N]_[主题]/subtitle.srt

Step 4: 视频合成（ffmpeg可用时）
  执行 ffmpeg 命令合并视频+字幕+配音
  输出：/workspace/fmt_pages/p[N]_[主题]/final_complete.mp4

Step 5: 检查输出
  核查：时长、分辨率、音画同步、字幕显示
  检查通过 → 上传CDN → 飞书发送
  检查失败 → 降级处理（见降级策略）

Step 6: 发送结果
  发送视频CDN链接 + 告知内容
```

### 批量流程：多页视频制作

```
[输入] 用户提供：页面列表 [p1,p2,...pN] + 每页解说词

Step 0: 生成片头（仅1次）
  gen_videos → 片头视频 → /workspace/fmt_video_intro.mp4

Step 1: 批量生成配音
  遍历页面列表，逐个调用 tts
  每页生成 narration.mp3

Step 2: 批量生成字幕
  遍历页面列表，逐个生成 SRT 文件

Step 3: 批量视频合成
  遍历页面列表，逐个执行 ffmpeg 全合成

Step 4: 片头拼接
  遍历页面，逐个拼接片头 + 内容视频

Step 5: 汇总报告
  生成汇总报告，包含所有视频CDN链接
```

---

## 七、降级策略

### 降级1：ffmpeg不可用
```
触发：ffmpeg -version 返回 command not found
降级动作：
  ① 尝试安装：apt-get install ffmpeg（或通过其他包管理器）
  ② 若无法安装：仅输出"视频+字幕"或"视频+配音"分开交付
     - 视频文件（HD.mp4）
     - 音频文件（narration.mp3）
     - 字幕文件（subtitle.srt）
     告知用户：用本地视频编辑软件（如剪映/PR）自行合成
```

### 降级2：字幕字体缺失
```
触发：烧录字幕时字体显示异常（方块/乱码）
降级动作：
  ① 更换字体为系统可用字体（用Python Pillow预渲染文字为图片叠加）
  ② 或生成ASS格式字幕（ffmpeg对ASS格式字体支持更好）
  ③ 最终方案：输出 .srt 文件，用户在视频软件中导入
```

### 降级3：音画不同步
```
触发：配音时长与视频时长差异 > 0.5秒
降级动作：
  ① 计算时长差，调整ffmpeg参数
  ② 若配音偏短：用 -af "apad=whole_dur=6" 填充静音
  ③ 若配音偏长：用 -t 6 截断
  ④ 或告知用户视频为静音版，字幕版可自行添加配音
```

---

## 八、输出规范

| 类型 | 路径 | 说明 |
|------|------|------|
| 完整视频 | `fmt_pages/p[NN]/final_complete.mp4` | 含字幕+配音 |
| 仅视频+字幕 | `fmt_pages/p[NN]/final_video_subtitle.mp4` | 无配音 |
| 配音音频 | `fmt_pages/p[NN]/narration.mp3` | TTS音频 |
| 字幕文件 | `fmt_pages/p[NN]/subtitle.srt` | SRT格式 |
| 片头视频 | `/workspace/fmt_video_intro.mp4` | 仅生成1次 |
| 全流程视频 | `fmt_pages/p[NN]/full_with_intro.mp4` | 含片头 |

---

## 九、常用命令速查

```bash
# 检查ffmpeg
ffmpeg -version 2>&1 | head -1

# 视频+字幕（最常用）
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt:force_style='FontName=Noto Sans CJK SC,FontSize=36,PrimaryColour=&HFFFFFF,Outline=2'" -c:v libx264 -preset fast -crf 23 -c:a copy output.mp4

# 视频+配音
ffmpeg -i input.mp4 -i audio.mp3 -c:v copy -c:a aac -b:a 192k -shortest output.mp4

# 视频+字幕+配音
ffmpeg -i input.mp4 -i audio.mp3 -vf "subtitles=subtitle.srt" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 192k -shortest output.mp4

# 拼接片头
ffmpeg -f concat -safe 0 -i <(echo "file 'intro.mp4'"; echo "file 'content.mp4'") -c copy output.mp4
```

---

*更新于：2026-05-12 v1.0 — 视频合成+字幕+配音+片头片尾全流程*