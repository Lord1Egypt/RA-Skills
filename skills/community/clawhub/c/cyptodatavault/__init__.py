"""
DataVault Skill - OpenClaw Skill Integration
DataVault - 全球领先的 Web3 Data Value 平台
"""

import sys
from pathlib import Path

# DataVault - 使用相对导入定位核心 app
# DataVault/skill/__init__.py -> DataVault/app/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.data import get_data_service
from app.onchain.service import OnChainService
from app.external.defillama import get_defillama_client
from typing import Dict, Any, List


class DataVaultSkill:
    """DataVault Skill - OpenClaw Skill Integration
    
    整合 DataVault 核心引擎的 13 个工具，提供统一的 Skill 接口
    """
    
    def __init__(self):
        self.data_service = get_data_service()
        self.onchain_service = OnChainService()
        self._tools = {}
        self._register_all_tools()
    
    def _register_all_tools(self):
        """注册所有工具"""
        
        # Market Data Tools (from data service)
        self._tools["get_price"] = self._get_price
        self._tools["get_all_prices"] = self._get_all_prices
        self._tools["get_funding_rate"] = self._get_funding_rate
        self._tools["get_market_summary"] = self._get_market_summary
        self._tools["get_best_price"] = self._get_best_price
        
        # OnChain Tools (from onchain service)
        self._tools["get_eth_balance"] = self._get_eth_balance
        self._tools["get_eth_transactions"] = self._get_eth_transactions
        self._tools["get_gas_price"] = self._get_gas_price
        
        # DeFi Tools (from defillama)
        self._tools["get_defi_tvl"] = self._get_defi_tvl
        self._tools["get_protocol_tvl"] = self._get_protocol_tvl
        self._tools["get_chain_tvl"] = self._get_chain_tvl
        self._tools["get_yields"] = self._get_yields
        self._tools["get_stablecoins"] = self._get_stablecoins
    
    @property
    def tool_count(self) -> int:
        return len(self._tools)
    
    # Market Data Tools
    def _get_price(self, symbol: str = "BTC/USDT", exchange: str = None) -> Dict[str, Any]:
        return self.data_service.get_price(symbol, exchange)
    
    def _get_all_prices(self, exchange: str = None) -> Dict[str, Any]:
        return self.data_service.get_all_prices(exchange)
    
    def _get_funding_rate(self, symbol: str = "BTC/USDT", exchange: str = None) -> Dict[str, Any]:
        return self.data_service.get_funding_rate(symbol, exchange)
    
    def _get_market_summary(self, exchange: str = None) -> Dict[str, Any]:
        return self.data_service.get_market_summary(exchange)
    
    def _get_best_price(self, symbol: str = "BTC/USDT", exchanges: List[str] = None) -> Dict[str, Any]:
        return self.data_service.get_best_price(symbol, exchanges)
    
    # OnChain Tools
    def _get_eth_balance(self, address: str) -> Dict[str, Any]:
        return self.onchain_service.get_eth_balance(address)
    
    def _get_eth_transactions(self, address: str, limit: int = 20) -> Dict[str, Any]:
        return self.onchain_service.get_eth_transactions(address, limit)
    
    def _get_gas_price(self) -> Dict[str, Any]:
        return self.onchain_service.get_gas_price()
    
    # DeFi Tools
    def _get_defi_tvl(self, chain: str = None) -> Dict[str, Any]:
        return get_defillama_client().get_defi_tvl(chain)
    
    def _get_protocol_tvl(self, protocol: str) -> Dict[str, Any]:
        return get_defillama_client().get_protocol_tvl(protocol)
    
    def _get_chain_tvl(self) -> Dict[str, Any]:
        return get_defillama_client().get_chain_tvl()
    
    def _get_yields(self, protocol: str = None, asset: str = None) -> Dict[str, Any]:
        return get_defillama_client().get_yields(protocol, asset)
    
    def _get_stablecoins(self) -> Dict[str, Any]:
        return get_defillama_client().get_stablecoins()
    
    # Public API
    def get_tools(self) -> List[Dict[str, Any]]:
        return [{"name": name} for name in self._tools.keys()]
    
    def call(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name](**kwargs)
    
    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "version": "1.0.0",
            "tools": self.tool_count
        }


# Singleton instance
_skill_instance = None


def get_skill() -> DataVaultSkill:
    """获取 DataVault Skill 单例"""
    global _skill_instance
    if _skill_instance is None:
        _skill_instance = DataVaultSkill()
    return _skill_instance


def call_tool(name: str, **kwargs):
    """调用指定工具"""
    return get_skill().call(name, **kwargs)


def get_all_tools():
    """获取所有可用工具列表"""
    return get_skill().get_tools()


def main():
    """CLI 入口"""
    skill = get_skill()
    print(f"DataVault Skill: {skill.tool_count} tools")
    print(f"Health: {skill.health()}")
    
    result = skill.call("get_price", symbol="BTC/USDT")
    print(f"BTC/USDT: ${result.get('last')}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())