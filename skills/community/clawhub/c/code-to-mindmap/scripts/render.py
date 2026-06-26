#!/usr/bin/env python3
"""
Render a Mermaid diagram from a .mmd file to PNG or SVG.
Requires: pip install mermaid-py or use mmdc (Mermaid CLI) if available.
"""
import os, sys, subprocess, argparse

def render_mermaid(mmd_path, output_path=None, format="png"):
    if not os.path.exists(mmd_path):
        print(f"ERROR: {mmd_path} not found")
        sys.exit(1)

    if output_path is None:
        output_path = mmd_path.replace(".mmd", f".{format}")

    # Try mmdc (Mermaid CLI) first — most reliable
    mmdc = os.getenv("MMDC_PATH", "mmdc")
    try:
        subprocess.run(
            [mmdc, "-i", mmd_path, "-o", output_path, "-b", format],
            check=True, capture_output=True
        )
        print(f"✅ Rendered: {output_path}")
        return
    except FileNotFoundError:
        pass  # mmdc not found, try mermaid-py
    except subprocess.CalledProcessError as e:
        print(f"⚠️  mmdc failed: {e.stderr.decode() if e.stderr else e}")

    # Fallback: try mermaid-py
    try:
        from mermaid import Mermaid
        m = Mermaid()
        with open(mmd_path) as f:
            content = f.read()
        # mermaid-py requires a server; use base64 image output
        print(f"⚠️  mermaid-py requires a running server. Try: mmdc CLI or https://mermaid.live")
        print(f"   Quick alternative: copy contents of {mmd_path} to https://mermaid.live")
    except ImportError:
        print(f"ERROR: No Mermaid renderer found.")
        print(f"   Install mmdc: npm install -g @mermaid-js/mermaid-cli")
        print(f"   Or visit: https://mermaid.live, paste content from {mmd_path}")
        sys.exit(1)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Render Mermaid .mmd file to PNG/SVG")
    p.add_argument("input", help=".mmd file path")
    p.add_argument("-o", "--output", help="Output file path")
    p.add_argument("-f", "--format", default="png", choices=["png", "svg"])
    args = p.parse_args()
    render_mermaid(args.input, args.output, args.format)
