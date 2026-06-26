"""
LLM Writer - 다중 페르소나 블로그 글 작성 시스템 (Async + Pydantic)
"""

import os
import re
import json
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
from modules.intelligence.config import GLM_API_KEY, GLM_BASE_URL, GLM_MODEL
from modules.intelligence.llm_client_async import AsyncLLMClient
from modules.intelligence.utils import setup_logger
from modules.intelligence.prompt_manager import PromptManager
from modules.intelligence.models import BlogPost

logger = setup_logger(__name__, "writer.log")

class Persona(Enum):
    SECURITY = "security"
    AI_ML = "ai_ml"
    DEVOPS = "devops"
    CVE_ANALYST = "cve_analyst"

class PersonaConfig:
    NOTION_CATEGORIES = ["보안", "AI", "DevOps", "CVE", "IT"]
    
    # 기존 하드코딩된 PERSONAS 딕셔너리는 제거되고 prompts.yaml로 이동됨

    @classmethod
    def get(cls, persona: Persona) -> Dict:
        """PromptManager를 통해 페르소나 설정을 로드합니다."""
        persona_key = persona.value
        config = PromptManager.get_raw(f"personas.{persona_key}")
        
        if not config:
            logger.error(f"Persona config for '{persona_key}' not found in prompts.yaml")
            # Fallback (최소한의 설정)
            return {
                "name": "기술 블로거",
                "expertise": "IT 기술 전반",
                "tone": "친절하고 명확하게",
                "category": "IT",
                "default_tags": ["IT", "Tech"],
                "tag_keywords": [],
                "specific_prompt": ""
            }
        return config

class CategoryClassifier:
    KEYWORDS = {
        Persona.SECURITY: ["취약점", "해킹", "보안", "exploit", "security"],
        Persona.AI_ML: ["ai", "ml", "딥러닝", "llm", "gpt", "model"],
        Persona.DEVOPS: ["devops", "ci/cd", "k8s", "docker", "cloud"],
        Persona.CVE_ANALYST: ["cve", "cvss", "poc", "패치"],
    }

    @classmethod
    def classify(cls, article_data: Dict) -> Persona:
        text = (article_data.get("title", "") + " " + article_data.get("summary", "")).lower()
        scores = {p: sum(1 for kw in kws if kw in text) for p, kws in cls.KEYWORDS.items()}
        if not scores or max(scores.values()) == 0:
            return Persona.SECURITY
        return max(scores, key=scores.get)

class TagExtractor:
    @classmethod
    def extract_tags(cls, article_data: Dict, persona: Persona, max_tags: int = 5) -> List[str]:
        config = PersonaConfig.get(persona)
        text = (article_data.get("title", "") + " " + article_data.get("summary", "")).lower()
        tags = []
        for kw in config.get("tag_keywords", []):
            if kw.lower() in text:
                tags.append(kw)
        tags.extend(re.findall(r'CVE-\d{4}-\d{4,7}', text, re.IGNORECASE))
        if len(tags) < max_tags:
            for t in config.get("default_tags", []):
                if t not in tags:
                    tags.append(t)
        return list(dict.fromkeys(tags))[:max_tags]

    @classmethod
    def get_category(cls, persona: Persona) -> str:
        return PersonaConfig.get(persona).get("category", "IT")

class BlogWriter:
    """다중 페르소나 블로그 작성기 (Async)"""

    def __init__(self, client: AsyncLLMClient = None):
        self.client = client or AsyncLLMClient()

    async def generate_article(self, article_data: Dict, persona: Optional[Persona] = None) -> Dict:
        """단일 기사 생성 (비동기) - 2단계 분리 방식"""
        persona = persona or CategoryClassifier.classify(article_data)
        config = PersonaConfig.get(persona)

        category = TagExtractor.get_category(persona)

        # ===== 1단계: 메타데이터 생성 (제목 + 요약 + 태그) =====
        logger.info(f"[Step 1/2] Generating metadata for: {article_data.get('title', 'N/A')[:40]}")
        metadata = await self._generate_metadata(article_data, persona, config, category)

        # ===== 2단계: 본문 생성 (순수 Markdown) =====
        logger.info(f"[Step 2/2] Generating content for: {metadata['title'][:40]}")
        content = await self._generate_content(article_data, metadata, persona, config)

        return {
            "title": metadata['title'],
            "summary": metadata['summary'],
            "content": content,
            "tags": metadata['tags'],
            "category": metadata['category'],
            "persona": persona.value,
            "original_url": article_data.get("url"),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    async def _generate_metadata(self, article_data: Dict, persona: Persona, config: Dict, category: str) -> Dict:
        """1단계: 메타데이터 생성 (제목 + 요약 + 태그)"""
        system_prompt = PromptManager.get("writer_metadata.base_system",
                                        name=config['name'],
                                        expertise=config['expertise'],
                                        tone=config['tone'],
                                        persona_specific=config.get('specific_prompt', ''))

        user_prompt = PromptManager.get("writer_metadata.user",
                                      source=article_data.get('source', 'Unknown'),
                                      title=article_data.get('title', 'N/A'),
                                      url=article_data.get('url', 'N/A'),
                                      summary=article_data.get('summary', 'N/A'),
                                      category=category)

        try:
            response = await self.client.chat(system_prompt, user_prompt)
            return self._parse_metadata_response(response, category)
        except Exception as e:
            logger.error(f"Failed to generate metadata: {e}")
            raise

    async def _generate_content(self, article_data: Dict, metadata: Dict, persona: Persona, config: Dict) -> str:
        """2단계: 본문 생성 (순수 Markdown)"""
        system_prompt = PromptManager.get("writer_content.base_system",
                                        name=config['name'],
                                        expertise=config['expertise'],
                                        tone=config['tone'],
                                        persona_specific=config.get('specific_prompt', ''))

        user_prompt = PromptManager.get("writer_content.user",
                                      title=metadata['title'],
                                      summary=metadata['summary'],
                                      tags=", ".join(metadata['tags']),
                                      source=article_data.get('source', 'Unknown'),
                                      original_title=article_data.get('title', 'N/A'),
                                      url=article_data.get('url', 'N/A'),
                                      original_summary=article_data.get('summary', 'N/A'))

        try:
            response = await self.client.chat(system_prompt, user_prompt)
            # 본문은 순수 마크다운이므로 그대로 사용 (앞뒤 공백 제거)
            content = response.strip()
            # 최소 길이 체크
            if len(content) < 1000:
                logger.warning(f"Generated content too short ({len(content)} chars), may need regeneration")
            return content
        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            raise

    def _parse_metadata_response(self, response: str, category: str) -> Dict:
        """메타데이터 JSON 응답 파싱"""
        try:
            # JSON 코드 블록 추출
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            json_str = json_match.group(1) if json_match else response

            # JSON 범위 추출
            if '{' in json_str:
                start = json_str.find('{')
                brace_count = 0
                end = start
                for i in range(start, len(json_str)):
                    if json_str[i] == '{':
                        brace_count += 1
                    elif json_str[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end = i + 1
                            break
                json_str = json_str[start:end]

            # JSON 파싱
            import json as json_lib
            data = json_lib.loads(json_str)

            # 필수 필드 검증
            if not data.get('title'):
                raise ValueError("Missing 'title' field")
            if not data.get('summary'):
                raise ValueError("Missing 'summary' field")
            if not data.get('tags'):
                raise ValueError("Missing 'tags' field")

            return {
                "title": data['title'],
                "summary": data['summary'],
                "tags": data['tags'],
                "category": data.get('category', category)
            }
        except Exception as e:
            logger.error(f"Failed to parse metadata JSON: {e}")
            logger.error(f"Response: {response[:500]}")
            raise

    async def generate_article_batch(self, articles: List[Dict]) -> List[Dict]:
        """여러 기사 병렬 생성"""
        tasks = [self.generate_article(article) for article in articles]
        return await asyncio.gather(*tasks, return_exceptions=True)

    def _parse_result(self, content: str, original: Dict, persona: Persona, category: str, tags: List[str]) -> Dict:
        """Pydantic 모델을 사용한 파싱"""
        # 빈 응답 체크
        if not content or not content.strip():
            logger.error("LLM returned empty response")
            return self._create_fallback(original, persona, category, tags)

        try:
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            json_str = json_match.group(1) if json_match else content

            # JSON 범위 추출 개선
            if '{' in json_str:
                start = json_str.find('{')
                # 중괄호 균형 맞추기
                brace_count = 0
                end = start
                for i in range(start, len(json_str)):
                    if json_str[i] == '{':
                        brace_count += 1
                    elif json_str[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end = i + 1
                            break
                json_str = json_str[start:end]

            # Pydantic 파싱
            blog_post = BlogPost.model_validate_json(json_str)

            return {
                "title": blog_post.title,
                "summary": blog_post.summary,
                "content": blog_post.content,
                "tags": blog_post.tags or tags,
                "category": blog_post.category or category,
                "persona": persona.value,
                "original_url": original.get("url"),
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.warning(f"Pydantic parsing failed ({e}), attempting fallback parsing...")
            return self._create_fallback(original, persona, category, tags, content)

    def _create_fallback(self, original: Dict, persona: Persona, category: str, tags: List[str], llm_response: str = None) -> Dict:
        """Fallback 결과 생성"""
        # LLM 응답에서 JSON 블록 제거 후 content 사용
        content_text = llm_response or ""

        # 디버깅: LLM 원본 응답 로깅
        logger.info(f"[FALLBACK] LLM response length: {len(content_text)}, First 200 chars: {content_text[:200] if content_text else '(EMPTY)'}")

        if content_text:
            # JSON 코드 블록 제거 (전체 JSON 객체 제거, content 필드 추출 아님!)
            # ````json ... ``` 블록 제거 후 그 안의 content만 사용
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', content_text, re.DOTALL)
            if json_match:
                # JSON 문자열에서 content 필드 추출
                json_str = json_match.group(1)
                # 정규식으로 content 필드 값 추출
                content_match = re.search(r'"content"\s*:\s*"((?:[^"\\]|\\.)*)"', json_str, re.DOTALL)
                if content_match:
                    import json as json_lib
                    try:
                        content_value = f'"{content_match.group(1)}"'
                        content_text = json_lib.loads(content_value)
                    except json_lib.JSONDecodeError:
                        content_text = content_match.group(1)
                    except Exception:
                        content_text = content_match.group(1)
                else:
                    content_text = ""
            else:
                # 코드 블록이 없으면 그냥 사용
                content_text = content_text.strip()

        # 여전히 비어있거나 너무 짧으면 원본 요약 사용
        if not content_text or len(content_text) < 100:
            logger.warning(f"[FALLBACK] Content still too short ({len(content_text)}), using original summary")
            content_text = f"# {original.get('title', '제목 없음')}\n\n{original.get('summary', '요약 없음')}\n\n> 본문 생성 실패: 원본 기사를 참고하세요\n\n원본 URL: {original.get('url', '')}"

        logger.info(f"[FALLBACK] Final content length: {len(content_text)}, First 200 chars: {content_text[:200]}")

        return {
            "title": original.get("title"),
            "summary": original.get("summary"),
            "content": content_text,
            "tags": tags,
            "category": category,
            "persona": persona.value,
            "original_url": original.get("url"),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }