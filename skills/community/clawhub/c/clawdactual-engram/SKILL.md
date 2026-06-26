---
name: engram
description: Build, query, and maintain structured knowledge graphs. Use when you need to remember relationships between code components, services, people, or any concepts across sessions. Provides persistent graph storage with type hierarchies, relationship ontology, branch overlays, git integration, and cross-model linking. Trigger on "engram", "knowledge graph", "dependency graph", "build a model of", "map the architecture", "what depends on", "blast radius", or any request to track relationships between entities.
metadata:
  author: Morpheis
  version: "2.2.0"
---

# Engram
*Persistent knowledge traces for AI agents — like a brain's memory engrams, but queryable.*

A persistent knowledge graph for AI agents. Store nodes (components, services, people, concepts) and edges (calls, depends_on, owns) in a local SQLite database. Survives sessions. Query dependencies, find paths, check freshness against git, export for visualization.

## Installation

```bash
npm install -g @clawdactual/engram
```

This installs the `engram` CLI globally. Verify with:

```bash
engram --help
```

## How to Run

```bash
engram <command>
```

**Database:** `~/.config/engram/models.db` (override: `ENGRAM_DB_PATH=/path/to/db`)

**Global flag:** `--json` on any command outputs structured JSON.

**Session awareness:** Add a line to your workspace bootstrap file (e.g., `AGENTS.md`) so future sessions know the knowledge graph exists and should maintain it. See the README's "Agent Setup" section.

## Quick Reference

### Models (containers for graphs)

```bash
engram create <name> [-t code|org|concept|infra] [-d "description"] [-r /repo/path]
engram list
engram delete <name>
engram export <name> [-f jsonld|json|dot] [-o file]
engram import <file>
```

### Nodes

```bash
engram add <model> <label> [--type <type>] [-m key=value ...]
engram add <model> <label> --upsert [--type <type>] [-m key=value ...]
engram upsert <model> <label> [--type <type>] [-m key=value ...]
engram rm <model> <node>
engram update <model> <node> [--label new] [--type new] [-m key=value ...]
engram verify <model> <node>           # mark as recently verified
engram nodes <model> [-t type]
```

`--set key=value` is accepted anywhere node metadata is accepted; it is an alias for `--meta`/`-m`. Prefer `engram upsert` for incremental agent discoveries when the node may already exist.

### Edges

```bash
engram link <model> <source> <rel> <target> [-m key=value ...]
engram unlink <model> <source> <rel> <target>
engram edges <model> [--from node] [--to node] [--rel type]
```

### Queries

```bash
engram q <model> <node>                # neighbors (depth 1)
engram q <model> <node> --depth 3     # expand neighborhood
engram q <model> --affects <node>     # what breaks if this changes? (reverse traversal)
engram q <model> --depends-on <node>  # what does this need? (forward traversal)
engram q <model> -t service           # all nodes of type (includes subtypes)
engram q <model> --stale --days 14    # nodes not verified in 14+ days
engram q <model> --orphans            # nodes with no edges
engram path <model> <from> <to> [--max-depth N]  # all paths between two nodes
```

### Search (cross-model)

```bash
engram search <query>                 # search ALL models (labels, types, metadata)
engram search <query> --model myapp   # search within one model
engram search <query> --limit 10      # max results (default 5)
engram search <query> --exclude zink-family --exclude test  # skip models
engram search <query> --json          # JSON output for recall/automation
```

Results show each matching node + its 1-hop edges, grouped by model.

### Types & Relationships

```bash
engram type list                      # show type hierarchy tree
engram type add <label> [--parent p] [--domain code|org|infra|concept]
engram type rm <label>
engram rel list                       # show all relationship types with inverses
engram rel add <label> [--inverse inv]
engram rel rm <label>
```

### Branch Overlays (feature branch knowledge tracking)

Use overlays when working on feature branches, reviewing PRs, or doing any work that hasn't merged yet. Overlays keep the base model clean while capturing architectural discoveries. Merge the overlay when the PR/branch merges; delete it if the branch is abandoned.

```bash
engram branch <model> <branch-name>             # create overlay
engram branch <model> --list                    # list overlays
engram merge <model> <branch-name>              # fold into parent
engram branch <model> <branch-name> --delete    # discard

# Add nodes/edges to an overlay (use --branch flag)
engram add <model> <label> -t <type> -m key=value --branch <branch-name>
engram link <model> <source> <rel> <target> --branch <branch-name>
```

**Key rule:** When working on a feature branch, always use `--branch <branch-name>`. Only write directly to the base model for merged/stable knowledge.

### Git Integration (code models only)

```bash
engram check <model>       # compare anchor vs HEAD, show affected nodes
engram refresh <model>     # update anchor to HEAD, mark all verified
engram diff <model>        # detailed file-by-file diff with affected subgraph
engram stale <model>       # show stale nodes and edges
```

### Cross-Model

```bash
engram xlink <model1> <node1> <rel> <model2> <node2>
```

### Batch

```bash
echo "add mymodel NodeA --type service
add mymodel NodeB --type database
link mymodel NodeA depends-on NodeB" | engram batch mymodel
```

### Scaffold (auto-generate engram from repo)

Generate a starting-point engram from a repository's file structure. Outputs batch import commands for top-level modules, API routes, services, workflows, clients, and commands.

```bash
# Preview what would be generated (no changes)
engram-scaffold ~/path/to/repo model-name --dry-run

# Generate batch file, then import (scaffold.sh lives in the engram repo's tools/ directory)
./tools/scaffold.sh ~/path/to/repo model-name
engram batch <model> < /tmp/engram-scaffold-*.txt
```

The scaffold is a **skeleton** — enrich nodes with descriptions and add cross-service relationship edges after import. Supports Node.js/TypeScript repos (Medusa, NestJS, CLI), monorepos.

## Built-in Types (extensible)

```
thing
├── code: component, page, widget, hook, function, service, microservice,
│         middleware, database, library, config, script, test-runner, module
├── org: person, team, role, company
├── infra: server, container, network, endpoint
└── concept: process, event, rule
```

Type queries include subtypes: `engram q model -t service` finds services AND microservices.

## Built-in Relationships (extensible)

| Relationship | Inverse |
|---|---|
| calls | called_by |
| depends_on | depended_on_by |
| contains | contained_in |
| owns | owned_by |
| uses | used_by |
| extends | extended_by |
| implements | implemented_by |
| configures | configured_by |
| produces | produced_by |
| consumes | consumed_by |
| proxies_to | proxied_by |
| manages | managed_by |
| tests | tested_by |
| belongs_to | has_member |
| renders | rendered_by |

## Best Practices for Building Models

### First Install: Seed Your Environment

On first use, scan your workspace and create models for:
- **Code** — repos you work on. Modules, services, dependencies.
- **Org** — company structure. People, teams, repos, service relationships, trust levels.
- **Infrastructure** — local tools. Email chains, SSH configs, credential paths, channel setups.
- **People** — who you interact with. Roles, channels, trust levels (owner/boss/coworker/friend).

A fresh session should be able to query the graph and understand your operational context immediately. This is a one-time investment that compounds every session.

### The Hybrid Approach (Recommended)

After testing both "review everything first, then batch" and "enter as you go", the optimal workflow is:

1. **Explore first (5-10 min)** — Scan the codebase or domain. Read key files, understand major components. Don't enter anything yet.

2. **Batch the skeleton** — Create all major nodes and their primary relationships in one batch command. This captures the obvious architecture quickly.
   ```bash
   engram batch myapp <<EOF
   add Frontend --type component -m file=src/App.tsx
   add API --type service -m file=src/api/server.ts
   add DB --type database
   link Frontend calls API
   link API depends_on DB
   EOF
   ```

3. **Add discoveries incrementally** — During coding, when you discover non-obvious relationships (e.g., "this function silently depends on NODE_ENV being set"), add them immediately:
   ```bash
   engram upsert myapp isPubSubDisabled --type function -m "note=returns false in production regardless of DISABLE_AUTH"
   engram link myapp fleet-rest calls isPubSubDisabled
   ```

4. **Review after sessions** — Quick pass: "Did I discover anything worth keeping?" Batch any accumulated additions.

### What to Model (and What Not To)

**DO model:**
- Services, modules, and their dependencies (the skeleton)
- Non-obvious relationships you'll forget (the surprises)
- Cross-repo connections (A calls B in a different repo)
- Config dependencies that cause subtle bugs
- External service integrations

**DON'T model:**
- Every file in the repo (too granular, maintain cost > query value)
- Internal function calls within a single module (grep handles this)
- Dependencies that are obvious from imports (the code is the model)
- Anything that changes every commit (constant staleness)

### Granularity Sweet Spot

Module/service level is the sweet spot for code models. Too fine (every function) = expensive to maintain. Too coarse (just repo names) = barely better than a README. The test: would a new session benefit from knowing this relationship exists? If yes, model it.

### Org Charts and People Graphs

The tool handles org charts well with `type: org` models and `type: person` nodes. A few tips:

**Dual-reporting:** People often report to multiple managers. Use multiple `reports_to` links — the graph handles this naturally:
```bash
engram link Ken reports_to Tom
engram link Ken reports_to Deepak
```

**Part-time / contractor status:** Encode employment status in metadata, not separate node types:
```bash
engram add Brandon --type person -m role="Hardware Manager (Part-Time)"
```

**Hierarchy queries work well:** `engram q org --affects CEO` shows everyone who reports up to that person (direct and transitive). `engram path org Engineer CEO` shows the reporting chain.

**Iterative correction is the norm.** Org charts are rarely right on the first pass — you'll get the public website version, then the human corrects you. Batch the skeleton from public info, then update incrementally as corrections come in. The `rm` and `unlink` commands make this cheap.

**Keep it current:** People leave, roles change. Org models go stale faster than code models. When you learn someone left, `rm` them immediately rather than marking them inactive.

## Common Workflows

### Map a codebase architecture

```bash
engram create myapp -t code -d "My application" -r /path/to/repo
engram add myapp Frontend --type component -m file=src/App.tsx
engram add myapp API --type service -m file=src/api/server.ts -m port=3000
engram add myapp DB --type database -m engine=postgres
engram link myapp Frontend calls API -m via="REST /api"
engram link myapp API depends-on DB
engram refresh myapp   # anchor to current git HEAD
```

### Check blast radius before a change

```bash
engram q myapp --affects API       # everything upstream of API
engram path myapp Frontend DB      # all paths from Frontend to DB
engram check myapp                 # what git changes affect which nodes
```

### Branch overlay for feature work

```bash
engram branch myapp feature/new-cache
engram add myapp Redis --type database
engram link myapp API uses Redis
# ... later ...
engram merge myapp feature/new-cache   # fold changes into base model
```

### Share models between agents (JSON-LD)

```bash
engram export myapp -f jsonld -o myapp.jsonld    # export with semantic context
engram import myapp.jsonld                        # another agent imports it
```

### Visualize with Graphviz

```bash
engram export myapp -f dot | dot -Tpng -o graph.png   # requires graphviz installed
engram export myapp -f dot -o myapp.dot                # save DOT file
```

### Track freshness over time

```bash
engram stale myapp --days 7        # what hasn't been verified this week?
engram verify myapp API            # mark a node as freshly verified
engram refresh myapp               # mark everything verified (after review)
```

### Maintain engrams with git diffs

When code changes, use `engram check` to see which nodes are affected, then update:

```bash
# 1. See what changed since last review
engram check myapp
# Output: lists changed files → affected nodes → affected edges

# 2. For cosmetic/rename changes (no structural change): just refresh
engram refresh myapp

# 3. For structural changes (new files, new dependencies, removed modules):
#    a. Check what's new/deleted
engram diff myapp
#    b. Add nodes for new files
engram add myapp NewService --type service -m file=src/new-service.ts
engram link myapp API calls NewService
#    c. Remove nodes for deleted files
engram rm myapp OldService
#    d. Update metadata if file paths changed
engram update myapp SomeModule -m file=src/new-path/module.ts
#    e. Refresh to anchor at new HEAD
engram refresh myapp
```

**Key principle:** `check` shows you what's stale, `diff` shows the detail, and `refresh` marks everything verified. The git anchor tracks *when you last reviewed the model* — it's not automatic sync, it's aided maintenance.

**The file→node mapping is the bridge.** Always include `file=path/to/file.ts` in node metadata — this is what `check` and `diff` use to map git changes to graph nodes. Without it, the node won't appear in staleness reports.

**After a rename/refactor:** If you renamed files but the structure is the same, just update file metadata and refresh. If you restructured (split a module, merged services), update the graph to match and then refresh.

### Updating engrams after code changes (source-of-truth workflow)

When you've just modified code and need to update the model, **always verify against the actual source** — never update from memory alone.

```bash
# 1. See what files changed (the source of truth)
cd /path/to/repo && git diff HEAD~N --stat        # or git diff main..branch --stat

# 2. For each changed file, review what actually changed
git diff HEAD~N -- src/changed-file.ts

# 3. List current engram nodes for this model
engram nodes mymodel

# 4. Cross-reference: for each changed file, find its engram node(s)
#    Check if the node's metadata/note is still accurate
#    Check if edges are still correct (added/removed imports, calls, etc.)

# 5. Update stale nodes with verified information from the diff
engram update mymodel <node-id> -m 'note=Updated description from actual code'

# 6. Check for stale edges (did you remove a dependency? add a new call?)
engram edges mymodel --from <changed-node>
engram edges mymodel --to <changed-node>
# Remove edges that no longer exist, add new ones

# 7. Add nodes for new exports/modules introduced in the changes
engram upsert mymodel NewThing -t function -m file=src/file.ts 'note=...'

# 8. Refresh the git anchor
engram refresh mymodel
```

**Anti-pattern:** Updating engram nodes from working memory of what you *think* you changed. The code is the source of truth — always `git diff` first, then update the graph to match. This is especially important after multi-file refactors where it's easy to miss removed dependencies or new relationships.

**The 30-second rule:** If you can't verify an engram update against the actual source in 30 seconds, you're guessing. Run the diff.
