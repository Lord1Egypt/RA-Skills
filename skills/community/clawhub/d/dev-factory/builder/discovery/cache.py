"""DiscoveryCache - 발굴 결과 캐싱"""

import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger('builder-agent.discovery.cache')


class DiscoveryCache:
    """소스별 캐시 관리"""

    def __init__(self, cache_dir: Path, ttl_seconds: int = 3600):
        self.cache_dir = cache_dir
        self.ttl = ttl_seconds
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, source: str) -> Optional[List[Dict]]:
        """캐시된 아이디어 가져오기"""
        cache_file = self.cache_dir / f"{source}_cache.json"
        if not cache_file.exists():
            return None

        try:
            data = json.loads(cache_file.read_text())
            if time.time() - data.get('timestamp', 0) > self.ttl:
                logger.debug("Cache expired for %s", source)
                return None

            logger.info("Cache hit for %s (%d ideas)", source, len(data['ideas']))
            return data['ideas']
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Cache read error for %s: %s", source, e)
            return None

    def set(self, source: str, ideas: List[Dict]):
        """아이디어 캐시 저장"""
        cache_file = self.cache_dir / f"{source}_cache.json"
        cache_file.write_text(json.dumps({
            'timestamp': time.time(),
            'ideas': ideas
        }, ensure_ascii=False, indent=2))
        logger.debug("Cached %d ideas for %s", len(ideas), source)

    def clear(self, source: Optional[str] = None):
        """캐시 삭제

        Args:
            source: 특정 소스만 삭제. None이면 전체 삭제.
        """
        if source:
            cache_file = self.cache_dir / f"{source}_cache.json"
            if cache_file.exists():
                cache_file.unlink()
                logger.info("Cleared cache for %s", source)
        else:
            for file in self.cache_dir.glob("*_cache.json"):
                file.unlink()
            logger.info("Cleared all caches")

    def is_expired(self, source: str) -> bool:
        """캐시 만료 여부 확인"""
        cache_file = self.cache_dir / f"{source}_cache.json"
        if not cache_file.exists():
            return True

        try:
            data = json.loads(cache_file.read_text())
            return time.time() - data.get('timestamp', 0) > self.ttl
        except (json.JSONDecodeError, KeyError):
            return True
