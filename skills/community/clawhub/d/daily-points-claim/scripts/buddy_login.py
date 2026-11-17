"""一次性登录：打开专用浏览器窗口 -> 你微信扫码 -> 自动把登录态写进 config.json。

之后每天的 claim.py 就能纯 HTTP 跑，不需要浏览器。
登录态（HttpOnly Cookie）只在本地 config.json 里，不外发。
"""
import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdp  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "config.json")
PROFILE = os.path.join(os.path.dirname(HERE), "browser-profile")
PORT = 9345
EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
STATUS_JS = """(async()=>{try{const r=await fetch('/billing/meter/checkin-status',{method:'POST',
credentials:'include',headers:{'Content-Type':'application/json'},body:'{}'});
return r.status+'|'+(await r.text()).slice(0,300);}catch(e){return 'ERR|'+e}})()"""


def find_edge():
    for p in EDGE_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("找不到 msedge.exe")


def save_cookie(cookie_str, sites=("buddy", "buddy-status")):
    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    n = 0
    for s in cfg.get("sites", []):
        if s.get("id") in sites:
            s["request"]["headers"]["Cookie"] = cookie_str
            n += 1
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=240, help="等待扫码的秒数")
    ap.add_argument("--headless", action="store_true", help="无头模式（仅用于验证已有登录态）")
    args = ap.parse_args()

    os.makedirs(PROFILE, exist_ok=True)
    cdp.kill_tree(PORT)
    time.sleep(1)
    cdp.launch_edge(find_edge(), PROFILE, PORT, headless=args.headless,
                    url="https://www.workbuddy.cn/app")
    if not cdp.wait_cdp(PORT, 40):
        raise SystemExit("浏览器没有起来，CDP 端口无响应")
    c = cdp.CDP(PORT)

    print("等待登录……（请在窗口里用微信扫码）", flush=True)
    deadline = time.time() + args.timeout
    ok = False
    while time.time() < deadline:
        try:
            raw = c.evaluate(STATUS_JS) or ""
        except Exception:
            raw = ""
        if raw and not raw.startswith("401") and not raw.startswith("ERR"):
            ok = True
            print("已登录。状态接口返回:", raw[:160], flush=True)
            break
        time.sleep(3)

    if not ok:
        print("超时：仍未检测到登录态", flush=True)
        cdp.kill_tree(PORT)
        return 3

    cookies = [k for k in c.cookies() if "workbuddy" in (k.get("domain") or "")]
    auth = [k for k in cookies if k.get("httpOnly")] or cookies
    if not auth:
        print("没有取到可用的登录 Cookie", flush=True)
        cdp.kill_tree(PORT)
        return 4
    cookie_str = "; ".join(f"{k['name']}={k['value']}" for k in auth)
    n = save_cookie(cookie_str)
    cdp.kill_tree(PORT)
    masked = re.sub(r"=([^;]{4})[^;]*", r"=\1***", cookie_str)
    print(f"已写入 config.json（{n} 个站点），Cookie 共 {len(auth)} 项：{masked[:120]}…", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
