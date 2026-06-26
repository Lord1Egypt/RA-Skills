"""Interactive setup wizard — walks a new user through configuration."""

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent


def _ask(prompt: str, default: str = "", choices: list[str] | None = None) -> str:
    """Prompt for input with an optional default and choice validation."""
    choice_hint = f" [{'/'.join(choices)}]" if choices else ""
    default_hint = f" (default: {default})" if default else ""
    while True:
        raw = input(f"{prompt}{choice_hint}{default_hint}: ").strip()
        value = raw or default
        if choices and value.lower() not in [c.lower() for c in choices]:
            print(f"  Please enter one of: {', '.join(choices)}")
            continue
        return value


def _ask_secret(prompt: str) -> str:
    """Prompt for a secret value (shown as-is since we're in a terminal)."""
    value = input(f"{prompt}: ").strip()
    return value


def _open_url(url: str, label: str) -> None:
    """Offer to open a URL in the browser."""
    ans = input(f"\n  Open {label} in your browser? [Y/n]: ").strip().lower()
    if ans != "n":
        try:
            webbrowser.open(url)
        except Exception:
            pass
    print(f"  URL: {url}")


def _detect_runtime() -> str:
    """Return 'python', 'docker', or 'none'."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", "import sys; sys.exit(0 if sys.version_info>=(3,9) else 1)"],
            capture_output=True,
        )
        if result.returncode == 0:
            return "python"
    except Exception:
        pass
    try:
        result = subprocess.run(
            ["docker", "info"], capture_output=True, timeout=5
        )
        if result.returncode == 0:
            return "docker"
    except Exception:
        pass
    return "none"


def _check_deps(runtime: str) -> bool:
    """Install requirements if needed (Python path only)."""
    if runtime != "python":
        return True
    req_file = SKILL_DIR / "requirements.txt"
    if not req_file.exists():
        return True
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file), "-q"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def run() -> None:
    """Run the interactive setup wizard."""
    env_path = SKILL_DIR / ".env"

    print("\n" + "═" * 60)
    print("  em-intel  Setup Wizard")
    print("═" * 60)
    print("\nThis will configure em-intel in about 2 minutes.")
    print("You'll need API tokens from your code platform and Jira.\n")

    # ── Step 1: Detect runtime ────────────────────────────────────────
    print("Step 1/5 — Checking runtime...")
    runtime = _detect_runtime()

    if runtime == "python":
        print("  ✓ Python detected — installing dependencies...")
        if _check_deps(runtime):
            print("  ✓ Dependencies ready\n")
        else:
            print("  ⚠ Could not install automatically. Run:")
            print(f"    pip3 install -r {SKILL_DIR / 'requirements.txt'}\n")

    elif runtime == "docker":
        print("  ✓ Docker detected — will build image after setup\n")

    else:
        print("  ❌ Neither Python 3.9+ nor Docker found.\n")
        print("  Install one of:")
        print("    Python: https://www.python.org/downloads/")
        print("    Docker: https://docs.docker.com/get-docker/")
        print("\n  Then re-run this wizard.\n")
        sys.exit(1)

    # ── Step 2: Code platform ─────────────────────────────────────────
    print("Step 2/5 — Code platform")
    code_provider = _ask("  Platform", default="gitlab", choices=["gitlab", "github"])

    if code_provider == "gitlab":
        print("\n  You'll need a GitLab Personal Access Token with 'read_api' scope.")
        _open_url(
            "https://gitlab.com/-/user_settings/personal_access_tokens",
            "GitLab token page"
        )
        gitlab_url = _ask("  GitLab URL", default="https://gitlab.com")
        gitlab_token = _ask_secret("  GitLab token (glpat-...)")
        gitlab_group = _ask("  GitLab group path (e.g. my-org/my-team)")
        github_token = github_org = github_repos = ""
    else:
        print("\n  You'll need a GitHub Personal Access Token with 'repo' and 'read:org' scopes.")
        _open_url(
            "https://github.com/settings/tokens/new",
            "GitHub token page"
        )
        github_token = _ask_secret("  GitHub token (ghp_...)")
        github_org = _ask("  GitHub org name")
        github_repos = _ask("  Repos to include (comma-separated, leave blank for all)")
        gitlab_url = gitlab_token = gitlab_group = ""

    # ── Step 3: Ticket system ─────────────────────────────────────────
    print("\nStep 3/5 — Ticket system")
    ticket_provider = _ask("  System", default="jira", choices=["jira", "github_issues"])

    if ticket_provider == "jira":
        print("\n  You'll need a Jira API token.")
        _open_url(
            "https://id.atlassian.com/manage-profile/security/api-tokens",
            "Atlassian token page"
        )
        jira_url = _ask("  Jira URL (e.g. https://yoursite.atlassian.net)")
        jira_email = _ask("  Jira account email")
        jira_token = _ask_secret("  Jira API token")
        jira_projects = _ask("  Jira project keys (comma-separated, e.g. ENG,OPS)")
    else:
        jira_url = jira_email = jira_token = jira_projects = ""

    # ── Step 4: Delivery ──────────────────────────────────────────────
    print("\nStep 4/5 — Delivery channel")
    print("  How should reports be sent?")
    print("  print   — display in terminal (good for testing)")
    print("  email   — send to your inbox")
    print("  slack   — post to a Slack channel")
    print("  telegram — send to a Telegram bot")
    delivery = _ask("  Delivery", default="print", choices=["print", "email", "slack", "telegram"])

    smtp_host = smtp_port = smtp_user = smtp_password = smtp_to = ""
    slack_webhook = ""
    telegram_token = telegram_chat_id = ""

    if delivery == "email":
        print("\n  For Gmail, use an App Password (not your login password).")
        _open_url("https://myaccount.google.com/apppasswords", "Gmail App Passwords")
        smtp_host = _ask("  SMTP host", default="smtp.gmail.com")
        smtp_port = _ask("  SMTP port", default="587")
        smtp_user = _ask("  SMTP username / from address")
        smtp_password = _ask_secret("  SMTP password / app password")
        smtp_to = _ask("  Send reports to (email address)", default=smtp_user)

    elif delivery == "slack":
        print("\n  Create an incoming webhook at:")
        _open_url("https://api.slack.com/apps", "Slack Apps")
        slack_webhook = _ask_secret("  Slack webhook URL (https://hooks.slack.com/...)")

    elif delivery == "telegram":
        print("\n  Talk to @BotFather on Telegram to create a bot and get a token.")
        telegram_token = _ask_secret("  Telegram bot token")
        telegram_chat_id = _ask("  Telegram chat ID (your user or group ID)")

    # ── Step 5: Write .env ────────────────────────────────────────────
    print("\nStep 5/5 — Writing configuration...")

    lines = [
        "# em-intel configuration — generated by setup wizard",
        "",
        "# Code platform",
        f"EM_CODE_PROVIDER={code_provider}",
    ]

    if code_provider == "gitlab":
        lines += [
            f"GITLAB_URL={gitlab_url}",
            f"GITLAB_TOKEN={gitlab_token}",
            f"GITLAB_GROUP={gitlab_group}",
        ]
    else:
        lines += [
            f"GITHUB_TOKEN={github_token}",
            f"GITHUB_ORG={github_org}",
        ]
        if github_repos:
            lines.append(f"GITHUB_REPOS={github_repos}")

    lines += ["", "# Ticket system", f"EM_TICKET_PROVIDER={ticket_provider}"]

    if ticket_provider == "jira":
        lines += [
            f"JIRA_URL={jira_url}",
            f"JIRA_EMAIL={jira_email}",
            f"JIRA_TOKEN={jira_token}",
            f"JIRA_PROJECTS={jira_projects}",
        ]

    lines += ["", "# Delivery", f"EM_DELIVERY={delivery}"]

    if delivery == "email":
        lines += [
            f"SMTP_HOST={smtp_host}",
            f"SMTP_PORT={smtp_port}",
            f"SMTP_USER={smtp_user}",
            f"SMTP_PASSWORD={smtp_password}",
            f"SMTP_TO={smtp_to}",
        ]
    elif delivery == "slack":
        lines.append(f"SLACK_WEBHOOK_URL={slack_webhook}")
    elif delivery == "telegram":
        lines += [
            f"TELEGRAM_BOT_TOKEN={telegram_token}",
            f"TELEGRAM_CHAT_ID={telegram_chat_id}",
        ]

    lines += [
        "",
        "# Tuning",
        "EM_QUIET_ENGINEER_DAYS=10",
        "EM_STALE_EPIC_DAYS=14",
        "EM_LOOKBACK_DAYS=30",
    ]

    env_path.write_text("\n".join(lines) + "\n")
    print(f"  ✓ Written to {env_path}\n")

    # ── Build Docker image if needed ──────────────────────────────────
    if runtime == "docker":
        print("Building Docker image (first time, ~30s)...")
        build = subprocess.run(
            ["docker", "build", "-t", "em-intel", str(SKILL_DIR), "-q"],
            cwd=str(SKILL_DIR),
        )
        if build.returncode == 0:
            print("  ✓ Image built\n")
        else:
            print("  ⚠ Docker build failed — check output above\n")

    # ── Run doctor ────────────────────────────────────────────────────
    print("Running doctor to verify...\n")
    run_cmd = (
        ["docker", "run", "--rm", "--env-file", str(env_path), "em-intel", "doctor"]
        if runtime == "docker"
        else [sys.executable, str(SKILL_DIR / "em_intel.py"), "doctor"]
    )
    result = subprocess.run(run_cmd, cwd=str(SKILL_DIR))

    run_script = f"{SKILL_DIR}/run.sh"
    if result.returncode == 0:
        print("\n✓ All set! Try your first command:")
        print(f"  {run_script} morning-brief\n")
    else:
        print("\n⚠ Some checks failed — fix the issues above and re-run:")
        print(f"  {run_script} doctor\n")
