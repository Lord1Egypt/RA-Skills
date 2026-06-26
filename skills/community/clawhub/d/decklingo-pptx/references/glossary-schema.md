# Glossary Schema

Use a JSON object with up to three layers:

```json
{
  "default": {
    "源术语": "Preferred translation used for all target languages unless overridden"
  },
  "en": {
    "源术语": "Preferred English translation"
  },
  "ja": {
    "源术语": "Preferred Japanese translation"
  }
}
```

Rules:

- `default` applies to every target language unless a language-specific override exists.
- Language keys should match the `--target-lang` value when possible.
- Keys are matched exactly after paragraph normalization.
- Use the glossary for repeated domain terms, names of assays, product labels, and presentation titles.
- Keep values short and presentation-ready.

When a full paragraph must stay fixed, you may store the full paragraph as the key and the preferred translated paragraph as the value.
