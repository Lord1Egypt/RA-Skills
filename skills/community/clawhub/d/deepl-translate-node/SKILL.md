---
name: deepl-translate-node
version: 1.1.1
description: Use DeepL's neural MT API as a fallback when you are NOT confident in your own translation — proper nouns, ambiguous phrasing, domain/legal/medical terminology, idioms, low-resource languages, or any text where a mistranslation carries real cost. Also use when the user explicitly asks to "用 DeepL 翻译" / "translate with DeepL". Calls the DeepL API (Free tier by default; Pro via DEEPL_API_HOST).
metadata:
  clawdbot:
    emoji: "🔤"
    requires:
      bins: ["node"]
    files:
      - translate.mjs
---

# DeepL Translate (confidence-gated fallback)

A thin wrapper around the DeepL API. The point of this skill is the
**trigger logic**, not the API call: translate with DeepL when your own translation
might be wrong and being wrong matters.

## When to reach for DeepL instead of translating yourself

Translate it yourself when the text is everyday prose and you are confident. Call
DeepL when **any** of these is true:

- **Proper nouns / brand / product names** that have official localized forms
- **Domain terminology** — legal, medical, financial, technical specs, patents
- **Ambiguous source** where one word maps to several target words and context
  doesn't disambiguate
- **Idioms / fixed expressions** that don't translate literally
- **Low-resource or distant language pairs** where your training signal is thin
- **High-stakes output** — anything the user will publish, sign, or send to a
  third party, where a subtle error is costly
- The user **explicitly asks** for DeepL.

If you're confident and the cost of a minor error is low, just translate directly —
don't burn an API call.

## Prerequisite: API key

The key is read from the `DEEPL_API_KEY` environment variable (never hardcode it).
Default endpoint is the **Free** tier host `api-free.deepl.com`; for Pro, set
`DEEPL_API_HOST=api.deepl.com`.

Set it once:

```bash
# macOS / Linux — add to ~/.bashrc or ~/.zshrc to persist
export DEEPL_API_KEY="your-deepl-auth-key-here"
```

```powershell
# Windows (persistent, user scope) — then open a NEW shell
setx DEEPL_API_KEY "your-deepl-auth-key-here"
```

Verify in a fresh shell: `echo $DEEPL_API_KEY` (bash) / `$env:DEEPL_API_KEY` (PowerShell).

If `DEEPL_API_KEY` is unset, stop and tell the user to set it — do not invent a key.

## How to call it

Use the bundled Node helper (cross-platform, Node 18+). `--source` is optional;
omit it to let DeepL auto-detect.

### Language codes (DeepL next-gen model — broad coverage)

DeepL supports far more than the classic ~30 languages. Don't assume a language is
unsupported — check before falling back to a self-translation.

- **Core (source + target):** `AR BG CS DA DE EL EN ES ET FI FR HU ID IT JA KO LT
  LV NB NL PL PT RO RU SK SL SV TR UK ZH`
- **Extended (~100 languages, incl. many low-resource ones):** `AF BN FA HE HI HR
  HY KA ML MR MS MY NE PA SW TA TE TH UR VI YUE ZU` … and many more.
- **Target-only regional variants — prefer these when precision matters:**
  - Chinese: `ZH-HANS` (Simplified), `ZH-HANT` (Traditional) — better than bare `ZH`
  - English: `EN-US`, `EN-GB`
  - Portuguese: `PT-BR`, `PT-PT`
  - Spanish: `ES-419` (Latin American)
  - `FR-CA` (Canadian French, beta), `DE-CH` (Swiss German, beta) — beta = not billed

For the authoritative, always-current list, query the API. Use the **v3** languages
endpoint (recommended for new integrations; replaces `/v2/languages`). The `resource`
query parameter is **required** — omitting it returns 400:
`GET https://api-free.deepl.com/v3/languages?resource=translate_text` with the
`Authorization: DeepL-Auth-Key <key>` header. Valid `resource` values:
`translate_text`, `translate_document`, `voice`, `write`, `glossary`, `style_rules`.
It returns one entry per language (100+ for `translate_text`) with source/target
support flags. Or see
https://developers.deepl.com/docs/getting-started/supported-languages

**Code-format caveat:** `/v3/languages` returns **BCP 47** codes (`en-US`, `pt-BR`,
`zh-Hant` — lowercase base, uppercase region, title-case script). But the
**translation** endpoint is still **`/v2/translate`**, whose `target_lang` accepts the
v2-style UPPERCASE codes (`EN-US`, `PT-BR`, `ZH-HANT`). Don't mix the two casings when
feeding a value from the languages endpoint into a translate call.

**Versioning note:** Only glossaries and the languages list have moved to v3. Text
translation has **no v3 endpoint** — `/v2/translate` is current and not deprecated.

```bash
node "{SKILL_DIR}/translate.mjs" --target ZH \
    --text "The plaintiff filed a motion to compel discovery."
```

With an explicit source language:

```bash
node "{SKILL_DIR}/translate.mjs" --source JA --target EN-US --text "持分会社"
```

The script prints **only the translated text** on success, or an error line
(prefixed `ERROR:`) on failure. Multiple lines / paragraphs are preserved.

## Workflow inside a task

1. You're translating something and hit a passage you're unsure about.
2. Confirm `DEEPL_API_KEY` is set (the script checks and errors clearly if not).
3. Run `translate.mjs` for the uncertain passage (or the whole text).
4. Use DeepL's output. If it conflicts with your own read, surface both to the
   user and explain the discrepancy rather than silently picking one.

## Glossary / terminology consistency (optional)

For repeated terminology, pass `--glossary` as a `term=translation;term=translation`
list and the script will post-process exact matches after DeepL returns. For real
glossary support DeepL has a Glossary API; ask the user if they need it and we can
extend the script.

## Notes

- Free tier: 500,000 chars/month. The script does not track quota; if you get a
  `456` response that means quota exhausted.
- `403` means a bad/missing key.
- For DeepL **Pro**, set `DEEPL_API_HOST=api.deepl.com` (default is `api-free.deepl.com`).
