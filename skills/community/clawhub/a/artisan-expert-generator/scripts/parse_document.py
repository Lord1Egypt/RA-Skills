#!/usr/bin/env python3
"""
用户私有知识解析脚本
解析PDF/Word/Markdown文件，提取内容并分类维度
"""

import argparse
import json
import sys
from pathlib import Path


def parse_pdf(file_path):
    """解析PDF文件"""
    try:
        import pypdf
        with open(file_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        raise Exception("pypdf库未安装，无法解析PDF文件")
    except Exception as e:
        raise Exception(f"PDF解析失败: {str(e)}")


def parse_word(file_path):
    """解析Word文件"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except ImportError:
        raise Exception("python-docx库未安装，无法解析Word文件")
    except Exception as e:
        raise Exception(f"Word解析失败: {str(e)}")


def parse_markdown(file_path):
    """解析Markdown文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Markdown解析失败: {str(e)}")


def classify_dimension(text):
    """根据关键词判断内容归属的采集维度"""
    text_lower = text.lower()

    # 维度关键词映射
    dimension_keywords = {
        "学科基础": ["概念", "理论", "定义", "原理", "基础", "概述", "体系", "框架"],
        "法规规范": ["法规", "法律", "规范", "标准", "条例", "规定", "政策", "合规"],
        "方法论": ["方法", "流程", "步骤", "分析", "评估", "判断", "决策", "策略"],
        "典型案例": ["案例", "实例", "例子", "实际", "应用", "场景", "情况", "问题"],
        "行业实践": ["实践", "经验", "技巧", "惯例", "做法", "注意", "要点", "建议"],
        "表达规范": ["术语", "格式", "规范", "标准", "要求", "模板", "样式", "表达"]
    }

    # 统计各维度关键词出现次数
    dimension_scores = {}
    for dimension, keywords in dimension_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        dimension_scores[dimension] = score

    # 返回得分最高的维度
    if max(dimension_scores.values()) == 0:
        return "未分类"

    return max(dimension_scores, key=dimension_scores.get)


def extract_key_points(text):
    """提取关键点（简单实现：按句号分句，过滤短句）"""
    sentences = [s.strip() for s in text.split('。') if s.strip()]
    key_points = [s for s in sentences if len(s) > 10][:20]  # 最多20个关键点
    return key_points


def main():
    parser = argparse.ArgumentParser(description='解析用户私有知识文件')
    parser.add_argument('--file_path', required=True, help='文件路径')

    args = parser.parse_args()

    try:
        file_path = Path(args.file_path)

        if not file_path.exists():
            raise Exception(f"文件不存在: {args.file_path}")

        # 识别文件类型并解析
        file_ext = file_path.suffix.lower()
        if file_ext == '.pdf':
            file_type = 'PDF'
            content = parse_pdf(file_path)
        elif file_ext in ['.doc', '.docx']:
            file_type = 'Word'
            content = parse_word(file_path)
        elif file_ext in ['.md', '.markdown', '.txt']:
            file_type = 'Markdown'
            content = parse_markdown(file_path)
        else:
            raise Exception(f"不支持的文件类型: {file_ext}")

        # 提取关键点
        key_points = extract_key_points(content)

        # 分类维度
        dimension_category = classify_dimension(content)

        # 统计信息
        char_count = len(content)
        line_count = len(content.split('\n'))

        result = {
            "status": "success",
            "file_type": file_type,
            "file_path": str(file_path.absolute()),
            "content_summary": {
                "char_count": char_count,
                "line_count": line_count
            },
            "extracted_content": content[:2000] + "..." if len(content) > 2000 else content,
            "dimension_category": dimension_category,
            "key_points": key_points[:10],
            "suggestions": f"该文件主要属于'{dimension_category}'维度，建议在对应采集阶段使用"
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        result = {
            "status": "error",
            "message": str(e)
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
