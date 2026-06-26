#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: subprocess calls are limited to local Browser and Python.

#!/usr/bin/env python3
"""
Doc-to-PPT - 统一入口

用法：
    python main.py input.pdf --slides 10 --output ./output
    python main.py input.md --output ./output
    python main.py input.docx --output ./output
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# 添加当前目录到路径
CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))

# 原版模块
try:
    from read_content import smart_read as smart_extract
    HAS_EXTRACT = True
except ImportError:
    HAS_EXTRACT = False

try:
    from workflow import run_workflow
    HAS_WORKFLOW = True
except ImportError:
    HAS_WORKFLOW = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def convert_to_ppt(
    input_files: List[str],
    output_dir: str = None,
    slides_count: int = None,
    user_query: str = "",
    style: str = "default",
    **kwargs
) -> Dict[str, Any]:
    """
    主转换函数
    
    Args:
        input_files: 输入文件列表
        output_dir: 输出目录
        slides_count: 目标幻灯片数量
        user_query: 用户查询（可选）
        style: 样式名称
    
    Returns:
        转换结果
    """
    if not input_files:
        return {"success": False, "error": "No input files provided"}
    
    output_dir = output_dir or f"./output_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 提取内容
    all_content = []
    for input_file in input_files:
        if not os.path.exists(input_file):
            logger.warning(f"File not found: {input_file}")
            continue
        
        if HAS_EXTRACT:
            result = smart_extract(input_file)
            if result.get("success"):
                all_content.append(result.get("text", ""))
        else:
            with open(input_file, 'r', encoding='utf-8') as f:
                all_content.append(f.read())
    
    if not all_content:
        return {"success": False, "error": "No content extracted"}
    
    # 生成 PPT
    if HAS_WORKFLOW:
        result = run_workflow(
            content="\n\n".join(all_content),
            output_dir=output_dir,
            slides_count=slides_count or 10,
            style=style
        )
        return result
    
    return {"success": True, "output_dir": output_dir, "message": "Content extracted, PPT generation requires workflow module"}


def main():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert documents to PowerPoint')
    parser.add_argument('inputs', nargs='+', help='Input files (PDF, DOCX, MD)')
    parser.add_argument('--output', '-o', default=None, help='Output directory')
    parser.add_argument('--slides', '-s', type=int, default=10, help='Number of slides')
    parser.add_argument('--query', '-q', default='', help='Query for content parsing')
    parser.add_argument('--style', default='default', help='Style name')
    
    args = parser.parse_args()
    
    result = asyncio.run(convert_to_ppt(
        input_files=args.inputs,
        output_dir=args.output,
        slides_count=args.slides,
        user_query=args.query,
        style=args.style
    ))
    
    if result.get("success"):
        print(f"✅ Success: {result.get('output_dir')}")
    else:
        print(f"❌ Error: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
