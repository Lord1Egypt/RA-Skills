#!/usr/bin/env python3
"""
Gas Monitor - Gas费用监控
"""

import time
from web3 import Web3


class GasMonitor:
    """Gas费用监控器 / Gas Fee Monitor"""
    
    def __init__(self, network: str = "mainnet"):
        from wallet_manager import NETWORKS
        
        self.network = network
        self.rpc_url = NETWORKS.get(network, NETWORKS["mainnet"])
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
    
    def get_gas_prices(self) -> dict:
        """获取当前Gas价格 / Get current gas prices"""
        if not self.w3.is_connected():
            raise ConnectionError("Cannot connect to network")
        
        # Get latest block to estimate gas prices
        latest_block = self.w3.eth.get_block('latest')
        base_fee = latest_block.get('baseFeePerGas', 0)
        
        # Standard gas price
        gas_price = self.w3.eth.gas_price
        
        # Estimate priority fees
        slow = int(gas_price * 0.8)
        standard = gas_price
        fast = int(gas_price * 1.2)
        
        return {
            "slow": {
                "gwei": self.w3.from_wei(slow, 'gwei'),
                "eth": self.w3.from_wei(slow, 'ether')
            },
            "standard": {
                "gwei": self.w3.from_wei(standard, 'gwei'),
                "eth": self.w3.from_wei(standard, 'ether')
            },
            "fast": {
                "gwei": self.w3.from_wei(fast, 'gwei'),
                "eth": self.w3.from_wei(fast, 'ether')
            },
            "base_fee_gwei": self.w3.from_wei(base_fee, 'gwei') if base_fee else 0
        }
    
    def monitor(self, interval: int = 60, callback=None):
        """
        持续监控Gas价格 / Continuously monitor gas prices
        
        Args:
            interval: 检查间隔(秒)
            callback: 价格变化时的回调函数
        """
        print(f"Starting gas price monitor on {self.network}...")
        print(f"Update interval: {interval}s")
        print("-" * 50)
        
        last_prices = None
        
        try:
            while True:
                prices = self.get_gas_prices()
                
                if last_prices != prices:
                    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}]")
                    print(f"Slow: {prices['slow']['gwei']:.2f} Gwei")
                    print(f"Standard: {prices['standard']['gwei']:.2f} Gwei")
                    print(f"Fast: {prices['fast']['gwei']:.2f} Gwei")
                    
                    if callback:
                        callback(prices)
                    
                    last_prices = prices
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nMonitor stopped.")


def main():
    """示例用法 / Example usage"""
    print("=" * 50)
    print("Ethereum Gas Price Monitor")
    print("=" * 50)
    
    monitor = GasMonitor("mainnet")
    prices = monitor.get_gas_prices()
    
    print("\nCurrent Gas Prices:")
    print(f"  Slow: {prices['slow']['gwei']:.2f} Gwei")
    print(f"  Standard: {prices['standard']['gwei']:.2f} Gwei")
    print(f"  Fast: {prices['fast']['gwei']:.2f} Gwei")
    
    print("\n" + "=" * 50)
    print("\nTo start continuous monitoring:")
    print("  monitor.monitor(interval=60)")


if __name__ == "__main__":
    main()
