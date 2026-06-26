#!/usr/bin/env python3
"""
1inch DEX 交易功能
提供代币交换交易的执行功能
"""

from typing import Dict, Optional, Any
from oneinch_client import OneInchClient
import json


class OneInchSwap:
    """1inch DEX 交易器"""
    
    def __init__(self, api_key: str):
        """
        初始化 1inch 交易器
        
        Args:
            api_key: 1inch API 密钥
        """
        self.client = OneInchClient(api_key=api_key)
    
    def get_best_quote(self, chain_id: int, from_token_address: str,
                       to_token_address: str, amount: str) -> Dict[str, Any]:
        """
        获取最优报价
        
        Args:
            chain_id: 链 ID
            from_token_address: 输入代币地址
            to_token_address: 输出代币地址
            amount: 输入数量
            
        Returns:
            报价信息
        """
        return self.client.get_quote(
            chain_id=chain_id,
            from_token_address=from_token_address,
            to_token_address=to_token_address,
            amount=amount
        )
    
    def swap(self, chain_id: int, from_token_address: str,
             to_token_address: str, amount: str,
             from_address: str, slippage: float = 1.0,
             disable_estimate: bool = False,
             allow_partial_fill: bool = False) -> Dict[str, Any]:
        """
        执行代币交换
        
        Args:
            chain_id: 链 ID
            from_token_address: 输入代币地址
            to_token_address: 输出代币地址
            amount: 输入数量 (最小单位)
            from_address: 发送方地址
            slippage: 滑点容忍度 (百分比，默认 1%)
            disable_estimate: (可选) 禁用 Gas 估算
            allow_partial_fill: (可选) 允许部分成交
            
        Returns:
            交易数据，包含：
            - tx: 交易对象
              - from: 发送方
              - to: 合约地址
              - data: 交易数据
              - value: 发送的 ETH 数量
              - gasPrice: Gas 价格
              - gas: Gas 限制
            - toTokenAmount: 预计输出数量
            - fromTokenAmount: 输入数量
            
        Example:
            >>> swap = OneInchSwap(api_key="your_key")
            >>> tx_data = swap.swap(
            ...     chain_id=1,
            ...     from_token_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            ...     to_token_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            ...     amount="1000000000000000000",
            ...     from_address="0xUser...",
            ...     slippage=1
            ... )
            >>> # 使用 tx_data['tx'] 构建和发送交易
        """
        params = {
            "src": from_token_address,
            "dst": to_token_address,
            "amount": amount,
            "fromAddress": from_address,
            "slippage": slippage
        }
        
        if disable_estimate:
            params["disableEstimate"] = "true"
        if allow_partial_fill:
            params["allowPartialFill"] = "true"
        
        # 获取交换交易数据
        swap_response = self.client._make_request("GET", "swap", params=params)
        
        # 构建完整的交换数据
        swap_data = {
            "transaction": swap_response.get("tx", {}),
            "to_token_amount": swap_response.get("toTokenAmount"),
            "from_token_amount": swap_response.get("fromTokenAmount"),
            "from_token": swap_response.get("fromToken"),
            "to_token": swap_response.get("toToken"),
            "protocols": swap_response.get("protocols", []),
            "estimated_gas": swap_response.get("estimatedGas")
        }
        
        return swap_data
    
    def check_approval_needed(self, token_address: str, amount: str,
                             owner_address: str, chain_id: int) -> Dict[str, Any]:
        """
        检查是否需要授权代币
        
        Args:
            token_address: 代币地址
            amount: 交易数量
            owner_address: 代币所有者地址
            chain_id: 链 ID
            
        Returns:
            授权检查结果
        """
        # 获取 spender 地址
        spender_info = self.client.get_spender(chain_id=chain_id)
        spender_address = spender_info.get("address")
        
        # 获取授权交易数据
        approval_data = self.client.get_approve_call_data(
            chain_id=chain_id,
            token_address=token_address,
            amount=amount,
            spender_address=spender_address
        )
        
        result = {
            "needs_approval": True,  # 默认需要授权
            "spender_address": spender_address,
            "approval_data": approval_data
        }
        
        return result
    
    def build_approval_transaction(self, chain_id: int, token_address: str,
                                   amount: str) -> Dict[str, Any]:
        """
        构建代币授权交易
        
        Args:
            chain_id: 链 ID
            token_address: 代币地址
            amount: 授权数量
            
        Returns:
            授权交易数据
        """
        approval_data = self.client.get_approve_call_data(
            chain_id=chain_id,
            token_address=token_address,
            amount=amount
        )
        
        return approval_data.get("tx", {})
    
    def execute_swap(self, swap_data: Dict[str, Any],
                    private_key: Optional[str] = None) -> Dict[str, Any]:
        """
        执行代币交换交易
        
        Args:
            swap_data: 交换数据 (从 swap() 方法获取)
            private_key: (可选) 私钥用于签名交易
            
        Returns:
            交易结果
        """
        tx = swap_data.get("transaction", {})
        
        if not tx:
            raise ValueError("无效的交易数据")
        
        result = {
            "status": "pending",
            "from_token": swap_data.get("from_token", {}),
            "to_token": swap_data.get("to_token", {}),
            "from_amount": swap_data.get("from_token_amount"),
            "to_amount": swap_data.get("to_token_amount"),
            "transaction_hash": None,
            "message": "交易已准备，需要签名和广播"
        }
        
        if private_key:
            print("⚠️  注意：实际交易执行需要 Web3 库和 RPC 节点")
            print(f"   交易数据：{json.dumps(tx, indent=2)}")
        
        return result
    
    def get_price_impact(self, chain_id: int, from_token_address: str,
                         to_token_address: str, amount: str) -> Dict[str, Any]:
        """
        获取价格影响信息
        
        Args:
            chain_id: 链 ID
            from_token_address: 输入代币地址
            to_token_address: 输出代币地址
            amount: 输入数量
            
        Returns:
            价格影响信息
        """
        quote = self.client.get_quote(
            chain_id=chain_id,
            from_token_address=from_token_address,
            to_token_address=to_token_address,
            amount=amount
        )
        
        # 1inch 报价包含详细信息
        price_impact_info = {
            "from_token": quote.get("fromToken"),
            "to_token": quote.get("toToken"),
            "from_amount": quote.get("fromTokenAmount"),
            "to_amount": quote.get("toTokenAmount"),
            "protocols": quote.get("protocols"),
            "estimated_gas": quote.get("estimatedGas")
        }
        
        return price_impact_info
    
    def get_router_address(self, chain_id: int) -> str:
        """
        获取 1inch 路由器地址
        
        Args:
            chain_id: 链 ID
            
        Returns:
            路由器地址
        """
        spender_info = self.client.get_spender(chain_id=chain_id)
        return spender_info.get("address", "")


def main():
    """测试交易功能"""
    # 注意：需要有效的 API 密钥才能测试
    api_key = "your_api_key_here"  # 替换为实际密钥
    
    print("测试 1inch DEX 交易")
    print("=" * 50)
    
    # 示例：ETH -> USDC
    chain_id = 1  # Ethereum
    from_token = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # WETH
    to_token = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
    amount = "1000000000000000000"  # 1 ETH
    from_address = "0x0000000000000000000000000000000000000000"
    
    print(f"\nDEX 交易示例:")
    print(f"  链：{chain_id} (Ethereum)")
    print(f"  输入：WETH")
    print(f"  输出：USDC")
    print(f"  数量：1 ETH")
    
    try:
        print("\n获取最优报价...")
        swap = OneInchSwap(api_key=api_key)
        quote = swap.get_best_quote(
            chain_id=chain_id,
            from_token_address=from_token,
            to_token_address=to_token,
            amount=amount
        )
        print(f"✓ 成功获取报价")
        print(f"  输出数量：{quote.get('toTokenAmount')}")
        print(f"  预估 Gas: {quote.get('estimatedGas')}")
        protocols = quote.get("protocols", [])
        print(f"  使用协议数量：{len(protocols)}")
    except Exception as e:
        print(f"✗ 获取报价失败：{e}")
        print(f"  提示：需要有效的 API 密钥")
    
    try:
        print("\n获取路由器地址...")
        router = swap.get_router_address(chain_id=chain_id)
        print(f"✓ 路由器地址：{router}")
    except Exception as e:
        print(f"✗ 获取路由器失败：{e}")


if __name__ == "__main__":
    main()
