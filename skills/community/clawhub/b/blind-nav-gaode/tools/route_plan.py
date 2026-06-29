import json
import os
from utils.gaode_client import GaodeClient
from utils.voice_formatter import format_route_for_voice

def plan_walking_route(destination: str, prefer_accessible: bool = True) -> str:
    """规划步行路线，输出语音友好的导航指令"""
    client = GaodeClient()
    
    lat = os.environ.get("USER_LAT")
    lng = os.environ.get("USER_LNG")
    if not lat or not lng:
        return json.dumps({"success": False, "message": "需要位置信息"})
    
    # 先地理编码获取目的地坐标
    dest_geo = client.geocode(destination)
    if not dest_geo.get("geocodes"):
        return json.dumps({"success": False, "message": f"找不到目的地：{destination}"})
    
    dest_location = dest_geo["geocodes"][0]["location"]
    dest_name = dest_geo["geocodes"][0]["formatted_address"]
    
    # 规划步行路线
    route = client.plan_walking(f"{lng},{lat}", dest_location)
    
    steps = route.get("route", {}).get("paths", [{}])[0].get("steps", [])
    
    # 格式化为语音友好格式
    voice_steps = format_route_for_voice(steps)
    
    return json.dumps({
        "success": True,
        "destination": dest_name,
        "total_distance": route.get("route", {}).get("paths", [{}])[0].get("distance"),
        "total_duration": route.get("route", {}).get("paths", [{}])[0].get("duration"),
        "steps": voice_steps,
        "voice_summary": f"已为您规划到{dest_name}的步行路线，全程约{voice_steps[-1]['cumulative_distance']}米"
    }, ensure_ascii=False)