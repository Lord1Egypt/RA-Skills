"""
completeness 子命令 - 文档批量嗅探

扫描目录下的文件，与给定的文档名称列表做精确+语义匹配。
直接使用 Container 中的 semantic_matcher，将全部文件名作为候选池传入
find_best_match，实现正确的语义消歧。

不使用 CompletenessChecker.match_document() + RequiredDocument，
原因：构造无 aliases 的最简 RequiredDocument 会导致 find_best_match
退化为单候选成对比较，语义消歧能力归零。
"""

import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# 可解析内容的文件扩展名（需要解析器读取内容）
PARSABLE_EXTENSIONS = {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg"}

# 所有其他文件扩展名都通过文件名进行存在性检查（非白名单制度）

# 去扩展名的正则
_EXT_RE = re.compile(r"\.(pdf|docx?|jpg|jpeg|png|tiff|bmp)$", re.IGNORECASE)


def _scan_supported_files(directory: str) -> Dict[str, str]:
    """
    扫描目录下所有支持格式的文件。

    包括：
    1. 可解析内容的格式（PDF/Word/图片）
    2. 仅支持文件名存在性检查的格式（dwg/xls等）

    Args:
        directory: 目录路径

    Returns:
        {文件名: 完整路径} 映射
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise FileNotFoundError(f"目录不存在: {directory}")

    file_map = {}
    for item in dir_path.iterdir():
        if item.is_file():
            # 跳过隐藏文件和系统文件
            if item.name.startswith('.') or item.name.startswith('~'):
                continue
            file_map[item.name] = str(item)

    return file_map


def _exact_match(doc_name: str, file_names: List[str]) -> Optional[str]:
    """
    精确匹配：检查 doc_name 是否作为子串出现在某个文件名中。

    匹配逻辑（复用 CompletenessChecker._exact_match 的规则）：
    1. doc_name 是文件名的子串（直接包含）
    2. doc_name 是去扩展名后文件名的子串，或反向包含

    Args:
        doc_name: 要查找的文档名称
        file_names: 所有文件名列表

    Returns:
        匹配到的文件名，未匹配返回 None
    """
    for file_name in file_names:
        # 直接包含匹配
        if doc_name in file_name:
            return file_name

        # 去扩展名后匹配
        clean_file = _EXT_RE.sub("", file_name)
        clean_doc = _EXT_RE.sub("", doc_name)
        if clean_doc in clean_file or clean_file in clean_doc:
            return file_name

    return None


async def run_completeness(path: str, documents: List[str]) -> dict:
    """
    执行 completeness 子命令。

    Args:
        path: 项目文件夹路径
        documents: 要查找的文档名称列表

    Returns:
        {doc_name: {path, similarity, match_type} | null}
    """
    if not documents:
        raise ValueError("--documents 不能为空")

    # 1. 扫描目录
    file_map = _scan_supported_files(path)
    file_names = list(file_map.keys())

    if not file_names:
        # 目录为空，所有文档都未找到
        return {doc_name: None for doc_name in documents}

    result = {}

    # 2. 精确匹配阶段
    unmatched_docs = []
    for doc_name in documents:
        matched_file = _exact_match(doc_name, file_names)
        if matched_file:
            result[doc_name] = {
                "path": file_map[matched_file],
                "similarity": 1.0,
                "match_type": "exact",
            }
        else:
            unmatched_docs.append(doc_name)

    # 3. 语义匹配阶段（仅对未精确匹配的文档进行）
    if unmatched_docs:
        try:
            from ..bootstrap import create_container

            container = create_container()
            matcher = container.semantic_matcher
            threshold = container.config.similarity_threshold

            if matcher:
                for doc_name in unmatched_docs:
                    # 关键：将全部文件名作为候选池，让语义匹配器做消歧
                    best_file, similarity = await matcher.find_best_match(
                        doc_name, file_names
                    )
                    if best_file and similarity >= threshold:
                        result[doc_name] = {
                            "path": file_map[best_file],
                            "similarity": round(similarity, 2),
                            "match_type": "semantic",
                        }
                    else:
                        result[doc_name] = None
            else:
                # 语义匹配器不可用，标记为未匹配
                logger.warning("语义匹配器不可用，仅使用精确匹配")
                for doc_name in unmatched_docs:
                    result[doc_name] = None

        except Exception as e:
            logger.warning(f"语义匹配失败，降级为精确匹配: {e}")
            for doc_name in unmatched_docs:
                result[doc_name] = None

    return result
