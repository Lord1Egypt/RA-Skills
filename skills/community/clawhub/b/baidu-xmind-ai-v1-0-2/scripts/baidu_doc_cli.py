#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度智能文档分析平台 - 命令行工具
"""

import os
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from baidu_api_client import BaiduDocAIClient


def load_file_as_base64(file_path: str) -> tuple:
    """加载文件并转换为base64"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    file_data = BaiduDocAIClient.file_to_base64(file_path)
    file_name = path.name
    
    return file_data, file_name


def parse_json_arg(json_str: str):
    """解析JSON字符串"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON解析失败: {e}")


def print_result(result, output_file=None):
    """打印结果"""
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {output_file}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


# ==================== 文档抽取 ====================

def cmd_extract(args):
    """文档抽取命令"""
    client = BaiduDocAIClient(args.api_key, args.secret_key)
    
    if args.file:
        file_data, file_name = load_file_as_base64(args.file)
        file_url = None
    elif args.file_url:
        file_data = None
        file_url = args.file_url
        file_name = None
    else:
        raise ValueError("必须提供 --file 或 --file-url")
    
    manifest = None
    if args.fields:
        manifest = parse_json_arg(args.fields)
    
    print("正在执行文档抽取...")
    result = client.extract(
        file_url=file_url,
        file_data=file_data,
        manifest=manifest,
        manifest_version_id=args.manifest_version_id,
        remove_duplicates=args.remove_duplicates,
        page_range=args.page_range,
        extract_seal=args.extract_seal,
        erase_watermark=args.erase_watermark,
        doc_correct=args.doc_correct
    )
    
    print_result(result, args.output)


# ==================== 文档解析 ====================

def cmd_parse(args):
    """文档解析命令"""
    client = BaiduDocAIClient(args.api_key, args.secret_key)
    
    if args.file:
        file_data, file_name = load_file_as_base64(args.file)
    elif args.file_url:
        file_data = None
        if not args.file_name:
            raise ValueError("使用 --file-url 时必须指定 --file-name")
        file_name = args.file_name
    else:
        raise ValueError("必须提供 --file 或 --file-url")
    
    return_doc_chunks = None
    if args.return_doc_chunks:
        return_doc_chunks = {
            "switch": True,
            "split_type": args.split_type,
            "chunk_size": args.chunk_size if args.chunk_size != -1 else -1
        }
        if args.separators:
            return_doc_chunks["separators"] = list(args.separators)
    
    print("正在执行文档解析...")
    result = client.parse(
        file_url=args.file_url,
        file_data=file_data,
        file_name=file_name,
        recognize_formula=args.recognize_formula,
        analysis_chart=args.analysis_chart,
        angle_adjust=args.angle_adjust,
        parse_image_layout=args.parse_image_layout,
        language_type=args.language_type,
        switch_digital_width=args.switch_digital_width,
        return_doc_chunks=return_doc_chunks
    )
    
    print_result(result, args.output)


# ==================== 文档解析 VL ====================

def cmd_parse_vl(args):
    """文档解析VL命令"""
    client = BaiduDocAIClient(args.api_key, args.secret_key)
    
    if args.file:
        file_data, file_name = load_file_as_base64(args.file)
    elif args.file_url:
        file_data = None
        file_name = args.file_name
    else:
        raise ValueError("必须提供 --file 或 --file-url")
    
    print("正在执行文档解析VL...")
    result = client.parse_vl(
        file_url=args.file_url,
        file_data=file_data,
        file_name=file_name,
        analysis_chart=args.analysis_chart,
        merge_tables=args.merge_tables,
        relevel_titles=args.relevel_titles,
        recognize_seal=args.recognize_seal,
        return_span_boxes=args.return_span_boxes
    )
    
    print_result(result, args.output)


# ==================== 文档比对 ====================

def cmd_compare(args):
    """文档比对命令"""
    client = BaiduDocAIClient(args.api_key, args.secret_key)
    
    if args.base_file:
        base_file_data, _ = load_file_as_base64(args.base_file)
    elif args.base_file_url:
        base_file_data = None
    else:
        raise ValueError("必须提供 --base-file 或 --base-file-url")
    
    if args.compare_file:
        compare_file_data, _ = load_file_as_base64(args.compare_file)
    elif args.compare_file_url:
        compare_file_data = None
    else:
        raise ValueError("必须提供 --compare-file 或 --compare-file-url")
    
    print("正在执行文档比对...")
    result = client.compare(
        base_file_url=args.base_file_url,
        base_file_data=base_file_data,
        compare_file_url=args.compare_file_url,
        compare_file_data=compare_file_data,
        seal_recognition=args.seal_recognition,
        hand_writing_recognition=args.hand_writing_recognition,
        font_family_recognition=args.font_family_recognition,
        font_size_recognition=args.font_size_recognition,
        full_width_half_width_recognition=args.full_width_half_width_recognition
    )
    
    print_result(result, args.output)


# ==================== 合同审查 ====================

def cmd_contract_review(args):
    """合同审查命令"""
    client = BaiduDocAIClient(args.api_key, args.secret_key)
    
    if args.file:
        file_data, file_name = load_file_as_base64(args.file)
    elif args.file_url:
        file_data = None
        file_name = None
    else:
        raise ValueError("必须提供 --file 或 --file-url")
    
    print("正在执行合同审查...")
    result = client.contract_review(
        file_url=args.file_url,
        file_data=file_data,
        file_name=file_name,
        template_name=args.template,
        comment_risk_level=args.risk_level
    )
    
    print_result(result, args.output)


# ==================== 文档格式转换 ====================

def cmd_convert(args):
    """文档格式转换命令"""
    client = BaiduDocAIClient(args.api_key, args.secret_key)
    
    if args.file:
        file_data, file_name = load_file_as_base64(args.file)
    elif args.file_url:
        file_data = None
        file_name = None
    else:
        raise ValueError("必须提供 --file 或 --file-url")
    
    print("正在执行文档格式转换...")
    result = client.convert(
        file_url=args.file_url,
        file_data=file_data,
        file_name=file_name
    )
    
    print_result(result, args.output)


# ==================== 主程序 ====================

def main():
    parser = argparse.ArgumentParser(
        description="百度智能文档分析平台 - 命令行工具"
    )
    parser.add_argument("--api-key", help="API Key（默认从环境变量读取）")
    parser.add_argument("--secret-key", help="Secret Key（默认从环境变量读取）")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 文档抽取
    extract_parser = subparsers.add_parser("extract", help="文档抽取")
    extract_group = extract_parser.add_mutually_exclusive_group(required=True)
    extract_group.add_argument("--file", help="本地文件路径")
    extract_group.add_argument("--file-url", help="文件URL")
    extract_parser.add_argument("--fields", help="抽取字段JSON")
    extract_parser.add_argument("--manifest-version-id", help="清单版本ID")
    extract_parser.add_argument("--remove-duplicates", action="store_true", help="去重")
    extract_parser.add_argument("--page-range", help="页码范围")
    extract_parser.add_argument("--extract-seal", action="store_true", help="抽取印章")
    extract_parser.add_argument("--erase-watermark", action="store_true", help="去除水印")
    extract_parser.add_argument("--doc-correct", action="store_true", help="图像矫正")
    extract_parser.add_argument("--output", help="输出文件")
    extract_parser.set_defaults(func=cmd_extract)
    
    # 文档解析
    parse_parser = subparsers.add_parser("parse", help="文档解析")
    parse_group = parse_parser.add_mutually_exclusive_group(required=True)
    parse_group.add_argument("--file", help="本地文件路径")
    parse_group.add_argument("--file-url", help="文件URL")
    parse_parser.add_argument("--file-name", help="文件名")
    parse_parser.add_argument("--recognize-formula", action="store_true", help="公式识别")
    parse_parser.add_argument("--analysis-chart", action="store_true", help="图表解析")
    parse_parser.add_argument("--angle-adjust", action="store_true", help="图片矫正")
    parse_parser.add_argument("--parse-image-layout", action="store_true", help="返回图片位置")
    parse_parser.add_argument("--language-type", default="CHN_ENG", help="识别语种")
    parse_parser.add_argument("--switch-digital-width", choices=["auto", "half", "full"], default="auto")
    parse_parser.add_argument("--return-doc-chunks", action="store_true", help="文档切分")
    parse_parser.add_argument("--split-type", choices=["chunk", "mark"], default="chunk")
    parse_parser.add_argument("--chunk-size", type=int, default=-1)
    parse_parser.add_argument("--separators", help="切分标点")
    parse_parser.add_argument("--output", help="输出文件")
    parse_parser.set_defaults(func=cmd_parse)
    
    # 文档解析VL
    parse_vl_parser = subparsers.add_parser("parse-vl", help="文档解析VL")
    parse_vl_group = parse_vl_parser.add_mutually_exclusive_group(required=True)
    parse_vl_group.add_argument("--file", help="本地文件路径")
    parse_vl_group.add_argument("--file-url", help="文件URL")
    parse_vl_parser.add_argument("--file-name", help="文件名")
    parse_vl_parser.add_argument("--analysis-chart", action="store_true", help="图表解析")
    parse_vl_parser.add_argument("--merge-tables", action="store_true", help="合并表格")
    parse_vl_parser.add_argument("--relevel-titles", action="store_true", help="标题分级")
    parse_vl_parser.add_argument("--recognize-seal", action="store_true", help="识别印章")
    parse_vl_parser.add_argument("--return-span-boxes", action="store_true", help="返回坐标")
    parse_vl_parser.add_argument("--output", help="输出文件")
    parse_vl_parser.set_defaults(func=cmd_parse_vl)
    
    # 文档比对
    compare_parser = subparsers.add_parser("compare", help="文档比对")
    compare_parser.add_argument("--base-file", help="主版文件")
    compare_parser.add_argument("--base-file-url", help="主版URL")
    compare_parser.add_argument("--compare-file", help="副版文件")
    compare_parser.add_argument("--compare-file-url", help="副版URL")
    compare_parser.add_argument("--seal-recognition", action="store_true", help="印章识别")
    compare_parser.add_argument("--hand-writing-recognition", action="store_true", help="手写识别")
    compare_parser.add_argument("--font-family-recognition", action="store_true", help="字体识别")
    compare_parser.add_argument("--font-size-recognition", action="store_true", help="字号识别")
    compare_parser.add_argument("--full-width-half-width-recognition", action="store_true", help="全半角识别")
    compare_parser.add_argument("--output", help="输出文件")
    compare_parser.set_defaults(func=cmd_compare)
    
    # 合同审查
    contract_parser = subparsers.add_parser("contract-review", help="合同审查")
    contract_group = contract_parser.add_mutually_exclusive_group(required=True)
    contract_group.add_argument("--file", help="合同文件")
    contract_group.add_argument("--file-url", help="合同URL")
    contract_parser.add_argument("--template", required=True, help="合同模板")
    contract_parser.add_argument("--risk-level", choices=["major", "normal", "all"], help="风险等级")
    contract_parser.add_argument("--output", help="输出文件")
    contract_parser.set_defaults(func=cmd_contract_review)
    
    # 格式转换
    convert_parser = subparsers.add_parser("convert", help="格式转换")
    convert_group = convert_parser.add_mutually_exclusive_group(required=True)
    convert_group.add_argument("--file", help="源文件")
    convert_group.add_argument("--file-url", help="源文件URL")
    convert_parser.add_argument("--output", help="输出文件")
    convert_parser.set_defaults(func=cmd_convert)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
