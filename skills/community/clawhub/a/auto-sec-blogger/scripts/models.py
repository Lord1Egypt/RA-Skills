"""
Data Models
Pydantic을 사용한 데이터 검증 및 파싱 모델
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class EvaluationItem(BaseModel):
    id: int = Field(..., description="기사 ID")
    score: int = Field(..., ge=1, le=10, description="평가 점수 (1-10)")
    reason: str = Field(..., description="선별 이유")

class EvaluationResponse(BaseModel):
    evaluations: List[EvaluationItem]

class BlogPost(BaseModel):
    title: str = Field(..., description="블로그 글 제목")
    summary: str = Field(..., description="핵심 요약")
    content: str = Field(..., description="마크다운 본문")
    tags: List[str] = Field(default_factory=list, description="태그 목록")
    category: str = Field(..., description="카테고리")
