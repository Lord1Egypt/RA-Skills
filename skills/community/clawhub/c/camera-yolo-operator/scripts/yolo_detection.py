#!/usr/bin/env python3
"""
YOLO Detection - Webcam + YOLO model for object detection.
Supports all YOLO models (detection, segmentation, pose, OBB, classification).
"""
import argparse
import os
import sys
import time
from pathlib import Path

import cv2
import torch
from ultralytics import YOLO

# ── Platform Detection ───────────────────────────────────────────────────────
IS_WINDOWS = sys.platform == "win32" or sys.platform == "cygwin"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"

# ── Default Paths ─────────────────────────────────────────────────────────────
def get_default_model_path():
    """Get default YOLO model path from the shared model cache."""
    return os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "modules",
                        "camera-yolo-operator", "yolo26s.pt")


def get_default_output_dir():
    """Get default output directory in workspace projects folder."""
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                               os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return os.path.join(workspace, "projects", "camera-yolo-operator", "detection")


def get_skill_dir():
    """Get the skill directory based on this script's location."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_model_search_paths():
    """Get search paths for YOLO models, in priority order."""
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                               os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return [
        # 1. Explicit path from env or default
        os.environ.get("YOLO_MODEL_PATH", ""),
        # 2. Shared model cache (skill folders must not contain model files)
        os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "modules",
                     "camera-yolo-operator"),
        # 3. Legacy workspace yolo folder
        os.path.join(workspace, "yolo"),
        # 4. Current working directory
        ".",
    ]


def find_model(model_name_or_path):
    """
    Find model file given a name or path.
    Searches in standard locations.
    """
    path = Path(model_name_or_path)

    # If it's an absolute path and exists, use it
    if path.is_absolute() and path.exists():
        return str(path)

    # If it's just a filename, search in standard locations
    if path.suffix.lower() in ['.pt', '.pth', '.yolo']:
        for search_dir in get_model_search_paths():
            if not search_dir:
                continue
            candidate = Path(search_dir) / path.name
            if candidate.exists():
                return str(candidate)

    # Try as-is path
    if path.exists():
        return str(path)

    return model_name_or_path  # Return original, let YOLO handle error


# ── Camera Opening ────────────────────────────────────────────────────────────
def open_camera(index: int):
    """Try multiple backends to open the camera."""
    if IS_WINDOWS:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
        cap.release()

    if IS_LINUX:
        cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
        if cap.isOpened():
            return cap
        cap.release()

    if IS_MACOS:
        cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            return cap
        cap.release()

    cap = cv2.VideoCapture(index)
    return cap


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="YOLO object detection on webcam feed with periodic snapshots."
    )
    parser.add_argument("--camera-index", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--seconds", type=int, default=30, help="Runtime in seconds (default: 30)")
    parser.add_argument("--save-every", type=float, default=10.0,
                        help="Save snapshot every N seconds (default: 10.0)")
    parser.add_argument("--max-saves", type=int, default=3,
                        help="Maximum number of saves (default: 3)")
    parser.add_argument("--conf", type=float, default=0.5,
                        help="YOLO confidence threshold (default: 0.5)")
    parser.add_argument("--yolo-model", default=None,
                        help=f"YOLO model path or name (default: yolo26s.pt in model cache)")
    parser.add_argument("--output-dir", default=None,
                        help=f"Output directory (default: ~/.../projects/camera-yolo-operator/detection)")
    parser.add_argument("--device", default="0",
                        help="Device: '0' for GPU, 'cpu' for CPU (default: '0')")
    parser.add_argument("--no-display", action="store_true",
                        help="Don't display window (headless mode)")
    args = parser.parse_args()

    # Resolve model path
    model_path = args.yolo_model or get_default_model_path()
    model_path = find_model(model_path)

    # Setup output
    output_dir = args.output_dir or get_default_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # Check model exists
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found: {model_path}", file=sys.stderr)
        print(f"Search paths: {get_model_search_paths()}", file=sys.stderr)
        print(f"\nRun scripts/download_models.sh to download models.", file=sys.stderr)
        sys.exit(1)

    # Load model
    print(f"[YOLO Detection] Starting...")
    print(f"  Model:      {model_path}")
    print(f"  Camera:     {args.camera_index}")
    print(f"  Runtime:    {args.seconds}s")
    print(f"  Device:     {args.device}")
    print(f"  Output:     {output_dir}")
    print(f"  PyTorch:    {torch.__version__}")
    print(f"  CUDA:       {torch.cuda.is_available()}")
    print()

    yolo = YOLO(model_path)

    # Open camera
    cap = open_camera(args.camera_index)
    if not cap.isOpened():
        print(f"ERROR: Cannot open camera {args.camera_index}", file=sys.stderr)
        sys.exit(2)

    # Warmup
    print("Warming up...")
    for _ in range(5):
        cap.read()

    # Run detection
    start = time.time()
    last_save_at = start
    save_count = 0
    detected_labels = set()
    saved_paths = []

    print(f"Running for {args.seconds}s, saving every {args.save_every}s...")
    print()

    window_name = "YOLO Detection (Press 'q' to quit)"

    while time.time() - start < args.seconds:
        ok, frame = cap.read()
        if not ok:
            print("Camera read error, exiting.")
            break

        # Run detection
        results = yolo(frame, conf=args.conf, verbose=False, device=args.device)
        annotated = results[0].plot()

        # Collect labels
        if results and results[0].boxes is not None and len(results[0].boxes) > 0:
            for cls in results[0].boxes.cls.cpu().numpy():
                detected_labels.add(results[0].names[int(cls)])

        # Display
        if not args.no_display:
            cv2.imshow(window_name, annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("User pressed 'q', stopping.")
                break

        # Save periodically
        now = time.time()
        if save_count < args.max_saves and now - last_save_at >= args.save_every:
            save_count += 1
            filename = f"yolo_det_{save_count}.jpg"
            path = os.path.join(output_dir, filename)
            cv2.imwrite(path, annotated)
            saved_paths.append(path)
            print(f"  [{save_count}/{args.max_saves}] Saved: {path}")
            last_save_at = now

    cap.release()
    if not args.no_display:
        cv2.destroyAllWindows()

    print()
    print(f"Done! Captured {len(saved_paths)} images.")
    print(f"Detected objects: {', '.join(sorted(detected_labels)) if detected_labels else 'none'}")
    print()
    for p in saved_paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
