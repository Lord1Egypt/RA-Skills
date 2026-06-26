# Backend Profiles (Capability-Driven)

Use these as neutral archetypes. Start from capability fit, not library fandom.

## web-2d-ui-first
Best when:
- menus / HUD / overlays dominate
- input clarity matters more than simulation complexity
- web delivery is primary

Strengths:
- fast iteration
- excellent UI layering
- easy shareability

Risks:
- can drift into app-like architecture unless game state is explicit

Specialist follow-through:
- `game-web-2d-specialist`

## web-2d-world-first
Best when:
- the playfield dominates
- simulation, collisions, and moment-to-moment action matter most

Strengths:
- game loop stays central
- good for action, arcade, puzzle, bullet-hell

Risks:
- UI can become an afterthought without an explicit HUD plan

Specialist follow-through:
- `game-web-2d-specialist`

## web-3d-preview
Best when:
- 3D presentation matters
- fast preview and browser delivery are still important

Strengths:
- quick sharing
- strong preview loops
- good for stylized 3D or hybrid UI-heavy products

Risks:
- easy to overbuild visuals before gameplay proves out
- performance budgets matter earlier

Specialist follow-through:
- `game-web-3d-specialist`

## engine-embedded-2d
Best when:
- the project already lives in a full engine ecosystem
- or stronger editor/runtime conventions are clearly worth it

Strengths:
- mature tooling
- many built-in systems

Risks:
- can be too heavy for rapid AI-native iteration

## engine-embedded-3d
Best when:
- the product clearly needs deeper engine systems from the start

Strengths:
- mature 3D systems
- existing production workflows

Risks:
- large surface area for agent-driven work
- expensive when the brief is vague

## custom-shader-lab
Best when:
- procedural visuals or graphics R&D are the point

Strengths:
- expressive
- great for visual experiments

Risks:
- UX and core loop can be underbuilt if not actively protected

## Selection rules
- Choose the narrowest profile that satisfies the spec.
- Prefer the profile with the shortest path to the chosen quality target.
- If the repo is already committed to a viable backend, bias toward that unless the current backend is the problem.
- Use compare mode only when uncertainty is real or the user explicitly asks for it.
- Compare mode usually costs more tokens and time; warn the user when enabling it.
