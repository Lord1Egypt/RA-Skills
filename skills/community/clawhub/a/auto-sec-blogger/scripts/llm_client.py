"""
LLM Client Module
OpenAI, GLM 등 LLM API와의 통신을 담당합니다.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, List, Optional, Any
from modules.intelligence.config import GLM_API_KEY, GLM_BASE_URL, GLM_MODEL
from modules.intelligence.utils import setup_logger

logger = setup_logger(__name__, "llm_client.log")

class LLMClient:
    """기본 LLM 클라이언트 추상 클래스 (Interface)"""
    def chat(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError

class GLMClient(LLMClient):
    """ZhipuAI GLM API 클라이언트"""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or GLM_API_KEY
        self.base_url = base_url or GLM_BASE_URL
        self.model = model or GLM_MODEL
        self.timeout = 300  # 5분

        if not self.api_key:
            logger.warning("GLM_API_KEY is not set.")

        # Requests Session with Retry
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """GLM API 호출"""
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

        url = self.base_url.rstrip('/') + "/chat/completions"

        try:
            response = self.session.post(
                url, headers=headers, json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            logger.error(f"GLM API Timeout ({self.timeout}s)")
            raise Exception(f"GLM API 요청 타임아웃 ({self.timeout}초 초과)")
        except requests.exceptions.RequestException as e:
            logger.error(f"GLM API Request Failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            raise Exception(f"GLM API 요청 실패: {str(e)}")

# 전역 인스턴스 (필요 시 사용)
# default_client = GLMClient()
