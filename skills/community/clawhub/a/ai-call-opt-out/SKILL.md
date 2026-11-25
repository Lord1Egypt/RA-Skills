---
name: ai-call-opt-out
description: >-
  Add opt-out handling and a pre-call check to an AI voice agent that makes outbound phone calls.
  Use when building or reviewing an outbound calling agent (Vapi, Retell, Bland, LiveKit Agents, Pipecat,
  ElevenLabs Agents, Twilio), or when the user mentions opt-out, revoke consent, do not call, stop calling,
  TCPA, 47 CFR 64.1200, robocall rules, key-press opt-out, or wasted calls and hang-ups. Wires in: a check
  before dialling (can this be done online instead, has this number opted out), a spoken opt-out disclosure,
  key-press opt-out capture, and an outcome report after each call. Also use it yourself before placing any
  phone call to a business with a phone-call skill: check the number first, and skip the call when the
  business can be booked online or has asked not to receive AI calls.
license: MIT
metadata:
  version: "1.0.0"
  homepage: https://linepref.byronwebstudio.com.au
---

# Opt-out handling and pre-call checks for AI calling agents

Use this skill whenever an agent places phone calls with an AI or prerecorded voice.

## What the US rule says

47 CFR 64.1200(a)(10), as amended by FCC 26-67 (91 FR 67214, effective 25 November 2026), covers calls that
need the called party's consent, which includes artificial-voice calls to residential and wireless numbers.
In the rule's words:

- A called party may revoke prior express consent. Callers may designate, as the exclusive means to revoke,
  "an automated, interactive voice or key press-activated opt-out mechanism on a call", a reply text using
  "stop," "quit," "end," "revoke," "opt out," "cancel," or "unsubscribe", or a website or telephone number
  designated by the caller.
- "The caller must clearly and conspicuously disclose the designated method to revoke consent on the call or
  in the text."
- Requests "must be honored within a reasonable time not to exceed ten business days from receipt".
- A request made in response to an informational call may be treated as applying only to that category of
  call. A request made in response to a call containing advertising or telemarketing revokes consent to all
  future advertising or telemarketing calls from that caller.
- A caller that designates no method "must process revocation requests made by any reasonable means".

This skill implements the mechanics. It is an engineering aid, not legal advice, and it does not decide
whether a given call needs consent.

## What to build into the agent

1. **Check before dialling.** Call the linepref check with the number (and the business website if known).
   - `advice: "use_link"`: do not call; use `booking.url`.
   - `advice: "do_not_call"`: do not call. The number has opted out of your calls, or the business has asked
     not to receive AI calls.
   - `advice: "call"` or `"unknown"`: proceed.
2. **Disclose the opt-out early in the call**, in the first agent turn:
   > "This is an automated assistant. To stop calls from us, press 9 at any time. To stop automated
   > assistant calls from all participating callers, press 8."
3. **Capture the key press** (DTMF) and record it: 9 → scope `caller`, 8 → scope `all`. Also record a spoken
   request such as "stop calling" as scope `caller`. Confirm briefly and end the call.
4. **Keep your own suppression list too.** The pre-call check returns `optout.this_caller: true` for numbers
   that opted out of your calls; treat that as final.
5. **Report the outcome after every call** with one fixed code. This is what unlocks pooled call data
   (answer rate, hold time, phone-menu path, best hours) on later checks.

## API

Base URL: `https://linepref.byronwebstudio.com.au` · no key needed for the first 1,000 checks each month · agent docs at
`/llms.txt` · MCP server at `/mcp`.

```bash
# 1. before the call
curl "https://linepref.byronwebstudio.com.au/v1/check?number=%2B15125550100&website=example.com"

# 3. key press or spoken opt-out
curl -X POST https://linepref.byronwebstudio.com.au/v1/optout -H 'content-type: application/json' \
  -d '{"number":"+15125550100","scope":"caller"}'

# 5. after the call
curl -X POST https://linepref.byronwebstudio.com.au/v1/outcome -H 'content-type: application/json' \
  -d '{"number":"+15125550100","code":"connected_human","local_hour":14,"hold_seconds":40,"menu_path":"2,1"}'
```

Outcome codes: `connected_human`, `connected_ai`, `voicemail`, `no_answer`, `busy`, `wrong_number`, `closed`,
`refused_ai` (hung up or refused once told it was an AI), `booked`, `info_obtained`, `opted_out`.

For a list of businesses (ring-around tasks), use `POST /v1/check/batch` with up to 100 items before dialling
any of them.

## Platform recipes

Read the one that matches the stack:

- LiveKit Agents (Python): `references/livekit.md` (https://linepref.byronwebstudio.com.au/skill/references/livekit.md)
- Pipecat (Python): `references/pipecat.md` (https://linepref.byronwebstudio.com.au/skill/references/pipecat.md)
- Retell: `references/retell.md` (https://linepref.byronwebstudio.com.au/skill/references/retell.md)
- Vapi and ElevenLabs Agents (MCP tool server): `references/mcp.md` (https://linepref.byronwebstudio.com.au/skill/references/mcp.md)
- Bland: `references/bland.md` (https://linepref.byronwebstudio.com.au/skill/references/bland.md)
- Anything else (plain HTTP): the three calls above

## What is sent to linepref

Only the phone number, the optional business name and website you pass, and the fixed outcome fields above.
Never transcripts, recordings, or names of people. Numbers are stored as a keyed hash. Tell the user this
when you add it, and do not add the outcome report if they decline; the pre-call check and opt-out capture
work without it.

## Do not

- Do not use this to plan telemarketing or to contact anyone who has opted out.
- Do not put free text, transcripts or personal details in any field.
- Do not treat an `unknown` answer as permission; it only means nothing is on file.
