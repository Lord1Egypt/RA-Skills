#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc-extract-filter - 文件处理技能封装脚本

支持 PDF、Word、Excel 文件的文本提取和关键词筛选
适配 OpenClaw 和 CoPaw 智能体调用规范
"""

import os
import sys
import json
import logging
import click
from pathlib import Path
from tqdm import tqdm

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.extractor import FileExtractor
from core.filter import ContentFilter

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DocExtractFilter:
    """
    文件处理技能类
    """
    
    @staticmethod
    def process(file_path, action, keywords=None, regex_pattern=None, enable_ocr=False, 
               exclude_keywords=None, exclude_regex=None, context_length=50, filter_level="line"):
        """
        处理文件操作
        
        Args:
            file_path: 文件路径
            action: 操作类型，extract 或 filter
            keywords: 关键词列表，仅 filter 操作需要
            regex_pattern: 正则表达式模式，仅 filter 操作需要
            enable_ocr: 是否启用 OCR 支持（用于扫描件 PDF）
            exclude_keywords: 排除关键词列表
            exclude_regex: 排除正则表达式模式
            context_length: 上下文长度（默认50字符）
            filter_level: 筛选级别，line（按行）或 paragraph（按段落）
            
        Returns:
            结构化 JSON 格式的结果
        """
        try:
            # 验证文件路径
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    "success": False,
                    "data": {},
                    "error": f"文件不存在: {file_path}"
                }
            
            # 初始化提取器和筛选器
            extractor = FileExtractor()
            filter = ContentFilter()
            
            # 提取文本
            extract_result = extractor.extract_text(file_path, enable_ocr)
            
            if "error" in extract_result:
                return {
                    "success": False,
                    "data": {},
                    "error": extract_result["error"]
                }
            
            text = extract_result.get("text", "")
            
            # 根据操作类型处理
            if action == "extract":
                return {
                    "success": True,
                    "data": {
                        "text": text
                    },
                    "error": ""
                }
            elif action == "filter":
                if not keywords and not regex_pattern:
                    return {
                        "success": False,
                        "data": {},
                        "error": "filter 操作需要提供关键词或正则表达式"
                    }
                
                # 筛选关键词或正则表达式
                if keywords:
                    filter_result = filter.filter_by_keyword(text, keywords, 
                                                           exclude_keywords=exclude_keywords, 
                                                           exclude_regex=exclude_regex, 
                                                           context_length=context_length, 
                                                           filter_level=filter_level)
                else:
                    filter_result = filter.filter_by_regex(text, regex_pattern, 
                                                         exclude_keywords=exclude_keywords, 
                                                         exclude_regex=exclude_regex, 
                                                         context_length=context_length, 
                                                         filter_level=filter_level)
                
                if filter_result.get("status") != "success":
                    return {
                        "success": False,
                        "data": {},
                        "error": filter_result.get("error", "筛选失败")
                    }
                
                # 构建筛选后的文本
                filtered_text = ""
                for result in filter_result.get("results", []):
                    if "keyword" in result:
                        filtered_text += f"关键词: {result['keyword']}\n"
                    else:
                        filtered_text += f"正则表达式: {result['pattern']}\n"
                    filtered_text += f"匹配: {result['match']}\n"
                    filtered_text += f"上下文: {result['context']}\n"
                    filtered_text += "-" * 80 + "\n"
                
                return {
                    "success": True,
                    "data": {
                        "text": text,
                        "filtered_text": filtered_text,
                        "matches": filter_result.get("results", []),
                        "total_matches": filter_result.get("total_matches", 0)
                    },
                    "error": ""
                }
            else:
                return {
                    "success": False,
                    "data": {},
                    "error": f"不支持的操作类型: {action}"
                }
                
        except Exception as e:
            logger.error(f"处理文件时出错: {str(e)}")
            return {
                "success": False,
                "data": {},
                "error": str(e)
            }
    
    @staticmethod
    def batch_process(input_dir=None, file_paths=None, action="extract", keywords=None, regex_pattern=None, 
                     output_dir=None, merge_results=False, enable_ocr=False, exclude_keywords=None, 
                     exclude_regex=None, context_length=50, filter_level="line"):
        """
        批量处理文件
        
        Args:
            input_dir: 输入文件夹路径
            file_paths: 文件路径列表
            action: 操作类型，extract 或 filter
            keywords: 关键词列表，仅 filter 操作需要
            regex_pattern: 正则表达式模式，仅 filter 操作需要
            output_dir: 输出目录
            merge_results: 是否合并所有文件结果为一个 JSON 文件
            enable_ocr: 是否启用 OCR 支持（用于扫描件 PDF）
            exclude_keywords: 排除关键词列表
            exclude_regex: 排除正则表达式模式
            context_length: 上下文长度（默认50字符）
            filter_level: 筛选级别，line（按行）或 paragraph（按段落）
            
        Returns:
            结构化 JSON 格式的结果
        """
        try:
            # 收集待处理的文件列表
            files_to_process = []
            
            # 处理输入文件夹
            if input_dir:
                input_dir = Path(input_dir)
                if not input_dir.exists() or not input_dir.is_dir():
                    return {
                        "success": False,
                        "data": {},
                        "error": f"输入目录不存在或不是目录: {input_dir}"
                    }
                
                # 遍历目录下所有支持的文件
                supported_extensions = ['.pdf', '.docx', '.xlsx', '.xls', '.txt', '.csv', '.md', '.wps', '.et']
                for file_path in input_dir.rglob('*'):
                    if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                        files_to_process.append(file_path)
            
            # 处理文件列表
            elif file_paths:
                for file_path_str in file_paths:
                    file_path = Path(file_path_str.strip())
                    if file_path.exists() and file_path.is_file():
                        files_to_process.append(file_path)
                    else:
                        logger.warning(f"文件不存在或不是文件: {file_path}")
            
            # 检查是否有文件需要处理
            if not files_to_process:
                return {
                    "success": False,
                    "data": {},
                    "error": "没有找到需要处理的文件"
                }
            
            # 设置输出目录
            if output_dir:
                output_dir = Path(output_dir)
            else:
                output_dir = Path.cwd() / "batch-results"
            
            # 创建输出目录
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 初始化结果列表
            file_results = []
            success_files = 0
            failed_files = 0
            failed_list = []
            
            logger.info(f"开始批量处理，共 {len(files_to_process)} 个文件")
            
            # 处理每个文件
            for file_path in tqdm(files_to_process, desc="处理进度", unit="file"):
                logger.info(f"开始处理文件: {file_path}")
                
                # 处理文件
                result = DocExtractFilter.process(file_path, action, keywords, regex_pattern, 
                                               enable_ocr, exclude_keywords, exclude_regex, 
                                               context_length, filter_level)
                
                if result["success"]:
                    success_files += 1
                    # 构建文件结果
                    file_result = {
                        "file_path": str(file_path),
                        "text": result["data"].get("text", "")
                    }
                    if "filtered_text" in result["data"]:
                        file_result["filtered_text"] = result["data"]["filtered_text"]
                    file_results.append(file_result)
                    
                    # 输出单个文件结果（如果不合并）
                    if not merge_results:
                        output_file = output_dir / f"{file_path.stem}_result.json"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(result, f, ensure_ascii=False, indent=2)
                        logger.info(f"文件处理完成，结果已保存到: {output_file}")
                else:
                    failed_files += 1
                    failed_list.append(str(file_path))
                    logger.error(f"文件处理失败: {file_path} - {result['error']}")
            
            # 构建汇总结果
            summary = {
                "total_files": len(files_to_process),
                "success_files": success_files,
                "failed_files": failed_files,
                "failed_list": failed_list
            }
            
            # 合并结果（如果需要）
            if merge_results:
                merge_output = {
                    "success": True,
                    "data": {
                        "file_results": file_results,
                        "summary": summary
                    },
                    "error": ""
                }
                merge_output_file = output_dir / "batch_merge_result.json"
                with open(merge_output_file, 'w', encoding='utf-8') as f:
                    json.dump(merge_output, f, ensure_ascii=False, indent=2)
                logger.info(f"批量处理完成，合并结果已保存到: {merge_output_file}")
            
            # 构建最终结果
            final_result = {
                "success": True,
                "data": {
                    "file_results": file_results,
                    "summary": summary
                },
                "error": ""
            }
            
            logger.info(f"批量处理完成，成功: {success_files}，失败: {failed_files}")
            return final_result
            
        except Exception as e:
            logger.error(f"批量处理时出错: {str(e)}")
            return {
                "success": False,
                "data": {},
                "error": str(e)
            }


@click.command()
@click.option('--file_path', help='文件路径')
@click.option('--action', required=True, type=click.Choice(['extract', 'filter']), help='操作类型')
@click.option('--keywords', help='关键词列表，逗号分隔')
@click.option('--regex', help='正则表达式模式')
@click.option('--enable-ocr', is_flag=True, help='启用 OCR 支持（用于扫描件 PDF）')
@click.option('--exclude-keywords', help='排除关键词列表，逗号分隔')
@click.option('--exclude-regex', help='排除正则表达式模式')
@click.option('--context-length', type=int, default=50, help='上下文长度（默认50字符）')
@click.option('--filter-level', type=click.Choice(['line', 'paragraph']), default='line', help='筛选级别，line（按行）或 paragraph（按段落）')
@click.option('--batch', is_flag=True, help='开启批量处理模式')
@click.option('--input-dir', help='批量处理的输入文件夹路径')
@click.option('--file-paths', help='批量处理的文件列表，逗号分隔')
@click.option('--output-dir', help='批量结果输出目录')
@click.option('--merge-results', is_flag=True, help='是否合并所有文件结果为一个 JSON 文件')
def cli(file_path, action, keywords, regex, enable_ocr, exclude_keywords, exclude_regex, 
        context_length, filter_level, batch, input_dir, file_paths, output_dir, merge_results):
    """
    命令行接口
    """
    # 处理关键词参数
    keyword_list = []
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(',')]
    
    # 处理排除关键词参数
    exclude_keyword_list = []
    if exclude_keywords:
        exclude_keyword_list = [k.strip() for k in exclude_keywords.split(',')]
    
    # 判断是否开启批量处理模式
    if batch:
        # 检查批量处理参数
        if not input_dir and not file_paths:
            print(json.dumps({
                "success": False,
                "data": {},
                "error": "批量处理模式需要提供 --input-dir 或 --file-paths 参数"
            }, ensure_ascii=False, indent=2))
            return
        
        # 处理文件路径列表
        file_path_list = []
        if file_paths:
            file_path_list = [p.strip() for p in file_paths.split(',')]
        
        # 调用批量处理函数
        result = DocExtractFilter.batch_process(
            input_dir=input_dir,
            file_paths=file_path_list,
            action=action,
            keywords=keyword_list,
            regex_pattern=regex,
            output_dir=output_dir,
            merge_results=merge_results,
            enable_ocr=enable_ocr,
            exclude_keywords=exclude_keyword_list,
            exclude_regex=exclude_regex,
            context_length=context_length,
            filter_level=filter_level
        )
    else:
        # 检查单个文件处理参数
        if not file_path:
            print(json.dumps({
                "success": False,
                "data": {},
                "error": "非批量处理模式需要提供 --file_path 参数"
            }, ensure_ascii=False, indent=2))
            return
        
        # 调用单个文件处理函数
        result = DocExtractFilter.process(file_path, action, keyword_list, regex, 
                                        enable_ocr, exclude_keyword_list, exclude_regex, 
                                        context_length, filter_level)
    
    # 输出 JSON 格式结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
