# Agent Scorecard — Output Quality Framework

**Configurable quality evaluation for AI agent outputs. Define criteria, run evaluations, track quality over time.**

Agent Scorecard gives you a structured, repeatable way to measure whether your AI agent is producing good output — and whether it's getting better or worse over time. No LLM-as-judge, no API calls, no external dependencies. Everything runs locally with pattern-based automated checks and optional human scoring.

---

## The Problem

You changed your agent's system prompt. Is the output better now? You don't know. You added a new tool. Did response quality degrade? You have a feeling, but no data. Quality management for AI agents is mostly vibes.

Agent Scorecard replaces vibes with numbers.

## What It Does

### 1. **Define Quality Dimensions** (`config_example.json`)
- Configure what "quality" means for your use case
- Set dimensions: accuracy, completeness, tone, format compliance, consistency — or your own
- Define rubrics (what does a 1 vs a 5 look like for each dimension?)
- Set weights (accuracy matters more than tone? Give it 2× weight)
- Set pass/fail thresholds per dimension

### 2. **Evaluate** (`scorecard.py`)
- **Automated mode:** Pattern-based checks run instantly with zero API calls
  - Response length analysis (too short? too long?)
  - Format compliance (expected headers, lists, code blocks present?)
  - Sycophancy detection ("Great question!" markers)
  - Filler/hedge word density ("basically", "perhaps", "I think")
  - Required section verification
  - Style consistency (sentence length variation)
- **Manual mode:** Interactive rubric-guided human scoring
- **Blended mode:** Combine auto scores with human judgment (averaged)
- Aggregate scoring with configurable method (weighted average, minimum, geometric mean)

### 3. **Track** (`scorecard_track.py`)
- Append every evaluation to a JSONL history file
- Filter by agent, task type, time period
- Compute trends per dimension (improving, degrading, stable)
- Linear regression slope for quantified direction
- Sparkline visualisations in terminal

### 4. **Compare** (`scorecard_track.py`)
- Before/after comparison (last N evals vs previous N)
- Per-dimension delta with direction indicators
- Perfect for measuring the impact of config changes

### 5. **Report** (`scorecard_report.py`)
- Single evaluation reports (markdown or JSON)
- History summary reports with tables and sparklines
- Per-dimension breakdowns with rubric reference
- Export to files or stdout

---

## Quick Start

```bash
# 1. Configure
cp config_example.json scorecard_config.json
# Edit dimensions, thresholds, and weights for your use case

# 2. Evaluate a response
python3 scorecard.py --config scorecard_config.json --input response.txt

# 3. Evaluate and save to history
python3 scorecard.py --config scorecard_config.json --input response.txt --save history.jsonl

# 4. Manual scoring mode
python3 scorecard.py --config scorecard_config.json --input response.txt --manual --save history.jsonl

# 5. View trends
python3 scorecard_track.py --history history.jsonl --summary

# 6. Compare before/after (last 10 vs previous 10)
python3 scorecard_track.py --history history.jsonl --compare 10

# 7. Generate a report
python3 scorecard_report.py --config scorecard_config.json --history history.jsonl
```

## Programmatic Usage

```python
from scorecard import Scorecard, _load_config

cfg = _load_config("scorecard_config.json")
sc = Scorecard(cfg)

text = open("agent_response.txt").read()
result = sc.evaluate(text, agent="my-agent", task_type="code-review")

print(result.summary())
# Overall: 3.85/5 (PASS)
#   ✓ Accuracy: 4.0/5 (threshold 3, weight 2.0) [auto]
#   ✓ Completeness: 3.5/5 (threshold 3, weight 1.5) [auto]
#   ...

# Save for tracking
import json
with open("history.jsonl", "a") as f:
    f.write(json.dumps(result.to_dict()) + "\n")
```

---

## Use Cases

- **Prompt engineering:** Measure whether prompt changes improve output quality
- **Model comparison:** Same task, different models — which scores higher?
- **Agent regression testing:** Catch quality degradation before it ships
- **Team quality standards:** Define shared rubrics for consistent evaluation
- **Continuous monitoring:** Track quality trends over days/weeks/months
- **A/B testing:** Quantified before/after comparisons

## What's Included

| File | Purpose |
|------|---------|
| `scorecard.py` | Main evaluation engine — define, evaluate, score |
| `scorecard_track.py` | Historical tracking and trend analysis |
| `scorecard_report.py` | Report generation (markdown, JSON) |
| `config_example.json` | Full configuration template with all tunables |
| `LIMITATIONS.md` | What this tool doesn't do |
| `LICENSE` | MIT License |

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- Works on any OS
- Platform-agnostic (works with any AI agent framework)

## Configuration

See `config_example.json` for the complete reference. Key areas:

- **`DIMENSIONS`** — Quality dimensions with rubrics, weights, thresholds, and auto-checks
- **`AUTO_CHECKS`** — Tuning for each pattern-based check (markers, thresholds, penalties)
- **`AGGREGATE_METHOD`** — How to combine dimension scores ("weighted_average", "minimum", "geometric_mean")
- **`HISTORY_FILE`** — Where to store evaluation history
- **`REPORT_OUTPUT_DIR`** — Where reports are saved

---

## quality-verified


## License

MIT — See `LICENSE` file.


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
