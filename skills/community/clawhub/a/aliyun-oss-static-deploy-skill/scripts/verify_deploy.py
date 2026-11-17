#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""部署后的语义验收：对着真实线上 URL 断言，而不是比字节数。

为什么需要：数据每天都在涨，比 `wc -c` 分不清是「没部署」还是「部署了但数据变了」。
这里断言的都是**不会因为数据增长而失效**的东西——根路径是否返回 XML（静态托管是否生效）、
入口页是否含本次构建的标记、详情页是否真内联了正文、公开版有没有夹带未核实数据。

零第三方依赖（纯 stdlib urllib）。

用法：
    python verify_deploy.py --base-url https://demo.example.com
    python verify_deploy.py --base-url https://demo.example.com \
        --expect-text 'schema_version' --expect-text 'generated_at' \
        --forbid-text '<?xml' --min-bytes 20000
    python verify_deploy.py --base-url https://d.example.com \
        --pages-file pages.txt --check-seo
    python verify_deploy.py --base-url https://d.example.com \
        --data-json data.json --expect-cases 42

退出码：0 全部通过；1 有失败项
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PROXY_KEYS = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
              "ALL_PROXY", "all_proxy"]


def log(msg):
    print("[%s] %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg), flush=True)


def fetch(url, timeout=20):
    """返回 (status, body_bytes)。缓存友好：显式要求源站别给旧对象。"""
    req = urllib.request.Request(url, headers={
        "User-Agent": "verify-deploy/1.0",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        return e.code, body
    except Exception as e:
        return 0, str(e).encode()


def main():
    ap = argparse.ArgumentParser(description="静态站部署后的语义验收")
    ap.add_argument("--base-url", required=True, help="站点根 URL，如 https://demo.example.com")
    ap.add_argument("--index", default="/", help="入口页路径，默认 /")
    ap.add_argument("--pages", default="", help="要检查的路径，逗号分隔")
    ap.add_argument("--pages-file", default="", help="要检查的路径清单文件，每行一个")
    ap.add_argument("--expect-text", action="append", default=[],
                    help="入口页必须包含的字符串（语义标记），可重复")
    ap.add_argument("--forbid-text", action="append", default=[],
                    help="入口页禁止出现的字符串，可重复")
    ap.add_argument("--xml-root-is-fail", action="store_true",
                    help="根路径返回 XML 即判失败（静态托管是否真正生效）")
    ap.add_argument("--min-bytes", type=int, default=0, help="页面最小字节数")
    ap.add_argument("--data-json", default="", help="要校验的数据文件路径，如 data.json")
    ap.add_argument("--expect-cases", type=int, default=-1,
                    help="期望的数据条数；案例数会涨，请从外部传入而不是写死")
    ap.add_argument("--expect-json-field", action="append", default=[],
                    help="数据文件必须存在的字段，可重复")
    ap.add_argument("--check-seo", action="store_true", help="顺带校验 robots.txt / sitemap.xml")
    ap.add_argument("--keep-proxy", action="store_true",
                    help="保留代理环境变量（默认清除，本机代理会让 urllib 报 502）")
    args = ap.parse_args()

    if not args.keep_proxy:
        removed = [k for k in PROXY_KEYS if os.environ.pop(k, None) is not None]
        if removed:
            log("已清除代理环境变量：%s" % ", ".join(removed))

    base = args.base_url.rstrip("/")
    fails, checks = [], 0

    # 1) 入口页
    url = base + args.index
    status, body = fetch(url)
    text = body.decode("utf-8", "ignore")
    log("入口页 %s -> HTTP %s (%d 字节)" % (url, status, len(body)))
    checks += 1
    if status != 200:
        fails.append("入口页状态码 %s（期望 200）" % status)

    if args.xml_root_is_fail:
        checks += 1
        if text.lstrip().startswith("<?xml"):
            fails.append("根路径返回 XML 对象列表 —— 静态网站托管没生效")
            log("  ✗ 返回的是 XML（静态托管未生效）")
        else:
            log("  ✓ 非 XML，静态托管生效")

    for t in args.expect_text:
        checks += 1
        ok = t in text
        log("  %s 必须包含：%s" % ("✓" if ok else "✗", t))
        if not ok:
            fails.append("入口页缺少语义标记：%s" % t)
    for t in args.forbid_text:
        checks += 1
        ok = t not in text
        log("  %s 禁止出现：%s" % ("✓" if ok else "✗", t))
        if not ok:
            fails.append("入口页出现了不该有的内容：%s" % t)

    # 2) 详情页
    pages = [p.strip() for p in args.pages.split(",") if p.strip()]
    if args.pages_file:
        pages += [l.strip() for l in open(args.pages_file, encoding="utf-8")
                  if l.strip() and not l.startswith("#")]
    pages = [p if p.startswith("/") else "/" + p for p in pages]
    for p in pages:
        checks += 1
        st, bb = fetch(base + p)
        ok = st == 200 and (args.min_bytes <= 0 or len(bb) >= args.min_bytes)
        note = "" if ok else "（状态码 %s / %d 字节）" % (st, len(bb))
        log("  %s %s -> HTTP %s (%d 字节) %s" % ("✓" if ok else "✗", p, st, len(bb), note))
        if not ok:
            fails.append("页面 %s 校验失败：HTTP %s, %d 字节" % (p, st, len(bb)))

    # 3) 数据文件
    if args.data_json:
        path = args.data_json if args.data_json.startswith("/") else "/" + args.data_json
        st, bb = fetch(base + path)
        checks += 1
        log("数据文件 %s -> HTTP %s (%d 字节)" % (path, st, len(bb)))
        if st != 200:
            fails.append("数据文件 %s 不可用：HTTP %s" % (path, st))
        else:
            try:
                d = json.loads(bb.decode("utf-8"))
                log("  ✓ JSON 可解析")
                for f in args.expect_json_field:
                    checks += 1
                    ok = f in d or isinstance(d, dict) and f in d.get("site", {})
                    log("  %s 字段存在：%s" % ("✓" if ok else "✗", f))
                    if not ok:
                        fails.append("数据文件缺少字段：%s" % f)
                if isinstance(d, dict):
                    # 常见命名都照顾到，找不到就跳过而不是误报
                    n = None
                    for key in ("cases", "items", "records", "posts", "count"):
                        if isinstance(d.get(key), list):
                            n = len(d[key]); k = key; break
                    if n is not None:
                        log("  ℹ %s 条数 = %d" % (k, n))
                        if args.expect_cases >= 0:
                            checks += 1
                            ok = n == args.expect_cases
                            log("  %s 条数断言（期望 %d）" % ("✓" if ok else "✗", args.expect_cases))
                            if not ok:
                                fails.append("%s 条数 %d != 期望 %d" % (k, n, args.expect_cases))
                    # 公开版不该夹带未核实数据
                    inbox = d.get("inbox")
                    if inbox is not None:
                        checks += 1
                        ok = (inbox == 0 or (isinstance(inbox, list) and len(inbox) == 0))
                        log("  %s 公开版 inbox 为空" % ("✓" if ok else "✗"))
                        if not ok:
                            fails.append("公开产物里含未核实数据 inbox=%s" % inbox)
            except Exception as e:
                fails.append("数据文件 JSON 解析失败：%s" % e)
                log("  ✗ JSON 解析失败：%s" % e)

    # 4) SEO 附件
    if args.check_seo:
        for p in ("/robots.txt", "/sitemap.xml"):
            checks += 1
            st, bb = fetch(base + p)
            ok = st == 200
            # 没有 robots/sitemap 不算致命错误，只提示
            log("  %s %s -> HTTP %s" % ("✓" if ok else "!", p, st))
            if not ok:
                log("    （%s 缺失不算致命，按需补）" % p)

    log("———— 共 %d 项检查 ————" % checks)
    if fails:
        for f in fails:
            log("✗ %s" % f)
        log("验收失败：%d 项不通过" % len(fails))
        sys.exit(1)
    log("✓ 验收通过")


if __name__ == "__main__":
    main()
