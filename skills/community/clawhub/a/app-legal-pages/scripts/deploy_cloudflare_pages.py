#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


def run(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr.strip()}")
    return p


def check_auth():
    # Priority: API token env, fallback to wrangler login session
    token = os.getenv("CLOUDFLARE_API_TOKEN")
    acct = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    if token and acct:
        return {"ok": True, "mode": "api-token", "account_id": acct}

    wrangler = shutil.which("wrangler")
    if not wrangler:
        return {"ok": False, "reason": "wrangler_not_installed"}

    p = run([wrangler, "whoami"], check=False)
    if p.returncode != 0:
        return {"ok": False, "reason": "wrangler_not_logged_in"}

    return {"ok": True, "mode": "wrangler-login", "account_id": acct or ""}


def ensure_project(project_name: str, production_branch: str):
    wrangler = shutil.which("wrangler")
    p = run([wrangler, "pages", "project", "list", "--json"], check=True)
    items = json.loads(p.stdout or "[]")
    names = {x.get("Project Name") for x in items}
    if project_name in names:
        return False

    run([
        wrangler,
        "pages",
        "project",
        "create",
        project_name,
        "--production-branch",
        production_branch,
    ], check=True)
    return True


def deploy_with_wrangler(project_name: str, site_dir: Path, production_branch: str):
    wrangler = shutil.which("wrangler")
    if not wrangler:
        raise RuntimeError("wrangler is not installed. Install: npm i -g wrangler")

    created = ensure_project(project_name, production_branch)

    # Explicitly deploy to production branch to avoid wrong default branch routes.
    p = run([
        wrangler,
        "pages",
        "deploy",
        str(site_dir),
        "--project-name",
        project_name,
        "--branch",
        production_branch,
    ], check=True)
    output = (p.stdout or "") + "\n" + (p.stderr or "")

    canonical = f"https://{project_name}.pages.dev"
    branch_alias = f"https://{production_branch}.{project_name}.pages.dev"

    return {
        "project": project_name,
        "created_project": created,
        "production_branch": production_branch,
        "url": canonical,
        "privacy_url": f"{canonical}/privacy",
        "terms_url": f"{canonical}/terms",
        "branch_alias_url": branch_alias,
        "raw": output,
    }


def main():
    ap = argparse.ArgumentParser(description="Check Cloudflare auth and deploy static site to Pages")
    ap.add_argument("--site-dir", required=True, help="Path to generated static legal site")
    ap.add_argument("--project-name", required=True, help="Cloudflare Pages project name")
    ap.add_argument("--check-auth", action="store_true", help="Only check auth and print JSON")
    ap.add_argument("--production-branch", default="main", help="Production branch for Pages project (default: main)")
    args = ap.parse_args()

    site_dir = Path(args.site_dir)
    if not site_dir.exists():
        raise SystemExit(f"site directory not found: {site_dir}")

    auth = check_auth()
    if args.check_auth:
        print(json.dumps(auth, ensure_ascii=False))
        raise SystemExit(0 if auth.get("ok") else 2)

    if not auth.get("ok"):
        print(json.dumps(auth, ensure_ascii=False))
        raise SystemExit("Cloudflare auth missing. Set CLOUDFLARE_API_TOKEN+CLOUDFLARE_ACCOUNT_ID or run: wrangler login")

    result = deploy_with_wrangler(args.project_name, site_dir, args.production_branch)
    print(json.dumps({"ok": True, **result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
