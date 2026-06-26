"""
Metrics collection logic for Ghostclaw analyzer.
"""

from pathlib import Path
from typing import List, Tuple


class MetricCollector:
    """Handles line counting and file size metrics."""

    @staticmethod
    def collect_metrics(file_list: List[str], threshold: int) -> Tuple[int, List[int], List[str]]:
        """
        Compute base metrics for a list of files.

        Returns:
            Tuple of (total_lines, line_counts, large_files)
        """
        total_lines = 0
        large_files = []
        line_counts = []
        for f in file_list:
            try:
                with open(f, 'rb') as file:
                    count = 0
                    while True:
                        chunk = file.read(65536)
                        if not chunk:
                            break
                        count += chunk.count(b'\n')
                    if count > 0 or Path(f).stat().st_size > 0:
                        count += 1
                    total_lines += count
                    line_counts.append(count)
                    if count > threshold:
                        large_files.append(f)
            except Exception:
                continue
        return total_lines, line_counts, large_files
