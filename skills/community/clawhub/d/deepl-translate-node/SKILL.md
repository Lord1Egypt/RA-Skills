---
name: deepl-translate-node
description: Translate via DeepL when explicitly requested, or when wording is uncertain and a translation error has material consequences, such as ambiguous legal/medical/technical terms or official names. 用 DeepL 翻译；高风险且存在歧义的翻译。Confident everyday translation can be handled directly.

metadata:
  version: "1.1.14"
  openclaw:
    homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/deepl-translate-node
    emoji: "🔤"
    requires:
      bins: ["node"]
      env: ["DEEPL_API_KEY"]
    primaryEnv: DEEPL_API_KEY
    envVars:
      - name: DEEPL_API_HOST
        required: false
        description: Point at api.deepl.com for a Pro key; the Free host is the default.
    files:
      - translate.mjs
---

# DeepL Translate

Use DeepL when the user requests it, or when wording is uncertain and a translation error has material consequences. Confident everyday prose can be translated directly. Proper names, technical terms, idioms and unfamiliar language pairs are cues to assess uncertainty, not automatic reasons to call the API.

## Configuration and data flow

The helper reads `DEEPL_API_KEY`, sends the supplied text over HTTPS to DeepL, and prints the translation. Use only content authorized for external processing; keep credentials out of the text and command output.

The default host is `api-free.deepl.com`; Pro keys use `DEEPL_API_HOST=api.deepl.com`. If the key is missing, explain how to provide it through the environment. Persistent shell configuration is optional.

```bash
export DEEPL_API_KEY="your-deepl-auth-key-here"
```

```powershell
$env:DEEPL_API_KEY = "your-deepl-auth-key-here"
```

To check configuration, print presence only:

```bash
if [ -n "${DEEPL_API_KEY//[[:space:]]/}" ]; then echo 'DEEPL_API_KEY is set'; else echo 'DEEPL_API_KEY is missing'; fi
```

```powershell
if ([string]::IsNullOrWhiteSpace($env:DEEPL_API_KEY)) { 'DEEPL_API_KEY is missing' } else { 'DEEPL_API_KEY is set' }
```

## Translate

Node 18+ is required. Substitute the installed skill directory and quote its path:

```bash
node "{SKILL_DIR}/translate.mjs" --target ZH-HANS --text "The plaintiff filed a motion to compel discovery."
node "{SKILL_DIR}/translate.mjs" --source JA --target EN-US --text "持分会社"
```

Omit `--source` for auto-detection. Aliases are `-t` for `--text`, and `--target-lang` / `--source-lang` for the language flags. Values accept either a following argument or `=`; use `--text=...` for text beginning with `--`.

Stdout contains only the translation, with paragraphs preserved. Failures print an `ERROR:` on stderr and return nonzero; the request timeout is 60 seconds. Respect shorter task deadlines when needed.

Treat the output as another translation, not independent proof of correctness. If it conflicts with the source context or an official term, resolve the discrepancy or explain the remaining ambiguity.

## Language selection

Use the user's requested locale. Common precise targets include `ZH-HANS`, `ZH-HANT`, `EN-US`, `EN-GB`, `PT-BR` and `PT-PT`.

For other languages or uncertain support, query the configured host's `GET /v3/languages?resource=translate_text` with the `Authorization: DeepL-Auth-Key <key>` header. The `resource` parameter is required; entries distinguish `usable_as_source` and `usable_as_target`. The endpoint returns BCP 47 codes, while the helper also accepts uppercase forms. Text translation uses `/v2/translate`.

A static list or documentation example may omit accepted targets. Check the live response and, when needed for the requested translation, the translate API's result rather than declaring a language unsupported from an old list. Branch on HTTP status, not exact error wording. See [supported languages](https://developers.deepl.com/docs/resources/supported-languages).

## Terminology consistency

Optional `--glossary 'term=translation;term=translation'` performs literal, case-sensitive substring replacement over **DeepL's output**. For example, `API=接口` also changes `APIs`. Use unambiguous terms; terms cannot contain `;`. A pair without `=` is skipped with a warning on stderr. This is not DeepL's Glossary API.

## Errors

- `403`: check the key, host and endpoint permission scope.
- `456`: inspect the account's usage, Cost Control or key-level limit; the applicable limit depends on the account.
- Unsupported language: inspect the API error and requested direction/variant.
- Timeout or connection failure: inspect connectivity and service availability before retrying.
