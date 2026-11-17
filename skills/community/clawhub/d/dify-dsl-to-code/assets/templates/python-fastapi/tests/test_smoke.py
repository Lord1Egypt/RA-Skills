"""Smoke test: the engine runs the example definition end to end.

Regenerate per project: mock LLM/HTTP boundaries, assert the main path
reaches the terminal node and produces the DSL-declared outputs.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.workflow.definition import DEFINITION, build_handlers
from app.workflow.runner import Engine


def test_main_path_runs():
    engine = Engine(DEFINITION, build_handlers())
    outputs = engine.run({"text": "hello"})
    assert outputs["result"] == "Echo: hello"
