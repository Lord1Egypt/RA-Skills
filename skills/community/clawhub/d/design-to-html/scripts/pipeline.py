#!/usr/bin/env python3
"""
Simple Python implementation for design-to-HTML pipeline
Uses PIL (Pillow) instead of heavy Node dependencies

Usage: python3 pipeline.py <original-image> [--threshold 95] [--iterations 5] [--output-dir output]
"""

import argparse
import os
import sys
from pathlib import Path
import json
from datetime import datetime

try:
    from PIL import Image
    import io
except ImportError:
    print("Installing Pillow...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image
    import io

def analyze_image(image_path):
    """Extract basic image information"""
    img = Image.open(image_path)
    
    width, height = img.size
    
    # Extract dominant colors (simplified)
    colors = []
    if img.mode == 'RGB':
        # Sample every 100th pixel
        pixels = list(img.getdata())
        sample_size = max(1, len(pixels) // 100)
        
        color_counts = {}
        for i in range(0, len(pixels), sample_size):
            r, g, b = pixels[i]
            # Quantize
            qr, qg, qb = (r // 32) * 32, (g // 32) * 32, (b // 32) * 32
            hex_color = f"#{qr:02x}{qg:02x}{qb:02x}"
            color_counts[hex_color] = color_counts.get(hex_color, 0) + 1
        
        # Top 5 colors
        colors = sorted(color_counts.items(), key=lambda x: -x[1])[:5]
        colors = [{"color": c, "count": n} for c, n in colors]
    
    return {
        "dimensions": {"width": width, "height": height},
        "colors": colors,
        "mode": img.mode,
        "timestamp": datetime.now().isoformat()
    }

def compare_images(original_path, rendered_path, output_path):
    """Pixel-level comparison"""
    orig = Image.open(original_path).convert('RGB')
    rend = Image.open(rendered_path).convert('RGB')
    
    if orig.size != rend.size:
        return {
            "matchScore": 0,
            "error": "Dimensions mismatch",
            "originalDimensions": orig.size,
            "renderedDimensions": rend.size
        }
    
    width, height = orig.size
    total_pixels = width * height
    
    # Compare pixel by pixel
    orig_data = list(orig.getdata())
    rend_data = list(rend.getdata())
    
    diff_pixels = 0
    diff_img = Image.new('RGB', (width, height))
    diff_data = []
    
    threshold = 32  # Allow some color variance
    
    for i in range(len(orig_data)):
        r1, g1, b1 = orig_data[i]
        r2, g2, b2 = rend_data[i]
        
        if abs(r1-r2) > threshold or abs(g1-g2) > threshold or abs(b1-b2) > threshold:
            diff_pixels += 1
            # Mark diff pixel as red
            diff_data.append((255, 0, 0))
        else:
            diff_data.append((0, 0, 0))
    
    diff_img.putdata(diff_data)
    diff_img.save(output_path)
    
    match_score = ((total_pixels - diff_pixels) / total_pixels) * 100
    
    return {
        "matchScore": round(match_score, 2),
        "diffPixels": diff_pixels,
        "totalPixels": total_pixels,
        "dimensions": {"width": width, "height": height}
    }

def generate_placeholder_html(analysis):
    """Generate basic HTML structure"""
    dims = analysis['dimensions']
    primary_color = analysis['colors'][0]['color'] if analysis['colors'] else '#FFFFFF'
    
    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: {dims['width']}px;
    height: {dims['height']}px;
    background: {primary_color};
    font-family: Arial, sans-serif;
}}
</style>
</head>
<body>
<div style="width: {dims['width']}px; height: {dims['height']}px;">
    <!-- Model will generate content based on design analysis -->
</div>
</body>
</html>'''

def run_pipeline(image_path, threshold=95, iterations=5, output_dir='output'):
    """Main pipeline"""
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("\n=== Design-to-HTML Pipeline ===\n")
    print(f"Input: {image_path}")
    print(f"Threshold: {threshold}%")
    print(f"Max iterations: {iterations}")
    print(f"Output: {output_dir}\n")
    
    # Step 1: Analyze
    print("[Step 1] Analyzing design...")
    analysis = analyze_image(image_path)
    
    analysis_file = output_path / 'analysis.json'
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"✓ Dimensions: {analysis['dimensions']['width']}x{analysis['dimensions']['height']}px")
    print(f"✓ Colors: {len(analysis['colors'])} detected\n")
    
    # Step 2: Generate placeholder
    initial_html = output_path / 'iteration_1.html'
    html_content = generate_placeholder_html(analysis)
    with open(initial_html, 'w') as f:
        f.write(html_content)
    
    print(f"[Step 2] Generated placeholder HTML: {initial_html}\n")
    
    print("Next: Model will iterate on HTML based on visual comparison")
    print("Use browser tool or puppeteer to render HTML and compare with original\n")
    
    # Note: Rendering requires external tool (puppeteer/playwright)
    # This script handles analysis and comparison only
    
    print("=== Pipeline Ready for Model Iteration ===")
    print(f"Analysis saved: {analysis_file}")
    print(f"Placeholder HTML: {initial_html}")
    print("\nInstructions for Agent:")
    print("1. Read analysis.json to understand design")
    print("2. Generate detailed HTML matching design")
    print("3. Use browser tool to render HTML")
    print("4. Compare with original image")
    print("5. Optimize based on diff report (repeat up to {iterations} times)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Design-to-HTML pipeline')
    parser.add_argument('image', help='Original design image')
    parser.add_argument('--threshold', type=int, default=95, help='Match threshold percentage')
    parser.add_argument('--iterations', type=int, default=5, help='Max iterations')
    parser.add_argument('--output-dir', default='output', help='Output directory')
    
    args = parser.parse_args()
    
    run_pipeline(args.image, args.threshold, args.iterations, args.output_dir)