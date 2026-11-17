#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capture.py — 桌宠摄像头截图脚本（pet-camera-vision Skill 的感知部分）

职责：稳定截取一帧画面，保存为 JPG，输出结构化信息（stdout JSON）。
设计：多后端自动回退，适配树莓派 Camera Module / USB 摄像头 / 开发机摄像头。

后端优先级：
  1. libcamera-still  （树莓派 Camera Module）
  2. fswebcam         （USB 摄像头，Linux）
  3. OpenCV           （通用，Windows/macOS 开发机也能用）

离线演示：--synthetic 生成一张合成测试图（无需摄像头）。

用法示例：
  python3 capture.py --outdir captures
  python3 capture.py --device /dev/video0 --resolution 1920x1080
  python3 capture.py --synthetic --outdir captures   # 离线演示
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8), "CST")


def now_str():
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S%z")


def run(cmd, timeout=30):
    """执行外部命令，返回 (returncode, stdout, stderr)。"""
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError:
        return 127, "", "command not found: %s" % cmd[0]
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def which(name):
    return shutil.which(name) is not None


def backend_libcamera(out_path, device, resolution):
    if not which("libcamera-still"):
        return None, "libcamera-still not found"
    cmd = ["libcamera-still", "-o", out_path, "-n", "--width", str(resolution[0]), "--height", str(resolution[1])]
    if device and str(device).isdigit():
        cmd += ["--camera", str(device)]
    rc, _, err = run(cmd)
    if rc != 0 or not os.path.exists(out_path):
        return None, err.strip() or "libcamera-still failed (rc=%d)" % rc
    return "libcamera-still", ""


def backend_fswebcam(out_path, device, resolution):
    if not which("fswebcam"):
        return None, "fswebcam not found"
    cmd = ["fswebcam", "-q", "-r", "%dx%d" % resolution]
    if device:
        cmd += ["-d", str(device)]
    cmd += [out_path]
    rc, _, err = run(cmd)
    if rc != 0 or not os.path.exists(out_path):
        return None, err.strip() or "fswebcam failed (rc=%d)" % rc
    return "fswebcam", ""


def backend_opencv(out_path, device, resolution):
    try:
        import cv2
    except ImportError:
        return None, "opencv-python not installed"
    idx = 0
    if device is not None:
        if str(device).isdigit():
            idx = int(device)
        else:
            # /dev/videoX 在 OpenCV 中按序号尝试
            idx = 0
    cap = cv2.VideoCapture(idx)
    if not cap.isOpened():
        cap.release()
        return None, "cannot open camera index %s" % device
    try:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        ok, frame = cap.read()
        if not ok or frame is None:
            return None, "failed to read frame"
        ok = cv2.imwrite(out_path, frame)
        if not ok:
            return None, "failed to write %s" % out_path
        return "opencv", ""
    finally:
        cap.release()


def make_synthetic(out_path, resolution):
    """无摄像头时生成合成测试图：渐变背景 + 圆形"人脸"色块。"""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None, "Pillow not installed (needed for --synthetic)"
    w, h = resolution
    img = Image.new("RGB", (w, h), (30, 41, 59))
    d = ImageDraw.Draw(img)
    # 背景渐变（蓝色 → 暖色，便于颜色识别演示）
    for y in range(h):
        ratio = y / h
        r = int(30 + ratio * 200)
        g = int(41 + ratio * 90)
        b = int(59 + ratio * 40)
        d.line([(0, y), (w, y)], fill=(r, g, b))
    # 中央"人脸"：肤色圆 + 眼睛 + 嘴（笑脸）
    cx, cy, r = w // 2, h // 2, int(min(w, h) * 0.22)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 200, 160))
    ey, er = cy - r // 3, r // 7
    d.ellipse([cx - r // 2 - er, ey - er, cx - r // 2 + er, ey + er], fill=(30, 30, 30))
    d.ellipse([cx + r // 2 - er, ey - er, cx + r // 2 + er, ey + er], fill=(30, 30, 30))
    d.arc([cx - r // 2, cy + r // 6, cx + r // 2, cy + r // 2], 0, 180, fill=(30, 30, 30), width=max(3, r // 12))
    img.save(out_path, "JPEG", quality=92)
    return "synthetic", ""


BACKENDS = [backend_libcamera, backend_fswebcam, backend_opencv]


def main():
    ap = argparse.ArgumentParser(description="桌宠摄像头截图")
    ap.add_argument("--outdir", default=os.environ.get("PET_CAMERA_OUTDIR", "captures"),
                    help="截图保存目录（默认 captures，可用环境变量 PET_CAMERA_OUTDIR）")
    ap.add_argument("--device", default=os.environ.get("PET_CAMERA_INDEX", None),
                    help="摄像头设备：数字索引（0）或 /dev/videoX")
    ap.add_argument("--resolution", default=os.environ.get("PET_CAMERA_RESOLUTION", "1280x720"),
                    help="分辨率，默认 1280x720")
    ap.add_argument("--filename", default=None, help="自定义文件名（不含扩展名）")
    ap.add_argument("--synthetic", action="store_true", help="离线演示：生成合成测试图，不调用摄像头")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    try:
        rw, rh = (int(x) for x in args.resolution.lower().split("x"))
    except Exception:
        sys.stderr.write("分辨率格式错误：%s（应为 宽x高）\n" % args.resolution)
        return 2
    resolution = (rw, rh)

    name = args.filename or datetime.now(CST).strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(args.outdir, name + ".jpg")

    if args.synthetic:
        backend, err = make_synthetic(out_path, resolution)
        if backend is None:
            print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
            return 1
        result = {"status": "ok", "path": out_path, "backend": backend,
                  "resolution": "%dx%d" % resolution, "timestamp": now_str(),
                  "note": "synthetic test image (offline demo)"}
        print(json.dumps(result, ensure_ascii=False))
        return 0

    errors = []
    for backend_fn in BACKENDS:
        backend, err = backend_fn(out_path, args.device, resolution)
        if backend is not None:
            result = {"status": "ok", "path": out_path, "backend": backend,
                      "resolution": "%dx%d" % resolution, "timestamp": now_str()}
            print(json.dumps(result, ensure_ascii=False))
            return 0
        errors.append(err)
    # 全部失败：提示并给建议
    print(json.dumps({
        "status": "error",
        "message": "所有截图后端均失败",
        "details": errors,
        "hint": "检查摄像头连接；或使用 --synthetic 离线演示",
    }, ensure_ascii=False), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
