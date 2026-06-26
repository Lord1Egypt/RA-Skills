#!/usr/bin/env python3
"""
Hacker News API source for podcast topic discovery.
Fetches top stories filtered by minimum points threshold.
"""
import json
import urllib.request
from typing import List, Dict
from .base import TopicSource


class HackerNewsSource(TopicSource):
    """Hacker News top stories source"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.min_points = int(config.get("min_points", 100))
        self.min_comments = int(config.get("min_comments", 0))
        
    def fetch(self) -> List[Dict]:
        """Fetch top HN stories"""
        try:
            # Get top story IDs
            top_ids = self._fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json")
            if not top_ids:
                return []
            
            items = []
            for story_id in top_ids[:50]:  # Check first 50
                story = self._fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                if not story:
                    continue
                
                score = story.get("score", 0)
                comments = story.get("descendants", 0)
                
                # Filter by thresholds
                if score < self.min_points:
                    continue
                if comments < self.min_comments:
                    continue
                
                title = story.get("title", "")
                url = story.get("url", "")
                
                if not title or len(title) < 10:
                    continue
                
                item = {
                    "title": title,
                    "url": url,
                    "category": "Tech/News",
                    "description": f"{score} points, {comments} comments",
                    "source": self.name,
                    "metadata": {
                        "score": score,
                        "comments": comments,
                        "hn_id": story_id
                    }
                }
                items.append(self.normalize_topic(item))
                
                # Stop after finding 15 good candidates
                if len(items) >= 15:
                    break
            
            return items
            
        except Exception as e:
            print(f"ERROR: HN fetch failed: {e}")
            return []
    
    def _fetch_json(self, url: str, timeout: int = 10) -> any:
        """Fetch and parse JSON from URL"""
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 OpenClaw Podcast Skill"
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"  WARNING: Failed to fetch {url}: {e}")
            return None
