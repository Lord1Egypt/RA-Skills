# Project Structure Blueprints

Use one blueprint and keep it stable for at least one milestone.

## Blueprint A - Browser Instant (No Build)

```text
game-project/
|-- index.html
|-- styles.css
|-- main.js
|-- game/
|   |-- config.js
|   |-- state.js
|   |-- systems/
|   |   |-- input.js
|   |   |-- movement.js
|   |   `-- scoring.js
|   `-- ui/
|       `-- hud.js
|-- assets/
|   |-- models/
|   |-- textures/
|   `-- audio/
`-- docs/
    |-- idea-brief.md
    |-- player-persona.md
    `-- playtest-notes.md
```

## Blueprint B - Browser Structured (TS + Bundler)

```text
game-project/
|-- src/
|   |-- app/
|   |   |-- bootstrap.ts
|   |   |-- game-loop.ts
|   |   `-- scene.ts
|   |-- domain/
|   |   |-- entities/
|   |   |-- systems/
|   |   `-- rules/
|   |-- presentation/
|   |   |-- hud/
|   |   `-- fx/
|   `-- infra/
|       |-- input/
|       |-- save/
|       `-- telemetry/
|-- public/
|-- tests/
|-- docs/
|   |-- concept/
|   |-- preferences/
|   |-- balancing/
|   `-- release/
`-- tools/
```

## Blueprint C - Advanced Multi-Feature Project

```text
game-project/
|-- client/
|-- server/
|-- shared/
|-- content-pipeline/
|-- analytics/
|-- tests/
|   |-- deterministic/
|   |-- integration/
|   `-- load/
|-- docs/
|   |-- product/
|   |-- technical/
|   |-- user-preferences/
|   `-- postmortems/
`-- operations/
```

## User Preference and Idea Files

Keep these files even in small projects:
- `docs/concept/idea-brief.md` for game fantasy and core pitch
- `docs/preferences/user-taste.md` for style and mechanics preferences
- `docs/balancing/targets.md` for difficulty and reward tuning goals

These files reduce rework when switching agents.
