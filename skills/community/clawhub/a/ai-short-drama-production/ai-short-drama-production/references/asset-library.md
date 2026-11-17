# Asset Library and Provenance

## Standard project tree

```text
project/
|-- 00_admin/
|   |-- production_brief.md
|   |-- rights_manifest.csv
|   `-- paid_task_ledger.csv
|-- 01_story/
|   |-- series_bible.md
|   |-- episode_matrix.csv
|   `-- scripts/
|-- 02_visual_bible/
|   |-- canvas_and_safe_area.md
|   |-- style_guide.md
|   `-- typography/
|-- 03_characters/
|   |-- character_registry.csv
|   |-- refs/
|   |-- outfits/
|   `-- expressions/
|-- 04_scenes/
|-- 05_props/
|-- 06_shots/
|   |-- shot_manifest.csv
|   |-- keyframes/
|   |-- raw_generations/
|   `-- selected_takes/
|-- 07_audio/
|   |-- dialogue/
|   |-- music/
|   |-- sfx/
|   `-- voice_timeline.csv
|-- 08_subtitles/
|-- 09_lipsync/
|-- 10_edit/
|-- 11_deliverables/
|-- 12_archive/
`-- project_manifest.json
```

## Naming convention

Use stable IDs rather than prose filenames:

`S01E01_SH03_V02_character-FHM_outfit-FHM-XH_scene-GJC_night.mp4`

Minimum fields:

- series/episode/shot;
- version;
- character/outfit/scene/prop IDs;
- type (`keyframe`, `raw`, `selected`, `final`, `audio`, `subtitle`, `lipsync`);
- status.

Never overwrite `raw` or `selected` files. New take means new version.

## Asset registry fields

At minimum:

`asset_id,type,name,series,episode,character_id,variant,version,path,source,task_id,rights_owner,license,sha256,state,status,approved_by,notes`

## Continuity state

The registry must record state, not just identity:

- costume version and damage;
- prop owner, hand, condition, and location;
- character knowledge and relationship state;
- scene geography, entrances/exits, and crowd state;
- time of day, weather, light direction, and color temperature;
- VFX state such as fire marks, cold-flame marks, or injuries;
- episode-to-episode unresolved loops.

Use `assets/templates/continuity_ledger.csv` to track changes that affect the next scene.

## Rights and provenance

For each asset record:

- owner and permitted uses;
- source: original, commissioned, licensed, stock, AI-generated;
- model/vendor and task ID for AI output;
- input reference rights;
- music, voice, font, and footage licenses;
- AI-label requirement;
- distribution territory and expiry.

For paid generation, log:

- task ID and model;
- prompt/version;
- duration/resolution;
- selected/rejected status;
- output URL and local path;
- SHA-256;
- operator and date.

## Archive policy

Keep:

- locked scripts and fact-check notes;
- approved character/scene bibles;
- prompts and negative prompts;
- raw generations and selected takes;
- task ledger;
- audio stems, subtitles, lip-sync files;
- edit project and final masters;
- rights records, hashes, and delivery manifest.

Store originals and finals in separate immutable folders. Preserve at least one local backup in addition to cloud storage.
