"""
Topic Analyzer - 기사 그룹화 및 주제 분석
"""

import json
import re
from typing import List, Dict, Optional
from datetime import datetime
from llm_client import GLMClient
from modules.intelligence.writer import BlogWriter, Persona, CategoryClassifier, TagExtractor, PersonaConfig
from modules.intelligence.config import GLM_API_KEY
from modules.intelligence.utils import setup_logger

logger = setup_logger(__name__, "topic_analyzer.log")

class TopicAnalyzer:
    """주제 분석기"""

    def __init__(self, api_key: Optional[str] = None):
        self.client = GLMClient(api_key=api_key or GLM_API_KEY)
        self.writer = BlogWriter(api_key=api_key)

    def analyze_and_group_articles(self, articles: List[Dict], max_groups: int = 5) -> List[Dict]:
        if not articles:
            return []

        logger.info(f"Analyzing {len(articles)} articles...")

        articles_summary = [
            f"[{i}] {a.get('title')} (Source: {a.get('source')})\n    Summary: {a.get('summary')[:200]}"
            for i, a in enumerate(articles)
        ]
        articles_text = "\n".join(articles_summary)

        system_prompt = """You are a news analysis expert.
Analyze the provided articles and group them into 3-5 interesting topics.
Output MUST be in JSON format:
{
  "topics": [
    {
      "topic_title": "Topic Title",
      "description": "Why this is important",
      "related_articles": [0, 2, 5],
      "angle": "Key perspective"
    }
  ]
}
"""
        user_prompt = f"Analyze these articles:\n{articles_text}"

        try:
            response = self.client.chat(system_prompt, user_prompt)
            
            # JSON parsing
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            json_str = json_match.group(1) if json_match else response.strip()
            # If plain text without code blocks, try to find { ... }
            if not json_match and '{' in response:
                 json_str = response[response.find('{'):response.rfind('}')+1]

            data = json.loads(json_str)
            topics = data.get("topics", [])

            grouped = []
            for topic in topics:
                indices = topic.get("related_articles", [])
                topic_articles = [articles[i] for i in indices if 0 <= i < len(articles)]
                
                if topic_articles:
                    grouped.append({
                        "topic": topic.get("topic_title"),
                        "description": topic.get("description"),
                        "angle": topic.get("angle"),
                        "articles": topic_articles,
                        "count": len(topic_articles)
                    })
            
            logger.info(f"Identified {len(grouped)} topics.")
            return grouped

        except Exception as e:
            logger.error(f"Topic analysis failed: {e}")
            return [{
                "topic": "General Updates",
                "description": "Mixed articles",
                "angle": "General Overview",
                "articles": articles,
                "count": len(articles)
            }]

    def generate_comprehensive_article(self, group: Dict) -> Dict:
        """종합 기사 생성"""
        topic = group["topic"]
        articles = group["articles"]
        angle = group.get("angle", "")
        
        logger.info(f"Generating comprehensive article for '{topic}'")

        # Persona & Config
        first_article = articles[0]
        persona = CategoryClassifier.classify(first_article)
        config = PersonaConfig.get(persona)
        
        category = TagExtractor.get_category(persona)
        all_tags = set()
        for a in articles:
            all_tags.update(TagExtractor.extract_tags(a, persona, max_tags=3))
        tags_list = list(all_tags)[:5]

        # Prompt
        system_prompt = f"""You are {config['name']}.
Expertise: {config['expertise']}
Tone: {config['tone']}

Write a comprehensive blog post about "{topic}".
Perspective: {angle}
Format: Markdown
Include: Title, Summary, Introduction, Main Body (synthesis of articles), Expert Insight, Conclusion, References.
"""
        articles_text = "\n".join([f"- {a.get('title')} ({a.get('url')})" for a in articles])
        user_prompt = f"Topic: {topic}\nPerspective: {angle}\nArticles:\n{articles_text}\n\nWrite the post."

        try:
            content = self.client.chat(system_prompt, user_prompt)
            
            # Simple parsing
            result = {
                "title": f"[종합] {topic}",
                "summary": f"{topic} 관련 종합 분석",
                "content": content,
                "tags": tags_list,
                "category": category,
                "persona": persona.value,
                "original_url": articles[0].get('url', ''),
                "original_source": "AI Topic Analysis",
                "source_articles": len(articles),
                "ai_derived_topic": topic
            }
            
            # Extract title if possible
            for line in content.split('\n'):
                if line.startswith("제목:") or line.startswith("# "):
                    result["title"] = line.replace("제목:", "").replace("# ", "").strip()
                    break

            return result
        except Exception as e:
            logger.error(f"Failed to generate comprehensive article: {e}")
            raise

    def analyze_and_generate(self, articles: List[Dict], max_groups: int = 5) -> List[Dict]:
        groups = self.analyze_and_group_articles(articles, max_groups)
        results = []
        for group in groups:
            try:
                res = self.generate_comprehensive_article(group)
                results.append(res)
            except Exception:
                pass
        return results

if __name__ == "__main__":
    analyzer = TopicAnalyzer()
    print("TopicAnalyzer initialized.")