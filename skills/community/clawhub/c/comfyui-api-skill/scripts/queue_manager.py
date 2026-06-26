#!/usr/bin/env python3
"""
ComfyUI 队列管理器

功能：
1. 查看当前执行队列
2. 中断正在执行的任务
3. 支持从配置文件读取配置

使用示例：
    python queue_manager.py --action list
    python queue_manager.py --action interrupt
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

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


class QueueManager:
    """ComfyUI 队列管理器"""
    
    def __init__(self, server_url: str = None, api_key: str = None):
        """
        初始化队列管理器
        
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
    
    def list_queue(self) -> Dict[str, Any]:
        """
        查看当前队列
        
        Returns:
            队列信息
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        url = f"{self.server_url}/queue"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code >= 400:
                raise Exception(f"查询队列失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def interrupt(self) -> bool:
        """
        中断当前执行
        
        Returns:
            是否成功
            
        Raises:
            Exception: 中断失败时抛出异常
        """
        url = f"{self.server_url}/interrupt"
        
        try:
            response = self.session.post(url, timeout=10)
            
            if response.status_code >= 400:
                raise Exception(f"中断失败: HTTP {response.status_code}, {response.text}")
            
            print("✓ 已发送中断信号")
            return True
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def format_queue_info(self, queue_data: Dict[str, Any]) -> str:
        """
        格式化队列信息
        
        Args:
            queue_data: 队列数据
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("ComfyUI 执行队列")
        lines.append("=" * 60)
        
        # 运行中的任务
        running = queue_data.get("queue_running", [])
        lines.append(f"\n【运行中】({len(running)} 个任务)")
        if running:
            for i, task in enumerate(running, 1):
                prompt_id = task.get("prompt_id", "N/A")
                lines.append(f"  {i}. 任务 ID: {prompt_id}")
        else:
            lines.append("  无")
        
        # 排队中的任务
        pending = queue_data.get("queue_pending", [])
        lines.append(f"\n【排队中】({len(pending)} 个任务)")
        if pending:
            for i, task in enumerate(pending, 1):
                prompt_id = task.get("prompt_id", "N/A")
                lines.append(f"  {i}. 任务 ID: {prompt_id}")
        else:
            lines.append("  无")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="ComfyUI 队列管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python queue_manager.py --action list
  python queue_manager.py --action interrupt
        """
    )
    
    parser.add_argument(
        "--action",
        required=True,
        choices=["list", "interrupt"],
        help="操作类型：list=查看队列，interrupt=中断执行"
    )
    
    parser.add_argument(
        "--server-url",
        help="ComfyUI 服务地址（默认：http://127.0.0.1:8188）"
    )
    
    parser.add_argument(
        "--api-key",
        help="API 密钥（可选）"
    )
    
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="以 JSON 格式输出（仅适用于 list 操作）"
    )
    
    args = parser.parse_args()
    
    # 创建队列管理器
    manager = QueueManager(
        server_url=args.server_url,
        api_key=args.api_key
    )
    
    try:
        if args.action == "list":
            queue_data = manager.list_queue()
            
            if args.output_json:
                print(json.dumps(queue_data, indent=2, ensure_ascii=False))
            else:
                print(manager.format_queue_info(queue_data))
                
        elif args.action == "interrupt":
            manager.interrupt()
            
    except Exception as e:
        print(f"✗ 操作失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
