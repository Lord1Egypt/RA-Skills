"""
Desktop Control Skill for OpenClaw
Optimized desktop automation with mouse, keyboard, and screen control

Usage:
    from desktop_control import DesktopController

    with DesktopController() as dc:
        dc.move_mouse(500, 300)
        dc.click()
        dc.type_text("Hello World!")
"""

from .desktop_control import (
    DesktopController,
    get_controller,
    reset_controller,
    move,
    click,
    typewrite,
    hotkey,
    screenshot,
    retry_on_error,
)

__version__ = "1.0.0"
__all__ = [
    "DesktopController",
    "get_controller",
    "reset_controller",
    "move",
    "click",
    "typewrite",
    "hotkey",
    "screenshot",
    "retry_on_error",
]
