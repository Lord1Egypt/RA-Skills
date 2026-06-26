"""Adapters for integrating Roundtable with agent frameworks.

Built-in adapters:
    - ``HermesAdapter`` — for Hermes Agent (via ``hermes.py``)
    - ``SimpleAdapter`` — minimal callable-based reference (via ``simple.py``)

Custom adapters:
    Subclass ``RoundtableAdapter`` from ``base.py`` and register via
    ``roundtable.register_adapter(name, adapter_class)``.
"""

from roundtable.adapters.base import RoundtableAdapter
from roundtable.adapters.simple import SimpleAdapter

__all__ = ["RoundtableAdapter", "SimpleAdapter"]
