#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-toolkit — 管理博客系统文章/标签/用户/评论/留言/说说/文件上传

能力（由 API 文档解析生成）:
  A. list-articles — 分页查询文章列表
  B. create-article — 发布新文章
  C. get-article — 查询单篇文章详情（含评论）
  D. update-article — 更新文章
  E. delete-article — 删除文章（默认软删除，soft=false 硬删除）
  F. restore-article — 恢复软删除的文章
  G. top-articles — 获取热门文章 Top N
  H. list-labels — 获取所有标签（API 路径 /api/lables）
  I. create-label — 创建标签（API 路径 /api/lables）
  J. list-users — 获取用户列表
  K. create-user — 创建用户
  L. list-comments — 获取文章的评论列表
  M. create-comment — 发表评论
  N. delete-comment — 删除评论（软删除）
  O. list-messages — 获取留言列表（含回复）
  P. create-message — 发表留言
  Q. reply-message — 回复留言
  R. delete-message — 删除留言（软删除）
  S. list-moods — 获取说说列表
  T. create-mood — 发布说说
  U. delete-mood — 删除说说
  V. upload-file — 上传单个文件
  W. upload-files — 批量上传文件
  X. list-uploads — 列出所有已上传文件
  Y. delete-upload — 删除已上传文件
  Z. health-check — 健康检查
  AA. capability-list — 列出本 skill 所有能力项

认证: none（无认证，公开 API。BLOG_TOOLKIT_BASE_URL 环境变量配置地址，前缀由 skill name 推导）
退出码: 0=成功; 2=参数错误; 3=缺少配置（地址或认证）; 4=API 调用失败
"""

import argparse
import glob as _glob
import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# Credentials（前缀由 skill name 推导，认证方式由需求澄清决定）
# ---------------------------------------------------------------------------

_CRED_PREFIX = "BLOG_TOOLKIT"   # skill name 转大写下划线
_AUTH_TYPE = "none"             # 无认证（公开 API）
_API_KEY_HEADER = ""            # API Key 的 Header/Query 名（无认证时不使用）
_API_KEY_LOCATION = ""          # header / query（无认证时不使用）

_VERSION = "1.0.0"


def _load_credentials():
    """动态扫描环境变量获取认证凭据（前缀由 skill name 推导）。"""
    creds = {}
    for k, v in os.environ.items():
        u = k.upper()
        if u.startswith(_CRED_PREFIX):
            if 'USERNAME' in u or u.endswith('_USER'):
                creds['username'] = v or creds.get('username', '')
            if 'PASSWORD' in u or u.endswith('_PASS'):
                creds['password'] = v or creds.get('password', '')
            if 'TOKEN' in u:
                creds['token'] = v or creds.get('token', '')
            if 'API_KEY' in u:
                creds['api_key'] = v or creds.get('api_key', '')
            if 'BASE_URL' in u:
                creds['base_url'] = v or creds.get('base_url', '')
    return creds


def _find_project_info():
    """向上递归查找 .project-info/member/ 目录。"""
    current = os.getcwd()
    for _ in range(10):
        candidate = os.path.join(current, '.project-info', 'member')
        if os.path.isdir(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None


def _get_base_url():
    """获取 API base URL——优先级：项目知识 > 环境变量 > 交互输入。

    只读 base_url/api_url/host——不读 token/密码等敏感凭据。
    """
    # 0. 项目知识——向上递归查找 .project-info/member/ 目录
    pi_dir = _find_project_info()
    if pi_dir:
        for fp in _glob.glob(os.path.join(pi_dir, '**'), recursive=True):
            if not os.path.isfile(fp):
                continue
            ext = os.path.splitext(fp)[1].lower()
            if ext not in ('.json', '.yaml', '.yml', '.md', '.txt'):
                continue
            if os.path.getsize(fp) > 1048576:
                continue
            try:
                with open(fp, encoding='utf-8') as f:
                    content = f.read()
                # JSON 解析
                try:
                    data = json.loads(content)
                    for key in ['%s_BASE_URL' % _CRED_PREFIX,
                                'base_url', 'api_url', 'host']:
                        val = (data.get(key)
                               or (data.get('config', {}) or {}).get(key))
                        if (val and isinstance(val, str) and val.strip()
                                and val.strip().startswith('http')):
                            return val.strip().rstrip('/')
                except Exception:
                    pass
                # YAML/Markdown 正则匹配
                for pat in [
                    r'%s_BASE_URL["\']?\s*[:=]\s*["\']?(https?://[^\s"\']+)'
                    % _CRED_PREFIX,
                    r'base_url["\']?\s*[:=]\s*["\']?(https?://[^\s"\']+)',
                    r'api_url["\']?\s*[:=]\s*["\']?(https?://[^\s"\']+)',
                    r'host["\']?\s*[:=]\s*["\']?(https?://[^\s"\']+)',
                ]:
                    m = re.search(pat, content, re.I)
                    if m:
                        return m.group(1).strip().rstrip('/')
            except Exception:
                continue

    # 1. 环境变量
    creds = _load_credentials()
    base_url = creds.get('base_url', '').rstrip('/')
    if not base_url:
        # 2. 交互输入
        print("未检测到 %s_BASE_URL 环境变量，也未从项目知识找到地址。"
              % _CRED_PREFIX)
        print("请输入目标系统 API 地址（如 http://host:port）：")
        base_url = input("> ").strip().rstrip('/')
        if not base_url:
            print("错误：API 地址不能为空", file=sys.stderr)
            sys.exit(3)
        if not (base_url.startswith("http://")
                or base_url.startswith("https://")):
            print("错误：地址必须以 http:// 或 https:// 开头", file=sys.stderr)
            sys.exit(3)
        print("提示：可通过 export %s_BASE_URL=\"%s\" 永久设置，"
              "或在 .project-info/member/ 下配置文件中添加 %s_BASE_URL。"
              % (_CRED_PREFIX, base_url, _CRED_PREFIX))
    return base_url


# ---------------------------------------------------------------------------
# API client（按认证方式生成不同请求代码）
# ---------------------------------------------------------------------------

def _build_auth(creds):
    """根据认证方式构建请求认证参数。

    返回值：dict，可能包含 auth/headers（不含 params——api_key query 模式的
    api_key 由 _api_request 合并到 params 里，避免 params 冲突）。
    """
    if _AUTH_TYPE == "basic":
        from requests.auth import HTTPBasicAuth
        if not creds.get('username') or not creds.get('password'):
            print("错误：缺少认证，请设置环境变量（%s_USERNAME / %s_PASSWORD）"
                  % (_CRED_PREFIX, _CRED_PREFIX), file=sys.stderr)
            sys.exit(3)
        return {"auth": HTTPBasicAuth(creds['username'], creds['password'])}
    elif _AUTH_TYPE == "token":
        if not creds.get('token'):
            print("错误：缺少认证，请设置环境变量（%s_TOKEN）" % _CRED_PREFIX,
                  file=sys.stderr)
            sys.exit(3)
        return {"headers": {"Authorization": "Bearer " + creds['token']}}
    elif _AUTH_TYPE == "api_key":
        if not creds.get('api_key'):
            print("错误：缺少认证，请设置环境变量（%s_API_KEY）" % _CRED_PREFIX,
                  file=sys.stderr)
            sys.exit(3)
        if _API_KEY_LOCATION == "header":
            return {"headers": {_API_KEY_HEADER: creds['api_key']}}
        else:
            return {"_api_key_param": _API_KEY_HEADER,
                    "_api_key_value": creds['api_key']}
    elif _AUTH_TYPE == "none":
        return {}  # 无认证（公开 API）
    else:
        print("错误：未知认证方式 %s" % _AUTH_TYPE, file=sys.stderr)
        sys.exit(2)


def _api_request(method, path, payload=None, params=None, files=None):
    """调用目标系统 REST API。"""
    import requests

    base_url = _get_base_url()
    creds = _load_credentials()
    auth_result = _build_auth(creds)

    # 提取 api_key query 信息（如果有），合并到 params
    api_key_param = auth_result.pop("_api_key_param", None)
    api_key_value = auth_result.pop("_api_key_value", None)
    if api_key_param and api_key_value:
        params = dict(params or {})
        params[api_key_param] = api_key_value

    auth_kwargs = auth_result
    url = f"{base_url}{path}"

    try:
        if method == 'GET':
            resp = requests.get(url, params=params, timeout=30, **auth_kwargs)
        elif method == 'POST':
            resp = requests.post(url, json=payload, files=files, timeout=30,
                                 **auth_kwargs)
        elif method == 'PUT':
            resp = requests.put(url, json=payload, files=files, timeout=30,
                                **auth_kwargs)
        elif method == 'PATCH':
            resp = requests.patch(url, json=payload, timeout=30,
                                  **auth_kwargs)
        elif method == 'DELETE':
            resp = requests.delete(url, params=params, timeout=30,
                                   **auth_kwargs)
        else:
            print(f"错误：不支持的方法 {method}", file=sys.stderr)
            sys.exit(2)

        # 404 等 HTTP 错误：尝试返回 JSON 错误体而非直接退出，便于排错
        if not resp.ok:
            try:
                body = resp.json()
            except ValueError:
                body = {"error": resp.text[:500]}
            body["_http_status"] = resp.status_code
            print(json.dumps(body, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            sys.exit(4)
        if resp.content:
            return resp.json()
        return {}
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)
    except ValueError:
        print("错误：API 返回非 JSON 格式（可能返回 HTML 错误页）",
              file=sys.stderr)
        sys.exit(4)


# ---------------------------------------------------------------------------
# Subcommand implementations（由 API 文档解析动态生成）
# ---------------------------------------------------------------------------

# --- 文章管理 ---

def cmd_list_articles(args):
    """能力 A：分页查询文章列表。"""
    # GET /api/articles
    params = {
        'page': args.page,
        'size': args.size,
        'lid': args.lid,
        'keyword': args.keyword,
    }
    return _api_request('GET', '/api/articles', params=params)


def cmd_create_article(args):
    """能力 B：发布新文章。"""
    # POST /api/articles
    payload = {
        'title': args.title,
        'content': args.content,
        'uid': args.uid,
        'lid': args.lid,
        'heat': args.heat,
    }
    if args.img is not None:
        payload['img'] = args.img
    return _api_request('POST', '/api/articles', payload=payload)


def cmd_get_article(args):
    """能力 C：查询单篇文章详情（含评论）。"""
    # GET /api/articles/{article_id}
    return _api_request('GET', '/api/articles/%s' % args.article_id)


def cmd_update_article(args):
    """能力 D：更新文章。"""
    # PUT /api/articles/{article_id}
    payload = {}
    if args.title is not None:
        payload['title'] = args.title
    if args.content is not None:
        payload['content'] = args.content
    if args.lid is not None:
        payload['lid'] = args.lid
    if args.img is not None:
        payload['img'] = args.img
    if args.heat is not None:
        payload['heat'] = args.heat
    return _api_request('PUT', '/api/articles/%s' % args.article_id,
                        payload=payload)


def cmd_delete_article(args):
    """能力 E：删除文章（默认软删除，soft=false 硬删除）。"""
    # DELETE /api/articles/{article_id}
    params = {'soft': 'true' if args.soft else 'false'}
    return _api_request('DELETE', '/api/articles/%s' % args.article_id,
                        params=params)


def cmd_restore_article(args):
    """能力 F：恢复软删除的文章。"""
    # POST /api/articles/{article_id}/restore
    return _api_request('POST', '/api/articles/%s/restore' % args.article_id)


def cmd_top_articles(args):
    """能力 G：获取热门文章 Top N。"""
    # GET /api/articles/heat/top
    return _api_request('GET', '/api/articles/heat/top',
                        params={'limit': args.limit})


# --- 标签管理（API 路径为 /api/lables，子命令用正确拼写 labels） ---

def cmd_list_labels(args):
    """能力 H：获取所有标签。"""
    # GET /api/lables （API 路径拼写为 lables）
    return _api_request('GET', '/api/lables')


def cmd_create_label(args):
    """能力 I：创建标签。"""
    # POST /api/lables （API 路径拼写为 lables）
    return _api_request('POST', '/api/lables', payload={'lname': args.lname})


# --- 用户管理 ---

def cmd_list_users(args):
    """能力 J：获取用户列表。"""
    # GET /api/users
    return _api_request('GET', '/api/users')


def cmd_create_user(args):
    """能力 K：创建用户。"""
    # POST /api/users
    payload = {
        'uname': args.uname,
        'phone': args.phone,
        'pwd': args.pwd,
        'email': args.email,
        'img': args.img,
    }
    return _api_request('POST', '/api/users', payload=payload)


# --- 评论管理 ---

def cmd_list_comments(args):
    """能力 L：获取文章的评论列表。"""
    # GET /api/comments/{aid}
    return _api_request('GET', '/api/comments/%s' % args.aid)


def cmd_create_comment(args):
    """能力 M：发表评论。"""
    # POST /api/comments
    payload = {
        'uid': args.uid,
        'aid': args.aid,
        'content': args.content,
    }
    return _api_request('POST', '/api/comments', payload=payload)


def cmd_delete_comment(args):
    """能力 N：删除评论（软删除）。"""
    # DELETE /api/comments/{comment_id}
    return _api_request('DELETE', '/api/comments/%s' % args.comment_id)


# --- 留言管理 ---

def cmd_list_messages(args):
    """能力 O：获取留言列表（含回复）。"""
    # GET /api/messages
    return _api_request('GET', '/api/messages')


def cmd_create_message(args):
    """能力 P：发表留言。"""
    # POST /api/messages
    payload = {'uid': args.uid, 'content': args.content}
    return _api_request('POST', '/api/messages', payload=payload)


def cmd_reply_message(args):
    """能力 Q：回复留言。"""
    # POST /api/messages/reply
    payload = {'uid': args.uid, 'mid': args.mid, 'content': args.content}
    return _api_request('POST', '/api/messages/reply', payload=payload)


def cmd_delete_message(args):
    """能力 R：删除留言（软删除）。"""
    # DELETE /api/messages/{message_id}
    return _api_request('DELETE', '/api/messages/%s' % args.message_id)


# --- 说说管理 ---

def cmd_list_moods(args):
    """能力 S：获取说说列表。"""
    # GET /api/moods
    return _api_request('GET', '/api/moods')


def cmd_create_mood(args):
    """能力 T：发布说说。"""
    # POST /api/moods
    payload = {'title': args.title, 'content': args.content, 'src': args.src}
    return _api_request('POST', '/api/moods', payload=payload)


def cmd_delete_mood(args):
    """能力 U：删除说说。"""
    # DELETE /api/moods/{mood_id}
    return _api_request('DELETE', '/api/moods/%s' % args.mood_id)


# --- 文件上传 ---

def cmd_upload_file(args):
    """能力 V：上传单个文件。"""
    # POST /api/upload  multipart/form-data
    path = args.file
    if not os.path.isfile(path):
        print("错误：文件不存在: %s" % path, file=sys.stderr)
        sys.exit(2)
    with open(path, 'rb') as f:
        files = {'file': (os.path.basename(path), f)}
        return _api_request('POST', '/api/upload', files=files)


def cmd_upload_files(args):
    """能力 W：批量上传文件。"""
    # POST /api/upload/multiple  multipart/form-data
    opened = []
    files_list = []
    for p in args.files:
        if not os.path.isfile(p):
            print("错误：文件不存在: %s" % p, file=sys.stderr)
            sys.exit(2)
        fh = open(p, 'rb')
        opened.append(fh)
        files_list.append(('files', (os.path.basename(p), fh)))
    try:
        return _api_request('POST', '/api/upload/multiple', files=files_list)
    finally:
        for fh in opened:
            fh.close()


def cmd_list_uploads(args):
    """能力 X：列出所有已上传文件。"""
    # GET /api/uploads/list
    return _api_request('GET', '/api/uploads/list')


def cmd_delete_upload(args):
    """能力 Y：删除已上传文件。"""
    # DELETE /api/uploads/{filename}
    return _api_request('DELETE', '/api/uploads/%s' % args.filename)


# --- 健康检查 ---

def cmd_health_check(args):
    """能力 Z：健康检查。"""
    # GET /health
    return _api_request('GET', '/health')


# ---------------------------------------------------------------------------
# Capability list
# ---------------------------------------------------------------------------

_CAPABILITIES = [
    ('list-articles', '分页查询文章列表',
     'list-articles [--page N] [--size N] [--lid N] [--keyword S]'),
    ('create-article', '发布新文章',
     'create-article --title S --content S [--uid N] [--lid N] [--img S] [--heat N]'),
    ('get-article', '查询单篇文章详情（含评论）', 'get-article --article-id N'),
    ('update-article', '更新文章',
     'update-article --article-id N [--title S] [--content S] [--lid N] [--img S] [--heat N]'),
    ('delete-article', '删除文章（默认软删除）',
     'delete-article --article-id N [--soft true|false]'),
    ('restore-article', '恢复软删除的文章', 'restore-article --article-id N'),
    ('top-articles', '获取热门文章 Top N', 'top-articles [--limit N]'),
    ('list-labels', '获取所有标签（API 路径 /api/lables）', 'list-labels'),
    ('create-label', '创建标签（API 路径 /api/lables）',
     'create-label --lname S'),
    ('list-users', '获取用户列表', 'list-users'),
    ('create-user', '创建用户',
     'create-user --uname S [--phone S] [--pwd S] [--email S] [--img S]'),
    ('list-comments', '获取文章的评论列表', 'list-comments --aid N'),
    ('create-comment', '发表评论',
     'create-comment --uid N --aid N --content S'),
    ('delete-comment', '删除评论（软删除）', 'delete-comment --comment-id N'),
    ('list-messages', '获取留言列表（含回复）', 'list-messages'),
    ('create-message', '发表留言', 'create-message --uid N --content S'),
    ('reply-message', '回复留言',
     'reply-message --uid N --mid N --content S'),
    ('delete-message', '删除留言（软删除）', 'delete-message --message-id N'),
    ('list-moods', '获取说说列表', 'list-moods'),
    ('create-mood', '发布说说', 'create-mood --content S [--title S] [--src S]'),
    ('delete-mood', '删除说说', 'delete-mood --mood-id N'),
    ('upload-file', '上传单个文件', 'upload-file --file PATH'),
    ('upload-files', '批量上传文件', 'upload-files --files PATH [PATH ...]'),
    ('list-uploads', '列出所有已上传文件', 'list-uploads'),
    ('delete-upload', '删除已上传文件', 'delete-upload --filename S'),
    ('health-check', '健康检查', 'health-check'),
]


def cmd_capability_list(args):
    """能力 AA：列出本 skill 所有能力项。"""
    caps = [{'name': n, 'description': d, 'command': c}
            for n, d, c in _CAPABILITIES]
    caps.append({'name': 'capability-list',
                 'description': '列出本 skill 所有能力项',
                 'command': 'capability-list'})
    return {
        'capability': 'capability-list',
        'skill': 'blog-toolkit',
        'version': _VERSION,
        'auth_type': _AUTH_TYPE,
        'cred_prefix': _CRED_PREFIX,
        'base_url_env': '%s_BASE_URL' % _CRED_PREFIX,
        'subcommand_count': len(caps),
        'capabilities': caps,
    }


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

_DISPATCH = {
    'list-articles': cmd_list_articles,
    'create-article': cmd_create_article,
    'get-article': cmd_get_article,
    'update-article': cmd_update_article,
    'delete-article': cmd_delete_article,
    'restore-article': cmd_restore_article,
    'top-articles': cmd_top_articles,
    'list-labels': cmd_list_labels,
    'create-label': cmd_create_label,
    'list-users': cmd_list_users,
    'create-user': cmd_create_user,
    'list-comments': cmd_list_comments,
    'create-comment': cmd_create_comment,
    'delete-comment': cmd_delete_comment,
    'list-messages': cmd_list_messages,
    'create-message': cmd_create_message,
    'reply-message': cmd_reply_message,
    'delete-message': cmd_delete_message,
    'list-moods': cmd_list_moods,
    'create-mood': cmd_create_mood,
    'delete-mood': cmd_delete_mood,
    'upload-file': cmd_upload_file,
    'upload-files': cmd_upload_files,
    'list-uploads': cmd_list_uploads,
    'delete-upload': cmd_delete_upload,
    'health-check': cmd_health_check,
    'capability-list': cmd_capability_list,
}


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def _cell(v):
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        s = json.dumps(v, ensure_ascii=False)
    else:
        s = str(v)
    s = s.replace("|", "\\|").replace("\n", " ")
    if len(s) > 120:
        s = s[:117] + "..."
    return s


def _render_rows(rows, title=None):
    if not rows:
        return (title + "\n\n" if title else "") + "（无数据）"
    cols = []
    for r in rows:
        if isinstance(r, dict):
            for k in r.keys():
                if k not in cols:
                    cols.append(k)
    if not cols:
        cols = ["value"]
        rows = [{"value": r} for r in rows]
    lines = []
    if title:
        lines.append("### %s" % title)
        lines.append("")
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join("---" for _ in cols) + " |")
    for r in rows:
        lines.append("| " + " | ".join(_cell(r.get(c, "")) for c in cols) + " |")
    return "\n".join(lines)


def _render_kv(obj, title=None):
    lines = []
    if title:
        lines.append("### %s" % title)
        lines.append("")
    lines.append("| 字段 | 值 |")
    lines.append("|---|---|")
    for k, v in obj.items():
        lines.append("| %s | %s |" % (k, _cell(v)))
    return "\n".join(lines)


def render_md(payload):
    """将 JSON 输出转为 Markdown 表格。"""
    # capability-list
    if isinstance(payload, dict) and payload.get('capability') == 'capability-list':
        lines = ["## 能力清单（%s）" % payload.get('skill', ''), "",
                 "认证方式：%s | 凭据前缀：%s | 地址变量：%s"
                 % (payload.get('auth_type', ''),
                    payload.get('cred_prefix', ''),
                    payload.get('base_url_env', '')), "",
                 "| 能力 | 说明 | 命令 |", "|---|---|---|"]
        for c in payload.get('capabilities', []):
            lines.append("| %s | %s | `%s` |"
                         % (c['name'], c['description'], c['command']))
        lines.append("\n共 %d 个子命令" % payload.get('subcommand_count', 0))
        return "\n".join(lines)

    # blog API 响应：{"code":200,"data":...}
    if isinstance(payload, dict) and 'data' in payload and 'code' in payload:
        data = payload['data']
        if isinstance(data, list):
            return _render_rows(data)
        if isinstance(data, dict):
            # get-article: {"article":{...},"comments":[...]}
            if 'article' in data and 'comments' in data:
                parts = [_render_kv(data['article'], title="文章详情")]
                parts.append("")
                parts.append(_render_rows(data['comments'], title="评论列表"))
                return "\n".join(parts)
            return _render_kv(data)
        return _render_kv({"code": payload['code'], "data": data})

    # 健康检查响应：{"status":"ok","service":"blog-api","version":"1.0.0"}
    if isinstance(payload, dict) and 'status' in payload:
        return _render_kv(payload, title="健康检查")

    # 其他：返回 JSON
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Argument helpers
# ---------------------------------------------------------------------------

def _str2bool(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return True
    s = str(v).lower()
    if s in ('true', '1', 'yes', 'y', 't'):
        return True
    if s in ('false', '0', 'no', 'n', 'f'):
        return False
    raise argparse.ArgumentTypeError("布尔值预期 (true/false)，得到: %s" % v)


def _add_common(p):
    p.add_argument('--format', choices=['json', 'md'], default='json',
                   help='输出格式，默认 json')


# ---------------------------------------------------------------------------
# Parser building & Main entry
# ---------------------------------------------------------------------------

def _register_subparsers(sub):
    """Register all subcommand parsers onto the given subparsers object."""
    # 文章管理
    p = sub.add_parser('list-articles', help='分页查询文章列表')
    p.add_argument('--page', type=int, default=1, help='页码，默认 1')
    p.add_argument('--size', type=int, default=10, help='每页数量，默认 10，最大 100')
    p.add_argument('--lid', type=int, default=0, help='标签筛选 ID，默认 0（不筛选）')
    p.add_argument('--keyword', type=str, default='', help='关键词搜索')
    _add_common(p)

    p = sub.add_parser('create-article', help='发布新文章')
    p.add_argument('--title', required=True, help='文章标题（必填）')
    p.add_argument('--content', required=True, help='文章内容（必填）')
    p.add_argument('--uid', type=int, default=1, help='作者用户 ID，默认 1')
    p.add_argument('--lid', type=int, default=1, help='标签 ID，默认 1')
    p.add_argument('--img', default=None, help='封面图片路径')
    p.add_argument('--heat', type=int, default=0, help='热度，默认 0')
    _add_common(p)

    p = sub.add_parser('get-article', help='查询单篇文章详情（含评论）')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    _add_common(p)

    p = sub.add_parser('update-article', help='更新文章')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    p.add_argument('--title', default=None, help='新标题')
    p.add_argument('--content', default=None, help='新内容')
    p.add_argument('--lid', type=int, default=None, help='新标签 ID')
    p.add_argument('--img', default=None, help='新封面图片路径')
    p.add_argument('--heat', type=int, default=None, help='新热度')
    _add_common(p)

    p = sub.add_parser('delete-article', help='删除文章（默认软删除）')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    p.add_argument('--soft', type=_str2bool, nargs='?', const=True, default=True,
                   help='是否软删除，默认 true；传 false 硬删除')
    _add_common(p)

    p = sub.add_parser('restore-article', help='恢复软删除的文章')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    _add_common(p)

    p = sub.add_parser('top-articles', help='获取热门文章 Top N')
    p.add_argument('--limit', type=int, default=5, help='返回数量，默认 5，范围 1-20')
    _add_common(p)

    # 标签管理
    p = sub.add_parser('list-labels', help='获取所有标签（API 路径 /api/lables）')
    _add_common(p)

    p = sub.add_parser('create-label', help='创建标签（API 路径 /api/lables）')
    p.add_argument('--lname', required=True, help='标签名称（必填）')
    _add_common(p)

    # 用户管理
    p = sub.add_parser('list-users', help='获取用户列表')
    _add_common(p)

    p = sub.add_parser('create-user', help='创建用户')
    p.add_argument('--uname', required=True, help='用户名（必填）')
    p.add_argument('--phone', default='', help='手机号，默认空')
    p.add_argument('--pwd', default='', help='密码，默认空')
    p.add_argument('--email', default='', help='邮箱，默认空')
    p.add_argument('--img', default='img/moren.jpg', help='头像，默认 img/moren.jpg')
    _add_common(p)

    # 评论管理
    p = sub.add_parser('list-comments', help='获取文章的评论列表')
    p.add_argument('--aid', type=int, required=True, help='文章 ID（必填）')
    _add_common(p)

    p = sub.add_parser('create-comment', help='发表评论')
    p.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p.add_argument('--aid', type=int, required=True, help='文章 ID（必填）')
    p.add_argument('--content', required=True, help='评论内容（必填）')
    _add_common(p)

    p = sub.add_parser('delete-comment', help='删除评论（软删除）')
    p.add_argument('--comment-id', type=int, required=True, help='评论 ID（必填）')
    _add_common(p)

    # 留言管理
    p = sub.add_parser('list-messages', help='获取留言列表（含回复）')
    _add_common(p)

    p = sub.add_parser('create-message', help='发表留言')
    p.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p.add_argument('--content', required=True, help='留言内容（必填）')
    _add_common(p)

    p = sub.add_parser('reply-message', help='回复留言')
    p.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p.add_argument('--mid', type=int, required=True, help='留言 ID（必填）')
    p.add_argument('--content', required=True, help='回复内容（必填）')
    _add_common(p)

    p = sub.add_parser('delete-message', help='删除留言（软删除）')
    p.add_argument('--message-id', type=int, required=True, help='留言 ID（必填）')
    _add_common(p)

    # 说说管理
    p = sub.add_parser('list-moods', help='获取说说列表')
    _add_common(p)

    p = sub.add_parser('create-mood', help='发布说说')
    p.add_argument('--title', default='', help='标题，默认空')
    p.add_argument('--content', required=True, help='内容（必填）')
    p.add_argument('--src', default='', help='图片路径，默认空')
    _add_common(p)

    p = sub.add_parser('delete-mood', help='删除说说')
    p.add_argument('--mood-id', type=int, required=True, help='说说 ID（必填）')
    _add_common(p)

    # 文件上传
    p = sub.add_parser('upload-file', help='上传单个文件')
    p.add_argument('--file', required=True, help='待上传文件路径（必填）')
    _add_common(p)

    p = sub.add_parser('upload-files', help='批量上传文件')
    p.add_argument('--files', required=True, nargs='+',
                   help='待上传文件路径列表（必填，至少 1 个）')
    _add_common(p)

    p = sub.add_parser('list-uploads', help='列出所有已上传文件')
    _add_common(p)

    p = sub.add_parser('delete-upload', help='删除已上传文件')
    p.add_argument('--filename', required=True, help='文件名（必填）')
    _add_common(p)

    # 健康检查
    p = sub.add_parser('health-check', help='健康检查')
    _add_common(p)

    # 能力清单
    p = sub.add_parser('capability-list', help='列出本 skill 所有能力项')
    _add_common(p)


def _build_parser():
    """构建完整参数解析器。"""
    parser = argparse.ArgumentParser(
        prog='blog-toolkit',
        description='管理博客系统文章/标签/用户/评论/留言/说说/文件上传')
    sub = parser.add_subparsers(dest='command', help='能力命令')
    _register_subparsers(sub)
    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(2)

    handler = _DISPATCH.get(args.command)
    if handler is None:
        print("错误：未知命令 %s" % args.command, file=sys.stderr)
        sys.exit(2)

    try:
        payload = handler(args)
        if args.format == 'md':
            print(render_md(payload))
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
    except SystemExit:
        raise
    except Exception as exc:
        print("错误：%s" % exc, file=sys.stderr)
        sys.exit(4)


if __name__ == '__main__':
    main()
