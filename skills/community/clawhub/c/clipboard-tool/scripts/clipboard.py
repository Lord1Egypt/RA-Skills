#!/usr/bin/env python3
"""Clipboard Tool - Copy and paste from system clipboard."""

import argparse
import os
import platform
import subprocess
import sys


def get_clipboard_cmd() -> tuple:
    """Get platform-specific clipboard commands."""
    system = platform.system()
    
    if system == 'Linux':
        # Try different clipboard tools
        for cmd in ['xclip', 'xsel', 'wl-paste']:
            if subprocess.call(['which', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                if cmd == 'xclip':
                    return (f'{cmd} -selection clipboard', f'{cmd} -selection clipboard -o')
                elif cmd == 'xsel':
                    return (f'{cmd} --clipboard --input', f'{cmd} --clipboard --output')
                elif cmd == 'wl-paste':
                    return (f'{cmd}', f'{cmd}')
        return (None, None)
    
    elif system == 'Darwin':  # macOS
        return ('pbcopy', 'pbpaste')
    
    elif system == 'Windows':
        return ('clip', 'powershell Get-Clipboard')
    
    return (None, None)


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard."""
    copy_cmd, _ = get_clipboard_cmd()
    
    if not copy_cmd:
        print("Error: No clipboard utility found", file=sys.stderr)
        return False
    
    try:
        if platform.system() == 'Windows':
            # Windows clip command
            process = subprocess.Popen(copy_cmd, stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        else:
            # Unix-like systems
            process = subprocess.Popen(copy_cmd, stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        
        print(f"Copied to clipboard: {text[:50]}{'...' if len(text) > 50 else ''}")
        return True
    except Exception as e:
        print(f"Error copying to clipboard: {e}", file=sys.stderr)
        return False


def paste_from_clipboard() -> str:
    """Paste text from clipboard."""
    _, paste_cmd = get_clipboard_cmd()
    
    if not paste_cmd:
        print("Error: No clipboard utility found", file=sys.stderr)
        return ""
    
    try:
        if platform.system() == 'Windows':
            # Windows PowerShell
            result = subprocess.run(
                ['powershell', '-Command', paste_cmd],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        else:
            result = subprocess.run(
                paste_cmd.split(),
                capture_output=True, text=True, check=True
            )
            return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error reading clipboard: {e}", file=sys.stderr)
        return ""
    except FileNotFoundError:
        print("Error: Clipboard command not found", file=sys.stderr)
        return ""


def clear_clipboard() -> bool:
    """Clear the clipboard."""
    return copy_to_clipboard("")


def main():
    parser = argparse.ArgumentParser(description='Clipboard tool')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--copy', '-c', help='Copy text to clipboard')
    group.add_argument('--paste', '-p', action='store_true', help='Paste from clipboard')
    group.add_argument('--clear', action='store_true', help='Clear clipboard')
    
    parser.add_argument('--file', '-f', help='Read from file')
    parser.add_argument('--upper', action='store_true', help='Convert to uppercase')
    parser.add_argument('--lower', action='store_true', help='Convert to lowercase')
    
    args = parser.parse_args()
    
    # Get text to copy
    text = ""
    
    if args.clear:
        clear_clipboard()
        print("Clipboard cleared")
        return
    
    if args.file:
        try:
            with open(args.file, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    
    if args.copy:
        text = args.copy
    
    # Apply transformations
    if args.upper and text:
        text = text.upper()
    if args.lower and text:
        text = text.lower()
    
    # Execute
    if args.paste:
        result = paste_from_clipboard()
        if result:
            print(result, end='')
    elif text:
        copy_to_clipboard(text)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
