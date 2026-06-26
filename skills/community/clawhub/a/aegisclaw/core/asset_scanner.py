"""
资产扫描模块 - 检测闲置资金和零钱兑换
"""

from typing import Dict, List, Optional
from core.api_client import BinanceAPIClient
from config import StrategyConfig


class AssetScanner:
    """资产扫描器 - 检测闲置资金和零钱"""

    def __init__(self, api_client: BinanceAPIClient, config: StrategyConfig):
        self.api_client = api_client
        self.config = config

    def scan_idle_assets(self, min_idle_usdt: float = 5.0) -> Dict[str, any]:
        """扫描闲置资产"""
        result = {
            "idle_usdt": 0.0,
            "idle_fdusd": 0.0,
            "idle_total": 0.0,
            "dust_assets": [],
            "dust_total_value": 0.0,
            "suggestions": []
        }

        try:
            balances = self.api_client.get_balances()
            asset_detail = self.api_client.get_asset_detail()

            # 扫描闲置稳定币
            for b in balances:
                if b["asset"] == "USDT":
                    idle = b["free"]
                    if idle >= min_idle_usdt:
                        result["idle_usdt"] = idle
                        result["idle_total"] += idle
                        if idle >= self.config.min_launchpool_amount:
                            result["suggestions"].append({
                                "type": "launchpool",
                                "asset": "USDT",
                                "amount": idle,
                                "message": f"检测到 {idle:.2f} USDT 闲置，可参与 Launchpool 赚取新币"
                            })

                elif b["asset"] == "FDUSD":
                    idle = b["free"]
                    if idle >= min_idle_usdt:
                        result["idle_fdusd"] = idle
                        result["idle_total"] += idle
                        if idle >= self.config.min_launchpool_amount:
                            result["suggestions"].append({
                                "type": "launchpool",
                                "asset": "FDUSD",
                                "amount": idle,
                                "message": f"检测到 {idle:.2f} FDUSD 闲置，可参与 Launchpool 赚取新币"
                            })

            # 扫描零钱（小额资产）
            dust_assets = self._scan_dust_assets(balances, asset_detail)
            result["dust_assets"] = dust_assets["assets"]
            result["dust_total_value"] = dust_assets["total_value"]

            if result["dust_total_value"] >= self.config.min_dust_threshold:
                result["suggestions"].append({
                    "type": "dust_sweep",
                    "assets": dust_assets["asset_list"],
                    "total_value": result["dust_total_value"],
                    "message": f"发现 {len(dust_assets['asset_list'])} 种零钱，总价值约 ${result['dust_total_value']:.2f}，建议兑换为 BNB"
                })

        except Exception as e:
            result["error"] = str(e)

        return result

    def _scan_dust_assets(self, balances: List[Dict], asset_detail: Dict) -> Dict:
        """扫描可兑换的零钱资产"""
        dust_assets = {
            "assets": [],
            "asset_list": [],
            "total_value": 0.0
        }

        # 获取 BNB/USDT 价格用于估值
        try:
            bnb_price = float(self.api_client.get_symbol_ticker("BNBUSDT")["price"])
        except:
            bnb_price = 300.0  # 默认估值

        for b in balances:
            asset = b["asset"]
            total = b["total"]

            # 跳过主要资产
            if asset in ["USDT", "FDUSD", "BNB", "BTC", "ETH"]:
                continue

            # 检查是否为零钱（通过资产详情获取最小交易量）
            asset_info = asset_detail.get(asset, {})
            min_trade = float(asset_info.get("minTradeAmount", 5))

            if total < min_trade:
                # 获取当前价格估算价值
                try:
                    price = float(self.api_client.get_symbol_ticker(f"{asset}USDT")["price"])
                    usdt_value = total * price
                except:
                    # 尝试通过 BNB 交易对
                    try:
                        price = float(self.api_client.get_symbol_ticker(f"{asset}BNB")["price"])
                        usdt_value = total * price * bnb_price
                    except:
                        usdt_value = 0

                if usdt_value > 0:
                    dust_assets["assets"].append({
                        "asset": asset,
                        "amount": total,
                        "usdt_value": usdt_value
                    })
                    dust_assets["asset_list"].append(asset)
                    dust_assets["total_value"] += usdt_value

        return dust_assets

    def execute_dust_sweep(self, assets: List[str] = None) -> Dict:
        """执行零钱兑换"""
        if assets is None:
            scan = self.scan_idle_assets()
            assets = [a["asset"] for a in scan.get("dust_assets", [])]

        if not assets:
            return {"success": False, "message": "没有可兑换的零钱"}

        try:
            # 使用 dust_transfer 接口兑换为 BNB
            result = self.api_client.dust_transfer(assets)
            return {
                "success": True,
                "result": result,
                "message": f"已将 {', '.join(assets)} 兑换为 BNB"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"兑换失败: {str(e)}"
            }

    def get_launchpool_opportunities(self) -> List[Dict]:
        """获取 Launchpool 机会（需要调用 Launchpool API）"""
        opportunities = []

        try:
            # 币安 Launchpool API
            url = f"{self.api_client.base_url}/sapi/v1/launchpool/project/list"
            response = self.api_client.session.get(url)
            if response.status_code == 200:
                data = response.json()
                for project in data:
                    # 只返回进行中的项目
                    if project.get("status") == "ongoing":
                        opportunities.append({
                            "id": project.get("id"),
                            "name": project.get("projectName"),
                            "token": project.get("token"),
                            "start_time": project.get("startTime"),
                            "end_time": project.get("endTime"),
                            "total_reward": project.get("totalReward"),
                            "quotas": project.get("quotas", [])
                        })
        except Exception as e:
            print(f"获取 Launchpool 信息失败: {e}")

        return opportunities

    def format_report(self, scan_result: Dict) -> str:
        """格式化资产扫描报告"""
        report = "📊 资产扫描报告\n"
        report += "=" * 40 + "\n\n"

        if scan_result.get("error"):
            report += f"❌ 扫描失败: {scan_result['error']}\n"
            return report

        # 闲置资金
        report += "💰 闲置资金:\n"
        if scan_result["idle_usdt"] > 0:
            report += f"  • USDT: ${scan_result['idle_usdt']:.2f}\n"
        if scan_result["idle_fdusd"] > 0:
            report += f"  • FDUSD: ${scan_result['idle_fdusd']:.2f}\n"
        report += f"  • 总计: ${scan_result['idle_total']:.2f}\n\n"

        # 零钱资产
        if scan_result["dust_assets"]:
            report += "🧹 零钱资产:\n"
            for d in scan_result["dust_assets"]:
                report += f"  • {d['asset']}: {d['amount']:.6f} (~${d['usdt_value']:.2f})\n"
            report += f"  • 总价值: ${scan_result['dust_total_value']:.2f}\n\n"

        # 建议
        if scan_result["suggestions"]:
            report += "💡 建议:\n"
            for s in scan_result["suggestions"]:
                if s["type"] == "launchpool":
                    report += f"  🚀 {s['message']}\n"
                elif s["type"] == "dust_sweep":
                    report += f"  🧹 {s['message']}\n"
                    report += f"     资产: {', '.join(s['assets'])}\n"

        return report
