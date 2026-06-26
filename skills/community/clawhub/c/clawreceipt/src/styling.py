import sys
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

# -----------------
# 🎨 COLOR PALETTE
# -----------------
COLORS = {
    "primary": "#ff9500",      # Orange
    "secondary": "#ff6b35",    # Deep orange
    "accent": "#ff9f1c",       # Bright orange
    "warning": "#ffd93d",      # Yellow
    "error": "#ff6b6b",        # Red
    "success": "#00ff9f",      # Neon green
    "info": "#6c5ce7",         # Purple
    "gray": "#666666",
}

# -----------------
# 🎨 ASCII LOGO
# -----------------
ASCII_LOGO = """
  ██████╗██╗      █████╗ ██╗    ██╗██████╗ ███████╗ ██████╗███████╗██╗██████╗ ████████╗███████╗
 ██╔════╝██║     ██╔══██╗██║    ██║██╔══██╗██╔════╝██╔════╝██╔════╝██║██╔══██╗╚══██╔══╝██╔════╝
 ██║     ██║     ███████║██║ █╗ ██║██████╔╝█████╗  ██║     █████╗  ██║██████╔╝   ██║   ███████╗
 ██║     ██║     ██╔══██║██║███╗██║██╔══██╗██╔══╝  ██║     ██╔══╝  ██║██╔═══╝    ██║   ╚════██║
 ╚██████╗███████╗██║  ██║╚███╔███╔╝██║  ██║███████╗╚██████╗███████╗██║██║        ██║   ███████║
  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝╚═╝        ╚═╝   ╚══════╝
"""

# -----------------
# 🚀 UTILS
# -----------------
def generate_gradient_text(text: str, color1: str = COLORS["primary"], color2: str = COLORS["secondary"]) -> Text:
    """Creates a gradient effect across a string of text using Rich."""
    rich_text = Text()
    # Extremely basic mapping: left half color1, right half color2.
    # Rich doesn't have built-in true character-by-character hex interpolation yet,
    # so we approximate it (or just use two main colors).
    length = len(text)
    mid = length // 2
    rich_text.append(text[:mid], style=f"bold {color1}")
    rich_text.append(text[mid:], style=f"bold {color2}")
    return rich_text

def print_banner(subtitle: str = "ClawReceipt - Receipt Manager for OpenClaw"):
    """Prints the awesome retro gradient banner."""
    title = generate_gradient_text(ASCII_LOGO, COLORS["primary"], COLORS["secondary"])
    console.print(title)
    
    line = "─" * 60
    console.print(generate_gradient_text(line, COLORS["primary"], COLORS["secondary"]))
    console.print(f"  [bold {COLORS['secondary']}]🦞[/] [bold {COLORS['primary']}]{subtitle}[/]")
    console.print(generate_gradient_text(line, COLORS["primary"], COLORS["secondary"]))
    console.print()

def print_section(title: str):
    """Prints a styled retro section header."""
    console.print()
    border_color = COLORS["secondary"]
    console.print(f"[{border_color}]┌{'─' * 58}┐[/]")
    console.print(f"[{border_color}]│[/] [bold cyan]{title.ljust(56)}[/] [{border_color}]│[/]")
    console.print(f"[{border_color}]└{'─' * 58}┘[/]")

def print_success(message: str):
    console.print(f"  [bold {COLORS['success']}]✓[/] {message}")

def print_error(message: str):
    console.print(f"  [bold {COLORS['error']}]✗[/] {message}")

def print_warning(message: str):
    console.print(f"  [bold {COLORS['warning']}]⚠[/] {message}")

def print_info(message: str):
    console.print(f"  [bold {COLORS['info']}]ℹ[/] {message}")

def print_key_value(key: str, value: str, indent: int = 2):
    spaces = " " * indent
    console.print(f"{spaces}[cyan]●[/] [{COLORS['gray']}]{key}:[/] [white]{value}[/]")
