#!/usr/bin/env python3
"""
Camera control script for OpenClaw Skill
Supports: capture, list, preview
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

def get_captures_dir():
    """Get the default captures directory"""
    workspace = Path.home() / ".openclaw" / "workspace"
    captures = workspace / "captures"
    captures.mkdir(parents=True, exist_ok=True)
    return captures

def list_cameras():
    """List available camera devices"""
    try:
        import cv2
    except ImportError:
        print("ERROR: OpenCV not installed. Run: pip install opencv-python")
        sys.exit(1)
    
    print("Scanning for cameras...")
    available = []
    
    # Check first 10 camera indices
    for i in range(10):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                available.append((i, width, height))
                print(f"  Camera {i}: {width}x{height}")
            cap.release()
    
    if not available:
        print("No cameras found.")
    else:
        print(f"\nFound {len(available)} camera(s). Use --camera <index> to select.")
    
    return available

def capture_photo(camera_index=0, output_path=None, warmup=0.5):
    """Capture a photo from the specified camera"""
    try:
        import cv2
    except ImportError:
        print("ERROR: OpenCV not installed. Run: pip install opencv-python")
        sys.exit(1)
    
    # Default output path
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = get_captures_dir() / f"photo_{timestamp}.jpg"
    else:
        output_path = Path(output_path).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Open camera with platform-specific backend
    backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_V4L2
    cap = cv2.VideoCapture(camera_index, backend)
    
    if not cap.isOpened():
        # Fallback to default backend
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print(f"ERROR: Cannot open camera {camera_index}")
            sys.exit(1)
    
    # Warmup - let camera adjust exposure/focus
    if warmup > 0:
        time.sleep(warmup)
        # Read a few frames to stabilize
        for _ in range(5):
            cap.read()
    
    # Capture frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("ERROR: Failed to capture frame")
        sys.exit(1)
    
    # Save image
    cv2.imwrite(str(output_path), frame)
    print(f"{output_path}")
    return str(output_path)

def preview_camera(camera_index=0, duration=3):
    """Show camera preview window for specified duration"""
    try:
        import cv2
    except ImportError:
        print("ERROR: OpenCV not installed. Run: pip install opencv-python")
        sys.exit(1)
    
    backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_V4L2
    cap = cv2.VideoCapture(camera_index, backend)
    
    if not cap.isOpened():
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print(f"ERROR: Cannot open camera {camera_index}")
            sys.exit(1)
    
    print(f"Opening preview (closes automatically in {duration}s)...")
    print("Press 'q' to close early")
    
    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow("Camera Preview (Press 'q' to close)", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Preview closed")

def main():
    parser = argparse.ArgumentParser(description="Camera control for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # List command
    subparsers.add_parser("list", help="List available cameras")
    
    # Capture command
    capture_parser = subparsers.add_parser("capture", help="Capture a photo")
    capture_parser.add_argument("--camera", "-c", type=int, default=0, help="Camera index (default: 0)")
    capture_parser.add_argument("--output", "-o", type=str, help="Output path (default: auto-generated)")
    capture_parser.add_argument("--warmup", "-w", type=float, default=0.5, help="Warmup time in seconds (default: 0.5)")
    
    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Show camera preview")
    preview_parser.add_argument("--camera", "-c", type=int, default=0, help="Camera index (default: 0)")
    preview_parser.add_argument("--duration", "-d", type=int, default=3, help="Preview duration in seconds (default: 3)")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_cameras()
    elif args.command == "capture":
        capture_photo(args.camera, args.output, args.warmup)
    elif args.command == "preview":
        preview_camera(args.camera, args.duration)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
