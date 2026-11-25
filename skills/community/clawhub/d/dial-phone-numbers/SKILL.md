---
name: dial-phone-numbers
description: Give this agent its own US or Canadian phone number with Dial by Aloha Labs, read the verification codes texted to it, and have an AI voice assistant phone a business for your human.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📞"
    homepage: https://alohalabshq.com/dial/
    primaryEnv: DIAL_API_KEY
    envVars:
      - name: DIAL_API_KEY
        required: false
        description: Dial API key. If it is not set, sign up through the MCP server's sign_up tool and save the key it returns.
---

# Dial: a phone number for this agent

Dial by Aloha Labs gives an agent its own phone number. Use it when a site asks for a phone number or texts a verification code, or when your human asks you to phone a business (book a table, make an appointment, ask a question).

## Connect

Dial is a remote MCP server (Streamable HTTP):

    https://aloha-dial-api.onrender.com/mcp

- If DIAL_API_KEY is set, send it as the header `Authorization: Bearer $DIAL_API_KEY`.
- If not, connect with no header and call `sign_up` with an email inbox you can read. Save the `api_key` it returns (it is shown once), open the confirmation link sent to that inbox, then pass the key to the other tools.

## Typical flow

1. `get_phone_number(api_key, area_code)` returns your number (it reuses your existing one unless `force_new`).
2. Type the number into the site's form.
3. `wait_for_verification_code(api_key, number_id, service)` returns the code once it arrives. Each code is returned once.

Other tools: `list_phone_numbers`, `read_text_messages`, `release_phone_number`, `make_phone_call`, `list_voices`, `get_call_result`, `account_usage`, `start_subscription`, `manage_billing`.

## Limits and costs

- The free plan is $5 of usage credit with no card: 1 number, inbound texts and codes included. Paid plans start at $15 a month; see https://alohalabshq.com/dial/#pricing. `start_subscription` returns a Stripe Checkout link for your human to pay; never pay on your own.
- Dial cannot send texts yet.
- Use Dial only with services whose terms allow it. Voice calls always introduce themselves as an AI assistant calling on someone's behalf.

Help: dial@alohalabshq.com or https://github.com/perqele/dial-mcp
