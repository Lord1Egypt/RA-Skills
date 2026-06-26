# Skill Definition: claimback_radar

**🔑 REQUIRED CREDENTIAL**: `OPENAI_API_KEY` environment variable (or pass `api_key` directly to `ClaimbackRadar`).  
**⚠️ EXTERNAL DATA FLOW**: User-provided text content is transmitted to OpenAI's API. Review OpenAI's data retention and privacy policies before use.  
**🛡️ DATA PRIVACY NOTICE**: Do not submit sensitive financial or identity data unless you explicitly accept this external data flow.

---

## Description
Scans user emails and bills to discover hidden refunds, subscription traps, and savings opportunities.

## Functions

### Function 1: extract
Extracts structured subscription / billing data from unstructured text.

**Input**: Raw email or bill text
**Output**: `confirmation_card` (JSON)

### Function 2: detect_and_recommend
Detects risks and generates actionable receipts.

**Input**: `confirmation_card` + user context
**Output**: `action_receipts` + `risk_flags`

## Invocation Schema
See `schema/input.json`

## Output Schema
See `schema/output.json`

## Example
See `examples/netflix_email.md`

## Security Notes
- The CLI entrypoint (`main.py`) explicitly loads `.env` if present and warns the user.
- Do not commit `.env` files containing real API keys to version control.
- For production use, prefer explicit `api_key` injection over implicit environment loading.
- Ensure no unrelated secrets are stored in `.env` in directories where you run this tool.