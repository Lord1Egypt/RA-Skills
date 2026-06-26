# Fund Purchase Status Tracker

[中文说明](./README.zh.md)

Track fund purchase availability, daily purchase quotas, fees, and changes since the previous run with AKShare.

## Quick Install

Install the skill:

```bash
npx skills add alondotsh/alon-skills --skill fund-tracker
```

Then install the Python runtime dependencies inside the installed skill directory:

```bash
pip install -r tools/requirements.txt
```

## When to Use

Use this when you want to check whether a fund is open for purchase, limited by a daily quota, paused, or changed since the previous check.

This skill is designed for fund purchase status tracking. It is not for stock or ETF market-price analysis.

## What It Does

- Reads fund code presets from `tools/presets.json`.
- Fetches purchase status from AKShare's Eastmoney fund purchase interface.
- Compares the latest result with `runtime/history_<preset>.json`.
- Prints JSON containing fund code, name, purchase status, daily quota, fee, net value, and detected changes.

## Usage

```bash
# Default preset
python3 tools/check.py

# Specific preset
python3 tools/check.py dingtou

# List available presets
python3 tools/check.py list
```

## Preset Management

Presets live in `tools/presets.json`:

```json
{
  "default": {
    "label": "汇丰QDII",
    "funds": ["006075", "050025", "016057", "016055", "016533", "016532"]
  }
}
```

Each preset has an independent runtime history file under `runtime/`.

## Safety and Limits

- The script depends on AKShare and the upstream Eastmoney data source.
- Network or upstream schema failures are returned as JSON errors.
- Runtime history is local state and should not be committed.
- The output is informational and is not financial advice.

## Output

The command prints JSON with:

- `preset`
- `label`
- `missing_funds`
- `data`

Each `data` row includes fund code, short name, purchase status, daily quota, fee, net value, and change summary.

## Project Structure

| Path | Purpose |
|------|---------|
| `SKILL.md` | Agent skill instructions |
| `tools/check.py` | Fund status checker |
| `tools/presets.json` | Preset definitions |
| `tools/requirements.txt` | Python dependencies |
| `runtime/history_<preset>.json` | Generated local history |
| `tests/test_check.py` | Unit tests |

## About Alon

These public skills come from Alon's real daily workflows.

Alon is actively exploring the future of agent skills and is open to connecting with people who want to build useful skills.

- GitHub: https://github.com/alondotsh
- ClawHub: https://clawhub.ai/u/alondotsh
- X: https://x.com/alondotsh
- WeChat Official Account: alondotsh
