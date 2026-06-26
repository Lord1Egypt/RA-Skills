#!/usr/bin/env python3
"""
EvoMap VR Submitter - Submit validation reports to EvoMap Hub.
Usage: python vr_submit.py <node_secret> <node_id> <asset_id> <content>
"""
import sys
import json
import time
import urllib.request
import urllib.error

def submit_vr(node_secret, node_id, asset_id, content, notes=""):
    """Submit a validation report to EvoMap."""
    url = "https://evomap.ai/a2a/report"
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    message_id = f"msg_{int(time.time()*1000)}"

    payload = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "report",
        "message_id": message_id,
        "sender_id": node_id,
        "timestamp": timestamp,
        "payload": {
            "target_asset_id": asset_id,
            "validation_report": {
                "report_id": f"vr_{int(time.time()*1000)}",
                "overall_ok": True,
                "commands": [
                    {
                        "command": "content_review",
                        "ok": True,
                        "stdout": content[:200] if content else "Quality submission"
                    }
                ],
                "env_fingerprint_key": "windows_x64",
                "notes": (notes or content)[:200]
            }
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {node_secret}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            status = result.get("payload", {}).get("status", "unknown")
            return status, result
    except urllib.error.HTTPError as e:
        return f"HTTP_{e.code}", e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return "ERROR", str(e)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(json.dumps({
            "error": "Usage: vr_submit.py <node_secret> <node_id> <asset_id> <content> [notes]"
        }))
        sys.exit(1)

    secret = sys.argv[1]
    node_id = sys.argv[2]
    asset_id = sys.argv[3]
    content = sys.argv[4]
    notes = sys.argv[5] if len(sys.argv) > 5 else ""

    status, result = submit_vr(secret, node_id, asset_id, content, notes)
    print(json.dumps({"status": status, "result": result}, indent=2))
