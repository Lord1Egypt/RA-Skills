"""
agent-bench-lite: A lightweight AI Agent evaluation benchmark toolkit.

Provides modular evaluation across six core dimensions:
- Tool Calling Accuracy
- Planning & Decomposition
- Context Retention
- Error Recovery
- Instruction Following
- Multi-step Reasoning
"""

__version__ = "0.1.0"

from agent_bench_lite.adapters.base import BaseAdapter, EchoAdapter
from agent_bench_lite.core.evaluator import Evaluator
from agent_bench_lite.core.reporter import BenchmarkReport
from agent_bench_lite.core.runner import BenchmarkRunner
from agent_bench_lite.dimensions.base import BaseDimension, Task, TaskResult

__all__ = [
    "BaseAdapter",
    "BaseDimension",
    "BenchmarkReport",
    "BenchmarkRunner",
    "EchoAdapter",
    "Evaluator",
    "Task",
    "TaskResult",
]
