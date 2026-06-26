"""
timeliness 子命令 - 时效性计算

解析单个文件，提取日期信息，判定文档时效性状态。
直接调用 TimelinessChecker.evaluate_document()（公开方法）。
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def _get_parser(file_path: str, container=None):
    """
    根据文件扩展名选择合适的解析器。

    Args:
        file_path: 文件路径
        container: 依赖注入容器（用于获取配置好的解析器）

    Returns:
        解析器实例

    Raises:
        ValueError: 不支持的文件格式
    """
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        from ...infrastructure.parsers.pdf_parser import PDFParser
        # 如果提供了容器，使用容器中配置好的 OCR 引擎
        if container is not None:
            ocr_engine = container.ocr_engine
            return PDFParser(ocr_engine=ocr_engine, use_ocr=True)
        else:
            # 回退：无 OCR 引擎的解析器
            return PDFParser()
    elif ext in (".docx", ".doc"):
        from ...infrastructure.parsers.docx_parser import DocxParser
        return DocxParser()
    elif ext in (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif", ".webp"):
        from ...infrastructure.parsers.image_parser import ImageParser
        return ImageParser()
    else:
        raise ValueError(f"不支持的文件格式: {ext}")


def _parse_reference_time(ref_time_str: Optional[str]) -> datetime:
    """
    解析 --reference-time 参数。

    Args:
        ref_time_str: 时间字符串 (YYYY-MM-DD) 或 None

    Returns:
        datetime 对象
    """
    if not ref_time_str:
        return datetime.now()

    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(ref_time_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"无法解析时间格式: {ref_time_str}，请使用 YYYY-MM-DD 格式")


async def run_timeliness(file: str, reference_time: Optional[str] = None) -> dict:
    """
    执行 timeliness 子命令。

    Args:
        file: 文件路径
        reference_time: 校验基准时间字符串 (YYYY-MM-DD)，默认为当前时间

    Returns:
        {status, sign_date, expiry_date, validity, branch, reason}
    """
    file_path = Path(file)
    if not file_path.is_file():
        raise FileNotFoundError(f"文件不存在: {file}")

    # 1. 创建容器并解析文件（使用配置好的 OCR 引擎）
    from ..bootstrap import create_container

    container = create_container()
    parser = _get_parser(file, container=container)
    document = parser.parse(file)

    # 2. 解析基准时间
    ref_time = _parse_reference_time(reference_time)

    # 3. 调用 TimelinessChecker.evaluate_document()
    from ...domain.checkers.timeliness import TimelinessChecker

    checker = TimelinessChecker(
        llm_client=container.llm_client,
        validity_retriever=container.validity_retriever,
    )
    # 使用异步版本以支持 LLM 和 Micro-RAG 提取
    eval_result = await checker.evaluate_document_async(document, ref_time)

    # 4. 映射输出格式
    if eval_result["passed"]:
        status = "VALID"
    elif eval_result["branch"] == "NONE":
        status = "UNKNOWN"
    else:
        status = "EXPIRED"

    output = {
        "status": status,
        "sign_date": eval_result.get("sign_date"),
        "expiry_date": eval_result.get("expiry_date"),
        "validity": eval_result.get("validity"),
        "branch": eval_result.get("branch"),
        "reason": eval_result.get("reason", ""),
    }

    return output
