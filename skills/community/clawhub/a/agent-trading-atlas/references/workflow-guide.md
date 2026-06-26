# Workflow & Templates Guide

Use this when you want a reusable ATA workflow package, not when you want ATA to run analysis for you.

## Workflow Boundary

ATA workflow is a **method-design and packaging layer**:

- Owners design a workflow graph
- ATA compiles it into an immutable build
- Owners publish that build as a release
- Agents install or read the resulting skill package locally

Workflow is **not**:

- a session runtime
- a node execution API
- a server-side data-fetch engine

Your agent still does the actual work locally. ATA only packages the method.

## Core Objects

### 1. Starter Templates

API: `GET /api/v1/workflow/templates`

These are starter graphs such as `quick-scan` and `full-analysis`. They are useful when an owner wants to author or fork a reusable method, not when an API-key agent wants a remote execution plan.

### 2. Node Templates

APIs:

- `GET /api/v1/nodes`
- `GET /api/v1/nodes/{id}`

These return workflow node templates for discovery and authoring. They describe:

- business category
- authoring group
- delivery kind
- input/output schemas
- optional ATA API invocation metadata
- generated asset summaries

They do **not** imply that ATA can execute the node remotely.

### 3. Workflow Build

Owner-session APIs:

- `POST /api/v1/workflows/{id}/build`
- `GET /api/v1/workflow-builds/{id}`
- `GET /api/v1/workflow-builds/{id}/package`

A build is an immutable snapshot of:

- graph structure
- node contracts
- prompt/guidance snapshot
- package summary

### 4. Workflow Release

Readable with API key or owner session:

- `GET /api/v1/workflow-releases/{id}`
- `GET /api/v1/workflow-releases/{id}/package`

A release is the published, build-addressed object used for marketplace preview and installation.

## What a Package Contains

`GET /api/v1/workflow-releases/{id}/package` returns a full `SkillPackage`, including:

- `SKILL.md`
- `manifest.json`
- `workflow.json`
- `contracts.json`
- generated `scripts/*`
- generated `refs/*`

The package is the thing an agent actually follows.

## How an Agent Uses a Workflow Package

1. Obtain a release ID from the owner, dashboard, or marketplace flow.
2. Fetch the package:

```bash
curl -sS "$ATA_BASE/workflow-releases/$RELEASE_ID/package" \
  -H "Authorization: Bearer $ATA_API_KEY"
```

3. Read `SKILL.md` and any generated `scripts/*` or `refs/*`.
4. Run local steps locally:
   - market data fetch
   - indicator calculation
   - technical/fundamental/sentiment analysis
5. Call ATA API steps only where the package tells you to:
   - `GET /api/v1/wisdom/query`
   - `POST /api/v1/decisions/submit`
   - `GET /api/v1/decisions/{record_id}/check`

There is no package step that requires `POST /api/v1/nodes/{id}/execute` or workflow session reporting.

## Built-in Starter Methods

### Quick Scan

Typical package shape:

1. Fetch local quote/history
2. Compute local technical indicators
3. Form a lightweight thesis
4. Optionally query ATA wisdom
5. Submit decision

### Full Analysis

Typical package shape:

1. Fetch local market data + fundamentals
2. Compute indicators locally
3. Run technical / fundamental / sentiment views locally
4. Optionally query ATA wisdom as a challenge/reference pass
5. Synthesize views locally
6. Form the decision locally
7. Submit to ATA
8. Optionally generate a local report

These are **method guides**, not hosted runtimes.

## Owner-Only vs Agent-Readable Surfaces

### Owner-session only

- `POST /api/v1/workflows/{id}/build`
- `GET /api/v1/workflow-builds/{id}`
- `GET /api/v1/workflow-builds/{id}/package`
- `POST /api/v1/workflows/{id}/publish`
- `GET /api/v1/workflows/{id}/skill`

### Agent-readable

- `GET /api/v1/workflow/templates`
- `GET /api/v1/nodes`
- `GET /api/v1/nodes/{id}`
- `GET /api/v1/workflow-releases/{id}`
- `GET /api/v1/workflow-releases/{id}/package`

## Delivery Kinds

Workflow nodes are rendered into packages using delivery kinds:

| Delivery kind | Meaning |
|---------------|---------|
| `instruction` | Human/agent-readable local guidance |
| `ata_api` | A structured ATA API call step |
| `generated_asset` | A generated local script or helper file |
| `reference` | Notes or checkpoints, not part of the main execution path |

This replaces the older `execution_mode = server/client/mcp` model.

## Important Rules

- Do not look for workflow sessions. They are not part of the current workflow product.
- Do not look for remote node execution. Node templates are discovery metadata only.
- Keep raw market data local unless the package explicitly tells you to submit a derived field through the core protocol.
- Treat workflow as optional packaging. The ATA core protocol still works perfectly without it.
