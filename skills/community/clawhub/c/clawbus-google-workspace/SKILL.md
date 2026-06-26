---
name: Google Workspace
description: >
  Manage Google Calendar, Google Drive, and Google Sheets through
  MyBrandMetrics-connected Google data sources and the local Google Workspace
  CLI. Use it to list, create, update, and delete Calendar events; read,
  append, update, and batch update Google Sheets; and search, create, move,
  copy, share, upload, export, and delete Google Drive files and folders. No
  Google Cloud project setup and no MCP server are required: sign in to
  MyBrandMetrics with Google, connect the needed Google data sources, get a
  MyBrandMetrics API key, and start using the skill.
---

# Google Workspace

Manage Google Calendar, Google Drive, and Google Sheets through
MyBrandMetrics-connected Google data sources.

This skill uses a local `gws` CLI wrapper, but the Google OAuth setup is handled
by MyBrandMetrics. That means no Google Cloud project setup, no OAuth client
configuration, and no MCP server are required. Sign in to MyBrandMetrics with
Google, connect the Google data sources you need, get a MyBrandMetrics API key,
and use natural-language requests or direct commands.

Website: [https://www.clawbus.com/](https://www.clawbus.com/)  
MyBrandMetrics API: [https://mybrandmetrics.com/](https://mybrandmetrics.com/)

## Why This Google Workspace Skill

| This skill | Typical MCP setup |
| --- | --- |
| Sign in to MyBrandMetrics with Google. | Create or configure a Google Cloud project. |
| Connect Google Calendar, Google Drive, and Google Sheets as data sources. | Configure OAuth clients, scopes, and local MCP server auth. |
| Use a MyBrandMetrics API key to fetch managed access tokens. | Manage credentials and token storage yourself. |
| Run with a local wrapper around `gws`; no MCP server required. | Requires running and maintaining an MCP server. |

Use this when you want Google Workspace actions without setting up your own
Google project or MCP server.

## Core Capabilities

| Capability | Details |
| --- | --- |
| Google Calendar | List, create, update, patch, and delete calendar events. |
| Google Sheets | Read values, update ranges, append rows, and run spreadsheet batch updates. |
| Google Drive search | List and search Drive files and folders. |
| Google Drive file management | Create folders, move files, copy files, trash/delete files, and manage sharing permissions. |
| Google Drive upload/export | Upload local files to Drive and export Google Docs files to formats such as PDF. |
| Managed Google auth | Fetch service-specific Google access tokens through MyBrandMetrics using `google_calendar`, `google_sheets`, or `google_drive`. |

## Setup Flow

1. Open [https://mybrandmetrics.com/](https://mybrandmetrics.com/) and sign in
   with Google.
2. In MyBrandMetrics, open **Data sources**.
3. Connect the Google data sources you need:
   - Google Calendar for calendar workflows;
   - Google Drive for file and folder workflows;
   - Google Sheets for spreadsheet workflows.
4. Wait until each selected connection is ready.
5. In [https://mybrandmetrics.com/](https://mybrandmetrics.com/), get the
   MyBrandMetrics API key.
6. Install the `google-workspace` skill.
7. Save the MyBrandMetrics API key for the wrapper:

   ```bash
   echo "YOUR_API_KEY" > ~/.google_workspace_api_key
   ```

   You can also set `GWS_SKILL_API_KEY` instead.

8. If `gws` is not installed, run:

   ```bash
   bash scripts/install_gws.sh
   ```

9. Start Google Calendar, Google Drive, or Google Sheets workflows with
   natural-language instructions.

## Workflow

Use natural-language prompts after the skill is installed. Include:

- which Google service to use: Calendar, Drive, or Sheets;
- the target calendar, spreadsheet, file, or folder;
- the action to perform;
- any date range, sheet range, search query, folder ID, file ID, or sharing
  email needed for the task.

Examples:

```text
List my next 10 Google Calendar events.
```

```text
Append this row to Sheet1 in my campaign spreadsheet.
```

```text
Find Google Drive files with "budget" in the name and share the selected file with editor access.
```

## Use The Wrapper Directly

Use `scripts/gws_wrapper.py`.

General pattern:

```bash
python3 scripts/gws_wrapper.py <service> <resource> <method> [args]
```

The wrapper maps services to MyBrandMetrics source keys:

| Service | MyBrandMetrics source key |
| --- | --- |
| `calendar` | `google_calendar` |
| `sheets` | `google_sheets` |
| `drive` | `google_drive` |

### Google Calendar

List events:

```bash
python3 scripts/gws_wrapper.py calendar events list \
  --params '{"calendarId": "primary", "maxResults": 10}'
```

Create an event:

```bash
python3 scripts/gws_wrapper.py calendar events insert \
  --params '{"calendarId": "primary"}' \
  --json '{"summary": "Planning meeting", "start": {"dateTime": "2026-05-21T10:00:00+08:00"}, "end": {"dateTime": "2026-05-21T10:30:00+08:00"}}'
```

### Google Sheets

Read values:

```bash
python3 scripts/gws_wrapper.py sheets spreadsheets values get \
  --params '{"spreadsheetId": "SPREADSHEET_ID", "range": "Sheet1!A1:D10"}'
```

Append values:

```bash
python3 scripts/gws_wrapper.py sheets spreadsheets values append \
  --params '{"spreadsheetId": "SPREADSHEET_ID", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["New row", "More data"]]}'
```

### Google Drive

Search files:

```bash
python3 scripts/gws_wrapper.py drive files list \
  --params '{"pageSize": 10, "q": "name contains '\''budget'\'' and trashed = false"}'
```

Upload a file:

```bash
python3 scripts/gws_wrapper.py drive +upload /local/path/file.pdf \
  --parent "FOLDER_ID" \
  --name "file.pdf"
```

Export a Google Docs file:

```bash
python3 scripts/gws_wrapper.py drive files export \
  --params '{"fileId": "FILE_ID", "mimeType": "application/pdf"}' \
  --output document.pdf
```

## Notes

- Connect only the Google data sources needed for the workflow.
- Keep the MyBrandMetrics API key private.
- If a token error occurs, confirm that the relevant data source is connected
  and that the API key is valid.
- If `gws` is missing, run `scripts/install_gws.sh`.
