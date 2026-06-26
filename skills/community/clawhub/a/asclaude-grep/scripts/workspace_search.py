#!/usr/bin/env python3
"""
Workspace Grep & Glob Tool
Searches for content or filenames within the OpenClaw workspace.
"""
import subprocess
import sys
import os

WORKSPACE_PATH = os.path.expanduser("~/.openclaw/workspace")

def grep_content(pattern, max_results=20):
    """Search file content using grep."""
    cmd = [
        "grep", "-rn", 
        "--include=*.py", "--include=*.md", "--include=*.ts", 
        "--include=*.js", "--include=*.json", "-i",
        pattern, WORKSPACE_PATH
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')
        if not lines or lines == ['']:
            return f"No content matches found for: {pattern}"
        return "\n".join(lines[:max_results])
    except Exception as e:
        return f"Grep error: {str(e)}"

def find_files(pattern, max_results=20):
    """List files using find (glob-like)."""
    cmd = ["find", WORKSPACE_PATH, "-name", pattern, "-type", "f"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')
        if not lines or lines == ['']:
            return f"No files found matching: {pattern}"
        return "\n".join(lines[:max_results])
    except Exception as e:
        return f"Find error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python workspace_search.py [grep|find] <pattern>")
        sys.exit(1)
        
    action = sys.argv[1]
    pattern = sys.argv[2]
    
    if action == "grep":
        print(grep_content(pattern))
    elif action == "find":
        print(find_files(pattern))
    else:
        print("Unknown action. Use 'grep' or 'find'.")
