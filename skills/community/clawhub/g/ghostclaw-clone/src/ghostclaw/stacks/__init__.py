"""Stack-specific analyzers."""

from .base import StackAnalyzer
from .node import NodeAnalyzer
from .python import PythonAnalyzer
from .go import GoAnalyzer
from .shell import ShellAnalyzer
from .typescript import TypeScriptAnalyzer
from .docker import DockerAnalyzer

__all__ = [
    'StackAnalyzer',
    'NodeAnalyzer',
    'PythonAnalyzer',
    'GoAnalyzer',
    'ShellAnalyzer',
    'TypeScriptAnalyzer',
    'DockerAnalyzer'
]

# Registry mapping stack names to their analyzers
STACK_REGISTRY = {
    'node': NodeAnalyzer(),
    'python': PythonAnalyzer(),
    'go': GoAnalyzer(),
    'shell': ShellAnalyzer(),
    'typescript': TypeScriptAnalyzer(),
    'docker': DockerAnalyzer()
}


def get_analyzer(stack: str) -> StackAnalyzer:
    """Get the appropriate analyzer for a given stack."""
    return STACK_REGISTRY.get(stack)
