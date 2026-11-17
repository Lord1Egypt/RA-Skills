# Internationalization Contract

design-guide separates language used to instruct an AIDE from language used by its command-line helpers.

## Supported locales

The supported locales are:

- `en` - English (fallback locale)
- `zh-CN` - Simplified Chinese

Unknown or unsupported values fall back to `en`. New locales must add a complete catalog under `locales/` and pass the catalog parity test before release.

## Locale resolution

CLI helpers resolve the locale in this order:

1. Explicit `--locale en` or `--locale zh-CN`.
2. `F_DESIGN_LOCALE`.
3. `LC_ALL`.
4. `LANG`.
5. English fallback.

The shell synchronizer accepts the same environment variables and also supports `bash scripts/sync-aide.sh --locale zh-CN`. `detect-frontend-env.sh` intentionally keeps its structured Markdown keys in English because its output is consumed as project context by agents.

The user-facing response language should follow the language of the current user request unless the user explicitly requests another language. A local preference may document a default, but it must not override an explicit request.

## Output stability

Human-readable help, status, and error messages may be localized. JSON output is an API surface: field names, enum values, and machine-readable structure remain in English. Human-readable error strings nested inside JSON may remain English for stable parsing; consumers should use the structured fields for decisions.

## Adding messages

Add the English source string and the same key to every supported catalog. Use `scripts/i18n.py` from CLI helpers instead of embedding a second translation mechanism. Missing translations intentionally fall back to the English source string.

## Verification

Run:

```bash
python3 -m unittest discover -s tests -q
python3 scripts/present-design.py --locale zh-CN --help
F_DESIGN_LOCALE=zh-CN python3 scripts/design-guide-doctor.py
```

Do not use locale-dependent text as a contract identifier, fixture key, JSON field name, route, selector, or filesystem path.
