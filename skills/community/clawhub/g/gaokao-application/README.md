# 高考志愿填报助手

`gaokao-application` is an AgentSkills-style assistant for mainland China Gaokao college application planning.

It helps students and parents build cautious志愿填报 plans from province rules, rank, subject choices, admission data, preferences, and risk tolerance. It is designed for Hermes, OpenClaw, Codex, and other agents that can read `SKILL.md`.

## What It Does

- Collects the right Gaokao application context before recommending anything.
- Uses provincial rank/位次 as the primary matching signal.
- Supports uploaded CSV admission datasets.
- Builds risk-labeled `冲 / 小冲 / 稳 / 保 / 垫` shortlists.
- Forces official-source verification before final submission.
- Avoids unsafe claims such as guaranteed admission.

## Install

SkillHub page:

```text
https://skillhub.cn/skills/gaokao-application
```

### Hermes

```bash
hermes skills install harrylabsj/gaokao-application --yes
```

Or install from the raw `SKILL.md` URL:

```bash
hermes skills install https://raw.githubusercontent.com/harrylabsj/gaokao-application/main/SKILL.md --yes
```

### OpenClaw

```bash
openclaw plugins install https://github.com/harrylabsj/gaokao-application
```

For local development:

```bash
openclaw plugins install ./gaokao-application --link
```

## Use

Ask your agent:

```text
Use $gaokao-application to help me build a Gaokao application plan.
```

Prepare:

- province and year
- score and provincial rank
- subject track or selected subjects
- target batch
- city, major, budget, and school preferences
- whether you accept adjustment, private universities, Sino-foreign programs, high tuition, or remote campuses
- official admission data, if available

## CSV Helpers

The `scripts/` directory contains optional standard-library Python helpers:

```bash
python3 scripts/validate_dataset.py admissions.csv
python3 scripts/normalize_admission_data.py raw.csv normalized.csv
python3 scripts/shortlist_builder.py normalized.csv --rank 24567 --subject physics --out shortlist.csv
python3 scripts/risk_scoring.py shortlist.csv --rank 24567 --out scored.csv
python3 scripts/rank_matcher.py normalized.csv --rank 24567 --window 0.25
```

## Safety

This skill does not guarantee admission. It is a decision-support workflow. Always verify final choices against current official documents from the provincial examination authority, university admissions office, and Sunshine Gaokao.

## License

MIT
