"""DiscoverySource 기본 클래스"""

from abc import ABC, abstractmethod
from typing import List, Dict
from builder.models import ProjectIdea


class DiscoverySource(ABC):
    """아이디어 발굴 소스 기본 클래스"""

    def __init__(self, config=None):
        self.config = config
        self.enabled = True
        if config and hasattr(config, 'enabled'):
            self.enabled = config.enabled

    @abstractmethod
    def discover(self) -> List[Dict]:
        """아이디어 발굴

        Returns:
            ProjectIdea.to_dict() 형식의 딕셔너리 리스트
        """
        pass

    def to_ideas(self, raw_data: List[Dict]) -> List[ProjectIdea]:
        """원본 데이터를 ProjectIdea로 변환"""
        return [ProjectIdea.from_dict(item) for item in raw_data]
