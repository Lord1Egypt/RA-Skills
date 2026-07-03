# HyperFrames Caption & Subtitle Patterns

## Full Workflow: Video → Transcript → Captions

### Step 1: Transcribe

```bash
# From video file
npx hyperframes transcribe talking-head.mp4 --model small

# From audio file
npx hyperframes transcribe narration.wav

# Import existing subtitles
npx hyperframes transcribe existing.srt
npx hyperframes transcribe existing.vtt
```

Output `transcript.json`:
```json
[
  {"id": "w0", "text": "Welcome", "start": 0.5, "end": 0.9},
  {"id": "w1", "text": "to", "start": 0.9, "end": 1.0},
  {"id": "w2", "text": "our", "start": 1.0, "end": 1.15},
  {"id": "w3", "text": "product", "start": 1.15, "end": 1.5},
  {"id": "w4", "text": "launch.", "start": 1.5, "end": 2.0}
]
```

### Step 2: Group Words into Phrases

Group 3-7 words per caption line based on natural pauses and phrase boundaries:

```javascript
// Example grouping logic
const groups = [
  { text: "Welcome to our", start: 0.5, end: 1.15 },
  { text: "product launch.", start: 1.15, end: 2.0 }
];
```

### Step 3: Create Caption Clips

Each caption group becomes a timed element:

```html
<div id="cap-1" class="caption" data-start="0.5" data-duration="0.65" data-track-index="3">
  Welcome to our
</div>
<div id="cap-2" class="caption" data-start="1.15" data-duration="0.85" data-track-index="3">
  product launch.
</div>
```

## Caption Styling

### Standard Bottom-Center (YouTube style)

```css
.caption {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 42px;
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 2px 8px rgba(0,0,0,0.8);
  text-align: center;
  max-width: 80%;
  padding: 8px 16px;
}
```

### Box Background (High contrast)

```css
.caption {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 38px;
  font-weight: 600;
  color: #ffffff;
  background: rgba(0, 0, 0, 0.75);
  border-radius: 8px;
  padding: 12px 24px;
  max-width: 85%;
  text-align: center;
}
```

### Vertical Video Captions (TikTok/Reels style)

```css
.caption {
  position: absolute;
  bottom: 200px; /* Higher up to avoid UI overlays */
  left: 50%;
  transform: translateX(-50%);
  font-size: 48px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 3px 10px rgba(0,0,0,0.9);
  text-align: center;
  max-width: 90%;
  text-transform: uppercase;
  letter-spacing: 1px;
}
```

### Word Highlight (active word colored)

Use per-word spans with GSAP color animation:

```html
<div id="cap-1" class="caption" data-start="0.5" data-duration="1.5" data-track-index="3">
  <span class="word" id="w0">Welcome</span>
  <span class="word" id="w1">to</span>
  <span class="word" id="w2">our</span>
  <span class="word" id="w3">product</span>
</div>
```

```javascript
// Highlight each word as it's spoken
tl.to("#w0", { color: "#ffdd00", duration: 0.01 }, 0.5);
tl.to("#w1", { color: "#ffdd00", duration: 0.01 }, 0.9);
tl.to("#w2", { color: "#ffdd00", duration: 0.01 }, 1.0);
tl.to("#w3", { color: "#ffdd00", duration: 0.01 }, 1.15);
```

## Caption Animation Patterns

### Fade In/Out

```javascript
// Each caption fades in and holds
tl.from("#cap-1", { opacity: 0, duration: 0.15, ease: "power1.out" }, 0.5);
tl.from("#cap-2", { opacity: 0, duration: 0.15, ease: "power1.out" }, 1.15);
```

### Pop Up

```javascript
tl.from("#cap-1", { opacity: 0, y: 20, scale: 0.9, duration: 0.2, ease: "back.out(2)" }, 0.5);
```

### Typewriter (word by word)

```javascript
const words = document.querySelectorAll("#cap-1 .word");
tl.from(words, {
  opacity: 0, duration: 0.05,
  stagger: { each: 0.1 }  // Match actual word timing from transcript
}, 0.5);
```

## Caption Exit Guarantee

Captions MUST disappear when their `data-duration` ends. The framework handles clip visibility based on `data-start` + `data-duration`. No manual exit animation needed for captions — they vanish when their time slot ends.

## Karaoke Effect (Advanced)

For music videos or lyric videos:

```css
.lyric {
  position: relative;
  color: rgba(255,255,255,0.4); /* Unsung = dim */
}
.lyric .highlight {
  position: absolute;
  top: 0; left: 0;
  color: #ffffff; /* Sung = bright */
  clip-path: inset(0 100% 0 0); /* Reveal left-to-right */
}
```

```javascript
// Reveal clip-path synced to word timing
tl.to("#lyric-1 .highlight", {
  clipPath: "inset(0 0% 0 0)",
  duration: 2.0,
  ease: "none" // Linear for natural speech pacing
}, 1.0);
```

## TTS + Caption Chain Workflow

When creating narrated video from scratch:

```bash
# 1. Write script
echo "Welcome to our quarterly review. Revenue grew 42 percent." > script.txt

# 2. Generate speech
npx hyperframes tts script.txt --voice af_heart --output narration.wav

# 3. Transcribe for precise word timing
npx hyperframes transcribe narration.wav

# 4. Use transcript.json in composition for captions
```

This gives pixel-perfect caption sync because Whisper extracts exact timing from the generated audio.

## Caption Text Overflow Prevention

- Set `max-width: 80%` (landscape) or `max-width: 90%` (vertical)
- Use `word-wrap: break-word` for long words
- Keep groups to 3-7 words max
- For languages with long words (German, etc.), reduce font size
- Test with `npx hyperframes inspect` to catch overflow

## Multiple Caption Tracks

For bilingual or multi-speaker:

```html
<!-- Speaker 1 captions (bottom) -->
<div id="speaker1-cap" class="caption speaker-1"
     data-start="0.5" data-duration="2" data-track-index="3">...</div>

<!-- Speaker 2 captions (top) -->
<div id="speaker2-cap" class="caption speaker-2"
     data-start="3.0" data-duration="1.5" data-track-index="4">...</div>
```

---

## 中文字幕适配规则

### 中文字幕 CSS 模板

#### 横版 (1920×1080) 中文字幕

```css
.caption-zh {
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  font-family: "Inter", sans-serif;  /* sans-serif 回退渲染中文 */
  font-size: 42px;
  font-weight: 700;
  color: #ffffff;
  text-align: center;
  max-width: 75%;            /* 中文更宽，限制更严 */
  padding: 12px 28px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.6);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  /* 中文排版关键属性 */
  line-height: 1.5;
  letter-spacing: 0.02em;
  word-break: keep-all;       /* 不在中文词中间断行 */
  overflow-wrap: break-word;
}
```

#### 竖版 (1080×1920) 中文字幕

```css
.caption-zh-vertical {
  position: absolute;
  bottom: 380px;             /* 避开底部平台 UI */
  left: 50%;
  transform: translateX(-50%);
  font-family: "Inter", sans-serif;
  font-size: 48px;           /* 竖版稍大，因为屏幕窄 */
  font-weight: 800;
  color: #ffffff;
  text-align: center;
  max-width: 85%;
  padding: 14px 24px;
  border-radius: 10px;
  text-shadow: 0 3px 12px rgba(0, 0, 0, 0.9);
  line-height: 1.4;
  letter-spacing: 0.03em;
}
```

#### 无背景板纯描边风格

```css
.caption-zh-stroke {
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  font-family: "Inter", sans-serif;
  font-size: 44px;
  font-weight: 900;
  color: #ffffff;
  text-align: center;
  max-width: 75%;
  /* 多层 text-shadow 模拟描边 */
  text-shadow:
    -2px -2px 0 #000,
    2px -2px 0 #000,
    -2px 2px 0 #000,
    2px 2px 0 #000,
    0 3px 8px rgba(0, 0, 0, 0.5);
  line-height: 1.5;
  letter-spacing: 0.03em;
}
```

### 中文字幕分组规则

| 规则 | 横版 (1920×1080) | 竖版 (1080×1920) |
|------|-----------------|-----------------|
| 每行最大字数 | 14-16 字 | 10-12 字 |
| 最大行数 | 2 行 | 2 行 |
| 断句优先 | 在 `，。！？、；：` 处断开 | 同左 |
| 次优断句 | 在主谓之间、动宾之间 | 同左 |
| 最短停留时间 | ≥ 1.2s | ≥ 1.5s（竖版阅读更慢） |
| 最长停留时间 | ≤ 5s | ≤ 4s（竖版节奏更快） |

#### 中文断句示例

```text
原句: "今天我们来聊一聊人工智能在编程领域的最新突破和应用场景"

分组方案:
  组1: "今天我们来聊一聊"        (3.0s - 4.5s) ← 9字，自然语义单位
  组2: "人工智能在编程领域的"    (4.5s - 6.2s) ← 10字，定语从句
  组3: "最新突破和应用场景"      (6.2s - 7.8s) ← 9字，并列结构

禁止的分组:
  ❌ "今天我们来聊一聊人工智" ← 把"智能"拆开了
  ❌ "编程领域的最新突破和应用场" ← 把"场景"拆开了
```

### 中英混排字幕处理

```html
<!-- 中英混排：英文词前后自动加半角空格 -->
<div class="caption-zh" data-start="5" data-duration="2.5" data-track-index="1">
  使用 GitHub Copilot 提升编码效率
</div>

<!-- 数字+中文：数字与中文单位之间不加空格 -->
<div class="caption-zh" data-start="8" data-duration="2.0" data-track-index="1">
  效率提升了156%，代码量减少40%
</div>
```

### 中文字幕字号参考

| 视频类型 | 横版字号 | 竖版字号 | 说明 |
|----------|---------|---------|------|
| 正式口播/商务 | 38-42px | 44-48px | 清晰稳重 |
| 教程/讲解 | 36-40px | 42-46px | 中性，不抢焦点 |
| 短视频/抖音 | 44-52px | 52-60px | 醒目，快速阅读 |
| 数据展示 | 32-36px | 38-42px | 配合数据图表 |
| 双语字幕（中） | 38-42px | 44-48px | 主语言 |
| 双语字幕（英） | 28-32px | 32-36px | 副语言，稍小 |

### 双语字幕模板

```html
<!-- 中文（主）在上，英文（副）在下 -->
<div id="bilingual-1" data-start="1.0" data-duration="2.5" data-track-index="3"
     style="position:absolute;bottom:80px;left:50%;transform:translateX(-50%);text-align:center;">
  <div style="font-size:42px;font-weight:700;color:#fff;line-height:1.4;
              text-shadow:0 2px 6px rgba(0,0,0,0.8);">
    欢迎来到今天的技术分享
  </div>
  <div style="font-size:28px;font-weight:400;color:rgba(255,255,255,0.75);
              margin-top:8px;text-shadow:0 1px 4px rgba(0,0,0,0.6);">
    Welcome to today's tech talk
  </div>
</div>
```

```css
.speaker-1 { bottom: 80px; color: #ffffff; }
.speaker-2 { bottom: 80px; color: #00ddff; } /* Different color per speaker */
```
