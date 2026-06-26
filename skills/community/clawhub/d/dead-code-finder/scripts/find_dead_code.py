#!/usr/bin/env python3
"""Dead code finder for JavaScript/TypeScript projects.

Detects:
- Unused exports (functions, classes, constants, types)
- Unreferenced files (never imported)
- Unused npm dependencies
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# File extensions to scan
JS_EXTS = {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.mts', '.cts'}

# Default ignore patterns
DEFAULT_IGNORES = {
    'node_modules', 'dist', 'build', '.next', '.nuxt', 'coverage',
    '__tests__', '__mocks__', '.git', '.cache', 'public', 'static',
}

# File patterns to skip
SKIP_PATTERNS = [
    r'\.test\.[jt]sx?$', r'\.spec\.[jt]sx?$', r'\.stories\.[jt]sx?$',
    r'\.config\.[jt]s$', r'\.d\.ts$', r'setupTests\.',
    r'jest\.', r'vite\.config', r'webpack\.config', r'next\.config',
    r'tailwind\.config', r'postcss\.config', r'babel\.config',
    r'eslint', r'prettier', r'tsconfig',
]

# Default entry point patterns
ENTRY_PATTERNS = [
    r'src/index\.[jt]sx?$', r'src/main\.[jt]sx?$', r'src/app\.[jt]sx?$',
    r'pages/', r'app/', r'src/pages/', r'src/app/',
    r'server\.[jt]sx?$', r'index\.[jt]sx?$',
]

# Regex patterns for exports
EXPORT_PATTERNS = [
    # export function name
    (r'export\s+(?:async\s+)?function\s+(\w+)', 'function'),
    # export class name
    (r'export\s+class\s+(\w+)', 'class'),
    # export const/let/var name
    (r'export\s+(?:const|let|var)\s+(\w+)', 'variable'),
    # export type name
    (r'export\s+type\s+(\w+)', 'type'),
    # export interface name
    (r'export\s+interface\s+(\w+)', 'interface'),
    # export enum name
    (r'export\s+enum\s+(\w+)', 'enum'),
    # export { name1, name2 }
    (r'export\s*\{([^}]+)\}(?:\s*from)?', 'named'),
    # export default (class|function) name
    (r'export\s+default\s+(?:class|function)\s+(\w+)', 'default'),
]

# Regex for imports
IMPORT_PATTERNS = [
    # import { x, y } from './module'
    r"import\s*\{([^}]+)\}\s*from\s*['\"]([^'\"]+)['\"]",
    # import x from './module'
    r"import\s+(\w+)\s+from\s*['\"]([^'\"]+)['\"]",
    # import * as x from './module'
    r"import\s+\*\s+as\s+(\w+)\s+from\s*['\"]([^'\"]+)['\"]",
    # import './module' (side-effect)
    r"import\s*['\"]([^'\"]+)['\"]",
    # require('./module')
    r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
    # dynamic import('./module')
    r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
]


def should_ignore(path, root, extra_ignores=None):
    """Check if a path should be ignored."""
    rel = os.path.relpath(path, root)
    parts = Path(rel).parts
    ignores = DEFAULT_IGNORES | set(extra_ignores or [])
    return any(p in ignores for p in parts)


def is_skippable(filepath):
    """Check if file matches skip patterns."""
    name = os.path.basename(filepath)
    return any(re.search(p, name) for p in SKIP_PATTERNS)


def is_entry_point(filepath, root, extra_entries=None):
    """Check if file is an entry point."""
    rel = os.path.relpath(filepath, root)
    patterns = ENTRY_PATTERNS + (extra_entries or [])
    return any(re.search(p, rel) for p in patterns)


def find_source_files(root, extra_ignores=None):
    """Find all JS/TS source files in the project."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune ignored directories
        dirnames[:] = [d for d in dirnames if not should_ignore(
            os.path.join(dirpath, d), root, extra_ignores)]
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            if Path(f).suffix in JS_EXTS:
                files.append(filepath)
    return files


def read_file(filepath):
    """Read file content, handling encoding issues."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except (OSError, IOError):
        return ''


def strip_comments(content):
    """Remove single-line and multi-line comments."""
    # Remove multi-line comments
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    # Remove single-line comments (but not URLs)
    content = re.sub(r'(?<!:)//.*$', '', content, flags=re.MULTILINE)
    return content


def extract_exports(content, filepath):
    """Extract all exports from file content."""
    exports = []
    clean = strip_comments(content)

    for pattern, kind in EXPORT_PATTERNS:
        for match in re.finditer(pattern, clean):
            if kind == 'named':
                # Parse { name1, name2 as alias, type name3 }
                names_str = match.group(1)
                for name in names_str.split(','):
                    name = name.strip()
                    # Handle 'as' aliases
                    if ' as ' in name:
                        name = name.split(' as ')[0].strip()
                    # Handle 'type' prefix
                    name = re.sub(r'^type\s+', '', name)
                    if name and name.isidentifier():
                        exports.append((name, 'named'))
            else:
                name = match.group(1)
                if name and name.isidentifier():
                    exports.append((name, kind))

    # Check for default export without name
    if re.search(r'export\s+default\s+(?!class|function|abstract)', clean):
        exports.append(('default', 'default'))

    return exports


def extract_imports(content):
    """Extract all imports from file content."""
    imports = {'names': set(), 'paths': set()}
    clean = strip_comments(content)

    for pattern in IMPORT_PATTERNS:
        for match in re.finditer(pattern, clean):
            groups = match.groups()
            if len(groups) == 2:
                names_str, path = groups
                imports['paths'].add(path)
                # Parse imported names
                for name in names_str.split(','):
                    name = name.strip()
                    if ' as ' in name:
                        name = name.split(' as ')[0].strip()
                    name = re.sub(r'^type\s+', '', name)
                    if name and name.isidentifier():
                        imports['names'].add(name)
            elif len(groups) == 1:
                imports['paths'].add(groups[0])

    return imports


def resolve_import_path(import_path, from_file, root, all_files):
    """Resolve an import path to an actual file."""
    if import_path.startswith('.'):
        # Relative import
        base_dir = os.path.dirname(from_file)
        resolved = os.path.normpath(os.path.join(base_dir, import_path))
    elif import_path.startswith('@/') or import_path.startswith('~/'):
        # Common alias for src/
        resolved = os.path.join(root, 'src', import_path[2:])
    else:
        # Node module or alias — not a local file
        return None

    # Try extensions and index files
    candidates = [resolved]
    for ext in JS_EXTS:
        candidates.append(resolved + ext)
    for ext in JS_EXTS:
        candidates.append(os.path.join(resolved, 'index' + ext))

    for c in candidates:
        if c in all_files:
            return c
    return None


def load_tsconfig_paths(root):
    """Load path aliases from tsconfig.json."""
    aliases = {}
    tsconfig = os.path.join(root, 'tsconfig.json')
    if not os.path.exists(tsconfig):
        return aliases
    try:
        content = read_file(tsconfig)
        # Strip comments from tsconfig (JSON with comments)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        data = json.loads(content)
        paths = data.get('compilerOptions', {}).get('paths', {})
        base_url = data.get('compilerOptions', {}).get('baseUrl', '.')
        base = os.path.join(root, base_url)
        for alias, targets in paths.items():
            # Convert tsconfig path pattern to prefix
            prefix = alias.replace('/*', '')
            if targets:
                target = targets[0].replace('/*', '')
                aliases[prefix] = os.path.join(base, target)
    except (json.JSONDecodeError, KeyError):
        pass
    return aliases


def find_unused_exports(files, root):
    """Find exported symbols that are never imported."""
    # Collect all exports per file
    file_exports = {}
    for f in files:
        content = read_file(f)
        exports = extract_exports(content, f)
        if exports:
            file_exports[f] = exports

    # Collect all imported names across entire project
    all_imported_names = set()
    for f in files:
        content = read_file(f)
        imports = extract_imports(content)
        all_imported_names.update(imports['names'])

    # Find unused
    unused = {}
    for filepath, exports in file_exports.items():
        if is_skippable(filepath) or is_entry_point(filepath, root):
            continue
        unused_in_file = []
        for name, kind in exports:
            if name == 'default':
                continue  # Default exports are harder to track
            if name not in all_imported_names:
                unused_in_file.append((name, kind))
        if unused_in_file:
            unused[os.path.relpath(filepath, root)] = unused_in_file

    return unused


def find_unreferenced_files(files, root, extra_entries=None):
    """Find files that are never imported by any other file."""
    file_set = set(files)

    # Collect all import target files
    referenced = set()
    for f in files:
        content = read_file(f)
        imports = extract_imports(content)
        for path in imports['paths']:
            resolved = resolve_import_path(path, f, root, file_set)
            if resolved:
                referenced.add(resolved)

    # Find unreferenced (excluding entry points and skippable)
    unreferenced = []
    for f in files:
        if f in referenced:
            continue
        if is_entry_point(f, root, extra_entries):
            continue
        if is_skippable(f):
            continue
        unreferenced.append(os.path.relpath(f, root))

    return sorted(unreferenced)


def find_unused_dependencies(files, root):
    """Find npm packages that are never imported."""
    pkg_path = os.path.join(root, 'package.json')
    if not os.path.exists(pkg_path):
        return []

    try:
        with open(pkg_path) as f:
            pkg = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

    deps = set(pkg.get('dependencies', {}).keys())
    dev_deps = set(pkg.get('devDependencies', {}).keys())
    all_deps = deps | dev_deps

    # Collect all imported package names
    imported_packages = set()
    for f in files:
        content = read_file(f)
        imports = extract_imports(content)
        for path in imports['paths']:
            if not path.startswith('.') and not path.startswith('/'):
                # Extract package name (handle scoped packages)
                if path.startswith('@'):
                    parts = path.split('/')
                    pkg_name = '/'.join(parts[:2]) if len(parts) > 1 else parts[0]
                else:
                    pkg_name = path.split('/')[0]
                imported_packages.add(pkg_name)

    # Also check scripts in package.json for CLI tools
    scripts = pkg.get('scripts', {})
    scripts_text = ' '.join(scripts.values())

    # Well-known dev tools that may only appear in scripts
    cli_tools = set()
    for dep in all_deps:
        bare_name = dep.split('/')[-1]
        if bare_name in scripts_text or dep in scripts_text:
            cli_tools.add(dep)

    # Find unused
    unused = []
    for dep in sorted(all_deps):
        if dep not in imported_packages and dep not in cli_tools:
            is_dev = dep in dev_deps and dep not in deps
            unused.append((dep, 'dev' if is_dev else 'prod'))

    return unused


def format_report(unused_exports, unreferenced_files, unused_deps, root):
    """Format findings as a human-readable report."""
    lines = ['=== Dead Code Report ===', f'Project: {root}', '']

    # Unused exports
    total_exports = sum(len(v) for v in unused_exports.values())
    lines.append(f'UNUSED EXPORTS ({total_exports} found):')
    if unused_exports:
        for filepath, exports in sorted(unused_exports.items()):
            names = ', '.join(f'{n} ({k})' for n, k in exports)
            lines.append(f'  {filepath}: {names}')
    else:
        lines.append('  None found.')
    lines.append('')

    # Unreferenced files
    lines.append(f'UNREFERENCED FILES ({len(unreferenced_files)} found):')
    if unreferenced_files:
        for f in unreferenced_files:
            lines.append(f'  {f}')
    else:
        lines.append('  None found.')
    lines.append('')

    # Unused dependencies
    lines.append(f'UNUSED DEPENDENCIES ({len(unused_deps)} found):')
    if unused_deps:
        for dep, scope in unused_deps:
            lines.append(f'  {dep} [{scope}]')
    else:
        lines.append('  None found.')
    lines.append('')

    # Summary
    total = total_exports + len(unreferenced_files) + len(unused_deps)
    lines.append(f'TOTAL: {total} issues found')

    return '\n'.join(lines)


def format_json(unused_exports, unreferenced_files, unused_deps, root):
    """Format findings as JSON."""
    return json.dumps({
        'project': root,
        'unusedExports': {
            k: [{'name': n, 'kind': t} for n, t in v]
            for k, v in unused_exports.items()
        },
        'unreferencedFiles': unreferenced_files,
        'unusedDependencies': [
            {'name': n, 'scope': s} for n, s in unused_deps
        ],
        'summary': {
            'unusedExports': sum(len(v) for v in unused_exports.values()),
            'unreferencedFiles': len(unreferenced_files),
            'unusedDependencies': len(unused_deps),
        }
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Find dead code in JS/TS projects')
    parser.add_argument('project', help='Project root directory')
    parser.add_argument('--mode', choices=['all', 'exports', 'files', 'deps'],
                        default='all', help='What to scan for')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--entry', help='Comma-separated entry point patterns')
    parser.add_argument('--ignore', help='Comma-separated additional ignore dirs')
    args = parser.parse_args()

    root = os.path.abspath(args.project)
    if not os.path.isdir(root):
        print(f'Error: {root} is not a directory', file=sys.stderr)
        sys.exit(1)

    extra_ignores = args.ignore.split(',') if args.ignore else None
    extra_entries = args.entry.split(',') if args.entry else None

    files = find_source_files(root, extra_ignores)
    if not files:
        print('No JS/TS source files found.', file=sys.stderr)
        sys.exit(1)

    print(f'Scanning {len(files)} files...', file=sys.stderr)

    unused_exports = {}
    unreferenced_files = []
    unused_deps = []

    if args.mode in ('all', 'exports'):
        unused_exports = find_unused_exports(files, root)
    if args.mode in ('all', 'files'):
        unreferenced_files = find_unreferenced_files(files, root, extra_entries)
    if args.mode in ('all', 'deps'):
        unused_deps = find_unused_dependencies(files, root)

    if args.json:
        print(format_json(unused_exports, unreferenced_files, unused_deps, root))
    else:
        print(format_report(unused_exports, unreferenced_files, unused_deps, root))


if __name__ == '__main__':
    main()
