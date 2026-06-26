#!/usr/bin/env python3
"""Desktop Control MCP Server - wraps osascript/screencapture for OpenClaw MCP"""
import json, sys, subprocess, os, tempfile

def run_osascript(script):
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True, text=True, timeout=10
    )
    return result.stdout.strip(), result.returncode == 0

def handle_screenshot():
    fd, path = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    subprocess.run(['screencapture', '-x', path], check=True)
    return path

def handle_request(data):
    method = data.get('method', '')
    params = data.get('params', {})

    if method == 'initialize':
        return {
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": True},
                "serverInfo": {"name": "desktop-control", "version": "1.0"}
            }
        }
    elif method == 'tools/list':
        return {
            "jsonrpc": "2.0",
            "result": {
                "tools": [
                    {"name": "screenshot", "description": "Take screenshot", "inputSchema": {"type": "object", "properties": {}}},
                    {"name": "click", "description": "Click at coordinates", "inputSchema": {"type": "object", "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}}}},
                    {"name": "type_text", "description": "Type text via clipboard paste", "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}}}},
                    {"name": "key_press", "description": "Press key", "inputSchema": {"type": "object", "properties": {"key": {"type": "string"}, "modifiers": {"type": "array", "items": {"type": "string"}, "default": []}}}},
                    {"name": "set_clipboard", "description": "Copy text to clipboard", "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}}}},
                    {"name": "shell", "description": "Run shell command", "inputSchema": {"type": "object", "properties": {"command": {"type": "string"}, "timeout": {"type": "integer", "default": 30}}}},
                ]
            }
        }
    elif method == 'tools/call':
        tool = params.get('name', '')
        args = params.get('arguments', {})

        try:
            if tool == 'screenshot':
                path = handle_screenshot()
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": f"Screenshot: {path}"}], "isError": False}}

            elif tool == 'click':
                x, y = args.get('x', 0), args.get('y', 0)
                script = f'tell application "System Events" to click at {{{x}, {y}}}'
                out, ok = run_osascript(script)
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": f"Clicked ({x},{y}) ok={ok}"}], "isError": False}}

            elif tool == 'type_text':
                text = args.get('text', '').replace('"', '\\"')
                subprocess.run(['osascript', '-e', f'set the clipboard to "{text}"'], check=True)
                subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke "v" using command down'], check=True)
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": f"Typed: {text[:50]}"}], "isError": False}}

            elif tool == 'key_press':
                key = args.get('key', 'return')
                mods = args.get('modifiers', [])
                script = f'tell application "System Events" to keystroke "{key}"'
                if mods:
                    script = f'tell application "System Events" to keystroke "{key}" using {", ".join(mods)} down'
                out, ok = run_osascript(script)
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": f"Key: {key} {mods}, ok={ok}"}], "isError": False}}

            elif tool == 'set_clipboard':
                text = args.get('text', '').replace('"', '\\"')
                subprocess.run(['osascript', '-e', f'set the clipboard to "{text}"'], check=True)
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": "Clipboard set"}], "isError": False}}

            elif tool == 'shell':
                cmd = args.get('command', '')
                timeout = args.get('timeout', 30)
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": result.stdout[:500]}], "isError": False}}

            else:
                return {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Unknown: {tool}"}}
        except Exception as e:
            return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": f"Error: {str(e)}"}], "isError": True}}

    return {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid request"}}

while True:
    try:
        line = sys.stdin.readline()
        if not line:
            break
        data = json.loads(line.strip())
        response = handle_request(data)
        print(json.dumps(response), flush=True)
    except json.JSONDecodeError:
        pass
    except Exception as e:
        print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)
