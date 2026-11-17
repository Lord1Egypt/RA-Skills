#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-manager CLI entry point wrapper.

Delegates to the modular main.py in the parent directory.
This wrapper exists so the skill conforms to the scripts/ entry convention.

Usage:
    python3 scripts/blog_manager.py <command> [options]

Run ``python3 scripts/blog_manager.py capability-list`` for all 27 commands.
"""

import os
import sys

_PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from main import main  # noqa: E402

if __name__ == "__main__":
    main()
