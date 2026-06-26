#!/usr/bin/env python3
"""
Simple wrapper for quick capture with default settings
"""

import sys
from pathlib import Path

# Add the scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from camera import capture_photo, get_captures_dir

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Quick photo capture")
    parser.add_argument("--camera", "-c", type=int, default=0, help="Camera index")
    args = parser.parse_args()
    
    capture_photo(camera_index=args.camera)
