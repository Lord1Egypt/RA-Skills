"""Codebase metrics: file sizes, lines, complexity indicators."""

from pathlib import Path
from typing import Dict, List
import os


def count_lines(filepath: str) -> int:
    """Count lines in a file, ignoring errors."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def analyze_file_sizes(files: List[str]) -> Dict:
    """Analyze file size distribution."""
    if not files:
        return {
            "total_files": 0,
            "total_lines": 0,
            "average_lines": 0,
            "large_files": [],
            "large_file_count": 0
        }

    line_counts = [count_lines(f) for f in files]
    total_lines = sum(line_counts)
    avg_lines = total_lines / len(files)

    # Define "large" thresholds per stack (will be parameterized)
    large_threshold = 300  # Default, will be overridden by stack
    large_files = [f for f, lines in zip(files, line_counts) if lines > large_threshold]

    return {
        "total_files": len(files),
        "total_lines": total_lines,
        "average_lines": avg_lines,
        "large_files": large_files,
        "large_file_count": len(large_files)
    }


def get_stack_threshold(stack: str) -> int:
    """Get the 'large file' line count threshold for a given stack."""
    thresholds = {
        'node': 400,
        'python': 300,
        'go': 500,
        'unknown': 300
    }
    return thresholds.get(stack, 300)
