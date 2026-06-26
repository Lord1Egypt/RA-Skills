#!/usr/bin/env python3
"""
ComfyUI DirectML AMD - Automatic Fix Script
Applies all necessary patches for DirectML compatibility on AMD GPUs.
"""

import os
import sys
import shutil
from pathlib import Path

def backup_file(filepath):
    """Create backup of file before modification."""
    backup_path = f"{filepath}.backup"
    if not os.path.exists(backup_path):
        shutil.copy2(filepath, backup_path)
        print(f"✓ Backup created: {backup_path}")
    return backup_path

def fix_model_patcher_line_326(filepath):
    """Fix line ~326 - aimdo_mem assignment."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: Broken comment (previous failed fix)
    old_pattern1 = "aimdo_mem = # [AMD DirectML]  comfy_aimdo.model_vbar.vbars_analyze()"
    new_pattern1 = """        # [AMD DirectML] Disabled - comfy_aimdo not available
        # aimdo_mem = comfy_aimdo.model_vbar.vbars_analyze()
        aimdo_mem = 0"""
    
    # Pattern 2: Original code
    old_pattern2 = "aimdo_mem = comfy_aimdo.model_vbar.vbars_analyze()"
    
    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_pattern1)
        print("✓ Fixed broken comment (line ~326)")
        return True, content
    elif old_pattern2 in content:
        content = content.replace(old_pattern2, new_pattern1)
        print("✓ Fixed aimdo_mem assignment (line ~326)")
        return True, content
    else:
        print("⚠ Line 326 already fixed or not found")
        return False, content

def fix_model_patcher_line_1512(filepath):
    """Fix line ~1512 - vbar assignment."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: Broken comment (previous failed fix)
    old_pattern1 = "vbar = # [AMD DirectML]  comfy_aimdo.model_vbar.ModelVBAR(self.model_size() * 10, self.load_device.index)"
    new_pattern1 = """            # [AMD DirectML] Disabled - comfy_aimdo not available
            # vbar = comfy_aimdo.model_vbar.ModelVBAR(self.model_size() * 10, self.load_device.index)
            vbar = None"""
    
    # Pattern 2: Original code
    old_pattern2 = "vbar = comfy_aimdo.model_vbar.ModelVBAR(self.model_size() * 10, self.load_device.index)"
    
    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_pattern1)
        print("✓ Fixed broken comment (line ~1512)")
        return True, content
    elif old_pattern2 in content:
        content = content.replace(old_pattern2, new_pattern1)
        print("✓ Fixed vbar assignment (line ~1512)")
        return True, content
    else:
        print("⚠ Line 1512 already fixed or not found")
        return False, content

def main():
    print("=" * 60)
    print("ComfyUI DirectML AMD - Automatic Fix Script")
    print("=" * 60)
    
    # Find ComfyUI installation
    possible_paths = [
        r"C:\ComfyUI",
        os.path.expanduser("~\\ComfyUI"),
        os.environ.get("COMFYUI_PATH", ""),
        os.getcwd()
    ]
    
    comfyui_dir = None
    for path in possible_paths:
        if os.path.exists(path) and os.path.exists(os.path.join(path, "main.py")):
            comfyui_dir = path
            break
    
    if not comfyui_dir:
        print("❌ ComfyUI installation not found!")
        print("Please run this script from ComfyUI directory or set COMFYUI_PATH")
        sys.exit(1)
    
    print(f"✓ Found ComfyUI: {comfyui_dir}")
    
    model_patcher = os.path.join(comfyui_dir, "comfy", "model_patcher.py")
    
    if not os.path.exists(model_patcher):
        print(f"❌ model_patcher.py not found at {model_patcher}")
        sys.exit(1)
    
    print(f"\n📁 Patching: {model_patcher}")
    
    # Create backup
    backup_file(model_patcher)
    
    # Apply fixes
    fixed_326, content = fix_model_patcher_line_326(model_patcher)
    
    # Write intermediate result
    with open(model_patcher, 'w', encoding='utf-8') as f:
        f.write(content)
    
    fixed_1512, content = fix_model_patcher_line_1512(model_patcher)
    
    # Write final result
    with open(model_patcher, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "=" * 60)
    if fixed_326 or fixed_1512:
        print("✅ All fixes applied successfully!")
        print("\n📝 Next steps:")
        print("   1. Install torch-directml:")
        print(f"      cd {comfyui_dir}")
        print("      .venv\\Scripts\\python.exe -m pip install torch-directml")
        print("\n   2. Start ComfyUI:")
        print(f"      .venv\\Scripts\\python.exe main.py --directml --port 8188")
    else:
        print("⚠ No fixes needed (already applied)")
    print("=" * 60)

if __name__ == "__main__":
    main()
