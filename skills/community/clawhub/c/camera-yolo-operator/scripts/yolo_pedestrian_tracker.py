#!/usr/bin/env python3
"""
YOLO Object Tracker — 通用目标轨迹跟踪

Usage:
    python3 scripts/yolo_pedestrian_tracker.py --source 0 --seconds 30
    python3 scripts/yolo_pedestrian_tracker.py --source video.mp4 --track --output-video out.mp4
"""

import argparse
import cv2
import numpy as np
import os
import sys
from collections import defaultdict
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
OUTPUT_DIR = os.path.join(WORKSPACE, "projects", "camera-yolo-operator", "pedestrian_track")

YOLO_MODEL_PATH = os.environ.get(
    "YOLO_MODEL_PATH",
    os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "modules", "camera-yolo-operator", "yolo26s.pt")
)


def parse_args():
    parser = argparse.ArgumentParser(description="YOLO Object Tracker — 通用目标轨迹跟踪")
    parser.add_argument("--source", default="0", help="视频源: 0=摄像头, 或视频文件路径")
    parser.add_argument("--seconds", type=int, default=30, help="运行秒数（仅摄像头模式有效）")
    parser.add_argument("--yolo-model", default=YOLO_MODEL_PATH, help="YOLO 模型路径")
    parser.add_argument("--classes", nargs="+", type=int, default=None,
                        help="要检测的目标类别（默认全部检测）")
    parser.add_argument("--conf", type=float, default=0.5, help="检测置信度")
    parser.add_argument("--device", default="0", help="设备: 0=GPU, cpu=CPU")
    parser.add_argument("--save-every", type=int, default=5, help="截图保存间隔秒数（仅视频文件模式）")
    parser.add_argument("--max-saves", type=int, default=10, help="最大截图数量")
    parser.add_argument("--output-dir", default=OUTPUT_DIR, help="输出目录")
    parser.add_argument("--trail-length", type=int, default=30, help="轨迹线长度（帧数）")
    parser.add_argument("--track", action="store_true", help="开启轨迹跟踪模式（默认关闭）")
    parser.add_argument("--output-video", default=None, help="输出视频路径（不填则不保存视频）")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # 初始化 YOLO
    from ultralytics import YOLO
    print(f"[INFO] Loading YOLO: {args.yolo_model}")
    model = YOLO(args.yolo_model)
    names = model.names  # 类别名称映射

    # 初始化 Supervision 标注器
    import supervision as sv
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    byte_tracker = None
    trace_annotator = None
    if args.track:
        trace_annotator = sv.TraceAnnotator(
            trace_length=args.trail_length,
            position=sv.Position.CENTER,
        )
        byte_tracker = sv.ByteTrack(
            track_activation_threshold=0.25,
            lost_track_buffer=30,
            minimum_matching_threshold=0.8,
            frame_rate=30,
        )

    # 打开视频源
    source = int(args.source) if args.source.isdigit() else args.source
    print(f"[INFO] Opening source: {source}")
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open source: {source}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    is_video_file = not args.source.isdigit()
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if is_video_file else None
    print(f"[INFO] Resolution: {width}x{height}, FPS: {fps}")
    if is_video_file:
        print(f"[INFO] Video file, total frames: {total_frames}")

    # 输出视频写入器
    writer = None
    if args.output_video:
        writer = cv2.VideoWriter(
            args.output_video,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height),
        )
        print(f"[INFO] Writing annotated video to: {args.output_video}")

    # 统计变量
    start_time = cv2.getTickCount()
    frame_idx = 0
    save_count = 0
    last_save_tick = start_time
    last_save_frame = 0

    # 独立目标统计
    unique_tracks = {}       # track_id -> class_id（去重后的独立目标）
    track_history = defaultdict(list)  # track_id -> [(frame, cx, cy), ...]

    print(f"[INFO] Mode: {'tracking ON' if args.track else 'detection only'}, classes: all, starting...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Video ended or read error")
            break

        frame_idx += 1
        elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

        # YOLO 检测
        results = model(frame, classes=args.classes, conf=args.conf, device=args.device, verbose=False)
        detections = results[0]

        if detections.boxes is None or len(detections.boxes) == 0:
            det_obj = sv.Detections(
                xyxy=np.empty((0, 4)),
                confidence=np.empty((0,)),
                class_id=np.empty((0,), dtype=int),
            )
        else:
            det_obj = sv.Detections(
                xyxy=detections.boxes.xyxy.cpu().numpy(),
                confidence=detections.boxes.conf.cpu().numpy(),
                class_id=detections.boxes.cls.cpu().numpy().astype(int),
            )

        # 跟踪模式：ByteTrack 更新 ID
        if args.track and byte_tracker is not None:
            det_obj = byte_tracker.update_with_detections(det_obj)

            # 记录独立目标和轨迹
            if det_obj.tracker_id is not None:
                for tid, (x1, y1, x2, y2), cid in zip(
                        det_obj.tracker_id, det_obj.xyxy, det_obj.class_id):
                    tid_int = int(tid)
                    unique_tracks[tid_int] = int(cid)
                    cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                    track_history[tid_int].append((frame_idx, cx, cy))

        # 标注
        annotated = frame.copy()
        if args.track and trace_annotator is not None:
            annotated = trace_annotator.annotate(annotated, det_obj)

        annotated = box_annotator.annotate(annotated, det_obj)

        if args.track and det_obj.tracker_id is not None:
            labels = [f"#{int(tid)}" for tid in det_obj.tracker_id]
            annotated = label_annotator.annotate(annotated, det_obj, labels)

        # 写入输出视频
        if writer is not None:
            writer.write(annotated)

        # 实时显示
        cv2.imshow("Tracker [q=quit]" if args.track else "Detector [q=quit]", annotated)

        # 保存截图（视频文件模式，每隔 save_every 秒保存一张）
        if is_video_file and args.output_video:
            save_interval_frames = int(fps * args.save_every)
            frames_since_last_save = frame_idx - last_save_frame
            if frames_since_last_save >= save_interval_frames and save_count < args.max_saves:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                out_path = os.path.join(args.output_dir, f"frame_{ts}.jpg")
                cv2.imwrite(out_path, annotated)
                print(f"[SAVE] {out_path}")
                save_count += 1
                last_save_frame = frame_idx

        # 超时退出（仅摄像头模式）
        if not is_video_file and elapsed >= args.seconds:
            print(f"[INFO] Time limit ({args.seconds}s) reached")
            break

        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), 27):
            print("[INFO] Quit by user")
            break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()

    # 打印统计摘要（独立目标数量）
    print(f"\n========== Video Summary ==========")
    print(f"Frames: {frame_idx}, Duration: {frame_idx / fps:.1f}s")

    if args.track and unique_tracks:
        # 按类别汇总独立目标数量
        class_track_counts = defaultdict(list)
        for tid, cid in unique_tracks.items():
            class_track_counts[names[cid]].append(tid)

        total_unique = len(unique_tracks)
        print(f"\n独立目标数量（共 {total_unique} 个）：")
        for cls_name, tids in sorted(class_track_counts.items(), key=lambda x: -len(x[1])):
            print(f"  {cls_name}: {len(tids)} 个")

        # 跟踪最久的 Top 5
        if track_history:
            print(f"\n跟踪最久的目标 Top 5：")
            for tid, history in sorted(track_history.items(), key=lambda x: -len(x[1]))[:5]:
                cid = unique_tracks.get(tid, '?')
                name = names.get(cid, str(cid))
                print(f"  #{tid} ({name}): {len(history)} 帧")

    print(f"\nOutput video: {args.output_video}" if args.output_video else "(no video saved)")
    if save_count > 0:
        print(f"Screenshots: {save_count} frames saved to {args.output_dir}")


if __name__ == "__main__":
    main()
