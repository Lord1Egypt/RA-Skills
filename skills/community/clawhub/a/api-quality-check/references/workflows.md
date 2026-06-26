# Workflow Notes

Provider names such as Ark/Volcengine, GLM, DeepSeek, Kimi, SiliconFlow, and similar services are examples only. Choose the workflow by endpoint protocol type first: `OpenAI`, `OpenAI-Compatible`, or `Anthropic`.

For a protocol-first overview, read `references/endpoint-types-playbook.md` before using vendor-specific examples.

## Quick smoke test

Use this first when the user wants to know whether an endpoint is even compatible with the detector.

If the user only has raw endpoint details, generate a normalized config file first:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" init-config \
  --provider "OpenAI-Compatible" \
  --base-url "https://api.siliconflow.cn/v1/chat/completions" \
  --api-key "$API_KEY" \
  --model-id "deepseek-ai/DeepSeek-V3.2" \
  --name "siliconflow-v3-2" \
  --config-output ./provider.json
```

Only add vendor-specific `headers` when required. For Kimi coding, use `{"User-Agent":"KimiCLI/2.0.0"}` only when the address is under `https://api.kimi.com/coding`; the OpenAI-compatible Kimi path is `https://api.kimi.com/coding/v1`.

For multiple endpoints, normalize them into one batch file first:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" init-batch-config \
  --configs ./raw-providers.json \
  --config-output ./providers.json
```

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" smoke \
  --provider "OpenAI-Compatible" \
  --base-url "https://ark.cn-beijing.volces.com/api/coding/v3" \
  --api-key "$API_KEY" \
  --model-id "ark-code-latest" \
  --html-output ./smoke.html
```

For OpenAI-compatible endpoints, pasting a full `.../chat/completions` URL is also acceptable. The script will normalize it to the base API root.

Interpretation:

- `b3it_supported=true`: the endpoint can return normal first-token text at `max_tokens=1`
- `lt_supported=true`: the endpoint also returns `logprobs`, so LT-lite can run
- `recommended_detector`: direct next-step recommendation from the script
- `first_token_error` mentioning `reasoning_content` or `thinking`: the script already tried the OpenAI-compatible retry path with `thinking.disabled`; if it still failed, the endpoint is not returning usable normal text

`init-config` notes:

- it normalizes full endpoint URLs back to the API root
- it writes auto-selected `extra_body` into the config file when needed
- `--batch` wraps the generated config in `{"configs":[...]}` for batch workflows

`init-batch-config` notes:

- it accepts either a top-level array or `{"configs":[...]}`
- it normalizes each entry with the same OpenAI-compatible rules as `init-config`
- it preserves `name` when present, otherwise falls back to `model_id`

## Batch smoke test

Use this when the user has multiple providers, multiple coding CLIs, or a matrix of staging/production endpoints.

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" batch-smoke \
  --configs ./providers.json \
  --output ./batch-smoke.json \
  --html-output ./batch-smoke.html
```

Interpretation:

- `total_configs`: how many endpoints were checked
- `b3it_supported_count`: endpoints that can support first-token support-set checks
- `lt_supported_count`: endpoints that also expose `logprobs`
- each item under `results`: per-endpoint capability summary and failure reason

## One-shot batch wrapper

Use this when you want the skill to drive the whole pipeline automatically:

```bash
"$CODEX_HOME/skills/api-quality-check/scripts/run_batch_checks.sh" \
  ./providers.json \
  ./api-quality-out
```

Optional third argument:

```bash
"$CODEX_HOME/skills/api-quality-check/scripts/run_batch_checks.sh" \
  ./providers.json \
  ./api-quality-out \
  ./lt-prompts.json
```

What it does:

- runs `batch-smoke`
- writes `providers.lt-ready.json` and `providers.b3it-ready.json`
- runs batch LT only for LT-ready endpoints
- runs batch B3IT only for B3IT-ready endpoints
- writes both JSON and HTML artifacts to the output directory
- creates `index.html` as the landing page that links smoke, LT, and B3IT reports

## Batch B3IT baseline workflow

Use this when you want to establish baselines for many endpoints in one run.

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" batch-b3it-baseline \
  --configs ./providers.json \
  --output-dir ./b3it-baselines \
  --output ./batch-b3it-baselines.json \
  --html-output ./batch-b3it-baselines.html
```

Interpretation:

- `output_dir`: where per-endpoint baseline JSON files were written
- `success_count`: baselines that were created successfully
- each successful item includes `baseline_file`, which is reused later

## Daily single-endpoint drift workflow

Use this when you want to run one endpoint every day and keep dated artifacts so you can pinpoint when behavior changed.

```bash
bash "$CODEX_HOME/skills/api-quality-check/scripts/run_daily_check.sh" \
  ./provider.json \
  ./daily-out \
  kimi-k2.5
```

What it does:

- runs `smoke` for the current day
- creates LT and B3IT baselines on the first successful run if they do not exist yet
- refreshes older B3IT baselines automatically if they predate the stable-support filtering fields
- reuses the saved baselines on later runs
- writes dated outputs under `daily-out/<label>/runs/YYYY-MM-DD/`
- writes long-lived baselines under `daily-out/<label>/baselines/`
- writes `summary.json`, `index.html`, and `latest-run.txt` for quick review

Interpretation:

- if `summary.json` shows `lt_detect.overall_changed=true`, the logprob behavior drifted versus the saved baseline
- if `summary.json` shows `b3it_detect.overall_changed=true`, the support set for one-token outputs changed versus the saved baseline
- repeated daily runs let you identify the first date on which the endpoint behavior diverged

## Batch B3IT detect workflow

Use the manifest from `batch-b3it-baseline` plus the same provider config list.

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" batch-b3it-detect \
  --configs ./providers.json \
  --baseline-manifest ./batch-b3it-baselines.json \
  --output ./batch-b3it-report.json \
  --html-output ./batch-b3it-report.html
```

Interpretation:

- `changed_count`: endpoints whose stable support sets changed
- each successful item includes an embedded `report`
- items whose baseline creation failed are reported as `skipped`
- defaults are tuned to reduce false positives: `detection-repeats=5`, `min-stable-count=2`, `min-stable-ratio=0.35`, `confirm-passes=1`

## LT-lite workflow

Build a baseline:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" lt-baseline \
  --config ./provider.json \
  --output ./lt-baseline.json \
  --html-output ./lt-baseline.html
```

Detect against the baseline:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" lt-detect \
  --config ./provider.json \
  --baseline ./lt-baseline.json \
  --output ./lt-report.json \
  --html-output ./lt-report.html
```

Use LT-lite only when the smoke check confirms `lt_supported=true`.

## Batch LT workflow

Use this when you have multiple OpenAI/OpenAI-compatible endpoints and want one manifest for later comparison.

Build baselines:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" batch-lt-baseline \
  --configs ./providers.json \
  --output-dir ./lt-baselines \
  --output ./batch-lt-baselines.json \
  --html-output ./batch-lt-baselines.html
```

Run detection:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" batch-lt-detect \
  --configs ./providers.json \
  --baseline-manifest ./batch-lt-baselines.json \
  --output ./batch-lt-report.json \
  --html-output ./batch-lt-report.html
```

Interpretation:

- a config that lacks `logprobs` will fail baseline creation with a clear error
- `changed_count` counts endpoints whose LT permutation test flagged drift
- each successful item includes an embedded `report`

## B3IT-lite workflow

Build a baseline:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" b3it-baseline \
  --config ./provider.json \
  --output ./b3it-baseline.json \
  --html-output ./b3it-baseline.html
```

If an OpenAI/OpenAI-compatible endpoint finds no border inputs with a low-cost search profile, the script will automatically retry with a stronger search profile before giving up. This is useful for endpoints like SiliconFlow where a very small candidate search may miss usable border inputs.

Detect against the baseline:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" b3it-detect \
  --config ./provider.json \
  --baseline ./b3it-baseline.json \
  --output ./b3it-report.json \
  --html-output ./b3it-report.html \
  --detection-repeats 5 \
  --min-stable-count 2 \
  --min-stable-ratio 0.35 \
  --confirm-passes 1
```

Interpretation:

- B3IT now compares stable support sets instead of every one-off token
- increasing `detection-repeats` and requiring `min-stable-count >= 2` reduces false positives from low-frequency outputs
- `confirm-passes=1` means a flagged prompt is rechecked once before it counts as a real change
- if you want a more sensitive detector, lower `min-stable-count` or `min-stable-ratio`

## CLI-specific usage

### Codex / Claude Code / Gemini CLI

Ask the agent to:

- run the `smoke` command first
- decide whether LT-lite, B3IT-lite, or both are available
- only run LT-lite if `logprobs` are actually present
- save artifacts as JSON so the next run can compare against a fixed baseline

### OpenClaw

Use the same script. Keep the interaction file-oriented:

- store provider config in a small JSON file
- store baselines and reports in explicit paths
- avoid GUI assumptions
- treat the smoke output as the capability gate before any heavier run
