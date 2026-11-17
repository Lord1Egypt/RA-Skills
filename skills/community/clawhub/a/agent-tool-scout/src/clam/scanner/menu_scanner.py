"""Probe macOS app menus via System Events UI Scripting.

This module discovers menu items that can be triggered via accessibility API,
enabling CLI wrappers for apps without .sdef scripting definitions.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field


@dataclass
class MenuItem:
    name: str           # "播放", "下一首"
    menu_bar_item: str  # "播放控制" (parent menu bar item)
    submenu_of: str | None = None  # parent menu item name if nested


@dataclass
class MenuGroup:
    """A menu bar item and its actionable menu items."""
    name: str                    # "播放控制"
    items: list[MenuItem] = field(default_factory=list)


@dataclass
class MenuScanResult:
    app_name: str
    process_name: str
    groups: list[MenuGroup] = field(default_factory=list)

    @property
    def total_items(self) -> int:
        return sum(len(g.items) for g in self.groups)


# Menu bar items to skip — standard macOS menus or OS-level menus
_SKIP_BARS = frozenset({
    "Apple", "帮助", "Help", "窗口", "Window",
    "编辑", "Edit",  # standard edit menu (undo/copy/paste)
    "Plugins", "Widgets",  # Figma-specific, not actionable
})

# Submenu parents whose children are dynamic/user-specific (e.g. recent files)
_SKIP_SUBMENUS = frozenset({
    "Recently Closed Tabs", "最近打开", "Open Recent", "最近使用的项目",
    "小程序",  # WeChat mini-programs
})


def _run_osascript(script: str, timeout: int = 10) -> str | None:
    """Run an AppleScript and return stdout, or None on failure."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


def _get_process_name(app_name: str) -> str | None:
    """Get the System Events process name for an app.

    Prefers foreground (non-background-only) processes to avoid picking
    helper agents like "figma_agent" instead of the main "Figma" process.
    """
    script = f'''
tell application "System Events"
    set procs to every process whose name contains "{app_name}" and background only is false
    if (count of procs) > 0 then
        return name of item 1 of procs
    end if
    -- Fallback to any matching process
    set procs to every process whose name contains "{app_name}"
    if (count of procs) > 0 then
        return name of item 1 of procs
    end if
end tell'''
    return _run_osascript(script)


def scan_menus(app_name: str, process_name: str | None = None) -> MenuScanResult | None:
    """Scan an app's menu bar for actionable menu items.

    The app must be running. Returns None if menus are inaccessible.

    Args:
        app_name: Display name or bundle name (e.g. "QQMusic").
        process_name: System Events process name; auto-detected if omitted.
    """
    if process_name is None:
        process_name = _get_process_name(app_name)
        if not process_name:
            return None

    # Step 1: Get menu bar item names
    bar_script = f'''
tell application "System Events"
    tell process "{process_name}"
        get name of every menu bar item of menu bar 1
    end tell
end tell'''
    raw = _run_osascript(bar_script)
    if not raw:
        return None

    bar_names = [n.strip() for n in raw.split(",")]
    result = MenuScanResult(app_name=app_name, process_name=process_name)

    for idx, bar_name in enumerate(bar_names):
        if bar_name in _SKIP_BARS:
            continue
        # Skip the app's own app-menu (2nd bar item, after Apple).
        # It always contains standard items: About, Hide, Quit, Preferences.
        if idx <= 1:
            continue

        group = _scan_menu_group(process_name, bar_name)
        if group and group.items:
            result.groups.append(group)

    return result


def _scan_menu_group(process_name: str, bar_name: str) -> MenuGroup | None:
    """Scan a single menu bar item for its menu items (including one level of submenus)."""
    script = f'''
tell application "System Events"
    tell process "{process_name}"
        set output to ""
        try
            set menuItems to every menu item of menu 1 of menu bar item "{bar_name}" of menu bar 1
            repeat with mi in menuItems
                try
                    set n to name of mi
                    if n is not missing value then
                        -- Check for submenu
                        try
                            set subItems to every menu item of menu 1 of mi
                            repeat with si in subItems
                                try
                                    set sn to name of si
                                    if sn is not missing value then
                                        set output to output & "SUB:" & n & ":" & sn & linefeed
                                    end if
                                end try
                            end repeat
                        on error
                            set output to output & "ITEM:" & n & linefeed
                        end try
                    end if
                end try
            end repeat
        end try
        return output
    end tell
end tell'''

    raw = _run_osascript(script, timeout=15)
    if not raw:
        return None

    group = MenuGroup(name=bar_name)
    for line in raw.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("ITEM:"):
            name = line[5:]
            if name and not _should_skip_item(name):
                group.items.append(MenuItem(
                    name=name,
                    menu_bar_item=bar_name,
                ))
        elif line.startswith("SUB:"):
            parts = line[4:].split(":", 1)
            if len(parts) == 2 and parts[1]:
                # Skip dynamic/user-specific submenus
                if parts[0] in _SKIP_SUBMENUS:
                    continue
                if not _should_skip_item(parts[1]):
                    group.items.append(MenuItem(
                        name=parts[1],
                        menu_bar_item=bar_name,
                        submenu_of=parts[0],
                    ))

    return group


def _should_skip_item(name: str) -> bool:
    """Skip menu items that are not actionable commands."""
    lower = name.lower()
    # "Unavailable" placeholders
    if "unavailable" in lower:
        return True
    return False
