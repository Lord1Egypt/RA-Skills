"""Node.js import analysis using built-in parsing (no external deps)."""

import re
from pathlib import Path
from typing import Dict, List, Set
from ghostclaw.core.graph import ImportGraph

# Modules in these directories are typically orchestrators and naturally have high efferent coupling
ENTRY_POINT_DIRS: Set[str] = {'cli', 'scripts', 'bin', '__main__'}


class NodeImportAnalyzer:
    """Analyzes Node.js imports using pattern matching."""

    PATTERNS = [
        re.compile(r"import\s+(?:[\w*{}\n, ]+)\s+from\s+['\"]([^'\"\n]+)['\"]"),
        re.compile(r"import\s+['\"]([^'\"\n]+)['\"]"),
        re.compile(r"require\s*\(\s*['\"]([^'\"\n]+)['\"]\s*\)"),
        re.compile(r'require\s*\(\s*[\'"]([^\'"\n]+)[\'"]\s*\)'),
        re.compile(r"export\s*(?:[\w*{}\n, ]+)\s+from\s+['\"]([^'\"\n]+)['\"]"),
    ]

    def __init__(self, root: str):
        self.root = Path(root)
        self.graph = ImportGraph()

    def _module_name_from_file(self, filepath: Path) -> str:
        rel = filepath.relative_to(self.root)
        if rel.name in ('index.js', 'index.ts', 'index.jsx', 'index.tsx'):
            parent = rel.parent
            if parent == Path('.'):
                return '.'
            parts = list(parent.parts)
        else:
            parts = list(rel.with_suffix('').parts)
        # Strip leading 'src' if present
        if parts and parts[0] == 'src':
            parts = parts[1:]
        if not parts:
            return '.'
        return ".".join(parts).replace('/', '.')

    def _resolve_import_path(self, import_path: str, source_file: Path) -> Path:
        """
        Resolve an import path to an absolute file path within the project.
        Returns None if not found.
        """
        # Only handle relative imports
        if not import_path.startswith('.'):
            return None

        # Strip query and hash
        import_path = import_path.split('?')[0].split('#')[0]

        source_dir = source_file.parent
        candidate = (source_dir / import_path).resolve()

        # If candidate is a directory, look for index.js or package.json main
        if candidate.is_dir():
            for ext in ['.js', '.ts', '.jsx', '.tsx']:
                index_file = candidate / f'index{ext}'
                if index_file.exists():
                    return index_file
            # Could also check package.json main, but skip for now

        # If candidate is a file (with or without extension)
        if candidate.is_file():
            return candidate

        # Try adding common extensions
        for ext in ['.js', '.ts', '.jsx', '.tsx', '.json']:
            candidate_with_ext = candidate.with_suffix(ext) if not candidate.suffix else candidate
            if candidate_with_ext.is_file():
                return candidate_with_ext

        return None

    def analyze(self) -> Dict:
        issues = []
        ghosts = []
        flags = []

        # Find all Node source files
        node_exts = ['.js', '.jsx', '.ts', '.tsx']
        files = []
        for ext in node_exts:
            files.extend(self.root.rglob(f"*{ext}"))

        # Build module map
        known_modules = set()
        for f in files:
            module_name = self._module_name_from_file(f)
            self.graph.module_to_file[module_name] = str(f)
            self.graph.nodes.add(module_name)
            known_modules.add(module_name)

        # Parse each file for imports
        for f in files:
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                importer = self._module_name_from_file(f)
                imported_modules = set()

                for pattern in self.PATTERNS:
                    for match in pattern.finditer(content):
                        imported = match.group(1)
                        # Only handle local relative imports for coupling
                        resolved = self._resolve_import_path(imported, f)
                        if resolved and resolved.is_relative_to(self.root):
                            imported_module = self._module_name_from_file(resolved)
                            if imported_module in known_modules:
                                imported_modules.add(imported_module)

                # Add unique edges
                for imported_module in imported_modules:
                    self.graph.add_edge(importer, imported_module)
            except Exception:
                continue

        # Detect cycles
        cycles = self.graph.detect_circular_dependencies()
        if cycles:
            for cycle in cycles[:5]:
                cycle_str = " → ".join(cycle)
                issues.append(f"Circular dependency: {cycle_str}")
                ghosts.append(f"Circular dependency: {cycle_str}")
            if len(cycles) > 5:
                issues.append(f"... and {len(cycles)-5} more cycles")

        # Compute coupling metrics
        coupling_metrics = {}
        for node in self.graph.nodes:
            afferent = self.graph.get_afferent_coupling(node)
            efferent = self.graph.get_efferent_coupling(node)
            instability = self.graph.get_instability(node)
            coupling_metrics[node] = {
                "afferent": afferent,
                "efferent": efferent,
                "instability": round(instability, 2)
            }
            if instability > 0.8:
                # Skip entry points as they naturally import many things
                module_parts = set(node.split('.'))
                if any(entry in module_parts for entry in ENTRY_POINT_DIRS):
                    continue

                issues.append(f"Module {node} is highly unstable (I={instability:.2f}, ce={efferent})")
                ghosts.append(f"Unstable module {node}: knows too many others")

        return {
            "coupling_metrics": coupling_metrics,
            "circular_dependencies": [{"cycle": cycle} for cycle in cycles],
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": flags
        }
