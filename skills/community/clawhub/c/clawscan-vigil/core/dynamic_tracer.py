"""
Dynamic Tracer - Lightweight sandboxed execution for behavior analysis
"""

import ast
import sys
import io
import builtins
from contextlib import redirect_stdout, redirect_stderr
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Guards import safe_builtins

from core.models import Finding, RiskLevel


@dataclass
class ExecutionTrace:
    """Trace of dynamic execution"""
    function_calls: List[str] = field(default_factory=list)
    imports: Set[str] = field(default_factory=set)
    file_accesses: List[str] = field(default_factory=list)
    network_urls: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    completed: bool = False


class DynamicTracer:
    """
    Execute Skill code in restricted environment to observe behavior.
    This catches runtime behaviors that static analysis misses.
    """
    
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.trace = ExecutionTrace()
    
    def analyze(self, code: str, file_path: Path) -> List[Finding]:
        """
        Attempt to execute code in sandbox and observe behavior.
        Returns findings based on observed behavior.
        """
        findings = []
        
        # Check if code is safe to attempt execution
        if not self._is_safe_to_execute(code):
            findings.append(Finding(
                level=RiskLevel.MEDIUM,
                category="dynamic_analysis_skipped",
                description="Code contains constructs unsafe for dynamic analysis",
                file=str(file_path),
                line=0,
                confidence=0.7,
            ))
            return findings
        
        # Prepare restricted environment
        restricted_globals = self._prepare_restricted_env()
        
        # Capture execution trace
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        try:
            # Compile with RestrictedPython
            compiled = compile_restricted(code, filename=str(file_path), mode='exec')
            
            if compiled is None:
                findings.append(Finding(
                    level=RiskLevel.MEDIUM,
                    category="restriction_violation",
                    description="Code violates RestrictedPython security policies",
                    file=str(file_path),
                    line=0,
                    confidence=0.9,
                ))
                return findings
            
            # Execute in sandbox
            exec(compiled, restricted_globals)
            self.trace.completed = True
            
        except Exception as e:
            self.trace.errors.append(str(e))
            # Errors during restricted execution are actually good signs
            # It means the code tried to do something suspicious
            if "_getiter_" in str(e) or "_iter_unpack_sequence_" in str(e):
                findings.append(Finding(
                    level=RiskLevel.LOW,
                    category="iteration_pattern",
                    description="Code uses iteration patterns (benign)",
                    file=str(file_path),
                    line=0,
                    confidence=0.6,
                ))
            elif "__import__" in str(e):
                findings.append(Finding(
                    level=RiskLevel.HIGH,
                    category="dynamic_import",
                    description="Code attempts dynamic imports (suspicious)",
                    file=str(file_path),
                    line=0,
                    confidence=0.85,
                ))
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        # Analyze trace for findings
        findings.extend(self._analyze_trace(file_path))
        
        return findings
    
    def _is_safe_to_execute(self, code: str) -> bool:
        """Quick check if code looks safe to execute"""
        dangerous_patterns = [
            "while True:",  # Infinite loops
            "__import__",
            "eval(",
            "exec(",
        ]
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                return False
        return True
    
    def _prepare_restricted_env(self) -> Dict[str, Any]:
        """Prepare restricted execution environment"""
        
        # Track imports
        class ImportTracker:
            def __init__(self, trace: ExecutionTrace):
                self.trace = trace
            
            def __call__(self, name, *args, **kwargs):
                self.trace.imports.add(name)
                # Return a mock object that tracks attribute access
                return MockObject(name, self.trace)
        
        # Mock object that tracks method calls
        class MockObject:
            def __init__(self, name: str, trace: ExecutionTrace):
                self._name = name
                self._trace = trace
            
            def __getattr__(self, name: str):
                full_name = f"{self._name}.{name}"
                self._trace.function_calls.append(full_name)
                
                # Track suspicious patterns
                if name in ("get", "post", "put", "delete", "patch"):
                    self._trace.network_urls.append(f"{full_name}()")
                if name in ("read", "write", "open"):
                    self._trace.file_accesses.append(full_name)
                
                return MockMethod(full_name, self._trace)
            
            def __call__(self, *args, **kwargs):
                self._trace.function_calls.append(f"{self._name}()")
                return MockObject(f"{self._name}_result", self._trace)
        
        class MockMethod:
            def __init__(self, name: str, trace: ExecutionTrace):
                self._name = name
                self._trace = trace
            
            def __call__(self, *args, **kwargs):
                self._trace.function_calls.append(f"{self._name}()")
                return MockObject(f"{self._name}_result", self._trace)
        
        tracker = ImportTracker(self.trace)
        
        # Build restricted globals
        restricted_globals = {
            "__builtins__": safe_builtins.copy(),
            "__import__": tracker,
            "_getattr_": getattr,
            "_setattr_": setattr,
            "_getitem_": lambda obj, key: obj[key],
            "_setitem_": lambda obj, key, value: obj.__setitem__(key, value),
            "_iter_unpack_sequence_": lambda it, spec: list(it),
            "_getiter_": lambda ob: ob,
        }
        
        return restricted_globals
    
    def _analyze_trace(self, file_path: Path) -> List[Finding]:
        """Analyze execution trace and generate findings"""
        findings = []
        
        # Check for network-related imports that were actually used
        network_modules = {"requests", "urllib", "http", "socket", "ftplib", "httpx"}
        used_network = self.trace.imports.intersection(network_modules)
        
        if used_network:
            findings.append(Finding(
                level=RiskLevel.HIGH,
                category="dynamic_network",
                description=f"Code dynamically uses network modules: {', '.join(used_network)}",
                file=str(file_path),
                line=0,
                confidence=0.9,
            ))
        
        # Check for file system operations
        fs_modules = {"os", "shutil", "pathlib"}
        used_fs = self.trace.imports.intersection(fs_modules)
        
        if used_fs and any("write" in fa.lower() or "open" in fa.lower() 
                          for fa in self.trace.file_accesses):
            findings.append(Finding(
                level=RiskLevel.HIGH,
                category="dynamic_filesystem",
                description="Code performs file system operations",
                file=str(file_path),
                line=0,
                confidence=0.85,
            ))
        
        # Check for subprocess
        if "subprocess" in self.trace.imports:
            findings.append(Finding(
                level=RiskLevel.HIGH,
                category="dynamic_subprocess",
                description="Code imports subprocess module",
                file=str(file_path),
                line=0,
                confidence=0.9,
            ))
        
        # Check for crypto-related imports
        crypto_modules = {"web3", "bitcoin", "ethereum", "eth_account", "bip39"}
        used_crypto = self.trace.imports.intersection(crypto_modules)
        
        if used_crypto:
            findings.append(Finding(
                level=RiskLevel.HIGH,
                category="dynamic_crypto",
                description=f"Code imports cryptocurrency modules: {', '.join(used_crypto)}",
                file=str(file_path),
                line=0,
                confidence=0.95,
            ))
        
        return findings
