---
name: azure-devops-reports
description: Read Azure DevOps projects, teams, team members, saved queries, and work items securely; run WIQL-based reporting; and export spreadsheet-ready reports with summaries and charts. Use when the user wants Azure DevOps project lists, team lists, team-member lists, saved query results, sprint/work item reporting, WIQL queries, Excel/CSV exports, charts, assignee/state/type breakdowns, or team/project work item analysis.
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["node", "python3", "pip3"],
        "env": [
          "AZURE_DEVOPS_ORG",
          "AZURE_DEVOPS_PAT"
        ]
      },
      "primaryEnv": "AZURE_DEVOPS_PAT"
    }
  }
---

# Azure DevOps Reports

Use this skill for secure, read-focused Azure DevOps reporting.

## Configuration

Load credentials from a local `.env` file stored in this skill directory.

Required variables:

- `AZURE_DEVOPS_ORG`
- `AZURE_DEVOPS_PAT`

Optional defaults:

- `AZURE_DEVOPS_DEFAULT_PROJECT`
- `AZURE_DEVOPS_DEFAULT_TEAM`
- `AZURE_DEVOPS_DEFAULT_QUERY_ID`
- `AZURE_DEVOPS_OUTPUT_DIR`

If required values are missing, ask the user to create or update `.env` in this skill directory.

## Runtime requirements

This skill requires:

- Node.js
- Python 3
- `pip3`
- Python package: `xlsxwriter`

Install Python dependency once:

```bash
pip3 install -r requirements.txt
```

## Safety guarantees

- Read-only Azure DevOps access only
- No create, update, or delete operations for Azure DevOps work items
- No secret logging
- No Authorization header logging
- No arbitrary shell execution from user input
- Output restricted to local report files under the skill directory
- `AZURE_DEVOPS_OUTPUT_DIR` must resolve inside the skill directory
- Prefer least-privilege PAT scopes: `vso.project` and `vso.work`

## Workflow

1. Load config from the skill-local `.env` file.
2. Resolve project, team, and query id from explicit arguments or configured defaults.
3. Decide whether the request is project-scoped, team-scoped, team-member scoped, saved-query, sprint-scoped, or custom-WIQL.
4. Fetch work item ids via WIQL when filtering is needed.
5. Fetch detailed work item fields.
6. Normalize records for reporting.
7. Default to the configured saved query when no explicit command or query id is provided.
8. Export to JSON or CSV data bundles.
9. Build summary tables for state, assignee, and work item type.
10. Build Excel charts from exported JSON when the user asks for workbook generation.
11. Use project listing, team listing, team-member listing, sprint listing, and saved-query reporting when the user asks in plain language.

## Scripts

- `scripts/projects.js` — list projects
- `scripts/teams.js` — list teams in a project and team members
- `scripts/iterations.js` — list team iterations / current sprint
- `scripts/queries.js` — list saved queries and inspect a query definition
- `scripts/workitems.js` — run work item queries and normalize results
- `scripts/export-report.js` — export JSON/CSV data bundles
- `scripts/build_excel_report.py` — generate Excel workbooks with charts from exported JSON

## Exact script usage

Run all commands from the skill directory:

```bash
cd /path/to/azure-devops-reports
```

### 1) List projects

```bash
node scripts/projects.js list
```

### 2) List teams in a project

```bash
node scripts/teams.js list "Project Name"
```

### 3) List members in a team

```bash
node scripts/teams.js members "Project Name" "Team Name"
```

### 4) List current sprint

```bash
node scripts/iterations.js current "Project Name" "Team Name"
```

### 5) List all iterations / sprints

```bash
node scripts/iterations.js list "Project Name" "Team Name"
```

### 6) List saved queries in a project

```bash
node scripts/queries.js list --project "Project Name"
```

### 7) Get a saved query definition by id

```bash
node scripts/queries.js get --project "Project Name" --id "QUERY_GUID"
```

### 8) Fetch work items using saved query id

Explicit:

```bash
node scripts/workitems.js query-id --project "Project Name" --id "QUERY_GUID"
```

With defaults from `.env`:

```bash
node scripts/workitems.js query-id
```

### 9) List work items closed in the last 7 days

Using the default project from `.env`:

```bash
node scripts/workitems.js closed-last-week
```

With an explicit project:

```bash
node scripts/workitems.js closed-last-week --project "Project Name"
```

### 10) Export report data as JSON

Default saved-query export using `.env` defaults:

```bash
node scripts/export-report.js
```

Explicit saved-query export:

```bash
node scripts/export-report.js query-id \
  --project "Project Name" \
  --id "QUERY_GUID" \
  --format json \
  --out query-data.json
```

Explicit sprint summary export:

```bash
node scripts/export-report.js sprint-summary \
  --project "Project Name" \
  --team "Team Name" \
  --format json \
  --out sprint-summary.json
```

### 11) Build Excel workbook from exported JSON

```bash
python3 scripts/build_excel_report.py \
  --input output/query-data.json \
  --output output/query-report.xlsx
```

## Ask ClawBot in plain English

These requests should map to the skill without manual script execution:

- `show my Azure DevOps projects`
- `how many teams do we have?`
- `list all team members in <Your Team Name> team`
- `can you list the sprints?`
- `generate the Azure DevOps report`
- `regenerate the excel`
- `list all work items closed in last week`
- `summarize closed items from last week`
- `show current progress of sprint 07`
- `which team member has most open items?`

## References

Read these only if needed:

- `references/field-mapping.md` for normalized field choices
- `references/report-types.md` for report presets and chart ideas
- `references/api-notes.md` for endpoint notes and PAT scope guidance
