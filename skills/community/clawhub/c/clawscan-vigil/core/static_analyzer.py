"""
Static Analyzer - AST-based security analysis
"""

import ast
import re
from pathlib import Path
from typing import List, Optional

from core.models import Finding, RiskLevel


# Dangerous patterns by category
DANGEROUS_PATTERNS = {
    "network": {
        "level": RiskLevel.HIGH,
        "patterns": [
            r"import\s+requests",
            r"import\s+urllib",
            r"import\s+http",
            r"import\s+socket",
            r"from\s+requests",
            r"from\s+urllib",
            r"urlopen\s*\(",
            r"requests\.(get|post|put|delete|patch)\s*\(",
        ],
        "description": "Network request capability detected",
    },
    "filesystem_write": {
        "level": RiskLevel.HIGH,
        "patterns": [
            r"open\s*\([^)]*,\s*['\"]w",
            r"\.write\s*\(",
            r"\.writelines\s*\(",
            r"os\.mkdir",
            r"os\.makedirs",
            r"shutil\.(copy|move|rmtree)",
            r"pathlib.*\.write",
        ],
        "description": "File system write access detected",
    },
    "filesystem_read_sensitive": {
        "level": RiskLevel.HIGH,
        "patterns": [
            r"open\s*\([^)]*\.env",
            r"open\s*\([^)]*config",
            r"open\s*\([^)]*secret",
            r"open\s*\([^)]*key",
            r"os\.environ\[",
            r"os\.getenv\s*\(",
        ],
        "description": "Access to sensitive file or environment variable",
    },
    "subprocess": {
        "level": RiskLevel.MEDIUM,
        "patterns": [
            r"import\s+subprocess",
            r"subprocess\.(run|call|Popen)",
            r"os\.system\s*\(",
            r"os\.popen\s*\(",
            r"eval\s*\(",
            r"exec\s*\(",
        ],
        "description": "Subprocess execution capability detected",
    },
    "crypto_wallet": {
        "level": RiskLevel.HIGH,
        "patterns": [
            r"bitcoin",
            r"ethereum",
            r"wallet",
            r"mnemonic",
            r"private.*key",
            r"seed.*phrase",
            r"web3",
            r"ethers",
        ],
        "description": "Cryptocurrency/wallet related code detected",
    },
    "api_keys": {
        "level": RiskLevel.MEDIUM,
        "patterns": [
            r"api[_-]?key",
            r"apikey",
            r"token\s*=",
            r"password\s*=",
            r"secret\s*=",
            r"Authorization",
        ],
        "description": "API key or credential handling detected",
    },
    "obfuscation": {
        "level": RiskLevel.MEDIUM,
        "patterns": [
            r"base64\.(b64decode|decode)",
            r"\.decode\s*\(\s*['\"]rot13",
            r"__import__\s*\(",
            r"getattr\s*\(.*__import__",
            r"eval\s*\(\s*compile",
            r"chr\s*\(\s*\d+\)\s*\+",
        ],
        "description": "Potential code obfuscation detected",
    },
}


class StaticAnalyzer:
    """Analyze Python code for security risks using AST and regex"""
    
    def __init__(self):
        self.findings: List[Finding] = []
    
    def analyze_file(self, file_path: Path) -> List[Finding]:
        """Analyze a single Python file"""
        self.findings = []
        
        if not file_path.exists() or not file_path.suffix == ".py":
            return self.findings
        
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")
            
            # AST analysis
            self._ast_analysis(content, file_path, lines)
            
            # Regex pattern matching
            self._pattern_analysis(content, file_path, lines)
            
        except SyntaxError as e:
            self.findings.append(Finding(
                level=RiskLevel.MEDIUM,
                category="syntax_error",
                description=f"Syntax error in file: {e}",
                file=str(file_path),
                line=e.lineno or 0,
                confidence=0.9,
            ))
        except Exception as e:
            self.findings.append(Finding(
                level=RiskLevel.LOW,
                category="analysis_error",
                description=f"Failed to analyze: {e}",
                file=str(file_path),
                line=0,
                confidence=0.5,
            ))
        
        return self.findings
    
    def _ast_analysis(self, content: str, file_path: Path, lines: List[str]):
        """Analyze code using AST"""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return
        
        for node in ast.walk(tree):
            # Check for network imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in ("requests", "urllib", "http", "socket", "ftplib"):
                        self._add_finding_from_node(
                            node, lines, RiskLevel.HIGH, "network",
                            f"Network module imported: {alias.name}",
                            str(file_path)
                        )
            
            if isinstance(node, ast.ImportFrom):
                if node.module in ("requests", "urllib", "http", "socket", "subprocess", "os"):
                    level = RiskLevel.HIGH if node.module in ("requests", "urllib") else RiskLevel.MEDIUM
                    self._add_finding_from_node(
                        node, lines, level, "import",
                        f"Module import: {node.module}",
                        str(file_path)
                    )
            
            # Check for function calls
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                
                if func_name in ("eval", "exec"):
                    self._add_finding_from_node(
                        node, lines, RiskLevel.HIGH, "code_execution",
                        f"Dangerous function call: {func_name}()",
                        str(file_path)
                    )
                
                if func_name in ("os.system", "os.popen", "subprocess.run", "subprocess.call", "subprocess.Popen"):
                    self._add_finding_from_node(
                        node, lines, RiskLevel.HIGH, "subprocess",
                        f"Subprocess execution: {func_name}()",
                        str(file_path)
                    )
                
                if func_name in ("open",) and self._is_write_mode(node):
                    self._add_finding_from_node(
                        node, lines, RiskLevel.HIGH, "filesystem_write",
                        "File write operation detected",
                        str(file_path)
                    )
    
    def _pattern_analysis(self, content: str, file_path: Path, lines: List[str]):
        """Analyze code using regex patterns"""
        for category, config in DANGEROUS_PATTERNS.items():
            for pattern in config["patterns"]:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    # Calculate line number
                    line_num = content[:match.start()].count("\n") + 1
                    line_content = lines[line_num - 1] if line_num <= len(lines) else ""
                    
                    # Check if not already found by AST
                    if not self._is_duplicate(str(file_path), line_num, category):
                        self.findings.append(Finding(
                            level=config["level"],
                            category=category,
                            description=config["description"],
                            file=str(file_path),
                            line=line_num,
                            code_snippet=line_content.strip()[:100],
                            confidence=0.8,
                        ))
    
    def _get_func_name(self, node) -> str:
        """Get full function name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self._get_func_name(node.value)
            return f"{value}.{node.attr}" if value else node.attr
        return ""
    
    def _is_write_mode(self, node: ast.Call) -> bool:
        """Check if open() is in write mode"""
        if node.args and len(node.args) >= 2:
            mode_arg = node.args[1]
            if isinstance(mode_arg, ast.Constant) and isinstance(mode_arg.value, str):
                return "w" in mode_arg.value or "a" in mode_arg.value or "x" in mode_arg.value
        return False
    
    def _add_finding_from_node(self, node, lines: List[str], level: RiskLevel, 
                               category: str, description: str, file: str):
        """Add finding from AST node"""
        line_num = getattr(node, "lineno", 0)
        line_content = lines[line_num - 1] if line_num > 0 and line_num <= len(lines) else ""
        
        self.findings.append(Finding(
            level=level,
            category=category,
            description=description,
            file=file,
            line=line_num,
            code_snippet=line_content.strip()[:100],
            confidence=0.9,
        ))
    
    def _is_duplicate(self, file: str, line: int, category: str) -> bool:
        """Check if finding already exists"""
        for f in self.findings:
            if f.file == file and f.line == line and f.category == category:
                return True
        return False
