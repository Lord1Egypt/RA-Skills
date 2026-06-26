# Setup - Brave Browser

Read this when `~/brave/` is missing or empty. Start naturally and keep the user in control.

## Your Attitude

Act like a careful browser operator.
Make the privacy and blast-radius tradeoffs explicit before changing Shields, profiles, extensions, or debugging settings.
Get the user to a working Brave state in the same session without making setup feel heavy.

## Priority Order

### 1. Integration First

Within the first exchanges, clarify activation boundaries:
- Should this skill activate whenever Brave Browser, Shields, profiles, extensions, remote debugging, or site breakage in Brave comes up?
- Should it jump in proactively when a site behaves differently in Brave than in another browser, or only on request?
- Are there situations where this skill should stay inactive, such as wallet changes, sync, or private-window workflows?

Before creating local memory files, ask for permission and explain that only durable Brave operating preferences will be kept.
If the user declines persistence, continue in stateless mode.

### 2. Map the Live Brave Environment Quickly

Capture only the facts that change behavior:
- operating system and how Brave is installed
- whether there is one daily profile, multiple profiles, or a disposable test profile
- whether the current issue is launch, site compatibility, extension conflict, or automation related
- whether remote debugging or local browser automation is allowed at all

Ask minimally, then move to the live browser task.

### 3. Lock the Safe Defaults

Align on defaults that prevent repeat incidents:
- which profiles are safe for testing versus daily use
- whether per-site Shields changes are acceptable before global changes
- whether extension debugging is allowed and under what limits
- whether cleanup may include cookies, cache, flags, or only observational checks

If uncertain, default to read-only diagnosis, per-site changes only, no remote debugging, and no destructive cleanup.

## What You Save Internally

Save only durable context:
- approved profiles and what they are used for
- OS-specific launch paths and known-good flags
- site-specific compatibility fixes worth reusing
- allowed automation posture and remote-debugging limits
- recurring incident patterns and the safest recovery order

Store data only in `~/brave/` after user consent.

## Golden Rule

Solve the immediate Brave problem first while quietly building enough durable context to make future browser work safer, faster, and less repetitive.
