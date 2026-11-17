# Templates

These are skeletons: replace every example row with what the actual project contains, and delete any row it doesn't need.

## Entry point (CLAUDE.md or AGENTS.md), target ≤ ~8 KB

```markdown
# <Project> — operating guide

<Two or three sentences: what it is, where it runs, what it must never break.>

## Read first
1. <docs index>  2. <architecture overview>  3. <security guide, if any>
When documents disagree: <order of authority>.

## Hard rules
- <Never-rules and security rules, each one line, bold lead-in.>

## Workflow
- <Branching, PR target, issue linking, commit style, versioning, attribution rules.>

## Commands
<The three to six commands every change runs.>

## Reflexes
| When you are about to… | Do this |
|---|---|
| <add a route / tool / migration / UI component> | <the steps a test or reviewer enforces> |

## Project map
Before opening files, read the router for the task, then only the files it points to:
- [docs/map/PRODUCT.md](docs/map/PRODUCT.md): where the code for each area lives
- [docs/map/OPERATIONS.md](docs/map/OPERATIONS.md): build, test, CI, release, deploy, configuration
- [docs/map/DOCS.md](docs/map/DOCS.md): which design or reference document answers which question

The map guides what to read first. It never replaces the rules above or a release gate.

**Keep the map true.** A change that adds, moves or removes a file a router names updates
that router in the same change. Each code area keeps its own short README router, linked from
PRODUCT.md, except folders that ship to users, which are routed from docs/map/ instead. Routers stay about 15–35 lines, link only to files that exist, and never hold
secrets. Reference material goes in docs/, not here.
```

If the project uses both Claude Code and Codex, the template above is `AGENTS.md`, and `CLAUDE.md` becomes:

```markdown
@AGENTS.md

<!-- Claude Code only: anything that applies to Claude Code and not to other agents. Usually nothing. -->
```

If only one tool is used and the other file already exists, make it a pointer: `The full guide is [CLAUDE.md](CLAUDE.md); its rules apply to every agent`, followed by the same router links.

## docs/map/PRODUCT.md

```markdown
# Map — product code

Start here for any code change. Find the area, open its README router, then only what the task needs.

| Area | What lives there | Design doc |
|---|---|---|
| [src/README.md](../../src/README.md) | <server: entry points and domain folders> | <architecture doc> |
| `src/<domain>/` | <what it owns, in a few words> | <doc> |
| [app/README.md](../../app/README.md) | <client app: sections, features, primitives, UI rules> | <design system> |

<Changes that cross repositories, and where the other half lives.>
```

## Area README (for example src/README.md)

```markdown
# src/ — <what this area is>

<One sentence on where it runs, one on where tests live, and the request path if there is one.>

| Folder | What lives there | Read before changing |
|---|---|---|
| `routes/` | <which file owns which endpoints> | <API doc> |

<This area's own rules, such as design or naming rules, when they apply only here.>
```

## docs/map/DOCS.md (or PLAN.md / CONTENT.md)

```markdown
| Task | Read |
|---|---|
| <a question someone actually asks> | <the one document that answers it> |
```

End it with a line that marks notes, plans and ADRs as history, so they are checked against the code before being trusted.
