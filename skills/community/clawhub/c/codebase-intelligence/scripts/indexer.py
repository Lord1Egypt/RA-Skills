#!/usr/bin/env python3
"""
Codebase Indexer with Caching

Builds and maintains a persistent index of the codebase for fast queries.
"""

import hashlib
import json
import pickle
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import fnmatch


@dataclass
class FileIndex:
    """Indexed information about a file"""
    path: str
    mtime: float
    size: int
    hash: str
    language: Optional[str] = None
    lines: int = 0
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    content_preview: str = ""  # First 500 chars for search


@dataclass
class CodebaseIndex:
    """Complete codebase index"""
    root: str
    created_at: float
    updated_at: float
    files: Dict[str, FileIndex] = field(default_factory=dict)
    modules: Dict[str, List[str]] = field(default_factory=dict)
    symbols: Dict[str, List[str]] = field(default_factory=dict)  # function/class -> files
    dependencies: Dict[str, Set[str]] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'root': self.root,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'files': {k: asdict(v) for k, v in self.files.items()},
            'modules': self.modules,
            'symbols': self.symbols,
            'dependencies': {k: list(v) for k, v in self.dependencies.items()},
            'stats': {
                'total_files': len(self.files),
                'total_modules': len(self.modules),
                'total_symbols': len(self.symbols)
            }
        }


class Indexer:
    """Builds and maintains codebase index"""
    
    DEFAULT_IGNORE = [
        '.git', '.svn', '.hg',
        'node_modules', 'vendor', '__pycache__',
        '.venv', 'venv', 'env', '.env',
        'dist', 'build', 'target', 'out',
        '*.min.js', '*.min.css', '*.map',
        '.DS_Store', 'Thumbs.db',
        '*.pyc', '*.pyo', '*.class',
        '*.so', '*.dll', '*.dylib', '*.exe',
        '.idea', '.vscode', '.vs',
        'coverage', '.coverage', 'htmlcov',
        '.pytest_cache', '.mypy_cache',
    ]
    
    LANGUAGE_MAP = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript (React)',
        '.tsx': 'TypeScript (React)',
        '.mjs': 'JavaScript (ESM)',
        '.go': 'Go',
        '.rs': 'Rust',
        '.java': 'Java',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.c': 'C',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.h': 'C/C++ Header',
        '.hpp': 'C++ Header',
        '.cs': 'C#',
        '.swift': 'Swift',
        '.m': 'Objective-C',
        '.mm': 'Objective-C++',
        '.r': 'R',
        '.R': 'R',
        '.sh': 'Shell',
        '.bash': 'Bash',
        '.zsh': 'Zsh',
        '.ps1': 'PowerShell',
        '.sql': 'SQL',
        '.html': 'HTML',
        '.htm': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.less': 'Less',
        '.vue': 'Vue',
        '.svelte': 'Svelte',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.toml': 'TOML',
        '.xml': 'XML',
        '.md': 'Markdown',
        '.rst': 'reStructuredText',
        '.dockerfile': 'Dockerfile',
        'Dockerfile': 'Dockerfile',
        '.dockerignore': 'Dockerignore',
        'Makefile': 'Makefile',
        '.mk': 'Makefile',
    }
    
    def __init__(self, root_path: str, cache_dir: Optional[str] = None):
        self.root = Path(root_path).resolve()
        self.cache_dir = Path(cache_dir) if cache_dir else self._get_default_cache_dir()
        self.cache_file = self.cache_dir / 'codebase_index.pkl'
        self.ignore_patterns = self.DEFAULT_IGNORE
        
        # Load or create index
        self.index: Optional[CodebaseIndex] = None
    
    def _get_default_cache_dir(self) -> Path:
        """Get default cache directory"""
        # Store cache in project's .codebase-intelligence directory
        cache_dir = self.root / '.codebase-intelligence'
        cache_dir.mkdir(exist_ok=True)
        return cache_dir
    
    def _get_file_hash(self, filepath: Path) -> str:
        """Get file hash for change detection"""
        try:
            content = filepath.read_bytes()
            return hashlib.md5(content).hexdigest()[:16]
        except:
            return ""
    
    def _detect_language(self, filepath: Path) -> Optional[str]:
        """Detect programming language"""
        ext = filepath.suffix.lower()
        if ext in self.LANGUAGE_MAP:
            return self.LANGUAGE_MAP[ext]
        
        # Check for special filenames
        name = filepath.name
        if name in self.LANGUAGE_MAP:
            return self.LANGUAGE_MAP[name]
        
        return None
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        try:
            rel_path = path.relative_to(self.root)
        except ValueError:
            return True
        
        for pattern in self.ignore_patterns:
            for part in rel_path.parts:
                if fnmatch.fnmatch(part, pattern):
                    return True
            if fnmatch.fnmatch(str(rel_path), pattern):
                return True
        
        return False
    
    def _parse_file(self, filepath: Path) -> Optional[FileIndex]:
        """Parse a single file and extract information"""
        try:
            stat = filepath.stat()
            language = self._detect_language(filepath)
            
            if not language:
                return None
            
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            lines = content.count('\n') + 1
            file_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
            
            # Extract symbols based on language
            functions, classes, imports = self._extract_symbols(content, language)
            
            return FileIndex(
                path=str(filepath.relative_to(self.root)),
                mtime=stat.st_mtime,
                size=stat.st_size,
                hash=file_hash,
                language=language,
                lines=lines,
                imports=imports,
                functions=functions,
                classes=classes,
                content_preview=content[:500]
            )
        except Exception as e:
            return None
    
    def _extract_symbols(self, content: str, language: str) -> Tuple[List[str], List[str], List[str]]:
        """Extract functions, classes, and imports from content"""
        functions = []
        classes = []
        imports = []
        
        if language == 'Python':
            functions, classes, imports = self._parse_python(content)
        elif language in ['JavaScript', 'TypeScript', 'JavaScript (React)', 'TypeScript (React)', 'JavaScript (ESM)']:
            functions, classes, imports = self._parse_js_ts(content)
        elif language == 'Go':
            functions, classes, imports = self._parse_go(content)
        elif language == 'Java':
            functions, classes, imports = self._parse_java(content)
        elif language == 'Rust':
            functions, classes, imports = self._parse_rust(content)
        
        return functions, classes, imports
    
    def _parse_python(self, content: str) -> Tuple[List[str], List[str], List[str]]:
        """Parse Python file"""
        import re
        
        functions = []
        classes = []
        imports = []
        
        # Find functions
        for match in re.finditer(r'^def\s+(\w+)\s*\(', content, re.MULTILINE):
            functions.append(match.group(1))
        
        # Find classes
        for match in re.finditer(r'^class\s+(\w+)', content, re.MULTILINE):
            classes.append(match.group(1))
        
        # Find imports
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                if line.startswith('import '):
                    mods = line[7:].split(',')
                    for mod in mods:
                        imports.append(mod.strip().split()[0].split('.')[0])
                else:
                    parts = line[5:].split(' import')
                    if parts:
                        imports.append(parts[0].strip().split('.')[0])
        
        return list(set(functions)), list(set(classes)), list(set(imports))
    
    def _parse_js_ts(self, content: str) -> Tuple[List[str], List[str], List[str]]:
        """Parse JavaScript/TypeScript file"""
        import re
        
        functions = []
        classes = []
        imports = []
        
        # Function declarations
        for match in re.finditer(r'function\s+(\w+)\s*\(', content):
            functions.append(match.group(1))
        
        # Arrow functions with names
        for match in re.finditer(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(', content):
            functions.append(match.group(1))
        
        # Method definitions
        for match in re.finditer(r'(\w+)\s*\([^)]*\)\s*\{', content):
            name = match.group(1)
            if name not in ['if', 'while', 'for', 'switch', 'catch']:
                functions.append(name)
        
        # Classes
        for match in re.finditer(r'class\s+(\w+)', content):
            classes.append(match.group(1))
        
        # Imports
        for match in re.finditer(r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]', content):
            pkg = match.group(1)
            if not pkg.startswith('.'):
                imports.append(pkg.split('/')[0])
        
        # Require
        for match in re.finditer(r'require\([\'"](.+?)[\'"]\)', content):
            pkg = match.group(1)
            if not pkg.startswith('.'):
                imports.append(pkg.split('/')[0])
        
        return list(set(functions)), list(set(classes)), list(set(imports))
    
    def _parse_go(self, content: str) -> Tuple[List[str], List[str], List[str]]:
        """Parse Go file"""
        import re
        
        functions = []
        classes = []  # structs and interfaces
        imports = []
        
        # Functions
        for match in re.finditer(r'^func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(', content, re.MULTILINE):
            functions.append(match.group(1))
        
        # Structs and interfaces
        for match in re.finditer(r'^type\s+(\w+)\s+(?:struct|interface)', content, re.MULTILINE):
            classes.append(match.group(1))
        
        # Imports
        in_import = False
        for line in content.split('\n'):
            line = line.strip()
            if 'import (' in line:
                in_import = True
            elif in_import and line.startswith(')'):
                in_import = False
            elif in_import or line.startswith('import '):
                for match in re.finditer(r'"([^"]+)"', line):
                    imports.append(match.group(1).split('/')[-1])
        
        return list(set(functions)), list(set(classes)), list(set(imports))
    
    def _parse_java(self, content: str) -> Tuple[List[str], List[str], List[str]]:
        """Parse Java file"""
        import re
        
        functions = []
        classes = []
        imports = []
        
        # Classes and interfaces
        for match in re.finditer(r'(?:public\s+|private\s+|protected\s+)?(?:class|interface|enum)\s+(\w+)', content):
            classes.append(match.group(1))
        
        # Methods
        for match in re.finditer(r'(?:public|private|protected)\s+\w+\s+(\w+)\s*\([^)]*\)\s*\{', content):
            functions.append(match.group(1))
        
        # Imports
        for match in re.finditer(r'^import\s+([\w.]+);', content, re.MULTILINE):
            imports.append(match.group(1).split('.')[-1])
        
        return list(set(functions)), list(set(classes)), list(set(imports))
    
    def _parse_rust(self, content: str) -> Tuple[List[str], List[str], List[str]]:
        """Parse Rust file"""
        import re
        
        functions = []
        classes = []  # structs, enums, traits
        imports = []  # use statements
        
        # Functions
        for match in re.finditer(r'^fn\s+(\w+)\s*\(', content, re.MULTILINE):
            functions.append(match.group(1))
        
        # Structs, enums, traits
        for match in re.finditer(r'^(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)', content, re.MULTILINE):
            classes.append(match.group(1))
        
        # Use statements
        for match in re.finditer(r'^use\s+([\w:]+)', content, re.MULTILINE):
            imports.append(match.group(1).split(':')[-1])
        
        return list(set(functions)), list(set(classes)), list(set(imports))
    
    def build_index(self, max_files: int = 5000) -> CodebaseIndex:
        """Build or update the codebase index"""
        print(f"🔍 Indexing codebase at: {self.root}")
        
        # Try to load existing index
        old_index = self._load_cache()
        
        index = CodebaseIndex(
            root=str(self.root),
            created_at=old_index.created_at if old_index else time.time(),
            updated_at=time.time()
        )
        
        if old_index:
            print(f"  📦 Found existing index ({len(old_index.files)} files)")
            print(f"  🔄 Incremental update...")
        
        # Collect all files
        all_files = list(self.root.rglob('*'))
        source_files = []
        
        for filepath in all_files:
            if not filepath.is_file():
                continue
            if self._should_ignore(filepath):
                continue
            if self._detect_language(filepath):
                source_files.append(filepath)
        
        print(f"  📁 Found {len(source_files)} source files")
        
        # Process files
        updated = 0
        added = 0
        unchanged = 0
        
        for i, filepath in enumerate(source_files[:max_files]):
            if i % 100 == 0 and i > 0:
                print(f"  📊 Progress: {i}/{len(source_files[:max_files])}")
            
            rel_path = str(filepath.relative_to(self.root))
            
            # Check if file needs re-indexing
            if old_index and rel_path in old_index.files:
                old_file = old_index.files[rel_path]
                try:
                    stat = filepath.stat()
                    if stat.st_mtime == old_file.mtime and stat.st_size == old_file.size:
                        # File unchanged, reuse index
                        index.files[rel_path] = old_file
                        unchanged += 1
                        continue
                except:
                    pass
            
            # Re-index file
            file_index = self._parse_file(filepath)
            if file_index:
                index.files[rel_path] = file_index
                if old_index and rel_path in old_index.files:
                    updated += 1
                else:
                    added += 1
        
        # Build module and symbol indexes
        self._build_derived_indexes(index)
        
        # Save cache
        self._save_cache(index)
        
        print(f"\n✅ Index complete:")
        print(f"   • {added} new files")
        print(f"   • {updated} updated files")
        print(f"   • {unchanged} unchanged (cached)")
        print(f"   • {len(index.files)} total files indexed")
        print(f"   • {len(index.modules)} modules")
        print(f"   • {len(index.symbols)} symbols")
        
        self.index = index
        return index
    
    def _build_derived_indexes(self, index: CodebaseIndex):
        """Build module and symbol indexes"""
        # Module index
        for file_path, file_info in index.files.items():
            path_parts = Path(file_path).parts
            if len(path_parts) > 1:
                module = path_parts[0]
                if module not in index.modules:
                    index.modules[module] = []
                index.modules[module].append(file_path)
        
        # Symbol index
        for file_path, file_info in index.files.items():
            for func in file_info.functions:
                key = f"func:{func}"
                if key not in index.symbols:
                    index.symbols[key] = []
                index.symbols[key].append(file_path)
            
            for cls in file_info.classes:
                key = f"class:{cls}"
                if key not in index.symbols:
                    index.symbols[key] = []
                index.symbols[key].append(file_path)
        
        # Dependency index
        for file_path, file_info in index.files.items():
            for imp in file_info.imports:
                if imp not in index.dependencies:
                    index.dependencies[imp] = set()
                index.dependencies[imp].add(file_path)
    
    def _load_cache(self) -> Optional[CodebaseIndex]:
        """Load index from cache"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            print(f"  ⚠️  Could not load cache: {e}")
        return None
    
    def _save_cache(self, index: CodebaseIndex):
        """Save index to cache"""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'wb') as f:
                pickle.dump(index, f)
            
            # Also save JSON version for inspection
            json_file = self.cache_dir / 'codebase_index.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(index.to_dict(), f, indent=2, default=str)
            
            print(f"  💾 Cache saved to {self.cache_file}")
        except Exception as e:
            print(f"  ⚠️  Could not save cache: {e}")
    
    def get_index(self) -> Optional[CodebaseIndex]:
        """Get current index, building if necessary"""
        if self.index is None:
            if self.cache_file.exists():
                self.index = self._load_cache()
            if self.index is None:
                self.build_index()
        return self.index
    
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, float]]:
        """Search the index for matching files"""
        index = self.get_index()
        if not index:
            return []
        
        query_lower = query.lower()
        query_terms = query_lower.split()
        results = []
        
        for file_path, file_info in index.files.items():
            score = 0.0
            path_lower = file_path.lower()
            content_lower = file_info.content_preview.lower()
            
            # Path matching
            if query_lower in path_lower:
                score += 20
            for term in query_terms:
                if term in path_lower:
                    score += 5
            
            # Content matching
            if query_lower in content_lower:
                score += 10
            for term in query_terms:
                if term in content_lower:
                    score += 2
            
            # Symbol matching
            for func in file_info.functions:
                if query_lower in func.lower():
                    score += 15
            for cls in file_info.classes:
                if query_lower in cls.lower():
                    score += 15
            
            if score > 0:
                results.append((file_path, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
    
    def find_symbol(self, name: str, symbol_type: Optional[str] = None) -> List[str]:
        """Find files containing a symbol"""
        index = self.get_index()
        if not index:
            return []
        
        results = []
        
        if symbol_type:
            key = f"{symbol_type}:{name}"
            results = index.symbols.get(key, [])
        else:
            # Search both functions and classes
            for key, files in index.symbols.items():
                if name.lower() in key.lower():
                    results.extend(files)
        
        return list(set(results))
    
    def get_stats(self) -> dict:
        """Get index statistics"""
        index = self.get_index()
        if not index:
            return {}
        
        languages = {}
        for file_info in index.files.values():
            lang = file_info.language or 'Unknown'
            if lang not in languages:
                languages[lang] = {'files': 0, 'lines': 0}
            languages[lang]['files'] += 1
            languages[lang]['lines'] += file_info.lines
        
        total_lines = sum(f.lines for f in index.files.values())
        
        return {
            'root': index.root,
            'total_files': len(index.files),
            'total_lines': total_lines,
            'total_modules': len(index.modules),
            'total_functions': sum(len(f.functions) for f in index.files.values()),
            'total_classes': sum(len(f.classes) for f in index.files.values()),
            'languages': languages,
            'indexed_at': index.updated_at
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Codebase Indexer')
    parser.add_argument('path', nargs='?', default='.', help='Path to index')
    parser.add_argument('--search', '-s', help='Search query')
    parser.add_argument('--symbol', help='Find symbol')
    parser.add_argument('--type', choices=['func', 'class'], help='Symbol type')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--max-files', type=int, default=5000)
    parser.add_argument('--cache-dir', help='Cache directory')
    
    args = parser.parse_args()
    
    indexer = Indexer(args.path, args.cache_dir)
    
    if args.search:
        results = indexer.search(args.search)
        print(f"\n🔍 Search results for '{args.search}':")
        for file_path, score in results:
            print(f"   {score:6.1f}  {file_path}")
    
    elif args.symbol:
        results = indexer.find_symbol(args.symbol, args.type)
        print(f"\n🔍 Symbol '{args.symbol}' found in:")
        for file_path in results:
            print(f"   • {file_path}")
    
    elif args.stats:
        indexer.build_index(args.max_files)
        stats = indexer.get_stats()
        print(f"\n📊 Codebase Statistics")
        print(f"   Root: {stats.get('root')}")
        print(f"   Files: {stats.get('total_files')}")
        print(f"   Lines: {stats.get('total_lines'):,}")
        print(f"   Modules: {stats.get('total_modules')}")
        print(f"   Functions: {stats.get('total_functions')}")
        print(f"   Classes: {stats.get('total_classes')}")
        print(f"\n   Languages:")
        for lang, data in sorted(stats.get('languages', {}).items(), key=lambda x: x[1]['lines'], reverse=True):
            print(f"      {lang}: {data['files']} files, {data['lines']:,} lines")
    
    else:
        indexer.build_index(args.max_files)
        print("\n✅ Indexing complete!")
        print(f"   Use --search, --symbol, or --stats to query the index")


if __name__ == '__main__':
    main()
