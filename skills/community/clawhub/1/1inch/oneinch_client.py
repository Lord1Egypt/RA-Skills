#!/usr/bin/env python3
"""
1inch API 客户端
提供与 1inch DEX 聚合器 API v5.2 的交互功能
"""

import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class QuoteRequest:
    """交易报价请求参数"""
    chain_id: int
    from_token_address: str
    to_token_address: str
    amount: str
    protocols: Optional[str] = None
    gas_price: Optional[str] = None
    complexity_level: int = 2


@dataclass
class QuoteResponse:
    """交易报价响应"""
    from_token: Dict
    to_token: Dict
    from_token_amount: str
    to_token_amount: str
    protocols: List
    estimated_gas: int


class OneInchClient:
    """1inch API 客户端"""
    
    BASE_URL = "https://api.1inch.dev/swap/v5.2"
    
    def __init__(self, api_key: str):
        """
        初始化 1inch 客户端
        
        Args:
            api_key: 1inch API 密钥 (必需)
        """
        if not api_key:
            raise ValueError("1inch API 密钥是必需的")
        
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
    
    def _make_request(self, method: str, endpoint: str,
                      params: Optional[Dict] = None,
                      data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送 HTTP 请求
        
        Args:
            method: HTTP 方法 (GET/POST)
            endpoint: API 端点
            params: 查询参数
            data: 请求体数据
            
        Returns:
            API 响应数据
            
        Raises:
            requests.RequestException: 请求失败
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params, json=data, timeout=30)
            else:
                raise ValueError(f"不支持的 HTTP 方法：{method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP 错误：{e.response.status_code}"
            try:
                error_data = e.response.json()
                error_msg += f" - {error_data.get('description', error_data.get('message', '未知错误'))}"
            except:
                pass
            raise requests.RequestException(error_msg)
    
    def get_quote(self, chain_id: int, from_token_address: str,
                  to_token_address: str, amount: str,
                  protocols: Optional[str] = None,
                  gas_price: Optional[str] = None,
                  complexity_level: int = 2) -> Dict[str, Any]:
        """
        获取交易报价
        
        Args:
            chain_id: 链 ID (1=Ethereum, 56=BSC, 137=Polygon, etc.)
            from_token_address: 输入代币地址
            to_token_address: 输出代币地址
            amount: 输入数量 (最小单位)
            protocols: (可选) 指定使用的协议，逗号分隔
            gas_price: (可选) Gas 价格
            complexity_level: (可选) 路由复杂度级别 (1-3)
            
        Returns:
            报价信息字典，包含：
            - fromToken: 输入代币信息
            - toToken: 输出代币信息
            - fromTokenAmount: 输入数量
            - toTokenAmount: 输出数量
            - protocols: 使用的协议列表
            - estimatedGas: 预估 Gas
            
        Example:
            >>> client = OneInchClient(api_key="your_key")
            >>> quote = client.get_quote(
            ...     chain_id=1,
            ...     from_token_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            ...     to_token_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            ...     amount="1000000000000000000"
            ... )
        """
        params = {
            "src": from_token_address,
            "dst": to_token_address,
            "amount": amount,
            "complexityLevel": complexity_level
        }
        
        if protocols:
            params["protocols"] = protocols
        if gas_price:
            params["gasPrice"] = gas_price
        
        return self._make_request("GET", "quote", params=params)
    
    def get_tokens(self, chain_id: int) -> Dict[str, Any]:
        """
        获取支持的代币列表
        
        Args:
            chain_id: 链 ID
            
        Returns:
            代币列表信息
        """
        params = {"chainId": chain_id}
        return self._make_request("GET", "tokens", params=params)
    
    def get_chains(self) -> Dict[str, Any]:
        """
        获取支持的链列表
        
        Returns:
            链列表信息
        """
        return self._make_request("GET", "chains")
    
    def get_spender(self, chain_id: int) -> Dict[str, Any]:
        """
        获取 1inch 路由器地址 (用于代币授权)
        
        Args:
            chain_id: 链 ID
            
        Returns:
            路由器地址信息
        """
        params = {"chainId": chain_id}
        return self._make_request("GET", "approve/spender", params=params)
    
    def get_approve_call_data(self, chain_id: int, token_address: str,
                              amount: str, spender_address: Optional[str] = None) -> Dict[str, Any]:
        """
        获取代币授权交易数据
        
        Args:
            chain_id: 链 ID
            token_address: 代币地址
            amount: 授权数量
            spender_address: (可选) 被授权地址
            
        Returns:
            授权交易数据
        """
        params = {
            "tokenAddress": token_address,
            "amount": amount,
            "chainId": chain_id
        }
        
        if spender_address:
            params["spenderAddress"] = spender_address
        
        return self._make_request("GET", "approve/transaction", params=params)
    
    def get_rate(self, chain_id: int, from_token_address: str,
                 to_token_address: str, amount: str) -> Dict[str, Any]:
        """
        获取实时汇率
        
        Args:
            chain_id: 链 ID
            from_token_address: 输入代币地址
            to_token_address: 输出代币地址
            amount: 输入数量
            
        Returns:
            汇率信息
        """
        params = {
            "src": from_token_address,
            "dst": to_token_address,
            "amount": amount
        }
        
        return self._make_request("GET", "rate", params=params)


def main():
    """测试客户端功能"""
    # 注意：需要有效的 API 密钥才能测试
    api_key = "your_api_key_here"  # 替换为实际密钥
    
    print("测试 1inch 客户端")
    print("=" * 50)
    
    # 测试获取支持的链
    try:
        print("\n获取支持的链...")
        client = OneInchClient(api_key=api_key)
        chains = client.get_chains()
        print(f"✓ 成功获取链列表")
        chain_list = chains.get("chains", [])
        print(f"  支持的链数量：{len(chain_list)}")
        for chain in chain_list[:5]:
            print(f"    - {chain.get('name')} (ID: {chain.get('id')})")
    except Exception as e:
        print(f"✗ 获取链失败：{e}")
        print(f"  提示：需要有效的 API 密钥")
    
    # 测试获取代币
    try:
        print("\n获取 Ethereum 代币列表...")
        client = OneInchClient(api_key=api_key)
        tokens = client.get_tokens(chain_id=1)
        print(f"✓ 成功获取代币列表")
        token_list = tokens.get("tokens", {})
        print(f"  代币数量：{len(token_list)}")
    except Exception as e:
        print(f"✗ 获取代币失败：{e}")


if __name__ == "__main__":
    main()
