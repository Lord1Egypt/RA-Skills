"""Scheduler task registry; entries are resolved by name at run time."""

import importlib

TASKS = {
    "nightly-revenue": "app.report:nightly_revenue",
    "cleanup": "app.cleanup:run",
}


def resolve(name: str):
    """Import and return the callable registered under name."""
    module_name, _, attribute = TASKS[name].partition(":")
    return getattr(importlib.import_module(module_name), attribute)
