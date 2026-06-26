# Security

## Permissions

| Permission | Purpose |
|------------|---------|
| `shell` | Runs `measure.py` for quantitative scoring (regex + spaCy dependency parse). No network calls, no downloads. |

**No `network` permission is requested.** All rewriting is performed by the orchestrating LLM locally. No essay content is sent to external services.

## Data Handling

- All essay processing happens locally within the LLM context.
- No user data is persisted between sessions.
- Pattern weights (`weights.json`) are static corpus-derived statistics bundled with the skill, not user data.
- No remote API calls are made. No environment variables are required.

## Dependencies

- **spaCy `en_core_web_sm`**: Required for syntactic analysis (MDD computation). Must be pre-installed by the user (`python -m spacy download en_core_web_sm`). The skill does **not** auto-download models at runtime.

## Reporting

Report security issues at https://github.com/kevin0818-lxd/essay-humanize-iterator/issues.
