"""
Daily Geopolitical TikTok Reporter - TikTok Script Generator
Converts geopolitical news into engaging 60-90 second TikTok scripts
"""

from datetime import datetime
from typing import List, Dict, Any
import random

class TikTokGeoScriptGenerator:
    """Generate optimized TikTok scripts from geopolitical news"""
    
    # TikTok-style hooks for engagement
    HOOKS = [
        "🔥 Breaking right now",
        "⚠️ This changes everything",
        "🌍 What just happened",
        "😱 You won't believe this",
        "🚨 Major development",
        "💥 Breaking news",
        "📢 Important update",
        "🎯 Here's what matters",
        "🔊 Everyone's watching this",
        "⭐ The biggest story today"
    ]
    
    # Trending geopolitical hashtags
    HASHTAGS = {
        'general': ['#geopolitics', '#worldnews', '#geopolitical', '#breakingnews'],
        'conflicts': ['#war', '#conflict', '#military', '#geopolitics'],
        'diplomacy': ['#diplomacy', '#international', '#relations', '#politics'],
        'sanctions': ['#sanctions', '#economy', '#trade', '#geopolitics'],
        'elections': ['#election', '#politics', '#vote', '#democracy'],
        'middle_east': ['#middleeast', '#israel', '#palestine', '#geopolitics'],
        'europe': ['#europe', '#ukraine', '#russia', '#nato'],
        'asia': ['#asia', '#china', '#korea', '#geopolitics'],
        'americas': ['#usa', '#americas', '#politics', '#geopolitics'],
        'africa': ['#africa', '#african', '#geopolitics', '#news']
    }
    
    # Transition phrases for smooth flow
    TRANSITIONS = [
        "Here's what happened:",
        "Let me break this down:",
        "Here's the situation:",
        "Here's what you need to know:",
        "Here's the deal:",
        "This is what's going on:"
    ]
    
    # Impact statements for engagement
    IMPACT_STATEMENTS = [
        "This changes the regional balance.",
        "Experts are divided on what this means.",
        "This could escalate further.",
        "The international community is watching.",
        "This has long-term implications.",
        "Markets are reacting to this news.",
        "This could affect global relations.",
        "Allies are taking notice."
    ]
    
    # Next steps hooks for engagement
    NEXT_STEPS = [
        "Watch for updates in the next 24 hours.",
        "Expect statements from officials.",
        "This story is developing fast.",
        "Stay tuned for more developments.",
        "We'll know more by tomorrow."
    ]
    
    def __init__(self):
        """Initialize TikTok script generator"""
        self.generated_scripts = []
    
    def generate_single_story_script(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a TikTok script for a single story
        
        Args:
            story: News article with metadata
        
        Returns:
            Generated script with timing and structure
        """
        hook = self._generate_hook(story)
        context = self._generate_context(story)
        news_content = self._generate_news_content(story)
        impact = self._generate_impact(story)
        next_step = self._generate_next_step(story)
        hashtags = self._generate_hashtags(story)
        
        script = {
            'title': story['title'],
            'source': story['source'],
            'importance': story['importance_score'],
            'segments': {
                'hook': hook,
                'context': context,
                'news': news_content,
                'impact': impact,
                'next': next_step
            },
            'hashtags': hashtags,
            'estimated_duration': self._estimate_duration(hook, context, news_content, impact, next_step),
            'full_script': self._assemble_full_script(hook, context, news_content, impact, next_step, hashtags)
        }
        
        self.generated_scripts.append(script)
        return script
    
    def generate_daily_report_script(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a daily TikTok script covering multiple stories
        
        Args:
            stories: List of news articles (should be top 3-5)
        
        Returns:
            Generated daily report script
        """
        if not stories:
            return None
        
        # Hook
        hook = f"🌍 Today's top {len(stories)} geopolitical stories that matter"
        
        # Brief coverage of each story
        story_briefs = []
        for i, story in enumerate(stories, 1):
            brief = f"{i}. {self._truncate_to_seconds(story['title'], 15)}"
            story_briefs.append(brief)
        
        # Deep dive on top story
        top_story = stories[0]
        context = self._generate_context(top_story)
        news_content = self._generate_news_content(top_story)
        impact = self._generate_impact(top_story)
        
        # Quick mentions of other stories
        other_stories = "\n\n".join([
            f"Also: {story['title']}" 
            for story in stories[1:3]
        ]) if len(stories) > 1 else ""
        
        next_step = "Follow for daily geopolitical updates!"
        hashtags = self._generate_daily_report_hashtags()
        
        script = {
            'type': 'daily_report',
            'stories_count': len(stories),
            'segments': {
                'hook': hook,
                'stories_brief': story_briefs,
                'context': context,
                'news': news_content,
                'impact': impact,
                'other_stories': other_stories,
                'next': next_step
            },
            'hashtags': hashtags,
            'full_script': self._assemble_daily_report_script(
                hook, story_briefs, context, news_content, 
                impact, other_stories, next_step, hashtags
            )
        }
        
        return script
    
    def _generate_hook(self, story: Dict[str, Any]) -> str:
        """Generate attention-grabbing hook"""
        hook = random.choice(self.HOOKS)
        if story['importance_score'] >= 8:
            hook = "🔥 MAJOR BREAKING NEWS"
        return f"{hook}: {self._truncate_to_seconds(story['title'], 5)}"
    
    def _generate_context(self, story: Dict[str, Any]) -> str:
        """Generate background context"""
        transition = random.choice(self.TRANSITIONS)
        regions = story['relevance']['detected_regions']
        
        region_text = f"in {', '.join(regions)}" if regions else "globally"
        
        return f"{transition} This is happening {region_text} and has significant implications."
    
    def _generate_news_content(self, story: Dict[str, Any]) -> str:
        """Generate main news content"""
        # Extract key information from description
        description = story.get('description', '')
        
        # Create 30-45 second content
        content = self._truncate_to_seconds(description, 40)
        
        if story['source']:
            content += f"\n\nSource: {story['source']}"
        
        return content
    
    def _generate_impact(self, story: Dict[str, Any]) -> str:
        """Generate impact statement"""
        return random.choice(self.IMPACT_STATEMENTS)
    
    def _generate_next_step(self, story: Dict[str, Any]) -> str:
        """Generate next steps hook"""
        return random.choice(self.NEXT_STEPS)
    
    def _generate_hashtags(self, story: Dict[str, Any]) -> List[str]:
        """Generate relevant hashtags"""
        hashtags = ['#geopolitics', '#worldnews', '#breakingnews']
        
        # Add category-specific hashtags
        for category, score in story['relevance']['category_scores'].items():
            if score > 0 and category in self.HASHTAGS:
                hashtags.extend(self.HASHTAGS[category])
        
        # Add region-specific hashtags
        for region in story['relevance']['detected_regions']:
            if region in self.HASHTAGS:
                hashtags.extend(self.HASHTAGS[region])
        
        # Remove duplicates and limit
        hashtags = list(set(hashtags))[:8]
        return hashtags
    
    def _generate_daily_report_hashtags(self) -> List[str]:
        """Generate hashtags for daily report"""
        return [
            '#geopolitics', '#worldnews', '#dailynews', 
            '#geopolitical', '#breakingnews', '#international',
            '#worldupdate', '#newsdaily'
        ]
    
    def _truncate_to_seconds(self, text: str, target_seconds: int) -> str:
        """Truncate text to fit within target seconds (assuming 140 wpm)"""
        words_per_second = 2.3  # Average speaking rate
        max_words = int(target_seconds * words_per_second)
        
        words = text.split()
        if len(words) <= max_words:
            return text
        
        truncated = ' '.join(words[:max_words])
        return truncated + "..."
    
    def _estimate_duration(self, *segments) -> int:
        """Estimate total script duration in seconds"""
        total_words = 0
        for segment in segments:
            total_words += len(segment.split())
        
        return int(total_words / 2.3)  # 2.3 words per second average
    
    def _assemble_full_script(self, *segments) -> str:
        """Assemble full TikTok script"""
        hook, context, news, impact, next_step, hashtags = segments
        
        script = f"""🎵 TIKTOK SCRIPT
⏱️ Estimated Duration: ~{self._estimate_duration(hook, context, news, impact, next_step)} seconds

---

🎵 HOOK (3-5 seconds)
{hook}

---

🌍 CONTEXT (10-15 seconds) 
{context}

---

📰 NEWS (30-45 seconds)
{news}

---

💡 IMPACT (10-15 seconds)
{impact}

---

📈 NEXT STEPS (5 seconds)
{next_step}

---

🏷️ HASHTAGS
{' '.join(hashtags)}

---

💡 PRO TIPS:
- Use trending sounds: Search "news," "break," "intense" in TikTok sound library
- Add text overlays for key points
- Include relevant stock footage or news clips
- Post during peak hours (12 PM, 7 PM local time)
- Engage with comments in first 30 minutes
"""
        return script
    
    def _assemble_daily_report_script(self, *segments) -> str:
        """Assemble daily report script"""
        hook, story_briefs, context, news, impact, other_stories, next_step, hashtags = segments
        
        script = f"""🎵 DAILY GEOPOLITICAL REPORT TIKTOK SCRIPT

---

🎵 HOOK
{hook}

---

📋 TODAY'S TOP STORIES
{chr(10).join(story_briefs)}

---

🌍 DEEP DIVE: MAIN STORY

{context}

---

📰 DETAILS
{news}

---

💡 WHY IT MATTERS
{impact}

---

📊 OTHER DEVELOPMENTS
{other_stories}

---

📈 STAY TUNED
{next_step}

---

🏷️ HASHTAGS
{' '.join(hashtags)}

---

💡 PRO TIPS:
- This is a longer format (90-120 seconds)
- Use countdown timer visual
- Include map graphics for regional context
- Post multiple times per day for different timezones
"""
        return script
    
    def format_for_video_creation(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """Format script for video creation tools"""
        return {
            'title': script.get('title', 'Daily Geopolitical Report'),
            'duration': script.get('estimated_duration', 90),
            'voiceover_text': script.get('full_script', ''),
            'suggested_visuals': self._suggest_visuals(script),
            'music_genre': 'news',
            'style': 'documentary'
        }
    
    def _suggest_visuals(self, script: Dict[str, Any]) -> List[str]:
        """Suggest visual elements for video"""
        visuals = [
            'News ticker overlay',
            'Globe animation',
            'Map of affected region',
            'Stock footage: government buildings',
            'Photo of key leaders',
            'Breaking news graphic',
            'Text overlays for key points'
        ]
        return visuals


if __name__ == "__main__":
    # Example usage
    generator = TikTokGeoScriptGenerator()
    
    # Example story
    example_story = {
        'title': 'Major diplomatic talks begin between regional powers',
        'description': 'Historic negotiations have commenced between multiple nations in the region, with international observers calling for peaceful resolution to long-standing disputes.',
        'source': 'Test News',
        'importance_score': 8,
        'relevance': {
            'detected_regions': ['middle_east', 'europe'],
            'category_scores': {'diplomacy': 3, 'alliances': 2},
            'total_score': 5
        }
    }
    
    script = generator.generate_single_story_script(example_story)
    print(script['full_script'])