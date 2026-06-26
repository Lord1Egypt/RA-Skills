#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

#!/usr/bin/env python3
"""
workflow_html2pptx.py - Complete workflow: HTML → PNG → PPTX

This is the main entry point for doc-to-ppt skill.
Generates PPTX by:
1. Rendering HTML slides with content
2. Converting HTML to PNG using Chrome headless
3. Creating PPTX with PNG images as slide backgrounds
"""

import argparse
import json
import os
import sys
from subprocess import run as _run, TimeoutExpired as _Timeout
from pathlib import Path
from datetime import datetime

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))

import generate_html
import html2png_batch
import png2pptx


def find_renderer():
    """Find Chrome executable"""
    return html2png_batch.find_renderer()


def workflow(pdf_content: dict, slide_structure: dict, output_path: str, 
             temp_dir: str = None, style: dict = None):
    """
    Complete workflow: PDF content → HTML → PNG → PPTX
    
    Args:
        pdf_content: Processed PDF content (from read_content.py)
        slide_structure: Slide structure with template assignments
        output_path: Final PPTX output path
        temp_dir: Directory for intermediate files (HTML, PNG)
        style: Optional style overrides
    
    Returns:
        Dict with success status and file paths
    """
    # Setup directories
    if temp_dir is None:
        temp_dir = '/tmp/doc-to-ppt-slides'
    
    html_dir = Path(temp_dir) / 'html'
    png_dir = Path(temp_dir) / 'png'
    
    html_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*50}")
    print(f"Doc-to-PPT Workflow: HTML → PNG → PPTX")
    print(f"{'='*50}")
    
    # Step 1: Generate HTML slides
    print(f"\n[1/3] Generating HTML slides...")
    
    slides_data = slide_structure.get('slide_structure', slide_structure.get('slides', []))
    
    if not slides_data:
        raise ValueError("No slide structure provided")
    
    # Add style to each slide
    if style:
        for slide in slides_data:
            slide['style'] = style
    
    html_files = []
    for i, slide in enumerate(slides_data, 1):
        html_path = html_dir / f'slide_{i:02d}.html'
        
        template = slide.get('template', 'CONTENT')
        
        # Render HTML (template first, then data)
        html_content = generate_html.render_slide(template, slide)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        html_files.append(html_path)
        print(f"  [{i}/{len(slides_data)}] {template.upper()}: {slide.get('title', '')[:40]}")
    
    print(f"✓ Generated {len(html_files)} HTML slides")
    
    # Step 2: Render HTML to PNG
    print(f"\n[2/3] Rendering HTML to PNG...")
    
    renderer_path = find_renderer()
    print(f"  Chrome: {renderer_path}")
    
    png_result = html2png_batch.batch_convert(
        str(html_dir), str(png_dir),
        width=1200, height=675
    )
    
    if not png_result['success']:
        raise RuntimeError(f"Failed to render all slides: {png_result}")
    
    print(f"✓ Rendered {png_result['rendered']} PNG slides")
    
    # Step 3: Create PPTX from PNG
    print(f"\n[3/3] Creating PPTX...")
    
    # Prepare metadata
    metadata = {
        'title': slide_structure.get('title', 'Presentation'),
        'author': slide_structure.get('author', ''),
        'subject': slide_structure.get('subject', ''),
    }
    
    pptx_result = png2pptx.create_pptx_from_pngs(
        str(png_dir), output_path, metadata
    )
    
    print(f"✓ Created PPTX: {output_path}")
    
    return {
        'success': True,
        'output': output_path,
        'total_slides': len(slides_data),
        'html_dir': str(html_dir),
        'png_dir': str(png_dir),
        'file_size_kb': pptx_result['file_size_kb']
    }


def main():
    parser = argparse.ArgumentParser(description='Complete workflow: HTML → PNG → PPTX')
    parser.add_argument('--content', '-c', required=True, help='JSON file with PDF content')
    parser.add_argument('--structure', '-s', required=True, help='JSON file with slide structure')
    parser.add_argument('--output', '-o', required=True, help='Output PPTX file path')
    parser.add_argument('--temp-dir', help='Directory for intermediate files')
    parser.add_argument('--style', help='JSON file with style overrides')
    
    args = parser.parse_args()
    
    # Load inputs
    with open(args.content, 'r', encoding='utf-8') as f:
        pdf_content = json.load(f)
    
    with open(args.structure, 'r', encoding='utf-8') as f:
        slide_structure = json.load(f)
    
    style = None
    if args.style and os.path.exists(args.style):
        with open(args.style, 'r', encoding='utf-8') as f:
            style = json.load(f)
    
    # Run workflow
    result = workflow(
        pdf_content, slide_structure, args.output,
        args.temp_dir, style
    )
    
    print(f"\n{json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == '__main__':
    main()
