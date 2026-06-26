# Repo Mapping For Chain-Referenced Shortform

Use this file when turning film-language advice into this repository's YAML and CLI.

## Map cinematic concepts to repo fields

- `dramatic beat` -> `shot.dramatic_purpose`
- `performance read` -> `shot.emotional_state`
- `shot size / composition baseline` -> `shot_template.framing`
- `blocking and floor marks` -> `shot_template.blocking_rules`
- `allowed shot-specific change` -> `shot.allowed_changes`
- `forbidden shot-specific drift` -> `shot.forbidden_changes`
- `must keep visible` -> `shot.must_show` and `shot.must_not_hide`
- `bad framing patterns` -> `shot.forbidden_compositions`
- `lens or camera feel` -> `dimensions.camera_optics.text`
- `time-of-day or scene-state shift` -> `dimensions.temporal_state.text`
- `master-scene locked atmosphere` -> `scene_pack.dimensions.*`
- `explicit shot planning` -> `shot.shot_card.*`

## How to encode a shot card

Convert a shot card like this:

- beat: realization
- shot size: MCU
- angle: eye level
- movement: slow push-in
- blocking: actor stops at shelf, looks right, hand enters frame
- screen direction: left-to-right
- must show: report folder, aisle sign

Into repo-friendly fields like this:

- `dramatic_purpose`: `"realization at the shelf after noticing the report folder"`
- `emotional_state`: `"suspicion tightening into certainty"`
- `shot_template.framing`:
  - `"medium close-up baseline"`
  - `"same side of line as prior shot"`
- `shot_template.blocking_rules`:
  - `"actor lands on the same floor mark near the shelf"`
  - `"report folder remains readable in frame once touched"`
- `shot.allowed_changes`:
  - `"slow push-in as realization lands"`
  - `"right hand reaches toward the report folder"`
- `shot.must_show`:
  - `"report folder"`
  - `"aisle sign"`
- `shot.forbidden_compositions`:
  - `"crossing the line"`
  - `"folder fully occluded during the reach"`
- `shot.shot_card`:
  - `beat: "realization at the shelf"`
  - `shot_size: "MCU"`
  - `angle: "eye level"`
  - `movement: "slow push-in"`

## CLI surfaces

- `uv run aivideo print-shot-card <spec> <shot_id>`
- `uv run aivideo print-continuity-ledger <spec>`
- `uv run aivideo init-continuity-ledger <spec>`

Search and render also write `continuity_ledger.json` into the episode artifact directory.

## When to change packs vs shot text

- Change `scene_pack` when geography or lighting is unstable.
- Change `prop_pack` when objects drift or appear/disappear incorrectly.
- Change `shot_template` when staging rules repeat across many shots.
- Change per-shot fields when only one beat or move is changing.

## Prompt pollution reminder

Do not put these back into shot-delta text if they are already locked elsewhere:

- full character appearance
- full wardrobe description
- room layout
- fixed prop inventory
- baseline lighting rig

In this repo, better structure beats more descriptive density.
