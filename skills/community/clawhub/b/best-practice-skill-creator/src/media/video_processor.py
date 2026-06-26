"""Extract frames from video files for MLLM analysis."""

import base64
import io
from pathlib import Path

import cv2
from PIL import Image


def extract_frames_from_video(
    video_path: str,
    max_frames: int = 30,
    frame_interval_sec: int = 2,
    max_resolution: tuple[int, int] = (1280, 720),
) -> list[str]:
    """Extract frames from a video file and return as base64-encoded JPEGs.

    Args:
        video_path: Path to the video file.
        max_frames: Maximum number of frames to extract.
        frame_interval_sec: Seconds between extracted frames.
        max_resolution: Maximum (width, height) for resizing.

    Returns:
        List of base64-encoded JPEG strings.
    """
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_step = int(fps * frame_interval_sec)

    if frame_step < 1:
        frame_step = 1

    frames_b64: list[str] = []
    frame_idx = 0

    while frame_idx < total_frames and len(frames_b64) < max_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR -> RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # Resize to fit within max_resolution
        img.thumbnail(max_resolution, Image.LANCZOS)

        # Encode to base64 JPEG
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        frames_b64.append(b64)

        frame_idx += frame_step

    cap.release()

    if not frames_b64:
        raise RuntimeError(f"No frames could be extracted from: {video_path}")

    return frames_b64
