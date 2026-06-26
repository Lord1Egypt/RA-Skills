"""
Box Data Collection - English path only
Fix: Chinese path encoding issue
"""

import pyrealsense2 as rs
import numpy as np
import cv2
import os
import json
from datetime import datetime

# 使用纯英文路径
BASE_DIR = r"C:\Users\Administrator\.openclaw\workspace\box_dataset"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
dataset_name = f"box_{timestamp}"  # 纯英文
dataset_dir = os.path.join(BASE_DIR, dataset_name)
raw_data_dir = os.path.join(dataset_dir, "raw_data")
os.makedirs(raw_data_dir, exist_ok=True)

print("=" * 60)
print("Box Data Collection - English Path Version")
print("=" * 60)
print(f"Save to: {dataset_dir}")
print("")
print("Controls:")
print("  [S] = Save 1 frame")
print("  [A] = Auto save 10 frames (5s interval)")
print("  [Q] = Quit")
print("=" * 60)

# Save config
with open(os.path.join(dataset_dir, "dataset_config.json"), "w") as f:
    json.dump({
        "dataset_name": dataset_name,
        "box_type": "box",
        "capture_date": datetime.now().isoformat(),
        "camera": "Intel RealSense D455",
    }, f, indent=2)

# Init camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)

# Save intrinsics
intrinsics = profile.get_stream(rs.stream.depth).as_video_stream_profile().intrinsics
with open(os.path.join(dataset_dir, "camera_intrinsic.json"), "w") as f:
    json.dump({
        "fx": float(intrinsics.fx),
        "fy": float(intrinsics.fy),
        "ppx": float(intrinsics.ppx),
        "ppy": float(intrinsics.ppy),
        "width": 640,
        "height": 480,
    }, f, indent=2)

print(f"Camera ready. Intrinsics: fx={intrinsics.fx:.1f}, fy={intrinsics.fy:.1f}")
print("=" * 60)

frame_count = 0

while True:
    frames = pipeline.wait_for_frames(timeout_ms=3000)
    if not frames:
        continue
    
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    
    if not depth_frame or not color_frame:
        continue
    
    # Get raw data
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    
    # Display with overlay
    display = color_image.copy()
    h, w = display.shape[:2]
    
    center_depth = depth_frame.get_distance(w//2, h//2)
    status = "OK" if 0.5 <= center_depth <= 2.5 else "ADJUST"
    color = (0, 255, 0) if status == "OK" else (0, 0, 255)
    
    cv2.putText(display, f"Depth: {center_depth:.3f}m [{status}]", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(display, f"Saved: {frame_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(display, "[S]Save [A]Auto10 [Q]Quit", (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.imshow('RGB Camera', display)
    cv2.imshow('Depth', cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET))
    
    key = cv2.waitKey(100) & 0xFF
    
    if key == ord('s') or key == ord('S'):
        frame_count += 1
        fid = f"{frame_count:06d}"
        
        # Save Color.png
        color_path = os.path.join(raw_data_dir, f"{fid}_Color.png")
        print(f"\nSaving Color: {color_path}")
        ret_color = cv2.imwrite(color_path, color_image)
        
        # Save Depth.raw
        depth_path = os.path.join(raw_data_dir, f"{fid}_Depth.raw")
        print(f"Saving Depth: {depth_path}")
        depth_image.astype(np.uint16).tofile(depth_path)
        
        # Verify
        color_ok = os.path.exists(color_path)
        depth_ok = os.path.exists(depth_path)
        
        print(f"Result: Color={'OK' if color_ok else 'FAIL'}, Depth={'OK' if depth_ok else 'FAIL'}")
        if color_ok:
            print(f"Color size: {os.path.getsize(color_path)} bytes")
        if depth_ok:
            print(f"Depth size: {os.path.getsize(depth_path)} bytes")
        print(f"Total saved: {frame_count}\n")
    
    elif key == ord('a') or key == ord('A'):
        print("\n" + "=" * 50)
        print("Auto save 10 frames, 5 seconds interval")
        print("Move the box between captures!")
        print("=" * 50)
        
        for i in range(10):
            # 5 second countdown
            print(f"\nFrame {i+1}/10:")
            for cd in range(5, 0, -1):
                print(f"  Countdown: {cd}s - MOVE THE BOX!", end="\r")
                cv2.waitKey(1000)
            print("                              ")  # Clear line
            
            frames = pipeline.wait_for_frames(timeout_ms=3000)
            if frames:
                frame_count += 1
                fid = f"{frame_count:06d}"
                
                d = np.asanyarray(frames.get_depth_frame().get_data())
                c = np.asanyarray(frames.get_color_frame().get_data())
                
                color_path = os.path.join(raw_data_dir, f"{fid}_Color.png")
                depth_path = os.path.join(raw_data_dir, f"{fid}_Depth.raw")
                
                cv2.imwrite(color_path, c)
                d.astype(np.uint16).tofile(depth_path)
                
                if os.path.exists(color_path):
                    print(f"  OK #{frame_count}: {fid} - Color: {os.path.getsize(color_path)} bytes")
                else:
                    print(f"  FAIL #{frame_count}: {fid}")
        
        print("\n" + "=" * 50)
        print(f"Auto capture done! Total: {frame_count}")
        print("=" * 50 + "\n")
    
    elif key == ord('q') or key == ord('Q'):
        break

pipeline.stop()
cv2.destroyAllWindows()

# Save stats
with open(os.path.join(dataset_dir, "capture_stats.json"), "w") as f:
    json.dump({"total_frames": frame_count}, f, indent=2)

print(f"\nDone! Total: {frame_count} frames")
print(f"Location: {dataset_dir}")

# Open folder
os.startfile(dataset_dir)