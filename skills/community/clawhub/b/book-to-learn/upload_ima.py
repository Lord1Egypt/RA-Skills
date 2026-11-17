#!/usr/bin/env python3
"""
Upload a file to an IMA knowledge base folder.
Parameterized: reads kb_name/folder_name from config.json.

Usage:
  python upload_ima.py --file <local.pdf> --config <config.json>
  python upload_ima.py --file <local.pdf> --config <config.json> --book-dir <book_dir>

Steps: preflight → check_repeated_names → create_media → cos-upload → add_knowledge
On auth failure: calls notify_failure.py, exits with code 2.
"""
import json, sys, os, subprocess, argparse, datetime

BASE = os.path.dirname(os.path.abspath(__file__))

def find_ima_skill_dir():
    """Dynamically locate ima-skill across platforms and skill roots."""
    home = os.path.expanduser('~')
    candidates = [
        os.environ.get('IMA_SKILL_DIR', ''),           # explicit env override
        os.path.join(home, '.codebuddy', 'skills', 'ima-skill'),   # CodeBuddy
        os.path.join(home, '.openclaw', 'skills', 'ima-skill'),    # OpenClaw
        os.path.join(home, '.claude', 'skills', 'ima-skill'),      # Claude Code
        os.path.join(home, '.copilot', 'skills', 'ima-skill'),     # GitHub Copilot CLI
        os.path.join(home, '.agents', 'skills', 'ima-skill'),      # Amp / cross-agent
        os.path.join(home, '.config', 'agents', 'skills', 'ima-skill'),
        os.path.join(home, '.config', 'amp', 'skills', 'ima-skill'),
    ]
    for c in candidates:
        if c and os.path.isfile(os.path.join(c, 'ima_api.cjs')):
            return c
    return None

IMA_SKILL_DIR = find_ima_skill_dir()
if IMA_SKILL_DIR:
    IMA_API = os.path.join(IMA_SKILL_DIR, 'ima_api.cjs')
    PREFLIGHT = os.path.join(IMA_SKILL_DIR, 'knowledge-base', 'scripts', 'preflight-check.cjs')
    COS_UPLOAD = os.path.join(IMA_SKILL_DIR, 'knowledge-base', 'scripts', 'cos-upload.cjs')
else:
    IMA_API = PREFLIGHT = COS_UPLOAD = None

def find_node():
    """Find a working node binary (skip bun shims)."""
    for candidate in ['/usr/bin/node', '/usr/local/bin/node', '/opt/homebrew/bin/node']:
        if os.path.isfile(candidate):
            return candidate
    # try nvm
    home = os.path.expanduser('~')
    import glob
    for p in sorted(glob.glob(os.path.join(home, '.nvm', 'versions', 'node', '*', 'bin', 'node')), reverse=True):
        return p
    return 'node'  # fallback

NODE = find_node()

def run(cmd, input_str=None):
    env = dict(os.environ)
    env.pop('NODE_OPTIONS', None)
    try:
        r = subprocess.run(cmd, input=input_str, capture_output=True, text=True,
                           env=env, timeout=300)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        # 超时不抛异常：调用方按既有错误分支输出 JSON（保持 0/1/2 退出码契约）
        return 124, '', 'subprocess timeout after 300s: %s' % os.path.basename(str(cmd[0]))
    except FileNotFoundError as e:
        # 可执行文件缺失：不能让 traceback 打出完整命令行（可能含 COS 临时凭据）
        return 127, '', 'executable not found: %s' % e.filename
    except Exception as e:
        # 其他异常：只报异常类型与消息，绝不打印 argv（可能含 COS 临时凭据）
        return 1, '', '%s: %s' % (type(e).__name__, e)

def ima_api(api_path, body_dict):
    cid_path = os.path.expanduser('~/.config/ima/client_id')
    akey_path = os.path.expanduser('~/.config/ima/api_key')
    if not os.path.exists(cid_path) or not os.path.exists(akey_path):
        return False, {'msg': 'IMA credentials not configured (~/.config/ima/)', 'auth_fail': True}
    try:
        with open(cid_path, encoding='utf-8-sig') as f:
            cid = f.read().strip()
        with open(akey_path, encoding='utf-8-sig') as f:
            akey = f.read().strip()
    except OSError as e:
        return False, {'msg': 'IMA credentials unreadable: %s' % e, 'auth_fail': True}
    opts = json.dumps({'clientId': cid, 'apiKey': akey})
    rc, out, err = run([NODE, IMA_API, api_path, json.dumps(body_dict, ensure_ascii=False), opts])
    if rc != 0:
        err_data = {}
        try: err_data = json.loads(err)
        except Exception: pass
        return False, {'script_error': err_data.get('msg', err.strip()[:300]), 'code': err_data.get('code')}
    try:
        resp = json.loads(out)
    except:
        return False, {'parse_error': out[:300]}
    if resp.get('code') != 0:
        return False, {'msg': resp.get('msg', ''), 'code': resp.get('code'), 'auth_fail': is_auth_error(resp)}
    return True, resp.get('data', {})

def is_auth_error(resp):
    """Classify by API error code first; keyword match is only a fallback.
    Guessing by msg text mislabels e.g. 'invalid filename' as AUTH_FAIL,
    which would skip retries and wrongly notify users that keys expired."""
    code = resp.get('code')
    if isinstance(code, int) and code != 0:
        # known auth-ish codes (per IMA OpenAPI behavior) -> definitive True
        if code in (10013, 10014, 10015, 10017, 10018, 10019, 10020, 10021, 10022,
                    99991, 99992, 99993, 99994, 99995, 99996, 99997, 99998, 99999,
                    40001, 40002, 40003, 40004, 40005, 40006, 40007, 40008, 40009,
                    40100, 40101, 40102, 40103):
            return True
        # unknown numeric code -> fall through to keyword fallback (safer than guessing)
    elif code in (None, 0, '') and not resp.get('msg'):
        return False
    # fallback for unknown numeric/string codes: match explicit auth phrases only
    msg = (resp.get('msg') or '').lower()
    return any(k in msg for k in ['unauthorized', 'invalid api key', 'invalid apikey',
                                  'api key expired', 'apikey expired', 'credential',
                                  'auth fail', 'authentication', 'token expired',
                                  '鉴权失败', '密钥失效', '密钥过期', '认证失败', '令牌过期', '凭证无效'])

def find_kb_by_name(name):
    cursor = ''
    for _ in range(50):  # 分页上限：异常 next_cursor 回环时不至于无限循环
        ok, data = ima_api('openapi/wiki/v1/search_knowledge_base', {'query': name, 'cursor': cursor, 'limit': 20})
        if ok is not True and ok != True:
            return None, data  # data carries auth_fail flag when applicable
        for item in data.get('info_list', []):
            if item.get('kb_name') == name:
                return item.get('kb_id'), None
        if data.get('is_end'):
            return None, {'msg': 'knowledge base not found: ' + name}
        cursor = data.get('next_cursor', '')

def find_folder_by_name(kb_id, name):
    cursor = ''
    for _ in range(50):  # paginate: folders beyond page 1 must be found too（带上限防回环）
        ok, data = ima_api('openapi/wiki/v1/get_knowledge_list', {'knowledge_base_id': kb_id, 'cursor': cursor, 'limit': 50})
        if ok is not True and ok != True:
            return None, data
        for item in data.get('knowledge_list', []):
            if item.get('media_type') == 99 and item.get('title') == name:
                return item.get('media_id'), None
        if data.get('is_end'):
            return None, {'msg': 'folder not found: ' + name}
        cursor = data.get('next_cursor', '')
        if not cursor:
            return None, {'msg': 'folder not found: ' + name}

def notify_failure(book_dir, config, reason):
    script = os.path.join(BASE, 'notify_failure.py')
    cfg_path = os.path.join(book_dir, 'config.json') if book_dir else (config or '')
    if not cfg_path:
        return  # 无 config 路径可指向时无从通知，跳过（退出码 2 仍会告知调用方）
    try:
        subprocess.run([sys.executable, script, '--book', '', '--stage', 'upload', '--reason', reason,
                        '--config', cfg_path], capture_output=True, timeout=30)
    except Exception:
        # notification is best-effort; the exit code 2 still signals AUTH_FAIL
        pass

def upload(file_path, config, book_dir=None):
    if not IMA_SKILL_DIR:
        print(json.dumps({'ok': False, 'error': 'ima-skill not found. Set IMA_SKILL_DIR env or install to ~/.codebuddy/skills/ima-skill (or ~/.openclaw, ~/.claude, ~/.copilot, ~/.agents)'}, ensure_ascii=False))
        return 1
    ima_cfg = config.get('ima', {})
    kb_name = ima_cfg.get('kbName', '')
    folder_name = ima_cfg.get('folderName', '')
    if not kb_name:
        print(json.dumps({'ok': False, 'error': 'ima.kbName not set in config.json'}, ensure_ascii=False))
        return 1

    kb_id, err = find_kb_by_name(kb_name)
    if kb_id is None:
        if isinstance(err, dict) and err.get('auth_fail'):
            notify_failure(book_dir, config, 'IMA密钥失效: ' + str(err.get('msg', '')))
            print(json.dumps({'ok': False, 'stage': 'find_kb', 'auth_fail': True}, ensure_ascii=False))
            return 2
        print(json.dumps({'ok': False, 'stage': 'find_kb', 'error': err}, ensure_ascii=False))
        return 1
    folder_id = None
    if folder_name:
        folder_id, folder_err = find_folder_by_name(kb_id, folder_name)
        if folder_id is None:
            if isinstance(folder_err, dict) and folder_err.get('auth_fail'):
                notify_failure(book_dir, config, 'IMA密钥失效: ' + str(folder_err.get('msg', '')))
                print(json.dumps({'ok': False, 'stage': 'find_folder', 'auth_fail': True}, ensure_ascii=False))
                return 2
            # 不静默退化为传根目录：文件会散落在知识库根下，事后难以收拾
            print(json.dumps({'ok': False, 'stage': 'find_folder',
                              'error': 'IMA 文件夹未找到：%r（不会退化为传知识库根目录；'
                                       '请到 IMA 客户端核对文件夹名）' % folder_name}, ensure_ascii=False))
            return 1

    # preflight
    rc, out, err = run([NODE, PREFLIGHT, '--file', file_path])
    if rc != 0:
        print(json.dumps({'ok': False, 'stage': 'preflight', 'error': err.strip()[:300]}, ensure_ascii=False))
        return 1
    try:
        pf = json.loads(out)
    except Exception:
        print(json.dumps({'ok': False, 'stage': 'preflight_parse', 'error': out[:300]}, ensure_ascii=False))
        return 1
    if not pf.get('pass'):
        print(json.dumps({'ok': False, 'stage': 'preflight', 'reason': pf.get('reason')}, ensure_ascii=False))
        return 1
    file_name = pf.get('file_name'); file_ext = pf.get('file_ext')
    file_size = pf.get('file_size'); media_type = pf.get('media_type'); content_type = pf.get('content_type')
    if not all((file_name, file_ext, file_size is not None, media_type, content_type)):
        print(json.dumps({'ok': False, 'stage': 'preflight_parse',
                          'error': 'preflight 输出缺字段: %s' % sorted(pf.keys())}, ensure_ascii=False))
        return 1

    # check_repeated_names
    body = {'params': [{'name': file_name, 'media_type': media_type}], 'knowledge_base_id': kb_id}
    if folder_id: body['folder_id'] = folder_id
    ok, data = ima_api('openapi/wiki/v1/check_repeated_names', body)
    if data.get('auth_fail'):
        notify_failure(book_dir, config, 'IMA密钥失效: ' + str(data.get('msg','')))
        print(json.dumps({'ok': False, 'stage': 'check_repeated', 'auth_fail': True}, ensure_ascii=False))
        return 2
    if ok is not True and ok != True:
        print(json.dumps({'ok': False, 'stage': 'check_repeated', 'error': data}, ensure_ascii=False))
        return 1
    params = data.get('params', [])
    if params and params[0].get('is_repeated'):
        ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        name, ext = os.path.splitext(file_name)
        file_name = f"{name}_{ts}{ext}"

    # create_media
    body = {'file_name': file_name, 'file_size': file_size, 'content_type': content_type,
            'knowledge_base_id': kb_id, 'file_ext': file_ext}
    ok, data = ima_api('openapi/wiki/v1/create_media', body)
    if data.get('auth_fail'):
        notify_failure(book_dir, config, 'IMA密钥失效: ' + str(data.get('msg','')))
        print(json.dumps({'ok': False, 'stage': 'create_media', 'auth_fail': True}, ensure_ascii=False))
        return 2
    if ok is not True and ok != True:
        print(json.dumps({'ok': False, 'stage': 'create_media', 'error': data}, ensure_ascii=False))
        return 1
    media_id = data.get('media_id')
    cos = data.get('cos_credential', {})

    # cos-upload
    cmd = [NODE, COS_UPLOAD, '--file', file_path,
           '--secret-id', cos.get('secret_id',''), '--secret-key', cos.get('secret_key',''),
           '--token', cos.get('token',''), '--bucket', cos.get('bucket_name',''),
           '--region', cos.get('region',''), '--cos-key', cos.get('cos_key',''),
           '--content-type', content_type, '--start-time', str(cos.get('start_time','')),
           '--expired-time', str(cos.get('expired_time','')), '--timeout', '300000']
    rc, out, err = run(cmd)
    if rc != 0:
        print(json.dumps({'ok': False, 'stage': 'cos_upload', 'error': err.strip()[:400]}, ensure_ascii=False))
        return 1

    # add_knowledge
    body = {'media_type': media_type, 'media_id': media_id, 'title': file_name,
            'knowledge_base_id': kb_id,
            'file_info': {'cos_key': cos.get('cos_key',''), 'file_size': file_size, 'file_name': file_name}}
    if folder_id: body['folder_id'] = folder_id
    ok, data = ima_api('openapi/wiki/v1/add_knowledge', body)
    if data.get('auth_fail'):
        notify_failure(book_dir, config, 'IMA密钥失效: ' + str(data.get('msg','')))
        print(json.dumps({'ok': False, 'stage': 'add_knowledge', 'auth_fail': True}, ensure_ascii=False))
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
    ap.add_argument('--config', required=True, help='config.json path')
    ap.add_argument('--book-dir', help='book data directory (for notify_failure)')
    args = ap.parse_args()
    try:
        config = json.load(open(args.config, encoding='utf-8'))
    except (OSError, ValueError) as e:
        print(json.dumps({'ok': False, 'error': 'config 读取失败 %s: %s' % (args.config, e)},
                         ensure_ascii=False))
        sys.exit(1)
    try:
        sys.exit(upload(args.file, config, args.book_dir))
    except SystemExit:
        raise
    except Exception as e:
        # 兜底：任何未预期异常都以 JSON 报出（保持 0/1/2 契约，不裸 traceback）
        print(json.dumps({'ok': False, 'error': '%s: %s' % (type(e).__name__, e)},
                         ensure_ascii=False))
        sys.exit(1)
