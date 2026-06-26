# FILE_META
# INPUT:  none (derives from file location)
# OUTPUT: workspace root, data dir, output dir paths
# POS:    skill lib — called by most scripts
# MISSION: Resolve the centralized data directory path ({workspace}/.clawtraces/).

"""Centralized path resolution for ClawTraces data directory.

Data files live in {workspace}/.clawtraces/ (outside the skill dir),
so that skill updates (via ClawHub or install.md) don't destroy user data.

Workspace is determined by the skill's installation path:
  {workspace}/skills/clawtraces/scripts/lib/core/paths.py  ->  up 5 levels  ->  {workspace}
"""

import os

# Cache resolved paths to avoid repeated filesystem traversal
_workspace_dir = None


def get_workspace_dir():
    """Return workspace root (5 levels up from this file)."""
    global _workspace_dir
    if _workspace_dir is None:
        _workspace_dir = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..")
        )
    return _workspace_dir


def get_data_dir():
    """Return {workspace}/.clawtraces/ path (does NOT create the directory)."""
    return os.path.join(get_workspace_dir(), ".clawtraces")


def get_env_file_path():
    """Return path to the .env file."""
    return os.path.join(get_data_dir(), ".env")


def get_default_output_dir():
    """Return path to the output directory (does NOT create the directory)."""
    return os.path.join(get_data_dir(), "output")
