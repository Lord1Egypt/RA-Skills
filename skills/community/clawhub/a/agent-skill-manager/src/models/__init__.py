"""Models layer: typed data shapes for products and audit reports.

Mirrors the ``models/`` layer of MoneyPrinterTurbo's ``app/`` layout.
These are TypedDicts used for documentation / type-checking only; the
runtime code still works with plain dicts, so no behavioral change.
"""

from .product import ProductSpec
from .report import Finding, SkillReport, StatusEntry

__all__ = ["ProductSpec", "Finding", "SkillReport", "StatusEntry"]
