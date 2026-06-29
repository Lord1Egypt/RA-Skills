# Changelog

## [0.1.0] - 2026-06-15

### Added
- Initial release of `click-driven-presentation`: a playbook + minimal engine that turns an existing narration script into a click-driven, full-screen web presentation the speaker advances one beat per click and records.
- Governing idea (script = beats · step = one beat on screen · scene = a pure function of the current step · visuals show the idea) and the rule that time is the speaker's — no baked durations, no auto-advance timers.
- Two mandatory human STOP gates: plan confirmation (step breakdown / theme / asset list) and Scene 1 acceptance (the style anchor) before building the rest.
- Build modes for scenes 2..N: per-scene confirm (default), sequential, and parallel subagents.
- Single source of truth: per-scene `steps` array whose length must equal the scene's max step used, kept even without audio synthesis so the script and on-screen beats never drift.
- `scripts/scaffold.sh`: a Vite + React + TS engine (fixed 16:9 stage with letterbox, global step-as-pure-function counter, click/keyboard advance, hidden hover-only progress bar, token-based theming) plus one neutral token theme and a deletable demo scene.
- References: `SCENE-CRAFT.md` (content-driven animation, step-by-step reveal, dual-source rule, anti-AI-aesthetic checklist, code red-lines, completion self-check) and `STEPS-SPEC.md` (the per-scene steps data contract and slicing rules).
- Scope boundaries: not mp4 rendering, audio/TTS, screen recording, post-editing, or general web-app development; script-writing delegated to a content skill and per-scene visual craft to a front-end design skill, both referenced by capability.
- English-only skill text with locale-neutral examples; source uses one-sentence-per-line prose to match the repo convention.
