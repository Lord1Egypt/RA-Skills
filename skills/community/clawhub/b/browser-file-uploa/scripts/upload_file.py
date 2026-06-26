#!/usr/bin/env python3
"""
Browser file upload script using agent-browser CLI.
Uploads a file to a web page's file input element.

Supports flexible file path specification:
- Absolute paths: C:\Users\name\file.xlsx
- Relative paths: ./data/file.xlsx (resolved from current directory)
- Workspace paths: workspace/file.xlsx (resolved from OPENCLAW_WORKSPACE)
- Environment variables: ${HOME}/file.xlsx or %USERPROFILE%\file.xlsx
"""

import subprocess
import sys
import os
from pathlib import Path

def resolve_path(file_path: str) -> str:
    """
    Resolve file path with support for:
    - Environment variables (${VAR} or %VAR%)
    - Workspace-relative paths (workspace/...)
    - Relative paths (./...)
    
    Returns absolute path or original if already absolute.
    """
    # Expand environment variables
    expanded = os.path.expandvars(file_path)
    expanded = os.path.expanduser(expanded)
    
    # Check if it's a workspace-relative path
    if expanded.startswith("workspace/"):
        workspace = os.environ.get("OPENCLAW_WORKSPACE", 
            os.path.expanduser("~/.openclaw/workspace"))
        expanded = os.path.join(workspace, expanded[len("workspace/"):])
    
    # Convert to absolute path if relative
    if not os.path.isabs(expanded):
        expanded = os.path.abspath(expanded)
    
    return expanded


def upload_file(url: str, file_path: str, selector: str = None, wait_ms: int = 2000) -> bool:
    """
    Upload a file to a web page using agent-browser.
    
    Args:
        url: The URL to navigate to
        file_path: Path to the file to upload (supports relative, env vars, workspace/)
        selector: CSS selector for the file input element (optional)
        wait_ms: Wait time after page load in milliseconds (default: 2000)
    
    Returns:
        True if upload succeeded, False otherwise
    """
    # Resolve the file path
    resolved_path = resolve_path(file_path)
    
    if not os.path.exists(resolved_path):
        print(f"Error: File not found: {resolved_path} (from: {file_path})")
        return False
    
    print(f"Resolved path: {file_path} -> {resolved_path}")
    
    try:
        # Open the page
        print(f"Opening {url}...")
        result = subprocess.run(
            ["agent-browser", "open", url],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Failed to open page: {result.stderr}")
            return False
        
        # Wait for page to load
        subprocess.run(["agent-browser", "wait", str(wait_ms)], capture_output=True)
        
        # Find and click file input
        if selector:
            print(f"Clicking file input: {selector}...")
            result = subprocess.run(
                ["agent-browser", "click", selector],
                capture_output=True,
                text=True
            )
        else:
            # Try to find file input by text
            print("Finding file upload element...")
            result = subprocess.run(
                ["agent-browser", "find", "text", "选择文件", "click"],
                capture_output=True,
                text=True
            )
        
        # Upload the file
        print(f"Uploading {resolved_path}...")
        if selector:
            result = subprocess.run(
                ["agent-browser", "upload", selector, resolved_path],
                capture_output=True,
                text=True
            )
        else:
            # Use file input id if available
            result = subprocess.run(
                ["agent-browser", "upload", "#filePicker", resolved_path],
                capture_output=True,
                text=True
            )
        
        if result.returncode == 0:
            print("File uploaded successfully!")
            return True
        else:
            print(f"Upload failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error during upload: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: upload_file.py <url> <file_path> [selector] [wait_ms]")
        print()
        print("Arguments:")
        print("  url         - Target page URL")
        print("  file_path   - Path to file (supports relative, env vars, workspace/)")
        print("  selector    - Optional CSS selector for file input")
        print("  wait_ms     - Optional wait time after page load (default: 2000)")
        print()
        print("Path examples:")
        print("  C:\\Users\\name\\file.xlsx    - Absolute path")
        print("  ./data/file.xlsx            - Relative to current directory")
        print("  workspace/file.xlsx         - Relative to OPENCLAW_WORKSPACE")
        print("  ${HOME}/file.xlsx           - With environment variable")
        sys.exit(1)
    
    url = sys.argv[1]
    file_path = sys.argv[2]
    selector = sys.argv[3] if len(sys.argv) > 3 else None
    wait_ms = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    
    success = upload_file(url, file_path, selector, wait_ms)
    sys.exit(0 if success else 1)
