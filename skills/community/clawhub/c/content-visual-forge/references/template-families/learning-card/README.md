# Template Family · learning-card

`learning-card` is the shared executable family behind:

- `vocabulary-card`
- `grammar-card`
- `phrase-card`

These modes are separate routing outcomes because users ask for them differently, but they share one production contract.

## When To Use

- `vocabulary-card`: word lists, single words, collocations, pronunciation and meaning cards
- `grammar-card`: grammar points, sentence patterns, correction cards, usage rules
- `phrase-card`: fixed phrases, common expressions, sentence chunks, natural usage cards

## Required Data

All learning-card modes must include:

- source anchor
- main term or pattern
- pronunciation or pinyin when applicable
- English meaning or explanation
- usage note
- example sentence in Chinese, pinyin, and English
- forbidden labels
- illustration keywords

## Production Rule

For commercial, large-batch, or exact-text output, choose `engineering_rendering`.
For quick drafts, `direct_image_preview` or `prompt_package` is allowed, but the result must be labeled as preview quality.

