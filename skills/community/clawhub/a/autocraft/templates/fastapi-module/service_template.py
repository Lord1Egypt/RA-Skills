"""
FastAPI 服务层模板

职责：处理业务逻辑，协调数据访问和业务规则
文件名：{module_name}_service.py
位置：backend/services/
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

# 导入数据访问层
from backend.repositories.{module_name}_repository import {ModuleName}Repository
# 导入数据模型
from backend.models.{module_name} import {ModuleName}
# 导入Pydantic模型
from backend.schemas.{module_name} import (
    {ModuleName}Create,
    {ModuleName}Update,
    {ModuleName}Response,
    {ModuleName}ListResponse
)

class {ModuleName}Service:
    """{module_name_display}服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.repository = {ModuleName}Repository()
    
    async def get_list(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> {ModuleName}ListResponse:
        """
        获取{module_name_display}列表
        
        参数:
            skip: 跳过数量
            limit: 返回数量
            search: 搜索关键词
            filters: 过滤条件
            
        返回:
            {ModuleName}ListResponse: 列表响应
        """
        try:
            # 调用数据访问层获取数据
            items, total = await self.repository.get_list(
                skip=skip,
                limit=limit,
                search=search,
                filters=filters
            )
            
            # 转换为响应模型
            items_response = []
            for item in items:
                items_response.append(
                    {ModuleName}Response.from_orm(item)
                )
            
            return {ModuleName}ListResponse(
                items=items_response,
                total=total,
                skip=skip,
                limit=limit
            )
        except Exception as e:
            # 记录日志
            self._log_error(f"获取{module_name_display}列表失败: {str(e)}")
            raise
    
    async def get_by_id(self, id: int) -> Optional[{ModuleName}Response]:
        """
        根据ID获取{module_name_display}详情
        
        参数:
            id: {module_name_display}ID
            
        返回:
            Optional[{ModuleName}Response]: {module_name_display}详情或None
        """
        try:
            item = await self.repository.get_by_id(id)
            if not item:
                return None
            
            return {ModuleName}Response.from_orm(item)
        except Exception as e:
            self._log_error(f"获取{module_name_display}详情失败 (ID={id}): {str(e)}")
            raise
    
    async def create(self, data: {ModuleName}Create) -> {ModuleName}Response:
        """
        创建{module_name_display}
        
        参数:
            data: 创建数据
            
        返回:
            {ModuleName}Response: 创建的{module_name_display}
        """
        try:
            # 业务逻辑验证
            await self._validate_create_data(data)
            
            # 调用数据访问层创建
            item = await self.repository.create(data)
            
            # 返回响应
            return {ModuleName}Response.from_orm(item)
        except ValueError as e:
            # 业务逻辑验证失败
            raise
        except Exception as e:
            self._log_error(f"创建{module_name_display}失败: {str(e)}")
            raise
    
    async def update(self, id: int, data: {ModuleName}Update) -> Optional[{ModuleName}Response]:
        """
        更新{module_name_display}
        
        参数:
            id: {module_name_display}ID
            data: 更新数据
            
        返回:
            Optional[{ModuleName}Response]: 更新后的{module_name_display}或None
        """
        try:
            # 检查{module_name_display}是否存在
            existing = await self.repository.get_by_id(id)
            if not existing:
                return None
            
            # 业务逻辑验证
            await self._validate_update_data(id, data)
            
            # 调用数据访问层更新
            updated_item = await self.repository.update(id, data)
            
            return {ModuleName}Response.from_orm(updated_item)
        except ValueError as e:
            # 业务逻辑验证失败
            raise
        except Exception as e:
            self._log_error(f"更新{module_name_display}失败 (ID={id}): {str(e)}")
            raise
    
    async def delete(self, id: int) -> bool:
        """
        删除{module_name_display}
        
        参数:
            id: {module_name_display}ID
            
        返回:
            bool: 是否删除成功
        """
        try:
            # 检查{module_name_display}是否存在
            existing = await self.repository.get_by_id(id)
            if not existing:
                return False
            
            # 业务逻辑验证（如检查关联关系）
            await self._validate_delete(id)
            
            # 调用数据访问层删除
            success = await self.repository.delete(id)
            
            return success
        except ValueError as e:
            # 业务逻辑验证失败
            raise
        except Exception as e:
            self._log_error(f"删除{module_name_display}失败 (ID={id}): {str(e)}")
            raise
    
    async def _validate_create_data(self, data: {ModuleName}Create):
        """
        验证创建数据
        
        参数:
            data: 创建数据
            
        抛出:
            ValueError: 验证失败
        """
        # 示例验证逻辑
        if not data.name or len(data.name.strip()) == 0:
            raise ValueError("{module_name_display}名称不能为空")
        
        if len(data.name) > 100:
            raise ValueError("{module_name_display}名称不能超过100个字符")
        
        # 检查唯一性
        existing = await self.repository.get_by_name(data.name)
        if existing:
            raise ValueError(f"名称 '{data.name}' 已存在")
    
    async def _validate_update_data(self, id: int, data: {ModuleName}Update):
        """
        验证更新数据
        
        参数:
            id: {module_name_display}ID
            data: 更新数据
            
        抛出:
            ValueError: 验证失败
        """
        if data.name:
            if len(data.name) > 100:
                raise ValueError("{module_name_display}名称不能超过100个字符")
            
            # 检查名称唯一性（排除自己）
            existing = await self.repository.get_by_name(data.name)
            if existing and existing.id != id:
                raise ValueError(f"名称 '{data.name}' 已存在")
    
    async def _validate_delete(self, id: int):
        """
        验证删除操作
        
        参数:
            id: {module_name_display}ID
            
        抛出:
            ValueError: 验证失败
        """
        # 示例：检查是否有关联数据
        has_relations = await self.repository.has_relations(id)
        if has_relations:
            raise ValueError("该{module_name_display}有关联数据，无法删除")
    
    def _log_error(self, message: str):
        """记录错误日志"""
        # 实际项目中应使用logging模块
        print(f"[ERROR] {datetime.now()}: {message}")
    
    def _log_info(self, message: str):
        """记录信息日志"""
        # 实际项目中应使用logging模块
        print(f"[INFO] {datetime.now()}: {message}")

# 注意：服务层应包含以下内容：
# 1. 业务逻辑处理
# 2. 数据验证
# 3. 事务管理
# 4. 错误处理
# 5. 日志记录

# 不应包含：
# 1. HTTP请求/响应处理（应在路由层）
# 2. 数据库原始SQL操作（应在数据访问层）
# 3. 工具函数（应在utils目录）