"""
Article Selector - AI 기반 기사 평가 및 선별 모듈 (Async + Pydantic)
"""

import json
import re
import asyncio
from typing import List, Dict
from collections import defaultdict
from modules.intelligence.llm_client_async import AsyncLLMClient
from modules.intelligence.writer import CategoryClassifier, Persona, PersonaConfig
from modules.intelligence.utils import setup_logger
from modules.intelligence.prompt_manager import PromptManager
from modules.intelligence.models import EvaluationResponse

logger = setup_logger(__name__, "selector.log")

class ArticleSelector:
    """AI를 사용하여 수집된 기사 중 최적의 기사를 선별"""

    def __init__(self, client: AsyncLLMClient = None):
        self.client = client or AsyncLLMClient()

    async def evaluate_and_select(self, articles: List[Dict], max_articles: int = 5, min_score: int = 6) -> List[Dict]:
        if not articles:
            return []

        logger.info(f"Evaluating {len(articles)} articles for selection (Async)...")

        # 1. 카테고리별 그룹화
        category_groups = defaultdict(list)
        for i, article in enumerate(articles):
            persona = CategoryClassifier.classify(article)
            config = PersonaConfig.get(persona)
            category = config.get("category", "IT")
            
            article['_temp_id'] = i
            article['_category'] = category
            category_groups[category].append(article)

        # 2. 각 카테고리별 평가 태스크 생성
        tasks = []
        for category, items in category_groups.items():
            if not items:
                continue
            tasks.append(self._score_articles_in_category(category, items))
        
        # 3. 병렬 실행 및 결과 수집
        scored_results = await asyncio.gather(*tasks)
        
        # 4. 점수 매핑
        for result_list in scored_results:
            scored_dict = {item.id: item for item in result_list}
            for item in result_list:
                original_idx = item.id
                if 0 <= original_idx < len(articles):
                    articles[original_idx]['_score'] = item.score
                    articles[original_idx]['_reason'] = item.reason

        # 5. 카테고리별 최종 선택 (Round-robin)
        final_selected = []
        categories = list(category_groups.keys())
        for cat in categories:
            category_groups[cat].sort(key=lambda x: x.get('_score', 0), reverse=True)

        while len(final_selected) < max_articles:
            all_empty = True
            for cat in categories:
                if len(final_selected) >= max_articles:
                    break
                
                if category_groups[cat]:
                    all_empty = False
                    article = category_groups[cat].pop(0)
                    
                    score = article.get('_score', 0)
                    if score < min_score:
                        logger.info(f"Skipped [{cat}] '{article['title'][:30]}...' (Score: {score} < {min_score})")
                        continue

                    final_selected.append(article)
                    logger.info(f"Selected [{cat}] (Score: {score}): {article['title'][:50]}...")
            
            if all_empty:
                break

        return final_selected

    async def _score_articles_in_category(self, category: str, items: List[Dict]):
        """AI 평가 (Pydantic 검증)"""
        if len(items) == 1:
             # Mock object for single item
             from modules.intelligence.models import EvaluationItem
             return [EvaluationItem(id=items[0]['_temp_id'], score=9, reason="Only article in category")]

        articles_text = ""
        for item in items:
            safe_summary = (item.get('summary') or "")[:200].replace('\n', ' ')
            articles_text += f"ID: {item['_temp_id']}\nTitle: {item['title']}\nSummary: {safe_summary}\n---\n"

        system_prompt = PromptManager.get("selector.system", category=category)
        user_prompt = PromptManager.get("selector.user", category=category, articles_text=articles_text)

        try:
            response = await self.client.chat(system_prompt, user_prompt)
            
            # JSON 추출
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            json_str = json_match.group(1) if json_match else response.strip()
            if '{' in json_str:
                 json_str = json_str[json_str.find('{'):json_str.rfind('}')+1]

            # Pydantic 파싱
            data = EvaluationResponse.model_validate_json(json_str)
            return data.evaluations

        except Exception as e:
            logger.error(f"Failed to score articles in {category}: {e}")
            return []