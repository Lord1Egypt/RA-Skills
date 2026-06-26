"""의미론적 중복 제거 (Semantic Deduplication)

Phase 1: difflib.SequenceMatcher 기반 fuzzy matching
Phase 2: LanceDB 벡터 검색 (elite-longterm-memory 활용)
"""

import logging
from difflib import SequenceMatcher
from typing import List, Dict

logger = logging.getLogger('builder-agent.discovery.dedup')


class SemanticDeduplicator:
    """의미론적 중복 제거"""

    def __init__(self, similarity_threshold: float = 0.7):
        self.threshold = similarity_threshold

    def deduplicate(self, ideas: List[Dict]) -> List[Dict]:
        """중복 아이디어 제거"""
        if not ideas:
            return []

        unique = []
        seen_titles = set()

        for idea in ideas:
            title = idea.get('title', '').lower()
            description = idea.get('description', '').lower()

            # 정확히 일치하는 제목 체크
            if title in seen_titles:
                logger.debug("Exact duplicate: %s", idea['title'][:30])
                continue

            # 유사한 제목 체크
            is_duplicate = False
            for seen_title in seen_titles:
                if self._similar(title, seen_title) or self._similar(description, self._get_description_by_title(unique, seen_title)):
                    logger.debug("Similar duplicate: %s ~ %s", title[:30], seen_title[:30])
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique.append(idea)
                seen_titles.add(title)

        logger.info("Dedup: %d -> %d ideas", len(ideas), len(unique))
        return unique

    def _similar(self, a: str, b: str) -> bool:
        """두 문자열의 유사도 체크"""
        if not a or not b:
            return False

        ratio = SequenceMatcher(None, a, b).ratio()
        return ratio >= self.threshold

    def _get_description_by_title(self, ideas: List[Dict], title: str) -> str:
        """제목으로 description 찾기"""
        for idea in ideas:
            if idea.get('title', '').lower() == title:
                return idea.get('description', '').lower()
        return ""


class VectorDeduplicator:
    """벡터 기반 중복 제거 (Phase 2 - LanceDB 사용)

    elite-longterm-memory 스킬의 LanceDB 벡터 검색 활용
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.threshold = similarity_threshold
        self.embeddings = {}  # 임시: {title: vector}
        self._init_lancedb()

    def _init_lancedb(self):
        """LanceDB 초기화 시도"""
        try:
            import lancedb
            from pathlib import Path

            db_path = Path.home() / '.openclaw' / 'workspace' / 'data' / 'builder-dedup.lance'
            self.db = lancedb.connect(str(db_path))

            # 테이블 확인
            table_names = self.db.table_names()
            if 'ideas' in table_names:
                self.table = self.db.open_table('ideas')
            else:
                # 임베딩 없이 텍스트 인덱스만 생성
                import pyarrow as pa
                schema = pa.schema([
                    pa.field('id', pa.string()),
                    pa.field('title', pa.string()),
                    pa.field('description', pa.string()),
                    pa.field('discovered_at', pa.string()),
                ])
                self.table = self.db.create_table('ideas', schema=schema)

            logger.info("LanceDB dedup initialized")
            self.available = True

        except ImportError:
            logger.warning("LanceDB not available, using fallback")
            self.available = False
        except Exception as e:
            logger.warning("LanceDB init failed: %s", e)
            self.available = False

    def deduplicate(self, ideas: List[Dict]) -> List[Dict]:
        """벡터 유사도 기반 중복 제거"""
        if not self.available:
            # Fallback to fuzzy matching
            fallback = SemanticDeduplicator(similarity_threshold=0.7)
            return fallback.deduplicate(ideas)

        unique = []
        for idea in ideas:
            # 유사한 아이디어 검색
            similar = self._search_similar(idea)
            if not similar:
                unique.append(idea)
                self._add_idea(idea)

        return unique

    def _search_similar(self, idea: Dict) -> bool:
        """유사한 아이디어 검색"""
        title = idea.get('title', '')

        try:
            # 전체 텍스트 검색 (FTS)
            results = self.table.search(f"{title} {idea.get('description', '')}").limit(1).to_list()

            if results:
                # 간단한 유사도 체크
                for result in results:
                    if self._text_similarity(title, result.get('title', '')) > self.threshold:
                        return True

            return False

        except Exception as e:
            logger.warning("Vector search failed: %s", e)
            return False

    def _text_similarity(self, a: str, b: str) -> float:
        """텍스트 유사도 계산"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def _add_idea(self, idea: Dict):
        """아이디어 추가"""
        try:
            import uuid
            self.table.add([{
                'id': str(uuid.uuid4()),
                'title': idea.get('title', ''),
                'description': idea.get('description', ''),
                'discovered_at': idea.get('discovered_at', ''),
            }])
        except Exception as e:
            logger.warning("Failed to add idea: %s", e)
