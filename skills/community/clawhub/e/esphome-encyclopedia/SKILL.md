---
name: esphome-encyclopedia
description: >-
  ESPHome configuration/component documentation-first workflow for
  ESPHome-specific questions, YAML/config authoring, config review,
  component selection, substitutions/packages usage, device definitions,
  secrets handling, OTA/update planning, build/compile troubleshooting,
  sensor/actuator tuning, logs, diagnostics, and live dashboard or node
  maintenance. Use when the request is clearly about ESPHome or an ESPHome
  node/config: ESPHome/esphome, ESP32/ESP8266 in an ESPHome context, ESPHome
  dashboards, packages, substitutions, `secrets.yaml`, OTA flashing, compile
  errors, pin assignments, Wi-Fi provisioning, or node troubleshooting. Also
  use when ESPHome YAML sections such as `sensor:`, `binary_sensor:`,
  `switch:`, `light:`, `output:`, `display:`, `climate:`, `cover:`, `wifi:`,
  `api:`, `ota:`, `logger:`, `web_server:`, `esp32:`, `esp8266:`,
  `packages:`, or `substitutions:` appear in an ESPHome configuration
  context. Do not use for generic YAML, generic embedded/microcontroller
  programming, generic Home Assistant automation, or Arduino/C++ questions
  unless they are specifically about ESPHome.
metadata: {"openclaw":{"emoji":"🔌","homepage":"https://esphome.io/components/"}}
---

# ESPHome Encyclopedia

## Overview

Use a docs-first workflow for ESPHome work. Prefer the official ESPHome component documentation index at `https://esphome.io/components/`, consult cached local copies under `.ESPHome-Encyclopedia/` before re-fetching, and record useful official-doc excerpts plus environment-specific operational learnings so future work gets faster and safer.

This skill is for the **ESPHome config/component layer**: node YAML, dashboard/node operations, and ESPHome-specific component semantics. It should not trigger for generic YAML editing, generic Home Assistant work, or general embedded programming unless ESPHome is truly the thing being discussed.

## Workflow

1. **Classify the task**
   - Decide whether the task is an ESPHome question, YAML authoring task, config review, component-selection task, troubleshooting task, or live dashboard/node task.
   - Use this skill when the task materially depends on ESPHome syntax, component semantics, supported options, build/runtime behavior, dashboard behavior, or node operations.
   - Do not use this skill for generic YAML editing, generic microcontroller work, generic Home Assistant automation, or Arduino/C++ questions unless the ESPHome layer is actually in play.

2. **Check local cache first**
   - Use `.ESPHome-Encyclopedia/` as the local knowledge/cache root.
   - Check these locations first when relevant:
     - `.ESPHome-Encyclopedia/docs/esphome.io/...`
     - `.ESPHome-Encyclopedia/notes/devices/...`
     - `.ESPHome-Encyclopedia/notes/components/...`
     - `.ESPHome-Encyclopedia/notes/patterns/...`
     - `.ESPHome-Encyclopedia/inventory/...`
   - If a cached page or note already answers the question well enough, use it.

3. **Consult official ESPHome docs before answering or touching configs/nodes**
   - Before answering direct or indirect ESPHome questions that depend on YAML syntax, component behavior, version-sensitive options, dashboard behavior, OTA/update expectations, or pin/component constraints, consult the official docs unless the answer is already well-supported by the local cache.
   - When working on ESPHome YAML, look up the docs for the exact individual components/sections in play instead of relying only on general ESPHome knowledge. If a config touches `sensor`, `binary_sensor`, `switch`, `light`, `output`, `display`, `climate`, `cover`, `wifi`, `api`, `ota`, `logger`, `web_server`, `packages`, `substitutions`, or board/platform sections, check those exact component pages so the latest supported options and nesting are used.
   - Before performing direct ESPHome configuration or dashboard/node work, consult the relevant docs first when:
     - exact option names or nesting matter
     - component behavior is easy to misremember
     - the action could affect device availability, flashing, Wi-Fi reachability, sensors, relays, pins, or OTA updates
   - Do not improvise fragile ESPHome YAML from memory when the docs are easy to check.

4. **Cache consulted docs locally**
   - When you consult an ESPHome docs page, save a normalized cache copy under `.ESPHome-Encyclopedia/docs/esphome.io/...`.
   - Mirror the official path structure as much as practical.
   - Cache only pages actually consulted; do not try to mirror the whole docs site eagerly.
   - Use `scripts/cache_doc.py` when appropriate.

5. **Separate official documentation from local observations**
   - Store official-doc-derived material under `.ESPHome-Encyclopedia/docs/...`.
   - Store environment-specific operational knowledge under:
     - `.ESPHome-Encyclopedia/notes/devices/`
     - `.ESPHome-Encyclopedia/notes/components/`
     - `.ESPHome-Encyclopedia/notes/patterns/`
     - `.ESPHome-Encyclopedia/inventory/`
   - Distinguish clearly between:
     - official documented behavior
     - observed local configuration/state
     - inferred best-practice guidance

6. **Record useful local learnings**
   - After useful live work, save durable notes such as:
     - device names and roles
     - dashboard access paths
     - repeated YAML patterns
     - board/framework gotchas
     - pin mappings and hardware quirks
     - OTA/build trouble patterns
     - safe/unsafe operational boundaries for the environment
   - Prefer concise durable notes over re-learning the same ESPHome details later.

## Live Work Rules

- Treat official docs lookup as the default preflight for non-trivial ESPHome work.
- Prefer read/inspect first when entering an ESPHome dashboard, config set, or node you have not recently reviewed.
- Treat pin changes, framework changes, package/substitution refactors, OTA/update actions, and anything that could make a node unreachable as higher-sensitivity areas.
- When uncertainty remains after checking cache + docs, say so and avoid bluffing.
- When answering a question, mention when useful whether the answer comes from cached official docs, a fresh official docs lookup, or live observed environment state.

## Data Root

Use this workspace-local root for cache and notes:

- `.ESPHome-Encyclopedia/`

Expected structure:

- `.ESPHome-Encyclopedia/docs/esphome.io/...`
- `.ESPHome-Encyclopedia/notes/devices/...`
- `.ESPHome-Encyclopedia/notes/components/...`
- `.ESPHome-Encyclopedia/notes/patterns/...`
- `.ESPHome-Encyclopedia/inventory/...`

Use `scripts/init_workspace.py` to create or repair the expected directory structure.

## Note Destinations

- Device-specific observations → `.ESPHome-Encyclopedia/notes/devices/<device-name>.md`
- Component-specific observations → `.ESPHome-Encyclopedia/notes/components/<component-name>.md`
- Reusable ESPHome patterns/gotchas → `.ESPHome-Encyclopedia/notes/patterns/<topic>.md`
- Environment-wide dashboard/access inventories → `.ESPHome-Encyclopedia/inventory/*.md`
- Cached official docs → `.ESPHome-Encyclopedia/docs/esphome.io/...`

## Secrets / Sensitive Data

- Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia notes/inventory tree.
- If a note needs to mention access details, keep it high-level and redact or omit secret material.
- Treat these workspace notes as operational memory, not as a secrets vault.

## Resources

- `scripts/init_workspace.py` — create or repair the `.ESPHome-Encyclopedia/` directory tree.
- `scripts/cache_doc.py` — fetch and cache an official ESPHome docs page under `.ESPHome-Encyclopedia/docs/...`.
- `references/workflow.md` — detailed operating workflow and evidence-handling rules.
- `references/cache-layout.md` — canonical `.ESPHome-Encyclopedia/` directory structure.
- `references/topic-map.md` — useful ESPHome topic groupings for faster official-doc lookup.

## Good Outcomes

- Answer an ESPHome question using cached or freshly checked official docs instead of guesswork.
- Inspect a live ESPHome dashboard/config set after checking the relevant docs and record any new local device/config knowledge.
- Build a growing local ESPHome knowledge cache that makes later work faster, safer, and more grounded.
- Turn one-off ESPHome discoveries into durable notes so future work does not rediscover them from scratch.

## Avoid

- Answering ESPHome-specific questions purely from memory when docs are easy to consult.
- Treating local observed node behavior as if it were guaranteed official documented behavior.
- Dumping large amounts of low-value docs into the workspace without a reason.
- Writing device-specific observations into the official-doc cache tree.
- Making device-impacting config or OTA changes before checking the relevant docs when exact behavior matters.
