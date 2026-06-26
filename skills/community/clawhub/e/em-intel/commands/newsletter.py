"""Newsletter generation and delivery command."""

from typing import List

from rich.console import Console

from adapters.base import CodeAdapter, TicketAdapter
from core.delivery import send
from core.newsletter import generate_newsletter

console = Console()


def run(
    code_adapter: CodeAdapter,
    ticket_adapter: TicketAdapter,
    project_keys: List[str],
    days: int = 7,
    deliver: bool = True,
) -> str:
    """Generate and optionally deliver the weekly newsletter.

    Args:
        deliver: If True, send via configured delivery channel.
                 If False, just return the text.

    Returns:
        The generated newsletter text.
    """
    console.print("[bold cyan]Generating weekly newsletter...[/bold cyan]")

    text = generate_newsletter(code_adapter, ticket_adapter, project_keys, days=days)

    if deliver:
        success = send(text, title="Weekly Engineering Newsletter")
        if success:
            console.print("[green]Newsletter delivered successfully.[/green]")
        else:
            console.print("[red]Newsletter delivery failed. Printed above.[/red]")
    else:
        console.print(text)

    return text
