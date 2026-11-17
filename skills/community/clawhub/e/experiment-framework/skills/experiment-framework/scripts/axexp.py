#!/usr/bin/env python3
"""Use the installed runtime; support a repository-local checkout without private paths."""
from pathlib import Path
import sys

repository_src = Path(__file__).resolve().parents[3] / "src"
if repository_src.is_dir():
    sys.path.insert(0, str(repository_src))

try:
    from axiotic_experiments.cli import main
except ModuleNotFoundError as exc:
    raise SystemExit("Install the experiment-framework repository and its dependencies in this Python environment: " + str(exc))

if __name__ == "__main__":
    main()
