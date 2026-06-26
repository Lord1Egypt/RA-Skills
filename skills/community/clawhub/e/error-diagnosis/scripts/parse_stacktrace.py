#!/usr/bin/env python3
"""Parse stack traces from various languages into structured JSON."""

import sys
import re
import json

def parse_python(text):
    frames = []
    for m in re.finditer(r'File "([^"]+)", line (\d+), in (\w+)', text):
        frames.append({"file": m.group(1), "line": int(m.group(2)), "function": m.group(3)})
    err_match = re.search(r'^(\w+Error|\w+Exception|KeyboardInterrupt): (.+)$', text, re.MULTILINE)
    if not err_match:
        err_match = re.search(r'^(\w+Error|\w+Exception)$', text, re.MULTILINE)
    error_type = err_match.group(1) if err_match else "Unknown"
    error_msg = err_match.group(2) if err_match and err_match.lastindex >= 2 else ""
    return {"language": "python", "error_type": error_type, "message": error_msg, "frames": frames}

def parse_javascript(text):
    frames = []
    for m in re.finditer(r'at (?:(.+?) \()?(.+?):(\d+):(\d+)\)?', text):
        frames.append({
            "function": m.group(1) or "<anonymous>",
            "file": m.group(2), "line": int(m.group(3)), "column": int(m.group(4))
        })
    err_match = re.search(r'^(\w+Error|\w+Exception): (.+)$', text, re.MULTILINE)
    error_type = err_match.group(1) if err_match else "Unknown"
    error_msg = err_match.group(2) if err_match else ""
    return {"language": "javascript", "error_type": error_type, "message": error_msg, "frames": frames}

def parse_java(text):
    frames = []
    for m in re.finditer(r'at ([\w.$]+)\(([\w.]+):(\d+)\)', text):
        frames.append({"function": m.group(1), "file": m.group(2), "line": int(m.group(3))})
    err_match = re.search(r'^([\w.]+(?:Error|Exception)): (.+)$', text, re.MULTILINE)
    error_type = err_match.group(1) if err_match else "Unknown"
    error_msg = err_match.group(2) if err_match else ""
    return {"language": "java", "error_type": error_type, "message": error_msg, "frames": frames}

def parse_go(text):
    frames = []
    for m in re.finditer(r'([\w/.-]+\.go):(\d+)', text):
        frames.append({"file": m.group(1), "line": int(m.group(2))})
    err_match = re.search(r'(?:panic|fatal error): (.+)', text)
    error_type = "panic" if "panic:" in text else "fatal error" if "fatal error:" in text else "error"
    error_msg = err_match.group(1) if err_match else ""
    return {"language": "go", "error_type": error_type, "message": error_msg, "frames": frames}

def detect_and_parse(text):
    if re.search(r'File ".*", line \d+', text):
        return parse_python(text)
    if re.search(r'at .+:\d+:\d+', text):
        return parse_javascript(text)
    if re.search(r'at [\w.$]+\([\w.]+:\d+\)', text):
        return parse_java(text)
    if re.search(r'\.go:\d+', text):
        return parse_go(text)
    err_match = re.search(r'(?:error|Error|ERROR)[:\s]+(.+)', text)
    return {
        "language": "unknown",
        "error_type": "Error",
        "message": err_match.group(1).strip() if err_match else text.strip()[:200],
        "frames": []
    }

if __name__ == "__main__":
    text = sys.stdin.read()
    result = detect_and_parse(text)
    result["search_queries"] = [
        f'{result["language"]} {result["error_type"]} {result["message"][:80]}',
        f'{result["error_type"]} {result["message"][:50]} fix',
    ]
    print(json.dumps(result, indent=2))
