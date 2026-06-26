#!/usr/bin/env python3
"""
Dependency Analysis Script

Analyzes file and module dependencies, supports reverse dependency lookup.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


class DependencyAnalyzer:
    """Analyzes dependencies between files and modules"""
    
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.file_deps: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_deps: Dict[str, Set[str]] = defaultdict(set)
        self.module_deps: Dict[str, Set[str]] = defaultdict(set)
    
    def extract_imports_python(self, content: str) -> List[str]:
        """Extract imports from Python file"""
        imports = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('import '):
                # import X, Y, Z
                parts = line[7:].split(',')
                for part in parts:
                    mod = part.strip().split()[0].split('.')[0]
                    if mod:
                        imports.append(mod)
            elif line.startswith('from '):
                # from X import Y
                parts = line[5:].split(' import')
                if parts:
                    mod = parts[0].strip().split('.')[0]
                    if mod:
                        imports.append(mod)
        return imports
    
    def extract_imports_js_ts(self, content: str) -> List[str]:
        """Extract imports from JavaScript/TypeScript file"""
        imports = []
        for line in content.split('\n'):
            line = line.strip()
            # import X from 'package'
            if 'from ' in line and ('import ' in line or 'export ' in line):
                parts = line.split('from ')
                if len(parts) > 1:
                    pkg = parts[1].strip().strip('"\';`')
                    if pkg and not pkg.startswith('.'):
                        imports.append(pkg.split('/')[0])
            # require('package')
            elif 'require(' in line:
                start = line.find('require(') + 8
                end = line.find(')', start)
                if end > start:
                    pkg = line[start:end].strip('"\'`')
                    if pkg and not pkg.startswith('.'):
                        imports.append(pkg.split('/')[0])
        return imports
    
    def extract_imports_go(self, content: str) -> List[str]:
        """Extract imports from Go file"""
        imports = []
        in_import = False
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('import ('):
                in_import = True
            elif in_import and line.startswith(')'):
                in_import = False
            elif in_import or line.startswith('import '):
                # Extract quoted strings
                if '"' in line:
                    parts = line.split('"')
                    for i in range(1, len(parts), 2):
                        pkg = parts[i]
                        if pkg and not pkg.startswith('.'):
                            imports.append(pkg.split('/')[0])
        return imports
    
    def analyze_file(self, filepath: Path) -> Optional[List[str]]:
        """Analyze a single file's dependencies"""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            ext = filepath.suffix.lower()
            
            if ext == '.py':
                return self.extract_imports_python(content)
            elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                return self.extract_imports_js_ts(content)
            elif ext == '.go':
                return self.extract_imports_go(content)
            else:
                return []
        except Exception as e:
            print(f"Warning: Could not analyze {filepath}: {e}", file=sys.stderr)
            return []
    
    def analyze(self, target_path: Optional[str] = None) -> 'DependencyAnalyzer':
        """Analyze dependencies"""
        if target_path:
            target = Path(target_path).resolve()
            if target.is_file():
                self._analyze_single_file(target)
            else:
                self._analyze_directory(target)
        else:
            self._analyze_directory(self.root)
        
        return self
    
    def _analyze_single_file(self, filepath: Path):
        """Analyze a single file"""
        imports = self.analyze_file(filepath)
        rel_path = str(filepath.relative_to(self.root))
        
        for imp in imports:
            self.file_deps[rel_path].add(imp)
            self.reverse_deps[imp].add(rel_path)
    
    def _analyze_directory(self, dirpath: Path):
        """Analyze all files in directory"""
        ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
        
        for filepath in dirpath.rglob('*'):
            if not filepath.is_file():
                continue
            
            # Skip ignored directories
            if any(part in ignore_dirs for part in filepath.parts):
                continue
            
            imports = self.analyze_file(filepath)
            if imports:
                try:
                    rel_path = str(filepath.relative_to(self.root))
                except ValueError:
                    rel_path = str(filepath)
                
                for imp in imports:
                    self.file_deps[rel_path].add(imp)
                    self.reverse_deps[imp].add(rel_path)
    
    def get_dependencies(self, filepath: str, depth: int = 2) -> Dict[str, List[str]]:
        """Get dependencies of a file (what it imports)"""
        result = {}
        current_level = {filepath}
        
        for d in range(depth):
            next_level = set()
            for f in current_level:
                deps = self.file_deps.get(f, set())
                result[f"level_{d+1}"] = sorted(deps)
                next_level.update(deps)
            current_level = next_level
        
        return result
    
    def get_reverse_dependencies(self, target: str, depth: int = 2) -> Dict[str, List[str]]:
        """Get reverse dependencies (what imports this)"""
        result = {}
        current_level = {target}
        
        for d in range(depth):
            next_level = set()
            for item in current_level:
                # Find all files that import this item
                dependents = set()
                for file, deps in self.file_deps.items():
                    if item in deps or item in file:
                        dependents.add(file)
                
                # Also check reverse_deps
                if item in self.reverse_deps:
                    dependents.update(self.reverse_deps[item])
                
                result[f"level_{d+1}"] = sorted(dependents)
                next_level.update(dependents)
            current_level = next_level
        
        return result
    
    def generate_report(self, target: str, reverse: bool = False, format: str = 'md') -> str:
        """Generate dependency report"""
        if format == 'json':
            return self._generate_json_report(target, reverse)
        else:
            return self._generate_markdown_report(target, reverse)
    
    def _generate_markdown_report(self, target: str, reverse: bool) -> str:
        """Generate Markdown report"""
        lines = [
            "# Dependency Analysis Report",
            "",
            f"**Target**: `{target}`",
            f"**Root**: `{self.root}`",
            f"**Type**: {'Reverse Dependencies' if reverse else 'Dependencies'}",
            "",
        ]
        
        if reverse:
            deps = self.get_reverse_dependencies(target, depth=3)
            lines.append("## What depends on this?")
            lines.append("")
            
            for level, items in deps.items():
                level_num = level.split('_')[1]
                lines.append(f"### Level {level_num} (Direct dependents)")
                lines.append("")
                if items:
                    for item in items[:50]:  # Limit
                        lines.append(f"- `{item}`")
                else:
                    lines.append("_No dependencies found_")
                lines.append("")
        else:
            deps = self.get_dependencies(target, depth=3)
            lines.append("## What does this import?")
            lines.append("")
            
            for level, items in deps.items():
                level_num = level.split('_')[1]
                lines.append(f"### Level {level_num} (Direct imports)")
                lines.append("")
                if items:
                    for item in items[:50]:
                        lines.append(f"- `{item}`")
                else:
                    lines.append("_No imports found_")
                lines.append("")
        
        # Summary statistics
        lines.extend([
            "## Summary",
            "",
            f"- Total files analyzed: {len(self.file_deps)}",
            f"- Unique dependencies: {len(self.reverse_deps)}",
            "",
        ])
        
        return "\n".join(lines)
    
    def _generate_json_report(self, target: str, reverse: bool) -> str:
        """Generate JSON report"""
        if reverse:
            data = {
                'target': target,
                'type': 'reverse_dependencies',
                'dependencies': self.get_reverse_dependencies(target, depth=3)
            }
        else:
            data = {
                'target': target,
                'type': 'dependencies',
                'dependencies': self.get_dependencies(target, depth=3)
            }
        return json.dumps(data, indent=2)
    
    def generate_mermaid_graph(self, target: str, max_nodes: int = 20) -> str:
        """Generate Mermaid diagram for dependencies"""
        lines = ["```mermaid", "graph TD"]
        
        # Find files related to target
        related = set()
        related.add(target)
        
        # Add files that import target
        for file, deps in self.file_deps.items():
            if target in deps or target in file:
                related.add(file)
                for dep in list(deps)[:5]:  # Limit deps per file
                    related.add(dep)
        
        # Limit nodes
        related = list(related)[:max_nodes]
        
        # Create safe node IDs
        node_ids = {}
        for i, node in enumerate(related):
            node_id = f"N{i}"
            node_ids[node] = node_id
            display = node.split('/')[-1] if '/' in node else node
            lines.append(f'    {node_id}["{display}"]')
        
        # Create edges
        for file in related:
            if file in self.file_deps:
                for dep in self.file_deps[file]:
                    if dep in node_ids and file in node_ids:
                        lines.append(f"    {node_ids[file]} --> {node_ids[dep]}")
        
        lines.append("```")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Dependency Analyzer')
    parser.add_argument('target', help='File or module to analyze')
    parser.add_argument('--root', '-r', default='.', help='Project root directory')
    parser.add_argument('--reverse', '-R', action='store_true',
                        help='Show reverse dependencies')
    parser.add_argument('--depth', '-d', type=int, default=2,
                        help='Dependency depth')
    parser.add_argument('--format', '-f', choices=['md', 'json', 'mermaid'],
                        default='md', help='Output format')
    parser.add_argument('--output', '-o', help='Output file')
    
    args = parser.parse_args()
    
    analyzer = DependencyAnalyzer(args.root)
    analyzer.analyze()
    
    if args.format == 'mermaid':
        report = analyzer.generate_mermaid_graph(args.target)
    else:
        report = analyzer.generate_report(args.target, args.reverse, args.format)
    
    if args.output:
        Path(args.output).write_text(report, encoding='utf-8')
        print(f"Report saved to: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
