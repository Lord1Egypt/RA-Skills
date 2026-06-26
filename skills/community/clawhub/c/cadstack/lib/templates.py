"""Template rendering module for CADStack.

Provides Jinja2-based template rendering for parametric CAD parts.
Templates are stored in the templates/ directory and can be rendered
with custom parameters.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

from .exceptions import TemplateNotFoundError, TemplateRenderError

logger = logging.getLogger(__name__)

# Template directories
TEMPLATE_DIRS = [
    Path(__file__).parent.parent / "templates",
    Path.home() / ".claude" / "skills" / "cadstack" / "templates",
]


def get_template_env(template_dir: Optional[Path] = None) -> Environment:
    """Create a Jinja2 environment for template rendering.

    Args:
        template_dir: Optional custom template directory

    Returns:
        Configured Jinja2 Environment
    """
    search_paths = []
    if template_dir:
        search_paths.append(str(template_dir))
    search_paths.extend(str(d) for d in TEMPLATE_DIRS if d.exists())

    if not search_paths:
        search_paths = ["."]  # Fallback

    return Environment(
        loader=FileSystemLoader(search_paths),
        autoescape=False,  # CAD scripts don't need HTML escaping
        trim_blocks=True,
        lstrip_blocks=True,
    )


def list_templates(platform: Optional[str] = None) -> list:
    """List available templates.

    Args:
        platform: Filter by platform (cadquery, freecad, etc.)

    Returns:
        List of template paths
    """
    templates = []
    for template_dir in TEMPLATE_DIRS:
        if not template_dir.exists():
            continue

        if platform:
            platform_dir = template_dir / platform
            if platform_dir.exists():
                templates.extend(str(p.relative_to(template_dir))
                                for p in platform_dir.glob("**/*.py"))
        else:
            templates.extend(str(p.relative_to(template_dir))
                            for p in template_dir.glob("**/*.py"))

    return sorted(set(templates))


def render_template(template_name: str, context: Dict[str, Any],
                   platform: Optional[str] = None) -> str:
    """Render a template with the given context.

    Args:
        template_name: Template filename (e.g., "cadquery/basic_box.py")
        context: Dictionary of variables to pass to template
        platform: Platform subdirectory to search

    Returns:
        Rendered template string

    Raises:
        TemplateNotFoundError: If template doesn't exist
        TemplateRenderError: If rendering fails
    """
    logger.debug(f"Rendering template: {template_name}")

    # Build search path
    search_paths = []
    for base_dir in TEMPLATE_DIRS:
        if base_dir.exists():
            search_paths.append(str(base_dir))

    if not search_paths:
        raise TemplateNotFoundError(template_name, [])

    try:
        env = Environment(
            loader=FileSystemLoader(search_paths),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Resolve template path
        if platform:
            # Try platform-specific path first
            platform_path = f"{platform}/{template_name}"
            try:
                template = env.get_template(platform_path)
                return template.render(**context)
            except Exception:
                pass  # Fall back to generic path

        template = env.get_template(template_name)
        rendered = template.render(**context)

        logger.info(f"Rendered template: {template_name}")
        return rendered

    except TemplateSyntaxError as e:
        logger.error(f"Template syntax error in {template_name}: {e}")
        raise TemplateRenderError(template_name, f"Syntax error at line {e.lineno}: {e.message}")
    except Exception as e:
        if "not found" in str(e).lower():
            raise TemplateNotFoundError(template_name, search_paths)
        logger.error(f"Template render error: {e}")
        raise TemplateRenderError(template_name, str(e))


def render_template_file(template_path: Path, context: Dict[str, Any]) -> str:
    """Render a template from a file path.

    Args:
        template_path: Path to template file
        context: Dictionary of variables to pass to template

    Returns:
        Rendered template string

    Raises:
        TemplateNotFoundError: If template doesn't exist
        TemplateRenderError: If rendering fails
    """
    if not template_path.exists():
        raise TemplateNotFoundError(template_path.name, [str(template_path.parent)])

    try:
        env = Environment(
            loader=FileSystemLoader(str(template_path.parent)),
            autoescape=False,
        )
        template = env.get_template(template_path.name)
        return template.render(**context)
    except TemplateSyntaxError as e:
        raise TemplateRenderError(template_path.name, f"Syntax error: {e}")
    except Exception as e:
        raise TemplateRenderError(template_path.name, str(e))


# =============================================================================
# Template Parameter Validation
# =============================================================================

def get_template_parameters(template_name: str) -> Dict[str, Any]:
    """Extract parameter definitions from a template.

    Looks for parameter comments in the template file.

    Args:
        template_name: Template filename

    Returns:
        Dictionary of parameter names to their default values
    """
    # Find template file
    for template_dir in TEMPLATE_DIRS:
        template_path = template_dir / template_name
        if template_path.exists():
            return _extract_parameters(template_path)

    return {}


def _extract_parameters(template_path: Path) -> Dict[str, Any]:
    """Extract parameters from a template file.

    Looks for patterns like:
        # @param length=100 Length of the box
        length = {{ length }}

    Or:
        length = {{ length|default(100) }}
    """
    import re

    params = {}

    try:
        content = template_path.read_text()

        # Look for @param comments
        param_pattern = r'#\s*@param\s+(\w+)\s*=\s*([^\s]+)'
        for match in re.finditer(param_pattern, content):
            name = match.group(1)
            value_str = match.group(2)

            # Try to parse value
            try:
                if '.' in value_str:
                    params[name] = float(value_str)
                else:
                    params[name] = int(value_str)
            except ValueError:
                params[name] = value_str

        # Look for default filters
        default_pattern = r'\{\{\s*(\w+)\s*\|\s*default\(([^)]+)\)\s*\}\}'
        for match in re.finditer(default_pattern, content):
            name = match.group(1)
            if name not in params:
                value_str = match.group(2).strip('"\'')
                try:
                    if '.' in value_str:
                        params[name] = float(value_str)
                    else:
                        params[name] = int(value_str)
                except ValueError:
                    params[name] = value_str

    except Exception as e:
        logger.warning(f"Error extracting parameters from {template_path}: {e}")

    return params
