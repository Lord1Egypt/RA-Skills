# Azure DevOps Reports

A read-focused OpenClaw skill for Azure DevOps.

It can:

- list Azure DevOps projects
- list teams in a project
- list members in a team
- list sprints / iterations
- fetch work items from a saved query
- export report data to JSON
- generate Excel workbooks with charts using Python
- summarize sprint progress and recent closed work

This skill is designed around a secure, low-risk workflow:

- **Node.js** handles Azure DevOps API access and data normalization
- **Python** handles Excel workbook generation with native charts
- credentials are loaded from a skill-local `.env`
- reports are read-only by default

---

## Features

- Secure Azure DevOps REST API access using PAT
- Default saved-query workflow using `.env` values
- Project, team, member, and sprint listing
- Work item fetching with WIQL or saved query id
- Weekly reporting support
- Excel workbook generation with:
  - `RawData` sheet
  - `Summary` sheet
  - `WeeklyTrendData` sheet
  - `Charts` sheet

---

## Security model

This skill is intentionally narrow and read-focused.

### Safety guarantees

- **Read-only by default**
- **No create/update/delete actions for Azure DevOps work items**
- **No email sending**
- **No arbitrary shell execution from user input**
- **No secret logging**
- **No Authorization header logging**
- **No PAT values stored in source control**
- **Local output only**
- **Output file writes restricted to the skill directory**
- **`AZURE_DEVOPS_OUTPUT_DIR` must resolve inside the skill directory**

### Required PAT scopes

Use least-privilege Azure DevOps PAT scopes:

- `vso.project`
- `vso.work`

No write scopes or admin scopes are required for the intended workflow.

### Secrets

- Keep `.env` local
- Never commit `.env`
- Commit only `.env.example`
- Primary credential: `AZURE_DEVOPS_PAT`
- This skill reads configuration from the skill-local `.env` file only

---

## Requirements

- OpenClaw
- Node.js
- Python 3
- `pip3`
- `xlsxwriter`

Install Python dependency:

```bash
pip3 install -r requirements.txt
```

---

## Configuration

Create a local `.env` file in the skill directory.

Example:

```env
AZURE_DEVOPS_ORG=your-org-name
AZURE_DEVOPS_PAT=your-personal-access-token

AZURE_DEVOPS_DEFAULT_PROJECT=Your Project Name
AZURE_DEVOPS_DEFAULT_TEAM=Your Team Name
AZURE_DEVOPS_DEFAULT_QUERY_ID=your-query-guid
AZURE_DEVOPS_OUTPUT_DIR=output
```

### Required variables

- `AZURE_DEVOPS_ORG`
- `AZURE_DEVOPS_PAT` ← primary credential

### Useful defaults

- `AZURE_DEVOPS_DEFAULT_PROJECT`
- `AZURE_DEVOPS_DEFAULT_TEAM`
- `AZURE_DEVOPS_DEFAULT_QUERY_ID`
- `AZURE_DEVOPS_OUTPUT_DIR` (must remain inside the skill directory)

---

## How it works

### Data flow

1. Node.js loads config from the skill-local `.env`
2. Node.js fetches Azure DevOps data
3. Node.js normalizes work items into a clean JSON bundle
4. Python reads the JSON bundle
5. Python generates an `.xlsx` report with charts

### Default report flow

The default report flow uses:

- `AZURE_DEVOPS_DEFAULT_PROJECT`
- `AZURE_DEVOPS_DEFAULT_QUERY_ID`

That means you can generate the default report without manually passing project/query values every time.

---

## Script usage

Run from the skill directory:

```bash
cd /path/to/azure-devops-reports
```

### List projects

```bash
node scripts/projects.js list
```

### List teams in a project

```bash
node scripts/teams.js list "Project Name"
```

### List team members

```bash
node scripts/teams.js members "Project Name" "Team Name"
```

### List current sprint

```bash
node scripts/iterations.js current "Project Name" "Team Name"
```

### List all iterations / sprints

```bash
node scripts/iterations.js list "Project Name" "Team Name"
```

### List saved queries

```bash
node scripts/queries.js list --project "Project Name"
```

### Fetch work items from saved query id

Explicit:

```bash
node scripts/workitems.js query-id --project "Project Name" --id "QUERY_GUID"
```

Using defaults from `.env`:

```bash
node scripts/workitems.js query-id
```

### List work items closed in the last 7 days

```bash
node scripts/workitems.js closed-last-week
```

### Export default report data as JSON

```bash
node scripts/export-report.js
```

### Build Excel workbook from exported JSON

```bash
python3 scripts/build_excel_report.py \
  --input output/query-data.json \
  --output output/query-report.xlsx
```

This will typically create:

- `output/query-data.json`
- `output/query-report.xlsx`

---

## Natural language commands for ClawBot

Once the skill is installed and configured, you can ask ClawBot in plain English.

### Project and team queries

- `show my Azure DevOps projects`
- `list my Azure DevOps projects`
- `how many teams do we have?`
- `list all team members in <Your Team Name> team`
- `can you list the sprints?`

### Reporting queries

- `generate the Azure DevOps report`
- `please create the azure devops report`
- `regenerate the excel`
- `show current progress of sprint 07`
- `list all work items closed in last week`
- `summarize closed items from last week`

### Workload / progress questions

- `can you please show the count of open items?`
- `which team member has most open items?`
- `please compute the exact top assignee by open items only`
- `show sprint progress`

---

## License

MIT
