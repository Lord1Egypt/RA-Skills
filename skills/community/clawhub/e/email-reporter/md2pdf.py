#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts Markdown files to PDF with support for images and tables
"""

import os
import sys
import re
from pathlib import Path

def markdown_to_pdf(md_path, output_path=None, image_dir=None):
    """
    Convert Markdown file to PDF
    
    Args:
        md_path: Path to Markdown file
        output_path: Output PDF path (optional, defaults to same name with .pdf)
        image_dir: Directory containing images (optional, defaults to md file directory)
    
    Returns:
        Path to generated PDF
    """
    
    try:
        import markdown
        from weasyprint import HTML, CSS
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Install with: pip install markdown weasyprint")
        sys.exit(1)
    
    md_path = Path(md_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")
    
    if not output_path:
        output_path = md_path.with_suffix('.pdf')
    else:
        output_path = Path(output_path)
    
    if not image_dir:
        image_dir = md_path.parent
    else:
        image_dir = Path(image_dir)
    
    # Read Markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Process image paths - convert relative to absolute
    def replace_image_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # Keep data URIs as-is
        if img_path.startswith('data:'):
            return match.group(0)
        
        # Convert to absolute path
        if not img_path.startswith('/'):
            full_path = image_dir / img_path
        else:
            full_path = Path(img_path)
        
        if full_path.exists():
            return f'![{alt_text}](file://{full_path.absolute()})'
        else:
            print(f"⚠️  Image not found: {full_path}")
            return match.group(0)
    
    md_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_image_path, md_content)
    
    # Convert to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc']
    )
    
    # Add CSS styling
    styled_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: "Noto Sans CJK SC", "WenQuanYi Micro Hei", "DejaVu Sans", sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            font-size: 20pt;
            color: #1a1a2e;
            border-bottom: 2px solid #1a1a2e;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            font-size: 16pt;
            color: #333;
            margin-top: 30px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        h3 {{
            font-size: 13pt;
            color: #444;
            margin-top: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            font-size: 10pt;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 15px 0;
            display: block;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 15px 0;
            padding: 10px 15px;
            color: #666;
            background-color: #f9f9f9;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "SF Mono", "Monaco", monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        p {{
            margin: 12px 0;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
    
    # Generate PDF
    HTML(string=styled_html, base_url=str(image_dir)).write_pdf(output_path)
    
    print(f"✅ PDF generated: {output_path}")
    return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 md2pdf.py <markdown_file> [output_pdf] [image_dir]")
        print("")
        print("Examples:")
        print("  python3 md2pdf.py report.md")
        print("  python3 md2pdf.py report.md report.pdf")
        print("  python3 md2pdf.py report.md report.pdf ./images")
        sys.exit(1)
    
    md_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
    img_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        result = markdown_to_pdf(md_file, pdf_file, img_dir)
        print(f"📄 Output: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
