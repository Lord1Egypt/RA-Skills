"""
Prompt Manager
YAML 파일에서 프롬프트를 로드하고 관리합니다.
"""

import yaml
from pathlib import Path
from typing import Any, Dict

# 프로젝트 내의 prompts.yaml 경로 설정
PROMPTS_PATH = Path(__file__).resolve().parent / "prompts.yaml"

class PromptManager:
    _prompts: Dict[str, Any] = {}

    @classmethod
    def load(cls):
        """YAML 파일 로드"""
        if not PROMPTS_PATH.exists():
            raise FileNotFoundError(f"Prompts file not found at {PROMPTS_PATH}")
        
        with open(PROMPTS_PATH, 'r', encoding='utf-8') as f:
            cls._prompts = yaml.safe_load(f)

    @classmethod
    def get(cls, key: str, **kwargs) -> str:
        """
        키(예: 'writer.system')에 해당하는 프롬프트를 가져와 포맷팅

        Args:
            key: 점(.)으로 구분된 키 (예: 'writer.base_system')
            **kwargs: 포맷팅에 사용할 변수들

        Returns:
            포맷팅된 프롬프트 문자열
        """
        if not cls._prompts:
            cls.load()

        keys = key.split('.')
        value = cls._prompts
        
        try:
            for k in keys:
                value = value[k]
        except (KeyError, TypeError):
            raise KeyError(f"Prompt key '{key}' not found.")

        if isinstance(value, str):
            return value.format(**kwargs)
        return value

    @classmethod
    def get_raw(cls, key: str) -> Any:
        """포맷팅 없이 원본 값(dict 등) 반환"""
        if not cls._prompts:
            cls.load()

        keys = key.split('.')
        value = cls._prompts
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return None

# 초기화 시 로드
PromptManager.load()
