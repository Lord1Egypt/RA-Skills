#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-publish — 博客系统内容发布与管理

能力（由 API 文档解析生成）:
  A. health-check — 检查 API 可达性
  B. list-articles — 分页查询文章列表
  C. get-article — 查询单篇文章详情
  D. create-article — 发布新文章
  E. update-article — 更新文章
  F. delete-article — 删除文章（默认软删除，可硬删除）
  G. restore-article — 恢复软删除的文章
  H. top-articles — 获取热门文章 Top N
  I. list-labels — 获取所有标签
  J. create-label — 创建标签
  K. list-uploads — 列出所有已上传文件
  L. upload-file — 上传单个文件
  M. upload-files — 批量上传文件

认证: none（公开 API，无需凭据）
退出码: 0=成功; 2=参数错误; 3=缺少配置（地址）; 4=API 调用失败
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Credentials（前缀由 skill name 推导，认证方式为 none）
# ---------------------------------------------------------------------------

_CRED_PREFIX = "BLOG_PUBLISH"
_AUTH_TYPE = "none"
_API_KEY_HEADER = ""
_API_KEY_LOCATION = ""


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
            if 'USERNAME' in u or u.endswith('_USER'):
                creds.setdefault('username', v)
            if 'PASSWORD' in u or u.endswith('_PASS'):
                creds.setdefault('password', v)
            if 'TOKEN' in u:
                creds.setdefault('token', v)
            if 'API_KEY' in u:
                creds.setdefault('api_key', v)
    return creds


def _load_from_project_knowledge():
    """从 .project-info/ 目录递归查找 JSON 配置文件，读取 config.{PREFIX}_BASE_URL。"""
    import glob
    creds = {}
    for pattern in ['.project-info/**/*.json',
                    '../.project-info/**/*.json',
                    '../../.project-info/**/*.json']:
        for filepath in glob.glob(pattern, recursive=True):
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
                for key, val in config.items():
                    if key.upper().startswith(prefix) and 'BASE_URL' in key.upper():
                        creds.setdefault('base_url', val)
            except Exception:
                continue
    return creds


def _get_base_url():
    """获取 API base URL——4 级优先级。"""
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

    resp = None
    try:
        if method == 'GET':
            resp = requests.get(url, params=params, timeout=30, **auth_kwargs)
        elif method == 'POST':
            resp = requests.post(url, json=payload, files=files, timeout=30, **auth_kwargs)
        elif method == 'PUT':
            resp = requests.put(url, json=payload, files=files, timeout=30, **auth_kwargs)
        elif method == 'PATCH':
            resp = requests.patch(url, json=payload, files=files, timeout=30, **auth_kwargs)
        elif method == 'DELETE':
            resp = requests.delete(url, params=params, timeout=30, **auth_kwargs)
        else:
            print(f"错误：不支持的方法 {method}", file=sys.stderr)
            sys.exit(2)

        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return {}
    except requests.exceptions.HTTPError:
        if resp is not None:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text[:500]
            print(f"错误：API 调用失败 {resp.status_code}: {detail}", file=sys.stderr)
        else:
            print("错误：API 调用失败（无响应对象）", file=sys.stderr)
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
    """能力 A：检查 API 可达性"""
    # GET /health
    return _api_request('GET', '/health')


def cmd_list_articles(args):
    """能力 B：分页查询文章列表"""
    # GET /api/articles
    params = {'page': args.page, 'size': args.size}
    if args.lid and args.lid > 0:
        params['lid'] = args.lid
    if args.keyword:
        params['keyword'] = args.keyword
    return _api_request('GET', '/api/articles', params=params)


def cmd_get_article(args):
    """能力 C：查询单篇文章详情"""
    # GET /api/articles/{id}
    return _api_request('GET', f'/api/articles/{args.id}')


def cmd_create_article(args):
    """能力 D：发布新文章"""
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


def cmd_update_article(args):
    """能力 E：更新文章"""
    # PUT /api/articles/{id}
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
        print("错误：至少指定一个需要更新的字段", file=sys.stderr)
        sys.exit(2)
    return _api_request('PUT', f'/api/articles/{args.id}', payload=payload)


def cmd_delete_article(args):
    """能力 F：删除文章（默认软删除，--hard 硬删除不可恢复）"""
    # DELETE /api/articles/{id}?soft=true|false
    soft = 'false' if args.hard else 'true'
    return _api_request('DELETE', f'/api/articles/{args.id}', params={'soft': soft})


def cmd_restore_article(args):
    """能力 G：恢复软删除的文章"""
    # POST /api/articles/{id}/restore
    return _api_request('POST', f'/api/articles/{args.id}/restore')


def cmd_top_articles(args):
    """能力 H：获取热门文章 Top N"""
    # GET /api/articles/heat/top
    return _api_request('GET', '/api/articles/heat/top', params={'limit': args.limit})


def cmd_list_labels(args):
    """能力 I：获取所有标签"""
    # GET /api/lables
    return _api_request('GET', '/api/lables')


def cmd_create_label(args):
    """能力 J：创建标签"""
    # POST /api/lables
    payload = {'lname': args.lname}
    return _api_request('POST', '/api/lables', payload=payload)


def cmd_list_uploads(args):
    """能力 K：列出所有已上传文件"""
    # GET /api/uploads/list
    return _api_request('GET', '/api/uploads/list')


def cmd_upload_file(args):
    """能力 L：上传单个文件"""
    # POST /api/upload (multipart/form-data, field=file)
    with open(args.filepath, 'rb') as f:
        return _api_request('POST', '/api/upload', files={'file': f})


def cmd_upload_files(args):
    """能力 M：批量上传文件"""
    # POST /api/upload/multiple (multipart/form-data, field=files)
    file_objects = [open(fp, 'rb') for fp in args.filepaths]
    try:
        return _api_request('POST', '/api/upload/multiple',
                            files=[('files', f) for f in file_objects])
    finally:
        for f in file_objects:
            f.close()


# ---------------------------------------------------------------------------
# Capability list
# ---------------------------------------------------------------------------

def cmd_capability_list(args):
    """列出本 skill 所有能力项。"""
    return {
        'capability': 'capability-list',
        'skill': 'blog-publish',
        'version': '1.0.0',
        'capabilities': [
            {'name': 'health-check', 'description': '检查 API 可达性',
             'command': 'health-check'},
            {'name': 'list-articles', 'description': '分页查询文章列表',
             'command': 'list-articles [--page N] [--size N] [--lid N] [--keyword K]'},
            {'name': 'get-article', 'description': '查询单篇文章详情',
             'command': 'get-article --id N'},
            {'name': 'create-article', 'description': '发布新文章',
             'command': 'create-article --title T --content C [--uid N] [--lid N] [--img U] [--heat N]'},
            {'name': 'update-article', 'description': '更新文章',
             'command': 'update-article --id N [--title T] [--content C] [--lid N] [--img U] [--heat N]'},
            {'name': 'delete-article', 'description': '删除文章（默认软删除，--hard 硬删除）',
             'command': 'delete-article --id N [--hard]'},
            {'name': 'restore-article', 'description': '恢复软删除的文章',
             'command': 'restore-article --id N'},
            {'name': 'top-articles', 'description': '获取热门文章 Top N',
             'command': 'top-articles [--limit N]'},
            {'name': 'list-labels', 'description': '获取所有标签',
             'command': 'list-labels'},
            {'name': 'create-label', 'description': '创建标签',
             'command': 'create-label --lname L'},
            {'name': 'list-uploads', 'description': '列出所有已上传文件',
             'command': 'list-uploads'},
            {'name': 'upload-file', 'description': '上传单个文件',
             'command': 'upload-file --filepath P'},
            {'name': 'upload-files', 'description': '批量上传文件',
             'command': 'upload-files --filepaths P1 P2 ...'},
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
    code = payload.get('code', '')
    if code == 200 and isinstance(payload.get('data'), list):
        rows = payload['data']
        if not rows:
            return "| (无数据) |\n|---|"
        headers = list(rows[0].keys())
        lines = ["| " + " | ".join(headers) + " |",
                 "|" + "|".join(["---"] * len(headers)) + "|"]
        for r in rows[:20]:
            lines.append("| " + " | ".join(str(r.get(h, '')) for h in headers) + " |")
        return "\n".join(lines)
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='blog-publish',
        description='博客系统内容发布与管理')
    parser.add_argument('--format', choices=['json', 'md'], default='json',
                        help='输出格式，默认 json')

    sub = parser.add_subparsers(dest='command', help='能力命令')

    def add_common_args(p):
        p.add_argument('--format', choices=['json', 'md'], default='json',
                       help='输出格式，默认 json')

    # health-check
    p_hc = sub.add_parser('health-check', help='检查 API 可达性')
    add_common_args(p_hc)

    # list-articles
    p_la = sub.add_parser('list-articles', help='分页查询文章列表')
    p_la.add_argument('--page', type=int, default=1, help='页码，默认 1')
    p_la.add_argument('--size', type=int, default=10, help='每页条数，默认 10')
    p_la.add_argument('--lid', type=int, default=0, help='按标签 ID 过滤，0=不过滤')
    p_la.add_argument('--keyword', default='', help='标题关键词搜索')
    add_common_args(p_la)

    # get-article
    p_ga = sub.add_parser('get-article', help='查询单篇文章详情')
    p_ga.add_argument('--id', type=int, required=True, help='文章 ID')
    add_common_args(p_ga)

    # create-article
    p_ca = sub.add_parser('create-article', help='发布新文章')
    p_ca.add_argument('--title', required=True, help='文章标题（必填）')
    p_ca.add_argument('--content', required=True, help='文章内容（必填，支持 HTML）')
    p_ca.add_argument('--uid', type=int, default=1, help='作者用户 ID，默认 1')
    p_ca.add_argument('--lid', type=int, default=1, help='标签 ID，默认 1')
    p_ca.add_argument('--img', default=None, help='封面图 URL（可选）')
    p_ca.add_argument('--heat', type=int, default=0, help='初始热度，默认 0')
    add_common_args(p_ca)

    # update-article
    p_ua = sub.add_parser('update-article', help='更新文章')
    p_ua.add_argument('--id', type=int, required=True, help='文章 ID')
    p_ua.add_argument('--title', default=None, help='新标题')
    p_ua.add_argument('--content', default=None, help='新内容')
    p_ua.add_argument('--lid', type=int, default=None, help='新标签 ID')
    p_ua.add_argument('--img', default=None, help='新封面图 URL')
    p_ua.add_argument('--heat', type=int, default=None, help='新热度值')
    add_common_args(p_ua)

    # delete-article
    p_da = sub.add_parser('delete-article', help='删除文章（默认软删除，--hard 硬删除不可恢复）')
    p_da.add_argument('--id', type=int, required=True, help='文章 ID')
    p_da.add_argument('--hard', action='store_true',
                      help='⚠️ 硬删除（不可恢复），不指定则默认软删除')
    add_common_args(p_da)

    # restore-article
    p_ra = sub.add_parser('restore-article', help='恢复软删除的文章')
    p_ra.add_argument('--id', type=int, required=True, help='文章 ID')
    add_common_args(p_ra)

    # top-articles
    p_ta = sub.add_parser('top-articles', help='获取热门文章 Top N')
    p_ta.add_argument('--limit', type=int, default=5, help='返回条数，默认 5（1-20）')
    add_common_args(p_ta)

    # list-labels
    p_ll = sub.add_parser('list-labels', help='获取所有标签')
    add_common_args(p_ll)

    # create-label
    p_cl = sub.add_parser('create-label', help='创建标签')
    p_cl.add_argument('--lname', required=True, help='标签名称（必填）')
    add_common_args(p_cl)

    # list-uploads
    p_lu = sub.add_parser('list-uploads', help='列出所有已上传文件')
    add_common_args(p_lu)

    # upload-file
    p_uf = sub.add_parser('upload-file', help='上传单个文件')
    p_uf.add_argument('--filepath', required=True, help='本地文件路径')
    add_common_args(p_uf)

    # upload-files
    p_ufs = sub.add_parser('upload-files', help='批量上传文件')
    p_ufs.add_argument('--filepaths', nargs='+', required=True, help='本地文件路径列表')
    add_common_args(p_ufs)

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
        'list-uploads': cmd_list_uploads,
        'upload-file': cmd_upload_file,
        'upload-files': cmd_upload_files,
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
