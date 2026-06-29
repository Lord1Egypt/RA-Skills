import json
import os
from utils.gaode_client import GaodeClient

def search_accessible(type: str = "all", radius: int = 2000) -> str:
    """搜索无障碍设施"""
    client = GaodeClient()
    
    lat = os.environ.get("USER_LAT")
    lng = os.environ.get("USER_LNG")
    if not lat or not lng:
        return json.dumps({"success": False, "message": "需要位置信息"})
    
    # 无障碍相关关键词映射
    keyword_map = {
        "toilet": "无障碍厕所",
        "elevator": "无障碍电梯",
        "ramp": "无障碍坡道",
        "all": "无障碍"
    }
    
    pois = client.search_nearby(
        float(lat), float(lng), 
        keyword_map.get(type, "无障碍"), 
        radius
    )
    
    results = []
    for poi in pois[:5]:
        results.append({
            "name": poi.get("name"),
            "type": type,
            "distance": poi.get("distance"),
            "address": poi.get("address"),
            "voice_friendly": f"{poi.get('name')}，距离{poi.get('distance')}米"
        })
    
    return json.dumps({
        "success": True,
        "results": results,
        "voice_summary": f"找到{len(results)}个无障碍设施" if results else "附近暂未找到无障碍设施"
    }, ensure_ascii=False)