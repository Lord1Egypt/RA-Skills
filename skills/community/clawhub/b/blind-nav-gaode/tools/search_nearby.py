import json
import os
from utils.gaode_client import GaodeClient

def search_nearby(keyword: str, radius: int = 3000) -> str:
    """搜索附近设施，返回按距离排序的结果"""
    client = GaodeClient()
    
    lat = os.environ.get("USER_LAT")
    lng = os.environ.get("USER_LNG")
    if not lat or not lng:
        return json.dumps({"success": False, "message": "需要位置信息"})
    
    pois = client.search_nearby(float(lat), float(lng), keyword, radius)
    
    results = []
    for poi in pois[:5]:  # 只返回最近的5个
        results.append({
            "name": poi.get("name"),
            "address": poi.get("address"),
            "distance": poi.get("distance"),
            "location": poi.get("location"),
            "tel": poi.get("tel"),
            "voice_friendly": f"{poi.get('name')}，距离{poi.get('distance')}米，"
                            f"地址：{poi.get('address', '未知')}"
        })
    
    return json.dumps({
        "success": True,
        "count": len(results),
        "results": results,
        "voice_summary": f"找到{len(results)}个{keyword}，最近的是{results[0]['name']}，距离{results[0]['distance']}米" if results else f"附近没有找到{keyword}"
    }, ensure_ascii=False)