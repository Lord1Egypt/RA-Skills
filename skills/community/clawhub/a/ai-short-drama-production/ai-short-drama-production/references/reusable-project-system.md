# Reusable Project System

Use this reference when adapting the skill to a new IP, genre, studio, language, or model vendor. The project profile is the source of truth; references and examples are interchangeable.

## 1. Operating modes

Choose one mode at intake:

- **Trailer mode:** 6s hook, 15s cutdown, 30s main trailer, 45s story trailer, cover and launch copy.
- **Pilot mode:** 1–3 episodes, full asset library, voice, subtitles, lip-sync and release QC.
- **Season mode:** episode matrix, recurring continuity, batch generation, delivery schedule.
- **Audit mode:** inspect an existing production for character drift, continuity, rights, packaging or workload gaps.

Do not produce a full season package for a trailer request. Do not treat a good script as paid-generation approval.

## 2. Project profile

Fill `assets/templates/project_profile.json` and place it at the project root as `project_profile.json`.

Required fields:

- project ID, title, owner, copyright, language, deliverable type;
- canvas, resolution, FPS, episode duration, episode count, shots per episode;
- series IDs and genre/audience/visual/voice direction;
- character IDs, immutable anchors, references, outfits, voice IDs and rights;
- video/image/TTS model adapters;
- generation defaults and approval policies.

The profile must not contain API keys, passwords or private tokens. Use environment variables for credentials.

## 3. Adapter model

The workflow is model-agnostic:

- **Video adapter:** Seedance/Ark, another API, or a manual editor. Store provider, model ID, API surface and generation limits.
- **Image adapter:** Seedream or another image model for keyframes and covers.
- **TTS adapter:** provider, voice IDs, pronunciation lexicon and sample files.
- **Finishing adapter:** editor, subtitle tool, lip-sync tool and delivery codec.

Switching a vendor must not require rewriting the story, shot manifest or asset registry.

## 4. Reuse workflow

1. Duplicate a project profile.
2. Replace project, series and character records.
3. Run `python scripts/scaffold_project.py <project-dir> --project-name <name>`.
4. Fill scene breakdown, continuity ledger, retention plan and shot manifest.
5. Validate the project with `python scripts/validate_project.py <project-dir>`.
6. Build generation tasks with `python scripts/build_seedance_tasks.py --shot-manifest <csv> --project-profile <json> --output <jsonl>`.
7. Dry-run the task JSONL, obtain explicit approval, submit with `seedance_client.py`, poll and download, then voice, subtitle, lip-sync, edit and package.
8. Re-run validation before delivery.

## 5. Naming rules

Use stable IDs:

- project: `PROJECT-YYYY-###`
- series: `SER-###`
- episode: `S01E03`
- scene: `SER-SCENE-###`
- shot: `S01E03-SH07`
- character: `CHAR-###`
- outfit: `OUT-###`
- prop: `PROP-###`
- task: provider task ID
- asset: `AST-###`

Do not use prose-only filenames for production assets.

## 6. Minimal reusable package

A new project is reusable when it has:

- `project_profile.json`
- `01_story/scene_breakdown.csv`
- `01_story/continuity_ledger.csv`
- `01_story/retention_plan.csv`
- `02_visual_bible/technique_plan.csv`
- `03_characters/character_registry.csv`
- `06_shots/shot_manifest.csv`
- `07_audio/voice_timeline.csv`
- `11_deliverables/delivery_manifest.csv`
- rights manifest and project brief

Everything else is project-specific.

## 7. Security and rights

- Keep credentials in environment variables.
- Record input rights, model provider, output rights and allowed distribution.
- Do not publish or upload assets without authorization.
- Keep a private project profile and a sanitized public version when sharing the skill or examples.
