# heartvoice ECG Analysis Skill

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![API: heartvoice](https://img.shields.io/badge/API-heartvoice%20cloud-red.svg)](https://www.heartvoice.com.cn/aiCloud)

An [OpenClaw](https://github.com/openclaw) / [CrawHub](https://crawhub.com) Skill that analyzes ECG (electrocardiogram) signals via the **heartvoice (心之声)** cloud API. Automatically selects the correct analysis endpoint based on user intent (single-lead or 12-lead) and responds in the user's language.

## Features

- **Single-lead (1-lead)** and **12-lead** ECG signal analysis
- Automatic endpoint selection based on natural-language keywords
- Bilingual output: Chinese (`--lang zh`) and English (`--lang en`)
- Structured JSON results with diagnostic labels, heart rate, intervals, and more
- Signal quality scoring and abnormality detection
- Ready-to-use example data for quick testing

## Directory Structure

```
ecg-ai-diag_skill/
├── SKILL.md                      # Skill declaration for OpenClaw / CrawHub
├── README.md                     # This file
├── LICENSE                       # MIT license
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── scripts/
│   └── call_api.py               # API call script (CLI + importable)
└── data/
    ├── example_1lead.json        # Example single-lead ECG data
    └── example_12lead.json       # Example 12-lead ECG data
```

## Quick Start

### 1. Get an API Key

Visit the [heartvoice AI ECG Cloud](https://www.heartvoice.com.cn/aiCloud) to register and obtain your API Key.

### 2. Set Environment Variable

```bash
export HEARTVOICE_API_KEY="your_api_key"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Analysis

```bash
# Single-lead analysis (Chinese output)
python3 scripts/call_api.py 1-lead --json_path data/example_1lead.json

# Single-lead analysis (English output)
python3 scripts/call_api.py 1-lead --json_path data/example_1lead.json --lang en

# 12-lead analysis
python3 scripts/call_api.py 12-lead --json_path data/example_12lead.json --lang en
```

### 5. Example Output

```json
{
  "status": "success",
  "summary": "Detected: SN. Avg heart rate 72 bpm, QRS duration 86 ms, ...",
  "diagnosis": ["SN"],
  "possible_diagnosis": [],
  "is_abnormal": false,
  "avg_hr": 72,
  "sq_grade": "0.95",
  "pac_count": 0,
  "pvc_count": 0
}
```

## Data Formats

Data arrays contain **raw sample values** (integers or floats, depending on the device). The API converts them to millivolts using:

```
voltage_mV = (sampleValue - adcZero) / adcGain
```

`adcGain` = sample units per 1 mV; `adcZero` = sample value at 0 mV. If your device already outputs mV, set `adcGain = 1.0` and `adcZero = 0.0`.

### Single-lead JSON

| Field | Type | Required | Description |
|---|---|---|---|
| `ecgData` | number[] | Yes | Sample value array (integers or floats) |
| `ecgSampleRate` | number | Yes | Sampling rate in Hz (e.g. 500) |
| `adcGain` | number | Yes | Sample units per 1 mV |
| `adcZero` | number | Yes | Sample value at 0 mV baseline |

### 12-lead JSON

| Field | Type | Required | Description |
|---|---|---|---|
| `dataI` … `dataV6` | number[] | Yes | 12 lead sample arrays (integers or floats) |
| `ecgSampleRate` | number | Yes | Sampling rate in Hz |
| `adcGain` | number | Yes | Sample units per 1 mV (shared for all leads) |
| `adcZero` | number | Yes | Sample value at 0 mV baseline |

See `SKILL.md` for the complete ADC conversion formula, field specifications, and response format documentation.

## Programmatic Usage

```python
import os
from scripts.call_api import load_json, build_1lead_payload, call_api, format_1lead_result

api_key = os.environ["HEARTVOICE_API_KEY"]
data = load_json("data/example_1lead.json")
payload = build_1lead_payload(data)
raw_result = call_api(
    "https://api.heartvoice.com.cn/api/v1/basic/ecg/1-lead/analyze",
    payload, api_key
)
output = format_1lead_result(raw_result, lang="en")
print(output["summary"])
```

## Requirements

- Python 3.7+
- `requests` library
- A valid `HEARTVOICE_API_KEY`

## Security & Privacy

- **Data flow**: this skill reads a user-specified local JSON file and sends its ECG data over HTTPS to the heartvoice cloud API for analysis. No other files or env vars beyond `HEARTVOICE_API_KEY` are accessed.
- Never hardcode API keys — use environment variables
- ECG data is sensitive medical data — handle with care and inform users before transmitting
- This tool provides AI-assisted analysis only; it is **not** a substitute for professional medical diagnosis

## License

[MIT](LICENSE)

## Links

- [heartvoice AI ECG Cloud](https://www.heartvoice.com.cn/aiCloud) — API documentation & key management
- [heartvoice Official Site](https://www.heartvoice.com.cn) — Company homepage
