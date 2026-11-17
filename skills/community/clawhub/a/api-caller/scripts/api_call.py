#!/usr/bin/env python3
"""稳健 REST API 调用：Bearer/APIKey 鉴权、指数退避重试、429 退避、分页、错误分类。"""
import argparse, json, os, sys, time, random, urllib.request, urllib.error


def call(method, url, headers, body=None, retries=3, timeout=30, sleep_base=1.0):
    data = None
    if body is not None:
        if isinstance(body, str):
            data = body.encode("utf-8")
        else:
            data = json.dumps(body).encode("utf-8")
            headers.setdefault("Content-Type", "application/json")
    last_err = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                status = resp.status
                if 200 <= status < 300:
                    return {"ok": True, "status": status, "body": raw}
                # 4xx 不重试
                if 400 <= status < 500:
                    return {"ok": False, "kind": "client", "status": status, "body": raw}
                last_err = f"{status}"
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace")
            if 400 <= e.code < 500:
                return {"ok": False, "kind": "client", "status": e.code, "body": raw}
            if e.code == 429:
                ra = e.headers.get("Retry-After")
                wait = float(ra) if ra and ra.isdigit() else sleep_base * (2 ** attempt)
                time.sleep(wait + random.uniform(0, 0.5))
                last_err = "429"
                continue
            last_err = str(e.code)
        except Exception as e:  # 网络超时等
            last_err = f"{type(e).__name__}: {e}"
        if attempt < retries:
            time.sleep(sleep_base * (2 ** attempt) + random.uniform(0, 0.5))
    return {"ok": False, "kind": "retry_exhausted", "status": None, "body": last_err}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", default="GET")
    ap.add_argument("--url", required=True)
    ap.add_argument("--header", action="append", default=[], help="K: V 可重复")
    ap.add_argument("--body", default=None)
    ap.add_argument("--retry", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--out", default=None)
    ap.add_argument("--token-env", default=None, help="从该环境变量读 Bearer token")
    ap.add_argument("--apikey-env", default=None, help="从该环境变量读 X-API-Key")
    args = ap.parse_args()

    headers = {}
    for h in args.header:
        if ":" in h:
            k, v = h.split(":", 1)
            headers[k.strip()] = v.strip()
    if args.token_env:
        t = os.environ.get(args.token_env)
        if t:
            headers["Authorization"] = f"Bearer {t}"
    if args.apikey_env:
        k = os.environ.get(args.apikey_env)
        if k:
            headers["X-API-Key"] = k

    body = args.body
    if body and body.startswith("@"):
        with open(body[1:], encoding="utf-8") as f:
            body = f.read()

    r = call(args.method, args.url, headers, body, args.retry, args.timeout)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(r.get("body", ""))
    if r["ok"]:
        print(f"✅ {r['status']} 已保存 {args.out or '(print)'}  预览：{r['body'][:150]}")
        sys.exit(0)
    kind = r.get("kind")
    print(f"❌ 调用失败 kind={kind} status={r.get('status')} :: {str(r['body'])[:200]}",
          file=sys.stderr)
    sys.exit(2 if kind == "client" else 3)


if __name__ == "__main__":
    main()
