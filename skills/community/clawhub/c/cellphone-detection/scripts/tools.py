from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def cellphone_detection(
    dataUrl: str
) -> Dict[str, Any]:
    """
    输入一张图像，对其中的手机进行检测，输出图片中所有目标的检测框、置信度和标签。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826131895879690", "cellphone_detection", arguments)

def cellphone_detection_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    输入一张图像，对其中的手机进行检测，输出图片中所有目标的检测框、置信度和标签。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826131895879690", "cellphone_detection_for_data_base64", arguments)

