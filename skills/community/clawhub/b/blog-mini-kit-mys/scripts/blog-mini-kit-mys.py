#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-mini-kit-mys — 管理 Blog System (FastAPI) 全部 32 个 API 端点

能力（由 OpenAPI 文档解析生成）:
  A. list-articles — 分页查询文章列表
  B. create-article — 发布新文章
  C. get-article — 查询单篇文章详情（含评论）
  D. update-article — 更新文章
  E. delete-article — 删除文章（默认软删除）
  F. restore-article — 恢复软删除的文章
  G. top-articles — 获取热门文章 Top N
  H. list-labels — 获取所有标签
  I. create-label — 创建标签
  J. list-users — 获取用户列表
  K. create-user — 创建用户
  L. create-comment — 发表评论
  M. list-comments — 获取文章评论列表
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
  X. list-uploads — 列出已上传文件
  Y. delete-upload — 删除已上传文件
  Z. health-check — 健康检查
  AA. blog-home — 博客首页（HTML）
  AB. blog-article — 文章详情页（HTML）
  AC. admin-page — 后台管理页面（HTML）
  AD. admin-login — 后台登录（获取 token）
  AE. admin-logout — 退出后台登录
  AF. admin-delete-articles — 后台批量删除文章

认证: none（公开 API，无需凭据；后台管理端点需 admin/admin 登录获取 token）
退出码: 0=成功; 2=参数错误; 3=缺少配置（地址）; 4=API 调用失败
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Credentials（前缀由 skill name 推导，认证方式为 none）
# ---------------------------------------------------------------------------

_CRED_PREFIX = "BLOG_MINI_KIT_MYS"
_AUTH_TYPE = "none"
_API_KEY_HEADER = ""
_API_KEY_LOCATION = ""


def _load_credentials():
    """获取认证凭据——4 级优先级（与 base_url 一致）。

    1. 项目知识：递归扫描 .project-info/ 下所有 JSON 文件（secrets.{PREFIX}_*）
    2. 环境变量：扫描 {PREFIX}_* 开头变量（项目知识缺失时回退）
    3. 当前上下文：A2A context 已注入的环境变量（已包含在步骤 2）
    4. 交互输入：以上都无时提示用户输入
    """
    creds = {}
    creds.update(_load_from_project_knowledge())
    for k, v in os.environ.items():
        u = k.upper()
        if u.startswith(_CRED_PREFIX):
            if 'USERNAME' in u or u.endswith('_USER'):
                creds.setdefault('username', v)
            if 'PASSWORD' in u or u.endswith('_PASS'):
                creds.setdefault('password', v)
            if 'TOKEN' in u:
                creds.setdefault('token', v)
            if 'API_KEY' in u:
                creds.setdefault('api_key', v)
            if 'BASE_URL' in u:
                creds.setdefault('base_url', v)
    return creds


def _load_from_project_knowledge():
    """从 .project-info/ 目录递归查找 JSON 配置文件，读取 secrets/config 字段。

    .project-info/ 由 grape worker 物化到 agent 工作目录（cwd）下。
    从当前目录逐级向上查找 .project-info/，兼容从 skill 子目录运行的情况。
    base_url 和 secrets 都严格按 {PREFIX}_ 前缀精确匹配，不做 fallback。
    """
    import glob
    creds = {}
    search_root = os.getcwd()
    info_dir = None
    for _ in range(6):
        candidate = os.path.join(search_root, '.project-info')
        if os.path.isdir(candidate):
            info_dir = candidate
            break
        parent = os.path.dirname(search_root)
        if parent == search_root:
            break
        search_root = parent
    if info_dir is None:
        info_dir = '.project-info'
    for filepath in glob.glob(os.path.join(info_dir, '**', '*.json'), recursive=True):
        try:
            with open(filepath) as f:
                data = json.load(f)
            secrets = data.get('secrets', {})
            config = data.get('config', {})
            prefix = _CRED_PREFIX + '_'
            for key, val in secrets.items():
                if key.upper().startswith(prefix):
                    if 'USERNAME' in key.upper():
                        creds.setdefault('username', val)
                    if 'PASSWORD' in key.upper():
                        creds.setdefault('password', val)
                    if 'TOKEN' in key.upper():
                        creds.setdefault('token', val)
                    if 'API_KEY' in key.upper():
                        creds.setdefault('api_key', val)
            if 'base_url' not in creds:
                for key, val in config.items():
                    if key.upper() == (prefix + 'BASE_URL'):
                        creds.setdefault('base_url', val)
                        break
        except Exception:
            continue
    return creds


def _get_base_url():
    """获取 API base URL——4 级优先级（与凭据读取一致）。"""
    creds = _load_credentials()
    base_url = creds.get('base_url', '').rstrip('/')
    if not base_url:
        print("未检测到 %s_BASE_URL 环境变量，也未在 .project-info/ 找到配置。" % _CRED_PREFIX)
        print("请输入目标系统 API 地址（如 http://host:port）：")
        base_url = input("> ").strip().rstrip('/')
        if not base_url:
            print("错误：API 地址不能为空", file=sys.stderr)
            sys.exit(3)
        if not (base_url.startswith("http://") or base_url.startswith("https://")):
            print("错误：地址必须以 http:// 或 https:// 开头", file=sys.stderr)
            sys.exit(3)
        print("提示：可通过 export %s_BASE_URL=\"%s\" 永久设置，避免每次输入。" % (_CRED_PREFIX, base_url))
    return base_url


# ---------------------------------------------------------------------------
# API client（无认证模式）
# ---------------------------------------------------------------------------

def _build_auth(creds):
    """根据认证方式构建请求认证参数。"""
    if _AUTH_TYPE == "none":
        return {}
    print("错误：未知认证方式 %s" % _AUTH_TYPE, file=sys.stderr)
    sys.exit(2)


def _api_request(method, path, payload=None, params=None, files=None, raw=False):
    """调用目标系统 REST API。

    raw=True 时返回响应文本（用于 HTML 页面端点）。
    """
    import requests

    base_url = _get_base_url()
    creds = _load_credentials()
    auth_kwargs = _build_auth(creds)
    url = f"{base_url}{path}"

    try:
        if method == 'GET':
            resp = requests.get(url, params=params, timeout=30, **auth_kwargs)
        elif method == 'POST':
            resp = requests.post(url, json=payload, files=files, timeout=30, **auth_kwargs)
        elif method == 'PUT':
            resp = requests.put(url, json=payload, files=files, timeout=30, **auth_kwargs)
        elif method == 'PATCH':
            resp = requests.patch(url, json=payload, timeout=30, **auth_kwargs)
        elif method == 'DELETE':
            resp = requests.delete(url, params=params, timeout=30, **auth_kwargs)
        else:
            print(f"错误：不支持的方法 {method}", file=sys.stderr)
            sys.exit(2)

        resp.raise_for_status()
        if raw:
            return resp.text
        if resp.content:
            try:
                return resp.json()
            except ValueError:
                return resp.text
        return {}
    except requests.exceptions.HTTPError as e:
        print(f"错误：API 调用失败 {resp.status_code}: {e}", file=sys.stderr)
        sys.exit(4)
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)


# ---------------------------------------------------------------------------
# Subcommand implementations — 文章 API (7)
# ---------------------------------------------------------------------------

def cmd_list_articles(args):
    """A: 分页查询文章列表。"""
    params = {'page': args.page, 'size': args.size}
    if args.lid:
        params['lid'] = args.lid
    if args.keyword:
        params['keyword'] = args.keyword
    return _api_request('GET', '/api/articles', params=params)


def cmd_create_article(args):
    """B: 发布新文章。"""
    payload = {'title': args.title, 'content': args.content, 'uid': args.uid,
               'lid': args.lid, 'heat': args.heat}
    if args.img is not None:
        payload['img'] = args.img
    return _api_request('POST', '/api/articles', payload=payload)


def cmd_get_article(args):
    """C: 查询单篇文章详情（含评论）。"""
    return _api_request('GET', f'/api/articles/{args.article_id}')


def cmd_update_article(args):
    """D: 更新文章。"""
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
    return _api_request('PUT', f'/api/articles/{args.article_id}', payload=payload)


def cmd_delete_article(args):
    """E: 删除文章（默认软删除）。"""
    soft = 'false' if args.hard else 'true'
    return _api_request('DELETE', f'/api/articles/{args.article_id}', params={'soft': soft})


def cmd_restore_article(args):
    """F: 恢复软删除的文章。"""
    return _api_request('POST', f'/api/articles/{args.article_id}/restore')


def cmd_top_articles(args):
    """G: 获取热门文章 Top N。"""
    return _api_request('GET', '/api/articles/heat/top', params={'limit': args.limit})


# ---------------------------------------------------------------------------
# 标签 API (2)
# ---------------------------------------------------------------------------

def cmd_list_labels(args):
    """H: 获取所有标签。"""
    return _api_request('GET', '/api/lables')


def cmd_create_label(args):
    """I: 创建标签。"""
    return _api_request('POST', '/api/lables', payload={'lname': args.lname})


# ---------------------------------------------------------------------------
# 用户 API (2)
# ---------------------------------------------------------------------------

def cmd_list_users(args):
    """J: 获取用户列表。"""
    return _api_request('GET', '/api/users')


def cmd_create_user(args):
    """K: 创建用户。"""
    payload = {'uname': args.uname, 'phone': args.phone, 'pwd': args.pwd,
               'email': args.email, 'img': args.img}
    return _api_request('POST', '/api/users', payload=payload)


# ---------------------------------------------------------------------------
# 评论 API (3)
# ---------------------------------------------------------------------------

def cmd_create_comment(args):
    """L: 发表评论。"""
    payload = {'uid': args.uid, 'aid': args.aid, 'content': args.content}
    return _api_request('POST', '/api/comments', payload=payload)


def cmd_list_comments(args):
    """M: 获取文章评论列表。"""
    return _api_request('GET', f'/api/comments/{args.aid}')


def cmd_delete_comment(args):
    """N: 删除评论（软删除）。"""
    return _api_request('DELETE', f'/api/comments/{args.comment_id}')


# ---------------------------------------------------------------------------
# 留言 API (4)
# ---------------------------------------------------------------------------

def cmd_list_messages(args):
    """O: 获取留言列表（含回复）。"""
    return _api_request('GET', '/api/messages')


def cmd_create_message(args):
    """P: 发表留言。"""
    payload = {'uid': args.uid, 'content': args.content}
    return _api_request('POST', '/api/messages', payload=payload)


def cmd_reply_message(args):
    """Q: 回复留言。"""
    payload = {'uid': args.uid, 'mid': args.mid, 'content': args.content}
    return _api_request('POST', '/api/messages/reply', payload=payload)


def cmd_delete_message(args):
    """R: 删除留言（软删除）。"""
    return _api_request('DELETE', f'/api/messages/{args.message_id}')


# ---------------------------------------------------------------------------
# 说说 API (3)
# ---------------------------------------------------------------------------

def cmd_list_moods(args):
    """S: 获取说说列表。"""
    return _api_request('GET', '/api/moods')


def cmd_create_mood(args):
    """T: 发布说说。"""
    payload = {'title': args.title, 'content': args.content, 'src': args.src}
    return _api_request('POST', '/api/moods', payload=payload)


def cmd_delete_mood(args):
    """U: 删除说说。"""
    return _api_request('DELETE', f'/api/moods/{args.mood_id}')


# ---------------------------------------------------------------------------
# 文件上传 API (4)
# ---------------------------------------------------------------------------

def cmd_upload_file(args):
    """V: 上传单个文件。"""
    with open(args.file, 'rb') as f:
        return _api_request('POST', '/api/upload', files={'file': f})


def cmd_upload_files(args):
    """W: 批量上传文件。"""
    opened = [open(fp, 'rb') for fp in args.files]
    try:
        return _api_request('POST', '/api/upload/multiple',
                            files=[('files', f) for f in opened])
    finally:
        for f in opened:
            f.close()


def cmd_list_uploads(args):
    """X: 列出已上传文件。"""
    return _api_request('GET', '/api/uploads/list')


def cmd_delete_upload(args):
    """Y: 删除已上传文件。"""
    return _api_request('DELETE', f'/api/uploads/{args.filename}')


# ---------------------------------------------------------------------------
# 健康检查 API (1)
# ---------------------------------------------------------------------------

def cmd_health_check(args):
    """Z: 健康检查。"""
    return _api_request('GET', '/health')


# ---------------------------------------------------------------------------
# 博客页面 API (2) — 返回 HTML
# ---------------------------------------------------------------------------

def cmd_blog_home(args):
    """AA: 博客首页（HTML）。"""
    params = {'page': args.page}
    if args.lid:
        params['lid'] = args.lid
    if args.keyword:
        params['keyword'] = args.keyword
    return _api_request('GET', '/', params=params, raw=True)


def cmd_blog_article(args):
    """AB: 文章详情页（HTML）。"""
    return _api_request('GET', f'/article/{args.article_id}', raw=True)


# ---------------------------------------------------------------------------
# 后台管理 API (4)
# ---------------------------------------------------------------------------

def cmd_admin_page(args):
    """AC: 后台管理页面（HTML）。"""
    return _api_request('GET', '/admin', raw=True)


def cmd_admin_login(args):
    """AD: 后台登录（获取 token）。"""
    import requests
    base_url = _get_base_url()
    try:
        resp = requests.post(f"{base_url}/admin/login",
                             data={'username': args.username, 'password': args.password},
                             allow_redirects=False, timeout=30)
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)
    token = resp.cookies.get('admin_token', '')
    if token:
        return {"code": 200, "data": {"token": token}, "message": "登录成功"}
    return {"code": 401, "message": "账号或密码错误"}


def cmd_admin_logout(args):
    """AE: 退出后台登录。"""
    return _api_request('GET', f'/admin/logout', params={'t': args.token}, raw=True)


def cmd_admin_delete_articles(args):
    """AF: 后台批量删除文章。"""
    payload = {'ids': [int(i) for i in args.ids], 'token': args.token}
    return _api_request('POST', '/admin/api/delete', payload=payload)


# ---------------------------------------------------------------------------
# Capability list
# ---------------------------------------------------------------------------

_CAPABILITIES = [
    ('list-articles', '分页查询文章列表', 'list-articles [--page N] [--size N] [--lid N] [--keyword TEXT]'),
    ('create-article', '发布新文章', 'create-article --title TEXT --content TEXT [--uid N] [--lid N] [--img URL] [--heat N]'),
    ('get-article', '查询单篇文章详情（含评论）', 'get-article --article-id N'),
    ('update-article', '更新文章', 'update-article --article-id N [--title T] [--content C] [--lid N] [--img U] [--heat N]'),
    ('delete-article', '删除文章（默认软删除）', 'delete-article --article-id N [--hard]'),
    ('restore-article', '恢复软删除的文章', 'restore-article --article-id N'),
    ('top-articles', '获取热门文章 Top N', 'top-articles [--limit N]'),
    ('list-labels', '获取所有标签', 'list-labels'),
    ('create-label', '创建标签', 'create-label --lname TEXT'),
    ('list-users', '获取用户列表', 'list-users'),
    ('create-user', '创建用户', 'create-user --uname TEXT [--phone T] [--pwd T] [--email T] [--img U]'),
    ('create-comment', '发表评论', 'create-comment --uid N --aid N --content TEXT'),
    ('list-comments', '获取文章评论列表', 'list-comments --aid N'),
    ('delete-comment', '删除评论（软删除）', 'delete-comment --comment-id N'),
    ('list-messages', '获取留言列表（含回复）', 'list-messages'),
    ('create-message', '发表留言', 'create-message --uid N --content TEXT'),
    ('reply-message', '回复留言', 'reply-message --uid N --mid N --content TEXT'),
    ('delete-message', '删除留言（软删除）', 'delete-message --message-id N'),
    ('list-moods', '获取说说列表', 'list-moods'),
    ('create-mood', '发布说说', 'create-mood --content TEXT [--title T] [--src U]'),
    ('delete-mood', '删除说说', 'delete-mood --mood-id N'),
    ('upload-file', '上传单个文件', 'upload-file --file PATH'),
    ('upload-files', '批量上传文件', 'upload-files --files PATH [PATH ...]'),
    ('list-uploads', '列出已上传文件', 'list-uploads'),
    ('delete-upload', '删除已上传文件', 'delete-upload --filename NAME'),
    ('health-check', '健康检查', 'health-check'),
    ('blog-home', '博客首页（HTML）', 'blog-home [--page N] [--lid N] [--keyword TEXT]'),
    ('blog-article', '文章详情页（HTML）', 'blog-article --article-id N'),
    ('admin-page', '后台管理页面（HTML）', 'admin-page'),
    ('admin-login', '后台登录（获取 token）', 'admin-login --username T --password T'),
    ('admin-logout', '退出后台登录', 'admin-logout --token T'),
    ('admin-delete-articles', '后台批量删除文章', 'admin-delete-articles --token T --ids N [N ...]'),
]


def cmd_capability_list(args):
    """列出本 skill 所有能力项。"""
    return {
        'capability': 'capability-list',
        'skill': 'blog-mini-kit-mys',
        'version': '1.0.0',
        'endpoint_count': 32,
        'subcommand_count': len(_CAPABILITIES),
        'capabilities': [
            {'name': name, 'description': desc, 'command': cmd}
            for name, desc, cmd in _CAPABILITIES
        ] + [
            {'name': 'capability-list', 'description': '列出本 skill 所有能力项',
             'command': 'capability-list'},
        ],
    }


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_md(payload):
    """将 JSON 输出转为 Markdown 表格（可选）。"""
    if isinstance(payload, str):
        return payload
    cap = payload.get('capability', '') if isinstance(payload, dict) else ''
    if cap == 'capability-list':
        lines = [f"## 能力清单（{payload.get('skill', '')}）", "",
                 f"端点总数: {payload.get('endpoint_count', '')} | 子命令数: {payload.get('subcommand_count', '')}", "",
                 "| 能力 | 说明 | 命令 |", "|---|---|---|"]
        for c in payload.get('capabilities', []):
            lines.append(f"| {c['name']} | {c['description']} | `{c['command']}` |")
        return "\n".join(lines)
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='blog-mini-kit-mys',
        description='管理 Blog System (FastAPI) 全部 32 个 API 端点')

    def add_common_args(p):
        p.add_argument('--format', choices=['json', 'md'], default='json',
                       help='输出格式，默认 json')

    sub = parser.add_subparsers(dest='command', help='能力命令')

    # --- 文章 ---
    p = sub.add_parser('list-articles', help='分页查询文章列表')
    p.add_argument('--page', type=int, default=1, help='页码，默认 1')
    p.add_argument('--size', type=int, default=10, help='每页数量，默认 10')
    p.add_argument('--lid', type=int, default=0, help='标签 ID 筛选，0=不限')
    p.add_argument('--keyword', type=str, default='', help='标题关键词')
    add_common_args(p)

    p = sub.add_parser('create-article', help='发布新文章')
    p.add_argument('--title', required=True, help='文章标题')
    p.add_argument('--content', required=True, help='文章内容')
    p.add_argument('--uid', type=int, default=1, help='作者用户 ID，默认 1')
    p.add_argument('--lid', type=int, default=1, help='标签 ID，默认 1')
    p.add_argument('--img', default=None, help='封面图 URL')
    p.add_argument('--heat', type=int, default=0, help='热度，默认 0')
    add_common_args(p)

    p = sub.add_parser('get-article', help='查询单篇文章详情（含评论）')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    add_common_args(p)

    p = sub.add_parser('update-article', help='更新文章')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    p.add_argument('--title', default=None, help='文章标题')
    p.add_argument('--content', default=None, help='文章内容')
    p.add_argument('--lid', type=int, default=None, help='标签 ID')
    p.add_argument('--img', default=None, help='封面图 URL')
    p.add_argument('--heat', type=int, default=None, help='热度')
    add_common_args(p)

    p = sub.add_parser('delete-article', help='删除文章（默认软删除）')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    p.add_argument('--hard', action='store_true', help='硬删除（默认软删除）')
    add_common_args(p)

    p = sub.add_parser('restore-article', help='恢复软删除的文章')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    add_common_args(p)

    p = sub.add_parser('top-articles', help='获取热门文章 Top N')
    p.add_argument('--limit', type=int, default=5, help='返回数量，默认 5')
    add_common_args(p)

    # --- 标签 ---
    p = sub.add_parser('list-labels', help='获取所有标签')
    add_common_args(p)

    p = sub.add_parser('create-label', help='创建标签')
    p.add_argument('--lname', required=True, help='标签名称')
    add_common_args(p)

    # --- 用户 ---
    p = sub.add_parser('list-users', help='获取用户列表')
    add_common_args(p)

    p = sub.add_parser('create-user', help='创建用户')
    p.add_argument('--uname', required=True, help='用户名')
    p.add_argument('--phone', default='', help='手机号')
    p.add_argument('--pwd', default='', help='密码')
    p.add_argument('--email', default='', help='邮箱')
    p.add_argument('--img', default='img/moren.jpg', help='头像，默认 img/moren.jpg')
    add_common_args(p)

    # --- 评论 ---
    p = sub.add_parser('create-comment', help='发表评论')
    p.add_argument('--uid', type=int, required=True, help='用户 ID')
    p.add_argument('--aid', type=int, required=True, help='文章 ID')
    p.add_argument('--content', required=True, help='评论内容')
    add_common_args(p)

    p = sub.add_parser('list-comments', help='获取文章评论列表')
    p.add_argument('--aid', type=int, required=True, help='文章 ID')
    add_common_args(p)

    p = sub.add_parser('delete-comment', help='删除评论（软删除）')
    p.add_argument('--comment-id', type=int, required=True, help='评论 ID')
    add_common_args(p)

    # --- 留言 ---
    p = sub.add_parser('list-messages', help='获取留言列表（含回复）')
    add_common_args(p)

    p = sub.add_parser('create-message', help='发表留言')
    p.add_argument('--uid', type=int, required=True, help='用户 ID')
    p.add_argument('--content', required=True, help='留言内容')
    add_common_args(p)

    p = sub.add_parser('reply-message', help='回复留言')
    p.add_argument('--uid', type=int, required=True, help='用户 ID')
    p.add_argument('--mid', type=int, required=True, help='留言 ID')
    p.add_argument('--content', required=True, help='回复内容')
    add_common_args(p)

    p = sub.add_parser('delete-message', help='删除留言（软删除）')
    p.add_argument('--message-id', type=int, required=True, help='留言 ID')
    add_common_args(p)

    # --- 说说 ---
    p = sub.add_parser('list-moods', help='获取说说列表')
    add_common_args(p)

    p = sub.add_parser('create-mood', help='发布说说')
    p.add_argument('--content', required=True, help='说说内容')
    p.add_argument('--title', default='', help='标题')
    p.add_argument('--src', default='', help='媒体 URL')
    add_common_args(p)

    p = sub.add_parser('delete-mood', help='删除说说')
    p.add_argument('--mood-id', type=int, required=True, help='说说 ID')
    add_common_args(p)

    # --- 文件上传 ---
    p = sub.add_parser('upload-file', help='上传单个文件')
    p.add_argument('--file', required=True, help='文件路径')
    add_common_args(p)

    p = sub.add_parser('upload-files', help='批量上传文件')
    p.add_argument('--files', required=True, nargs='+', help='文件路径列表')
    add_common_args(p)

    p = sub.add_parser('list-uploads', help='列出已上传文件')
    add_common_args(p)

    p = sub.add_parser('delete-upload', help='删除已上传文件')
    p.add_argument('--filename', required=True, help='文件名')
    add_common_args(p)

    # --- 健康检查 ---
    p = sub.add_parser('health-check', help='健康检查')
    add_common_args(p)

    # --- 博客页面 ---
    p = sub.add_parser('blog-home', help='博客首页（HTML）')
    p.add_argument('--page', type=int, default=1, help='页码')
    p.add_argument('--lid', type=int, default=0, help='标签 ID 筛选')
    p.add_argument('--keyword', type=str, default='', help='标题关键词')
    add_common_args(p)

    p = sub.add_parser('blog-article', help='文章详情页（HTML）')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    add_common_args(p)

    # --- 后台管理 ---
    p = sub.add_parser('admin-page', help='后台管理页面（HTML）')
    add_common_args(p)

    p = sub.add_parser('admin-login', help='后台登录（获取 token）')
    p.add_argument('--username', required=True, help='账号（默认 admin）')
    p.add_argument('--password', required=True, help='密码（默认 admin）')
    add_common_args(p)

    p = sub.add_parser('admin-logout', help='退出后台登录')
    p.add_argument('--token', required=True, help='登录 token')
    add_common_args(p)

    p = sub.add_parser('admin-delete-articles', help='后台批量删除文章')
    p.add_argument('--token', required=True, help='登录 token')
    p.add_argument('--ids', required=True, nargs='+', help='文章 ID 列表')
    add_common_args(p)

    # --- capability-list ---
    p = sub.add_parser('capability-list', help='列出本 skill 所有能力项')
    add_common_args(p)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(2)

    dispatch = {
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
        'create-comment': cmd_create_comment,
        'list-comments': cmd_list_comments,
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
        'blog-home': cmd_blog_home,
        'blog-article': cmd_blog_article,
        'admin-page': cmd_admin_page,
        'admin-login': cmd_admin_login,
        'admin-logout': cmd_admin_logout,
        'admin-delete-articles': cmd_admin_delete_articles,
        'capability-list': cmd_capability_list,
    }

    handler = dispatch.get(args.command)
    if handler is None:
        print(f"错误：未知命令 {args.command}", file=sys.stderr)
        sys.exit(2)

    try:
        payload = handler(args)
        if args.format == 'md':
            print(render_md(payload))
        else:
            if isinstance(payload, str):
                print(payload)
            else:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
    except SystemExit:
        raise
    except Exception as exc:
        print(f"错误：{exc}", file=sys.stderr)
        sys.exit(4)


if __name__ == '__main__':
    main()
