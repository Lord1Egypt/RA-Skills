#!/usr/bin/env python3
"""
YOLO Detection + DA3Metric Depth Estimation with Distance Overlay.
Combines YOLO bounding boxes with metric depth estimation.
Each detection box shows: class name + confidence + distance in meters.
"""
import argparse
import os
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import torch

from depth_anything_3.api import DepthAnything3
from ultralytics import YOLO

# ── Platform Detection ───────────────────────────────────────────────────────
IS_WINDOWS = sys.platform == "win32" or sys.platform == "cygwin"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"

# ── Default Paths ─────────────────────────────────────────────────────────────
def get_default_yolo_model_path():
    """Get default YOLO model path from the shared model cache."""
    return os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "modules",
                        "camera-yolo-operator", "yolo26s.pt")


def get_default_output_dir():
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                               os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return os.path.join(workspace, "projects", "camera-yolo-operator", "depth_distance")


def get_skill_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_model_search_paths():
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                               os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return [
        os.environ.get("YOLO_MODEL_PATH", ""),
        os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "modules",
                     "camera-yolo-operator"),
        os.path.join(workspace, "yolo"),
        ".",
    ]


def find_model(model_name_or_path):
    path = Path(model_name_or_path)
    if path.is_absolute() and path.exists():
        return str(path)
    if path.suffix.lower() in ['.pt', '.pth', '.yolo']:
        for search_dir in get_model_search_paths():
            if not search_dir:
                continue
            candidate = Path(search_dir) / path.name
            if candidate.exists():
                return str(candidate)
    if path.exists():
        return str(path)
    return model_name_or_path


# ── Camera Opening ────────────────────────────────────────────────────────────
def open_camera(index: int):
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
        description="YOLO detection + DA3Metric depth estimation with distance overlay."
    )
    parser.add_argument("--camera-index", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--seconds", type=int, default=30, help="Runtime in seconds (default: 30)")
    parser.add_argument("--save-every", type=float, default=5.0,
                        help="Save snapshot every N seconds (default: 5.0)")
    parser.add_argument("--max-saves", type=int, default=6,
                        help="Maximum number of saves (default: 6)")
    parser.add_argument("--conf", type=float, default=0.5,
                        help="YOLO confidence threshold (default: 0.5)")
    parser.add_argument("--depth-scale", type=float, default=1.0,
                        help="Depth calibration scale factor. "
                             "E.g. real=3m, reads=1.9m → scale=3.0/1.9≈1.574 (default: 1.0)")
    parser.add_argument("--yolo-model", default=None,
                        help="YOLO model path (default: yolo26s.pt)")
    parser.add_argument("--depth-model", default="depth-anything/DA3Metric-Large",
                        help="Depth model (default: depth-anything/DA3Metric-Large)")
    parser.add_argument("--output-dir", default=None,
                        help=f"Output directory (default: ~/.../projects/camera-yolo-operator/depth_distance)")
    parser.add_argument("--device", default="cuda:0",
                        help="Device for depth model (default: cuda:0)")
    parser.add_argument("--no-display", action="store_true", help="Headless mode")
    args = parser.parse_args()

    # Resolve paths
    yolo_model_path = find_model(args.yolo_model or get_default_yolo_model_path())
    output_dir = args.output_dir or get_default_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # Check YOLO model
    if not os.path.exists(yolo_model_path):
        print(f"ERROR: YOLO model not found: {yolo_model_path}", file=sys.stderr)
        print(f"\nRun scripts/download_models.sh to download models.", file=sys.stderr)
        sys.exit(1)

    # Load models
    print(f"[YOLO + Depth] Starting...")
    print(f"  YOLO Model:   {yolo_model_path}")
    print(f"  Depth Model:  {args.depth_model}")
    print(f"  Camera:       {args.camera_index}")
    print(f"  Runtime:      {args.seconds}s")
    print(f"  Depth Scale:  {args.depth_scale}")
    print(f"  Output:       {output_dir}")
    print()

    # Load YOLO
    print("Loading YOLO model...")
    yolo = YOLO(yolo_model_path)

    # Load Depth model (auto-downloads from HuggingFace on first run)
    print("Loading depth model (may download from HuggingFace on first run)...")
    print("  TIP: Run 'unset all_proxy ALL_PROXY' if download is slow/fails")
    print("  Or:  export HF_ENDPOINT=https://hf-mirror.com")

    # Check for proxy issues
    proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY',
                  'all_proxy', 'ALL_PROXY']
    active_proxies = [v for v in proxy_vars if os.environ.get(v)]
    if active_proxies:
        print(f"  [WARN] Active proxy env vars detected: {active_proxies}")
        print(f"         These may interfere with HuggingFace downloads.")

    depth_model = DepthAnything3.from_pretrained(args.depth_model)
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    depth_model = depth_model.to(device=device)
    print(f"  Depth model loaded on: {device}")
    print(f"  PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}")

    # Open camera
    cap = open_camera(args.camera_index)
    if not cap.isOpened():
        print(f"ERROR: Cannot open camera {args.camera_index}", file=sys.stderr)
        sys.exit(2)

    # Warmup
    print("Warming up camera and models...")
    for _ in range(5):
        cap.read()

    print(f"\nRunning for {args.seconds}s, saving every {args.save_every}s...")
    print("(Press 'q' in window or wait for timeout)")
    print()

    start = time.time()
    last_save_at = start
    save_count = 0
    saved_paths = []
    window_name = "YOLO + Depth Distance (Press 'q' to quit)"

    while time.time() - start < args.seconds:
        ok, frame = cap.read()
        if not ok:
            print("Camera read error.")
            break

        # ── YOLO Detection ──────────────────────────────────────────────
        det_results = yolo(frame, conf=args.conf, verbose=False, device=0)
        det = det_results[0]

        # ── Depth Estimation ─────────────────────────────────────────────
        depth_pred = depth_model.inference([frame])
        depth_map = depth_pred.depth[0]  # [H, W] in meters

        # ── Draw Annotations ─────────────────────────────────────────────
        annotated = frame.copy()

        if det.boxes is not None and len(det.boxes) > 0:
            for i in range(len(det.boxes)):
                cls_id = int(det.boxes.cls[i].item())
                conf = float(det.boxes.conf[i].item())
                name = det.names[cls_id]

                # Bounding box
                x1, y1, x2, y2 = det.boxes.xyxy[i].cpu().numpy().astype(int)

                # Center point
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Get depth at center
                h, w = depth_map.shape
                cx_clip = np.clip(cx, 0, w - 1)
                cy_clip = np.clip(cy, 0, h - 1)
                depth_m = float(depth_map[cy_clip, cx_clip]) * args.depth_scale

                # Label: class + confidence + distance
                label = f"{name} {conf:.2f} | {depth_m:.1f}m"

                # Draw box and label
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated, label, (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

        # ── Depth Colormap Overlay ──────────────────────────────────────
        depth_calibrated = depth_map * args.depth_scale
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs((depth_calibrated / max(depth_calibrated.max(), 1e-6) * 255).astype(np.uint8)),
            cv2.COLORMAP_INFERNO
        )
        depth_colormap = cv2.resize(depth_colormap, (frame.shape[1], frame.shape[0]))
        alpha = 0.35
        annotated = cv2.addWeighted(annotated, 1, depth_colormap, alpha, 0)

        # Display
        if not args.no_display:
            cv2.imshow(window_name, annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("User pressed 'q'.")
                break

        # Save periodically
        now = time.time()
        if save_count < args.max_saves and now - last_save_at >= args.save_every:
            save_count += 1
            path = os.path.join(output_dir, f"yolo_depth_{save_count}.jpg")
            cv2.imwrite(path, annotated)
            saved_paths.append(path)
            print(f"  [{save_count}/{args.max_saves}] Saved: {path}")
            last_save_at = now

    cap.release()
    if not args.no_display:
        cv2.destroyAllWindows()

    print()
    print(f"Done! Saved {len(saved_paths)} images to {output_dir}")
    if saved_paths:
        print("Output files:")
        for p in saved_paths:
            print(f"  {p}")


if __name__ == "__main__":
    main()
