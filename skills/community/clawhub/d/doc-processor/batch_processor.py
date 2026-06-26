#!/usr/bin/env python3
"""批量处理模块 - v2.5.0"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class BatchResult:
    success: int = 0
    failed: int = 0
    total: int = 0
    duration: float = 0.0
    errors: List[dict] = field(default_factory=list)
    output_paths: List[str] = field(default_factory=list)
    
    @property
    def speed(self) -> float:
        return self.total / self.duration if self.duration > 0 else 0
    
    @property
    def success_rate(self) -> float:
        return self.success / self.total * 100 if self.total > 0 else 0

@dataclass
class ProgressInfo:
    current: int
    total: int
    success: int
    failed: int
    percent: float
    elapsed: float
    eta: float = None

class ProgressTracker:
    def __init__(self, total: int, description: str = "处理中"):
        self.total = total
        self.description = description
        self.start_time = __import__('time').time()
        self.current = 0
        self.success = 0
        self.failed = 0
    
    def update(self, current: int, success: int, failed: int):
        self.current = current
        self.success = success
        self.failed = failed
    
    def get_info(self) -> ProgressInfo:
        import time
        elapsed = time.time() - self.start_time
        percent = (self.current / self.total * 100) if self.total > 0 else 0
        eta = None
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
        return ProgressInfo(self.current, self.total, self.success, self.failed, percent, elapsed, eta)

class SimpleProgress:
    def __init__(self, total: int, bar_length: int = 40):
        self.total = total
        self.bar_length = bar_length
    
    def __call__(self, current: int, total: int, success: int, failed: int):
        import sys
        percent = current / self.total * 100
        filled = int(self.bar_length * current / self.total)
        bar = '█' * filled + '░' * (self.bar_length - filled)
        sys.stdout.write(f'\r[{bar}] {percent:.1f}% ({current}/{total}) ✓{success} ✗{failed}')
        sys.stdout.flush()
        if current == total:
            print()
