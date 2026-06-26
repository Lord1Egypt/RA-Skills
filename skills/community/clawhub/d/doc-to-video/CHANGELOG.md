# Changelog for doc-to-video v1.0.4

## v1.0.4 → v1.0.4 changelog (paste this into clawhub):

```
Version 1.0.4 of doc-to-video

Major workflow improvements and new tooling based on 27 real video projects (~75 minutes of content) produced with this skill:

- Added templates/audio_frames.py: CLI tool with `measure` and `frames` subcommands. `measure` measures per-scene audio durations and writes a scenes.json snapshot. `frames` computes the F[] frame-boundary array from those durations for direct paste into src/Scene.tsx. Replaces fragile inline `python -c` invocations.

- Added templates/voice_test.py: standalone script to audition 6 candidate edge-tts voices (Xiaoxiao, Yunxi, Yunjian, Xiaoyi, Yunyang, Yunxia) with the same narration sample, so users can pick a voice before committing to 8 segments of generation. Addresses repeated "voice swap after full render" iterations.

- Added references/voice-swap-and-iterate.md: full workflow for changing voice / 语速 / 旁白文本 after first render. Documents the atempo 1.2 vs 1.17 ffmpeg precision quirk, F[] 整体缩放 vs 逐段重算 trade-offs, and the "永远不要把音频拉回去贴合视频" anti-pattern. Includes reference F[] calculation examples.

- Added references/macos-gotchas.md: consolidated list of macOS-specific issues (chrome-headless-shell spawn error -88, localhost:3000 dev server, ffmpeg 8.x AAC re-encode requirement, node_modules cache hits).

- Added references/batch-rendering.md: workflow for running 5+ videos in parallel using subagent + parallel npm install + parallel render. Documents the 2+3 render concurrency sweet spot, the file_list.txt path-relative-to-list-file gotcha, and when to use subagent vs hand-written narration.

- Added references/second-video-pattern.md: 2nd-video workflow showing that on subsequent videos the boilerplate (Remotion config, package.json, Primitives.tsx) can be cp -R'd from the first project, saving 30+ minutes per video.

- Added references/syncing-to-openclaw.md: documents the content sync between ~/.hermes/skills/doc-to-video (canonical) and ~/.openclaw/workspace/skills/doc-to-video (mirror) — what files are public vs openclaw-private (skill-card.md, _meta.json, .clawhub/).

- Added references/worked-example-tsp-solidity04.md: full end-to-end trace of one video project — directory structure, 10 narration segments, F[] calculation, render+merge shell sequence, frame inspection, audio/video sync verification.

- Updated SKILL.md: bumped to v1.0.4. Added Step 0 (voice audition) to quickstart. Replaced Step 4 inline ffprobe loop with `audio_frames.py measure` invocation. Replaced "ffmpeg atempo by hand" Step 5 with `audio_frames.py frames` invocation. Added forward-link to voice-swap-and-iterate.md in Q8 (voice quality).

- Updated skill-card.md: refreshed mitigation list to include audio_frames.py, F[] measurement, macOS Chrome executable requirement.

- Updated templates/: Scene.tsx unchanged, but added Primitives.tsx reference in references/second-video-pattern.md. generate_audio.py, merge.sh, all 3 remotion configs are unchanged from v1.0.1.

## v1.0.3 (intermediate, never published as clawhub version)

Added references/voice-swap-and-iterate.md (initial draft). Fixed ffmpeg concat path bug in generate_audio.py.

## v1.0.2 (intermediate, never published as clawhub version)

Added Q8 about edge-tts 48kbps MP3 ceiling + voice comparison table.

## v1.0.1 (intermediate, never published as clawhub version)

Fixed ffmpeg concat path bug. Added macOS Remotion chrome gotcha. Added fast-path (no atempo) when total audio already in 180-210s range. Added references/ and templates/ skeleton.

## v1.0.0 (original published version on clawhub)

Initial release.
