"""
YesApi Skill 处理器
为 OpenCraw 提供 YesApi 功能的统一接口
"""

import json
import os
from typing import Dict, Any, List, Optional
from yesapi_client import YesApiClient, YesApiConfig, YesApiError


class YesApiSkillHandler:
    """YesApi Skill 处理器"""
    
    def __init__(self):
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化客户端"""
        try:
            config = YesApiConfig(
                app_key=os.getenv("YESAPI_APP_KEY", ""),
                domain=os.getenv("YESAPI_DOMAIN", "https://api.yesapi.net"),
                sign=os.getenv("YESAPI_SIGN", "")
            )
            self.client = YesApiClient(config)
        except Exception as e:
            print(f"初始化 YesApi 客户端失败: {e}")
            self.client = None
    
    def _check_client(self) -> bool:
        """检查客户端是否可用"""
        if self.client is None:
            print("YesApi 客户端未初始化，请检查环境变量配置")
            return False
        return True
    
    def handle_models_request(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理表单模型相关请求"""
        if not self._check_client():
            return {"error": "客户端未初始化"}
        
        try:
            if action == "list":
                return self.client.get_models()
            elif action == "create":
                model_name = params.get("model_name")
                model_desc = params.get("model_desc")
                if not model_name or not model_desc:
                    return {"error": "缺少 model_name 或 model_desc 参数"}
                return self.client.create_model(model_name, model_desc)
            elif action == "add_field":
                model_name = params.get("model_name")
                field_name = params.get("field_name")
                field_desc = params.get("field_desc")
                field_type = params.get("field_type")
                field_length = params.get("field_length")
                if not all([model_name, field_name, field_desc, field_type, field_length]):
                    return {"error": "缺少添加字段所需的参数"}
                return self.client.add_model_new_field(model_name, field_name, field_desc, field_type, field_length)
            elif action == "update":
                # 更新功能暂未实现
                return {"error": "更新模型功能暂未实现"}
            elif action == "delete":
                model_name = params.get("model_name")
                if not model_name:
                    return {"error": "缺少 model_name 参数"}
                is_drop_table = params.get("is_drop_table", False)
                return self.client.delete_model(model_name, is_drop_table)
            else:
                return {"error": f"不支持的操作: {action}"}
        except YesApiError as e:
            return {"error": str(e), "ret": e.ret}
        except Exception as e:
            return {"error": f"未知错误: {str(e)}"}
    
    def handle_data_request(self, action: str, model_name: str, 
                           params: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理表单数据相关请求"""
        if not self._check_client():
            return {"error": "客户端未初始化"}
        
        if not model_name:
            return {"error": "缺少表名(model_name)"}
        
        try:
            if action == "query":
                return self.client.query_data(model_name, **(params or {}))
            elif action == "insert":
                return self.client.insert_data(model_name, params or {})
            elif action == "update":
                record_id = params.pop("id", None)
                if not record_id:
                    return {"error": "缺少记录ID"}
                return self.client.update_data(model_name, record_id, params)
            elif action == "delete":
                record_id = params.get("id")
                if not record_id:
                    return {"error": "缺少记录ID"}
                return self.client.delete_data(model_name, record_id)
            elif action == "batch_update":
                where = params.get("where", {})
                data = params.get("data", {})
                if not where or not data:
                    return {"error": "缺少 where 或 data 参数"}
                return self.client.batch_update(model_name, where, data)
            elif action == "batch_delete":
                where = params.get("where", {})
                if not where:
                    return {"error": "缺少 where 参数"}
                return self.client.batch_delete(model_name, where)
            else:
                return {"error": f"不支持的操作: {action}"}
        except YesApiError as e:
            return {"error": str(e), "ret": e.ret}
        except Exception as e:
            return {"error": f"未知错误: {str(e)}"}
    
    def parse_natural_request(self, request: str) -> Dict[str, Any]:
        """解析自然语言请求"""
        request = request.strip().lower()
        
        # 表单模型相关
        if "模型" in request or "表单" in request:
            if "列表" in request or "获取" in request:
                return {"type": "models", "action": "list"}
            elif "创建" in request or "新建" in request:
                return {"type": "models", "action": "create"}
            elif "添加字段" in request or "新增字段" in request:
                return {"type": "models", "action": "add_field"}
            elif "更新" in request or "修改" in request:
                return {"type": "models", "action": "update"}
            elif "删除" in request:
                return {"type": "models", "action": "delete"}
        
        # 数据操作相关
        if "数据" in request or "记录" in request:
            if "查询" in request or "获取" in request or "搜索" in request:
                return {"type": "data", "action": "query"}
            elif "添加" in request or "插入" in request or "新增" in request:
                return {"type": "data", "action": "insert"}
            elif "更新" in request or "修改" in request:
                return {"type": "data", "action": "update"}
            elif "删除" in request:
                return {"type": "data", "action": "delete"}
        
        return {"type": "unknown", "action": "unknown"}


# 全局处理器实例
handler = YesApiSkillHandler()


def process_request(request: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """处理请求的主入口函数"""
    if params is None:
        params = {}
    
    # 解析请求类型
    parsed = handler.parse_natural_request(request)
    
    if parsed["type"] == "models":
        return handler.handle_models_request(parsed["action"], params)
    elif parsed["type"] == "data":
        model_name = params.pop("model_name", None)
        return handler.handle_data_request(parsed["action"], model_name, params)
    else:
        return {"error": "无法识别的请求类型"}


# 便捷函数
def get_models():
    """获取模型列表"""
    return handler.handle_models_request("list")


def query_table_data(model_name: str, **kwargs):
    """查询表数据"""
    return handler.handle_data_request("query", model_name, kwargs)


def insert_table_data(model_name: str, data: Dict[str, Any]):
    """插入表数据"""
    return handler.handle_data_request("insert", model_name, data)


if __name__ == "__main__":
    # 测试代码
    print("测试 YesApi Skill Handler...")
    
    # 测试自然语言解析
    test_requests = [
        "获取我的表单模型列表",
        "查询用户表的数据",
        "向订单表添加新数据",
        "更新产品表中ID为123的记录"
    ]
    
    for req in test_requests:
        parsed = handler.parse_natural_request(req)
        print(f"请求: {req}")
        print(f"解析结果: {parsed}")
        print("-" * 50)
