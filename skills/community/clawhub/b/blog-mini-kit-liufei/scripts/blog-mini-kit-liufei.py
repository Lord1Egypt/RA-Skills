#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-mini-kit-liufei — 博客系统(FastAPI) API 管理 skill

能力（由 API 文档解析生成，共 28 个子命令 + capability-list）:
  A. health-check — 健康检查
  B. list-articles — 分页查询文章列表
  C. get-article — 查询单篇文章详情（含评论）
  D. create-article — 发布新文章
  E. update-article — 更新文章
  F. delete-article — 删除文章（支持软删/硬删）
  G. restore-article — 恢复软删除的文章
  H. top-articles — 获取热门文章 Top N
  I. list-lables — 获取所有标签
  J. create-lable — 创建标签
  K. list-users — 获取用户列表
  L. create-user — 创建用户
  M. create-comment — 发表评论
  N. list-comments — 获取文章的评论列表
  O. delete-comment — 删除评论（软删除）
  P. list-messages — 获取留言列表（含回复）
  Q. create-message — 发表留言
  R. reply-message — 回复留言
  S. delete-message — 删除留言（软删除）
  T. list-moods — 获取说说列表
  U. create-mood — 发布说说
  V. delete-mood — 删除说说
  W. upload-file — 上传单个文件
  X. upload-files — 批量上传文件
  Y. list-uploads — 列出所有已上传文件
  Z. delete-upload — 删除已上传文件
  AA. admin-login — 后台登录获取 token
  BB. admin-delete-articles — 后台批量删除文章

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

_CRED_PREFIX = "BLOG_MINI_KIT_LIUFEI"
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
            if 'BASE_URL' in u:
                creds.setdefault('base_url', v)
    return creds


def _load_from_project_knowledge():
    """从 .project-info/ 目录递归查找 JSON 配置文件，读取 config.{PREFIX}_BASE_URL。

    不固定文件名——扫描所有 .json 文件，检查是否含 config 字段。
    base_url 严格按 {PREFIX}_ 前缀精确匹配。
    """
    import glob
    creds = {}
    for filepath in glob.glob('.project-info/**/*.json', recursive=True):
        try:
            with open(filepath) as f:
                data = json.load(f)
            config = data.get('config', {})
            prefix = _CRED_PREFIX + '_'
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
        print("提示：可通过 export %s_BASE_URL=\"%s\" 永久设置。" % (_CRED_PREFIX, base_url))
    return base_url


# ---------------------------------------------------------------------------
# API client（无认证模式）
# ---------------------------------------------------------------------------

def _build_auth(creds):
    """根据认证方式构建请求认证参数。无认证返回空 dict。"""
    return {}


def _api_request(method, path, payload=None, params=None, files=None):
    """调用目标系统 REST API。"""
    import requests

    base_url = _get_base_url()
    creds = _load_credentials()
    auth_result = _build_auth(creds)

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
            if files:
                resp = requests.post(url, files=files, timeout=30, **auth_kwargs)
            else:
                resp = requests.post(url, json=payload, timeout=30, **auth_kwargs)
        elif method == 'PUT':
            resp = requests.put(url, json=payload, timeout=30, **auth_kwargs)
        elif method == 'PATCH':
            resp = requests.patch(url, json=payload, timeout=30, **auth_kwargs)
        elif method == 'DELETE':
            resp = requests.delete(url, params=params, timeout=30, **auth_kwargs)
        else:
            print(f"错误：不支持的方法 {method}", file=sys.stderr)
            sys.exit(2)

        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return {}
    except requests.exceptions.HTTPError as e:
        print(f"错误：API 调用失败 {resp.status_code}: {e}", file=sys.stderr)
        sys.exit(4)
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)
    except ValueError:
        print("错误：API 返回非 JSON 格式（可能返回 HTML 错误页）", file=sys.stderr)
        sys.exit(4)


# ---------------------------------------------------------------------------
# Subcommand implementations
# ---------------------------------------------------------------------------

def cmd_health_check(args):
    """能力 A：健康检查"""
    return _api_request('GET', '/health')


def cmd_list_articles(args):
    """能力 B：分页查询文章列表"""
    params = {
        'page': args.page,
        'size': args.size,
        'lid': args.lid,
        'keyword': args.keyword,
    }
    return _api_request('GET', '/api/articles', params=params)


def cmd_get_article(args):
    """能力 C：查询单篇文章详情（含评论）"""
    return _api_request('GET', f'/api/articles/{args.article_id}')


def cmd_create_article(args):
    """能力 D：发布新文章"""
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


def cmd_update_article(args):
    """能力 E：更新文章"""
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
    if not payload:
        print("错误：至少指定一个要更新的字段", file=sys.stderr)
        sys.exit(2)
    return _api_request('PUT', f'/api/articles/{args.article_id}', payload=payload)


def cmd_delete_article(args):
    """能力 F：删除文章（支持软删/硬删）"""
    params = {'soft': 'false' if args.hard else 'true'}
    return _api_request('DELETE', f'/api/articles/{args.article_id}', params=params)


def cmd_restore_article(args):
    """能力 G：恢复软删除的文章"""
    return _api_request('POST', f'/api/articles/{args.article_id}/restore')


def cmd_top_articles(args):
    """能力 H：获取热门文章 Top N"""
    params = {'limit': args.limit}
    return _api_request('GET', '/api/articles/heat/top', params=params)


def cmd_list_lables(args):
    """能力 I：获取所有标签"""
    return _api_request('GET', '/api/lables')


def cmd_create_lable(args):
    """能力 J：创建标签"""
    payload = {'lname': args.lname}
    return _api_request('POST', '/api/lables', payload=payload)


def cmd_list_users(args):
    """能力 K：获取用户列表"""
    return _api_request('GET', '/api/users')


def cmd_create_user(args):
    """能力 L：创建用户"""
    payload = {
        'uname': args.uname,
        'phone': args.phone,
        'pwd': args.pwd,
        'email': args.email,
        'img': args.img,
    }
    return _api_request('POST', '/api/users', payload=payload)


def cmd_create_comment(args):
    """能力 M：发表评论"""
    payload = {
        'uid': args.uid,
        'aid': args.aid,
        'content': args.content,
    }
    return _api_request('POST', '/api/comments', payload=payload)


def cmd_list_comments(args):
    """能力 N：获取文章的评论列表"""
    return _api_request('GET', f'/api/comments/{args.aid}')


def cmd_delete_comment(args):
    """能力 O：删除评论（软删除）"""
    return _api_request('DELETE', f'/api/comments/{args.comment_id}')


def cmd_list_messages(args):
    """能力 P：获取留言列表（含回复）"""
    return _api_request('GET', '/api/messages')


def cmd_create_message(args):
    """能力 Q：发表留言"""
    payload = {
        'uid': args.uid,
        'content': args.content,
    }
    return _api_request('POST', '/api/messages', payload=payload)


def cmd_reply_message(args):
    """能力 R：回复留言"""
    payload = {
        'uid': args.uid,
        'mid': args.mid,
        'content': args.content,
    }
    return _api_request('POST', '/api/messages/reply', payload=payload)


def cmd_delete_message(args):
    """能力 S：删除留言（软删除）"""
    return _api_request('DELETE', f'/api/messages/{args.message_id}')


def cmd_list_moods(args):
    """能力 T：获取说说列表"""
    return _api_request('GET', '/api/moods')


def cmd_create_mood(args):
    """能力 U：发布说说"""
    payload = {
        'title': args.title,
        'content': args.content,
        'src': args.src,
    }
    return _api_request('POST', '/api/moods', payload=payload)


def cmd_delete_mood(args):
    """能力 V：删除说说"""
    return _api_request('DELETE', f'/api/moods/{args.mood_id}')


def cmd_upload_file(args):
    """能力 W：上传单个文件"""
    with open(args.filepath, 'rb') as f:
        return _api_request('POST', '/api/upload', files={'file': f})


def cmd_upload_files(args):
    """能力 X：批量上传文件"""
    files = [open(fp, 'rb') for fp in args.filepaths]
    try:
        return _api_request('POST', '/api/upload/multiple',
                            files=[('files', f) for f in files])
    finally:
        for f in files:
            f.close()


def cmd_list_uploads(args):
    """能力 Y：列出所有已上传文件"""
    return _api_request('GET', '/api/uploads/list')


def cmd_delete_upload(args):
    """能力 Z：删除已上传文件"""
    return _api_request('DELETE', f'/api/uploads/{args.filename}')


def cmd_admin_login(args):
    """能力 AA：后台登录获取 token"""
    import requests
    base_url = _get_base_url()
    url = f"{base_url}/admin/login"
    try:
        resp = requests.post(url, data={
            'username': args.username,
            'password': args.password,
        }, timeout=30, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)
    token = resp.cookies.get('admin_token', '')
    if not token:
        print("错误：登录失败，未获取到 admin_token", file=sys.stderr)
        sys.exit(4)
    return {'code': 200, 'data': {'token': token}}


def cmd_admin_delete_articles(args):
    """能力 BB：后台批量删除文章"""
    payload = {
        'ids': args.ids,
        'token': args.token,
    }
    return _api_request('POST', '/admin/api/delete', payload=payload)


# ---------------------------------------------------------------------------
# Capability list
# ---------------------------------------------------------------------------

def cmd_capability_list(args):
    """列出本 skill 所有能力项。"""
    caps = [
        {'name': 'health-check', 'description': '健康检查',
         'command': 'health-check'},
        {'name': 'list-articles', 'description': '分页查询文章列表',
         'command': 'list-articles [--page N] [--size N] [--lid N] [--keyword TEXT]'},
        {'name': 'get-article', 'description': '查询单篇文章详情（含评论）',
         'command': 'get-article --article-id N'},
        {'name': 'create-article', 'description': '发布新文章',
         'command': 'create-article --title TEXT --content TEXT [--uid N] [--lid N] [--img URL] [--heat N]'},
        {'name': 'update-article', 'description': '更新文章',
         'command': 'update-article --article-id N [--title T] [--content T] [--lid N] [--img URL] [--heat N]'},
        {'name': 'delete-article', 'description': '删除文章（支持软删/硬删）',
         'command': 'delete-article --article-id N [--hard]'},
        {'name': 'restore-article', 'description': '恢复软删除的文章',
         'command': 'restore-article --article-id N'},
        {'name': 'top-articles', 'description': '获取热门文章 Top N',
         'command': 'top-articles [--limit N]'},
        {'name': 'list-lables', 'description': '获取所有标签',
         'command': 'list-lables'},
        {'name': 'create-lable', 'description': '创建标签',
         'command': 'create-lable --lname TEXT'},
        {'name': 'list-users', 'description': '获取用户列表',
         'command': 'list-users'},
        {'name': 'create-user', 'description': '创建用户',
         'command': 'create-user --uname TEXT [--phone T] [--pwd T] [--email T] [--img URL]'},
        {'name': 'create-comment', 'description': '发表评论',
         'command': 'create-comment --uid N --aid N --content TEXT'},
        {'name': 'list-comments', 'description': '获取文章的评论列表',
         'command': 'list-comments --aid N'},
        {'name': 'delete-comment', 'description': '删除评论（软删除）',
         'command': 'delete-comment --comment-id N'},
        {'name': 'list-messages', 'description': '获取留言列表（含回复）',
         'command': 'list-messages'},
        {'name': 'create-message', 'description': '发表留言',
         'command': 'create-message --uid N --content TEXT'},
        {'name': 'reply-message', 'description': '回复留言',
         'command': 'reply-message --uid N --mid N --content TEXT'},
        {'name': 'delete-message', 'description': '删除留言（软删除）',
         'command': 'delete-message --message-id N'},
        {'name': 'list-moods', 'description': '获取说说列表',
         'command': 'list-moods'},
        {'name': 'create-mood', 'description': '发布说说',
         'command': 'create-mood --content TEXT [--title T] [--src URL]'},
        {'name': 'delete-mood', 'description': '删除说说',
         'command': 'delete-mood --mood-id N'},
        {'name': 'upload-file', 'description': '上传单个文件',
         'command': 'upload-file --filepath PATH'},
        {'name': 'upload-files', 'description': '批量上传文件',
         'command': 'upload-files --filepaths PATH [PATH ...]'},
        {'name': 'list-uploads', 'description': '列出所有已上传文件',
         'command': 'list-uploads'},
        {'name': 'delete-upload', 'description': '删除已上传文件',
         'command': 'delete-upload --filename TEXT'},
        {'name': 'admin-login', 'description': '后台登录获取 token',
         'command': 'admin-login --username TEXT --password TEXT'},
        {'name': 'admin-delete-articles', 'description': '后台批量删除文章',
         'command': 'admin-delete-articles --ids N [N ...] --token TEXT'},
    ]
    return {
        'capability': 'capability-list',
        'skill': 'blog-mini-kit-liufei',
        'version': '0.1.0',
        'subcommand_count': len(caps),
        'capabilities': caps + [
            {'name': 'capability-list', 'description': '列出本 skill 所有能力项',
             'command': 'capability-list'}
        ],
    }


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_md(payload):
    """将 JSON 输出转为 Markdown 表格（可选）。"""
    cap = payload.get('capability', '')
    if cap == 'capability-list':
        lines = [f"## 能力清单（{payload.get('skill', '')}）", "",
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
        prog='blog-mini-kit-liufei',
        description='博客系统(FastAPI) API 管理 skill — 覆盖 32 个端点')

    def add_common_args(p):
        p.add_argument('--format', choices=['json', 'md'], default='json',
                       help='输出格式，默认 json')

    sub = parser.add_subparsers(dest='command', help='能力命令')

    # A. health-check
    p = sub.add_parser('health-check', help='健康检查')
    add_common_args(p)

    # B. list-articles
    p = sub.add_parser('list-articles', help='分页查询文章列表')
    p.add_argument('--page', type=int, default=1, help='页码，默认 1')
    p.add_argument('--size', type=int, default=10, help='每页数量，默认 10')
    p.add_argument('--lid', type=int, default=0, help='标签 ID 筛选，0=不筛选')
    p.add_argument('--keyword', default='', help='标题关键词搜索')
    add_common_args(p)

    # C. get-article
    p = sub.add_parser('get-article', help='查询单篇文章详情（含评论）')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    add_common_args(p)

    # D. create-article
    p = sub.add_parser('create-article', help='发布新文章')
    p.add_argument('--title', required=True, help='文章标题（必填）')
    p.add_argument('--content', required=True, help='文章内容（必填）')
    p.add_argument('--uid', type=int, default=1, help='作者用户 ID，默认 1')
    p.add_argument('--lid', type=int, default=1, help='标签 ID，默认 1')
    p.add_argument('--img', default=None, help='封面图 URL')
    p.add_argument('--heat', type=int, default=0, help='初始热度，默认 0')
    add_common_args(p)

    # E. update-article
    p = sub.add_parser('update-article', help='更新文章')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    p.add_argument('--title', default=None, help='新标题')
    p.add_argument('--content', default=None, help='新内容')
    p.add_argument('--lid', type=int, default=None, help='新标签 ID')
    p.add_argument('--img', default=None, help='新封面图 URL')
    p.add_argument('--heat', type=int, default=None, help='新热度值')
    add_common_args(p)

    # F. delete-article
    p = sub.add_parser('delete-article', help='删除文章（默认软删除，--hard 硬删除）')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    p.add_argument('--hard', action='store_true', help='硬删除（默认软删除）')
    add_common_args(p)

    # G. restore-article
    p = sub.add_parser('restore-article', help='恢复软删除的文章')
    p.add_argument('--article-id', type=int, required=True, help='文章 ID')
    add_common_args(p)

    # H. top-articles
    p = sub.add_parser('top-articles', help='获取热门文章 Top N')
    p.add_argument('--limit', type=int, default=5, help='返回数量，默认 5（1-20）')
    add_common_args(p)

    # I. list-lables
    p = sub.add_parser('list-lables', help='获取所有标签')
    add_common_args(p)

    # J. create-lable
    p = sub.add_parser('create-lable', help='创建标签')
    p.add_argument('--lname', required=True, help='标签名称（必填）')
    add_common_args(p)

    # K. list-users
    p = sub.add_parser('list-users', help='获取用户列表')
    add_common_args(p)

    # L. create-user
    p = sub.add_parser('create-user', help='创建用户')
    p.add_argument('--uname', required=True, help='用户名（必填）')
    p.add_argument('--phone', default='', help='手机号')
    p.add_argument('--pwd', default='', help='密码')
    p.add_argument('--email', default='', help='邮箱')
    p.add_argument('--img', default='img/moren.jpg', help='头像路径')
    add_common_args(p)

    # M. create-comment
    p = sub.add_parser('create-comment', help='发表评论')
    p.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p.add_argument('--aid', type=int, required=True, help='文章 ID（必填）')
    p.add_argument('--content', required=True, help='评论内容（必填）')
    add_common_args(p)

    # N. list-comments
    p = sub.add_parser('list-comments', help='获取文章的评论列表')
    p.add_argument('--aid', type=int, required=True, help='文章 ID')
    add_common_args(p)

    # O. delete-comment
    p = sub.add_parser('delete-comment', help='删除评论（软删除）')
    p.add_argument('--comment-id', type=int, required=True, help='评论 ID')
    add_common_args(p)

    # P. list-messages
    p = sub.add_parser('list-messages', help='获取留言列表（含回复）')
    add_common_args(p)

    # Q. create-message
    p = sub.add_parser('create-message', help='发表留言')
    p.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p.add_argument('--content', required=True, help='留言内容（必填）')
    add_common_args(p)

    # R. reply-message
    p = sub.add_parser('reply-message', help='回复留言')
    p.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p.add_argument('--mid', type=int, required=True, help='留言 ID（必填）')
    p.add_argument('--content', required=True, help='回复内容（必填）')
    add_common_args(p)

    # S. delete-message
    p = sub.add_parser('delete-message', help='删除留言（软删除）')
    p.add_argument('--message-id', type=int, required=True, help='留言 ID')
    add_common_args(p)

    # T. list-moods
    p = sub.add_parser('list-moods', help='获取说说列表')
    add_common_args(p)

    # U. create-mood
    p = sub.add_parser('create-mood', help='发布说说')
    p.add_argument('--title', default='', help='标题')
    p.add_argument('--content', required=True, help='内容（必填）')
    p.add_argument('--src', default='', help='媒体 URL')
    add_common_args(p)

    # V. delete-mood
    p = sub.add_parser('delete-mood', help='删除说说')
    p.add_argument('--mood-id', type=int, required=True, help='说说 ID')
    add_common_args(p)

    # W. upload-file
    p = sub.add_parser('upload-file', help='上传单个文件')
    p.add_argument('--filepath', required=True, help='文件路径（必填）')
    add_common_args(p)

    # X. upload-files
    p = sub.add_parser('upload-files', help='批量上传文件')
    p.add_argument('--filepaths', required=True, nargs='+', help='文件路径列表（必填，空格分隔）')
    add_common_args(p)

    # Y. list-uploads
    p = sub.add_parser('list-uploads', help='列出所有已上传文件')
    add_common_args(p)

    # Z. delete-upload
    p = sub.add_parser('delete-upload', help='删除已上传文件')
    p.add_argument('--filename', required=True, help='文件名（必填）')
    add_common_args(p)

    # AA. admin-login
    p = sub.add_parser('admin-login', help='后台登录获取 token')
    p.add_argument('--username', required=True, help='管理员账号（必填）')
    p.add_argument('--password', required=True, help='管理员密码（必填）')
    add_common_args(p)

    # BB. admin-delete-articles
    p = sub.add_parser('admin-delete-articles', help='后台批量删除文章')
    p.add_argument('--ids', type=int, required=True, nargs='+', help='文章 ID 列表（必填）')
    p.add_argument('--token', required=True, help='admin token（通过 admin-login 获取）')
    add_common_args(p)

    # capability-list
    p_cl = sub.add_parser('capability-list', help='列出本 skill 所有能力项')
    add_common_args(p_cl)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(2)

    dispatch = {
        'health-check': cmd_health_check,
        'list-articles': cmd_list_articles,
        'get-article': cmd_get_article,
        'create-article': cmd_create_article,
        'update-article': cmd_update_article,
        'delete-article': cmd_delete_article,
        'restore-article': cmd_restore_article,
        'top-articles': cmd_top_articles,
        'list-lables': cmd_list_lables,
        'create-lable': cmd_create_lable,
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
        'admin-login': cmd_admin_login,
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
