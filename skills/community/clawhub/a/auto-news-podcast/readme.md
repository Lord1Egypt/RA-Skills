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

## 系统要求 | System Requirements

- **Python**: 3.8+
- **依赖包**: requests, edge-tts, pydub (可选)
- **API Keys**: 
  - TAVILY_API_KEY（推荐）
  - BAIDU_API_KEY（备选）
  - UNSPLASH_ACCESS_KEY（可选，用于封面图）

---

## 标签 | Tags

`news` `podcast` `audio` `tts` `batch` `automation` `chinese`

---

## 版本 | Version

v1.0.0 - 支持批量生成、多搜索源降级

v1.0.0 - Supports batch generation, multi-source search fallback
