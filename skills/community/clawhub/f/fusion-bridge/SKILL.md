---
name: fusion-bridge
description: Use the Fusion 360 Bridge to inspect or control Autodesk Fusion 360 over HTTP from OpenClaw. Use this skill when interacting with the Fusion Bridge add-in, `/ping` `/state` `/logs` `/exec`, raw Python execution, or helper-style Fusion automation.
license: MIT
metadata: {"openclaw":{"project":"fusion-360-bridge","source":"https://github.com/smicbee/fusion-360-bridge"}}
---

# Fusion Bridge

Use this skill when interacting with a Fusion 360 Bridge environment.

## Quick start

1. This skill is tied to the **official Fusion 360 Bridge repository**:
   - `https://github.com/smicbee/fusion-360-bridge`
   - Use this repo as the source of truth for both the add-in and the OpenClaw plugin.
2. Install the Fusion add-in:
   - Option A (preferred): `git clone https://github.com/smicbee/fusion-360-bridge.git`
   - Option B: download the repository ZIP from GitHub Releases.
   - Copy `fusion-addin/FusionBridge` into your Fusion add-ins directory:
     - Windows: `%appdata%\\Autodesk\\Autodesk Fusion\\API\\AddIns\\`
     - macOS: `~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/`
3. Install the OpenClaw plugin from the same repo:
   ```bash
   openclaw plugins install --link <path-to-repo>/openclaw-plugin
   ```
4. Start/launch Fusion 360 add-in (`FusionBridge`) and verify it is running.
5. Check `GET /ping` first, then `GET /state`.
6. Prefer helper-style snippets for common tasks.
7. Keep raw Python as the fallback whenever a helper is missing or too limiting.

### Network requirement for OpenClaw

The bridge listens on TCP port `8765` (inside the repo: `0.0.0.0:8765` by default).
OpenClaw must be able to reach this host/port from the machine it runs on.

## Workflow

### 1. Verify bridge health

Check these in order:
- `/ping`
- `/state`
- `/logs` if something looks wrong

If the bridge is not reachable remotely but works locally, suspect bind-address or host firewall.

### 2. Choose execution style

Use one of these two modes:

- **Helper-style Python** for repeatable tasks like listing components, showing messages, creating simple geometry, or reading document info.
- **Raw Python** when the task is custom, exploratory, or needs full Fusion API power.

Do not force a DSL when raw Python is the better fit.

### 3. Send code with `/exec`

`POST /exec` accepts:
- `code` as a Python string
- optional `timeoutSeconds`

Current rule for this bridge:
- raw Python is allowed
- code length is not artificially capped
- execution time is capped at **300 seconds**

## Modeling strategy for future CAD work

When building or modifying geometry through the bridge, prefer this order:

1. **Read the sketch carefully and restate the model in words first**
   - body size
   - hole positions
   - top/bottom feature intent
   - symmetry or non-symmetry
   - explicit uncertainties

2. **Convert all dimensions into one unit system before coding**
   - for this bridge/Fusion API flow, use centimeters in code when working with `createByReal(...)`
   - say the millimeter values back to the user before building if there is ambiguity

3. **Build in layers, not in one giant script**
   - base body
   - hole pattern
   - top-side features
   - bottom-side features
   - final cleanup/visibility

4. **Verify after each layer with machine-readable output**
   - print/result body names
   - inspect body count
   - inspect bounding boxes or face counts if needed
   - use `/logs` when behavior is surprising

5. **Avoid blocking popups during the middle of a long build**
   - use `print(...)` and `result = ...` during the build
   - only use `ui.messageBox(...)` at the end or for deliberate checkpoints

6. **Prefer robust geometry operations over elegant but fragile ones**
   - if a direct Hole/Extrude/Cut API path behaves inconsistently in the current Fusion build, fall back to more reliable construction methods
   - prioritize “works reliably on this machine” over ideal API purity

7. **Keep old attempt bodies from confusing review**
   - rename the newest intended body clearly
   - hide old experiment bodies after a successful iteration
   - do not assume visual output is wrong until old overlapping bodies are ruled out

8. **Use helper functions for repetitive work, but keep raw Python available**
   - helpers for common tasks
   - raw Python for custom geometry or API workarounds

## Lessons learned from the Peroxo disc modeling session

Use these rules when a user iteratively describes a small rotational part with recesses/pads from photos.

### 1. Freeze known-good milestones

- When the user says a state is correct, treat that body as a checkpoint.
- Keep the checkpoint body visible or easy to restore by name.
- For this session, `Peroxo_Disc_V9` became the accepted rollback point.
- When experimenting after a confirmed checkpoint, prefer creating a new body/version instead of mutating the accepted one too aggressively.

### 1b. Prefer photos plus concrete verbal descriptions

- Ask for photos from multiple angles whenever the geometry is not fully obvious.
- Treat good plain-language descriptions as first-class modeling input, not just measurements.
- Specifically ask about:
  - which face is front/back/top/bottom
  - whether a feature is a recess or a protrusion
  - whether a hole is blind or through
  - whether arcs/roundings bulge inward or outward
- If the user can provide both images and concise descriptions, use both; that combination is much more reliable than either one alone.

### 2. Separate "blind recess" from "through-hole"

Do not collapse these into one feature unless the user explicitly says they are the same.

For stepped hole language like:
- "the first hole stops before the bottom plate"
- "in the bottom plate there is another 5 mm hole that goes completely through"

model it as:
- one **blind recess** from the top
- one **separate through-hole** in the remaining bottom plate

Restate that distinction back to the user before coding if there is any ambiguity.

### 3. Verify geometry, not just intent

After each critical operation, inspect the resulting body instead of assuming the feature landed correctly.

Useful checks:
- bounding box changed in the expected direction
- expected cylindrical face radius exists
- expected planar face exists at the intended offset
- old bodies are hidden so visuals are not misleading

For example:
- an obround pad extruded on the wrong face may leave the outer bounding box unchanged
- a "5 mm hole" may be missing even if the script succeeded; verify a cylinder with radius `0.25 cm` exists

### 4. Be careful with Fusion face orientation and axes

In this environment, revolve/extrude results may not line up with the intuitive axis you first imagine.

Do not assume:
- `PositiveExtentDirection` always means "outward"
- the obvious top/bottom face is still planar after multiple edits
- the sketch plane orientation matches your mental picture

Instead:
- inspect the body's bounding box before/after
- inspect planar face origins/normals
- inspect cylinder axes/radii
- if needed, create only the sketch first, let the user confirm it, then extrude

Concrete rule from the Peroxo session:
- after extruding a rear pad/boss, immediately verify the body's rear-most extent changed in the intended direction
- for this kind of part, the accepted manual correction showed the rear pad extends to about `y = -0.25 cm`, while the main bottom-plate plane sits at about `y = -0.1 cm`
- if the bounding box stays unchanged, the pad did not land on the exterior
- if the pad grows in the opposite direction, stop and inspect the actual rear-most planar face instead of retrying the same sign blindly
- when a user manually corrects the direction in Fusion, inspect the resulting face origins/areas and encode that pattern into the next attempt
- do not stop at "which way is outward"; also identify **which plane is the reference plane for the feature**
- in this session, the crucial mistake was extruding from the wrong rear plane even after inspecting the normal correctly
- for multi-level backsides, distinguish explicitly between:
  - main body bottom plane
  - intermediate rear plane(s)
  - outermost boss/pad plane
- when the user manually fixes the part, measure those plane levels and preserve that stack instead of re-deriving it from memory

### 5. For obround/capsule pads, confirm the sketch before extrusion

For rear pads shaped like an obround/capsule:
- sketch first
- verify the top arc bulges toward the top and the bottom arc toward the bottom
- only then extrude

A reliable pattern is:
- draw the two straight side lines
- draw the top arc with an explicit top midpoint
- draw the bottom arc with an explicit bottom midpoint
- include the center reference hole in the sketch if it helps review

In this session, naming the sketch (`Peroxo_rear_obround_sketch`) and getting user confirmation before extrusion prevented more guesswork.

### 6. Mutate less once geometry gets dirty

After several cuts/joins, faces may become torus/NURBS fragments and stop being easy to target.

When that happens:
- stop patching the same body repeatedly
- rebuild a fresh clean version from the last confirmed interpretation
- keep the old body hidden for fallback

This is often faster and safer than trying to repair heavily fragmented topology.

### 7. Prefer narrow changes after user correction

When the user says:
- "only change the pad"
- "go back to the state before that"
- "leave the outer shape alone"

make the smallest possible change.

Do not combine unrelated fixes in one step. In particular, do not simultaneously:
- change side-wall height
- reinterpret the hole structure
- and modify the rear pad

unless the user explicitly asked for all three.

## Operating rules

- Treat the bridge as **open inside a trusted environment**.
- Prefer concise snippets, but allow large scripts when needed.
- When debugging, inspect `/logs` before making architectural guesses.
- When testing UI behavior, sending `ui.messageBox(...)` through `/exec` is valid and useful.
- If remote access fails while local access works, check whether the bridge is bound to LAN and whether Windows Firewall is blocking port `8765`.

## Known environment facts

- The bridge exposes `/state` including `pumpMode`, `queueSize`, and `busy`.
- Default runtime port is `8765`.
- The exposed tools are `GET /ping`, `GET /state`, `GET /logs`, and `POST /exec`.


## Read these references when needed

- For endpoint contract and timeout behavior: `references/api.md`
- For practical request patterns and ready-to-send snippets: `references/recipes.md`

## Response style for future use

When using this skill later:
- first confirm reachability quickly
- then act, instead of re-explaining the whole architecture
- mention helper-style options, but preserve raw Python as the default escape hatch

## OpenClaw Plugin integration

This repository also ships an OpenClaw plugin at `openclaw-plugin/` and it must be used with the same Fusion Bridge repo above.
When installed, prefer these tool names instead of manually calling endpoints:

- `fusion_bridge_ping`
- `fusion_bridge_state`
- `fusion_bridge_logs`
- `fusion_bridge_exec`

Install from the same source:

```bash
cd <path-to-fusion-360-bridge>
openclaw plugins install --link ./openclaw-plugin
```

Example assumptions for plugin use:
- `baseUrl` points to the machine running Fusion 360 (default `http://localhost:8765`).
- If running remote, that machine must be reachable on TCP port `8765`.
