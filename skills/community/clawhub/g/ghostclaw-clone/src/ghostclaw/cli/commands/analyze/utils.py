"""
Utilities for the analyze command.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional


def detect_github_remote(repo_path: str) -> Optional[str]:
    """Detect if the repository has a GitHub remote (origin)."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            if "github.com" in url:
                return url
    except Exception:
        pass
    return None


def estimate_repo_file_count(repo_path: str) -> int:
    """Estimate the number of files in the repository, excluding common non-source dirs."""
    repo = Path(repo_path)
    if not repo.exists():
        return 0

    exclude_dirs = {
        '.git', 'node_modules', 'venv', '.venv', 'env', 'virtualenv',
        '__pycache__', '.pytest_cache', 'build', 'dist', 'target', 'bin', 'obj',
        '.idea', '.vscode', '.cache', 'tmp', 'temp', 'coverage', '.coverage', 'htmlcov',
        '.next', '.nuxt', 'out', 'turbo', '.turbo'
    }
    exclude_extensions = {
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.bin', '.obj', '.o', '.a', '.lib',
        '.class', '.jar', '.war', '.ear', '.log', '.cache', '.pid', '.lock',
        '.sqlite', '.db', '.sqlite3', '.svg', '.png', '.jpg', '.jpeg', '.gif', '.ico',
        '.pdf', '.zip', '.tar', '.gz', '.tgz', '.rar', '.7z'
    }

    count = 0
    try:
        for root, dirs, files in os.walk(repo):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
            for file in files:
                if file.startswith('.'):
                    continue
                if any(file.lower().endswith(ext) for ext in exclude_extensions):
                    continue
                count += 1
                if count > 10000:
                    return count
    except Exception:
        return 0
    return count
