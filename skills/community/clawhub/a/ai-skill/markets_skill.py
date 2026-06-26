"""
ClawMarkets OpenClaw Skill - 核心交易功能
AI 可以连接市场、创建市场、买卖份额、查询持仓和交易历史
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class OrderType(Enum):
    """订单类型"""
    BUY = "buy"
    SELL = "sell"


@dataclass
class MarketConfig:
    """市场配置"""
    name: str
    description: str
    initial_price: float = 100.0
    total_shares: int = 10000
    creator: Optional[str] = None


class ClawMarketsSkill:
    """ClawMarkets 交易技能核心类"""

    def __init__(self, api_base_url: str = "http://localhost:8080", api_key: Optional[str] = None):
        """
        初始化 ClawMarkets 技能

        Args:
            api_base_url: API 基础 URL
            api_key: API 密钥（可选）
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
        self.connected = False

    async def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def connect(self) -> bool:
        """
        连接到 ClawMarkets API

        Returns:
            bool: 连接是否成功
        """
        try:
            self.session = aiohttp.ClientSession()
            # 测试连接
            async with self.session.get(
                f"{self.api_base_url}/health",
                headers=await self._get_headers(),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    self.connected = True
                    print(f"✅ 成功连接到 ClawMarkets API: {self.api_base_url}")
                    return True
                else:
                    print(f"❌ 连接失败，状态码：{response.status}")
                    return False
        except Exception as e:
            print(f"❌ 连接错误：{e}")
            self.connected = False
            return False

    async def disconnect(self):
        """断开连接"""
        if self.session:
            await self.session.close()
            self.session = None
            self.connected = False
            print("🔌 已断开连接")

    async def create_market(
        self,
        name: str,
        description: str,
        initial_price: float = 100.0,
        total_shares: int = 10000
    ) -> Optional[Dict[str, Any]]:
        """
        创建新市场

        Args:
            name: 市场名称
            description: 市场描述
            initial_price: 初始价格
            total_shares: 总份额

        Returns:
            Dict: 创建的市场信息，失败返回 None
        """
        if not self.connected:
            print("❌ 未连接到 API，请先调用 connect()")
            return None

        try:
            payload = {
                "name": name,
                "description": description,
                "initial_price": initial_price,
                "total_shares": total_shares
            }

            async with self.session.post(
                f"{self.api_base_url}/api/v1/markets",
                json=payload,
                headers=await self._get_headers()
            ) as response:
                result = await response.json()
                if response.status in [200, 201]:
                    print(f"✅ 市场创建成功：{name} (ID: {result.get('id', 'N/A')})")
                    return result
                else:
                    print(f"❌ 创建市场失败：{result.get('error', '未知错误')}")
                    return None
        except Exception as e:
            print(f"❌ 创建市场错误：{e}")
            return None

    async def buy(
        self,
        market_id: str,
        shares: int,
        max_price: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        买入份额

        Args:
            market_id: 市场 ID
            shares: 购买份额数量
            max_price: 最高限价（可选，市价单为 None）

        Returns:
            Dict: 订单信息，失败返回 None
        """
        if not self.connected:
            print("❌ 未连接到 API，请先调用 connect()")
            return None

        try:
            payload = {
                "market_id": market_id,
                "shares": shares,
                "order_type": "buy"
            }
            if max_price is not None:
                payload["max_price"] = max_price

            async with self.session.post(
                f"{self.api_base_url}/api/v1/orders",
                json=payload,
                headers=await self._get_headers()
            ) as response:
                result = await response.json()
                if response.status in [200, 201]:
                    print(f"✅ 买入成功：{shares} 份额 @ {result.get('price', 'N/A')}")
                    return result
                else:
                    print(f"❌ 买入失败：{result.get('error', '未知错误')}")
                    return None
        except Exception as e:
            print(f"❌ 买入错误：{e}")
            return None

    async def sell(
        self,
        market_id: str,
        shares: int,
        min_price: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        卖出份额

        Args:
            market_id: 市场 ID
            shares: 卖出份额数量
            min_price: 最低限价（可选，市价单为 None）

        Returns:
            Dict: 订单信息，失败返回 None
        """
        if not self.connected:
            print("❌ 未连接到 API，请先调用 connect()")
            return None

        try:
            payload = {
                "market_id": market_id,
                "shares": shares,
                "order_type": "sell"
            }
            if min_price is not None:
                payload["min_price"] = min_price

            async with self.session.post(
                f"{self.api_base_url}/api/v1/orders",
                json=payload,
                headers=await self._get_headers()
            ) as response:
                result = await response.json()
                if response.status in [200, 201]:
                    print(f"✅ 卖出成功：{shares} 份额 @ {result.get('price', 'N/A')}")
                    return result
                else:
                    print(f"❌ 卖出失败：{result.get('error', '未知错误')}")
                    return None
        except Exception as e:
            print(f"❌ 卖出错误：{e}")
            return None

    async def get_positions(self, market_id: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        获取持仓信息

        Args:
            market_id: 市场 ID（可选，None 返回所有持仓）

        Returns:
            List[Dict]: 持仓列表，失败返回 None
        """
        if not self.connected:
            print("❌ 未连接到 API，请先调用 connect()")
            return None

        try:
            url = f"{self.api_base_url}/api/v1/positions"
            if market_id:
                url += f"?market_id={market_id}"

            async with self.session.get(
                url,
                headers=await self._get_headers()
            ) as response:
                result = await response.json()
                if response.status == 200:
                    positions = result.get('positions', [])
                    print(f"📊 持仓数量：{len(positions)}")
                    return positions
                else:
                    print(f"❌ 获取持仓失败：{result.get('error', '未知错误')}")
                    return None
        except Exception as e:
            print(f"❌ 获取持仓错误：{e}")
            return None

    async def get_trades(
        self,
        market_id: Optional[str] = None,
        limit: int = 50
    ) -> Optional[List[Dict[str, Any]]]:
        """
        获取交易历史

        Args:
            market_id: 市场 ID（可选）
            limit: 返回数量限制

        Returns:
            List[Dict]: 交易历史列表，失败返回 None
        """
        if not self.connected:
            print("❌ 未连接到 API，请先调用 connect()")
            return None

        try:
            url = f"{self.api_base_url}/api/v1/trades?limit={limit}"
            if market_id:
                url += f"&market_id={market_id}"

            async with self.session.get(
                url,
                headers=await self._get_headers()
            ) as response:
                result = await response.json()
                if response.status == 200:
                    trades = result.get('trades', [])
                    print(f"📜 交易记录数量：{len(trades)}")
                    return trades
                else:
                    print(f"❌ 获取交易历史失败：{result.get('error', '未知错误')}")
                    return None
        except Exception as e:
            print(f"❌ 获取交易历史错误：{e}")
            return None

    async def get_market_info(self, market_id: str) -> Optional[Dict[str, Any]]:
        """
        获取市场信息

        Args:
            market_id: 市场 ID

        Returns:
            Dict: 市场信息，失败返回 None
        """
        if not self.connected:
            print("❌ 未连接到 API，请先调用 connect()")
            return None

        try:
            async with self.session.get(
                f"{self.api_base_url}/api/v1/markets/{market_id}",
                headers=await self._get_headers()
            ) as response:
                result = await response.json()
                if response.status == 200:
                    return result
                else:
                    print(f"❌ 获取市场信息失败：{result.get('error', '未知错误')}")
                    return None
        except Exception as e:
            print(f"❌ 获取市场信息错误：{e}")
            return None


# 便捷函数（面向 OpenClaw Skill 接口）
async def connect(api_base_url: str = "http://localhost:8080", api_key: Optional[str] = None) -> ClawMarketsSkill:
    """连接市场"""
    skill = ClawMarketsSkill(api_base_url, api_key)
    await skill.connect()
    return skill


async def create_market(skill: ClawMarketsSkill, name: str, description: str, **kwargs) -> Optional[Dict]:
    """创建市场"""
    return await skill.create_market(name, description, **kwargs)


async def buy(skill: ClawMarketsSkill, market_id: str, shares: int, **kwargs) -> Optional[Dict]:
    """买入份额"""
    return await skill.buy(market_id, shares, **kwargs)


async def sell(skill: ClawMarketsSkill, market_id: str, shares: int, **kwargs) -> Optional[Dict]:
    """卖出份额"""
    return await skill.sell(market_id, shares, **kwargs)


async def get_positions(skill: ClawMarketsSkill, market_id: Optional[str] = None) -> Optional[List]:
    """获取持仓"""
    return await skill.get_positions(market_id)


async def get_trades(skill: ClawMarketsSkill, market_id: Optional[str] = None, limit: int = 50) -> Optional[List]:
    """获取交易历史"""
    return await skill.get_trades(market_id, limit)
