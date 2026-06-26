# -*- coding: utf-8 -*-
"""
Auto Video Generator v3.0
==========================

Professional demo video generation from HTML pages with AI voice narration.

Features:
- Multi-framework UI detection (Vue, React, Angular)
- 8+ component handlers (Table, Form, DatePicker, etc.)
- AI-powered TTS narration (Edge TTS, SAPI)
- Production-grade error handling (circuit breaker, retry)
- Performance monitoring and structured logging
- Configurable via YAML/JSON/Environment variables

Quick Start:
    >>> from auto_video_generator import VideoGenerator
    >>> gen = VideoGenerator()
    >>> result = await gen.generate("https://example.com/demo.html")
    >>> print(f"Video saved to: {result.output_path}")

CLI Usage:
    $ avg generate https://example.com/demo.html --output ./video.mp4
    $ avg generate ./demo.html --voice zh-CN-YunxiNeural --fps 4
    $ avg web                    # Start web UI at http://localhost:5000
    $ avg init my-project        # Initialize new project

For full documentation, visit: https://auto-video-generator.readthedocs.io
"""

__version__ = "3.0.0"
__author__ = "AVG Team"
__email__ = "team@avg.dev"

from .generator import VideoGenerator
from .config import ConfigurationManager
from .environment import EnvironmentDetector
from .adapters import AdapterFactory

__all__ = [
    "VideoGenerator",
    "ConfigurationManager",
    "EnvironmentDetector",
    "AdapterFactory",
    "__version__",
]
