import json
import os
from utils.gaode_client import GaodeClient

def get_current_location(latitude: Optional[float] = None, 
                        longitude: Optional[float] = None) -> str:
    """
    获取当前位置信息，返回语音友好的地址描述
    """
    client = GaodeClient()
    
    # 如果没有传入坐标，尝试从环境变量获取设备定位
    if latitude is None or longitude is None:
        latitude = os.environ.get("USER_LAT")
        longitude = os.environ.get("USER_LNG")
        if not latitude or not longitude:
            return json.dumps({
                "success": False,
                "message": "无法获取位置信息，请确保已授权定位权限"
            })
        latitude = float(latitude)
        longitude = float(longitude)
    
    result = client.reverse_geocode(latitude, longitude)
    address = result.get("regeocode", {})
    
    formatted = {
        "success": True,
        "province": address.get("addressComponent", {}).get("province"),
        "city": address.get("addressComponent", {}).get("city"),
        "district": address.get("addressComponent", {}).get("district"),
        "street": address.get("addressComponent", {}).get("street"),
        "address": address.get("formatted_address"),
        "location": f"{longitude},{latitude}",
        "voice_friendly": f"您当前位于{address.get('formatted_address', '未知位置')}"
    }
    
    return json.dumps(formatted, ensure_ascii=False)