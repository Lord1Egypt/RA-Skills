# Phase 4 — Music Executor Skill

> 使用 MiniMax CLI 批量生成音乐，3 个 Prompt 版本并行执行。

---

## 触发

phase4-prompt-reviewer 审查通过后自动启动。

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 4 | `generate/prompts/T{N}-曲名-prompt{1,2,3}.txt` | 审查通过的 3 个 Prompt 版本 |
| Phase 3 | `generate/lyrics/cn/T{N}-曲名.txt` | 中文标准歌词 |
| Phase 3 | `generate/lyrics/en/T{N}-曲名.txt` | 英文标准歌词（如适用） |
| Phase 4 | `generate/prompts/index.json` | Prompt 索引（含参数提取参考） |

---

## 执行

### ⚠️ 修改范围
- **读取**：`generate/prompts/*.txt`、`generate/lyrics/cn/*.txt`、`generate/lyrics/en/*.txt`、`index.json`
- **写入**：`generate/cn/T{N}-曲名-p{1,2,3}.mp3`、`generate/en/T{N}-曲名-p{1,2,3}.mp3`
- **禁止**：修改 `generate/prompts/` 或 `generate/lyrics/` 中的任何文件

### 并行策略

**N 首歌 = N 个并行 agent 群**，每个 agent 群负责一首歌的全部 Prompt 版本生成。

每首歌内部：
- 3 个 Prompt 版本 → 3 个并行生成任务
- 双语专辑 → 中文 × 3 + 英文 × 3 = 6 个并行任务

⚠️ **限流处理**：MiniMax music-2.6 有 API rate limit。如遇 429 响应，降级为串行生成，每首完成后间隔 2-3 秒再发起下一首。

### CLI 命令模板

**常规歌曲：**

```bash
minimax music generate \
  --model music-2.6 \
  --prompt "$(cat generate/prompts/T1-出发-prompt1.txt)" \
  --lyrics-file generate/lyrics/cn/T1-出发.txt \
  --vocals "{从 prompt 提取}" \
  --genre "{从 prompt 提取}" \
  --mood "{从 prompt 提取}" \
  --instruments "{从 prompt 提取}" \
  --bpm "{从 prompt 提取}" \
  --key "{从 prompt 提取}" \
  --structure "{曲式结构}" \
  --extra "{额外细粒度要求}" \
  --out generate/cn/T1-出发-p1.mp3
```

**纯音乐曲目：**

```bash
minimax music generate \
  --model music-2.6 \
  --prompt "$(cat generate/prompts/T3-间奏-prompt1.txt)" \
  --genre "{从 prompt 提取}" \
  --mood "{从 prompt 提取}" \
  --instruments "{从 prompt 提取}" \
  --bpm "{从 prompt 提取}" \
  --key "{从 prompt 提取}" \
  --structure "{曲式结构}" \
  --extra "{额外细粒度要求}" \
  --out generate/cn/T3-间奏-p1.mp3
```

纯音乐无 `--lyrics-file` 参数。

### 产物管理

```
generate/cn/TN-曲名-p1.mp3
generate/cn/TN-曲名-p2.mp3
generate/cn/TN-曲名-p3.mp3
generate/en/TN-曲名-p1.mp3
generate/en/TN-曲名-p2.mp3
generate/en/TN-曲名-p3.mp3
```

### 参数提取规则

从 Prompt 文本中提取 CLI 参数：
| CLI 参数 | 提取来源 | 示例 |
|---------|---------|------|
| --vocals | Vocals/Vocal Character/Timbre Focus → Vocals | "清唱进入，混响深，气声" |
| --genre | 首行流派/风格 | "氛围电子+叙事感" |
| --mood | Mood Arc/Narrative/Emotional Journey | "从困到走的转变" |
| --instruments | Instruments/Instrument Palette | "钢琴单音，左手八度低音" |
| --bpm | 首行 BPM 值 | 85 |
| --key | 首行调性 | "B小调" |
| --structure | Structure Timeline 中的段落列表 | "Intro-Verse-Pre Chorus-Hook-Bridge-Outro" |
| --extra | 未在以上参数中覆盖的细粒度要求 | "心跳采样垫底，窗外风声-40dB" |

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 生成任务全部完成 | N 首 × 3 Prompt × 语言数 = 全部产物文件存在 |
| 2 | 文件可播放 | 非静音/错误音频，文件大小 ≥ 100KB |
| 3 | 产物目录结构正确 | cn/ + en/ 下按 `TN-曲名-p{1,2,3}.mp3` 命名 |
| 4 | 原始文件未污染 | 未修改 `generate/prompts/` 或 `generate/lyrics/` 中的文件 |
| 5 | 生成日志已保存 | 记录每首生成耗时/模型版本/CLI 参数 |

全部 ✅ → 进入 Phase 5（选定 + 转码）
