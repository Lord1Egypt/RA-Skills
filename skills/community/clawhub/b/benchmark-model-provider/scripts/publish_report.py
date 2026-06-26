#!/usr/bin/env python3
"""Publish helper (safe/no-shell).

This skill intentionally does NOT run external deployment commands (e.g., `npx vercel`).
ClawHub scanners may flag skills that combine credentialed network calls and shell execution.

Instead, this script can:
- copy/export a PDF to a "published-*.pdf" filename
- print suggestions for publishing the generated static HTML folder using common services

If you want one-click deployment, do it manually in your own terminal.
"""

import argparse
import json
import shutil
from pathlib import Path


def publish_pdf(pdf: Path):
    if not pdf.exists():
        raise SystemExit(f'PDF not found: {pdf}')
    out = pdf.parent / ('published-' + pdf.name)
    shutil.copy2(pdf, out)
    return {'mode': 'pdf', 'source': str(pdf), 'published_copy': str(out)}


def publish_suggestions(html_dir: Path):
    return {
        'mode': 'suggestions',
        'html_dir': str(html_dir),
        'services': [
            {
                'name': 'Vercel',
                'how': 'Deploy as a static site (framework: Other). Point to the folder containing index.html.',
                'url': 'https://vercel.com/docs/deployments/static-sites',
            },
            {
                'name': 'Netlify',
                'how': 'Drag-and-drop the HTML folder, or connect a GitHub repo and set publish directory to the HTML output folder.',
                'url': 'https://docs.netlify.com/site-deploys/overview/',
            },
            {
                'name': 'Cloudflare Pages',
                'how': 'Connect a GitHub repo, set build command to none, and set output directory to the HTML folder.',
                'url': 'https://developers.cloudflare.com/pages/',
            },
            {
                'name': 'GitHub Pages',
                'how': 'Commit the HTML files to a repo (often /docs or root) and enable Pages in repo settings.',
                'url': 'https://docs.github.com/pages',
            },
        ],
    }


def main():
    ap = argparse.ArgumentParser(description='Publish helper: export PDF and suggest static hosting (no deployment automation).')
    ap.add_argument('--html-dir', help='Directory containing index.html (for suggestions only)')
    ap.add_argument('--pdf-file', help='PDF file to copy/export')
    ap.add_argument('--mode', required=True, choices=['suggest', 'pdf', 'both'])
    ap.add_argument('--output-json', help='Optional file to store result metadata')
    args = ap.parse_args()

    outputs = []

    if args.mode in ('suggest', 'both'):
        if not args.html_dir:
            raise SystemExit('--html-dir is required for suggest/both mode')
        outputs.append(publish_suggestions(Path(args.html_dir)))

    if args.mode in ('pdf', 'both'):
        if not args.pdf_file:
            raise SystemExit('--pdf-file is required for pdf/both mode')
        outputs.append(publish_pdf(Path(args.pdf_file)))

    print(json.dumps(outputs, ensure_ascii=False, indent=2))

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(outputs, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
