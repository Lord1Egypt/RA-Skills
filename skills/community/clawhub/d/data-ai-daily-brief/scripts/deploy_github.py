# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — GitHub Pages 部署脚本
自动查找当天日报 HTML，部署到 GitHub Pages。

用法:
  python deploy_github.py                     # 部署今天的日报
  python deploy_github.py 2026-03-10          # 部署指定日期的日报

环境变量:
  GITHUB_TOKEN       — GitHub Personal Access Token（需要 repo 权限）
  GITHUB_USER        — GitHub 用户名
  GITHUB_REPO        — 目标仓库名（默认 data-ai-daily）
"""
import json
import base64
import ssl
import urllib.request
import urllib.error
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_DIR / "daily-brief-config.json"

API_BASE = "https://api.github.com"
ctx = ssl.create_default_context()


def load_config():
    """加载配置文件。"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_github_config(args):
    """获取 GitHub 配置。"""
    token = args.token or os.environ.get("GITHUB_TOKEN", "")
    user = args.user or os.environ.get("GITHUB_USER", "")
    repo = args.repo or os.environ.get("GITHUB_REPO", "data-ai-daily")

    if not token:
        print("[错误] 未设置 GITHUB_TOKEN")
        print("  请运行: set GITHUB_TOKEN=ghp_xxxxx")
        sys.exit(1)

    if not user:
        print("[错误] 未设置 GITHUB_USER")
        print("  请运行: set GITHUB_USER=your_username")
        sys.exit(1)

    return token, user, repo


def find_html(date_str, search_dirs=None):
    """查找指定日期的 HTML 日报文件。"""
    if search_dirs is None:
        search_dirs = [PROJECT_DIR, Path(".")]

    patterns = [
        f"Data+AI全球日报_{date_str}.html",
        f"Data+AI全球日报_{date_str}_v3.html",
        f"Data+AI全球日报_{date_str}_v2.html",
    ]
    for directory in search_dirs:
        for name in patterns:
            path = directory / name
            if path.exists():
                return path
    return None


def api_request(method, url, data=None, token=""):
    """Make GitHub API request."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DataAI-Daily-Deploy",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    else:
        body = None

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8")), resp.status
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
        except Exception:
            err_json = {"message": err_body}
        return err_json, e.code


def step(msg):
    print(f"\n{'='*55}")
    print(f"  {msg}")
    print(f"{'='*55}")


def main():
    parser = argparse.ArgumentParser(description="Data+AI 日报 GitHub Pages 部署")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--token", help="GitHub Token")
    parser.add_argument("--user", help="GitHub 用户名")
    parser.add_argument("--repo", help="GitHub 仓库名")
    parser.add_argument("--search-dir", action="append", help="额外搜索目录")
    args = parser.parse_args()

    # 确定日期
    if args.date:
        try:
            dt = datetime.strptime(args.date, "%Y-%m-%d")
            date_str = dt.strftime("%Y-%m-%d")
        except ValueError:
            print(f"[错误] 日期格式无效: {args.date}，应为 YYYY-MM-DD")
            sys.exit(1)
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    token, github_user, repo_name = get_github_config(args)

    # 搜索目录
    search_dirs = [PROJECT_DIR, Path(".")]
    if args.search_dir:
        search_dirs.extend(Path(d) for d in args.search_dir)

    step(f"Data+AI Daily Brief — 部署 {date_str}")

    # 1. Find HTML file
    html_path = find_html(date_str, search_dirs)
    if not html_path:
        print(f"  [错误] 未找到 {date_str} 的 HTML 日报文件")
        sys.exit(1)
    print(f"  文件: {html_path.name}")

    # 2. Check / create repo
    step("1. Checking repo...")
    resp, code = api_request("GET", f"{API_BASE}/repos/{github_user}/{repo_name}", token=token)
    if code == 200:
        print(f"  Repo exists: {resp.get('html_url')}")
    elif code == 404:
        print("  Creating repo...")
        resp, code = api_request("POST", f"{API_BASE}/user/repos", {
            "name": repo_name,
            "description": "Data+AI Global Daily Report",
            "homepage": f"https://{github_user}.github.io/{repo_name}/",
            "public": True,
            "auto_init": True,
            "has_pages": True,
        }, token=token)
        if code in (200, 201):
            print(f"  Repo created: {resp.get('html_url')}")
        else:
            print(f"  ERROR: {code} - {resp}")
            sys.exit(1)

    # 3. Read & encode HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    encoded = base64.b64encode(html_content.encode("utf-8")).decode("ascii")
    print(f"  Read {len(html_content)} chars")

    # 4. Upload index.html
    step("2. Uploading index.html...")
    file_url = f"{API_BASE}/repos/{github_user}/{repo_name}/contents/index.html"
    existing, ecode = api_request("GET", file_url, token=token)
    upload_data = {
        "message": f"Deploy: Data+AI daily report {date_str}",
        "content": encoded,
        "branch": "main",
    }
    if ecode == 200 and "sha" in existing:
        upload_data["sha"] = existing["sha"]
    resp, code = api_request("PUT", file_url, upload_data, token=token)
    if code in (200, 201):
        print("  index.html OK")
    else:
        print(f"  ERROR: {code} - {resp}")
        sys.exit(1)

    # 5. Upload archive
    step("3. Archiving...")
    archive_url = f"{API_BASE}/repos/{github_user}/{repo_name}/contents/archive/{date_str}.html"
    existing2, ecode2 = api_request("GET", archive_url, token=token)
    archive_data = {
        "message": f"Archive: {date_str}",
        "content": encoded,
        "branch": "main",
    }
    if ecode2 == 200 and "sha" in existing2:
        archive_data["sha"] = existing2["sha"]
    resp2, code2 = api_request("PUT", archive_url, archive_data, token=token)
    if code2 in (200, 201):
        print(f"  archive/{date_str}.html OK")
    else:
        print(f"  Warning: {code2}")

    # 6. Ensure GitHub Pages
    step("4. Checking GitHub Pages...")
    pages_url = f"{API_BASE}/repos/{github_user}/{repo_name}/pages"
    pages_resp, pages_code = api_request("GET", pages_url, token=token)
    if pages_code == 200:
        print("  Pages already enabled")
    else:
        pages_resp, pages_code = api_request("POST", pages_url, {
            "source": {"branch": "main", "path": "/"}
        }, token=token)
        if pages_code in (200, 201):
            print("  Pages enabled!")
        else:
            print(f"  Note: enable Pages manually if needed ({pages_code})")

    # 7. Done
    step("DONE!")
    print(f"  Repository:  https://github.com/{github_user}/{repo_name}")
    print(f"  Public page: https://{github_user}.github.io/{repo_name}/")
    print(f"  Archive:     archive/{date_str}.html")
    print(f"\n  GitHub Pages may take 1-2 min to update.")


if __name__ == "__main__":
    main()
