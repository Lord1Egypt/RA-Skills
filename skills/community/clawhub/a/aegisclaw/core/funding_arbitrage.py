"""
资金费率套利模块 - 检测套利机会
"""

from typing import Dict, List, Optional
from core.api_client import BinanceAPIClient
from config import StrategyConfig


class FundingArbitrage:
    """资金费率套利检测器"""

    def __init__(self, api_client: BinanceAPIClient, config: StrategyConfig):
        self.api_client = api_client
        self.config = config

    def scan_arbitrage_opportunities(self, symbols: List[str] = None) -> List[Dict]:
        """扫描套利机会"""
        opportunities = []

        try:
            # 获取资金费率数据
            funding_data = self.api_client.get_funding_rate()

            for item in funding_data:
                symbol = item["symbol"]
                funding_rate = float(item["fundingRate"])
                mark_price = float(item["markPrice"])

                # 筛选高费率机会
                if abs(funding_rate) >= self.config.funding_rate_threshold:
                    # 获取现货价格
                    try:
                        ticker = self.api_client.get_symbol_ticker(symbol.replace("USDT", "USDT"))
                        spot_price = float(ticker["price"])

                        # 计算价格偏差
                        price_diff_pct = (mark_price - spot_price) / spot_price * 100

                        # 计算预计利润
                        estimated_profit = abs(funding_rate) * 100  # 转换为百分比

                        # 判断是否有套利价值
                        if estimated_profit >= self.config.min_arbitrage_profit * 100:
                            opportunities.append({
                                "symbol": symbol,
                                "spot_price": spot_price,
                                "mark_price": mark_price,
                                "funding_rate": funding_rate,
                                "funding_rate_pct": funding_rate * 100,
                                "price_diff_pct": price_diff_pct,
                                "estimated_profit_pct": estimated_profit,
                                "direction": "long_funding" if funding_rate > 0 else "short_funding",
                                "next_funding_time": item.get("nextFundingTime"),
                                "recommendation": self._get_recommendation(funding_rate, price_diff_pct)
                            })
                    except Exception:
                        # 单个交易对获取失败时跳过
                        pass
        except Exception as e:
            print(f"扫描套利机会失败: {e}")

        # 按利润排序
        opportunities.sort(key=lambda x: x["estimated_profit_pct"], reverse=True)
        return opportunities

    def _get_recommendation(self, funding_rate: float, price_diff_pct: float) -> str:
        """获取操作建议"""
        if funding_rate > 0:
            return f"做多现货，做空合约，收取 {funding_rate*100:.4f}% 资金费"
        else:
            return f"做空现货，做多合约，收取 {-funding_rate*100:.4f}% 资金费"

    def format_report(self, opportunities: List[Dict], top_n: int = 10) -> str:
        """格式化套利报告"""
        report = "📈 资金费率套利机会\n"
        report += "=" * 50 + "\n\n"

        if not opportunities:
            report += "暂无高价值套利机会\n"
            report += f"当前检测阈值: 资金费率 ≥ {self.config.funding_rate_threshold*100:.2f}%\n"
            report += f"最小利润要求: {self.config.min_arbitrage_profit*100:.2f}%\n"
            return report

        top = opportunities[:top_n]
        for i, opp in enumerate(top, 1):
            direction_emoji = "📈" if opp["funding_rate"] > 0 else "📉"

            report += f"{i}. {direction_emoji} {opp['symbol']}\n"
            report += f"   资金费率: {opp['funding_rate_pct']:+.4f}%\n"
            report += f"   现货价格: ${opp['spot_price']:.4f}\n"
            report += f"   标记价格: ${opp['mark_price']:.4f}\n"
            report += f"   价格偏差: {opp['price_diff_pct']:+.2f}%\n"
            report += f"   预计收益: {opp['estimated_profit_pct']:.4f}%\n"
            report += f"   操作建议: {opp['recommendation']}\n\n"

        report += f"⚠️ 提醒: 套利有风险，请使用子账户并控制仓位\n"

        return report
