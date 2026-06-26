"""Helper utilities for CAD automation."""

import re
import ast
import logging
from pathlib import Path
from typing import Optional, Tuple, List

logger = logging.getLogger(__name__)


def parse_dimension(dim_str: str) -> float:
    """Parse a dimension string to millimeters.

    Supports: mm, cm, m, in, inch, ft, foot
    Returns value in mm.
    """
    dim_str = dim_str.strip().lower()

    # Extract number and unit
    match = re.match(r'^([\d.]+)\s*(mm|cm|m|in|inch|ft|foot)?$', dim_str)
    if not match:
        raise ValueError(f"Invalid dimension format: {dim_str}")

    value = float(match.group(1))
    unit = match.group(2) or 'mm'

    # Convert to mm
    conversions = {
        'mm': 1.0,
        'cm': 10.0,
        'm': 1000.0,
        'in': 25.4,
        'inch': 25.4,
        'ft': 304.8,
        'foot': 304.8,
    }

    return value * conversions.get(unit, 1.0)


def format_filename(name: str, extension: str = ".step") -> str:
    """Create a safe filename from a description."""
    # Replace spaces and special chars
    safe_name = re.sub(r'[^\w\s-]', '', name)
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    safe_name = safe_name.strip('_').lower()

    if not safe_name:
        safe_name = "cad_part"

    return f"{safe_name}{extension}"


def parse_color(color_str: str) -> Tuple[float, float, float]:
    """Parse a color string to RGB tuple (0-1 range).

    Supports: hex (#RRGGBB), named colors, rgb(r,g,b)
    """
    color_str = color_str.strip().lower()

    # Named colors
    named_colors = {
        'red': (1.0, 0.0, 0.0),
        'green': (0.0, 1.0, 0.0),
        'blue': (0.0, 0.0, 1.0),
        'yellow': (1.0, 1.0, 0.0),
        'cyan': (0.0, 1.0, 1.0),
        'magenta': (1.0, 0.0, 1.0),
        'white': (1.0, 1.0, 1.0),
        'black': (0.0, 0.0, 0.0),
        'gray': (0.5, 0.5, 0.5),
        'grey': (0.5, 0.5, 0.5),
        'orange': (1.0, 0.5, 0.0),
    }

    if color_str in named_colors:
        return named_colors[color_str]

    # Hex color
    if color_str.startswith('#'):
        hex_val = color_str[1:]
        if len(hex_val) == 6:
            r = int(hex_val[0:2], 16) / 255.0
            g = int(hex_val[2:4], 16) / 255.0
            b = int(hex_val[4:6], 16) / 255.0
            return (r, g, b)

    # RGB function
    match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color_str)
    if match:
        r = int(match.group(1)) / 255.0
        g = int(match.group(2)) / 255.0
        b = int(match.group(3)) / 255.0
        return (r, g, b)

    raise ValueError(f"Invalid color format: {color_str}")


def ensure_output_dir(base_dir: Path) -> Path:
    """Ensure output directory exists and return path."""
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_default_output_path(name: str, format: str = "step", base_dir: Optional[Path] = None) -> Path:
    """Get default output path for a CAD file."""
    if base_dir is None:
        base_dir = Path.home() / ".claude" / "skills" / "cadstack"

    output_dir = ensure_output_dir(base_dir)
    filename = format_filename(name, f".{format}")
    return output_dir / filename


class CADScriptValidator:
    """Validates CAD scripts for security.

    Uses both regex pattern matching and AST analysis to detect
    potentially dangerous code patterns.
    """

    # Patterns that are ALWAYS dangerous in exec() context
    DANGEROUS_PATTERNS = [
        # System command execution
        (r'os\.system\s*\(', "os.system - system command execution"),
        (r'subprocess\.(call|run|Popen|check_output)\s*\(', "subprocess - command execution"),
        (r'commands\.', "commands module (deprecated but dangerous)"),

        # Code execution
        (r'\beval\s*\(', "eval - arbitrary code execution"),
        (r'\bexec\s*\(', "exec - arbitrary code execution"),
        (r'compile\s*\(', "compile - code compilation"),

        # Import manipulation
        (r'__import__\s*\(', "__import__ - dynamic import"),
        (r'importlib\.', "importlib - dynamic import"),
        (r'imp\.', "imp module - dynamic import"),

        # File system access
        (r'\bopen\s*\([^)]*[\'"]w[\'"]', "open() in write mode - file modification"),
        (r'\bopen\s*\([^)]*[\'"]a[\'"]', "open() in append mode - file modification"),
        (r'shutil\.(rmtree|copy|move)', "shutil - file system operations"),
        (r'os\.(remove|unlink|rmdir|rename|makedirs)', "os file operations"),
        (r'pathlib\.Path\.(write|unlink|rmdir)', "pathlib file modifications"),

        # Dangerous builtins access
        (r'__builtins__', "__builtins__ access"),
        (r'globals\s*\(\)', "globals() - namespace access"),
        (r'locals\s*\(\)', "locals() - namespace access"),
        (r'vars\s*\(\)', "vars() - namespace access"),

        # Network access
        (r'socket\.', "socket - network access"),
        (r'urllib\.', "urllib - network access"),
        (r'requests\.', "requests - network access"),
        (r'httpx\.', "httpx - network access"),

        # Dangerous decorators/attributes
        (r'@property', "property decorator (may hide dangerous code)"),

        # Deletion
        (r'\bdel\s+', "del statement"),
    ]

    # Patterns that are suspicious but may be legitimate
    SUSPICIOUS_PATTERNS = [
        (r'getattr\s*\(', "getattr - dynamic attribute access"),
        (r'setattr\s*\(', "setattr - dynamic attribute modification"),
        (r'hasattr\s*\(', "hasattr - attribute probing"),
        (r'delattr\s*\(', "delattr - attribute deletion"),
    ]

    @classmethod
    def validate(cls, script: str) -> Tuple[bool, List[str]]:
        """Validate a script for dangerous patterns (legacy - warns only).

        Returns: (is_safe, list of warnings)
        """
        warnings = []

        for pattern, description in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, script):
                warnings.append(f"Potentially dangerous pattern: {description}")

        return len(warnings) == 0, warnings

    @classmethod
    def validate_strict(cls, script: str) -> Tuple[bool, List[str]]:
        """Validate a script strictly - returns errors, not warnings.

        This method BLOCKS execution on dangerous patterns.
        Used by the CLI executor for security.

        Returns: (is_safe, list of errors)
        """
        errors = []

        # Regex-based pattern matching
        for pattern, description in cls.DANGEROUS_PATTERNS:
            matches = re.findall(pattern, script)
            if matches:
                errors.append(f"Blocked pattern: {description}")

        # AST-based analysis for deeper inspection
        try:
            tree = ast.parse(script)
            ast_errors = cls._analyze_ast(tree)
            errors.extend(ast_errors)
        except SyntaxError as e:
            errors.append(f"Script has syntax error: {e}")

        # Log blocked attempts
        if errors:
            logger.warning(f"Script validation blocked: {len(errors)} issues found")

        return len(errors) == 0, errors

    @classmethod
    def _analyze_ast(cls, tree: ast.AST) -> List[str]:
        """Analyze AST for dangerous patterns that regex might miss."""
        errors = []

        class DangerousNodeVisitor(ast.NodeVisitor):
            def visit_Import(self, node):
                for alias in node.names:
                    # Block certain modules
                    blocked_modules = {
                        'os', 'subprocess', 'sys', 'shutil',
                        'socket', 'pickle', 'marshal', 'imp',
                        'importlib', 'ctypes', 'multiprocessing',
                    }
                    if alias.name.split('.')[0] in blocked_modules:
                        errors.append(f"Import of blocked module: {alias.name}")
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                if node.module:
                    blocked_modules = {
                        'os', 'subprocess', 'sys', 'shutil',
                        'socket', 'pickle', 'marshal', 'imp',
                        'importlib', 'ctypes', 'multiprocessing',
                    }
                    if node.module.split('.')[0] in blocked_modules:
                        errors.append(f"Import from blocked module: {node.module}")
                self.generic_visit(node)

            def visit_Call(self, node):
                # Check for dangerous function calls
                if isinstance(node.func, ast.Name):
                    dangerous_funcs = {
                        'eval', 'exec', 'compile', '__import__',
                        'globals', 'locals', 'vars', 'open',
                    }
                    if node.func.id in dangerous_funcs:
                        errors.append(f"Call to dangerous function: {node.func.id}()")
                self.generic_visit(node)

        visitor = DangerousNodeVisitor()
        visitor.visit(tree)
        return errors

    @classmethod
    def sanitize_script(cls, script: str) -> str:
        """Remove or escape dangerous patterns (basic sanitization).

        WARNING: This is not foolproof. For production use, consider
        using a proper sandboxing solution like RestrictedPython.
        """
        # This is intentionally minimal - the recommended approach
        # is to reject dangerous scripts, not try to sanitize them
        return script


# =============================================================================
# Template Helpers
# =============================================================================

def render_template(template_path: Path, context: dict) -> str:
    """Render a Jinja2 template with the given context.

    Args:
        template_path: Path to the template file
        context: Dictionary of variables to pass to the template

    Returns:
        Rendered template string

    Raises:
        TemplateNotFoundError: If template doesn't exist
        TemplateRenderError: If rendering fails
    """
    from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
    from exceptions import TemplateNotFoundError, TemplateRenderError

    if not template_path.exists():
        raise TemplateNotFoundError(
            template_path.name,
            [str(template_path.parent)]
        )

    try:
        env = Environment(
            loader=FileSystemLoader(str(template_path.parent)),
            autoescape=False,  # CAD scripts don't need HTML escaping
        )
        template = env.get_template(template_path.name)
        return template.render(**context)
    except TemplateSyntaxError as e:
        raise TemplateRenderError(template_path.name, f"Syntax error: {e}")
    except Exception as e:
        raise TemplateRenderError(template_path.name, str(e))
