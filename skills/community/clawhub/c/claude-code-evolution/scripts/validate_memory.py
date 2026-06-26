#!/usr/bin/env python3
"""
记忆文件校验脚本
基于Claude Code记忆系统的闭合四类型设计

使用方法:
  python validate_memory.py memory/user-profile.md      # 校验单个文件
  python validate_memory.py memory/*.md                # 校验所有文件
  python validate_memory.py --generate-index           # 生成索引文件
"""

import re
import sys
import os
import yaml
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 配置
ALLOWED_TYPES = {"user", "feedback", "project", "reference"}
MAX_DESCRIPTION_LENGTH = 150
REQUIRED_FIELDS = ["name", "description", "type"]

# 排除模式（不应保存为记忆的内容）
EXCLUDED_PATTERNS = [
    r"文件结构如下：",
    r"代码目录：",
    r"git (log|blame|diff|status)",
    r"commit [a-f0-9]{7,}",
    r"调试步骤：",
    r"临时文件：",
    r"进程ID：\d+",
    r"API端点列表：",
    r"package\.json内容：",
    r"数据库表结构：",
    r"表结构：",
    r"字段列表：",
    r"函数定义：",
    r"类定义：",
    r"接口定义：",
    r"配置项列表：",
    r"环境变量：",
    r"依赖包列表：",
]

class MemoryValidator:
    """记忆文件校验器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "by_type": {t: 0 for t in ALLOWED_TYPES}
        }
    
    def validate_type(self, memory_type: str) -> bool:
        """验证类型是否在允许范围内"""
        return memory_type in ALLOWED_TYPES
    
    def should_exclude(self, content: str) -> Tuple[bool, Optional[str]]:
        """检查内容是否应被排除"""
        for pattern in EXCLUDED_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return True, f"匹配排除模式: {pattern}"
        return False, None
    
    def parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], Optional[str]]:
        """解析Frontmatter，返回(元数据, 错误信息)"""
        lines = content.splitlines()
        
        if not lines or lines[0] != "---":
            return None, "缺少Frontmatter起始标记 '---'"
        
        # 查找Frontmatter结束标记
        try:
            end_index = lines.index("---", 1)
        except ValueError:
            return None, "缺少Frontmatter结束标记 '---'"
        
        frontmatter_lines = lines[1:end_index]
        frontmatter_text = "\n".join(frontmatter_lines)
        
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return None, "Frontmatter格式错误，应为YAML字典"
            return frontmatter, None
        except yaml.YAMLError as e:
            return None, f"YAML解析错误: {str(e)}"
    
    def validate_frontmatter(self, frontmatter: Dict) -> List[str]:
        """验证Frontmatter完整性"""
        errors = []
        
        # 检查必需字段
        for field in REQUIRED_FIELDS:
            if field not in frontmatter:
                errors.append(f"缺少必需字段: {field}")
            elif not frontmatter[field]:
                errors.append(f"字段为空: {field}")
        
        # 验证类型
        if "type" in frontmatter:
            if not self.validate_type(frontmatter["type"]):
                errors.append(f"无效的类型: {frontmatter['type']} (允许的类型: {', '.join(ALLOWED_TYPES)})")
            else:
                self.stats["by_type"][frontmatter["type"]] += 1
        
        # 验证描述长度
        if "description" in frontmatter:
            desc = frontmatter["description"]
            if len(desc) > MAX_DESCRIPTION_LENGTH:
                errors.append(f"描述过长: {len(desc)}字符 (最大{MAX_DESCRIPTION_LENGTH})")
        
        # 检查日期格式
        date_fields = ["created", "updated", "expires"]
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        
        for field in date_fields:
            if field in frontmatter and frontmatter[field]:
                if not re.match(date_pattern, frontmatter[field]):
                    errors.append(f"日期格式错误: {field}应为YYYY-MM-DD格式")
        
        return errors
    
    def validate_file(self, filepath: str) -> bool:
        """验证单个记忆文件"""
        self.stats["total"] += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"无法读取文件 {filepath}: {str(e)}")
            self.stats["invalid"] += 1
            return False
        
        # 解析Frontmatter
        frontmatter, parse_error = self.parse_frontmatter(content)
        if parse_error:
            self.errors.append(f"{filepath}: {parse_error}")
            self.stats["invalid"] += 1
            return False
        
        # 验证Frontmatter
        frontmatter_errors = self.validate_frontmatter(frontmatter)
        if frontmatter_errors:
            for error in frontmatter_errors:
                self.errors.append(f"{filepath}: {error}")
            self.stats["invalid"] += 1
            return False
        
        # 检查内容是否应被排除
        # 获取Frontmatter之后的内容
        lines = content.splitlines()
        end_index = lines.index("---", 1) if "---" in lines[1:] else 0
        main_content = "\n".join(lines[end_index + 1:]) if end_index > 0 else content
        
        excluded, reason = self.should_exclude(main_content)
        if excluded:
            self.warnings.append(f"{filepath}: {reason}")
            # 这只是一个警告，不标记为无效
        
        self.stats["valid"] += 1
        return True
    
    def generate_index(self, memory_dir: str) -> str:
        """生成MEMORY.md索引文件"""
        memory_files = []
        
        for filepath in glob.glob(os.path.join(memory_dir, "*.md")):
            if os.path.basename(filepath) == "MEMORY.md":
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                frontmatter, _ = self.parse_frontmatter(content)
                if frontmatter and "name" in frontmatter and "type" in frontmatter:
                    memory_files.append({
                        "path": os.path.basename(filepath),
                        "name": frontmatter["name"],
                        "type": frontmatter["type"],
                        "description": frontmatter.get("description", ""),
                        "updated": frontmatter.get("updated", ""),
                    })
            except:
                continue
        
        # 按类型和更新日期排序
        memory_files.sort(key=lambda x: (x["type"], x["updated"]), reverse=True)
        
        # 生成索引内容
        lines = []
        lines.append("# MEMORY.md — 记忆索引")
        lines.append("")
        lines.append("**注意**: 这是基于Claude Code记忆系统生成的索引文件，最多200行/25KB")
        lines.append("")
        
        current_type = None
        for mem in memory_files:
            if mem["type"] != current_type:
                current_type = mem["type"]
                lines.append(f"## {current_type}类型记忆")
                lines.append("")
            
            # 索引条目格式: - [名称](文件.md) -- 一行描述
            desc = mem["description"][:100] + "..." if len(mem["description"]) > 100 else mem["description"]
            line = f"- [{mem['name']}]({mem['path']}) -- {desc}"
            
            # 确保单行不超过150字符（Claude Code限制）
            if len(line) > 150:
                line = line[:147] + "..."
            
            lines.append(line)
        
        # 添加统计信息
        lines.append("")
        lines.append("## 统计信息")
        lines.append(f"- 总记忆文件: {len(memory_files)}")
        for type_name in ALLOWED_TYPES:
            count = sum(1 for m in memory_files if m["type"] == type_name)
            lines.append(f"- {type_name}: {count}")
        
        # 容量警告（模拟Claude Code的双重截断）
        content = "\n".join(lines)
        if len(lines) > 200:
            content = "\n".join(lines[:200])
            content += "\n\n<!-- 索引截断：达到200行限制 -->"
        
        if len(content.encode('utf-8')) > 25 * 1024:  # 25KB
            # 简单截断，实际应该更智能
            content = content[:25*1024]
            last_newline = content.rfind("\n")
            if last_newline != -1:
                content = content[:last_newline]
            content += "\n\n<!-- 索引截断：达到25KB限制 -->"
        
        return content
    
    def print_report(self):
        """打印校验报告"""
        print("=" * 60)
        print("记忆文件校验报告")
        print("=" * 60)
        
        print(f"\n统计信息:")
        print(f"  总文件数: {self.stats['total']}")
        print(f"  有效文件: {self.stats['valid']}")
        print(f"  无效文件: {self.stats['invalid']}")
        
        if self.stats['by_type']:
            print(f"\n按类型分布:")
            for type_name, count in self.stats['by_type'].items():
                if count > 0:
                    print(f"  {type_name}: {count}")
        
        if self.errors:
            print(f"\n错误 ({len(self.errors)}个):")
            for error in self.errors[:10]:  # 只显示前10个错误
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... 还有{len(self.errors)-10}个错误未显示")
        
        if self.warnings:
            print(f"\n警告 ({len(self.warnings)}个):")
            for warning in self.warnings[:5]:  # 只显示前5个警告
                print(f"  - {warning}")
            if len(self.warnings) > 5:
                print(f"  ... 还有{len(self.warnings)-5}个警告未显示")
        
        print("\n" + "=" * 60)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="记忆文件校验工具")
    parser.add_argument("files", nargs="*", help="要校验的文件（支持通配符）")
    parser.add_argument("--generate-index", action="store_true", 
                       help="生成MEMORY.md索引文件")
    parser.add_argument("--memory-dir", default="memory",
                       help="记忆目录路径（默认: memory）")
    
    args = parser.parse_args()
    
    validator = MemoryValidator()
    
    if args.generate_index:
        # 生成索引文件
        index_content = validator.generate_index(args.memory_dir)
        
        index_path = os.path.join(args.memory_dir, "MEMORY.md")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"索引文件已生成: {index_path}")
        print(f"内容大小: {len(index_content)}字符, {len(index_content.encode('utf-8'))}字节")
        return 0
    
    # 收集要校验的文件
    files_to_validate = []
    if args.files:
        for pattern in args.files:
            matched = glob.glob(pattern)
            if matched:
                files_to_validate.extend(matched)
            else:
                # 如果没有匹配到，尝试直接使用（可能是具体文件）
                if os.path.exists(pattern):
                    files_to_validate.append(pattern)
                else:
                    print(f"警告: 文件不存在: {pattern}")
    else:
        # 默认校验memory目录下所有.md文件
        memory_dir = args.memory_dir
        if os.path.exists(memory_dir):
            files_to_validate = glob.glob(os.path.join(memory_dir, "*.md"))
        else:
            print(f"错误: 记忆目录不存在: {memory_dir}")
            return 1
    
    if not files_to_validate:
        print("错误: 没有找到要校验的文件")
        return 1
    
    # 校验文件
    print(f"开始校验 {len(files_to_validate)} 个文件...")
    
    for filepath in files_to_validate:
        if os.path.basename(filepath) == "MEMORY.md":
            continue  # 跳过索引文件
        
        print(f"  校验: {os.path.basename(filepath)}", end="")
        if validator.validate_file(filepath):
            print(" ✓")
        else:
            print(" ✗")
    
    # 打印报告
    validator.print_report()
    
    # 返回退出码
    return 1 if validator.errors else 0

if __name__ == "__main__":
    sys.exit(main())