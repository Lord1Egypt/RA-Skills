from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def animal_recognition(
    dataUrl: str
) -> Dict[str, Any]:
    """
    对含有动物的图像进行标签识别，无需任何额外输入，输出动物的类别标签。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826131895162890", "animal_recognition", arguments)

def animal_recognition_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    对含有动物的图像进行标签识别，无需任何额外输入，输出动物的类别标签。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826131895162890", "animal_recognition_for_data_base64", arguments)

