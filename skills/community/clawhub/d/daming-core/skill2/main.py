"""
民夫团队 - 外部执行、统计追踪
负责实际任务执行，生产环境行为，统计更新
"""

import json
import time
import random
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# 导入工部调度器
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skill1.bu.gong.scheduler import GongBuScheduler


class MinFuTeam:
    """民夫团队 - 外部执行器"""
    
    def __init__(self, task_id: str, execution_id: str):
        self.task_id = task_id
        self.execution_id = execution_id
        # 生产环境需要配置 PROJECT_ROOT
        project_root = os.environ.get("PROJECT_ROOT", "{{PROJECT_ROOT}}")
        self.task_dir = Path(project_root) / "active_tasks" / task_id
        self.stats_file = self.task_dir / "execution_stats.json"
        
        # 确保任务目录存在
        if not self.task_dir.exists():
            self.task_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict[str, Any]:
        """加载执行统计"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "task_id": self.task_id,
            "execution_id": self.execution_id,
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_tokens_used": 0,
            "average_execution_time": 0,
            "execution_history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    def _save_stats(self):
        """保存执行统计"""
        self.stats["updated_at"] = datetime.now().isoformat()
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def _build_default_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """构建默认工作流"""
        return {
            "action": "generate_image",
            "params": params,
            "estimated_tokens": 50
        }
    
    def execute_comfyui(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行ComfyUI工作流（真实调用高算力设备）
        连接到配置的ComfyUI服务器执行实际工作流
        """
        start_time = time.time()
        
        # 执行参数
        action = workflow_config.get("action", "generate_image")
        params = workflow_config.get("params", {})
        estimated_tokens = workflow_config.get("estimated_tokens", 50)
        workflow_file = workflow_config.get("workflow_file")
        
        print(f"👷 民夫团队：开始执行 {action}")
        print(f"  任务ID: {self.task_id}")
        print(f"  执行ID: {self.execution_id}")
        print(f"  参数: {params}")
        
        # 初始化变量
        is_success = False
        status = "failed"
        result_message = ""
        prompt_id = None
        output_files = []
        
        try:
            # 加载外部代理配置
            try:
                import yaml
            except ImportError:
                # 尝试从虚拟环境导入
                import sys
                # 生产环境需要配置虚拟环境路径
                venv_path = os.environ.get("VENV_PATH", "{{VENV_PATH}}")
                sys.path.insert(0, venv_path)
                import yaml
            
            # 生产环境需要配置配置文件路径
            project_root = os.environ.get("PROJECT_ROOT", "{{PROJECT_ROOT}}")
            config_path = Path(project_root) / "config" / "external_agents.yaml"
            if not config_path.exists():
                raise FileNotFoundError(f"外部代理配置文件不存在: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 获取主ComfyUI服务器配置
            server_config = config.get("comfyui_servers", {}).get("main", {})
            base_url = server_config.get("base_url", "http://{{COMFYUI_SERVER_IP}}:{{COMFYUI_SERVER_PORT}}")
            api_endpoints = server_config.get("api_endpoints", {})
            
            print(f"  连接到ComfyUI服务器: {base_url}")
            
            # 导入requests库（如果可用）
            try:
                import requests
            except ImportError:
                # 尝试从虚拟环境导入
                try:
                    import sys
                    # 生产环境需要配置虚拟环境路径
                    venv_path = os.environ.get("VENV_PATH", "{{VENV_PATH}}")
                    sys.path.insert(0, venv_path)
                    import requests
                    use_curl = False
                except ImportError:
                    print("⚠️  requests库未安装，使用curl替代")
                    use_curl = True
            else:
                use_curl = False
            
            # 读取工作流文件
            if workflow_file and Path(workflow_file).exists():
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
            else:
                # 如果没有指定工作流文件，使用默认参数构建简单工作流
                workflow_data = self._build_default_workflow(params)
            
            # 准备API请求
            prompt_url = f"{base_url}{api_endpoints.get('prompt', '/prompt')}"
            prompt_payload = {"prompt": workflow_data}
            
            # 执行工作流
            if use_curl:
                # 使用curl执行
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
                    json.dump(prompt_payload, tmp, ensure_ascii=False, indent=2)
                    tmp_path = tmp.name
                
                curl_cmd = [
                    "curl", "-X", "POST",
                    "-H", "Content-Type: application/json",
                    "-d", f"@{tmp_path}",
                    prompt_url
                ]
                
                result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
                
                import os
                os.unlink(tmp_path)
                
                if result.returncode != 0:
                    raise Exception(f"Curl请求失败: {result.stderr}")
                
                response = json.loads(result.stdout)
            else:
                # 使用requests执行
                response = requests.post(prompt_url, json=prompt_payload, timeout=30)
                response.raise_for_status()
                response = response.json()
            
            # 获取提示ID
            prompt_id = response.get("prompt_id")
            if not prompt_id:
                raise Exception(f"API响应中没有prompt_id: {response}")
            
            print(f"  ✅ 工作流提交成功，提示ID: {prompt_id}")
            
            # 轮询执行状态
            history_url = f"{base_url}{api_endpoints.get('history', '/history')}/{prompt_id}"
            max_wait_time = server_config.get("performance", {}).get("execution_timeout", 600)
            poll_interval = 5
            
            print(f"  等待执行完成，超时: {max_wait_time}秒...")
            
            import time as time_module
            start_wait = time_module.time()
            status = "pending"
            
            while time_module.time() - start_wait < max_wait_time:
                if use_curl:
                    curl_cmd = ["curl", "-s", history_url]
                    result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
                    if result.returncode != 0:
                        time_module.sleep(poll_interval)
                        continue
                    
                    history_data = json.loads(result.stdout)
                else:
                    history_resp = requests.get(history_url, timeout=10)
                    history_resp.raise_for_status()
                    history_data = history_resp.json()
                
                # 检查执行状态
                if prompt_id in history_data:
                    prompt_info = history_data[prompt_id]
                    if prompt_info.get("status", {}).get("completed", False):
                        is_success = True
                        status = "completed"
                        result_message = f"{action} 执行成功"
                        break
                    elif prompt_info.get("status", {}).get("error", False):
                        status = "failed"
                        result_message = f"{action} 执行失败: {prompt_info.get('status', {}).get('error_message', '未知错误')}"
                        break
                
                time_module.sleep(poll_interval)
            
            if status == "pending":
                status = "timeout"
                result_message = f"{action} 执行超时"
            
            # 如果成功，下载生成的图像
            if is_success and prompt_id in history_data:
                prompt_info = history_data[prompt_id]
                outputs = prompt_info.get("outputs", {})
                
                for node_id, node_output in outputs.items():
                    images = node_output.get("images", [])
                    for img in images:
                        filename = img.get("filename")
                        if filename:
                            # 构建图像下载URL
                            subfolder = img.get('subfolder', '')
                            img_type = img.get('type', 'output')
                            image_url = f"{base_url}/view?filename={filename}"
                            if subfolder:
                                image_url += f"&subfolder={subfolder}"
                            image_url += f"&type={img_type}"
                            
                            # 下载图像
                            output_path = self.task_dir / filename
                            if use_curl:
                                curl_cmd = ["curl", "-s", "-o", str(output_path), image_url]
                                subprocess.run(curl_cmd, timeout=30)
                            else:
                                img_resp = requests.get(image_url, timeout=30)
                                img_resp.raise_for_status()
                                with open(output_path, 'wb') as f:
                                    f.write(img_resp.content)
                            
                            output_files.append(str(output_path))
                            print(f"  📸 下载生成图像: {output_path}")
            
        except Exception as e:
            is_success = False
            status = "failed"
            result_message = f"{action} 执行失败: {str(e)}"
            print(f"  ❌ 执行错误: {e}")
        
        execution_time = time.time() - start_time
        
        # 更新统计
        self.stats["total_executions"] += 1
        if is_success:
            self.stats["successful_executions"] += 1
        else:
            self.stats["failed_executions"] += 1
        
        self.stats["total_tokens_used"] += estimated_tokens
        
        # 计算平均执行时间
        total_time = self.stats.get("total_execution_time", 0) + execution_time
        self.stats["total_execution_time"] = total_time
        self.stats["average_execution_time"] = total_time / self.stats["total_executions"]
        
        # 记录执行历史
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "params": params,
            "estimated_tokens": estimated_tokens,
            "actual_tokens": estimated_tokens,
            "execution_time": execution_time,
            "status": status,
            "result_message": result_message,
            "success": is_success,
            "prompt_id": prompt_id,
            "output_files": output_files
        }
        
        self.stats["execution_history"].append(execution_record)
        self._save_stats()
        
        # 创建执行结果文件
        result_file = self.task_dir / f"execution_result_{int(time.time())}.json"
        result_data = {
            "task_id": self.task_id,
            "execution_id": self.execution_id,
            "action": action,
            "params": params,
            "execution_record": execution_record,
            "stats_snapshot": self.stats.copy(),
            "prompt_id": prompt_id,
            "output_files": output_files
        }
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        # 输出结果
        if is_success:
            print(f"✅ 民夫团队：执行成功")
            print(f"  执行时间: {execution_time:.2f}秒")
            print(f"  消耗Token: {estimated_tokens}")
            print(f"  结果: {result_message}")
            if output_files:
                print(f"  生成文件: {output_files}")
        else:
            print(f"❌ 民夫团队：执行失败")
            print(f"  执行时间: {execution_time:.2f}秒")
            print(f"  消耗Token: {estimated_tokens}")
            print(f"  错误: {result_message}")
        
        return {
            "success": is_success,
            "task_id": self.task_id,
            "execution_id": self.execution_id,
            "action": action,
            "execution_time": execution_time,
            "tokens_used": estimated_tokens,
            "status": status,
            "result_message": result_message,
            "execution_record": execution_record,
            "result_file": str(result_file),
            "prompt_id": prompt_id,
            "output_files": output_files
        }
    
    def _build_default_workflow_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """构建默认工作流（当没有指定工作流文件时）"""
        # 这是一个简单的文生图工作流示例
        # 实际生产环境中应该使用配置的工作流文件
        prompt = params.get("prompt", "a beautiful landscape")
        width = params.get("width", 512)
        height = params.get("height", 512)
        
        return {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": random.randint(0, 2**32 - 1),
                    "steps": 20,
                    "cfg": 7,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "v1-5-pruned-emaonly.safetensors"
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": prompt,
                    "clip": ["4", 1]
                }
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": "",
                    "clip": ["4", 1]
                }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": ["8", 0]
                }
            }
        }
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """获取执行统计"""
        return self.stats
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "task_id": self.task_id,
            "execution_id": self.execution_id,
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_tokens_used": 0,
            "total_execution_time": 0,
            "average_execution_time": 0,
            "execution_history": [],
            "created_at": self.stats.get("created_at", datetime.now().isoformat()),
            "updated_at": datetime.now().isoformat()
        }
        self._save_stats()


def execute_comfyui_workflow(task_id: str, execution_id: str, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行ComfyUI工作流（兼容函数）
    返回执行结果
    """
    team = MinFuTeam(task_id, execution_id)
    return team.execute_comfyui(workflow_config)


def get_minfu_stats(task_id: str, execution_id: str) -> Dict[str, Any]:
    """获取民夫团队统计（兼容函数）"""
    team = MinFuTeam(task_id, execution_id)
    return team.get_execution_stats()


if __name__ == "__main__":
    # 测试民夫团队功能
    print("👷 民夫团队功能测试")
    
    # 创建测试实例
    test_task_id = "TEST_TASK"
    test_execution_id = "TEST_EXEC"
    
    team = MinFuTeam(test_task_id, test_execution_id)
    
    # 测试执行
    workflow_config = {
        "action": "generate_image",
        "params": {
            "prompt": "美丽的风景",
            "width": 512,
            "height": 512
        },
        "estimated_tokens": 75,
        "success_rate": 1.0  # 100%成功用于测试
    }
    
    result = team.execute_comfyui(workflow_config)
    print(f"✅ 测试完成：{result['success']}")
    print(f"统计: {team.get_execution_stats()}")