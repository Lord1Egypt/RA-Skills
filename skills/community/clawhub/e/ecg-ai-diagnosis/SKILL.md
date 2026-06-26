---
name: heartvoice_cloud
description: Analyze ECG signals via heartvoice (心之声) API — single-lead and 12-lead. Automatically selects endpoint based on user intent and responds in the user's language. Use when user mentions ECG, 心电图, 心电分析, 单导联, 十二导联, 1-lead, 12-lead, heart rhythm, arrhythmia, QRS, QT interval, signal quality, or asks to analyze an ECG JSON file.
homepage: https://www.heartvoice.com.cn/aiCloud
metadata: {"clawdbot":{"emoji":"❤","requires":{"bins":[],"env":["HEARTVOICE_API_KEY"]},"primaryEnv":"HEARTVOICE_API_KEY"}}
---

# heartvoice ECG Analysis Skill

Analyze ECG data via the heartvoice (心之声) cloud API. The **agent** is responsible for detecting user intent (1-lead vs 12-lead) and language (Chinese vs English), then passing the appropriate explicit flags to the CLI script. The script itself requires explicit `--mode` and `--lang` parameters — all "automatic" behavior lives in the agent layer, not the script.

## When to Activate

- User wants to analyze ECG / heart rhythm / electrocardiogram data
- User provides a JSON file containing ECG signal data
- Code or conversation mentions 心电图, ECG, 心电分析, 心律分析
- Keywords: 单导联, 十二导联, 1-lead, 12-lead, single lead, twelve lead
- User asks about arrhythmia detection, QRS/QT intervals, or signal quality
- User says "analyze ECG", "分析心电", "ecg diagnosis", or similar

## Environment Setup

```bash
# Required — get your key at https://www.heartvoice.com.cn/aiCloud
export HEARTVOICE_API_KEY="your_api_key"

# Install dependencies
pip install requests
```

Never hardcode API keys. Always use environment variables or `.env` files.

## Agent Responsibilities

The agent (not the CLI script) is responsible for two kinds of detection:

### 1. Detect analysis type → pass as CLI mode

Scan the user message for keywords and map to the explicit CLI mode argument:

| User Intent | CN Keywords | EN Keywords | CLI Mode |
|---|---|---|---|
| Single-lead signal | 单导联、单导、1导联 | 1-lead, single lead, one lead | `1-lead` |
| 12-lead signal | 十二导联、12导联、多导联 | 12-lead, twelve lead | `12-lead` |

**If the user does not specify a type**, ask before running the script:
- Chinese: "请问您要分析的是单导联信号还是十二导联信号？"
- English: "Would you like to analyze a single-lead or 12-lead signal?"

### 2. Detect user language → pass as `--lang` flag

Detect the language the user writes in and pass it as the `--lang` CLI flag:

| User Language | `--lang` Value |
|---|---|
| Chinese (中文) | `zh` (default) |
| English | `en` |

Then respond entirely in that language throughout the session.

## Workflow

1. **Agent detects** analysis type (1-lead / 12-lead) from user message keywords. If ambiguous, ask.
2. **Agent detects** user language (zh / en) from the message.
3. **Agent extracts** file path from the user message.
4. **Agent runs** the CLI script with explicit arguments: `python3 scripts/call_api.py <mode> --json_path <path> --lang <lang>`.
5. **Agent parses** the structured JSON output from stdout.
6. **Agent presents** the result as a natural-language report in the user's language.

## Script Commands

```bash
# 1-lead signal analysis (Chinese output)
python3 scripts/call_api.py 1-lead --json_path <path/to/file.json>

# 1-lead signal analysis (English output)
python3 scripts/call_api.py 1-lead --json_path <path/to/file.json> --lang en

# 12-lead signal analysis (Chinese output)
python3 scripts/call_api.py 12-lead --json_path <path/to/file.json>

# 12-lead signal analysis (English output)
python3 scripts/call_api.py 12-lead --json_path <path/to/file.json> --lang en
```

Set `--lang zh` (default) or `--lang en` based on the language the user writes in.

## Input File Formats

### ADC Conversion Formula

The data arrays contain **raw sample values** from your recording device (integers or floats, depending on the device). The API internally converts them to millivolts (mV) using:

```
voltage_mV = (sampleValue - adcZero) / adcGain
```

- `adcZero` — the sample value that corresponds to 0 mV (baseline offset)
- `adcGain` — the number of sample units per 1 mV

**Example 1 (integer samples)**: `adcGain = 1000`, `adcZero = 0`, sample = `512` → `voltage = (512 - 0) / 1000 = 0.512 mV`.

**Example 2 (float samples, already in mV)**: if your device outputs values already in millivolts (e.g. `0.512`), set `adcGain = 1.0` and `adcZero = 0.0` so the formula becomes a no-op: `voltage = (0.512 - 0) / 1 = 0.512 mV`.

These two parameters must match your recording device's output configuration; incorrect values will produce wrong voltage readings and unreliable diagnoses.

### 1-lead JSON

```json
{
  "ecgData": [0.512, 0.515, 0.520, 0.518, 0.525, 0.530, 0.528, 0.535],
  "ecgSampleRate": 500,
  "adcGain": 1.0,
  "adcZero": 0.0
}
```

In this example, values are already in mV, so `adcGain = 1.0` and `adcZero = 0.0` (identity conversion). If your device outputs raw integer ADC values instead, adjust `adcGain` and `adcZero` accordingly.

| Field | Type | Required | Description |
|---|---|---|---|
| `ecgData` | number[] | Yes | Sample value array — integers or floats, converted to mV via the formula above |
| `ecgSampleRate` | number | Yes | Sampling rate in Hz (e.g. 500) |
| `adcGain` | number | Yes | Sample units per 1 mV |
| `adcZero` | number | Yes | Sample value corresponding to 0 mV baseline |

### 12-lead JSON

```json
{
  "dataI":   [...], "dataII":  [...], "dataIII": [...],
  "dataAVR": [...], "dataAVL": [...], "dataAVF": [...],
  "dataV1":  [...], "dataV2":  [...], "dataV3":  [...],
  "dataV4":  [...], "dataV5":  [...], "dataV6":  [...],
  "ecgSampleRate": 500,
  "adcGain": 1000.0,
  "adcZero": 0.0
}
```

In this example, values are raw integer ADC samples with `adcGain = 1000` (1000 units = 1 mV).

| Field | Type | Required | Description |
|---|---|---|---|
| `dataI` … `dataV6` | number[] | Yes | 12 lead sample arrays (I, II, III, aVR, aVL, aVF, V1–V6) — integers or floats, converted to mV via the formula above |
| `ecgSampleRate` | number | Yes | Sampling rate in Hz |
| `adcGain` | number | Yes | Sample units per 1 mV — shared across all 12 leads |
| `adcZero` | number | Yes | Sample value corresponding to 0 mV baseline |

## Response Format

The fields below are the **script's output** (printed to stdout as JSON). The script normalizes the API's camelCase field names (e.g. `avgHr`, `avgQrs`, `isAbnormal`) to snake_case (e.g. `avg_hr`, `avg_qrs`, `is_abnormal`) for consistency. When reading the script output, always use the snake_case names listed here.

### 1-lead response fields

| Field | Type | Description |
|---|---|---|
| `status` | string | `"success"` or `"error"` |
| `summary` | string | Natural-language summary in requested language |
| `diagnosis` | string[] | Label list, e.g. `["SN"]` |
| `possible_diagnosis` | string[] | Possible labels list |
| `is_abnormal` | boolean | Whether abnormal rhythm detected |
| `is_reverse` | boolean | Whether lead reversal detected |
| `sq_grade` | string | Signal quality score, e.g. `"0.95"` |
| `avg_hr` | number | Average heart rate (bpm) |
| `avg_qrs` | number | QRS duration (ms) |
| `pr_interval` | number | PR interval (ms) |
| `avg_qt` | number | QT interval (ms) |
| `avg_p` | number | P wave duration (ms) |
| `avg_qtc` | number | Corrected QT interval (ms) |
| `pac_count` | number | Atrial premature beat count |
| `pvc_count` | number | Ventricular premature beat count |

### 12-lead response fields

| Field | Type | Description |
|---|---|---|
| `status` | string | `"success"` or `"error"` |
| `analysis_state` | boolean | Whether analysis succeeded |
| `summary` | string | Natural-language summary in requested language |
| `diagnoses` | object[] | Array of `{"label", "result", "description"}` |
| `diagnosis_results` | string[] | Flat list of result strings |
| `risk_level` | number | Risk level — `0` = normal |
| `HR` | number | Heart rate (bpm) |
| `atrial_rate` | number | Atrial rate (bpm) |
| `ventricular_rate` | number | Ventricular rate (bpm) |
| `P` / `PR` / `QRS` / `QT` / `QTc` / `T` | number | Intervals (ms) |
| `QRS_axis` / `P_axis` / `T_axis` | number | Electrical axes (degrees) |
| `SV1` / `SV2` / `SV5` / `RV1` / `RV2` / `RV5` / `RV6` | number | Wave amplitudes (mV) |

## Examples

### Example 1 — Chinese user, single-lead

> 用户：请帮我分析这个单导联信号，数据放在 data/ecg_data.json 里

Agent runs:

```bash
python3 scripts/call_api.py 1-lead --json_path data/ecg_data.json --lang zh
```

Output:

```json
{
  "status": "success",
  "summary": "检测到：窦性心律。平均心率 72 次/分钟，QRS 宽度 86 毫秒，PR 间期 156 毫秒，QT 间期 380 毫秒，QTc 412 毫秒，P 波宽度 102 毫秒。信号质量 0.95。房性早搏 0 次，室性早搏 0 次。",
  "diagnosis": ["SN"],
  "possible_diagnosis": [],
  "is_abnormal": false,
  "avg_hr": 72,
  "sq_grade": "0.95"
}
```

Agent responds:

> 分析完成。该心电信号显示**窦性心律**，平均心率 72 次/分钟，各项参数均在正常范围内。信号质量评分 0.95（优秀），未检测到房性或室性早搏。

### Example 2 — English user, 12-lead

> User: Analyze my 12-lead ECG data from records/12lead.json

Agent runs:

```bash
python3 scripts/call_api.py 12-lead --json_path records/12lead.json --lang en
```

Output:

```json
{
  "status": "success",
  "summary": "Detected: Sinus Rhythm. Heart rate 75 bpm, QRS duration 88 ms, PR interval 160 ms, QT interval 376 ms, QTc 420 ms, P wave 100 ms, T wave 180 ms. Risk assessment: normal.",
  "diagnoses": [{"label": "SN", "result": "Sinus Rhythm", "description": "Normal sinus rhythm"}],
  "risk_level": 0,
  "HR": 75
}
```

Agent responds:

> Analysis complete. The 12-lead ECG shows **Sinus Rhythm** with a heart rate of 75 bpm. All intervals are within normal range. Risk level: normal (0).

### Example 3 — Ambiguous intent

> User: Can you analyze this ECG for me? The file is at data/signal.json

Agent asks:

> Would you like to analyze a **single-lead (1-lead)** or **12-lead** signal?

## Error Handling

| Situation | Action |
|---|---|
| File not found | Report the exact path; ask user for the correct path |
| Missing JSON fields | List the missing required fields by name |
| `HEARTVOICE_API_KEY` not set | Tell the user to visit https://www.heartvoice.com.cn/aiCloud to obtain an API Key and set it as the `HEARTVOICE_API_KEY` environment variable |
| HTTP error from API | Show status code and error message from the response |
| API business error (`errorCode != 0`) | Show the error message returned by the API |
| File too large (> 5 MB) | Tell the user the file exceeds the 5 MB limit |
| Ambiguous intent | Ask whether the data is 1-lead or 12-lead |

## Security & Privacy

**Data flow**: This skill reads a user-specified local JSON file and sends its contents (ECG signal data, sample rate, ADC parameters) over HTTPS to the heartvoice cloud API (`api.heartvoice.com.cn`) for analysis. The user should be aware that their ECG data leaves the local machine. No other files or environment variables beyond `HEARTVOICE_API_KEY` are accessed.

- **Never hardcode API keys** in scripts or commit them to version control
- ECG data is **sensitive medical data** — do not log or store raw signal data unnecessarily; inform the user before transmitting
- Always use HTTPS (the API endpoint enforces TLS)
- Add `.env` to `.gitignore` if using dotenv files
- The skill only reads the file path explicitly provided by the user — it does not scan or access other files
- This tool provides **AI-assisted analysis only**; it is NOT a substitute for professional medical diagnosis

## Tips

- Signal quality (`sq_grade`) below 0.6 usually indicates noisy data — suggest the user re-record or check electrode contact
- For 12-lead analysis, all 12 lead arrays must be present; partial data will fail field validation
- The `adcGain` and `adcZero` values must match your recording device's ADC configuration — see the **ADC Conversion Formula** section for how they translate raw samples to millivolts
- JSON file size limit is 5 MB
- Typical `ecgSampleRate` values: 250, 500, 1000 Hz — check your device specs
- Use the example files in `data/` to verify your setup before analyzing real signals

## Programmatic Usage

You can also import the script functions directly in Python:

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
output = format_1lead_result(raw_result)
print(output["summary"])
print(f"Heart rate: {output['avg_hr']} bpm")
```
