# 内容筛选模块
import re
import logging
from typing import Dict, List, Optional, Union, Pattern
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ContentFilter:
    """
    内容筛选器类，支持按关键词和正则表达式筛选文件内容
    """
    
    def __init__(self):
        """
        初始化内容筛选器
        """
        pass
    
    def filter_by_keyword(self, content: Union[str, List[str]], keywords: List[str], 
                         case_sensitive: bool = False, exclude_keywords: Optional[List[str]] = None, 
                         exclude_regex: Optional[str] = None, context_length: int = 50, 
                         filter_level: str = "line") -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        按关键词筛选内容
        
        Args:
            content: 要筛选的内容，可以是字符串或字符串列表
            keywords: 关键词列表
            case_sensitive: 是否区分大小写，默认为 False
            exclude_keywords: 排除关键词列表
            exclude_regex: 排除正则表达式模式
            context_length: 上下文长度（默认50字符）
            filter_level: 筛选级别，line（按行）或 paragraph（按段落）
            
        Returns:
            包含筛选结果的字典
        """
        try:
            results = []
            
            if isinstance(content, str):
                content_list = [content]
            else:
                content_list = content
            
            for idx, text in enumerate(content_list):
                if not isinstance(text, str):
                    continue
                
                # 按行或段落分割文本
                if filter_level == "line":
                    segments = text.split('\n')
                else:  # paragraph
                    segments = text.split('\n\n')
                
                for keyword in keywords:
                    for seg_idx, segment in enumerate(segments):
                        if case_sensitive:
                            if keyword in segment:
                                # 提取上下文
                                context = self._get_context(segments, seg_idx, context_length, filter_level)
                                # 检查是否需要排除
                                if not self._should_exclude(context, exclude_keywords, exclude_regex):
                                    # 计算在原文本中的位置
                                    position = text.find(segment)
                                    results.append({
                                        "keyword": keyword,
                                        "match": keyword,
                                        "context": context.replace('\n', ' '),
                                        "position": position if position != -1 else 0,
                                        "content_index": idx if len(content_list) > 1 else None
                                    })
                        else:
                            if keyword.lower() in segment.lower():
                                # 提取上下文
                                context = self._get_context(segments, seg_idx, context_length, filter_level)
                                # 检查是否需要排除
                                if not self._should_exclude(context, exclude_keywords, exclude_regex):
                                    # 计算在原文本中的位置
                                    position = text.find(segment)
                                    results.append({
                                        "keyword": keyword,
                                        "match": keyword,
                                        "context": context.replace('\n', ' '),
                                        "position": position if position != -1 else 0,
                                        "content_index": idx if len(content_list) > 1 else None
                                    })
            
            return {
                "status": "success",
                "results": results,
                "total_matches": len(results)
            }
        except Exception as e:
            logger.error(f"关键词筛选时出错: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def filter_by_regex(self, content: Union[str, List[str]], pattern: str, 
                       exclude_keywords: Optional[List[str]] = None, 
                       exclude_regex: Optional[str] = None, context_length: int = 50, 
                       filter_level: str = "line") -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        按正则表达式筛选内容
        
        Args:
            content: 要筛选的内容，可以是字符串或字符串列表
            pattern: 正则表达式模式
            exclude_keywords: 排除关键词列表
            exclude_regex: 排除正则表达式模式
            context_length: 上下文长度（默认50字符）
            filter_level: 筛选级别，line（按行）或 paragraph（按段落）
            
        Returns:
            包含筛选结果的字典
        """
        try:
            regex = re.compile(pattern)
            results = []
            
            if isinstance(content, str):
                content_list = [content]
            else:
                content_list = content
            
            for idx, text in enumerate(content_list):
                if not isinstance(text, str):
                    continue
                
                # 按行或段落分割文本
                if filter_level == "line":
                    segments = text.split('\n')
                else:  # paragraph
                    segments = text.split('\n\n')
                
                for seg_idx, segment in enumerate(segments):
                    matches = regex.finditer(segment)
                    for match in matches:
                        # 提取上下文
                        context = self._get_context(segments, seg_idx, context_length, filter_level)
                        # 检查是否需要排除
                        if not self._should_exclude(context, exclude_keywords, exclude_regex):
                            # 计算在原文本中的位置
                            position = text.find(segment)
                            results.append({
                                "pattern": pattern,
                                "match": match.group(),
                                "context": context.replace('\n', ' '),
                                "position": position + match.start() if position != -1 else match.start(),
                                "content_index": idx if len(content_list) > 1 else None
                            })
            
            return {
                "status": "success",
                "results": results,
                "total_matches": len(results)
            }
        except re.error as e:
            logger.error(f"正则表达式语法错误: {str(e)}")
            return {
                "status": "error",
                "error": f"正则表达式语法错误: {str(e)}"
            }
        except Exception as e:
            logger.error(f"正则筛选时出错: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def export_results(self, results: Dict, output_file: Union[str, Path]) -> Dict[str, str]:
        """
        导出筛选结果到文件
        
        Args:
            results: 筛选结果字典
            output_file: 输出文件路径
            
        Returns:
            导出结果状态
        """
        try:
            output_file = Path(output_file)
            
            if results.get("status") != "success":
                return {
                    "status": "error",
                    "error": "筛选结果无效"
                }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# 筛选结果\n\n")
                f.write(f"总匹配数: {results.get('total_matches', 0)}\n\n")
                
                for idx, result in enumerate(results.get('results', [])):
                    f.write(f"匹配 #{idx + 1}:\n")
                    f.write(f"关键词/模式: {result.get('keyword', result.get('pattern', 'N/A'))}\n")
                    f.write(f"匹配内容: {result.get('match', 'N/A')}\n")
                    f.write(f"上下文: {result.get('context', 'N/A')}\n")
                    f.write(f"位置: {result.get('position', 'N/A')}\n")
                    if result.get('content_index') is not None:
                        f.write(f"内容索引: {result.get('content_index')}\n")
                    f.write("-" * 80 + "\n\n")
            
            return {
                "status": "success",
                "output_file": str(output_file)
            }
        except Exception as e:
            logger.error(f"导出结果时出错: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _should_exclude(self, text: str, exclude_keywords: Optional[List[str]], 
                       exclude_regex: Optional[str]) -> bool:
        """
        检查文本是否应该被排除
        
        Args:
            text: 待检查的文本
            exclude_keywords: 排除关键词列表
            exclude_regex: 排除正则表达式模式
            
        Returns:
            是否应该被排除
        """
        # 检查排除关键词
        if exclude_keywords:
            for keyword in exclude_keywords:
                if keyword in text:
                    return True
        
        # 检查排除正则表达式
        if exclude_regex:
            if re.search(exclude_regex, text, re.MULTILINE | re.DOTALL):
                return True
        
        return False
    
    def _get_context(self, segments: List[str], index: int, context_length: int, 
                    filter_level: str) -> str:
        """
        获取匹配内容的上下文
        
        Args:
            segments: 文本段列表
            index: 匹配段的索引
            context_length: 上下文长度
            filter_level: 筛选级别
            
        Returns:
            包含上下文的文本
        """
        # 计算上下文范围
        start = max(0, index - 1)
        end = min(len(segments), index + 2)
        
        # 提取上下文
        context_segments = segments[start:end]
        
        # 连接上下文
        if filter_level == "line":
            context = '\n'.join(context_segments)
        else:  # paragraph
            context = '\n\n'.join(context_segments)
        
        # 限制上下文长度
        if len(context) > context_length:
            # 找到匹配段在上下文中的位置
            match_start = context.find(segments[index])
            if match_start == -1:
                match_start = 0
            
            # 计算上下文的起始和结束位置
            context_start = max(0, match_start - context_length // 2)
            context_end = min(len(context), match_start + len(segments[index]) + context_length // 2)
            
            # 截取上下文
            context = context[context_start:context_end]
            if context_start > 0:
                context = "..." + context
            if context_end < len(context):
                context = context + "..."
        
        return context
