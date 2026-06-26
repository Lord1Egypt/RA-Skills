"""GitHub integration — open PRs with architectural improvement suggestions."""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class GitHubClient:
    """Interface to GitHub via gh CLI or API."""

    def __init__(self, token: str = None):
        self.token = token
        # Ensure gh auth is configured if token provided
        if token:
            # Set GH_TOKEN env for subprocesses
            import os
            os.environ['GH_TOKEN'] = token

    def can_open_prs(self) -> bool:
        """Check if we have capability to open PRs."""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def create_pr(
        self,
        repo: str,
        title: str,
        body: str,
        head: str = "ghostclaw-refactor",
        base: str = "main",
        draft: bool = False
    ) -> Optional[str]:
        """
        Create a pull request.

        Args:
            repo: Repository slug (e.g., "owner/repo")
            title: PR title
            body: PR description
            head: Branch with changes
            base: Target branch
            draft: Create as draft PR

        Returns:
            PR URL if successful, None otherwise
        """
        try:
            cmd = [
                "gh", "pr", "create",
                "--repo", repo,
                "--title", title,
                "--body", body,
                "--head", head,
                "--base", base
            ]
            if draft:
                cmd.append("--draft")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                # Extract PR URL from output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('https://github.com/'):
                        return line.strip()
                # Fallback: parse from gh output pattern
                import re
                match = re.search(r'(https://github\.com/[^\s]+)', result.stdout)
                if match:
                    return match.group(1)
            else:
                # Log error
                print(f"gh PR creation failed: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error creating PR: {e}")
            return None

    def create_or_update_branch(
        self,
        repo_local_path: Path,
        branch_name: str,
        files_to_commit: List[Path],
        commit_message: str
    ) -> bool:
        """
        Create a branch, add files, commit, and push to origin.

        This is a simplified version — assumes we're operating on a local clone.
        """
        try:
            # Ensure we're in repo root
            import os
            old_cwd = os.getcwd()
            os.chdir(repo_local_path)

            # Fetch latest
            subprocess.run(["git", "fetch", "origin"], check=True, capture_output=True)

            # Create branch from base (main)
            subprocess.run(["git", "checkout", "-B", branch_name, "origin/main"], check=True, capture_output=True)

            # Copy files into working tree
            for src in files_to_commit:
                import shutil
                dest = repo_local_path / src.relative_to(repo_local_path) if src.is_relative_to(repo_local_path) else src
                shutil.copy2(src, dest)

            # Stage and commit
            subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True)

            # Push
            subprocess.run(["git", "push", "-u", "origin", branch_name], check=True, capture_output=True)

            os.chdir(old_cwd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e.stderr}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
