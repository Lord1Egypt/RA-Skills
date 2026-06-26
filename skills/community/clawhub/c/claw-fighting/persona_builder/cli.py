"""
Persona Builder CLI Interface
Interactive command-line interface for creating AI agent personas
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint

from .builder import PersonaBuilder

app = typer.Typer(help="Claw-Fighting Persona Builder")
console = Console()


@app.command("create")
def create_persona(
    name: str = typer.Option(None, "--name", "-n", help="Name for your persona"),
    expert: bool = typer.Option(False, "--expert", help="Use expert mode for direct YAML editing")
):
    """Create a new AI agent persona using interactive builder"""

    console.print(Panel.fit(
        "[bold blue]🤖 Claw-Fighting Persona Builder v1.1[/bold blue]\n"
        "Create your AI agent's fighting personality",
        title="Welcome",
        border_style="blue"
    ))

    if not name:
        name = Prompt.ask("[bold]Enter a name for your persona[/bold]")

    if expert:
        _expert_mode(name)
        return

    builder = PersonaBuilder()

    # Step 1: Archetype Selection
    console.print("\n[bold green]Step 1/3: Style Portrait[/bold green]")
    answers = _conduct_archetype_interview(builder)
    archetype_result = builder.step1_archetype_selection(answers)

    # Show results
    table = Table(title="Archetype Analysis")
    table.add_column("Archetype", style="cyan")
    table.add_column("Score", style="green")
    table.add_column("Description", style="yellow")

    for arch, score in archetype_result['scores'].items():
        template = builder.base_templates[arch]
        table.add_row(
            template['name'],
            str(score),
            template['description']
        )

    console.print(table)
    console.print(f"\n[bold]Selected Archetype: {archetype_result['base_persona']['name']}[/bold]")

    # Step 2: Fine-tuning
    console.print("\n[bold green]Step 2/3: Fine-tuning[/bold green]")
    adjustments = _conduct_finetuning(builder, archetype_result['base_persona'])
    tuned_persona = builder.step2_finetune_parameters(archetype_result['base_persona'], adjustments)

    # Step 3: Final generation
    console.print("\n[bold green]Step 3/3: Final Persona[/bold green]")
    final_persona = builder.step3_generate_final_persona(tuned_persona, name)

    # Save persona
    _save_persona_interactive(builder, final_persona)


def _conduct_archetype_interview(builder: PersonaBuilder) -> list:
    """Conduct interactive interview for archetype selection"""
    questions = builder.get_questions_for_step1()
    answers = []

    for i, question in enumerate(questions, 1):
        console.print(f"\n[bold]Question {i}/{len(questions)}[/bold]")

        if question['type'] == 'situational':
            console.print(Panel(question['scenario'], title="Scenario", border_style="blue"))
        else:
            console.print(f"[cyan]{question['question']}[/cyan]")

        console.print("\nChoose your response:")
        for j, option in enumerate(question['options'], 1):
            console.print(f"  [{j}] {option['text']}")

        choice = Prompt.ask("Your choice", choices=[str(j) for j in range(1, len(question['options']) + 1)])
        selected_option = question['options'][int(choice) - 1]
        answers.append(selected_option)

    return answers


def _conduct_finetuning(builder: PersonaBuilder, base_persona: dict) -> dict:
    """Conduct parameter fine-tuning"""
    console.print("\n[bold]Fine-tune your persona's characteristics:[/bold]")

    base_params = base_persona.get('base_params', {})
    adjustments = {}

    # Risk tolerance
    current_risk = base_params.get('risk_tolerance', 50)
    risk = Prompt.ask(
        f"Risk tolerance (0-100) [current: {current_risk}]",
        default=str(current_risk),
        show_default=False
    )
    adjustments['risk_tolerance'] = int(risk)

    # Bluff frequency
    current_bluff = base_params.get('bluff_frequency', 0.5)
    bluff = Prompt.ask(
        f"Bluff frequency (0.0-1.0) [current: {current_bluff}]",
        default=str(current_bluff),
        show_default=False
    )
    adjustments['bluff_frequency'] = float(bluff)

    # Catchphrases
    console.print("\n[bold]Add catchphrases for your persona:[/bold]")
    catchphrases = []
    while True:
        phrase = Prompt.ask("Enter a catchphrase (or press Enter to finish)")
        if not phrase:
            break
        catchphrases.append(phrase)

    if catchphrases:
        adjustments['catchphrases'] = catchphrases

    return adjustments


def _save_persona_interactive(builder: PersonaBuilder, persona: dict):
    """Save persona with user interaction"""
    console.print("\n[bold]Persona Summary:[/bold]")
    console.print(f"Name: {persona['meta']['name']}")
    console.print(f"Archetype: {persona['archetype']['primary']}")
    console.print(f"Risk Tolerance: {persona['personality_vectors']['risk_tolerance']}")
    console.print(f"Bluff Frequency: {persona['personality_vectors']['bluff_frequency']}")

    if Confirm.ask("\nSave this persona?", default=True):
        default_path = f"~/.claw-fighting/personas/{persona['meta']['name'].lower().replace(' ', '_')}.yaml"
        filepath = Prompt.ask("Save location", default=default_path)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Saving persona...", total=100)

            builder.save_persona(persona, filepath)
            progress.update(task, completed=100)

        console.print(f"[green]✅ Persona saved to {filepath}[/green]")
        console.print(f"[blue]Signature: {persona['meta']['signature']}[/blue]")
    else:
        console.print("[yellow]Persona not saved.[/yellow]")


def _expert_mode(name: str):
    """Expert mode for direct YAML editing"""
    console.print("\n[bold red]Expert Mode: Direct YAML Editing[/bold red]")
    console.print("This will open your default editor for manual persona configuration.")

    if Confirm.ask("Continue to expert mode?", default=True):
        # This would typically open an editor like vim/nano
        console.print("[yellow]Expert mode: Please edit the YAML file directly[/yellow]")
        console.print("Template location: ~/.claw-fighting/personas/templates/expert_template.yaml")


@app.command("list")
def list_personas():
    """List all available personas"""
    personas_dir = "~/.claw-fighting/personas"
    console.print(f"[bold]Available personas in {personas_dir}:[/bold]")

    # This would list actual persona files
    console.print("[yellow]Persona listing functionality coming soon...[/yellow]")


if __name__ == "__main__":
    app()