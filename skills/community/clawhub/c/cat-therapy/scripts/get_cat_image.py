#!/usr/bin/env python3
"""
Fetch a random cat image from various online sources.
Supports multiple fallback sources for reliability.
Returns image URL for cross-platform cat-therapy skill.
"""

import urllib.request
import json
import random
import ssl

# ✅ 修复：启用 SSL 证书验证（安全）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

def get_cat_image():
    """Fetch a random cat image from multiple sources with fallbacks."""
    
    # Source 1: Cataas (Cat As A Service) - simple and reliable
    try:
        url = "https://cataas.com/cat?json=true"
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": "CatTherapy/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            if data and "_id" in data:
                return {"url": f"https://cataas.com/cat/{data['_id']}", "source": "cataas"}
    except Exception as e:
        pass
    
    # Source 2: TheCatAPI
    try:
        req = urllib.request.Request(
            "https://api.thecatapi.com/v1/images/search",
            headers={"Accept": "application/json", "User-Agent": "CatTherapy/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0 and "url" in data[0]:
                return {"url": data[0]["url"], "source": "thecatapi"}
    except Exception as e:
        pass
    
    # Source 3: PlaceKitten (fixed sizes but reliable)
    try:
        sizes = ["400/300", "400/400", "500/400", "600/400"]
        size = random.choice(sizes)
        url = f"https://placekitten.com/{size}"
        # Check if URL is accessible
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=3, context=ssl_context):
            return {"url": url, "source": "placekitten"}
    except Exception as e:
        pass
    
    # Source 4: Direct CDN links (fallback list)
    fallback_urls = [
        "https://cdn2.thecatapi.com/images/0XYvCQ7q2.jpg",
        "https://cdn2.thecatapi.com/images/b1.jpg",
        "https://cdn2.thecatapi.com/images/MTY2NjUzMQ.jpg",
        "https://cdn2.thecatapi.com/images/NjE2MzY.jpg",
    ]
    
    return {"url": random.choice(fallback_urls), "source": "fallback"}

if __name__ == "__main__":
    result = get_cat_image()
    print(json.dumps(result, ensure_ascii=False))
