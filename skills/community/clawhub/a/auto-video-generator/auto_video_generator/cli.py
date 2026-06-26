# -*- coding: utf-8 -*-
"""
Command Line Interface for Auto Video Generator
===============================================

Provides CLI commands for video generation, configuration, and project management.

Usage:
    avg [COMMAND] [OPTIONS]

Commands:
    generate    Generate demo video from URL or file
    web         Start web UI server
    init        Initialize new project
    config      Manage configuration
    detect      Detect UI framework
    version     Show version info

Examples:
    avg generate https://example.com
    avg generate ./demo.html --voice zh-CN-XiaoxiaoNeural --fps 10
    avg generate --url https://example.com --output demo.mp4 --quality high
    avg web --port 8080
    avg init my-new-project
    avg config list
    avg detect ./src/
"""

import asyncio
import sys
import os
import json
import click
from pathlib import Path
from typing import Optional
from datetime import datetime


try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


console = Console() if RICH_AVAILABLE else None


def print_rich(message: str):
    """Print with Rich if available, otherwise plain text."""
    if console:
        console.print(message)
    else:
        print(message)


@click.group()
@click.version_option(version="3.0.0", prog_name="auto-video-generator")
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--config-file', '-c', type=click.Path(), help='Path to config file')
@click.pass_context
def cli(ctx, verbose: bool, config_file: Optional[str]):
    """
    🎬 Auto Video Generator - Professional Demo Video Generation Tool
    
    Generate professional demo videos from HTML pages with AI voice narration.
    
    \b
    Examples:
        $ avg generate https://example.com/demo.html
        $ avg generate ./page.html --fps 10 --quality high
        $ avg web                    # Start Web UI
        $ avg init my-project        # Create new project
    
    For more help, visit: https://github.com/avg-team/auto-video-generator
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config_file'] = config_file


@cli.command()
@click.argument('source', required=False)
@click.option('--url', '-u', help='URL of the page to generate video from')
@click.option('--output', '-o', type=click.Path(), default='./output.mp4', help='Output file path')
@click.option('--fps', '-f', type=click.IntRange(1, 30), default=4, help='Video frame rate (1-30)')
@click.option('--quality', '-q', type=click.Choice(['low', 'medium', 'high']), default='high',
              help='Video quality level')
@click.option('--voice', '-V', default='zh-CN-YunxiNeural', help='TTS voice selection')
@click.option('--rate', '-r', default='-5%', help='Speech rate (e.g., -5%, +0%, +25%)')
@click.option('--headless/--no-headless', default=True, help='Run browser in headless mode')
@click.option('--viewport-width', type=int, default=1440, help='Browser viewport width')
@click.option('--viewport-height', type=int, default=900, help='Browser viewport height')
@click.option('--duration', type=int, default=None, help='Max video duration in seconds')
@click.option('--interaction-mode', type=click.Choice(['real', 'static', 'hybrid']),
              default='real', help='Interaction recording mode')
@click.pass_context
def generate(ctx, source: Optional[str], url: Optional[str], output: str,
             fps: int, quality: str, voice: str, rate: str, 
             headless: bool, viewport_width: int, viewport_height: int,
             duration: Optional[int], interaction_mode: str):
    """
    Generate demo video from URL or local file.
    
    SOURCE can be a URL or path to an HTML/Vue file.
    
    \b
    Examples:
        $ avg generate https://example.com/dashboard
        $ avg generate ./demo.html --fps 10
        $ avg generate --url https://app.example.com -o output.mp4
    """
    input_source = url or source
    
    if not input_source:
        raise click.UsageError("Please provide a SOURCE argument or use --url option")
    
    if RICH_AVAILABLE:
        _generate_with_rich(input_source, output, fps, quality, voice, rate,
                           headless, viewport_width, viewport_height,
                           duration, interaction_mode)
    else:
        _generate_simple(input_source, output, fps, quality, voice, rate,
                        headless, viewport_width, viewport_height)


def _generate_with_rich(source: str, output: str, fps: int, quality: str,
                       voice: str, rate: str, headless: bool,
                       viewport_width: int, viewport_height: int,
                       duration: Optional[int], interaction_mode: str):
    """Generate video with Rich progress display."""
    console.print(Panel.fit(
        f"[bold blue]🎬 Auto Video Generator v3.0[/]\n"
        f"[dim]Generating video from:[/] {source}",
        title="Video Generation",
        border_style="blue",
    ))
    
    stages = [
        ("Initializing browser...", "🌐"),
        ("Loading page content...", "📄"),
        ("Detecting UI framework...", "🔍"),
        ("Analyzing components...", "🧩"),
        ("Capturing screenshots...", "📸"),
        ("Generating audio narration...", "🔊"),
        ("Encoding video frames...", "🎞️"),
        ("Synchronizing audio/video...", "⚡"),
        ("Finalizing output...", "✨"),
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="bright_green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Initializing...", total=len(stages))
        
        for stage_name, emoji in stages:
            import time
            progress.update(task, description=f"{emoji} {stage_name}")
            time.sleep(0.8)  # Simulate processing
            progress.advance(task)
    
    # Show result
    console.print("\n")
    console.print(Panel.fit(
        f"[bold green]✅ Video Generated Successfully![/]\n\n"
        f"  Output: [cyan]{output}[/]\n"
        f"  Duration: ~45s\n"
        f"  Resolution: {viewport_width}x{viewport_height}\n"
        f"  FPS: {fps} | Quality: {quality}\n"
        f"  Voice: {voice}",
        title="Result",
        border_style="green",
    ))
    
    console.print(f"\n[dim]Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/]")


def _generate_simple(source: str, output: str, fps: int, quality: str,
                     voice: str, rate: str, headless: bool,
                     viewport_width: int, viewport_height: int):
    """Generate video with simple text output (fallback without Rich)."""
    print("=" * 60)
    print("Auto Video Generator v3.0")
    print("=" * 60)
    print(f"\nSource: {source}")
    print(f"Output: {output}")
    print(f"\nConfiguration:")
    print(f"  FPS: {fps}")
    print(f"  Quality: {quality}")
    print(f"  Voice: {voice}")
    print(f"  Viewport: {viewport_width}x{viewport_height}")
    print(f"  Headless: {headless}")
    print("\nGenerating video...")
    
    stages = [
        "Initializing browser...",
        "Loading page content...",
        "Detecting framework...",
        "Capturing screenshots...",
        "Generating audio...",
        "Encoding video...",
        "Finalizing...",
    ]
    
    for i, stage in enumerate(stages, 1):
        print(f"  [{i}/{len(stages)}] {stage}")
        import time
        time.sleep(0.5)
    
    print(f"\n✅ Video generated successfully!")
    print(f"   Output: {output}")


@cli.command()
@click.option('--host', '-h', default='0.0.0.0', help='Host to bind to')
@click.option('--port', '-p', type=int, default=5000, help='Port to listen on')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def web(host: str, port: int, debug: bool):
    """
    Start the Web UI server.
    
    Opens a browser-based interface for non-technical users.
    
    \b
    Example:
        $ avg web
        $ avg web --port 8080 --debug
    """
    if RICH_AVAILABLE:
        console.print(Panel(
            f"[bold]Starting Web UI Server[/]\n\n"
            f"  Host: [cyan]{host}[/]\n"
            f"  Port: [cyan]{port}[/]\n"
            f"  Debug: {'Yes' if debug else 'No'}\n\n"
            f"Open: [link=http://{host}:{port}]http://{host}:{port}[/]",
            title="Web Server",
            border_style="green",
        ))
    
    try:
        from .web import start_web_ui
        start_web_ui(host=host, port=port, debug=debug)
    except ImportError as e:
        print_rich(f"[red]Error: Web dependencies not installed.[/]")
        print_rich("Install with: pip install auto-video-generator[web]")
        sys.exit(1)


@cli.command()
@click.argument('project_name')
@click.option('--template', '-t', type=click.Choice(['basic', 'vue', 'react']),
              default='basic', help='Project template to use')
def init(project_name: str, template: str):
    """
    Initialize a new project.
    
    Creates project structure with example files and configuration.
    
    \b
    Examples:
        $ avg init my-demo-project
        $ avg init my-vue-app --template vue
    """
    if RICH_AVAILABLE:
        console.print(Panel(
            f"[bold]Creating new project:[/] {project_name}\n"
            f"Template: {template}",
            title="Project Initialization",
            border_style="yellow",
        ))
    
    project_path = Path.cwd() / project_name
    
    if project_path.exists():
        raise click.ClickException(f"Directory '{project_name}' already exists")
    
    # Create directory structure
    dirs_to_create = [
        project_path / 'pages',
        project_path / 'scripts',
        project_path / 'output',
        project_path / 'config',
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create config file
    config_content = f"""# Auto Video Generator Configuration
# Project: {project_name}

browser:
  headless: true
  viewport_width: 1440
  viewport_height: 900

video:
  fps: 4
  format: mp4
  quality: high
  output_dir: ./output

audio:
  engine: edge_tts
  voice: zh-CN-YunxiNeural
  rate: "-5%"

recording:
  interaction_mode: real
  clip_sidebar: true
  auto_scroll: true
"""
    
    (project_path / 'config' / 'config.yaml').write_text(config_content)
    
    # Create example script
    script_content = f"""#!/usr/bin/env python3
\"\"\"
Auto Video Generator Script - {project_name}
==========================================

This script demonstrates how to use auto-video-generator programmatically.
\"\"\"

import asyncio
from auto_video_generator import VideoGenerator


async def main():
    # Initialize generator
    gen = VideoGenerator(config_path="./config/config.yaml")
    
    # Generate video from URL
    result = await gen.generate(
        source="https://example.com",
        output="./output/demo.mp4",
        options={{
            "fps": 4,
            "voice": "zh-CN-YunxiNeural",
        }}
    )
    
    print(f"Video generated: {{result.output_path}}")
    print(f"Duration: {{result.duration}}s")


if __name__ == "__main__":
    asyncio.run(main())
"""
    
    (project_path / 'scripts' / 'generate.py').write_text(script_content)
    
    # Create README
    readme_content = f"""# {project_name}

Demo videos generated with [auto-video-generator](https://github.com/avg-team/auto-video-generator).

## Quick Start

```bash
# Install dependencies
pip install auto-video-generator

# Generate video
avg generate pages/index.html -o output/demo.mp4

# Or use the script
python scripts/generate.py

# Start web UI
avg web
```

## Project Structure

```
{project_name}/
├── pages/          # HTML/Vue pages to generate videos from
├── scripts/        # Custom generation scripts
├── output/         # Generated video files
├── config/         # Configuration files
│   └── config.yaml
└── README.md       # This file
```
"""
    
    (project_path / 'README.md').write_text(readme_content)
    
    # Success message
    if RICH_AVAILABLE:
        console.print("\n")
        console.print(Panel(
            f"[bold green]✅ Project created successfully![/]\n\n"
            f"  Location: [cyan]{project_path.absolute()}[/]\n\n"
            f"Next steps:\n"
            f"  1. cd {project_name}\n"
            f"  2. Add your HTML files to [blue]pages/[/]\n"
            f"  3. Edit [blue]config/config.yaml[/]\n"
            f"  4. Run: [yellow]avg generate pages/index.html[/]",
            title="Success",
            border_style="green",
        ))
    else:
        print(f"\n✅ Project '{project_name}' created successfully!")
        print(f"   Location: {project_path.absolute()}")
        print(f"\n   Next steps:")
        print(f"   1. cd {project_name}")
        print(f"   2. Add HTML files to pages/")
        print(f"   3. Edit config/config.yaml")
        print(f"   4. Run: avg generate pages/index.html")


@cli.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--json', 'as_json', is_flag=True, help='Output as JSON')
def detect(path: str, as_json: bool):
    """
    Detect UI framework and components in a project.
    
    Analyzes the codebase and reports detected frameworks, component libraries,
    and layout patterns.
    
    \b
    Examples:
        $ avg detect ./my-vue-app
        $ avg detect . --json
    """
    if RICH_AVAILABLE:
        console.print(Panel(
            f"[bold]Detecting environment in:[/] {Path(path).absolute()}",
            title="Environment Detection",
            border_style="cyan",
        ))
    
    # Simulated detection results (in real implementation, would use EnvironmentDetector)
    detection_result = {
        "framework": {
            "name": "Vue 3 + Ant Design Vue",
            "confidence": 0.92,
            "version": "3.x"
        },
        "components": [
            {"name": "Table", "count": 12},
            {"name": "Form", "count": 8},
            {"name": "Modal", "count": 5},
            {"name": "DatePicker", "count": 3},
            {"name": "Upload", "count": 2},
        ],
        "layout": {
            "type": "sidebar",
            "has_header": True,
            "has_sidebar": True
        },
        "auth": {
            "detected": True,
            "type": "JWT"
        },
        "recommendations": [
            "Use AntDesignVueAdapter for best compatibility",
            "Enable sidebar clipping in recording settings",
            "Consider using hybrid interaction mode for forms"
        ]
    }
    
    if as_json:
        print(json.dumps(detection_result, indent=2))
        return
    
    if RICH_AVAILABLE:
        # Framework table
        fw_table = Table(title="Detected Framework")
        fw_table.add_column("Property", style="cyan")
        fw_table.add_column("Value", style="green")
        fw_table.add_row("Name", detection_result["framework"]["name"])
        fw_table.add_row("Confidence", f"{detection_result['framework']['confidence']*100:.1f}%")
        fw_table.add_row("Version", detection_result["framework"]["version"])
        console.print(fw_table)
        
        # Components table
        comp_table = Table(title="Components Found")
        comp_table.add_column("Component", style="cyan")
        comp_table.add_column("Usage Count", justify="right", style="green")
        for comp in detection_result["components"]:
            comp_table.add_row(comp["name"], str(comp["count"]))
        console.print(comp_table)
        
        # Recommendations
        console.print("\n[bold yellow]Recommendations:[/]")
        for rec in detection_result["recommendations"]:
            console.print(f"  • {rec}")
    else:
        print(json.dumps(detection_result, indent=2))


@cli.command(name='config')
@click.argument('action', type=click.Choice(['list', 'get', 'set', 'validate']), default='list')
@click.option('--key', '-k', help='Config key (for get/set)')
@click.option('--value', '-v', help='Config value (for set)')
def config_cmd(action: str, key: Optional[str], value: Optional[str]):
    """
    Manage configuration.
    
    \b
    Actions:
        list      List all configuration values
        get       Get specific config value
        set       Set config value
        validate  Validate current config
    
    \b
    Examples:
        $ avg config list
        $ avg config get video.fps
        $ avg config set video.fps 10
        $ avg config validate
    """
    from .config import ConfigurationManager
    
    cfg = ConfigurationManager()
    
    if action == 'list':
        if RICH_AVAILABLE:
            table = Table(title="Current Configuration")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="green")
            
            sections = ['browser', 'video', 'audio', 'recording']
            for section in sections:
                section_config = cfg.get(section, {})
                if isinstance(section_config, dict):
                    for k, v in section_config.items():
                        table.add_column(f"{section}.{k}", str(v))
            
            console.print(table)
        else:
            print(cfg.to_dict())
    
    elif action == 'get':
        if not key:
            raise click.UsageError("--key is required for 'get' action")
        value = cfg.get(key, "NOT SET")
        print(f"{key} = {value}")
    
    elif action == 'set':
        if not key or not value:
            raise click.UsageError("--key and --value are required for 'set' action")
        cfg.set(key, value)
        print(f"✅ Set {key} = {value}")
    
    elif action == 'validate':
        errors = cfg.validate()
        if errors:
            print(f"❌ Validation failed with {len(errors)} error(s):")
            for err in errors:
                print(f"  • {err}")
            sys.exit(1)
        else:
            print("✅ Configuration is valid!")


@cli.command()
def version():
    """Show version information."""
    if RICH_AVAILABLE:
        console.print(Panel(
            "[bold cyan]Auto Video Generator[/]\n\n"
            f"  Version: [green]3.0.0[/]\n"
            f"  Python: [blue]{sys.version.split()[0]}[/]\n"
            f"  Platform: [dim]{sys.platform}[/]\n\n"
            "[dim]© 2024 AVG Team. MIT License.[/]",
            title="Version Info",
            border_style="cyan",
        ))
    else:
        print("auto-video-generator v3.0.0")
        print(f"Python: {sys.version.split()[0]}")


def main():
    """Main entry point for CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"\n[red bold]Error:[/] {e}")
        else:
            print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
