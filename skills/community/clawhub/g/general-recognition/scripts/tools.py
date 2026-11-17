from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def general_recognition(
    dataUrl: str
) -> Dict[str, Any]:
    """
    对包含主体物体的图像进行标签识别，输出主体物体的类别标签，目前已经覆盖了5万多类的物体类别。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826131898617866", "general_recognition", arguments)

def general_recognition_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    对包含主体物体的图像进行标签识别，输出主体物体的类别标签，目前已经覆盖了5万多类的物体类别。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826131898617866", "general_recognition_for_data_base64", arguments)

