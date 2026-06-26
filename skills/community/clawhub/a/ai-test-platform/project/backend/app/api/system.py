"""
系统管理 API 路由

提供AI模型配置、测试环境、操作日志和数据备份管理
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from app.core.database import get_db
from app.services.system_service import SystemManagementService
from app.schemas.system import (
    AIModelConfigCreate, AIModelConfigUpdate, AIModelConfigResponse,
    EnvironmentCreate, EnvironmentUpdate, EnvironmentResponse,
    OperationLogResponse, BackupCreate, BackupResponse, BackupRestoreRequest
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/system", tags=["系统管理"])


# ==================== AI模型配置 ====================

@router.post("/ai-model", summary="创建AI模型配置")
def create_ai_model_config(
    config_data: AIModelConfigCreate,
    db: Session = Depends(get_db)
):
    """创建AI模型配置（支持DeepSeek在线模型和本地模型）"""
    try:
        service = SystemManagementService(db)
        config = service.create_ai_model_config(config_data)
        return {"code": 200, "msg": "创建成功", "data": config.to_dict()}
    except Exception as e:
        logger.error(f"创建AI模型配置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai-model/list", summary="获取AI模型配置列表")
def list_ai_model_configs(
    model_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取AI模型配置列表"""
    service = SystemManagementService(db)
    configs = service.list_ai_model_configs(model_type=model_type)
    return {"code": 200, "msg": "查询成功", "data": [config.to_dict() for config in configs]}


@router.get("/ai-model/default", summary="获取默认AI模型配置")
def get_default_ai_model_config(db: Session = Depends(get_db)):
    """获取默认AI模型配置"""
    service = SystemManagementService(db)
    config = service.get_default_ai_model_config()
    if not config:
        raise HTTPException(status_code=404, detail="未设置默认配置")
    return {"code": 200, "msg": "查询成功", "data": config.to_dict()}


@router.get("/ai-model/{config_id}", summary="获取AI模型配置详情")
def get_ai_model_config(config_id: int, db: Session = Depends(get_db)):
    """获取AI模型配置详情"""
    service = SystemManagementService(db)
    config = service.get_ai_model_config(config_id)
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return {"code": 200, "msg": "查询成功", "data": config.to_dict()}


@router.put("/ai-model/{config_id}", summary="更新AI模型配置")
def update_ai_model_config(
    config_id: int,
    config_data: AIModelConfigUpdate,
    db: Session = Depends(get_db)
):
    """更新AI模型配置"""
    service = SystemManagementService(db)
    config = service.update_ai_model_config(config_id, config_data)
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return {"code": 200, "msg": "更新成功", "data": config.to_dict()}


@router.delete("/ai-model/{config_id}", summary="删除AI模型配置")
def delete_ai_model_config(config_id: int, db: Session = Depends(get_db)):
    """删除AI模型配置"""
    service = SystemManagementService(db)
    success = service.delete_ai_model_config(config_id)
    if not success:
        raise HTTPException(status_code=404, detail="配置不存在")
    return {"code": 200, "msg": "删除成功"}


@router.post("/ai-model/{config_id}/test", summary="测试AI模型配置")
def test_ai_model_config(config_id: int, db: Session = Depends(get_db)):
    """测试AI模型配置连接"""
    service = SystemManagementService(db)
    result = service.test_ai_model_config(config_id)
    return {"code": 200, "msg": "测试完成", "data": result}


# ==================== 测试环境管理 ====================

@router.post("/environment", summary="创建测试环境")
def create_environment(
    env_data: EnvironmentCreate,
    db: Session = Depends(get_db)
):
    """创建测试环境"""
    try:
        service = SystemManagementService(db)
        environment = service.create_environment(env_data)
        return {"code": 200, "msg": "创建成功", "data": environment.to_dict()}
    except Exception as e:
        logger.error(f"创建测试环境失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/environment/list", summary="获取测试环境列表")
def list_environments(
    env_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取测试环境列表"""
    service = SystemManagementService(db)
    environments = service.list_environments(env_type=env_type)
    return {"code": 200, "msg": "查询成功", "data": [env.to_dict() for env in environments]}


@router.get("/environment/default", summary="获取默认测试环境")
def get_default_environment(db: Session = Depends(get_db)):
    """获取默认测试环境"""
    service = SystemManagementService(db)
    environment = service.get_default_environment()
    if not environment:
        raise HTTPException(status_code=404, detail="未设置默认环境")
    return {"code": 200, "msg": "查询成功", "data": environment.to_dict()}


@router.get("/environment/{env_id}", summary="获取测试环境详情")
def get_environment(env_id: int, db: Session = Depends(get_db)):
    """获取测试环境详情"""
    service = SystemManagementService(db)
    environment = service.get_environment(env_id)
    if not environment:
        raise HTTPException(status_code=404, detail="环境不存在")
    return {"code": 200, "msg": "查询成功", "data": environment.to_dict()}


@router.put("/environment/{env_id}", summary="更新测试环境")
def update_environment(
    env_id: int,
    env_data: EnvironmentUpdate,
    db: Session = Depends(get_db)
):
    """更新测试环境"""
    service = SystemManagementService(db)
    environment = service.update_environment(env_id, env_data)
    if not environment:
        raise HTTPException(status_code=404, detail="环境不存在")
    return {"code": 200, "msg": "更新成功", "data": environment.to_dict()}


@router.delete("/environment/{env_id}", summary="删除测试环境")
def delete_environment(env_id: int, db: Session = Depends(get_db)):
    """删除测试环境"""
    service = SystemManagementService(db)
    success = service.delete_environment(env_id)
    if not success:
        raise HTTPException(status_code=404, detail="环境不存在")
    return {"code": 200, "msg": "删除成功"}


# ==================== 操作日志 ====================

@router.get("/log/list", summary="获取操作日志列表")
def list_operation_logs(
    user_id: Optional[str] = None,
    operation_type: Optional[str] = None,
    operation_module: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取操作日志列表"""
    service = SystemManagementService(db)
    logs = service.list_operation_logs(
        user_id=user_id,
        operation_type=operation_type,
        operation_module=operation_module,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    return {"code": 200, "msg": "查询成功", "data": [log.to_dict() for log in logs]}


# ==================== 数据备份 ====================

@router.post("/backup", summary="创建数据备份")
def create_backup(
    backup_data: BackupCreate,
    db: Session = Depends(get_db)
):
    """创建数据备份"""
    try:
        service = SystemManagementService(db)
        backup = service.create_backup(backup_data)
        return {"code": 200, "msg": "备份任务已创建", "data": backup.to_dict()}
    except Exception as e:
        logger.error(f"创建备份失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/backup/list", summary="获取备份列表")
def list_backups(
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取备份列表"""
    service = SystemManagementService(db)
    backups = service.list_backups(status=status, limit=limit)
    return {"code": 200, "msg": "查询成功", "data": [backup.to_dict() for backup in backups]}


@router.get("/backup/{backup_id}", summary="获取备份详情")
def get_backup(backup_id: int, db: Session = Depends(get_db)):
    """获取备份详情"""
    service = SystemManagementService(db)
    backup = service.get_backup(backup_id)
    if not backup:
        raise HTTPException(status_code=404, detail="备份不存在")
    return {"code": 200, "msg": "查询成功", "data": backup.to_dict()}


@router.delete("/backup/{backup_id}", summary="删除备份")
def delete_backup(backup_id: int, db: Session = Depends(get_db)):
    """删除备份"""
    service = SystemManagementService(db)
    success = service.delete_backup(backup_id)
    if not success:
        raise HTTPException(status_code=404, detail="备份不存在")
    return {"code": 200, "msg": "删除成功"}


@router.post("/backup/restore", summary="恢复备份")
def restore_backup(
    restore_data: BackupRestoreRequest,
    db: Session = Depends(get_db)
):
    """恢复备份"""
    service = SystemManagementService(db)
    result = service.restore_backup(restore_data)
    return {"code": 200, "msg": "恢复完成", "data": result}
