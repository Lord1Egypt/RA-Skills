import argparse
import requests
import os
import sys
from dotenv import load_dotenv
import json

def load_config(token_override=None):
    load_dotenv()
    
    base_url = os.getenv("API_URL")
    if not base_url:
        print("Error: API_URL not found in .env file.")
        sys.exit(1)
        
    token = token_override if token_override else os.getenv("JWT_TOKEN")
    
    # Check if the token is about to expire
    if token:
        try:
            import jwt
            from datetime import datetime, timezone
            # Decode without verification just to read the expiration claim
            payload = jwt.decode(token, options={"verify_signature": False})
            exp = payload.get("exp")
            if exp:
                exp_date = datetime.fromtimestamp(exp, tz=timezone.utc)
                now = datetime.now(timezone.utc)
                days_left = (exp_date - now).days
                if 0 <= days_left <= 3:
                    print(f"\\n⚠️  WARNING: Your authentication token will expire in {days_left} day(s)!")
                    print("⚠️  Please run `python3 cli.py renew-token` to automatically generate a new one.\\n")
        except:
            pass
            
    return base_url.rstrip('/'), token

def get_headers(token):
    if not token:
        print("Error: JWT_TOKEN not found in .env and not provided as an argument.")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def cmd_service_account(base_url, token):
    print("Fetching service account information...")
    try:
        response = requests.get(f"{base_url}/service-account", headers=get_headers(token))
        response.raise_for_status()
        data = response.json()
        print(f"\\n✅ Service Account Email: {data.get('service_account_email')}")
        print(f"\\nℹ️  {data.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"\\n❌ Error fetching service account: {e}")
        if e.response is not None:
            print(f"Details: {e.response.text}")

def cmd_add_folder(base_url, token, folder_name):
    print(f"Adding folder '{folder_name}' to tracked RAG indexes...")
    try:
        payload = {"folder_name": folder_name}
        response = requests.post(f"{base_url}/add-folder", headers=get_headers(token), json=payload)
        response.raise_for_status()
        data = response.json()
        print("\\n✅ Success!")
        print(f"Store Name: {data.get('store_name')}")
        print(f"Message: {data.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"\\n❌ Error adding folder: {e}")
        if e.response is not None:
            print(f"Details: {e.response.text}")

def cmd_sync(base_url, token, force=False):
    if force:
        print("⚠️  Initiating FORCED background sync. All your synced files will be completely re-downloaded and re-indexed.")
    else:
        print("Initiating background sync and auto-discovery...")
        
    try:
        payload = {"force": force}
        response = requests.post(f"{base_url}/sync", headers=get_headers(token), json=payload)
        response.raise_for_status()
        data = response.json()
        print("\\n✅ Success!")
        print(f"Message: {data.get('message')}")
        print("Note: Indexing large files may take a few minutes in the background.")
    except requests.exceptions.RequestException as e:
        print(f"\\n❌ Error triggering sync: {e}")
        if e.response is not None:
            print(f"Details: {e.response.text}")

def cmd_search(base_url, token, prompt, folder_names=None):
    print(f"Searching RAG index for: '{prompt}'...")
    if folder_names:
        print(f"Filtering strictly to folders: {folder_names}")
        
    try:
        payload = {"prompt": prompt}
        if folder_names:
            payload["folder_names"] = folder_names
            
        response = requests.post(f"{base_url}/search", headers=get_headers(token), json=payload)
        response.raise_for_status()
        data = response.json()
        
        print("\\n" + "="*50)
        print("🤖 RAG ANSWER:")
        print("="*50)
        print(data.get('answer', 'No answer provided.'))
        
        citations = data.get('citations', [])
        if citations:
            print("\\n" + "="*50)
            print(f"📚 SOURCE DOCUMENTS ({len(citations)} used):")
            print("="*50)
            for i, citation in enumerate(citations, 1):
                if isinstance(citation, dict):
                    title = citation.get('title', 'Unknown')
                    uri = citation.get('uri')
                    if title.endswith('.jpg.txt') or title.endswith('.png.txt'):
                        title = title[:-4]
                    if uri:
                        print(f"[{i}] {title} (URL: {uri})")
                    else:
                        print(f"[{i}] {title}")
                else:
                    print(f"[{i}] {citation[:100]}..." if len(str(citation)) > 100 else f"[{i}] {citation}")
        else:
            print("\\n(No source documents found)")
            
    except requests.exceptions.RequestException as e:
        print(f"\\n❌ Error searching: {e}")
        if e.response is not None:
            print(f"Details: {e.response.text}")

def cmd_status(base_url, token):
    print("Fetching ingestion status for your account...")
    try:
        response = requests.get(f"{base_url}/status", headers=get_headers(token))
        response.raise_for_status()
        data = response.json()
        
        folders = data.get("folders", [])
        if not folders:
            print("\nℹ️ No folders are currently being tracked for your account.")
            return
            
        print(f"\n✅ Sync Status for: {data.get('user')}")
        print(f"Total Folders Tracked: {data.get('total_folders', 0)}")
        print(f"Total Files Successfully Indexed: {data.get('total_files_indexed', 0)}")
        print("\n" + "="*50)
        
        for idx, f in enumerate(folders, 1):
            print(f"[{idx}] Folder: {f.get('folder_name')} (ID: {f.get('folder_id')})")
            print(f"    Target Gemini Store: {f.get('store_name')}")
            print(f"    Total Indexed Files: {f.get('total_files_indexed', 0)}")
            sync_time = f.get('last_sync_time')
            print(f"    Last Sync Time: {sync_time if sync_time else 'Pending / In Progress...'}")
            print("-" * 50)
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching status: {e}")
        if e.response is not None:
            print(f"Details: {e.response.text}")

def cmd_list_files(base_url, token):
    print("Fetching tracked files from database...")
    try:
        response = requests.get(f"{base_url}/list-files", headers=get_headers(token))
        response.raise_for_status()
        data = response.json()
        
        files = data.get("files", [])
        if not files:
            print("\nℹ️ No files are currently indexed for your account.")
            return
            
        print(f"\n✅ Tracked Files for: {data.get('user')}")
        print(f"Total Files Indexed: {data.get('total_files', 0)}")
        print("\n" + "="*50)
        
        for idx, f in enumerate(files, 1):
            doc_name = f.get('gemini_document_name', 'Unknown')
            # Extract the human-readable part of the document name if possible
            # Usually it's in the format: fileSearchStores/xyz/documents/filename-hash
            clean_name = doc_name.split('/')[-1] if '/' in doc_name else doc_name
            # If the filename ends with a hash and a hyphen, we can't perfectly reconstruct the original extension
            # But the web_view_link often has hints. For debug purposes, we print the raw ID and link.
            link = f.get('web_view_link', 'No Google Drive Link Stored')
            print(f"[{idx}] {clean_name}")
            print(f"    Drive ID: {f.get('file_id')}")
            print(f"    Link: {link}")
            print("-" * 50)
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching file list: {e}")
        if e.response is not None:
            print(f"Details: {e.response.text}")

def cmd_renew_token(base_url, token, days):
    print("Requesting a new token from the server...")
    try:
        payload = {"expires_in_days": int(days)}
        response = requests.post(f"{base_url}/renew-token", headers=get_headers(token), json=payload)
        response.raise_for_status()
        data = response.json()
        print("\n✅ Success! New token generated.")
        print(f"User: {data.get('email')}")
        print(f"Expires at: {data.get('expires_at')}")
        print("\nNEW_TOKEN:")
        print(data.get('token'))
        print("\nPlease update your .env file with this new token.")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error renewing token: {e}")
        if e.response is not None:
            print(f"Details: {e.response.text}")

def main():
    parser = argparse.ArgumentParser(description="Google Drive RAG CLI")
    parser.add_argument("-t", "--token", help="Override JWT token from .env")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    
    # service-account
    subparsers.add_parser("service-account", help="Get the service account email to share folders with")
    
    # add-folder
    add_parser = subparsers.add_parser("add-folder", help="Manually track a new Google Drive folder")
    add_parser.add_argument("folder_name", help="The exact name of the folder shared in Google Drive")
    
    # sync
    sync_parser = subparsers.add_parser("sync", help="Trigger auto-discovery and background sync of all tracked folders")
    sync_parser.add_argument("--force", action="store_true", help="Force a complete re-download and re-index of all tracked files")
    
    # status
    subparsers.add_parser("status", help="Check the indexing status of your folders and files")
    
    # list-files
    subparsers.add_parser("list-files", help="List the actual Google Drive files currently tracked in the RAG database")
    
    # renew-token
    renew_parser = subparsers.add_parser("renew-token", help="Generate a new JWT token before your current one expires")
    renew_parser.add_argument("-d", "--days", default=30, help="Number of days until the new token expires (default: 30)")
    
    # search
    search_parser = subparsers.add_parser("search", help="Search your indexed RAG documents")
    search_parser.add_argument("prompt", help="The question or search prompt")
    search_parser.add_argument("-f", "--folders", nargs="+", help="Optional list of specific folder names to restrict the search to")
    
    args = parser.parse_args()
    
    base_url, token = load_config(args.token)
    
    if args.command == "service-account":
        cmd_service_account(base_url, token)
    elif args.command == "add-folder":
        cmd_add_folder(base_url, token, args.folder_name)
    elif args.command == "status":
        cmd_status(base_url, token)
    elif args.command == "list-files":
        cmd_list_files(base_url, token)
    elif args.command == "renew-token":
        cmd_renew_token(base_url, token, args.days)
    elif args.command == "sync":
        cmd_sync(base_url, token, args.force)
    elif args.command == "search":
        cmd_search(base_url, token, args.prompt, args.folders)

if __name__ == "__main__":
    main()
