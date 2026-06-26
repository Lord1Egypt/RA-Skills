# GitHub Stars Notion Sync Agent Skill

A specialized agent skill designed to automate the backup and synchronization of your GitHub starred repositories into a structured Notion database. This skill organizes your stars by GitHub's custom lists (categories), making it easier to manage and search your collection.

## 📁 Repository Structure

```text
github-stars-notion-sync/
├── SKILL.md             # (Required) Skill definition for Gemini CLI
├── agent.yaml           # Agent metadata and tool mapping
├── README.md            # Main documentation
├── requirements.txt     # Python dependencies
├── scripts/             # Implementation logic
│   ├── export_stars.sh
│   └── sync_stars_to_notion_db.py
├── references/          # Supplemental documentation
│   ├── export_stars.md
│   └── sync_stars.md
└── assets/              # Data and local state
    ├── starred_lists.md
    └── .notion_sync_config.json
```

## 🚀 Getting Started

### Prerequisites

1.  **GitHub CLI (`gh`)**: Must be installed and authenticated.
2.  **jq**: Required for JSON processing in the shell script.
3.  **Notion API Key**: Obtain a token from [Notion Developers](https://developers.notion.com/) and set it as an environment variable:
    ```bash
    export NOTION_API_KEY="ntn_..."
    ```

### Installation

Install Python dependencies:
```bash
pip install -r requirements.txt
```

## 🛠️ Usage

This skill exposes two primary tools:

### 1. `export_stars`
Fetches all your starred repositories and organizes them by GitHub List.
- **Run manually**: `bash scripts/export_stars.sh`
- **Output**: `./assets/starred_lists.md`

### 2. `sync_to_notion`
Parses the local Markdown file and populates/updates a Notion database.
- **Run manually**: `python3 scripts/sync_stars_to_notion_db.py`
- **State**: Tracks the Notion database ID in `./assets/.notion_sync_config.json`.

## 📚 Documentation
Detailed information for each script can be found in the `references/` directory.
- [Exporting Stars](./references/export_stars.md)
- [Syncing to Notion](./references/sync_stars.md)
