import os
import sys
import json
import argparse
import requests
import urllib.parse

# Configuration paths
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.expanduser('~/.openclaw/workspace/bwp_config.json')

# Baidu API Endpoints
OAUTH_AUTHORIZE_URL = "https://openapi.baidu.com/oauth/2.0/authorize"
OAUTH_TOKEN_URL = "https://openapi.baidu.com/oauth/2.0/token"
API_BASE_URL = "https://pan.baidu.com/rest/2.0/xpan"
API_QUOTA_URL = "https://pan.baidu.com/api/quota"
PCS_BASE_URL = "https://d.pcs.baidu.com/rest/2.0/pcs"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def auth_url(app_key):
    params = {
        'response_type': 'code',
        'client_id': app_key,
        'redirect_uri': 'oob',
        'scope': 'basic,netdisk'
    }
    url = f"{OAUTH_AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"
    print(f"Please open the following URL in your browser to authorize:")
    print(f"\n{url}\n")
    print(f"After authorization, copy the 'Authorization Code' and run:")
    print(f"python bwp.py auth --code YOUR_CODE")
    
    config = load_config()
    config['app_key'] = app_key
    save_config(config)

def get_token(code, app_key=None, secret_key=None):
    config = load_config()
    app_key = app_key or config.get('app_key')
    secret_key = secret_key or config.get('secret_key')
    
    if not app_key or not secret_key:
        print("Error: AppKey and SecretKey are required.")
        sys.exit(1)
        
    params = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': app_key,
        'client_secret': secret_key,
        'redirect_uri': 'oob'
    }
    
    response = requests.get(OAUTH_TOKEN_URL, params=params)
    data = response.json()
    
    if 'access_token' in data:
        config.update({
            'app_key': app_key,
            'secret_key': secret_key,
            'access_token': data['access_token'],
            'refresh_token': data['refresh_token'],
            'expires_in': data['expires_in']
        })
        save_config(config)
        print("Successfully authenticated and saved tokens!")
    else:
        print(f"Failed to authenticate: {data}")

def refresh_access_token(config):
    refresh_token = config.get('refresh_token')
    app_key = config.get('app_key')
    secret_key = config.get('secret_key')
    if not all([refresh_token, app_key, secret_key]):
        return None
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': app_key,
        'client_secret': secret_key,
    }
    try:
        response = requests.get(OAUTH_TOKEN_URL, params=params)
        data = response.json()
        if 'access_token' in data:
            config['access_token'] = data['access_token']
            config['refresh_token'] = data.get('refresh_token', refresh_token)
            config['expires_in'] = data.get('expires_in')
            save_config(config)
            return data['access_token']
    except Exception:
        pass
    return None

def check_token():
    config = load_config()
    if 'access_token' not in config:
        print("Error: Not authenticated. Please run 'auth' command first.")
        sys.exit(1)
    token = config['access_token']
    # Quick validation: try a lightweight call; if 111 (token expired), refresh
    try:
        r = requests.get(API_QUOTA_URL, params={'access_token': token, 'checkfree': 1}, timeout=10)
        if r.json().get('errno') == 111:
            new_token = refresh_access_token(config)
            if new_token:
                print("Access token refreshed automatically.")
                return new_token
            print("Error: Token expired and refresh failed. Please re-authenticate.")
            sys.exit(1)
    except Exception:
        pass
    return token

def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_idx = 0
    while size_bytes >= 1024 and unit_idx < len(units) - 1:
        size_bytes /= 1024.0
        unit_idx += 1
    return f"{size_bytes:.2f}{units[unit_idx]}"

def get_quota():
    token = check_token()
    params = {'access_token': token, 'checkfree': 1, 'checkexpire': 1}
    response = requests.get(API_QUOTA_URL, params=params)
    data = response.json()
    
    if 'errno' in data and data['errno'] != 0:
        print(f"Error getting quota: {data}")
        return
        
    total = data.get('total', 0)
    used = data.get('used', 0)
    print(f"Quota: {format_size(used)} used / {format_size(total)} total")

def list_files(dir_path):
    token = check_token()
    params = {
        'method': 'list',
        'access_token': token,
        'dir': dir_path,
        'order': 'time',
        'desc': 1
    }
    response = requests.get(f"{API_BASE_URL}/file", params=params)
    data = response.json()
    
    if 'errno' in data and data['errno'] != 0:
        print(f"Error listing files: {data}")
        return
        
    files = data.get('list', [])
    print(f"Files in {dir_path}:")
    print(f"{'TYPE':<6} | {'SIZE':<10} | {'FS_ID':<16} | {'NAME'}")
    print("-" * 70)
    for f in files:
        ftype = "DIR" if f['isdir'] == 1 else "FILE"
        size = format_size(f['size']) if f['isdir'] == 0 else "-"
        print(f"{ftype:<6} | {size:<10} | {f['fs_id']:<16} | {f['server_filename']}")

def search_files(keyword, dir_path="/"):
    token = check_token()
    params = {
        'method': 'search',
        'access_token': token,
        'key': keyword,
        'dir': dir_path
    }
    response = requests.get(f"{API_BASE_URL}/file", params=params)
    data = response.json()
    
    if 'errno' in data and data['errno'] != 0:
        print(f"Error searching files: {data}")
        return
        
    files = data.get('list', [])
    print(f"Search results for '{keyword}' in {dir_path}:")
    print(f"{'TYPE':<6} | {'SIZE':<10} | {'FS_ID':<16} | {'PATH'}")
    print("-" * 70)
    for f in files:
        ftype = "DIR" if f.get('isdir') == 1 else "FILE"
        size = format_size(f.get('size', 0)) if f.get('isdir') == 0 else "-"
        print(f"{ftype:<6} | {size:<10} | {f.get('fs_id', ''):<16} | {f.get('path', '')}")

def get_dlink(fs_id):
    token = check_token()
    params = {
        'method': 'filemetas',
        'access_token': token,
        'fsids': f"[{fs_id}]",
        'dlink': 1
    }
    response = requests.get(f"{API_BASE_URL}/multimedia", params=params)
    data = response.json()
    
    if data.get('errno') != 0:
        print(f"Error getting download link: {data}")
        return
        
    file_list = data.get('list', [])
    if not file_list:
        print(f"File with fs_id {fs_id} not found.")
        return
        
    f = file_list[0]
    if f.get('isdir') == 1:
        print(f"Cannot download directory directly: {f['path']}")
        return
        
    dlink = f.get('dlink')
    if dlink:
        # According to Baidu API, you must append access_token to the dlink to download it
        download_url = f"{dlink}&access_token={token}"
        print(f"File: {f['filename']}")
        print(f"Size: {format_size(f['size'])}")
        print(f"Download URL (User-Agent requires 'pan.baidu.com'):")
        print(download_url)
        print("\nCurl example:")
        print(f"curl -L -A 'pan.baidu.com' '{download_url}' -o '{f['filename']}'")
    else:
        print(f"Download link not available for this file: {f}")

def mkdir(path):
    token = check_token()
    url = f"{API_BASE_URL}/file?method=create&access_token={token}"
    data = {
        'path': path,
        'size': 0,
        'isdir': 1,
        'block_list': '[]',
        'autoinit': 1,
        'rtype': 1 # Rename if exists
    }
    response = requests.post(url, data=data)
    res_data = response.json()
    if res_data.get('errno') == 0:
        print(f"Successfully created directory: {res_data.get('path')}")
    else:
        print(f"Failed to create directory: {res_data}")

def delete_path(path):
    token = check_token()
    url = f"{API_BASE_URL}/file?method=filemanager&access_token={token}&opera=delete"
    data = {
        'async': 2, # Sync operation
        'filelist': json.dumps([path])
    }
    response = requests.post(url, data=data)
    res_data = response.json()
    if res_data.get('errno') == 0:
        print(f"Successfully deleted: {path}")
    else:
        print(f"Failed to delete: {res_data}")

def rename_path(path, new_name):
    token = check_token()
    url = f"{API_BASE_URL}/file?method=filemanager&access_token={token}&opera=rename"
    file_info = {"path": path, "newname": new_name}
    data = {
        'async': 2, # Sync operation
        'filelist': json.dumps([file_info])
    }
    response = requests.post(url, data=data)
    res_data = response.json()
    if res_data.get('errno') == 0:
        print(f"Successfully renamed {path} to {new_name}")
    else:
        print(f"Failed to rename: {res_data}")

def move_path(path, dest_dir):
    token = check_token()
    url = f"{API_BASE_URL}/file?method=filemanager&access_token={token}&opera=move"
    file_info = {"path": path, "dest": dest_dir, "newname": os.path.basename(path)}
    data = {
        'async': 2, # Sync operation
        'filelist': json.dumps([file_info])
    }
    response = requests.post(url, data=data)
    res_data = response.json()
    if res_data.get('errno') == 0:
        print(f"Successfully moved {path} to {dest_dir}")
    else:
        print(f"Failed to move: {res_data}")

CHUNK_SIZE = 4 * 1024 * 1024  # 4MB per Baidu API spec

def _collect_files(local_path, remote_dir):
    """Recursively collect (local_file_path, remote_dir) pairs."""
    pairs = []
    if os.path.isfile(local_path):
        pairs.append((local_path, remote_dir))
    elif os.path.isdir(local_path):
        for entry in os.listdir(local_path):
            full = os.path.join(local_path, entry)
            if os.path.isfile(full):
                pairs.append((full, remote_dir))
            elif os.path.isdir(full):
                sub_remote = f"{remote_dir.rstrip('/')}/{entry}"
                pairs.extend(_collect_files(full, sub_remote))
    return pairs

def upload_file(local_path, remote_dir):
    import concurrent.futures

    pairs = _collect_files(local_path, remote_dir)
    if not pairs:
        print(f"No files found at {local_path}")
        return

    if len(pairs) == 1:
        _do_upload(*pairs[0])
        return

    print(f"Found {len(pairs)} files (recursive). Starting batch upload...")
    failed = []

    def _upload_single(pair):
        try:
            _do_upload(*pair)
        except Exception as e:
            failed.append((pair[0], str(e)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        list(executor.map(_upload_single, pairs))

    if failed:
        print(f"\n{len(failed)} file(s) failed:")
        for path, err in failed:
            print(f"  {path}: {err}")
    else:
        print(f"\nAll {len(pairs)} files uploaded successfully.")

def _do_upload(local_path, remote_dir):
    import hashlib

    if not os.path.exists(local_path):
        print(f"Error: Local file {local_path} does not exist.")
        return

    token = check_token()
    file_name = os.path.basename(local_path)
    remote_path = f"{remote_dir.rstrip('/')}/{file_name}"
    file_size = os.path.getsize(local_path)

    print(f"Uploading {file_name} ({format_size(file_size)}) -> {remote_path}")

    # Calculate per-block MD5 list
    block_list = []
    with open(local_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            block_list.append(hashlib.md5(chunk).hexdigest())

    if not block_list:
        block_list = [hashlib.md5(b'').hexdigest()]

    # Step 1: Precreate
    precreate_url = f"{API_BASE_URL}/file?method=precreate&access_token={token}"
    pre_data = {
        'path': remote_path,
        'size': file_size,
        'isdir': 0,
        'autoinit': 1,
        'rtype': 1,
        'block_list': json.dumps(block_list)
    }
    pre_res = requests.post(precreate_url, data=pre_data).json()
    if pre_res.get('errno') != 0:
        print(f"  Precreate failed: {pre_res}")
        return

    upload_id = pre_res.get('uploadid')
    if not upload_id:
        print(f"  Rapid upload / already exists: {pre_res.get('path', remote_path)}")
        return

    need_blocks = pre_res.get('block_list', list(range(len(block_list))))

    # Step 2: Upload each needed chunk
    with open(local_path, 'rb') as f:
        for seq in need_blocks:
            f.seek(seq * CHUNK_SIZE)
            chunk = f.read(CHUNK_SIZE)
            upload_url = (
                f"{PCS_BASE_URL}/superfile2?method=upload&access_token={token}"
                f"&type=tmpfile&path={urllib.parse.quote(remote_path)}"
                f"&uploadid={upload_id}&partseq={seq}"
            )
            up_res = requests.post(upload_url, files={'file': (file_name, chunk)}).json()
            if 'md5' not in up_res:
                print(f"  Chunk {seq} upload failed: {up_res}")
                return
            print(f"  Chunk {seq+1}/{len(block_list)} done")

    # Step 3: Commit
    create_url = f"{API_BASE_URL}/file?method=create&access_token={token}"
    create_data = {
        'path': remote_path,
        'size': file_size,
        'isdir': 0,
        'block_list': json.dumps(block_list),
        'uploadid': upload_id,
        'rtype': 1
    }
    final_res = requests.post(create_url, data=create_data).json()
    if final_res.get('errno') == 0:
        print(f"  OK: {final_res.get('path')}")
    else:
        print(f"  Commit failed: {final_res}")


def main():
    parser = argparse.ArgumentParser(description="Baidu Wangpan CLI Tool for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Auth command
    auth_parser = subparsers.add_parser("auth", help="Authenticate with Baidu")
    auth_parser.add_argument("--app-key", help="Baidu App Key (Client ID)")
    auth_parser.add_argument("--secret-key", help="Baidu Secret Key (Client Secret)")
    auth_parser.add_argument("--code", help="Authorization Code obtained from browser")
    
    # Quota command
    subparsers.add_parser("quota", help="Check storage quota")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List files in a directory")
    list_parser.add_argument("--dir", default="/", help="Directory path (default: /)")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for files")
    search_parser.add_argument("keyword", help="Keyword to search for")
    search_parser.add_argument("--dir", default="/", help="Directory to search in (default: /)")
    
    # Download link command
    download_parser = subparsers.add_parser("download", help="Get true download link for a file")
    download_parser.add_argument("fs_id", help="The fs_id of the file to download")
    
    # Mkdir command
    mkdir_parser = subparsers.add_parser("mkdir", help="Create a directory")
    mkdir_parser.add_argument("path", help="Full path of the new directory (e.g., /apps/myfolder)")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a file or directory")
    delete_parser.add_argument("path", help="Full path to delete")
    
    # Rename command
    rename_parser = subparsers.add_parser("rename", help="Rename a file or directory")
    rename_parser.add_argument("path", help="Full path of the file/dir to rename")
    rename_parser.add_argument("newname", help="New name (just the name, not full path)")
    
    # Move command
    move_parser = subparsers.add_parser("move", help="Move a file or directory")
    move_parser.add_argument("path", help="Full path of the file/dir to move")
    move_parser.add_argument("dest", help="Destination directory path")
    
    # Upload command 
    upload_parser = subparsers.add_parser("upload", help="Upload a local file")
    upload_parser.add_argument("local", help="Local file path")
    upload_parser.add_argument("remote", help="Remote destination directory path (e.g. /apps/)")
    
    args = parser.parse_args()
    
    if args.command == "auth":
        if args.code:
            get_token(args.code, args.app_key, args.secret_key)
        elif args.app_key:
            auth_url(args.app_key)
            if args.secret_key:
                config = load_config()
                config['secret_key'] = args.secret_key
                save_config(config)
        else:
            print("Please provide --app-key to generate auth URL, or --code to verify.")
    elif args.command == "quota":
        get_quota()
    elif args.command == "list":
        list_files(args.dir)
    elif args.command == "search":
        search_files(args.keyword, args.dir)
    elif args.command == "download":
        get_dlink(args.fs_id)
    elif args.command == "mkdir":
        mkdir(args.path)
    elif args.command == "delete":
        delete_path(args.path)
    elif args.command == "rename":
        rename_path(args.path, args.newname)
    elif args.command == "move":
        move_path(args.path, args.dest)
    elif args.command == "upload":
        upload_file(args.local, args.remote)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
