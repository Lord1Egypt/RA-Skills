#!/usr/bin/env python3
"""
Gradle module resolver for project_scan.

Reads settings.gradle(.kts) to discover all project modules,
then filters to those with actual resources or source code to scan.
"""

import re
from pathlib import Path


def parse_settings_modules(project_root: str) -> list[str]:
    """
    Parse settings.gradle(.kts) to get all declared modules.
    
    Looks for: include(":app"), include ':lib', etc.
    Returns list of module paths like [':app', ':core:ui', ':LibCommon'].
    """
    root = Path(project_root)
    settings_file = None
    for name in ("settings.gradle.kts", "settings.gradle"):
        candidate = root / name
        if candidate.exists():
            settings_file = candidate
            break
    
    if not settings_file:
        return []
    
    text = settings_file.read_text(encoding="utf-8")
    modules = []
    
    # include(":module:path") or include ':module:path'
    for match in re.finditer(r"""include\s*\(?\s*["']([^"']+)["']""", text):
        mod = match.group(1)
        if mod not in modules:
            modules.append(mod)
    
    return modules


def resolve_all_modules(project_root: str, target_module: str | None = None) -> dict:
    """
    Discover all modules from settings.gradle, filter to those worth scanning.
    
    A module is "worth scanning" if it has res/ or source code under src/main/.
    
    Args:
        project_root: Path to Android project root.
        target_module: Optional target module name (e.g. ':app').
                       Used to mark which module is the primary target.
    
    Returns:
        {
            "target": Path | None,
            "target_name": str,
            "scannable": [(name, Path), ...],  # modules with res/ or src/
            "skipped": [str, ...],             # modules without scannable content
            "errors": [str, ...],
        }
    """
    root = Path(project_root)
    target_name = target_module or "app"
    result = {
        "target": None,
        "target_name": target_name,
        "scannable": [],
        "skipped": [],
        "errors": [],
    }
    
    all_modules = parse_settings_modules(project_root)
    if not all_modules:
        result["errors"].append(
            f"No settings.gradle(.kts) found or no modules declared in {project_root}"
        )
        return result
    
    for mod_name in all_modules:
        mod_dir = _find_module_dir(root, mod_name)
        if not mod_dir:
            result["skipped"].append(mod_name)
            continue
        
        if _has_scannable_content(mod_dir):
            result["scannable"].append((mod_name, mod_dir))
            # Mark target
            if mod_name.lstrip(":") == target_name.lstrip(":"):
                result["target"] = mod_dir
        else:
            result["skipped"].append(mod_name)
    
    if result["target"] is None:
        result["errors"].append(f"Target module '{target_name}' not found or has no content")
    
    return result


def _find_module_dir(root: Path, module_name: str) -> Path | None:
    """Convert Gradle module path to filesystem path and verify it exists."""
    rel_path = module_name.lstrip(":").replace(":", "/")
    candidate = root / rel_path
    if candidate.is_dir():
        return candidate
    return None


def _has_scannable_content(module_dir: Path) -> bool:
    """Check if a module has resources or source code worth scanning."""
    src_main = module_dir / "src" / "main"
    if not src_main.is_dir():
        return False
    
    # Has res/values/ (colors, strings, etc.)
    if (src_main / "res" / "values").is_dir():
        return True
    # Has res/drawable/ 
    if any((src_main / "res").glob("drawable*")) if (src_main / "res").is_dir() else False:
        return True
    # Has source code (for custom View scanning)
    if (src_main / "java").is_dir() or (src_main / "kotlin").is_dir():
        return True
    
    return False
