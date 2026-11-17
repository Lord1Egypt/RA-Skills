# Channel preflight

Do this before starting a generation run, every single time.

## Tool definitions lie about availability

A channel's tool definitions can be **fully present in your tool list** while the channel is not mounted. Calling it then fails.

Consequence: **presence in the index proves nothing.** Verify by calling.

Use a zero-cost probe — a call that fails on auth or returns an empty result is enough to prove the tool is mounted and callable. Read the error carefully:

- an auth or argument error means **mounted**
- "not found in the tool index" means **not mounted**

## Availability is per-session

A channel that was available yesterday may not be mounted today, in the same environment, in the same mode. This was observed directly: available on one date, unavailable on a later date under identical conditions.

**Re-probe every session.** Never carry a previous session's result forward as the current state.

## If it is not available

**Stop and report the blocker.** Do not route around it:

- do not fall back to a different provider
- do not substitute a different capability
- do not start the run on the assumption it will be available later

If a channel has been explicitly banned for this project, it stays banned. It is not a fallback.

## Credentials are not availability

Obtaining a token or passing a credential check does not mean the tool is mounted. Credential validity and channel availability are separate facts. Do not use one as evidence for the other.

## Balance

Check remaining balance before the run, not after. Generation spend is per-second or per-image and a single large run can consume most of a small balance. Report the cost before spending it if it is a significant fraction of what remains.

## Preflight summary

```
[ ] required channel probed this session — callable, not just listed
[ ] balance checked and cost estimated
[ ] cost reported before the run if it is a large fraction of the remainder
[ ] fallback plan agreed, or explicitly: stop on failure
```
