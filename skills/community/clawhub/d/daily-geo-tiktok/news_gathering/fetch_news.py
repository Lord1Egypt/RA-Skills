"""
Daily Geopolitical TikTok Reporter - News Gathering Module
Fetches geopolitical news from free RSS sources
"""

import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeoNewsGatherer:
    """Gather geopolitical news from free RSS sources"""
    
    # Free RSS sources for geopolitical news
    NEWS_SOURCES = {
        'bbc_world': {
            'url': 'http://feeds.bbci.co.uk/news/world/rss.xml',
            'name': 'BBC World',
            'region': 'global'
        },
        'reuters_world': {
            'url': 'https://www.reuters.com/rssFeed/worldNews',
            'name': 'Reuters World',
            'region': 'global'
        },
        'reuters_conflicts': {
            'url': 'https://www.reuters.com/rssFeed/conflict',
            'name': 'Reuters Conflict',
            'region': 'global'
        },
        'ap_world': {
            'url': 'https://storage.googleapis.com/afs-prod/media/feeds/AP.WorldNews.xml',
            'name': 'AP World News',
            'region': 'global'
        },
        'aljazeera': {
            'url': 'https://www.aljazeera.com/xml/rss/all.xml',
            'name': 'Al Jazeera',
            'region': 'middle_east'
        }
    }
    
    # Geopolitical keywords for filtering
    GEO_KEYWORDS = {
        'conflicts': ['war', 'conflict', 'attack', 'military', 'troops', 'battle', 'clashes'],
        'diplomacy': ['diplomatic', 'negotiation', 'talks', 'treaty', 'summit', 'meeting'],
        'sanctions': ['sanctions', 'embargo', 'restrictions', 'economic'],
        'elections': ['election', 'vote', 'president', 'prime minister', 'parliament'],
        'alliances': ['alliance', 'nato', 'eu', 'union', 'bloc', 'coalition'],
        'crisis': ['crisis', 'emergency', 'unrest', 'protests', 'revolution']
    }
    
    # Geopolitical regions for categorization
    REGIONS = {
        'middle_east': ['israel', 'palestine', 'iran', 'iraq', 'syria', 'lebanon', 'yemen', 'saudi', 'gulf'],
        'europe': ['ukraine', 'russia', 'eu', 'nato', 'european', 'britain', 'france', 'germany'],
        'asia': ['china', 'taiwan', 'north korea', 'south korea', 'japan', 'india', 'pakistan'],
        'americas': ['us', 'usa', 'united states', 'canada', 'mexico', 'brazil', 'argentina'],
        'africa': ['africa', 'african', 'sudan', 'congo', 'nigeria', 'ethiopia', 'kenya']
    }
    
    def __init__(self, hours_back: int = 24):
        """Initialize news gatherer
        
        Args:
            hours_back: How many hours back to fetch news (default: 24 hours)
        """
        self.hours_back = hours_back
        self.cutoff_time = datetime.now() - timedelta(hours=hours_back)
        self.news_articles = []
    
    def fetch_all_sources(self) -> List[Dict[str, Any]]:
        """Fetch news from all configured sources
        
        Returns:
            List of news articles with metadata
        """
        all_articles = []
        
        for source_id, source_config in self.NEWS_SOURCES.items():
            try:
                articles = self._fetch_rss_feed(source_id, source_config)
                all_articles.extend(articles)
                logger.info(f"Fetched {len(articles)} articles from {source_config['name']}")
            except Exception as e:
                logger.error(f"Failed to fetch from {source_config['name']}: {str(e)}")
        
        self.news_articles = all_articles
        return all_articles
    
    def _fetch_rss_feed(self, source_id: str, source_config: Dict) -> List[Dict[str, Any]]:
        """Fetch and parse RSS feed from a single source"""
        feed = feedparser.parse(source_config['url'])
        articles = []
        
        for entry in feed.entries:
            try:
                # Parse publication time
                pub_time = self._parse_pub_time(entry)
                
                # Filter by time
                if pub_time and pub_time < self.cutoff_time:
                    continue
                
                # Extract content
                title = entry.get('title', '')
                description = entry.get('description', '')
                link = entry.get('link', '')
                
                # Geopolitical relevance check
                relevance = self._calculate_geo_relevance(title, description)
                
                if relevance['total_score'] > 0:
                    articles.append({
                        'source': source_config['name'],
                        'source_id': source_id,
                        'title': title,
                        'description': description,
                        'link': link,
                        'published_time': pub_time,
                        'relevance': relevance,
                        'importance_score': self._calculate_importance(relevance)
                    })
                    
            except Exception as e:
                logger.warning(f"Error parsing entry: {str(e)}")
                continue
        
        return articles
    
    def _parse_pub_time(self, entry) -> datetime:
        """Parse publication time from RSS entry"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                return datetime(*entry.updated_parsed[:6])
        except:
            pass
        return None
    
    def _calculate_geo_relevance(self, title: str, description: str) -> Dict[str, Any]:
        """Calculate geopolitical relevance score"""
        combined_text = f"{title} {description}".lower()
        
        scores = {}
        for category, keywords in self.GEO_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            scores[category] = score
        
        # Detect regions
        detected_regions = []
        for region, countries in self.REGIONS.items():
            if any(country in combined_text for country in countries):
                detected_regions.append(region)
        
        return {
            'category_scores': scores,
            'detected_regions': detected_regions,
            'total_score': sum(scores.values())
        }
    
    def _calculate_importance(self, relevance: Dict) -> int:
        """Calculate importance score (1-10)"""
        base_score = min(10, relevance['total_score'])
        
        # Boost for multiple categories
        if sum(1 for score in relevance['category_scores'].values() if score > 0) >= 2:
            base_score = min(10, base_score + 2)
        
        # Boost for multiple regions
        if len(relevance['detected_regions']) >= 2:
            base_score = min(10, base_score + 1)
        
        return base_score
    
    def get_top_stories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top geopolitical stories by importance
        
        Args:
            limit: Maximum number of stories to return
        
        Returns:
            List of top stories sorted by importance
        """
        sorted_stories = sorted(
            self.news_articles,
            key=lambda x: x['importance_score'],
            reverse=True
        )
        return sorted_stories[:limit]
    
    def filter_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Filter stories by geographic region"""
        return [
            story for story in self.news_articles
            if region in story['relevance']['detected_regions']
        ]
    
    def filter_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Filter stories by topic category"""
        return [
            story for story in self.news_articles
            if story['relevance']['category_scores'].get(topic, 0) > 0
        ]


if __name__ == "__main__":
    # Example usage
    gatherer = GeoNewsGatherer(hours_back=24)
    gatherer.fetch_all_sources()
    
    print(f"\n📰 Found {len(gatherer.news_articles)} geopolitical articles in last 24 hours")
    
    top_stories = gatherer.get_top_stories(5)
    print(f"\n🔥 Top 5 Geopolitical Stories:")
    
    for i, story in enumerate(top_stories, 1):
        print(f"\n{i}. {story['title']}")
        print(f"   Source: {story['source']}")
        print(f"   Importance: {story['importance_score']}/10")
        print(f"   Regions: {', '.join(story['relevance']['detected_regions'])}")
        print(f"   Link: {story['link']}")