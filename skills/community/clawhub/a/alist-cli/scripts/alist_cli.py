#!/usr/bin/env python3
"""
AList CLI - 文件管理工具

Usage:
    alist login [username] [password]
    alist ls [path]
    alist get <path>
    alist mkdir <path>
    alist upload <local_path> <remote_path>
    alist rm <path>
    alist mv <src> <dst>
    alist search <keyword> [path]
    alist url <path>
    alist whoami

Note:
    - Auth token 通过环境变量管理（ALIST_AUTH_TOKEN, ALIST_USER_INFO）
    - 用户路径是相对于 base_path 的虚拟路径
    - 脚本自动处理 base_path 转换
    - Token 过期时自动重新登录
    - 依赖：requests（需预先安装）

URL 拼接规则:
    - 网页浏览: {ALIST_URL}/#/{real_path}  (AList 前端 SPA hash router)
    - 预览直链: {ALIST_URL}/d{real_path}?sign={sign}  (需要签名，临时有效)
    - 下载直链: {ALIST_URL}/p{real_path}?sign={sign}  (需要签名，临时有效)
    其中 real_path = base_path + user_path
"""

import argparse
import json
import os
import sys
import urllib.parse

import requests

# ── 配置 ──────────────────────────────────────────────────────
ENV_URL = "ALIST_URL"
ENV_TOKEN = "ALIST_AUTH_TOKEN"
ENV_USER_INFO = "ALIST_USER_INFO"
ENV_USERNAME = "ALIST_USERNAME"
ENV_PASSWORD = "ALIST_PASSWORD"


class AList:
    def __init__(self, url=None):
        if not url:
            url = os.environ.get(ENV_URL, "")
        if not url:
            print(f"❌ 请设置 {ENV_URL} 环境变量")
            sys.exit(1)
        self.url = url.rstrip('/')
        self.token = os.environ.get(ENV_TOKEN, "")
        self._load_user_info_from_env()
        self._ensure_auth()

    # ── 环境变量读写 ──────────────────────────────────────────

    def _load_user_info_from_env(self):
        raw = os.environ.get(ENV_USER_INFO, "")
        if raw:
            try:
                info = json.loads(raw)
                self.base_path = info.get('base_path', '')
            except json.JSONDecodeError:
                self.base_path = ''
        else:
            self.base_path = ''

    def _save_token_to_env(self, token):
        self.token = token
        os.environ[ENV_TOKEN] = token

    def _save_user_info_to_env(self, user_info):
        os.environ[ENV_USER_INFO] = json.dumps(user_info, ensure_ascii=False)
        self.base_path = user_info.get('base_path', '')

    # ── Auth 管理 ─────────────────────────────────────────────

    def _ensure_auth(self):
        if not self.token:
            self._auto_login()

    def _auto_login(self):
        username = os.environ.get(ENV_USERNAME, "")
        password = os.environ.get(ENV_PASSWORD, "")
        if not username or not password:
            print(f"❌ 未认证。请先设置 {ENV_USERNAME} 和 {ENV_PASSWORD} 环境变量，或运行 alist login。")
            sys.exit(1)
        self._do_login(username, password, silent=True)

    def _check_and_refresh_auth(self, resp_data):
        if resp_data.get('code') == 401:
            print("⚠️  Token 已过期，正在自动重新登录...")
            self._auto_login()
            return True
        return False

    def _do_login(self, username, password, silent=False):
        data = requests.post(
            f"{self.url}/api/auth/login",
            json={"username": username, "password": password},
        ).json()

        if data.get('code') != 200:
            if not silent:
                print(f"❌ 登录失败: {data.get('message', '未知错误')}")
            return False

        token = data['data']['token']
        self._save_token_to_env(token)

        me_resp = requests.get(
            f"{self.url}/api/me",
            headers={"Authorization": token},
        ).json()

        if me_resp.get('code') == 200:
            user_info = me_resp['data']
            self._save_user_info_to_env(user_info)
            if not silent:
                print(f"✅ 登录成功！")
                print(f"   用户: {user_info['username']}")
                print(f"   根目录: {user_info.get('base_path', '/')}")
        else:
            if not silent:
                print(f"✅ 登录成功！Token 已保存")
        return True

    def login(self, username, password):
        if self._do_login(username, password):
            print()
            print("📌 请运行以下命令使 token 在当前 shell 生效：")
            print(f'   export {ENV_TOKEN}="{self.token}"')
            user_info_raw = os.environ.get(ENV_USER_INFO, "")
            if user_info_raw:
                print(f'   export {ENV_USER_INFO}=\'{user_info_raw}\'')
            return True
        return False

    # ── 路径转换 ──────────────────────────────────────────────

    def _to_real_path(self, user_path):
        user_path = user_path.lstrip('/')
        if self.base_path and self.base_path != '/':
            return f"{self.base_path.rstrip('/')}/{user_path}".rstrip('/')
        return f"/{user_path}".rstrip('/') or '/'

    def _to_user_path(self, real_path):
        if self.base_path and real_path.startswith(self.base_path):
            return real_path[len(self.base_path):] or '/'
        return real_path

    # ── URL 生成 ─────────────────────────────────────────────

    def _extract_urls(self, raw_url):
        """从 raw_url 提取预览链接和下载直链"""
        if not raw_url:
            return None, None
        # raw_url 格式: {url}/p{path}?sign={sign}
        # 预览链接: {url}{path} (去掉 /p 前缀和 ?sign=xxx)
        # 下载直链: raw_url 本身
        parsed = urllib.parse.urlparse(raw_url)
        path = parsed.path  # /p/private/storage/file.txt
        if path.startswith('/p'):
            preview_path = path[2:]  # /private/storage/file.txt
        else:
            preview_path = path
        preview_url = f"{parsed.scheme}://{parsed.netloc}{preview_path}"
        return preview_url, raw_url

    # ── HTTP 请求（带自动刷新） ───────────────────────────────

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.url}{endpoint}"
        headers = kwargs.pop('headers', {})
        if self.token:
            headers['Authorization'] = self.token
        headers.setdefault('Content-Type', 'application/json')

        resp = requests.request(method, url, headers=headers, **kwargs)
        data = resp.json()

        if self._check_and_refresh_auth(data):
            headers['Authorization'] = self.token
            resp = requests.request(method, url, headers=headers, **kwargs)
            data = resp.json()

        return data

    # ── 文件操作 ──────────────────────────────────────────────

    def whoami(self):
        data = self._request('GET', '/api/me')
        if data['code'] == 200:
            user = data['data']
            print(f"用户: {user['username']}")
            print(f"ID: {user['id']}")
            print(f"根目录 (base_path): {user.get('base_path', '/')}")
            print(f"用户视角根目录: /")
            return user
        print(f"❌ {data['message']}")
        return None

    def ls(self, path="/", page=1, per_page=20):
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/list', json={
            "path": real_path, "password": "", "page": page,
            "per_page": per_page, "refresh": False
        })
        if data['code'] != 200:
            print(f"❌ {data['message']}")
            return []

        files = data['data']['content']
        total = data['data']['total']
        print(f"📂 {path} ({total} items)\n")

        for f in files:
            icon = "📁" if f['is_dir'] else "📄"
            size = f.get('size', 0)
            size_str = self._format_size(size) if not f['is_dir'] else ""
            print(f"  {icon} {f['name']} {size_str}")
        return files

    def get(self, path):
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/get', json={
            "path": real_path, "password": ""
        })
        if data['code'] != 200:
            print(f"❌ {data['message']}")
            return None

        f = data['data']
        print(f"📄 {f['name']}")
        print(f"   用户路径: {path}")
        print(f"   实际路径: {real_path}")
        print(f"   大小: {self._format_size(f.get('size', 0))}")
        print(f"   类型: {'文件夹' if f['is_dir'] else '文件'}")
        print(f"   修改: {f.get('modified', '')}")
        # URL 输出
        raw_url = f.get('raw_url', '')
        if not f['is_dir'] and raw_url:
            preview, download = self._extract_urls(raw_url)
            print(f"   预览: {preview}")
            print(f"   下载: {download}")
        return f

    def mkdir(self, path):
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/mkdir', json={"path": real_path})
        if data['code'] == 200:
            print(f"✅ 已创建文件夹: {path}")
            return True
        print(f"❌ {data['message']}")
        return False

    def upload(self, local_path, remote_path):
        if not os.path.exists(local_path):
            print(f"❌ 文件不存在: {local_path}")
            return False

        real_path = self._to_real_path(remote_path)

        with open(local_path, 'rb') as f:
            data = self._request('PUT', '/api/fs/put',
                headers={
                    "File-Path": urllib.parse.quote(real_path),
                    "Content-Type": "application/octet-stream"
                },
                data=f
            )

        if data['code'] == 200:
            print(f"✅ 上传成功!")
            print(f"   用户路径: {remote_path}")
            print(f"   实际路径: {real_path}")
            file_info = self._request('POST', '/api/fs/get', json={
                "path": real_path, "password": ""
            })
            if file_info['code'] == 200:
                raw_url = file_info['data'].get('raw_url', '')
                if raw_url:
                    preview, download = self._extract_urls(raw_url)
                    print(f"   预览: {preview}")
                    print(f"   下载: {download}")
            return True
        print(f"❌ {data['message']}")
        return False

    def rm(self, path):
        real_path = self._to_real_path(path)
        parts = real_path.rsplit('/', 1)
        if len(parts) == 2:
            dir_path, name = parts
        else:
            dir_path = "/"
            name = real_path

        data = self._request('POST', '/api/fs/remove', json={
            "dir": dir_path, "names": [name]
        })
        if data['code'] == 200:
            print(f"✅ 已删除: {path}")
            return True
        print(f"❌ {data['message']}")
        return False

    def mv(self, src, dst):
        real_src = self._to_real_path(src)
        real_dst = self._to_real_path(dst)

        src_dir = real_src.rsplit('/', 1)[0] or "/"
        name = real_src.split('/')[-1]

        data = self._request('POST', '/api/fs/move', json={
            "src_dir": src_dir,
            "dst_dir": real_dst if real_dst.endswith('/') else real_dst + '/',
            "names": [name]
        })
        if data['code'] == 200:
            print(f"✅ 已移动: {src} -> {dst}")
            return True
        print(f"❌ {data['message']}")
        return False

    def search(self, keyword, path="/"):
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/search', json={
            "parent": real_path,
            "keywords": keyword,
            "scope": 0,
            "page": 1,
            "per_page": 20,
            "password": ""
        })
        if data['code'] != 200:
            print(f"❌ {data['message']}")
            return []

        files = data['data']['content']
        print(f"🔍 搜索 '{keyword}' 在 {path}:\n")

        for f in files:
            icon = "📁" if f['is_dir'] else "📄"
            parent = f.get('parent', '')
            user_parent = self._to_user_path(parent)
            print(f"  {icon} {user_parent}/{f['name']}")
        return files

    def get_urls(self, path):
        """输出文件/文件夹的所有可用 URL"""
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/get', json={
            "path": real_path, "password": ""
        })
        if data['code'] != 200:
            print(f"❌ {data['message']}")
            return None

        f = data['data']
        print(f"📄 {f['name']}")
        raw_url = f.get('raw_url', '')
        if not f['is_dir'] and raw_url:
            preview, download = self._extract_urls(raw_url)
            print(f"   预览: {preview}")
            print(f"   下载: {download}")
        return f

    @staticmethod
    def _format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"


def main():
    parser = argparse.ArgumentParser(description="AList CLI - 文件管理工具")
    parser.add_argument("command", choices=["login", "ls", "get", "mkdir", "upload", "rm", "mv", "search", "url", "whoami"])
    parser.add_argument("args", nargs="*", help="命令参数")

    args = parser.parse_args()

    if args.command == "login":
        username = args.args[0] if len(args.args) > 0 else os.environ.get(ENV_USERNAME, "")
        password = args.args[1] if len(args.args) > 1 else os.environ.get(ENV_PASSWORD, "")
        if not username or not password:
            print(f"❌ 请提供用户名和密码，或设置环境变量 {ENV_USERNAME} 和 {ENV_PASSWORD}")
            sys.exit(1)
        url = os.environ.get(ENV_URL, "")
        if not url:
            print(f"❌ 请设置 {ENV_URL} 环境变量")
            sys.exit(1)
        alist = AList.__new__(AList)
        alist.url = url.rstrip('/')
        alist.token = ""
        alist.base_path = ""
        alist.login(username, password)
        return

    alist = AList()

    if args.command == "whoami":
        alist.whoami()
    elif args.command == "ls":
        alist.ls(args.args[0] if args.args else "/")
    elif args.command == "get":
        if not args.args:
            print("用法: alist get <path>"); sys.exit(1)
        alist.get(args.args[0])
    elif args.command == "mkdir":
        if not args.args:
            print("用法: alist mkdir <path>"); sys.exit(1)
        alist.mkdir(args.args[0])
    elif args.command == "upload":
        if len(args.args) < 2:
            print("用法: alist upload <local_path> <remote_path>"); sys.exit(1)
        alist.upload(args.args[0], args.args[1])
    elif args.command == "rm":
        if not args.args:
            print("用法: alist rm <path>"); sys.exit(1)
        alist.rm(args.args[0])
    elif args.command == "mv":
        if len(args.args) < 2:
            print("用法: alist mv <src> <dst>"); sys.exit(1)
        alist.mv(args.args[0], args.args[1])
    elif args.command == "search":
        if not args.args:
            print("用法: alist search <keyword> [path]"); sys.exit(1)
        alist.search(args.args[0], args.args[1] if len(args.args) > 1 else "/")
    elif args.command == "url":
        if not args.args:
            print("用法: alist url <path>"); sys.exit(1)
        alist.get_urls(args.args[0])


if __name__ == "__main__":
    main()
