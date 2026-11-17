"""
Helper for running LibreOffice (soffice) headlessly.

Usage:
    from office.soffice import run_soffice, get_soffice_env

    # Option 1 - run soffice directly
    result = run_soffice(["--headless", "--convert-to", "pdf", "input.docx"])

    # Option 2 - get env dict for your own subprocess calls
    env = get_soffice_env()
    subprocess.run(["soffice", ...], env=env)
"""

import os
import subprocess


def get_soffice_env() -> dict:
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    return env


def run_soffice(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    env = get_soffice_env()
    return subprocess.run(["soffice"] + args, env=env, **kwargs)


if __name__ == "__main__":
    import sys

    result = run_soffice(sys.argv[1:])
    sys.exit(result.returncode)
