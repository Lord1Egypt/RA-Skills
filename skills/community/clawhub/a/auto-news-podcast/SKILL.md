---
name: auto-news-podcast
description: >
  **Auto News Podcast** 是一款智能新闻播客生成工具，能够根据用户输入的关键词自动完成从新闻搜索到音频生成的完整流程。

  **Auto News Podcast** is an intelligent news podcast generation tool that automatically completes the entire workflow from news search to audio generation based on user-provided keywords.

  Use when user asks to: 生成新闻播客、搜索新闻并生成音频、自动新闻播报、新闻摘要+语音播报、
  news podcast, auto news briefing, generate news audio, 每日新闻早报, 新闻晚报, 批量生成新闻播报.
  支持英文输入：Generate news broadcasts [keyword, style is..., format is..., voice is...]
  支持自定义输出目录、音色描述、播报风格、播报形式，自动完成搜索→去重→摘要→风格化文案→配图→播报全流程。
---

# Auto News Podcast 智能新闻播客生成器

## 简介 | Introduction

**Auto News Podcast** 是一款智能新闻播客生成工具，能够根据用户输入的关键词自动完成从新闻搜索到音频生成的完整流程。

**Auto News Podcast** is an intelligent news podcast generation tool that automatically completes the entire workflow from news search to audio generation based on user-provided keywords.

---

## 核心功能 | Core Features

### 1. 多源新闻搜索 | Multi-Source News Search
- **智能搜索降级**: Tavily Search → Baidu Search → Tavily API Retry → News Aggregator
- **智能标签**: 自动为新闻打上分类标签（科技/财经/政治/国际等）

- **Intelligent Search Fallback**: Tavily Search → Baidu Search → Tavily API Retry → News Aggregator
- **Smart Tagging**: Auto-tag news categories (Tech/Finance/Politics/International, etc.)

### 2. 三级摘要生成 | Three-Level Summary Generation
- **20秒速报**: 60字以内，适合快速口播
- **60秒解读**: 300字以内，完整通顺

- **20-Second Brief**: Under 60 characters, suitable for quick broadcasting
- **60-Second Analysis**: Under 300 characters, complete and coherent

### 3. 风格化播报文案 | Styled Broadcast Script
- **4种预设风格**: 正式新闻腔 / 轻松早报腔 / 财经严肃腔 / 科技快评腔
- **智能风格匹配**: 根据关键词自动匹配最适合的播报风格
- **口语化改写**: 自动将书面语转换为适合朗读的口语表达

- **4 Preset Styles**: Formal News / Morning Brief / Finance Serious / Tech Commentary
- **Smart Style Matching**: Automatically match the best style based on keywords
- **Colloquial Rewrite**: Convert written language to spoken language suitable for broadcasting

### 4. 双人对话播报 | Dual-Host Dialogue Broadcasting
  除了传统的单人播报之外，还可以为用户生成双人对话式播报，使新闻内容的展示更加的生动活泼

- **角色设定**: 主播（引导话题）+ 评论员（深度解读）
- **交替音色**: 支持为两个角色分别配置不同音色
- **自然对话**: 生成真实感对话，包含追问、总结等互动环节

- **Role Settings**: Host (topic guide) + Commentator (in-depth analysis)
- **Alternating Voices**: Configure different voices for each role
- **Natural Dialogue**: Generate realistic conversations with follow-ups and summaries

### 5. AI语音合成 | AI Voice Synthesis
- **多音色选择**: 5种音色（年轻女生/沉稳男声/温柔女生/专业主播等）
- **智能降级**: CellCog → edge-tts → System TTS
- **双人音频拼接**: 自动按对话顺序拼接音频片段

- **Multiple Voice Options**: 5 voices (Young Female / Mature Male / Gentle Female / Professional Anchor, etc.)
- **Smart Fallback**: CellCog → edge-tts → System TTS
- **Dual Audio Splicing**: Automatically splice audio clips in dialogue order

### 6. 批量生成模式 | Batch Generation Mode
- **批量配置**: 一次性输入多条新闻配置，逐条生成
- **配置清单**: 自动生成配置表格，清晰展示每条播报的设置
- **结果汇总**: 生成完整的执行报告，包含成功/失败状态

- **Batch Configuration**: Input multiple news configurations at once, generate sequentially
- **Configuration List**: Auto-generate configuration table showing each broadcast setting
- **Result Summary**: Generate complete execution report with success/failure status

### 7. 事件深度解读 | Event Deep Analysis
- **5维分析**: 事件核心 / 背景前因 / 多维影响 / 利益博弈 / 趋势判断
- **独立音频**: 生成专门的深度解读播报音频
- **专业风格**: 默认采用正式新闻腔，适合深度内容，也可以自定义深度解读音色

- **5-Dimension Analysis**: Core Event / Background / Multi-dimensional Impact / Interest Game / Trend Judgment
- **Independent Audio**: Generate dedicated deep analysis broadcast audio
- **Professional Style**: Formal news tone, suitable for in-depth content

---

## 技术亮点 | Technical Highlights

### 零配置搜索 | Zero-Configuration Search
无需手动配置搜索源，系统自动选择最优搜索策略，支持国内外网络环境。

No manual search source configuration needed. The system automatically selects the optimal search strategy, supporting both domestic and international network environments.

### 智能容错 | Intelligent Fault Tolerance
搜索失败自动降级，音频生成失败自动切换备选方案，确保任务完成率。

Automatic fallback on search failure, automatic switch to backup options on audio generation failure, ensuring task completion rate.

### 多模型支持 | Multi-Model Support
自动识别 OpenClaw 配置的模型（Kimi/Qwen/Ollama等），动态调用API生成文案。

Automatically recognizes OpenClaw configured models (Kimi/Qwen/Ollama, etc.), dynamically calls API to generate scripts.

---

## 使用方式 | Usage

### 方式一：交互模式 | Method 1: Interactive Mode
输入 生成“某某关键词”的新闻播报 【注：关键词可以是具体的内容，比如 “国际原油价格暴涨”，也可以是宽泛的领域信息，比如 “科技领域”】
然后按提示逐步输入：风格、形式、音色、是否需要深度解读，深度等配置。
Follow prompts to input: keyword, style, format, voice, etc.

示例如下：
"生成国际原油价格暴涨的新闻播报"

For example:
"Generate news broadcasts about Apple earnings report"

Note: English input is not supported in interactive mode. If you only input the key search word, the default style, format, voice will be 
used for generating the news broadcast.
If you do not want to use the default configurations, please use Method 2 to generate news broadcast.

```

### 方式二：完整配置一次性输入 | Method 2: Input the complete configuration at one time
如果用户一次性提供了完整的配置信息（包含所有必要参数），则可以跳过交互环节直接执行，完整信息必须用【】或[]包裹。

示例如下：
    - 示例1: 生成新闻播报【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
    - 示例2: 生成新闻播报【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，不需要深度解读】
    - 示例3: 生成新闻播报【华为Mate80发布，风格是科技快评腔，形式是单人口播，用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
    - 示例4: 生成新闻播报【华为Mate80发布，风格是科技快评腔，形式是单人口播，用温柔女生音色，不需要深度解读】
    - 示例5: 生成新闻播报【华为Mate80发布，使用默认配置】
    - 示例6: 生成新闻播报【华为Mate80发布，风格是科技快评腔，其他用默认配置】

For example:
    - Example 1: Generate news broadcasts [Huawei Mate80 release, style is tech commentary, format is dual dialogue, host voice is mature male, commentator voice is gentle female, need deep analysis, deep analysis voice is professional anchor]
    - Example 2: Generate news broadcasts [Apple earnings report, style is formal news, format is single broadcast, voice is young female, no deep analysis]
    - Example 3: Generate news broadcasts [Tesla new model, use default config]
    - Example 4: Generate news broadcasts [Bitcoin market update, style is finance serious, other use default]

    # 风格映射（英文 -> 标准中文）
    style_map_en = {
        'formal news': '正式新闻腔',
        'formal': '正式新闻腔',
        'morning brief': '轻松早报腔',
        'casual morning': '轻松早报腔',
        'finance serious': '财经严肃腔',
        'financial serious': '财经严肃腔',
        'finance': '财经严肃腔',
        'tech commentary': '科技快评腔',
        'technology commentary': '科技快评腔',
        'tech': '科技快评腔',
        'technology': '科技快评腔',
    }
    
    # 形式映射（英文 -> 标准中文）
    format_map_en = {
        'single broadcast': '单人口播',
        'single': '单人口播',
        'solo': '单人口播',
        'dual dialogue': '双人对话式播报',
        'dual': '双人对话式播报',
        'dialogue': '双人对话式播报',
        'double': '双人对话式播报',
        'two person': '双人对话式播报',
        'two host': '双人对话式播报',
    }
    
    # 音色映射（英文关键词 -> 标准中文）
    voice_map_en = {
        'young female': '年轻活力的女生',
        'young woman': '年轻活力的女生',
        'young girl': '年轻活力的女生',
        'energetic female': '年轻活力的女生',
        'mature male': '沉稳的中年男性',
        'mature man': '沉稳的中年男性',
        'middle aged male': '沉稳的中年男性',
        'middle aged man': '沉稳的中年男性',
        'calm male': '沉稳的中年男性',
        'gentle female': '温柔的女生',
        'gentle woman': '温柔的女生',
        'soft female': '温柔的女生',
        'soft voice': '温柔的女生',
        'professional anchor': '专业新闻主播',
        'professional broadcaster': '专业新闻主播',
        'news anchor': '专业新闻主播',
        'anchor': '专业新闻主播',
        'emotional': '情感丰富的声音',
        'dramatic': '情感丰富的声音',
        'lively': '情感丰富的声音',
    }

```

### 方式三：批量生成 | Method 3: Batch Generation
如果需要一次性批量生成新闻播报，可以使用批量生成命令，输入一个新闻播报列表

示例如下：
"生成批量新闻播报
【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读】
【宝马X5最新信息，风格是科技快评腔，形式是单人口播，用温柔女生音色，需要深度解读】
【奔驰S级最新信息，风格是正式新闻，其他用默认值】"

For example:
"Generate batch news broadcasts
[Apple earnings report, style is formal news, format is single broadcast, voice is young female, no deep analysis]
[Huawei Mate80 release, style is tech commentary, format is dual dialogue, host voice is mature male, commentator voice is gentle female, need deep analysis, deep analysis voice is professional anchor]
[Tesla new model, use default config]"

```

---

## 配置格式 | Configuration Format

### 完整配置 | Full Configuration
```
【关键词，风格是XXX，形式是XXX，主播用XXX音色，评论员用XXX音色，需要深度解读，深度解读音色是XXX】
```

### 简写配置 | Short Configuration
```
【关键词，风格是XXX，形式是XXX，用XXX音色】
```

### 默认配置 | Default Configuration
```
【关键词，使用默认配置】
【关键词，风格是XXX，其他用默认配置】
```

---

## 输出文件 | Output Files

```
单个新闻播报会生成到下面位置：
Single news broadcast will be generated to the following path:

workspace/news/{YYYYMMDD_HHMMSS}_{关键词}/
├── 新闻摘要_{关键词}_{日期}.md    # 完整新闻摘要（含三级摘要）
├── 播报文案_{关键词}_{日期}.txt    # 纯文本播报稿
├── titleAndLabels.txt              # 新闻标题和标签
├── cover.jpg                       # 封面图片
├── 播报.mp3 / 播报_对话版.mp3       # 播报音频
├── 深度解读文案.txt                 # 深度解读文章（可选）
└── 事件深度解读.mp3                 # 深度解读音频（可选）

├── NewsSummary_{Keyword}_{Date}.md    # Complete news summary (including three-level abstracts)
├── BroadcastScript_{Keyword}_{Date}.txt    # Plain text broadcast script
├── titleAndLabels.txt              # News titles and tags
├── cover.jpg                       # Cover image
├── Broadcast.mp3 / Broadcast_Dialogue.mp3       # Broadcast audio (Podcast)
├── InDepthAnalysis.txt                 # In-depth interpretation article (optional)
└── InDepthAnalysis.mp3                 # In-depth interpretation audio (optional)


批量新闻播报会生成到下面位置：
Batch news broadcasts will be generated to the following path:

workspace/news/batch_{YYYYMMDD_HHMMSS}/
├── news1 folder    
├── news2 folder    
├── news3 folder            
├── ...                       
├── 配置清单.md                   # config list
└── 生成结果汇总.md               # result report

```

---

# Auto News Podcast

根据用户输入的关键词/领域，自动完成：**多源搜索 → 去重清洗 → 三级摘要 → 风格化播报文案 → 搜索配图 → 生成播报音频**。

---

## ⛔ 执行纪律（必须遵守，不可跳过）

**本技能的 Step 1 是强制交互环节，AI 不得自行替用户做决定。**

### 例外情况：完整配置一次性输入

如果用户**一次性提供了完整的配置信息**（包含所有必要参数），则可以**跳过交互环节直接执行**。

#### 支持的一次性格式（用【】或[]包裹）

```
【搜索关键词信息，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
```

**完整配置示例：**

| 示例 | 说明 |
|------|------|
| 【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】 | 完整双人对话配置 |
| 【华为Mate80发布，风格是科技快评腔，形式是单人口播，用温柔女生音色，不需要深度解读】 | 完整单人口播配置 |
| 【华为Mate80发布，使用默认配置】 | 除关键词外全部使用默认值 |
| 【华为Mate80发布，风格是科技快评腔，其他用默认配置】 | 部分指定+部分默认 |

**配置解析规则：**
1. ✅ **搜索关键词信息必须要有** — 位于【】内的第一个逗号前内容
2. ✅ **如果包含"使用默认配置"** — 除关键词外，其他全部使用默认值
3. ✅ **如果包含"其他用默认配置"** — 未指定的配置项使用默认值
4. ❌ **如果未使用默认配置模式** — 所有配置项必须齐全，否则仍需交互确认

#### 检测到完整配置后的流程

```
用户：【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读】
AI：[OK] 检测到完整配置，直接开始执行...
    Step 2: 搜索新闻...
    Step 3: 生成摘要...
    ...
```

---

## 🌐 英文输入支持（新增）

系统现在支持全英文输入，自动检测语言并生成英文播报内容。

### 英文配置格式

使用方括号 `[]` 包裹英文配置：

```
[Keyword, style is ..., format is ..., voice is ...]
```

### 英文配置示例

| 英文示例 | 说明 |
|----------|------|
| [Apple earnings report, style is formal news, format is single broadcast, voice is young female, no deep analysis] | 单人口播，正式新闻风格 |
| [Huawei Mate80 release, style is tech commentary, format is dual dialogue, host voice is mature male, commentator voice is gentle female, need deep analysis] | 双人对话，科技快评风格 |
| [Tesla new model, use default config] | 使用默认配置 |

### 英文配置映射

| 英文配置项 | 对应中文 |
|-----------|---------|
| **Style** | |
| formal news | 正式新闻腔 |
| morning brief | 轻松早报腔 |
| finance serious | 财经严肃腔 |
| tech commentary | 科技快评腔 |
| **Format** | |
| single broadcast | 单人口播 |
| dual dialogue | 双人对话式播报 |
| **Voice** | |
| young female | 年轻活力的女生 |
| mature male | 沉稳的中年男性 |
| gentle female | 温柔的女生 |
| professional anchor | 专业新闻主播 |
| emotional | 情感丰富的声音 |

### 英文批量生成

```
[Apple earnings report, style is formal news, format is single broadcast, voice is young female, no deep analysis]
[Tesla new model, style is tech commentary, format is dual dialogue, host voice is mature male, commentator voice is gentle female, need deep analysis]
```

---

## 🚀 批量生成模式（新增）

支持一次性输入多条新闻播报配置，系统将按顺序逐条生成。

### 批量配置格式

每条配置用【】包裹，多条配置连续输入：

```
【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
【宝马X5最新信息，风格是科技快评腔，形式是单人口播，用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
【奔驰S级最新信息，风格是正式新闻，其他用默认值】
```

### 批量生成规则

1. **逐条解析**：系统会按顺序解析每一条配置
2. **关键词必填**：如果某条配置不包含搜索关键词信息，直接舍弃
3. **默认值填充**：如果配置信息不全，缺失部分使用默认值
4. **配置清单**：解析完成后生成配置清单表格展示给用户
5. **逐条执行**：按配置清单顺序逐条生成新闻播报
6. **结果汇总**：全部生成完成后，生成结果汇总报告

### 默认值说明

| 配置项 | 默认值 |
|--------|--------|
| 风格 | 自动匹配（根据关键词和新闻内容） |
| 形式 | 单人口播 |
| 音色 | 年轻活力的女生 |
| 深度解读 | 根据关键词自动判断（具体事件=是，宽泛领域=否） |
| 深度解读风格 | 正式新闻腔 |
| 深度解读音色 | 沉稳的中年男性 |

### 批量生成流程

```
用户：【配置1】【配置2】【配置3】...
AI：解析配置 → 生成配置清单 → 展示给用户
AI：开始逐条生成...
    [1/3] 生成配置1...
    [2/3] 生成配置2...
    [3/3] 生成配置3...
AI：生成完成！输出结果汇总
```

### 批量生成输出

批量生成的文件结构：

```
workspace/news/batch_YYYYMMDD_HHMMSS/
├── 配置清单.md              # 配置清单表格
├── 生成结果汇总.md          # 结果汇总报告
├── YYYYMMDD_HHMMSS_关键词1/  # 第1条新闻播报
│   ├── 新闻摘要_*.md
│   ├── 播报文案_*.txt
│   ├── titleAndLabels.txt
│   ├── cover.jpg
│   └── 播报.mp3
├── YYYYMMDD_HHMMSS_关键词2/  # 第2条新闻播报
│   └── ...
└── ...
```

### 不可偷懒规则（非完整配置时）

1. **未确认 ≠ 默认**：用户未明确选择风格/形式/音色时，**禁止**自行假设"默认最优"并直接执行
2. **不可合并步骤**：不能把"询问 + 执行"合并成一个回复，必须先问，等用户回复后再执行
3. **不可预判跳过**：即使用户给的关键词已经很明确，也**必须**走完 Step 1 的全部确认项
4. **违规后果**：跳过确认直接生成的结果视为无效，用户有权要求重新生成

### Step 1 确认清单（缺一不可，除非使用完整配置格式）

| 序号 | 确认项 | 是否可跳过 | 默认值 |
|------|--------|-----------|--------|
| 1 | 新闻关键词 | ❌ 不可跳过 | 无 |
| 2 | 播报风格 | ❌ 必须展示选项 | 自动匹配 |
| 3 | 播报形式 | ❌ 必须展示选项 | 单人口播 |
| 4 | 音色选择 | ❌ 必须展示选项 | 年轻活力女生 |
| 5 | 输出目录 | ✅ 可跳过 | 时间戳子目录 |
| 6 | 深度解读* | ❌ **必须询问** | 具体事件关键词时必须询问，不可跳过 |

\* **深度解读选项**：当关键词为具体新闻事件（非宽泛领域）时**必须询问**，不可默认选择「否」跳过。

### 正确的交互流程

```
用户：帮我生成美军拦截霍尔木兹船只的新闻播报
AI：展示 Step 1 全部选项 → 等待用户选择
用户：风格选2，形式选1，音色选4
AI：确认后开始执行 Step 2-6
```

### 错误的交互流程（禁止出现）

```
用户：帮我生成美军拦截霍尔木兹船只的新闻播报
AI：直接开始搜索、生成、输出结果（❌ 跳过了确认）
```

**记住：多问一句比自作主张好。用户觉得烦会告诉你，但你替他做决定他一定会不满意。**

---

## 工作流程

### Step 1：收集用户输入

向用户确认以下信息（可一次性输入，也可逐步询问）：

#### 1.1 新闻关键词 / 领域

> 📰 请输入你感兴趣的新闻关键词或领域：
>
> **示例：**
> - **领域类**：财经、科技、教育、医疗、体育、娱乐、房产、汽车
> - **主题类**：AI 芯片、新能源汽车、中东局势、北京房价
> - **具体词**：华为 Mate80、宝马 X5、伊朗声明
>
> 💡 可以输入多个，用空格分隔，如"科技 AI 芯片"

#### 1.2 播报文案风格（可选）

> 🎨 请选择播报文案风格，**回复序号或直接输入自定义描述**：
>
> 1. 📻 **正式新闻腔** — 标准播音风格，适合时政、财经、官方消息
> 2. ☀️ **轻松早报腔** — 亲切自然，适合日常热点、生活资讯
> 3. 💹 **财经严肃腔** — 专业理性，适合股市、产业、数据
> 4. 🚀 **科技快评腔** — 简洁有力带点评，适合 AI、互联网、新产品
>
> 💡 **也可以直接输入你想要的风格**，如：
> - `幽默风趣` — 轻松诙谐的语调
> - `严肃深度` — 沉稳专业的分析风格
> - `故事化叙述` — 像讲故事一样播报新闻
> - `快节奏快讯` — 简洁明快的短句风格
>
> ⚡ 未选择时，系统会根据新闻内容自动匹配最适合的风格。

#### 1.3 播报形式（可选）

> 🎙️ 请选择播报形式，回复序号：
>
> 1. 🎤 **单人口播**（默认）— 一位主播完整播报
> 2. 🗣️ **双人对话式播报** — 主播 + 评论员对话形式，更生动有趣
>
> 💡 双人对话示例：
> ```
> 主播：欢迎收听今日新闻，首先关注……
> 评论员：这件事核心看点是……
> 主播：对普通用户/投资者有什么影响？
> 评论员：主要有这几点……
> 主播：以上就是本次播报的内容
> ```
>
> ⚠️ **选择双人对话后，必须进一步询问主播和评论员的音色选择（见 1.4.1）**

#### 1.4 音色选择（可选）

> 🎵 请选择播报音色，**回复序号或直接输入自定义描述**：
>
> 1. 🌸 **年轻活力的女生** — 清脆明亮，适合科技、娱乐、生活类新闻
> 2. 💼 **沉稳的中年男性** — 深沉有力，适合财经、时政、深度报道
> 3. 🎀 **温柔的女生** — 柔和舒缓，适合文化、情感、社会类新闻
> 4. 📻 **专业新闻主播** — 标准播音腔，适合严肃新闻、国际时事
> 5. 🎭 **情感丰富的声音** — 表现力强，适合故事性、戏剧性内容
>
> 💡 **也可以直接输入你想要的音色**，如：
> - `成熟男声` — 稳重低沉的男性声音
> - `甜美女生` — 温柔甜美的女性声音
> - `磁性嗓音` — 有磁性的声音
> - `知性女声` — 知性优雅的女性声音

#### 1.4.1 双人对话音色选择（当选择形式2时必须询问）

> 🎭 **您选择了双人对话式播报，请分别为主播和评论员选择音色：**
>
> **主播音色**（引导话题、提出问题、总结要点）：
> 1. 🌸 年轻活力的女生
> 2. 💼 沉稳的中年男性（默认）
> 3. 🎀 温柔的女生
> 4. 📻 专业新闻主播
> 5. 🎭 情感丰富的声音
>
> **评论员音色**（解读新闻、分析细节、提供观点）：
> 1. 🌸 年轻活力的女生（默认）
> 2. 💼 沉稳的中年男性
> 3. 🎀 温柔的女生
> 4. 📻 专业新闻主播
> 5. 🎭 情感丰富的声音
>
> 💡 建议选择不同音色以形成对话感，如：主播用沉稳男声，评论员用活力女声

#### 1.5 事件深度解读（条件触发，必须询问）

> 📊 **检测到您输入的是具体新闻事件关键词，必须询问是否生成深度解读播报**
>
> 您输入的关键词属于**具体新闻事件**（如"华为 Mate80 发布"、"伊朗袭击以色列"），而非宽泛领域（如"科技"、"财经"）。
>
> 是否需要生成【事件深度解读播报】？
>
> 1. ✅ **是** — 生成深度解读文章 + 单人播报音频
> 2. ❌ **否** — 仅生成常规新闻播报
>
> ⚠️ **此问题必须询问，不可默认选择「否」跳过**
>
> 如果选择「是」，还会询问：
> - **深度解读风格**：可选预设风格（1-4）或直接输入自定义描述
> - **深度解读音色**：可选预设音色（1-6）或直接输入自定义描述
>
> 💡 深度解读包含：事件核心梳理、背景与前因、多维影响分析、利益博弈、趋势判断
> 💡 默认风格：正式新闻腔，默认音色：沉稳的中年男性

**判断标准：**
| 关键词类型 | 示例 | 是否询问深度解读 |
|------|------|----------------|
| 宽泛领域 | 财经、科技、AI、房地产、体育 | ❌ 否 |
| 具体事件 | 华为 Mate80 发布、伊朗袭击以色列、MiniMax 发布 MaxHermes | ✅ **必须询问** |

#### 1.6 输出目录（可选）

未指定时默认使用 `workspace/news/`，并**在此目录下自动创建以时间戳命名的子目录**。

**命名规则：** `workspace/news/{YYYYMMDD_HHMMSS}_{关键词}/`

**示例：**
```
workspace/news/20260414_103500_科技AI芯片/
├── 新闻摘要_科技AI芯片_2026-04-14.md
├── 播报文案_科技AI芯片_2026-04-14.txt
├── titleAndLabels.txt
├── cover.jpg
├── 播报_科技AI芯片.mp3
├── 深度解读文案.txt          # 可选（具体事件时生成）
└── 事件深度解读.mp3          # 可选（具体事件时生成）
```

这样可以确保每次生成的新闻播报文件都有独立的目录，不会互相覆盖。

---

### Step 2：搜索新闻

#### 2.1 搜索策略（优先级排序）

**搜索工具优先级（自动降级）：**

| 优先级 | 工具 | 说明 | 配置要求 |
|--------|------|------|----------|
| 1 | **Tavily Search** | AI 优化搜索，结果质量高 | `TAVILY_API_KEY` |
| 2 | **Baidu Search** | 国内搜索，中文新闻质量高 | `BAIDU_API_KEY` |
| 3 | Tavily API | Tavily 基础模式重试 | `TAVILY_API_KEY` |
| 4 | news-aggregator | 多源聚合 | 无需配置 |
| 5 | web_fetch | 直接抓取网页 | 无需配置 |

**使用建议：**
- ✅ **优先使用 Tavily**：配置 `TAVILY_API_KEY` 后，搜索质量最高，国际新闻覆盖全面
- ✅ **Baidu Search 备选**：当 Tavily 不可用时，自动使用 Baidu Search，国内网络稳定，中文新闻质量高
- ⚠️ **SearXNG/Felo**：国内访问受限，不推荐

**搜索降级流程：**
```
Tavily Search → Baidu Search → Tavily API (重试) → news-aggregator → web_fetch
     ↓ 超时/失败      ↓ 无结果        ↓ 失败            ↓ 失败
   自动降级          自动降级        自动降级          自动降级
```

#### 2.2 多新闻源 + 去重 + 可信度判断

**联网搜索至少 3 类来源：**

| 来源类型 | 代表媒体 | 优先级 |
|---------|---------|--------|
| 权威媒体 | 央视 / 新华社 / 人民网 / 路透社 | 🔴 最高 |
| 官方发布 | 公司官网 / 政府公告 / 部委通报 | 🟠 高 |
| 垂直门户 | 36Kr / 华尔街见闻 / 腾讯科技 / 汽车之家 | 🟡 中 |
| 社交媒体 | 微博热搜 / 知乎热榜 / V2EX | 🟢 参考 |

**搜索要求：**
- 搜索相关新闻 ≥ 5 条
- 来源优先：权威媒体 > 官方 > 垂直媒体 > 社交媒体

**新闻清洗处理：**
1. **去重**：对标题和正文做相似度去重（相同事件只保留一条）
2. **排序**：按时间倒序（最新在前）
3. **打标**：给每条新闻打标签和可信度

**标签体系：**

| 标签 | 说明 | 示例 |
|------|------|------|
| 【权威】 | 权威媒体首发 | 新华社、央视 |
| 【突发】 | 刚刚发生的事件 | 地震、事故 |
| 【数据】 | 以数据为核心的报道 | 经济数据、财报 |
| 【争议】 | 有争议性的话题 | 政策变动 |
| 【预告】 | 即将发生的事件 | 新品发布、会议 |

**可信度评估：**
- **高**：权威媒体或官方来源，且有多个来源交叉验证
- **中**：垂直媒体报道，或单一权威来源
- **低**：社交媒体来源，或未验证的传言

**输出格式：**
```
【新闻来源】新华社
【可信度】高
【事件标签】【权威】【数据】
【时间】2026-04-13
【正文】……
```

#### 2.2 搜索策略选择

**根据关键词类型自动选择搜索源：**

| 关键词类型 | 搜索策略 | 工具 |
|-----------|---------|------|
| 通用新闻（时政/社会） | web_search + 权威媒体抓取 | web_search, web_fetch |
| 具体产品/品牌 | 行业网站 + 综合搜索 | web_fetch(行业站), web_search |
| 财经类 | 华尔街见闻 + 财经网站 | web_fetch(wallstreetcn) |
| 科技类 | 36Kr + GitHub + HackerNews | web_fetch(36kr), news-aggregator |
| 英文新闻 | HackerNews + ProductHunt | news-aggregator |

#### 2.3 三级摘要（必做）

对每条筛选后的新闻生成 **3 种摘要**：

| 级别 | 时长 | 字数 | 用途 |
|------|------|------|------|
| 20 秒速报 | ~20s | 60 字以内 | 快速口播、标题新闻 |
| 60 秒解读 | ~60s | 300 字以内 | 完整播报、深度理解 |
| 要点清单 | - | 3-5 条短句 | 快速浏览、结构化信息 |

**提示词模板：**
```
请对下面新闻生成三级摘要：
1. 20秒速报：60字以内，适合口播
2. 60秒解读：300字以内，完整通顺
3. 要点清单：3-5条，每条短句

新闻内容：
{news_content}
```

---

### Step 3：生成播报文案

#### 3.1 调用大模型生成文案

**所有播报文案均通过动态读取 OpenClaw 配置后，调用大模型 API 生成，不再使用简单模板替换。**

**配置读取流程（优先使用当前 Agent 配置）：**

```python
# 1. 读取 OpenClaw 配置
config = _load_openclaw_config()  # ~/.openclaw/openclaw.json

# 2. 获取当前会话 Agent 的模型配置（优先）
agent_list = config.get('agents', {}).get('list', [])
current_agent_model = None
for agent in agent_list:
    if agent.get('id') == 'main':  # 当前会话通常是 main agent
        current_agent_model = agent.get('model')
        break

# 回退到全局默认配置
default_model = current_agent_model or config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary')

# 3. 解析 provider 和 model
if default_model and '/' in default_model:
    provider_name, model_id = default_model.split('/', 1)
else:
    provider_name = 'qwen'
    model_id = default_model or 'qwen3.5-plus'

# 4. 查找对应的 provider 配置
providers = config.get('models', {}).get('providers', {})
provider_config = providers.get(provider_name)

# 如果当前 provider 没有 apiKey，尝试查找其他有 apiKey 的 provider
fallback_to_manual = False
if not provider_config or not provider_config.get('apiKey'):
    for pname, pconfig in providers.items():
        if pconfig.get('apiKey') and pconfig.get('baseUrl'):
            provider_config = pconfig
            provider_name = pname
            print(f'当前 provider 无 apiKey，自动切换到: {pname}')
            break
    else:
        # 没有找到有 apiKey 的 provider，使用手动编写兜底
        fallback_to_manual = True
        print('警告：找不到配置有 apiKey 的模型提供商，将使用手动编写文案')

# 5. 提取 API 配置（如果未回退到手动编写）
if not fallback_to_manual:
    api_key = provider_config.get('apiKey')
    base_url = provider_config.get('baseUrl')
```

**配置来源（零硬编码）：**

| 配置项 | JSON 路径 | 说明 |
--------|-----------|------
| **Agent 模型** | `agents.list[].model` | 当前会话 Agent 的模型配置（优先）|
| **全局默认模型** | `agents.defaults.model.primary` | 格式：`provider/model`（回退）|
| **API Key** | `models.providers.{provider}.apiKey` | 动态读取 |
| **Base URL** | `models.providers.{provider}.baseUrl` | 动态读取 |
| **模型 ID** | `models.providers.{provider}.models[].id` | 动态读取 |

**API 调用（仅在未回退到手动编写时）：**
- **端点**：`{baseUrl}/chat/completions`
- **格式**：OpenAI-compatible
- **超时**：120秒
- **温度**：0.7
- **最大 tokens**：3000

**特点：**
- ✅ **零硬编码**：所有配置从 `openclaw.json` 动态读取
- ✅ **多提供商支持**：自动识别 DashScope、Kimi、Ollama 等
- ✅ **配置即代码**：OpenClaw 配置更新后自动生效
- ✅ **安全**：API Key 不写在代码里

**失败回退（按优先级）：**
1. 当前 Agent 的 provider 无 apiKey → 自动查找其他有 apiKey 的 provider（如 dashscope 系列）
2. 所有 provider 都失败 → **使用手动编写文案作为兜底方案**

**⚠️ 优先使用大模型 API 生成文案，API 不可用时允许手动编写。**

**提示词设计：**

**单人口播提示词：**
```
请基于以下新闻内容，撰写一篇单人口播新闻播报文案。
要求：
1. 风格：{风格}
2. 开头要有问候语和栏目介绍
3. 每条新闻之间要有自然过渡
4. 要包含新闻来源和可信度说明
5. 结尾要有结束语
6. 语言口语化，适合朗读，避免长句
7. 控制总时长在 3-5 分钟
```

**双人对话提示词：**
```
请基于以下新闻内容，撰写一篇双人对话式新闻播报文案。
角色设定：
- 主播（晓晓）：引导话题，提出问题，总结要点
- 评论员（云深）：解读新闻，分析细节，提供观点
要求：
1. 风格：{风格}
2. 开头要有问候语和自我介绍
3. 采用对话形式，主播和评论员交替发言
4. 每条新闻的结构：主播引入 → 评论员速报 → 主播追问 → 评论员解读 → 要点总结
5. 要包含新闻来源和可信度说明
6. 结尾要有结束语
7. 语言口语化，自然流畅，像真实对话
8. 控制总时长在 4-6 分钟
输出格式：
主播：...
评论员：...
（以此类推）
```

#### 3.2 风格化重写

**根据用户选择的风格重写新闻文案。用户未选择时，根据新闻内容自动匹配：**

| 内置风格 | 适配场景 | 语调特征 |
|---------|---------|---------|
| 📻 正式新闻腔 | 时政、财经、官方消息 | 规范、客观、简洁 |
| ☀️ 轻松早报腔 | 日常热点、生活资讯 | 亲切、口语化、有温度 |
| 💹 财经严肃腔 | 股市、产业、数据 | 专业、理性、数据驱动 |
| 🚀 科技快评腔 | AI、互联网、新产品 | 简洁有力、带点评、有态度 |

**自动匹配规则：**
- 关键词含"政策/政府/国务院/部委" → 正式新闻腔
- 关键词含"股票/基金/经济/房价/GDP" → 财经严肃腔
- 关键词含"AI/芯片/互联网/产品/发布" → 科技快评腔
- 其他 → 轻松早报腔

#### 3.2 播报形式

**单人口播文案结构：**
```
各位听众朋友大家好，欢迎收听{栏目名称}。

{新闻1 - 60秒解读}

{新闻2 - 60秒解读}

...

以上就是本次播报的内容，感谢您的收听。
```

**双人对话播报文案结构：**
```
主播：欢迎收听{栏目名称}，我是{主播名}。
评论员：大家好，我是{评论员名}。

主播：首先关注今天的一条重要新闻……
评论员：这件事核心看点是……主要有三个方面。第一……
主播：这对普通用户/投资者有什么影响呢？
评论员：主要有这几点影响……

主播：接下来我们来看……
评论员：这个事件背后其实……

主播：以上就是本次播报的全部内容。
评论员：我们下次再见！
```

**双人对话音色分配（默认）：**
- 主播：🌸 年轻活力的女生（zh-CN-XiaoxiaoNeural）
- 评论员：💼 沉稳的中年男性（zh-CN-YunxiNeural）

用户可自定义双方音色，如"主播用温柔女声，评论员用专业男声"。

#### ⚠️ 双人对话音频生成规则（必须遵守）

**错误做法（禁止）：**
```python
# ❌ 把所有主播台词合并成一段音频
# ❌ 把所有评论员台词合并成一段音频
# ❌ 把两段音频首尾相连
host_all = "主播第一句。主播第二句。主播第三句。"
commentator_all = "评论员第一句。评论员第二句。评论员第三句。"
# 结果：主播说完所有话，评论员再说所有话 → 不是对话！
```

**正确做法（必须按此流程）：**
```python
# ✅ 第一步：逐句解析播报文案，按对话顺序提取每一句
# 文案格式：
#   主播：第一句
#   评论员：第一句
#   主播：第二句
#   评论员：第二句
# ...

lines = []
for line in script.split('\n'):
    if line.startswith('主播：'):
        lines.append(('host', line.split('：', 1)[1]))
    elif line.startswith('评论员：'):
        lines.append(('commentator', line.split('：', 1)[1]))

# ✅ 第二步：按对话顺序，逐句生成音频（交替使用不同音色）
#   第1句 主播 → audio_001.mp3
#   第2句 评论员 → audio_002.mp3
#   第3句 主播 → audio_003.mp3
#   第4句 评论员 → audio_004.mp3
# ...

# ✅ 第三步：按对话顺序拼接所有音频片段
#   audio_001 + audio_002 + audio_003 + audio_004 + ...
# 使用 ffmpeg concat 或 pydub 按顺序拼接

# ✅ 最终效果：主播说一句，评论员接一句，真实对话感
```

**关键原则：**
1. **逐句拆分**：每行独立作为一段音频生成，不可合并
2. **交替音色**：主播和评论员使用不同的 voice_id
3. **顺序拼接**：严格按文案中的对话顺序拼接，先出现的先拼接
4. **临时文件**：每句生成独立 mp3 到临时目录，拼接完成后清理

**拼接工具：**
- 首选：`ffmpeg -f concat`（需安装 ffmpeg）
- 备选：`pydub.AudioSegment`（需 ffmpeg 支持）
- 兜底：生成独立 mp3 文件，告知用户手动拼接

#### 3.3 文案生成规则

- **口语化**：避免书面语，使用"百分之"替代"%"，"二零二六年"替代"2026年"
- **流畅性**：句子简短，避免长句和复杂从句
- **转场自然**：新闻之间用"接下来"、"再来看"、"另一方面"等过渡
- **时长控制**：单条新闻播报控制在 30-90 秒

---

### Step 4：搜索配图

**封面图搜索采用组合策略，按优先级执行：**

| 优先级 | 方案 | 说明 | 准确度 |
|--------|------|------|--------|
| 1 | **新闻源原图抓取** | 从新闻网页提取 og:image、twitter:image 或文章配图 | ⭐⭐⭐⭐⭐ 最高 |
| 2 | **AI 生成** | 使用 `autoglm-generate-image` 根据新闻内容生成 | ⭐⭐⭐⭐ 高 |
| 3 | **图库搜索** | Unsplash API，使用智能关键词优化 | ⭐⭐⭐ 中 |

#### 4.1 新闻源原图抓取（推荐）

**抓取策略优先级：**
1. `og:image` - Open Graph 标准，社交媒体分享图（最可靠）
2. `twitter:image` - Twitter 卡片图
3. `<article>` 标签内的首图
4. 内容区域的大图（>300px）

**智能关键词优化：**
- 从关键词去除动词/时间词（如"首次"、"亮相"、"今天"）
- 从新闻标题提取高频实体词
- 添加类别词作为兜底（如"机车"→"摩托车"）

**示例优化：**
- 输入：`"张雪机车首次亮相广交会"`
- 提取实体：`["张雪机车", "广交会", "摩托车"]`
- 搜索词：`"张雪机车"` → `"摩托车 展会"`

#### 4.2 AI 生成配图

当新闻源无图或图库搜索不匹配时，使用 AI 生成：

```bash
# 自动生成提示词示例
"张雪机车 新闻配图，专业摄影风格，高清，适合新闻播报封面，16:9 横版构图"
```

**优势：**
- 完全匹配新闻主题
- 风格统一可控
- 无版权风险

#### 4.3 图库搜索（兜底）

使用 Unsplash API 进行图库搜索。

**API Key 配置方式（优先级排序）：**

1. **OpenClaw 配置文件**（推荐）
   编辑 `~/.openclaw/openclaw.json`：
   ```json
   {
     "custom": {
       "unsplash": {
         "accessKey": "你的_Unsplash_Access_Key"
       }
     }
   }
   ```

2. **环境变量**
   ```bash
   export UNSPLASH_ACCESS_KEY="你的_Unsplash_Access_Key"
   ```

⚠️ **注意**：如果未配置 Unsplash Key，图库搜索功能将被跳过，但新闻源原图抓取和 AI 生成功能仍然可用。

**获取 Unsplash Access Key：**
1. 访问 https://unsplash.com/developers
2. 注册/登录账号
3. 创建 New Application
4. 复制 Access Key

**使用示例：**
```python
import requests
access_key = '你的_Unsplash_Access_Key'
r = requests.get('https://api.unsplash.com/search/photos',
    params={'query': '{优化后的关键词}', 'per_page': 3, 'orientation': 'landscape'},
    headers={'Authorization': f'Client-ID {access_key}'}, timeout=10)
```

**改进点：**
- 使用实体提取优化搜索词
- 多候选图片选择（避免返回图标/小图）
- 图片大小过滤（≥10KB）

将封面图引用嵌入摘要文档开头：`![封面图](cover.jpg)`

---

### Step 5：生成播报音频

**音频生成优先级（按用户环境自动选择）：**

| 优先级 | 方案 | 条件 | 优势 |
|--------|------|------|------|
| 1 | CellCog / audio-cog | 已安装 `cellcog` SDK 或 `audio-cog` 技能 | AI 音色更自然 |
| 2 | edge-tts | 已安装 `edge-tts` 包（免费） | 稳定快速，6 种中文声音 |
| 3 | 系统 TTS | Windows SAPI / macOS say | 兜底方案 |

#### 5.1 使用 CellCog / audio-cog（推荐）

**检测方式：**
- 检查 `~/.agents/skills/audio-cog/SKILL.md` 是否存在
- 检查环境变量 `CELLCOG_API_KEY` 是否已配置

**CellCog 使用方式：**
```python
from cellcog import CellCogClient

client = CellCogClient()
result = client.create_chat(
    prompt=f'Generate TTS audio using MiniMax provider with {voice_name} voice. Read this news script:\n\n{script}',
    task_label='news-podcast',
    chat_mode='agent',
    timeout=120
)
```

**audio-cog 技能使用方式：**
```python
import subprocess
# 调用 audio-cog 技能目录下的脚本
skill_dir = os.path.expanduser('~/.agents/skills/audio-cog')
subprocess.run([sys.executable, f'{skill_dir}/scripts/generate.py',
    '--text', script, '--voice', voice_id, '--output', output_path])
```

> ⚠️ CellCog Agent 模式需要账户余额 ≥ 100 credits。如余额不足，自动回退到 edge-tts。

#### 5.2 使用 edge-tts（免费兜底）

```python
import edge_tts, asyncio

async def generate():
    communicate = edge_tts.Communicate(script, voice_id)
    await communicate.save(output_path)

asyncio.run(generate())
```

**edge-tts 可用中文声音：**

| 声音 ID | 描述 | 适用场景 |
|---------|------|---------|
| zh-CN-XiaoxiaoNeural | 年轻活力女声 | 科技、娱乐、生活（默认主播音） |
| zh-CN-YunxiNeural | 沉稳中年男声 | 财经、时政、深度（默认评论员音） |
| zh-CN-XiaoyiNeural | 温柔女声 | 文化、情感、社会 |
| zh-CN-YunyangNeural | 专业新闻男声 | 严肃新闻、国际时事 |
| zh-CN-XiaobeiNeural | 活泼女声 | 故事、专题、娱乐 |
| zh-CN-YunhaoNeural | 年轻活力女声 | 体育、青年话题 |

**双人对话音频生成：**
1. 将文案按角色拆分为多段
2. 分别为每段生成音频
3. 使用 pydub 拼接为完整音频（可选加转场音效）

---

### Step 6：事件深度解读播报（可选）

当用户输入**具体新闻事件关键词**（而非宽泛领域）时，系统会询问是否生成事件深度解读播报。

**关键词类型判断：**
| 类型 | 示例 | 是否询问深度解读 |
|------|------|----------------|
| 宽泛领域 | 财经、科技、AI、房地产 | ❌ 否 |
| 具体事件 | 华为Mate80发布、伊朗袭击以色列 | ✅ 是 |

**深度解读结构（5部分）：**
1. **事件核心梳理**：概括新闻关键信息
2. **事件背景与前因**：政策、行业环境、历史脉络
3. **多维度影响分析**：行业、市场、企业、用户影响
4. **利益博弈与各方态度**：不同主体立场与冲突
5. **趋势判断与启示**：短期/长期趋势、风险、机会

**默认配置：**
- 风格：正式新闻腔
- 音色：沉稳的中年男性
- 字数：800-1200字

**实现方式：**

**使用 OpenClaw 当前会话 Agent 的模型配置，自动识别模型提供商**

```python
# 1. 读取 OpenClaw 配置
config = _load_openclaw_config()  # ~/.openclaw/openclaw.json

# 2. 获取当前会话 Agent 的模型配置（优先使用 agent 特定配置，而非全局默认）
# 首先尝试获取当前 agent 的配置
agent_list = config.get('agents', {}).get('list', [])
current_agent_model = None
for agent in agent_list:
    if agent.get('id') == 'main':  # 当前会话通常是 main agent
        current_agent_model = agent.get('model')
        break

# 如果找不到 agent 特定配置，才回退到全局默认
default_model = current_agent_model or config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary')
# 示例：qwen/kimi-k2.5 → provider=qwen, model=kimi-k2.5

# 3. 解析 provider 和 model
if default_model and '/' in default_model:
    provider_name, model_id = default_model.split('/', 1)
else:
    provider_name = 'qwen'
    model_id = default_model or 'qwen3.5-plus'

# 4. 查找对应的 provider 配置
providers = config.get('models', {}).get('providers', {})
provider_config = providers.get(provider_name)

# 如果当前 provider 没有 apiKey，尝试查找其他有 apiKey 的 provider
fallback_to_manual = False
if not provider_config or not provider_config.get('apiKey'):
    for pname, pconfig in providers.items():
        if pconfig.get('apiKey') and pconfig.get('baseUrl'):
            provider_config = pconfig
            provider_name = pname
            print(f'当前 provider 无 apiKey，自动切换到: {pname}')
            break
    else:
        # 没有找到有 apiKey 的 provider，使用手动编写兜底
        fallback_to_manual = True
        print('警告：找不到配置有 apiKey 的模型提供商，将使用手动编写文案')

# 5. 提取 API 配置（如果未回退到手动编写）
if not fallback_to_manual:
    api_key = provider_config.get('apiKey')
    base_url = provider_config.get('baseUrl')
```

**配置来源（零硬编码）：**

| 配置项 | JSON 路径 | 说明 |
|--------|-----------|------|
| **Agent 模型** | `agents.list[].model` | 当前会话 Agent 的模型配置（优先）|
| **全局默认模型** | `agents.defaults.model.primary` | 格式：`provider/model`（回退）|
| **Provider** | `models.providers.{provider}` | 根据模型自动匹配 |
| **API Key** | `models.providers.{provider}.apiKey` | 动态读取 |
| **Base URL** | `models.providers.{provider}.baseUrl` | 动态读取 |
| **模型 ID** | `models.providers.{provider}.models[].id` | 动态读取 |

**注意**：优先读取 `agents.list` 中当前 Agent 的 `model` 字段，而非全局 `agents.defaults.model.primary`。如果当前 provider 无 apiKey，自动查找其他有 apiKey 的 provider；如果都不可用，使用手动编写文案作为兜底。

**支持的模型提供商：**
- DashScope（通义千问）
- Kimi
- Ollama（本地模型）
- 任意 OpenAI-compatible API

**API 调用：**
- **端点**：`{baseUrl}/chat/completions`
- **格式**：OpenAI-compatible
- **超时**：120秒
- **温度**：0.7
- **最大 tokens**：3000

**特点：**
- ✅ **零硬编码**：所有配置从 `openclaw.json` 动态读取
- ✅ **自动识别**：根据默认模型自动匹配 provider
- ✅ **多提供商支持**：支持任意配置好的模型提供商
- ✅ **配置即代码**：OpenClaw 配置更新后自动生效
- ✅ **安全**：API Key 不写在代码里

**失败回退（按优先级）：**
1. 当前 Agent 的 provider 无 apiKey → 自动查找其他有 apiKey 的 provider（如 dashscope 系列）
2. 所有 provider 都失败 → **使用手动编写文案作为兜底方案**

**⚠️ 优先使用大模型 API 生成文案，API 不可用时允许手动编写。**

**提示词模板：**
```
请基于以下新闻内容，撰写一篇专业、客观、深度解读文章，要求逻辑严谨、结构清晰，适合公众号 / 行业分析使用。
请精简冗余语句，强化逻辑链条，使全文更像专业深度评论。
...
（详见代码中的 DEEP_ANALYSIS_PROMPT）
```

---

### Step 7：输出结果

#### 7.1 向用户展示生成的文件列表和概要信息

| 文件 | 说明 | 是否必需 |
|------|------|---------|
| 📄 新闻摘要_{关键词}.md | 完整新闻摘要文档（含三级摘要） | ✅ 必需 |
| 📄 播报文案_{关键词}.txt | 纯文本播报稿（可直接用于 TTS） | ✅ 必需 |
| 📋 **titleAndLabels.txt** | **新闻标题和标签信息（固定文件名）** | ✅ 必需 |
| 🖼️ cover.jpg | 新闻封面图 | ✅ 必需 |
| 🎵 播报_{关键词}.mp3 | 新闻播报音频（单人或双人） | ✅ 必需 |
| 📊 **深度解读文案.txt** | **事件深度解读文章（可选）** | ⚪ 可选 |
| 🎙️ **事件深度解读.mp3** | **深度解读播报音频（可选）** | ⚪ 可选 |

#### 7.2 文件完整性检查（必须执行）

**在向用户展示结果之前，必须执行以下检查：**

```python
import os

def check_output_files(output_dir, keyword, has_deep_analysis=False):
    """
    检查输出文件是否齐全
    
    Args:
        output_dir: 输出目录路径
        keyword: 新闻关键词（用于文件名匹配）
        has_deep_analysis: 是否包含深度解读
    
    Returns:
        (is_complete: bool, missing_files: list, file_status: dict)
    """
    required_files = [
        ('新闻摘要', f'新闻摘要_{keyword}_*.md'),
        ('播报文案', f'播报文案_{keyword}.txt'),
        ('titleAndLabels', 'titleAndLabels.txt'),
        ('封面图', 'cover.jpg'),
        ('播报音频', f'播报_{keyword}.mp3'),
    ]
    
    optional_files = []
    if has_deep_analysis:
        optional_files = [
            ('深度解读文案', '深度解读文案.txt'),
            ('深度解读音频', '事件深度解读.mp3'),
        ]
    
    file_status = {}
    missing_files = []
    
    # 检查必需文件
    for name, pattern in required_files:
        if '*' in pattern:
            # 通配符匹配
            import glob
            matches = glob.glob(os.path.join(output_dir, pattern))
            if matches:
                file_status[name] = os.path.basename(matches[0])
            else:
                file_status[name] = '❌ 缺失'
                missing_files.append(name)
        else:
            # 精确匹配
            filepath = os.path.join(output_dir, pattern)
            if os.path.exists(filepath):
                file_status[name] = pattern
            else:
                file_status[name] = '❌ 缺失'
                missing_files.append(name)
    
    # 检查可选文件
    for name, pattern in optional_files:
        filepath = os.path.join(output_dir, pattern)
        if os.path.exists(filepath):
            file_status[name] = pattern
        else:
            file_status[name] = '⚪ 未生成'
    
    is_complete = len(missing_files) == 0
    return is_complete, missing_files, file_status


# 使用示例（带重试机制，最多3次）
def generate_with_retry(output_dir, keyword, has_deep_analysis=False, max_retries=3):
    """
    生成文件并检查完整性，最多重试3次
    """
    retry_count = 0
    last_missing = []
    last_status = {}
    
    while retry_count < max_retries:
        is_complete, missing, status = check_output_files(
            output_dir=output_dir,
            keyword=keyword,
            has_deep_analysis=has_deep_analysis
        )
        
        if is_complete:
            print('✅ 所有文件已齐全')
            return True, status
        
        retry_count += 1
        last_missing = missing
        last_status = status
        
        if retry_count < max_retries:
            print(f'第 {retry_count} 次检查：以下文件缺失，正在补充生成：{missing}')
            # 根据缺失的文件类型，调用相应的生成函数补充
            for missing_file in missing:
                try:
                    if missing_file == '封面图':
                        generate_cover_image()
                    elif missing_file == '播报音频':
                        generate_broadcast_audio()
                    elif missing_file == '新闻摘要':
                        generate_news_summary()
                    elif missing_file == '播报文案':
                        generate_broadcast_script()
                    elif missing_file == 'titleAndLabels':
                        generate_title_and_labels()
                    # ... 其他补充逻辑
                except Exception as e:
                    print(f'生成 {missing_file} 失败：{str(e)}')
        else:
            print(f'第 {retry_count} 次检查：以下文件仍然缺失：{missing}')
    
    # 超过最大重试次数，向用户说明原因
    print(f'\n⚠️ 文件完整性检查完成，但以下文件未能生成（已尝试 {max_retries} 次）：')
    for missing_file in last_missing:
        print(f'  - {missing_file}')
    
    print('\n可能的原因：')
    print('  1. 网络连接问题（如 Unsplash API、新闻源网站无法访问）')
    print('  2. API Key 配置问题（如大模型 API 未配置或已过期）')
    print('  3. 依赖工具缺失（如 ffmpeg、edge-tts 未安装）')
    print('  4. 新闻源内容问题（如网页结构变化导致抓取失败）')
    print('\n建议：')
    print('  - 检查网络连接和 API 配置')
    print('  - 查看具体错误日志定位问题')
    print('  - 如需完整结果，可重新执行技能')
    
    return False, last_status


# 执行生成和检查
success, final_status = generate_with_retry(
    output_dir='/path/to/output',
    keyword='北京国际电影节',
    has_deep_analysis=True,
    max_retries=3
)
```

**检查规则：**
1. **必需文件**（5个）：新闻摘要、播报文案、titleAndLabels.txt、封面图、播报音频
2. **可选文件**（2个）：深度解读文案、深度解读音频（仅当用户选择深度解读时检查）
3. **发现缺失**：调用对应生成函数补充，最多重试 **3 次**
4. **重试机制**：每次补充后再次检查，记录失败原因
5. **最终处理**：3次后仍有缺失，向用户说明原因并展示已生成文件

**完整性检查流程图（最多3次）：**
```
生成所有文件 → 执行完整性检查 → 发现缺失？
    ↓ 是                    ↓ 否（3次内齐全）
重试次数 < 3？          向用户展示完整结果
    ↓ 是                    ↓
调用生成函数补充 → 再次检查    
    ↓ 否（已达3次）
向用户说明缺失原因 → 展示已生成文件
```

**缺失原因说明模板：**
```
⚠️ 文件完整性检查完成，但以下文件未能生成（已尝试 3 次）：
  - {文件1}
  - {文件2}

可能的原因：
  1. 网络连接问题（如 Unsplash API、新闻源网站无法访问）
  2. API Key 配置问题（如大模型 API 未配置或已过期）
  3. 依赖工具缺失（如 ffmpeg、edge-tts 未安装）
  4. 新闻源内容问题（如网页结构变化导致抓取失败）

建议：
  - 检查网络连接和 API 配置
  - 查看具体错误日志定位问题
  - 如需完整结果，可重新执行技能
```

#### titleAndLabels.txt 格式规范

**文件名固定为** `titleAndLabels.txt`，编码为 UTF-8 with BOM。

**内容格式：**
```
【新闻标题】{标题1}
【事件标签】{标签1}
【可信度】{可信度}
【时间】{时间}

【新闻标题】{标题2}
【事件标签】{标签2}
【可信度】{可信度}
【时间】{时间}

...
```

**如果播报包含多条新闻，分段落分别展示，每条新闻之间用空行分隔。**

**示例：**
```
【新闻标题】央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元
【事件标签】【权威】【数据】
【可信度】高
【时间】2026-04-14

【新闻标题】AI 芯片巨头英伟达发布新一代 Blackwell Ultra GPU
【事件标签】【预告】
【可信度】高
【时间】2026-04-14

【新闻标题】北京二手房成交量连续三个月环比上涨
【事件标签】【数据】
【可信度】中
【时间】2026-04-13
```

---

## 注意事项

1. **编码**：所有含中文的文件必须使用 **UTF-8 with BOM**（`utf-8-sig`）编码
2. **音色提示**：用户未提供音色信息时，必须主动展示示例并询问
3. **风格自适应**：用户未选择风格时，根据新闻内容自动匹配
4. **去重处理**：同一事件多篇报道只保留最权威的一条
5. **可信度标注**：每条新闻必须标注来源和可信度
6. **输出目录**：如目录不存在则自动创建
7. **搜索失败**：如某个源搜索失败，尝试其他可用源
8. **双人音频**：如果 pydub 未安装，退化为生成两个独立 mp3 文件

---

## 批量生成使用示例

### Python API 调用方式

```python
from fetch_and_generate_v2 import run_batch_broadcast

# 批量配置文本
batch_config = """
【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
【宝马X5最新信息，风格是科技快评腔，形式是单人口播，用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
【奔驰S级最新信息，风格是正式新闻，其他用默认值】
"""

# 执行批量生成
result = run_batch_broadcast(batch_config)

# 检查结果
if result['success']:
    print(f"成功生成 {result['success_count']} 条")
    print(f"输出目录: {result['output_dir']}")
else:
    print(f"批量生成失败: {result['error']}")
```

### 命令行调用方式

```bash
# 单条生成
python fetch_and_generate_v2.py "【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读】"

# 批量生成（在Python脚本中调用）
python -c "from fetch_and_generate_v2 import run_batch_broadcast; run_batch_broadcast('【配置1】【配置2】...')"
```

### 批量生成结果示例

```
============================================================
📰 Auto News Podcast - 批量生成模式
============================================================

[Step 1] 解析批量配置...
[OK] 解析到 3 条配置

[Step 2] 填充默认配置...
[OK] 已填充默认值

[Step 3] 生成配置清单...
# 📋 新闻播报配置清单

| 序号 | 关键词 | 风格 | 形式 | 音色 | 深度解读 | 状态 |
|------|--------|------|------|------|----------|------|
| 1 | 华为Mate80发布 | 科技快评腔 | 双人对话式播报 | 双人对话 | ✅ | ⏳ 待生成 |
| 2 | 宝马X5最新信息 | 科技快评腔 | 单人口播 | 温柔的女生... | ✅ | ⏳ 待生成 |
| 3 | 奔驰S级最新信息 | 正式新闻腔 | 单人口播 | 年轻活力的... | ❌ | ⏳ 待生成 |

**总计：3 条新闻播报**

[OK] 配置清单已保存: .../batch_20260423_114500/配置清单.md

============================================================
[Step 4] 开始逐条生成新闻播报...
============================================================

------------------------------------------------------------
📰 [1/3] 开始生成第 1 条
------------------------------------------------------------
...
✅ 第 1 条生成成功: 华为Mate80发布

------------------------------------------------------------
📰 [2/3] 开始生成第 2 条
------------------------------------------------------------
...
✅ 第 2 条生成成功: 宝马X5最新信息

------------------------------------------------------------
📰 [3/3] 开始生成第 3 条
------------------------------------------------------------
...
✅ 第 3 条生成成功: 奔驰S级最新信息

============================================================
📊 批量生成完成 - 结果汇总
============================================================
总计: 3 条
成功: 3 条 ✅
失败: 0 条 ❌
输出目录: .../batch_20260423_114500

[OK] 结果汇总已保存: .../batch_20260423_114500/生成结果汇总.md

============================================================
✅ 批量生成任务全部完成!
============================================================
```
