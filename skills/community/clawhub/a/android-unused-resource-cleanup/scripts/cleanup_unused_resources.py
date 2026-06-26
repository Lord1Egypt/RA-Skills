#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android 未使用资源清理工具
分析 Git 改动，找出不再使用的资源文件
"""

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set, Tuple


@dataclass
class ResourceRef:
    """资源引用"""
    type: str  # drawable, layout, string, color, dimen, etc.
    name: str
    file_path: str = ""
    
    def __hash__(self):
        return hash((self.type, self.name))
    
    def __eq__(self, other):
        return isinstance(other, ResourceRef) and self.type == other.type and self.name == other.name


class ResourceCleaner:
    """资源清理器"""
    
    # 资源类型映射
    RESOURCE_TYPES = {
        'drawable', 'layout', 'string', 'color', 'dimen', 'style', 'anim', 'animator',
        'mipmap', 'menu', 'raw', 'xml', 'attr', 'bool', 'integer', 'array',
        'font', 'transition', 'interpolator'
    }
    
    # 资源引用模式
    JAVA_KOTLIN_PATTERN = re.compile(r'R\.(\w+)\.(\w+)')
    XML_PATTERN = re.compile(r'@(\w+)/(\w+)')
    XML_TOOLS_PATTERN = re.compile(r'tools:\w+="@(\w+)/(\w+)"')
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.src_dirs = ['src/main/java', 'src/main/kotlin', 'src/main/res']
        
    def get_git_diff(self, commit_range: str = "HEAD~1") -> str:
        """获取 Git diff 内容"""
        try:
            result = subprocess.run(
                ['git', 'diff', commit_range],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.stdout
        except Exception as e:
            print(f"获取 Git diff 失败: {e}")
            return ""
    
    def get_staged_changes(self) -> str:
        """获取已暂存的改动"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.stdout
        except Exception as e:
            print(f"获取暂存改动失败: {e}")
            return ""
    
    def get_unstaged_changes(self) -> str:
        """获取未暂存的改动"""
        try:
            result = subprocess.run(
                ['git', 'diff'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.stdout
        except Exception as e:
            print(f"获取未暂存改动失败: {e}")
            return ""
    
    def parse_resource_refs(self, diff_content: str) -> Tuple[Set[ResourceRef], Set[ResourceRef]]:
        """
        解析 diff 内容，提取资源引用
        返回: (旧资源集合, 新资源集合)
        """
        old_resources = set()
        new_resources = set()
        
        current_file = ""
        
        for line in diff_content.split('\n'):
            # 获取当前文件名
            if line.startswith('diff --git'):
                parts = line.split()
                if len(parts) >= 4:
                    current_file = parts[-1].lstrip('b/')
            
            # 解析删除的行 (- 开头)
            if line.startswith('-') and not line.startswith('---'):
                refs = self._extract_refs(line[1:], current_file)
                old_resources.update(refs)
            
            # 解析新增的行 (+ 开头)
            if line.startswith('+') and not line.startswith('+++'):
                refs = self._extract_refs(line[1:], current_file)
                new_resources.update(refs)
        
        return old_resources, new_resources
    
    def _extract_refs(self, content: str, file_path: str) -> List[ResourceRef]:
        """从内容中提取资源引用"""
        refs = []
        
        # Java/Kotlin 代码: R.type.name
        for match in self.JAVA_KOTLIN_PATTERN.finditer(content):
            res_type, name = match.groups()
            if res_type in self.RESOURCE_TYPES:
                refs.append(ResourceRef(res_type, name, file_path))
        
        # XML 引用: @type/name
        for match in self.XML_PATTERN.finditer(content):
            res_type, name = match.groups()
            if res_type in self.RESOURCE_TYPES:
                refs.append(ResourceRef(res_type, name, file_path))
        
        return refs
    
    def find_resource_usage(self, resource: ResourceRef) -> List[str]:
        """
        在项目中查找资源的使用情况
        返回使用此资源的文件列表
        """
        usages = []
        
        # 构建搜索模式
        java_pattern = f"R.{resource.type}.{resource.name}"
        xml_pattern = f"@{resource.type}/{resource.name}"
        
        # 搜索 Java/Kotlin 文件
        for pattern in ['**/*.java', '**/*.kt']:
            for file_path in self.project_root.rglob(pattern):
                # 跳过生成的文件和测试文件
                if 'build/' in str(file_path) or '/test/' in str(file_path):
                    continue
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if java_pattern in content:
                        usages.append(str(file_path.relative_to(self.project_root)))
                except:
                    pass
        
        # 搜索 XML 文件
        for pattern in ['**/*.xml']:
            for file_path in self.project_root.rglob(pattern):
                if 'build/' in str(file_path):
                    continue
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if xml_pattern in content or java_pattern in content:
                        usages.append(str(file_path.relative_to(self.project_root)))
                except:
                    pass
        
        return usages
    
    def get_resource_files(self, resource: ResourceRef) -> List[Path]:
        """
        获取资源对应的实际文件路径
        """
        files = []
        res_dir = self.project_root / 'src' / 'main' / 'res'
        
        if not res_dir.exists():
            return files
        
        if resource.type in ['drawable', 'mipmap']:
            # 图片资源可能在多个 drawable/mipmap 目录中
            for subdir in res_dir.iterdir():
                if subdir.is_dir() and resource.type in subdir.name:
                    # 查找匹配的文件
                    for ext in ['.xml', '.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif']:
                        file_path = subdir / f"{resource.name}{ext}"
                        if file_path.exists():
                            files.append(file_path)
        
        elif resource.type == 'layout':
            layout_dir = res_dir / 'layout'
            if layout_dir.exists():
                file_path = layout_dir / f"{resource.name}.xml"
                if file_path.exists():
                    files.append(file_path)
        
        elif resource.type == 'raw':
            raw_dir = res_dir / 'raw'
            if raw_dir.exists():
                for file_path in raw_dir.iterdir():
                    if file_path.stem == resource.name:
                        files.append(file_path)
        
        elif resource.type == 'anim':
            for subdir in res_dir.iterdir():
                if subdir.is_dir() and 'anim' in subdir.name:
                    file_path = subdir / f"{resource.name}.xml"
                    if file_path.exists():
                        files.append(file_path)
        
        elif resource.type == 'animator':
            animator_dir = res_dir / 'animator'
            if animator_dir.exists():
                file_path = animator_dir / f"{resource.name}.xml"
                if file_path.exists():
                    files.append(file_path)
        
        elif resource.type == 'font':
            font_dir = res_dir / 'font'
            if font_dir.exists():
                for ext in ['.ttf', '.otf', '.xml']:
                    file_path = font_dir / f"{resource.name}{ext}"
                    if file_path.exists():
                        files.append(file_path)
        
        elif resource.type == 'transition':
            transition_dir = res_dir / 'transition'
            if transition_dir.exists():
                file_path = transition_dir / f"{resource.name}.xml"
                if file_path.exists():
                    files.append(file_path)
        
        elif resource.type == 'xml':
            xml_dir = res_dir / 'xml'
            if xml_dir.exists():
                file_path = xml_dir / f"{resource.name}.xml"
                if file_path.exists():
                    files.append(file_path)
        
        elif resource.type == 'menu':
            menu_dir = res_dir / 'menu'
            if menu_dir.exists():
                file_path = menu_dir / f"{resource.name}.xml"
                if file_path.exists():
                    files.append(file_path)
        
        # values 资源 (string, color, dimen, style, bool, integer, array, attr)
        else:
            for subdir in res_dir.iterdir():
                if subdir.is_dir() and 'values' in subdir.name:
                    for file_path in subdir.glob('*.xml'):
                        try:
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            # 查找资源定义
                            pattern = rf'<{resource.type}[\s>].*?name="{resource.name}"'
                            if re.search(pattern, content):
                                files.append(file_path)
                        except:
                            pass
        
        return files
    
    def analyze(self, diff_source: str = "staged") -> dict:
        """
        分析改动，找出可删除的资源
        
        Args:
            diff_source: "staged" (暂存), "unstaged" (未暂存), "HEAD~1" (最近提交)
        
        Returns:
            分析结果字典
        """
        # 获取 diff 内容
        if diff_source == "staged":
            diff_content = self.get_staged_changes()
        elif diff_source == "unstaged":
            diff_content = self.get_unstaged_changes()
        else:
            diff_content = self.get_git_diff(diff_source)
        
        if not diff_content:
            return {"error": "没有找到改动内容"}
        
        # 解析资源引用
        old_resources, new_resources = self.parse_resource_refs(diff_content)
        
        # 只保留被替换的资源（旧资源不在新资源中）
        replaced_resources = old_resources - new_resources
        
        # 分析每个被替换的资源
        removable = []
        keep = []
        
        for resource in replaced_resources:
            usages = self.find_resource_usage(resource)
            files = self.get_resource_files(resource)
            
            # 过滤掉改动文件本身的使用
            original_file = Path(resource.file_path) if resource.file_path else None
            external_usages = [
                u for u in usages 
                if original_file is None or Path(u).name != original_file.name
            ]
            
            info = {
                "resource": resource,
                "files": files,
                "usages": external_usages,
                "total_usages": len(usages)
            }
            
            if len(usages) <= 1:  # 只在原文件中使用或完全未使用
                removable.append(info)
            else:
                keep.append(info)
        
        return {
            "replaced_resources": list(replaced_resources),
            "removable": removable,
            "keep": keep
        }
    
    def print_report(self, result: dict):
        """打印分析报告"""
        if "error" in result:
            print(f"[ERROR] {result['error']}")
            return
        
        print("=" * 60)
        print("Android 未使用资源分析报告")
        print("=" * 60)
        
        # 可删除的资源
        removable = result.get("removable", [])
        if removable:
            print(f"\n[可删除] 可以安全删除的资源 ({len(removable)} 个):")
            print("-" * 60)
            for info in removable:
                r = info["resource"]
                print(f"\n  [{r.type}] {r.name}")
                if info["files"]:
                    for f in info["files"]:
                        print(f"    [文件] {f.relative_to(self.project_root)}")
                else:
                    print(f"    [警告] 未找到对应的资源文件")
        else:
            print("\n[OK] 没有发现可以安全删除的资源")
        
        # 需要保留的资源
        keep = result.get("keep", [])
        if keep:
            print(f"\n\n[保留] 仍在使用，不能删除的资源 ({len(keep)} 个):")
            print("-" * 60)
            for info in keep:
                r = info["resource"]
                print(f"\n  [{r.type}] {r.name}")
                print(f"    [使用位置] 仍在以下位置使用:")
                for usage in info["usages"][:5]:  # 最多显示5个
                    print(f"       - {usage}")
                if len(info["usages"]) > 5:
                    print(f"       ... 还有 {len(info['usages']) - 5} 处")
        
        print("\n" + "=" * 60)
        
        # 提供删除命令建议
        if removable:
            print("\n[删除建议]:")
            for info in removable:
                for f in info["files"]:
                    print(f"   del \"{f}\"")


def main():
    parser = argparse.ArgumentParser(
        description='Android 未使用资源清理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 分析暂存的改动
  python cleanup_unused_resources.py --source staged
  
  # 分析未暂存的改动
  python cleanup_unused_resources.py --source unstaged
  
  # 分析最近的一次提交
  python cleanup_unused_resources.py --source HEAD~1
  
  # 指定项目根目录
  python cleanup_unused_resources.py --project /path/to/project
        """
    )
    parser.add_argument(
        '--source', '-s',
        choices=['staged', 'unstaged', 'HEAD~1', 'HEAD~2', 'HEAD~3'],
        default='staged',
        help='要分析的改动来源 (默认: staged)'
    )
    parser.add_argument(
        '--project', '-p',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    
    args = parser.parse_args()
    
    cleaner = ResourceCleaner(args.project)
    result = cleaner.analyze(args.source)
    cleaner.print_report(result)


if __name__ == '__main__':
    main()
