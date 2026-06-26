"""
FastAPI 测试模板

职责：测试路由和服务层功能
文件名：test_{module_name}.py
位置：tests/backend/api/ 或 tests/backend/services/
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from typing import List, Dict, Any

# 导入应用和模型
from backend.main import app
from backend.models.{module_name} import {ModuleName}
from backend.schemas.{module_name} import {ModuleName}Create, {ModuleName}Update

# 测试客户端
client = TestClient(app)

class Test{ModuleName}Router:
    """{module_name_display}路由测试类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.base_url = "/api/{module_name_plural}"
        self.test_data = {{
            "name": "测试{module_name_display}",
            "description": "这是一个测试{module_name_display}",
            "status": "active"
        }}
    
    def test_list_{module_name_plural}_success(self):
        """测试获取{module_name_display}列表成功"""
        # Mock服务层返回
        mock_response = {{
            "items": [
                {{"id": 1, "name": "测试1", "created_at": "2024-01-01T00:00:00"}},
                {{"id": 2, "name": "测试2", "created_at": "2024-01-01T00:00:00"}}
            ],
            "total": 2,
            "skip": 0,
            "limit": 100
        }}
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.get_list") as mock_get_list:
            mock_get_list.return_value = mock_response
            
            response = client.get(f"{{self.base_url}}/")
            
            assert response.status_code == 200
            data = response.json()
            assert "items" in data
            assert "total" in data
            assert len(data["items"]) == 2
            assert data["total"] == 2
    
    def test_list_{module_name_plural}_with_pagination(self):
        """测试分页获取{module_name_display}列表"""
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.get_list") as mock_get_list:
            mock_get_list.return_value = {{
                "items": [],
                "total": 0,
                "skip": 10,
                "limit": 20
            }}
            
            response = client.get(f"{{self.base_url}}/?skip=10&limit=20")
            
            assert response.status_code == 200
            mock_get_list.assert_called_once_with(skip=10, limit=20, search=None)
    
    def test_get_{module_name}_by_id_success(self):
        """测试根据ID获取{module_name_display}成功"""
        test_id = 1
        mock_response = {{
            "id": test_id,
            "name": "测试{module_name_display}",
            "created_at": "2024-01-01T00:00:00"
        }}
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.get_by_id") as mock_get_by_id:
            mock_get_by_id.return_value = mock_response
            
            response = client.get(f"{{self.base_url}}/{{test_id}}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == test_id
            assert data["name"] == "测试{module_name_display}"
    
    def test_get_{module_name}_by_id_not_found(self):
        """测试获取不存在的{module_name_display}"""
        test_id = 999
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.get_by_id") as mock_get_by_id:
            mock_get_by_id.return_value = None
            
            response = client.get(f"{{self.base_url}}/{{test_id}}")
            
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "不存在" in data["detail"]
    
    def test_create_{module_name}_success(self):
        """测试创建{module_name_display}成功"""
        mock_response = {{
            "id": 1,
            "name": "测试{module_name_display}",
            "created_at": "2024-01-01T00:00:00"
        }}
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.create") as mock_create:
            mock_create.return_value = mock_response
            
            response = client.post(f"{{self.base_url}}/", json=self.test_data)
            
            assert response.status_code == 201
            data = response.json()
            assert data["id"] == 1
            assert data["name"] == "测试{module_name_display}"
    
    def test_create_{module_name}_validation_error(self):
        """测试创建{module_name_display}验证失败"""
        invalid_data = {{"name": ""}}  # 空名称
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.create") as mock_create:
            mock_create.side_effect = ValueError("名称不能为空")
            
            response = client.post(f"{{self.base_url}}/", json=invalid_data)
            
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
            assert "名称不能为空" in data["detail"]
    
    def test_update_{module_name}_success(self):
        """测试更新{module_name_display}成功"""
        test_id = 1
        update_data = {{"name": "更新后的名称"}}
        mock_response = {{
            "id": test_id,
            "name": "更新后的名称",
            "created_at": "2024-01-01T00:00:00"
        }}
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.update") as mock_update:
            mock_update.return_value = mock_response
            
            response = client.put(f"{{self.base_url}}/{{test_id}}", json=update_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == test_id
            assert data["name"] == "更新后的名称"
    
    def test_update_{module_name}_not_found(self):
        """测试更新不存在的{module_name_display}"""
        test_id = 999
        update_data = {{"name": "新名称"}}
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.update") as mock_update:
            mock_update.return_value = None
            
            response = client.put(f"{{self.base_url}}/{{test_id}}", json=update_data)
            
            assert response.status_code == 404
    
    def test_delete_{module_name}_success(self):
        """测试删除{module_name_display}成功"""
        test_id = 1
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.delete") as mock_delete:
            mock_delete.return_value = True
            
            response = client.delete(f"{{self.base_url}}/{{test_id}}")
            
            assert response.status_code == 204
    
    def test_delete_{module_name}_not_found(self):
        """测试删除不存在的{module_name_display}"""
        test_id = 999
        
        with patch("backend.api.routers.{module_name}_router.{module_name}_service.delete") as mock_delete:
            mock_delete.return_value = False
            
            response = client.delete(f"{{self.base_url}}/{{test_id}}")
            
            assert response.status_code == 404

class Test{ModuleName}Service:
    """{module_name_display}服务层测试类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        from backend.services.{module_name}_service import {ModuleName}Service
        self.service = {ModuleName}Service()
        
        # Mock数据访问层
        self.mock_repository = AsyncMock()
        self.service.repository = self.mock_repository
    
    @pytest.mark.asyncio
    async def test_get_list_success(self):
        """测试获取列表成功"""
        # 准备Mock数据
        mock_items = [
            MagicMock(id=1, name="测试1"),
            MagicMock(id=2, name="测试2")
        ]
        self.mock_repository.get_list.return_value = (mock_items, 2)
        
        # 执行测试
        result = await self.service.get_list(skip=0, limit=100)
        
        # 验证结果
        assert result.total == 2
        assert len(result.items) == 2
        assert result.items[0].id == 1
        assert result.items[1].id == 2
        self.mock_repository.get_list.assert_called_once_with(
            skip=0, limit=100, search=None, filters=None
        )
    
    @pytest.mark.asyncio
    async def test_get_by_id_success(self):
        """测试根据ID获取成功"""
        # 准备Mock数据
        mock_item = MagicMock(id=1, name="测试{module_name_display}")
        self.mock_repository.get_by_id.return_value = mock_item
        
        # 执行测试
        result = await self.service.get_by_id(1)
        
        # 验证结果
        assert result is not None
        assert result.id == 1
        self.mock_repository.get_by_id.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self):
        """测试获取不存在的{module_name_display}"""
        self.mock_repository.get_by_id.return_value = None
        
        result = await self.service.get_by_id(999)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_create_success(self):
        """测试创建成功"""
        # 准备Mock数据
        create_data = {ModuleName}Create(name="测试{module_name_display}")
        mock_item = MagicMock(id=1, name="测试{module_name_display}")
        self.mock_repository.create.return_value = mock_item
        
        # 执行测试
        result = await self.service.create(create_data)
        
        # 验证结果
        assert result is not None
        assert result.id == 1
        self.mock_repository.create.assert_called_once_with(create_data)
    
    @pytest.mark.asyncio
    async def test_create_validation_error(self):
        """测试创建验证失败"""
        create_data = {ModuleName}Create(name="")  # 空名称
        
        # 执行测试，期望抛出异常
        with pytest.raises(ValueError) as exc_info:
            await self.service.create(create_data)
        
        assert "名称" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_update_success(self):
        """测试更新成功"""
        update_data = {ModuleName}Update(name="更新后的名称")
        mock_item = MagicMock(id=1, name="更新后的名称")
        self.mock_repository.update.return_value = mock_item
        self.mock_repository.get_by_id.return_value = MagicMock(id=1)  # 模拟存在
        
        result = await self.service.update(1, update_data)
        
        assert result is not None
        assert result.name == "更新后的名称"
    
    @pytest.mark.asyncio
    async def test_update_not_found(self):
        """测试更新不存在的{module_name_display}"""
        update_data = {ModuleName}Update(name="新名称")
        self.mock_repository.get_by_id.return_value = None
        
        result = await self.service.update(999, update_data)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_delete_success(self):
        """测试删除成功"""
        self.mock_repository.delete.return_value = True
        self.mock_repository.get_by_id.return_value = MagicMock(id=1)  # 模拟存在
        
        result = await self.service.delete(1)
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_delete_not_found(self):
        """测试删除不存在的{module_name_display}"""
        self.mock_repository.get_by_id.return_value = None
        
        result = await self.service.delete(999)
        
        assert result is False

# 测试覆盖率要求：
# 1. 路由层：所有API端点
# 2. 服务层：所有公共方法
# 3. 边界条件：正常/异常/边界值
# 4. 错误处理：各种错误场景
# 5. 集成测试：端到端流程