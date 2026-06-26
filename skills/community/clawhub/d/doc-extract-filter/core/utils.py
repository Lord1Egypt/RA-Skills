# 通用工具模块
import os
import logging
from typing import Dict, List, Optional, Union
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def ensure_directory(directory: Union[str, Path]) -> bool:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
        
    Returns:
        是否成功创建或目录已存在
    """
    try:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"创建目录 {directory} 时出错: {str(e)}")
        return False


def get_file_info(file_path: Union[str, Path]) -> Dict[str, Union[str, int, float]]:
    """
    获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件信息字典
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists() or not file_path.is_file():
            return {"error": "文件不存在"}
        
        return {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_size": file_path.stat().st_size,
            "modified_time": file_path.stat().st_mtime,
            "extension": file_path.suffix.lower()
        }
    except Exception as e:
        logger.error(f"获取文件信息时出错: {str(e)}")
        return {"error": str(e)}


def list_files(directory: Union[str, Path], extensions: Optional[List[str]] = None) -> List[Dict[str, Union[str, int]]]:
    """
    列出目录中的文件
    
    Args:
        directory: 目录路径
        extensions: 要筛选的文件扩展名列表，默认为 None（所有文件）
        
    Returns:
        文件列表
    """
    try:
        directory = Path(directory)
        if not directory.exists() or not directory.is_dir():
            return [{"error": "目录不存在或不是目录"}]
        
        files = []
        for file_path in directory.iterdir():
            if file_path.is_file():
                if extensions is None or file_path.suffix.lower() in extensions:
                    files.append({
                        "file_path": str(file_path),
                        "file_name": file_path.name,
                        "file_size": file_path.stat().st_size
                    })
        
        return files
    except Exception as e:
        logger.error(f"列出文件时出错: {str(e)}")
        return [{"error": str(e)}]


def validate_file_path(file_path: Union[str, Path]) -> bool:
    """
    验证文件路径是否有效
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件路径是否有效
    """
    try:
        file_path = Path(file_path)
        # 检查路径是否可写（如果文件不存在）
        if not file_path.exists():
            # 检查父目录是否存在且可写
            parent_dir = file_path.parent
            if not parent_dir.exists():
                parent_dir.mkdir(parents=True, exist_ok=True)
            return os.access(parent_dir, os.W_OK)
        # 如果文件存在，检查是否可写
        return os.access(file_path, os.W_OK)
    except Exception as e:
        logger.error(f"验证文件路径时出错: {str(e)}")
        return False


def format_response(code: int, message: str, data: Optional[Union[Dict, List]] = None) -> Dict[str, Union[int, str, Dict, List]]:
    """
    格式化 API 响应
    
    Args:
        code: 状态码
        message: 消息
        data: 数据，默认为 None
        
    Returns:
        格式化后的响应字典
    """
    response = {
        "code": code,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response


def handle_error(error: Exception, default_message: str = "操作失败") -> Dict[str, Union[int, str]]:
    """
    处理错误并返回标准化的错误响应
    
    Args:
        error: 异常对象
        default_message: 默认错误消息
        
    Returns:
        错误响应字典
    """
    logger.error(f"错误: {str(error)}")
    return {
        "code": 500,
        "message": f"{default_message}: {str(error)}"
    }
