---
name: ai-short-drama-production
description: Plan and run end-to-end AI short-drama production, including workload estimation, full-chain orchestration from script creation to paid video generation, reusable project profiles, audience retention and comment loops, screenwriting logic and scene craft, episode and coverage design, cinematic technique and transition design, shot breakdown, canvas and visual bibles, character consistency, layered prompt packs, Seedance/Ark manifests, voice performance, subtitles, lip-sync, asset libraries, QC, rights, and delivery. Use for multi-episode or production-package requests, not for one-off image generation or screenplay-only work.
metadata:
  version: "1.5.0"
---

# AI Short Drama Production

Use this skill when the user wants to turn a premise, screenplay, mascot, or IP into a producible AI short-drama package or complete pipeline.

## Required outcome

A production-ready package normally contains:

- reusable project profile, scope, assumptions, rights notes, and workload estimate;
- audience promise, retention plan, story spine, character logic, episode matrix, scene map, scripts, and continuity locks;
- canvas, visual bible, character bible, scene bible, and prop bible;
- technique plan with transition family, effect budget, recurring motif, and originality check;
- shot manifest with story function, coverage role, eyelines, camera intention, prompts, references, and generation parameters;
- asset registry, naming rules, versioning, and task IDs;
- voice bible, performance beats, TTS script, subtitle script, and lip-sync plan;
- cliffhanger budget, payoff ledger, comment prompts, shareable moments, release cadence, and retention targets;
- edit/sound/color instructions and delivery manifest;
- QC checkpoints, copyright/watermark policy, and archive record;
- generation state, task ledger, downloaded outputs, and a reproducible command path from script to video.

Scale the deliverable to the request. Do not create empty artifacts merely to match the list.

## Non-negotiable production invariants

1. **Lock canon before paid generation.** Do not submit billable video tasks until story beats, character references, canvas, and shot intent are approved.
2. **Character consistency is an asset system.** Use fixed reference images, a written anchor, outfit variants, shot-level QC, and last-frame/first-frame chaining. Prompt repetition alone is insufficient.
3. **Never let video models render final Chinese text.** Generate blank surfaces or abstract glyphs; add dialogue, signage, UI, captions, and legal text in post.
4. **Generate picture and dialogue separately when consistency matters.** Use clean silent video, then TTS/recording, subtitle timing, and lip-sync. Enable model audio only for tests or non-dialogue ambience.
5. **Preserve provenance.** Keep prompts, task IDs, raw generations, selected takes, final renders, hashes, model names, and rights records. Never overwrite raw files.
6. **Paid or externally mutating actions require explicit user intent.** Before running paid generation, state the number of tasks, duration/resolution, expected variants, likely wait, and any known budget implication. Do not publish, upload, or overwrite source assets without permission.
7. **Separate creative approval from production approval.** A good script does not authorize a fifty-episode render.
8. **Influence without imitation.** Analyze named filmmakers as craft references only; never copy protected scenes, costumes, dialogue, music, character designs, or recognizable shot-for-shot sequences.

## Script and coverage quality gate

Before shot lock, verify:

- the protagonist has a concrete want, a resisting obstacle, and a cost;
- each scene has objective, obstacle, tactic, turn, and exit;
- every episode changes knowledge, power, relationship, safety, ownership, identity, or moral position;
- setups and payoffs are tracked across episodes;
- cliffhanger types rotate rather than repeating one device;
- coverage preserves geography, eyelines, screen direction, props, and light direction;
- every camera move has a narrative intention;
- each 4–8 second shot carries one dominant action and one dominant camera idea;
- dialogue is performable, character-specific, and not used to explain what the image already shows.

Before shot lock, also choose one primary storytelling technique, one staging technique, one transition family, one hero VFX motif, and one recurring visual or sound gag. Do not stack techniques without story purpose.

Do not move a weak scene into generation and hope the camera will fix it.

## Audience retention gate

Before production, define:

- the audience promise in one sentence;
- the opening question that makes a viewer stay;
- the emotional driver: justice, curiosity, fear, tenderness, identity, or social debate;
- one major cliffhanger per episode and a planned payoff;
- no more than 2–3 major open loops at once;
- one comment prompt that creates a choice, camp, prediction, or hidden clue;
- one shareable moment that works without context;
- one concrete next-episode tease;
- a release cadence and a pinned-comment plan.

Do not mistake a polished scene for a retention event. Every episode must change information, power, relationship, safety, ownership, identity, or moral position.

## Full-chain execution path

Run the pipeline in this order:

1. Fill `project_profile.json`.
2. Lock story, episode matrix, scripts, scene breakdown and retention plan.
3. Lock characters, outfits, scenes, props, technique plan and cover direction.
4. Build and validate `shot_manifest.csv`.
5. Run `validate_project.py` and `audit_retention.py`.
6. Build Seedance JSONL with `build_seedance_tasks.py`.
7. Run `seedance_client.py dry-run` and report task count, duration, references, expected wait and budget.
8. Submit paid tasks only with explicit approval and both `--execute --confirm-paid`.
9. Poll and download with `seedance_client.py poll`.
10. Record selected takes, rejected reasons, task IDs and hashes.
11. Add voice, subtitles, lip-sync, edit, sound and color.
12. Add post typography, watermark and AI label.
13. Validate the final package and write the delivery manifest.

For the phase-by-phase artifacts, gates and stop conditions, read `references/end-to-end-orchestration.md`.

## Reusable operating modes

- **Trailer mode:** 6s hook, 15s cutdown, 30s main trailer, 45s story trailer, covers and launch copy.
- **Pilot mode:** 1–3 episodes with complete asset, voice, subtitle, lip-sync and delivery records.
- **Season mode:** episode matrix, recurring continuity, batch generation and release schedule.
- **Audit mode:** diagnose an existing project for story, coverage, consistency, rights or delivery gaps.

The project profile is the source of truth. The Fire Monkey reference is an optional case study, not a dependency.

## Intake

Establish or infer these before production:

- audience, genre, platform, aspect ratio, episode count, episode duration, language;
- visual style, era, rating, dialogue density, and music direction;
- character references and rights ownership;
- available model/API, budget, deadline, concurrency, and storage;
- whether the deliverable is a pilot, trailer, one episode, or full season.

If a required item is missing but can be safely defaulted, state the default. For example: vertical drama defaults to `9:16`, `1080x1920`, `24 fps`, and 15 shots per two-minute episode unless the user specifies otherwise.

## Workflow

1. **Scope and rights:** define deliverables, ownership, AI-label policy, forbidden content, and paid-generation gates.
2. **Estimate workload:** run `scripts/estimate_production.py` or document equivalent assumptions. Estimate shots, raw generations, keyframes, person-hours, wall-clock days, storage, and rework.
3. **Story canon:** lock promise, protagonist want/need/flaw, pressure, price, character relationships, season arc, scene map, setup/payoff ledger, episode matrix, continuity rules, and causal episode bridges.
4. **Script and table read:** lock scene objective/obstacle/tactic/turn/exit, dialogue, visual action, runtime, cliffhanger type, and voice intent before shot design.
5. **Visual system:** lock canvas, safe areas, palette, lighting, lens language, typography, VFX language, and text-in-post rules.
6. **Asset library:** register character, outfit, expression, scene, prop, voice, music, and font assets with IDs, versions, rights, and checksums.
7. **Shot manifest:** assign story function, coverage role, timecodes, shot size, camera intention, eyeline, screen direction, action, dialogue/performance beat, prompt, reference IDs, model, resolution, duration, and status to every shot.
8. **Previs and keyframes:** approve character/look continuity on stills before video generation.
9. **Video generation:** generate in 4–30 second tasks, ensure reference-image payloads are public URLs/Base64/asset IDs, select takes, record task IDs, and preserve raw outputs.
10. **Voice, subtitles, and lip-sync:** performance beats, voice casting, audio-first timing, pronunciation lexicon, subtitle line breaks, forced alignment, and drift checks.
11. **Edit and finishing:** assemble, trim, color-match, sound-mix, add post typography, copyright watermark, AI label, and platform masters.
12. **QC and delivery:** run visual, audio, subtitle, continuity, legal, and technical checks; generate hashes and delivery manifest; archive the project.

## Production defaults

- Two-minute episode: 12–18 shots, usually 15.
- Seedance 2.5: one task lasts 4–30 seconds; use 4–6 generation blocks for a two-minute episode.
- Dialogue-heavy scenes: generate silent video and sync dialogue in post.
- Character reference: one primary full-body image, one face image, plus optional expression/side views.
- Text: post-production vector typography only.
- Vertical safe area: keep faces and key props out of the top/bottom 10–12%.

## Reference routing

Read only the references needed for the current stage:

- Screenwriting, scene logic, coverage, camera grammar, continuity: `references/screenwriting-and-shot-logic.md`
- Full chain from script to generation: `references/end-to-end-orchestration.md`
- Audience desire, cliffhangers, comment prompts, retention metrics: `references/audience-retention-and-serialization.md`
- Reusable profiles, modes, adapters, naming, minimal package: `references/reusable-project-system.md`
- Covers, launch packaging, A/B assets: `references/cover-and-packaging.md`
- Filmmaker principles, transitions, VFX grammar, sequence recipes: `references/cinematic-technique-cookbook.md`
- Pipeline, gates, and roles: `references/production-pipeline.md`
- Workload formulas and staffing: `references/workload-estimation.md`
- Prompts, canvas, consistency, Seedance parameters: `references/prompt-consistency.md`
- Voice, subtitles, lip-sync: `references/audio-subtitle-lipsync.md`
- Asset library, naming, rights, archive: `references/asset-library.md`
- Optional Fire Monkey/Flame Advertising case study: `references/fire-monkey-project.md`

## Scripts and templates

- Estimate workload: `python scripts/estimate_production.py --episodes 60 --duration 120 --avg-shot 8 --variants 2.5 --characters 1 --scenes 20 --complexity medium`
- Scaffold a project: `python scripts/scaffold_project.py <project-dir> --project-name <name>`
- Validate a reusable project: `python scripts/validate_project.py <project-dir>`
- Build Seedance JSONL tasks: `python scripts/build_seedance_tasks.py --shot-manifest <csv> --project-profile <json> --output <jsonl>`
- Audit retention and cliffhangers: `python scripts/audit_retention.py <retention_plan.csv>`
- Seedance dry run: `python scripts/seedance_client.py dry-run --tasks <jsonl>`
- Seedance paid submit: `python scripts/seedance_client.py submit --tasks <jsonl> --state <state.json> --output-dir <raw-dir> --execute --confirm-paid --limit <n> [--embed-local-refs]`
- Seedance poll/download: `python scripts/seedance_client.py poll --state <state.json> --download-dir <raw-dir>`
- Project profile template: `assets/templates/project_profile.json`
- Retention plan template: `assets/templates/retention_plan.csv`
- Cover copy template: `assets/templates/cover_copy.csv`
- Technique plan template: `assets/templates/technique_plan.csv`
- Scene breakdown template: `assets/templates/scene_breakdown.csv`
- Shot manifest template: `assets/templates/shot_manifest.csv`
- Asset registry template: `assets/templates/asset_registry.csv`
- Voice timeline template: `assets/templates/voice_timeline.csv`
- Delivery manifest template: `assets/templates/delivery_manifest.csv`

## Completion checks

Before calling a production package complete:

- every scene has a story function, objective, obstacle, tactic, turn, and exit;
- every shot has timecode, duration, action, dialogue/intent, coverage role, camera intention, prompt, reference IDs, and status;
- the same character IDs resolve to the same reference/outfit/voice across the project;
- eyelines, screen direction, props, costume state, time of day, and light direction survive the edit;
- camera moves are motivated and do not fight the action;
- transition families are deliberate and limited by the technique budget;
- effects are layered, motivated, and do not hide unclear action;
- named-filmmaker influence has passed an originality check;
- all text is planned for post;
- all paid tasks have task IDs and selected takes;
- subtitle timing and lip-sync drift have been checked;
- copyright, AI label, music, and input rights are recorded;
- final masters have checksums and a delivery manifest;
- `project_profile.json` is populated without secrets;
- `validate_project.py` passes and every generated task comes from the shot manifest;
- every episode has an opening question, midpoint turn, cliffhanger, payoff, comment prompt, shareable moment and next-episode tease;
- cliffhanger types rotate and open loops have planned payoffs;
- unresolved creative or rights issues are explicitly listed.
