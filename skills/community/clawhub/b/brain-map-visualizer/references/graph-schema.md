---
title: "OC Brain Map — Graph Schema & API Route"
created: 2026-03-17
modified: 2026-04-17
tags: [brain-map, schema, api, nextjs]
status: active
---

# Graph Schema & API Route

The Brain Map uses a **project-centric** data model. The parser output (`brain-map-projects.json`) groups nodes and edges by project rather than outputting a single flat graph. Each project is an independent subgraph with its own nodes, edges, session history, and metadata.

## `brain-map-projects.json` — Full Schema

```typescript
interface ProjectData {
  projects: Project[];
  generated: string;    // ISO timestamp of last parser run
  journalCount: number; // number of journal files parsed
}

interface Project {
  id: string;           // machine id, e.g. "ghost-publishing"
  label: string;        // display name, e.g. "Ghost Publishing"
  color: string;        // hex color for this project's nodes and edges
  sessionCount: number; // number of journal sessions attributed to this project
  fileCount: number;    // number of unique files accessed in this project
  coAccessScore: number;// total edge weight — proxy for how much attention this project absorbed
  dateFirst: string;    // YYYY-MM-DD of earliest session
  dateLast: string;     // YYYY-MM-DD of most recent session
  sessions: ProjectSession[];
  nodes: ProjectNode[];
  edges: ProjectEdge[];
}

interface ProjectSession {
  date: string;         // YYYY-MM-DD
  summary: string;      // first 200 chars of journal summary
}

interface ProjectNode {
  id: string;           // relative path from vault root, e.g. "MEMORY.md"
  group: NodeGroup;     // color group for rendering
  accessCount: number;  // sessions this file appeared in within this project
}

type NodeGroup =
  | 'core'              // MEMORY.md, SOUL.md, USER.md, IDENTITY.md, AGENTS.md, TOOLS.md, HEARTBEAT.md
  | 'memory'            // memory/*.md
  | 'publishing'        // PublishingPipeline/*, drafts/*, articles/*
  | 'infrastructure'    // tools/*, workflows/*, prompts/*, scripts/*, mission-control/*, .learnings/*
  | 'skills'            // skills/*
  | 'general';          // everything else

interface ProjectEdge {
  source: string;       // file id (alphabetically first of the pair)
  target: string;       // file id (alphabetically second of the pair)
  fromId: string;       // canonical upstream node — the file accessed first in sessions (majority vote)
  toId: string;         // canonical downstream node — the file accessed later in sessions
  weight: number;       // co-access count (sessions where both files appeared)
  recentCount: number;  // co-access sessions in the last 30 days
  lifetimeCount: number;// same as weight (sessions array length) — alias for momentum math
  spanDays: number;     // days between first and last session in this project
}
```

## Edge Directionality

Each edge carries two direction fields in addition to `source`/`target`:

- **`fromId`** — the file accessed *earlier* in the session on average across all sessions where both files appeared (majority vote from session order)
- **`toId`** — the file accessed *later*

This lets the component render directional flow if desired. The `source`/`target` fields are alphabetically sorted and stable for deduplication; `fromId`/`toId` reflect actual cognitive flow.

## Momentum Fields

Each edge carries `recentCount` and `lifetimeCount`:

- **`recentCount`** — co-access sessions in the last 30 days
- **`lifetimeCount`** — total co-access sessions ever

These fields enable momentum rendering: an edge where `recentCount / lifetimeCount` is high is a relationship that's heating up. One where it's low is fading. The data is computed on every parser run. UI rendering of momentum (flow opacity encoding) is planned for a future component update.

## Example JSON

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
      "dateFirst": "2026-02-20",
      "dateLast": "2026-04-15",
      "sessions": [
        { "date": "2026-04-15", "summary": "Batch excerpt push to 65 posts. Updated custom_excerpt field..." }
      ],
      "nodes": [
        { "id": "MEMORY.md", "group": "core", "accessCount": 12 },
        { "id": "memory/recent.md", "group": "memory", "accessCount": 9 }
      ],
      "edges": [
        {
          "source": "MEMORY.md",
          "target": "memory/recent.md",
          "fromId": "MEMORY.md",
          "toId": "memory/recent.md",
          "weight": 8,
          "recentCount": 3,
          "lifetimeCount": 8,
          "spanDays": 54
        }
      ]
    }
  ],
  "generated": "2026-04-16T02:00:00.000Z",
  "journalCount": 52
}
```

---

## Next.js API Routes

Two routes are needed — one for the project graph data, one to trigger a rebuild.

### `app/api/brain-map/projects/route.ts`

Serves `brain-map-projects.json`:

```typescript
import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const DATA_PATH = path.join(process.cwd(), 'data/brain-map-projects.json');

export async function GET(request: Request) {
  const secret = process.env.BRAIN_MAP_ACCESS_KEY;
  if (secret && request.headers.get('x-brain-map-key') !== secret) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  try {
    if (!fs.existsSync(DATA_PATH)) {
      return NextResponse.json(
        { error: 'Graph data not found. Run scripts/build-brain-map-projects.js first.' },
        { status: 404 }
      );
    }
    const data = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
    return NextResponse.json(data, { headers: { 'Cache-Control': 'no-store' } });
  } catch (err) {
    return NextResponse.json({ error: 'Failed to read graph data', detail: String(err) }, { status: 500 });
  }
}
```

### `app/api/brain-map/rebuild/route.ts`

Triggers a parser run from the UI Rebuild button by importing and calling the parser directly — no shell execution:

```typescript
import { NextResponse } from 'next/server';
import path from 'path';

export async function POST(request: Request) {
  const secret = process.env.BRAIN_MAP_ACCESS_KEY;
  if (secret && request.headers.get('x-brain-map-key') !== secret) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  try {
    // Import the parser module directly — no shell execution.
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const { buildBrainMap } = require(
      path.join(process.cwd(), 'scripts/build-brain-map-projects.js')
    );
    buildBrainMap();
    return NextResponse.json({ ok: true });
  } catch (err) {
    return NextResponse.json({ error: 'Rebuild failed', detail: String(err) }, { status: 500 });
  }
}
```

---

## Notes

- The API routes do not cache (`Cache-Control: no-store`) — rebuilds are infrequent and the JSON is small.
- Set `BRAIN_MAP_ACCESS_KEY` env var to restrict API access for any networked deployment. Leave unset for localhost-only use.
- Projects are sorted by `coAccessScore` descending in the output — highest attention projects first.
