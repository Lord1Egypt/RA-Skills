from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import requests


API = "https://api.github.com"
MAX_CHARS = int(os.environ.get("PAPERKB_MAX_CHARS", "60000"))
DEP_FILES = ["requirements.txt", "environment.yml", "pyproject.toml", "package.json", "Dockerfile", "setup.py"]


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def fail(error: str, message: str) -> None:
    out({"success": False, "error": error, "message": message})
    sys.exit(0)


def parse_repo(value: str) -> tuple[str, str] | None:
    s = value.strip().rstrip("/")
    m = re.search(r"github\.com[:/]([^/\s]+)/([^/\s]+?)(?:\.git)?(?:/.*)?$", s)
    if m:
        return m.group(1), m.group(2)
    m = re.fullmatch(r"([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", s)
    return (m.group(1), m.group(2)) if m else None


def headers() -> dict:
    h = {"Accept": "application/vnd.github+json", "User-Agent": "paper-kb-v3"}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def get_json(url: str):
    r = requests.get(url, headers=headers(), timeout=30)
    try:
        data = r.json()
    except ValueError:
        data = None
    return r.status_code, data


def raw(owner: str, repo: str, branch: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    try:
        r = requests.get(url, headers={"User-Agent": "paper-kb-v3"}, timeout=20)
    except requests.RequestException:
        return ""
    return r.text if r.status_code == 200 else ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    parsed = parse_repo(args.url)
    if not parsed:
        fail("invalid_github_url", "无法识别 GitHub 仓库链接。")
    owner, repo = parsed
    code, data = get_json(f"{API}/repos/{owner}/{repo}")
    if code == 404:
        fail("repo_not_found", "仓库不存在或为私有仓库。")
    if code != 200 or not isinstance(data, dict):
        fail("fetch_failed", f"获取仓库信息失败 HTTP {code}。")
    branch = data.get("default_branch") or "main"
    readme = ""
    for name in ["README.md", "readme.md", "README.rst", "README.txt", "README"]:
        readme = raw(owner, repo, branch, name)
        if readme.strip():
            break
    deps = {}
    for dep in DEP_FILES:
        text = raw(owner, repo, branch, dep)
        if text.strip():
            deps[dep] = text[:8000]
    parts = [
        f"# GitHub 仓库：{data.get('full_name', f'{owner}/{repo}')}",
        f"地址：{data.get('html_url')}",
        f"简介：{data.get('description') or ''}",
        f"主语言：{data.get('language') or ''}",
        f"Stars：{data.get('stargazers_count', 0)}",
        f"Forks：{data.get('forks_count', 0)}",
        f"Open issues：{data.get('open_issues_count', 0)}",
        f"最近提交：{(data.get('pushed_at') or '')[:10]}",
        "",
        "## README",
        readme or "（未获取到 README）",
        "",
        "## 依赖文件",
    ]
    for name, text in deps.items():
        parts += [f"### {name}", "```", text, "```"]
    full_text = "\n".join(parts)[:MAX_CHARS]
    tmp = Path(os.environ.get("TMP", "/tmp")) / "paperkb"
    tmp.mkdir(parents=True, exist_ok=True)
    text_path = tmp / f"github_{owner}_{repo}.txt"
    text_path.write_text(full_text, encoding="utf-8")
    out({
        "success": True,
        "full_name": data.get("full_name", f"{owner}/{repo}"),
        "url": data.get("html_url"),
        "description": data.get("description") or "",
        "language": data.get("language") or "",
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "pushed_at": (data.get("pushed_at") or "")[:10],
        "license": (data.get("license") or {}).get("spdx_id", "") if isinstance(data.get("license"), dict) else "",
        "archived": bool(data.get("archived")),
        "dep_files_found": list(deps),
        "has_readme": bool(readme.strip()),
        "text_path": str(text_path),
    })


if __name__ == "__main__":
    main()
