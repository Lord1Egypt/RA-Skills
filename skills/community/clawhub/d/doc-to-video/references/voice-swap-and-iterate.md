# 配音迭代工作流：换 voice / 改语速后的重新同步

> 配套 SKILL.md v1.0.2 用。
> 适用：第一次渲染完后，发现 voice 不理想、语速太慢/太快、旁白文本要改，**音频时长变了但视频已渲染过**的情况。

---

## 什么时候走这个流程

第一次跑完 SKILL.md 的标准 8 步后，**任一项**不满足时就走：

- 配音听着别扭（参 SKILL.md Q8，48kbps MP3 天花板）
- 配音整体偏快 / 偏慢（用户反馈）
- 旁白文本要改（多一段、合并两段、删一段）

不要从头跑 SKILL.md 的 8 步。**Remotion 视频文件不需要重写场景组件**，只需要重渲染（如果总时长变了）。

---

## 完整流程

### Step 1：改 `generate_audio.py` 里的旁白或 VOICE 常量

```python
# 改 voice
VOICE = "zh-CN-YunxiNeural"  # 之前是 XiaoxiaoNeural

# 改语速（如果只是觉得整体慢/快）
# 优先用 rate 参数改 edge-tts，而不是后面 ffmpeg atempo
# 因为 rate 让 TTS 引擎按"快语速"模型生成，比 atempo 重新拉伸自然
```

### Step 2：删旧音频，重生

```bash
cd ~/vscode/your-project
rm -f audio/*.m4a audio/combined.m4a audio/file_list.txt
python3 generate_audio.py
```

### Step 3：测新总时长，决定走哪条分支

```bash
python3 -c "
import subprocess, os
total = 0
per_scene = []
for f in sorted(os.listdir('audio')):
    if f.endswith('.m4a'):
        d = float(subprocess.check_output(
            ['ffprobe','-v','error','-show_entries','format=duration',
             '-of','default=noprint_wrappers=1:nokey=1', f'audio/{f}']
        ).decode().strip())
        per_scene.append(d)
        total += d
print(f'总时长: {total:.2f}s (旧视频: {OLD_VIDEO_DURATION:.2f}s)')
print(f'各段: {per_scene}')
"
```

把 `OLD_VIDEO_DURATION` 换成当前 `out/final_video.mp4` 的时长（`ffprobe -v error -show_entries format=duration out/final_video.mp4`）。

### Step 4：分支 A — 拼接后总时长已经在 178–180s 范围内

> 多数情况。换 voice 让总时长漂移通常 < 5s。

直接拼接，**不加速**：

```bash
cd audio && printf "file '00_title.m4a'\nfile '01_why.m4a'\n..." > file_list.txt && cd ..
ffmpeg -y -f concat -safe 0 -i audio/file_list.txt \
  -c:a aac -b:a 128k audio/combined.m4a
```

如果总时长 < 178s 或 > 180s，**不要硬塞 atempo**。看分支 B。

### Step 5：分支 B — 用户明确要求"语速更快 / 更慢"

如果用户反馈"听着太慢"，最干净的做法是 **ffmpeg atempo 1.2 左右**：

```bash
# 单级 atempo 1.2 即可（ffmpeg 范围 0.5–2.0）
ffmpeg -y -i audio/combined.m4a -filter:a "atempo=1.2" \
  -c:a aac -b:a 128k audio/combined_fast.m4a
```

⚠️ **坑**：实测 atempo 1.2 输出的是 1.17x 而不是 1.2x（ffmpeg 内部精度）。ffprobe 验证一下实际时长，不要按数学算。

### Step 6：必须重渲染 Remotion（如果新音频时长 ≠ 旧视频时长）

旧 `out/final_video.mp4` 的时长是 N 秒。**直接合并新音频会导致：**

- 新音频 < 旧视频：结尾几秒静音（难看）
- 新音频 > 旧视频：`-shortest` 切掉音频结尾（旁白被吞）

正确做法：**改 `src/index.tsx` 的 `DURATION_IN_FRAMES` 和 `src/Scene.tsx` 的 `F[]`**，重渲染。

```typescript
// src/index.tsx
const DURATION_IN_FRAMES = NEW_TOTAL_FRAMES;  // = round(NEW_TOTAL_SECONDS × 30)

// src/Scene.tsx
const F = [0, ...];  // 重新算，见下
```

**F[] 重算的两条路径：**

**路径 1（推荐）：整体缩放** — 当 atempo 是在拼接后整段应用的（每个场景相对时长比例保持不变）：

```python
# 旧视频 5367 帧，新音频 4471 帧
F_new = [round(f * 4471 / 5367) for f in F_old]
F_new[-1] = 4471 - 10  # 最后一个值兜底
```

适用：换 voice 后用 atempo 调速。

**路径 2（精确）：逐段重算** — 当每个场景的音频时长独立变化（比如改了某段文本）：

```python
F = [0]
cum = 0
for s in new_per_scene_durations[:-1]:
    cum += s
    F.append(round(cum / total * new_total_frames))
F.append(new_total_frames - 10)
```

适用：改旁白文本、增加/删除场景。

### Step 7：重渲染 + 合并

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 重渲染（不传 out/temp.mp4 那个，第一遍的可以直接当 final 用）
npx remotion render src/index.tsx MyVideo out/final_video.mp4 \
  --browser-executable="$CHROME" --concurrency=2
# 约 2-3 分钟（如果总帧数比第一次少，时间也会少）

# 合并（注意用新 audio 文件名）
ffmpeg -y -i out/final_video.mp4 -an -c:v copy /tmp/noaudio.mp4
ffmpeg -y -i /tmp/noaudio.mp4 -i audio/combined_fast.m4a \
  -c:v copy -c:a aac -b:a 128k -shortest out/final_with_audio.mp4
```

### Step 8：校验

```bash
# 音视频时长差应在 100ms 以内
ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 out/final_with_audio.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=duration -of csv=p=0 out/final_with_audio.mp4
```

---

## 常见误区

### ❌ "我只换了 voice 但用旧视频合并"

如果新 voice 节奏和老 voice 差几秒，结尾会出几秒 EndScene 静音。**必须重渲染。**

### ❌ "用 atempo 把新音频拉回旧视频时长"

这样保住了视频文件不动，但**F[] 是基于"音频驱动场景切换"算的**，每个场景的视觉长度会和实际配音错位。观众看到的是：场景 05 的代码块已经切到 06，但配音还在说 05 的内容。**比"结尾几秒静音"还难看。**

正确做法：要么新音频贴合旧视频（接受错位），要么视频重渲染（保持同步）。**永远不要把音频拉回去贴合视频。**

### ❌ "改 rate 参数让 edge-tts 加速 20% 就不需要 atempo 了"

`rate="+20%"` 只影响 TTS 输出速度，**不会**让生成的 10 段总时长恰好少 20%（每段缩短比例不完全一致）。结果仍然是"新音频时长 ≠ 旧视频时长"，需要走完整流程。

---

## 实测耗时（M 系列 MacBook，1080p/30fps）

| 操作 | 耗时 |
|------|------|
| 重生 10 段 edge-tts | ~30s |
| ffmpeg 拼接 | < 1s |
| atempo 1.2（如果用） | < 1s |
| Remotion 重渲染 | 2-3 分钟（取决于总帧数） |
| ffmpeg 合并音视频 | < 1s |
| **合计** | **3-4 分钟** |

vs. 完整重做（从 SKILL.md 第 1 步起）：~10 分钟（写场景组件、抽帧检查等）。

---

## 流程图

```
第一次跑完 SKILL.md 8 步 → 输出 final_with_audio.mp4
         ↓
用户反馈 voice / 语速 / 文本问题
         ↓
[分支 1] 改 VOICE 常量 + 重生
[分支 2] 改 rate 参数 + 重生
[分支 3] 改 SCENES 文本 + 重生
         ↓
测新总时长 vs 旧视频时长
         ↓
差 < 5s？─── 是 ─→ 直接拼接不加速，跳到合并
     │
     否（差 > 5s，或用户要更快/更慢）
     ↓
应用 atempo（或不应用，让新音频自然长度）
     ↓
重算 F[]（路径 1 或 2）+ durationInFrames
     ↓
Remotion 重渲染
     ↓
合并音视频
     ↓
校验 100ms 内
```
