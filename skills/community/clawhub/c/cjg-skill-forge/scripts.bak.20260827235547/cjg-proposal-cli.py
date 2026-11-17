#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""藏经阁·易筋 进化提案 CLI（stdlib-only，随技能包分发）。

方案C：包内 cloud_config.json 仅含公网 URL（无 token）。
- list / get：需创作者 token（与 approve/reject 同源；防凭 slug 枚举读取他人提案）
- approve / reject：写操作，需创作者本地凭据
  （优先级：~/.workbuddy/data/skills/<slug>/.cloud_token -> 创作者开发环境 .deploy/cloud_open.json）
  绝不从包内文件读取 token。

用法:
  python cjg-proposal-cli.py list [--slug SLUG] [--status pending|all]
  python cjg-proposal-cli.py get  --id <proposal_id>
  python cjg-proposal-cli.py approve --id <proposal_id> [--note "..."]
  python cjg-proposal-cli.py reject  --id <proposal_id> [--note "..."]
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)


def _read(name):
    for base in (HERE, SKILL_DIR):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return open(p, encoding="utf-8").read().strip()
    return None


def _read_frontmatter(skill_md):
    if not os.path.exists(skill_md):
        return {}
    text = open(skill_md, encoding="utf-8").read()
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data


def _load_cfg():
    """读云端配置：仅 URL，不含 token（方案C：包零密钥）"""
    raw = _read("cloud_config.json")
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            pass
    return {}


def _read_local_token(slug):
    """创作者本地凭据（绝不选包内 token）。单点真相在技能包外的密钥库。"""
    if slug:
        p1 = os.path.expanduser(f"~/.workbuddy/data/skills/{slug}/.cloud_token")
        if os.path.exists(p1):
            return open(p1, encoding="utf-8").read().strip()
    # 统一密钥库（技能包外 ~/.workbuddy/secrets，绝不被发布工具打包）
    secret_store = os.path.expanduser("~/.workbuddy/secrets/cjg-evo/cloud_open.json")
    if os.path.exists(secret_store):
        try:
            cc = json.loads(open(secret_store, encoding="utf-8").read())
            t = cc.get("token") or cc.get("signal_token")
            if t:
                return t
        except Exception:
            pass
    # 技能目录外 .deploy（若开发者在包外维护；发布工具已排除 .deploy）
    dev = os.path.join(SKILL_DIR, ".deploy", "cloud_open.json")
    if os.path.exists(dev):
        try:
            cc = json.loads(open(dev, encoding="utf-8").read())
            t = cc.get("token") or cc.get("signal_token")
            if t:
                return t
        except Exception:
            pass
    return None


def _req(method, url, token, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


def _render(p):
    lines = []
    pid = p.get("proposal_id", "")
    lines.append(f"# 提案 {pid[:8] if pid else ''} · {p.get('skill_slug','')} · {p.get('status','')}")
    lines.append(f"  版本: {p.get('base_version')} → {p.get('proposed_version')}   置信度: {p.get('confidence')}")
    if p.get("abandon_reason"):
        lines.append(f"  流失归因: {p['abandon_reason']}")
    if p.get("summary"):
        lines.append(f"  摘要: {p['summary']}")
    for c in (p.get("changes") or []):
        lines.append(f"  - 文件 {c.get('file')} [{c.get('action')}]：{c.get('rationale','')}")
        draft = c.get("draft_text", "")
        if draft:
            lines.append(f"      草稿: {draft[:240]}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="藏经阁·易筋 进化提案 CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("list"); pl.add_argument("--slug"); pl.add_argument("--status", default="pending")
    pm = sub.add_parser("mine"); pm.add_argument("--status", default="pending"); pm.add_argument("--slug")
    pg = sub.add_parser("get"); pg.add_argument("--id", required=True); pg.add_argument("--slug")
    pa = sub.add_parser("approve"); pa.add_argument("--id", required=True); pa.add_argument("--note"); pa.add_argument("--slug")
    pr = sub.add_parser("reject"); pr.add_argument("--id", required=True); pr.add_argument("--note"); pr.add_argument("--slug")
    args = ap.parse_args()

    cfg = _load_cfg()
    base = cfg.get("proposal_url")
    if not base:
        print("✗ 云端配置缺少 proposal_url（旧包），请重发含 proposal_url 的包"); sys.exit(1)
    base = base.rstrip("/")

    slug = args.slug or _read_frontmatter(os.path.join(SKILL_DIR, "SKILL.md")).get("slug")

    if args.cmd == "mine":
        # 跨技能总览：取统一密钥库 token（用任一技能 slug 定位本地凭据），不绑特定 slug
        token = _read_local_token(slug)
        if not token:
            print("✗ 查看提案需创作者本地凭据（包内不再含 token）。")
            print("  请将创作者 token 放到 ~/.workbuddy/data/skills/<slug>/.cloud_token，")
            print("  或在本地开发环境 .deploy/cloud_open.json 配置后重试。")
            sys.exit(1)
        st, body = _req("GET", base + "/?mine=1&status=" + urllib.parse.quote(args.status), token)
        if st != 200:
            print(f"✗ HTTP {st}: {body[:300]}"); sys.exit(1)
        data = json.loads(body)
        ps = data.get("proposals", [])
        if not ps:
            print("（暂无可审核提案。蒸馏引擎定时运行，发现可改进点会生成提案出现在这里。）")
            return
        by_slug = {}
        for p in ps:
            by_slug.setdefault(p.get("skill_slug", "?"), []).append(p)
        for s, lst in by_slug.items():
            print(f"## 技能 {s}")
            for p in lst:
                print(_render(p)); print()

    elif args.cmd == "list":
        if not slug:
            print("✗ list 需 --slug 或从 SKILL.md 读取 slug"); sys.exit(1)
        token = _read_local_token(slug)
        if not token:
            print("✗ 查看提案需创作者本地凭据（包内不再含 token）。")
            print("  请将创作者 token 放到 ~/.workbuddy/data/skills/<slug>/.cloud_token，")
            print("  或在本地开发环境 .deploy/cloud_open.json 配置后重试。")
            sys.exit(1)
        qs = [f"slug={urllib.parse.quote(slug)}", f"status={urllib.parse.quote(args.status)}"]
        st, body = _req("GET", base + "/?" + "&".join(qs), token)
        if st != 200:
            print(f"✗ HTTP {st}: {body[:300]}"); sys.exit(1)
        data = json.loads(body)
        ps = data.get("proposals", [])
        if not ps:
            print("（暂无可审核提案。蒸馏引擎定时运行，发现可改进点会生成提案出现在这里。）")
            return
        for p in ps:
            print(_render(p)); print()

    elif args.cmd == "get":
        token = _read_local_token(slug)
        if not token:
            print("✗ 查看提案需创作者本地凭据（包内不再含 token）。")
            print("  请将创作者 token 放到 ~/.workbuddy/data/skills/<slug>/.cloud_token，")
            print("  或在本地开发环境 .deploy/cloud_open.json 配置后重试。")
            sys.exit(1)
        st, body = _req("GET", base + "/?id=" + urllib.parse.quote(args.id), token)
        if st != 200:
            print(f"✗ HTTP {st}: {body[:300]}"); sys.exit(1)
        data = json.loads(body)
        ps = data.get("proposals", [])
        if not ps:
            print("✗ 未找到该提案"); sys.exit(1)
        print(_render(ps[0]))

    elif args.cmd in ("approve", "reject"):
        token = _read_local_token(slug)
        if not token:
            print("✗ 应用/打回提案需创作者本地凭据（包内不再含 token）。")
            print("  请将创作者 token 放到 ~/.workbuddy/data/skills/<slug>/.cloud_token，")
            print("  或在本地开发环境 .deploy/cloud_open.json 配置后重试。")
            sys.exit(1)
        st, body = _req("POST", base + "/approve", token,
                        {"proposal_id": args.id, "decision": args.cmd, "user_note": args.note})
        if st != 200:
            print(f"✗ HTTP {st}: {body[:300]}"); sys.exit(1)
        data = json.loads(body)
        print(f"{'✓ 已批准' if args.cmd=='approve' else '✓ 已打回'}提案（{data.get('skill_slug')}）→ 状态: {data.get('status')}")
        content = data.get("content") or {}
        if args.cmd == "approve" and content.get("changes"):
            print("\n请按以下草稿在本地应用改进（应用前会自动备份原文件）：")
            print(_render({"proposal_id": args.id, "skill_slug": data.get("skill_slug"),
                           "status": data.get("status"), "changes": content.get("changes"),
                           "base_version": content.get("base_version"),
                           "proposed_version": content.get("proposed_version")}))


if __name__ == "__main__":
    main()
