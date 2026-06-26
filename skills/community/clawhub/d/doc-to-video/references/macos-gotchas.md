# macOS 上跑 doc-to-video 的环境配置 + 踩坑记录

> 最后验证：macOS 26.5.1（M 系列），ffmpeg 8.1.1，node 24.16.0，Python 3.9（系统自带）。
> 本文档配套 SKILL.md v1.0.4 使用。

---

## 0. 一次性环境配置

```bash
# edge-tts（用 --user 装，避开系统 pip 权限问题）
pip3 install --user edge-tts
# 验证
python3 -c "import edge_tts; print('OK')"
# 快速 smoke test
python3 -c "
import asyncio, edge_tts
async def t():
    await edge_tts.Communicate('测试', 'zh-CN-XiaoxiaoNeural').save('/tmp/edge_smoke.m4a')
asyncio.run(t())
"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /tmp/edge_smoke.m4a
# 应输出 ~1-2 秒的时长

# ffmpeg（homebrew 装）
brew install ffmpeg
ffmpeg -version  # 验证 7.x 或 8.x 均可

# node >= 18
node --version

# Google Chrome（macOS 自带或 brew 装）
ls "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

---

## 1. 初始化项目骨架

```bash
mkdir my-video-project && cd my-video-project
mkdir -p src audio out

cat > package.json << 'EOF'
{
  "name": "my-video-project",
  "version": "1.0.0",
  "scripts": {
    "build": "remotion render src/index.tsx MyVideo out/temp.mp4"
  },
  "dependencies": {
    "@remotion/cli": "4.0.242",
    "remotion": "4.0.242",
    "react": "18.3.1",
    "react-dom": "18.3.1"
  },
  "devDependencies": {
    "@types/react": "18.3.3",
    "@types/node": "20.14.10",
    "typescript": "5.4.5"
  }
}
EOF

cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2018",
    "module": "ESNext",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "moduleResolution": "Bundler",
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "isolatedModules": true,
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true
  },
  "include": ["src"]
}
EOF

npm install --no-audit --no-fund
```

> 别用 `npx create-video@latest` 的交互式模板，会卡在 picker。手动写 package.json + tsconfig.json 更快。

---

## 2. Remotion 渲染时必须用 system Chrome

**症状 A：第一次跑**
```
Error: spawn Unknown system error -88
```

**症状 B：指定 headless-shell 路径后**
```
Error: Visited "http://localhost:3000/index.html" but got no response.
```

**根因**：Remotion 4.x 内置的 chrome-headless-shell 在 macOS 上有 sandbox/网络绑定问题。

**解法**：所有 `npx remotion render` 命令都加 `--browser-executable`：

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
npx remotion render src/index.tsx MyVideo out/temp.mp4 \
  --browser-executable="$CHROME" --concurrency=2
```

Linux 上不需要这个参数，macOS 上两个 render pass 都要加。

---

## 3. ffmpeg concat 路径 bug

**症状**：
```
[in#0 @ ...] Impossible to open 'audio/audio/00_title.m4a'
Error opening input file audio/file_list.txt.
```

**根因**：`ffmpeg -f concat` 的 demuxer 把 file_list.txt 里的路径解析为相对列表文件所在目录（不是 cwd）。所以 `audio/file_list.txt` 里写 `audio/00.m4a` 会被解析成 `audio/audio/00.m4a`。

**正确写法**：

```bash
# 切到 audio/ 下生成 list，路径用裸文件名
cd audio
printf "file '00_title.m4a'\nfile '01_chapter1.m4a'\n" > file_list.txt
cd ..

ffmpeg -y -f concat -safe 0 -i audio/file_list.txt \
  -c:a aac -b:a 128k audio/combined.m4a
```

> 注意：必须用 `-c:a aac` 重编码。`-c copy` 拼接 m4a 会因 AAC bitstream 不一致报 "moov atom not found" / "codec not currently supported in container"。

---

## 4. 不需要 atempo 加速的快路径

如果各段音频拼起来总时长已经在 180-210s 范围内（目标 3-3.5 分钟），直接跳到 step 5b 拼接，不加速。我的 Solidity 错误处理项目就是这种情况（10 段共 178.9s），零音质损失。

判断方法：

```bash
python3 -c "
import subprocess, os
total = 0
for f in sorted(os.listdir('audio')):
    if f.endswith('.m4a'):
        out = subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1', f'audio/{f}']).decode().strip()
        total += float(out)
print(f'{total:.2f}s ({total/60:.2f} min)')
"
```

总时长 < 180s 才考虑加速；< 150s 才必须加速。

---

## 5. 渲染中途抽帧检查

```bash
# 在 out/temp.mp4 已有内容后，任意秒数抽一帧
ffmpeg -y -ss 30 -i out/temp.mp4 -frames:v 1 -q:v 2 out/preview_30s.jpg
```

让 vision 工具看 jpg 就能判断布局/字体有没有问题，省得全程跑完才发现。

---

## 6. 性能基线（M 系列 MacBook）

- 1080p/30fps/180s 视频
- Chrome 并发 2
- 渲染：约 3 分钟 / pass
- 两遍渲染 + stitch：约 6-7 分钟
- 加 ffmpeg 合并：< 1 秒

如果想加速：开 `--concurrency=4`（机器内存够的话）；或换到多核 Linux 容器。

---

## 7. 已知不会修的问题

- Remotion 4.x 在 macOS 上 `npx remotion studio`（带 GUI 的开发模式）也用不了同样的 Chrome 路径，但可以在 dev 流程里手动启动 Chrome DevTools 看 React 组件
- ffmpeg atempo 限制在 0.5x-2.0x/级，超过 2.0x 必须级联两级

## 8. edge-tts 48kbps MP3 硬上限（v1.0.2 新增）

**症状**：女声（默认 XiaoxiaoNeural）听着有金属感、齿音重，怎么调参数都没用。

**根因**：edge-tts 服务端只输出 `48kbps MP3 / 24kHz / mono`。`ffprobe` 确认：

```bash
ffprobe -v error -show_streams audio/combined.m4a | grep -E "codec_name|sample_rate|bit_rate"
# codec_name=aac        ← 这是我们重编码后的，源是 mp3
# sample_rate=24000     ← 24kHz 不会更高
# bit_rate=102029       ← 上限 ~96-102k AAC，源头 48k MP3 已经丢了细节
```

**白费力气的方向**（都不会改善）：
- 改 rate/pitch 参数（只影响语速音调，不动码率）
- 把 AAC 码率提到 192k/256k（徒增文件大小）
- `aresample=48000` 升采样（0 新增信息）

**真正能改善的路径**（按代价排）：

| 方案 | 成本 | 音质改善 | 适合场景 |
|------|------|---------|---------|
| 换 voice（Yunxi/Xiaoyi/Yunyang） | 0，重跑 generate_audio.py | 中 | 首选尝试 |
| macOS `say` 命令 | 半小时摸索风格 | 中偏低，风格差异大 | 离线、无网络时 |
| Azure TTS 付费 | 注册+充值+改脚本 | 明显（48k/192k MP3） | 正式发布、对音质有要求 |
| CosyVoice / GPT-SoVITS 本地 | 半天配置 | 最高（可微调/克隆声） | 有特定声音需求时 |

**推荐 voice 排序**（按"不像机器女声"程度，从高到低）：
1. `zh-CN-YunxiNeural` — 男声，故事感，最不像 AI
2. `zh-CN-YunyangNeural` — 男声，新闻腔，正式
3. `zh-CN-YunjianNeural` — 男声，活力感
4. `zh-CN-XiaoyiNeural` — 女声，柔和，齿音最轻（如果坚持要女声）
5. `zh-CN-XiaoxiaoNeural` — 默认，自然但齿音在 48k MP3 下最明显

**试音最快的方法**：单独跑一句 ~15 秒的旁白，对比后再决定。

### 客观听感不够时：用频谱分析辅助选 voice（v1.0.4 新增）

如果试听几个 voice 觉得"都差不多"或"都怪但说不上来哪里怪"，可以加一轮频谱对比。用 spectral centroid（频谱质心，越高越亮/越尖）和 zero-crossing rate（过零率，越高细节越多）两个客观指标辅助判断：

```python
# 测每个 voice 的 centroid 和 zcr
import wave, array, math
def analyze(path):
    with wave.open(path, 'rb') as w:
        nch, sr, nframes = w.getnchannels(), w.getframerate(), w.getnframes()
        samples = array.array('h', w.readframes(nframes))
    n = len(samples)
    rms = math.sqrt(sum(s*s for s in samples) / n)
    zc = sum(1 for i in range(1, n) if (samples[i-1] >= 0) != (samples[i] >= 0))
    zcr = zc / n
    # 简化版 centroid：粗略算 4 个频段能量加权
    # 实际用 numpy 更快，这里只是示意
    return rms, zcr

# Xiaoxiao：centroid ~3859Hz, zcr 0.066（偏亮，齿音重）
# Xiaoyi：  centroid ~3078Hz, zcr 0.077（柔和，高频细节多）
# Yunxi：   centroid ~2633Hz, zcr 0.055（低沉温润）
# Yunjian： centroid ~2598Hz, zcr 0.056（男声活力）
# Yunyang： centroid ~3458Hz, zcr 0.056（新闻腔）
```

**判断规则**（实测自 6 个 voice × 同句旁白）：

- centroid 3000–4000Hz → 偏亮，听起来"尖"，女声多
- centroid 2500–3500Hz → 温润，男声多
- zcr > 0.07 → 细节多（齿音、辅音清晰），如果觉得"刺耳"通常就是 zcr 太高
- zcr < 0.06 → 偏闷，但通常更耐听

**典型决策路径**：
- 觉得 Xiaoxiao"金属感"重 → 它的 centroid 偏高 + zcr 不低导致齿音明显。换成 Yunxi（centroid 低 1200Hz）通常立刻改善
- 觉得男声"太闷" → 选 Yunjian（centroid 2598Hz 仍偏低但 zcr 跟 Yunxi 接近）
- 想要"正式感"（产品发布、企业宣传） → Yunyang（centroid 3458Hz 但 zcr 低，听感"稳"）

**频谱分析只辅助，最终决定还是耳朵**。特别是男声/女声的主观偏好因人而异，centroid 数值只是参考。

---

## 9. templates/ 目录索引

`templates/` 下的所有可复用文件：

| 文件 | 何时用 | 用法 |
|------|--------|------|
| `voice_test.py` | Step 0 选 voice 前 | `python3 templates/voice_test.py` 生成 6 个对比样本 |
| `generate_audio.py` | Step 2 写配音脚本 | 复制到项目根目录，改 SCENES 和 VOICE |
| `audio_frames.py` | Step 4 测时长 / 算 F[] | `python3 templates/audio_frames.py measure` / `frames` |
| `merge.sh` | 最后一步合并 | 复制到项目根目录，`./merge.sh` |
| `Scene.tsx`, `index.tsx` | Step 6/7 Remotion 场景 | 复制到 `src/`，按你的内容改 |
| `remotion.config.ts`, `tsconfig.json`, `remotion-package.json` | 项目初始化 | 合并到 `package.json`，**别用 `npx create-video`** |
