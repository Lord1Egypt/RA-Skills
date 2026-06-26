#!/usr/bin/env python3
"""Scan configured knowledge sources for new content.

Reads ~/.hermes/deltas.json for scan_sources configuration.
Outputs a summary of new findings.

Usage:
    python3 scan_sources.py
    # Or as a cron job (runs silently if nothing new)
"""
import json
import sys
from datetime import datetime


def load_deltas(home_dir=None):
    """Load deltas.json from the Hermes home directory."""
    if home_dir is None:
        home_dir = "/home/openfang/.hermes"
    path = f"{home_dir}/deltas.json"
    with open(path, "r") as f:
        return json.load(f)


def scan_youtube_channel(channel_id, last_scanned):
    """Scan a YouTube channel for new videos since last_scanned."""
    import urllib.request
    import xml.etree.ElementTree as ET

    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)

    try:
        html = urllib.request.urlopen(req).read().decode("utf-8")
        root = ET.fromstring(html)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        entries = root.findall("atom:entry", ns)
        new_videos = []

        for entry in entries:
            published = entry.find("atom:published", ns).text
            vid = entry.find("atom:id", ns).text.replace("yt:video:", "")
            title = entry.find("atom:title", ns).text

            pub_date = datetime.fromisoformat(
                published.replace("Z", "+00:00")
            ).date()
            scan_date = datetime.fromisoformat(last_scanned).date()

            if pub_date > scan_date:
                new_videos.append(
                    {
                        "video_id": vid,
                        "title": title,
                        "published": published,
                    }
                )

        return new_videos
    except Exception as e:
        return [{"error": str(e)}]


def main():
    """Main entry point: scan all configured sources and output results."""
    data = load_deltas()
    results = {}

    for source in data.get("scan_sources", []):
        name = source["name"]
        source_type = source.get("type", "")
        last_scanned = source.get("last_scanned", "2000-01-01")

        if source_type == "youtube_channel":
            url = source.get("url", "")
            channel_id = url.split("channel/")[-1].split("/")[0]
            new_videos = scan_youtube_channel(channel_id, last_scanned)
            results[name] = new_videos

    print(json.dumps(results, indent=2, ensure_ascii=False))

    # Update last_scanned dates
    for source in data.get("scan_sources", []):
        source["last_scanned"] = datetime.now().strftime("%Y-%m-%d")

    with open("/home/openfang/.hermes/deltas.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
