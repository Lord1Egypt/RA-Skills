# AI Layoff Radar Skill

AI Layoff Radar is an OpenClaw skill that scans global news and detects company layoffs that are specifically tied to AI adoption (automation, AI replacing workers, and AI efficiency-driven cuts).

## What This Skill Does

1. Fetches layoff-related news from:
   - Google News RSS
   - TechCrunch
   - Bloomberg
   - Reuters
   - Financial Times
   - The Verge
   - Wired
2. Detects layoff candidate events from article text.
3. Extracts structured fields:
   - `company_name`
   - `date`
   - `country`
   - `layoff_count`
   - `reason`
   - `source_url`
4. Classifies each event using an LLM prompt and keeps only AI-related layoffs.
5. Returns a structured JSON report.
6. Enforces SkillPay billing before detection runs.

## Project Structure

- `SKILL.md`
- `README.md`
- `requirements.txt`
- `main.py`
- `layoff_detector.py`
- `news_fetcher.py`
- `ai_classifier.py`
- `billing.py`

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables:

```bash
# OpenAI (for layoff causality classification)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# SkillPay
SKILLPAY_API_KEY=your_skillpay_api_key
SKILLPAY_DEV_MODE=false
```

## SkillPay Billing Setup

SkillPay uses the official API host `https://skillpay.me` and the following endpoints:

- `GET /api/v1/billing/balance`
- `POST /api/v1/billing/charge`
- `POST /api/v1/billing/payment-link`

Set API key:

```bash
export SKILLPAY_API_KEY="your_api_key"
```

DEV mode:

- Set `SKILLPAY_DEV_MODE=true` to bypass live billing calls during local development.
- In DEV mode, billing functions simulate success responses (for example balance `999`).
- In non-DEV mode, missing `SKILLPAY_API_KEY` raises: `SKILLPAY_API_KEY not configured`.

## Run Locally

```bash
python main.py --user_id user_123
```

## Billing Flow (SkillPay)

Skill ID:

- `d81a694a-f0bd-4119-a07a-926927d75631`

Price per call:

- `$0.02`

Execution order in `main.py`:

1. Receive `user_id`
2. `GET /api/v1/billing/balance?user_id=xxx`
3. `POST /api/v1/billing/charge`
4. If insufficient balance: request payment link and return:
   `{"error":"payment_required","payment_url":"...","balance":...}`
5. If charge succeeds: run layoff detection and return report

## Output Format

Example:

```json
{
  "detected_events": [
    {
      "company": "IBM",
      "country": "USA",
      "layoffs": 7800,
      "reason": "AI automation replacing HR staff",
      "source": "https://..."
    }
  ],
  "summary": "3 companies announced AI-related layoffs in the past 24h"
}
```

## Deploy to OpenClaw / ClawHub

1. Ensure all files are present at skill root.
2. Include `SKILL.md` with proper frontmatter and usage metadata.
3. Package/upload the folder as `ai-layoff-radar-skill`.
4. In ClawHub, configure environment variables:
   - `OPENAI_API_KEY`
   - `SKILLPAY_API_KEY`
   - `SKILLPAY_DEV_MODE` (optional)
5. Publish and run using `user_id` input.
