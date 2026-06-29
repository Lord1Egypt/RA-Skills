import os
import requests
from typing import Optional, Dict, List, Tuple

class GaodeClient:
    """高德开放平台 API 封装"""
    
    BASE_URL = "https://restapi.amap.com/v3"
    
    def __init__(self):
        self.api_key = os.environ.get("GAODE_API_KEY")
        if not self.api_key:
            raise ValueError("缺少 GAODE_API_KEY 环境变量")
        self.session = requests.Session()
    
    def _get(self, endpoint: str, params: Dict) -> Dict:
        """统一 GET 请求"""
        params["key"] = self.api_key
        resp = self.session.get(f"{self.BASE_URL}/{endpoint}", params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "1":
            raise RuntimeError(f"API 调用失败: {data.get('info', '未知错误')}")
        return data
    
    # 逆地理编码：坐标 → 地址
    def reverse_geocode(self, lat: float, lng: float) -> Dict:
        return self._get("geocode/regeo", {
            "location": f"{lng},{lat}",
            "extensions": "all"
        })
    
    # 地理编码：地址 → 坐标
    def geocode(self, address: str, city: Optional[str] = None) -> Dict:
        params = {"address": address}
        if city:
            params["city"] = city
        return self._get("geocode/geo", params)
    
    # 周边搜索
    def search_nearby(self, lat: float, lng: float, keyword: str, 
                      radius: int = 3000) -> List[Dict]:
        return self._get("place/around", {
            "location": f"{lng},{lat}",
            "keywords": keyword,
            "radius": radius,
            "extensions": "all"
        }).get("pois", [])
    
    # 步行路线规划
    def plan_walking(self, origin: str, destination: str) -> Dict:
        """origin/destination 格式: '经度,纬度'"""
        return self._get("direction/walking", {
            "origin": origin,
            "destination": destination
        })
    
    # 公交路线规划
    def plan_transit(self, origin: str, destination: str, city: str) -> Dict:
        return self._get("direction/transit/integrated", {
            "origin": origin,
            "destination": destination,
            "city": city
        })