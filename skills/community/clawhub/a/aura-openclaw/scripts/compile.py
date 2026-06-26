#!/usr/bin/env python3
"""Aura Compile Script for OpenClaw Integration.

Compiles a directory of files into an .aura knowledge base.
Used as an OpenClaw skill action.

Security Manifest:
    Environment Variables: None
    External Endpoints: None
    Local Files Read: User-specified input directory
    Local Files Written: User-specified .aura output file

Usage:
    python compile.py <input_dir> <output_file> [--pii-mask] [--min-quality 0.3] [--domain financial]
"""

import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: python compile.py <input_dir> <output.aura>")
        print("  Options:")
        print("    --pii-mask              Mask PII before compilation")
        print("    --min-quality 0.3       Filter low-quality content")
        print("    --domain <type>         Domain hint (financial, technical, etc.)")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    # Parse optional flags
    pii_mask = "--pii-mask" in sys.argv

    min_quality = 0.0
    if "--min-quality" in sys.argv:
        idx = sys.argv.index("--min-quality")
        if idx + 1 < len(sys.argv):
            try:
                min_quality = float(sys.argv[idx + 1])
            except ValueError:
                print("❌ --min-quality must be a number (e.g., 0.3)")
                sys.exit(1)

    domain = ""
    if "--domain" in sys.argv:
        idx = sys.argv.index("--domain")
        if idx + 1 < len(sys.argv):
            domain = sys.argv[idx + 1]

    print(f"🔥 Compiling: {input_dir} → {output_file}")

    try:
        from aura.compiler import compile_directory

        stats = compile_directory(
            input_dir=input_dir,
            output_path=output_file,
            enable_pii_masking=pii_mask,
            min_quality_score=min_quality,
            domain=domain,
        )

        print(f"✅ Compiled successfully → {output_file}")
        print(f"   Processed: {stats.processed_files}/{stats.total_files} files")
        print(f"   Words: {stats.total_tokens:,}")
        if stats.failed_files:
            print(f"   Failed: {stats.failed_files}")
        if stats.pii_masked:
            print(f"   PII masked: {stats.pii_masked} occurrences")

    except ImportError:
        print("❌ aura-core not found. Install with: pip install auralith-aura")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
