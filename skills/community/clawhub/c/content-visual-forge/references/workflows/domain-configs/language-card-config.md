# Language Card 领域配置

> **本文件定义语言学习卡的差异化内容。**
> 
> 完整流程请参考：[base-card-workflow.md](../base-card-workflow.md)

---

## 领域定位

**覆盖范围：** 单字、词汇、语法、短语、发音、翻译等语言学习内容

**不覆盖：** 数学公式、编程代码、历史时间线等非语言学习内容

---

## 扩展点 #1：输入路由规则

```md
- 单个汉字 → character-card
- 词汇表 → vocabulary-card
- 语法点列表 → grammar-card
- 短语列表 → phrase-card
- 发音练习材料 → pronunciation-card
- 翻译练习文本 → translation-card
```

---

## 扩展点 #2：Source Lock 要求

**禁止偏离约束：**
- 不得添加 HSK 或考试标签（除非用户明确要求）
- 例句必须适合目标学习者水平

---

## 扩展点 #3：输出模式

支持 6 种卡片类型：
- `character-card` - 单字学习卡
- `vocabulary-card` - 词汇卡
- `grammar-card` - 语法卡
- `phrase-card` - 短语卡
- `pronunciation-card` - 发音卡
- `translation-card` - 翻译卡

---

## 扩展点 #4：执行模式偏好

- 单张预览：`direct_image_preview` 可用
- 批量生成：必须 `engineering_rendering`
- 商用场景：必须 `engineering_rendering`

---

## 扩展点 #5：内容字段

### Character-card 特有字段
```json
{
  "character": "穿",
  "pinyin": "chuān",
  "tone_number": 1,
  "stroke_count": 9,
  "radical": "穴",
  "english_meanings": ["wear", "put on"],
  "words": [...]
}
```

### Vocabulary-card 特有字段
```json
{
  "word": "serendipity",
  "phonetic": "/ˌserənˈdɪpɪti/",
  "part_of_speech": "noun",
  "definition": "...",
  "synonyms": [...]
}
```

### Pronunciation-card 特有字段
```json
{
  "target_sound": "/θ/ vs /ð/",
  "phonemes": ["/θ/", "/ð/"],
  "minimal_pairs": [...],
  "articulation_guide": "..."
}
```

### Translation-card 特有字段
```json
{
  "source_text": "It's raining cats and dogs.",
  "literal_translation": "（字面）...",
  "idiomatic_translation": "（意译）...",
  "cultural_note": "..."
}
```

完整字段定义见：[language-card-workflow.md](../language-card-workflow.md) 阶段 4

---

## 扩展点 #6：视觉导演规则

不适用（language-card 不使用视觉导演系统）

---

## 扩展点 #7：渲染包结构

使用模板：`learning-card-template`

```json
{
  "template": "learning-card",
  "batch_info": {
    "total_cards": 数量,
    "card_type": "vocabulary|character|grammar|phrase|pronunciation|translation",
    "style_anchor": "simple-professional | childlike"
  },
  "cards": [...]
}
```

---

## 扩展点 #8：质量标准

### 语言学习卡特有标准
- [ ] 拼音/音标声调准确
- [ ] 例句语法正确
- [ ] 词汇选择适合目标水平
- [ ] 没有未经要求的 HSK/考试标签

---

## 扩展点 #9：领域硬规则

### Language Card 特定硬规则
1. **No Unrequested Exam Labels** - 不得添加 HSK 或考试标签（除非用户明确要求）
2. **Pronunciation Accuracy** - pronunciation-card 必须包含清晰的发音指导
3. **Translation Distinction** - translation-card 必须区分字面翻译和意译

---

## 视觉系统

### Character-card 风格
- 背景：浅黄/浅蓝/浅绿
- 主色：柔和色调（低饱和度）
- 风格：童趣、贴纸感、启蒙友好

### 其他类型风格
- 背景：白色/浅灰
- 主色：专业蓝、深灰
- 风格：简洁专业、信息层级清晰

---

**配置版本：** 1.0.0  
**对应 base-card-workflow 版本：** 1.0.0
