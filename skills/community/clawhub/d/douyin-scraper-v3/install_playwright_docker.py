#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

PLAYWRIGHT_VERSION = os.environ.get("PW_VERSION", "1.50.0")
IMAGE_TAG = f"mcr.microsoft.com/playwright/python:v{PLAYWRIGHT_VERSION}-noble"
APP_IMAGE = f"douyin-scraper-playwright:{PLAYWRIGHT_VERSION}"


def run(cmd: list[str], cwd: str | None = None, env: dict[str, str] | None = None) -> None:
    print("\n>>>", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def mode_official() -> None:
    run(["docker", "pull", IMAGE_TAG])
    dockerfile = f"""FROM {IMAGE_TAG}
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD [\"python\", \"--version\"]
""".strip()
    Path("Dockerfile.generated").write_text(dockerfile, encoding="utf-8")
    run(["docker", "build", "-f", "Dockerfile.generated", "-t", APP_IMAGE, "."])


def mode_native() -> None:
    env = os.environ.copy()
    env.setdefault("PLAYWRIGHT_DOWNLOAD_HOST", "https://npmmirror.com/mirrors/playwright")
    env.setdefault("PLAYWRIGHT_CHROMIUM_DOWNLOAD_HOST", "https://cdn.npmmirror.com/binaries/chrome-for-testing")
    venv_python = Path("venv/bin/python")
    venv_pip = Path("venv/bin/pip")
    if not venv_python.exists():
        run([sys.executable, "-m", "venv", "venv"])
    run([str(venv_pip), "install", "-r", "requirements.txt"], env=env)
    run([str(venv_python), "-m", "playwright", "install", "chromium"], env=env)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "official"
    if mode == "official":
        mode_official()
    elif mode == "native":
        mode_native()
    else:
        raise SystemExit(f"Unknown mode: {mode}")
