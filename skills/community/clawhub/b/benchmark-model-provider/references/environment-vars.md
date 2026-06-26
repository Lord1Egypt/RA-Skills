# Environment Variables and Dependencies

## Environment variables

### Required in real benchmark runs
- `BENCHMARK_API_KEY` — API key for the benchmark provider, when the target endpoint requires authentication

### Optional
- `BENCHMARK_BASE_URL` — fallback OpenAI-compatible base URL if the spec does not provide one
- `VERCEL_TOKEN` — token for non-interactive Vercel publishing when using `publish_report.py`

## Python dependencies
- `PyYAML`
- `reportlab`

## External tooling
- `npx vercel` is required only when the user explicitly chooses Vercel publishing

## Design rule
- Do not inject real secrets into example files.
- Prefer placeholder values in examples and references.
