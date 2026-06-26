#!/usr/bin/env python3
"""
Android module dependency resolver.

Parses build.gradle(.kts) files to build a dependency graph,
so we know which module's resources are visible to which modules.
"""

from __future__ import annotations

import re
from pathlib import Path


def parse_module_deps(module_dir: Path) -> list[str]:
    """
    Parse implementation/api project dependencies from build.gradle(.kts).

    Returns list of module names like [':core:ui', ':LibCommon'].
    """
    deps: list[str] = []
    for name in ("build.gradle.kts", "build.gradle"):
        gradle = module_dir / name
        if gradle.is_file():
            try:
                text = gradle.read_text(encoding="utf-8")
            except OSError:
                continue
            # implementation(project(":core:ui"))
            # api(project(":LibCommon"))
            for m in re.finditer(
                r'(?:implementation|api)\s*\(\s*project\s*\(\s*"([^"]+)"\s*\)',
                text,
            ):
                dep = m.group(1)
                if dep not in deps:
                    deps.append(dep)
            # Groovy: implementation project(':core:ui')
            for m in re.finditer(
                r"(?:implementation|api)\s+project\s*\(\s*'([^']+)'\s*\)",
                text,
            ):
                dep = m.group(1)
                if dep not in deps:
                    deps.append(dep)
            break
    return deps


def build_dep_graph(
    project_root: str,
    scannable: list[tuple[str, Path]],
) -> dict[str, list[str]]:
    """
    Build a dependency graph for all scannable modules.

    Returns: { ":app": [":core:ui", ":LibCommon", ...], ... }
    """
    graph: dict[str, list[str]] = {}
    for mod_name, mod_dir in scannable:
        graph[mod_name] = parse_module_deps(mod_dir)
    return graph


def visible_resources(
    target_module: str,
    dep_graph: dict[str, list[str]],
) -> set[str]:
    """
    Get all modules whose resources are visible to target_module.

    Includes direct deps + transitive (simple BFS, 2 levels deep).
    Returns set of module names including target itself.
    """
    visible = {target_module}
    # Direct deps
    direct = set(dep_graph.get(target_module, []))
    visible |= direct
    # One level transitive (api deps propagate)
    for dep in direct:
        visible |= set(dep_graph.get(dep, []))
    return visible
