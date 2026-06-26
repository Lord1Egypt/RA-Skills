"""
战报生成模块 - 生成收益统计和海报
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from core.api_client import BinanceAPIClient
from db.database import Database


class ReportGenerator:
    """战报生成器 - 生成收益统计和分享内容"""

    def __init__(self, api_client: BinanceAPIClient, database: Database):
        self.api_client = api_client
        self.db = database

    def generate_weekly_report(self) -> Dict:
        """生成周报"""
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        # 获取当前余额
        current_balances = self.api_client.get_balances()
        bnb_balance = next((b for b in current_balances if b["asset"] == "BNB"), {"total": 0})["total"]

        # 从数据库获取历史数据
        history = self.db.get_balance_history(week_ago, now)

        # 计算收益
        bnb_start = history[-1]["bnb_amount"] if history else bnb_balance
        bnb_profit = bnb_balance - bnb_start
        bnb_profit_pct = (bnb_profit / bnb_start * 100) if bnb_start > 0 else 0

        # 获取交易记录
        trades = self.db.get_trades(week_ago, now)

        # 计算用户排名（模拟）
        user_rank = self._calculate_user_rank(bnb_profit_pct)

        report = {
            "period": f"{week_ago.strftime('%m/%d')} - {now.strftime('%m/%d')}",
            "bnb_start": bnb_start,
            "bnb_current": bnb_balance,
            "bnb_profit": bnb_profit,
            "bnb_profit_pct": bnb_profit_pct,
            "trade_count": len(trades),
            "user_rank": user_rank,
            "highlights": self._generate_highlights(trades, bnb_profit),
            "recommendations": self._generate_recommendations(current_balances)
        }

        return report

    def _calculate_user_rank(self, profit_pct: float) -> int:
        """模拟用户排名（实际需要真实数据对比）"""
        # 简单模拟：收益率越高排名越好
        if profit_pct < 0:
            return 90 + int(abs(profit_pct) * 10)
        elif profit_pct < 1:
            return 60 + int((1 - profit_pct) * 30)
        elif profit_pct < 3:
            return 30 + int((3 - profit_pct) * 15)
        elif profit_pct < 5:
            return 10 + int((5 - profit_pct) * 5)
        else:
            return max(1, 10 - int((profit_pct - 5) * 2))

    def _generate_highlights(self, trades: List[Dict], bnb_profit: float) -> List[str]:
        """生成亮点"""
        highlights = []

        if bnb_profit > 0:
            highlights.append(f"🎉 本周净赚 {bnb_profit:.4f} BNB")

        # 统计操作类型
        dust_sweeps = sum(1 for t in trades if t.get("type") == "dust_sweep")
        arbitrages = sum(1 for t in trades if t.get("type") == "arbitrage")

        if dust_sweeps > 0:
            highlights.append(f"🧹 执行了 {dust_sweeps} 次零钱兑换")
        if arbitrages > 0:
            highlights.append(f"📈 执行了 {arbitrages} 次资金费率套利")

        return highlights

    def _generate_recommendations(self, balances: List[Dict]) -> List[str]:
        """生成建议"""
        recommendations = []

        # 检查闲置资金
        idle_usdt = next((b for b in balances if b["asset"] == "USDT"), {"free": 0})["free"]
        if idle_usdt > 50:
            recommendations.append(f"💡 有 ${idle_usdt:.2f} USDT 闲置，考虑参与 Launchpool")

        # 检查 BNB 余额
        bnb = next((b for b in balances if b["asset"] == "BNB"), {"total": 0})["total"]
        if bnb < 0.5:
            recommendations.append("🦞 BNB 余额不足 0.5，建议增加持有")

        return recommendations

    def format_text_report(self, report: Dict) -> str:
        """格式化文本报告"""
        text = "🦞 金甲龙虾 - 周收益战报\n"
        text += "=" * 40 + "\n\n"

        text += f"📅 统计周期: {report['period']}\n\n"

        text += "💰 收益汇总:\n"
        text += f"  • 本期初 BNB: {report['bnb_start']:.4f}\n"
        text += f"  • 本期末 BNB: {report['bnb_current']:.4f}\n"

        if report['bnb_profit'] >= 0:
            text += f"  • 净增 BNB: +{report['bnb_profit']:.4f} ({report['bnb_profit_pct']:+.2f}%)\n"
        else:
            text += f"  • 净减 BNB: {report['bnb_profit']:.4f} ({report['bnb_profit_pct']:+.2f}%)\n"

        text += f"  • 用户排名: 超越 {report['user_rank']}% 用户\n\n"

        text += "📊 操作统计:\n"
        text += f"  • 交易次数: {report['trade_count']}\n\n"

        if report['highlights']:
            text += "✨ 本周亮点:\n"
            for h in report['highlights']:
                text += f"  {h}\n"
            text += "\n"

        if report['recommendations']:
            text += "💡 建议:\n"
            for r in report['recommendations']:
                text += f"  {r}\n"

        text += "\n🚀 #AIBinance #金甲龙虾 #BNB本位\n"

        return text

    def generate_poster_data(self, report: Dict) -> Dict:
        """生成海报数据（可用于生成图片）"""
        return {
            "title": "🦞 金甲龙虾周报",
            "period": report["period"],
            "bnb_profit": f"{report['bnb_profit']:+.4f}",
            "bnb_profit_pct": f"{report['bnb_profit_pct']:+.2f}%",
            "bnb_current": f"{report['bnb_current']:.4f}",
            "user_rank": f"超越 {report['user_rank']}% 用户",
            "highlights": report["highlights"],
            "hashtags": "#AIBinance #金甲龙虾 #BNB本位",
            "footer": "Powered by AegisClaw - AI守护您的加密资产"
        }

    def save_snapshot(self, balances: List[Dict]) -> bool:
        """保存余额快照到数据库"""
        try:
            bnb = next((b for b in balances if b["asset"] == "BNB"), {"total": 0})["total"]
            usdt = next((b for b in balances if b["asset"] == "USDT"), {"total": 0})["total"]

            self.db.save_balance_snapshot({
                "bnb_amount": bnb,
                "usdt_amount": usdt,
                "total_assets": len(balances),
                "timestamp": datetime.now()
            })
            return True
        except Exception as e:
            print(f"保存快照失败: {e}")
            return False
