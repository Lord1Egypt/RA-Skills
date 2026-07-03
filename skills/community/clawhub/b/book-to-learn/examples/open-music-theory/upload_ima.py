#!/usr/bin/env python3
"""
Upload a file to an IMA knowledge base folder.
Uses the installed ima-skill's ima_api.cjs + cos-upload.cjs.

Usage:
  python upload_ima.py --file <local.pdf> --kb-name "【权威】音乐制作：风格与流派" --folder-name "每日一个知识点"

Steps follow ima-skill knowledge-base SKILL.md:
  preflight → check_repeated_names → create_media → cos-upload → add_knowledge
On auth failure (key expired), calls notify_key_expired.py and exits with code 2.
"""
import json, sys, os, subprocess, argparse, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
IMA_SKILL_DIR = '/root/.codebuddy/skills/ima-skill'
IMA_API = os.path.join(IMA_SKILL_DIR, 'ima_api.cjs')
PREFLIGHT = os.path.join(IMA_SKILL_DIR, 'knowledge-base', 'scripts', 'preflight-check.cjs')
COS_UPLOAD = os.path.join(IMA_SKILL_DIR, 'knowledge-base', 'scripts', 'cos-upload.cjs')
NODE = '/usr/bin/node'

# Target knowledge base & folder (resolved at runtime by name)
DEFAULT_KB_NAME = '【权威】音乐制作：风格与流派'
DEFAULT_FOLDER_NAME = '每日一个知识点'

def run(cmd, input_str=None):
    """Run a command with clean env (strip NODE_OPTIONS bun shim), return (rc, stdout, stderr)."""
    env = dict(os.environ)
    env.pop('NODE_OPTIONS', None)
    r = subprocess.run(cmd, input=input_str, capture_output=True, text=True, env=env, timeout=300)
    return r.returncode, r.stdout, r.stderr

def ima_api(api_path, body_dict):
    """Call ima_api.cjs. Returns (ok, data_or_error)."""
    cid = open(os.path.expanduser('~/.config/ima/client_id')).read().strip()
    akey = open(os.path.expanduser('~/.config/ima/api_key')).read().strip()
    opts = json.dumps({'clientId': cid, 'apiKey': akey})
    rc, out, err = run([NODE, IMA_API, api_path, json.dumps(body_dict, ensure_ascii=False), opts])
    if rc != 0:
        # script-level error
        err_data = {}
        try: err_data = json.loads(err)
        except: pass
        return False, {'script_error': err_data.get('msg', err.strip()[:300]), 'code': err_data.get('code')}
    try:
        resp = json.loads(out)
    except:
        return False, {'parse_error': out[:300]}
    if resp.get('code') != 0:
        msg = resp.get('msg', '')
        # detect auth/key failure
        low = msg.lower()
        if any(k in low for k in ['auth', 'unauthorized', 'invalid', 'expired', 'token', 'credential', '密钥', '认证', '鉴权']):
            return 'AUTH_FAIL', {'msg': msg, 'code': resp.get('code')}
        return False, {'msg': msg, 'code': resp.get('code')}
    return True, resp.get('data', {})

def find_kb_by_name(name):
    cursor = ''
    while True:
        ok, data = ima_api('openapi/wiki/v1/search_knowledge_base', {'query': name, 'cursor': cursor, 'limit': 20})
        if ok is not True and ok != True:
            return None, data
        for item in data.get('info_list', []):
            if item.get('kb_name') == name:
                return item.get('kb_id'), None
        if data.get('is_end'):
            return None, {'msg': 'knowledge base not found: ' + name}
        cursor = data.get('next_cursor', '')

def find_folder_by_name(kb_id, name):
    ok, data = ima_api('openapi/wiki/v1/get_knowledge_list', {'knowledge_base_id': kb_id, 'cursor': '', 'limit': 50})
    if ok is not True and ok != True:
        return None, data
    for item in data.get('knowledge_list', []):
        if item.get('media_type') == 99 and item.get('title') == name:
            return item.get('media_id'), None
    return None, {'msg': 'folder not found: ' + name}

def notify_expired(reason):
    """Call notify_key_expired.py"""
    script = os.path.join(BASE, 'notify_key_expired.py')
    subprocess.run(['python3.11', script, reason], capture_output=True, timeout=30)

def upload(file_path, kb_name=DEFAULT_KB_NAME, folder_name=DEFAULT_FOLDER_NAME):
    # Step 0: resolve kb_id & folder_id
    kb_id, err = find_kb_by_name(kb_name)
    if kb_id is None:
        if err and err.get('msg','').lower().find('not found')>=0:
            print(json.dumps({'ok': False, 'stage': 'find_kb', 'error': err}, ensure_ascii=False))
            return 1
        print(json.dumps({'ok': False, 'stage': 'find_kb', 'error': err}, ensure_ascii=False))
        return 1
    folder_id, err = find_folder_by_name(kb_id, folder_name)
    if folder_id is None:
        # fallback: upload to root (omit folder_id)
        folder_id = None

    # Step 1: preflight
    rc, out, err = run([NODE, PREFLIGHT, '--file', file_path])
    if rc != 0:
        print(json.dumps({'ok': False, 'stage': 'preflight', 'error': err.strip()[:300]}, ensure_ascii=False))
        return 1
    try:
        pf = json.loads(out)
    except:
        print(json.dumps({'ok': False, 'stage': 'preflight_parse', 'error': out[:300]}, ensure_ascii=False))
        return 1
    if not pf.get('pass'):
        print(json.dumps({'ok': False, 'stage': 'preflight', 'reason': pf.get('reason')}, ensure_ascii=False))
        return 1
    file_name = pf['file_name']; file_ext = pf['file_ext']
    file_size = pf['file_size']; media_type = pf['media_type']; content_type = pf['content_type']

    # Step 2: check_repeated_names
    body = {'params': [{'name': file_name, 'media_type': media_type}], 'knowledge_base_id': kb_id}
    if folder_id: body['folder_id'] = folder_id
    ok, data = ima_api('openapi/wiki/v1/check_repeated_names', body)
    if ok == 'AUTH_FAIL':
        notify_expired(data.get('msg',''))
        print(json.dumps({'ok': False, 'stage': 'check_repeated', 'auth_fail': True, 'msg': data.get('msg')}, ensure_ascii=False))
        return 2
    if ok is not True and ok != True:
        print(json.dumps({'ok': False, 'stage': 'check_repeated', 'error': data}, ensure_ascii=False))
        return 1
    # if repeated, append timestamp
    params = data.get('params', [])
    if params and params[0].get('is_repeated'):
        import datetime
        ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        name, ext = os.path.splitext(file_name)
        file_name = f"{name}_{ts}{ext}"

    # Step 3: create_media
    body = {'file_name': file_name, 'file_size': file_size, 'content_type': content_type,
            'knowledge_base_id': kb_id, 'file_ext': file_ext}
    ok, data = ima_api('openapi/wiki/v1/create_media', body)
    if ok == 'AUTH_FAIL':
        notify_expired(data.get('msg',''))
        print(json.dumps({'ok': False, 'stage': 'create_media', 'auth_fail': True, 'msg': data.get('msg')}, ensure_ascii=False))
        return 2
    if ok is not True and ok != True:
        print(json.dumps({'ok': False, 'stage': 'create_media', 'error': data}, ensure_ascii=False))
        return 1
    media_id = data.get('media_id')
    cos = data.get('cos_credential', {})

    # Step 4: cos-upload
    cmd = [NODE, COS_UPLOAD,
           '--file', file_path,
           '--secret-id', cos.get('secret_id',''),
           '--secret-key', cos.get('secret_key',''),
           '--token', cos.get('token',''),
           '--bucket', cos.get('bucket_name',''),
           '--region', cos.get('region',''),
           '--cos-key', cos.get('cos_key',''),
           '--content-type', content_type,
           '--start-time', str(cos.get('start_time','')),
           '--expired-time', str(cos.get('expired_time','')),
           '--timeout', '300000']
    rc, out, err = run(cmd)
    if rc != 0:
        print(json.dumps({'ok': False, 'stage': 'cos_upload', 'error': err.strip()[:400]}, ensure_ascii=False))
        return 1

    # Step 5: add_knowledge
    body = {'media_type': media_type, 'media_id': media_id, 'title': file_name,
            'knowledge_base_id': kb_id,
            'file_info': {'cos_key': cos.get('cos_key',''), 'file_size': file_size, 'file_name': file_name}}
    if folder_id: body['folder_id'] = folder_id
    ok, data = ima_api('openapi/wiki/v1/add_knowledge', body)
    if ok == 'AUTH_FAIL':
        notify_expired(data.get('msg',''))
        print(json.dumps({'ok': False, 'stage': 'add_knowledge', 'auth_fail': True, 'msg': data.get('msg')}, ensure_ascii=False))
        return 2
    if ok is not True and ok != True:
        print(json.dumps({'ok': False, 'stage': 'add_knowledge', 'error': data}, ensure_ascii=False))
        return 1

    print(json.dumps({'ok': True, 'file_name': file_name, 'kb_id': kb_id,
                      'folder_id': folder_id, 'media_id': media_id}, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--file', required=True)
    ap.add_argument('--kb-name', default=DEFAULT_KB_NAME)
    ap.add_argument('--folder-name', default=DEFAULT_FOLDER_NAME)
    args = ap.parse_args()
    sys.exit(upload(args.file, args.kb_name, args.folder_name))
