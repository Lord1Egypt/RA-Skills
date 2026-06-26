#!/usr/bin/env python3
"""Check health of AI APIs."""
import sys
import json
import urllib.request
import urllib.error
import ssl
import time

APIS = {
    "OpenAI": "https://api.openai.com/v1/models",
    "Anthropic": "https://api.anthropic.com/v1/models",
    "Google Gemini": "https://generativelanguage.googleapis.com/v1/models",
    "Pollinations Image": "https://image.pollinations.ai/models",
    "Pollinations Text": "https://text.pollinations.ai/models",
    "OpenRouter": "https://openrouter.ai/api/v1/models",
    "Stability AI": "https://api.stability.ai/v1/user/account",
    "Groq": "https://api.groq.com/openai/v1/models",
}

def check_api(name, url):
    """Check if API is responsive."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (API-Health-Check/1.0)'
        }
        
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        start = time.time()
        
        try:
            with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                elapsed = (time.time() - start) * 1000
                return (True, elapsed, response.status)
        except urllib.error.HTTPError as e:
            # 401/403 means API is up but requires auth
            elapsed = (time.time() - start) * 1000
            if e.code in (401, 403):
                return (True, elapsed, e.code)
            return (False, elapsed, e.code)
            
    except Exception as e:
        return (False, 0, str(e))

def main():
    specific = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("API Health Check")
    print("=" * 50)
    
    apis_to_check = {specific: APIS[specific]} if specific and specific in APIS else APIS
    
    for name, url in apis_to_check.items():
        is_up, elapsed, status = check_api(name, url)
        
        if is_up:
            icon = "✅"
            status_str = f"UP ({status})"
        else:
            icon = "❌"
            status_str = f"DOWN ({status})"
        
        if elapsed > 0:
            print(f"{icon} {name:20} - {status_str} - {elapsed:.0f}ms")
        else:
            print(f"{icon} {name:20} - {status_str}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()