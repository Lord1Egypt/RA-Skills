# Stage 2：音频解析与数据驱动时间轴

### 2.1 获取音频精确时长

```bash
export PATH=./bin:$PATH
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 YYYYMMDD/assets/narration.wav
# 记录输出的 duration=XX.XXXXXX，这是视频总时长的唯一权威数据
```

### 2.2 获取精确断句时间戳（三级方案，按精度递减选择）

**方案 A — Whisper 词级转录（精度最高，优先推荐）：**
```bash
npx hyperframes transcribe YYYYMMDD/assets/narration.wav
# 生成 YYYYMMDD/assets/transcript.json，包含词级时间戳
# 直接按句末时间戳切分场景，误差 < 0.1s
```

**方案 B — RMS 能量分析 + 字数比例交叉验证（Whisper 不可用时）：**
```bash
export PATH=./bin:$PATH
# 1. 提取 RMS 能量流
ffmpeg -v error -i YYYYMMDD/assets/narration.wav \
  -af astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=rms.txt \
  -f null -

# 2. 用 Python 脚本分析静默段（>= 0.85s 的低能量区间为段间分界）
# 3. 将 RMS 检测到的分界与「字数比例推算」交叉验证：
#    - 按各段旁白字数比例分配总时长，得出各段预估 start
#    - 在预估 start ± 8s 范围内找最近 of RMS 静默段
#    - 取静默段结束时间作为实际 scene start
```

> ⚠️ 更多技术细节及排坑规范，请查阅 [技术排坑手册](file://./resources/troubleshooting.md)。

**方案 C — 纯字数比例分配（兜底方案）：**
```python
# 当 RMS 分析不可靠时（如 TTS crossfade 过重），直接按字数分配
# 误差 ±2s，对 10s+ 的场景可接受
for scene in scenes:
    scene.duration = scene.char_count / total_chars * total_audio_duration
```

### 2.3 将时间戳映射到分镜

根据 2.2 的输出，将每幕的 `data-start` 和 `data-duration` 精确填入剧本或直接生成为 JS 数组：

```js
// 由音频数据派生，禁止手动估算
const scenes = [
  { id: "scene1", start: 0,    duration: 5.8,  subtitle: "旁白文本..." },
  { id: "scene2", start: 5.8,  duration: 6.2,  subtitle: "旁白文本..." },
  // ...
];
```

**✅ Stage 2 退出标准：**
- [ ] Whisper `transcript.json` 已生成，或 RMS 分析 + 字数交叉验证已完成，或纯字数比例已计算
- [ ] 所有分镜的 `start + duration` 之和与音频总时长误差 < 0.5 秒
- [ ] 标注所使用的方案等级（A/B/C），方便后续迭代时升级
