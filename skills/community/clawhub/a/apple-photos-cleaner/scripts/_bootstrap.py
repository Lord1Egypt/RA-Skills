"""
Python version guard. Import it before any other project module.

The project modules use 3.10 syntax (``X | None`` annotations), so on older
Pythons (stock macOS ``/usr/bin/python3`` is 3.9) they fail on import with a
TypeError that says nothing useful. Importing this first replaces that with
the fix. It must itself stay importable on old Pythons: no 3.10+ syntax here.
"""

import sys

MIN_PYTHON = (3, 10)

if sys.version_info < MIN_PYTHON:
    sys.stderr.write(
        "❌ python: Python {}.{} is too old; apple-photos-cleaner needs {}.{}+.\n"
        "     → Install a current Python (`brew install python`) and run this with its `python3`.\n".format(
            *sys.version_info[:2], *MIN_PYTHON
        )
    )
    sys.exit(1)
