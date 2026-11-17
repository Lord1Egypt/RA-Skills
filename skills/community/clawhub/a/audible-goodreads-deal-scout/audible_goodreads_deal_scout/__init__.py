"""Shared prep layer for the Audible Goodreads Deal Scout skill."""

__version__ = "0.1.19"

from .core import prepare_run
from .delivery import setup_configuration

__all__ = ["__version__", "prepare_run", "setup_configuration"]
