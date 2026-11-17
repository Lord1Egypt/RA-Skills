#!/usr/bin/env python3
"""Local mirror of the server-side grounding quality gate.

Validates a brief and, only if it passes, prints the ack request body as JSON on
stdout. It NEVER performs any network call: piping the output to curl is a
separate, explicit step you control.

    python3 brief-gate.py <card_id> <payload.json> <prompt.txt> > body.json

Exit codes:
    0  gate green, body on stdout
    1  gate red (or bad input) - message on stderr, nothing produced

Why this exists twice (here and on the server): failing locally costs no network
call and gives a readable message; the server must re-check because it cannot
assume its client is polite.

Configure the mandated first line through the environment, so an update of this
skill never overwrites your value:

    export BRIEF_GATE_PREFIX="Read CLAUDE.md AND AGENTS.md at the root of app-example first"

It must be byte-identical to the string your server checks with startsWith().
"""
import json
import os
import sys

PREFIX_TEMPLATE = "Read CLAUDE.md AND AGENTS.md at the root of ${TARGET_REPO} first"
MIN_CHARS = 3000
TARGET_RANGE = (10_000, 16_000)


def die(msg):
    print("brief-gate: %s -- NOTHING was sent." % msg, file=sys.stderr)
    raise SystemExit(1)


def mandated_prefix():
    value = os.environ.get("BRIEF_GATE_PREFIX", PREFIX_TEMPLATE)
    # Fail CLOSED on an empty prefix. `export BRIEF_GATE_PREFIX="$SOME_UNSET_VAR"` in a cron
    # env yields "", and str.startswith("") is True for every input: the gate would accept
    # any first line while still reporting green. An unset gate must never look like a passed one.
    if not value.strip():
        die("BRIEF_GATE_PREFIX is empty. Refusing to run: an empty prefix matches every "
            "prompt, which would disable the mandated-first-line gate instead of enforcing it")
    if "${TARGET_REPO}" in value or "<target-repo>" in value:
        die("BRIEF_GATE_PREFIX still holds the repo placeholder. Export it with your "
            "repo name substituted, byte-identical to the string your server checks, "
            "e.g. 'Read CLAUDE.md AND AGENTS.md at the root of app-example first'")
    return value


def main(argv):
    if len(argv) != 4:
        die("usage: brief-gate.py <card_id> <payload.json> <prompt.txt>")
    card_id, payload_path, prompt_path = argv[1], argv[2], argv[3]
    prefix = mandated_prefix()

    try:
        with open(payload_path, encoding="utf-8") as fh:
            payload_in = json.load(fh)
    except OSError as exc:
        die("cannot read payload: %s" % exc)
    except json.JSONDecodeError as exc:
        die("payload is not valid JSON: %s" % exc)
    if not isinstance(payload_in, dict):
        die("payload.json must be a JSON object")

    try:
        with open(prompt_path, encoding="utf-8") as fh:
            prompt = fh.read()
    except OSError as exc:
        die("cannot read prompt: %s" % exc)

    # Send only the keys you actually have. Blanking an absent key to "" would make the ack's
    # non-destructive merge destructive from the client side: a payload carrying just
    # technical+definition would overwrite an already-grounded `context` with emptiness.
    payload = {key: str(value)
               for key in ("context", "impact", "definition", "technical", "risks", "title")
               for value in [payload_in.get(key)] if value}

    # --- the gate: same predicate as the server, in the same canonical order:
    #     prefix -> length -> technical -> definition ---
    if not prompt.startswith(prefix):
        die("prompt must start EXACTLY with the mandated prefix %r" % prefix)
    if len(prompt) < MIN_CHARS:
        die("prompt too short (%d < %d chars). Flesh out the brief: target %d-%d"
            % (len(prompt), MIN_CHARS, TARGET_RANGE[0], TARGET_RANGE[1]))
    for gated in ("technical", "definition"):
        # .get, not []: an absent key is now genuinely absent from `payload`, and absent must
        # fail the gate exactly like empty -- never raise, never pass.
        if not payload.get(gated, "").strip():
            die("payload.%s is missing or empty" % gated)

    if not TARGET_RANGE[0] <= len(prompt) <= TARGET_RANGE[1]:
        print("brief-gate: note - prompt is %d chars, outside the %d-%d target (gate still green)"
              % (len(prompt), TARGET_RANGE[0], TARGET_RANGE[1]), file=sys.stderr)

    json.dump({"card_id": card_id, "payload": payload, "prompt": prompt},
              sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
