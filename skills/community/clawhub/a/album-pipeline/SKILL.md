# Album Pipeline — AI 音乐专辑流水线 Skill

> 专辑制作流水线总入口。从概念设计到发布物料打包，6 个 Phase 完整流程。

---

## 核心原则（所有 Phase 严格遵守）

### 1. 绝对文件契约

所有 Phase 的输入/输出文件路径、格式、必填字段定义在 `FILE_CONTRACTS.md` 中。

**这是流水线的宪法。任何专家/子 agent 不得偏离。**

- 写入路由严格按契约（读什么、写什么、禁止写什么）
- 文件格式严格按契约（区块顺序、字段校验、必填项）
- 任何偏离 = bug，必须修复

### 2. 子 agent 强制分离

**主 agent 唯一职责：Phase 1 Step 0（与用户对话探索概念意图）。**

除此之外的**所有工作**必须由独立的子 agent 承担：

| Phase | 子 agent 数量 | 说明 |
|-------|-------------|------|
| Phase 1 Step 1 | 4 个 | 创意总监/市场专家/音乐总监/总评专家（并行 3 + 串行 1） |
| Phase 2 每轮 | 5 个 | 作词/编曲/韵脚/市场/评分专家（串行） |
| Phase 3 | 1 个 | 歌词标准化提取 |
| Phase 4.1 | 1 个 | 3 版本 Prompt 生成 |
| Phase 4.2 | 1 个 | Prompt 审查优化 |
| Phase 4.3 | N 个 | MiniMax CLI 并行生成（每首歌/每语言独立 agent） |
| Phase 5.1 | 1 个 | 听评选定（主 agent 配合用户） |
| Phase 5.2 | 1 个 | 质量验证 |
| Phase 6.1-6.6 | 各 1 个 | 6 个独立打包专家 |

**每个专家必须是独立的 `sessions_spawn` 调用，不得合并。**

作词专家 ≠ 编曲专家 ≠ 市场专家 ≠ 评分专家。每个都是独立的子 agent，有独立的 SKILL.md、独立的修改范围、独立的 Checklist。

### 3. 飞书推送机制 + 提示节奏

**关键机制：飞书在 turn 结束后才一次性推送消息。**

**正确模式（所有 Phase 通用）：**

```
1. 主 agent 输出提示文本（预计时长、下一步说明）
2. 立即 spawn 子 agent
3. sessions_yield 结束当前 turn → 提示推送给用户
4. 子 agent 后台工作
5. 子 agent 完成后 → 主 agent 收到通知 → 主动通知用户
```

**禁止：spawn 子 agent 后不 yield 就挂着等（主 agent 不动，用户看不到任何提示）。**

**提示节奏原则：**
- ✅ 只在**阶段边界**提示用户（Phase 启动时、Phase 完成时、需要用户决策时）
- ❌ Round 之间不停顿确认（Phase 2 内部多轮滚动自动完成，不中断）
- ✅ 只有 Phase 1 Step 0.1（概念确认开始）和 Phase 1 Step 3（方案确认）需要用户明确确认
- ✅ 其他所有 Phase 启动时提示预计时长即可，无需确认

---

## 触发

- 「做一张专辑」
- 「album pipeline」
- 「AI 音乐专辑」
- 用户表达想做概念专辑

---

## 流水线架构

```
Phase 1: Album Concept     → 专辑概念设计（叙事轴 + 曲目定位 + 调性）
Phase 2: Song Writing      → 歌曲生成（5 专家串行 × 3-6 轮迭代，N 首歌并行）
Phase 3: Lyrics Formatter  → 歌词标准化提取（结构标签 + 字符限制）
Phase 4: Music Generator   → 音乐生成（MiniMax CLI 多 Take 并行）
Phase 5: Audio Transcoder  → 选定 + 转码（320kbps/44.1kHz）
Phase 6: Album Packager    → 发布物料打包（统筹文档 + 封面 + 宣传 + 艺人说）
```

---

## 目录结构

```
skills/album-pipeline/
├── SKILL.md                     ← 本文件（总入口）
├── FILE_CONTRACTS.md            ← 绝对文件契约
├── album-concept/               ← Phase 1
├── song-writer/                 ← Phase 2 编排器
├── song-expert-lyrics/          ← Phase 2 作词专家
├── song-expert-arrangement/     ← Phase 2 编曲专家
├── song-expert-rhyme/           ← Phase 2 韵脚专家
├── song-expert-market/          ← Phase 2 市场专家
├── song-expert-scoring/         ← Phase 2 评分专家
├── lyrics-formatter/            ← Phase 3 歌词标准化
├── music-generator/             ← Phase 4 总入口（编排）
├── audio-transcoder/            ← Phase 5 总入口（编排）
├── album-packager/              ← Phase 6 总入口（编排）
│
│   ── Phase 4 子模块 ──
├── phase4-prompt-generator/     ← Phase 4.1 3 版本 Prompt 生成
├── phase4-prompt-reviewer/      ← Phase 4.2 Prompt 审查优化
├── phase4-music-executor/       ← Phase 4.3 MiniMax CLI 并行生成
│
│   ── Phase 5 子模块 ──
├── phase5-listener-selector/    ← Phase 5.1 听评选定
├── phase5-quality-verifier/     ← Phase 5.2 转码后质量验证
│
│   ── Phase 6 子模块 ──
├── phase6-album-overview-updater/  ← Phase 6.1 专辑统筹更新
├── phase6-promotional-writer/      ← Phase 6.2 宣传文档
├── phase6-artist-story-writer/     ← Phase 6.3 艺人说文案
├── phase6-cover-designer/          ← Phase 6.4 封面概念
├── phase6-platform-checker/        ← Phase 6.5 平台适配检查
└── phase6-packager/                ← Phase 6.6 最终打包
```

---

## Phase 2 详细流程

```对每首歌（T1-TN，N = Phase 1 曲目数）：
  打开已初始化的 songs/TN-曲名.md（模板已由 Phase 0.5 初始化）
  
  Round = 1 → 最多 6 轮：
    spawn 作词专家 agent → 读/写 songs/TN-曲名.md
    spawn 编曲专家 agent → 读/写 songs/TN-曲名.md
    spawn 韵脚专家 agent → 读/写 songs/TN-曲名.md
    spawn 市场专家 agent → 读/写 songs/TN-曲名.md
    spawn 评分专家 agent → 读 songs/TN-曲名.md，输出评分
                                      ↓
                                  评分 ≥ 80?
                                  ├─ 是 + Round ≥ 3 → ✅ 通过
                                  └─ 否 → 标记低分 → Round++
```

**关键规则**：
- 歌曲间**并行**（N 个 agent 群同时跑）
- 歌曲内专家**串行**（5 个独立子 agent 依次操作同一文件）
- **每个专家必须是独立的 sessions_spawn 调用，不得合并**
- **增量修改**（Round 2+ 基于上一轮评分针对性优化）
- **最少 3 轮**（即使第 1 轮就 95 分也要跑满 3 轮）
- **最多 6 轮**

---

## 每个 Phase 的质量门禁

| Phase | 入口条件 | 出口条件 | 详见 |
|-------|---------|---------|------|
| Phase 1 | 用户提供核心主题 | 曲目定位表完整 | `album-concept/SKILL.md` |
| Phase 2 | Phase 1 完成 | 所有歌曲 ≥ 80 分 + 跑满 3 轮（或达最大轮次 6 轮时取最高分版本） | `song-writer/SKILL.md` |
| Phase 3 | Phase 2 完成 | 所有歌词文件通过验证 | `lyrics-formatter/SKILL.md` |
| Phase 4 | Phase 3 完成 | 所有 Take 生成完毕 | `music-generator/SKILL.md` |
| Phase 5 | Phase 4 完成 | 选定转码验证通过 | `audio-transcoder/SKILL.md` |
| Phase 6 | Phase 5 完成 | 发布物料齐全 | `album-packager/SKILL.md` |

---

## 绝对文件契约

所有 Phase 的输入/输出文件路径、格式、必填字段定义在 `FILE_CONTRACTS.md` 中。

每个 Skill 在执行时必须遵守对应 Phase 的文件契约，不得偏离。

---

## 快速参考

| 参考项 | 路径 |
|--------|------|
| 完整流程回顾 | `docs/production-pipeline-review.md` |
| 范例歌曲 | `examples/songs/T1-出发.md`（98 分终稿） |
| 歌词范例 | `examples/lyrics/cn/T1-出发.txt` |
| MiniMax CLI | `minimax music generate --help` |
| 模型时长 | music-2.6 可生成 3-5 分钟优质内容，质量通常随时长正比例提升（详见调优实验数据，待补充） |
| 歌词长度 | ≤ 3500 字符（不含结构标签文字） |

---

## 纯音乐 / 器乐曲特殊处理

**核心原则：即使是单曲纯音乐，6 Phase 的骨架不走样。**

纯音乐只是**跳过歌词相关的专家环节**，文档一个不少，文件契约一个不缺。

### 各 Phase 纯音乐处理规则

| Phase | 常规操作 | 纯音乐调整 |
|-------|---------|----------|
| Phase 1 | 概念设计 + 曲目定位 | 无变化。曲目单中「语言」字段标注「纯音乐」 |
| Phase 2 | 5 专家串行迭代 | 作词专家**跳过歌词区块**，写「器乐描述」区块（情绪弧线/音色/段落）；韵脚专家**跳过韵脚分析**，改为「节奏/音色×编曲配合分析」；编曲/市场/评分专家**无变化** |
| Phase 3 | 歌词标准化提取 | 输出空文件 + `metadata.json` 中 `has_lyrics: false`，`validation.txt` 标注「纯音乐，跳过」 |
| Phase 4 | 3 版本 Prompt + CLI 生成 | 无 `--lyrics-file` 参数，Prompt 侧重编曲/音色/情绪描述 |
| Phase 5 | 听评选定 + 转码 + 验证 | 无变化 |
| Phase 6 | 发布物料打包 | 无变化。艺人说中说明「本曲为纯音乐」 |

### 纯音乐曲目单标识

曲目单中纯音乐曲目的「语言」字段填「纯音乐」，状态列标注「🎵 纯音乐」：

| # | 曲目 | 语言 | 状态 |
|---|------|------|------|
| 03 | T3《间奏》 | 纯音乐 | 🎵 纯音乐 |

### 纯音乐歌曲文件契约

纯音乐歌曲文件（`songs/TN-曲名.md`）结构：
- **基本信息表**：「语言」= 纯音乐
- **歌词区块**：替换为「器乐描述」区块（段落情绪/主旋律音色/编曲意图）
- **英文歌词区块**：删除或标注「纯音乐，无」
- **完整编曲设计**：正常填写
- **关键 Sound Design**：正常填写
- **韵脚分析**：替换为「节奏/音色分析」区块
- **封面高光文案**：正常填写
- **市场评估报告**：正常填写
- **数据**：正常填写（韵律维度改为「器乐表现力」维度）
- **评分进化史**：正常填写

### 全纯音乐专辑（整张专辑无歌词）

当专辑「语言」字段 =「纯音乐」时（即所有曲目均为纯音乐）：

| Phase | 影响 |
|-------|------|
| Phase 3 | `generate/lyrics/cn/` 和 `generate/lyrics/en/` 目录下**不生成任何 .txt 歌词文件**，仅生成 `metadata.json`（每首标记 `has_lyrics: false`）和 `validation.txt`（全曲标注「纯音乐，跳过」） |
| Phase 4 | Prompt 不含 `--lyrics-file` 参数，侧重编曲/音色/情绪描述；产物目录 `generate/cn/` 和 `generate/en/` 仍正常生成 .mp3 |
| Phase 5-6 | 无变化，正常转码、听评、打包 |

**目录分配总结**：即使整张专辑无歌词，`generate/lyrics/` 目录仍需创建（内含 metadata.json + validation.txt），`generate/cn/` + `generate/en/` 目录仍正常存放 .mp3 产物。

### 识别触发

Phase 1 概念设计时，如果用户指定某首为纯音乐，从 Phase 1 开始标注。
Phase 2 编排器读取曲目定位表时，自动识别「纯音乐」语言字段并调整专家流程。

## Phase 子模块索引

| Phase | 子模块 | 说明 |
|-------|--------|------|
| Phase 1 | `album-concept/SKILL.md` | 概念设计（4 专家 + 总评） |
| Phase 2 | `song-writer/SKILL.md` | 编排器 |
| Phase 2 | `song-expert-lyrics/SKILL.md` | 作词专家 |
| Phase 2 | `song-expert-arrangement/SKILL.md` | 编曲专家 |
| Phase 2 | `song-expert-rhyme/SKILL.md` | 韵脚专家 |
| Phase 2 | `song-expert-market/SKILL.md` | 市场专家 |
| Phase 2 | `song-expert-scoring/SKILL.md` | 评分专家 |
| Phase 3 | `lyrics-formatter/SKILL.md` | 歌词标准化 + metadata + validation |
| Phase 4 | `phase4-prompt-generator/SKILL.md` | 3 版本 Prompt 生成 |
| Phase 4 | `phase4-prompt-reviewer/SKILL.md` | Prompt 审查优化 |
| Phase 4 | `phase4-music-executor/SKILL.md` | MiniMax CLI 并行生成 |
| Phase 5 | `phase5-listener-selector/SKILL.md` | 听评选定 |
| Phase 5 | `phase5-quality-verifier/SKILL.md` | 转码后质量验证 |
| Phase 6 | `phase6-album-overview-updater/SKILL.md` | 专辑统筹更新 |
| Phase 6 | `phase6-promotional-writer/SKILL.md` | 宣传文档 |
| Phase 6 | `phase6-artist-story-writer/SKILL.md` | 艺人说文案 |
| Phase 6 | `phase6-cover-designer/SKILL.md` | 封面概念 |
| Phase 6 | `phase6-platform-checker/SKILL.md` | 平台适配检查 |
| Phase 6 | `phase6-packager/SKILL.md` | 最终打包 |
