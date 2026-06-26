#!/usr/bin/env python3
"""
Feishu Document Sender Helper Script
Finds and lists document files (.docx, .pdf) in the workspace.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def get_workspace_path():
    """Get the workspace path from environment or default."""
    return os.environ.get('OPENCLAW_WORKSPACE', '/root/.openclaw/workspace')

def find_documents(workspace=None, keywords=None, extensions=None):
    """
    Find document files in workspace.
    
    Args:
        workspace: Path to workspace directory
        keywords: List of keywords to match in filename
        extensions: List of file extensions to include (default: .docx, .pdf)
    
    Returns:
        List of dicts with file info: [{path, name, size, modified}]
    """
    if workspace is None:
        workspace = get_workspace_path()
    
    if extensions is None:
        extensions = ['.docx', '.pdf']
    
    workspace = Path(workspace)
    if not workspace.exists():
        return []
    
    files = []
    for ext in extensions:
        for file_path in workspace.glob(f'*{ext}'):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'extension': ext,
                    'size': stat.st_size,
                    'size_human': format_size(stat.st_size),
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                })
    
    # Filter by keywords if provided
    if keywords:
        keywords = [k.lower() for k in keywords]
        files = [f for f in files if any(k in f['name'].lower() for k in keywords)]
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    return files

def format_size(size_bytes):
    """Format file size to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"

def format_output(files):
    """Format file list for display."""
    if not files:
        return "没有找到匹配的文件。"
    
    lines = [f"找到 {len(files)} 个文件：\n"]
    for i, f in enumerate(files, 1):
        lines.append(f"{i}. {f['name']} ({f['size_human']})")
    
    return "\n".join(lines)

def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Find document files in workspace')
    parser.add_argument('--workspace', '-w', help='Workspace directory path')
    parser.add_argument('--keyword', '-k', nargs='+', help='Keywords to match in filename')
    parser.add_argument('--ext', '-e', nargs='+', default=['.docx', '.pdf'],
                       help='File extensions to include')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='text',
                       help='Output format')
    
    args = parser.parse_args()
    
    files = find_documents(
        workspace=args.workspace,
        keywords=args.keyword,
        extensions=args.ext
    )
    
    if args.format == 'json':
        import json
        # Convert datetime to string for JSON serialization
        for f in files:
            f['modified'] = f['modified'].isoformat()
        print(json.dumps(files, indent=2, ensure_ascii=False))
    else:
        print(format_output(files))
    
    return 0 if files else 1

if __name__ == '__main__':
    sys.exit(main())
