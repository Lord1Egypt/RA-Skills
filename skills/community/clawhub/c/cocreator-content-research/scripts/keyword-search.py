#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
import argparse
import os
import sys
import json
import requests
from typing import Dict

def get_api_key(provided_key: str | None) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get("SCRAPE_CREATORS_API_KEY")

def make_request(url: str, params: dict, api_key: str) -> dict:
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return {}

def search_tiktok(query: str, search_type: str, api_key: str, date_posted: str = None, sort_by: str = None, region: str = None, format_filter: str = "both") -> Dict:
    url = "https://api.scrapecreators.com/v1/tiktok/search/keyword" if search_type == "keyword" else "https://api.scrapecreators.com/v1/tiktok/search/hashtag"
    params = {"query": query} if search_type == "keyword" else {"hashtag": query.replace("#", "")}
    
    if search_type == "keyword":
        if date_posted:
            params["date_posted"] = date_posted
        if sort_by:
            params["sort_by"] = sort_by
        if region:
            params["region"] = region
            
    data = make_request(url, params, api_key)
    # The API returns 'search_item_list' for TikTok search, and the video info is inside 'aweme_info'
    items = data.get("search_item_list", [])
    videos = [item.get("aweme_info", {}) for item in items if isinstance(item, dict) and "aweme_info" in item]
    
    # Filter by format
    if format_filter == "video":
        videos = [v for v in videos if not (bool(v.get("image_infos")) or v.get("aweme_type") in [61, 68, 150])]
    elif format_filter == "slideshow":
        videos = [v for v in videos if bool(v.get("image_infos")) or v.get("aweme_type") in [61, 68, 150]]
    
    # Sort by views to find the most viral ones
    sorted_videos = sorted(videos, key=lambda v: v.get("statistics", {}).get("play_count", 0), reverse=True)
    top_videos = sorted_videos[:5]
    
    return {
        "query": query,
        "type": search_type,
        "top_results": [
            {
                "url": f"https://www.tiktok.com/@{v.get('author', {}).get('unique_id', 'unknown')}/video/{v.get('aweme_id', '')}",
                "video_url": v.get("video", {}).get("bit_rate", [{}])[0].get("play_addr", {}).get("url_list", [""])[0] if v.get("video", {}).get("bit_rate") else "",
                "is_slideshow": bool(v.get("image_infos")) or v.get("aweme_type") in [61, 68, 150],
                "author": v.get("author", {}).get("unique_id", "unknown"),
                "caption": v.get("desc", ""),
                "views": v.get("statistics", {}).get("play_count", 0),
                "likes": v.get("statistics", {}).get("digg_count", 0)
            } for v in top_videos
        ]
    }

def search_ig_reels(query: str, api_key: str, format_filter: str = "both") -> Dict:
    # IG currently supports Reels search by keyword
    url = "https://api.scrapecreators.com/v2/instagram/reels/search"
    params = {"query": query}
    
    data = make_request(url, params, api_key)
    # the API responds with a nested data object, or directly with items depending on the version
    reels = data.get("data", {}).get("items", data.get("items", []))
    
    # Filter by format (8 is carousel/slideshow)
    if format_filter == "video":
        reels = [r for r in reels if r.get("media_type") != 8]
    elif format_filter == "slideshow":
        reels = [r for r in reels if r.get("media_type") == 8]
    
    # Sort by play_count
    sorted_reels = sorted(reels, key=lambda r: r.get("play_count", 0), reverse=True)
    top_reels = sorted_reels[:5]
    
    return {
        "query": query,
        "type": "keyword (reels)",
        "top_results": [
            {
                "url": f"https://www.instagram.com/reel/{r.get('code')}/",
                "is_slideshow": False,
                "author": r.get("user", {}).get("username", "unknown"),
                "caption": r.get("caption", {}).get("text", "") if r.get("caption") else "",
                "views": r.get("play_count", 0),
                "likes": r.get("like_count", 0)
            } for r in top_reels
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="Search TikTok and Instagram Reels by keyword or hashtag.")
    parser.add_argument("--platform", choices=["tiktok", "instagram"], required=True)
    parser.add_argument("--type", choices=["keyword", "hashtag"], required=True, help="Note: Instagram currently uses keyword search for Reels.")
    parser.add_argument("--query", required=True, help="The search query (e.g., 'dinner recipes' or 'healthyfood')")
    parser.add_argument("--date-posted", choices=["yesterday", "this-week", "this-month", "last-3-months", "last-6-months", "all-time"], help="TikTok Keyword Search Time Frame")
    parser.add_argument("--sort-by", choices=["relevance", "most-liked", "date-posted"], help="TikTok Keyword Sort by")
    parser.add_argument("--region", help="TikTok Keyword Proxy Region (e.g., US, GB, FR)")
    parser.add_argument("--format", choices=["video", "slideshow", "both"], default="both", help="Filter by content format")
    parser.add_argument("--api-key", help="ScrapeCreators API Key")
    
    args = parser.parse_args()
    
    api_key = get_api_key(args.api_key)
    if not api_key:
        print(json.dumps({"error": "SCRAPE_CREATORS_API_KEY environment variable is required."}), file=sys.stderr)
        sys.exit(1)

    if args.platform == "tiktok":
        data = search_tiktok(args.query, args.type, api_key, args.date_posted, args.sort_by, args.region, args.format)
    else:
        # We route IG to reels search regardless of type to focus on video content
        data = search_ig_reels(args.query, api_key, args.format)
        
    print(json.dumps({
        "status": "success",
        "platform": args.platform,
        "search_results": data
    }, indent=2))

if __name__ == "__main__":
    main()
