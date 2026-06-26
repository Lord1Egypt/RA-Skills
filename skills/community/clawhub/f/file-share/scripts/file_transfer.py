#!/usr/bin/env python3
"""
File Transfer Skill for OpenClaw
Transfers files from the workspace to transfer.whalebone.io using curl upload.
"""

import sys
import os
import subprocess
from pathlib import Path

def is_safe_path(path_str, workspace_root):
    """
    Check if the given path is within the workspace root to prevent directory traversal.
    """
    try:
        # Convert to absolute paths and resolve any symlinks or '..'
        abs_path = os.path.abspath(path_str)
        abs_workspace = os.path.abspath(workspace_root)
        # Ensure the path starts with the workspace root
        return abs_path.startswith(abs_workspace)
    except Exception:
        return False

def get_filename_from_path(filepath):
    """
    Extract the filename from a given path.
    """
    return os.path.basename(filepath)

def run_upload(filepath):
    """
    Execute the curl upload command and return the output.
    """
    filename = get_filename_from_path(filepath)
    # The command uses the current directory as the workspace root for the relative path.
    # We assume the script is run from the workspace root, or we adjust the path accordingly.
    # For safety, we change the working directory to the workspace root.
    workspace_root = "/home/ubuntu/.openclaw/workspace"
    os.chdir(workspace_root)
    
    # Construct the relative path from the workspace root
    rel_path = os.path.relpath(filepath, workspace_root)
    
    # The curl command: upload the file and get the URL
    url = f"https://transfer.whalebone.io/{filename}"
    command = ["curl", "--upload-file", rel_path, url]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30  # 30 seconds timeout
        )
        if result.returncode == 0:
            return result.stdout.strip(), None
        else:
            return None, result.stderr.strip()
    except subprocess.TimeoutExpired:
        return None, "Error: Upload timed out after 30 seconds"
    except Exception as e:
        return None, f"Error during upload: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 file_transfer.py <file_path>")
        print("Example: python3 file_transfer.py memory/2026-05-15.md")
        print("The file path can be absolute or relative to the OpenClaw workspace.")
        sys.exit(1)
    
    # The input file path from the user
    input_path = ' '.join(sys.argv[1:]).strip()
    
    # Define the workspace root
    workspace_root = "/home/ubuntu/.openclaw/workspace"
    
    # If the path is not absolute, make it relative to the workspace root
    if not os.path.isabs(input_path):
        input_path = os.path.join(workspace_root, input_path)
    
    # Normalize the path (remove any redundant separators or up-level references)
    input_path = os.path.normpath(input_path)
    
    # Security check: ensure the path is within the workspace
    if not is_safe_path(input_path, workspace_root):
        print("Error: Access denied. The file must be within the OpenClaw workspace.", file=sys.stderr)
        sys.exit(1)
    
    # Check if the file exists
    if not os.path.isfile(input_path):
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    # Perform the upload
    output, error = run_upload(input_path)
    if error:
        print(error, file=sys.stderr)
        sys.exit(1)
    
    # Output the result (the download URL)
    print(output)

if __name__ == "__main__":
    main()