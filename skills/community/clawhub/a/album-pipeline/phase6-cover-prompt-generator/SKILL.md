# Phase 6.4.5 — Cover Prompt Generator Skill

> 从封面概念方案和歌曲核心意象生成 3 个不同视觉策略的图片生成 Prompt，用于 MiniMax image-01 模型。

---

## 触发

phase6-cover-designer 完成后自动启动。

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 6 | `docs/cover-concept.md` | 封面概念方案（≥3 个视觉方向 + 配色方案） |
| Phase 1 | `docs/album-overview.md` | 核心概念/叙事轴/调性主线 |
| Phase 2 | `songs/T{N}-曲名.md` | 每首歌的核心意象/身体感/情绪弧线 |

---

## 执行

### ⚠️ 修改范围
- **读取**：`docs/cover-concept.md`、`docs/album-overview.md`、`songs/T{N}-*.md`
- **写入**：`generate/covers/prompts/album-cover-prompt{1,2,3}.txt`、`generate/covers/prompts/T{N}-曲名-cover-prompt{1,2,3}.txt`
- **禁止**：修改任何源文档文件

### 核心原则

封面概念方案是设计意图的文字描述，image-01 模型需要结构化的视觉 Prompt 才能生成高质量图片。因此将概念方案翻译为 **3 个不同视觉策略** 的 Prompt 版本，每个 ≤ 1000 字符（image-01 模型不需要太长）。

### 专辑封面 Prompt — 版本 1：概念忠实型

**凝练策略**：直接映射 `docs/cover-concept.md` 中的最佳视觉方向，忠实还原设计意图。

**输出格式（≤ 1000 字符）：**
```
Album cover art, {主视觉描述 from cover-concept.md}, {色调}, {构图方式}, {质感/风格}, {排版暗示}
Style: {摄影/插画/3D渲染/抽象}, Mood: {情绪}, Color palette: {主色 HEX + 辅色 HEX}
Usage: 3000x3000px square format, centered composition
```

**凝练规则：**
- 从 cover-concept.md 的配色方案提取 HEX 色值
- 保留核心悖论的视觉隐喻
- 强调"小图可辨识"（流媒体缩略图场景）

### 专辑封面 Prompt — 版本 2：情绪氛围型

**凝练策略**：从专辑情绪弧线和身体感出发，强调氛围、色调和感官体验。

**输出格式（≤ 1000 字符）：**
```
Album cover art, {氛围场景描述}, {色调/光线}, {空间感}, {质感}, {情绪基调}
Style: {摄影/插画/3D渲染/抽象}, Mood: {情绪弧线起点→终点映射}, Color palette: {主色 HEX + 辅色 HEX}
Usage: 3000x3000px square format, atmospheric composition, negative space for typography
```

**凝练规则：**
- 从 songs/T{N}-*.md 的情绪弧线提取身体感关键词
- 强调光线/色调/空间感（氛围优先）
- 留白考虑（为后续专辑名/艺人名排版留空间）

### 专辑封面 Prompt — 版本 3：极简符号型

**凝练策略**：提取核心悖论为一个视觉符号，极简构图，强视觉冲击。

**输出格式（≤ 1000 字符）：**
```
Album cover art, {核心视觉符号}, {极简背景}, {对比/张力}, {排版暗示}
Style: {极简插画/图形设计/符号摄影}, Mood: {核心悖论的视觉张力}, Color palette: {主色 HEX + 点缀色 HEX}
Usage: 3000x3000px square format, bold centered element, high contrast
```

**凝练规则：**
- 将核心悖论浓缩为一个可视觉化的符号
- 极简主义（少即是多）
- 高对比度，小图辨识度高

### 单曲封面 Prompt

为每首歌生成对应的单曲封面 Prompt（复用专辑封面的 3 版本策略）：

```
generate/covers/prompts/T{N}-曲名-cover-prompt1.txt
generate/covers/prompts/T{N}-曲名-cover-prompt2.txt
generate/covers/prompts/T{N}-曲名-cover-prompt3.txt
```

单曲封面从对应歌曲的 `songs/T{N}-*.md` 提取：
- 核心意象（3-5 个）
- 身体感
- 情绪弧线
- 封面高光文案

在专辑统一视觉语言下，单曲封面做小变体。

### Prompt 索引

同时生成 `generate/covers/prompts/index.json`：

```json
{
  "album": {
    "prompts": [
      {
        "version": 1,
        "strategy": "概念忠实型",
        "file": "generate/covers/prompts/album-cover-prompt1.txt",
        "char_count": 850
      },
      {
        "version": 2,
        "strategy": "情绪氛围型",
        "file": "generate/covers/prompts/album-cover-prompt2.txt",
        "char_count": 820
      },
      {
        "version": 3,
        "strategy": "极简符号型",
        "file": "generate/covers/prompts/album-cover-prompt3.txt",
        "char_count": 790
      }
    ]
  },
  "tracks": [
    {
      "track": "T1-出发",
      "prompts": [
        { "version": 1, "strategy": "概念忠实型", "file": "generate/covers/prompts/T1-出发-cover-prompt1.txt", "char_count": 800 },
        { "version": 2, "strategy": "情绪氛围型", "file": "generate/covers/prompts/T1-出发-cover-prompt2.txt", "char_count": 780 },
        { "version": 3, "strategy": "极简符号型", "file": "generate/covers/prompts/T1-出发-cover-prompt3.txt", "char_count": 760 }
      ]
    }
  ]
}
```

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 专辑封面 3 个 Prompt 已生成 | prompt1/prompt2/prompt3 文件存在 |
| 2 | 每首歌 3 个单曲封面 Prompt 已生成 | N 首歌 × 3 个文件 |
| 3 | 字符数合规 | 每个 Prompt ≤ 1000 字符 |
| 4 | 三版本差异化明显 | 概念忠实型 / 情绪氛围型 / 极简符号型，策略完全不同 |
| 5 | 配色方案已映射 | HEX 色值从 cover-concept.md 正确提取 |
| 6 | 核心悖论/意象已融入 | Prompt 反映专辑核心概念 |
| 7 | index.json 已生成 | 专辑 + 所有单曲的 Prompt 元数据完整 |
| 8 | 留白/排版考虑 | 至少一个版本包含 typography negative space 提示 |

全部 ✅ → 进入 phase6-cover-executor
