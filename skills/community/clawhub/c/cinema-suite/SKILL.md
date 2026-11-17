---
name: cinema-suite
description: Production cinema ticketing catalog that maps cinema identities to installable OpenClaw mode capabilities for capture, replay, coupon binding, and failure handling.
---

# Cinema Suite

Cinema Suite is the installable catalog for Cinema Agent. It turns the production ticket-channel configuration into deterministic, redacted Skill entries. Use it when an order, capture session, or replay request must be routed to the correct cinema and mode package. The host provides scheduling, routing, browser/capture APIs, and event publication; this Skill supplies the cinema-to-capability mapping.

## What this release contains

This release contains **63 cinema entries** and **10 mode mappings** (version `1.1.0`). The source is `/api/merchant/chupiaoChanne/list` in the `prod` environment, selected as `merchant-enabled`. The manifest is redacted: it contains no login password, session token, cookie, uuid, authorization header, or raw private payload.

## Mode capability map

| Mode | Installable package | Capabilities | Status |
| --- | --- | --- | --- |
| `wxamp_mode_5` | `clawhub:@rascalagnt001/wxamp-mode-5` | capture, replay, coupon, failure | plugin_required |
| `wxamp_mode_4/mode_a` | `clawhub:@rascalagnt001/wxamp-mode-4-a` | capture, replay, coupon, failure | supported |
| `wxamp_mode_1` | `clawhub:@rascalagnt001/wxamp-mode-1` | capture, replay, coupon, failure, pageWorld | supported |
| `wxamp_mode_7` | `clawhub:@rascalagnt001/wxamp-mode-7` | capture, replay, coupon, failure, pageWorld | supported |
| `wxamp_mode_6` | `clawhub:@rascalagnt001/wxamp-mode-6` | capture, replay, coupon, failure, pageWorld | supported |
| `wxamp_mode_8` | `clawhub:@rascalagnt001/wxamp-mode-8` | capture, replay, coupon, failure, pageWorld | supported |
| `wxamp_mode_9` | `clawhub:@rascalagnt001/wxamp-mode-9` | capture, replay, coupon, failure, pageWorld | supported |
| `wxamp_mode_10` | `clawhub:@rascalagnt001/wxamp-mode-10` | capture, replay, coupon, failure, pageWorld | supported |
| `wxamp_mode_11` | `clawhub:@rascalagnt001/wxamp-mode-11` | capture, replay, coupon, failure | supported |
| `wxamp_mode_4/mode_b` | `clawhub:@rascalagnt001/wxamp-mode-4-b` | capture, replay, coupon, failure | supported |

Install the mode package referenced by an entry before dispatching that entry: `openclaw plugins install <openclawPackage>`, e.g. `openclaw plugins install clawhub:@rascalagnt001/wxamp-mode-6`. A `plugin_required` status means the catalog entry is valid but its executable mode Skill must be installed separately.

## Entry contract

Each entry in `cinema-suite.json` contains:

- `skillId`: long-lived compatibility identity. It is reused across releases for the same channel/mode/business identity.
- `skillKey`: ASCII-only lookup key for SQL, URLs, and routing. Use this field for links; do not use punctuation in database keys.
- `chupiaoChannel`: backend ticket-channel code used to select authorization and capture data.
- `mode` and optional `businessMode`: executable mode package selection.
- `appId` or `weixinMpLink`: public target identity required by the selected mini-program or H5 flow.
- `capabilities`: declared operations such as `capture`, `replay`, `coupon`, `failure`, and `pageWorld`.

Example entries from this release:

- `cinema_c_wanda` (万达): mode `wxamp_mode_5`, channel `c_wanda`
- `cinema_c_happyblue` (幸福蓝海): mode `wxamp_mode_4`, channel `c_happyblue`
- `cinema_c_star` (星轶影城): mode `wxamp_mode_1`, channel `c_star`

## Runtime workflow

1. Resolve an order's `chupiaoChannel`, `mode`, and `businessMode` to one entry by `skillKey`.
2. Confirm the referenced mode package is installed and exposes the declared capabilities.
3. Pass only the order data and public identity parameters required by that capability to the host bridge. Do not copy credentials into the suite manifest.
4. Let the host schedule capture/replay work and publish lifecycle events; the mode Skill performs business-specific encryption, coupon binding, page-world actions, and failure formatting.
5. Persist the stable `skillId` with the order so later retries continue to resolve the same cinema identity.

## Updating and safety

Generate a new release from the production merchant endpoint, review the resulting manifest, pack it, and install the new version alongside the previous one. Existing identifiers are retained when the same channel and mode identity reappears. If the endpoint returns no enabled merchant channels, the generator records the explicit system-catalog fallback in `source.selection`; consumers must treat those entries as catalog definitions until the merchant enables them. Never treat this package as a credential store.

## Package files

- `cinema-suite.json`: machine-readable catalog and installation contract.
- `openclaw.plugin.json`: OpenClaw discovery metadata.
- `SKILL.md`: this operational contract.
- `README.md`: release and security summary.
