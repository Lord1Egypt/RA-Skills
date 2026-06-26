"""
Frontmatter 解析工具

简单 YAML 解析，无需额外依赖。
"""

from typing import Dict


def parse_frontmatter(content: str) -> Dict:
    """
    解析 YAML frontmatter
    
    格式:
    ---
    type: decision
    description: 技术栈选择
    created_at: 2026-04-01
    ---
    
    参数:
        content: 文件内容
        
    返回:
        字典格式的元数据
    """
    if not content.startswith("---"):
        return {}
    
    try:
        # 查找结束标记
        end = content.index("---", 3)
        yaml_content = content[4:end].strip()
        
        # 简单 YAML 解析（无需额外依赖）
        result = {}
        for line in yaml_content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                # 去除引号
                value = value.strip('"').strip("'")
                result[key] = value
        
        return result
    except (ValueError, IndexError):
        return {}


def extract_frontmatter_and_body(content: str) -> tuple:
    """
    提取 frontmatter 和正文
    
    返回:
        (frontmatter_dict, body_string)
    """
    if not content.startswith("---"):
        return {}, content
    
    try:
        end = content.index("---", 3)
        frontmatter = parse_frontmatter(content)
        body = content[end + 3:].strip()
        return frontmatter, body
    except (ValueError, IndexError):
        return {}, content
