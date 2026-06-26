import argparse
import json
import os
import sys

try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    print("The 'requests' library is required. Install it using: pip install requests")
    sys.exit(1)

# Default Notion API Token
NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
NOTION_VERSION = "2022-06-28"
CONFIG_FILE = "assets/.notion_sync_config.json"
DEFAULT_PARENT_PAGE_ID = "f94aa417-3269-4fa6-a869-dc5b22eb1cca"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def parse_markdown(filepath):
    """Parses markdown and returns a list of dictionaries representing the rows."""
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        sys.exit(1)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    rows = []
    current_category = "Uncategorized"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("## "):
            # Multi-select options in Notion cannot contain commas
            current_category = line[3:].strip().replace(",", "")[:100] 
        elif line.startswith("|") and not line.startswith("|---"):
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            # Ignore the header row
            if len(cells) == 4 and cells[0].lower() != "repo name":
                try:
                    stars = int(cells[3].replace(",", ""))
                except ValueError:
                    stars = 0
                
                rows.append({
                    "repo_name": cells[0],
                    "repo_handler": cells[1],
                    "url": cells[2],
                    "stars": stars,
                    "category": current_category
                })
                
    return rows

def create_database(db_name, parent_id):
    """Creates a new Notion database and returns its ID."""
    url = "https://api.notion.com/v1/databases"
    payload = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": [
            {"type": "text", "text": {"content": db_name}}
        ],
        "properties": {
            "Repo name": {"title": {}},
            "Repo handler": {"rich_text": {}},
            "Full URL to Repo": {"url": {}},
            "Number of Stars": {"number": {"format": "number"}},
            "category": {"multi_select": {}}
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload, verify=False)
    if response.status_code != 200:
        print(f"Error creating database: {response.text}")
        sys.exit(1)
    return response.json()["id"]

def clear_database(db_id):
    """Archives all existing pages in the database so it can be 'overwritten'."""
    print(f"Clearing existing entries in database {db_id}...")
    query_url = f"https://api.notion.com/v1/databases/{db_id}/query"
    
    has_more = True
    next_cursor = None
    count = 0
    
    while has_more:
        payload = {}
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        response = requests.post(query_url, headers=HEADERS, json=payload, verify=False)
        if response.status_code != 200:
            print(f"Error querying database for clearing: {response.text}")
            break
            
        data = response.json()
        pages = data.get("results", [])
        
        for page in pages:
            page_id = page["id"]
            patch_url = f"https://api.notion.com/v1/pages/{page_id}"
            requests.patch(patch_url, headers=HEADERS, json={"archived": True}, verify=False)
            count += 1
            
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")
        
    print(f"Cleared {count} existing entries.")

def insert_row(db_id, row):
    """Inserts a single row into the Notion database."""
    url = "https://api.notion.com/v1/pages"
    
    payload = {
        "parent": {"type": "database_id", "database_id": db_id},
        "properties": {
            "Repo name": {
                "title": [{"type": "text", "text": {"content": row["repo_name"]}}]
            },
            "Repo handler": {
                "rich_text": [{"type": "text", "text": {"content": row["repo_handler"]}}]
            },
            "Number of Stars": {
                "number": row["stars"]
            },
            "category": {
                "multi_select": [{"name": row["category"]}]
            }
        }
    }
    
    # Only assign URL if it looks like a valid URL start to avoid Notion API schema errors
    url_val = row["url"]
    if url_val.startswith("http"):
        payload["properties"]["Full URL to Repo"] = {"url": url_val}
        
    response = requests.post(url, headers=HEADERS, json=payload, verify=False)
    if response.status_code != 200:
        print(f"Error inserting row for {row['repo_name']}: {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Sync GitHub stars markdown to a Notion Database.")
    parser.add_argument("--input", default="assets/starred_lists.md", help="Path to the input markdown file.")
    parser.add_argument("--db-name", default="Starred GitHub Repositories DB", help="Name of the Notion Database.")
    parser.add_argument("--parent-id", default=DEFAULT_PARENT_PAGE_ID, help="ID of the parent Notion page.")
    args = parser.parse_args()
    
    # Check config for existing database ID mapping
    config = load_config()
    db_id = config.get(args.db_name)
    
    if db_id:
        print(f"Found existing database ID in config for '{args.db_name}': {db_id}")
        clear_database(db_id)
    else:
        print(f"Creating new database '{args.db_name}'...")
        db_id = create_database(args.db_name, args.parent_id)
        config[args.db_name] = db_id
        save_config(config)
        print(f"Database created with ID: {db_id}")
        
    print(f"Parsing {args.input}...")
    rows = parse_markdown(args.input)
    
    if not rows:
        print("No content found to sync.")
        sys.exit(0)
        
    print(f"Inserting {len(rows)} rows into the Notion Database...")
    for i, row in enumerate(rows, 1):
        insert_row(db_id, row)
        if i % 10 == 0:
            print(f"Inserted {i}/{len(rows)} rows...")
            
    print("Sync complete!")

if __name__ == "__main__":
    main()
