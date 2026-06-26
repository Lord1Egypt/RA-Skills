#!/usr/bin/env python3
"""诊断自动检测为什么失败"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

import platform
from comfyui_config import _get_detection_candidates, _windows_path_exists

print(f"Platform: {platform.system()}")
print()

candidates = _get_detection_candidates()
print(f"总候选路径数: {len(candidates)}")
print()

# 测试每个路径
found = []
not_found = []
for path in candidates:
    if not path:
        continue
    exists = _windows_path_exists(path)
    if exists:
        found.append(path)
        print(f"  [FOUND] {path}")
    elif path.startswith("H:"):
        # 只打印 H 盘的详细状态
        wsl_path = f"/mnt/h/{path[3:].replace(chr(92), '/')}"
        real_exists = os.path.exists(wsl_path)
        print(f"  [H盘] {path}")
        print(f"         WSL路径: {wsl_path}")
        print(f"         WSL exists: {real_exists}")
        print(f"         _windows_path_exists: {exists}")

print()
print(f"找到的路径数: {len(found)}")
for p in found:
    print(f"  {p}")

# 直接测试 H:\ 路径
print()
print("=== 直接测试 H:\\ 路径 ===")
direct = os.path.exists("H:\\ComfyUI-aki-v3\\ComfyUI\\main.py")
print(f"H:\\ComfyUI-aki-v3\\ComfyUI\\main.py exists: {direct}")
