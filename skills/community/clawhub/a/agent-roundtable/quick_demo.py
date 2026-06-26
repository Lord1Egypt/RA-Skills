"""Roundtable Demo — 3 lines of code, full discussion flow.

Usage:
    python quick_demo.py

This demonstrates the complete Roundtable workflow:
  1. Create a discussion with participants
  2. Run multi-round speeches with convergence tracking
  3. Generate conclusion with consensus/disagreement summary
"""

from roundtable import RoundtableCore

core = RoundtableCore()
result = core.run_demo()
