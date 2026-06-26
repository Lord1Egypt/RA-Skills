"""
Benchmark Store Interfaces

Frozen benchmarks and hidden test suites.
"""

from .frozen_benchmark import FrozenBenchmark, BenchmarkResult, BenchmarkSuite
from .hidden_tests import (
    HiddenTest,
    HiddenTestSuite,
    TestResult,
    TestType,
    TestVisibility,
    create_hidden_test,
    DictHiddenTestDataSource,
    FileHiddenTestDataSource,
)

__all__ = [
    "FrozenBenchmark",
    "BenchmarkResult",
    "BenchmarkSuite",
    "HiddenTest",
    "HiddenTestSuite",
    "TestResult",
    "TestType",
    "TestVisibility",
    "create_hidden_test",
    "DictHiddenTestDataSource",
    "FileHiddenTestDataSource",
]
