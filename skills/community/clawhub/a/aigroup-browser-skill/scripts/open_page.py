import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from typing import Any

CN_PORT = 18810
GLOBAL_PORT = 18800
CN_CMD = "/home/jack/.local/bin/oc-cn"
GLOBAL_CMD = "/home/jack/.local/bin/oc-global"
AUTO_CMD = "/home/jack/.local/bin/oc-browser"

CN_HOSTS = {
    "baidu.com", "www.baidu.com", "bilibili.com", "www.bilibili.com",
    "eastmoney.com", "www.eastmoney.com", "finance.eastmoney.com",
    "xiaohongshu.com", "www.xiaohongshu.com", "tianyancha.com", "www.tianyancha.com",
}


def fetch_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def list_pages(port: int) -> list[dict[str, Any]]:
    data = fetch_json(f"http://127.0.0.1:{port}/json/list")
    return [item for item in data if item.get("type") == "page"]


def choose(mode: str) -> tuple[str, str]:
    if mode == "cn":
        return CN_CMD, "cn"
    if mode == "global":
        return GLOBAL_CMD, "global"
    return AUTO_CMD, "auto"


def resolve_port(mode: str, url: str) -> int:
    if mode == "cn":
        return CN_PORT
    if mode == "global":
        return GLOBAL_PORT
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    return CN_PORT if host in CN_HOSTS else GLOBAL_PORT


def open_url(cmd: str, url: str) -> None:
    subprocess.run([cmd, url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def same_target(page_url: str, requested_url: str) -> bool:
    page_host = (urllib.parse.urlparse(page_url).hostname or "").lower()
    req_host = (urllib.parse.urlparse(requested_url).hostname or "").lower()
    return bool(page_host and req_host and page_host == req_host)


def pick_candidate(pages: list[dict[str, Any]], requested_url: str) -> dict[str, Any] | None:
    matching = [p for p in pages if same_target(p.get("url", ""), requested_url)]
    if not matching:
        return pages[0] if pages else None
    titled = [p for p in matching if (p.get("title") or "").strip()]
    return titled[0] if titled else matching[0]


def wait_for_page(port: int, requested_url: str, timeout: int) -> dict[str, Any]:
    deadline = time.time() + timeout
    fallback = None
    while time.time() < deadline:
        try:
            pages = list_pages(port)
        except Exception:
            time.sleep(1)
            continue
        candidate = pick_candidate(pages, requested_url)
        if candidate:
            fallback = candidate
            if (candidate.get("title") or "").strip():
                return candidate
        time.sleep(1)
    if fallback:
        return fallback
    raise RuntimeError("timed out waiting for page")


def read_request() -> dict[str, Any]:
    raw = sys.argv[1] if len(sys.argv) >= 2 else sys.stdin.read().strip()
    if not raw:
        print("Usage: open_page.py '<JSON>'", file=sys.stderr)
        raise SystemExit(1)
    return json.loads(raw)


def main() -> int:
    req = read_request()
    url = req.get("url")
    if not url or not isinstance(url, str):
        print("Error: url is required", file=sys.stderr)
        return 1
    mode = str(req.get("mode", "auto")).lower()
    timeout = int(req.get("timeout", 20))
    cmd, chosen_mode = choose(mode)
    port = resolve_port(mode, url)
    open_url(cmd, url)
    page = wait_for_page(port, url, timeout)
    effective_mode = chosen_mode if mode != "auto" else ("cn" if port == CN_PORT else "global")
    out = {
        "ok": True,
        "mode": effective_mode,
        "port": port,
        "title": (page.get("title") or "").strip(),
        "url": page.get("url", ""),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
