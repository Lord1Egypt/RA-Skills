import json
import os
from utils.gaode_client import GaodeClient

def sos_location_share(message: Optional[str] = None) -> str:
    """紧急求助：获取精确位置并生成求助信息"""
    client = GaodeClient()
    
    lat = os.environ.get("USER_LAT")
    lng = os.environ.get("USER_LNG")
    if not lat or not lng:
        return json.dumps({"success": False, "message": "无法获取位置"})
    
    # 获取详细地址
    result = client.reverse_geocode(float(lat), float(lng))
    address = result.get("regeocode", {}).get("formatted_address", "未知位置")
    
    sos_info = {
        "success": True,
        "timestamp": os.environ.get("CURRENT_TIME", "现在"),
        "location": {
            "latitude": lat,
            "longitude": lng,
            "address": address
        },
        "message": message or "我需要帮助",
        "emergency_contacts": [
            {"name": "紧急联系人1", "phone": "120"},
            {"name": "报警", "phone": "110"}
        ],
        "voice_alert": f"紧急求助！我位于{address}，需要帮助！"
    }
    
    return json.dumps(sos_info, ensure_ascii=False)