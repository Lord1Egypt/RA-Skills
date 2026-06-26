from rich.console import Console
from rich.panel import Panel

console = Console()

def display_thought(thought_process):
    """
    在终端展示 Agent 的 Chain of Thought
    """
    panel = Panel("\n".join(thought_process), title="Agent CoT")
    console.print(panel)

def display_tools(tools):
    """
    在终端展示当前注册的工具
    """
    panel = Panel(", ".join(tools), title="Registered Tools")
    console.print(panel)
