#!/usr/bin/env python3
"""
Neverland农场自动化助手 v1.5.2
ClawHub版本 - 使用环境变量配置

环境变量:
- NEVERLAND_API_KEY: Agent World API密钥
- NEVERLAND_FARM_ID: 农场ID
"""

import json
import time
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List

try:
    import requests
except ImportError:
    print("❌ 请先安装requests库: pip install requests")
    sys.exit(1)

# 从环境变量读取配置
API_KEY = os.environ.get("NEVERLAND_API_KEY", "")
FARM_ID = os.environ.get("NEVERLAND_FARM_ID", "")
BASE_URL = "https://neverland.coze.site/api"
STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

# 检查配置
if not API_KEY or not FARM_ID:
    print("❌ 请设置环境变量 NEVERLAND_API_KEY 和 NEVERLAND_FARM_ID")
    sys.exit(1)

# 健康检查模式
if "--check" in sys.argv:
    print("✅ 配置检查通过")
    sys.exit(0)


class RateLimitError(Exception):
    """频率限制异常"""
    def __init__(self, message: str, reset_time: str):
        super().__init__(message)
        self.reset_time = reset_time


class NeverlandAPIClient:
    """Neverland农场API客户端"""
    
    def __init__(self, api_key: str, farm_id: str):
        self.farm_id = farm_id
        self.base_url = BASE_URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                r = requests.get(url, headers=self.headers, timeout=30)
            else:
                r = requests.post(url, headers=self.headers, json=data, timeout=30)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitError("频率限制", "30分钟后重试")
            raise
        except requests.exceptions.RequestException as e:
            print(f"⚠️ 请求失败: {e}")
            raise
    
    def get_status(self) -> Dict:
        """获取农场状态"""
        return self._request("GET", f"/farm/{self.farm_id}/status")
    
    def collect_products(self) -> Dict:
        """收集动物产品"""
        return self._request("POST", f"/farm/{self.farm_id}/collect")
    
    def get_crops(self) -> Dict:
        """获取作物信息（从状态中提取）"""
        status = self.get_status()
        return {"plots": status.get("data", {}).get("plots", [])}
    
    def get_backpack(self) -> Dict:
        """获取背包信息（从状态中提取）"""
        status = self.get_status()
        return {"items": status.get("data", {}).get("inventory", [])}
    
    def harvest_crop(self, plot_id: int) -> Dict:
        """收获作物"""
        return self._request("POST", f"/farm/{self.farm_id}/harvest/{plot_id}")
    
    def sell_item(self, item_id: str, quantity: int = 1) -> Dict:
        """出售物品"""
        return self._request("POST", f"/farm/{self.farm_id}/sell", {"item_id": item_id, "quantity": quantity})
    
    def next_day(self) -> Dict:
        """进入下一天"""
        return self._request("POST", f"/farm/{self.farm_id}/next-day")


class SmartFarmManager:
    """智能农场管理器"""
    
    def __init__(self, client: NeverlandAPIClient):
        self.client = client
        self.post_count = 0
        self.max_posts = 3
    
    def run(self):
        print(f"\n🌾 Neverland农场自动化 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        # 1. 状态
        try:
            status = self.client.get_status()
            data = status.get("data", status)
            print(f"金币: {data.get('coins')} | 体力: {data.get('energy')}")
        except Exception as e:
            print(f"⚠️ 获取状态失败: {e}")
            return
        
        # 2. 收集
        if self.post_count < self.max_posts:
            try:
                self.client.collect_products()
                self.post_count += 1
                print("✅ 收集动物产品")
            except Exception as e:
                print(f"⚠️ 收集失败: {e}")
        
        # 3. 收获
        if self.post_count < self.max_posts:
            try:
                crops = self.client.get_crops()
                for plot in crops.get("plots", []):
                    if plot.get("harvestable") and self.post_count < self.max_posts:
                        self.client.harvest_crop(plot["id"])
                        self.post_count += 1
                        print(f"✅ 收获地块 {plot['id']}")
            except Exception as e:
                print(f"⚠️ 收获失败: {e}")
        
        # 4. 出售
        if self.post_count < self.max_posts:
            try:
                backpack = self.client.get_backpack()
                for item in backpack.get("items", []):
                    if self.post_count < self.max_posts:
                        self.client.sell_item(item["id"], item.get("quantity", 1))
                        self.post_count += 1
                        print(f"✅ 出售 {item['id']}")
            except Exception as e:
                print(f"⚠️ 出售失败: {e}")
        
        # 5. 下一天
        if self.post_count < self.max_posts:
            try:
                self.client.next_day()
                self.post_count += 1
                print("✅ 进入下一天")
            except Exception as e:
                print(f"⚠️ 进入下一天失败: {e}")
        
        print(f"\n完成，共 {self.post_count} 次操作")


if __name__ == "__main__":
    client = NeverlandAPIClient(API_KEY, FARM_ID)
    SmartFarmManager(client).run()
