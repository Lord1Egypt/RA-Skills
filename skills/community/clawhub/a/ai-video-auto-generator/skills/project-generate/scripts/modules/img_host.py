"""
图片托管模块 — 上传图片到图床（默认 GitHub），返回公网直链。
图床提供者在 config.toml [img_host] 中配置，当前仅支持 github。
"""
from __future__ import annotations
import base64, json, os, time
from typing import Optional
from urllib.parse import quote
from urllib.request import Request, urlopen


_GH_HEADERS = {"User-Agent": "WorkBuddy/img_host"}


def _url_still_valid(url: str, timeout: int = 5) -> bool:
    """轻量 HEAD 请求验证 provider URL 是否仍可访问。过期则降级到图床上传。"""
    try:
        req = Request(url, method="HEAD", headers=_GH_HEADERS)
        with urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def _load_github_config() -> tuple[str, str]:
    """从 config.toml 读取 GitHub 仓库配置（集中配置入口）。"""
    from config import get_github_repo, get_github_branch
    return get_github_repo(), get_github_branch()

GITHUB_REPO, GITHUB_BRANCH = _load_github_config()
PROJECT_DIR = None
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒


def _load_token() -> Optional[str]:
    """加载 GitHub PAT（config.toml → ~/.github-pat → GITHUB_PAT）。"""
    from config import get_github_pat
    return get_github_pat()


def _retry(attempt: int, label: str = "") -> bool:
    """返回 True 应重试，False 应放弃。"""
    if attempt >= MAX_RETRIES:
        return False
    print(f"  [重试] {label} 第 {attempt + 1}/{MAX_RETRIES} 次...", flush=True)
    time.sleep(RETRY_DELAY)
    return True


def upload_image(local_path: str, remote_name: str | None = None, project: str | None = None) -> Optional[str]:
    """上传图片到 GitHub 仓库，返回 raw 直链。失败自动重试最多 3 次。"""
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError

    token = _load_token()
    if not token:
        return None

    if not os.path.isfile(local_path):
        return None

    # 优先使用 provider 返回的原始 URL（旁注文件），跳过 GitHub 上传
    url_sidecar = local_path + ".origin_url.txt"
    if os.path.isfile(url_sidecar):
        with open(url_sidecar, encoding="utf-8") as f:
            provider_url = f.read().strip()
        if provider_url and _url_still_valid(provider_url):
            print(f"  [图床] 使用 provider URL: {provider_url[:60]}...", flush=True)
            return provider_url
        else:
            # URL 已过期或不可达，降级到 GitHub 上传
            try:
                os.remove(url_sidecar)
                    print(f"  [图床] provider URL 已过期或不可达，删除 .origin_url.txt 旁注，降级到图床上传", flush=True)
            except OSError:
                pass

    proj = os.path.basename(os.path.abspath(project)) if project else (os.environ.get("BUDDY_PROJECT") or "default")
    if not project and not os.environ.get("BUDDY_PROJECT"):
        print(f"  ⚠️ upload_image: project=None，使用'default'（检查调用方是否漏传 project）", flush=True)
    encoded_proj = quote(proj, safe="")
    remote_name = remote_name or os.path.basename(local_path)
    remote_path = f"{proj}/{remote_name}"
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{quote(remote_path, safe='')}"
    raw_prefix = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{encoded_proj}/"

    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # 检查文件是否已存在，获取 sha
            sha = None
            get_req = Request(api_url, headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            }, method="GET")
            try:
                with urlopen(get_req, timeout=15) as resp:
                    existing = json.loads(resp.read().decode())
                    sha = existing.get("sha")
                    if sha:
                        raw_url = raw_prefix + remote_name
                        print(f"  [图床] GitHub 已存在: {raw_url}")
                        return raw_url
            except HTTPError:
                pass

            # PUT 上传
            payload = {
                "message": f"upload {remote_name}",
                "content": content_b64,
                "branch": GITHUB_BRANCH,
            }
            if sha:
                payload["sha"] = sha

            data = json.dumps(payload).encode("utf-8")
            put_req = Request(api_url, data=data, headers={
                "Authorization": f"token {token}",
                "Content-Type": "application/json",
                "Accept": "application/vnd.github.v3+json",
            }, method="PUT")
            with urlopen(put_req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                if result.get("content", {}).get("name"):
                    raw_url = raw_prefix + remote_name
                    print(f"  [图床] GitHub: {raw_url}")
                    return raw_url
                return None

        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"  [ERROR] GitHub 上传失败 HTTP {e.code}: {body[:200]}")
            if e.code in (429, 500, 502, 503):
                if _retry(attempt, f"HTTP {e.code}"):
                    continue
            return None

        except Exception as e:
            err_name = type(e).__name__
            print(f"  [ERROR] GitHub 上传异常 ({err_name}): {e}")
            if _retry(attempt, str(e)[:60]):
                continue
            return None

    return None
