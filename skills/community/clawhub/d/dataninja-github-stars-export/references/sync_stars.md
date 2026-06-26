# Sync Stars to Notion DB (`sync_stars_to_notion_db.py`)

## 📖 Overview

The `sync_stars_to_notion_db.py` script bridges the gap between an exported local markdown list of GitHub Starred repositories and your Notion workspace. Given a markdown file structured with tables and category headings, this script interprets the data and programmatically builds a native **Notion Database** populated with your repositories.

Unlike traditional exports that just create a Notion text block or simple subpage layout, this script generates an actionable, sortable, and filterable database using explicit Notion property types (Options, URLs, Numbers, and Text).

## ✨ Key Features

- **Database Property Mapping**: The script parses tabular markdown and assigns it robust data types within Notion:
  - `Repo name` ➔ `title`
  - `Repo handler` ➔ `rich_text`
  - `Full URL to Repo` ➔ `url`
  - `Number of Stars` ➔ `number`
  - `category` ➔ `multi_select`
- **Idempotent Syncing (Smart Overwrites)**: The tool relies on a local `.notion_sync_config.json` state tracker to map the database name to its Notion Database ID. If you rerun the script without changing the target database name, it prevents duplicates by archiving the existing row entries in the database before pushing the fresh updates.
- **CLI Configuration**: Fully powered by Python's `argparse`, letting you dynamically tweak file mappings and execution arguments.

## ⚙️ Prerequisites

1. **Python Packages**: The script requires the `requests` library. Install it using pip:
   ```bash
   pip install requests
   ```
2. **Notion API Key**: 
   The script will securely read your integration token from your environment variables:
   ```bash
   export NOTION_API_KEY="ntn_..."
   ```
   *(Note: A default fallback key is hardcoded within the script if the environment variable is not set).*

---

## 🚀 Usage

### Basic Execution
Run the script using all default properties (Looks for `starred_lists.md` and generates a database named "Starred GitHub Repositories DB"):
```bash
python sync_stars_to_notion_db.py
```

### Specifying a Custom Title (State Identifier)
The database name works as the unique identifier in your caching state:
```bash
python sync_stars_to_notion_db.py --db-name "My Awesome Repo Collection"
```

### Declaring a Different Data Source
Use the `--input` argument to utilize a different local markdown file:
```bash
python sync_stars_to_notion_db.py --input "other_stars.md"
```

### Assigning a Parent Page Destination
Select which Notion page will host the newly generated database by assigning its UUID:
```bash
python sync_stars_to_notion_db.py --parent-id "YOUR_NOTION_PAGE_UUID_HERE"
```

### View Help Menu
```bash
python sync_stars_to_notion_db.py --help
```

---

## 🧠 How It Works Under the Hood

1. **Local State Check**  
   The script starts by looking for `.notion_sync_config.json`. It tries to find a pre-existing Notion Database ID linked to the requested `--db-name`.

2. **Smart Database Management**
   - **If an ID is found (Updating):** The script queries the `/databases/{id}/query` endpoint to fetch all current records, iterates through them, and sets them to `"archived": True`. This guarantees a clean slate to host fresh updates without deleting the actual core database permissions.
   - **If no ID is found (Creation):** The script queries the `/v1/databases` Notion endpoint to set up a brand new table with the associated Data Types (URLs, numbers, options), assigns it to your `parent-id`, and caches the new Database ID to `.notion_sync_config.json`.

3. **Data Parsing (`parse_markdown`)**  
   The script processes your target file line by line:
   - Captures any text following `## ` headers and assigns it as the `category`.
   - Cleans the header strings by stripping commas, as the Notion API restricts commas in `multi_select` options.
   - Parses the Markdown Table syntaxes (`|`) and sanitizes commas out of the Number of Stars count so that they can accurately be injected as Integers.

4. **Data Injection (`insert_row`)**  
   After establishing the schema, the script loops through your parsed categories/tables and inserts them progressively as individual database items. It prints its sync progress to your console every 10 rows.
