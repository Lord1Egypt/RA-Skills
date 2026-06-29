from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from urllib.parse import quote

import requests

COMMON_MODULE_VERSION = "paperkb-v3.0"


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    here = Path(__file__).resolve().parent
    for candidate in (here / ".env", here.parent / ".env"):
        if candidate.exists():
            load_dotenv(candidate)
            return


_load_env()

GITEA_URL = os.environ.get("GITEA_URL", "").rstrip("/")
ADMIN_TOKEN = os.environ.get("GITEA_ADMIN_TOKEN", "")
BOT_USERNAME = os.environ.get("GITEA_BOT_USERNAME", "AIFusionBot")


class GiteaError(Exception):
    pass


def headers() -> dict:
    return {"Authorization": f"token {ADMIN_TOKEN}", "Content-Type": "application/json"}


def api(method: str, path: str, *, json_body: dict | None = None, params: dict | None = None,
        ok: tuple[int, ...] = (200, 201, 204)):
    if not GITEA_URL:
        raise GiteaError("GITEA_URL is not configured")
    resp = requests.request(
        method, f"{GITEA_URL}/api/v1{path}", headers=headers(),
        json=json_body, params=params, timeout=30,
    )
    data = None
    if resp.content:
        try:
            data = resp.json()
        except ValueError:
            data = resp.text
    if resp.status_code not in ok:
        raise GiteaError(f"{method} {path} failed HTTP {resp.status_code}: {data}")
    return data


def token_is_site_admin() -> bool:
    try:
        api("GET", "/admin/users", params={"limit": 1})
        return True
    except GiteaError:
        return False


def get_user(username: str) -> dict | None:
    try:
        return api("GET", f"/users/{username}")
    except GiteaError:
        return None


def repo_exists(owner: str, repo: str) -> bool:
    try:
        api("GET", f"/repos/{owner}/{repo}")
        return True
    except GiteaError:
        return False


def get_repo(owner: str, repo: str) -> dict | None:
    try:
        return api("GET", f"/repos/{owner}/{repo}")
    except GiteaError:
        return None


def default_branch(owner: str, repo: str) -> str:
    data = get_repo(owner, repo) or {}
    return data.get("default_branch") or "main"


def get_branch(owner: str, repo: str, branch: str) -> dict | None:
    try:
        return api("GET", f"/repos/{owner}/{repo}/branches/{quote(branch, safe='')}")
    except GiteaError:
        return None


def branch_commit_sha(owner: str, repo: str, branch: str) -> str:
    data = get_branch(owner, repo, branch)
    if not data:
        return branch
    commit = data.get("commit") or {}
    return commit.get("id") or commit.get("sha") or branch


def create_repo_for_user(username: str, name: str, description: str, private: bool = True) -> dict:
    if repo_exists(username, name):
        return {"created": False, "html_url": f"{GITEA_URL}/{username}/{name}"}
    data = api("POST", f"/admin/users/{username}/repos", json_body={
        "name": name, "private": private, "description": description,
        "auto_init": True, "default_branch": "main",
    })
    return {"created": True, "html_url": data.get("html_url", f"{GITEA_URL}/{username}/{name}")}


def create_bot_repo(name: str, description: str, private: bool = True) -> dict:
    if repo_exists(BOT_USERNAME, name):
        return {"created": False, "html_url": f"{GITEA_URL}/{BOT_USERNAME}/{name}"}
    data = api("POST", "/user/repos", json_body={
        "name": name, "private": private, "description": description,
        "auto_init": True, "default_branch": "main",
    })
    return {"created": True, "html_url": data.get("html_url", f"{GITEA_URL}/{BOT_USERNAME}/{name}")}


def add_collaborator(owner: str, repo: str, username: str, permission: str) -> None:
    api("PUT", f"/repos/{owner}/{repo}/collaborators/{username}", json_body={"permission": permission}, ok=(204, 201, 200))


def get_file(owner: str, repo: str, path: str, ref: str | None = None) -> tuple[str, str] | None:
    try:
        params = {"ref": ref} if ref else None
        data = api("GET", f"/repos/{owner}/{repo}/contents/{path}", params=params)
    except GiteaError:
        return None
    if isinstance(data, dict) and data.get("content") is not None:
        return base64.b64decode(data["content"]).decode("utf-8"), data["sha"]
    return None


def get_content(owner: str, repo: str, path: str, ref: str | None = None) -> dict | None:
    try:
        params = {"ref": ref} if ref else None
        data = api("GET", f"/repos/{owner}/{repo}/contents/{path}", params=params)
    except GiteaError:
        return None
    return data if isinstance(data, dict) else None


def get_file_bytes(owner: str, repo: str, path: str, ref: str | None = None) -> tuple[bytes, str] | None:
    data = get_content(owner, repo, path, ref=ref)
    if not data or data.get("content") is None:
        return None
    return base64.b64decode(data["content"]), data["sha"]


def put_file(owner: str, repo: str, path: str, content: str, message: str, sha: str | None = None) -> None:
    body = {"message": message, "content": base64.b64encode(content.encode("utf-8")).decode("ascii")}
    if sha:
        body["sha"] = sha
        api("PUT", f"/repos/{owner}/{repo}/contents/{path}", json_body=body)
    else:
        try:
            api("POST", f"/repos/{owner}/{repo}/contents/{path}", json_body=body)
        except GiteaError:
            existing = get_file(owner, repo, path)
            if not existing:
                raise
            put_file(owner, repo, path, content, message, existing[1])


def get_file_sha(owner: str, repo: str, path: str) -> str | None:
    data = get_content(owner, repo, path)
    return data.get("sha") if data else None


def put_file_bytes(owner: str, repo: str, path: str, raw: bytes, message: str) -> None:
    body = {"message": message, "content": base64.b64encode(raw).decode("ascii")}
    sha = get_file_sha(owner, repo, path)
    if sha:
        body["sha"] = sha
        api("PUT", f"/repos/{owner}/{repo}/contents/{path}", json_body=body)
    else:
        api("POST", f"/repos/{owner}/{repo}/contents/{path}", json_body=body)


def ensure_file(owner: str, repo: str, path: str, content: str, message: str) -> bool:
    if get_file(owner, repo, path):
        return False
    put_file(owner, repo, path, content, message)
    return True


def list_tree(owner: str, repo: str, ref: str | None = None, recursive: bool = True) -> list[dict]:
    branch = ref or default_branch(owner, repo)
    sha = branch_commit_sha(owner, repo, branch)
    data = api("GET", f"/repos/{owner}/{repo}/git/trees/{sha}", params={"recursive": str(recursive).lower()})
    return data.get("tree", []) if isinstance(data, dict) else []
