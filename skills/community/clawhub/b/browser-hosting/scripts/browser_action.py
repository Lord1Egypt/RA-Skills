#!/usr/bin/env python3
"""
Browser action script for OpenClaw browser hosting skill.

This script provides a wrapper around the openclaw browser act command
for performing UI interactions.
"""

import subprocess
import sys
import json
import argparse

def run_browser_command(args):
    """Run openclaw browser command with given arguments."""
    cmd = ["openclaw", "browser"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running browser command: {e}", file=sys.stderr)
        print(f"Command: {' '.join(cmd)}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Perform browser action")
    parser.add_argument("--profile", default="openclaw", help="Browser profile (default: openclaw)")
    parser.add_argument("action", choices=["click", "type", "press", "hover", "drag", "select", "fill", "resize", "wait", "evaluate", "close"], 
                       help="Action to perform")
    parser.add_argument("ref", nargs="?", help="Element reference (for click, type, etc.)")
    parser.add_argument("--text", help="Text to type or fill")
    parser.add_argument("--submit", action="store_true", help="Submit form after typing")
    parser.add_argument("--double", action="store_true", help="Double click")
    parser.add_argument("--start-ref", help="Start reference for drag")
    parser.add_argument("--end-ref", help="End reference for drag")
    parser.add_argument("--values", nargs="+", help="Values for select")
    parser.add_argument("--fields", help="JSON fields for fill action")
    parser.add_argument("--width", type=int, help="Width for resize")
    parser.add_argument("--height", type=int, help="Height for resize")
    parser.add_argument("--time-ms", type=int, help="Time in milliseconds for wait")
    parser.add_argument("--text-gone", help="Text that should disappear for wait")
    parser.add_argument("--fn", help="JavaScript function for evaluate or wait")
    
    args = parser.parse_args()
    
    # Build command arguments
    cmd_args = ["--browser-profile", args.profile]
    
    # Add action-specific arguments
    if args.action == "click":
        if not args.ref:
            print("Error: click action requires a ref", file=sys.stderr)
            return 1
        cmd_args.append("click")
        cmd_args.append(args.ref)
        if args.double:
            cmd_args.append("--double")
            
    elif args.action == "type":
        if not args.ref or not args.text:
            print("Error: type action requires ref and text", file=sys.stderr)
            return 1
        cmd_args.append("type")
        cmd_args.append(args.ref)
        cmd_args.append(args.text)
        if args.submit:
            cmd_args.append("--submit")
            
    elif args.action == "press":
        if not args.ref:
            print("Error: press action requires a key", file=sys.stderr)
            return 1
        cmd_args.append("press")
        cmd_args.append(args.ref)
        
    elif args.action == "drag":
        if not args.start_ref or not args.end_ref:
            print("Error: drag action requires start-ref and end-ref", file=sys.stderr)
            return 1
        cmd_args.append("drag")
        cmd_args.append(args.start_ref)
        cmd_args.append(args.end_ref)
        
    elif args.action == "select":
        if not args.ref or not args.values:
            print("Error: select action requires ref and values", file=sys.stderr)
            return 1
        cmd_args.append("select")
        cmd_args.append(args.ref)
        cmd_args.extend(args.values)
        
    elif args.action == "fill":
        if not args.fields:
            print("Error: fill action requires fields JSON", file=sys.stderr)
            return 1
        cmd_args.append("fill")
        cmd_args.append("--fields")
        cmd_args.append(args.fields)
        
    elif args.action == "resize":
        if not args.width or not args.height:
            print("Error: resize action requires width and height", file=sys.stderr)
            return 1
        cmd_args.append("resize")
        cmd_args.append(str(args.width))
        cmd_args.append(str(args.height))
        
    elif args.action == "wait":
        cmd_args.append("wait")
        if args.ref:
            cmd_args.append(args.ref)
        if args.time_ms:
            cmd_args.append("--time-ms")
            cmd_args.append(str(args.time_ms))
        if args.text_gone:
            cmd_args.append("--text-gone")
            cmd_args.append(args.text_gone)
        if args.fn:
            cmd_args.append("--fn")
            cmd_args.append(args.fn)
            
    elif args.action == "evaluate":
        if not args.ref or not args.fn:
            print("Error: evaluate action requires ref and fn", file=sys.stderr)
            return 1
        cmd_args.append("evaluate")
        cmd_args.append("--fn")
        cmd_args.append(args.fn)
        cmd_args.append("--ref")
        cmd_args.append(args.ref)
        
    elif args.action == "close":
        cmd_args.append("close")
        if args.ref:
            cmd_args.append(args.ref)
    
    result = run_browser_command(cmd_args)
    if result is not None:
        if result:  # Only print if there's output
            print(result)
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())