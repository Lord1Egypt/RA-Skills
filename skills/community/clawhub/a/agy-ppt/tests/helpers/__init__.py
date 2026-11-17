"""Deterministic test helpers for the agy-ppt recovery suite (Phase 9).

Nothing in this package launches a real process, calls Codex, calls Kiro, calls
the built-in ``image_gen`` tool, or reads an API key. Every fault is injected in
memory / on a temporary filesystem, so the recovery suite consumes zero
subscription quota.
"""
