# Distil PII Redactor - OpenClaw Skill

Locally redact PII from text using a fine-tuned 1B parameter model. Your sensitive data never leaves your machine -- the frontier LLM powering OpenClaw never sees the raw text. Only the local model processes it, and only the redacted output is returned.

## Prerequisites

- **llama.cpp** installed (`brew install llama.cpp` on macOS, or [build from source](https://github.com/ggerganov/llama.cpp#build))
- **Python 3**
- **~5 GB disk space** for the GGUF model

## Install from ClawHub

```bash
clawhub install distil-open-claw-pii
```

Or install directly in your OpenClaw chat:

```
/install distil-open-claw-pii
```

## Quick Start with OpenClaw

1. Install the skill (see above), or copy this folder to `~/.openclaw/skills/distil-pii-redactor/`

2. Tell OpenClaw: **"set up the PII redactor"**
   (this downloads the model and starts the local server)

3. Use it: **"redact this: Hi I'm John Smith, john@smith.com, call me at 555-123-4567"**

## Standalone Usage (without OpenClaw)

```bash
# One-time setup: download model + start server
bash scripts/setup.sh

# Redact text (via argument or stdin)
python scripts/redact.py "Hi, I'm John Smith. Reach me at john.smith@example.com or 555-123-4567."
cat examples/sample_input.txt | python scripts/redact.py

# Stop the server when done
bash scripts/stop.sh
```

## Example

**Input** ([examples/sample_input.txt](examples/sample_input.txt)):
```
Hi, my name is Sarah Johnson and I need help with my recent order #ORD-29481.

You can reach me at sarah.johnson@gmail.com or call me at +1 (415) 555-7823.
I'm a 34-year-old married woman living at 742 Evergreen Terrace, Apt 3B,
Springfield, IL 62704.

My credit card ending in 4111 1111 1111 1234 was charged twice. My SSN is
198-76-5432 and my patient ID is MRN-00284713. My IBAN is
GB29 NWBK 6016 1331 9268 19.

Please resolve this as soon as possible. I'm a long-time customer of Acme Corp
and I expect better service.
```

**Output** (default -- redacted text only):
```
Hi, my name is [PERSON] and I need help with my recent order #ORD-29481.

You can reach me at [EMAIL] or call me at [PHONE]. I'm a [AGE_YEARS:34]-year-old
[MARITAL_STATUS] woman living at [ADDRESS].

My credit card ending in 4111 1111 1111 1234 was charged twice. My SSN is [SSN]
and my patient ID is [UUID]. My IBAN is [IBAN_LAST4:6819].

Please resolve this as soon as possible. I'm a long-time customer of Acme Corp
and I expect better service.
```

To see which entities were detected, add `--show-entities` for the full JSON output (see [examples/sample_output.json](examples/sample_output.json)).

## Supported PII Types

| Type | Replacement Token | Example |
|------|-------------------|---------|
| Person names | `[PERSON]` | John Smith |
| Email addresses | `[EMAIL]` | john@example.com |
| Phone numbers | `[PHONE]` | 555-123-4567 |
| Street addresses | `[ADDRESS]` | 123 Main St, Apt 4B |
| Social Security numbers | `[SSN]` | 123-45-6789 |
| National IDs | `[ID]` | PESEL, NIN, Aadhaar |
| System identifiers | `[UUID]` | Patient/customer IDs |
| Credit cards | `[CARD_LAST4:####]` | Last 4 digits preserved |
| IBANs | `[IBAN_LAST4:####]` | Last 4 digits preserved |
| Gender | `[GENDER]` | male, female, non-binary |
| Age | `[AGE_YEARS:##]` | "I'm 29 years old" |
| Race/ethnicity | `[RACE]` | Self-identification |
| Marital status | `[MARITAL_STATUS]` | married, single, etc. |

## Alternative Models

The default model is the 1B parameter version. You can swap it by editing `scripts/setup.sh`:

- **[Distil-PII-Llama-3.2-3B](https://huggingface.co/distil-labs/Distil-PII-Llama-3.2-3B-Instruct-gguf)** -- higher accuracy (0.82), larger download
- **[Distil-PII-gemma-3-270m](https://huggingface.co/distil-labs/Distil-PII-gemma-3-270m-it-gguf)** -- smaller footprint (270M params), lower accuracy (0.73)

## Links

- [ClawHub: distil-open-claw-pii](https://clawhub.ai/skills/distil-open-claw-pii)
- [Distil-PII GitHub repo](https://github.com/distil-labs/Distil-PII)
- [Distil-PII HuggingFace collection](https://huggingface.co/distil-labs)
- [Distil Labs blog](https://www.distil-labs.com/blog)
