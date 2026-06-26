#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GEN = ROOT / "generate_legal_site.py"
CHK = ROOT / "check_consistency.py"
DEP = ROOT / "deploy_cloudflare_pages.py"


def run(cmd):
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError((p.stdout or "") + "\n" + (p.stderr or ""))
    return p.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description="End-to-end legal site generation/check/deploy pipeline")
    ap.add_argument("--feature", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--app-name", required=True)
    ap.add_argument("--company", required=True)
    ap.add_argument("--base-email", required=True)
    ap.add_argument("--email-tag", required=True)
    ap.add_argument("--effective-date", required=True)
    ap.add_argument("--jurisdiction", default="")
    ap.add_argument("--project-name", help="Cloudflare Pages project name for deployment")
    ap.add_argument("--production-branch", default="main", help="Cloudflare Pages production branch")
    ap.add_argument("--confirm-deploy", action="store_true", help="Deploy only when explicitly confirmed")
    args = ap.parse_args()

    out = Path(args.out)

    run([
        "python3", str(GEN),
        "--input", args.feature,
        "--out", str(out),
        "--app-name", args.app_name,
        "--company", args.company,
        "--base-email", args.base_email,
        "--email-tag", args.email_tag,
        "--effective-date", args.effective_date,
        "--jurisdiction", args.jurisdiction,
    ])

    run([
        "python3", str(CHK),
        "--feature", args.feature,
        "--privacy", str(out / "privacy.html"),
        "--terms", str(out / "terms.html"),
    ])

    payload = {
        "ok": True,
        "generated": str(out),
        "privacy": str(out / "privacy.html"),
        "terms": str(out / "terms.html"),
        "ready_for_review": True,
        "deployed": False,
    }

    if args.confirm_deploy:
        if not args.project_name:
            raise SystemExit("--project-name is required with --confirm-deploy")
        deploy_json = run([
            "python3", str(DEP),
            "--site-dir", str(out),
            "--project-name", args.project_name,
            "--production-branch", args.production_branch,
        ])
        deploy_result = json.loads(deploy_json)
        payload["deployed"] = True
        payload["url"] = deploy_result.get("url")
        payload["project"] = deploy_result.get("project")

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
