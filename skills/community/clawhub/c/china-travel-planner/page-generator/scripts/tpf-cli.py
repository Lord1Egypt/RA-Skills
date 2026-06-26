#!/usr/bin/env python3
"""
CLI tool for travel-page-framework.

Usage:
    tpf validate          # Validate data/trip-data.json against schema
    tpf build             # Build static site to dist/
    tpf deploy --to gh-pages   # Deploy to GitHub Pages

Install:
    ln -s scripts/tpf-cli.py /usr/local/bin/tpf
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Find framework root (where this script is located)
SCRIPT_DIR = Path(__file__).parent.resolve()
FRAMEWORK_DIR = SCRIPT_DIR.parent
SCHEMA_FILE = FRAMEWORK_DIR / "schema" / "trip-schema.json"
TEMPLATES_DIR = FRAMEWORK_DIR / "templates"


def error(msg):
    print(f"[tpf] ❌ {msg}", file=sys.stderr)
    sys.exit(1)


def info(msg):
    print(f"[tpf] ℹ️  {msg}")


def success(msg):
    print(f"[tpf] ✅ {msg}")


def find_project_root():
    """Find project root by looking for data/trip-data.json."""
    cwd = Path.cwd()
    for path in [cwd] + list(cwd.parents):
        if (path / "data" / "trip-data.json").exists():
            return path
    return None


def cmd_validate(args):
    """Validate trip-data.json against schema."""
    project_dir = find_project_root()
    if not project_dir:
        error("Not in a travel page project (no data/trip-data.json found)")

    data_file = project_dir / "data" / "trip-data.json"

    # Simple JSON validation first
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        error(f"Invalid JSON: {e}")
    except FileNotFoundError:
        error(f"File not found: {data_file}")

    # Check required top-level keys
    required = ["meta", "hero", "stats", "hotels", "metroCoverage", "days", "sideTrips", "attractions", "tips"]
    missing = [k for k in required if k not in data]
    if missing:
        error(f"Missing required keys: {', '.join(missing)}")

    # Check meta
    if not all(k in data.get("meta", {}) for k in ["title", "subtitle", "description"]):
        error("meta must have title, subtitle, description")

    # Check hero
    hero_required = ["title", "subtitle", "dateRange", "tags", "summary"]
    if not all(k in data.get("hero", {}) for k in hero_required):
        error(f"hero must have {', '.join(hero_required)}")

    # Check arrays
    for key in ["stats", "hotels", "days", "sideTrips", "attractions", "tips"]:
        if not isinstance(data.get(key), list):
            error(f"{key} must be an array")

    success(f"Validation passed: {data_file}")

    # Show stats
    info(f"Title: {data['hero']['title']}")
    info(f"Duration: {data['hero']['dateRange']}")
    info(f"Days: {len(data['days'])}")
    info(f"Hotels: {len(data['hotels'])}")
    info(f"Attractions: {len(data['attractions'])}")


def cmd_build(args):
    """Build static site to dist/."""
    project_dir = find_project_root()
    if not project_dir:
        error("Not in a travel page project")

    # Validate first
    info("Validating data...")
    cmd_validate(args)

    dist_dir = project_dir / "dist"
    data_file = project_dir / "data" / "trip-data.json"

    # Clean and create dist
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # Copy data
    shutil.copy(data_file, dist_dir / "trip-data.json")

    # Create standalone HTML that inlines everything
    html_template = (TEMPLATES_DIR / "trip-page-tailwind.html").read_text(encoding="utf-8")
    theme_js = (TEMPLATES_DIR / "themes" / "light.js").read_text(encoding="utf-8")
    renderer_js = (TEMPLATES_DIR / "trip-renderer.js").read_text(encoding="utf-8")

    # Replace external script refs with inline
    # Remove the external script tags
    import re
    html = re.sub(r'<script src="[^"]*trip-renderer\.js"[^>]*></script>', '', html_template)
    html = re.sub(r'<script src="[^"]*light\.js"[^>]*></script>', '', html_template)

    # Insert inline scripts before closing </body>
    inline_scripts = f"""
<script>
{theme_js}
</script>
<script>
{renderer_js}
</script>
<script>
TripRenderer.init({{ dataUrl: './trip-data.json', theme: 'light' }});
</script>
"""
    html = html.replace('</body>', inline_scripts + '\n</body>')

    # Write standalone HTML
    (dist_dir / "index.html").write_text(html, encoding="utf-8")

    success(f"Built to: {dist_dir}")
    info("Files:")
    for f in dist_dir.iterdir():
        size = f.stat().st_size
        info(f"  {f.name} ({size:,} bytes)")

    info("")
    info("To preview: cd dist && python3 -m http.server 8080")


def cmd_deploy(args):
    """Deploy to GitHub Pages."""
    project_dir = find_project_root()
    if not project_dir:
        error("Not in a travel page project")

    # Check if git repo
    if not (project_dir / ".git").exists():
        error("Not a git repository. Run: git init")

    # Check remote
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    if "github.com" not in result.stdout:
        error("No GitHub remote found. Add one with: git remote add origin <url>")

    # Build first
    cmd_build(args)

    dist_dir = project_dir / "dist"

    # Deploy using gh-pages branch
    info("Deploying to GitHub Pages...")

    # Create temporary worktree for gh-pages
    gh_pages_dir = project_dir / ".gh-pages-temp"
    if gh_pages_dir.exists():
        shutil.rmtree(gh_pages_dir)

    try:
        # Check if gh-pages branch exists
        result = subprocess.run(
            ["git", "branch", "--list", "gh-pages"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        if "gh-pages" not in result.stdout:
            # Create orphan branch
            subprocess.run(
                ["git", "checkout", "--orphan", "gh-pages"],
                cwd=project_dir,
                check=True
            )
            subprocess.run(
                ["git", "rm", "-rf", "."],
                cwd=project_dir,
                check=True
            )
        else:
            subprocess.run(
                ["git", "checkout", "gh-pages"],
                cwd=project_dir,
                check=True
            )

        # Copy dist contents to root
        for item in dist_dir.iterdir():
            if item.is_file():
                shutil.copy(item, project_dir / item.name)

        # Commit and push
        subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Deploy to GitHub Pages"],
            cwd=project_dir,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "push", "origin", "gh-pages"],
            cwd=project_dir,
            check=True
        )

        # Get repo URL
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True
        )
        repo_url = result.stdout.strip()
        # Convert git@github.com:user/repo.git to https://user.github.io/repo
        if repo_url.startswith("git@github.com:"):
            parts = repo_url.replace("git@github.com:", "").replace(".git", "").split("/")
            pages_url = f"https://{parts[0]}.github.io/{parts[1]}"
        elif "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").replace(".git", "").split("/")
            pages_url = f"https://{parts[0]}.github.io/{parts[1]}"
        else:
            pages_url = "(check GitHub repository settings)"

        success(f"Deployed to: {pages_url}")

    finally:
        # Switch back to main branch
        subprocess.run(
            ["git", "checkout", "-"],
            cwd=project_dir,
            capture_output=True
        )


def main():
    parser = argparse.ArgumentParser(
        prog="tpf",
        description="Travel Page Framework CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate trip-data.json")

    # build
    p_build = subparsers.add_parser("build", help="Build static site to dist/")

    # deploy
    p_deploy = subparsers.add_parser("deploy", help="Deploy to GitHub Pages")
    p_deploy.add_argument("--to", choices=["gh-pages"], default="gh-pages",
                         help="Deployment target")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "validate": cmd_validate,
        "build": cmd_build,
        "deploy": cmd_deploy,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
