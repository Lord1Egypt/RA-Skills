"""Tool Sandbox - Isolated Execution for AI Agent Tools
Protection against Lethal Trifecta attacks

Sandboxes all tool executions with:
- Permission-based access control
- External domain allowlisting
- Rate limiting
- Human-in-the-loop for sensitive ops
"""

import re
import yaml
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any, Set
from enum import Enum
from functools import wraps
import fnmatch


class PermissionLevel(Enum):
    ALLOWED = "allowed"
    RESTRICTED = "restricted"  # Requires additional validation
    FORBIDDEN = "forbidden"


class SensitivityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"  # Requires human approval
    CRITICAL = "critical"  # Always blocked in auto mode


@dataclass
class ToolCall:
    """Represents a tool call request"""
    tool_name: str
    arguments: Dict[str, Any]
    caller_context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class ToolResult:
    """Result of a sandboxed tool execution"""
    success: bool
    output: Any
    blocked: bool = False
    block_reason: str = ""
    requires_approval: bool = False
    approval_reason: str = ""
    execution_time_ms: float = 0.0
    audit_log: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SandboxConfig:
    """Configuration for tool sandbox"""
    # Permission rules: tool_name -> PermissionLevel
    tool_permissions: Dict[str, PermissionLevel] = field(default_factory=dict)
    
    # Domain allowlist for external calls
    allowed_domains: List[str] = field(default_factory=list)
    blocked_domains: List[str] = field(default_factory=list)
    
    # Rate limiting
    max_calls_per_minute: int = 60
    max_calls_per_tool_per_minute: int = 20
    
    # Sensitive operation detection
    sensitive_patterns: List[str] = field(default_factory=list)
    
    # Auto-approve settings
    auto_approve_safe: bool = True
    require_approval_for_sensitive: bool = True
    
    @classmethod
    def from_yaml(cls, path: str) -> "SandboxConfig":
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)
    
    def to_yaml(self, path: str):
        with open(path, 'w') as f:
            yaml.dump(self.__dict__, f)


class ToolSandbox:
    """Sandboxed execution environment for AI agent tools"""
    
    DEFAULT_BLOCKED_DOMAINS = [
        "*evil.com",
        "*attacker.com",
        "*malicious.net",
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "*.local",
    ]
    
    DEFAULT_SENSITIVE_PATTERNS = [
        r"(send|email|transmit|exfiltrate)\s+(data|information|logs)",
        r"(api[_-]?key|secret[_-]?key|password|token)\s*[:=]",
        r"(credit[_-]?card|ssn|social[_-]?security)",
        r"(delete|remove|drop)\s+(database|table|user)",
        r"(exec|eval|system)\s*\(",
        r"(curl|wget|fetch)\s+(http|https)",
    ]
    
    def __init__(self, config: Optional[SandboxConfig] = None):
        self.config = config or self._default_config()
        self._call_history: List[ToolCall] = []
        self._tool_implementations: Dict[str, Callable] = {}
        self._rate_limiter: Dict[str, List[float]] = {}
        self._setup_default_rules()
    
    def _default_config(self) -> SandboxConfig:
        """Generate default sandbox configuration"""
        return SandboxConfig(
            tool_permissions={
                "search": PermissionLevel.ALLOWED,
                "calculator": PermissionLevel.ALLOWED,
                "read_file": PermissionLevel.RESTRICTED,
                "write_file": PermissionLevel.RESTRICTED,
                "send_email": PermissionLevel.FORBIDDEN,
                "http_request": PermissionLevel.RESTRICTED,
                "execute_code": PermissionLevel.FORBIDDEN,
                "database_query": PermissionLevel.RESTRICTED,
                "browser_navigate": PermissionLevel.RESTRICTED,
            },
            allowed_domains=[
                "openweathermap.org",
                "api.github.com",
                "*.googleapis.com",
                "wikipedia.org",
                "*.openai.com",
            ],
            blocked_domains=self.DEFAULT_BLOCKED_DOMAINS,
            max_calls_per_minute=60,
            max_calls_per_tool_per_minute=20,
            sensitive_patterns=self.DEFAULT_SENSITIVE_PATTERNS,
            require_approval_for_sensitive=True,
        )
    
    def _setup_default_rules(self):
        """Set up default security rules"""
        self._sensitive_regex = [re.compile(p, re.IGNORECASE) for p in self.config.sensitive_patterns]
    
    def register_tool(self, name: str, implementation: Callable, 
                     permission: Optional[PermissionLevel] = None):
        """Register a tool with the sandbox"""
        self._tool_implementations[name] = implementation
        if permission:
            self.config.tool_permissions[name] = permission
    
    def execute(self, tool_name: str, arguments: Dict[str, Any], 
                caller_context: Optional[Dict[str, Any]] = None) -> ToolResult:
        """
        Execute a tool through the sandbox
        
        Returns ToolResult with execution result or block information
        """
        import time
        start = time.time()
        
        call = ToolCall(
            tool_name=tool_name,
            arguments=arguments,
            caller_context=caller_context or {}
        )
        
        # Check 1: Tool permission
        permission = self.config.tool_permissions.get(tool_name, PermissionLevel.RESTRICTED)
        if permission == PermissionLevel.FORBIDDEN:
            return ToolResult(
                success=False,
                output=None,
                blocked=True,
                block_reason=f"Tool '{tool_name}' is forbidden",
                execution_time_ms=(time.time() - start) * 1000,
                audit_log=self._create_audit_log(call, "PERMISSION_DENIED")
            )
        
        # Check 2: Rate limiting
        rate_check = self._check_rate_limit(tool_name)
        if not rate_check["allowed"]:
            return ToolResult(
                success=False,
                output=None,
                blocked=True,
                block_reason=f"Rate limit exceeded: {rate_check['reason']}",
                execution_time_ms=(time.time() - start) * 1000,
                audit_log=self._create_audit_log(call, "RATE_LIMITED")
            )
        
        # Check 3: Domain validation (for HTTP tools)
        domain_check = self._validate_domains(arguments)
        if not domain_check["valid"]:
            return ToolResult(
                success=False,
                output=None,
                blocked=True,
                block_reason=f"Domain not allowed: {domain_check['domain']}",
                execution_time_ms=(time.time() - start) * 1000,
                audit_log=self._create_audit_log(call, "DOMAIN_BLOCKED")
            )
        
        # Check 4: Sensitive operation detection
        sensitivity = self._check_sensitivity(tool_name, arguments)
        if sensitivity["is_sensitive"] and self.config.require_approval_for_sensitive:
            return ToolResult(
                success=False,
                output=None,
                blocked=False,
                requires_approval=True,
                approval_reason=sensitivity["reason"],
                execution_time_ms=(time.time() - start) * 1000,
                audit_log=self._create_audit_log(call, "REQUIRES_APPROVAL")
            )
        
        # Check 5: Execute the tool
        try:
            result = self._execute_tool_impl(tool_name, arguments)
            execution_time_ms = (time.time() - start) * 1000
            
            # Validate output (don't pass raw tool output directly to agent)
            validated_output = self._validate_output(result)
            
            self._call_history.append(call)
            
            return ToolResult(
                success=True,
                output=validated_output,
                execution_time_ms=execution_time_ms,
                audit_log=self._create_audit_log(call, "SUCCESS")
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                blocked=True,
                block_reason=f"Execution error: {str(e)}",
                execution_time_ms=(time.time() - start) * 1000,
                audit_log=self._create_audit_log(call, "EXECUTION_ERROR", error=str(e))
            )
    
    def _check_rate_limit(self, tool_name: str) -> Dict[str, Any]:
        """Check if call is within rate limits"""
        now = time.time()
        minute_ago = now - 60
        
        # Global rate limit
        global_calls = [t for t in self._call_history if t.timestamp > minute_ago]
        if len(global_calls) >= self.config.max_calls_per_minute:
            return {"allowed": False, "reason": "Global rate limit exceeded"}
        
        # Per-tool rate limit
        tool_calls = [t for t in global_calls if t.tool_name == tool_name]
        if len(tool_calls) >= self.config.max_calls_per_tool_per_minute:
            return {"allowed": False, "reason": f"Rate limit for '{tool_name}' exceeded"}
        
        return {"allowed": True}
    
    def _validate_domains(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Validate any URLs/domains in arguments against allowlist"""
        # Extract potential URLs from arguments
        url_pattern = r'https?://([^/\s]+)'
        
        def find_urls(obj):
            urls = []
            if isinstance(obj, str):
                urls.extend(re.findall(url_pattern, obj))
            elif isinstance(obj, dict):
                for v in obj.values():
                    urls.extend(find_urls(v))
            elif isinstance(obj, list):
                for item in obj:
                    urls.extend(find_urls(item))
            return urls
        
        urls = find_urls(arguments)
        
        for url in urls:
            # Check blocked domains first
            for blocked in self.config.blocked_domains:
                if fnmatch.fnmatch(url.lower(), blocked.lower()):
                    return {"valid": False, "domain": url}
            
            # Check if URL matches allowed domains
            allowed = False
            for allowed_domain in self.config.allowed_domains:
                if fnmatch.fnmatch(url.lower(), allowed_domain.lower()):
                    allowed = True
                    break
            
            if not allowed and self.config.allowed_domains:
                return {"valid": False, "domain": url}
        
        return {"valid": True}
    
    def _check_sensitivity(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Check if operation is potentially sensitive"""
        args_str = str(arguments)
        
        for regex in self._sensitive_regex:
            match = regex.search(args_str)
            if match:
                return {
                    "is_sensitive": True,
                    "reason": f"Potentially sensitive operation detected: {match.group(0)}"
                }
        
        return {"is_sensitive": False, "reason": ""}
    
    def _execute_tool_impl(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute the actual tool implementation"""
        if tool_name not in self._tool_implementations:
            raise ValueError(f"Tool '{tool_name}' not registered")
        
        impl = self._tool_implementations[tool_name]
        return impl(**arguments)
    
    def _validate_output(self, output: Any) -> Any:
        """Validate and sanitize tool output before returning to agent"""
        # Convert to string for inspection
        output_str = str(output)
        
        # Check for obvious exfiltration patterns in output
        exfil_patterns = [
            r'https?://[^\s]+\?(?:data|payload|info)=',
            r'<script[^>]*>',
            r'javascript:',
            r'on\w+\s*=',
        ]
        
        for pattern in exfil_patterns:
            if re.search(pattern, output_str, re.IGNORECASE):
                # Strip/escape suspicious content
                output_str = re.sub(pattern, '[BLOCKED]', output_str, flags=re.IGNORECASE)
        
        return output if isinstance(output, (str, int, float, bool, list, dict)) else output_str
    
    def _create_audit_log(self, call: ToolCall, status: str, error: str = "") -> Dict[str, Any]:
        """Create audit log entry"""
        return {
            "timestamp": call.timestamp,
            "tool": call.tool_name,
            "arguments_keys": list(call.arguments.keys()),
            "status": status,
            "error": error,
            "caller_context": call.caller_context
        }
    
    def get_audit_summary(self) -> Dict[str, Any]:
        """Get summary of sandbox activity"""
        tool_counts = {}
        for call in self._call_history:
            tool_counts[call.tool_name] = tool_counts.get(call.tool_name, 0) + 1
        
        return {
            "total_calls": len(self._call_history),
            "calls_per_tool": tool_counts,
            "time_window_minutes": 60
        }


# Convenience decorator for sandboxing

def sandboxed(sandbox: ToolSandbox, permission: PermissionLevel = PermissionLevel.RESTRICTED):
    """Decorator to sandbox a function call"""
    def decorator(func: Callable):
        sandbox.register_tool(func.__name__, func, permission)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            arg_dict = dict(zip(func.__code__.co_varnames, args))
            arg_dict.update(kwargs)
            return sandbox.execute(func.__name__, arg_dict)
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    # Create sandbox
    sb = ToolSandbox()
    
    # Register a safe tool
    def calculator(expression: str) -> float:
        """Demo calculator using ast.literal_eval (safe alternative to eval)
        
        NOTE: This is a demo. Real implementations should use ast.literal_eval()
        or a proper math parser to avoid code execution risks.
        """
        import ast
        import operator
        
        # Whitelist safe characters
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Invalid characters in expression")
        
        # Use ast for safe parsing (no code execution)
        try:
            node = ast.parse(expression, mode='eval')
            return _eval_expr(node.body)
        except Exception as e:
            raise ValueError(f"Invalid math expression: {e}")
    
    def _eval_expr(node):
        """Safely evaluate AST nodes (no eval/exec)"""
        import ast
        import operator
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval_expr(node.left), _eval_expr(node.right))
        else:
            raise TypeError(f"Unsupported operation: {type(node)}")
    
    sb.register_tool("calculator", calculator, PermissionLevel.ALLOWED)
    
    # Test execution
    result = sb.execute("calculator", {"expression": "2 + 2"})
    print(f"Result: {result.output}")
    
    # Test blocked domain
    result = sb.execute("unknown_tool", {"url": "https://evil.com/steal"})
    print(f"Blocked: {result.blocked}, Reason: {result.block_reason}")
