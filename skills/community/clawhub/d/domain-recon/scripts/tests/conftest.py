"""Pytest configuration: make the helper importable and expose fixture loaders."""
import json
import os
import sys

# This file lives at scripts/tests/conftest.py; recon.py is one level up.
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS = os.path.dirname(_HERE)
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

FIXTURES = os.path.join(_HERE, "fixtures")


def load_fixture(name):
    """Load a JSON fixture from tests/fixtures/ by filename."""
    with open(os.path.join(FIXTURES, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_fixture_text(name):
    with open(os.path.join(FIXTURES, name), "r", encoding="utf-8") as fh:
        return fh.read()
