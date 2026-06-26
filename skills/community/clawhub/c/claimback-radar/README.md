# Claimback Radar

**🔑 REQUIRED CREDENTIAL**: `OPENAI_API_KEY` environment variable.  
**⚠️ EXTERNAL DATA FLOW**: User content is sent to OpenAI API. Review OpenAI's privacy policy before use.  
**🛡️ DATA PRIVACY NOTICE**: Do not submit sensitive financial or identity data unless you explicitly accept this external data flow.

---

AI-powered inbox scanner for hidden refunds, subscription traps, and savings opportunities.

## Installation

```bash
pip install -r requirements.txt
```

Required packages: `openai`, `python-dotenv`, `pydantic`.

## ⚠️ Prerequisites & Privacy

- **OpenAI API Key required**: Set `OPENAI_API_KEY` environment variable.
- **External data flow**: This skill sends your email/bill text to OpenAI API for processing. Do not use with sensitive data unless you explicitly accept OpenAI's data handling terms.
- **.env safety**: This skill loads `.env` from the working directory if present. Ensure no unrelated secrets are stored in that file.

## What it does

**Function 1: Structured Extraction**
- Scans raw email / bill / subscription text and extracts: service name, provider, amount, billing cycle, next charge date, refund deadline, warranty expiry, cancellation method.

**Function 2: Risk Detection & Action Generation**
- Detects risks: upcoming charges, refund windows closing, unused services, price hikes, warranty expiring.
- Generates prioritized action receipts with deadlines and estimated savings.

## Quick Start

Paste an email or bill text into the Skill invocation:

```json
{
  "skill": "claimback_radar",
  "input": {
    "source": "email_text",
    "content": "Your raw email or bill text here...",
    "user_timezone": "Asia/Singapore",
    "current_date": "2026-04-22",
    "user_context": {
      "last_used_date": "2026-03-15",
      "monthly_budget": 50
    }
  }
}
```

## Output

- `confirmation_card`: Clean structured summary of the subscription / bill
- `action_receipts`: Prioritized todo list with deadlines, reasons, and savings estimates
- `risk_flags`: Alert tags (e.g., `refund_window_closing`, `unused_service`)

## Examples

- [Netflix subscription email](examples/netflix_email.md)
- [Amazon Prime renewal notice](examples/amazon_prime_email.md)

## Schema

- Input: [`schema/input.json`](schema/input.json)
- Output: [`schema/output.json`](schema/output.json)

## Security Notes

- `main.py` explicitly loads `.env` if present and warns the user.
- Never commit `.env` files containing real API keys to version control.
- For production, prefer explicit `api_key` injection over implicit environment loading.
- This skill loads `.env` from the working directory if present. Ensure no unrelated secrets are stored there.

## License

MIT