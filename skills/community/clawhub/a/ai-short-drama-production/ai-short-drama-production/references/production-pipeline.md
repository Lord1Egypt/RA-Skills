# AI Short Drama Production Pipeline

Use this reference to plan, staff, gate, and audit a multi-episode AI short-drama production.

## 1. Production roles

| Role | Owns | Required sign-off |
|---|---|---|
| Producer | scope, budget, schedule, rights, paid-task authorization | final delivery |
| Head writer / showrunner | canon, episode matrix, scripts, continuity | script lock |
| Storyboard / prompt director | shot design, prompt manifest, camera language | shot lock |
| Character consistency lead | reference sheets, outfit variants, regeneration decisions | character lock |
| Generation operator | Ark/Seedance jobs, task IDs, takes, downloads, queue | generation log |
| Voice director | casting, TTS/recording, pronunciation, emotion | audio lock |
| Subtitle / lip-sync editor | timing, line breaks, forced alignment, drift | sync lock |
| Editor / finisher | assembly, color, sound, text, watermark, masters | picture lock |
| QC / rights reviewer | continuity, technical, legal, AI labels, hashes | release gate |

One person may hold several roles in a small team, but the sign-off responsibilities remain distinct.

## 2. Stage gates

### Gate A — Scope and rights

Before creative work:

- episode count, runtime, platform, canvas, language, audience;
- ownership of character, script, music, voice, fonts, and input assets;
- permitted model vendors and data handling;
- AI disclosure and company watermark requirements;
- maximum paid generations and approval path.

**Output:** one-page production brief, assumptions list, rights checklist, populated `project_profile.json`.

### Gate B — Story lock

- logline, theme, audience promise, season arc;
- protagonist want, need, flaw, pressure, price, and payoff;
- character relationships, knowledge state, and continuity locks;
- scene map with objective, obstacle, tactic, turn, and exit;
- episode matrix with beginning, escalation, reversal, cliffhanger;
- episode-to-episode causal bridge, not just a premise;
- setup/payoff ledger and cliffhanger-type rotation;
- factual/legal/classical review where relevant.

**Output:** story bible, episode scripts, continuity notes, fact-check log.

### Gate C — Visual lock

- canvas, safe areas, palette, lighting, lens language, texture, typography;
- technique plan: storytelling mode, staging mode, transition family, hero VFX motif, recurring gag;
- technique budget and originality check;
- character turnaround, expressions, outfit variants, scale chart;
- scene key art and prop references;
- text-in-post policy.

**Output:** visual bible, character bible, scene/prop registry, approved keyframes.

### Gate D — Shot lock

Every shot must have:

- shot ID, episode, scene, timecode, duration;
- story function and coverage role;
- technique tags, shot size, camera intention, action, emotion, transition;
- eyeline, screen direction, axis, and match point;
- character IDs, outfit IDs, scene/prop IDs, condition state;
- light direction, time of day, weather, color continuity;
- prompt, negative prompt, reference IDs;
- model, ratio, resolution, duration, audio policy;
- intended dialogue, performance beat, SFX, music cue;
- generation status and acceptance criteria.

**Output:** shot manifest, production board, and validated generation-task JSONL.

### Gate E — Generation lock

Before paid generation, confirm:

- task count and variant policy;
- resolution and duration per task;
- reference-image payload method;
- concurrency and expected wait;
- dry-run task count and reference-image coverage;
- storage plan for raw files and generation state ledger;
- retry policy and stopping condition.

**Output:** generation queue, task ledger, selected-take log.

### Gate F — Audio and sync lock

- final voice files and pronunciation decisions;
- subtitle script and line breaks;
- music/SFX cue sheet;
- lip-sync per dialogue shot;
- audio/subtitle drift check;
- loudness and output format.

**Output:** voice timeline, subtitle master, lip-sync map, mix notes.

### Gate G — Picture lock and delivery

- edit conform and trim;
- color consistency across generated shots;
- typography and copyright watermark;
- platform masters and caption files;
- checksums and archive;
- unresolved issues list.

**Output:** delivery manifest, masters, checksum registry, archive.

## 3. Episode production sequence

For each episode:

1. Read the locked script and adjacent episode bridge.
2. Break into 12–18 shots; mark scene turns, coverage roles, dialogue shots, reaction shots, inserts, and visual-only shots.
3. Generate the shot manifest and reference IDs.
4. Create keyframes and approve character/scene continuity.
5. Generate 4–30 second video tasks, usually 4–6 blocks per two-minute episode.
6. Select takes and log task IDs, seed/model metadata, and rejects.
7. Generate or record clean dialogue and voice tracks.
8. Add subtitles and lip-sync.
9. Assemble, sound-design, color-match, and add post text.
10. Apply copyright watermark and AI label.
11. Run QC and export masters.
12. Archive raw and final assets with hashes.

## 4. Rework policy

- Reject a take only for a stated reason: face drift, outfit drift, hand defect, wrong action, camera failure, text artifact, safety issue.
- Regenerate the smallest affected unit, not the full episode.
- Keep a rejected-take log when it affects continuity.
- If three consecutive takes fail the same invariant, stop and revise the reference or prompt instead of spending more.
- Escalate when a defect crosses episodes, violates rights, or cannot be fixed in post.

## 5. Minimum QC

- Character: face, ears, silhouette, tail, hands, outfit, scale, age, condition state.
- Coverage: story purpose, eyeline, screen direction, axis, match on action, reaction necessity.
- Technique: transition motivation, effect budget, originality, recurring motif.
- Motion: limb continuity, foot contact, gaze, prop hand, camera motivation, motion direction.
- Scene: prop continuity, time of day, weather, background, crowd, light direction, geography.
- Audio: voice match, pronunciation, sync, music/SFX balance.
- Text: no AI gibberish; all final text is post-produced.
- Rights: input, model, music, font, voice, company watermark.
- Technical: resolution, FPS, codec, audio channels, duration, checksum.
