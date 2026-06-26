---
name: batch-rendering
description: N 个视频一次跑通的批量 pipeline（subagent 委派 + 并行渲染 + 跳过第二遍 render 的 F[] 优化）
---
# 批量渲染：N 个视频一次跑通

> 配套 SKILL.md v1.0.6 用。适用：系列教程（10+ 视频）、同一作者的多个文章一次性转视频。
> 第一个视频的脚手架看 `worked-example-tsp-solidity04.md`，第二个的复用看 `second-video-pattern.md`。本文档是 N≥3 的进阶。

## 什么时候走这个流程

满足以下任一条件时，**不要逐个走 8 步流程**，改用批量 pipeline：

- 同一作者的教程系列（10+ 篇）
- 同一技术栈的多篇博客
- 任何"我有 N 篇 markdown 要转视频"的需求

**核心收益**：
- 5 个视频串行 ~80 分钟，批量并行 ~20-30 分钟
- 不需要每个项目都从零写 SCENES 旁白
- subagent 承担机械写作（生成 SCENES + scene TSX），主 agent 只做 pipeline integration

---

## 完整流程

### Step 0：规划阶段（一次性 5 分钟）

明确以下参数并**写到一个 `batch.json` 里**：

```json
{
  "voice": "zh-CN-YunxiNeural",
  "output_root": "/Users/neo/vscode",
  "source_root": "/Users/neo/vscode/mengbin/mengbin92.github.io/_posts",
  "lessons": [
    {"num": 6,  "source": "2025-08-01-TSP-solidity06.md"},
    {"num": 7,  "source": "2025-08-04-TSP-solidity07.md"},
    {"num": 8,  "source": "2025-08-06-TSP-solidity08.md"},
    {"num": 9,  "source": "2025-08-08-TSP-solidity09.md"},
    {"num": 10, "source": "2025-08-09-TSP-solidity10.md"}
  ]
}
```

### Step 1：委派 subagent 写 SCENES + scene TSX（10 分钟）

**不要主 agent 自己写 5 套**——纯机械重复，主 agent 价值在 pipeline 编排。

委派 prompt 模板（精简版）：

> "读这 5 个 markdown：{source 列表}。为每个视频写一份 8 段的中文旁白脚本（SCENES 数组），输出到 `tsp-solidity{NN}-video/generate_audio.py`。每段 80-130 字，对应 12-20 秒配音。Voice 用 {voice}。
> 
> 另：从 `tsp-solidity05-video/src/scenes/` 拷 Primitives.tsx 到每个新项目，并写 9 个场景 TSX 文件（Cover/Intro/Section1-6/EndScene）。命名按文章章节内容。
>
> **不要**做：npm install、生成配音、渲染。这些交给主 agent。"

### Step 2：主 agent 接管 pipeline（10 分钟）

收到 subagent 输出后，主 agent 在每个项目目录里跑：

```bash
# 2.1 npm install（5 个并行，后台）
for n in 06 07 08 09 10; do
  (cd tsp-solidity${n}-video && npm install --no-audit --no-fund) &
done
wait

# 2.2 生成配音（顺序，edge-tts 网络受限）
for n in 06 07 08 09 10; do
  (cd tsp-solidity${n}-video && python3 generate_audio.py)
done
```

> ⚠️ 2.2 看着像能并行——`asyncio.gather` 内部就是并发的——但 Microsoft edge-tts 服务端对**单 IP 高并发**有限制，串行更稳。5 段 × 9 段 = 45 个 m4a，串行 ~30 秒。

### Step 3：测时长 + 算 F[]（10 秒）

```bash
for n in 06 07 08 09 10; do
  (cd tsp-solidity${n}-video && \
    python3 ~/.hermes/skills/doc-to-video/templates/audio_frames.py measure --json-out scenes.json)
done
```

> 🎯 **关键优化**：用 `audio_frames.py` 算出的 F[] 是**基于实测音频时长**的（不是基于估算视频长度）。这意味着——**第一遍 Remotion 渲染的帧数 = 最终帧数，不需要第二遍渲染**。SKILL.md Step 8 里的"先 render 一遍测帧数 → 改 F[] → 再 render"流程可以**整个跳过第二步**。

实测验证（tsp-solidity06–10 batch run）：
- 5 个视频，5 个 measure
- 渲染一次直接命中目标帧数（5326/5477/5384/5460/5373 全部 = audio × 30fps 精确）
- **省掉 5 次第二遍渲染 = 节省 ~25 分钟**

### Step 4：拼 audio file list + 拼接（10 秒）

⚠️ **bash 转义陷阱**（v1.0.6 新加 — 历史踩过两次）：

```bash
# ❌ 错：sed 拼接单引号会被 shell 吃掉，产出 broken 行
sed "s/^/file '/; s/$/'/" *.m4a > file_list.txt
# 输出: 'file 00_title.m4a file file 01_intro.m4a ...'  (每词一行)

# ✅ 对：printf 是这个场景下唯一稳的
for f in $(ls *.m4a | grep -v combined | sort); do
  printf "file '%s'\n" "$f" >> file_list.txt
done
```

> 💡 **为什么 sed 不行**：`%s` 转义内嵌单引号 + 双引号包整个表达式时，shell 会按 word-split 把每行变成多行。`printf "%s\n" "$f"` 用格式化的单参数，不会被 word-split 拆。

然后拼接（必走 `-c:a aac` 重编码，详见 SKILL.md Q6 路径坑）：

```bash
for n in 06 07 08 09 10; do
  (cd tsp-solidity${n}-video/audio && \
   for f in $(ls *.m4a | grep -v combined | sort); do
     printf "file '%s'\n" "$f" >> file_list.txt
   done)
done
for n in 06 07 08 09 10; do
  (cd tsp-solidity${n}-video && \
   ffmpeg -y -f concat -safe 0 -i audio/file_list.txt -c:a aac -b:a 128k audio/combined.m4a)
done
```

### Step 5：F[] 自动更新（5 秒）

```python
# 在主 agent 用 execute_code 跑，对所有项目批量改 Scene.tsx 和 index.tsx
import json, re

for n in [6, 7, 8, 9, 10]:
    d = f'/Users/neo/vscode/tsp-solidity{n:02d}-video'
    with open(f'{d}/scenes.json') as f: data = json.load(f)
    durations = [s['duration_s'] for s in data['scenes']]
    total_s = sum(durations)
    total_frames = round(total_s * 30)
    F = [0]
    cum = 0.0
    for s in durations[:-1]:
        cum += s
        F.append(round(cum / total_s * total_frames))
    F.append(total_frames - 10)
    for path, old_pat, new_val in [
        (f'{d}/src/Scene.tsx',  r'const F = \[[\d,\s]+\];', f'const F = {F};'),
        (f'{d}/src/index.tsx',  r'const DURATION_IN_FRAMES = \d+;', f'const DURATION_IN_FRAMES = {total_frames};'),
    ]:
        with open(path) as f: content = f.read()
        content = re.sub(old_pat, new_val, content)
        with open(path, 'w') as f: f.write(content)
```

### Step 6：并行渲染（关键 — M 系列 Mac 实测 2-3 并行最佳）

```bash
# 启动 2 个并发（推荐，资源安全）
(cd tsp-solidity06-video && npx remotion render src/index.tsx TSPVideo out/temp.mp4 \
   --concurrency=1 --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") &
(cd tsp-solidity07-video && npx remotion render src/index.tsx TSPVideo out/temp.mp4 \
   --concurrency=1 --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") &
wait

# 启动剩下 3 个并发
(cd tsp-solidity08-video && npx remotion render src/index.tsx TSPVideo out/temp.mp4 \
   --concurrency=1 --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") &
(cd tsp-solidity09-video && npx remotion render src/index.tsx TSPVideo out/temp.mp4 \
   --concurrency=1 --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") &
(cd tsp-solidity10-video && npx remotion render src/index.tsx TSPVideo out/temp.mp4 \
   --concurrency=1 --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") &
wait
```

> **并发数选择**（M 系列 MacBook, 64GB RAM 实测）：
> 
> | 并发 | 单 render 时长 (5k 帧) | 总 wall-clock (5 个) | 内存峰值 | 风险 |
> |---|---|---|---|---|
> | 1 | ~5 min | 25 min | ~1.5 GB | 0 |
> | 2 | ~5 min | 12 min | ~3 GB | 0 |
> | 3 | ~6-7 min | 7 min | ~4.5 GB | 偶尔 Chrome OOM |
> | 4+ | ~10+ min | 7+ min | ~6 GB | 必触发 swap |
> 
> **推荐：2-3 并行**。`--concurrency=1` 是因为单 process 已经在用 Chrome 多线程，Remotion 内部并行通过 Chrome 的多 tab 协调。

### Step 7：合并（5 秒）

```bash
for n in 06 07 08 09 10; do
  (cd tsp-solidity${n}-video && \
   ffmpeg -y -i out/temp.mp4 -an -c:v copy /tmp/noaudio_${n}.mp4 && \
   ffmpeg -y -i /tmp/noaudio_${n}.mp4 -i audio/combined.m4a \
     -c:v copy -c:a aac -b:a 128k -shortest out/final_with_audio.mp4 && \
   rm /tmp/noaudio_${n}.mp4)
done
```

### Step 8：清理 + 验证

```bash
# 删 temp.mp4 释放磁盘
for n in 06 07 08 09 10; do
  rm -f tsp-solidity${n}-video/out/temp.mp4
done

# 批量 ffprobe 验证音视频同步
for n in 06 07 08 09 10; do
  v=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 tsp-solidity${n}-video/out/final_with_audio.mp4)
  a=$(ffprobe -v error -select_streams a:0 -show_entries stream=duration -of csv=p=0 tsp-solidity${n}-video/out/final_with_audio.mp4)
  echo "L${n}: v=${v}s a=${a}s drift=$(python3 -c "print(round((${a}-${v})*1000))")ms"
done
# 期望所有 drift < 50ms
```

---

## 实测耗时（M 系列 MacBook, 5 个视频批量）

| 阶段 | 串行 5 个 | 批量并行 |
|---|---|---|
| subagent 写 SCENES + scenes | 50 min | 10 min（委派） |
| npm install（5×） | 15s | 3s（缓存 + 并行） |
| 配音生成 | 30s × 5 = 2.5 min | 30s（串行受网络限） |
| measure + 算 F[] | 30s | 5s（脚本化） |
| file_list + 拼接 | 50s | 10s |
| 渲染（5×） | 25 min | 7-12 min（2-3 并行） |
| 合并 | 1 min | 10s |
| **合计** | **~80 min** | **~20-30 min** |

vs. 第一个视频 ~50 min → 节省 40-60% 时间。

---

## ⚠️ 批量模式独有的坑

### 1. Skill self-update 陷阱（v1.0.6 新发现）

`~/.hermes/skills/doc-to-video/` 的 SKILL.md 和 references/ 会在 **你写入后 1-10 秒内被 skill 自我更新机制修改**（v1.0.5 → v1.0.6 转换期间实测到两次自动编辑）。

**症状**：你刚 `cp` 完一份文件到 OpenClaw，1 秒后 SHA 对不上了，因为 Hermes 那边已经被更新。

**解决**：sync 完文件后**重新 verify SHA**：

```bash
for f in SKILL.md templates/*.py references/*.md; do
  h=$(sha256sum ~/.hermes/skills/doc-to-video/$f | cut -c1-12)
  o=$(sha256sum ~/.openclaw/workspace/skills/doc-to-video/$f | cut -c1-12)
  [ "$h" = "$o" ] || echo "MISMATCH: $f (hermes=$h openclaw=$o)"
done
```

详细 sync 流程见 `references/syncing-to-openclaw.md`。

### 2. Subagent 写的内容可能"形式对，质量平"

subagent 写的 Section1-Section6 命名是统一的（如 "Storage", "Memory", "Experiment"），不是 1:1 复刻原文章节。**视频产出 OK，但内容保真度有损失**。

**缓解**：
- 让 subagent 输出的章节名**严格按原文章节**（改 prompt）
- 或者主 agent 在收到 subagent 输出后**抽样检查**一篇的 SCENES 和 scene TSX，发现问题再修

### 2a. Subagent 600s 超时（v1.0.6 实测）

Hermes subagent 默认 10 分钟封顶。**5+ 个项目一次性委派**会在 timeout 时未完成（TSP 12 视频批量时实测：L11-L15 委派在 600s 截止，4 个完成 1 个未完成，主 agent 手写 L15）。

**避免**：
- **单次委派 ≤4 个项目**（实测 4 个能在 600s 内完成）
- **5+ 个分批委派**：第一批 4 个等完成，第二批 4 个
- 或者**委派只写 SCENES 旁白**（核心价值），**场景 TSX 主 agent 自己写**——场景文件结构高度重复（参考已有项目套模板），不值得为它冒险等 subagent 超时

### 2b. Subagent 写 JSX 容易踩的字符串转义坑（实测）

**症状**：L12 渲染 esbuild 报 `Expected ">" but found "("`，定位到 Section1.tsx:16:44。
**根因**：subagent 写了 `title="selector = keccak256(\"name(types)\")"`，看起来转义了 `\"`，但 JSX 解析时 `\"` 是字面量 `"`——**attribute 被提前关闭**。

**预防**（写 subagent prompt 时显式禁）：
> ⚠️ JSX attribute 里**禁用**内层双引号。改用 JS 表达式 `title={"selector = keccak256(\"name(types)\")"}` 或 HTML 实体 `&quot;`。

**事后修复**（用 sed 一行扫）：
```bash
grep -rn 'title="[^"]*\\"[^"]*\\"[^"]*"' src/scenes/  # 找问题
sed -i '' 's|title="\([^"]*\)\\"\([^"]*\)\\"\([^"]*\)"|title={`\1"\2"\3`}|g' src/scenes/Section*.tsx
```

### 2c. `cp -R` 派生新项目时缺 `out/` 目录

Remotion render 不会自动创建 `out/`，如果源项目里 `out/` 不存在或被删过，新项目里也会没有，渲染直接失败（错误信息 `Cannot open output file` 不像 npm 那样明显）。

**预防**：
```bash
for n in 06 07 08 09 10; do mkdir -p tsp-solidity${n}-video/out; done
```

### 2d. 用户偏好：voice 一选定下来，整个系列都用

TSP 12 视频运行显示：第一个视频用户用 Xiaoxiao，听完不满意改 Yunxi，**之后 11 个视频全程用 Yunxi**。

**workflow 含义**：Step 0 的 voice 试听不是为单个视频，是**为整个系列**。选定后所有后续视频直接用同一 voice（这正是"跨 voice 时长漂移"的来源——同 voice 时长稳定，跨 voice 才漂）。

详见 SKILL.md Step 0 的"决定后记下来"。

### 3. 渲染失败的静默吞错

并行渲染时，单个 process 失败不会阻塞其他。如果一个视频渲染卡住或 OOM 了，**要 `ls -la out/temp.mp4` 验证**：

```bash
for n in 06 07 08 09 10; do
  f=tsp-solidity${n}-video/out/temp.mp4
  [ -f "$f" ] && sz=$(stat -f%z "$f") || sz=MISSING
  echo "L${n}: $sz bytes"
done
# 期望每个 ~11-12MB（h264 1080p ~3 min 视频）
```

### 4. Remotion 缓存的 `build/` 目录

`cp -R` 派生新项目时记得删 `build/`：

```bash
rm -rf tsp-solidity{N}-video/build/
```

否则可能渲染出**旧项目的场景**（Remotion 默认会从 `build/` 读 cached bundle）。

### 5. 跳过第二遍渲染的前提条件

"用 `audio_frames.py` 算的 F[] = 实际帧数"只在以下条件同时成立时：

- Remotion 渲染出的帧数 **= `durationInFrames` 设置值**（即没有用 CSS 动画让它超出）
- F[] 的**最后一个值**是 `total_frames - 10`（不是 `total_frames`，避免 EndScene 出不来）

**如果用了会改变内容时长的 CSS 动画**（例如 `transition: all 1s`），Remotion 仍可能渲染超过 `durationInFrames` 几帧——这种项目仍需第一遍 → ffprobe → 改 F[] → 第二遍。

### 6. Scene.tsx 路由数 ≠ SCENES 段数（v1.0.7+ 高发坑，5 个批量项目命中 3 个）

**症状**：video 渲染成功，但**某些 Section 静默显示几秒没配音**，或**EndScene 只剩 10 帧看不见**。

**根因**：subagent 给所有项目写相同的 Scene.tsx 模板（9 routes: Cover, Intro, S1-S6, EndScene），但有些文章**只有 8 段 SCENES**（如 L16/L17/L20）或**9 段 SCENES 但压缩到 6 个 Section**（如 L18 源文章 10 段）。结果 Scene.tsx 路由数 ≠ SCENES 段数，尾段要么空白要么被 EndScene 压缩。

**检测脚本**（跑 batch 前跑一次，5 个批量项目实测命中 3 个）：

```python
import re

for n in [16, 17, 20]:  # 跑 batch 前先看哪些是 8 段项目
    d = f'/Users/neo/vscode/tsp-solidity{n:02d}-video'
    p = f'{d}/src/Scene.tsx'
    with open(p) as f: sc = f.read()
    m = re.search(r'const F = \[([\d, ]+)\];', sc)
    if not m: continue
    f_vals = [int(x.strip()) for x in m.group(1).split(',') if x.strip()]
    n_segments = len(f_vals) - 1
    n_routes = sc.count('if (f < F[') + 1
    print(f'L{n}: {n_segments} SCENES, {n_routes} routes → '
          f'{"OK" if n_segments == n_routes else "FIX NEEDED"}')
```

**修复方法**（仅 8 段 SCENES 的项目需要）：Scene.tsx 重写为 `Cover + Intro + S1-S5 + EndScene = 8 routes`，对应 9 F[] 值。F 数组不用动，只改 routes 部分。

**预防 subagent 写错**：在 subagent prompt 里**显式要求**：

> 写 Scene.tsx 时，**route 数 = SCENES 段数**（不是固定的 9）。如果 SCENES 有 8 段，route 就 8 个（Cover + Intro + S1-S5 + EndScene）。每个 route 严格 1:1 对应一段 SCENES。

### 7. Python f-string 写 JSX 时的双重花括号转义陷阱（v1.0.7+ 主 agent 修复时踩坑）

**症状**：用 Python f-string 生成 Scene.tsx 内容时，**JSX 表达式会被双重花括号吞掉**。例如想输出 `<Cover p={prog(f, F[0], 30)} />`，f-string 里写 `{prog(...)}` 会被 Python 当作格式化占位符——**完全没花括号输出**。

**反例**（写出来变成 `if (f < F[1]) return <Cover p=prog(f, F[0], 30) />` —— 语法错）：

```python
new_scene = f'''
  if (f < F[1]) return <Cover p={prog(f, F[0], 30)} />;
'''
```

**正例**（f-string 里 JSX 的 `{}` 要写成 `{{}}`）：

```python
new_scene = f'''
  if (f < F[1]) return <Cover p={{prog(f, F[0], 30)}} />;
'''
# 输出: if (f < F[1]) return <Cover p={prog(f, F[0], 30)} />;  ← 正确
```

**安全做法**：

- 用 `str.format()` 而非 f-string（少一层转义）
- 或者写到临时 `.tsx.template` 文件后再 `sed` 替换 F 值
- 或者**别用 Python 写 JSX**，让 subagent 或人写

### 9. 复杂代码项目（实战/Foundry 重）的 subagent 委派策略（v1.0.7+ 实测）

`§2a` 说"≤4 项目"，但**前提是 5-7 节的概念性文章**。如果文章是**实战项目**（10+ 段、Foundry 代码 ≥200 行、含 4-5 个测试），代码复杂度会**爆量 token**，5 项目委派必然超时。

**实测（tsp-solidity16–25 实战项目 batch run）**：

| 委派内容 | 项目数 | token 量 | 完成时间 | 结果 |
|---|---|---|---|---|
| 5 个概念性文章 (L11–15) | 5 | ~25K out | 600s | ⏱️ 超时 1 个，主 agent 手写 L15 |
| 5 个实战项目 (L21–25) | 5 | ~40K out | 600s | ⏱️ 超时 3 个 |
| **2 个实战项目 (L24–25)** | **2** | **~20K out** | **307s** | ✅ 全部完成 |
| 1 个有 JSX 错误的修复 | 1 | ~5K | 60s | ✅ |

**关键经验**：

- **复杂项目 = 单次委派 ≤ 2 个**，**简单项目 = ≤ 4 个**
- 判断标准：看文章里**代码块数量**。0-2 个代码块（概念性）→ ≤4 个；3+ 个代码块（实战）→ ≤2 个
- 委派时**明确指定**："if any project is incomplete after 600s, the main agent will hand-write those projects using templates"——给 subagent 心理预期，别让它卡在质量上

**混合策略最佳**（v1.0.7+ 默认 workflow）：

1. **主 agent 写 generate_audio.py**（旁白是高上下文写作，main agent 不会跑偏）
2. **Subagent 写 9 个场景 TSX**（机械重复，low-context，正适合 subagent）
3. 委派 scope：**≤2 个**复杂项目，或 **≤4 个**简单项目
4. 超时的项目**主 agent 用模板手写**（参考 last-good-project 复制 + 改 narration）

### 10. JSX 文本里嵌入 `<code>` 标签的坑（v1.0.7+ 实测 L23）

**与 §2b 的"属性嵌套双引号"是不同坑**。§2b 是属性值里的引号问题，这一条是 JSX 文本节点里嵌 JSX 标签的问题。

**症状**：`Module build failed: The character ">" is not valid inside a JSX element`，定位到 `Section3.tsx:40:66`。

**根因**：subagent 想在 JSX 文本里突出"映射表 (id → balance)"，写成：

```tsx
<div>
  ERC1155 用一张 <code style={{color: "#f0883e"}}>(id => balance)</code> 表管理所有 token 类型,
  适合<strong style={{color: "#f0883e"}}>需要管理多种资产</strong>的场景。
</div>
```

JSX 解析器看到 `<code>` 试图匹配 JSX 元素，但这是**文本节点位置**（在 `<div>` 标签内但在 JSX 子元素位置），不是合法的 JSX 语法位置。`>` 被识别为标签闭合，触发 parse error。

**修复**：

```tsx
<div>
  用一张映射表 (id → balance) 管理所有 token 类型,
  适合需要管理多种资产的场景。
</div>
```

**预防 subagent 写错**：在 subagent prompt 里加：

> ⚠️ JSX 文本节点（夹在两个标签之间的普通文字）里**禁止**用 JSX 标签语法 (`<code>`, `<strong>`, `<em>` 等)。如果想强调术语，要么：
> - 用全大写：`BALANCE`
> - 用反引号 + mono font：` `id → balance` `
> - 把整段拆成两个 JSX 子元素
>
> JSX 文本节点里**只允许**纯字符串和 `{js-expression}`。

### 11. 长文实战项目（10+ 段）的 SCENES 压缩策略

文章节数 ≠ SCENES 段数。一个 10 段的实战项目**不要**写 10 段旁白——视频会变 6-7 分钟太长，且每段只剩 20-30 秒，场景切换频繁。

**策略**（tsp-solidity18 实战 case, 10 段 → 6 SCENES）：

| 原文章节 | 合并到 SCENES | 理由 |
|---|---|---|
| 引言 | 00_title + 01_intro | 简短铺垫不单独一段 |
| Diamond Standard 的设计目标 | 02_goals | 独立 |
| Diamond 的核心结构 | 03_structure | 独立 |
| 调用流程对比 | 04_routing | 独立 |
| 存储布局问题 | 05_storage | 独立（重点内容）|
| 简化版实现 | 06_practice | 合并实现和测试 |
| Foundry 测试 | (并入 06) | 同一主题 |
| Diamond 的优势与挑战 | 07_summary | 独立 |
| 适用场景 | (并入 07) | 简短 |
| 总结与思考 | (并入 07) | 简短 |
| 下一课预告 | 08_end | 独立 |

**经验法则**：
- 目标 **8-9 段 SCENES**（不是 9 是 8，多数 8 段项目更稳）
- 8 段 × 18-22 秒 = 144-176 秒（2:24-2:56），**完美**对应 SKILL.md 的"3 分钟左右"目标
- 9 段 = 162-198 秒，**略长**但仍 OK
- 10+ 段 = 必须合并（见 §6 路由不匹配问题）
- 合并时**保留最重要的核心概念**，放弃"练习题"、"作业"、"适用场景"、"下一课预告"等次要小节

### 12. Skill 自我更新行为（v1.0.7+ 实测两次）

跑批量时发现：subagent 写入 `templates/audio_frames.py` 或 `references/*.md` 几秒后，文件 mtime 会被 skill 自身更新，**SHA 跟你刚写入的不同**。

**实测**：
- 写 `~/.hermes/skills/doc-to-video/SKILL.md` → 9 秒后文件 mtime 更新，内容微调（v1.0.4 → v1.0.5 自动 bump）
- 写 `~/.hermes/skills/doc-to-video/references/voice-swap-and-iterate.md` → 3 秒后**自动新建** `templates/voice_test.py` 并补 SKILL.md 引用
- 写 `~/.hermes/skills/doc-to-video/SKILL.md` 引用块 → 7 秒后**自动改写**该引用块为更精确表述

**影响**：
- ✅ **正面**：skill 持续自我完善，不需要每次手动改 SKILL.md
- ⚠️ **负面**：如果 sync 到 OpenClaw 后立即验 SHA，**可能因为 Hermes 端还在被改而 mismatch**——**先在 Hermes 端等 30 秒再 sync**

**经验**：当你需要 sync Hermes ↔ OpenClaw 时：
1. 写入完成
2. **sleep 30**
3. 重新 verify SHA
4. 才 cp 到 OpenClaw

详见 `references/syncing-to-openclaw.md` §3。

### 13. 17+ 视频批量跑的磁盘管理（v1.0.7+ 实测）

| 视频数 | 项目目录占用 | final_with_audio.mp4 总量 | Remotion 临时帧 | 备注 |
|---|---|---|---|---|
| 5 | ~700MB（含 node_modules） | ~30MB | ~5GB（渲染时） | 单批可清 |
| 10 | ~1.5GB | ~60MB | ~10GB | 临时帧需清 |
| 17 | ~2.5GB | ~100MB | ~20GB | 必须清 temp.mp4 |
| 22 | ~3.6GB | ~130MB | ~30GB | 渲染时 disk 需 ≥40GB |

**清理**：
```bash
# 每批完成后删 temp.mp4
for n in 04 05 06 07 08 09 10; do
  rm -f tsp-solidity${n}-video/out/temp.mp4
done
```

**前置**：
- 跑 batch 前 `df -h /Users/neo/vscode/` 确保 ≥30GB 可用
- 视频数 >10 时中途也清一次 temp.mp4（Remotion 渲染时不会自动清）

### 14. 22 视频实测统计（v1.0.7+, 完整 TSP 系列）

| 段 | 视频数 | 总时长 | 总大小 | 平均每个 |
|---|---|---|---|---|
| L04-L10 (基础 7 个) | 7 | ~22 min | ~42MB | ~3:08 / 6MB |
| L11-L15 (进阶 5 个) | 5 | ~18 min | ~31MB | ~3:36 / 6.2MB |
| L16-L20 (安全 5 个) | 5 | ~12 min | ~30MB | ~2:24 / 6MB |
| L21-L25 (实战 5 个) | 5 | ~13 min | ~35MB | ~2:36 / 7MB |
| **合计** | **22** | **~65 min** | **~138MB** | **~3:00 / 6.3MB** |

**经验**：
- 平均**单视频 3 分钟**、**6MB** 是稳定产出的基线
- 安全/概念段（2:24-2:36）比实战段（2:36-3:36）短，因为实战要展示代码
- 任何单个 video >4 分钟 = 旁白/视觉同步出问题了
- 22 视频系列 = 主 agent 约 1.5 小时**实际工作**（不算 subagent 等待和 render 等待）

### 9. 视频跑完后归集到子目录（v1.0.7+ L04-L20 17 个视频实测）

跑完 N 个视频后，`~/vscode/` 顶层会塞满 N 个项目目录。**主 agent 主动归集**到子目录：

```bash
mkdir -p /Users/neo/vscode/tsp
for n in 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20; do
  src="/Users/neo/vscode/tsp-solidity${n}-video"
  dst="/Users/neo/vscode/tsp/tsp-solidity${n}-video"
  [ -d "$src" ] && mv "$src" "$dst"
done
```

**前提**：所有项目代码用相对路径（`./scenes/`, `audio/`, `out/`），不用绝对路径。子目录移动不影响运行。**这也是 v1.0.5 起项目结构改成"一切相对"的另一个理由**。

---

## 经验法则

- **3+ 个视频 = 值得批量**
- **批量时优先并行 render**（2-3），不要为单 render 速度纠结
- **subagent 写场景，主 agent 跑 pipeline**——这是角色分工
- **第一遍渲染的帧数 = 最终帧数**（如果 F[] 是从实测 audio 算的）
- **disk 留 10 GB**：5 个视频 × 100MB = 500MB，加上 Remotion 临时 JPEG 帧 ~5GB
- **跑 batch 前先做 §6 检测**（Scene.tsx 路由数 vs SCENES 段数），命中就修——比渲染完发现"少一段"再回头快
- **别用 Python f-string 写 JSX 内容**（§7 转义陷阱），让 subagent 写
