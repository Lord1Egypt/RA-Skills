#!/usr/bin/env python3
"""
Generate dress-up playable ads from template and assets.
"""

import argparse
import os
import shutil
import json
import re
from pathlib import Path

def copy_assets(input_dir, output_dir):
    """Copy and organize assets from input to output."""
    assets_output = os.path.join(output_dir, 'assets')
    os.makedirs(assets_output, exist_ok=True)
    
    # Copy character parts
    char_dirs = ['hair', 'dress', 'shoes']
    for category in char_dirs:
        src_dir = os.path.join(input_dir, 'character', category)
        if os.path.exists(src_dir):
            dst_dir = os.path.join(assets_output, category)
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
    
    # Copy background
    bg_src = os.path.join(input_dir, 'background.jpg')
    if os.path.exists(bg_src):
        shutil.copy(bg_src, os.path.join(assets_output, 'background.jpg'))
    
    # Copy UI assets if exist
    ui_dir = os.path.join(input_dir, 'ui')
    if os.path.exists(ui_dir):
        shutil.copytree(ui_dir, os.path.join(assets_output, 'ui'), dirs_exist_ok=True)

def generate_js_config(input_dir):
    """Generate JavaScript config with asset paths."""
    config = {
        'categories': []
    }
    
    char_dir = os.path.join(input_dir, 'character')
    if os.path.exists(char_dir):
        for category in ['hair', 'dress', 'shoes']:
            cat_dir = os.path.join(char_dir, category)
            if os.path.exists(cat_dir):
                images = sorted([f for f in os.listdir(cat_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
                config['categories'].append({
                    'name': category,
                    'assets': [f'assets/{category}/{img}' for img in images]
                })
    
    return config

def update_template(template_path, output_path, config, custom_css=None):
    """Update template HTML with generated config."""
    with open(template_path, 'r') as f:
        html = f.read()
    
    # Replace asset paths in JavaScript
    for category in config['categories']:
        cat_name = category['name']
        assets = category['assets']
        
        # Generate array string
        assets_array = ', '.join([f"'{a}'" for a in assets])
        
        # Replace in HTML (find variable like hairAssets = [...])
        pattern = rf"({cat_name}Assets\s*=\s*\[)[^\]]*(\])"
        replacement = rf"\1{assets_array}\2"
        html = re.sub(pattern, replacement, html, flags=re.IGNORECASE)
    
    # Update background if exists
    bg_path = 'assets/background.jpg'
    if 'background.jpg' in str(html):
        html = re.sub(r"backgroundImage\s*=\s*'[^']*'", f"backgroundImage = '{bg_path}'", html)
    
    # Inject custom CSS if provided
    if custom_css:
        css_block = f"<style>{custom_css}</style>"
        html = html.replace('</head>', f'{css_block}</head>')
    
    with open(output_path, 'w') as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser(description='Generate dress-up playable ad')
    parser.add_argument('--input-dir', required=True, help='Directory containing assets')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--scale', type=float, default=1.1, help='Character scale factor')
    parser.add_argument('--primary-color', default='#ff69b4', help='Primary theme color')
    
    args = parser.parse_args()
    
    # Get template directory
    skill_dir = Path(__file__).parent.parent
    template_dir = skill_dir / 'assets' / 'template'
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Copy assets
    copy_assets(args.input_dir, args.output_dir)
    
    # Generate config
    config = generate_js_config(args.input_dir)
    
    # Generate custom CSS
    custom_css = f"""
        :root {{
            --character-scale: {args.scale};
            --primary-color: {args.primary_color};
        }}
    """
    
    # Update template
    template_html = template_dir / 'index.html'
    output_html = os.path.join(args.output_dir, 'index.html')
    update_template(str(template_html), output_html, config, custom_css)
    
    # Copy mraid.js
    shutil.copy(template_dir / 'mraid.js', os.path.join(args.output_dir, 'mraid.js'))
    
    print(f"✅ Generated playable at: {args.output_dir}")
    print(f"   Categories: {len(config['categories'])}")
    for cat in config['categories']:
        print(f"   - {cat['name']}: {len(cat['assets'])} items")

if __name__ == '__main__':
    main()
