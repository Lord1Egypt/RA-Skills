"""Consolidated commander module for v0.1.9 simplification."""

from abc import ABC, abstractmethod
import importlib
import inspect
import pkgutil
import sys
from argparse import ArgumentParser, Namespace
from typing import Dict, List, Type, Optional

# === Command (from commander/base.py) ===

class Command(ABC):
    """
    Base class for all modular CLI commands.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the command, used in the CLI argument parser."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the command."""
        pass

    @abstractmethod
    def configure_parser(self, parser: ArgumentParser) -> None:
        """
        Configure the argparse subparser for this command.

        Args:
            parser (ArgumentParser): The subparser to configure.
        """
        pass

    @abstractmethod
    async def execute(self, args: Namespace) -> int:
        """
        Execute the command.

        Args:
            args (Namespace): The parsed arguments.

        Returns:
            int: The exit code (0 for success, non-zero for failure).
        """
        pass

    def validate(self, args: Namespace) -> None:
        """
        Validate the parsed arguments before execution.
        Raises ValueError if arguments are invalid.

        Args:
            args (Namespace): The parsed arguments.
        """
        pass

# === CommandRegistry (from commander/registry.py) ===

class CommandRegistry:
    """Registry to auto-discover and manage CLI commands."""

    def __init__(self):
        self._commands: Dict[str, Type[Command]] = {}

    def register(self, command_class: Type[Command]) -> None:
        """Register a single command class."""
        if not inspect.isclass(command_class) or not issubclass(command_class, Command):
            raise TypeError(f"Cannot register {command_class}: must be a subclass of Command")

        # Instantiate to get the name property
        try:
            cmd_instance = command_class()
            name = cmd_instance.name
            if not name:
                raise ValueError(f"Command class {command_class.__name__} must define a name property.")

            # Don't register the base class itself or optional bases that lack a name
            if name != "base_command_name":
                self._commands[name] = command_class
        except Exception:
             # Ignore abstract classes or bases missing implementations
             pass

    def get(self, name: str) -> Optional[Type[Command]]:
        """Get a registered command class by name."""
        return self._commands.get(name)

    def all(self) -> List[Type[Command]]:
        """Get all registered command classes."""
        return list(self._commands.values())

    def auto_discover(self, package_name: str = "ghostclaw.cli.commands") -> None:
        """
        Auto-discover and register all Command subclasses in the given package.
        """
        try:
            package = importlib.import_module(package_name)
        except ImportError as e:
            print(f"Warning: Command package '{package_name}' could not be imported. Auto-discovery skipped. ({e})", file=sys.stderr)
            return

        # Walk through the package and import all modules
        for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            try:
                module = importlib.import_module(module_name)
                # Find all Command subclasses in the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Command) and obj is not Command:
                        # Avoid registering abstract classes
                        if not inspect.isabstract(obj):
                            self.register(obj)
            except ImportError as e:
                print(f"Warning: Failed to import command module {module_name}: {e}", file=sys.stderr)

# Create a singleton registry instance
registry = CommandRegistry()

__all__ = ['Command', 'CommandRegistry', 'registry']
