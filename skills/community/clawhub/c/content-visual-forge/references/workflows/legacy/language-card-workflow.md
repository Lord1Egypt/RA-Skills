# 语言学习卡完整流程（Language Learning Card Workflow）

> **领域定位：** 本工作流专注于**语言学习领域**的卡片生成。
> 
> **覆盖范围：** 单字、词汇、语法、短语、发音、翻译等语言学习内容。
> 
> **不覆盖：** 数学公式、编程代码、历史时间线等非语言学习内容。  
> 如需支持其他领域，未来将提供独立的工作流文件。

---

> **🔤 术语说明（重要）：**
> 
> 本文档中会出现两个相似的术语，它们是**不同层次**的概念：
> 
> | 术语 | 层次 | 含义 | 示例 |
> |------|------|------|------|
> | **`language-card`** | 领域层 | 本工作流的定位，指"语言学习域" | 本文件名：language-card-workflow.md |
> | **`learning-card`** | 模板层 | 共享模板族名称，提供数据契约和渲染模板 | template-families/learning-card/ |
> 
> **类比理解：**
> - `language-card-workflow.md` 就像"餐饮业务流程手册"（定义如何经营餐厅）
> - `learning-card` 模板族就像"餐具套装"（提供可复用的工具）
> - 两者是不同层次的概念，前者使用后者，但不能混用
> 
> **为什么要区分？**
> - 未来会有 `stem-card-workflow.md`（理工科域）、`humanities-card-workflow.md`（人文域）
> - 但它们都可能使用同一套底层模板（learning-card）
> - 这样可以避免重复造轮子，同时保持领域清晰

---

本文件描述所有语言学习卡类型的统一生成流程，包括单字卡、词汇卡、语法卡、短语卡、发音卡、翻译卡。

---

## 适用场景

`language-card` 是以下卡片类型的共享执行家族：

- **character-card** - 单字学习卡（汉字启蒙、识字卡片）
- **vocabulary-card** - 词汇卡（词表、单词、搭配、发音和含义卡）
- **grammar-card** - 语法卡（语法点、句型、纠错卡、用法规则）
- **phrase-card** - 短语卡（固定短语、常用表达、句块、自然用法卡）
- **pronunciation-card** - 发音卡（音标对比、最小对比对、语调练习）⭐ 新增
- **translation-card** - 翻译卡（句子翻译、段落翻译、文化语境翻译）⭐ 新增

**核心原则：** 这些模式是不同的路由结果（因为用户说法不同），但它们共享同一套生产契约。

---

## 完整流程

### 阶段 0：Input Type Router

**参考：** [00-input-router.md](00-input-router.md)

识别输入源：
- 单个汉字 → character-card
- 词汇表 → vocabulary-card
- 语法点列表 → grammar-card
- 短语列表 → phrase-card
- 发音练习材料 → pronunciation-card
- 翻译练习文本 → translation-card
- 结构化表格（包含多种类型）

**输出：**
```md
输入源类型：单字 / 词表 / 语法点 / 短语列表
可读取程度：完整 / 部分
短路提示：Output Mode Router 可优先路由到对应 learning-card 类型
下一步：快速 Source Lock
```

---

### 阶段 1：快速 Source Lock

**参考：** [01-source-lock.md](01-source-lock.md)

**简版 Source Lock：**
```md
源类型：单字 / 词表 / 语法点 / 短语列表
目标内容：[具体内容]
主题：学习卡
禁止偏离：不得添加 HSK 或考试标签（除非用户明确要求）
页数：1 或批量数量
```

**注意：** learning-card 可使用快速 Source Lock，但不能完全跳过。

---

### 阶段 2：Output Mode Router

**参考：** [02-output-mode-router.md](02-output-mode-router.md)

**路由逻辑：**

#### 路由到 `character-card`
- 核心对象是单个汉字 ✓
- 需要拼音、英文义项、常用词、例句、记忆点 ✓

#### 路由到 `vocabulary-card`
- 核心对象是词表、单词、搭配 ✓
- 需要发音、释义、例句 ✓

#### 路由到 `grammar-card`
- 核心对象是语法点、句型、用法规则 ✓
- 需要结构、例句、对比、纠错 ✓

#### 路由到 `phrase-card`
- 核心对象是固定短语、常用表达、句块 ✓
- 需要自然用法、场景、例句 ✓

#### 路由到 `pronunciation-card` ⭐ 新增
- 核心对象是音标、发音规则、语调练习 ✓
- 需要音标对比、发音技巧、听力示例 ✓
- 适用场景：音标学习、最小对比对（ship vs sheep）、语调练习、连读规则

#### 路由到 `translation-card` ⭐ 新增
- 核心对象是翻译练习文本 ✓
- 需要原文、译文、翻译技巧、文化注释 ✓
- 适用场景：句子翻译、idiom 翻译、多译法对比、文化语境翻译

**输出：**
```md
输出模式：character-card / vocabulary-card / grammar-card / phrase-card / pronunciation-card / translation-card
选择原因：单字/词表/语法点/短语/发音/翻译
预期卡片数量：1 张 / 批量
使用模板：learning-card-template（共享）
风格建议：童趣（character）/ 简洁专业（其他）
```

---

### 阶段 3：Execution Mode Router

**参考：** [03-execution-mode-router.md](03-execution-mode-router.md)

**判定执行路径：**

#### `direct_image_preview` - 直接生图预览
**适用场景：**
- 单张快速预览
- 验证卡片结构和风格

**劣势：**
- 中文准确性不稳定
- 拼音声调可能错误
- 不适合批量生成

---

#### `engineering_rendering` - 工程化渲染 ⭐⭐⭐ 强烈推荐
**适用场景：**
- 批量生成（多个学习卡）
- 商用发布
- 中文字段必须精确
- 教学场景
- 付费课程材料

**特点：** 
- HTML/CSS 模板渲染
- 保证汉字、拼音、例句准确无误
- 批量生成效率高
- 风格完全一致

**硬规则：** 对于商用、大批量或精确文本输出，必须选择 `engineering_rendering`。

---

#### `prompt_package` - 仅输出提示词包
**适用场景：**
- 无图像生成能力
- 需要交给第三方工具

---

### 阶段 4：Content Analysis

**参考：** [04-content-analysis.md](04-content-analysis.md)

**学习卡信息提取（共享字段）：**

#### 必填字段（所有类型）
- `source_anchor` - 内容来源锚点
- `main_term` - 主要术语或模式
- `pronunciation` - 发音或拼音（如适用）
- `english_meaning` - 英文释义或解释
- `usage_note` - 用法说明
- `example_sentence` - 例句（中文、拼音、英文）
- `forbidden_labels` - 禁止标签（默认不添加 HSK/考试等级）
- `illustration_keywords` - 插图关键词

#### 类型特定字段

**character-card 特有：**
```md
- character: "穿"
- pinyin: "chuān"
- tone_number: 1
- stroke_count: 9
- radical: "穴"
- words: ["穿衣服", "穿鞋", "穿过"]
- memory_cue: "穴下有牙，像衣服的洞要穿过去"
```

**vocabulary-card 特有：**
```md
- word: "serendipity"
- part_of_speech: "noun"
- phonetic: "/ˌserənˈdɪpɪti/"
- synonyms: ["luck", "fortune"]
- collocations: ["by serendipity", "pure serendipity"]
```

**grammar-card 特有：**
```md
- grammar_point: "把字句"
- structure: "主语 + 把 + 宾语 + 动词 + 其他成分"
- usage_rules: ["表示处置", "宾语必须是特指"]
- common_mistakes: ["把我喜欢你 ✗", "我把作业做完了 ✓"]
```

**phrase-card 特有：**
```md
- phrase: "break the ice"
- literal_meaning: "打破冰"
- idiomatic_meaning: "打破僵局、活跃气氛"
- usage_context: "社交场合、会议开始"
```

**pronunciation-card 特有：** ⭐ 新增
```md
- target_sound: "/θ/ vs /ð/"
- phonemes: ["/θ/", "/ð/"]
- minimal_pairs: [{"word1": "think", "word2": "this"}, {"word1": "mouth", "word2": "mouthe"}]
- articulation_guide: "舌尖轻触上齿，/θ/不振动声带，/ð/振动声带"
- audio_url: "pronunciation-th-dh.mp3"
- practice_words: ["think", "this", "mouth", "breathe"]
```

**translation-card 特有：** ⭐ 新增
```md
- source_text: "It's raining cats and dogs."
- source_language: "en"
- target_text: "倾盆大雨。"
- target_language: "zh"
- literal_translation: "（字面）天上在下猫和狗"
- idiomatic_translation: "（意译）倾盆大雨 / 大雨滂沱"
- cultural_note: "英语习语，源于17世纪英国，形容雨势极大"
- translation_variants: ["倾盆大雨", "大雨滂沱", "瓢泼大雨"]
```

---

### 阶段 7：Card Data Fill

**参考：** [07-card-data-fill.md](07-card-data-fill.md)

**使用模板：** `assets/templates/learning-card-template.md`

**填充示例（character-card）：**

```json
{
  "card_type": "character",
  "character": "穿",
  "pinyin": "chuān",
  "tone_number": 1,
  "stroke_count": 9,
  "radical": "穴",
  "english_meanings": ["wear", "put on", "pass through"],
  "words": [
    {"chinese": "穿衣服", "pinyin": "chuān yīfu"},
    {"chinese": "穿鞋", "pinyin": "chuān xié"},
    {"chinese": "穿过", "pinyin": "chuān guò"}
  ],
  "example_sentence": {
    "chinese": "我每天都要穿校服上学。",
    "pinyin": "Wǒ měitiān dōu yào chuān xiàofú shàngxué.",
    "english": "I have to wear a school uniform to school every day."
  },
  "memory_cue": "穴下有牙，像衣服的洞要穿过去",
  "visual": {
    "hint": "小孩穿衣服的场景插图",
    "style": "童趣、贴纸感",
    "color_scheme": {
      "background": "#FFF9E6",
      "primary": "#5DADE2",
      "accent": "#FFD93D"
    }
  },
  "forbidden_labels": {
    "hsk_level": null,
    "exam_level": null
  }
}
```

**硬规则（所有类型）：**
- ✅ 不得添加 HSK 或考试标签（除非用户明确要求）
- ✅ 例句必须适合目标学习者水平
- ✅ 中文、拼音、英文必须准确

---

**填充示例（pronunciation-card）：** ⭐ 新增

```json
{
  "card_type": "pronunciation",
  "target_sound": "/θ/ vs /ð/",
  "phonemes": ["/θ/", "/ð/"],
  "minimal_pairs": [
    {"word1": "think", "ipa1": "/θɪŋk/", "word2": "this", "ipa2": "/ðɪs/"},
    {"word1": "mouth", "ipa1": "/maʊθ/", "word2": "mouthe", "ipa2": "/maʊð/"}
  ],
  "articulation_guide": {
    "chinese": "舌尖轻触上齿，/θ/不振动声带（清音），/ð/振动声带（浊音）",
    "steps": [
      "将舌尖放在上下齿之间",
      "轻轻吹气（/θ/）或振动声带（/ð/）",
      "保持舌头位置不变"
    ]
  },
  "audio_url": "pronunciation-th-dh.mp3",
  "practice_words": [
    {"word": "think", "ipa": "/θɪŋk/", "chinese": "思考"},
    {"word": "this", "ipa": "/ðɪs/", "chinese": "这个"},
    {"word": "breath", "ipa": "/breθ/", "chinese": "呼吸（名词）"},
    {"word": "breathe", "ipa": "/briːð/", "chinese": "呼吸（动词）"}
  ],
  "common_mistakes": [
    {"wrong": "将 /θ/ 发成 /s/", "example": "think → sink"},
    {"wrong": "将 /ð/ 发成 /z/", "example": "this → zis"}
  ],
  "visual": {
    "hint": "舌头位置示意图、音波对比图",
    "style": "简洁专业、教学清晰",
    "color_scheme": {
      "background": "#F8F9FA",
      "primary": "#3498DB",
      "accent": "#E74C3C"
    }
  }
}
```

---

**填充示例（translation-card）：** ⭐ 新增

```json
{
  "card_type": "translation",
  "source_text": "It's raining cats and dogs.",
  "source_language": "en",
  "target_text": "倾盆大雨。",
  "target_language": "zh",
  "literal_translation": "（字面）天上在下猫和狗",
  "idiomatic_translation": "（意译）倾盆大雨",
  "translation_type": "idiom",
  "cultural_note": "英语习语，源于17世纪英国。一种说法是当时屋顶用茅草铺设，暴雨时猫狗会从屋顶掉下；另一说法与北欧神话有关（猫代表雨，狗代表风）。",
  "translation_variants": [
    {"text": "倾盆大雨", "style": "书面语", "usage": "正式场合"},
    {"text": "大雨滂沱", "style": "成语", "usage": "文学表达"},
    {"text": "瓢泼大雨", "style": "口语", "usage": "日常对话"},
    {"text": "雨下得很大", "style": "直译", "usage": "初学者"}
  ],
  "similar_idioms": [
    {"english": "when it rains, it pours", "chinese": "祸不单行 / 福无双至"},
    {"english": "rain or shine", "chinese": "风雨无阻"}
  ],
  "usage_example": {
    "english": "We can't go out now. It's raining cats and dogs!",
    "chinese": "我们现在不能出去，外面倾盆大雨！"
  },
  "visual": {
    "hint": "暴雨场景插图、习语对比图",
    "style": "简洁专业",
    "color_scheme": {
      "background": "#FFFFFF",
      "primary": "#2ECC71",
      "accent": "#F39C12"
    }
  }
}
```

---

**硬规则（所有类型）：**
- ✅ 不得添加 HSK 或考试标签（除非用户明确要求）
- ✅ 例句必须适合目标学习者水平
- ✅ 中文、拼音、英文必须准确
- ✅ pronunciation-card 必须包含清晰的发音指导
- ✅ translation-card 必须区分字面翻译和意译

---

### 阶段 6：Prompt / Render Package

**参考：** [10-prompt-and-render-package.md](10-prompt-and-render-package.md)

#### 如果是 `engineering_rendering`（强烈推荐）

**批量渲染数据包结构：**
```json
{
  "template": "learning-card",
  "batch_info": {
    "total_cards": 50,
    "card_type": "vocabulary",
    "style_anchor": "simple-professional",
    "consistency_rules": {
      "background_color": "#F8F9FA",
      "font_family": "思源黑体",
      "layout_template": "standard"
    }
  },
  "cards": [
    {
      "id": 1,
      "card_type": "vocabulary",
      "word": "serendipity",
      "pronunciation": "/ˌserənˈdɪpɪti/",
      "part_of_speech": "noun",
      "chinese_meaning": "意外发现珍奇事物的本领；有意外收获的运气",
      "english_definition": "the occurrence of events by chance in a happy way",
      "example_sentence": {
        "english": "Finding that book was pure serendipity.",
        "chinese": "找到那本书纯属意外之喜。"
      },
      "visual_hint": "幸运发现宝藏"
    }
    // ... 其他 49 张卡片
  ]
}
```

**使用模板：** 
- `assets/render-engine/html-templates/learning-card.html`（共享模板）
- 根据 `card_type` 自动适配字段布局

---

### 阶段 7：Batch Generation / Rendering

#### 执行路径 A：工程化渲染（强烈推荐）
```
1. 准备批量渲染数据包（JSON）
2. 调用 HTML/CSS 模板
3. 批量渲染所有卡片（1080×1440）
4. 检查准确性：
   - 汉字/单词正确
   - 拼音/音标声调准确
   - 例句语法正确
   - 风格一致
5. 输出 PNG 文件
```

**优势：**
- 文字显示准确
- 拼音/音标声调准确
- 例句排版规范
- 批量生成效率高
- 风格完全统一

---

#### 执行路径 B：直接生图（不推荐批量）
```
1. 逐张使用提示词生成卡片
2. 检查准确性
3. 不合格重新生成
```

**劣势：**
- 汉字/单词可能不准确
- 拼音/音标声调可能错误
- 例句排版可能混乱
- 批量生成效率低
- 风格一致性难保证

---

### 阶段 8：Quality Gate

**质量检查清单（所有类型）：**

#### 内容准确性（核心）
- [ ] 主要术语正确无误
- [ ] 拼音/音标准确含声调
- [ ] 英文释义准确
- [ ] 例句语法正确、适合学习者水平
- [ ] 用法说明合理

#### 教学适用性
- [ ] 没有未经要求的 HSK/考试标签
- [ ] 例句难度适中
- [ ] 词汇选择适合目标水平
- [ ] 说明简单直观

#### 视觉效果
- [ ] 主要内容足够大，清晰可读
- [ ] 拼音/音标声调标注清楚
- [ ] 色彩适合学习场景
- [ ] 整体风格符合卡片类型

#### 批量一致性（批量生成时）
- [ ] 所有卡片背景色一致
- [ ] 字体字号统一
- [ ] 版式规范一致
- [ ] 视觉风格协调

#### 平台规范
- [ ] 画幅 3:4 (1080×1440)
- [ ] 安全区内没有被裁切的内容

---

### 阶段 9：Retry / Production Upgrade

#### 不合格情况处理

**文字/拼音不准确 →** 升级到 `engineering_rendering`

**例句过于复杂 →** 回到阶段 7，简化例句

**风格不适合目标学习者 →** 调整色彩方案和视觉风格

**需要批量生成 →** 必须升级到 `engineering_rendering`

**商用/付费课程 →** 必须使用 `engineering_rendering`

---

## 核心规则

### 硬规则（非协商）
1. **No Source Lock, No Generation** - 即使是单张卡也必须完成快速 Source Lock
2. **Content Fidelity First** - 主要术语、拼音/音标、例句必须准确
3. **Chinese Legibility First** - 中文显示清晰优先
4. **No Unrequested Exam Labels** - 不得添加 HSK 或考试标签（除非用户明确要求）
5. **Engineering Rendering For Production** - 商用、大批量或精确文本必须用工程化渲染

### 推荐实践
- 批量生成必须用 `engineering_rendering`
- 商用/付费课程材料必须用 `engineering_rendering`
- 例句必须适合目标学习者水平
- 视觉风格要符合卡片类型定位
- 保持批量卡片风格一致性
- 不允许把大量中文小字交给图像模型排版

---

## 视觉系统

### 画幅
- 标准：3:4 (1080×1440)

### 风格分类

#### character-card（单字卡）
- **背景：** 浅黄 (#FFF9E6) / 浅蓝 (#E8F4F8) / 浅绿 (#E8F8F5)
- **主色：** 柔和蓝、柔和绿、柔和橙（低饱和度）
- **风格：** 童趣、贴纸感、启蒙友好
- **插图：** 简单场景、卡通风格

#### vocabulary-card / grammar-card / phrase-card
- **背景：** 白色 (#FFFFFF) / 浅灰 (#F8F9FA)
- **主色：** 专业蓝、深灰、强调色
- **风格：** 简洁专业、信息层级清晰
- **插图：** 抽象图标、简洁示意图

---

## 批量生成示例

### 场景：生成 50 个词汇卡（付费课程材料）

**输入：**
```
词汇表：50 个 GRE 高频词汇
目标：付费课程材料
要求：中文释义、例句必须精确
```

**执行流程：**
1. 完成 Source Lock（词表 + 目标学习者水平）
2. 路由到 vocabulary-card
3. 检测：批量 + 商用 + 精确中文 → `engineering_rendering`
4. 对每个单词完成 Content Analysis
5. 准备 50 个卡片的渲染数据包
6. 设置 style_anchor 保证风格一致
7. 批量调用 `engineering_rendering`
8. 逐张质量检查
9. 输出 50 张卡片（1080×1440）

**输出：**
```
vocabulary-card-001-serendipity.png
vocabulary-card-002-ephemeral.png
...
vocabulary-card-050-ubiquitous.png
```

---

## 参考资源

### 模板族（共享）
- [template-families/learning-card/](../template-families/learning-card/)
- [template-families/character-card/](../template-families/character-card/)（character-card 特定视觉）

### 模板文件
- `assets/templates/learning-card-template.md`（共享模板）
- `assets/templates/character-card-template.md`
- `assets/templates/learning-card-prompt-template.md`

### 渲染引擎
- `assets/render-engine/html-templates/learning-card.html`（共享渲染模板）
- `assets/render-engine/css/learning-card.css`

### 配置文件
- [config/risk-action-blacklist.md](../config/risk-action-blacklist.md)
- [config/asset-source-policy.md](../config/asset-source-policy.md)

### Schemas
- `references/schemas/learning-card-schema.md`

---

## 关键差异说明

### learning-card vs knowledge-carousel

| 维度 | learning-card | knowledge-carousel |
|------|---------------|-------------------|
| **目标** | 语言学习、词汇记忆 | 知识讲解、方法论传播 |
| **内容** | 结构化字段（术语、释义、例句） | 连贯叙事（问题、方法、步骤） |
| **风格** | 简洁专业 / 童趣（单字） | 书卷感、编辑感 |
| **批量** | 常见（词表、语法点集） | 较少（单篇内容） |
| **准确性** | 极高（商用教学材料） | 高（内容忠实） |

---

**版本：** 1.0.0  
**最后更新：** 2026-06-16  
**维护：** Content Visual Forge
