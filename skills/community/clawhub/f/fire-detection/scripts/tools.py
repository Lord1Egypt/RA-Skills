from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def fire_detection(
    dataUrl: str
) -> Dict[str, Any]:
    """
    检测各类通用场景中出现的火焰，最佳使用场景：安防摄像头、交通摄像头视角。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826131897926666", "fire_detection", arguments)

def fire_detection_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    检测各类通用场景中出现的火焰，最佳使用场景：安防摄像头、交通摄像头视角。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826131897926666", "fire_detection_for_data_base64", arguments)

