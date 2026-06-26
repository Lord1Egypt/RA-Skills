#!/usr/bin/env python3
"""
Browser status checker for OpenClaw browser hosting capability.
Checks if the browser control service is running and accessible.
"""
import subprocess
import sys
import json

def check_browser_status(profile="openclaw"):
    """Check browser status using openclaw CLI"""
    try:
        result = subprocess.run([
            "openclaw", "browser", 
            "--browser-profile", profile, 
            "status", "--json"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"status": "stopped", "error": result.stderr}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "error": "Command timed out"}
    except FileNotFoundError:
        return {"status": "error", "error": "openclaw command not found"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    profile = sys.argv[1] if len(sys.argv) > 1 else "openclaw"
    status = check_browser_status(profile)
    print(json.dumps(status, indent=2))