---
name: ceac-visa-status-checker
description: Automatically check U.S. visa application status in CEAC (NIV), solve CEAC captcha with Zhipu vision model, and return structured status JSON. Use this when user asks to check CEAC status, monitor visa case status, troubleshoot CEAC captcha issues, or run CEAC checks with LOCATION/NUMBER/PASSPORT_NUMBER/SURNAME and ZHIPU_API_KEY.
---
# CEAC Visa Status Checker (Zhipu Captcha)

This skill checks U.S. visa application status from CEAC and uses Zhipu vision model to read captcha.

## Required User Fields

- LOCATION: visa application location text in CEAC (example: CHINA, BEIJING)
- NUMBER: Application ID or Case Number (example: AA0020AKAX)
- PASSPORT_NUMBER: passport number
- SURNAME: first letters of surname as used in CEAC
- ZHIPU_API_KEY: API key for captcha OCR

Optional:

- ZHIPU_MODEL_VISION (default: glm-4v-flash)
- MAX_RETRIES (default: 5)
- RETRY_DELAY_SECONDS (default: 5)

Location help:

- See references/LOCATION.md

## Workflow

1. Ensure dependencies are installed from requirements.txt.
2. Create .env based on .env.example.txt.
3. Run scripts/check_ceac_status.py.
4. Return JSON output to user.

## Commands

Install:

python -m pip install -r requirements.txt

Run:

python scripts/check_ceac_status.py

## Output Contract

On success:

- success: true
- status: CEAC status text
- case_last_updated: CEAC last updated date
- description: CEAC message
- application_num: returned case number

On failure:

- success: false
- error/message/last_error

## Notes

- Captcha recognition may fail occasionally. The script retries automatically.
- LOCATION must match CEAC location dropdown text. Fuzzy match is attempted.
- Keep API keys in environment variables. Avoid hardcoding secrets in scripts.
