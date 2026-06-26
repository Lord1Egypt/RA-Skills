---
name: bazi-pro
description: Professional Bazi analysis skill. Invoke when user asks for "bazi", "fortune telling", "calculate bazi", "eight characters", or "interpret bazi".
metadata: {"clawdbot":{"emoji":"🔮","requires":{"bins":["node"],"env":["OPENAI_API_KEY"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# Bazi Pro Skill

A professional Bazi (Four Pillars of Destiny) calculation and analysis tool based on Node.js and specialized SDK.

## CRITICAL INSTRUCTION FOR AGENT

**This tool automatically performs AI interpretation by default.**
You do NOT need to add `--interpret` flag anymore, unless you want to force it.
If the user wants raw data only, use `--no-interpret`.
The tool contains a specialized DeepSeek prompt that follows 《子平真诠》; you should prefer this over your own interpretation.

**IMPORTANT: OUTPUT FORMAT**
- The tool output is a complete, formatted Markdown report.
- **DO NOT** summarize or reformat the content into a structured card/table.
- **DO NOT** wrap the entire report in a code block (triple backticks). Output it as normal text so it renders correctly.
- **MUST** include the "AI Interpretation" section at the end.

## Usage

### Standard (Analysis & Calculation)
Use this for almost all requests:
```bash
node {baseDir}/index.js --year 1990 --month 5 --day 15 --hour 14 --gender Male
```

### 3. Calculate with AI Interpretation (Life Main Line Only)
Get a detailed analysis of the lifetime fate pattern, excluding decade luck cycles (Da Yun).

```bash
node {baseDir}/index.js --year 1990 --month 5 --day 15 --hour 14 --gender Male --no-dayun
```

### 4. Raw Output Only (No AI)
Use this ONLY if user explicitly asks for "calculation only" or "no interpretation":
```bash
node {baseDir}/index.js --year 1990 --month 5 --day 15 --hour 14 --gender Male --no-interpret
```

## Arguments

- `--year`: Birth year (e.g., 1990)
- `--month`: Birth month (1-12)
- `--day`: Birth day (1-31)
- `--hour`: Birth hour (0-23)
- `--minute`: Birth minute (0-59, default: 0)
- `--gender`: Gender ('Male' or 'Female', default: 'Male')
- `--interpret`: Force enable AI interpretation (default: true if API key configured)
- `--no-interpret`: Disable AI interpretation (for raw data output)

## Examples

- "Calculate bazi for 1990-05-15 14:00 Male" -> `node {baseDir}/index.js --year 1990 --month 5 --day 15 --hour 14 --gender Male`
- "Interpret bazi for 1990-05-15 14:00 Male" -> `node {baseDir}/index.js --year 1990 --month 5 --day 15 --hour 14 --gender Male --interpret`
- "Analyze my fortune: 1988/8/8 8:00 Female" -> `node {baseDir}/index.js --year 1988 --month 8 --day 8 --hour 8 --gender Female --interpret`

## Features

- **Precise Calculation**: Uses true solar time and E120 longitude (default).
- **Comprehensive Analysis**:
  - Four Pillars (Year, Month, Day, Hour)
  - Day Master (Gan/Element)
  - Shishen (Ten Gods)
  - Zhi Relations (Clash, Combine, Harm, Punishment)
  - Day Master Strength (Score & Status)
  - Dayun (Major Cycles) & Current Cycle
  - Pattern Analysis (Normal/Special Structures, Yong/Xi/Ji Shen)
- **AI Interpretation**: Supports deep analysis using LLM (DeepSeek recommended).

## Environment Variables

Primary Configuration (DeepSeek):
- `DEEPSEEK_API_KEY`: Required for AI interpretation.
- `DEEPSEEK_BASE_URL`: Optional, defaults to `https://api.deepseek.com`.
- `DEEPSEEK_MODEL`: Optional, defaults to `deepseek-chat`.

Fallback Configuration (OpenAI):
- `OPENAI_API_KEY`: Used if DeepSeek key is missing.
- `OPENAI_BASE_URL`: Optional, defaults to `https://api.openai.com/v1`.

## Output

Returns a structured report including:
1. Basic Info
2. Four Pillars
3. Day Master Status
4. Current Dayun
5. Pattern Analysis
6. Zhi Relations
7. AI Interpretation (if requested)
