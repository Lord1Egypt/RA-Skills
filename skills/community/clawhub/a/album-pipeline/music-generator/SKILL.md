# Music Generator — 音乐生成 Skill

> Phase 4 总入口。编排 3 个子模块：Prompt 生成 → Prompt 审查 → CLI 并行生成。

---

## 核心原则

1. **绝对文件契约**：所有输入/输出严格遵循 `FILE_CONTRACTS.md`，不得偏离
2. **子 agent 强制分离**：prompt-generator ≠ prompt-reviewer ≠ music-executor，3 个独立的 `sessions_spawn` 调用
3. **主 agent 只编排**：主 agent 负责启动/等待/判断完成，不直接生成 Prompt 或执行 CLI

---

## 子模块索引

| 子模块 | 路径 | 说明 |
|--------|------|------|
| Phase 4.1 | `phase4-prompt-generator/SKILL.md` | 3 版本 Prompt 生成（编曲忠实/情绪叙事/听感质感） |
| Phase 4.2 | `phase4-prompt-reviewer/SKILL.md` | Prompt 审查优化（6 项检查） |
| Phase 4.3 | `phase4-music-executor/SKILL.md` | MiniMax CLI 并行生成 |

**执行顺序**：4.1 → 4.2 → 4.3（串行依赖，每个阶段完成后才能进入下一个）

---

## 启动前提示（用户心理预期管理）

**⚠️ 飞书推送机制关键：消息在 turn 结束后才推送。必须先输出提示文本，然后 spawn 子 agent，最后 `sessions_yield`。**

**正确流程：**
1. 主 agent 输出提示：
   > 🪚 Phase 4 音乐生成已启动。{N} 首歌 × 3 个 Prompt 版本 × {语言数} 语言 = {总数} 个生成任务。预计约 **{N × 10 分钟}** 完成。完成后我会主动通知你，无需等待。
2. 按顺序 spawn 子 agent（4.1 → 4.2 → 4.3）
3. `sessions_yield` 结束当前 turn

---

## 触发

Phase 3 完成后，用户指令：
- 「生成音乐」
- 「Phase 4」
- 「music generation」

---

## 输入

- `generate/lyrics/cn/` 下的中文标准歌词文件
- `generate/lyrics/en/` 下的英文标准歌词文件
- `docs/album-overview.md` 中的曲目定位表（BPM/调性/风格）
- `songs/TN-*.md` 中的完整编曲设计（用于生成 Prompt）

---

## 执行

### ⚠️ 修改范围
- **读取**：`generate/lyrics/cn/*.txt` + `en/*.txt`、`songs/T{N}-*.md` 编曲设计
- **写入**：`generate/cn/` 和 `generate/en/` 下的新 .mp3 文件、`generate/prompts/` 下的 Prompt 文件
- **禁止**：修改歌词文件或歌曲设计文件

### 1. 3 版本 Prompt 生成

每首歌从 `songs/TN-曲名.md` 的完整编曲设计出发，生成 **3 个不同凝练方式的 Prompt 版本**。

**核心原则：压满 2000 字符上限。** 编曲设计信息太多，无法全部塞入一个 Prompt，因此用三种不同凝练策略各写一个版本，确保每个版本都尽可能详细地呈现之前的劳动成果。

#### Prompt 版本 1 — 编曲忠实还原型

**凝练策略**：按编曲段落时间线顺序凝练，保留最精确的结构描述。

**格式（≤ 2000 字符）：**
```
{流派} {风格}, {BPM}BPM, {调性}

Mood Arc: {起点情绪} → {终点情绪}

Structure Timeline:
[Intro 0:00-{end}] {音色/乐器/氛围}
[Verse {start}-{end}] {人声处理/伴奏密度/空间感}
[Pre Chorus {start}-{end}] {张力构建方式}
[Hook {start}-{end}] {高潮编曲特征/和声层次}
[Bridge {start}-{end}] {变化/留白/转折点}
[Outro {start}-{end}] {收尾方式/渐弱/留白}

Vocals: {人声类型、处理手法、和声编排}
Instruments: {主奏乐器列表 + 音色特征}
Key Elements: {关键音效/Sound Design 核心项}
Scene: {使用场景}
```

#### Prompt 版本 2 — 情绪叙事驱动型

**凝练策略**：按情绪弧线和叙事线索组织，突出歌曲的身体感和哲学内核。

**格式（≤ 2000 字符）：**
```
{流派} {风格}, {BPM}BPM, {调性}

Narrative: {核心悖论 → 情绪转化路径}

Emotional Journey:
- Opening: {开篇氛围 + 身体感暗示}
- Build: {张力累积方式 + 意象对应的音乐处理}
- Climax: {Hook 情绪峰值 + 核心 Hook 的音乐表现}
- Resolution: {收尾情绪 + 悖论的音乐化解答}

Body & Texture: {身体感关键词对应的声音质感}
Vocal Character: {人声性格 + 情感距离（贴近/疏离）}
Instrument Palette: {乐器选择 + 音色隐喻}
Spatial Design: {空间感/混/远近层次}
Key Elements: {Sound Design 中服务叙事的音效}
Scene: {使用场景}
```

#### Prompt 版本 3 — 听感质感优先型

**凝练策略**：从最终听感出发，用质感关键词驱动，适合 AI 生成模型理解。

**格式（≤ 2000 字符）：**
```
{流派} {风格}, {BPM}BPM, {调性}

Overall Texture: {整体听感描述，如 "温暖颗粒感 + 低频呼吸感"}

Sonic Layers:
Layer 1 (Foreground): {人声/主旋律 + 质感}
Layer 2 (Mid): {伴奏 + 和声 + 节奏骨架}
Layer 3 (Background): {氛围层 + Space + Drone}

Timbre Focus:
- Vocals: {音色特征 + 处理手法（近场/远场/气声/嘶吼/和声）}
- Rhythm: {鼓组特征 + 节奏密度 + Groove}
- Harmony: {和声风格 + 紧张度}
- Bass: {低频角色 + 质感}
- Lead: {主奏乐器 + 音色}
- FX: {音效/空间效果/特殊处理}

Dynamic Shape: {整曲动态曲线 — 哪里密/哪里疏}
Emotional Weight: {情绪重心 — 哪里最重/哪里最轻}
Reference Vibe: {最接近的参考感觉，但不写具体艺人名}
Scene: {使用场景}
```

### 2. Prompt 写入文件

将 3 个 Prompt 版本写入 `generate/prompts/`：

```
generate/prompts/TN-曲名-prompt1.txt
generate/prompts/TN-曲名-prompt2.txt
generate/prompts/TN-曲名-prompt3.txt
```

每个文件内容即对应 Prompt 文本（纯文本，≤ 2000 字符）。

同时生成 `generate/prompts/index.json`：

```json
{
  "songs": [
    {
      "track": "T1-出发",
      "prompts": [
        {
          "version": 1,
          "strategy": "编曲忠实还原型",
          "file": "generate/prompts/T1-出发-prompt1.txt",
          "char_count": 1980
        },
        {
          "version": 2,
          "strategy": "情绪叙事驱动型",
          "file": "generate/prompts/T1-出发-prompt2.txt",
          "char_count": 1950
        },
        {
          "version": 3,
          "strategy": "听感质感优先型",
          "file": "generate/prompts/T1-出发-prompt3.txt",
          "char_count": 1970
        }
      ]
    }
  ]
}
```

### 3. Prompt 审查优化

spawn 独立的 **Prompt 审查 Agent**，对所有 Prompt 进行审查优化。

**审查 Agent 输入**：`generate/prompts/` 下所有 Prompt 文件 + `generate/prompts/index.json`

**审查 Agent 执行**：

对每个 Prompt 版本逐项检查：

| # | 检查项 | 标准 |
|---|--------|------|
| 1 | 字符数 | ≤ 2000 且 ≥ 1500（压满上限） |
| 2 | 包含所有核心参数 | 流派/风格/BPM/调性/Mood/Vocals/Instruments |
| 3 | 无无效信息 | 不含时间戳精确到毫秒、不含 dB 值、不含 Sound Design 表格 |
| 4 | 编曲信息传递 | 至少覆盖编曲设计的 60% 核心信息 |
| 5 | 可读性 | MiniMax 音乐模型能理解的结构化文本 |
| 6 | 三版本差异化 | 3 个版本有明显差异，不是同一段文字的微调 |

**优化动作**：
- 如果字符数 < 1500 → 补充编曲细节直到接近 2000
- 如果遗漏核心参数 → 从 `songs/TN-曲名.md` 补充
- 如果包含无效信息 → 改写为模型可理解的描述
- 如果三版本差异不足 → 强化差异化

**输出**：更新 `generate/prompts/` 下的 Prompt 文件（覆盖原版），更新 `index.json` 中的 char_count。

### 4. 音乐生成

使用审查优化后的 3 个 Prompt 版本，分别生成 3 个 Take。

**N 首歌 = N 个并行 agent 群**，每个 agent 群负责一首歌的全部 Prompt 版本生成。每首歌内部：
- 3 个 Prompt 版本 → 3 个并行生成任务
- 双语专辑 → 中文 × 3 + 英文 × 3 = 6 个并行任务

⚠️ **注意**：MiniMax music-2.6 有 API rate limit。如遇 429 限流，降级为串行生成，每首完成后间隔 2-3 秒再发起下一首。

**CLI 命令**：

```bash
# Prompt 版本 1
minimax music generate \
  --model music-2.6 \
  --prompt "$(cat generate/prompts/T1-出发-prompt1.txt)" \
  --lyrics-file generate/lyrics/cn/T1-出发.txt \
  --vocals {从 prompt 中提取} \
  --genre {从 prompt 中提取} \
  --mood {从 prompt 中提取} \
  --instruments {从 prompt 中提取} \
  --bpm {从 prompt 中提取} \
  --key {从 prompt 中提取} \
  --structure {曲式结构} \
  --extra "{额外细粒度要求}" \
  --out generate/cn/T1-出发-p1.mp3

# Prompt 版本 2 → T1-出发-p2.mp3
# Prompt 版本 3 → T1-出发-p3.mp3
```

### 5. 产物管理

```
generate/cn/TN-曲名-p1.mp3
generate/cn/TN-曲名-p2.mp3
generate/cn/TN-曲名-p3.mp3
generate/en/TN-曲名-p1.mp3
generate/en/TN-曲名-p2.mp3
generate/en/TN-曲名-p3.mp3
```

3 个 Prompt 版本对应 3 个 Take（p1/p2/p3），用户听评后选定最佳版本。

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 歌词文件路径正确 | 指向 `generate/lyrics/` 下的标准文件 |
| 2 | 3 个 Prompt 版本已生成 | 每首歌有 prompt1/prompt2/prompt3，策略不同 |
| 3 | Prompt 压满上限 | 每个 Prompt ≥ 1500 且 ≤ 2000 字符 |
| 4 | Prompt 已写入文件 | `generate/prompts/TN-曲名-promptN.txt` 存在 |
| 5 | Prompt 审查优化完成 | 审查 Agent 逐项检查通过，6 项全 ✅ |
| 6 | 生成成功验证 | 文件存在、可播放、非静音/错误音频 |
| 7 | 全部 Take 完成 | 每首歌 × 3 个 Prompt 版本 × 每语言 都有产物 |

---

## 输出文件契约

严格遵循 `FILE_CONTRACTS.md` 中 Phase 4 契约。

---

## 进入 Phase 5 条件

- [ ] 每首歌 3 个 Prompt 版本均已生成
- [ ] Prompt 审查优化通过
- [ ] 所有产物文件存在且可播放
- [ ] 产物目录结构正确（cn/ + en/ 下按 p1/p2/p3 命名）

全部 ✅ → 进入 Phase 5（选定 + 转码）

---

## 关键限制

| 参数 | 值 |
|------|-----|
| 可用模型 | music-2.6（需额度）、music-2.6-free（按量付费） |
| 单次生成时长 | 可生成 3-5 分钟优质内容，质量通常随时长正比例提升（详见调优实验数据，待补充） |
| 歌词长度 | ≤ 3,500 字符 |
| Prompt 长度 | ≤ 2,000 字符（压满上限） |
| 每首歌 Take 数 | 3（对应 3 个 Prompt 版本） |
