#!/usr/bin/env python3
"""
Diagram Generation Script

Generates architecture diagrams in various formats (Mermaid, DOT/Graphviz).
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


class DiagramGenerator:
    """Generates architecture diagrams"""
    
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.modules: Dict[str, Set[str]] = defaultdict(set)
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self._analyze_structure()
    
    def _analyze_structure(self):
        """Analyze codebase structure"""
        ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                       'dist', 'build', 'target', '.idea', '.vscode'}
        
        for filepath in self.root.rglob('*'):
            if not filepath.is_file():
                continue
            
            # Skip ignored directories
            if any(part in ignore_dirs for part in filepath.parts):
                continue
            
            # Get module (directory) name
            try:
                rel_path = filepath.relative_to(self.root)
            except ValueError:
                continue
            
            if len(rel_path.parts) > 1:
                module = rel_path.parts[0]
                self.modules[module].add(filepath.suffix.lower())
                
                # Try to detect dependencies from imports
                deps = self._extract_deps_from_file(filepath)
                for dep in deps:
                    if dep in self.modules or self._is_likely_module(dep):
                        self.dependencies[module].add(dep)
    
    def _extract_deps_from_file(self, filepath: Path) -> Set[str]:
        """Extract dependencies from a file"""
        deps = set()
        ext = filepath.suffix.lower()
        
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            
            if ext == '.py':
                # Python imports
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        if line.startswith('import '):
                            mod = line[7:].split()[0].split('.')[0]
                        else:
                            parts = line[5:].split(' import')
                            if parts:
                                mod = parts[0].strip().split('.')[0]
                            else:
                                continue
                        if mod and not self._is_stdlib_py(mod):
                            deps.add(mod)
            
            elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                # JS/TS imports
                for line in content.split('\n'):
                    line = line.strip()
                    if 'from ' in line or 'require(' in line:
                        if 'from ' in line:
                            parts = line.split('from ')
                            if len(parts) > 1:
                                pkg = parts[1].strip().strip('"\';`')
                                if pkg.startswith('.'):
                                    # Local import - resolve
                                    local_dep = self._resolve_local_import(filepath, pkg)
                                    if local_dep:
                                        deps.add(local_dep)
                                elif not pkg.startswith('@types'):
                                    deps.add(pkg.split('/')[0])
            
            elif ext == '.go':
                # Go imports
                in_import = False
                for line in content.split('\n'):
                    line = line.strip()
                    if 'import (' in line:
                        in_import = True
                    elif in_import and line.startswith(')'):
                        in_import = False
                    elif in_import or line.startswith('import '):
                        if '"' in line:
                            parts = line.split('"')
                            for i in range(1, len(parts), 2):
                                pkg = parts[i]
                                if pkg and not pkg.startswith('.'):
                                    deps.add(pkg.split('/')[0])
            
        except Exception:
            pass
        
        return deps
    
    def _resolve_local_import(self, source_file: Path, import_path: str) -> Optional[str]:
        """Resolve a local import to a module name"""
        # Simple resolution - get the first directory component
        if import_path.startswith('./') or import_path.startswith('../'):
            # Count leading ../
            parts = import_path.split('/')
            if len(parts) > 1:
                # Try to find which module this points to
                for part in parts:
                    if part and part not in ['.', '..']:
                        return part
        return None
    
    def _is_likely_module(self, name: str) -> bool:
        """Check if a name is likely a module in the project"""
        # Check if directory exists
        return (self.root / name).is_dir()
    
    def _is_stdlib_py(self, module: str) -> bool:
        """Check if Python module is stdlib"""
        stdlib = {'os', 'sys', 'json', 're', 'collections', 'itertools', 'functools',
                  'datetime', 'pathlib', 'typing', 'argparse', 'subprocess', 'tempfile',
                  'shutil', 'glob', 'hashlib', 'base64', 'urllib', 'http', 'socket',
                  'asyncio', 'unittest', 'logging', 'warnings', 'inspect', 'copy'}
        return module in stdlib
    
    def generate_mermaid(self, max_nodes: int = 30) -> str:
        """Generate Mermaid diagram"""
        lines = ["```mermaid", "graph TD"]
        
        # Create module nodes
        modules = list(self.modules.keys())[:max_nodes]
        node_ids = {}
        
        for i, module in enumerate(modules):
            node_id = f"M{i}"
            node_ids[module] = node_id
            
            # Get file types for icon
            extensions = self.modules[module]
            icon = self._get_module_icon(extensions)
            
            lines.append(f'    {node_id}["{icon} {module}"]')
        
        # Create edges
        edges_added = set()
        for module, deps in self.dependencies.items():
            if module not in node_ids:
                continue
            
            for dep in deps:
                if dep in node_ids and dep != module:
                    edge = (node_ids[module], node_ids[dep])
                    if edge not in edges_added:
                        lines.append(f"    {edge[0]} --> {edge[1]}")
                        edges_added.add(edge)
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_mermaid_flow(self, entry_points: List[str]) -> str:
        """Generate flow diagram from entry points"""
        lines = ["```mermaid", "flowchart TD"]
        
        # Build flow from entry points
        visited = set()
        queue = list(entry_points)
        node_ids = {}
        node_count = 0
        
        while queue and len(node_ids) < 30:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            node_id = f"N{node_count}"
            node_ids[current] = node_id
            node_count += 1
            
            # Determine node type
            icon = "🚀" if current in entry_points else "📦"
            lines.append(f'    {node_id}["{icon} {current}"]')
            
            # Add dependencies
            deps = self.dependencies.get(current, set())
            for dep in list(deps)[:5]:  # Limit deps
                if dep not in queue and dep not in visited:
                    queue.append(dep)
        
        # Add edges
        edges_added = set()
        for module, deps in self.dependencies.items():
            if module not in node_ids:
                continue
            
            for dep in deps:
                if dep in node_ids and dep != module:
                    edge = (node_ids[module], node_ids[dep])
                    if edge not in edges_added:
                        lines.append(f"    {edge[0]} --> {edge[1]}")
                        edges_added.add(edge)
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_dot(self, max_nodes: int = 30) -> str:
        """Generate Graphviz DOT format"""
        lines = [
            "digraph codebase {",
            '    rankdir=TB;',
            '    node [shape=box, style=rounded];',
            ''
        ]
        
        # Create nodes
        modules = list(self.modules.keys())[:max_nodes]
        node_ids = {}
        
        for i, module in enumerate(modules):
            node_id = f"m{i}"
            node_ids[module] = node_id
            
            # Get color based on language
            extensions = self.modules[module]
            color = self._get_module_color(extensions)
            
            lines.append(f'    {node_id} [label="{module}", fillcolor="{color}", style="filled,rounded"];')
        
        lines.append('')
        
        # Create edges
        for module, deps in self.dependencies.items():
            if module not in node_ids:
                continue
            
            for dep in deps:
                if dep in node_ids and dep != module:
                    lines.append(f"    {node_ids[module]} -> {node_ids[dep]};")
        
        lines.append('}')
        return "\n".join(lines)
    
    def generate_component_diagram(self) -> str:
        """Generate component-level diagram"""
        lines = ["```mermaid", "graph TB"]
        
        # Group modules by category
        categories = defaultdict(list)
        for module in self.modules:
            cat = self._categorize_module(module)
            categories[cat].append(module)
        
        # Create subgraphs for categories
        subgraph_colors = {
            'core': 'fill:#f9f,stroke:#333',
            'api': 'fill:#bbf,stroke:#333',
            'ui': 'fill:#bfb,stroke:#333',
            'data': 'fill:#fbb,stroke:#333',
            'utils': 'fill:#ffb,stroke:#333',
            'other': 'fill:#ddd,stroke:#333'
        }
        
        node_ids = {}
        node_count = 0
        
        for cat, modules in categories.items():
            lines.append(f"    subgraph {cat.upper()}")
            
            for module in modules[:10]:  # Limit per category
                node_id = f"N{node_count}"
                node_ids[module] = node_id
                node_count += 1
                
                style = subgraph_colors.get(cat, subgraph_colors['other'])
                lines.append(f'        {node_id}["{module}"]:::{cat}')
            
            lines.append("    end")
            lines.append("")
        
        # Add class definitions for styling
        for cat in categories:
            style = subgraph_colors.get(cat, subgraph_colors['other'])
            lines.append(f"    classDef {cat} {style};")
        
        lines.append('')
        
        # Add inter-module dependencies
        for module, deps in self.dependencies.items():
            if module not in node_ids:
                continue
            
            for dep in deps:
                if dep in node_ids and dep != module:
                    lines.append(f"    {node_ids[module]} --> {node_ids[dep]}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def _get_module_icon(self, extensions: Set[str]) -> str:
        """Get icon for module based on file types"""
        if '.py' in extensions:
            return '🐍'
        elif any(e in extensions for e in ['.js', '.ts', '.jsx', '.tsx']):
            return '📜'
        elif '.go' in extensions:
            return '🐹'
        elif '.rs' in extensions:
            return '🦀'
        elif '.java' in extensions:
            return '☕'
        else:
            return '📁'
    
    def _get_module_color(self, extensions: Set[str]) -> str:
        """Get color for module based on file types"""
        if '.py' in extensions:
            return '#3776ab'  # Python blue
        elif any(e in extensions for e in ['.js', '.ts']):
            return '#f7df1e'  # JavaScript yellow
        elif '.go' in extensions:
            return '#00add8'  # Go cyan
        elif '.rs' in extensions:
            return '#dea584'  # Rust brown
        elif '.java' in extensions:
            return '#b07219'  # Java brown
        else:
            return '#cccccc'  # Gray
    
    def _categorize_module(self, module: str) -> str:
        """Categorize module by name"""
        name_lower = module.lower()
        
        if any(word in name_lower for word in ['core', 'main', 'app', 'engine']):
            return 'core'
        elif any(word in name_lower for word in ['api', 'route', 'endpoint', 'server', 'controller']):
            return 'api'
        elif any(word in name_lower for word in ['ui', 'view', 'component', 'page', 'frontend']):
            return 'ui'
        elif any(word in name_lower for word in ['data', 'model', 'db', 'store', 'repository']):
            return 'data'
        elif any(word in name_lower for word in ['util', 'helper', 'tool', 'common', 'shared']):
            return 'utils'
        else:
            return 'other'


def main():
    parser = argparse.ArgumentParser(description='Diagram Generator')
    parser.add_argument('--root', '-r', default='.', help='Project root directory')
    parser.add_argument('--format', '-f', 
                        choices=['mermaid', 'mermaid-flow', 'mermaid-component', 'dot'],
                        default='mermaid', help='Output format')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--max-nodes', '-n', type=int, default=30,
                        help='Maximum nodes to include')
    parser.add_argument('--entry-points', '-e', nargs='+',
                        help='Entry point modules for flow diagram')
    
    args = parser.parse_args()
    
    generator = DiagramGenerator(args.root)
    
    if args.format == 'mermaid':
        diagram = generator.generate_mermaid(args.max_nodes)
    elif args.format == 'mermaid-flow':
        entry_points = args.entry_points or ['src', 'app', 'main', 'index']
        diagram = generator.generate_mermaid_flow(entry_points)
    elif args.format == 'mermaid-component':
        diagram = generator.generate_component_diagram()
    elif args.format == 'dot':
        diagram = generator.generate_dot(args.max_nodes)
    else:
        diagram = generator.generate_mermaid(args.max_nodes)
    
    if args.output:
        Path(args.output).write_text(diagram, encoding='utf-8')
        print(f"Diagram saved to: {args.output}")
    else:
        print(diagram)


if __name__ == '__main__':
    main()
