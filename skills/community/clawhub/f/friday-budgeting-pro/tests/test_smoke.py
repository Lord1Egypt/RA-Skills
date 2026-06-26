"""Smoke tests — keep these fast and trivial.

The goal is "does the project import and parse cleanly", not "is everything
correct". Real feature tests get added as features are built.
"""


def test_python_works():
    """Sanity: pytest itself runs."""
    assert 1 + 1 == 2


def test_repo_structure_exists():
    """The directories we plan to have should exist (or be planned)."""
    import os

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # These docs should always be present
    for f in ("README.md", "ARCHITECTURE.md", "PLAN.md"):
        assert os.path.exists(os.path.join(root, f)), f"Missing {f}"
