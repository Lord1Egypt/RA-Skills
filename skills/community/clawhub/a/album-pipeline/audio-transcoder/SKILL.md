# Audio Transcoder — 音频转码 Skill

> Phase 5 总入口。编排 2 个子模块：听评选定 → 质量验证。

---

## 核心原则

1. **绝对文件契约**：所有输入/输出严格遵循 `FILE_CONTRACTS.md`，不得偏离
2. **子 agent 强制分离**：listener-selector ≠ quality-verifier，2 个独立的子 agent
3. **主 agent 只编排**：主 agent 负责启动/等待/配合用户听评，不直接转码或验证

---

## 子模块索引

| 子模块 | 路径 | 说明 |
|--------|------|------|
| Phase 5.1 | `phase5-listener-selector/SKILL.md` | 听评选定最佳 Prompt 版本 |
| Phase 5.2 | `phase5-quality-verifier/SKILL.md` | 转码后质量验证（bitrate/sample_rate/LUFS/时长） |

**执行顺序**：5.1 → 转码（主 agent 执行 ffmpeg）→ 5.2（验证）

---

## 启动前提示（用户心理预期管理）

**⚠️ 飞书推送机制关键：消息在 turn 结束后才推送。必须先输出提示文本，然后 spawn 子 agent，最后 `sessions_yield`。**

**正确流程：**
1. 主 agent 输出提示：
   > 🪚 Phase 5 选定 + 转码已启动。{N} 首 × 2 语言 = {总数} 个转码任务。预计约 **{N × 3 分钟}** 完成。完成后我会主动通知你，无需等待。
2. spawn 5.1 listener-selector（听评由主 agent 配合用户）
3. `sessions_yield` 结束当前 turn

---

## 触发

Phase 4 完成后，用户指令：
- 「选定并转码」
- 「Phase 5」
- 「听评选定」

---

## 输入

- `generate/cn/` 下的所有中文生成物（各 Take 版本）
- `generate/en/` 下的所有英文生成物

---

## 执行

### ⚠️ 修改范围
- **读取**：`generate/cn/*.mp3` + `generate/en/*.mp3`、用户选定表
- **写入**：`generate/cn_320k/` 和 `generate/en_320k/` 下的新 .mp3 文件
- **禁止**：修改原始生成文件或删除任何 .mp3

### 1. 听评选定

用户听完所有生成物（3 个 Prompt 版本 × 每语言），给出选定表：

```
CN版：T1-p1, T2-p1, T3-p3, ...
EN版：T1-p2, T2-p1, T3-p1, ...
```

### 2. 转码 + 响度归一化

对每首选定版本，执行两步处理：

**Step 1: 转码（320kbps/44.1kHz）：**
```bash
ffmpeg -i input.mp3 -b:a 320000 -ar 44100 -y temp.mp3
```

**Step 2: 响度归一化（-14 LUFS，网易云标准）：**
```bash
ffmpeg -i temp.mp3 -af loudnorm=I=-14:TP=-1.5:LRA=11 -y output.mp3
```

### 3. 验证

对每个输出文件，运行 ffprobe 验证：
```bash
ffprobe -v error -show_entries format=bit_rate:stream=sample_rate -of json output.mp3
```

确认：bit_rate=320000, sample_rate=44100

**时长验证：**
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 output.mp3
```
确认：时长在合理范围内（≥ 1:00 且 ≤ 6:00）

### 4. 输出

```
generate/cn_320k/TN-曲名-pX.mp3
generate/en_320k/TN-曲名-pX.mp3
```

### 5. 响度报告

生成 `generate/loudness-report.txt`：
```
（示例）
[T1-出发] CN: -13.8 LUFS | 2:47 | ✅
[T1-出发] EN: -14.1 LUFS | 2:47 | ✅
[T2-数据] CN: -13.9 LUFS | 3:12 | ✅
...
```

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 每首选定一个 Prompt 版本（p1/p2/p3） | N 首 × 2 语言，无遗漏 |
| 2 | 转码参数正确 | 320kbps, 44.1kHz, MP3 |
| 3 | 响度归一化 | -14 LUFS ± 0.5 LUFS |
| 4 | 时长验证 | ≥ 1:00 且 ≤ 6:00 |
| 5 | ffprobe 验证通过 | bit_rate=320000, sample_rate=44100 |
| 6 | 输出目录隔离 | 只在 `cn_320k/` `en_320k/`，不污染原始目录 |
| 7 | 响度报告已生成 | `generate/loudness-report.txt` 包含每首数据 |

---

## 输出文件契约

严格遵循 `FILE_CONTRACTS.md` 中 Phase 5 契约。

---

## 进入 Phase 6 条件

- [ ] 所有曲目已选定并转码
- [ ] 所有文件验证通过（bit_rate/sample_rate/响度/时长）
- [ ] `cn_320k/` 文件数 = `en_320k/` 文件数 = 曲目数
- [ ] `generate/loudness-report.txt` 全 ✅

全部 ✅ → 进入 Phase 6（发布物料打包）
