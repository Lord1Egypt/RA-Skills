#!/usr/bin/env python3
"""
评估要点对比脚本

功能：
1. 读取产品对应的标准单产品硬件资源测算文件
2. 提取所需的评估要点
3. 对比提供的评估要点与所需评估要点
4. 返回对比结果
"""

import os
import re
import sys
import json
from pathlib import Path


def find_product_file(product_name: str, kb_dir: str) -> str:
    """
    根据产品名称查找对应的标准单产品硬件资源测算文件
    
    Args:
        product_name: 产品名称（如：病历质控系统、CDSS 系统等）
        kb_dir: 知识库目录路径
    
    Returns:
        文件路径，如果未找到返回 None
    """
    # 遍历 kb 目录下的所有子目录
    kb_path = Path(kb_dir)
    if not kb_path.exists():
        return None
    
    # 查找包含产品名称的目录
    for subdir in kb_path.iterdir():
        if subdir.is_dir() and product_name in subdir.name:
            # 在该目录下查找标准单产品硬件资源测算文件
            for file in subdir.glob("*标准单产品硬件资源测算.md"):
                return str(file)
    
    return None


def extract_required_elements(file_path: str) -> list:
    """
    从文件中提取所需的评估要点
    
    Args:
        file_path: 文件路径
    
    Returns:
        评估要点列表
    """
    required_elements = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取"服务器资源评估输入项"部分的内容
        match = re.search(r'## 服务器资源评估输入项\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if match:
            section = match.group(1)
            # 提取编号列表项
            items = re.findall(r'^\d+\.\s*(.+?)$', section, re.MULTILINE)
            required_elements.extend(items)
        
        # 清理空白字符
        required_elements = [item.strip() for item in required_elements if item.strip()]
        
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return []
    
    return required_elements


def compare_elements(required: list, provided: list) -> dict:
    """
    对比所需评估要点和已提供的评估要点
    
    Args:
        required: 所需评估要点列表
        provided: 已提供评估要点列表
    
    Returns:
        对比结果字典
    """
    # 标准化处理（去除空格、统一大小写等）
    required_normalized = [item.strip().lower() for item in required]
    provided_normalized = [item.strip().lower() for item in provided]
    
    missing_elements = []
    satisfied_elements = []
    
    for req in required:
        req_norm = req.strip().lower()
        found = False
        for prov in provided:
            prov_norm = prov.strip().lower()
            # 检查是否匹配（支持部分匹配）
            if req_norm in prov_norm or prov_norm in req_norm:
                found = True
                break
        
        if found:
            satisfied_elements.append(req)
        else:
            missing_elements.append(req)
    
    return {
        "satisfied": satisfied_elements,
        "missing": missing_elements,
        "is_complete": len(missing_elements) == 0
    }


def main():
    """
    主函数
    
    输入格式（JSON）:
    {
        "product": "产品名称",
        "provided_elements": ["已提供的评估要点 1", "已提供的评估要点 2", ...],
        "kb_dir": "知识库目录路径（可选，默认为 workspace/kb）"
    }
    
    输出格式（JSON）:
    {
        "status": "ok" | "missing",
        "message": "ok" 或 缺少的评估要点信息,
        "details": {
            "satisfied": [...],
            "missing": [...],
            "is_complete": true/false
        }
    }
    """
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Please provide input JSON as argument"
        }, ensure_ascii=False))
        sys.exit(1)
    
    try:
        input_data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": f"Invalid JSON input: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)
    
    product = input_data.get("product", "")
    provided_elements = input_data.get("provided_elements", [])
    kb_dir = input_data.get("kb_dir", "/Users/hushuai/.openclaw/workspace-ClinicalManager/kb")
    
    if not product:
        print(json.dumps({
            "error": "Product name is required"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 查找产品文件
    file_path = find_product_file(product, kb_dir)
    if not file_path:
        print(json.dumps({
            "error": f"Could not find resource file for product: {product}"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 提取所需评估要点
    required_elements = extract_required_elements(file_path)
    if not required_elements:
        print(json.dumps({
            "error": f"No required elements found in file: {file_path}"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 对比评估要点
    result = compare_elements(required_elements, provided_elements)
    
    # 输出结果
    if result["is_complete"]:
        output = {
            "status": "ok",
            "message": "ok",
            "details": result
        }
    else:
        missing_str = "、".join(result["missing"])
        output = {
            "status": "missing",
            "message": f"缺少的评估要点：{missing_str}",
            "details": result
        }
    
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
