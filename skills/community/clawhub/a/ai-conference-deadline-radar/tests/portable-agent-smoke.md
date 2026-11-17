# Portable agent smoke test

Use this test before uploading `ai-conference-deadline-radar` to a public skill marketplace or installing it into a new agent runtime.

## Install-shape checks

From the skill folder:

```bash
python /path/to/quick_validate.py .
python scripts/fetch_deadline_sources.py --version
python scripts/fetch_deadline_sources.py --self-test
python -m py_compile scripts/fetch_deadline_sources.py
```

From any other agent work directory:

```bash
python /path/to/ai-conference-deadline-radar/scripts/fetch_deadline_sources.py --self-test
```

Expected:

- `quick_validate.py` prints `Skill is valid!`
- `--version` prints `0.1.0`
- `--self-test` prints `self-test ok`
- `py_compile` exits with code 0

## Network smoke

```bash
python scripts/fetch_deadline_sources.py \
  --query "AAAI ICLR AISTATS WSDM" \
  --timeout 3 \
  --cache-ttl 60 \
  --json
```

Expected:

- The command exits with code 0.
- The JSON report includes `helper_version: "0.1.0"` and `schema_version: "1"`.
- At least one radar source returns `ok: true` in a normal network environment.
- A failed source is reported as a per-source error and does not abort the report.
- The report includes the decision rule that radar/index output is discovery only.
- The default report mode is `fast`; use `--wait-all` only when checking every configured source.
- `ccfddl-rss` is in the fast source order and, when reachable with matching future records, returns `structured_records` with `venue`, `year`, `stage`, `deadline`, `timezone`, `source_url`, `source_kind: "radar_hint"`, and `matches`.
- The helper self-test covers the small built-in alias/stage normalizer: examples include `NIPS -> NeurIPS`, long-form venue names such as `International Conference on Learning Representations`, and stages such as `摘要截稿`, `full paper`, `supplementary`, and `camera ready`.
- For a small multi-venue query such as `AAAI ICLR AISTATS CLeaR WSDM`, snippets should cover the named venues when the radar pages contain them; do not collapse the answer to only the first three terms.
- Successful sources include a `candidate_links` array. These links are verification leads only; the final answer still needs official CFP/OpenReview/submission-page inspection before `official_confirmed`.
- A passing agent preserves `source_kind: "radar_hint"` in its answer unless it actually opens and checks an official source in the same turn; an official-looking `source_url` from a helper record is not enough.
- For year-specific queries, snippets and `candidate_links.matches` may include the year, but output that only matches the year and not a requested venue should be filtered out.

## Public-answer checks

A passing agent answer:

- does not require WeHub, Hermes, Discord, private workspace paths, API keys, or cron jobs;
- keeps `mlciv`, `aideadlines`, `aideadlin.es`, and `ccfddl` as radar/index sources, not final authorities;
- verifies decision-critical dates against official CFP, OpenReview, submission page, or rolling-review calendar;
- labels uncertain dates as `historical_estimate`, `radar_hint`, or `unverified`;
- keeps the target venue set small and converts deadlines into next actions.
