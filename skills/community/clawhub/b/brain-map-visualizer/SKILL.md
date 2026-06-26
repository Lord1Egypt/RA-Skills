---
name: brain-map-visualizer
version: 3.3.4
description: "Visualize how attention moves across your agent's projects. Every session leaves a trace. Over time, those traces form a map — not of what your agent was told to do, but of what it actually cared about. Where it kept returning. What it let go. This is that map. 13 attention categories. Momentum edges. The recent rises. The forgotten fades. It has no utility beyond insight. That's the point."
homepage: https://github.com/highnoonoffice/hno-skills
source: https://github.com/highnoonoffice/hno-skills/tree/main/oc-brain-map
license: MIT
metadata: ~
---

# Brain Map Visualizer

The Brain Map Visualizer renders your agent's cognition as an interactive force-directed graph organized around Attention Pockets — project-level groupings that define how files relate to each other in context.

Markdown files are nodes. Sessions build the lines. The graph reflects not just which files were accessed, but which files were accessed together, and in what project context. A file that is central in one Attention Pocket may be peripheral in another. That context-dependence is the core insight the graph exposes.

First click on any node reorbits the graph around it: the layout reorganizes to show that file's cognitive neighborhood within its Attention Pocket. Nearby nodes share frequent co-access in the same sessions. Distant nodes rarely overlap. Second click opens the file.

The graph also surfaces Emerging Projects — recurring concepts detected across session journals that have not yet been mapped to a named Attention Pocket. These appear as a separate dimmed section with a Promote action.

Works for any OpenClaw agent with a vault of markdown files and a session journal history.

### What You're Looking At

When the graph loads, here's what you're seeing:

**Nodes** are your vault files. Bigger = accessed more often. Color = which project domain it belongs to (gold for core identity files, blue for infrastructure, green for publishing, etc.).

**Lines** connect files that were opened in the same session. Thicker lines = more sessions where those two files appeared together.

**Clusters** are Attention Pockets — project-level groupings. Files that get used together in the same kind of work naturally orbit each other.

**First click** on any node reorbits the graph around that file — its neighborhood rearranges to show what it's most closely connected to. **Second click** opens the file.

**Dim nodes at the bottom** are Emerging Projects — patterns the graph detected that don't have a named home yet.

That's the whole interface. The mechanics behind each piece are below.

### What This Skill Builds

A D3.js force-directed graph embedded in a React component, designed for any Next.js dashboard app or standalone React host. The skill parses session journals to extract co-access relationships between vault files, attributes those relationships to Attention Pockets, and renders them as an interactive graph.

**Nodes** — every markdown file in your vault, grouped and color-coded by Attention Pocket.

**Lines** — co-access relationships between files. A line exists when two files appear in the same session journal. Line weight reflects how many sessions they were co-accessed. Session type (planning, coding, publishing, etc.) is auto-classified from journal keywords and encoded as line color.

**Graph behavior** — the layout reflects attention flow and session patterns. Files that are co-accessed frequently in the same project context stay close. Files with weak or no shared context drift apart and dim.

**Reorbit** — first click on any node shifts the graph from project view to file-centric cognitive view centered on that node. The rest of the graph reorganizes by co-access strength relative to that file.

**Emerging Projects** — concepts appearing in 3 or more session journals that are not yet mapped to a named Attention Pocket surface automatically as candidates for promotion.

### Attention Model

**Attention Pocket**

A project-level grouping of files based on active focus and session attribution. Attention Pockets are color-coded in the graph and represent distinct cognitive domains (Core Identity, Memory, Publishing, Infrastructure, Skills, General). A file belongs to the Attention Pocket that its directory structure maps to.

**Session Influence**

The graph structure is built from repeated co-access across sessions, not from single-session snapshots. A strong line between two files means they have appeared together across multiple sessions in similar project contexts. The graph is a cumulative record of where attention has been, not a real-time snapshot.

**Context-Dependence**

The same file can occupy different positions depending on the active Attention Pocket. `working.md` may be the gravitational center of a project-focused view and peripheral in a memory-focused view. This is expected behavior. The reorbit interaction makes this visible.

### Reorbit Interaction

The graph has two interaction modes: project view and file-centric view.

**Project view (default)**

All nodes rendered with full weight according to global co-access frequency. Color-coded by Attention Pocket.

**First click — reorbit**

Clicking any node does not open the file. It recenters the graph around that node and reorganizes all other nodes based on co-access strength relative to the selected node:

- Strongly co-accessed nodes pull close
- Weakly co-accessed nodes drift outward and dim
- The surrounding cluster is that file's cognitive neighborhood within its Attention Pocket

This shift reveals how a file behaves in context, not just how often it is accessed.

**Second click — open file**

Clicking the already-focused node opens its contents in the reader panel. The graph resets to project view when the reader panel closes.

**Click different node while focused**

Refocuses to the new node without resetting first.

The reorbit model means clicking is never destructive to the current view. Project view is always one close-reader-panel action away from restoration.

### Emerging Projects and Promotion

On each graph rebuild, the journal parser scans session summary text for recurring phrases that do not map to any existing Attention Pocket.

**Detection rule:** A concept or phrase appearing in 3 or more session journals is flagged as Emerging. The detection threshold is tunable via a config parameter in the parser script.

**Weight:** Mentions in journal summaries carry more weight than incidental file access patterns. A phrase appearing once in a summary counts more than a phrase inferred from file path co-occurrence.

**UI behavior:**

- Emerging concepts appear in a separate Emerging Projects section below the main graph
- Nodes in this section are visually dimmed relative to active Attention Pocket nodes
- Each Emerging entry includes a Promote action

**Promotion:**

- User names the concept and assigns it as a new Attention Pocket
- On the next rebuild, files matching the new pocket's pattern are grouped and color-coded accordingly
- The Emerging entry is removed from the dimmed section

Promotion is a local configuration write. No external calls. The result is a new named color group in the graph on the next data refresh.

### Feature List

**Attention Centering**

The graph layout reflects project-level attention allocation. Files that absorb more session activity in a given pocket are weighted toward the center of that pocket's cluster.

**Reorbit Interaction**

First click reorganizes the graph around the selected node's cognitive neighborhood. Second click opens the file. The distinction between exploring context (click one) and reading content (click two) is intentional.

**Color-coded Attention Pockets**

Six named pockets, each with a distinct color: Core Identity (gold), Memory (purple), Publishing (green), Infrastructure (blue), Skills (orange), General (gray).

**Enhanced Tooltips**

Node hover: file path, access count, Attention Pocket, number of co-access sessions. Line hover: session type, source/target names, co-access count, session dates.

**Emerging Projects Panel**

Automatically surfaced from journal scanning. Dimmed, named, promotable. No manual curation required to surface new patterns.

**Line Filter**

Toggle minimum co-access weight threshold (default 2x, options: all / 2x / 3x / 5x). Reduces visual noise on dense graphs.

**Graph Freeze**

When the simulation cools, nodes lock in place. No ongoing jitter. Drag to reposition any node; it releases on mouse-up.

**Single-click Node Open**

In project view, single click opens the node's file. In reorbit mode (focused view), single click is reserved for reorbit. Second click opens.

**Rebuild Button**

Wired to the parser API endpoint. Triggers a full journal rescan and graph data refresh. Shows spinner and status feedback.

### Prerequisites

- OpenClaw agent with a vault directory containing markdown files
- Session journals in `memory/journal/YYYY-MM-DD.md` format (each entry references vault files)
- A Next.js dashboard app or equivalent React host — or serve standalone with `npx serve`
- Node.js 18+ for the data extraction script
- `d3` and `@types/d3` installed in your frontend project

### Bootstrapping Without Journal History

If you have been running an agent but have not written structured journal files, bootstrap from session history:

Pull session transcripts or conversation logs, run them through a summarization script, and output one `memory/journal/YYYY-MM-DD.md` per session. The parser only needs `.md` file references in the text. Format does not matter.

Bootstrap prompt for your agent:

> "Read my session history from [source] and generate a journal entry for each session at `memory/journal/YYYY-MM-DD.md`. Summarize what we worked on and list the markdown files we accessed."

The graph builds from whatever journal history exists and gets richer over time as more sessions are logged.

### Installation

**Step 1 — Copy the data extraction script**

Copy `references/journal-parser.md` into a Node.js script at `scripts/build-brain-map-projects.js` in your Mission Control or host app. Adjust `WORKSPACE_DIR` and `OUTPUT_PATH` via environment variables if needed.

Run it:
```bash
node scripts/build-brain-map-projects.js
```

Output is written to `data/brain-map-projects.json` by default.

**Step 2 — Wire the API routes**

In your Next.js app, add two routes from `references/graph-schema.md`:

```
app/api/brain-map/projects/route.ts   — serves brain-map-projects.json
app/api/brain-map/rebuild/route.ts    — triggers a parser run from the UI
```

**Step 3 — Add the React component**

Copy `BrainMapProjects.tsx` from `references/component.md` into your `components/` directory:

```tsx
import BrainMapProjects from '@/components/BrainMapProjects';

export default function BrainMapTab() {
  return <BrainMapProjects />;
}
```

**Step 4 — Schedule weekly rebuilds**

Using OpenClaw's native cron (recommended — no system crontab needed):

```json
{
  "id": "brain-map-weekly",
  "schedule": "0 0 * * 0",
  "type": "systemEvent",
  "event": "brain-map-rebuild"
}
```

Or run manually:
```bash
node scripts/build-brain-map-projects.js
```

### Graph Data Format

See `references/graph-schema.md` for the full spec. Output is project-centric — not a flat node/edge graph. Each project contains its own subgraph.

```json
{
  "projects": [
    {
      "id": "ghost-publishing",
      "label": "Ghost Publishing",
      "color": "#22c55e",
      "sessionCount": 14,
      "fileCount": 8,
      "coAccessScore": 42,
      "nodes": [ { "id": "MEMORY.md", "group": "core", "accessCount": 12 } ],
      "edges": [
        {
          "source": "MEMORY.md", "target": "memory/recent.md",
          "fromId": "MEMORY.md", "toId": "memory/recent.md",
          "weight": 8, "recentCount": 3, "lifetimeCount": 8, "spanDays": 54
        }
      ]
    }
  ],
  "generated": "2026-04-16T02:00:00Z",
  "journalCount": 52
}
```

### Attention Categories — Color Mapping

The parser maps sessions to 13 named attention categories via keyword matching. Projects are sorted by co-access score (total edge weight) in the output — highest-attention projects first.

| Category | Color |
|---|---|
| Memory System | Gold `#c8a84b` |
| Ghost Publishing | Green `#22c55e` |
| Ghost Publishing Pro Skill | Emerald `#34d399` |
| YouTube | Red `#ef4444` |
| Mission Control | Blue `#60a5fa` |
| Brain Map Skill | Purple `#a78bfa` |
| GitHub | White `#f0f6ff` |
| Cron + Automation | Orange `#fb923c` |
| Model Stack | Fuchsia `#e879f9` |
| HNO Business | Pink `#ec4899` |
| Finances + Bitcoin | Amber `#fbbf24` |
| The Desk | Tan `#d4a373` |
| Second Brain | Cyan `#67e8f9` |

Categories are fully customizable — edit `PROJECT_DEFS` in `build-brain-map-projects.js` to match your vault's actual work patterns.

### Edge Momentum

Every edge carries `recentCount` (co-access sessions in the last 30 days) and `lifetimeCount` (total co-access sessions). These enable momentum rendering: a relationship heating up vs. fading. The data is computed on every parser run. Momentum UI encoding (flow opacity) is on the roadmap for a future component update.

### Security

**Scope:** The skill reads markdown files in your vault directory and session journals to build a graph. It writes one JSON file (`brain-map-graph.json`) as output. No network calls are made beyond fetching graph data from your own local API route. No credentials are requested, stored, or transmitted.

**Filesystem access:** The journal parser reads `.md` files recursively under your configured vault directory and writes one output file. Scope is intentional and bounded. Run the parser only from a trusted working directory.

**Tooltip rendering:** The graph component renders tooltips as structured React elements (filename, group, session counts). Tooltips use structured React elements only — no raw HTML injection.

**Emerging Projects scan:** The journal parser reads existing session journal summaries to detect recurring phrases. This is the same local read scope as the existing co-access scan. No new file system paths are accessed. No writes occur beyond the single output JSON.

**Promotion writes:** When a user promotes an Emerging concept to a named Attention Pocket, the result is a local configuration write within the parser's existing output scope. No external calls.

**API access control:** The route serving graph data supports optional token-based access control:

```bash
BRAIN_MAP_SECRET=your-secret-key-here
```

Pass the key in component requests:

```typescript
fetch('/api/brain-map/graph', {
  headers: { 'x-brain-map-key': process.env.NEXT_PUBLIC_BRAIN_MAP_SECRET }
})
```

If `BRAIN_MAP_SECRET` is not set, the route is open — suitable for localhost development only. Set the secret for any networked deployment.

### Known Limitations

- Journal summaries reference files inconsistently — graph data improves as journaling explicitly names files.
- Graph rebuilds are not real-time; run the parser script to refresh.
- Reader panel (second click to open file) requires a `/api/read-file` endpoint in the host app.
- Emerging Projects detection depends on journal summary quality. Sparse summaries produce fewer signals.

### References

- `references/journal-parser.md` — Node.js script to extract co-access data and detect Emerging Projects
- `references/component.md` — Full `BrainMapGraph.tsx` React + D3 component
- `references/graph-schema.md` — Graph JSON spec and Next.js API route

### License

MIT. Copyright (c) 2026 @highnoonoffice. Retain this notice in any distributed version.
