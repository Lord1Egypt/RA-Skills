"""
YesApi 果创云低代码平台 Python 客户端
支持表单结构管理和数据操作
"""

import os
import hashlib
import time
import json
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


@dataclass
class YesApiConfig:
    """YesApi 配置类"""
    app_key: str
    domain: str = "https://api.yesapi.net"
    sign: str = ""
    
    def __post_init__(self):
        if not self.app_key:
            raise ValueError("app_key is required")
        if not self.domain:
            raise ValueError("domain is required")


class YesApiError(Exception):
    """YesApi 错误类"""
    def __init__(self, message: str, ret: str = None, data: Dict = None):
        super().__init__(message)
        self.ret = ret
        self.data = data


class YesApiClient:
    """YesApi 客户端类"""
    
    def __init__(self, config: YesApiConfig = None):
        if config is None:
            config = YesApiConfig(
                app_key=os.getenv("YESAPI_APP_KEY", ""),
                domain=os.getenv("YESAPI_DOMAIN", "https://api.yesapi.net"),
                sign=os.getenv("YESAPI_SIGN", "")
            )
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'YesApi-Skill/1.0.0',
            'Content-Type': 'application/json'
        })
    
    def _make_request(self, service: str, params: Dict[str, Any] = None, 
                     method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
        """发起API请求"""
        if params is None:
            params = {}
        
        # 添加必要参数
        params['app_key'] = self.config.app_key
        params['_timestamp'] = int(time.time())
        
        # 静态签名
        sign = self.config.sign
        if sign:
            params['sign'] = sign
        
        url = f"{self.config.domain}/?s={service}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=30)
            else:
                response = self.session.post(url, params=params, json=data, timeout=30)
            
            response.raise_for_status()
            result = response.json()
            
            # 检查API返回状态
            if result.get('ret') != 200:
                raise YesApiError(
                    message=result.get('msg', 'Unknown error'),
                    ret=result.get('ret'),
                    data=result
                )
            
            return result.get('data', {})
            
        except requests.exceptions.RequestException as e:
            raise YesApiError(f"Network error: {str(e)}")
        except ValueError as e:
            raise YesApiError(f"Invalid JSON response: {str(e)}")
    
    # 表单结构管理接口
    def get_models(self) -> Dict[str, Any]:
        """获取表单模型列表"""
        return self._make_request("App.Platform_MyModels.GetMyModelsList")
    
    def create_model(self, model_name: str, model_desc: str) -> Dict[str, Any]:
        """创建表单模型
        Args:
            model_name: 表单名称，待创建的表单名称(英文)，用于数据库建表，由字母开头和数字的组成（如：demo），50个字符以内。
            model_desc: 表单描述，用于页面展示，请起一个简短的中文名称（如：示例），100个字符以内。
        """
        return self._make_request(
            "App.Platform_MyModels.CreateNewModel",
            method="POST",
            data={"model_name": model_name, "model_desc": model_desc}
        )
    
    def add_model_new_field(self, model_name: str, field_name: str, field_desc: str, field_type: str, field_length: int) -> Dict[str, Any]:
        """添加表单新字段
        Args:
            model_name: 表单名称(英文)
            field_name: 字段名称(英文)，请填写有效的数据库表字段名称，如：demo
            field_desc: 字段描述（中文），将会显示在各大菜单，如：示例数据
            field_type: 字段类型，可选字段类型如下：tinyint/smallint/mediumint/int/bigint/float/double/char/varchar/tinytext/text/mediumtext/longtext/date/time/year/datetime/timestamp。
            field_length: 字段类型长度，重要提示：varchar时长度必填！
        """
        params = {
            'model_name': model_name,
            'field_name': field_name,
            'field_desc': field_desc,
            'field_type': field_type,
            'field_length': field_length
        }
        return self._make_request(
            "App.Platform_MyModels.AddNewField",
            params=params,
            method="POST"
        )
    
    def delete_model(self, model_name: str, is_drop_table: bool = False) -> Dict[str, Any]:
        """删除表单模型
        Args:
            model_name: 表单名称
            is_drop_table: 是否删除数据库表，默认False
        """
        params = {'model_name': model_name, 'is_drop_table': is_drop_table}
        return self._make_request("App.Platform_MyModels.DangerClear", params=params)
    
    # 表单数据操作接口
    def query_data(self, model_name: str, **kwargs) -> Dict[str, Any]:
        """查询表单数据
        
        Args:
            model_name: 表单名称
            **kwargs: 其他查询参数
                - page: 页码 (默认1)
                - perpage: 每页数量 (默认20)
                - where: 查询条件，SQL语句的WHERE查询条件，JSON格式，格式为：[第一组条件, 第二组条件, ……]。每一组的条件格式为：["字段名", "比较符", "比较值"]。
                - order: 排序字段，SQL语句的ORDER部分，JSON格式。具体格式为：[第一组排序，第二组排序，……]，可以单个或组合排序。每一组排序格式为："字段名 + 空格 + ASC|DESC"。
        """
        params = {'model_name': model_name}
        params.update(kwargs)
        return self._make_request("App.Table.FreeQuery", params=params)
    
    def insert_data(self, model_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """插入表单数据
        
        Args:
            model_name: 表单名称
            data: 要插入的数据，字典格式，创建时的初始化数据，需要JSON编码后传递。格式：data={"字段名1":"字段值1","字段名2":"字段值2"...}。
        """
        params = {'model_name': model_name}
        return self._make_request(
            "App.Table.Create",
            params=params,
            method="POST",
            data={'data': json.dumps(data)}
        )
    
    def update_data(self, model_name: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新表单数据
        Args:
            model_name: 表单名称
            record_id: 记录ID
            data: 要更新的数据，字典格式，更新时的初始化数据，需要JSON编码后传递。格式：data={"字段名1":"字段值1","字段名2":"字段值2"...}。
        """
        params = {
            'model_name': model_name,
            'id': record_id
        }
        return self._make_request(
            "App.Table.Update",
            params=params,
            method="POST",
            data={'data': json.dumps(data)}
        )
    
    def delete_data(self, model_name: str, record_id: str) -> Dict[str, Any]:
        """删除表单数据
        Args:
            model_name: 表单名称
            record_id: 记录ID
        """
        params = {
            'model_name': model_name,
            'id': record_id
        }
        return self._make_request("App.Table.Delete", params=params)
    
    def batch_update(self, model_name: str, where: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """批量更新数据
        Args:
            model_name: 表单名称
            where: 查询条件，字典格式，查询条件，需要JSON编码后传递。格式：where={"字段名1":"字段值1","字段名2":"字段值2"...}。
            data: 要更新的数据，字典格式，更新时的初始化数据，需要JSON编码后传递。格式：data={"字段名1":"字段值1","字段名2":"字段值2"...}。
        """
        params = {
            'model_name': model_name,
        }
        return self._make_request("App.Table.FreeUpdate", 
            params=params, 
            method="POST", 
            data={'where': json.dumps(where), 'data': json.dumps(data)}
        )
    
    def batch_delete(self, model_name: str, where: Dict[str, Any]) -> Dict[str, Any]:
        """批量删除数据
        Args:
            model_name: 表单名称
            where: 查询条件，字典格式，查询条件，需要JSON编码后传递。格式：where={"字段名1":"字段值1","字段名2":"字段值2"...}。
        """
        params = {
            'model_name': model_name
        }
        return self._make_request("App.Table.FreeDelete", 
            params=params, 
            method="POST", 
            data={'where': json.dumps(where)}
        )


# 便捷函数
def create_client() -> YesApiClient:
    """创建 YesApi 客户端实例"""
    return YesApiClient()


if __name__ == "__main__":
    # 测试代码
    try:
        client = create_client()
        
        # 测试获取模型列表
        print("获取表单模型列表...")
        models = client.get_models()
        print(f"模型列表: {models}")
        
    except YesApiError as e:
        print(f"YesApi 错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
