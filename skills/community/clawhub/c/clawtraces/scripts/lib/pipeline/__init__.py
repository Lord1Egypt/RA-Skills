# lib.pipeline — 业务编排:串联 parse → convert,定义 I/O 契约
"""Pipeline package. Re-exports names from ``pipeline.py`` so that
callers can keep using ``from lib.pipeline import discover_sessions`` /
``from lib import pipeline; pipeline.discover_sessions`` unchanged after
the directory restructure.
"""
from .pipeline import *  # noqa: F401, F403
from .pipeline import _is_cron_task  # noqa: F401
