#!/usr/bin/env python3
"""Code review using Gemini AI."""

import os
import sys
import json

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDe5i94YxqNZ9OT7mFeuotgfttRmDQ7tz0")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def call_gemini(prompt: str) -> str:
    """Call Gemini API."""
    import urllib.request
    
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    data = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error calling Gemini: {e}"

def review_code(code: str) -> str:
    """Review code and suggest improvements."""
    prompt = f"""You are a senior code reviewer. Review this code and provide:
1. Issues found (bugs, security risks, performance issues)
2. Suggestions for improvement
3. Overall assessment

Be specific and actionable. Code to review:

```{code}```"""
    return call_gemini(prompt)

def main():
    if len(sys.argv) < 3:
        print("Usage: code_review.py <action> <code_or_file>")
        print("Actions: review, suggest, debug")
        sys.exit(1)
    
    action = sys.argv[1]
    input_data = sys.argv[2]
    
    # If input is a file path, read it
    if os.path.isfile(input_data):
        with open(input_data) as f:
            code = f.read()
    else:
        code = input_data
    
    if action == "review":
        result = review_code(code)
    elif action == "suggest":
        prompt = f"""Suggest improvements for this code. Focus on:
- Readability
- Performance  
- Best practices
- Modern patterns

```{code}```"""
        result = call_gemini(prompt)
    elif action == "debug":
        error_desc = sys.argv[3] if len(sys.argv) > 3 else "No error description provided"
        prompt = f"""Debug this code. Error description: {error_desc}

Code:
```{code}```

Provide:
1. Likely cause
2. How to fix
3. Prevention tips"""
        result = call_gemini(prompt)
    else:
        result = f"Unknown action: {action}"
    
    print(result)

if __name__ == "__main__":
    main()