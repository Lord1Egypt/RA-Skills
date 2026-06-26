"""PRService — automates GitHub Pull Request creation."""

import subprocess
import sys
from pathlib import Path
from typing import Optional
import datetime


class PRService:
    """
    Service for automating GitHub Pull Request creation.
    """

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    async def create_pr(self, report_file: Path, title: str, body: str) -> None:
        """
        Automate PR creation: branch, commit, push, gh pr create.

        Args:
            report_file (Path): The path to the report file.
            title (str): The PR title.
            body (str): The PR body.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
        branch_name = f"ghostclaw/arch-report-{timestamp}"

        try:
            # Create branch
            subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.repo_path, check=True, capture_output=True, text=True)

            # Add report with force (to bypass gitignore if needed)
            rel_report_path = report_file.relative_to(Path(self.repo_path))
            subprocess.run(["git", "add", "-f", str(rel_report_path)], cwd=self.repo_path, check=True, capture_output=True, text=True)

            # Commit
            subprocess.run(["git", "commit", "-m", f"Add architecture report: {report_file.name}"], cwd=self.repo_path, check=True, capture_output=True, text=True)

            # Push
            subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=self.repo_path, check=True, capture_output=True, text=True)

            # Create PR
            pr_cmd = ["gh", "pr", "create", "--title", title, "--body", body]
            result = subprocess.run(pr_cmd, cwd=self.repo_path, capture_output=True, text=True, check=True)
            print(f"🔗 PR created: {result.stdout.strip()}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create PR: {e.stderr or e}", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"❌ Error during PR creation: {str(e)}", file=sys.stderr)
            raise e
