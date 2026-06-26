#!/usr/bin/env python3
import json, sys
def normalize(item):
    return {
        "url": item.get("url") or item.get("link") or item.get("finalUrl"),
        "title": item.get("title") or item.get("headline"),
        "text": item.get("text") or item.get("markdown") or item.get("description"),
        "source": item.get("source") or item.get("actorId")
    }
data = json.load(sys.stdin)
items = data if isinstance(data, list) else data.get("items", [])
print(json.dumps([normalize(x) for x in items], indent=2))
