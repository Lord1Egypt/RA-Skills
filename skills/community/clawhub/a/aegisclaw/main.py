#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金甲龙虾 (AegisClaw) - 主入口
既可作为 CLI 运行，也可作为 OpenClaw 插件使用
"""

import os
import sys
import argparse
from typing import Optional

# 设置输出编码为 UTF-8
if sys.platform == "win32":
    import codecs
    # 只在第一次输出时设置编码
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from core.api_client import BinanceAPIClient
from core.security_checker import SecurityChecker
from core.asset_scanner import AssetScanner
from core.funding_arbitrage import FundingArbitrage
from core.report_generator import ReportGenerator
from db.database import Database


class AegisClaw:
    """金甲龙虾主类"""

    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = False):
        # 从环境变量或参数读取配置
        self.api_key = api_key or config.binance.api_key
        self.api_secret = api_secret or config.binance.api_secret
        self.testnet = testnet or config.binance.testnet

        # 初始化组件
        self.api_client = None
        self.database = None
        self.security_checker = None
        self.asset_scanner = None
        self.arbitrage = None
        self.report_generator = None

    def initialize(self):
        """初始化组件"""
        if not self.api_key or not self.api_secret:
            raise ValueError("缺少 API Key 或 Secret。请设置环境变量或传入参数。")

        # 更新配置
        config.binance.api_key = self.api_key
        config.binance.api_secret = self.api_secret
        config.binance.testnet = self.testnet

        # 初始化客户端和组件
        self.api_client = BinanceAPIClient(config.binance)
        self.database = Database(config.database.path)
        self.security_checker = SecurityChecker(self.api_client, config.binance)
        self.asset_scanner = AssetScanner(self.api_client, config.strategy)
        self.arbitrage = FundingArbitrage(self.api_client, config.strategy)
        self.report_generator = ReportGenerator(self.api_client, self.database)

        print("🦞 金甲龙虾已初始化")
        print("=" * 40)

    # ========== 核心功能 ==========

    def security_check(self) -> str:
        """运行安全检查"""
        print("\n🛡️ 运行安全围栏检查...\n")
        result = self.security_checker.run_full_check()
        self.database.save_security_check(result)
        return self.security_checker.format_report(result)

    def scan_assets(self) -> str:
        """扫描资产"""
        print("\n📊 扫描资产...\n")
        result = self.asset_scanner.scan_idle_assets()
        return self.asset_scanner.format_report(result)

    def scan_arbitrage(self, symbols: Optional[list] = None) -> str:
        """扫描套利机会"""
        print("\n📈 扫描套利机会...\n")
        opportunities = self.arbitrage.scan_arbitrage_opportunities(symbols)
        return self.arbitrage.format_report(opportunities)

    def dust_sweep(self, assets: Optional[list] = None) -> str:
        """零钱兑换"""
        print("\n🧹 执行零钱兑换...\n")
        result = self.asset_scanner.execute_dust_sweep(assets)
        return result.get("message", "")

    def weekly_report(self) -> str:
        """生成周报"""
        print("\n📊 生成周收益战报...\n")
        report = self.report_generator.generate_weekly_report()
        return self.report_generator.format_text_report(report)

    def status(self) -> str:
        """查看状态"""
        print("\n📌 查看状态...\n")
        balances = self.api_client.get_balances()
        self.report_generator.save_snapshot(balances)

        bnb = next((b for b in balances if b["asset"] == "BNB"), {"total": 0})["total"]
        usdt = next((b for b in balances if b["asset"] == "USDT"), {"free": 0})["free"]

        status = f"""
🦞 金甲龙虾状态
{'='*30}

🔌 API 连接: ✅ 正常
📊 资产数量: {len(balances)}
💎 BNB 余额: {bnb:.4f}
💵 USDT 余额: {usdt:.2f}
"""
        return status

    def run_all_checks(self) -> str:
        """运行所有检查"""
        output = []
        output.append(self.security_check())
        output.append(self.scan_assets())
        output.append(self.scan_arbitrage())
        return "\n".join(output)


def main():
    """CLI 入口"""
    parser = argparse.ArgumentParser(
        description="🦞 金甲龙虾 - 币安安全赚币与护境神将",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --check              # 运行安全检查
  python main.py --scan               # 扫描资产
  python main.py --arbitrage          # 扫描套利
  python main.py --dust               # 兑换零钱
  python main.py --report             # 生成周报
  python main.py --all                # 运行所有检查
  python main.py --testnet            # 使用测试网
        """
    )

    parser.add_argument("--key", help="Binance API Key")
    parser.add_argument("--secret", help="Binance API Secret")
    parser.add_argument("--testnet", action="store_true", help="使用测试网")
    parser.add_argument("--check", action="store_true", help="运行安全检查")
    parser.add_argument("--scan", action="store_true", help="扫描资产")
    parser.add_argument("--arbitrage", action="store_true", help="扫描套利机会")
    parser.add_argument("--dust", action="store_true", help="兑换零钱")
    parser.add_argument("--report", action="store_true", help="生成周报")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--all", action="store_true", help="运行所有检查")

    args = parser.parse_args()

    # 如果没有指定任何操作，显示帮助
    if not any([args.check, args.scan, args.arbitrage, args.dust, args.report, args.status, args.all]):
        parser.print_help()
        return

    # 初始化
    try:
        claw = AegisClaw(args.key, args.secret, args.testnet)
        claw.initialize()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return

    # 执行命令
    try:
        if args.all:
            print(claw.run_all_checks())
        elif args.check:
            print(claw.security_check())
        elif args.scan:
            print(claw.scan_assets())
        elif args.arbitrage:
            print(claw.scan_arbitrage())
        elif args.dust:
            print(claw.dust_sweep())
        elif args.report:
            print(claw.weekly_report())
        elif args.status:
            print(claw.status())
    except Exception as e:
        import traceback
        print(f"❌ 执行失败: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
