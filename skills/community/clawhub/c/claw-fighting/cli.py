"""
Main CLI interface for Claw-Fighting skill
"""

import typer
import asyncio
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from .claw_fighting_skill import ClawFightingSkill
from .persona_builder.cli import app as persona_app

app = typer.Typer(help="Claw-Fighting - Decentralized AI Agent Battle Platform")
console = Console()

# Add persona builder as a subcommand
app.add_typer(persona_app, name="persona", help="Manage AI agent personas")


@app.callback()
def main():
    """Claw-Fighting - The world's first decentralized AI Agent competitive training platform"""
    pass


@app.command("start")
def start_game(
    coordinator: str = typer.Option(None, "--coordinator", "-c", help="Coordinator URL"),
    persona: str = typer.Option(None, "--persona", "-p", help="Persona file to use"),
    trainer: str = typer.Option(None, "--trainer", "-t", help="Trainer name")
):
    """Start Claw-Fighting (enters guided mode for first-time users)"""

    console.print(Panel.fit(
        "[bold blue]🎮 Claw-Fighting Arena[/bold blue]\n"
        "🤖 The world's first decentralized AI Agent competitive training platform",
        title="Welcome",
        border_style="blue"
    ))

    # Check if first time user
    config_dir = Path.home() / ".claw-fighting"
    first_time = not (config_dir / "config.json").exists()

    if first_time:
        console.print("\n[bold green]🚀 First-time setup detected![/bold green]")
        console.print("Would you like to create your first AI fighter?")

        choice = typer.prompt(
            "Choose an option",
            type=typer.Choice(["1", "2", "3"]),
            default="1",
            show_choices=False,
            show_default=False,
            prompt_suffix="\n[1] Yes, start guided builder (recommended)\n[2] Direct YAML editing (expert mode)\n[3] Load example persona\n\nYour choice: "
        )

        if choice == "1":
            # Launch persona builder
            from .persona_builder.cli import create_persona
            create_persona(name=None, expert=False)
            return
        elif choice == "2":
            from .persona_builder.cli import create_persona
            create_persona(name=None, expert=True)
            return
        elif choice == "3":
            _load_example_persona()
            return

    # Normal startup
    console.print("\n[bold]Starting Claw-Fighting session...[/bold]")

    # Initialize skill
    try:
        # This would normally get the OpenClaw runtime
        # For CLI demo, we'll create a mock runtime
        skill = _initialize_skill(coordinator, persona, trainer)

        # Start connection
        asyncio.run(skill.connect())

    except Exception as e:
        console.print(f"[red]Error starting Claw-Fighting: {e}[/red]")
        raise typer.Exit(1)


@app.command("status")
def show_status():
    """Show current Claw-Fighting status"""
    console.print("[bold]Claw-Fighting Status:[/bold]")

    # Check configuration
    config_dir = Path.home() / ".claw-fighting"
    if config_dir.exists():
        console.print(f"✅ Configuration directory: {config_dir}")
    else:
        console.print(f"❌ Configuration directory not found: {config_dir}")

    # Check personas
    personas_dir = config_dir / "personas"
    if personas_dir.exists():
        personas = list(personas_dir.glob("*.yaml"))
        console.print(f"✅ Personas found: {len(personas)}")
        for persona in personas:
            console.print(f"  - {persona.name}")
    else:
        console.print("❌ No personas directory found")


@app.command("marketplace")
def marketplace(
    action: str = typer.Argument(..., help="Action: browse, install, share"),
    name: str = typer.Option(None, "--name", "-n", help="Persona name")
):
    """Browse or manage persona marketplace"""

    if action == "browse":
        console.print("[bold]🏪 Persona Marketplace[/bold]")
        console.print("Top-rated personas from the community:")
        console.print("  • [blue]MathMaster Pro[/blue] - 95% win rate")
        console.print("  • [blue]BluffKing Elite[/blue] - 89% win rate")
        console.print("  • [blue]PsychOut Champion[/blue] - 87% win rate")

    elif action == "install" and name:
        console.print(f"[green]Installing persona: {name}[/green]")
        # This would download and install the persona

    elif action == "share" and name:
        console.print(f"[blue]Sharing persona: {name}[/blue]")
        # This would upload the persona to marketplace


@app.command("leaderboard")
def show_leaderboard(
    season: str = typer.Option("current", "--season", "-s", help="Season to show")
):
    """Show current leaderboard"""
    console.print("[bold]🏆 Current Season Leaderboard[/bold]")
    console.print("Top 10 AI Fighters:")
    console.print("  1. [gold1]QuantumGambit[/gold1] - 3420 MMR")
    console.print("  2. [gold1]BluffMaster3000[/gold1] - 3380 MMR")
    console.print("  3. [gold1]DiceOracle[/gold1] - 3350 MMR")
    console.print("  ...")


def _load_example_persona():
    """Load an example persona for new users"""
    console.print("\n[bold]Loading example persona...[/bold]")

    examples = ["mathematician", "gambler", "observer", "psychologist", "berserker"]
    choice = typer.prompt(
        "Choose an example persona",
        type=typer.Choice(examples),
        show_choices=True
    )

    console.print(f"[green]✅ Loaded {choice} example persona![/green]")
    console.print("You can modify it later using: claw-fighting persona edit")


def _initialize_skill(coordinator=None, persona=None, trainer=None):
    """Initialize ClawFightingSkill with configuration"""
    # This is a simplified version for CLI demo
    # In real usage, this would integrate with OpenClaw runtime

    class MockRuntime:
        def get_model_info(self):
            return {"model": "llama3:70b", "provider": "local"}

        def register_hook(self, hook_name, callback):
            pass

        async def make_decision(self, context):
            return {"action": "bid", "data": {"dice_count": 3, "face_value": 6}}

        async def add_memory(self, memory_entry):
            pass

    runtime = MockRuntime()
    skill = ClawFightingSkill(runtime)

    return skill


if __name__ == "__main__":
    app()