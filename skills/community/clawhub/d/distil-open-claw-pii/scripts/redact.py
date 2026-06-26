"""PII redaction script using a local llama.cpp server.

Sends text to the Distil-PII model running on localhost:8712 and prints
the redacted JSON to stdout. Uses only the Python standard library.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

SERVER_URL = "http://localhost:8712/v1/chat/completions"

SYSTEM_PROMPT = """\
You are a problem solving model working on task_description XML block:
<task_description>
Produce a redacted version of texts, removing sensitive personal data while preserving operational signals. The model must return a single json blob with:

* **redacted_text** is the input with minimal, in-place replacements of redacted entities.
* **entities** as an array of objects with exactly three fields {value: original_value, replacement_token: replacement, reason: reasoning}.

## What to redact (-> replacement token)

* **PERSON** -- customer/patient/person names (first/last/full; identifying initials) -> `[PERSON]`
* **EMAIL** -- any email, including obfuscated `name(at)domain(dot)com` -> `[EMAIL]`
* **PHONE** -- any international/national format (separators/emoji bullets allowed) -> `[PHONE]`
* **ADDRESS** -- street + number; full postal lines; apartment/unit numbers -> `[ADDRESS]`
* **SSN** -- US Social Security numbers -> `[SSN]`
* **ID** -- national IDs (PESEL, NIN, Aadhaar, DNI, etc.) when personal -> `[ID]`
* **UUID** -- person-scoped system identifiers (e.g., MRN/NHS/patient IDs/customer UUIDs) -> `[UUID]`
* **CREDIT_CARD** -- 13-19 digits (spaces/hyphens allowed) -> `[CARD_LAST4:####]` (keep last-4 only)
* **IBAN** -- IBAN/bank account numbers -> `[IBAN_LAST4:####]` (keep last-4 only)
* **GENDER** -- self-identification (male/female/non-binary/etc.) -> `[GENDER]`
* **AGE** -- stated ages ("I'm 29", "age: 47", "29 y/o") -> `[AGE_YEARS:##]`
* **RACE** -- race/ethnicity self-identification -> `[RACE]`
* **MARITAL_STATUS** -- married/single/divorced/widowed/partnered -> `[MARITAL_STATUS]`

## Keep (do not redact)

* Card **last-4** when only last-4 is present (e.g., "ending 9021").
* Operational IDs: order/ticket/invoice numbers, shipment tracking, device serials, case IDs.
* Non-personal org info: company names, product names, team names.
* Cities/countries alone (redact full street+number, not plain city/country mentions).

## Output schema (exactly these fields)
* **redacted_text** The original text with all the sensitive information replaced with redacted tokens
* **entities** Array with all the replaced elements, each element represented by following fields
  * **replacement_token**: one of `[PERSON] | [EMAIL] | [PHONE] | [ADDRESS] | [SSN] | [ID] | [UUID] | [CREDIT_CARD] | [IBAN] | [GENDER] | [AGE] | [RACE] | [MARITAL_STATUS]`
  * **value**: original text that was redacted
  * **reason**: brief string explaining the rule/rationale
</task_description>
You will be given a single task with context in the context XML block and the task in the question XML block
Solve the task in question block based on the context in context block.
Generate only the answer, do not generate anything else"""

USER_PROMPT_TEMPLATE = """\
Now for the real task, solve the task in question block based on the context in context block.
Generate only the solution, do not generate anything else
<context>
{text}
</context>
<question>Redact provided text according to the task description and return redacted elements.</question>"""


def main(text: str, show_entities: bool = False):
    """Send text to the local Distil-PII model and print the redacted JSON."""
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "pii_redaction",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "redacted_text": {"type": "string"},
                    "entities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "replacement_token": {"type": "string"},
                                "reason": {"type": "string"},
                            },
                            "required": ["value", "replacement_token", "reason"],
                        },
                    },
                },
                "required": ["redacted_text", "entities"],
            },
        },
    }

    payload = json.dumps({
        "model": "distil-pii",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)},
        ],
        "temperature": 0,
        "response_format": response_format,
    }).encode()

    req = urllib.request.Request(
        SERVER_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.URLError:
        print(
            "ERROR: Could not connect to llama-server at localhost:8712.\n"
            "Run 'bash scripts/setup.sh' first to download the model and start the server.",
            file=sys.stderr,
        )
        sys.exit(1)

    content = result["choices"][0]["message"]["content"]
    if show_entities:
        print(content)
    else:
        parsed = json.loads(content)
        print(parsed["redacted_text"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redact PII from text using a local Distil-PII model.")
    parser.add_argument("text", nargs="*", help="Text to redact (or pipe via stdin)")
    parser.add_argument("--show-entities", action="store_true",
                        help="Output full JSON with entities (default: redacted text only)")
    args = parser.parse_args()

    if args.text:
        input_text = " ".join(args.text)
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    else:
        parser.print_usage(sys.stderr)
        sys.exit(1)

    if not input_text:
        print("ERROR: No text provided.", file=sys.stderr)
        sys.exit(1)

    main(text=input_text, show_entities=args.show_entities)
