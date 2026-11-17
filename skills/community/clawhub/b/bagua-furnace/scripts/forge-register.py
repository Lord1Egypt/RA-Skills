#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能锻造炉 (SkillForge) — 云端注册引导器 forge-register.py

让「技能锻造炉」锻造出的技能，在发布前/后由创作者本人一键完成「藏经阁·易筋」
slug 注册 + 邮箱验证，拿到审核提案所需的创作者 token（signal_token）。

token 仅落在被注册技能目录的 `.deploy/cloud_open.json`，**不进发布包**，
与终端用户零配置匿名上传（cloud_config.json 仅公网 URL）严格分离。

用法（在被锻造技能的目录下运行，或 --path 指定）：
    python forge-register.py register            # 注册 slug + 发验证码到邮箱
    python forge-register.py verify <验证码>      # 校验并保存 token 到 .deploy/cloud_open.json
    python forge-register.py status              # 查看注册/验证态
    python forge-register.py resend              # 重发验证码

依赖：仅 Python 标准库。创作者邮箱默认读 .deploy/cloud_open.json，
若不存在则交互询问（也可 --email 指定）。
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

SKILLS_BASE = Path.home() / ".workbuddy" / "skills"
# 注册端点只来自外部配置（环境变量 CJG_REGISTER_URL / cloud_config.json），不硬编码。
DEPLOY_DIR = ".deploy"
CLOUD_OPEN_FILE = "cloud_open.json"
CREATOR_EMAIL_HINT = "252005371@qq.com"  # 创作者运营邮箱（默认，可用 --email 覆盖）


# ============================================================
# 工具
# ============================================================
def _read_frontmatter(skill_md: Path) -> dict:
    if not skill_md.exists():
        return {}
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data = {}
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                v = v[1:-1]
            data[k] = v
    return data


def _post(register_url: str, path: str, payload: dict) -> dict:
    url = register_url.rstrip("/") + "/" + path.lstrip("/")
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"ok": False, "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _load_open(skill_dir: Path) -> dict:
    p = skill_dir / DEPLOY_DIR / CLOUD_OPEN_FILE
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_open(skill_dir: Path, data: dict):
    d = skill_dir / DEPLOY_DIR
    d.mkdir(parents=True, exist_ok=True)
    (d / CLOUD_OPEN_FILE).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    # 确保不进发布包
    gitignore = skill_dir / ".gitignore"
    line = f"{DEPLOY_DIR}/\n"
    if gitignore.exists():
        txt = gitignore.read_text(encoding="utf-8")
        if DEPLOY_DIR + "/" not in txt and DEPLOY_DIR not in txt:
            gitignore.write_text(txt + line, encoding="utf-8")
    else:
        gitignore.write_text(line, encoding="utf-8")


def _register_url_of(skill_dir: Path) -> str:
    # 端点只来自外部配置（环境变量 / cloud_config.json），不在代码中硬编码。
    env = os.environ.get("CJG_REGISTER_URL")
    if env:
        return env.strip().rstrip("/")
    cands = [
        skill_dir / "cloud_config.json",
        Path.home() / ".workbuddy" / "secrets" / "cjg-evo" / "cloud_config.json",
    ]
    for cc in cands:
        try:
            if cc.exists():
                data = json.loads(cc.read_text(encoding="utf-8"))
                if data.get("register_url"):
                    return data["register_url"]
        except Exception:
            pass
    sys.exit("✗ 未找到 register_url：请设置环境变量 CJG_REGISTER_URL，或在 cloud_config.json 中提供 register_url")


def resolve_skill_dir(args) -> Path:
    if args.path:
        p = Path(args.path).expanduser().resolve()
        return p if p.exists() else None
    if args.skill:
        p = SKILLS_BASE / args.skill
        return p if p.exists() else None
    cwd = Path.cwd()
    return cwd if (cwd / "SKILL.md").exists() else None


# ============================================================
# 子命令
# ============================================================
def cmd_register(args, skill_dir: Path, slug: str, email: str, register_url: str):
    r = _post(register_url, "register",
              {"email": email, "slug": slug, "mode": "cloud"})
    if not r.get("ok"):
        print(f"✗ 注册失败: {r.get('error')}")
        return 1
    print(f"✓ 已向 {email} 发送验证码（20 分钟内有效）")
    print(f"  查收后运行:  python forge-register.py verify <验证码>")
    return 0


def cmd_verify(args, skill_dir: Path, slug: str, email: str, register_url: str):
    code = args.code
    if not code:
        print("✗ 请提供验证码: python forge-register.py verify <验证码>")
        return 1
    r = _post(register_url, "verify", {"email": email, "code": code})
    if not r.get("ok"):
        print(f"✗ 验证失败: {r.get('error')}")
        if r.get("attempts_left") is not None:
            print(f"  剩余尝试次数: {r['attempts_left']}")
        return 1
    token = r.get("signal_token")
    if not token:
        print("✗ 验证成功但未返回 token（异常）")
        return 1
    data = _load_open(skill_dir)
    data.update({
        "email": email,
        "signal_token": token,
        "register_url": register_url,
        "slug": slug,
    })
    _save_open(skill_dir, data)
    print(f"✓ 验证成功，创作者 token 已保存到 {skill_dir / DEPLOY_DIR / CLOUD_OPEN_FILE}")
    print(f"  现在可以用「看看提案」查看/审核该 slug 的进化提案了。")
    return 0


def cmd_status(args, skill_dir: Path, slug: str, email: str, register_url: str):
    r = _post(register_url, "status", {"email": email})
    if not r.get("ok"):
        print(f"✗ 查询失败: {r.get('error')}")
        return 1
    if not r.get("registered"):
        print(f"○ 该邮箱尚未注册 slug「{slug}」")
        return 0
    print(f"✓ 已注册 slug「{slug}」")
    print(f"  验证状态 : {'已验证' if r.get('verified') else '未验证（请 verify）'}")
    print(f"  验证码   : {'有效' if r.get('code_sent') else '已过期'}"
          + (f"（{r.get('code_expires_in')} 秒后过期）" if r.get('code_sent') else ""))
    print(f"  剩余次数 : {r.get('attempts_left')}")
    return 0


def cmd_resend(args, skill_dir: Path, slug: str, email: str, register_url: str):
    r = _post(register_url, "resend", {"email": email})
    if not r.get("ok"):
        print(f"✗ 重发失败: {r.get('error')}")
        return 1
    print(f"✓ 验证码已重新发送到 {email}，请查收后运行 verify。")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="技能锻造炉 · 云端注册引导器（藏经阁·易筋 slug 注册 + 邮箱验证）")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--skill", help="技能 slug（从 ~/.workbuddy/skills/<slug> 读取目录）")
    g.add_argument("--path", help="技能目录绝对路径（默认：当前目录，需含 SKILL.md）")
    parser.add_argument("--email", default=None, help="创作者邮箱（默认读 .deploy/cloud_open.json 或询问）")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("register", help="注册 slug 并发送验证码")
    pv = sub.add_parser("verify", help="校验验证码并保存 token")
    pv.add_argument("code", help="邮箱收到的 6 位验证码")
    sub.add_parser("status", help="查看注册/验证态")
    sub.add_parser("resend", help="重发验证码")

    args = parser.parse_args()

    skill_dir = resolve_skill_dir(args)
    if not skill_dir:
        print("✗ 技能目录不存在或不含 SKILL.md")
        sys.exit(1)

    fm = _read_frontmatter(skill_dir / "SKILL.md")
    slug = fm.get("slug") or (args.skill or "")
    if not slug:
        print("✗ 无法从 SKILL.md frontmatter 读取 slug")
        sys.exit(1)

    open_data = _load_open(skill_dir)
    email = args.email or open_data.get("email") or CREATOR_EMAIL_HINT
    register_url = _register_url_of(skill_dir)

    print(f"技能: {skill_dir.name}  |  slug: {slug}  |  邮箱: {email}")
    print(f"端点: {register_url}\n")

    dispatch = {
        "register": cmd_register,
        "verify": cmd_verify,
        "status": cmd_status,
        "resend": cmd_resend,
    }
    rc = dispatch[args.cmd](args, skill_dir, slug, email, register_url)
    sys.exit(rc)


if __name__ == "__main__":
    main()
