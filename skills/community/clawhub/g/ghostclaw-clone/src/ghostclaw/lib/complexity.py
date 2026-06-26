"""Unified cognitive complexity analysis using complexipy."""

from typing import Optional, Dict, List
from pathlib import Path

try:
    from complexipy import file_complexity, ComplexityResult
    HAS_COMPLEXIPY = True
except ImportError:
    HAS_COMPLEXIPY = False


def get_cognitive_complexity(file_path: str) -> Optional[Dict]:
    """
    Compute cognitive complexity for a single file using complexipy.

    Returns:
        dict with keys: complexity (int), functions (list), or None if unavailable.
    """
    if not HAS_COMPLEXIPY:
        return None

    try:
        result: ComplexityResult = file_complexity(file_path)
        return {
            'complexity': result.complexity,
            'functions': [
                {'name': f.name, 'complexity': f.complexity}
                for f in result.functions
            ]
        }
    except Exception:
        return None


def analyze_files_cognitive(files: List[str]) -> Dict:
    """
    Analyze a list of files and aggregate cognitive complexity metrics.

    Returns:
        Dict with:
          - avg_complexity: float
          - max_complexity: int
          - complex_files: list of top 5 (file, complexity) over threshold (10)
          - per_function: list of top 10 most complex functions across all files
    """
    if not HAS_COMPLEXIPY:
        return {}

    scores = []
    max_complex = 0
    complex_files = []
    per_function = []

    for f in files:
        try:
            result = file_complexity(f)
            scores.append(result.complexity)
            if result.complexity > max_complex:
                max_complex = result.complexity
            if result.complexity > 10:  # threshold for "complex file"
                complex_files.append({
                    "file": str(Path(f).name),
                    "cognitive": result.complexity
                })

            # Collect top functions
            for func in result.functions:
                per_function.append({
                    "file": str(Path(f).name),
                    "function": func.name,
                    "complexity": func.complexity
                })
        except Exception:
            continue

    # Sort and limit
    complex_files.sort(key=lambda x: x['cognitive'], reverse=True)
    complex_files = complex_files[:5]

    per_function.sort(key=lambda x: x['complexity'], reverse=True)
    per_function = per_function[:10]

    avg = sum(scores) / len(scores) if scores else 0.0

    return {
        'avg_cognitive': round(avg, 2),
        'max_cognitive': max_complex,
        'complex_files': complex_files,
        'top_functions': per_function
    }
