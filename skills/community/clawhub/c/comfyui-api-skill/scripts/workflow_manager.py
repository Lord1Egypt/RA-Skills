#!/usr/bin/env python3
"""
工作流管理器

功能：
1. 列出存储的工作流
2. 查看工作流详情
3. 删除工作流
4. 复制/移动工作流

使用示例：
    python workflow_manager.py --action list
    python workflow_manager.py --action show --name my_workflow.json
    python workflow_manager.py --action delete --name old_workflow.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 导入配置加载器
from config_loader import get_config


class WorkflowManager:
    """工作流管理器"""
    
    def __init__(self):
        """初始化工作流管理器"""
        self.config = get_config()
        self.workflows_dir = self.config.get_workflows_dir()
        
        # 确保目录存在
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        列出所有工作流
        
        Returns:
            工作流列表，每个元素包含名称、大小、修改时间等信息
        """
        workflows = []
        
        # 遍历 workflows 目录
        for file_path in self.workflows_dir.glob("*.json"):
            try:
                stat = file_path.stat()
                
                # 尝试读取工作流以获取元数据
                metadata = self._extract_metadata(file_path)
                
                workflows.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": stat.st_size,
                    "size_human": self._format_size(stat.st_size),
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "metadata": metadata
                })
            except Exception as e:
                print(f"警告：无法读取工作流 {file_path.name}: {str(e)}")
        
        # 按修改时间排序（最新的在前）
        workflows.sort(key=lambda x: x["modified"], reverse=True)
        
        return workflows
    
    def _extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        从工作流文件中提取元数据
        
        Args:
            file_path: 工作流文件路径
            
        Returns:
            元数据字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            
            # 统计节点数量
            node_count = len(workflow) if isinstance(workflow, dict) else 0
            
            # 尝试识别工作流类型
            workflow_type = "unknown"
            if isinstance(workflow, dict):
                # 检查是否有 KSampler 节点
                for node_id, node_data in workflow.items():
                    if isinstance(node_data, dict):
                        class_type = node_data.get("class_type", "")
                        if class_type == "KSampler":
                            # 检查是否有 LoadImage 节点
                            has_load_image = any(
                                n.get("class_type") == "LoadImage"
                                for n in workflow.values()
                                if isinstance(n, dict)
                            )
                            workflow_type = "img2img" if has_load_image else "txt2img"
                            break
            
            return {
                "node_count": node_count,
                "type": workflow_type
            }
        except Exception:
            return {
                "node_count": 0,
                "type": "unknown"
            }
    
    def _format_size(self, size: int) -> str:
        """
        格式化文件大小
        
        Args:
            size: 文件大小（字节）
            
        Returns:
            格式化的大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def show_workflow(self, name: str) -> Dict[str, Any]:
        """
        显示工作流详情
        
        Args:
            name: 工作流文件名
            
        Returns:
            工作流详情
            
        Raises:
            FileNotFoundError: 工作流不存在
        """
        file_path = self.workflows_dir / name
        
        if not file_path.exists():
            raise FileNotFoundError(f"工作流不存在: {name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
        
        stat = file_path.stat()
        
        return {
            "name": name,
            "path": str(file_path),
            "size": stat.st_size,
            "size_human": self._format_size(stat.st_size),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "content": workflow,
            "metadata": self._extract_metadata(file_path)
        }
    
    def delete_workflow(self, name: str) -> bool:
        """
        删除工作流
        
        Args:
            name: 工作流文件名
            
        Returns:
            是否成功
            
        Raises:
            FileNotFoundError: 工作流不存在
        """
        file_path = self.workflows_dir / name
        
        if not file_path.exists():
            raise FileNotFoundError(f"工作流不存在: {name}")
        
        file_path.unlink()
        return True
    
    def format_list_output(self, workflows: List[Dict[str, Any]]) -> str:
        """
        格式化工作流列表输出
        
        Args:
            workflows: 工作流列表
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"工作流列表（共 {len(workflows)} 个）")
        lines.append("=" * 80)
        
        if not workflows:
            lines.append("\n没有找到工作流")
            lines.append(f"工作流目录: {self.workflows_dir}")
        else:
            for i, workflow in enumerate(workflows, 1):
                lines.append(f"\n{i}. {workflow['name']}")
                lines.append(f"   类型: {workflow['metadata']['type']}")
                lines.append(f"   节点数: {workflow['metadata']['node_count']}")
                lines.append(f"   大小: {workflow['size_human']}")
                lines.append(f"   修改时间: {workflow['modified']}")
        
        lines.append("\n" + "=" * 80)
        
        return "\n".join(lines)
    
    def format_show_output(self, workflow: Dict[str, Any]) -> str:
        """
        格式化工作流详情输出
        
        Args:
            workflow: 工作流详情
            
        Returns:
            格式化的文本
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"工作流详情: {workflow['name']}")
        lines.append("=" * 80)
        
        lines.append(f"\n文件路径: {workflow['path']}")
        lines.append(f"文件大小: {workflow['size_human']}")
        lines.append(f"修改时间: {workflow['modified']}")
        lines.append(f"工作流类型: {workflow['metadata']['type']}")
        lines.append(f"节点数量: {workflow['metadata']['node_count']}")
        
        lines.append("\n工作流内容:")
        lines.append(json.dumps(workflow['content'], indent=2, ensure_ascii=False))
        
        lines.append("\n" + "=" * 80)
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="ComfyUI 工作流管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python workflow_manager.py --action list
  python workflow_manager.py --action show --name my_workflow.json
  python workflow_manager.py --action delete --name old_workflow.json
        """
    )
    
    parser.add_argument(
        "--action",
        required=True,
        choices=["list", "show", "delete"],
        help="操作类型：list=列出工作流，show=查看详情，delete=删除工作流"
    )
    
    parser.add_argument(
        "--name",
        help="工作流文件名（show 和 delete 操作必需）"
    )
    
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="以 JSON 格式输出"
    )
    
    args = parser.parse_args()
    
    # 创建工作流管理器
    manager = WorkflowManager()
    
    try:
        if args.action == "list":
            workflows = manager.list_workflows()
            
            if args.output_json:
                print(json.dumps(workflows, indent=2, ensure_ascii=False))
            else:
                print(manager.format_list_output(workflows))
                
        elif args.action == "show":
            if not args.name:
                print("错误：show 操作需要 --name 参数")
                sys.exit(1)
            
            workflow = manager.show_workflow(args.name)
            
            if args.output_json:
                print(json.dumps(workflow, indent=2, ensure_ascii=False))
            else:
                print(manager.format_show_output(workflow))
                
        elif args.action == "delete":
            if not args.name:
                print("错误：delete 操作需要 --name 参数")
                sys.exit(1)
            
            manager.delete_workflow(args.name)
            print(f"✓ 已删除工作流: {args.name}")
            
    except FileNotFoundError as e:
        print(f"✗ 错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 操作失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
