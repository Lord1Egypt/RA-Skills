#!/usr/bin/env python3
import os, json
keys = [
    "APIFY_API_TOKEN","PAGESPEED_API_KEY","GSC_EXPORT_PATH","GA4_EXPORT_PATH",
    "AHREFS_EXPORT_PATH","SEMRUSH_EXPORT_PATH","MOZ_EXPORT_PATH",
    "SCREAMING_FROG_EXPORT_PATH","CUSTOM_SCRAPER_API_KEY","CUSTOM_SCRAPER_BASE_URL"
]
print(json.dumps({k: bool(os.getenv(k)) for k in keys}, indent=2))
