#!/usr/bin/env python3
"""
Base source class for podcast topic discovery.
All source implementations should inherit from this.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime


class TopicSource(ABC):
    """Base class for topic sources"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.name = config.get("name", self.__class__.__name__)
        
    @abstractmethod
    def fetch(self) -> List[Dict]:
        """
        Fetch topics from this source.
        
        Returns:
            List of topic dictionaries with keys:
            - title (str): Topic title
            - url (str): Source URL
            - category (str, optional): Category/tag
            - description (str, optional): Brief description
            - published (datetime, optional): Publication date
            - metadata (dict, optional): Source-specific metadata
        """
        pass
    
    def is_recent(self, published: Optional[datetime], max_age_days: int = 7) -> bool:
        """Check if a topic is recent enough"""
        if not published:
            return True  # Unknown date, assume recent
        age = datetime.now() - published
        return age.days <= max_age_days
    
    def normalize_topic(self, raw: Dict) -> Dict:
        """Normalize a raw topic to standard format"""
        return {
            "title": raw.get("title", ""),
            "url": raw.get("url", ""),
            "category": raw.get("category", ""),
            "description": raw.get("description", ""),
            "source": self.name,
            "published": raw.get("published"),
            "metadata": raw.get("metadata", {})
        }
