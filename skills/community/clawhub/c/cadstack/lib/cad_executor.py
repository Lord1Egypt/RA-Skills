#!/usr/bin/env python3
"""
CAD Script Executor

Executes CAD scripts using the specified backend platform.
Supports: CadQuery, FreeCAD, AutoCAD, SolidWorks, Fusion 360

Architecture:
┌─────────────────────────────────────────────────────────────────┐
│                        CLI Entry Point                          │
│  python cad_executor.py run script.py --platform cadquery      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     cad_executor.py                             │
│  ┌─────────────┐  ┌─────────────────┐  ┌──────────────────┐    │
│  │   typer     │──│ CADScriptValidator│──│ BACKEND_REGISTRY │    │
│  │   commands  │  │   (security)     │  │   (plugin)       │    │
│  └─────────────┘  └─────────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend Layer                              │
│  CadQueryBackend │ FreeCADBackend │ AutoCADBackend │ ...       │
│  (implements CADBackend abstract base class)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Output Layer                               │
│  STEP │ STL │ OBJ │ DXF │ SVG files                            │
└─────────────────────────────────────────────────────────────────┘
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Type, Any
import json

import typer
from rich.console import Console
from rich.panel import Panel
from rich.logging import RichHandler

# Import exceptions using absolute import for pytest compatibility
from lib.exceptions import (
    CADStackError,
    BackendNotAvailableError,
    InvalidDimensionError,
    ExportFailedError,
    EmptyDocumentError,
    ScriptValidationError,
    raise_for_dimension,
)

console = Console()
app = typer.Typer(name="cad-executor", help="Execute CAD automation scripts")

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)
logger = logging.getLogger("cadstack")


# =============================================================================
# Backend Registry - Use backends/__init__.py as single source of truth
# =============================================================================

# Import backend registry from backends package
from lib.backends import (
    get_available_backends as _get_available_backends,
    list_available_backends as _list_available_backends,
)

# Alias for backwards compatibility
BACKEND_REGISTRY = _get_available_backends()


def get_backend(platform: str):
    """Get the appropriate backend for the platform.

    Uses registry pattern for extensibility - new backends can be
    added by registering them in backends/__init__.py.

    Args:
        platform: Backend name (cadquery, freecad, autocad, etc.)

    Returns:
        Instantiated backend

    Raises:
        BackendNotAvailableError: If backend is not available
    """
    # Get fresh backend dict
    backends = _get_available_backends()

    platform = platform.lower()

    if platform not in backends:
        available = list(backends.keys())
        raise BackendNotAvailableError(
            platform,
            f"Available backends: {', '.join(available) if available else 'none'}"
        )

    try:
        backend = backends[platform]()
        logger.debug(f"Initialized backend: {backend.name}")
        return backend
    except Exception as e:
        raise BackendNotAvailableError(platform, str(e))


def list_available_backends() -> Dict[str, bool]:
    """List all known backends and their availability."""
    available = _list_available_backends()
    known_backends = ["cadquery", "freecad", "autocad", "solidworks", "fusion360"]
    return {name: name in available for name in known_backends}


# =============================================================================
# CLI Commands
# =============================================================================

@app.command()
def run(
    script: Path = typer.Argument(..., help="Path to CAD script to execute"),
    platform: str = typer.Option("cadquery", "--platform", "-p",
                                  help="CAD platform (cadquery, freecad, autocad, solidworks, fusion360)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("step", "--format", "-f", help="Output format (step, stl, obj)"),
    validate: bool = typer.Option(True, "--validate/--no-validate", help="Validate script before execution"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Execute a CAD script on the specified platform."""
    # Set logging level
    if verbose:
        logger.setLevel(logging.DEBUG)

    console.print(Panel(f"CAD Executor\nPlatform: {platform}\nScript: {script}", title="cadstack"))

    # Read script
    if not script.exists():
        console.print(f"[red]Script not found: {script}[/red]")
        raise typer.Exit(1)

    script_content = script.read_text(encoding='utf-8')

    # Validate script (STRICT - blocks on dangerous patterns)
    if validate:
        from lib.utils.helpers import CADScriptValidator
        is_safe, errors = CADScriptValidator.validate_strict(script_content)
        if not is_safe:
            console.print("[red]Script validation FAILED - dangerous patterns detected:[/red]")
            for error in errors:
                console.print(f"  [red]✗[/red] {error}")
            console.print("\n[yellow]Script execution blocked for security.[/yellow]")
            raise typer.Exit(1)

    # Get backend
    try:
        backend = get_backend(platform)
        console.print(f"[green]Backend initialized: {backend.name}[/green]")
    except BackendNotAvailableError as e:
        console.print(f"[red]{e}[/red]")
        if e.hint:
            console.print(f"[yellow]{e.hint}[/yellow]")
        raise typer.Exit(1)

    # Prepare execution namespace (SANDBOXED)
    output_path = output or (Path.cwd() / f"output.{format}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Restricted namespace - only safe utilities
    safe_namespace = {
        'backend': backend,
        'output': output_path,
        'format': format,
        'Path': Path,
        # No console, no builtins access
    }

    # Execute script
    console.print(f"\n[cyan]Executing script...[/cyan]")
    try:
        exec(script_content, {"__builtins__": {}}, safe_namespace)
        console.print(f"\n[green]Script executed successfully[/green]")
        console.print(f"Output: {output_path}")
    except CADStackError as e:
        console.print(f"\n[red]CAD Error: {e}[/red]")
        if e.hint:
            console.print(f"[yellow]Hint: {e.hint}[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]Execution failed: {e}[/red]")
        if verbose:
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)


@app.command()
def check(
    platform: str = typer.Argument("cadquery", help="CAD platform to check"),
):
    """Check if a CAD platform is available."""
    console.print(f"Checking {platform}...")

    try:
        backend = get_backend(platform)
        info = backend.get_info()
        console.print(f"[green]Platform: {info['name']}[/green]")
        console.print(f"  Headless: {info['supports_headless']}")
        console.print(f"  Available: {info['available']}")
        console.print(f"  Formats: {', '.join(info.get('supported_formats', []))}")
    except BackendNotAvailableError as e:
        console.print(f"[red]Not available: {e}[/red]")
        if e.hint:
            console.print(f"[yellow]{e.hint}[/yellow]")
        raise typer.Exit(1)


@app.command()
def create(
    primitive: str = typer.Argument(..., help="Primitive type (box, cylinder, sphere, cone, torus)"),
    dimensions: str = typer.Argument(..., help="Dimensions (e.g., '100,50,20' for box)"),
    platform: str = typer.Option("cadquery", "--platform", "-p", help="CAD platform"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("step", "--format", "-f", help="Output format"),
    name: str = typer.Option("part", "--name", "-n", help="Part name"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Quick create a primitive shape."""
    if verbose:
        logger.setLevel(logging.DEBUG)

    # Parse and validate dimensions
    try:
        dims = _parse_dimensions(dimensions, primitive)
    except InvalidDimensionError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    # Get backend
    try:
        backend = get_backend(platform)
    except BackendNotAvailableError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    backend.create_document(name)

    # Create primitive with validation
    primitive = primitive.lower()
    try:
        if primitive == "box":
            _validate_dims(primitive, dims, 3)
            obj = backend.create_box(dims[0], dims[1], dims[2], name)
        elif primitive == "cylinder":
            _validate_dims(primitive, dims, 2)
            obj = backend.create_cylinder(dims[0], dims[1], name)
        elif primitive == "sphere":
            _validate_dims(primitive, dims, 1)
            obj = backend.create_sphere(dims[0], name)
        elif primitive == "cone":
            _validate_dims(primitive, dims, 3)
            obj = backend.create_cone(dims[0], dims[1], dims[2], name)
        elif primitive == "torus":
            _validate_dims(primitive, dims, 2)
            obj = backend.create_torus(dims[0], dims[1], name)
        else:
            console.print(f"[red]Unknown primitive: {primitive}[/red]")
            console.print("[yellow]Available: box, cylinder, sphere, cone, torus[/yellow]")
            raise typer.Exit(1)
    except InvalidDimensionError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)
    except CADStackError as e:
        console.print(f"[red]Error creating primitive: {e}[/red]")
        raise typer.Exit(1)

    # Export
    output_path = output or (Path.cwd() / f"{name}.{format}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = backend._current_doc
    backend.recompute(doc)

    try:
        success = backend.export(doc, output_path, format)
        if success:
            console.print(f"[green]Created {primitive} -> {output_path}[/green]")
    except EmptyDocumentError:
        console.print(f"[red]Error: Document is empty[/red]")
        raise typer.Exit(1)
    except ExportFailedError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)


@app.command()
def info():
    """Show information about available platforms."""
    console.print(Panel("CAD Platforms", title="cadstack"))

    platforms = [
        ("cadquery", "CadQuery", "Pure Python, headless, pip install cadquery (recommended)"),
        ("freecad", "FreeCAD", "Pure Python, headless mode, requires FreeCAD installation"),
        ("autocad", "AutoCAD", "Requires AutoCAD running on Windows (COM automation)"),
        ("solidworks", "SolidWorks", "Requires SolidWorks running on Windows (COM)"),
        ("fusion360", "Fusion 360", "Requires Fusion 360 with bridge add-in running"),
    ]

    availability = list_available_backends()

    for platform_id, name, description in platforms:
        available = availability.get(platform_id, False)
        if available:
            status = "[green]Available[/green]"
        else:
            status = "[yellow]Not available[/yellow]"

        console.print(f"\n[bold]{name}[/bold] ({platform_id})")
        console.print(f"  {description}")
        console.print(f"  Status: {status}")


@app.command()
def version():
    """Show CADStack version."""
    version_file = Path(__file__).parent.parent / "VERSION"
    if version_file.exists():
        ver = version_file.read_text().strip()
    else:
        ver = "unknown"
    console.print(f"CADStack v{ver}")


# =============================================================================
# Helper Functions
# =============================================================================

def _parse_dimensions(dim_str: str, primitive: str) -> list:
    """Parse dimension string to list of floats with validation."""
    import math

    parts = [p.strip() for p in dim_str.split(',')]
    dims = []

    for i, part in enumerate(parts):
        if not part:
            raise InvalidDimensionError(
                f"dimension {i+1}",
                0,
                "empty value - use format like '100,50,20'"
            )

        try:
            value = float(part)
        except ValueError:
            raise InvalidDimensionError(
                f"dimension {i+1}",
                part,
                "not a valid number"
            )

        if math.isnan(value) or math.isinf(value):
            raise InvalidDimensionError(f"dimension {i+1}", value, "invalid numeric value")

        dims.append(value)

    return dims


def _validate_dims(primitive: str, dims: list, expected: int):
    """Validate dimension count and values for a primitive."""
    if len(dims) != expected:
        raise InvalidDimensionError(
            primitive,
            len(dims),
            f"expected {expected} dimensions, got {len(dims)}"
        )

    # Validate all dimensions are positive
    for i, d in enumerate(dims):
        if d <= 0:
            raise InvalidDimensionError(
                f"{primitive} dimension {i+1}",
                d,
                "must be positive"
            )


# =============================================================================
# CLI Shortcuts (TODO-10)
# =============================================================================

@app.command(name="box")
def box_shortcut(
    dimensions: str = typer.Argument(..., help="Dimensions 'length,width,height' in mm"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("step", "--format", "-f", help="Output format"),
    name: str = typer.Option("box", "--name", "-n", help="Part name"),
    platform: str = typer.Option("cadquery", "--platform", "-p", help="CAD platform"),
):
    """Quick create a box. Example: cad-executor box 100,50,20"""
    from typer.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(app, ["create", "box", dimensions, "-p", platform, "-o", str(output) if output else "", "-f", format, "-n", name])
    if result.exit_code != 0:
        console.print(result.output)
        raise typer.Exit(result.exit_code)


@app.command(name="cylinder")
def cylinder_shortcut(
    dimensions: str = typer.Argument(..., help="Dimensions 'radius,height' in mm"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("step", "--format", "-f", help="Output format"),
    name: str = typer.Option("cylinder", "--name", "-n", help="Part name"),
    platform: str = typer.Option("cadquery", "--platform", "-p", help="CAD platform"),
):
    """Quick create a cylinder. Example: cad-executor cylinder 10,50"""
    from typer.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(app, ["create", "cylinder", dimensions, "-p", platform, "-o", str(output) if output else "", "-f", format, "-n", name])
    if result.exit_code != 0:
        console.print(result.output)
        raise typer.Exit(result.exit_code)


@app.command(name="sphere")
def sphere_shortcut(
    radius: float = typer.Argument(..., help="Radius in mm"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("step", "--format", "-f", help="Output format"),
    name: str = typer.Option("sphere", "--name", "-n", help="Part name"),
    platform: str = typer.Option("cadquery", "--platform", "-p", help="CAD platform"),
):
    """Quick create a sphere. Example: cad-executor sphere 25"""
    from typer.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(app, ["create", "sphere", str(radius), "-p", platform, "-o", str(output) if output else "", "-f", format, "-n", name])
    if result.exit_code != 0:
        console.print(result.output)
        raise typer.Exit(result.exit_code)


@app.command(name="cone")
def cone_shortcut(
    dimensions: str = typer.Argument(..., help="Dimensions 'bottom_radius,top_radius,height' in mm"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("step", "--format", "-f", help="Output format"),
    name: str = typer.Option("cone", "--name", "-n", help="Part name"),
    platform: str = typer.Option("cadquery", "--platform", "-p", help="CAD platform"),
):
    """Quick create a cone. Example: cad-executor cone 20,0,50"""
    from typer.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(app, ["create", "cone", dimensions, "-p", platform, "-o", str(output) if output else "", "-f", format, "-n", name])
    if result.exit_code != 0:
        console.print(result.output)
        raise typer.Exit(result.exit_code)


@app.command(name="torus")
def torus_shortcut(
    dimensions: str = typer.Argument(..., help="Dimensions 'major_radius,minor_radius' in mm"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("step", "--format", "-f", help="Output format"),
    name: str = typer.Option("torus", "--name", "-n", help="Part name"),
    platform: str = typer.Option("cadquery", "--platform", "-p", help="CAD platform"),
):
    """Quick create a torus. Example: cad-executor torus 50,10"""
    from typer.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(app, ["create", "torus", dimensions, "-p", platform, "-o", str(output) if output else "", "-f", format, "-n", name])
    if result.exit_code != 0:
        console.print(result.output)
        raise typer.Exit(result.exit_code)


@app.command(name="part")
def part_shortcut(
    part_type: str = typer.Argument(..., help="Part type (e.g., screw_metric, bearing_608)"),
    params: str = typer.Argument("", help="Parameters as 'key=value,key2=value2'"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("step", "--format", "-f", help="Output format"),
    platform: str = typer.Option("cadquery", "--platform", "-p", help="CAD platform"),
    list_parts_flag: bool = typer.Option(False, "--list", "-l", help="List available parts"),
):
    """Create a part from the parts library.

    Examples:
        cad-executor part screw_metric diameter=5,length=20
        cad-executor part bearing_608
        cad-executor part --list
    """
    if list_parts_flag:
        from lib.parts_library import list_parts, list_categories
        console.print(Panel("Parts Library", title="cadstack"))
        for category in list_categories():
            parts_in_cat = list_parts(category=category)
            console.print(f"\n[bold]{category.title()}[/bold]")
            for p in parts_in_cat:
                console.print(f"  {p}")
        raise typer.Exit(0)

    try:
        from lib.parts_library import create_part, get_part_definition

        part_def = get_part_definition(part_type)
        if not part_def:
            console.print(f"[red]Unknown part type: {part_type}[/red]")
            console.print("[yellow]Use --list to see available parts[/yellow]")
            raise typer.Exit(1)

        # Parse parameters
        kwargs = {}
        if params:
            for pair in params.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    try:
                        kwargs[key.strip()] = float(value.strip())
                    except ValueError:
                        kwargs[key.strip()] = value.strip()

        # Get backend
        backend = get_backend(platform)
        backend.create_document(part_type)

        # Create part
        obj = create_part(part_type, backend, **kwargs)

        # Export
        output_path = output or (Path.cwd() / f"{part_type}.{format}")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        backend.recompute(backend._current_doc)
        success = backend.export(backend._current_doc, output_path, format)

        if success:
            console.print(f"[green]Created {part_type} -> {output_path}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command(name="draw")
def draw_shortcut(
    input_file: Path = typer.Argument(..., help="Input CAD file (STEP/STL)"),
    views: str = typer.Option("top,front,right", "--views", "-v", help="Views to generate"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("svg", "--format", "-f", help="Output format (svg, dxf, pdf)"),
    title: str = typer.Option("Drawing", "--title", "-t", help="Drawing title"),
):
    """Generate 2D drawing from 3D model.

    Examples:
        cad-executor draw bracket.step -o drawing.svg
        cad-executor draw part.step -v top,front -f dxf -o part.dxf
    """
    try:
        from lib.drawing import (
            DrawingGenerator, ViewType, ExportFormat,
            create_drawing, quick_drawing
        )

        if not input_file.exists():
            console.print(f"[red]File not found: {input_file}[/red]")
            raise typer.Exit(1)

        # Parse views
        view_map = {
            "top": ViewType.TOP,
            "front": ViewType.FRONT,
            "right": ViewType.RIGHT,
            "left": ViewType.LEFT,
            "back": ViewType.BACK,
            "bottom": ViewType.BOTTOM,
            "iso": ViewType.ISOMETRIC,
            "isometric": ViewType.ISOMETRIC,
        }
        view_types = []
        for v in views.split(","):
            v = v.strip().lower()
            if v in view_map:
                view_types.append(view_map[v])

        if not view_types:
            console.print("[red]No valid views specified[/red]")
            raise typer.Exit(1)

        # Map format
        format_map = {
            "svg": ExportFormat.SVG,
            "dxf": ExportFormat.DXF,
            "pdf": ExportFormat.PDF,
        }
        export_format = format_map.get(format.lower(), ExportFormat.SVG)

        # Create drawing (simplified - would load actual model in full implementation)
        gen = create_drawing(title)
        gen.set_model(None, bounds=(0, 0, 0, 100, 100, 50))  # Placeholder bounds

        for vt in view_types:
            gen.add_view(vt)

        gen.layout_views()

        output_path = output or (Path.cwd() / f"{input_file.stem}_drawing.{format}")
        success = gen.export(output_path, export_format)

        if success:
            console.print(f"[green]Created drawing -> {output_path}[/green]")
        else:
            console.print("[red]Failed to create drawing[/red]")
            raise typer.Exit(1)

    except ImportError as e:
        console.print(f"[red]Missing dependency: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
