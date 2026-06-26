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

**方案 B — VAD 全局物理声学平铺匹配算法 (Globally Optimized Acoustic VAD-Tiling)（Whisper 不可用时）：**
```python
# 1. 读取音频数据提取 RMS 帧能量，自适应推算噪声基底作为能量阈值：
#    threshold = max(noise_floor + 0.002, max_energy * 0.015)
# 2. 通过滑动窗口锁定持续说话区间，过滤短微瞬时噪音（如静音阈值 >= 0.35s）：
#    speech_segments = [(start_t, end_t), ...]
# 3. 计算台词总字数与总活跃发音时长比率，求得发音平均时间单位。
# 4. 根据每句台词字数比重，映射到 VAD 活跃区间内计算对应的物理绝对起止时间戳：
#    s_t = active_t_to_physical_t(start_active_t)
#    e_t = active_t_to_physical_t(end_active_t)
# 5. 生成高精度的 transcript.json，该算法产出的语速极其均匀自然。
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

根据 2.2 的输出，将每幕的 `data-start` 和 `data-duration` 精确填入 HTML 的标签属性或生成为 JS 数组，并遵循以下时序安全红线：

> [!IMPORTANT]
> **时序映射安全红线（防首幕死静、浮点重叠与语速突变）：**
> 1. **首幕死静防范**：音频全局偏移 `global_offset` 必须保持在极短气口（如 `0.20s`），让旁白与背景音乐从 0.2s 即可响起，杜绝因粗暴设置长达数秒的全局偏移导致视频开头死静。封面幕（`scene_cover`）的时长禁止硬编码，必须自适应获取前几句封面台词结束点 `transcript[n]["end"]` 作为其真实持续时间。
> 2. **浮点数重叠避让**：由于 JavaScript/Python 浮点数相加精度溢出（例如 `38.58 + 3.32 = 41.900000000000006`），极易导致 HyperFrames 编译器报错 `overlapping_clips_same_track`。因此，在计算各个分镜的 `data-duration` 时，必须**主动减少 0.01 秒安全气口**进行微调避让（例如 `duration = round(end - start, 2) - 0.01`），以完全规避浮点重叠。
> 3. **语速健康度自动审计 (Health Check Gatekeeper)**：时间轴生成后，必须自动审计每句话的自适应物理语速：$\text{语速} = \text{字符数} \div \text{持续时间(秒)}$。健康的口播语速应严格落在 **3.2 ~ 5.5 字/s** 舒适区间。若单句语速 $\le 1.5$ 字/s（过慢）或 $\ge 6.5$ 字/s（急促），必须拦截物理压制并重新平铺，杜绝脱节。

```js
// 由音频数据派生，结合 0.01s 浮点避让、0.2s 气口与语速审计，禁止手动估算
const scenes = [
  { id: "scene_cover", start: 0,    duration: 7.31,  subtitle: "封面旁白..." }, // (7.32 - 0.01)
  { id: "scene1",      start: 7.32, duration: 17.50, subtitle: "旁白文本..." }, // (24.83 - 7.32 - 0.01)
  // ...
];
```

**✅ Stage 2 退出标准：**
- [ ] Whisper `transcript.json` 已生成，或 VAD 物理声学平铺匹配已完成，或纯字数比例已计算
- [ ] **已通过语速健康度审计**：每一句口播的字符语速严格处于 **3.2 ~ 5.5 字/s** 区间内，绝无大段错位
- [ ] 所有分镜的 `start + duration` 之和与音频总时长误差 < 0.5 秒
- [ ] 标注所使用的方案等级（A/B/C），方便后续迭代时升级
