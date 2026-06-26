"""Cross-platform service manager: install/uninstall/start/stop/status for ws_listener background process.

[INPUT]: sys.platform, subprocess, pathlib, SDKConfig, logging_config
[OUTPUT]: ServiceManager (base), MacOSServiceManager, LinuxServiceManager, WindowsServiceManager, get_service_manager()
[POS]: Abstraction layer between ws_listener.py CLI and OS-specific service management (launchd / systemd / Task Scheduler)

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from utils.config import SDKConfig
from utils.logging_config import find_latest_log_file, get_log_dir, get_log_file_path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SERVICE_LABEL = "com.awiki.ws-listener"


def _application_log_path() -> Path:
    """Return the current or latest application log file path under <DATA_DIR>/logs."""
    log_dir = get_log_dir(SDKConfig())
    return find_latest_log_file(log_dir) or get_log_file_path(log_dir)


class ServiceManager(ABC):
    """Base class for platform-specific service managers."""

    @abstractmethod
    def install(self, credential: str, config_path: str | None, mode: str | None) -> None:
        """Install and start the background service."""

    @abstractmethod
    def uninstall(self) -> None:
        """Stop and remove the background service."""

    @abstractmethod
    def start(self) -> None:
        """Start an installed service."""

    @abstractmethod
    def stop(self) -> None:
        """Stop a running service."""

    @abstractmethod
    def status(self) -> dict[str, Any]:
        """Return service status as a dict."""

    @abstractmethod
    def log_dir(self) -> Path:
        """Return the platform-specific log directory."""

    @abstractmethod
    def is_installed(self) -> bool:
        """Check if the service is installed."""

    @staticmethod
    def _user_path() -> str:
        """Return the current user's PATH for service environment."""
        return os.environ.get("PATH", "")

    def find_python(self) -> str:
        """Find the best Python interpreter path."""
        if sys.platform == "win32":
            venv_python = _PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
        else:
            venv_python = _PROJECT_ROOT / ".venv" / "bin" / "python"
        if venv_python.exists():
            return str(venv_python)
        return sys.executable

    def _build_run_args(self, credential: str, config_path: str | None, mode: str | None) -> list[str]:
        """Build the command-line arguments for 'ws_listener.py run'."""
        python_path = self.find_python()
        script_path = str((_PROJECT_ROOT / "scripts" / "ws_listener.py").resolve())
        args = [python_path, script_path, "run", "--credential", credential]
        if config_path:
            args.extend(["--config", str(Path(config_path).resolve())])
        if mode:
            args.extend(["--mode", mode])
        return args

    def _ensure_log_dir(self) -> Path:
        """Create and return the log directory."""
        d = self.log_dir()
        d.mkdir(parents=True, exist_ok=True)
        return d


# ---------------------------------------------------------------------------
# macOS  —  launchd
# ---------------------------------------------------------------------------

class MacOSServiceManager(ServiceManager):
    """macOS service manager using launchd (LaunchAgent)."""

    def __init__(self) -> None:
        self._agents_dir = Path.home() / "Library" / "LaunchAgents"
        self._plist_path = self._agents_dir / f"{_SERVICE_LABEL}.plist"

    def log_dir(self) -> Path:
        return Path.home() / "Library" / "Logs" / "awiki-ws-listener"

    def is_installed(self) -> bool:
        return self._plist_path.exists()

    # -- public API --

    def install(self, credential: str, config_path: str | None, mode: str | None) -> None:
        if self._plist_path.exists():
            print(f"Service already installed: {self._plist_path}")
            print("To reinstall, run first: python scripts/ws_listener.py uninstall")
            return

        self._agents_dir.mkdir(parents=True, exist_ok=True)
        logs = self._ensure_log_dir()

        plist_content = self._generate_plist(credential, config_path, mode, logs)
        self._plist_path.write_text(plist_content, encoding="utf-8")
        print(f"plist written to: {self._plist_path}")

        result = self._launchctl("load", str(self._plist_path))
        if result.returncode == 0:
            print("Service installed and started")
            print(f"  Logs: tail -f {logs / 'stderr.log'}")
            print(f"  App logs: tail -f {_application_log_path()}")
        else:
            print(f"launchctl load failed: {result.stderr.strip()}")

    def uninstall(self) -> None:
        if not self._plist_path.exists():
            print("Service not installed")
            return
        result = self._launchctl("unload", str(self._plist_path))
        if result.returncode != 0:
            print(f"launchctl unload warning: {result.stderr.strip()}")
        self._plist_path.unlink()
        print("Service uninstalled")

    def start(self) -> None:
        if not self._plist_path.exists():
            print("Service not installed, run first: python scripts/ws_listener.py install")
            return
        result = self._launchctl("load", str(self._plist_path))
        if result.returncode == 0:
            print("Service started")
        else:
            print(f"Start failed: {result.stderr.strip()}")

    def stop(self) -> None:
        if not self._plist_path.exists():
            print("Service not installed")
            return
        result = self._launchctl("unload", str(self._plist_path))
        if result.returncode == 0:
            print("Service stopped")
        else:
            print(f"Stop failed: {result.stderr.strip()}")

    def status(self) -> dict[str, Any]:
        output: dict[str, Any] = {
            "platform": "macOS (launchd)",
            "installed": self._plist_path.exists(),
            "service_file": str(self._plist_path),
            "application_log_dir": str(get_log_dir(SDKConfig())),
            "application_log_path": str(_application_log_path()),
        }
        if self._plist_path.exists():
            result = self._launchctl("list")
            output["running"] = _SERVICE_LABEL in result.stdout

            try:
                plist_text = self._plist_path.read_text(encoding="utf-8")
                if "--mode" in plist_text:
                    parts = plist_text.split("--mode")
                    if len(parts) > 1:
                        match = re.search(r"<string>(\w[\w-]*)</string>", parts[1])
                        if match:
                            output["mode"] = match.group(1)
            except Exception:
                pass

            stderr_log = self.log_dir() / "stderr.log"
            if stderr_log.exists():
                output["log_size_bytes"] = stderr_log.stat().st_size
                output["log_path"] = str(stderr_log)
            app_log = _application_log_path()
            if app_log.exists():
                output["application_log_size_bytes"] = app_log.stat().st_size
        else:
            output["running"] = False
        return output

    # -- internal helpers --

    @staticmethod
    def _launchctl(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["launchctl", *args],
            capture_output=True, text=True,
        )

    def _generate_plist(
        self,
        credential: str,
        config_path: str | None,
        mode: str | None,
        logs: Path,
    ) -> str:
        run_args = self._build_run_args(credential, config_path, mode)
        args_xml = "\n        ".join(f"<string>{a}</string>" for a in run_args)
        user_path = self._user_path()
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{_SERVICE_LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        {args_xml}
    </array>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>{user_path}</string>
    </dict>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>ThrottleInterval</key>
    <integer>10</integer>

    <key>WorkingDirectory</key>
    <string>{_PROJECT_ROOT}</string>

    <key>StandardOutPath</key>
    <string>{logs / 'stdout.log'}</string>
    <key>StandardErrorPath</key>
    <string>{logs / 'stderr.log'}</string>
</dict>
</plist>
"""


# ---------------------------------------------------------------------------
# Linux  —  systemd user service
# ---------------------------------------------------------------------------

class LinuxServiceManager(ServiceManager):
    """Linux service manager using systemd user units."""

    _UNIT_NAME = "awiki-ws-listener.service"

    def __init__(self) -> None:
        config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        self._unit_dir = config_home / "systemd" / "user"
        self._unit_path = self._unit_dir / self._UNIT_NAME

    def log_dir(self) -> Path:
        state_home = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
        return state_home / "awiki-ws-listener" / "logs"

    def is_installed(self) -> bool:
        return self._unit_path.exists()

    # -- public API --

    def install(self, credential: str, config_path: str | None, mode: str | None) -> None:
        if self._unit_path.exists():
            print(f"Service already installed: {self._unit_path}")
            print("To reinstall, run first: python scripts/ws_listener.py uninstall")
            return

        self._unit_dir.mkdir(parents=True, exist_ok=True)
        logs = self._ensure_log_dir()

        unit_content = self._generate_unit(credential, config_path, mode, logs)
        self._unit_path.write_text(unit_content, encoding="utf-8")
        print(f"Unit file written to: {self._unit_path}")

        self._systemctl("daemon-reload")
        result = self._systemctl("enable", "--now", self._UNIT_NAME)
        if result.returncode == 0:
            print("Service installed and started")
            print(f"  Logs: journalctl --user -u {self._UNIT_NAME} -f")
            print(f"  File logs: tail -f {logs / 'stderr.log'}")
            print(f"  App logs: tail -f {_application_log_path()}")
            print()
            print("Hint: For headless servers (SSH-only, no GUI session), run:")
            print("  sudo loginctl enable-linger $USER")
            print("This allows the user service to start at boot without a login session.")
        else:
            print(f"systemctl enable --now failed: {result.stderr.strip()}")

    def uninstall(self) -> None:
        if not self._unit_path.exists():
            print("Service not installed")
            return
        self._systemctl("disable", "--now", self._UNIT_NAME)
        self._unit_path.unlink()
        self._systemctl("daemon-reload")
        print("Service uninstalled")

    def start(self) -> None:
        if not self._unit_path.exists():
            print("Service not installed, run first: python scripts/ws_listener.py install")
            return
        result = self._systemctl("start", self._UNIT_NAME)
        if result.returncode == 0:
            print("Service started")
        else:
            print(f"Start failed: {result.stderr.strip()}")

    def stop(self) -> None:
        if not self._unit_path.exists():
            print("Service not installed")
            return
        result = self._systemctl("stop", self._UNIT_NAME)
        if result.returncode == 0:
            print("Service stopped")
        else:
            print(f"Stop failed: {result.stderr.strip()}")

    def status(self) -> dict[str, Any]:
        output: dict[str, Any] = {
            "platform": "Linux (systemd)",
            "installed": self._unit_path.exists(),
            "service_file": str(self._unit_path),
            "application_log_dir": str(get_log_dir(SDKConfig())),
            "application_log_path": str(_application_log_path()),
        }
        if self._unit_path.exists():
            result = self._systemctl("is-active", self._UNIT_NAME)
            state = result.stdout.strip()
            output["running"] = state == "active"
            output["state"] = state

            try:
                unit_text = self._unit_path.read_text(encoding="utf-8")
                for line in unit_text.splitlines():
                    if "--mode" in line:
                        match = re.search(r"--mode\s+(\S+)", line)
                        if match:
                            output["mode"] = match.group(1)
                            break
            except Exception:
                pass

            stderr_log = self.log_dir() / "stderr.log"
            if stderr_log.exists():
                output["log_size_bytes"] = stderr_log.stat().st_size
                output["log_path"] = str(stderr_log)
            app_log = _application_log_path()
            if app_log.exists():
                output["application_log_size_bytes"] = app_log.stat().st_size
        else:
            output["running"] = False
        return output

    # -- internal helpers --

    @staticmethod
    def _systemctl(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["systemctl", "--user", *args],
            capture_output=True, text=True,
        )

    def _generate_unit(
        self,
        credential: str,
        config_path: str | None,
        mode: str | None,
        logs: Path,
    ) -> str:
        run_args = self._build_run_args(credential, config_path, mode)
        exec_start = " ".join(run_args)
        user_path = self._user_path()
        return f"""[Unit]
Description=awiki WebSocket Listener
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart={exec_start}
WorkingDirectory={_PROJECT_ROOT}
Environment=PATH={user_path}
Restart=on-failure
RestartSec=10
StandardOutput=append:{logs / 'stdout.log'}
StandardError=append:{logs / 'stderr.log'}

[Install]
WantedBy=default.target
"""


# ---------------------------------------------------------------------------
# Windows  —  Task Scheduler
# ---------------------------------------------------------------------------

class WindowsServiceManager(ServiceManager):
    """Windows service manager using Task Scheduler (schtasks)."""

    _TASK_NAME = "awiki-ws-listener"

    def __init__(self) -> None:
        local_app = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        self._app_dir = local_app / "awiki-ws-listener"
        self._bat_path = self._app_dir / "run-listener.bat"

    def log_dir(self) -> Path:
        return self._app_dir / "logs"

    def is_installed(self) -> bool:
        result = subprocess.run(
            ["schtasks", "/Query", "/TN", self._TASK_NAME],
            capture_output=True, text=True,
        )
        return result.returncode == 0

    # -- public API --

    def install(self, credential: str, config_path: str | None, mode: str | None) -> None:
        if self.is_installed():
            print(f"Task '{self._TASK_NAME}' already exists in Task Scheduler")
            print("To reinstall, run first: python scripts/ws_listener.py uninstall")
            return

        self._app_dir.mkdir(parents=True, exist_ok=True)
        logs = self._ensure_log_dir()

        bat_content = self._generate_bat(credential, config_path, mode, logs)
        self._bat_path.write_text(bat_content, encoding="utf-8")
        print(f"Batch file written to: {self._bat_path}")

        result = subprocess.run(
            [
                "schtasks", "/Create",
                "/TN", self._TASK_NAME,
                "/TR", str(self._bat_path),
                "/SC", "ONLOGON",
                "/RL", "LIMITED",
                "/F",
            ],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"schtasks /Create failed: {result.stderr.strip()}")
            return

        print("Scheduled task created")

        run_result = subprocess.run(
            ["schtasks", "/Run", "/TN", self._TASK_NAME],
            capture_output=True, text=True,
        )
        if run_result.returncode == 0:
            print("Service installed and started")
        else:
            print(f"Task created but start failed: {run_result.stderr.strip()}")

        print(f"  Logs: {logs}")
        print(f"  App logs: {_application_log_path()}")

    def uninstall(self) -> None:
        if not self.is_installed():
            print("Service not installed")
            return
        subprocess.run(
            ["schtasks", "/End", "/TN", self._TASK_NAME],
            capture_output=True, text=True,
        )
        result = subprocess.run(
            ["schtasks", "/Delete", "/TN", self._TASK_NAME, "/F"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print("Scheduled task removed")
        else:
            print(f"schtasks /Delete warning: {result.stderr.strip()}")

        if self._bat_path.exists():
            self._bat_path.unlink()
        print("Service uninstalled")

    def start(self) -> None:
        if not self.is_installed():
            print("Service not installed, run first: python scripts/ws_listener.py install")
            return
        result = subprocess.run(
            ["schtasks", "/Run", "/TN", self._TASK_NAME],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print("Service started")
        else:
            print(f"Start failed: {result.stderr.strip()}")

    def stop(self) -> None:
        if not self.is_installed():
            print("Service not installed")
            return
        result = subprocess.run(
            ["schtasks", "/End", "/TN", self._TASK_NAME],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print("Service stopped")
        else:
            print(f"Stop failed: {result.stderr.strip()}")

    def status(self) -> dict[str, Any]:
        installed = self.is_installed()
        output: dict[str, Any] = {
            "platform": "Windows (Task Scheduler)",
            "installed": installed,
            "task_name": self._TASK_NAME,
            "application_log_dir": str(get_log_dir(SDKConfig())),
            "application_log_path": str(_application_log_path()),
        }
        if installed:
            result = subprocess.run(
                ["schtasks", "/Query", "/TN", self._TASK_NAME, "/FO", "LIST", "/V"],
                capture_output=True, text=True,
            )
            output["running"] = "Running" in result.stdout
            output["details"] = result.stdout.strip()

            stderr_log = self.log_dir() / "stderr.log"
            if stderr_log.exists():
                output["log_size_bytes"] = stderr_log.stat().st_size
                output["log_path"] = str(stderr_log)
            app_log = _application_log_path()
            if app_log.exists():
                output["application_log_size_bytes"] = app_log.stat().st_size
        else:
            output["running"] = False
        return output

    # -- internal helpers --

    def _generate_bat(
        self,
        credential: str,
        config_path: str | None,
        mode: str | None,
        logs: Path,
    ) -> str:
        run_args = self._build_run_args(credential, config_path, mode)
        cmd_line = " ".join(f'"{a}"' for a in run_args)
        return f"""@echo off
REM awiki WebSocket Listener — auto-generated, do not edit manually
cd /d "{_PROJECT_ROOT}"
{cmd_line} >> "{logs / 'stdout.log'}" 2>> "{logs / 'stderr.log'}"
"""


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def get_service_manager() -> ServiceManager:
    """Return the appropriate ServiceManager for the current platform."""
    if sys.platform == "darwin":
        return MacOSServiceManager()
    if sys.platform == "linux":
        return LinuxServiceManager()
    if sys.platform == "win32":
        return WindowsServiceManager()
    raise RuntimeError(f"Unsupported platform: {sys.platform}")


__all__ = [
    "ServiceManager",
    "MacOSServiceManager",
    "LinuxServiceManager",
    "WindowsServiceManager",
    "get_service_manager",
]
