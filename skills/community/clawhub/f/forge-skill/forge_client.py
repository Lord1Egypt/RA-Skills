#!/usr/bin/env python3
"""forge_client.py — Forge AI API CLI client

Usage:
  forge_client.py login <email> <password>
  forge_client.py me
  forge_client.py logout
  forge_client.py article list [--name <keyword>]
  forge_client.py article create <file.json>
  forge_client.py article update <file.json>
  forge_client.py evaluation list [--name <keyword>]
  forge_client.py evaluation create <file.json>
  forge_client.py evaluation update <file.json>
  forge_client.py tag list
  forge_client.py tag create <name> [--color <hex>]
  forge_client.py upload <file> [--storage-path <path>]
"""

import base64
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = 'https://cloud1-2gavd8kj8a1ce021.service.tcloudbase.com/api/forge'
ENDPOINTS = {
    'auth': 'auth',
    'articleCrud': 'article-crud',
    'evaluationCrud': 'evaluation-crud',
    'tagsCrud': 'tag-crud',
    'fileUpload': 'file-upload',
}

FORGEAI_DIR = os.path.join(os.getcwd(), '.forgeai')
SESSION_FILE = os.path.join(FORGEAI_DIR, 'session.json')
TAGS_FILE = os.path.join(FORGEAI_DIR, 'tags.json')


def ensure_forgeai_dir():
    os.makedirs(FORGEAI_DIR, exist_ok=True)
    os.makedirs(os.path.join(FORGEAI_DIR, 'articles'), exist_ok=True)
    os.makedirs(os.path.join(FORGEAI_DIR, 'evaluations'), exist_ok=True)


def api_request(endpoint, action, data=None, require_auth=True):
    if data is None:
        data = {}
    url = f'{API_BASE}/{ENDPOINTS[endpoint]}'
    headers = {'Content-Type': 'application/json'}

    if require_auth:
        token = load_token()
        if not token:
            die('Not logged in. Use `login` first.')
        headers['Authorization'] = f'Bearer {token}'

    body = json.dumps({'action': action, 'data': data}).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            result = json.loads(e.read().decode('utf-8'))
        except Exception:
            die(f'HTTP error: {e.code} {e.reason}')
    except urllib.error.URLError as e:
        die(f'Network error: {e.reason}')

    if result.get('code') != 0:
        die(f'API error: {result.get("message", "unknown")}')

    return result.get('data')


def load_token():
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE) as f:
            session = json.load(f)
        return session.get('token')
    except Exception:
        return None


def save_session(data):
    ensure_forgeai_dir()
    with open(SESSION_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'Session saved to {SESSION_FILE}')


def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print('Logged out.')


def read_json(filepath):
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)


def cmd_login(args):
    if len(args) < 2:
        die('Usage: forge_client.py login <email> <password>')
    email, password = args[0], args[1]
    data = api_request('auth', 'login', {'email': email, 'password': password}, require_auth=False)
    save_session({'user': data['user'], 'token': data['token']})
    user = data['user']
    print(f'Logged in as {user.get("email")} ({user.get("nickname")}) [{user.get("role")}]')


def cmd_me(args):
    data = api_request('auth', 'getUserInfo')
    user = data if isinstance(data, dict) and '_id' in data else data.get('user', data)
    print(f'User: {user.get("email")} ({user.get("nickname")})')
    print(f'Role: {user.get("role")}')
    print(f'ID: {user.get("_id")}')


def cmd_logout(args):
    clear_session()


def list_local_files(directory, name_filter=None):
    entries = []
    data_dir = os.path.join(FORGEAI_DIR, directory)
    if not os.path.isdir(data_dir):
        return entries
    for fname in sorted(os.listdir(data_dir), reverse=True):
        if not fname.endswith('.json'):
            continue
        fpath = os.path.join(data_dir, fname)
        try:
            data = read_json(fpath)
        except Exception:
            continue
        item_id = data.get('articleId') or data.get('evaluationId') or ''
        title = data.get('title') or (data.get('pending') or {}).get('title', '') or fname
        mtime = os.path.getmtime(fpath)
        if name_filter and name_filter.lower() not in title.lower():
            continue
        entries.append({'id': item_id, 'title': title, 'time': mtime, 'file': fname})
    return entries


def cmd_article_list(args):
    name_filter = None
    rest = list(args)
    while rest:
        if rest[0] == '--name' and len(rest) > 1:
            name_filter = rest[1]
            rest = rest[2:]
        else:
            rest = rest[1:]

    entries = list_local_files('articles', name_filter)
    print(f'Local articles ({len(entries)}):')
    print(f'{"ID":<30} {"Title":<50} {"Time":<25}')
    print('-' * 105)
    for e in entries:
        t = e['time']
        print(f'{e["id"]:<30} {e["title"][:48]:<50} {str(t):<25}')


def cmd_article_create(args):
    if not args:
        die('Usage: forge_client.py article create <file.json>')
    filepath = args[0]
    payload = read_json(filepath)
    result = api_request('articleCrud', 'create', payload)
    article_id = result.get('articleId')
    print(f'Article created: {article_id}')


def cmd_article_update(args):
    if not args:
        die('Usage: forge_client.py article update <file.json>')
    filepath = args[0]
    payload = read_json(filepath)
    api_request('articleCrud', 'update', payload)
    article_id = payload.get('articleId', '')
    print(f'Article updated: {article_id}')


def cmd_evaluation_list(args):
    name_filter = None
    rest = list(args)
    while rest:
        if rest[0] == '--name' and len(rest) > 1:
            name_filter = rest[1]
            rest = rest[2:]
        else:
            rest = rest[1:]

    entries = list_local_files('evaluations', name_filter)
    print(f'Local evaluations ({len(entries)}):')
    print(f'{"ID":<30} {"Title":<50} {"Time":<25}')
    print('-' * 105)
    for e in entries:
        t = e['time']
        print(f'{e["id"]:<30} {e["title"][:48]:<50} {str(t):<25}')


def cmd_evaluation_create(args):
    if not args:
        die('Usage: forge_client.py evaluation create <file.json>')
    filepath = args[0]
    payload = read_json(filepath)
    result = api_request('evaluationCrud', 'create', payload)
    evaluation_id = result.get('evaluationId')
    print(f'Evaluation created: {evaluation_id}')


def cmd_evaluation_update(args):
    if not args:
        die('Usage: forge_client.py evaluation update <file.json>')
    filepath = args[0]
    payload = read_json(filepath)
    api_request('evaluationCrud', 'update', payload)
    evaluation_id = payload.get('evaluationId', '')
    print(f'Evaluation updated: {evaluation_id}')


def cmd_tag_list(args):
    data = api_request('tagsCrud', 'list', require_auth=False)
    tags = data.get('list', [])
    ensure_forgeai_dir()
    with open(TAGS_FILE, 'w') as f:
        json.dump({'tags': tags}, f, indent=2)
    if not tags:
        print('No tags found.')
        return
    for t in tags:
        print(f'{t.get("_id")}: {t.get("name")} ({t.get("color", "none")})')
    print(f'\nCached to {TAGS_FILE}')


def cmd_tag_create(args):
    if not args:
        die('Usage: forge_client.py tag create <name> [--color <hex>]')
    name = args[0]
    color = '#6366F1'
    if '--color' in args:
        idx = args.index('--color')
        if idx + 1 < len(args):
            color = args[idx + 1]
    result = api_request('tagsCrud', 'create', {'name': name, 'color': color})
    tag_id = result.get('tagId')
    print(f'Tag created: {tag_id}')


def cmd_upload(args):
    if not args:
        die('Usage: forge_client.py upload <file> [--storage-path <path>]')
    filepath = args[0]
    if not os.path.isfile(filepath):
        die(f'File not found: {filepath}')

    storage_path = 'forge/image'
    if '--storage-path' in args:
        idx = args.index('--storage-path')
        if idx + 1 < len(args):
            storage_path = args[idx + 1]

    with open(filepath, 'rb') as f:
        file_content = base64.b64encode(f.read()).decode('utf-8')

    filename = os.path.basename(filepath)
    data = {
        'fileContent': file_content,
        'fileName': filename,
        'storagePath': storage_path,
    }
    result = api_request('fileUpload', 'upload', data)
    url = result.get('url', '')
    file_id = result.get('fileId', '')
    print(f'File uploaded: {url}')
    print(f'File ID: {file_id}')


def die(msg):
    print(f'Error: {msg}', file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    ensure_forgeai_dir()
    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        'login': cmd_login,
        'me': cmd_me,
        'logout': cmd_logout,
        'upload': cmd_upload,
        'article': None,
        'evaluation': None,
        'tag': None,
    }

    if cmd == 'article':
        if not args:
            die('Usage: forge_client.py article <create|update> <file.json>')
        sub = args[0]
        sub_args = args[1:]
        if sub == 'list':
            cmd_article_list(sub_args)
        elif sub == 'create':
            cmd_article_create(sub_args)
        elif sub == 'update':
            cmd_article_update(sub_args)
        else:
            die(f'Unknown article subcommand: {sub}')
    elif cmd == 'evaluation':
        if not args:
            die('Usage: forge_client.py evaluation <create|update> <file.json>')
        sub = args[0]
        sub_args = args[1:]
        if sub == 'list':
            cmd_evaluation_list(sub_args)
        elif sub == 'create':
            cmd_evaluation_create(sub_args)
        elif sub == 'update':
            cmd_evaluation_update(sub_args)
        else:
            die(f'Unknown evaluation subcommand: {sub}')
    elif cmd == 'tag':
        if not args:
            die('Usage: forge_client.py tag <list|create> [args...]')
        sub = args[0]
        sub_args = args[1:]
        if sub == 'list':
            cmd_tag_list(sub_args)
        elif sub == 'create':
            cmd_tag_create(sub_args)
        else:
            die(f'Unknown tag subcommand: {sub}')
    elif cmd in commands:
        commands[cmd](args)
    else:
        die(f'Unknown command: {cmd}')


if __name__ == '__main__':
    main()
