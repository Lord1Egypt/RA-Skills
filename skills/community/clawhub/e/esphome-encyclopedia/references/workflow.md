# ESPHome Encyclopedia Workflow Notes

Use this file for the slightly more detailed operating pattern behind the skill.

## Default sequence

1. Identify whether the task is docs lookup, config review, troubleshooting, or live dashboard/node work.
2. Check `.ESPHome-Encyclopedia/` for already cached docs or environment notes.
3. Consult the relevant official ESPHome docs page when syntax, component options, or behavior matters.
4. Cache the page locally if it was useful.
5. Perform read/inspect-first work on live configs or nodes.
6. Record durable environment-specific notes when new knowledge is discovered.

## Read-first bias

Prefer this order before changing ESPHome configs or nodes:

1. inspect current YAML / dashboard state
2. consult official docs
3. reason about changes
4. apply the smallest safe change
5. verify node/dashboard behavior afterward

## Useful note categories

### Device notes
Capture:
- node purpose
- board/chip family
- special pins/peripherals
- OTA reliability quirks
- Wi-Fi signal/power quirks

### Component notes
Capture:
- local defaults that work well
- known-bad combinations
- version-specific gotchas
- practical tuning heuristics

### Pattern notes
Capture:
- reusable substitutions/packages structures
- naming conventions
- recovery procedures
- common troubleshooting sequences

## Suggested official-doc cache targets

Common first-wave docs worth caching when they come up:
- `/components/index.html` (treat this as the primary docs entry point)
- `/components/esphome.html`
- `/components/esp32.html`
- `/components/esp8266.html`
- `/components/wifi.html`
- `/components/api.html`
- `/components/ota.html`
- `/components/logger.html`
- the exact component pages relevant to the active devices

## Safety reminders

- Do not improvise pin assignments when the docs or current config should be checked.
- Treat OTA-affecting changes as higher sensitivity.
- Prefer exact option names and nesting from docs over memory.
- When a node may become unreachable, call that out before acting.
