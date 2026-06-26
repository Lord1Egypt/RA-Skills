"""
Web to PDF converter using Playwright.
Usage: python pdf2.py <url> [output_filename]
"""
import sys
import os
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


def url_to_pdf(url: str, output: str = None) -> str:
    """Convert a web page to PDF."""
    
    if not url:
        print("Error: URL is required")
        print("Usage: python pdf2.py <url> [output_filename]")
        sys.exit(1)
    
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Determine output filename
    if not output:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace(':', '_').replace('.', '_')
        output = f"{domain}.pdf"
    
    # Ensure .pdf extension
    if not output.endswith('.pdf'):
        output += '.pdf'
    
    print(f"Converting: {url}")
    print(f"Output: {output}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until='load', timeout=60000)
            
            # Generate PDF
            page.pdf(
                path=output,
                format='A4',
                print_background=True,
                margin={
                    'top': '20px',
                    'bottom': '20px',
                    'left': '20px',
                    'right': '20px'
                }
            )
            
            browser.close()
        
        print(f"[OK] PDF saved: {os.path.abspath(output)}")
        return output
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf2.py <url> [output_filename]")
        print("Example: python pdf2.py https://example.com myfile.pdf")
        sys.exit(1)
    
    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    url_to_pdf(url, output)
