# Lyrics Formatter — 歌词标准化提取 Skill

> Phase 3 入口。从 Phase 2 产出的 `songs/TN-*.md` 中提取标准歌词文件，供 Phase 4 音乐生成使用。

---

## 核心原则

1. **绝对文件契约**：所有输入/输出严格遵循 `FILE_CONTRACTS.md`，不得偏离
2. **子 agent 执行**：歌词标准化提取由独立的 `sessions_spawn` 子 agent 完成
3. **主 agent 只编排**：主 agent 负责启动/等待/验证结果，不直接提取歌词

---

## 启动前提示（用户心理预期管理）

**⚠️ 飞书推送机制关键：消息在 turn 结束后才推送。必须先输出提示文本，然后 spawn 子 agent，最后 `sessions_yield`。**

**正确流程：**
1. 主 agent 输出提示：
   > 🪚 Phase 3 歌词标准化提取已启动。预计约 **{N × 2 分钟}** 完成。完成后我会主动通知你，无需等待。
2. 立即 spawn 子 agent
3. `sessions_yield` 结束当前 turn

---

## 触发

Phase 2 全部歌曲通过后,用户指令:
- 「提取歌词」
- 「Phase 3」
- 「歌词标准化」

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 2 | `docs/album-overview.md` | 曲目单 + **语言**字段 |
| Phase 2 | `songs/TN-曲名.md` | 每首歌的完整歌词区块 |

---

## 执行

### ⚠️ 修改范围
- **读取**:`songs/T{N}-曲名.md` 中的「歌词」区块
- **写入**:`generate/lyrics/cn/` 和 `generate/lyrics/en/` 下的新文件
- **禁止**:修改 `songs/` 目录中的任何源文件

### 1. 语言判断

从 `docs/album-overview.md` 读取 `**语言**` 字段:

| 语言 | 提取中文 | 提取英文 |
|------|---------|---------|
| 中文 | ✅ 读取「歌词」区块 → `cn/` | - |
| 中文+英文 | ✅ 读取「歌词」区块 → `cn/` | ✅ 读取「英文歌词」区块 → `en/` |
| 英文 | - | ✅ 读取「英文歌词」区块 → `en/` |
| **纯音乐** | - | - |

**纯音乐处理**:跳过该曲目的歌词提取,在 `metadata.json` 中标记 `has_lyrics: false`,在 `validation.txt` 中标注「纯音乐,跳过」。

### 2. 逐首歌提取中文歌词(语言 = 中文 / 中文+英文)

对每首 `songs/TN-曲名.md`:
- 读取「歌词」区块(从 `## 歌词` 到下一个 `##` 之间的内容)
- 去掉所有注释、编曲描述、市场分析
- 保留纯歌词 + 结构标签
- 确保结构标签使用官方支持格式
- **写入** `generate/lyrics/cn/TN-曲名.txt`

### 3. 逐首歌提取英文歌词(语言 = 英文 / 中文+英文)

对每首 `songs/TN-曲名.md`:
- 读取「英文歌词」区块(从 `## 英文歌词` 到下一个 `##` 之间的内容)
- 去掉所有注释、编曲描述、市场分析
- 保留纯歌词 + 结构标签
- 确保结构标签使用官方支持格式
- **写入** `generate/lyrics/en/TN-曲名.txt`

### 4. 输出标准歌词文件

```
generate/lyrics/cn/TN-曲名.txt    ← 中文标准歌词(中文/中文+英文专辑必填)
generate/lyrics/en/TN-曲名.txt    ← 英文标准歌词(英文/中文+英文专辑必填)
```

### 5. 生成歌词元数据

输出 `generate/lyrics/metadata.json`:
```json
{
  "songs": [
    {
      "track": "T1-出发",
      "cn": {
        "file": "generate/lyrics/cn/T1-出发.txt",
        "char_count": 1234,
        "structure_tags": ["Intro", "Verse", "Pre Chorus", "Hook", "Bridge", "Outro"],
        "section_count": 6,
        "has_hook": true,
        "tags_valid": true,
        "language": "中文"
      },
      "en": {
        "file": "generate/lyrics/en/T1-出发.txt",
        "char_count": 1180,
        "structure_tags": ["Intro", "Verse", "Hook", "Outro"],
        "section_count": 4,
        "has_hook": true,
        "tags_valid": true,
        "language": "英文"
      }
    }
  ]
}
```

### 6. 验证

对每个歌词文件:
- 确认字符数 ≤ 3500
- 确认结构标签内无描述文字
- 确认至少包含 [Verse] + [Hook/Chorus] + [Outro]

验证结果写入 `generate/lyrics/validation.txt`:

**中文/中文+英文专辑:**
```
[T1-出发] CN: ✅ EN: ✅  | 结构(示例): [Intro][Verse][Hook][Bridge][Outro]
```

**英文专辑:**
```
[T1-出发] EN: ✅  | 结构(示例): [Intro][Verse][Hook][Outro]
```

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 纯歌词无注释 | 去掉所有编曲描述、市场分析、注释 |
| 2 | 结构标签正确 | 使用官方支持标签,不在标签内夹描述文字 |
| 3 | 字符数 ≤ 3500 | 纯歌词字符 ≤ 3500(不含结构标签文字) |
| 4 | cn/en 输出正确 | 中文专辑只输出 cn/;英文专辑只输出 en/;中文+英文专辑输出 cn/ + en/,结构对齐 |
| 5 | 伴唱用圆括号 | `(Ooh)` `(Harmonize)` 等格式正确 |
| 6 | metadata.json 已生成 | 每首歌的歌词元数据完整,结构标签列表准确 |
| 7 | validation.txt 已生成 | 每首歌双版本验证结果,全 ✅ |

---

## 输出文件契约

严格遵循 `FILE_CONTRACTS.md` 中 Phase 3 契约。

---

## 进入 Phase 4 条件

- [ ] 所有曲目的歌词文件已生成(根据语言决定 cn/ 和/或 en/)
- [ ] 所有文件通过验证(字符数/标签/内容)
- [ ] `generate/lyrics/metadata.json` 已生成
- [ ] `generate/lyrics/validation.txt` 全 ✅

全部 ✅ → 进入 Phase 4(音乐生成)

---

## 参考

`examples/lyrics/cn/T1-出发.txt` 是格式范例。
