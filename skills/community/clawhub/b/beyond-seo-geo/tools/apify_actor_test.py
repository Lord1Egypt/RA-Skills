#!/usr/bin/env python3
import os, sys, json
token = os.getenv("APIFY_API_TOKEN")
if not token:
    print(json.dumps({"apify_available": False, "message": "APIFY_API_TOKEN not found"}))
else:
    print(json.dumps({"apify_available": True, "message": "Token detected. Use host agent or Apify client to run actors."}))
