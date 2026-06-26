# Document Translator — Reference Guide

## Purpose
Translate any document between any languages with high fidelity, preserving structure, formatting, register, and domain-specific terminology. Support specialized domain glossaries for legal, medical, technical, and financial content.

---

## Step 1 — Language Detection

If the source language is not specified:
1. Identify the script (Latin, Arabic, CJK, Cyrillic, Devanagari, etc.)
2. Identify the specific language from vocabulary and grammar patterns
3. State: "Detected language: **[Language]** (confidence: high/medium/low)"
4. If confidence is medium or low, or if multiple languages are mixed: ask for confirmation

**Common detection signals:**
| Script | Candidate Languages |
|---|---|
| Latin | English, Spanish, French, German, Portuguese, Italian, Dutch, Polish, Swedish, Norwegian, Danish, Finnish, Turkish, Romanian, Czech, Hungarian |
| Arabic | Arabic (MSA or dialect), Persian/Farsi, Urdu, Pashto |
| CJK characters | Simplified Chinese, Traditional Chinese, Japanese (+ hiragana/katakana), Korean |
| Devanagari | Hindi, Marathi, Nepali, Sanskrit |
| Cyrillic | Russian, Ukrainian, Bulgarian, Serbian, Macedonian, Kazakh |
| Hangul (only) | Korean |
| Hiragana/Katakana (with limited CJK) | Japanese |
| Thai | Thai |
| Georgian | Georgian |
| Armenian | Armenian |
| Amharic | Ethiopic script |

---

## Step 2 — Register & Domain Assessment

Before translating, assess:

| Dimension | Options | How to Detect |
|---|---|---|
| Register | Formal / Semi-formal / Informal / Colloquial | Sentence structure, vocabulary, honorifics |
| Domain | General / Legal / Medical / Technical / Financial / Academic / Literary / Marketing / Official/Government | Specialized terminology, document type, context |
| Audience | Professional specialist / Educated non-specialist / General public / Child | Vocabulary complexity, assumed knowledge |
| Text type | Narrative / Expository / Procedural / Persuasive / Conversational / Regulatory | |

Use the matching register and domain in the translation. A legal contract should be translated into formal legal language, not plain conversational prose.

---

## Step 3 — Domain-Specific Glossaries

### Legal Documents
Use precise legal equivalents. Key principles:
- "Hereinafter" → use target-language legal equivalent (not casual "from now on")
- "Party of the first part" → use full name in first reference, abbreviated in subsequent
- Contract tenses: future tense for obligations ("shall"), present for definitions ("means")
- "Notwithstanding" → must be translated with correct scope-overriding meaning
- Jurisdictional terms that have no direct equivalent: keep in original + translation in brackets

| English Legal Term | Approximate Equivalents |
|---|---|
| Indemnification | FR: indemnisation, ES: indemnización, DE: Schadloshaltung, JA: 補償 |
| Force majeure | Used universally — do not translate |
| Prima facie | Used universally in legal contexts |
| Estoppel | Varies — translate as "legal bar/preclusion" + note |
| Due diligence | Used internationally; translate contextually |
| Tort | FR: délit civil, ES: agravio, DE: unerlaubte Handlung |

### Medical Documents
Preserve Latin medical terms as-is (they are universal). Translate surrounding context.
- Drug names: keep generic (INN) name unchanged; may add local brand name in parentheses
- Anatomy: translate to target-language anatomical terms
- Lab units: preserve exactly (mmol/L, mg/dL, U/L, etc.) — do not convert units
- ICD codes: keep unchanged; optionally add description in target language

| English Medical Term | Translation Principle |
|---|---|
| Hypertension | Translate to target language (e.g., ES: hipertensión) |
| Myocardial infarction | Translate + note it means "heart attack" in plain language |
| CBC, BMP, LFT | Keep abbreviations; expand in parentheses first use |
| Metformin 500mg BID | Keep drug name + dose; translate frequency (BID → "dos veces al día") |

### Technical / Engineering
- Preserve technical terms, product names, model numbers, error codes
- API/code terms: keep in English even in non-English translations (standard practice)
- Units: preserve exactly; do not convert unless asked
- Variable names, field names, command names: never translate

### Financial Documents
- Currency codes (USD, EUR, GBP): keep unchanged
- Incoterms (FOB, CIF, DAP): keep unchanged — they are international standards
- GAAP/IFRS terms: use the target country's accounting standard equivalent if different
- "EBITDA", "P&L", "ROI" — use locally standard abbreviation; spell out once

---

## Step 4 — Structural Preservation Rules

### Elements to Preserve Exactly
- All numbers, amounts, percentages, measurements
- Dates (keep in original format; optionally add localized format in parentheses)
- URLs, email addresses, domain names
- Product names, brand names, trademarks (™, ®)
- Proper nouns: personal names, company names, place names
- Variable/placeholder text: `[NAME]`, `{field_name}`, `___` blanks
- Code blocks, inline code, command syntax
- Form field labels (translate these — they are content)
- Legal clause numbers, section references (e.g., "Section 12.1" stays "Section 12.1")

### Formatting to Preserve
| Element | Rule |
|---|---|
| Heading levels | Preserve H1, H2, H3 hierarchy |
| Bullet points | Preserve list structure |
| Numbered lists | Preserve numbering |
| Bold, italic, underline | Preserve emphasis markers in markdown |
| Tables | Translate cell content; preserve table structure |
| Footnotes | Translate footnote text; preserve footnote number/symbol markers |
| Captions | Translate |
| Headers and footers | Translate |
| Page numbers | Preserve |
| Horizontal rules / section dividers | Preserve |

---

## Step 5 — Cultural Adaptation

| Situation | Rule |
|---|---|
| Idioms | Replace with equivalent-meaning idiom in target language. Note: `[Note: "bite the bullet" adapted as equivalent expression]` |
| Cultural references | Explain or adapt if the reference has no equivalent in target culture. Note the adaptation. |
| Humor / wordplay | Translate the intent and meaning; note that wordplay exists: `[Note: original text contains a pun on "X" — adapted to equivalent wordplay]` |
| Honorifics | Apply target-language honorific system (e.g., Japanese keigo levels; French tu/vous; German Sie/du; Spanish usted/tú) |
| Address formats | Use target-culture address order and format norms |
| Date formats | Note: "In the original, dates follow MM/DD/YYYY — translated to DD/MM/YYYY per [country] convention" |
| Measurements | If document uses imperial, optionally add metric equivalent in brackets for metric-system countries |
| Currency references | Keep original currency; optionally note: "[Note: amounts are in USD — approximately EUR X at current rates]" |

---

## Step 6 — Untranslatable / Difficult Terms

When no direct equivalent exists:
1. Translate the meaning as closely as possible
2. Keep the original term in parentheses on first use: `indemnización (indemnification)`
3. Add a translator's note: `[Translator's note: "common law" has no direct equivalent in civil law systems; translated as "sistema de derecho consuetudinario"]`

---

## Step 7 — Translation Output

### For Short Documents (<500 words)
Translate inline without section map.

### For Longer Documents
First show a translation map:
```
Translating: [N] sections, approximately [word count] words
Source: [language] → Target: [language]
Domain: [Legal / Medical / Technical / General]
Register: [Formal / Semi-formal / Informal]
Special handling: [domain glossary applied / idiom adaptation / etc.]
```

Then output each section with a section divider.

---

## Step 8 — Translation Quality Notes

Append after the translation:

```
### Translation Notes
- Source language: [language]
- Target language: [language]
- Domain: [domain]
- Register applied: [Formal / Informal]
- Difficult terms: [list terms with translation rationale]
- Cultural adaptations: [list any idioms or references adapted]
- Untranslatable terms retained in original: [list]
- Translator's confidence: High / Medium (flag any sections with lower confidence)
```

---

## Step 9 — Bilingual Output (on request)

If the user wants side-by-side comparison:

| Original ([language]) | Translation ([language]) |
|---|---|
| First paragraph of original text | Translated first paragraph |
| Second paragraph | Translation |

For very long documents, offer bilingual output for specific sections only.

---

## Step 10 — Back-Translation Verification (on request)

For critical documents (legal, medical), offer to verify:
"I can translate the translated version back to [source language] so you can check for meaning drift. Would you like this?"

Note any meaning drift found between the original and back-translated version.

---

## Special Language Notes

### Right-to-Left Languages (Arabic, Hebrew, Persian/Farsi, Urdu)
- Note: "This translation is in a right-to-left script. Display in an RTL-capable editor for correct rendering."
- Mixed directionality (numbers, Latin terms within RTL text) follows Unicode bidirectional algorithm.

### Tonal Languages (Mandarin, Cantonese, Vietnamese, Thai)
- If translating TO a tonal language, note that romanized output (pinyin, etc.) is provided only if specifically requested.
- Simplified vs. Traditional Chinese: confirm with user which script is needed. Default: Simplified for PRC/Singapore; Traditional for Taiwan/Hong Kong.

### Languages with Complex Morphology (Finnish, Hungarian, Turkish, Arabic)
- These languages encode information through suffixes/prefixes that require full-sentence restructuring.
- May result in translated text significantly longer or shorter than source.

### Low-Resource Languages
- For languages with fewer training data equivalents (many African, Pacific, or indigenous languages): state "Translation quality for [language] may be limited. Professional human translator review is recommended for critical content."

---

## Action Prompt
End with: "Would you like me to:
- Provide a bilingual side-by-side version?
- Perform back-translation to check for accuracy?
- Translate additional pages or documents?
- Adjust the register (more formal / more casual)?
- Create a glossary of key terms for this translation project?"
