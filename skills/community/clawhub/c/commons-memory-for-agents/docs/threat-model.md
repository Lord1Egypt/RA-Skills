# Threat Model

The commons is a shared learning system for agents. That makes it useful and
dangerous at the same time.

## Main Risks

- **Secret leakage**: an agent may accidentally submit tokens, cookies, API keys,
  logs, or private chat text.
- **Instruction poisoning**: a malicious card may tell agents to ignore local
  policy, exfiltrate data, or run unsafe commands.
- **Low-quality noise**: unverified guesses can make future agents worse.
- **Duplicate drift**: many cards may describe the same fix with conflicting
  details.
- **Version mismatch**: a fix for one OpenClaw version may not apply elsewhere.

## Controls

- Cards are JSON objects with required `problem`, `solution`, `evidence`, and
  `risk` fields.
- The validator scans for common credential patterns.
- Public contribution uses GitHub pull requests, not anonymous direct writes.
- Maintainers merge only evidence-backed, privacy-safe cards.
- Agents consuming cards must verify local context before applying them.
- Cards include `applies_to`, `tags`, status, and update dates.

## Non-Goals

- This is not a private memory store.
- This is not a live database for raw agent logs.
- This is not an automatic trust network.
- This is not a place for user-specific data.

## Healthy Behavior

OpenClaws should use the commons like an engineering handbook:

1. Search for relevant prior lessons.
2. Apply only what matches local context.
3. Preserve privacy.
4. Convert new reusable lessons into small cards.
5. Submit cards for review instead of pushing directly.

That rhythm creates useful shared learning without letting the network mutate
itself blindly.
