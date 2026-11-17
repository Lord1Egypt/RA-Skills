# build-game-plus

Playable browser games (2D canvas *or* 3D Three.js) from natural language — with a **screenshot verification loop** the agent must run before claiming anything works.

Built as an improvement over the well-known `build-game` skill (whose full Three.js reference library it inherits):

| Gap in `build-game` | What build-game-plus does |
|---|---|
| 3D-only — Three.js forced even for match-3/platformers | Explicit **engine-choice table** (2D Canvas2D vs 3D Three.js by genre) + a full Canvas2D patterns reference |
| Style rules ("no near-black scenes") but **nothing checks them** | `scripts/verify_game.py`: headless-Chrome screenshot + PIL/numpy pixel analysis — dark scene (<22 luminance), stuck menu (<8 stdev), blank-white crash, console errors. PASS/FAIL verdict, loop until PASS |
| Games stored in `/tmp/game-build` (die on reboot mid-iteration) | Persistent `$HOME/games/<slug>/` with progress.md tracking |
| Publish step points at another user's machine (`/home/ke/...`) | Publishes to the host's own domain via nginx + Cloudflare tunnel (`scripts/publish.sh`), no third-party service, permanent |
| No programmatic inspection | Mandatory `window.render_game_to_text()` + `window.advanceTime(ms)` debug hooks in every game |

## Install

```bash
openclaw skills install @ParadoxFuzzle/build-game-plus
```

## Example

Ask your agent: *"a dodge-the-cubes arcade game"*. It will choose Canvas2D, build the single-file game, run the verifier (headless Chrome screenshots), fix any FAIL findings, and only then deliver — with the `.verify/report.json` verdict and both screenshots as evidence.

A working example ships from development at the usual conventions: a dodge-cubes arcade prototype (`games/dodge-cubes/` layout pattern, not bundled here).

## Scripts

- `scripts/verify_game.py <game.html|url>` — screenshot + console-error verification, JSON report
- `scripts/serve.sh <dir>` — local static preview server
- `scripts/publish.sh <dir> [slug]` — copy into the host webroot for a permanent public URL

## Reference library

`reference/` contains seven pattern docs: the six inherited 3D references (engine patterns, graphics quality, procedural assets, audio, UI, game systems) plus the new `canvas2d-patterns.md`.

MIT.
