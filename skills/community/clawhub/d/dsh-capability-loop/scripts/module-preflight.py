#!/usr/bin/env python3
"""交接前置检查：目标工程内是否已存在同名/相似模块（防重复开发、防路由冲突）。

用法：
  python module-preflight.py --project <工程根> --keyword "资源需求" --alias resource-demand resourceDemand
退出码：0=NONE（默认新建路由）、1=EXISTS（必须先与开发者确认）、3=WEAK（存在相似线索，需确认）、2=参数错误。
"""
import argparse, json, os, sys

def norm(s: str) -> str:
    return "".join(ch for ch in s.lower() if ch.isalnum())

def collect_roots(project):
    views, apis = [], []
    p = os.path.join(project, "src", "views")
    if os.path.isdir(p): views.append(p)
    p = os.path.join(project, "src", "api")
    if os.path.isdir(p): apis.append(p)
    apps = os.path.join(project, "apps")
    if os.path.isdir(apps):
        for app in sorted(os.listdir(apps)):
            v = os.path.join(apps, app, "src", "views")
            a = os.path.join(apps, app, "src", "api")
            if os.path.isdir(v): views.append(v)
            if os.path.isdir(a): apis.append(a)
    return views, apis

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--keyword", required=True)
    ap.add_argument("--alias", nargs="*", default=[])
    ap.add_argument("--menu-dump", default="")
    ap.add_argument("--route-hint", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    project = os.path.abspath(args.project)
    if not os.path.isdir(project):
        print("[ERROR] project not found:", project); sys.exit(2)

    keys = []
    for t in [args.keyword] + args.alias:
        k = norm(t)
        if k and k not in keys: keys.append(k)
    print("[INFO] project=", project)
    print("[INFO] keys=", "|".join(keys))

    views, apis = collect_roots(project)
    print("[INFO] views=", len(views), "apis=", len(apis))
    exact, weak = [], []

    for root in views:
        for cur, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d != "node_modules"]
            rel = os.path.relpath(cur, root)
            if rel == ".": continue
            segs = rel.split(os.sep)
            if len(segs) > 5: dirs[:] = []; continue
            last_key = norm(segs[-1]); whole_key = norm(rel)
            if any(last_key == k or whole_key == k for k in keys):
                exact.append("view|" + rel)
            elif any(len(k) >= 4 and (k in last_key or k in whole_key) for k in keys):
                weak.append("view-name|" + rel)

    for root in apis:
        for cur, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d != "node_modules"]
            rel = os.path.relpath(cur, root)
            if rel == ".": continue
            segs = rel.split(os.sep)
            if len(segs) > 5: dirs[:] = []; continue
            if norm(segs[-1]) in keys: exact.append("api|" + rel)

    router_dirs = []
    apps = os.path.join(project, "apps")
    if os.path.isdir(apps):
        for app in sorted(os.listdir(apps)):
            r = os.path.join(apps, app, "src", "router")
            if os.path.isdir(r): router_dirs.append(r)
    r2 = os.path.join(project, "src", "router")
    if os.path.isdir(r2): router_dirs.append(r2)
    for rr in router_dirs:
        for cur, dirs, files in os.walk(rr):
            dirs[:] = [d for d in dirs if d != "node_modules"]
            for f in files:
                fp = os.path.join(cur, f)
                try:
                    txt = open(fp, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                relf = os.path.relpath(fp, project)
                if args.keyword in txt:
                    weak.append("router-keyword|" + relf)
                for a in args.alias:
                    if len(a) >= 4 and a.lower() in txt.lower():
                        weak.append("router-alias|" + relf + "|" + a); break

    if args.menu_dump and os.path.isfile(args.menu_dump):
        try:
            mt = open(args.menu_dump, encoding="utf-8", errors="ignore").read()
            if args.keyword in mt: exact.append("menu|" + os.path.abspath(args.menu_dump))
        except Exception:
            pass

    verdict = "EXISTS" if exact else ("WEAK" if weak else "NONE")
    lines = ["# 模块/路由预检报告", "",
             "- 工程：" + project,
             "- 关键词：" + args.keyword + "；别名：" + ", ".join(args.alias),
             "- 结论：" + verdict, ""]
    if verdict == "EXISTS":
        lines.append("已存在同名模块，**未与开发者确认前不得默认新建**。请确认：复用现有 / 改造现有 / 另建（另建须说明理由与路由不冲突）。")
        lines += ["- " + h for h in exact]
    elif verdict == "WEAK":
        lines.append("存在相似模块或路由线索，请先确认能否复用，避免重复建设。")
        lines += ["- " + h for h in weak[:12]]
    else:
        lines.append("工程内未发现同名模块，**默认按新建路由开发**；建议先建 views/api 目录占位再交给 Trae。")
        if args.route_hint: lines.append("- 建议路由：" + args.route_hint)
    lines += ["", "纪律：EXISTS 未确认不得进实现；NONE 默认新建；WEAK 先确认复用可行性。"]
    report = "\n".join(lines)
    out = args.out
    if not out:
        tmp = os.path.join(project, ".tmp", "module-preflight")
        os.makedirs(tmp, exist_ok=True)
        out = os.path.join(tmp, "module-preflight-report.md")
    else:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "w", encoding="utf-8").write(report)
    print()
    print(report)
    print("[INFO] report=", out)
    sys.exit(1 if verdict == "EXISTS" else (3 if verdict == "WEAK" else 0))

if __name__ == "__main__":
    main()