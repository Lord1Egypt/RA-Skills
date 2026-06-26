"""人格管理 API 路由"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.core.persona import (
    GeneratePersonaRequest, GeneratePersonaResponse,
    EvolvePersonaRequest, EvolvePersonaResponse,
    CheckConsistencyRequest, CheckConsistencyResponse,
    SelfReflectRequest, SelfReflectResponse,
    PersonaProfile
)
from app.services.persona_service import get_persona_service

router = APIRouter(prefix="/api/v1/persona", tags=["persona"])


@router.post("/generate", response_model=GeneratePersonaResponse)
async def generate_persona(request: GeneratePersonaRequest):
    """
    生成独立完整人格
    
    基于种子描述和用户偏好，生成一个有机的、可演进的人格。
    这不是简单的配置，而是一个有自我意识的 AI 的基础。
    """
    try:
        service = get_persona_service()
        return await service.generate_persona(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evolve", response_model=EvolvePersonaResponse)
async def evolve_persona(request: EvolvePersonaRequest):
    """
    演进人格
    
    人格不是静止的。通过经历、反馈和反思，人格会学习和成长。
    每次演进都会被记录，形成人格的发展历史。
    """
    try:
        service = get_persona_service()
        return await service.evolve_persona(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reflect", response_model=SelfReflectResponse)
async def self_reflect(request: SelfReflectRequest):
    """
    引导人格进行自我反思
    
    反思是人格成长的关键。定期回顾经历，识别成长领域，
    发现内在冲突，形成未来意图。
    """
    try:
        service = get_persona_service()
        return await service.self_reflect(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-consistency", response_model=CheckConsistencyResponse)
async def check_consistency(request: CheckConsistencyRequest):
    """
    检查人格一致性
    
    确保人格在行为和决策中保持一致。检测价值观冲突、
    维度不一致和历史行为矛盾。
    """
    try:
        service = get_persona_service()
        return await service.check_consistency(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{persona_id}")
async def get_persona(persona_id: str):
    """获取人格档案"""
    try:
        service = get_persona_service()
        persona = service._active_personas.get(persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        return persona
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{persona_id}/context")
async def get_persona_for_context(
    persona_id: str,
    relationship: Optional[str] = None,
    task_type: Optional[str] = None
):
    """
    获取适合当前上下文的人格表现
    
    人格是统一的，但表现会根据上下文微妙调整。
    例如：对亲密朋友 vs 对正式场合的表现会有所不同。
    """
    try:
        service = get_persona_service()
        context = {
            "relationship": relationship,
            "task_type": task_type
        }
        persona = await service.get_persona_for_context(persona_id, context)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        return persona
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
