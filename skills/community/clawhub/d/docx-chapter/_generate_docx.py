#!/usr/bin/env python3
"""Read MD content from stdin, write to chapter.md, run pandoc."""
import sys, os, subprocess

output_dir = os.path.expanduser(sys.argv[1])
os.makedirs(output_dir, exist_ok=True)

md_path = os.path.join(output_dir, 'chapter.md')
docx_path = os.path.join(output_dir, 'chapter.docx')

md_content = sys.stdin.read()
with open(md_path, 'w') as f:
    f.write(md_content)

ref_docx = sys.argv[2] if len(sys.argv) > 2 else None
args = ['pandoc', md_path, '-o', docx_path,
        '--from', 'markdown+footnotes',
        '--to', 'docx']
if ref_docx:
    args += ['--reference-doc', ref_docx]

subprocess.run(args, check=True)
print(docx_path)
