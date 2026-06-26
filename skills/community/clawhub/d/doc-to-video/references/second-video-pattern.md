# 第二个及之后的视频：复用项目骨架

> 配套 SKILL.md v1.0.5 用。
> 适用：**已经跑过一个完整视频**之后，要做第二个、第三个……同系列视频。
> 核心：**`cp -R` 旧项目 → 改 SCENES + 改场景组件 → 复用一切**。

**这个 patterns 在第二次跑视频时省了 5-10 分钟**，比从 templates/ 重搭快得多。同系列视频（同一个作者/同一种 voice/同一种代码风格）尤其适合。

---

## 核心操作

```bash
cd ~/vscode
cp -R tsp-solidity04-video tsp-solidity05-video
cd tsp-solidity05-video
rm -rf audio/* out/*.mp4 out/*.jpg node_modules package-lock.json
# build/ 是 Remotion 缓存，也可以删（重新 render 会自动重建）
rm -rf build
```

**删了哪些 / 留了哪些：**

| 删 | 留 | 原因 |
|---|---|---|
| `audio/*` | `audio/file_list.txt` 占位 | 旧配音毫无用处 |
| `out/*.mp4` | `out/` 目录本身 | 旧视频要重渲 |
| `out/*.jpg` | | 旧预览帧要重抽 |
| `node_modules` | | 重新 `npm install` 速度反而更快（缓存命中 3-5s）|
| `package-lock.json` | | 让 npm 重新锁定（v4.0.242 vs 实际版本） |
| `build/` | | Remotion 渲染产物缓存 |

---

## 改什么 / 不改什么

**改：**

1. **`generate_audio.py` 里的 `SCENES` 数组**：新文章的内容
2. **`src/scenes/*.tsx`**：新文章的视觉（10 段对 13 段组件，几乎全要重写）
3. **`src/Scene.tsx` 里的 `F` 和 `index.tsx` 里的 `DURATION_IN_FRAMES`**：用 audio_frames.py 重算

**不改：**

1. **`src/scenes/Primitives.tsx`**：VideoScene / FadeIn / CodeBlock / Tag / Title 是通用的，**几乎永远不用改**
2. **`package.json`**：Remotion 4.0.242 / React 18.3.1 已经稳定
3. **`tsconfig.json` / `remotion.config.ts`**：配置稳定
4. **`merge.sh`**：合并逻辑通用

---

## 第二个视频实测耗时（tsp-solidity05）

| 步骤 | 耗时 |
|---|---|
| `cp -R` + 删产物 | 5s |
| `npm install` | 3s（缓存命中）|
| 改 `generate_audio.py`（13 段 SCENES） | 5min（手写旁白）|
| `python3 generate_audio.py` | 30s |
| `python3 audio_frames.py measure --json-out scenes.json` | 5s |
| 改 13 个 scene tsx 文件 | 8min（体力活）|
| 改 `src/Scene.tsx` 占位 F[] | 30s |
| 第一次 Remotion render | 5min（7100 帧）|
| 抽 5 帧 JPG 检查视觉 | 30s |
| 修正 F[]（用 `audio_frames.py frames`）| 1min |
| 第二次 Remotion render | 5min |
| 合并音视频 | 5s |
| **合计** | **~25 分钟** |

vs. 第一个视频（tsp-solidity04）~50 分钟，**节省 50%**。

vs. 从 templates/ 重搭（同系列假设省掉 5-10 分钟的 package.json / Primitives.tsx / merge.sh 重写），**`cp -R` 又省 5-10 分钟**。

---

## 13 段视频的 4 个新 visual patterns（vs 第一个的 10 段）

第二个视频引入了 4 种新视觉模式，**没在第一个视频用过**，未来同系列可以复用：

### Pattern A: CEI 时间线（Checks-Effects-Interactions）

3 标签条 + 1 代码块，强调"流程顺序"：

```tsx
// src/scenes/CEI.tsx
<div style={{display: "flex", gap: 16, marginBottom: 24}}>
  {[
    {n: 1, t: "Checks",       d: "检查",     c: "#5ab0ff"},
    {n: 2, t: "Effects",      d: "更新状态", c: "#7ee787"},
    {n: 3, t: "Interactions", d: "外部调用", c: "#f0883e"},
  ].map((s, i) => (
    <div key={i} style={{
      flex: 1, background: `${s.c}11`, border: `1px solid ${s.c}55`, borderRadius: 10,
      padding: "12px 18px", textAlign: "center",
    }}>
      <div style={{fontSize: 18, color: s.c, fontWeight: 600}}>{s.n}. {s.t}</div>
      <div style={{fontSize: 16, color: "#c9d1d9"}}>{s.d}</div>
    </div>
  ))}
</div>
<CodeBlock code={...} highlight={[5, 7]} />  // 高亮步骤 2 和步骤 3
```

### Pattern B: 双卡对比（DelegateCall vs StaticCall）

两个并排的对比卡，强调"两种相似但不同的事物"：

```tsx
<div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, flex: 1}}>
  <FadeIn p={p} delay={0.35}>
    <div style={{background: `${colorA}11`, border: `1px solid ${colorA}55`, borderRadius: 12, padding: "24px 32px", height: "100%", boxSizing: "border-box"}}>
      <div style={{fontSize: 28, fontWeight: 600, color: colorA, marginBottom: 12}}>名称 A</div>
      <div style={{fontSize: 22, color: "#c9d1d9", lineHeight: 1.6}}>说明 A</div>
    </div>
  </FadeIn>
  <FadeIn p={p} delay={0.5}>
    <div style={{...同结构，colorB...}}>说明 B</div>
  </FadeIn>
</div>
```

### Pattern C: 4-file 列表（Foundry 项目结构）

强调"4 个角色共同工作"，用 2×2 grid 列出文件 + 角色：

```tsx
<div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, flex: 1}}>
  {FILES.map((f, i) => (
    <FadeIn key={i} p={p} delay={0.3 + i * 0.12}>
      <div style={{display: "flex", alignItems: "center", gap: 24,
        background: "#ffffff0a", border: `1px solid ${f.color}55`, borderRadius: 14,
        padding: "24px 32px", borderLeft: `6px solid ${f.color}`}}>
        <code style={{fontSize: 26, color: f.color, fontFamily: '"SF Mono", Menlo, monospace', minWidth: 280}}>{f.name}</code>
        <div style={{fontSize: 24, color: "#c9d1d9"}}>{f.role}</div>
      </div>
    </FadeIn>
  ))}
</div>
```

### Pattern D: 4-列对比表（策略选型表）

强调"多种选项按多维度对比"，每行 4 列：名称 / 安全评级 / 优点 / 风险：

```tsx
<div style={{display: "flex", flexDirection: "column", gap: 16, flex: 1, justifyContent: "center"}}>
  {COMPARE.map((r, i) => (
    <FadeIn key={i} p={p} delay={0.12 + i * 0.1}>
      <div style={{display: "grid", gridTemplateColumns: "240px 120px 1fr 1fr", alignItems: "center", gap: 24,
        background: "#ffffff0a", border: "1px solid #ffffff22", borderRadius: 12,
        padding: "18px 28px", borderLeft: `6px solid ${r.safetyColor}`}}>
        <code style={{fontSize: 24, color: r.safetyColor, fontFamily: '"SF Mono", Menlo, monospace', fontWeight: 600}}>{r.name}</code>
        <span style={{fontSize: 20, color: r.safetyColor, fontWeight: 600, textAlign: "center"}}>{r.safety}</span>
        <div style={{fontSize: 20, color: "#c9d1d9"}}>{r.pros}</div>
        <div style={{fontSize: 20, color: "#8b949e"}}>{r.cons}</div>
      </div>
    </FadeIn>
  ))}
</div>
```

---

## 第二个视频的 SCENES 设计原则（13 段）

第一个视频（10 段）是"概念+例子"结构：每个机制各占 1 段，加 cover/why/choose/practice/summary/end。

第二个视频（13 段）增加了"对比+风险"结构：每种调用方式各占 1 段（接口/.call/delegatecall 各 1 段而不是合并到 1 段），加上 4 类风险、2 种防御、Foundry 项目结构、重入攻击、防御对比、下节预告。

**经验**：

- **同系列第二个视频起，建议把"风险"和"对比"显式拆成独立场景**（不要塞进 choose / summary 里）
- **攻击演示值得独立成段**（10_attack = 22s），观众需要时间看代码递归
- **下节预告建议放在 EndScene 里**（不要独立一段），节省 5s

---

## 通用建议

1. **同系列 N>3 后，可以把"项目骨架"独立成 git repo**（e.g. `~/vscode/solidity-video-template`），用 `git clone` 而不是 `cp -R` 拿骨架。这样改 Primitives.tsx 时一处改、N 处受益。

2. **保持 SCENES 数量稳定**：第一个 10 段、第二个 13 段。**不要追求 100% 对称**——按内容自然分，能 10 段就别凑 13 段。

3. **每段时长控制在 12-25s**：< 12s 场景切换太频繁，> 25s 观众视觉疲劳。短于 12s 的内容直接和相邻场景合并。

4. **render 两次是默认**：哪怕你"很确定" F[] 占位是对的，也**先 render 一次 ffprobe 确认实际帧数**，再二次 render 出 final。实测第二个视频的 F[] 占位偏差 0.3% 但相对位置偏 5-10%，导致第一遍渲染时 t=60s 显示的已经是 LowLevelScene 而不是 ThreeWays。
