# Album Pipeline — 绝对文件契约（Absolute File Contracts）

> 本文档定义流水线每个 Phase 的输入/输出文件路径、格式、必填字段。
> 所有 Skill 必须严格遵守，不得偏离。

---

## 项目根目录

```
<project-root>/                    ← 专辑项目根目录（如 album-新专辑/）
├── songs/                         ← Phase 2 产出（歌曲设计文件）
│   ├── T1-曲名.md
│   ├── T2-曲名.md
│   └── ...
├── docs/                          ← Phase 1 + Phase 6 产出
│   ├── album-overview.md          ← Phase 1 主产物
│   ├── cover-concept.md           ← Phase 6.4
│   ├── promotional-materials.md   ← Phase 6
│   ├── artist-story-cn.md         ← Phase 6
│   ├── artist-story-en.md         ← Phase 6
│   ├── artist-story-short.md      ← Phase 6
│   ├── artist-story-quotes.md     ← Phase 6
│   ├── platform-check.txt         ← Phase 6.5
│   ├── promo-video.mp4            ← Phase 6.7 宣传视频完整版
│   └── promo-video-15s.mp4        ← Phase 6.7 宣传视频精简版
├── generate/                      ← Phase 3-4 产出
│   ├── prompts/                   ← Phase 4 Prompt 文件
│   │   ├── TN-曲名-prompt1.txt
│   │   ├── TN-曲名-prompt2.txt
│   │   ├── TN-曲名-prompt3.txt
│   │   └── index.json
│   ├── lyrics/cn/                 ← Phase 3 中文标准歌词
│   ├── lyrics/en/                 ← Phase 3 英文标准歌词
│   ├── cn/                        ← Phase 4 中文原始生成
│   ├── en/                        ← Phase 4 英文原始生成
│   ├── cn_320k/                   ← Phase 5 中文最终交付
│   ├── en_320k/                   ← Phase 5 英文最终交付
│   └── covers/                    ← Phase 6.4.5-6.4.6 封面产物
│       ├── album-cover-p1.png
│       ├── album-cover-p2.png
│       ├── album-cover-p3.png
│       ├── prompts/               ← Phase 6.4.5 Prompt 文件
│       │   ├── album-cover-prompt{1,2,3}.txt
│       │   ├── T{N}-曲名-cover-prompt{1,2,3}.txt
│       │   └── index.json
│       └── tracks/                ← Phase 6.4.6 单曲封面
│           └── T{N}-曲名-p{1,2,3}.png
└── assets/                        ← Phase 6 封面概念图
```

---

## Phase 1 契约

### 输入

无文件输入。由主 agent 与用户对话收集概念意图。

### ⚠️ 硬规则：文件修改范围限制

**所有 Phase 1 子 agent（4 个专家）必须严格遵守以下规则：**

1. **只修改自己负责的区块**，不得修改其他区块
2. **不得新增区块**（除合约明确允许的可选区块外）
3. **不得删减区块**（所有必填区块必须保留）
4. **不得修改文件结构顺序**（区块必须按合约定义顺序排列）
5. **只读依赖**：可以读取前序专家已写入的内容，但不得修改

**各专家修改范围：**

| 专家 | 可写区块 | 可读但不可写区块 |
|------|---------|-----------------|
| 创意总监 | 专辑概述、叙事轴线、曲目单、待办事项（初始化） | 市场分析/调性主线/英文信息/评分总览（只读） |
| 市场专家 | 市场分析、核心传播概念（位于市场分析区块内）、英文专辑信息 | 专辑概述/曲目单/调性/评分（只读） |
| 音乐总监 | 调性主线 | 专辑概述/曲目单/市场分析/英文信息/评分（只读） |
| 总评专家 | 评分总览 | 所有已有区块（只读） |

### 输出文件（唯一）

`docs/album-overview.md`

### 文件结构（严格）

```markdown
# 《{中文名}》专辑统筹文档

> 状态：概念设计中
> 更新日期：YYYY-MM-DD
> 优化轮次：Round{N}

---

## 专辑概述

**专辑名称**：《{中文名}》 / **{English Name}**
**核心概念**：{1-2 句话}
**核心悖论**：{一句话}
**目标听众**：{描述}
**参考风格**：{参考艺人/专辑}

**叙事轴线**：
- **{轴名1}**：{轴含义}，{曲目列表}
- **{轴名2}**：{轴含义}，{曲目列表}
- ...（至少 2 条，最多 5 条）

---

## 市场分析

**市场定位**：{一句话定位}
**目标受众**：{精准画像，2-3 层}
**竞品差异化**：{与同类作品的差异点}
**核心传播概念**：{一句话，可独立传播}
**潜在风险**：{≥1 个风险 + 应对策略}

### 英文专辑信息（网易云 / 发行用）

### Album Name
**{English Name}**

### Album Description
{2-4 句英文，适合流媒体平台展示}

### Creator's Note
{第一人称英文，3-6 段，讲述创作动机和专辑含义}

### Track One-Liners

| # | Track | English Title | One-Liner |
|---|-------|--------------|-----------|
| 01 | T1 {曲名} | {英文} | {一句话介绍} |
| ... | | | |

---

## 曲目单

| # | 曲目 | 英文名 | 方向 | 核心Hook | 核心悖论 | 核心意象 | 身体感 | 情绪弧线 | 编曲风格 | 时长(估) | 状态 |
|---|------|--------|------|----------|----------|----------|--------|----------|----------|----------|------|
| 01 | T1《{曲名}》 | {English} | {轴名} | {Hook} | {悖论} | {意象1}/{意象2}/{意象3} | {身体感1}/{身体感2} | {起点}→{终点} | {风格}，{调性}，{BPM}BPM | ~{M}:{SS} | ⏳ 待生成 |
| ... | | | | | | | | | | | |

**✅ 时长状态**：{汇总描述}

---

## 调性主线

{主调性}
调性分布：T1 {调性} | T2 {调性} | ...
调性逻辑：{设计说明}

---

## 评分总览（Round{N}）

| 维度 | 分数 | 评语 |
|------|------|------|
| 概念原创性 | {0-25} | {评语} |
| 叙事连贯性 | {0-25} | {评语} |
| 市场潜力 | {0-25} | {评语} |
| 音乐一致性 | {0-25} | {评语} |

总分：{XX}/100

---

## 待办事项

- [x] Phase 1 概念确认（Round{N}）
- [ ] Phase 2 歌曲生成
- [ ] Phase 3 歌词标准化
- [ ] Phase 4 音乐生成
- [ ] Phase 5 选定与转码
- [ ] Phase 6 发布物料
```

### 必填字段校验

| 字段 | 类型 | 必填 | 校验规则 |
|------|------|------|---------|
| 语言 | enum | ✅ | 中文 / 中文+英文 / 英文 / 纯音乐 四选一 |
| 专辑名称（中） | string | ✅ | 2-6 字符 |
| 专辑名称（英） | string | ✅ | 1-5 词 |
| 核心概念 | string | ✅ | 50-200 字符 |
| 核心悖论 | string | ✅ | ≤ 50 字符 |
| 叙事轴线 | array | ✅ | ≥ 2 条，覆盖所有曲目 |
| 曲目单 | array | ✅ | 每首 11 字段，数量 = 用户指定的曲目数 |
| 市场定位 | string | ✅ | ≤ 50 字符，一句话 |
| 目标受众 | string | ✅ | 2-3 层受众画像 |
| 竞品差异化 | string | ✅ | ≥1 个差异点 |
| 核心传播概念 | string | ✅ | ≤ 30 字符，可独立传播 |
| 潜在风险 | string | ✅ | ≥1 个风险 + 应对 |
| 调性主线 | object | ✅ | 主调性 + 各曲调性 |
| 评分总览 | table | ✅ | 4 维度 × 25 分，总分 100 |
| Track One-Liners | table | ✅ | N 首，每首一句话 |
| Album Description | string | ✅ | 50-300 英文字符 |
| Creator's Note | string | ✅ | 100-800 英文字符 |

### Phase 1 产物验证

完成后必须确认：
- [ ] `docs/album-overview.md` 存在
- [ ] 曲目单行数 = 用户指定的曲目数
- [ ] 所有曲目的叙事轴都存在于"叙事轴线"列表
- [ ] 调性主线包含所有曲目的调性
- [ ] 评分总览所有维度总分 ≥ 80
- [ ] **用户已确认概念方向**

### Phase 1 可选区块清单

Phase 1 不允许新增任何区块。所有区块均为必填。

---

## Phase 2 契约

### ⚠️ 硬规则：文件修改范围限制

**所有 Phase 2 子 agent（5 个专家）必须严格遵守以下规则：**

1. **只修改自己负责的区块**，不得修改其他区块
2. **不得新增区块**（除合约明确允许的可选区块外）
3. **不得删减区块**（所有必填区块必须保留）
4. **不得修改文件结构顺序**（区块必须按合约定义顺序排列）
5. **只读依赖**：可以读取前序专家已写入的内容，但不得修改

**各专家修改范围：**

| 专家 | 可写区块 | 可读但不可写区块 |
|------|---------|-----------------|
| 作词专家 | 歌词（中文版）、英文歌词（双语/英文专辑时） | 基本信息/其他区块（只读） |
| 编曲专家 | 完整编曲设计、关键 Sound Design | 基本信息/歌词/其他区块（只读） |
| 韵脚专家 | 韵脚分析（Round 1 必填，Round ≥ 2 追加优化建议） | 所有已有区块（只读） |
| 市场专家 | 市场评估报告、封面高光文案、市场深度分析（Round ≥ 2 可选） | 所有已有区块（只读） |
| 评分专家 | 数据、评分进化史、需要修改的具体问题清单 | 所有已有区块（只读） |

### 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 1 | `docs/album-overview.md` | 曲目定位表 + 叙事轴 + 调性主线 |

### 输出文件（每首歌一个）

`songs/T{N}-{曲名}.md`

### 文件结构（严格）

每首歌曲文件必须包含以下区块，**按固定顺序**：

```markdown
# T{N}《{曲名}》

**{叙事轴名} · 专辑第{N}首**

---

## 基本信息

| 项目 | 内容 |
|------|------|
| 语言 | {中文 / 中文+英文 / 英文} |
| 方向 | {叙事轴}（{轴含义简述}） |
| 核心Hook | {≤ 8 字} |
| 核心悖论 | {1 句话} |
| 核心意象 | {3-5 个，用 / 分隔} |
| 身体感 | {≥ 2 个身体意象} |
| 情绪弧线 | {起点→终点} |
| 估计时长 | ~{M}:{SS} |
| 编曲风格 | {风格}，{调性}，{BPM} BPM |

---

## 歌词（Round{N} · {状态描述}）

{可选：优化切入说明}

```
[结构标签]
歌词行...

[结构标签]
歌词行...
```

{可选：韵脚优化对照表}

---

## 英文歌词（English Lyrics）（Round{N} · {状态描述}）

> 仅双语/英文专辑时填写，纯中文专辑删除此区块。

```
[Structure Tag]
Lyrics...

[Structure Tag]
Lyrics...
```

{可选：English rhyme analysis}

---

## 完整编曲设计

> **BPM: {N} BPM · {调性} · {风格}**

### 1. {段落名}设计（{起始时间}-{结束时间}）

{详细编曲描述，含音色/乐器/人声处理/情绪}

### 2. {段落名}设计（{起始时间}-{结束时间}）
...

---

## 关键 Sound Design

| 音效 | 描述 | 出现位置 | 音量 |
|------|------|---------|------|
| {名称} | {描述} | {位置} | {dB} |
| ... | | | |

---

## 韵脚分析（Round{N}）

### 韵部分布

| 韵部 | 音 | 出现位置 | 情绪质感 |
|------|---|---------|---------|
| {韵名} | {音} | {位置} | {描述} |

### Hook 韵脚设计逻辑
{说明}

### 韵脚×编曲配合评分

| 维度 | 评分 | 说明 |
|------|------|------|
| {维度} | {X}/10 | {说明} |

---

## 封面高光文案

> **"{一句话文案}"**
> {补充说明}

---

## 市场评估报告

### 核心竞争力
- {卖点 1}
- {卖点 2}
- ...

### 目标受众分析

| 受众层 | 特征 | 接受度评估 |
|--------|------|-----------|
| {层名} | {描述} | {星级} |
| ... | | |

{可选：推广建议、商业化潜力、风险评估}

---

## 需要修改的具体问题清单（Round{N}）

| # | 优先级 | 模块 | 问题描述 | 修改方案 |
|---|--------|------|---------|---------|
| {N} | 🔴/🟡/🟢 | {模块} | {描述} | {方案} |
| ... | | | | |

---

## 数据

- **评分**：{总分}/100（Round{N} {版本描述}）
- **韵律**：{0-20}/20
- **市场**：{0-20}/20
- **结构**：{0-20}/20
- **哲学**：{0-20}/20
- **编排**：{0-20}/20
- **状态**：{✅ 定稿 / 🔄 优化中}

---

## 评分进化史

| 阶段 | 分数 | 主要改动 |
|------|------|---------|
| Round{N-1} | {总分} | {改动描述} |
| Round{N}（本次） | {总分} | {改动描述} |
```

### 必填区块校验

| 区块 | 必填 | 校验规则 |
|------|------|---------|
| 基本信息表 | ✅ | 9 个字段（含语言），全部非空。纯音乐曲目「语言」=「纯音乐」 |
| 编曲风格 | ✅ | 必填，非空，格式如「{风格}，{调性}，{BPM} BPM」 |
| 歌词区块 | ✅ 常规歌曲 / ❌ 纯音乐 | 常规歌曲：含 ≥3 个结构标签，纯歌词字符 ≤ 3500（不含标签文字），且歌词用 Markdown 代码块包裹。纯音乐：此区块替换为「器乐描述」区块 |
| 英文歌词区块 | 双语/英文专辑必填 | 含 ≥3 个结构标签，纯歌词字符 ≤ 3500（不含标签文字），且歌词用 Markdown 代码块包裹 |
| 器乐描述区块 | ❌ 常规歌曲 / ✅ 纯音乐 | 纯音乐专用：主旋律情绪弧线 + 段落意图 + 核心音色 + 关键转折 |
| 完整编曲设计 | ✅ | ≥5 个段落，每段有明确时间范围 |
| 关键 Sound Design | ✅ | ≥3 个音效，含位置和音量 |
| 封面高光文案 | ✅ | 1 句话文案 + 补充说明 |
| 韵脚分析 / 节奏音色分析 | 常规歌曲 Round 1 必填，Round ≥ 2 追加 / 纯音乐必填「节奏/音色分析」 | 含韵部分布表 + Hook 韵脚检查 + 韵脚×编曲配合评分，或纯音乐的节奏型/音色层次分析 |
| 市场评估报告 | ✅ | 核心竞争力 + 受众分析 |
| 需要修改的具体问题清单 | Round ≥ 2 必填 | 有具体问题则逐项列出，无问题则写 `无` |
| 数据 | ✅ | 总分 + 5 维度 + 状态。纯音乐「韵律」维度替换为「器乐表现力」 |
| 评分进化史 | Round ≥ 2 必填 | ≥1 行历史记录 |

### 歌词区块格式约束

✅ 正确：

```
[Verse]
我把笼子 走成天空
把每条退路 走成出路

[Pre Chorus]
一步一步 把身体寄回现场

[Hook]
走成天空 走成天空
```

❌ 错误（结构标签内含描述）：

```
[Verse — 清唱进入]  ← 标签内不得有描述
我把笼子 走成天空
```

### 编曲设计区块格式约束

每个段落必须包含：
- 段落编号 + 名称：`### N. {段落名}设计（{start}-{end}）`
- 时间范围：精确到秒，如 `0:00-0:30`
- 至少 3 个时间锚点（如 `0:05`、`0:15`、`0:22`）
- 每个时间锚点有对应的编曲动作描述

### 音韵 × 编曲配合（韵脚分析，Round 1 必填，Round ≥ 2 追加优化建议）

```markdown
## 韵脚分析

### 韵部分布

| 韵部 | 音 | 出现位置 | 情绪质感 |
|------|---|---------|---------|
| {韵名} | {音} | {位置} | {描述} |

### Hook 韵脚设计逻辑
{说明}

### 韵脚×编曲配合评分

| 维度 | 评分 | 说明 |
|------|------|------|
| {维度} | {X}/10 | {说明} |
```

### 市场深度分析（Round ≥ 2 可选增强区块）

```markdown
## 市场深度分析

{竞品对标/差异化分析/平台适配/Sync 潜力/营销建议/风险评估}

### 市场潜力评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 概念独特性 | {X}/10 | {说明} |
| Hook传播力 | {X}/10 | {说明} |
| ... | | |
| 综合市场潜力 | {X.X}/10 | {说明} |
```

### Phase 2 产物验证（每首歌）

完成后必须确认：
- [ ] `songs/T{N}-{曲名}.md` 存在且非空
- [ ] 基本信息表 9 个字段（含语言）全部有值
- [ ] 歌词含 ≥3 个结构标签，纯歌词字符 ≤ 3500（不含标签文字），且歌词用 Markdown 代码块包裹
- [ ] 编曲设计 ≥5 个段落，每段含 ≥3 个时间锚点，时间轴无重叠/断裂
- [ ] Sound Design ≥3 个音效
- [ ] 封面高光文案存在
- [ ] 市场评估含核心竞争力 + 受众分析
- [ ] 评分总分 + 5 维度分都在
- [ ] Round ≥ 2 时：问题清单 + 评分进化史都在

### Phase 2 通过条件（全局）

所有歌曲通过时确认：
- [ ] 所有 `songs/T{N}-*.md` 存在
- [ ] 每首评分 ≥ 80 分且跑满 3 轮（或达最大轮次 6 轮）
- [ ] `docs/album-overview.md` 中评分总览已更新

### Phase 2 可选区块清单

| 区块 | 插入位置 | 触发条件 | 写入专家 |
|------|---------|---------|----------|
| 韵脚分析 | 插入于「关键 Sound Design」之后、「封面高光文案」之前 | Round 1 必填（新增），Round ≥ 2 追加优化建议（修改/追加） | 韵脚专家（Round 1 新增，Round ≥ 2 修改/追加） |
| 市场深度分析 | 插入于「市场评估报告」之后、「问题清单」之前 | Round ≥ 2 可选 | 市场专家 |

---

## Phase 3 契约

### ⚠️ 修改范围
- **读取**：`docs/album-overview.md`（语言字段）、`songs/T{N}-曲名.md` 中的歌词区块
- **写入**：`generate/lyrics/cn/` 和/或 `generate/lyrics/en/` 下的新文件
- **禁止**：修改 `songs/` 目录中的任何源文件

### 输入
- `docs/album-overview.md`（**语言**字段：中文 / 中文+英文 / 英文 / 纯音乐）
- `songs/T{N}-曲名.md`（歌词区块，纯音乐曲目无此输入）

### 语言判断

| 语言 | 提取中文 | 提取英文 |
|------|---------|---------|
| 中文 | ✅ → `cn/` | — |
| 中文+英文 | ✅ → `cn/` | ✅ → `en/` |
| 英文 | — | ✅ → `en/` |
| 纯音乐 | — | — |

### 输出文件
```
generate/lyrics/cn/T{N}-曲名.txt              ← 中文标准歌词（中文/中文+英文专辑必填）
generate/lyrics/en/T{N}-曲名.txt              ← 英文标准歌词（英文/中文+英文专辑必填）
generate/lyrics/metadata.json                 ← 歌词元数据（含 language 字段）
generate/lyrics/validation.txt                ← 验证结果汇总
```

### 元数据格式（metadata.json）

```json
{
  "songs": [
    {
      "track": "T1-出发",
      "cn": {
        "file": "generate/lyrics/cn/T1-出发.txt",
        "char_count": 1234,
        "structure_tags": ["Intro", "Verse", "Hook", "Bridge", "Outro"],
        "section_count": 5,
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

### 验证
- [ ] 所有曲目歌词文件已生成（根据语言决定 cn/ 和/或 en/）
- [ ] 所有文件字符数 ≤ 3500
- [ ] 结构标签合法且内无描述
- [ ] `metadata.json` 已生成且每首歌数据完整
- [ ] `validation.txt` 全 ✅

### 歌词格式约束
- 伴唱/和声使用圆括号包裹，如 `(Ooh)`、`(Harmonize)`
- 结构标签内不得有任何描述文字

### 纯音乐曲目 metadata.json 示例

纯音乐曲目在 `metadata.json` 中标记如下（不生成 `cn/` 或 `en/` 下的 .txt 文件）：

```json
{
  "track": "T3-间奏",
  "has_lyrics": false,
  "language": "纯音乐"
}
```

---

## Phase 4 契约

### ⚠️ 修改范围
- **读取**：`generate/lyrics/cn/*.txt` + `en/*.txt` 和 `songs/T{N}-*.md` 编曲设计
- **写入**：`generate/cn/` 和 `generate/en/` 下的新 .mp3 文件、`generate/prompts/` 下的 Prompt 文件
- **禁止**：修改歌词文件或歌曲设计文件

### 输入
- `generate/lyrics/cn/*.txt`（中文/中文+英文专辑）和/或 `generate/lyrics/en/*.txt`（英文/中文+英文专辑）
- `songs/T{N}-*.md`（编曲设计用于生成 Prompt）

### 输出文件
```
generate/prompts/TN-曲名-prompt1.txt     ← Prompt 版本 1（编曲忠实还原型）
generate/prompts/TN-曲名-prompt2.txt     ← Prompt 版本 2（情绪叙事驱动型）
generate/prompts/TN-曲名-prompt3.txt     ← Prompt 版本 3（听感质感优先型）
generate/prompts/index.json              ← Prompt 索引（含 char_count）
generate/cn/TN-曲名-p1.mp3
generate/cn/TN-曲名-p2.mp3
generate/cn/TN-曲名-p3.mp3
generate/en/TN-曲名-p1.mp3
generate/en/TN-曲名-p2.mp3
generate/en/TN-曲名-p3.mp3
```

### Prompt 策略

每首歌从完整编曲设计生成 **3 个不同凝练方式的 Prompt 版本**，每个版本压满 2000 字符上限。

| 版本 | 凝练策略 | 组织方式 |
|------|---------|---------|
| 1 | 编曲忠实还原型 | 按编曲段落时间线顺序 |
| 2 | 情绪叙事驱动型 | 按情绪弧线和叙事线索 |
| 3 | 听感质感优先型 | 从最终听感出发，质感关键词驱动 |

### Prompt 审查

独立的 Prompt 审查 Agent 对所有 Prompt 进行 6 项检查：
1. 字符数 ≤ 2000 且 ≥ 1500
2. 包含所有核心参数
3. 无无效信息（时间戳/ dB 值/表格）
4. 编曲信息传递 ≥ 60%
5. MiniMax 音乐模型可读
6. 三版本差异化明显

### 格式要求
- CLI 参数：--model music-2.6
- Prompt ≤ 2000 字符（每个版本压满上限）
- 歌词 ≤ 3500 字符
- 每首 × 每语言 × 每 Prompt 版本 = 独立生成任务

### 验证
- [ ] 每首歌 3 个 Prompt 版本均已生成
- [ ] Prompt 审查优化通过（6 项全 ✅）
- [ ] 所有产物文件存在且非空（≥ 100KB）
- [ ] 产物目录结构正确（cn/ + en/ 下按 p1/p2/p3 命名）
- [ ] `generate/prompts/index.json` 已生成

---

## Phase 5 契约

### ⚠️ 修改范围
- **读取**：`generate/cn/*.mp3` + `en/*.mp3`（全部 Take 版本）
- **写入**：`generate/cn_320k/` 和 `generate/en_320k/` 下的新 .mp3 文件
- **禁止**：修改原始生成文件或删除任何 .mp3

### 输入
- `generate/cn/*.mp3` + `en/*.mp3`（3 个 Prompt 版本 × 每语言）
- 用户选定表

### 输出文件
```
generate/cn_320k/TN-曲名-pX.mp3
generate/en_320k/TN-曲名-pX.mp3
generate/loudness-report.txt       ← 响度/时长报告
```

### 格式要求
- 转码参数：320kbps, 44.1kHz, MP3
- 响度归一化：-14 LUFS ± 0.5 LUFS（网易云标准）
- ffprobe 验证：bit_rate=320000, sample_rate=44100
- 时长验证：≥ 1:00 且 ≤ 6:00

### 验证
- [ ] 每首选定一个 Prompt 版本（p1/p2/p3），无遗漏
- [ ] bit_rate=320000, sample_rate=44100
- [ ] 响度 -14 LUFS ± 0.5 LUFS
- [ ] 时长 ≥ 1:00 且 ≤ 6:00
- [ ] `cn_320k/` 文件数 = 曲目数（中文/中文+英文专辑）
- [ ] `en_320k/` 文件数 = 曲目数（英文/中文+英文专辑；纯中文/纯音乐专辑此项跳过）
- [ ] `loudness-report.txt` 全 ✅

---

## Phase 6 契约

### ⚠️ 修改范围
- **读取**：`docs/album-overview.md`（Phase 1 的 4 维度评分总览）、`songs/T{N}-*.md`（Phase 2 的 5 维度评分）、`generate/cn_320k/` + `en_320k/`、`assets/`
- **写入**：`docs/` 下的新文档文件 + 压缩包
- **禁止**：修改 `songs/` 或 `generate/` 目录中的任何文件

**评分总览转换规则：**
Phase 1 使用 4 维度（概念原创性/叙事连贯性/市场潜力/音乐一致性，各 25 分），Phase 2 使用 5 维度（韵律/市场/结构/哲学/编排，各 20 分）。

Phase 6 更新 `docs/album-overview.md` 的评分总览时，应将 Phase 1 的 4 维度格式替换为 Phase 2 的 5 维度格式，并将 Phase 1 原始评分保留为历史参考（如 `## Phase 1 概念评分` 子区块）。

### 输入
- `docs/album-overview.md`
- `songs/T{N}-*.md`（封面高光文案、市场评估）
- `generate/cn_320k/` + `en_320k/`
- `assets/` 封面概念图

### 输出文件
| 文件 | 内容 |
|------|------|
| `docs/album-overview.md` | 专辑统筹文档（完整更新） |
| `docs/promotional-materials.md` | 宣传文档（从模板填充） |
| `docs/artist-story-cn.md` | 艺人说中文长版（~1800 字） |
| `docs/artist-story-en.md` | 艺人说英文长版（~1400 词） |
| `docs/artist-story-short.md` | 艺人说中英文短版（各 ~400 字/词） |
| `docs/artist-story-quotes.md` | 金句提取（5 条中英对照） |
| `docs/cover-concept.md` | 封面概念（≥3 方向 + HEX 配色 + 图片生成结构化描述） |
| `docs/platform-check.txt` | 平台适配检查结果 |
| `*.zip` | `<project-root>/<专辑名>-宣传物料.zip` |

### Phase 6.4.5 契约 — Cover Prompt Generator

#### 输入
| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 6.4 | `docs/cover-concept.md` | 封面概念方案 |
| Phase 1 | `docs/album-overview.md` | 核心概念/叙事轴 |
| Phase 2 | `songs/T{N}-曲名.md` | 每首歌核心意象 |

#### 输出文件
```
generate/covers/prompts/album-cover-prompt1.txt     ← 专辑封面 版本1：概念忠实型
generate/covers/prompts/album-cover-prompt2.txt     ← 专辑封面 版本2：情绪氛围型
generate/covers/prompts/album-cover-prompt3.txt     ← 专辑封面 版本3：极简符号型
generate/covers/prompts/T{N}-曲名-cover-prompt1.txt ← 单曲封面 版本1
generate/covers/prompts/T{N}-曲名-cover-prompt2.txt ← 单曲封面 版本2
generate/covers/prompts/T{N}-曲名-cover-prompt3.txt ← 单曲封面 版本3
generate/covers/prompts/index.json                  ← Prompt 索引
```

#### Prompt 策略

| 版本 | 策略 | 组织方式 | 字符上限 |
|------|------|---------|----------|
| 1 | 概念忠实型 | 直接映射封面概念方案 | ≤ 1000 |
| 2 | 情绪氛围型 | 从情绪弧线和身体感出发 | ≤ 1000 |
| 3 | 极简符号型 | 核心悖论 → 视觉符号 | ≤ 1000 |

#### 验证
- [ ] 专辑封面 3 个 Prompt 已生成
- [ ] 每首歌 3 个单曲封面 Prompt 已生成
- [ ] 每个 Prompt ≤ 1000 字符
- [ ] index.json 已生成

### Phase 6.4.6 契约 — Cover Executor

#### 输入
| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 6.4.5 | `generate/covers/prompts/*.txt` | 封面 Prompt 文件 |
| Phase 6.4.5 | `generate/covers/prompts/index.json` | Prompt 索引 |

#### 输出文件
```
generate/covers/album-cover-p1.png              ← 专辑封面 版本1
generate/covers/album-cover-p2.png              ← 专辑封面 版本2
generate/covers/album-cover-p3.png              ← 专辑封面 版本3
generate/covers/tracks/T{N}-曲名-p1.png          ← 单曲封面 版本1
generate/covers/tracks/T{N}-曲名-p2.png          ← 单曲封面 版本2
generate/covers/tracks/T{N}-曲名-p3.png          ← 单曲封面 版本3
```

#### 格式要求
- CLI 工具：`mmx image generate`
- 分辨率：2048×2048px（正方形）
- 格式：PNG

#### 验证
- [ ] 专辑封面 3 张已生成（≥ 50KB）
- [ ] 单曲封面全部已生成（N首 × 3张）
- [ ] 产物目录结构正确

### Phase 6.7 契约 — Promo Video Executor

#### 输入
| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 6 | `docs/album-overview.md` | 核心概念/曲目单 |
| Phase 6 | `docs/promotional-materials.md` | 宣传文档 |
| Phase 6 | `docs/cover-concept.md` | 封面概念 |
| Phase 6.4.6 | `generate/covers/album-cover-p1.png` | 最佳专辑封面（首帧参考） |

#### 输出文件
```
docs/promo-video.mp4           ← 宣传视频完整版（25-30秒）
docs/promo-video-15s.mp4       ← 宣传视频精简版（15秒）
```

#### 格式要求
- CLI 工具：`mmx video generate`
- 模型：MiniMax-Hailuo-2.3
- 画面比例：默认 16:9
- 首帧参考：可选（推荐用 album-cover-p1.png）

#### 验证
- [ ] 完整版视频已生成（≥ 1MB）
- [ ] 精简版视频已生成（≥ 1MB）
- [ ] 视频时长符合规格（完整版 20-30s，精简版 12-18s）

### 平台适配检查

| 检查项 | 网易云 | QQ 音乐 |
|--------|--------|--------|
| 格式 | MP3 320kbps | FLAC/MP3 320kbps |
| 采样率 | 44.1kHz | 44.1kHz |
| 响度 | -14 LUFS | -14 LUFS |
| 最短时长 | ≥ 60 秒 | ≥ 60 秒 |
| 最长时长 | ≤ 6 分钟 | ≤ 6 分钟 |
| 最低曲目数 | 3 首 | 3 首 |
| 必填信息 | 专辑名/曲目/艺人 | 专辑名/曲目/艺人 |

### 验证
- [ ] 所有文件存在且非空
- [ ] 制作信息标注准确（AI 生成工具/规模/标准）
- [ ] 曲目单与 Phase 5 最终文件一致
- [ ] `platform-check.txt` 网易云/QQ 音乐全 ✅

---

## Phase 间文件依赖关系

```
Phase 1 输出 → Phase 2 输入
  docs/album-overview.md  ──曲目定位表──→  每首歌的基本信息表
  docs/album-overview.md  ──叙事轴/调性──→ 编曲设计的调性/BPM/风格

Phase 2 输出 → Phase 3 输入
  songs/T{N}-*.md  ──歌词区块──→  generate/lyrics/cn/T{N}-曲名.txt
  songs/T{N}-*.md  ──英文版──→  generate/lyrics/en/T{N}-曲名.txt（如有）

Phase 3 输出 → Phase 4 输入
  generate/lyrics/cn/*.txt  ──歌词──→  MiniMax CLI --lyrics-file
  generate/lyrics/en/*.txt  ──歌词──→  MiniMax CLI --lyrics-file
  songs/T{N}-*.md  ──编曲设计──→  3 版本 Prompt 生成

Phase 4 输出 → Phase 5 输入
  generate/cn/*.mp3  ──听评──→  选定 Prompt 版本（p1/p2/p3）
  generate/en/*.mp3  ──听评──→  选定 Prompt 版本（p1/p2/p3）

Phase 5 输出 → Phase 6 输入
  generate/cn_320k/*.mp3  ──最终音频──→  上传平台
  generate/en_320k/*.mp3  ──最终音频──→  上传平台
  songs/T{N}-*.md  ──高光文案──→  promotional-materials.md
  docs/album-overview.md  ──统筹信息──→  album-packager

Phase 6 内部依赖
  docs/cover-concept.md  ──结构化描述──→  phase6-cover-prompt-generator
  generate/covers/prompts/*.txt  ──Prompt──→  phase6-cover-executor → 封面图 PNG
  generate/covers/album-cover-p1.png  ──首帧参考──→  phase6-promo-video-executor
  docs/promotional-materials.md  ──视频脚本──→  phase6-promo-video-executor → 宣传视频 MP4
  全部产物（封面图+视频+文档）──→  phase6-packager → zip 压缩包
```
