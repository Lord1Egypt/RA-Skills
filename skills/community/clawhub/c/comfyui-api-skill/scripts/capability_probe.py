#!/usr/bin/env python3
"""
ComfyUI 能力探测器（增强版）

功能：
1. 获取节点定义（全部或单个）
2. 获取模型列表（全部或按文件夹）
3. 获取系统状态
4. 获取 embeddings 列表
5. 获取扩展列表
6. 获取服务器特性
7. 获取模型元数据
8. 获取工作流模板

使用示例：
    python capability_probe.py --type nodes
    python capability_probe.py --type nodes --node-class KSampler
    python capability_probe.py --type models
    python capability_probe.py --type models --folder checkpoints
    python capability_probe.py --type embeddings
    python capability_probe.py --type extensions
    python capability_probe.py --type features
    python capability_probe.py --type metadata --model sd_xl_base.safetensors
    python capability_probe.py --type templates
    python capability_probe.py --type system
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


class CapabilityProbe:
    """ComfyUI 能力探测器"""
    
    def __init__(self, server_url: str = None, api_key: str = None):
        """
        初始化能力探测器
        
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
    
    def get_nodes(self, node_class: str = None) -> Dict[str, Any]:
        """
        获取节点定义
        
        Args:
            node_class: 节点类名（可选，不指定则返回所有节点）
            
        Returns:
            节点定义字典
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        if node_class:
            url = f"{self.server_url}/object_info/{node_class}"
        else:
            url = f"{self.server_url}/object_info"
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code >= 400:
                raise Exception(f"查询节点失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def get_models(self, folder: str = None) -> Dict[str, Any]:
        """
        获取模型列表
        
        Args:
            folder: 模型文件夹名（可选，如 'checkpoints', 'loras' 等）
            
        Returns:
            模型列表
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        if folder:
            url = f"{self.server_url}/models/{folder}"
        else:
            url = f"{self.server_url}/models"
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code >= 400:
                raise Exception(f"查询模型失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        获取系统状态
        
        Returns:
            系统状态信息
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        url = f"{self.server_url}/system_stats"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code >= 400:
                raise Exception(f"查询系统状态失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def get_embeddings(self) -> list:
        """
        获取可用的 embeddings 列表
        
        Returns:
            embeddings 名称列表
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        url = f"{self.server_url}/embeddings"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code >= 400:
                raise Exception(f"查询 embeddings 失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def get_extensions(self) -> list:
        """
        获取扩展列表
        
        Returns:
            扩展列表
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        url = f"{self.server_url}/extensions"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code >= 400:
                raise Exception(f"查询扩展失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def get_features(self) -> Dict[str, Any]:
        """
        获取服务器功能特性
        
        Returns:
            功能特性字典
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        url = f"{self.server_url}/features"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code >= 400:
                raise Exception(f"查询特性失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def get_model_metadata(self, filename: str) -> Dict[str, Any]:
        """
        获取模型元数据
        
        Args:
            filename: 模型文件名
            
        Returns:
            模型元数据
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        url = f"{self.server_url}/view_metadata/{filename}"
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code >= 400:
                raise Exception(f"查询元数据失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def get_workflow_templates(self) -> Dict[str, Any]:
        """
        获取工作流模板
        
        Returns:
            工作流模板映射
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        url = f"{self.server_url}/workflow_templates"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code >= 400:
                raise Exception(f"查询模板失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def format_nodes_info(self, nodes_data: Dict[str, Any]) -> str:
        """
        格式化节点信息
        
        Args:
            nodes_data: 节点数据
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 60)
        
        if len(nodes_data) == 1:
            # 单个节点
            node_name = list(nodes_data.keys())[0]
            lines.append(f"节点详情: {node_name}")
        else:
            lines.append(f"可用节点（共 {len(nodes_data)} 个）")
        
        lines.append("=" * 60)
        
        for node_name, node_info in nodes_data.items():
            lines.append(f"\n【{node_name}】")
            
            # 显示输入参数
            input_info = node_info.get("input", {})
            required = input_info.get("required", {})
            optional = input_info.get("optional", {})
            
            if required:
                lines.append("  必需参数:")
                for param, details in required.items():
                    lines.append(f"    - {param}: {details}")
            
            if optional:
                lines.append("  可选参数:")
                for param, details in optional.items():
                    lines.append(f"    - {param}: {details}")
        
        return "\n".join(lines)
    
    def format_models_info(self, models_data: Any) -> str:
        """
        格式化模型信息
        
        Args:
            models_data: 模型数据
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 60)
        
        if isinstance(models_data, dict):
            # 多个模型文件夹
            lines.append("可用模型")
            lines.append("=" * 60)
            
            for model_type, models in models_data.items():
                lines.append(f"\n【{model_type}】({len(models)} 个)")
                for model in models[:10]:  # 只显示前 10 个
                    lines.append(f"  - {model}")
                if len(models) > 10:
                    lines.append(f"  ... 还有 {len(models) - 10} 个模型")
        elif isinstance(models_data, list):
            # 单个文件夹的模型列表
            lines.append(f"模型列表（共 {len(models_data)} 个）")
            lines.append("=" * 60)
            
            for model in models_data[:20]:  # 只显示前 20 个
                lines.append(f"  - {model}")
            if len(models_data) > 20:
                lines.append(f"  ... 还有 {len(models_data) - 20} 个模型")
        
        return "\n".join(lines)
    
    def format_system_info(self, system_data: Dict[str, Any]) -> str:
        """
        格式化系统信息
        
        Args:
            system_data: 系统数据
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("系统状态")
        lines.append("=" * 60)
        
        # 系统信息
        system = system_data.get("system", {})
        if system:
            lines.append(f"\n操作系统: {system.get('os', 'N/A')}")
            lines.append(f"Python 版本: {system.get('python_version', 'N/A')}")
            lines.append(f"ComfyUI 版本: {system.get('comfyui_version', 'N/A')}")
        
        # 设备信息
        devices = system_data.get("devices", [])
        if devices:
            lines.append("\nGPU 设备:")
            for i, device in enumerate(devices, 1):
                lines.append(f"  设备 {i}:")
                lines.append(f"    名称: {device.get('name', 'N/A')}")
                lines.append(f"    类型: {device.get('type', 'N/A')}")
                vram_total = device.get('vram_total', 0)
                vram_used = device.get('vram_used', 0)
                if vram_total:
                    lines.append(f"    显存: {vram_total / (1024**3):.2f} GB")
                    lines.append(f"    已用显存: {vram_used / (1024**3):.2f} GB ({vram_used/vram_total*100:.1f}%)")
        
        return "\n".join(lines)
    
    def format_embeddings_info(self, embeddings: list) -> str:
        """
        格式化 embeddings 信息
        
        Args:
            embeddings: embeddings 列表
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"可用 Embeddings（共 {len(embeddings)} 个）")
        lines.append("=" * 60)
        
        if not embeddings:
            lines.append("\n没有找到 embeddings")
        else:
            for emb in embeddings:
                lines.append(f"  - {emb}")
        
        return "\n".join(lines)
    
    def format_extensions_info(self, extensions: list) -> str:
        """
        格式化扩展信息
        
        Args:
            extensions: 扩展列表
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"已安装扩展（共 {len(extensions)} 个）")
        lines.append("=" * 60)
        
        if not extensions:
            lines.append("\n没有安装扩展")
        else:
            for ext in extensions:
                lines.append(f"  - {ext}")
        
        return "\n".join(lines)
    
    def format_features_info(self, features: Dict[str, Any]) -> str:
        """
        格式化功能特性信息
        
        Args:
            features: 功能特性数据
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("服务器功能特性")
        lines.append("=" * 60)
        
        for key, value in features.items():
            lines.append(f"\n{key}: {value}")
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="ComfyUI 能力探测器（增强版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 获取所有节点
  python capability_probe.py --type nodes
  
  # 获取单个节点详情
  python capability_probe.py --type nodes --node-class KSampler
  
  # 获取所有模型
  python capability_probe.py --type models
  
  # 获取特定文件夹的模型
  python capability_probe.py --type models --folder checkpoints
  
  # 获取 embeddings
  python capability_probe.py --type embeddings
  
  # 获取扩展
  python capability_probe.py --type extensions
  
  # 获取服务器特性
  python capability_probe.py --type features
  
  # 获取模型元数据
  python capability_probe.py --type metadata --model sd_xl_base.safetensors
  
  # 获取工作流模板
  python capability_probe.py --type templates
  
  # 获取系统状态
  python capability_probe.py --type system
        """
    )
    
    parser.add_argument(
        "--type",
        required=True,
        choices=["nodes", "models", "system", "embeddings", "extensions", "features", "metadata", "templates"],
        help="探测类型"
    )
    
    parser.add_argument(
        "--node-class",
        help="节点类名（仅用于 nodes 类型）"
    )
    
    parser.add_argument(
        "--folder",
        help="模型文件夹名（仅用于 models 类型）"
    )
    
    parser.add_argument(
        "--model",
        help="模型文件名（仅用于 metadata 类型）"
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
    
    # 创建能力探测器
    probe = CapabilityProbe(
        server_url=args.server_url,
        api_key=args.api_key
    )
    
    try:
        if args.type == "nodes":
            data = probe.get_nodes(node_class=args.node_class)
            
            if args.output_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(probe.format_nodes_info(data))
                
        elif args.type == "models":
            data = probe.get_models(folder=args.folder)
            
            if args.output_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(probe.format_models_info(data))
                
        elif args.type == "system":
            data = probe.get_system_stats()
            
            if args.output_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(probe.format_system_info(data))
        
        elif args.type == "embeddings":
            data = probe.get_embeddings()
            
            if args.output_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(probe.format_embeddings_info(data))
        
        elif args.type == "extensions":
            data = probe.get_extensions()
            
            if args.output_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(probe.format_extensions_info(data))
        
        elif args.type == "features":
            data = probe.get_features()
            
            if args.output_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(probe.format_features_info(data))
        
        elif args.type == "metadata":
            if not args.model:
                print("错误：metadata 类型需要 --model 参数")
                sys.exit(1)
            
            data = probe.get_model_metadata(args.model)
            
            if args.output_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print("=" * 60)
                print(f"模型元数据: {args.model}")
                print("=" * 60)
                for key, value in data.items():
                    print(f"\n{key}: {value}")
        
        elif args.type == "templates":
            data = probe.get_workflow_templates()
            
            if args.output_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print("=" * 60)
                print("工作流模板")
                print("=" * 60)
                for module, template in data.items():
                    print(f"\n【{module}】")
                    if isinstance(template, dict):
                        for k, v in template.items():
                            print(f"  {k}: {v}")
                    else:
                        print(f"  {template}")
            
    except Exception as e:
        print(f"✗ 探测失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
