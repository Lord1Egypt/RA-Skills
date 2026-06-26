"""
FastAPI 路由模板

职责：只处理HTTP请求/响应，不包含业务逻辑
文件名：{module_name}_router.py
位置：backend/api/routers/
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

# 导入服务层（业务逻辑在服务层）
from backend.services.{module_name}_service import {ModuleName}Service
from backend.schemas.{module_name} import (
    {ModuleName}Create,
    {ModuleName}Update,
    {ModuleName}Response,
    {ModuleName}ListResponse
)

router = APIRouter(prefix="/api/{module_name_plural}", tags=["{module_name_display}管理"])

# 初始化服务
{module_name}_service = {ModuleName}Service()

@router.get("/", response_model={ModuleName}ListResponse)
async def list_{module_name_plural}(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
):
    """
    获取{module_name_display}列表
    
    参数:
        skip: 跳过数量
        limit: 返回数量
        search: 搜索关键词
    """
    try:
        result = await {module_name}_service.get_list(skip=skip, limit=limit, search=search)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取{module_name_display}列表失败: {str(e)}"
        )

@router.get("/{id}", response_model={ModuleName}Response)
async def get_{module_name}_by_id(id: int):
    """
    根据ID获取{module_name_display}详情
    """
    try:
        result = await {module_name}_service.get_by_id(id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID为{id}的{module_name_display}不存在"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取{module_name_display}详情失败: {str(e)}"
        )

@router.post("/", response_model={ModuleName}Response, status_code=status.HTTP_201_CREATED)
async def create_{module_name}(data: {ModuleName}Create):
    """
    创建{module_name_display}
    """
    try:
        # 验证数据
        # 业务逻辑在服务层处理
        result = await {module_name}_service.create(data)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建{module_name_display}失败: {str(e)}"
        )

@router.put("/{id}", response_model={ModuleName}Response)
async def update_{module_name}(id: int, data: {ModuleName}Update):
    """
    更新{module_name_display}
    """
    try:
        result = await {module_name}_service.update(id, data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID为{id}的{module_name_display}不存在"
            )
        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新{module_name_display}失败: {str(e)}"
        )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{module_name}(id: int):
    """
    删除{module_name_display}
    """
    try:
        success = await {module_name}_service.delete(id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID为{id}的{module_name_display}不存在"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除{module_name_display}失败: {str(e)}"
        )

# 注意：路由文件不应包含以下内容：
# 1. 数据库操作（应在服务层或数据访问层）
# 2. 复杂业务逻辑（应在服务层）
# 3. 工具函数（应在utils目录）
# 4. 数据验证（应在schemas层）