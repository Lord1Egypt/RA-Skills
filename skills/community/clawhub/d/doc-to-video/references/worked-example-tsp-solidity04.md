# 实战案例：Solidity 错误处理（require/revert/assert）

> 配套 SKILL.md v1.0.1 用。
> 源文档：`_posts/2025-07-30-TSP-solidity04.md`（Solidity 错误处理教程）
> 项目位置：`~/vscode/tsp-solidity04-video/`
> 输出：`out/final_with_audio.mp4` (6.4MB, 1920x1080, 178.9s, H.264+AAC)

完整跑过一遍的端到端实例，可作为下一个项目的起点模板。

---

## 1. 项目结构

```
tsp-solidity04-video/
├── package.json                # Remotion 4.0.242 + React 18.3.1
├── tsconfig.json
├── remotion.config.ts
├── merge.sh                    # FFmpeg 合并脚本
├── generate_audio.py           # 配音脚本
├── src/
│   ├── index.tsx               # Composition 入口
│   ├── Scene.tsx               # 帧边界 + 场景路由
│   └── scenes/
│       ├── Primitives.tsx      # VideoScene / FadeIn / CodeBlock / Tag / Title
│       ├── Cover.tsx
│       ├── WhyImportant.tsx
│       ├── RequireScene.tsx
│       ├── RevertScene.tsx
│       ├── AssertScene.tsx
│       ├── CustomErrorScene.tsx
│       ├── ChooseScene.tsx
│       ├── PracticeScene.tsx
│       ├── SummaryScene.tsx
│       └── EndScene.tsx
├── audio/
│   ├── 00_title.m4a  ...  09_end.m4a
│   ├── file_list.txt
│   └── combined.m4a            # 178.896s，AAC 128k
└── out/
    ├── temp.mp4                # 11.3MB, 5367 帧
    ├── final_video.mp4         # 11.6MB, 5367 帧
    ├── final_with_audio.mp4    # 6.4MB, 最终交付
    └── preview_*.jpg           # 中途抽帧检查
```

---

## 2. 10 段旁白（SCENES 数组）

| ID | 时长 | 内容主题 |
|----|------|---------|
| `00_title` | 11.4s | "纸上谈兵 Solidity 第 4 课..." |
| `01_why` | 19.2s | 为什么错误处理重要（不可逆、回滚、防资金损失） |
| `02_require` | 19.2s | require 语法 + deposit 例子 |
| `03_revert` | 15.6s | revert 灵活性 + executeTrade 多步判断 |
| `04_assert` | 16.8s | assert 内部不变量 + Panic |
| `05_custom` | 19.4s | Custom Errors 0.8.4+ + Gas 对比 |
| `06_choose` | 18.2s | 4 种机制选型表（4 行） |
| `07_practice` | 23.8s | Counter 合约 3 个练习 + Foundry 测试 |
| `08_summary` | 19.5s | 4 点最佳实践总结 |
| `09_end` | 15.7s | 结束 + 推荐看 Foundry 测试代码 |

**总音频：178.896s ≈ 2:59** - 正好在目标 180-210s 范围内，跳过 atempo 加速。

每段控制在 100-150 字、对应 15-24 秒，是 30fps 场景的合适节奏（每个画面有 1.5-2s 阅读时间）。

---

## 3. 帧边界（实测计算）

`src/Scene.tsx` 里的 F 数组，第一遍渲染（ffprobe 确认 5367 帧）后用这个公式算出：

```
F[i] = round(sum(audio_secs[0..i-1]) / total_audio_secs * total_rendered_frames)
```

```typescript
const F = [0, 343, 918, 1495, 1964, 2469, 3050, 3597, 4310, 4895, 5357];
//              ↑   ↑    ↑     ↑     ↑     ↑     ↑     ↑     ↑     ↑
//              00  01   02    03    04    05    06    07    08    09_end
```

每个场景给 30 帧（1秒）的淡入过渡，场景切换看起来自然。

---

## 4. Remotion 场景组件范式

每个 scene 文件长这样（以 RequireScene 为例）：

```tsx
import React from "react";
import { VideoScene, FadeIn, Title, CodeBlock, Tag } from "./Primitives";

export const RequireScene: React.FC<{p: number}> = ({p}) => (
  <VideoScene>
    <div style={{position: "absolute", inset: 0, padding: "80px 120px", display: "flex", flexDirection: "column"}}>
      <FadeIn p={p} delay={0}>
        <div style={{display: "flex", alignItems: "center", gap: 24}}>
          <Tag label="require" />
          <Title>外部输入的守门人</Title>
        </div>
      </FadeIn>
      <div style={{height: 40}} />
      <FadeIn p={p} delay={0.2}>
        <CodeBlock
          code={`function deposit(uint amount) public {
    require(amount > 0, "Deposit amount must be greater than zero");
    balance[msg.sender] += amount;
}`}
          title="典型场景：参数验证"
          highlight={[1]}
        />
      </FadeIn>
      ...
    </div>
  </VideoScene>
);
```

设计要点：
- 绝对定位 + flex 布局 占满 1920x1080
- `p` 进度值（0→1）传给 FadeIn，每段延迟 0.2 让元素分批淡入
- CodeBlock 的 `highlight` 参数 数组传入要高亮的行号（0-indexed）
- 统一色板：ACCENT #5ab0ff（require）、#a371f7（revert）、#ff7b72（assert）、#7ee787（custom）、#f0883e（实战）

---

## 5. 完整可复现的 shell 序列

```bash
# 0. 准备工作
cd ~/vscode
mkdir tsp-solidity04-video && cd tsp-solidity04-video
mkdir -p src audio out

# 1. 拷 package.json / tsconfig.json（见 SKILL.md 第 1 节）
# 2. 写 generate_audio.py（含 10 段 SCENES 数组，见上文）
# 3. 写 src/index.tsx, src/Scene.tsx, src/scenes/*.tsx

# 4. 装依赖
npm install --no-audit --no-fund

# 5. 生成配音（~30s）
python3 generate_audio.py

# 6. 测各段时长（可选，确认总时长在范围内）
for f in audio/*.m4a; do
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")
  echo "$f: ${dur}s"
done

# 7. 拼接（必走 -c:a aac 重编码，路径要相对 audio/）
cd audio && printf "file '00_title.m4a'\nfile '01_why.m4a'\nfile '02_require.m4a'\nfile '03_revert.m4a'\nfile '04_assert.m4a'\nfile '05_custom.m4a'\nfile '06_choose.m4a'\nfile '07_practice.m4a'\nfile '08_summary.m4a'\nfile '09_end.m4a'\n" > file_list.txt && cd ..
ffmpeg -y -f concat -safe 0 -i audio/file_list.txt -c:a aac -b:a 128k audio/combined.m4a

# 8. 写 src/ 场景组件
# 9. 第一次渲染（macOS 必须用 system Chrome）
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
npx remotion render src/index.tsx TSPVideo out/temp.mp4 \
  --browser-executable="$CHROME" --concurrency=2
# 约 3 分钟，输出 11.3MB

# 10. 确认实际帧数
ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of csv=p=0 out/temp.mp4
# -> 5367

# 11. 用 5367 修正 src/Scene.tsx 的 F[] 和 src/index.tsx 的 durationInFrames
# （本例实际渲染 5367 帧 = 估算值，差 0 帧，省了一步）

# 12. 第二遍渲染
npx remotion render src/index.tsx TSPVideo out/final_video.mp4 \
  --browser-executable="$CHROME" --concurrency=2

# 13. 合并音视频（-an 先去原音轨，-shortest 留最短）
ffmpeg -y -i out/final_video.mp4 -an -c:v copy /tmp/noaudio.mp4
ffmpeg -y -i /tmp/noaudio.mp4 -i audio/combined.m4a \
  -c:v copy -c:a aac -b:a 128k -shortest out/final_with_audio.mp4

# 14. 校验
ffprobe -v error -show_streams out/final_with_audio.mp4 | grep -E "codec_type|duration|width|height"
# 应输出 h264+aac, 1920x1080, ~178.9s
```

---

## 6. 抽帧检查（建议在 Step 9 后做）

```bash
ffmpeg -y -ss 6  -i out/temp.mp4 -frames:v 1 -q:v 2 out/preview_cover.jpg
ffmpeg -y -ss 30 -i out/temp.mp4 -frames:v 1 -q:v 2 out/preview_why.jpg
ffmpeg -y -ss 80 -i out/temp.mp4 -frames:v 1 -q:v 2 out/preview_revert.jpg
ffmpeg -y -ss 120 -i out/temp.mp4 -frames:v 1 -q:v 2 out/preview_choose.jpg
ffmpeg -y -ss 150 -i out/temp.mp4 -frames:v 1 -q:v 2 out/preview_practice.jpg
```

让 vision 工具看这些 jpg，能在 1 分钟内确认：
- 文字是否溢出/截断
- 布局是否平衡
- 配色是否一致

比等全程跑完才发现问题强 10 倍。

---

## 7. 音视频同步校验

合并后用 ffprobe 确认两路时长差：

```bash
# 视频流时长
ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 out/final_with_audio.mp4
# 音频流时长
ffprobe -v error -select_streams a:0 -show_entries stream=duration -of csv=p=0 out/final_with_audio.mp4
```

差值应在 100ms 以内（人耳不可察）。本例：视频 178.900s vs 音频 178.859s，差 41ms。
