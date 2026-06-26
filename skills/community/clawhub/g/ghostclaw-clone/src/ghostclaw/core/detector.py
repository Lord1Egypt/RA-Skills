"""Tech stack detection for codebases."""

import json
from pathlib import Path
from typing import List, Set
import asyncio

# Directories that should always be excluded from analysis
EXCLUDE_DIRS: Set[str] = {
    '.venv', 'venv', '.env', '__pycache__', '.pytest_cache', '.coverage',
    '.git', '.hg', '.svn', 'node_modules', 'dist', 'build', 'target',
    'vendor', '.deps', 'tests', 'test', 'spec', 'specs', 'docs', 'doc',
    'example', 'examples', 'scripts', '.ghostclaw'
}


def _should_exclude(path: Path) -> bool:
    """Check if a path or any of its parents should be excluded."""
    parts = set(path.parts)
    return any(excluded in parts for excluded in EXCLUDE_DIRS)


def detect_stack(root: str) -> str:
    """Detect the primary tech stack of a repository."""
    root_path = Path(root)

    # Python (Django, FastAPI, plain) - Prioritize Python to avoid misidentification in hybrid projects
    python_indicators = ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile', 'poetry.lock']
    if any((root_path / f).exists() for f in python_indicators):
        return 'python'

    # Node / TypeScript / React setup
    node_indicators = ['package.json', 'vite.config.ts', 'next.config.js', 'remix.config.js']
    typescript_indicators = ['tsconfig.json']

    # Prioritize TypeScript if tsconfig.json or many .ts files are present
    if any((root_path / f).exists() for f in typescript_indicators):
        return 'typescript'

    if any((root_path / f).exists() for f in node_indicators):
        return 'node'

    # Go
    if any((root_path / f).exists() for f in ['go.mod', 'go.sum']):
        return 'go'

    # Shell
    shell_indicators = ['.shellcheckrc', '.sh', '.bash', '.zsh']
    if any((root_path / ext).exists() or any(root_path.glob(f"*{ext}")) for ext in shell_indicators):
        return 'shell'

    # Docker
    docker_indicators = ['Dockerfile', 'docker-compose.yml', 'compose.yaml', '.dockerignore']
    if any((root_path / f).exists() for f in docker_indicators):
        return 'docker'

    return 'unknown'


def find_files(root: str, extensions: List[str]) -> List[str]:
    """Recursively find files with given extensions, excluding common noise directories."""
    root_path = Path(root)
    all_files = []
    for ext in extensions:
        for f in root_path.rglob(f"*{ext}"):
            if not _should_exclude(f.relative_to(root_path)):
                all_files.append(str(f))
    return sorted(all_files)


async def find_files_parallel(root: str, extensions: List[str], limit: int = 32) -> List[str]:
    """
    Parallel file discovery using multiple threads for I/O.

    Scans root-level files directly and processes top-level subdirectories concurrently.
    The concurrency 'limit' controls max simultaneous directory scans.
    """
    root_path = Path(root)
    all_files: List[str] = []

    # 1. Collect root-level files (non-recursive)
    for ext in extensions:
        for f in root_path.glob(f"*{ext}"):
            if f.is_file() and not _should_exclude(f.relative_to(root_path)):
                all_files.append(str(f))

    # 2. Determine top-level subdirectories to scan recursively
    subdirs = []
    try:
        for child in root_path.iterdir():
            if child.is_dir() and not _should_exclude(child.relative_to(root_path)):
                subdirs.append(child)
    except Exception:
        subdirs = []

    if not subdirs:
        return sorted(all_files)

    # 3. Define per-directory scanner with semaphore to respect concurrency limit
    semaphore = asyncio.Semaphore(limit)

    async def scan_dir(dir_path: Path) -> List[str]:
        async with semaphore:
            # Run blocking rglob in a thread to avoid blocking event loop
            def _blocking_scan():
                files = []
                for ext in extensions:
                    for f in dir_path.rglob(f"*{ext}"):
                        try:
                            rel = f.relative_to(root_path)
                        except ValueError:
                            # Should not happen, but skip if not under root
                            continue
                        if not _should_exclude(rel):
                            files.append(str(f))
                return files
            return await asyncio.to_thread(_blocking_scan)

    # 4. Launch tasks for all subdirs
    tasks = [scan_dir(d) for d in subdirs]
    for task in asyncio.as_completed(tasks):
        result = await task
        all_files.extend(result)

    return sorted(all_files)
