# End-to-End Orchestration

This reference is the execution runbook from script creation to generated video. It does not replace creative judgment or paid-generation approval.

## Phase 0 — Project profile

Input: premise, IP, audience, platform, canvas, episode count, duration.
Output: `project_profile.json`.

Gate:

- owner/copyright recorded;
- character references and rights recorded;
- model adapters filled;
- no API keys or secrets in the profile.

## Phase 1 — Story development

Create:

- story spine: promise, want, need, flaw, pressure, price, payoff;
- character logic and relationship map;
- season arc and three serialization engines;
- episode matrix with causal bridges;
- setup/payoff ledger.

Output:

- `01_story/series_bible.md`
- `01_story/episode_matrix.csv`
- `01_story/scripts/`
- `01_story/continuity_ledger.csv`

Gate:

- every episode changes knowledge, power, relationship, safety, ownership, identity, or moral position.

## Phase 2 — Scene and retention design

Create:

- scene breakdown with objective, obstacle, tactic, turn, exit;
- retention plan with opening question, midpoint turn, cliffhanger, payoff, comment prompt, shareable moment and next-episode tease.

Output:

- `01_story/scene_breakdown.csv`
- `01_story/retention_plan.csv`

Gate:

- `audit_retention.py` passes;
- cliffhanger types rotate;
- every open loop has a payoff plan.

## Phase 3 — Visual and character lock

Create:

- canvas and safe area;
- character anchors, outfit IDs and references;
- scene and prop bibles;
- technique plan: storytelling mode, staging mode, transition family, hero VFX, recurring motif;
- cover copy and packaging direction.

Output:

- `02_visual_bible/`
- `03_characters/character_registry.csv`
- `04_scenes/scene_registry.csv`
- `05_props/prop_registry.csv`

Gate:

- keyframes and character references approved before paid generation.

## Phase 4 — Shot manifest

Create a row for every shot:

- story function, coverage role, POV;
- shot size, camera intention, camera move, subject motion;
- eyeline, screen direction, axis, light direction;
- character/outfit/prop IDs;
- transition, VFX level, sound transition;
- prompt, reference URLs/IDs, duration, model, ratio, resolution.

Output:

- `06_shots/shot_manifest.csv`

Gate:

- all durations valid;
- prompts non-empty;
- every shot has a reference plan;
- coverage and continuity checks pass.

## Phase 5 — Generation preflight

Run:

```bash
python scripts/validate_project.py <project-dir>
python scripts/audit_retention.py <project-dir>/01_story/retention_plan.csv
python scripts/build_seedance_tasks.py --shot-manifest <csv> --project-profile <json> --output <jsonl>
python scripts/seedance_client.py dry-run --tasks <jsonl>
```

Inspect:

- number of tasks;
- durations and resolution;
- reference URLs/Base64/asset IDs;
- task limit;
- expected queue time;
- budget exposure.

Do not submit paid tasks yet.

## Phase 6 — Paid generation

After explicit approval:

```bash
python scripts/seedance_client.py submit --tasks <jsonl> --state <state.json> --output-dir <raw-dir> --execute --confirm-paid --limit <n> [--embed-local-refs]
```

The client must:

- require `ARK_API_KEY`;
- require both execute and confirmation flags;
- stop at the explicit task limit;
- resolve `meta.reference_paths` to Base64 only when `--embed-local-refs` is explicitly set;
- store provider task IDs and status;
- never store API keys in state files.

## Phase 7 — Poll and download

```bash
python scripts/seedance_client.py poll --state <state.json> --download-dir <raw-dir>
```

Review:

- status and failure reason;
- character drift;
- costume/prop/light continuity;
- action and camera intention;
- safety/compliance;
- selected take and rejected-take reason.

## Phase 8 — Voice, subtitles, lip-sync

- lock voice bible and pronunciation;
- generate/record dialogue;
- time subtitles to final audio;
- force-align or lip-sync per shot;
- check drift;
- create clean and watermarked masters.

## Phase 9 — Edit and delivery

- conform selected takes;
- trim and retime;
- color-match;
- sound design and mix;
- add post typography, copyright watermark and AI label;
- export platform masters;
- run `validate_project.py`;
- write hashes and delivery manifest;
- archive raw, selected, final and state files.

## Stop conditions

Stop and ask the user when:

- account balance or API permission fails;
- a task requires more than the approved limit;
- three attempts fail the same invariant;
- a character/rights conflict appears;
- subtitles or lip-sync require a change to locked dialogue;
- delivery would overwrite an approved master.

## Minimum command path

`scaffold` → fill profile → write story/scene/retention → lock characters → build shot manifest → validate → audit retention → build tasks → dry-run → explicit paid submit → poll/download → voice/subtitles/lip-sync → edit → validate → package.
