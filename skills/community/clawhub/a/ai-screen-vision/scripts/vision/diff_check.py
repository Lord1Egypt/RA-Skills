#!/usr/bin/env python3
"""
Image diff detection for screen-vision skill.
Compares two screenshots to detect changes and determine if AI analysis is needed.
"""

import sys
import os

def compare_images(img1_path, img2_path, threshold=0.02):
    """
    Compare two screenshots and return change metrics.
    
    Args:
        img1_path: Path to first (old) screenshot
        img2_path: Path to second (new) screenshot
        threshold: Minimum change ratio to consider significant (0.0-1.0)
    
    Returns:
        dict: {
            "changed": bool,
            "change_ratio": float,
            "change_regions": list of (x, y, w, h),
            "crop_suggested": bool
        }
    """
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        # Fallback: basic file size comparison
        s1 = os.path.getsize(img1_path)
        s2 = os.path.getsize(img2_path)
        changed = abs(s2 - s1) / max(s1, 1) > 0.05
        return {
            "changed": changed,
            "change_ratio": abs(s2 - s1) / max(s1, 1),
            "change_regions": [],
            "crop_suggested": False,
            "method": "filesize"
        }
    
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    
    if img1.size != img2.size:
        return {
            "changed": True,
            "change_ratio": 1.0,
            "change_regions": [],
            "crop_suggested": False,
            "method": "size_mismatch"
        }
    
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    # Pixel-level diff
    diff = np.abs(arr1.astype(int) - arr2.astype(int))
    changed_pixels = np.any(diff > 30, axis=2)  # threshold per channel
    change_ratio = np.sum(changed_pixels) / changed_pixels.size
    
    # Find change regions using simple grid approach
    regions = find_change_regions(changed_pixels, img1.size)
    
    return {
        "changed": change_ratio > threshold,
        "change_ratio": float(change_ratio),
        "change_regions": regions,
        "crop_suggested": 0.02 < change_ratio < 0.3,
        "method": "pixel_diff"
    }


def find_change_regions(changed_pixels, img_size, grid_size=100):
    """Find rectangular regions with significant changes."""
    h, w = changed_pixels.shape
    regions = []
    
    for y in range(0, h, grid_size):
        for x in range(0, w, grid_size):
            region = changed_pixels[y:y+grid_size, x:x+grid_size]
            if np.mean(region) > 0.1:  # >10% pixels changed in this region
                regions.append((x, y, min(grid_size, w-x), min(grid_size, h-y)))
    
    return regions[:10]  # Limit to top 10 regions


def crop_to_changes(img_path, regions, padding=50):
    """Crop image to include only changed regions with padding."""
    try:
        from PIL import Image
    except ImportError:
        return img_path  # Can't crop without PIL
    
    if not regions:
        return img_path
    
    img = Image.open(img_path)
    w, h = img.size
    
    # Find bounding box of all regions
    min_x = max(0, min(r[0] for r in regions) - padding)
    min_y = max(0, min(r[1] for r in regions) - padding)
    max_x = min(w, max(r[0] + r[2] for r in regions) + padding)
    max_y = min(h, max(r[1] + r[3] for r in regions) + padding)
    
    cropped = img.crop((min_x, min_y, max_x, max_y))
    
    out_path = img_path.replace(".png", "_cropped.png")
    cropped.save(out_path)
    return out_path


if __name__ == "__main__":
    import json
    if len(sys.argv) < 3:
        print("Usage: diff_check.py <old_image> <new_image> [threshold]")
        sys.exit(1)
    
    old_img = sys.argv[1]
    new_img = sys.argv[2]
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
    
    result = compare_images(old_img, new_img, threshold)
    print(json.dumps(result, indent=2))
