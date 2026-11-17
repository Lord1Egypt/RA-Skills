#!/usr/bin/env python3
"""Remove all canary files, manifest, and incidents log."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from generate_tokens import load_manifest, MANIFEST_PATH, CANARY_DIR

INCIDENT_LOG = os.path.join(CANARY_DIR, "incidents.log")

def cleanup():
    """Remove all canary artifacts."""
    manifest = load_manifest()
    
    if not manifest:
        print("No canary deployment found. Nothing to clean up.")
        return
    
    print("=== Agent Canary: Cleanup ===\n")
    
    # Remove planted files
    removed = 0
    for finfo in manifest.get("files", []):
        path = finfo["path"]
        if os.path.exists(path):
            os.remove(path)
            print(f"  REMOVED: {path}")
            removed += 1
    
    # Remove manifest
    if os.path.exists(MANIFEST_PATH):
        os.remove(MANIFEST_PATH)
        print(f"  REMOVED: {MANIFEST_PATH}")
    
    # Keep incident log (user may want to review), but note it
    if os.path.exists(INCIDENT_LOG):
        print(f"  KEPT: {INCIDENT_LOG} (review incidents before deleting)")
    
    print(f"\nCleanup complete. {removed} canary file(s) removed.")
    print("Remember to stop the canary monitoring cron job if active.")

if __name__ == "__main__":
    cleanup()
