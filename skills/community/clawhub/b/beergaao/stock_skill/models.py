"""模型加载安全防护 - 防止加载不可信的序列化文件"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# 模型文件白名单目录
_MODELS_DIR = Path(__file__).parent.parent / "models"

# 允许的文件扩展名
_ALLOWED_EXTENSIONS = {".joblib", ".pkl", ".json", ".safetensors"}

# 占位符检测
_PLACEHOLDER_PATTERNS = ["your_", "xxx", "test", "placeholder", "example", "sample"]


def _validate_model_path(file_path: str) -> None:
    """验证模型文件路径是否安全"""
    abs_path = Path(file_path).resolve()
    
    # 检查是否在允许的目录内
    if not str(abs_path).startswith(str(_MODELS_DIR.resolve())):
        raise ValueError(
            f"安全限制：模型文件必须位于 {_MODELS_DIR} 目录内。"
            f"尝试加载的路径: {file_path}"
        )
    
    # 检查文件扩展名
    if abs_path.suffix not in _ALLOWED_EXTENSIONS:
        raise ValueError(
            f"安全限制：不允许的文件扩展名 '{abs_path.suffix}'。"
            f"允许的扩展名: {_ALLOWED_EXTENSIONS}"
        )
    
    # 检查文件是否存在
    if not abs_path.exists():
        raise FileNotFoundError(f"模型文件不存在: {file_path}")


def _check_file_integrity(file_path: str) -> bool:
    """检查文件完整性（基础检查）"""
    try:
        abs_path = Path(file_path).resolve()
        
        # 检查文件大小（防止异常大的文件）
        file_size = abs_path.stat().st_size
        max_size = 100 * 1024 * 1024  # 100MB
        if file_size > max_size:
            logger.warning(f"模型文件过大 ({file_size / 1024 / 1024:.1f}MB > {max_size / 1024 / 1024}MB)")
            return False
        
        # 检查文件名是否包含可疑模式
        file_name = abs_path.name.lower()
        if any(pattern in file_name for pattern in _PLACEHOLDER_PATTERNS):
            logger.warning(f"模型文件名包含可疑模式: {file_name}")
            return False
        
        return True
    except Exception as e:
        logger.error(f"文件完整性检查失败: {e}")
        return False


def load_model_safe(file_path: str, loader_func=None) -> Optional[Any]:
    """安全加载模型文件

    Args:
        file_path: 模型文件路径
        loader_func: 自定义加载函数，默认使用 joblib.load

    Returns:
        加载的模型对象，或 None（加载失败时）
    """
    try:
        # 1. 路径验证
        _validate_model_path(file_path)
        
        # 2. 完整性检查
        if not _check_file_integrity(file_path):
            logger.error(f"模型文件完整性检查失败: {file_path}")
            return None
        
        # 3. 加载模型
        if loader_func is None:
            import joblib
            loader_func = joblib.load
        
        logger.info(f"安全加载模型: {file_path}")
        model = loader_func(file_path)
        
        return model
        
    except ValueError as e:
        logger.error(f"模型加载安全限制: {e}")
        return None
    except FileNotFoundError as e:
        logger.error(f"模型文件不存在: {e}")
        return None
    except Exception as e:
        logger.error(f"模型加载失败: {e}")
        return None


def list_available_models() -> list:
    """列出可用的模型文件"""
    models = []
    if _MODELS_DIR.exists():
        for f in _MODELS_DIR.iterdir():
            if f.suffix in _ALLOWED_EXTENSIONS and not f.name.startswith("."):
                models.append({
                    "name": f.name,
                    "path": str(f),
                    "size": f.stat().st_size,
                    "modified": f.stat().st_mtime,
                })
    return models
