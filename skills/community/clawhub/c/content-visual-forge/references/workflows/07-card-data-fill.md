# Workflow 07 · Card Data Fill

当输出模式为 `character-card`、`vocabulary-card`、`grammar-card` 或 `phrase-card` 时，必须先填充结构化字段，再进入生图或工程化渲染。

## character-card 字段清单

- character
- pinyin
- meaning_en
- level_tag_optional
- common_words[]
- example_sentence_zh
- example_sentence_pinyin
- example_sentence_en
- useful_phrase_zh
- useful_phrase_pinyin
- useful_phrase_en
- memory_tip_en
- illustration_keywords[]

## 规则

1. 拼音统一带声调。
2. 英文释义简洁、自然、初学者友好。
3. 常用词默认 3 个左右。
4. 例句必须自然、常用、可教学。
5. Useful Phrase 要和主字直接相关。
6. Memory Tip 必须帮助记忆字义或使用场景。
7. 默认不在具体内容里写考试名称或考试标签。

## 输出格式

建议输出为一个 YAML 或 JSON 风格的字段块，便于后续模板渲染。

## vocabulary-card / grammar-card / phrase-card 字段清单

使用 `references/schemas/learning-card-schema.md` 与 `assets/templates/learning-card-template.md`。

### 共同字段

- card_type
- item_id
- source_anchor
- display_term
- pinyin_or_pronunciation
- meaning_en
- usage_note
- example_sentence_zh
- example_sentence_pinyin
- example_sentence_en
- learner_level_optional
- forbidden_labels[]
- illustration_keywords[]

### 模式专项字段

- `vocabulary-card`：word_zh、word_pinyin、part_of_speech、collocations[]
- `grammar-card`：grammar_point、structure_pattern、common_mistake、correction_tip
- `phrase-card`：phrase_zh、phrase_pinyin、literal_meaning、natural_usage

## 学习卡规则

1. 批量卡必须先定义 batch_id、card_index、total_cards 与 style_anchor。
2. 商用、批量或中文字段必须精确时，优先进入 `engineering_rendering`。
3. 默认不填入 HSK、CEFR、考试、年级、课程标签。
4. 例句可以作为教学例句生成，但必须标注为 teaching example，不得伪装成原文事实。
