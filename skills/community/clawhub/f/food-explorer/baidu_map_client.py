#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度地图API客户端
封装地理编码和周边搜索功能
"""

import requests
import os
from typing import Dict, List, Optional, Tuple
import json

# 尝试加载.env文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class BaiduMapClient:
    """百度地图API客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_key: 百度地图API Key，如果不提供则从环境变量获取
        """
        self.api_key = api_key or self._get_api_key()
        if not self.api_key:
            raise ValueError(
                "请提供API Key或设置环境变量 BAIDU_MAP_API_KEY\n"
                "获取方式：https://lbsyun.baidu.com/apiconsole/key"
            )
        
        self.base_url = "https://api.map.baidu.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FoodExplorer/1.0'
        })
    
    def _get_api_key(self) -> Optional[str]:
        """尝试多种方式获取API Key"""
        # 方式1：环境变量
        ak = os.environ.get('BAIDU_MAP_API_KEY')
        if ak:
            return ak
        
        # 方式2：Windows用户环境变量（解决子进程继承问题）
        try:
            import subprocess
            result = subprocess.run(
                ['powershell', '-Command', 
                 '[Environment]::GetEnvironmentVariable("BAIDU_MAP_API_KEY", "User")'],
                capture_output=True, text=True, timeout=5
            )
            ak = result.stdout.strip()
            if ak and len(ak) > 10:  # AK通常比较长
                return ak
        except Exception:
            pass
        
        return None
    
    def geocode(self, address: str, city: Optional[str] = None) -> Optional[Tuple[float, float]]:
        """
        地理编码：将地址转换为经纬度
        
        Args:
            address: 地址字符串，如"杭州市西湖区断桥"
            city: 城市名（可选，提高解析精度）
            
        Returns:
            (纬度, 经度) 元组，失败返回None
        """
        endpoint = f"{self.base_url}/geocoding/v3/"
        params = {
            'address': address,
            'output': 'json',
            'ak': self.api_key
        }
        
        if city:
            params['city'] = city
        
        try:
            data = self._make_request(endpoint, params)
            
            if data.get('status') == 0 and 'result' in data:
                location = data['result']['location']
                return (location['lat'], location['lng'])
            else:
                print(f"地理编码失败: {data.get('msg', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"地理编码异常: {e}")
            return None
    
    def search_nearby(
        self, 
        location: Tuple[float, float], 
        keyword: str = "美食",
        radius: int = 2000,
        page_size: int = 10,
        page_num: int = 0
    ) -> List[Dict]:
        """
        周边搜索：搜索附近的餐厅
        
        Args:
            location: (纬度, 经度)
            keyword: 搜索关键词，如"美食"、"火锅"、"日料"
            radius: 搜索半径（米），默认2000
            page_size: 返回结果数量，默认10，最大20
            page_num: 分页页码，默认0
            
        Returns:
            餐厅列表，每个餐厅是一个字典
        """
        endpoint = f"{self.base_url}/place/v2/search"
        
        # 构建location参数：纬度,经度
        location_str = f"{location[0]},{location[1]}"
        
        params = {
            'query': keyword,
            'location': location_str,
            'radius': radius,
            'output': 'json',
            'ak': self.api_key,
            'page_size': min(page_size, 20),  # 最大20
            'page_num': page_num,
            'scope': 2  # 返回详细信息
        }
        
        try:
            data = self._make_request(endpoint, params)
            
            if data.get('status') == 0:
                results = data.get('results', [])
                # 过滤掉没有详细信息的条目
                valid_results = [
                    r for r in results 
                    if r.get('name') and r.get('location')
                ]
                return valid_results
            else:
                print(f"周边搜索失败: {data.get('msg', '未知错误')}")
                return []
                
        except Exception as e:
            print(f"周边搜索异常: {e}")
            return []
    
    def _make_request(self, endpoint: str, params: Dict, retries: int = 1) -> Dict:
        """
        发起HTTP请求，支持重试
        
        Args:
            endpoint: API端点
            params: 请求参数
            retries: 重试次数
            
        Returns:
            JSON响应
        """
        for attempt in range(retries + 1):
            try:
                response = self.session.get(
                    endpoint, 
                    params=params, 
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.Timeout:
                if attempt < retries:
                    print(f"请求超时，第{attempt + 1}次重试...")
                    continue
                raise
                
            except requests.exceptions.RequestException as e:
                if attempt < retries:
                    print(f"请求失败，第{attempt + 1}次重试: {e}")
                    continue
                raise
        
        return {}
    
    @staticmethod
    def parse_restaurant_info(raw_data: Dict) -> Dict:
        """
        解析餐厅原始数据，提取关键信息
        
        Args:
            raw_data: API返回的原始餐厅数据
            
        Returns:
            结构化的餐厅信息
        """
        detail = raw_data.get('detail_info', {})
        
        return {
            'name': raw_data.get('name', '未知餐厅'),
            'address': raw_data.get('address', '地址未知'),
            'telephone': raw_data.get('telephone', ''),
            'location': raw_data.get('location', {}),
            'rating': detail.get('overall_rating', '暂无'),
            'price': detail.get('price', '未知'),
            'tag': detail.get('tag', '美食'),
            'detail_url': detail.get('detail_url', ''),
            'distance': raw_data.get('detail_info', {}).get('distance', 0)
        }


# 测试代码
if __name__ == "__main__":
    # 测试用例 - 需要设置BAIDU_MAP_API_KEY环境变量
    import os
    
    api_key = os.environ.get('BAIDU_MAP_API_KEY')
    if not api_key:
        print("请先设置环境变量 BAIDU_MAP_API_KEY")
        print("示例: export BAIDU_MAP_API_KEY='你的API_KEY'")
        exit(1)
    
    client = BaiduMapClient(api_key)
    
    print("=== 测试地理编码 ===")
    location = client.geocode("杭州西湖断桥")
    if location:
        print(f"坐标: 纬度={location[0]}, 经度={location[1]}")
        
        print("\n=== 测试周边搜索 ===")
        restaurants = client.search_nearby(location, "杭帮菜", radius=2000, page_size=5)
        print(f"找到 {len(restaurants)} 家餐厅")
        
        for i, r in enumerate(restaurants[:3], 1):
            info = client.parse_restaurant_info(r)
            print(f"\n{i}. {info['name']}")
            print(f"   评分: {info['rating']} | 人均: ¥{info['price']}")
            print(f"   地址: {info['address']}")
    else:
        print("地理编码失败")
