#!/usr/bin/env python3
"""
Source loader for podcast topic discovery.
Dynamically loads source classes based on config.
"""
from typing import List, Dict
from .base import TopicSource
from .rss import RSSSource
from .hacker_news import HackerNewsSource
from .nature import NatureSource


def load_source(config: Dict) -> TopicSource:
    """Load a source instance from config"""
    source_type = config.get("type", "rss")
    
    sources = {
        "rss": RSSSource,
        "hackernews": HackerNewsSource,
        "nature": NatureSource,
    }
    
    source_class = sources.get(source_type)
    if not source_class:
        raise ValueError(f"Unknown source type: {source_type}")
    
    return source_class(config)


def load_all_sources(configs: List[Dict]) -> List[TopicSource]:
    """Load all sources from config list"""
    sources = []
    for config in configs:
        try:
            source = load_source(config)
            sources.append(source)
        except Exception as e:
            print(f"ERROR: Failed to load source {config.get('name', '?')}: {e}")
    return sources


__all__ = [
    "TopicSource",
    "RSSSource",
    "HackerNewsSource",
    "NatureSource",
    "load_source",
    "load_all_sources",
]
