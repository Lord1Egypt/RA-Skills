"""Import coupling analysis — detect dependencies, circular imports, layer violations."""

import ast
from pathlib import Path
from typing import Dict, List, Set
from ghostclaw.core.graph import ImportGraph

# Modules in these directories are typically orchestrators and naturally have high efferent coupling
ENTRY_POINT_DIRS: Set[str] = {'cli', 'scripts', 'bin', '__main__'}


class PythonImportAnalyzer:
    """Analyzes Python imports using AST."""

    def __init__(self, root: str):
        self.root = Path(root)
        self.graph = ImportGraph()

    def analyze(self) -> Dict:
        """
        Scan all .py files and build import dependency graph.

        Returns:
            Dict with coupling metrics and detected issues
        """
        # Map file paths to module names (relative to root, with optional 'src' prefix stripped)
        for py_file in self.root.rglob("*.py"):
            rel_path = py_file.relative_to(self.root)
            # Convert path to dotted module name
            if rel_path.name == "__init__.py":
                parts = list(rel_path.parent.parts)
            else:
                parts = list(rel_path.with_suffix("").parts)
            # Strip leading 'src' directory to align with import paths (src layout)
            if parts and parts[0] == 'src':
                parts = parts[1:]
            module_name = ".".join(parts)
            self.graph.module_to_file[module_name] = str(py_file)
            self.graph.nodes.add(module_name)

        # Parse each file and extract imports
        for module_name, filepath in self.graph.module_to_file.items():
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imported_module = alias.name
                            if self._is_local_import(imported_module):
                                self.graph.add_edge(module_name, imported_module)
                    elif isinstance(node, ast.ImportFrom):
                        imported_module = self._resolve_relative_import(module_name, node)
                        if imported_module and self._is_local_import(imported_module):
                            self.graph.add_edge(module_name, imported_module)
            except Exception:
                continue  # Skip files with parse errors

        # Compute metrics
        return self._compute_report()

    def _resolve_relative_import(self, current_module: str, node: ast.ImportFrom) -> str:
        """Resolve a relative or absolute 'from' import to an absolute module name."""
        if node.level == 0:
            return node.module

        # PEP 328: relative import dots indicate parent packages.
        # Determine the package name of the current module.
        parts = current_module.split('.')
        # Check if current_module is a package (i.e., __init__.py)
        filepath = self.graph.module_to_file.get(current_module)
        is_package = filepath and filepath.endswith('__init__.py')
        if is_package:
            base_parts = parts  # the package is the full module name
        else:
            base_parts = parts[:-1] if parts else []

        # Move up (node.level - 1) levels from base
        up_levels = node.level - 1
        if up_levels > 0:
            if up_levels > len(base_parts):
                return None  # invalid relative import
            base_parts = base_parts[:-up_levels]

        base = ".".join(base_parts)
        if node.module:
            return f"{base}.{node.module}" if base else node.module
        return base

    def _is_local_import(self, module_name: str) -> bool:
        """Check if an import is likely from the local project (not stdlib/third-party)."""
        if not module_name:
            return False
        if module_name in self.graph.nodes:
            return True
        # Also check prefix: import of a submodule within a known package
        for known in self.graph.nodes:
            if module_name.startswith(known + '.'):
                return True
        return False

    def _compute_report(self) -> Dict:
        """Generate coupling report with issues."""
        issues = []
        ghosts = []
        flags = []

        # Detect circular dependencies
        cycles = self.graph.detect_circular_dependencies()
        if cycles:
            for cycle in cycles[:5]:  # Limit to first 5
                cycle_str = " → ".join(cycle)
                issues.append(f"Circular dependency: {cycle_str}")
                ghosts.append(f"Circular dependency: {cycle_str}")
            if len(cycles) > 5:
                issues.append(f"... and {len(cycles) - 5} more cycles")

        # Identify highly unstable modules (God modules)
        for module in self.graph.nodes:
            # Skip entry points as they naturally import many things
            module_parts = set(module.split('.'))
            if any(entry in module_parts for entry in ENTRY_POINT_DIRS):
                continue

            instability = self.graph.get_instability(module)
            if instability > 0.8:
                ce = self.graph.get_efferent_coupling(module)
                issues.append(f"Module {module} is highly unstable (I={instability:.2f}, ce={ce})")
                ghosts.append(f"Unstable module {module}: knows too many others")

        # Modules with high afferent coupling (utility modules)
        for module in self.graph.nodes:
            ca = self.graph.get_afferent_coupling(module)
            if ca > 10:
                issues.append(f"Module {module} is heavily depended upon (ca={ca}) — treat as stable layer")

        return {
            "coupling_metrics": {
                module: {
                    "afferent": self.graph.get_afferent_coupling(module),
                    "efferent": self.graph.get_efferent_coupling(module),
                    "instability": round(self.graph.get_instability(module), 2)
                }
                for module in self.graph.nodes
            },
            "circular_dependencies": [{"cycle": cycle} for cycle in cycles],
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": flags
        }
