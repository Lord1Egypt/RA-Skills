#!/usr/bin/env python3
"""
Example: Full-featured CLI with Typer + Rich
Demonstrates: commands, options, prompts, tables, progress bars
"""

import typer
from typing import Optional
from typing_extensions import Annotated
from enum import Enum

# from rich.console import Console
# from rich.table import Table
# from rich.progress import track

app = typer.Typer(
    name="devtool",
    help="Developer productivity CLI",
    add_completion=True,
)


class Template(str, Enum):
    default = "default"
    minimal = "minimal"
    full = "full"
    api = "api"


# ─── Init command ──────────────────────────────────────────────────────────────


@app.command()
def init(
    name: str = typer.Argument(..., help="Project name (lowercase, no spaces)"),
    template: Annotated[Template, typer.Option("--template", "-t", help="Project template")] = Template.default,
    git: Annotated[bool, typer.Option("--git/--no-git", help="Initialize git repo")] = True,
    directory: Annotated[str, typer.Option("--dir", "-d", help="Output directory")] = ".",
):
    """Initialize a new project."""
    # Validate name
    if not name.replace("-", "").isalnum() or name != name.lower():
        typer.echo(f"Error: Name must be lowercase alphanumeric with hyphens.", err=True)
        raise typer.Exit(2)

    typer.echo(f"Creating project: {name}")
    typer.echo(f"  Template: {template.value}")
    typer.echo(f"  Directory: {directory}")
    typer.echo(f"  Git: {'yes' if git else 'no'}")

    # ... scaffold logic ...

    typer.echo("")
    typer.secho("Project created!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"\nNext steps:")
    typer.echo(f"  cd {name}")
    typer.echo(f"  pip install -r requirements.txt")


# ─── Build command ─────────────────────────────────────────────────────────────


@app.command()
def build(
    watch: Annotated[bool, typer.Option("--watch", "-w", help="Watch for changes")] = False,
    outdir: Annotated[str, typer.Option("--outdir", "-o", help="Output directory")] = "dist",
    minify: Annotated[bool, typer.Option("--minify", help="Minify output")] = False,
):
    """Build the project."""
    typer.echo(f"Building to {outdir}...")

    # with Progress() as progress:
    #     task = progress.add_task("Building...", total=100)
    #     for i in range(100):
    #         progress.update(task, advance=1)

    typer.secho("Build complete!", fg=typer.colors.GREEN)


# ─── List command ──────────────────────────────────────────────────────────────


@app.command("list")
def list_projects(
    json_output: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", "-q", help="Only output names")] = False,
):
    """List all projects."""
    import json as json_mod

    projects = [
        {"name": "web-app", "version": "2.1.0", "status": "active"},
        {"name": "api-server", "version": "1.5.3", "status": "active"},
        {"name": "legacy-tool", "version": "0.9.0", "status": "archived"},
    ]

    if json_output:
        typer.echo(json_mod.dumps(projects, indent=2))
        return

    if quiet:
        for p in projects:
            typer.echo(p["name"])
        return

    # Table output
    typer.echo(f"{'NAME':<14} {'VERSION':<9} STATUS")
    typer.echo(f"{'────':<14} {'───────':<9} ──────")
    for p in projects:
        status_color = typer.colors.GREEN if p["status"] == "active" else typer.colors.YELLOW
        typer.echo(f"{p['name']:<14} {p['version']:<9} ", nl=False)
        typer.secho(p["status"], fg=status_color)

    typer.echo(f"\n{len(projects)} projects total")


# ─── Config subcommands ───────────────────────────────────────────────────────

config_app = typer.Typer(help="Manage configuration")
app.add_typer(config_app, name="config")


@config_app.command("get")
def config_get(key: str = typer.Argument(..., help="Config key")):
    """Get a configuration value."""
    config = {"editor": "code", "theme": "dark", "lang": "en"}
    if key not in config:
        typer.echo(f"Unknown key: {key}", err=True)
        typer.echo(f"Available: {', '.join(config.keys())}", err=True)
        raise typer.Exit(1)
    typer.echo(config[key])


@config_app.command("set")
def config_set(
    key: str = typer.Argument(..., help="Config key"),
    value: str = typer.Argument(..., help="Config value"),
):
    """Set a configuration value."""
    typer.echo(f"Set {key} = {value}")


# ─── Interactive command ───────────────────────────────────────────────────────


@app.command()
def setup():
    """Interactive project setup wizard."""
    name = typer.prompt("Project name")
    template = typer.prompt("Template", default="default")
    use_git = typer.confirm("Initialize git?", default=True)

    typer.echo(f"\nCreating: {name} (template: {template}, git: {use_git})")


# ─── Version callback ─────────────────────────────────────────────────────────


def version_callback(value: bool):
    if value:
        typer.echo("devtool v1.0.0")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", callback=version_callback, is_eager=True),
    ] = None,
):
    """Developer productivity CLI."""
    pass


if __name__ == "__main__":
    app()
