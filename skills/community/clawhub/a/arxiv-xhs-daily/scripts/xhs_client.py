from __future__ import annotations

import os
import subprocess

DEFAULT_CONFIG_PATH = "/Users/ailor/.openclaw/workspace/config/mcporter.json"


class XHSClient:
    def __init__(self, server_name: str = "xiaohongshu-mcp", config_path: str | None = None) -> None:
        self.server_name = server_name
        self.config_path = config_path or os.environ.get("MCPORTER_CONFIG_PATH", DEFAULT_CONFIG_PATH)

    def publish_content(self, title: str, content: str, images: list[str]) -> str:
        image_literals = ", ".join(f'"{self._escape(path)}"' for path in images)
        expr = (
            f'{self.server_name}.publish_content('
            f'content: "{self._escape(content)}", '
            f'images: [{image_literals}], '
            f'title: "{self._escape(title)}")'
        )
        return self._run(expr, timeout_ms=240000)

    def _run(self, expr: str, timeout_ms: int = 180000) -> str:
        command = ["mcporter", "call", "--config", self.config_path, "--timeout", str(timeout_ms), expr]
        completed = subprocess.run(command, capture_output=True, text=True)
        if completed.returncode != 0:
            raise RuntimeError(
                f"mcporter call failed: expr={expr}\nstdout={completed.stdout.strip()}\nstderr={completed.stderr.strip()}"
            )
        stdout = completed.stdout.strip()
        return stdout or completed.stderr.strip()

    @staticmethod
    def _escape(value: str) -> str:
        return value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
