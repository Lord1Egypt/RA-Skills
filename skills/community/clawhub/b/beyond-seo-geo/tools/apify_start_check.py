#!/usr/bin/env python3
"""Check whether Beyond SEO can run in Apify-first mode.

This script never prints token values.
"""
import os, json

available = bool(os.getenv("APIFY_API_TOKEN"))
print(json.dumps({
    "apify_first_mode": available,
    "APIFY_API_TOKEN_detected": available,
    "message": "Use Apify Intelligence Mode." if available else "APIFY_API_TOKEN missing. Ask once for Apify token or Apify MCP setup."
}, indent=2))
