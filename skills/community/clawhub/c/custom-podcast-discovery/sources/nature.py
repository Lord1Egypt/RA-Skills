#!/usr/bin/env python3
"""
Nature journal source for podcast topic discovery.
Fetches latest articles from Nature's RSS feeds.
"""
from typing import List, Dict
from .rss import RSSSource


class NatureSource(RSSSource):
    """Nature journal source"""
    
    def __init__(self, config: Dict):
        # Map section names to RSS URLs
        section = config.get("section", "news")
        feed_urls = {
            "news": "https://www.nature.com/nature.rss",
            "research": "https://www.nature.com/nature/research.rss",
            "biotech": "https://www.nature.com/nbt.rss",
            "medicine": "https://www.nature.com/nm.rss",
        }
        
        # Override URL with section-specific feed
        config["url"] = feed_urls.get(section, feed_urls["news"])
        config["category"] = "Science/Research"
        
        if "name" not in config:
            config["name"] = f"Nature ({section.title()})"
        
        super().__init__(config)
