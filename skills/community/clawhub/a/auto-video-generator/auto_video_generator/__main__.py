# -*- coding: utf-8 -*-
"""
Python -m entry point for auto-video-generator

Usage:
    python -m auto_video_generator [command] [options]
    
Examples:
    python -m auto_video_generator generate https://example.com
    python -m auto_video_generator --help
    python -m auto_video_generator version
"""

import sys


def main():
    """Entry point for python -m auto_video_generator."""
    from .cli import main as cli_main
    
    try:
        cli_main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
