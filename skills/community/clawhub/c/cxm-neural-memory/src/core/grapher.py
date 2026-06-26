import ast
from pathlib import Path
from typing import Dict, List

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.functions = []
        self.classes = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

class DependencyGrapher:
    """Builds an AST-based dependency graph of Python files."""
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir).resolve()

    def build_graph(self, target: str = ".") -> Dict:
        target_path = (self.root_dir / target).resolve()
        
        graph = {
            "nodes": {},
            "edges": []
        }

        files_to_parse = []
        if target_path.is_file() and target_path.suffix == ".py":
            files_to_parse.append(target_path)
        elif target_path.is_dir():
            files_to_parse.extend(target_path.rglob("*.py"))
            
        for file_path in files_to_parse:
            # Aggressively skip non-project directories
            forbidden_parts = {
                'venv', '.venv', 'partner', 'env', 'ENV', 'node_modules', 
                '.git', '__pycache__', '.pytest_cache', 'site-packages', 
                'dist', 'build', '.cxm', 'cxm_agent_bundle'
            }
            if any(part in file_path.parts for part in forbidden_parts):
                continue
                
            try:
                content = file_path.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(file_path))
                
                visitor = ImportVisitor()
                visitor.visit(tree)
                
                try:
                    rel_path = str(file_path.relative_to(self.root_dir))
                except ValueError:
                    rel_path = str(file_path)
                    
                graph["nodes"][rel_path] = {
                    "type": "file",
                    "functions": visitor.functions,
                    "classes": visitor.classes,
                    "imports": visitor.imports
                }
                
                for imp in visitor.imports:
                    graph["edges"].append({"source": rel_path, "target": imp})
                    
            except Exception:
                # Ignore syntax errors or read errors
                pass

        # Compute Hotspots (Files/Modules most heavily depended upon)
        in_degree = {}
        for edge in graph["edges"]:
            target = edge["target"]
            in_degree[target] = in_degree.get(target, 0) + 1
            
        # Sort by most incoming connections
        hotspots = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:10]
        graph["hotspots"] = [{"module": k, "incoming_dependencies": v} for k, v in hotspots]

        return graph
