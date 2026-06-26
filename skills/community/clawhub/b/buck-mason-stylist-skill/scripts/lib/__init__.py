"""Shared helpers for the scripts/ bundle.

Modules are kept tiny and import-safe (no side effects on import) so they
can be unit-tested directly. Scripts in scripts/ that need them do:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from lib.profile import parse_profile
"""
