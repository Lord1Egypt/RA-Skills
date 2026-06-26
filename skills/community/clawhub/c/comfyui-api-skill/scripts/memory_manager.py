#!/usr/bin/env python3
"""
ComfyUI 内存和历史管理器

功能：
1. 释放内存（卸载模型）
2. 清理执行历史
3. 查看当前队列状态（GET /prompt）

使用示例：
    python memory_manager.py --action free
    python memory_manager.py --action free --unload-models
    python memory_manager.py --action free --free-memory 0.5
    python memory_manager.py --action clear-history
    python memory_manager.py --action clear-history --prompt-id task-id
    python memory_manager.py --action status
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import requests
except ImportError:
    print("错误：缺少 requests 库，请运行：pip install requests>=2.28.0")
    sys.exit(1)

# 导入配置加载器
try:
    from config_loader import get_config
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from config_loader import get_config


class MemoryManager:
    """ComfyUI 内存和历史管理器"""
    
    def __init__(self, server_url: str = None, api_key: str = None):
        """
        初始化内存管理器
        
        Args:
            server_url: ComfyUI 服务地址
            api_key: API 密钥（可选）
        """
        # 加载配置
        config = get_config()
        
        # 使用配置优先级
        self.server_url = config.get_server_url(cli_value=server_url)
        self.api_key = config.get_api_key(cli_value=api_key)
        self.session = requests.Session()
        
        # 设置请求头
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
    
    def free_memory(
        self,
        unload_models: bool = False,
        free_memory: float = None
    ) -> Dict[str, Any]:
        """
        释放内存
        
        Args:
            unload_models: 是否卸载模型
            free_memory: 释放内存比例 (0.0-1.0)
            
        Returns:
            操作结果
            
        Raises:
            Exception: 操作失败时抛出异常
        """
        url = f"{self.server_url}/free"
        
        data = {}
        if unload_models:
            data["unload_models"] = True
        if free_memory is not None:
            data["free_memory"] = free_memory
        
        try:
            response = self.session.post(url, json=data, timeout=30)
            
            if response.status_code >= 400:
                raise Exception(f"释放内存失败: HTTP {response.status_code}, {response.text}")
            
            result = response.json()
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def clear_history(self, prompt_id: str = None) -> Dict[str, Any]:
        """
        清理执行历史
        
        Args:
            prompt_id: 任务 ID（可选，不指定则清空所有历史）
            
        Returns:
            操作结果
            
        Raises:
            Exception: 操作失败时抛出异常
        """
        url = f"{self.server_url}/history"
        
        data = {}
        if prompt_id:
            data["delete"] = [prompt_id]
        else:
            data["clear"] = True
        
        try:
            response = self.session.post(url, json=data, timeout=30)
            
            if response.status_code >= 400:
                raise Exception(f"清理历史失败: HTTP {response.status_code}, {response.text}")
            
            result = response.json()
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        获取当前队列状态（GET /prompt）
        
        Returns:
            队列状态信息
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        url = f"{self.server_url}/prompt"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code >= 400:
                raise Exception(f"查询队列状态失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def format_queue_status(self, status: Dict[str, Any]) -> str:
        """
        格式化队列状态输出
        
        Args:
            status: 队列状态数据
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("队列状态")
        lines.append("=" * 60)
        
        # 执行信息
        exec_info = status.get("exec_info", {})
        if exec_info:
            lines.append(f"\n队列剩余任务: {exec_info.get('queue_remaining', 0)}")
        
        # 运行中的任务
        running = status.get("queue_running", [])
        lines.append(f"\n运行中任务: {len(running)} 个")
        if running:
            for i, task in enumerate(running, 1):
                prompt_id = task.get("prompt_id", "N/A")
                lines.append(f"  {i}. 任务 ID: {prompt_id}")
        
        # 排队中的任务
        pending = status.get("queue_pending", [])
        lines.append(f"\n排队中任务: {len(pending)} 个")
        if pending:
            for i, task in enumerate(pending, 1):
                prompt_id = task.get("prompt_id", "N/A")
                lines.append(f"  {i}. 任务 ID: {prompt_id}")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="ComfyUI 内存和历史管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 释放内存
  python memory_manager.py --action free
  python memory_manager.py --action free --unload-models
  python memory_manager.py --action free --free-memory 0.5
  
  # 清理历史
  python memory_manager.py --action clear-history
  python memory_manager.py --action clear-history --prompt-id task-id
  
  # 查看队列状态
  python memory_manager.py --action status
        """
    )
    
    parser.add_argument(
        "--action",
        required=True,
        choices=["free", "clear-history", "status"],
        help="操作类型：free=释放内存，clear-history=清理历史，status=队列状态"
    )
    
    parser.add_argument(
        "--unload-models",
        action="store_true",
        help="卸载模型（仅用于 free 操作）"
    )
    
    parser.add_argument(
        "--free-memory",
        type=float,
        help="释放内存比例 0.0-1.0（仅用于 free 操作）"
    )
    
    parser.add_argument(
        "--prompt-id",
        help="任务 ID（仅用于 clear-history 操作，不指定则清空所有历史）"
    )
    
    parser.add_argument(
        "--server-url",
        help="ComfyUI 服务地址（默认：使用配置文件中的值）"
    )
    
    parser.add_argument(
        "--api-key",
        help="API 密钥（可选）"
    )
    
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="以 JSON 格式输出"
    )
    
    args = parser.parse_args()
    
    # 创建内存管理器
    manager = MemoryManager(
        server_url=args.server_url,
        api_key=args.api_key
    )
    
    try:
        if args.action == "free":
            result = manager.free_memory(
                unload_models=args.unload_models,
                free_memory=args.free_memory
            )
            
            if args.output_json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("✓ 内存释放成功")
                if args.unload_models:
                    print("  已卸载模型")
                if args.free_memory is not None:
                    print(f"  释放比例: {args.free_memory * 100:.0f}%")
                
        elif args.action == "clear-history":
            result = manager.clear_history(prompt_id=args.prompt_id)
            
            if args.output_json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                if args.prompt_id:
                    print(f"✓ 已删除历史记录: {args.prompt_id}")
                else:
                    print("✓ 已清空所有历史记录")
                
        elif args.action == "status":
            status = manager.get_queue_status()
            
            if args.output_json:
                print(json.dumps(status, indent=2, ensure_ascii=False))
            else:
                print(manager.format_queue_status(status))
            
    except Exception as e:
        print(f"✗ 操作失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
