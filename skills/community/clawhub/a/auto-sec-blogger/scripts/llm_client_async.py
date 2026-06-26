"""
Async LLM Client Module
aiohttp를 사용하여 비동기로 LLM API를 호출합니다.
재시도 로직과 에러 처리 개선
"""

import aiohttp
import asyncio
import random
from typing import Dict, Optional, Any
from modules.intelligence.config import GLM_API_KEY, GLM_BASE_URL, GLM_MODEL
from modules.intelligence.utils import setup_logger

logger = setup_logger(__name__, "llm_client_async.log")

class AsyncLLMClient:
    """비동기 GLM API 클라이언트 (재시도 로직 포함)"""

    # 재시도 설정
    MAX_RETRIES = 3
    BASE_DELAY = 2  # 초
    MAX_DELAY = 30  # 초

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or GLM_API_KEY
        self.base_url = base_url or GLM_BASE_URL
        self.model = model or GLM_MODEL
        self.timeout = 300  # 5분

        if not self.api_key:
            logger.warning("GLM_API_KEY is not set.")

    def _get_url(self) -> str:
        """API URL 생성 (중복 경로 방지)"""
        base = self.base_url.rstrip('/')
        # 이미 /chat/completions가 포함되어 있으면 그대로 사용
        if base.endswith('/chat/completions'):
            return base
        # 아니면 추가
        return f"{base}/chat/completions"

    async def _exponential_backoff(self, attempt: int) -> float:
        """Exponential backoff 계산"""
        delay = min(self.BASE_DELAY * (2 ** attempt) + random.uniform(0, 1), self.MAX_DELAY)
        return delay

    async def chat(self, system_prompt: str, user_prompt: str) -> str:
        """GLM API 비동기 호출 (재시도 로직 포함)"""
        if not self.api_key:
            raise ValueError("API Key가 설정되지 않았습니다.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 8000
        }

        url = self._get_url()
        last_error = None

        for attempt in range(self.MAX_RETRIES):
            async with aiohttp.ClientSession() as session:
                try:
                    logger.debug(f"GLM API 호출 시도 {attempt + 1}/{self.MAX_RETRIES}: {url}")

                    async with session.post(url, headers=headers, json=payload, timeout=self.timeout) as response:
                        if response.status == 200:
                            data = await response.json()
                            content = data["choices"][0]["message"]["content"]
                            logger.debug(f"GLM API 성공: {len(content)}자 응답")
                            return content

                        # 429 (Rate Limit) 처리
                        if response.status == 429:
                            error_text = await response.text()
                            logger.warning(f"GLM API Rate Limit (429): {error_text}")

                            if attempt < self.MAX_RETRIES - 1:
                                delay = await self._exponential_backoff(attempt)
                                logger.info(f"Rate limit - {delay:.1f}초 후 재시도...")
                                await asyncio.sleep(delay)
                                continue
                            else:
                                raise Exception(f"GLM API Rate Limit 초과 (재시도 {self.MAX_RETRIES}회 실패)")

                        # 기타 에러
                        error_text = await response.text()
                        logger.error(f"GLM API Error {response.status}: {error_text}")

                        # 5xx 서버 에러는 재시도
                        if 500 <= response.status < 600 and attempt < self.MAX_RETRIES - 1:
                            delay = await self._exponential_backoff(attempt)
                            logger.info(f"서버 에러 - {delay:.1f}초 후 재시도...")
                            await asyncio.sleep(delay)
                            continue

                        response.raise_for_status()

                except asyncio.TimeoutError:
                    logger.warning(f"GLM API Timeout ({self.timeout}s) - 시도 {attempt + 1}/{self.MAX_RETRIES}")
                    last_error = Exception(f"GLM API 요청 타임아웃 ({self.timeout}초 초과)")

                    if attempt < self.MAX_RETRIES - 1:
                        delay = await self._exponential_backoff(attempt)
                        logger.info(f"타임아웃 - {delay:.1f}초 후 재시도...")
                        await asyncio.sleep(delay)
                        continue

                except aiohttp.ClientError as e:
                    logger.warning(f"GLM API 네트워크 에러: {e} - 시도 {attempt + 1}/{self.MAX_RETRIES}")
                    last_error = e

                    if attempt < self.MAX_RETRIES - 1:
                        delay = await self._exponential_backoff(attempt)
                        logger.info(f"네트워크 에러 - {delay:.1f}초 후 재시도...")
                        await asyncio.sleep(delay)
                        continue

                except Exception as e:
                    logger.error(f"GLM API Request Failed: {e}")
                    last_error = e
                    break

        # 모든 재시도 실패
        raise last_error or Exception("GLM API 호출 실패")

    async def health_check(self) -> Dict[str, Any]:
        """API 상태 확인"""
        url = self._get_url()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 5
                    },
                    timeout=10
                ) as response:
                    return {
                        "status": "ok" if response.status in [200, 429] else "error",
                        "status_code": response.status,
                        "url": url
                    }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "url": url
            }

# 동기 호환성을 위한 래퍼 (필요 시 사용)
# client = AsyncLLMClient()
# result = asyncio.run(client.chat(...))
