import sqlite3
import os
import sys
import json
import time
import ast
import re
import hashlib
import argparse
import fnmatch
import subprocess
from pathlib import Path
from collections import defaultdict, deque
from typing import List, Dict, Set, Tuple, Optional, Any

# --- Configuration ---
DB_NAME = "codebase.db"
MAX_FILE_SIZE = 1024 * 1024  # 1MB
DEFAULT_IGNORE_DIRS = {
    '.git', '.trae', 'node_modules', 'venv', '.venv', '__pycache__',
    'dist', 'build', '.import', 'android', 'ios', '.godot',
    'coverage', '.idea', '.vscode', 'tmp', 'temp', 'logs',
    'vendor', 'bower_components', 'bin', 'obj', 'target'
}
DEFAULT_IGNORE_FILES = {
    'package-lock.json', 'yarn.lock', '.DS_Store', 'codebase_index.json',
    'pnpm-lock.yaml', 'bun.lockb', 'composer.lock', 'Cargo.lock', 'Gemfile.lock',
    DB_NAME
}
SUPPORTED_EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript', '.jsx': 'javascript',
    '.ts': 'typescript', '.tsx': 'typescript',
    '.gd': 'gdscript',
    '.cs': 'csharp',
    '.go': 'go',
    '.java': 'java',
    '.rs': 'rust'
}

# --- Gitignore Parser ---
class GitignoreParser:
    def __init__(self, root: str):
        self.root = Path(root).resolve()
        self.patterns = []
        self._load_gitignore()

    def _load_gitignore(self):
        gitignore_path = self.root / '.gitignore'
        if not gitignore_path.exists():
            return
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    self.patterns.append(line)
        except Exception:
            pass

    def match(self, path: str) -> bool:
        # Simple fnmatch-based matcher (not fully git-compliant but good enough for 90% cases)
        rel_path = str(Path(path).resolve().relative_to(self.root)).replace('\\', '/')
        
        for pattern in self.patterns:
            # Handle directory patterns
            if pattern.endswith('/'):
                if f"{rel_path}/".startswith(pattern) or f"/{rel_path}/".find(f"/{pattern}") != -1:
                    return True
            # Handle wildcards
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(rel_path), pattern):
                return True
        return False

# --- Database Engine ---

class DatabaseEngine:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        # Performance optimization: WAL mode + Normal synchronous
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.init_schema()

    def init_schema(self):
        cur = self.conn.cursor()
        
        # Files Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL,
                mtime REAL,
                checksum TEXT,
                layer INTEGER DEFAULT -1,
                language TEXT,
                scc_id INTEGER DEFAULT -1
            )
        """)
        
        # Symbols Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS symbols (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER,
                name TEXT,
                type TEXT,
                line_start INTEGER,
                line_end INTEGER,
                doc TEXT,
                FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
            )
        """)
        
        # Dependencies Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS dependencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file_id INTEGER,
                target_file_id INTEGER,
                type TEXT,
                alias TEXT,
                count INTEGER DEFAULT 1,
                FOREIGN KEY(source_file_id) REFERENCES files(id) ON DELETE CASCADE,
                FOREIGN KEY(target_file_id) REFERENCES files(id) ON DELETE CASCADE,
                UNIQUE(source_file_id, target_file_id, type)
            )
        """)
        
        # FTS5 Search Index (Virtual Table)
        # Note: 'trigram' tokenizer requires SQLite compile option, fallback to standard
        try:
            cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(file_path, symbol_name, doc, content='symbols', content_rowid='id')")
        except sqlite3.OperationalError:
            # Fallback for older SQLite without FTS5
            print("Warning: FTS5 not supported. Search will be limited.")

        # Triggers to keep FTS updated
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS symbols_ai AFTER INSERT ON symbols BEGIN
                INSERT INTO search_index(rowid, file_path, symbol_name, doc) 
                SELECT new.id, f.path, new.name, new.doc FROM files f WHERE f.id = new.file_id;
            END;
        """)
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS symbols_ad AFTER DELETE ON symbols BEGIN
                INSERT INTO search_index(search_index, rowid, file_path, symbol_name, doc) VALUES('delete', old.id, 'unknown', old.name, old.doc);
            END;
        """)
        
        self.conn.commit()

    def get_file_id(self, path: str) -> Optional[int]:
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM files WHERE path = ?", (path,))
        row = cur.fetchone()
        return row['id'] if row else None

    def upsert_file(self, path: str, mtime: float, checksum: str, language: str) -> int:
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO files (path, mtime, checksum, language) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET 
                mtime=excluded.mtime, 
                checksum=excluded.checksum,
                language=excluded.language
        """, (path, mtime, checksum, language))
        # If updated, clear old data for this file to ensure atomicity of parsing
        file_id = self.get_file_id(path)
        cur.execute("DELETE FROM symbols WHERE file_id = ?", (file_id,))
        cur.execute("DELETE FROM dependencies WHERE source_file_id = ?", (file_id,))
        return file_id

    def add_symbol(self, file_id: int, name: str, type_: str, line_start: int, doc: str = None):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO symbols (file_id, name, type, line_start, doc) VALUES (?, ?, ?, ?, ?)",
                    (file_id, name, type_, line_start, doc))

    def add_dependency(self, source_id: int, target_id: int, type_: str):
        if source_id == target_id: return # Ignore self-reference
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO dependencies (source_file_id, target_file_id, type) VALUES (?, ?, ?)
            ON CONFLICT(source_file_id, target_file_id, type) DO UPDATE SET count = count + 1
        """, (source_id, target_id, type_))

    def get_all_files(self) -> Dict[str, dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, path, mtime FROM files")
        return {row['path']: {'id': row['id'], 'mtime': row['mtime']} for row in cur.fetchall()}

    def clean_deleted_files(self, active_paths: Set[str]):
        cur = self.conn.cursor()
        cur.execute("SELECT path FROM files")
        db_paths = {row['path'] for row in cur.fetchall()}
        
        to_delete = db_paths - active_paths
        if to_delete:
            print(f"Cleaning {len(to_delete)} deleted files from DB...")
            cur.executemany("DELETE FROM files WHERE path = ?", [(p,) for p in to_delete])
            self.conn.commit()

    def close(self):
        self.conn.close()

# --- Parsers ---

class BaseParser:
    def parse(self, content: str, file_path: str) -> dict:
        return {"symbols": [], "imports": []}

class PythonParser(BaseParser):
    def parse(self, content: str, file_path: str) -> dict:
        symbols = []
        imports = []
        try:
            tree = ast.parse(content)
        except Exception as e:
            print(f"  [Parse Error] {file_path}: {e}")
            return {"symbols": [], "imports": []}

        for node in ast.walk(tree):
            # Symbols
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                doc = ast.get_docstring(node)
                type_ = "class" if isinstance(node, ast.ClassDef) else "function"
                symbols.append({
                    "name": node.name,
                    "type": type_,
                    "line": node.lineno,
                    "doc": doc
                })
            
            # Imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"module": alias.name, "alias": alias.asname})
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module
                    for alias in node.names:
                        imports.append({"module": f"{module}.{alias.name}", "alias": alias.asname, "base_module": module})
                else:
                    # Relative import (from . import x)
                    for alias in node.names:
                        imports.append({"module": f".{alias.name}", "alias": alias.asname, "level": node.level})

        return {"symbols": symbols, "imports": imports}

class RegexParser(BaseParser):
    def __init__(self, lang):
        self.lang = lang
        # Simplified regex for JS/TS imports
        self.import_patterns = [
            re.compile(r'import\s+.*?from\s+[\'"](.*?)[\'"]'),  # import ... from '...'
            re.compile(r'require\s*\(\s*[\'"](.*?)[\'"]\s*\)'),  # require('...')
            re.compile(r'import\s*\(\s*[\'"](.*?)[\'"]\s*\)')    # import('...')
        ]
        self.symbol_patterns = [
            re.compile(r'(?:class|function|interface|type)\s+(\w+)'), # class Foo
            re.compile(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:function|=>|\()') # const foo = ...
        ]

    def parse(self, content: str, file_path: str) -> dict:
        symbols = []
        imports = []
        
        # Strip comments (simple)
        content_no_comments = re.sub(r'//.*', '', content)
        content_no_comments = re.sub(r'/\*.*?\*/', '', content_no_comments, flags=re.DOTALL)

        for line_num, line in enumerate(content.splitlines(), 1):
            # Symbols
            for pat in self.symbol_patterns:
                match = pat.search(line)
                if match:
                    symbols.append({
                        "name": match.group(1),
                        "type": "definition",
                        "line": line_num,
                        "doc": None
                    })
        
        # Imports (scan whole content for multiline imports)
        for pat in self.import_patterns:
            for match in pat.finditer(content_no_comments):
                imports.append({"module": match.group(1)})

        return {"symbols": symbols, "imports": imports}

# --- Import Resolver ---

class ImportResolver:
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.file_map = {} # path -> id (populated later)
        self.id_map = {}   # id -> path
        self.ts_paths = self._load_tsconfig_paths()

    def _load_tsconfig_paths(self) -> Dict[str, List[str]]:
        # Naive tsconfig parser
        paths = {}
        for config_name in ['tsconfig.json', 'jsconfig.json']:
            config_path = self.root / config_name
            if config_path.exists():
                try:
                    # Remove comments (standard json doesn't support them, but tsconfig does)
                    text = config_path.read_text(encoding='utf-8')
                    text = re.sub(r'//.*', '', text)
                    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
                    data = json.loads(text)
                    if 'compilerOptions' in data and 'paths' in data['compilerOptions']:
                        for alias, target_list in data['compilerOptions']['paths'].items():
                            # clean alias (e.g., "@/*" -> "@")
                            clean_alias = alias.replace('/*', '')
                            clean_targets = [t.replace('/*', '') for t in target_list]
                            paths[clean_alias] = clean_targets
                except Exception:
                    pass
        return paths

    def update_file_map(self, db_files: Dict[str, dict]):
        self.file_map = {path: info['id'] for path, info in db_files.items()}
        self.id_map = {info['id']: path for path, info in db_files.items()}

    def resolve(self, source_path: str, import_info: dict) -> Optional[int]:
        """Returns target file_id or None"""
        module = import_info.get('module')
        if not module: return None

        source_file = Path(source_path)
        source_dir = source_file.parent

        candidates = []

        # 1. Relative Imports (Python . / ..)
        if 'level' in import_info: 
            # Python relative import
            level = import_info['level']
            # level 1 = ., level 2 = ..
            target_dir = source_dir
            for _ in range(level - 1):
                target_dir = target_dir.parent
            
            # module name might be None (from . import x) -> implies __init__.py
            mod_parts = module.lstrip('.').split('.') if module else []
            candidates.append(target_dir.joinpath(*mod_parts))
        
        # 2. Relative Imports (JS/General ./ or ../)
        elif module.startswith('.'):
            candidates.append(source_dir / module)
        
        # 3. Alias Imports (TS/Webpack @/)
        elif self.ts_paths:
            for alias, targets in self.ts_paths.items():
                if module.startswith(alias):
                    suffix = module[len(alias):]
                    for t in targets:
                        candidates.append(self.root / t / suffix.lstrip('/'))

        # 4. Absolute Imports (Python/Root)
        else:
            # Try from root
            candidates.append(self.root / module.replace('.', '/'))

        # Try extensions
        valid_exts = list(SUPPORTED_EXTENSIONS.keys())
        final_target = None
        
        for cand in candidates:
            # Normalize path to handle '..' and ensure absolute path
            try:
                cand_path = cand.resolve()
            except Exception:
                cand_path = cand.absolute()
            
            cand_str = str(cand_path)

            # Case A: Exact match (unlikely for imports, but possible)
            if cand_str in self.file_map:
                final_target = cand_str
                break
                
            # Case B: Add extension
            for ext in valid_exts:
                p = cand_str + ext
                if p in self.file_map:
                    final_target = p
                    break
            if final_target: break

            # Case C: Index file (folder import)
            for ext in valid_exts:
                p = str(cand_path / f"index{ext}") # JS/TS style
                if p in self.file_map:
                    final_target = p
                    break
                p = str(cand_path / f"__init__{ext}") # Python style
                if p in self.file_map:
                    final_target = p
                    break
            if final_target: break

        if final_target:
            return self.file_map[final_target]
        
        return None

# --- Graph Engine ---

class GraphEngine:
    def __init__(self, db: DatabaseEngine):
        self.db = db

    def compute_layers(self):
        """Computes topological layers, handling cycles via SCC."""
        print("Computing dependency layers...")
        cur = self.db.conn.cursor()
        
        # 1. Load Graph
        cur.execute("SELECT id FROM files")
        nodes = {row['id'] for row in cur.fetchall()}
        
        cur.execute("SELECT source_file_id, target_file_id FROM dependencies")
        edges = defaultdict(set)
        for row in cur.fetchall():
            edges[row['source_file_id']].add(row['target_file_id'])

        # 2. Tarjan's SCC Algorithm
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = set()
        sccs = []

        def strongconnect(v):
            index[v] = index_counter[0]
            lowlinks[v] = index_counter[0]
            index_counter[0] += 1
            stack.append(v)
            on_stack.add(v)

            for w in edges[v]:
                if w not in index:
                    strongconnect(w)
                    lowlinks[v] = min(lowlinks[v], lowlinks[w])
                elif w in on_stack:
                    lowlinks[v] = min(lowlinks[v], index[w])

            if lowlinks[v] == index[v]:
                new_scc = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    new_scc.append(w)
                    if w == v: break
                sccs.append(new_scc)

        for v in nodes:
            if v not in index:
                strongconnect(v)

        # 3. Build DAG of SCCs
        scc_map = {} # node_id -> scc_id
        for i, scc in enumerate(sccs):
            for node in scc:
                scc_map[node] = i
        
        scc_edges = defaultdict(set)
        scc_in_degree = defaultdict(int)
        
        # Initialize in-degree for all SCCs
        for i in range(len(sccs)):
            scc_in_degree[i] = 0

        for u in nodes:
            for v in edges[u]:
                if scc_map[u] != scc_map[v]:
                    if scc_map[v] not in scc_edges[scc_map[u]]:
                        scc_edges[scc_map[u]].add(scc_map[v])
                        scc_in_degree[scc_map[v]] += 1

        # 4. Topological Sort on SCC DAG
        queue = deque([i for i in range(len(sccs)) if scc_in_degree[i] == 0])
        scc_layers = {}
        
        while queue:
            u = queue.popleft()
            layer = scc_layers.get(u, 0)
            
            for v in scc_edges[u]:
                scc_layers[v] = max(scc_layers.get(v, 0), layer + 1)
                scc_in_degree[v] -= 1
                if scc_in_degree[v] == 0:
                    queue.append(v)

        # 5. Update DB
        updates = []
        for node in nodes:
            scc_id = scc_map[node]
            layer = scc_layers.get(scc_id, 0) # Default to 0 if cycle isolated
            updates.append((layer, scc_id, node))
            
        cur.executemany("UPDATE files SET layer = ?, scc_id = ? WHERE id = ?", updates)
        self.db.conn.commit()
        
        cycle_count = sum(1 for scc in sccs if len(scc) > 1)
        if cycle_count > 0:
            print(f"Warning: {cycle_count} dependency cycles detected (treated as single layer).")

# --- Main Manager ---

class CodebaseManager:
    def __init__(self, root: str = "."):
        self.root = os.path.abspath(root)
        self.trae_dir = os.path.join(self.root, '.trae')
        if not os.path.exists(self.trae_dir):
            os.makedirs(self.trae_dir)
        self.db_path = os.path.join(self.trae_dir, DB_NAME)
        self.db = DatabaseEngine(self.db_path)
        self.resolver = ImportResolver(self.root)
        self.gitignore = GitignoreParser(self.root)

    def normalize_path(self, path: str) -> str:
        # Store as absolute paths, but normalized separators
        return str(Path(path).resolve())

    def should_ignore(self, path: str) -> bool:
        p = Path(path)
        if p.name in DEFAULT_IGNORE_FILES: return True
        for part in p.parts:
            if part in DEFAULT_IGNORE_DIRS: return True
        
        # Check gitignore
        if self.gitignore.match(path):
            return True
            
        return False

    def get_git_changed_files(self) -> Set[str]:
        """Returns a set of absolute paths that have changed according to git."""
        changed = set()
        try:
            # Check for unstaged changes
            output = subprocess.check_output(['git', 'diff', '--name-only'], cwd=self.root, text=True)
            for line in output.splitlines():
                if line.strip():
                    changed.add(os.path.join(self.root, line.strip()))
            
            # Check for staged changes
            output = subprocess.check_output(['git', 'diff', '--name-only', '--cached'], cwd=self.root, text=True)
            for line in output.splitlines():
                if line.strip():
                    changed.add(os.path.join(self.root, line.strip()))
                    
            # Check for untracked files
            output = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=self.root, text=True)
            for line in output.splitlines():
                if line.strip():
                    changed.add(os.path.join(self.root, line.strip()))
                    
        except Exception:
            # Git not available or not a git repo, fallback to mtime
            pass
        return changed

    def scan_files(self) -> List[str]:
        files = []
        for root, _, filenames in os.walk(self.root):
            if self.should_ignore(root): continue
            for f in filenames:
                if self.should_ignore(os.path.join(root, f)): continue
                ext = os.path.splitext(f)[1]
                if ext in SUPPORTED_EXTENSIONS:
                    files.append(os.path.join(root, f))
        return files

    def update(self):
        print("Starting incremental update...")
        start_time = time.time()
        
        # 1. Scan Disk
        disk_files = self.scan_files()
        disk_files_set = {self.normalize_path(f) for f in disk_files}
        
        # 2. Clean Deleted
        self.db.clean_deleted_files(disk_files_set)
        
        # 3. Identify Changed Files
        db_files = self.db.get_all_files() # path -> {id, mtime}
        to_process = []
        
        # Optimization: Try git diff first
        git_changes = self.get_git_changed_files()
        use_git = len(git_changes) > 0
        if use_git:
            print(f"Detected {len(git_changes)} changes via git.")
        
        for f_path in disk_files:
            norm_path = self.normalize_path(f_path)
            
            # If git detected changes, only check those (plus files not in DB)
            if use_git:
                if norm_path not in db_files or f_path in git_changes or norm_path in git_changes:
                    # Double check mtime just in case
                    try:
                        mtime = os.path.getmtime(f_path)
                        to_process.append((f_path, norm_path, mtime))
                    except FileNotFoundError:
                        continue
                continue
            
            # Fallback to mtime check
            try:
                mtime = os.path.getmtime(f_path)
            except FileNotFoundError:
                continue

            if norm_path not in db_files or db_files[norm_path]['mtime'] != mtime:
                to_process.append((f_path, norm_path, mtime))

        if not to_process:
            print("No changes detected.")
            return

        print(f"Processing {len(to_process)} changed files...")
        
        # 4. Parse & Upsert Nodes (Files & Symbols)
        # We must upsert files first to get IDs for dependency resolution
        temp_imports = [] # Store (source_id, import_info) for pass 2

        for f_path, norm_path, mtime in to_process:
            ext = os.path.splitext(f_path)[1]
            lang = SUPPORTED_EXTENSIONS.get(ext, 'unknown')
            
            # Read content
            try:
                with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                checksum = hashlib.md5(content.encode()).hexdigest()
            except Exception as e:
                print(f"Error reading {f_path}: {e}")
                continue

            # DB Upsert
            file_id = self.db.upsert_file(norm_path, mtime, checksum, lang)
            
            # Parse
            parser = PythonParser() if lang == 'python' else RegexParser(lang)
            result = parser.parse(content, f_path)
            
            # Insert Symbols
            for sym in result['symbols']:
                self.db.add_symbol(file_id, sym['name'], sym['type'], sym['line'], sym['doc'])
            
            # Store imports for dependency resolution
            for imp in result['imports']:
                temp_imports.append((file_id, imp, norm_path))

        self.db.conn.commit() # Commit nodes before edges

        # 5. Resolve Dependencies (Pass 2)
        # We need updated file map
        self.resolver.update_file_map(self.db.get_all_files())
        
        for source_id, imp, source_path in temp_imports:
            target_id = self.resolver.resolve(source_path, imp)
            if target_id:
                self.db.add_dependency(source_id, target_id, 'import')

        self.db.conn.commit()

        # 6. Recompute Layers
        GraphEngine(self.db).compute_layers()
        
        print(f"Update complete in {time.time() - start_time:.2f}s")

    def search(self, query: str):
        cur = self.db.conn.cursor()
        results = []
        
        # Try FTS first
        try:
            cur.execute("""
                SELECT file_path, symbol_name, doc, rank
                FROM search_index 
                WHERE search_index MATCH ? 
                ORDER BY rank LIMIT 10
            """, (query,))
            rows = cur.fetchall()
            if rows:
                for r in rows:
                    results.append({
                        "file": r['file_path'],
                        "symbol": r['symbol_name'],
                        "doc": r['doc'],
                        "score": r['rank']
                    })
        except Exception:
            pass
        
        # Fallback to exact match if no FTS results
        if not results:
            cur.execute("""
                SELECT f.path, s.name, s.line_start, s.doc 
                FROM symbols s 
                JOIN files f ON s.file_id = f.id 
                WHERE s.name LIKE ? LIMIT 10
            """, (f"%{query}%",))
            rows = cur.fetchall()
            for r in rows:
                results.append({
                    "file": r['path'],
                    "symbol": r['name'],
                    "line": r['line_start'],
                    "doc": r['doc']
                })

        # Output as JSONL for AI consumption
        if not results:
            print(json.dumps({"error": "No matches found", "query": query}))
        else:
            for res in results:
                print(json.dumps(res))

    def inspect(self, file_pattern: str):
        cur = self.db.conn.cursor()
        
        # Find file (support partial match)
        cur.execute("SELECT id, path, layer, mtime FROM files WHERE path LIKE ? OR path LIKE ? LIMIT 1", 
                   (f"%{file_pattern}", f"%/{file_pattern}"))
        f = cur.fetchone()
        
        if not f:
            print(json.dumps({"error": "File not found", "pattern": file_pattern}))
            return

        file_id = f['id']
        file_path = f['path']
        layer = f['layer']
        
        # 1. Upstream (Who imports me?) - Impact Analysis
        cur.execute("""
            SELECT f.path, d.count FROM dependencies d 
            JOIN files f ON d.source_file_id = f.id 
            WHERE d.target_file_id = ?
        """, (file_id,))
        upstream_rows = cur.fetchall()
        upstream = [r['path'] for r in upstream_rows]
        
        # 2. Downstream (Who do I import?) - Dependency Analysis
        cur.execute("""
            SELECT f.path FROM dependencies d 
            JOIN files f ON d.target_file_id = f.id 
            WHERE d.source_file_id = ?
        """, (file_id,))
        downstream = [r['path'] for r in cur.fetchall()]
        
        # 3. Symbols defined in this file
        cur.execute("SELECT name, type, line_start FROM symbols WHERE file_id = ?", (file_id,))
        symbols = [{"name": r['name'], "type": r['type'], "line": r['line_start']} for r in cur.fetchall()]

        # 4. Risk Calculation
        # Heuristic: High impact if used by many files, or if it's a core layer (0-1) used by upper layers
        impact_count = len(upstream)
        risk_score = "LOW"
        if impact_count > 5: risk_score = "MEDIUM"
        if impact_count > 20: risk_score = "HIGH"
        if layer == 0 and impact_count > 0: risk_score = "HIGH" # Core util modification is risky
        
        # 5. Generate External Doc (codeguiddoc.md)
        doc_path = os.path.join(self.trae_dir, "codeguiddoc.md")
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(f"# Analysis: {os.path.basename(file_path)}\n\n")
            f.write(f"**Risk Score**: {risk_score} (Impact: {impact_count} files)\n")
            f.write(f"**File Path**: `{file_path}`\n\n")
            
            f.write("## 📊 Dependency Graph (Mermaid)\n")
            f.write("```mermaid\ngraph TD\n")
            f.write(f"    Target[{os.path.basename(file_path)}]:::target\n")
            f.write("    classDef target fill:#f9f,stroke:#333,stroke-width:2px;\n\n")
            
            # Limit graph complexity for readability
            for p in upstream[:20]:
                f.write(f"    {os.path.basename(p)} --> Target\n")
            if len(upstream) > 20:
                f.write(f"    ...({len(upstream)-20} more) --> Target\n")
                
            for p in downstream[:20]:
                f.write(f"    Target --> {os.path.basename(p)}\n")
            if len(downstream) > 20:
                f.write(f"    Target --> ...({len(downstream)-20} more)\n")
            f.write("```\n\n")
            
            f.write("## ⬆️ Used By (Upstream)\n")
            for p in upstream:
                f.write(f"- `{p}`\n")
            if not upstream: f.write("*(None)*\n")
            
            f.write("\n## ⬇️ Depends On (Downstream)\n")
            for p in downstream:
                f.write(f"- `{p}`\n")
            if not downstream: f.write("*(None)*\n")

        # Output structured JSON (Summary only)
        output = {
            "file": file_path,
            "layer": layer,
            "risk_score": risk_score,
            "impact_count": impact_count,
            "doc_file": doc_path,
            "summary": f"Full dependency graph written to {doc_path}. Check Mermaid chart for visual confirmation.",
            "symbols": symbols[:5] # Just a peek
        }
        print(json.dumps(output, indent=2))

    def export_graph(self):
        cur = self.db.conn.cursor()
        
        # Layers
        cur.execute("SELECT path, layer FROM files ORDER BY layer, path")
        layers = defaultdict(list)
        for r in cur.fetchall():
            layers[r['layer']].append(os.path.basename(r['path']))
        
        md_path = os.path.join(self.trae_dir, "architecture_layers.md")
        with open(md_path, "w", encoding='utf-8') as f:
            f.write("# Architecture Layers\n\n")
            for layer_id in sorted(layers.keys()):
                files = layers[layer_id]
                f.write(f"- **Layer {layer_id}**: {', '.join(files)}\n")
        print(f"Exported layers to {md_path}")
        
        # JSON Graph
        cur.execute("SELECT id, path, layer FROM files")
        nodes = [{"id": r['id'], "label": os.path.basename(r['path']), "layer": r['layer']} for r in cur.fetchall()]
        
        cur.execute("SELECT source_file_id, target_file_id, type FROM dependencies")
        links = [{"source": r['source_file_id'], "target": r['target_file_id'], "type": r['type']} for r in cur.fetchall()]
        
        json_path = os.path.join(self.trae_dir, "dependency_graph.json")
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump({"nodes": nodes, "links": links}, f, indent=2)
        print(f"Exported graph to {json_path}")

# --- CLI ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trae Codebase Manager")
    parser.add_argument("command", choices=["update", "search", "inspect", "graph"])
    parser.add_argument("arg", nargs="?", help="Search query or file pattern")
    parser.add_argument("--root", default=".", help="Root directory")
    
    args = parser.parse_args()
    
    manager = CodebaseManager(args.root)
    
    if args.command == "update":
        manager.update()
    elif args.command == "search":
        if not args.arg: print("Error: Search query required"); sys.exit(1)
        manager.search(args.arg)
    elif args.command == "inspect":
        if not args.arg: print("Error: File pattern required"); sys.exit(1)
        manager.inspect(args.arg)
    elif args.command == "graph":
        manager.export_graph()
