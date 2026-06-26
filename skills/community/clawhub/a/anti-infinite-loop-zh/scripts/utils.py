#!/usr/bin/env python3
"""
Utility functions for SKILL_NAME
Common helper functions used across the skill
"""

import sys
import logging
from pathlib import Path


def setup_logging(verbose=False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_skill_root():
    """Get the skill root directory"""
    return Path(__file__).parent.parent


def validate_environment():
    """Validate the execution environment"""
    return {'valid': True, 'python_version': sys.version}


def log_metrics(metric_name, value):
    """Log a metric for monitoring"""
    print(f"METRIC: {metric_name}={value}")


if __name__ == "__main__":
    print("SKILL_NAME utils module")
