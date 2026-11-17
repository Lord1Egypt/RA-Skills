#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-big-kimi-kit — 博客内容发布 Skill

能力（由 API 文档解析生成）:
  A. health-check — 检查 API 可达性
  B. list-articles — 查询文章列表（分页+标签筛选+关键词）
  C. get-article — 查询文章详情（含评论）
  D. create-article — 创建文章
  E. update-article — 更新文章
  F. delete-article — 删除文章（支持软删除）
  G. restore-article — 恢复已删除文章
  H. top-articles — 查询热门文章
  I. list-labels — 查询标签列表
  J. create-label — 创建标签
  K. list-users — 查询用户列表
  L. create-user — 创建用户
  M. list-comments — 查询文章评论列表
  N. create-comment — 创建评论
  O. delete-comment — 删除评论
  P. list-messages — 查询留言列表
  Q. create-message — 创建留言
  R. reply-message — 回复留言
  S. delete-message — 删除留言
  T. list-moods — 查询说说列表
  U. create-mood — 创建说说
  V. delete-mood — 删除说说
  W. upload-file — 上传单个文件
  X. upload-files — 批量上传文件
  Y. list-uploads — 查询已上传文件列表
  Z. delete-upload — 删除已上传文件

认证: none（公开 API，BLOG_BIG_KIMI_KIT_* 环境变量，前缀由 skill name 推导）
退出码: 0=成功; 2=参数错误; 3=缺少配置（地址或认证）; 4=API 调用失败
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Credentials（前缀由 skill name 推导，认证方式由需求澄清决定）
# ---------------------------------------------------------------------------

_CRED_PREFIX = "BLOG_BIG_KIMI_KIT"  # skill name 转大写下划线
_AUTH_TYPE = "none"      # 公开 API，无认证
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
    # 1. 项目知识优先
    creds.update(_load_from_project_knowledge())
    # 2. 环境变量回退：项目知识缺失的字段从环境变量补充
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
    """从 .project-info/ 目录递归查找 JSON 配置文件，读取 secrets.{PREFIX}_* 字段。

    不固定文件名——扫描所有 .json 文件，检查是否含 secrets/config 字段。
    .project-info/ 由 grape worker 物化到 agent 工作目录（cwd）下，直接在当前目录查找。
    base_url 和 secrets 都严格按 {PREFIX}_ 前缀精确匹配，不做 fallback。
    """
    import glob
    creds = {}
    for filepath in glob.glob('.project-info/**/*.json', recursive=True):
        try:
            with open(filepath) as f:
                data = __import__('json').load(f)
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
            # base_url：严格按前缀精确匹配
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
        # 提示用户如何永久设置
        print("提示：可通过 export %s_BASE_URL=\"%s\" 永久设置，避免每次输入。" % (_CRED_PREFIX, base_url))
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
            print("错误：缺少认证，请设置环境变量（%s_USERNAME / %s_PASSWORD）" % (_CRED_PREFIX, _CRED_PREFIX), file=sys.stderr)
            sys.exit(3)
        return {"auth": HTTPBasicAuth(creds['username'], creds['password'])}
    elif _AUTH_TYPE == "token":
        if not creds.get('token'):
            print("错误：缺少认证，请设置环境变量（%s_TOKEN）" % _CRED_PREFIX, file=sys.stderr)
            sys.exit(3)
        return {"headers": {"Authorization": "Bearer " + creds['token']}}
    elif _AUTH_TYPE == "api_key":
        if not creds.get('api_key'):
            print("错误：缺少认证，请设置环境变量（%s_API_KEY）" % _CRED_PREFIX, file=sys.stderr)
            sys.exit(3)
        if _API_KEY_LOCATION == "header":
            return {"headers": {_API_KEY_HEADER: creds['api_key']}}
        else:
            # query 模式：返回 api_key 信息，由 _api_request 合并到 params（避免 params 冲突）
            return {"_api_key_param": _API_KEY_HEADER, "_api_key_value": creds['api_key']}
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
            return resp.json()
        return {}
    except requests.exceptions.HTTPError as e:
        print(f"错误：API 调用失败 {resp.status_code}: {e}", file=sys.stderr)
        sys.exit(4)
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败: {e}", file=sys.stderr)
        sys.exit(4)
    except ValueError:
        print(f"错误：API 返回非 JSON 格式（可能返回 HTML 错误页）", file=sys.stderr)
        sys.exit(4)


# ---------------------------------------------------------------------------
# Subcommand implementations（由 API 文档解析动态生成）
# ---------------------------------------------------------------------------

def cmd_health_check(args):
    """能力 A：检查 API 可达性"""
    # GET /health
    result = _api_request('GET', '/health')
    return result


def cmd_list_articles(args):
    """能力 B：查询文章列表（分页+标签筛选+关键词）"""
    # GET /api/articles
    params = {}
    if args.page is not None:
        params['page'] = args.page
    if args.size is not None:
        params['size'] = args.size
    if args.lid is not None:
        params['lid'] = args.lid
    if args.keyword is not None:
        params['keyword'] = args.keyword
    result = _api_request('GET', '/api/articles', params=params)
    return result


def cmd_get_article(args):
    """能力 C：查询文章详情（含评论）"""
    # GET /api/articles/{article_id}
    result = _api_request('GET', f'/api/articles/{args.article_id}')
    return result


def cmd_create_article(args):
    """能力 D：创建文章"""
    # POST /api/articles
    payload = {'title': args.title, 'content': args.content}
    if args.uid is not None:
        payload['uid'] = args.uid
    if args.lid is not None:
        payload['lid'] = args.lid
    if args.img is not None:
        payload['img'] = args.img
    if args.heat is not None:
        payload['heat'] = args.heat
    result = _api_request('POST', '/api/articles', payload=payload)
    return result


def cmd_update_article(args):
    """能力 E：更新文章"""
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
    result = _api_request('PUT', f'/api/articles/{args.article_id}', payload=payload)
    return result


def cmd_delete_article(args):
    """能力 F：删除文章（支持软删除）"""
    # DELETE /api/articles/{article_id}
    params = {}
    if args.soft is not None:
        params['soft'] = args.soft
    result = _api_request('DELETE', f'/api/articles/{args.article_id}', params=params)
    return result


def cmd_restore_article(args):
    """能力 G：恢复已删除文章"""
    # POST /api/articles/{article_id}/restore
    result = _api_request('POST', f'/api/articles/{args.article_id}/restore')
    return result


def cmd_top_articles(args):
    """能力 H：查询热门文章"""
    # GET /api/articles/heat/top
    params = {}
    if args.limit is not None:
        params['limit'] = args.limit
    result = _api_request('GET', '/api/articles/heat/top', params=params)
    return result


def cmd_list_labels(args):
    """能力 I：查询标签列表"""
    # GET /api/lables （API 实际路径为 lables，非 labels）
    result = _api_request('GET', '/api/lables')
    return result


def cmd_create_label(args):
    """能力 J：创建标签"""
    # POST /api/lables （API 实际路径为 lables，非 labels）
    payload = {'lname': args.lname}
    result = _api_request('POST', '/api/lables', payload=payload)
    return result


def cmd_list_users(args):
    """能力 K：查询用户列表"""
    # GET /api/users
    result = _api_request('GET', '/api/users')
    return result


def cmd_create_user(args):
    """能力 L：创建用户"""
    # POST /api/users
    payload = {'uname': args.uname}
    if args.phone is not None:
        payload['phone'] = args.phone
    if args.pwd is not None:
        payload['pwd'] = args.pwd
    if args.email is not None:
        payload['email'] = args.email
    if args.img is not None:
        payload['img'] = args.img
    result = _api_request('POST', '/api/users', payload=payload)
    return result


def cmd_list_comments(args):
    """能力 M：查询文章评论列表"""
    # GET /api/comments/{aid}
    result = _api_request('GET', f'/api/comments/{args.aid}')
    return result


def cmd_create_comment(args):
    """能力 N：创建评论"""
    # POST /api/comments
    payload = {'uid': args.uid, 'aid': args.aid, 'content': args.content}
    result = _api_request('POST', '/api/comments', payload=payload)
    return result


def cmd_delete_comment(args):
    """能力 O：删除评论"""
    # DELETE /api/comments/{comment_id}
    result = _api_request('DELETE', f'/api/comments/{args.comment_id}')
    return result


def cmd_list_messages(args):
    """能力 P：查询留言列表"""
    # GET /api/messages
    result = _api_request('GET', '/api/messages')
    return result


def cmd_create_message(args):
    """能力 Q：创建留言"""
    # POST /api/messages
    payload = {'uid': args.uid, 'content': args.content}
    result = _api_request('POST', '/api/messages', payload=payload)
    return result


def cmd_reply_message(args):
    """能力 R：回复留言"""
    # POST /api/messages/reply
    payload = {'uid': args.uid, 'mid': args.mid, 'content': args.content}
    result = _api_request('POST', '/api/messages/reply', payload=payload)
    return result


def cmd_delete_message(args):
    """能力 S：删除留言"""
    # DELETE /api/messages/{message_id}
    result = _api_request('DELETE', f'/api/messages/{args.message_id}')
    return result


def cmd_list_moods(args):
    """能力 T：查询说说列表"""
    # GET /api/moods
    result = _api_request('GET', '/api/moods')
    return result


def cmd_create_mood(args):
    """能力 U：创建说说"""
    # POST /api/moods
    payload = {'content': args.content}
    if args.title is not None:
        payload['title'] = args.title
    if args.src is not None:
        payload['src'] = args.src
    result = _api_request('POST', '/api/moods', payload=payload)
    return result


def cmd_delete_mood(args):
    """能力 V：删除说说"""
    # DELETE /api/moods/{mood_id}
    result = _api_request('DELETE', f'/api/moods/{args.mood_id}')
    return result


def cmd_upload_file(args):
    """能力 W：上传单个文件"""
    # POST /api/upload
    with open(args.filepath, 'rb') as f:
        result = _api_request('POST', '/api/upload', files={'file': f})
    return result


def cmd_upload_files(args):
    """能力 X：批量上传文件"""
    # POST /api/upload/multiple
    files = [open(fp, 'rb') for fp in args.filepaths]
    try:
        result = _api_request('POST', '/api/upload/multiple', files=[('files', f) for f in files])
    finally:
        for f in files:
            f.close()
    return result


def cmd_list_uploads(args):
    """能力 Y：查询已上传文件列表"""
    # GET /api/uploads/list
    result = _api_request('GET', '/api/uploads/list')
    return result


def cmd_delete_upload(args):
    """能力 Z：删除已上传文件"""
    # DELETE /api/uploads/{filename}
    result = _api_request('DELETE', f'/api/uploads/{args.filename}')
    return result


# ---------------------------------------------------------------------------
# Capability list
# ---------------------------------------------------------------------------

def cmd_capability_list(args):
    """列出本 skill 所有能力项。"""
    return {
        'capability': 'capability-list',
        'skill': 'blog-big-kimi-kit',
        'version': '0.1.0',
        'capabilities': [
            {'name': 'health-check', 'description': '检查 API 可达性',
             'command': 'health-check'},
            {'name': 'list-articles', 'description': '查询文章列表（分页+标签筛选+关键词）',
             'command': 'list-articles [--page N] [--size N] [--lid N] [--keyword TEXT]'},
            {'name': 'get-article', 'description': '查询文章详情（含评论）',
             'command': 'get-article --article-id N'},
            {'name': 'create-article', 'description': '创建文章',
             'command': 'create-article --title TEXT --content TEXT [--uid N] [--lid N] [--img URL] [--heat N]'},
            {'name': 'update-article', 'description': '更新文章',
             'command': 'update-article --article-id N [--title TEXT] [--content TEXT] [--lid N] [--img URL] [--heat N]'},
            {'name': 'delete-article', 'description': '删除文章（支持软删除）',
             'command': 'delete-article --article-id N [--soft true/false]'},
            {'name': 'restore-article', 'description': '恢复已删除文章',
             'command': 'restore-article --article-id N'},
            {'name': 'top-articles', 'description': '查询热门文章',
             'command': 'top-articles [--limit N]'},
            {'name': 'list-labels', 'description': '查询标签列表',
             'command': 'list-labels'},
            {'name': 'create-label', 'description': '创建标签',
             'command': 'create-label --lname TEXT'},
            {'name': 'list-users', 'description': '查询用户列表',
             'command': 'list-users'},
            {'name': 'create-user', 'description': '创建用户',
             'command': 'create-user --uname TEXT [--phone TEXT] [--pwd TEXT] [--email TEXT] [--img URL]'},
            {'name': 'list-comments', 'description': '查询文章评论列表',
             'command': 'list-comments --aid N'},
            {'name': 'create-comment', 'description': '创建评论',
             'command': 'create-comment --uid N --aid N --content TEXT'},
            {'name': 'delete-comment', 'description': '删除评论',
             'command': 'delete-comment --comment-id N'},
            {'name': 'list-messages', 'description': '查询留言列表',
             'command': 'list-messages'},
            {'name': 'create-message', 'description': '创建留言',
             'command': 'create-message --uid N --content TEXT'},
            {'name': 'reply-message', 'description': '回复留言',
             'command': 'reply-message --uid N --mid N --content TEXT'},
            {'name': 'delete-message', 'description': '删除留言',
             'command': 'delete-message --message-id N'},
            {'name': 'list-moods', 'description': '查询说说列表',
             'command': 'list-moods'},
            {'name': 'create-mood', 'description': '创建说说',
             'command': 'create-mood --content TEXT [--title TEXT] [--src TEXT]'},
            {'name': 'delete-mood', 'description': '删除说说',
             'command': 'delete-mood --mood-id N'},
            {'name': 'upload-file', 'description': '上传单个文件',
             'command': 'upload-file --filepath PATH'},
            {'name': 'upload-files', 'description': '批量上传文件',
             'command': 'upload-files --filepaths PATH [PATH ...]'},
            {'name': 'list-uploads', 'description': '查询已上传文件列表',
             'command': 'list-uploads'},
            {'name': 'delete-upload', 'description': '删除已上传文件',
             'command': 'delete-upload --filename TEXT'},
            {'name': 'capability-list', 'description': '列出本 skill 所有能力项',
             'command': 'capability-list'},
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
    # 其他子命令的 Markdown 渲染按实际响应结构生成
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='blog-big-kimi-kit',
        description='博客内容发布 Skill — 覆盖文章/标签/用户/评论/留言/说说/文件上传/健康检查全部 API')

    def add_common_args(p):
        p.add_argument('--format', choices=['json', 'md'], default='json',
                       help='输出格式，默认 json')

    sub = parser.add_subparsers(dest='command', help='能力命令')

    # health-check
    p_hc = sub.add_parser('health-check', help='检查 API 可达性')
    add_common_args(p_hc)

    # list-articles
    p_la = sub.add_parser('list-articles', help='查询文章列表（分页+标签筛选+关键词）')
    p_la.add_argument('--page', type=int, default=None, help='页码，默认 1')
    p_la.add_argument('--size', type=int, default=None, help='每页数量，默认 10，最大 100')
    p_la.add_argument('--lid', type=int, default=None, help='标签 ID 筛选，默认 0（不限）')
    p_la.add_argument('--keyword', type=str, default=None, help='关键词搜索')
    add_common_args(p_la)

    # get-article
    p_ga = sub.add_parser('get-article', help='查询文章详情（含评论）')
    p_ga.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    add_common_args(p_ga)

    # create-article
    p_ca = sub.add_parser('create-article', help='创建文章')
    p_ca.add_argument('--title', type=str, required=True, help='文章标题（必填）')
    p_ca.add_argument('--content', type=str, required=True, help='文章内容（必填）')
    p_ca.add_argument('--uid', type=int, default=None, help='用户 ID，默认 1')
    p_ca.add_argument('--lid', type=int, default=None, help='标签 ID，默认 1')
    p_ca.add_argument('--img', type=str, default=None, help='封面图 URL')
    p_ca.add_argument('--heat', type=int, default=None, help='热度值，默认 0')
    add_common_args(p_ca)

    # update-article
    p_ua = sub.add_parser('update-article', help='更新文章')
    p_ua.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    p_ua.add_argument('--title', type=str, default=None, help='新标题')
    p_ua.add_argument('--content', type=str, default=None, help='新内容')
    p_ua.add_argument('--lid', type=int, default=None, help='新标签 ID')
    p_ua.add_argument('--img', type=str, default=None, help='新封面图')
    p_ua.add_argument('--heat', type=int, default=None, help='新热度值')
    add_common_args(p_ua)

    # delete-article
    p_da = sub.add_parser('delete-article', help='删除文章（支持软删除）')
    p_da.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    p_da.add_argument('--soft', type=str, default=None, help='是否软删除（true/false），默认 true')
    add_common_args(p_da)

    # restore-article
    p_ra = sub.add_parser('restore-article', help='恢复已删除文章')
    p_ra.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    add_common_args(p_ra)

    # top-articles
    p_ta = sub.add_parser('top-articles', help='查询热门文章')
    p_ta.add_argument('--limit', type=int, default=None, help='返回数量，默认 5，最大 20')
    add_common_args(p_ta)

    # list-labels
    p_ll = sub.add_parser('list-labels', help='查询标签列表')
    add_common_args(p_ll)

    # create-label
    p_cl = sub.add_parser('create-label', help='创建标签')
    p_cl.add_argument('--lname', type=str, required=True, help='标签名（必填）')
    add_common_args(p_cl)

    # list-users
    p_lu = sub.add_parser('list-users', help='查询用户列表')
    add_common_args(p_lu)

    # create-user
    p_cu = sub.add_parser('create-user', help='创建用户')
    p_cu.add_argument('--uname', type=str, required=True, help='用户名（必填）')
    p_cu.add_argument('--phone', type=str, default=None, help='手机号')
    p_cu.add_argument('--pwd', type=str, default=None, help='密码')
    p_cu.add_argument('--email', type=str, default=None, help='邮箱')
    p_cu.add_argument('--img', type=str, default=None, help='头像，默认 img/moren.jpg')
    add_common_args(p_cu)

    # list-comments
    p_lc = sub.add_parser('list-comments', help='查询文章评论列表')
    p_lc.add_argument('--aid', type=int, required=True, help='文章 ID（必填）')
    add_common_args(p_lc)

    # create-comment
    p_cc = sub.add_parser('create-comment', help='创建评论')
    p_cc.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p_cc.add_argument('--aid', type=int, required=True, help='文章 ID（必填）')
    p_cc.add_argument('--content', type=str, required=True, help='评论内容（必填）')
    add_common_args(p_cc)

    # delete-comment
    p_dc = sub.add_parser('delete-comment', help='删除评论')
    p_dc.add_argument('--comment-id', type=int, required=True, help='评论 ID（必填）')
    add_common_args(p_dc)

    # list-messages
    p_lm = sub.add_parser('list-messages', help='查询留言列表')
    add_common_args(p_lm)

    # create-message
    p_cm = sub.add_parser('create-message', help='创建留言')
    p_cm.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p_cm.add_argument('--content', type=str, required=True, help='留言内容（必填）')
    add_common_args(p_cm)

    # reply-message
    p_rm = sub.add_parser('reply-message', help='回复留言')
    p_rm.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p_rm.add_argument('--mid', type=int, required=True, help='留言 ID（必填）')
    p_rm.add_argument('--content', type=str, required=True, help='回复内容（必填）')
    add_common_args(p_rm)

    # delete-message
    p_dm = sub.add_parser('delete-message', help='删除留言')
    p_dm.add_argument('--message-id', type=int, required=True, help='留言 ID（必填）')
    add_common_args(p_dm)

    # list-moods
    p_lmo = sub.add_parser('list-moods', help='查询说说列表')
    add_common_args(p_lmo)

    # create-mood
    p_cmo = sub.add_parser('create-mood', help='创建说说')
    p_cmo.add_argument('--content', type=str, required=True, help='说说内容（必填）')
    p_cmo.add_argument('--title', type=str, default=None, help='标题，默认空')
    p_cmo.add_argument('--src', type=str, default=None, help='来源/配图，默认空')
    add_common_args(p_cmo)

    # delete-mood
    p_dmo = sub.add_parser('delete-mood', help='删除说说')
    p_dmo.add_argument('--mood-id', type=int, required=True, help='说说 ID（必填）')
    add_common_args(p_dmo)

    # upload-file
    p_uf = sub.add_parser('upload-file', help='上传单个文件')
    p_uf.add_argument('--filepath', type=str, required=True, help='文件路径（必填）')
    add_common_args(p_uf)

    # upload-files
    p_ufs = sub.add_parser('upload-files', help='批量上传文件')
    p_ufs.add_argument('--filepaths', type=str, nargs='+', required=True, help='文件路径列表（必填，至少一个）')
    add_common_args(p_ufs)

    # list-uploads
    p_lul = sub.add_parser('list-uploads', help='查询已上传文件列表')
    add_common_args(p_lul)

    # delete-upload
    p_dul = sub.add_parser('delete-upload', help='删除已上传文件')
    p_dul.add_argument('--filename', type=str, required=True, help='文件名（必填）')
    add_common_args(p_dul)

    # capability-list
    p_cl2 = sub.add_parser('capability-list', help='列出本 skill 所有能力项')
    add_common_args(p_cl2)

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
