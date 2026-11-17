---
name: build-game-plus
description: >-
  Build playable browser games (2D canvas or 3D Three.js) from natural language,
  with an automated screenshot verification loop the agent runs before claiming
  the game works — no unverifiable "should look fine" claims. Persists games in
  a stable workspace (games/<slug>/, not /tmp), iterates via targeted edits,
  publishes to https://jerithai.com/games/<slug>/ via the existing nginx +
  Cloudflare tunnel. Reuses the full 3D pattern library from the original
  build-game skill and adds 2D canvas, genre-appropriate engine choice, and
  verify-before-deliver as a hard gate.
argument-hint: [game description or modification]
metadata: {"openclaw":{"emoji":"🕹️","requires":{"bins":["python3"]}}}
user-invocable: true
---

# Build Game Plus

You are a game architect. You design, build, and iterate on **playable browser
games**, choosing the right engine for the job (not always 3D), and you never
say a game "works" without **seeing it work**.

## The core difference from other game skills: VERIFY BEFORE DELIVER

Every build ends with the verification loop, executed by you, for real:

```bash
cd "$SKILL_DIR"   # directory containing this SKILL.md
python3 scripts/verify_game.py "$GAME_DIR/index.html" --out "$GAME_DIR/.verify" --click
```

This launches headless Chrome (WebGL via SwiftShader), screenshots the title
screen and gameplay, catches console errors, and analyzes the pixels:

- **mean luminance** — catches the classic "I picked near-black colors and the
  scene is invisible" failure. FAIL < 22.
- **luminance stdev** — catches stuck menus and worlds that never rendered. FAIL < 8.
- **blank white screen** — crash or CSS-only render. FAIL > 248 mean with stdev < 6.
- **console errors** — first error is quoted in the report.

**Verdict FAIL → you read `report.json`, fix the specific issue, re-verify.**
Loop until PASS, or until you've made 3 fix attempts and must report honestly
what's still broken. NEVER deliver a game with a FAIL report without saying so
explicitly. The screenshots in `.verify/menu.png` and `.verify/gameplay.png`
are evidence — cite them.

## Phase 0: Detect Mode

```bash
ls "$GAMES_DIR/<existing-slug>/index.html" 2>/dev/null && echo EXISTS
cat "$GAMES_DIR/<existing-slug>/progress.md" 2>/dev/null
```

`$GAMES_DIR` defaults to `~/games/` (persistent across sessions — NOT /tmp;
games survive reboots and reappear in the workspace listing).

- **ITERATION** — request modifies/extends an existing game → read its
  `index.html` + `progress.md`, make targeted edits, re-verify. When in doubt,
  treat as iteration.
- **NEW GAME** — a different game concept → new slug dir, fresh build.

Always update `progress.md` after every build or edit (see template below).

## Phase 1: Analyze the Request

Extract from `$ARGUMENTS`:

1. **Genre + mechanics** — what does the player DO?
2. **Visual concept** — characters, enemies, setting, mood
3. **Scope** — quick toy vs. systems-heavy game
4. **References** — images the user provides (view them; map to procedural models or embed as base64 textures)

### Engine choice — 2D or 3D? (decide explicitly, say why)

| If the game is… | Build it as… | Why |
|---|---|---|
| Platformer, match-3, roguelike, tactics, chess/checkers, Galaga/Space-Invaders shooter, rhythm, Sokoban, TUI-likes, idle/clicker, most "retro arcade" | **2D canvas** (plain Canvas2D, or PixiJS pattern if many sprites) | Canvas2D is fewer lines, faster to iterate, harder to make "invisible scene" mistakes, and screen-space logic is simpler |
| FPS, third-person action, racing, true-3D RPG overworld, flight, tower defense with 3D depth, "walking around a world" | **3D Three.js** | Depth, camera control, atmosphere are the point |

If the user explicitly asks for 3D, use 3D. If the request is silent and genres
match, prefer 2D — ship quality is easier to hit, and the verification loop
catchers (luminance, uniformity) work identically on both.

### For 3D games

Read `reference/engine-patterns.md`, `reference/graphics-quality.md` (mandatory
every time), `reference/procedural-assets.md`, `reference/gui-patterns.md`,
`reference/audio-patterns.md`, `reference/game-systems.md` as needed. Follow
the original build-game rules: camera-relative WASD for third-person, no
near-black surfaces, sky dome shader, 4+ light rig, post-processing stack
(RenderPass → SSAO → Bloom → color grade → FXAA), PMREM environment map,
instanced scatter, procedural canvas textures, `ACESFilmicToneMapping`.

### For 2D games

Read `reference/canvas2d-patterns.md`. Highlights:

- **Single file, same discipline**: CONSTANTS → DATA → STATE → ASSET FACTORIES
  (offscreen canvas sprites drawn procedurally; no external images needed) →
  SYSTEMS → RENDER (single canvas, fixed 1280×720 logical, scale to DPR) → LOOP.
- **Palette rule (same as 3D)**: no near-black playfield unless deliberate and
  contrast-compensated; player + obstacles must be distinguishable; 3+ hues,
  2+ luminance bands minimum.
- **Juice**: screen shake, hit flash, particles (plain arrays ofobjects, pooled),
  tweened UI, Web Audio procedural SFX (see `audio-patterns.md` — patterns are
  engine-agnostic).
- **Save/load**: localStorage, same as 3D games.

## Phase 2: Design

Same planning discipline as games in general:

- **Game loop**: what updates per frame (fixed timestep accumulator for
  physics/logic; render decoupled).
- **Entities**: roster, appearance (procedural sprite/object recipes), FSM AI,
  stats.
- **Systems needed** (from `game-systems.md`): combat, inventory, dialogue,
  capture, quests, save/load, day/night — include only what serves the game.
- **HUD/UI** and **game flow**: title screen → gameplay → game over, with
  clear objective stated on the title screen.
- Win/lose conditions and progression arc.

## Phase 3: Generate

Write the game as ONE `index.html` in `$GAMES_DIR/<slug>/` with the CODE
STRUCTURE ordering from `engine-patterns.md` (2D or 3D variant) — CONSTANTS at
top, modular commented sections, magic numbers nowhere inline. Crucially:

```html
<!-- DEBUG HOOKS — required, both 2D and 3D -->
window.render_game_to_text()  // returns HUD text snapshot for verification
window.advanceTime(ms)        // advances game state deterministically
```

These exist so the verification loop and future agents can inspect state
without playing by hand.

Three.js (when used): v0.160.0 via jsdelivr importmap exactly as in
`engine-patterns.md`. Canvas2D: no imports needed.

## Phase 4: Quality bar (both engines)

- **Visuals**: polished, not tech-demo. At minimum: cohesive palette,
  environment decoration, readable player/enemies, title screen with animated
  backdrop.
- **Feel**: juice (shake, flash, particles), smooth movement, procedural audio
  for key actions, responsive menus.
- **Code**: instancing/pooling where counts are high, no per-frame allocations
  in hot loops, all tunables in CONSTANTS.
- **Playable**: real objective, lose state, restart works, plays in ~2–5 min
  minimum for arcade or one full loop for RPGs.

## Phase 5: Verify (RUN IT)

```bash
python3 "$SKILL_DIR/scripts/verify_game.py" "$GAMES_DIR/<slug>/index.html" --out "$GAMES_DIR/<slug>/.verify" --click
```

Read `report.json`. If FAIL: fix the named issue, re-run. Confirm PASS before
telling the user it works. Cite the two screenshot paths as proof.

Console-error notes:
- SwiftShader software rendering may log a benign `GPU stall`/perf warning —
  not a failure.
- `AudioContext` warnings before user gesture are benign in headless.

## Phase 6: Serve / Publish

```bash
# local preview (blocks; run in background, report the port)
bash "$SKILL_DIR/scripts/serve.sh" "$GAMES_DIR/<slug>" &

# permanent public URL via this host's nginx + Cloudflare tunnel
bash "$SKILL_DIR/scripts/publish.sh" "$GAMES_DIR/<slug>" [slug]
# → https://jerithai.com/games/<slug>/
```

Publish is **permanent** by design (site's own domain, no 24h expiry). Don't
publish unless the user asked for a public link — local + verification is the
default deliverable.

## Phase 7: Update progress.md

```markdown
# [Game Title]
slug: <slug>          engine: <2d-canvas|three-160>       updated: <date>

## Original Request
[first prompt]

## Current State
[what works now]

## Iteration History
- <n>: [what changed since last build]

## Entity Roster
[player / enemies / NPCs list]

## Systems Active
- [x] movement  [x] combat(realtime)  [ ] inventory  [ ] dialogue …

## Verification
- last run: <date>  verdict: <PASS|FAIL>  report: .verify/report.json
- issues found + fixed: [list]

## Known Issues
- [bugs/rough edges, honestly]

## Suggested Next Steps
- [ideas]
```

## Phase 8: Self-Review Checklist (before final answer)

- [ ] verify_game.py run, verdict PASS, screenshots exist
- [ ] engine choice matches genre (2D where 2D was right)
- [ ] WASD camera-relative for 3D third-person (see engine-patterns.md)
- [ ] no near-black surfaces; player distinguishable from background
- [ ] all user-described entities actually present
- [ ] title/controls shown; game over + restart works
- [ ] progress.md updated, verification section filled in
- [ ] `window.render_game_to_text()` + `window.advanceTime(ms)` present
- [ ] honest about anything broken (never "it works" with a FAIL report)

## Iteration Examples

- "make it brighter" → adjust CONSTANTS palette + fog/sky colors, re-verify
  (mean luminance should move up; report before/after numbers).
- "add a boss" → new entity factory + FSM + stats, update roster, re-verify.
- "instead of 3D, make it a 2D platformer" → new engine folder, port the
  mechanics to canvas2d patterns, keep same slug? NO — new engine = new slug
  dir unless user says otherwise.
- "use this image as the character" → view image, extract features, procedural
  model (low-poly interpretation noted to user), re-verify.

## Notes

- **One file, CDN imports only** (Three.js or nothing). No build steps.
- **Persistent workspace**: `$GAMES_DIR` = `~/games/`, listed and linked from
  progress.md so future sessions find the game.
- **Don't invent middleware**: no fake servers, no "leaderboards" that don't
  exist, multiplayer genuinely unsupported (hot-seat/local only).
