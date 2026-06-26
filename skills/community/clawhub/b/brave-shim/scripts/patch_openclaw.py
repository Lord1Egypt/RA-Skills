#!/usr/bin/env python3
"""Patch OpenClaw's built-in Brave provider JS to redirect to localhost shim."""

import os, re

OPENCLAW_DIST = r"F:\npm\node_modules\openclaw\dist"
REPLACEMENTS = {
    "const BRAVE_SEARCH_ENDPOINT = \"https://api.search.brave.com/res/v1/web/search\";":
        "const BRAVE_SEARCH_ENDPOINT = \"http://127.0.0.1:8000/res/v1/web/search\";",
    "const BRAVE_LLM_CONTEXT_ENDPOINT = \"https://api.search.brave.com/res/v1/llm/context\";": 
        "const BRAVE_LLM_CONTEXT_ENDPOINT = \"http://127.0.0.1:8000/res/v1/llm/context\";",
}

def main():
    count = 0
    for fname in os.listdir(OPENCLAW_DIST):
        if not (fname.startswith("brave-web-search-provider") and fname.endswith(".js")):
            continue
        fpath = os.path.join(OPENCLAW_DIST, fname)
        content = open(fpath).read()
        new_content = content
        for old, new in REPLACEMENTS.items():
            if old in new_content:
                new_content = new_content.replace(old, new)
                print(f"Patched {fname}: {old[:40]}... -> {new[:40]}...")
                count += 1
        if new_content != content:
            open(fpath, "w").write(new_content)
    if count == 0:
        print("No patches applied - BRAVE_SEARCH_ENDPOINT already patched or file not found")
    else:
        print(f"Done. {count} replacement(s) made.")

if __name__ == "__main__":
    main()
