# Phase 4 — Prompt Generator Skill

> 从完整编曲设计生成 3 个不同凝练策略的 Prompt 版本，每个压满 2000 字符上限。

---

## 触发

Phase 3 完成后，主 agent 启动 Phase 4 流程的第一步。

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 2 | `songs/T{N}-曲名.md` | 完整编曲设计（段落/时间/乐器/Sound Design/情绪弧线） |
| Phase 2 | `songs/T{N}-曲名.md` | 基本信息表（BPM/调性/风格/情绪弧线/核心悖论） |
| Phase 3 | `generate/lyrics/cn/T{N}-曲名.txt` | 中文标准歌词（纯音乐曲目不存在） |
| Phase 3 | `generate/lyrics/en/T{N}-曲名.txt` | 英文标准歌词（如适用，纯音乐曲目不存在） |

**纯音乐处理**：纯音乐曲目无 `--lyrics-file` 参数，Prompt 侧重编曲/音色/情绪描述。3 个版本的凝练策略不变。

---

## 执行

### ⚠️ 修改范围
- **读取**：`songs/T{N}-曲名.md`（编曲设计 + 基本信息）、`generate/lyrics/cn/*.txt`（常规歌曲）、`generate/lyrics/en/*.txt`（如适用，常规歌曲）
- **写入**：`generate/prompts/T{N}-曲名-promptN.txt`
- **禁止**：修改 `songs/` 或 `generate/lyrics/` 中的任何文件

### 核心原则

完整编曲设计信息量太大，无法直接塞入一个 Prompt（music-2.6 限制 ≤ 2000 字符）。因此用**三种不同凝练策略**各写一个版本，确保每个版本都尽可能详细地传递编曲劳动成果。

### Prompt 版本 1 — 编曲忠实还原型

**凝练策略**：按编曲段落时间线顺序，保留最精确的结构描述。

**输出格式（≤ 2000 字符）：**
```
{流派} {风格}, {BPM}BPM, {调性}

Mood Arc: {起点情绪} → {终点情绪}

Structure Timeline:
[Intro] {音色/乐器/氛围}
[Verse] {人声处理/伴奏密度/空间感}
[Pre Chorus] {张力构建方式}
[Hook] {高潮编曲特征/和声层次}
[Bridge] {变化/留白/转折点}
[Outro] {收尾方式/渐弱/留白}

Vocals: {人声类型、处理手法、和声编排}
Instruments: {主奏乐器列表 + 音色特征}
Key Elements: {关键音效/Sound Design 核心项}
Scene: {使用场景}
```

**凝练规则：**
- 保留每段的核心时间范围和编曲动作
- 去掉精确到毫秒的时间戳、dB 值、Sound Design 表格
- 将技术性描述转化为音乐模型可理解的感性描述
- 至少覆盖编曲设计的 60% 核心信息

### Prompt 版本 2 — 情绪叙事驱动型

**凝练策略**：按情绪弧线和叙事线索组织，突出身体感和哲学内核。

**输出格式（≤ 2000 字符）：**
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
Spatial Design: {空间感/混响/远近层次}
Key Elements: {Sound Design 中服务叙事的音效}
Scene: {使用场景}
```

**凝练规则：**
- 以核心悖论为叙事主线，串联全曲情绪
- 将 Sound Design 中服务叙事的关键音效提取出来
- 强调人声的情感距离（贴近/疏离/气声/嘶吼）
- 保留身体感关键词的声音质感映射

### Prompt 版本 3 — 听感质感优先型

**凝练策略**：从最终听感出发，用质感关键词驱动，最适合 AI 生成模型理解。

**输出格式（≤ 2000 字符）：**
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

**凝练规则：**
- 从听众最终听到的质感出发，不是从编曲过程出发
- 用"层"的概念组织信息（前景/中景/背景）
- 每个频段/乐器角色都有明确的质感描述
- 包含动态曲线和情绪重心分布

---

## 写入文件

将 3 个 Prompt 版本写入：

```
generate/prompts/TN-曲名-prompt1.txt
generate/prompts/TN-曲名-prompt2.txt
generate/prompts/TN-曲名-prompt3.txt
```

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

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 3 个版本均已生成 | prompt1/prompt2/prompt3 文件存在 |
| 2 | 字符数达标 | 每个 Prompt ≥ 1500 且 ≤ 2000 字符 |
| 3 | 三版本差异化明显 | 不是同一段文字的微调，凝练策略完全不同 |
| 4 | 核心参数完整 | 流派/风格/BPM/调性/Mood/Vocals/Instruments/Scene 都有 |
| 5 | 无无效信息 | 不含精确毫秒级时间戳、不含 dB 值、不含表格 |
| 6 | 编曲信息传递 ≥ 60% | 从完整编曲设计中提取了核心编曲意图 |
| 7 | index.json 已生成 | 每首歌 3 个 Prompt 的元数据完整 |
| 8 | 语言匹配 | 中文专辑生成中文 Prompt，双语专辑生成中英文 Prompt |

全部 ✅ → 进入 Prompt 审查阶段（phase4-prompt-reviewer）
