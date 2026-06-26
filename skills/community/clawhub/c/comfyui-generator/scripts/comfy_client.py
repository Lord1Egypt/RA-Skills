#!/usr/bin/env python3
"""
ComfyUI API Client for OpenClaw
"""

import requests
import json
import time
import os
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class ComfyUIClient:
    """ComfyUI API客户端"""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or os.getenv("COMFY_BASE_URL", "http://127.0.0.1:8188")
        self.api_key = api_key or os.getenv("COMFY_API_KEY", "local_comfyui")
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "OpenClaw-ComfyUI-Client/1.0",
            "Accept": "application/json"
        })
        
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
        
        logger.info(f"ComfyUI客户端初始化: {self.base_url}")
    
    def check_connection(self) -> bool:
        """检查连接状态"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"连接检查失败: {e}")
            return False
    
    def get_system_stats(self) -> Optional[Dict]:
        """获取系统状态"""
        try:
            response = self.session.get(f"{self.base_url}/system_stats", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"获取系统状态失败: {e}")
        return None
    
    def load_workflow(self, workflow_path: str) -> Optional[Dict]:
        """加载工作流文件"""
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            return workflow
        except Exception as e:
            logger.error(f"加载工作流失败 {workflow_path}: {e}")
            return None
    
    def generate_image(self, prompt: str, workflow_path: str = None, **kwargs) -> Optional[Dict]:
        """生成图片"""
        
        # 如果没有指定工作流，使用默认
        if workflow_path is None:
            workflow_path = os.path.join(
                os.path.dirname(__file__),
                "..", "workflows", "image_generation.json"
            )
        
        # 加载工作流
        workflow = self.load_workflow(workflow_path)
        if not workflow:
            return None
        
        # 更新工作流参数
        workflow = self._update_workflow_params(workflow, prompt, **kwargs)
        
        # 发送生成请求
        try:
            logger.info(f"发送生成请求: {prompt[:50]}...")
            response = self.session.post(
                f"{self.base_url}/prompt",
                json={"prompt": workflow},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"生成请求成功: {result.get('prompt_id')}")
                return result
            else:
                logger.error(f"生成请求失败: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"生成图片失败: {e}")
            return None
    
    def _update_workflow_params(self, workflow: Dict, prompt: str, **kwargs) -> Dict:
        """更新工作流参数"""
        
        # 找到文本编码节点
        for node_id, node_data in workflow.get("workflow", {}).items():
            if node_data.get("class_type") == "CLIPTextEncode":
                # 检查是否是正面提示词节点
                inputs = node_data.get("inputs", {})
                if "text" in inputs:
                    current_text = inputs["text"]
                    if not current_text or current_text.startswith("{"):
                        # 替换为实际提示词
                        node_data["inputs"]["text"] = prompt
        
        # 更新其他参数
        if "seed" in kwargs:
            self._update_seed(workflow, kwargs["seed"])
        
        if "width" in kwargs and "height" in kwargs:
            self._update_dimensions(workflow, kwargs["width"], kwargs["height"])
        
        if "steps" in kwargs:
            self._update_steps(workflow, kwargs["steps"])
        
        return workflow
    
    def _update_seed(self, workflow: Dict, seed: int):
        """更新随机种子"""
        for node_id, node_data in workflow.get("workflow", {}).items():
            if node_data.get("class_type") == "KSampler":
                if "inputs" in node_data and "seed" in node_data["inputs"]:
                    node_data["inputs"]["seed"] = seed
    
    def _update_dimensions(self, workflow: Dict, width: int, height: int):
        """更新图片尺寸"""
        for node_id, node_data in workflow.get("workflow", {}).items():
            if node_data.get("class_type") == "EmptyLatentImage":
                if "inputs" in node_data:
                    node_data["inputs"]["width"] = width
                    node_data["inputs"]["height"] = height
    
    def _update_steps(self, workflow: Dict, steps: int):
        """更新生成步数"""
        for node_id, node_data in workflow.get("workflow", {}).items():
            if node_data.get("class_type") == "KSampler":
                if "inputs" in node_data and "steps" in node_data["inputs"]:
                    node_data["inputs"]["steps"] = steps
    
    def get_history(self, limit: int = 10) -> Optional[List]:
        """获取生成历史"""
        try:
            response = self.session.get(f"{self.base_url}/history", timeout=5)
            if response.status_code == 200:
                history = response.json()
                # 只返回最新的记录
                return list(history.values())[-limit:]
        except Exception as e:
            logger.error(f"获取历史失败: {e}")
        return None
    
    def upload_image(self, image_path: str) -> Optional[str]:
        """上传图片到ComfyUI"""
        try:
            with open(image_path, 'rb') as f:
                files = {'image': (os.path.basename(image_path), f, 'image/jpeg')}
                response = self.session.post(
                    f"{self.base_url}/upload/image",
                    files=files,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("name")
                else:
                    logger.error(f"上传图片失败: HTTP {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"上传图片失败: {e}")
            return None
    
    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> bool:
        """等待生成完成"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                history = self.get_history(limit=50)
                if history:
                    for entry in history:
                        if entry.get("prompt") == prompt_id:
                            status = entry.get("status")
                            if status == "success":
                                logger.info(f"生成完成: {prompt_id}")
                                return True
                            elif status == "error":
                                logger.error(f"生成失败: {prompt_id}")
                                return False
                
                # 等待一段时间再检查
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"等待生成时出错: {e}")
                time.sleep(5)
        
        logger.warning(f"生成超时: {prompt_id}")
        return False
    
    def batch_generate(self, prompts: List[str], workflow_path: str = None, **kwargs) -> List[Dict]:
        """批量生成"""
        results = []
        
        for i, prompt in enumerate(prompts):
            logger.info(f"批量生成 [{i+1}/{len(prompts)}]: {prompt[:50]}...")
            
            result = self.generate_image(prompt, workflow_path, **kwargs)
            if result:
                results.append({
                    "index": i,
                    "prompt": prompt,
                    "result": result
                })
            
            # 批次间等待
            if i < len(prompts) - 1:
                time.sleep(2)
        
        return results

# 使用示例
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ComfyUI客户端测试")
    parser.add_argument("--test-connection", action="store_true", help="测试连接")
    parser.add_argument("--generate", type=str, help="生成图片的提示词")
    parser.add_argument("--workflow", type=str, help="工作流文件路径")
    
    args = parser.parse_args()
    
    # 设置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建客户端
    client = ComfyUIClient()
    
    if args.test_connection:
        if client.check_connection():
            print("✅ 连接成功")
            
            stats = client.get_system_stats()
            if stats:
                print(f"系统状态: {stats}")
        else:
            print("❌ 连接失败")
    
    elif args.generate:
        print(f"生成图片: {args.generate}")
        result = client.generate_image(args.generate, args.workflow)
        if result:
            print(f"✅ 生成请求发送成功")
            print(f"任务ID: {result.get('prompt_id')}")
        else:
            print("❌ 生成失败")