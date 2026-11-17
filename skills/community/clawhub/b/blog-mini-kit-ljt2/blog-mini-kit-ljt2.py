#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-mini-kit-ljt2 — 博客系统 API 管理工具（无认证，公开 API）

能力（由 OpenAPI 文档解析生成）:
  A. health-check — 健康检查
  B. list-articles — 查询文章列表
  C. create-article — 创建文章
  D. top-articles — 查询热门文章
  E. get-article — 查询文章详情
  F. update-article — 更新文章
  G. delete-article — 删除文章（软删除/硬删除）
  H. restore-article — 恢复软删除的文章
  I. list-labels — 查询标签列表（API 路径 /api/lables）
  J. create-label — 创建标签（API 路径 /api/lables）
  K. list-users — 查询用户列表
  L. create-user — 创建用户
  M. create-comment — 创建评论
  N. list-comments — 查询文章评论列表
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
  AA. capability-list — 列出本 skill 所有能力项

认证: none（公开 API，无认证）
退出码: 0=成功; 2=参数错误; 3=缺少配置（地址）; 4=API 调用失败
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Credentials（前缀由 skill name 推导，认证方式为 none）
# ---------------------------------------------------------------------------

_CRED_PREFIX = "BLOG_MINI_KIT_LJT2"
_AUTH_TYPE = "none"


def _load_credentials():
    """获取认证凭据——4 级优先级（与 base_url 一致）。

    1. 项目知识：递归扫描 .project-info/ 下所有 JSON 文件
    2. 环境变量：扫描 {PREFIX}_* 开头变量
    3. 当前上下文：A2A context 已注入的环境变量
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
    .project-info/ 由 grape worker 物化到 agent 工作目录（cwd）下。
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
# API client（无认证，公开 API）
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
# Subcommand implementations
# ---------------------------------------------------------------------------

def cmd_health_check(args):
    """能力 A：健康检查"""
    return _api_request('GET', '/health')


def cmd_list_articles(args):
    """能力 B：查询文章列表"""
    params = {'page': args.page, 'size': args.size}
    if args.lid is not None:
        params['lid'] = args.lid
    if args.keyword:
        params['keyword'] = args.keyword
    return _api_request('GET', '/api/articles', params=params)


def cmd_create_article(args):
    """能力 C：创建文章"""
    payload = {'title': args.title, 'content': args.content, 'uid': args.uid, 'lid': args.lid}
    if args.img is not None:
        payload['img'] = args.img
    if args.heat is not None:
        payload['heat'] = args.heat
    return _api_request('POST', '/api/articles', payload=payload)


def cmd_top_articles(args):
    """能力 D：查询热门文章"""
    params = {'limit': args.limit}
    return _api_request('GET', '/api/articles/heat/top', params=params)


def cmd_get_article(args):
    """能力 E：查询文章详情"""
    return _api_request('GET', f'/api/articles/{args.article_id}')


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
    return _api_request('PUT', f'/api/articles/{args.article_id}', payload=payload)


def cmd_delete_article(args):
    """能力 G：删除文章（软删除/硬删除）"""
    soft_val = args.soft == 'true'
    if not soft_val:
        print("⚠️  警告：正在执行硬删除，此操作不可恢复！", file=sys.stderr)
    else:
        print("ℹ️  正在执行软删除（可通过 restore-article 恢复）", file=sys.stderr)
    return _api_request('DELETE', f'/api/articles/{args.article_id}', params={'soft': soft_val})


def cmd_restore_article(args):
    """能力 H：恢复软删除的文章"""
    return _api_request('POST', f'/api/articles/{args.article_id}/restore')


def cmd_list_labels(args):
    """能力 I：查询标签列表（API 路径 /api/lables）"""
    return _api_request('GET', '/api/lables')


def cmd_create_label(args):
    """能力 J：创建标签（API 路径 /api/lables）"""
    payload = {'lname': args.lname}
    return _api_request('POST', '/api/lables', payload=payload)


def cmd_list_users(args):
    """能力 K：查询用户列表"""
    return _api_request('GET', '/api/users')


def cmd_create_user(args):
    """能力 L：创建用户"""
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


def cmd_create_comment(args):
    """能力 M：创建评论"""
    payload = {'uid': args.uid, 'aid': args.aid, 'content': args.content}
    return _api_request('POST', '/api/comments', payload=payload)


def cmd_list_comments(args):
    """能力 N：查询文章评论列表"""
    return _api_request('GET', f'/api/comments/{args.aid}')


def cmd_delete_comment(args):
    """能力 O：删除评论"""
    print("⚠️  警告：正在删除评论，此操作不可恢复。", file=sys.stderr)
    return _api_request('DELETE', f'/api/comments/{args.comment_id}')


def cmd_list_messages(args):
    """能力 P：查询留言列表"""
    return _api_request('GET', '/api/messages')


def cmd_create_message(args):
    """能力 Q：创建留言"""
    payload = {'uid': args.uid, 'content': args.content}
    return _api_request('POST', '/api/messages', payload=payload)


def cmd_reply_message(args):
    """能力 R：回复留言"""
    payload = {'uid': args.uid, 'mid': args.mid, 'content': args.content}
    return _api_request('POST', '/api/messages/reply', payload=payload)


def cmd_delete_message(args):
    """能力 S：删除留言"""
    print("⚠️  警告：正在删除留言，此操作不可恢复。", file=sys.stderr)
    return _api_request('DELETE', f'/api/messages/{args.message_id}')


def cmd_list_moods(args):
    """能力 T：查询说说列表"""
    return _api_request('GET', '/api/moods')


def cmd_create_mood(args):
    """能力 U：创建说说"""
    payload = {'content': args.content}
    if args.title is not None:
        payload['title'] = args.title
    if args.src is not None:
        payload['src'] = args.src
    return _api_request('POST', '/api/moods', payload=payload)


def cmd_delete_mood(args):
    """能力 V：删除说说"""
    print("⚠️  警告：正在删除说说，此操作不可恢复。", file=sys.stderr)
    return _api_request('DELETE', f'/api/moods/{args.mood_id}')


def cmd_upload_file(args):
    """能力 W：上传单个文件"""
    with open(args.filepath, 'rb') as f:
        return _api_request('POST', '/api/upload', files={'file': f})


def cmd_upload_files(args):
    """能力 X：批量上传文件"""
    files = [open(fp, 'rb') for fp in args.filepaths]
    try:
        return _api_request('POST', '/api/upload/multiple', files=[('files', f) for f in files])
    finally:
        for f in files:
            f.close()


def cmd_list_uploads(args):
    """能力 Y：查询已上传文件列表"""
    return _api_request('GET', '/api/uploads/list')


def cmd_delete_upload(args):
    """能力 Z：删除已上传文件"""
    print("⚠️  警告：正在删除已上传文件，此操作不可恢复。", file=sys.stderr)
    return _api_request('DELETE', f'/api/uploads/{args.filename}')


# ---------------------------------------------------------------------------
# Capability list
# ---------------------------------------------------------------------------

_CAPABILITIES = [
    {'name': 'health-check', 'description': '健康检查', 'command': 'health-check'},
    {'name': 'list-articles', 'description': '查询文章列表', 'command': 'list-articles [--page N] [--size N] [--lid N] [--keyword TXT]'},
    {'name': 'create-article', 'description': '创建文章', 'command': 'create-article --title TXT --content TXT [--uid N] [--lid N] [--img TXT] [--heat N]'},
    {'name': 'top-articles', 'description': '查询热门文章', 'command': 'top-articles [--limit N]'},
    {'name': 'get-article', 'description': '查询文章详情', 'command': 'get-article --article-id N'},
    {'name': 'update-article', 'description': '更新文章', 'command': 'update-article --article-id N [--title TXT] [--content TXT] [--lid N] [--img TXT] [--heat N]'},
    {'name': 'delete-article', 'description': '删除文章（软删除/硬删除）', 'command': 'delete-article --article-id N [--soft true|false]'},
    {'name': 'restore-article', 'description': '恢复软删除的文章', 'command': 'restore-article --article-id N'},
    {'name': 'list-labels', 'description': '查询标签列表（API 路径 /api/lables）', 'command': 'list-labels'},
    {'name': 'create-label', 'description': '创建标签（API 路径 /api/lables）', 'command': 'create-label --lname TXT'},
    {'name': 'list-users', 'description': '查询用户列表', 'command': 'list-users'},
    {'name': 'create-user', 'description': '创建用户', 'command': 'create-user --uname TXT [--phone TXT] [--pwd TXT] [--email TXT] [--img TXT]'},
    {'name': 'create-comment', 'description': '创建评论', 'command': 'create-comment --uid N --aid N --content TXT'},
    {'name': 'list-comments', 'description': '查询文章评论列表', 'command': 'list-comments --aid N'},
    {'name': 'delete-comment', 'description': '删除评论', 'command': 'delete-comment --comment-id N'},
    {'name': 'list-messages', 'description': '查询留言列表', 'command': 'list-messages'},
    {'name': 'create-message', 'description': '创建留言', 'command': 'create-message --uid N --content TXT'},
    {'name': 'reply-message', 'description': '回复留言', 'command': 'reply-message --uid N --mid N --content TXT'},
    {'name': 'delete-message', 'description': '删除留言', 'command': 'delete-message --message-id N'},
    {'name': 'list-moods', 'description': '查询说说列表', 'command': 'list-moods'},
    {'name': 'create-mood', 'description': '创建说说', 'command': 'create-mood --content TXT [--title TXT] [--src TXT]'},
    {'name': 'delete-mood', 'description': '删除说说', 'command': 'delete-mood --mood-id N'},
    {'name': 'upload-file', 'description': '上传单个文件', 'command': 'upload-file --filepath PATH'},
    {'name': 'upload-files', 'description': '批量上传文件', 'command': 'upload-files --filepaths PATH [PATH ...]'},
    {'name': 'list-uploads', 'description': '查询已上传文件列表', 'command': 'list-uploads'},
    {'name': 'delete-upload', 'description': '删除已上传文件', 'command': 'delete-upload --filename TXT'},
]


def cmd_capability_list(args):
    """列出本 skill 所有能力项。"""
    return {
        'capability': 'capability-list',
        'skill': 'blog-mini-kit-ljt2',
        'version': '0.1.0',
        'subcommand_count': len(_CAPABILITIES),
        'capabilities': _CAPABILITIES + [
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
        lines = [f"## 能力清单（{payload.get('skill', '')} v{payload.get('version', '')}）", "",
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
        prog='blog-mini-kit-ljt2',
        description='博客系统 API 管理工具（无认证，公开 API）')

    def add_common_args(p):
        p.add_argument('--format', choices=['json', 'md'], default='json',
                       help='输出格式，默认 json')

    sub = parser.add_subparsers(dest='command', help='能力命令')

    # --- Health ---
    p_hc = sub.add_parser('health-check', help='健康检查')
    add_common_args(p_hc)

    # --- Articles ---
    p_la = sub.add_parser('list-articles', help='查询文章列表')
    p_la.add_argument('--page', type=int, default=1, help='页码，默认 1')
    p_la.add_argument('--size', type=int, default=10, help='每页条数，默认 10')
    p_la.add_argument('--lid', type=int, default=None, help='标签 ID 过滤')
    p_la.add_argument('--keyword', default=None, help='关键词搜索')
    add_common_args(p_la)

    p_ca = sub.add_parser('create-article', help='创建文章')
    p_ca.add_argument('--title', required=True, help='标题（必填）')
    p_ca.add_argument('--content', required=True, help='内容（必填）')
    p_ca.add_argument('--uid', type=int, default=1, help='作者 ID，默认 1')
    p_ca.add_argument('--lid', type=int, default=1, help='标签 ID，默认 1')
    p_ca.add_argument('--img', default=None, help='封面图片路径')
    p_ca.add_argument('--heat', type=int, default=0, help='热度值，默认 0')
    add_common_args(p_ca)

    p_ta = sub.add_parser('top-articles', help='查询热门文章')
    p_ta.add_argument('--limit', type=int, default=5, help='返回条数，默认 5')
    add_common_args(p_ta)

    p_ga = sub.add_parser('get-article', help='查询文章详情')
    p_ga.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    add_common_args(p_ga)

    p_ua = sub.add_parser('update-article', help='更新文章')
    p_ua.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    p_ua.add_argument('--title', default=None, help='标题')
    p_ua.add_argument('--content', default=None, help='内容')
    p_ua.add_argument('--lid', type=int, default=None, help='标签 ID')
    p_ua.add_argument('--img', default=None, help='封面图片路径')
    p_ua.add_argument('--heat', type=int, default=None, help='热度值')
    add_common_args(p_ua)

    p_da = sub.add_parser('delete-article', help='删除文章（软删除/硬删除）')
    p_da.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    p_da.add_argument('--soft', choices=['true', 'false'], default='true',
                      help='删除方式：true=软删除（默认，可恢复），false=硬删除（不可恢复，需谨慎）')
    add_common_args(p_da)

    p_ra = sub.add_parser('restore-article', help='恢复软删除的文章')
    p_ra.add_argument('--article-id', type=int, required=True, help='文章 ID（必填）')
    add_common_args(p_ra)

    # --- Labels (API path: /api/lables) ---
    p_ll = sub.add_parser('list-labels', help='查询标签列表')
    add_common_args(p_ll)

    p_cl = sub.add_parser('create-label', help='创建标签')
    p_cl.add_argument('--lname', required=True, help='标签名称（必填）')
    add_common_args(p_cl)

    # --- Users ---
    p_lu = sub.add_parser('list-users', help='查询用户列表')
    add_common_args(p_lu)

    p_cu = sub.add_parser('create-user', help='创建用户')
    p_cu.add_argument('--uname', required=True, help='用户名（必填）')
    p_cu.add_argument('--phone', default=None, help='手机号')
    p_cu.add_argument('--pwd', default=None, help='密码')
    p_cu.add_argument('--email', default=None, help='邮箱')
    p_cu.add_argument('--img', default=None, help='头像路径，默认 img/moren.jpg')
    add_common_args(p_cu)

    # --- Comments ---
    p_cc = sub.add_parser('create-comment', help='创建评论')
    p_cc.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p_cc.add_argument('--aid', type=int, required=True, help='文章 ID（必填）')
    p_cc.add_argument('--content', required=True, help='评论内容（必填）')
    add_common_args(p_cc)

    p_lc = sub.add_parser('list-comments', help='查询文章评论列表')
    p_lc.add_argument('--aid', type=int, required=True, help='文章 ID（必填）')
    add_common_args(p_lc)

    p_dc = sub.add_parser('delete-comment', help='删除评论')
    p_dc.add_argument('--comment-id', type=int, required=True, help='评论 ID（必填）')
    add_common_args(p_dc)

    # --- Messages ---
    p_lm = sub.add_parser('list-messages', help='查询留言列表')
    add_common_args(p_lm)

    p_cm = sub.add_parser('create-message', help='创建留言')
    p_cm.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p_cm.add_argument('--content', required=True, help='留言内容（必填）')
    add_common_args(p_cm)

    p_rm = sub.add_parser('reply-message', help='回复留言')
    p_rm.add_argument('--uid', type=int, required=True, help='用户 ID（必填）')
    p_rm.add_argument('--mid', type=int, required=True, help='留言 ID（必填）')
    p_rm.add_argument('--content', required=True, help='回复内容（必填）')
    add_common_args(p_rm)

    p_dm = sub.add_parser('delete-message', help='删除留言')
    p_dm.add_argument('--message-id', type=int, required=True, help='留言 ID（必填）')
    add_common_args(p_dm)

    # --- Moods ---
    p_lmo = sub.add_parser('list-moods', help='查询说说列表')
    add_common_args(p_lmo)

    p_cmo = sub.add_parser('create-mood', help='创建说说')
    p_cmo.add_argument('--content', required=True, help='说说内容（必填）')
    p_cmo.add_argument('--title', default=None, help='标题')
    p_cmo.add_argument('--src', default=None, help='来源/媒体路径')
    add_common_args(p_cmo)

    p_dmo = sub.add_parser('delete-mood', help='删除说说')
    p_dmo.add_argument('--mood-id', type=int, required=True, help='说说 ID（必填）')
    add_common_args(p_dmo)

    # --- Uploads ---
    p_uf = sub.add_parser('upload-file', help='上传单个文件')
    p_uf.add_argument('--filepath', required=True, help='文件路径（必填）')
    add_common_args(p_uf)

    p_ufs = sub.add_parser('upload-files', help='批量上传文件')
    p_ufs.add_argument('--filepaths', required=True, nargs='+', help='文件路径列表（至少一个）')
    add_common_args(p_ufs)

    p_lup = sub.add_parser('list-uploads', help='查询已上传文件列表')
    add_common_args(p_lup)

    p_dup = sub.add_parser('delete-upload', help='删除已上传文件')
    p_dup.add_argument('--filename', required=True, help='文件名（必填）')
    add_common_args(p_dup)

    # --- capability-list ---
    p_cl2 = sub.add_parser('capability-list', help='列出本 skill 所有能力项')
    add_common_args(p_cl2)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(2)

    dispatch = {
        'health-check': cmd_health_check,
        'list-articles': cmd_list_articles,
        'create-article': cmd_create_article,
        'top-articles': cmd_top_articles,
        'get-article': cmd_get_article,
        'update-article': cmd_update_article,
        'delete-article': cmd_delete_article,
        'restore-article': cmd_restore_article,
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
