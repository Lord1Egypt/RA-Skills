"""Suppress Windows console popups for subprocess calls."""
import platform
import subprocess

if platform.system() == "Windows":
    # Monkey-patch subprocess to hide console windows by default
    _original_run = subprocess.run
    _original_popen = subprocess.Popen

    def _patched_run(*args, **kwargs):
        if "creationflags" not in kwargs and platform.system() == "Windows":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        return _original_run(*args, **kwargs)

    def _patched_popen(*args, **kwargs):
        if "creationflags" not in kwargs and platform.system() == "Windows":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        return _original_popen(*args, **kwargs)

    subprocess.run = _patched_run
    subprocess.Popen = _patched_popen
