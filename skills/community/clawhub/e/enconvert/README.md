# EnConvert skill for OpenClaw

An [OpenClaw](https://openclaw.ai) skill that lets an agent read the web and convert files
through [EnConvert](https://www.enconvert.com) — clean markdown, structured JSON, screenshots,
and PDFs, each web read carrying a **`render_quality`** honesty score (0.0-1.0). A detected
content-free block is a normal `200` with `is_blocked: true`, empty `outputs` and `billed: false`.

The skill wraps six operations against `https://api.enconvert.com`:

| Operation | Endpoint |
|-----------|----------|
| Perceive URL | `POST /v2/perceive` |
| Web Search | `POST /v2/lookup` |
| Discover URLs | `POST /v2/discover` |
| Extract Structured | `POST /v2/distill` |
| Convert File to Markdown | `POST /v1/convert/anything-to-markdown` |
| Convert File to PDF | `POST /v1/convert/anything-to-pdf` |

## Setup

Set one secret — a **private** API key (`sk_...`) from
[your dashboard](https://www.enconvert.com/dashboard/api-keys):

```bash
ENCONVERT_API_KEY=sk_...
```

Public `pk_` keys are rejected. The skill reads the key from the `ENCONVERT_API_KEY` secret
and never hardcodes it. Full agent-facing instructions and examples live in
[`SKILL.md`](SKILL.md); `scripts/convert.sh` is a small curl helper for the file-convert flow.

## Publishing

```bash
npx clawhub@latest login
npx clawhub@latest publish . --slug enconvert --name "EnConvert" --version 0.0.2 --changelog "Blocked-read contract: is_blocked, billed, render_quality floor"
```

`--version` must match `version:` in `SKILL.md`. Add `--dry-run` to preview first.

## Licence

[MIT](LICENSE)
