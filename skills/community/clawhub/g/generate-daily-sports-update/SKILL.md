---
name: generate-daily-sports-update
description: Runs the sports science crawler to generate a daily report, sync to Notion, and prevent duplicate content.
metadata:
  openclaw.homepage: https://github.com/w2478328197-arch/sports-science-daily
  user-invocable: true
requires.bins:
  - python3
requires.env:
  - NOTION_TOKEN
  - NOTION_PAGE_ID
---

# Generate Daily Sports Update

This skill runs the `daily_sports_update.py` script to fetch the latest sports science research and wearable tech news. It automatically handles deduplication, so you can run it frequently without worrying about seeing the same content twice.

## Prerequisites

- **Python 3**: Requires `python3` to be installed.
- **Dependencies**: The required Python packages defined in `requirements.txt` must be installed (`pip3 install -r requirements.txt`).
- **Environment Variables**:
  - `NOTION_TOKEN`: The integration token for Notion API.
  - `NOTION_PAGE_ID`: The ID of the Notion page to sync the daily update to.
- **Tools Needed**: You must have access to the `run_command` tool to execute the script in a bash terminal.

## Instructions

1.  **Locate the Script**:
    The script `daily_sports_update.py` is located in the user's sports-science-daily directory. You should first ensure you are in the correct working directory.

2.  **Run the update**:
    Use the `run_command` tool to execute the python script.

    ```bash
    python3 daily_sports_update.py --days 2
    ```

    -   `--days N`: (Optional) Number of days to look back (default is 7). If you haven't run it in a while, increase this (e.g., `--days 7` or `--days 30`).
    -   `--no-history`: (Optional) Use this ONLY if you want to force re-fetching of already seen items (e.g., for debugging).

3.  **Output & Sync**:
    -   The script will generate a local Markdown file named: `YYYY-MM-DD_运动科学日报.md`
    -   It will automatically sync the compiled blocks directly to the specified Notion page using the Notion APIs.
    -   It updates `processed_history.json` locally to mark fetched URLs/PMIDs as seen.

4.  **Handling "No New Content"**:
    -   If the script's terminal output contains "🎉 没有发现新内容" (No new content found), it means all found items in the lookback period have already been processed and synced previously. You can try running with a larger `--days` argument.

## Security & Privacy Note

- **External Endpoints Called**:
  - `https://eutils.ncbi.nlm.nih.gov`: Accessed to fetch PubMed paper statistics and abstracts.
  - `https://api.notion.com`: Accessed to create and populate the daily reports.
  - Various RSS feed URLs (e.g., Garmin, MySportScience, YouTube RSS).
- **Files Checked**: Opens and updates `processed_history.json` and creates `.md` reporting files locally in the working directory.
- This skill invokes web requests to fetch relevant sports science data but does not expose any user PII.
