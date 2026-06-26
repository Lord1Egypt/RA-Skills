#!/usr/bin/env python3
"""
Pure webcam capture script - no AI models, just take pictures.
Cross-platform: Linux (V4L2), Windows (DirectShow/DShow), macOS (AVFoundation).
"""
import argparse
import os
import sys
import time

import cv2

# ── Platform Detection ───────────────────────────────────────────────────────
IS_WINDOWS = sys.platform == "win32" or sys.platform == "cygwin"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"

# ── Default Paths ─────────────────────────────────────────────────────────────
# 统一使用环境变量或默认值，不硬编码用户目录
def get_default_output_dir():
    """Get default output directory in workspace projects folder."""
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return os.path.join(workspace, "projects", "camera-yolo-operator", "captures")


def get_skill_dir():
    """Get the skill directory based on this script's location."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Camera Opening ────────────────────────────────────────────────────────────
def open_camera(index: int):
    """
    Try multiple backends to open the camera.
    Order: platform-specific first, then fallback.
    """
    if IS_WINDOWS:
        # DirectShow (DSHOW) is Windows-specific, fastest for Windows
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
        cap.release()

    if IS_LINUX:
        # Try V4L2 first (most common on Linux)
        cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
        if cap.isOpened():
            return cap
        cap.release()

    if IS_MACOS:
        # AVFoundation on macOS
        cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            return cap
        cap.release()

    # Fallback: default backend
    cap = cv2.VideoCapture(index)
    return cap


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Capture photos from local webcam. No AI models - pure camera capture."
    )
    parser.add_argument("--camera-index", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--count", type=int, default=3, help="Number of photos to take (default: 3)")
    parser.add_argument("--interval", type=float, default=0.5,
                        help="Interval between shots in seconds (default: 0.5)")
    parser.add_argument("--output-dir", default=None,
                        help=f"Output directory (default: ~/.../projects/camera-yolo-operator/captures)")
    parser.add_argument("--warmup", type=int, default=5,
                        help="Number of warmup frames (default: 5)")
    parser.add_argument("--prefix", default="shot",
                        help="Filename prefix (default: 'shot')")
    args = parser.parse_args()

    # Setup output directory
    output_dir = args.output_dir or get_default_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    print(f"[Camera Capture] Starting...")
    print(f"  Platform:   {sys.platform}")
    print(f"  Camera:     {args.camera_index}")
    print(f"  Count:      {args.count}")
    print(f"  Interval:   {args.interval}s")
    print(f"  Output:     {output_dir}")
    print()

    # Open camera
    cap = open_camera(args.camera_index)
    if not cap.isOpened():
        print(f"ERROR: Cannot open camera {args.camera_index}", file=sys.stderr)
        sys.exit(1)

    # Warmup - discard initial frames for auto-exposure to settle
    print(f"Warming up camera ({args.warmup} frames)...")
    for i in range(args.warmup):
        cap.read()
        time.sleep(0.05)

    # Capture
    saved_paths = []
    for i in range(1, args.count + 1):
        ok, frame = cap.read()
        if not ok:
            print(f"ERROR: Failed to read frame {i}", file=sys.stderr)
            cap.release()
            sys.exit(2)

        filename = f"{args.prefix}{i}.jpg"
        path = os.path.join(output_dir, filename)

        if not cv2.imwrite(path, frame):
            print(f"ERROR: Failed to write {path}", file=sys.stderr)
            cap.release()
            sys.exit(3)

        saved_paths.append(path)
        print(f"  [{i}/{args.count}] Saved: {path}")

        if i < args.count:
            time.sleep(args.interval)

    cap.release()

    print()
    print(f"Done! Captured {len(saved_paths)} photos.")
    for p in saved_paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
