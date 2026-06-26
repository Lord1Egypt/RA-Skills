---
name: api-quality-check
description: Check coding-model API quality, capability fit, and drift with LT-lite and B3IT-lite. Use when Codex needs to verify whether an OpenAI/OpenAI-compatible/Anthropic endpoint can support first-token detection, logprob tracking, baseline-vs-current drift checks, or headless API quality smoke tests for coding CLIs, terminal agents, and OpenClaw-style workflows.
---

# API Quality Check

Use the bundled script to run headless API-quality checks. Treat this skill as script-first: do not recreate LT-lite/B3IT-lite logic inline unless the script is clearly insufficient.

Provider names such as Ark/Volcengine, GLM, DeepSeek, Kimi, SiliconFlow, and similar services are examples only. The primary decision is the endpoint protocol type: `OpenAI`, `OpenAI-Compatible`, or `Anthropic`.

## Quick start

Set the path once:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export APIQ="$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py"
export APIQ_BATCH="$CODEX_HOME/skills/api-quality-check/scripts/run_batch_checks.sh"
export APIQ_DAILY="$CODEX_HOME/skills/api-quality-check/scripts/run_daily_check.sh"
```

Run a capability smoke test first:

```bash
python "$APIQ" smoke \
  --provider "OpenAI-Compatible" \
  --base-url "https://ark.cn-beijing.volces.com/api/coding/v3" \
  --api-key "$API_KEY" \
  --model-id "ark-code-latest" \
  --html-output ./smoke.html
```

For many OpenAI-compatible endpoints, the same command also works if the user pastes the full `.../chat/completions` URL. The script will normalize it back to the API root automatically.

If you want a ready-to-run `provider.json` first, generate it with:

```bash
python "$APIQ" init-config \
  --provider "OpenAI-Compatible" \
  --base-url "https://api.siliconflow.cn/v1/chat/completions" \
  --api-key "$API_KEY" \
  --model-id "deepseek-ai/DeepSeek-V3.2" \
  --name "siliconflow-v3-2" \
  --config-output ./provider.json
```

If an endpoint requires client-specific headers, put them in the config JSON as a `headers` object or pass them with `--headers-json`. For Kimi coding endpoints, use `{"User-Agent":"KimiCLI/2.0.0"}` only when the address is under `https://api.kimi.com/coding`; for the OpenAI-compatible Kimi path, use `https://api.kimi.com/coding/v1`.

If you already have multiple raw endpoint entries, normalize them into `providers.json` with:

```bash
python "$APIQ" init-batch-config \
  --configs ./raw-providers.json \
  --config-output ./providers.json
```

Or run the full batch pipeline:

```bash
"$APIQ_BATCH" ./providers.json ./api-quality-out
```

That command also creates `./api-quality-out/index.html` as the landing page for all generated reports.

For one endpoint that you want to check every day and archive by date:

```bash
bash "$APIQ_DAILY" ./provider.json ./daily-out my-endpoint
```

## Workflow

1. Run `smoke` before any baseline or detect run.
2. If you have many endpoints, run `batch-smoke` with a config list before choosing which ones deserve deeper LT/B3IT work.
3. Read the result:
   - `b3it_supported=true`: the endpoint can return normal first-token text at `max_tokens=1`
   - `lt_supported=true`: the endpoint also returns `logprobs`, so LT-lite can run
   - `recommended_detector`: the script's direct recommendation for the next step
4. If `lt_supported=false`, do not force LT-lite; pivot to B3IT-lite or report that LT is unavailable.
5. Save baselines to explicit JSON files and reuse them for later detection.
6. Keep outputs file-based for coding CLIs and OpenClaw. Do not depend on GUI state.
7. For noisy endpoints, prefer the built-in B3IT defaults before tightening or loosening thresholds manually.

## Endpoint Types

- `OpenAI`: use this for official OpenAI-style endpoints.
- `OpenAI-Compatible`: use this for third-party endpoints that follow OpenAI request and response shapes; vendor-specific headers may be required.
- `Anthropic`: use this for `/v1/messages` style endpoints; in this skill it is `B3IT-only`.

## Commands

### Capability smoke

```bash
python "$APIQ" smoke --config ./provider.json --output ./smoke.json
```

### Generate a provider config template

```bash
python "$APIQ" init-config \
  --provider "OpenAI-Compatible" \
  --base-url "https://api.siliconflow.cn/v1/chat/completions" \
  --api-key "$API_KEY" \
  --model-id "deepseek-ai/DeepSeek-V3.2" \
  --config-output ./provider.json
```

### Generate a batch providers.json template

```bash
python "$APIQ" init-batch-config \
  --configs ./raw-providers.json \
  --config-output ./providers.json
```

### Batch capability smoke

```bash
python "$APIQ" batch-smoke --configs ./providers.json --output ./batch-smoke.json --html-output ./batch-smoke.html
```

### Batch LT-lite baselines

```bash
python "$APIQ" batch-lt-baseline \
  --configs ./providers.json \
  --output-dir ./lt-baselines \
  --output ./batch-lt-baselines.json \
  --html-output ./batch-lt-baselines.html
```

### Batch LT-lite detect

```bash
python "$APIQ" batch-lt-detect \
  --configs ./providers.json \
  --baseline-manifest ./batch-lt-baselines.json \
  --output ./batch-lt-report.json \
  --html-output ./batch-lt-report.html
```

### Batch B3IT-lite baselines

```bash
python "$APIQ" batch-b3it-baseline \
  --configs ./providers.json \
  --output-dir ./b3it-baselines \
  --output ./batch-b3it-baselines.json \
  --html-output ./batch-b3it-baselines.html
```

### Batch B3IT-lite detect

```bash
python "$APIQ" batch-b3it-detect \
  --configs ./providers.json \
  --baseline-manifest ./batch-b3it-baselines.json \
  --output ./batch-b3it-report.json \
  --html-output ./batch-b3it-report.html \
  --detection-repeats 5 \
  --min-stable-count 2 \
  --min-stable-ratio 0.35 \
  --confirm-passes 1
```

### LT-lite baseline

```bash
python "$APIQ" lt-baseline --config ./provider.json --output ./lt-baseline.json
```

### LT-lite detect

```bash
python "$APIQ" lt-detect \
  --config ./provider.json \
  --baseline ./lt-baseline.json \
  --output ./lt-report.json
```

### B3IT-lite baseline

```bash
python "$APIQ" b3it-baseline --config ./provider.json --output ./b3it-baseline.json
```

### B3IT-lite detect

```bash
python "$APIQ" b3it-detect \
  --config ./provider.json \
  --baseline ./b3it-baseline.json \
  --output ./b3it-report.json \
  --detection-repeats 5 \
  --min-stable-count 2 \
  --min-stable-ratio 0.35 \
  --confirm-passes 1
```

### Daily single-endpoint drift run

```bash
bash "$APIQ_DAILY" ./provider.json ./daily-out my-endpoint
```

## Defaults and guardrails

- Default to non-streaming, `timeout=60`, and temperature values matched to the detector.
- Every command can additionally write a human-readable report with `--html-output`.
- OpenAI/OpenAI-compatible requests may include custom JSON `headers`, either from the config file or `--headers-json`.
- The Kimi-specific `{"User-Agent":"KimiCLI/2.0.0"}` header is not a general default. Use it only for `https://api.kimi.com/coding` endpoints; for the OpenAI-compatible Kimi path, use `https://api.kimi.com/coding/v1`.
- The script auto-disables thinking for common reasoning-first providers such as Ark, Doubao, GLM, and Zhipu unless `extra_body` is explicitly provided in the config JSON.
- For OpenAI/OpenAI-compatible endpoints that still return `reasoning_content` without normal text, the script will retry once with `{"thinking":{"type":"disabled"}}` before failing.
- OpenAI/OpenAI-compatible configs may use either the API root or a full `.../chat/completions` URL; the script normalizes the base URL internally.
- `init-config` writes the normalized config explicitly, including any auto-selected `extra_body`, so the saved file is portable across Codex, Claude Code, Gemini CLI, and OpenClaw runs.
- `init-batch-config` does the same normalization for a whole config list and writes a ready-to-run `providers.json`.
- Anthropic mode is treated as B3IT-only in this skill.
- If the endpoint returns reasoning/thinking blocks but no normal text, report that as a capability mismatch instead of fabricating a token result.
- If the endpoint does not return `logprobs`, report that LT-lite is unavailable instead of guessing.
- B3IT baseline discovery on OpenAI/OpenAI-compatible endpoints will automatically retry with a stronger candidate-search profile if an initial low-cost run finds no border inputs.
- B3IT detection defaults are tuned for lower false positives: `detection-repeats=5`, `min-stable-count=2`, `min-stable-ratio=0.35`, `confirm-passes=1`.
- Daily runs auto-refresh older B3IT baselines when they predate the stable-support filtering fields.

## Resources

Open only what you need:

- Workflow examples and CLI usage: `references/workflows.md`
- Protocol-first playbook for `OpenAI`, `OpenAI-Compatible`, and `Anthropic`: `references/endpoint-types-playbook.md`
- Kimi coding endpoint quickstart: `references/kimi-coding-quickstart.md`
- Kimi Anthropic endpoint quickstart: `references/kimi-anthropic-quickstart.md`
- JSON config format: `references/config-schema.md`
- Example provider list: `references/providers.example.json`
- Main executable: `scripts/api_quality_check.py`
- One-shot batch wrapper: `scripts/run_batch_checks.sh`
- Daily single-endpoint wrapper: `scripts/run_daily_check.sh`
