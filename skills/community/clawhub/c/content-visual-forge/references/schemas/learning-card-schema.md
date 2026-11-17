# Learning Card Schema

```yaml
card_type: "vocabulary-card | grammar-card | phrase-card"
item_id: ""
source_anchor: ""
display_term: ""
pinyin_or_pronunciation: ""
meaning_en: ""
usage_note: ""
example_sentence_zh: ""
example_sentence_pinyin: ""
example_sentence_en: ""
learner_level_optional: ""
forbidden_labels:
  - ""
illustration_keywords:
  - ""
mode_specific_fields:
  vocabulary:
    word_zh: ""
    word_pinyin: ""
    part_of_speech: ""
    collocations:
      - zh: ""
        pinyin: ""
        en: ""
  grammar:
    grammar_point: ""
    structure_pattern: ""
    common_mistake: ""
    correction_tip: ""
  phrase:
    phrase_zh: ""
    phrase_pinyin: ""
    literal_meaning: ""
    natural_usage: ""
batch:
  batch_id: ""
  card_index: 1
  total_cards: 1
  style_anchor: ""
  render_mode: ""
```

## Rules

- `learner_level_optional` must stay empty unless the user explicitly asks for a level or exam label.
- Every example sentence must be source-grounded or clearly marked as a teaching example.
- Batch cards must keep the same `style_anchor`.
