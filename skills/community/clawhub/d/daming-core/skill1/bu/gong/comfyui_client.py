#!/usr/bin/env python3
"""
ComfyUI客户端 - 真正的ComfyUI API调用
用于连接高算力设备执行工作流
"""

import json
import time
import requests
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComfyUIClient:
    """ComfyUI客户端"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # 生产环境需要配置配置文件路径
            project_root = os.environ.get("PROJECT_ROOT", "{{PROJECT_ROOT}}")
            config_path = str(Path(project_root) / "config" / "external_agents.json")
        """初始化ComfyUI客户端"""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.base_url = self.config["comfyui_servers"]["main"]["base_url"]
        self.api_endpoints = self.config["comfyui_servers"]["main"]["api_endpoints"]
        self.connection_config = self.config["comfyui_servers"]["main"]["connection"]
        
        # 创建会话
        self.session = requests.Session()
        self.session.timeout = self.connection_config["timeout"]
        
        logger.info(f"ComfyUI客户端初始化完成，服务器: {self.base_url}")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            logger.error(f"配置文件不存在: {self.config_path}")
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return config
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            url = f"{self.base_url}{self.api_endpoints.get('view', '/')}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "status": "healthy",
                    "response_time": response.elapsed.total_seconds(),
                    "message": "ComfyUI服务器运行正常"
                }
            else:
                return {
                    "success": False,
                    "status": "unhealthy",
                    "status_code": response.status_code,
                    "message": f"服务器返回状态码: {response.status_code}"
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "status": "timeout",
                "message": "连接超时"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "status": "connection_error",
                "message": "连接失败"
            }
        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "message": f"健康检查异常: {str(e)}"
            }
    
    def execute_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行ComfyUI工作流
        
        Args:
            workflow_config: 工作流配置，包含：
                - workflow: 工作流JSON
                - client_id: 客户端ID
                - extra_data: 额外数据
        
        Returns:
            执行结果
        """
        start_time = time.time()
        
        try:
            # 准备API请求
            url = f"{self.base_url}{self.api_endpoints['prompt']}"
            
            # 提取工作流
            workflow = workflow_config.get("workflow", {})
            client_id = workflow_config.get("client_id", "daming_court")
            extra_data = workflow_config.get("extra_data", {})
            
            # 构建请求数据
            payload = {
                "prompt": workflow,
                "client_id": client_id
            }
            
            if extra_data:
                payload["extra_data"] = extra_data
            
            logger.info(f"发送工作流执行请求: {url}")
            logger.debug(f"工作流配置: {json.dumps(workflow_config, indent=2)}")
            
            # 发送请求
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            execution_time = time.time() - start_time
            
            logger.info(f"工作流执行成功，执行时间: {execution_time:.2f}秒")
            
            return {
                "success": True,
                "execution_id": result.get("prompt_id"),
                "node_errors": result.get("node_errors", {}),
                "execution_time": execution_time,
                "raw_response": result,
                "message": "工作流执行成功"
            }
        
        except requests.exceptions.Timeout:
            execution_time = time.time() - start_time
            logger.error(f"工作流执行超时，耗时: {execution_time:.2f}秒")
            return {
                "success": False,
                "error": "请求超时",
                "execution_time": execution_time,
                "message": "ComfyUI服务器响应超时"
            }
        
        except requests.exceptions.ConnectionError:
            execution_time = time.time() - start_time
            logger.error(f"连接失败，耗时: {execution_time:.2f}秒")
            return {
                "success": False,
                "error": "连接失败",
                "execution_time": execution_time,
                "message": "无法连接到ComfyUI服务器"
            }
        
        except requests.exceptions.HTTPError as e:
            execution_time = time.time() - start_time
            logger.error(f"HTTP错误: {str(e)}，耗时: {execution_time:.2f}秒")
            return {
                "success": False,
                "error": f"HTTP错误: {response.status_code}",
                "status_code": response.status_code,
                "execution_time": execution_time,
                "message": f"服务器返回错误: {response.status_code}"
            }
        
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"工作流执行异常: {str(e)}，耗时: {execution_time:.2f}秒")
            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "message": f"工作流执行异常: {str(e)}"
            }
    
    def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        try:
            url = f"{self.base_url}{self.api_endpoints['queue']}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            queue_data = response.json()
            
            return {
                "success": True,
                "queue_running": queue_data.get("queue_running", []),
                "queue_pending": queue_data.get("queue_pending", []),
                "message": "队列状态获取成功"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"获取队列状态失败: {str(e)}"
            }
    
    def get_history(self, prompt_id: str = None) -> Dict[str, Any]:
        """获取执行历史"""
        try:
            url = f"{self.base_url}{self.api_endpoints['history']}"
            if prompt_id:
                url = f"{url}/{prompt_id}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            history_data = response.json()
            
            return {
                "success": True,
                "history": history_data,
                "message": "历史记录获取成功"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"获取历史记录失败: {str(e)}"
            }
    
    def upload_image(self, image_path: str) -> Dict[str, Any]:
        """上传图片到ComfyUI"""
        try:
            url = f"{self.base_url}{self.api_endpoints['upload']}"
            
            with open(image_path, 'rb') as f:
                files = {'image': f}
                response = self.session.post(url, files=files, timeout=30)
            
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "success": True,
                "image_info": result,
                "message": "图片上传成功"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"图片上传失败: {str(e)}"
            }


def test_connection() -> Dict[str, Any]:
    """测试连接"""
    try:
        client = ComfyUIClient()
        
        # 健康检查
        health = client.health_check()
        
        if not health["success"]:
            return health
        
        # 获取队列状态
        queue_status = client.get_queue_status()
        
        return {
            "success": True,
            "health_check": health,
            "queue_status": queue_status,
            "message": "连接测试成功"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"连接测试失败: {str(e)}"
        }


if __name__ == "__main__":
    print("🔌 ComfyUI客户端测试")
    
    result = test_connection()
    
    if result["success"]:
        print("✅ 连接测试成功")
        print(f"   服务器状态: {result['health_check']['status']}")
        print(f"   响应时间: {result['health_check'].get('response_time', 'N/A')}秒")
        print(f"   队列状态: 获取成功")
    else:
        print("❌ 连接测试失败")
        print(f"   错误: {result.get('error', '未知错误')}")
        print(f"   消息: {result.get('message', '无消息')}")