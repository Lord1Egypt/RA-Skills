#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-mini-ljt — 博客系统 API 管理 skill（8 模块 28 端点）

能力（由 API 文档解析生成）:
  A. health-check — 检查 API 可达性
  B. list-articles — 分页查询文章列表
  C. get-article — 查询单篇文章详情（含评论）
  D. top-articles — 获取热门文章 Top N
  E. create-article — 发布新文章
  F. update-article — 更新文章
  G. delete-article — 删除文章（默认软删除）
  H. restore-article — 恢复软删除的文章
  I. create-comment — 发表评论
  J. list-comments — 获取文章评论列表
  K. delete-comment — 删除评论（软删除）
  L. list-labels — 获取所有标签（端点实际路径 /api/lables）
  M. create-label — 创建标签（端点实际路径 /api/lables）
  N. list-messages — 获取留言列表（含回复）
  O. create-message — 发表留言
  P. reply-message — 回复留言
  Q. delete-message — 删除留言（软删除）
  R. list-moods — 获取说说列表
  S. create-mood — 发布说说
  T. delete-mood — 删除说说
  U. upload-file — 上传单个文件（图片/视频/文档）
  V. upload-files — 批量上传文件
  W. list-uploads — 列出所有已上传文件
  X. delete-upload — 删除已上传文件
  Y. list-users — 获取用户列表
  Z. create-user — 创建用户
  AA. admin-login — 后台登录（返回 token）
  AB. admin-logout — 退出登录
  AC. admin-delete-articles — 后台批量删除文章
  AD. capability-list — 列出本 skill 所有能力项

认证: none（无认证，公开 API）
退出码: 0=成功; 2=参数错误; 3=缺少配置（地址）; 4=API 调用失败
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Credentials（前缀由 skill name 推导，认证方式为 none）
# ---------------------------------------------------------------------------

_CRED_PREFIX = "BLOG_MINI_LJT"  # skill name 转大写下划线
_AUTH_TYPE = "none"             # 无认证（公开 API）

# 无认证公开 API，内置默认地址——无配置即可用（可被环境变量/项目知识覆盖）
_DEFAULT_BASE_URL = "http://121.36.13.125"


def _load_from_project_knowledge():
    """从 .project-info/ 目录递归查找 JSON 配置文件，读取 config.{PREFIX}_BASE_URL。

    不固定文件名——扫描所有 .json 文件，检查是否含 config 字段。
    .project-info/ 由 grape worker 物化到 agent 工作目录（cwd）下，直接在当前目录查找。
    base_url 严格按 {PREFIX}_ 前缀精确匹配，不做 fallback。
    """
    import glob
    creds = {}
    for filepath in glob.glob('.project-info/**/*.json', recursive=True):
        try:
            with open(filepath) as f:
                data = json.load(f)
            config = data.get('config', {})
            prefix = _CRED_PREFIX + '_'
            for key, val in config.items():
                if key.upper() == (prefix + 'BASE_URL'):
                    creds.setdefault('base_url', val)
                    break
        except Exception:
            continue
    return creds


def _load_credentials():
    """获取配置——4 级优先级（与 base_url 一致）。

    1. 项目知识：递归扫描 .project-info/ 下所有 JSON 文件（config.{PREFIX}_BASE_URL）
    2. 环境变量：扫描 {PREFIX}_* 开头变量（项目知识缺失时回退）
    3. 当前上下文：A2A context 已注入的环境变量（已包含在步骤 2）
    4. 内置默认地址（无认证公开 API，无配置即可用）
    """
    creds = {}
    # 1. 项目知识优先
    creds.update(_load_from_project_knowledge())
    # 2. 环境变量回退
    for k, v in os.environ.items():
        u = k.upper()
        if u.startswith(_CRED_PREFIX) and 'BASE_URL' in u:
            creds.setdefault('base_url', v)
    return creds


def _get_base_url():
    """获取 API base URL——4 级优先级，无配置时使用内置默认地址。"""
    creds = _load_credentials()
    base_url = creds.get('base_url', '').rstrip('/')
    if not base_url:
        base_url = _DEFAULT_BASE_URL
    return base_url


# ---------------------------------------------------------------------------
# API client（无认证）
# ---------------------------------------------------------------------------

def _build_auth(creds):
    """根据认证方式构建请求认证参数（无认证返回空 dict）。"""
    return {}


def _api_request(method, path, payload=None, params=None, files=None):
    """调用目标系统 REST API（无认证）。"""
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
        if resp.content:
            try:
                return resp.json()
            except ValueError:
                return {"status": "ok", "http_code": resp.status_code}
        return {}
    except requests.exceptions.HTTPError as e:
        print(f"错误：API 调用失败 {resp.status_code}: {e}", file=sys.stderr)
        sys.exit(4)
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)


# ---------------------------------------------------------------------------
# Subcommand implementations
# ---------------------------------------------------------------------------

def cmd_health_check(args):
    """能力 A：检查 API 可达性"""
    result = _api_request('GET', '/health')
    return result


def cmd_list_articles(args):
    """能力 B：分页查询文章列表"""
    params = {'page': args.page, 'size': args.size}
    if args.lid:
        params['lid'] = args.lid
    if args.keyword:
        params['keyword'] = args.keyword
    return _api_request('GET', '/api/articles', params=params)


def cmd_get_article(args):
    """能力 C：查询单篇文章详情（含评论）"""
    return _api_request('GET', f'/api/articles/{args.id}')


def cmd_top_articles(args):
    """能力 D：获取热门文章 Top N"""
    return _api_request('GET', '/api/articles/heat/top', params={'limit': args.limit})


def cmd_create_article(args):
    """能力 E：发布新文章"""
    payload = {'title': args.title, 'content': args.content}
    if args.uid is not None:
        payload['uid'] = args.uid
    if args.lid is not None:
        payload['lid'] = args.lid
    if args.img is not None:
        payload['img'] = args.img
    if args.heat is not None:
        payload['heat'] = args.heat
    return _api_request('POST', '/api/articles', payload=payload)


def cmd_update_article(args):
    """能力 F：更新文章"""
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
    return _api_request('PUT', f'/api/articles/{args.id}', payload=payload)


def cmd_delete_article(args):
    """能力 G：删除文章（默认软删除）"""
    params = {'soft': 'true' if args.soft else 'false'}
    return _api_request('DELETE', f'/api/articles/{args.id}', params=params)


def cmd_restore_article(args):
    """能力 H：恢复软删除的文章"""
    return _api_request('POST', f'/api/articles/{args.id}/restore')


def cmd_create_comment(args):
    """能力 I：发表评论"""
    payload = {'uid': args.uid, 'aid': args.aid, 'content': args.content}
    return _api_request('POST', '/api/comments', payload=payload)


def cmd_list_comments(args):
    """能力 J：获取文章评论列表"""
    return _api_request('GET', f'/api/comments/{args.aid}')


def cmd_delete_comment(args):
    """能力 K：删除评论（软删除）"""
    return _api_request('DELETE', f'/api/comments/{args.id}')


def cmd_list_labels(args):
    """能力 L：获取所有标签（端点实际路径 /api/lables）"""
    return _api_request('GET', '/api/lables')


def cmd_create_label(args):
    """能力 M：创建标签（端点实际路径 /api/lables）"""
    payload = {'lname': args.lname}
    return _api_request('POST', '/api/lables', payload=payload)


def cmd_list_messages(args):
    """能力 N：获取留言列表（含回复）"""
    return _api_request('GET', '/api/messages')


def cmd_create_message(args):
    """能力 O：发表留言"""
    payload = {'uid': args.uid, 'content': args.content}
    return _api_request('POST', '/api/messages', payload=payload)


def cmd_reply_message(args):
    """能力 P：回复留言"""
    payload = {'uid': args.uid, 'mid': args.mid, 'content': args.content}
    return _api_request('POST', '/api/messages/reply', payload=payload)


def cmd_delete_message(args):
    """能力 Q：删除留言（软删除）"""
    return _api_request('DELETE', f'/api/messages/{args.id}')


def cmd_list_moods(args):
    """能力 R：获取说说列表"""
    return _api_request('GET', '/api/moods')


def cmd_create_mood(args):
    """能力 S：发布说说"""
    payload = {'content': args.content}
    if args.title is not None:
        payload['title'] = args.title
    if args.src is not None:
        payload['src'] = args.src
    return _api_request('POST', '/api/moods', payload=payload)


def cmd_delete_mood(args):
    """能力 T：删除说说"""
    return _api_request('DELETE', f'/api/moods/{args.id}')


def cmd_upload_file(args):
    """能力 U：上传单个文件（图片/视频/文档）"""
    with open(args.filepath, 'rb') as f:
        return _api_request('POST', '/api/upload', files={'file': f})


def cmd_upload_files(args):
    """能力 V：批量上传文件"""
    opened = [open(fp, 'rb') for fp in args.filepaths]
    try:
        return _api_request('POST', '/api/upload/multiple',
                            files=[('files', f) for f in opened])
    finally:
        for f in opened:
            f.close()


def cmd_list_uploads(args):
    """能力 W：列出所有已上传文件"""
    return _api_request('GET', '/api/uploads/list')


def cmd_delete_upload(args):
    """能力 X：删除已上传文件"""
    return _api_request('DELETE', f'/api/uploads/{args.filename}')


def cmd_list_users(args):
    """能力 Y：获取用户列表"""
    return _api_request('GET', '/api/users')


def cmd_create_user(args):
    """能力 Z：创建用户"""
    payload = {'uname': args.uname}
    if args.phone is not None:
        payload['phone'] = args.phone
    if args.pwd is not None:
        payload['pwd'] = args.pwd
    if args.email is not None:
        payload['email'] = args.email
    if args.img is not None:
        payload['img'] = args.img
    return _api_request('POST', '/api/users', payload=payload)


def cmd_admin_login(args):
    """能力 AA：后台登录（form 表单，返回 token）"""
    import requests
    base_url = _get_base_url()
    url = f"{base_url}/admin/login"
    form_data = {'username': args.username, 'password': args.password}
    try:
        resp = requests.post(url, data=form_data, allow_redirects=False, timeout=30)
        token = resp.cookies.get('admin_token', '')
        if token:
            return {"code": 200, "data": {"token": token}, "message": "登录成功"}
        if resp.status_code == 200 and 'login-error' in resp.text:
            return {"code": 401, "message": "账号或密码错误"}
        return {"code": resp.status_code, "message": "登录异常"}
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)


def cmd_admin_logout(args):
    """能力 AB：退出登录"""
    import requests
    base_url = _get_base_url()
    url = f"{base_url}/admin/logout"
    try:
        requests.get(url, params={'t': args.token}, allow_redirects=False, timeout=30)
        return {"code": 200, "message": "已退出登录"}
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)


def cmd_admin_delete_articles(args):
    """能力 AC：后台批量删除文章"""
    payload = {'token': args.token, 'ids': args.ids}
    return _api_request('POST', '/admin/api/delete', payload=payload)


# ---------------------------------------------------------------------------
# Capability list
# ---------------------------------------------------------------------------

_CAPABILITIES = [
    {'name': 'health-check', 'description': '检查 API 可达性', 'command': 'health-check'},
    {'name': 'list-articles', 'description': '分页查询文章列表', 'command': 'list-articles [--page 1] [--size 10] [--lid 0] [--keyword ""]'},
    {'name': 'get-article', 'description': '查询单篇文章详情（含评论）', 'command': 'get-article --id <id>'},
    {'name': 'top-articles', 'description': '获取热门文章 Top N', 'command': 'top-articles [--limit 5]'},
    {'name': 'create-article', 'description': '发布新文章', 'command': 'create-article --title <t> --content <c> [--uid 1] [--lid 1] [--img url] [--heat 0]'},
    {'name': 'update-article', 'description': '更新文章', 'command': 'update-article --id <id> [--title t] [--content c] [--lid n] [--img url] [--heat n]'},
    {'name': 'delete-article', 'description': '删除文章（默认软删除）', 'command': 'delete-article --id <id> [--soft true]'},
    {'name': 'restore-article', 'description': '恢复软删除的文章', 'command': 'restore-article --id <id>'},
    {'name': 'create-comment', 'description': '发表评论', 'command': 'create-comment --uid <uid> --aid <aid> --content <c>'},
    {'name': 'list-comments', 'description': '获取文章评论列表', 'command': 'list-comments --aid <aid>'},
    {'name': 'delete-comment', 'description': '删除评论（软删除）', 'command': 'delete-comment --id <id>'},
    {'name': 'list-labels', 'description': '获取所有标签（端点实际路径 /api/lables）', 'command': 'list-labels'},
    {'name': 'create-label', 'description': '创建标签（端点实际路径 /api/lables）', 'command': 'create-label --lname <name>'},
    {'name': 'list-messages', 'description': '获取留言列表（含回复）', 'command': 'list-messages'},
    {'name': 'create-message', 'description': '发表留言', 'command': 'create-message --uid <uid> --content <c>'},
    {'name': 'reply-message', 'description': '回复留言', 'command': 'reply-message --uid <uid> --mid <mid> --content <c>'},
    {'name': 'delete-message', 'description': '删除留言（软删除）', 'command': 'delete-message --id <id>'},
    {'name': 'list-moods', 'description': '获取说说列表', 'command': 'list-moods'},
    {'name': 'create-mood', 'description': '发布说说', 'command': 'create-mood --content <c> [--title ""] [--src ""]'},
    {'name': 'delete-mood', 'description': '删除说说', 'command': 'delete-mood --id <id>'},
    {'name': 'upload-file', 'description': '上传单个文件', 'command': 'upload-file --filepath <path>'},
    {'name': 'upload-files', 'description': '批量上传文件', 'command': 'upload-files --filepaths <p1> <p2> ...'},
    {'name': 'list-uploads', 'description': '列出所有已上传文件', 'command': 'list-uploads'},
    {'name': 'delete-upload', 'description': '删除已上传文件', 'command': 'delete-upload --filename <name>'},
    {'name': 'list-users', 'description': '获取用户列表', 'command': 'list-users'},
    {'name': 'create-user', 'description': '创建用户', 'command': 'create-user --uname <name> [--phone ""] [--pwd ""] [--email ""] [--img ""]'},
    {'name': 'admin-login', 'description': '后台登录（返回 token）', 'command': 'admin-login --username <u> --password <p>'},
    {'name': 'admin-logout', 'description': '退出登录', 'command': 'admin-logout --token <t>'},
    {'name': 'admin-delete-articles', 'description': '后台批量删除文章', 'command': 'admin-delete-articles --token <t> --ids <id1> <id2> ...'},
    {'name': 'capability-list', 'description': '列出本 skill 所有能力项', 'command': 'capability-list'},
]


def cmd_capability_list(args):
    """能力 AD：列出本 skill 所有能力项。"""
    return {
        'capability': 'capability-list',
        'skill': 'blog-mini-ljt',
        'version': '1.0.0',
        'auth_type': 'none',
        'endpoint_count': 28,
        'subcommand_count': len(_CAPABILITIES),
        'capabilities': _CAPABILITIES,
    }


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_md(payload):
    """将 JSON 输出转为 Markdown 表格（可选）。"""
    cap = payload.get('capability', '')
    if cap == 'capability-list':
        lines = [f"## 能力清单（{payload.get('skill', '')} v{payload.get('version', '')}）", "",
                 f"认证方式：{payload.get('auth_type', 'none')} | 端点数：{payload.get('endpoint_count', 0)} | 子命令数：{payload.get('subcommand_count', 0)}", "",
                 "| # | 能力 | 说明 | 命令 |", "|---|---|---|---|"]
        for i, c in enumerate(payload.get('capabilities', []), 1):
            lines.append(f"| {i} | {c['name']} | {c['description']} | `{c['command']}` |")
        return "\n".join(lines)
    data = payload.get('data')
    if isinstance(data, list) and data:
        cols = list(data[0].keys())
        lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        for row in data[:50]:
            lines.append("| " + " | ".join(str(row.get(c, '')) for c in cols) + " |")
        if len(data) > 50:
            lines.append(f"\n*共 {len(data)} 条，仅显示前 50 条*")
        return "\n".join(lines)
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='blog-mini-ljt',
        description='博客系统 API 管理 skill（8 模块 28 端点，无认证）')

    def add_common_args(p):
        p.add_argument('--format', choices=['json', 'md'], default='json',
                       help='输出格式，默认 json')

    sub = parser.add_subparsers(dest='command', help='能力命令')

    # A. health-check
    p = sub.add_parser('health-check', help='检查 API 可达性')
    add_common_args(p)

    # B. list-articles
    p = sub.add_parser('list-articles', help='分页查询文章列表')
    p.add_argument('--page', type=int, default=1, help='页码，默认 1')
    p.add_argument('--size', type=int, default=10, help='每页条数，默认 10')
    p.add_argument('--lid', type=int, default=0, help='按标签 ID 筛选，0=不筛选')
    p.add_argument('--keyword', default='', help='标题关键词搜索')
    add_common_args(p)

    # C. get-article
    p = sub.add_parser('get-article', help='查询单篇文章详情（含评论）')
    p.add_argument('--id', type=int, required=True, help='文章 ID')
    add_common_args(p)

    # D. top-articles
    p = sub.add_parser('top-articles', help='获取热门文章 Top N')
    p.add_argument('--limit', type=int, default=5, help='返回条数，默认 5（1-20）')
    add_common_args(p)

    # E. create-article
    p = sub.add_parser('create-article', help='发布新文章')
    p.add_argument('--title', required=True, help='文章标题（必填）')
    p.add_argument('--content', required=True, help='文章内容（必填）')
    p.add_argument('--uid', type=int, default=None, help='作者用户 ID，默认 1')
    p.add_argument('--lid', type=int, default=None, help='标签 ID，默认 1')
    p.add_argument('--img', default=None, help='封面图 URL')
    p.add_argument('--heat', type=int, default=None, help='热度初始值，默认 0')
    add_common_args(p)

    # F. update-article
    p = sub.add_parser('update-article', help='更新文章')
    p.add_argument('--id', type=int, required=True, help='文章 ID')
    p.add_argument('--title', default=None, help='新标题')
    p.add_argument('--content', default=None, help='新内容')
    p.add_argument('--lid', type=int, default=None, help='新标签 ID')
    p.add_argument('--img', default=None, help='新封面图 URL')
    p.add_argument('--heat', type=int, default=None, help='新热度值')
    add_common_args(p)

    # G. delete-article
    p = sub.add_parser('delete-article', help='删除文章（默认软删除）')
    p.add_argument('--id', type=int, required=True, help='文章 ID')
    p.add_argument('--soft', type=lambda x: str(x).lower() == 'true', default=True,
                   help='是否软删除，默认 true（false=硬删除）')
    add_common_args(p)

    # H. restore-article
    p = sub.add_parser('restore-article', help='恢复软删除的文章')
    p.add_argument('--id', type=int, required=True, help='文章 ID')
    add_common_args(p)

    # I. create-comment
    p = sub.add_parser('create-comment', help='发表评论')
    p.add_argument('--uid', type=int, required=True, help='评论者用户 ID（必填）')
    p.add_argument('--aid', type=int, required=True, help='文章 ID（必填）')
    p.add_argument('--content', required=True, help='评论内容（必填）')
    add_common_args(p)

    # J. list-comments
    p = sub.add_parser('list-comments', help='获取文章评论列表')
    p.add_argument('--aid', type=int, required=True, help='文章 ID')
    add_common_args(p)

    # K. delete-comment
    p = sub.add_parser('delete-comment', help='删除评论（软删除）')
    p.add_argument('--id', type=int, required=True, help='评论 ID')
    add_common_args(p)

    # L. list-labels
    p = sub.add_parser('list-labels', help='获取所有标签（端点实际路径 /api/lables）')
    add_common_args(p)

    # M. create-label
    p = sub.add_parser('create-label', help='创建标签（端点实际路径 /api/lables）')
    p.add_argument('--lname', required=True, help='标签名称（必填）')
    add_common_args(p)

    # N. list-messages
    p = sub.add_parser('list-messages', help='获取留言列表（含回复）')
    add_common_args(p)

    # O. create-message
    p = sub.add_parser('create-message', help='发表留言')
    p.add_argument('--uid', type=int, required=True, help='留言者用户 ID（必填）')
    p.add_argument('--content', required=True, help='留言内容（必填）')
    add_common_args(p)

    # P. reply-message
    p = sub.add_parser('reply-message', help='回复留言')
    p.add_argument('--uid', type=int, required=True, help='回复者用户 ID（必填）')
    p.add_argument('--mid', type=int, required=True, help='被回复的留言 ID（必填）')
    p.add_argument('--content', required=True, help='回复内容（必填）')
    add_common_args(p)

    # Q. delete-message
    p = sub.add_parser('delete-message', help='删除留言（软删除）')
    p.add_argument('--id', type=int, required=True, help='留言 ID')
    add_common_args(p)

    # R. list-moods
    p = sub.add_parser('list-moods', help='获取说说列表')
    add_common_args(p)

    # S. create-mood
    p = sub.add_parser('create-mood', help='发布说说')
    p.add_argument('--content', required=True, help='说说内容（必填）')
    p.add_argument('--title', default=None, help='标题，默认空')
    p.add_argument('--src', default=None, help='来源/配图 URL，默认空')
    add_common_args(p)

    # T. delete-mood
    p = sub.add_parser('delete-mood', help='删除说说')
    p.add_argument('--id', type=int, required=True, help='说说 ID')
    add_common_args(p)

    # U. upload-file
    p = sub.add_parser('upload-file', help='上传单个文件（图片/视频/文档）')
    p.add_argument('--filepath', required=True, help='本地文件路径（必填）')
    add_common_args(p)

    # V. upload-files
    p = sub.add_parser('upload-files', help='批量上传文件')
    p.add_argument('--filepaths', required=True, nargs='+', help='本地文件路径列表（必填，空格分隔）')
    add_common_args(p)

    # W. list-uploads
    p = sub.add_parser('list-uploads', help='列出所有已上传文件')
    add_common_args(p)

    # X. delete-upload
    p = sub.add_parser('delete-upload', help='删除已上传文件')
    p.add_argument('--filename', required=True, help='文件名（必填）')
    add_common_args(p)

    # Y. list-users
    p = sub.add_parser('list-users', help='获取用户列表')
    add_common_args(p)

    # Z. create-user
    p = sub.add_parser('create-user', help='创建用户')
    p.add_argument('--uname', required=True, help='用户名（必填）')
    p.add_argument('--phone', default=None, help='手机号，默认空')
    p.add_argument('--pwd', default=None, help='密码，默认空')
    p.add_argument('--email', default=None, help='邮箱，默认空')
    p.add_argument('--img', default=None, help='头像 URL，默认 img/moren.jpg')
    add_common_args(p)

    # AA. admin-login
    p = sub.add_parser('admin-login', help='后台登录（返回 token）')
    p.add_argument('--username', required=True, help='管理员账号（必填）')
    p.add_argument('--password', required=True, help='管理员密码（必填）')
    add_common_args(p)

    # AB. admin-logout
    p = sub.add_parser('admin-logout', help='退出登录')
    p.add_argument('--token', required=True, help='登录 token（必填）')
    add_common_args(p)

    # AC. admin-delete-articles
    p = sub.add_parser('admin-delete-articles', help='后台批量删除文章')
    p.add_argument('--token', required=True, help='登录 token（必填）')
    p.add_argument('--ids', required=True, nargs='+', type=int, help='文章 ID 列表（必填）')
    add_common_args(p)

    # AD. capability-list
    p = sub.add_parser('capability-list', help='列出本 skill 所有能力项')
    add_common_args(p)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(2)

    dispatch = {
        'health-check': cmd_health_check,
        'list-articles': cmd_list_articles,
        'get-article': cmd_get_article,
        'top-articles': cmd_top_articles,
        'create-article': cmd_create_article,
        'update-article': cmd_update_article,
        'delete-article': cmd_delete_article,
        'restore-article': cmd_restore_article,
        'create-comment': cmd_create_comment,
        'list-comments': cmd_list_comments,
        'delete-comment': cmd_delete_comment,
        'list-labels': cmd_list_labels,
        'create-label': cmd_create_label,
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
        'list-users': cmd_list_users,
        'create-user': cmd_create_user,
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
            print(json.dumps(payload, ensure_ascii=False, indent=2))
    except SystemExit:
        raise
    except Exception as exc:
        print(f"错误：{exc}", file=sys.stderr)
        sys.exit(4)


if __name__ == '__main__':
    main()
