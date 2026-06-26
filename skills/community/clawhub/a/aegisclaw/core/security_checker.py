"""
安全检查模块 - AI 主动式"安全围栏"
"""

from typing import Dict, List, Tuple
from core.api_client import BinanceAPIClient
from config import BinanceConfig


class SecurityChecker:
    """安全检查器 - AI 拒绝越权的核心模块"""

    def __init__(self, api_client: BinanceAPIClient, config: BinanceConfig):
        self.api_client = api_client
        self.config = config

    def run_full_check(self) -> Dict[str, any]:
        """运行完整的安全检查"""
        results = {
            "api_connection": False,
            "account_type": "unknown",
            "permissions": [],
            "dangerous_permissions": [],
            "balance_summary": {},
            "security_score": 0,
            "warnings": [],
            "recommendations": []
        }

        try:
            # 1. 测试 API 连接
            if not self.api_client.ping():
                results["warnings"].append("❌ API 连接失败，请检查 API Key 和网络")
                return results
            results["api_connection"] = True

            # 2. 获取账户信息
            account = self.api_client.get_account()
            balances = self.api_client.get_balances()

            # 判断账户类型（通过余额特征）
            results["balance_summary"] = self._analyze_balances(balances)
            results["account_type"] = self._detect_account_type(balances, account)

            # 3. 检测危险权限
            perm_check = self._check_permissions(account)
            results["permissions"] = perm_check["all_permissions"]
            results["dangerous_permissions"] = perm_check["dangerous"]

            # 4. 计算安全评分
            results["security_score"] = self._calculate_security_score(results)

            # 5. 生成建议
            results["recommendations"] = self._generate_recommendations(results)

        except Exception as e:
            results["warnings"].append(f"⚠️ 检查过程中出错: {str(e)}")

        return results

    def _analyze_balances(self, balances: List[Dict]) -> Dict:
        """分析余额情况"""
        total_value = 0.0
        assets = {}

        for b in balances:
            if b["asset"] == "USDT":
                assets["USDT"] = b["total"]
                total_value += b["total"]
            elif b["asset"] == "FDUSD":
                assets["FDUSD"] = b["total"]
                total_value += b["total"]
            elif b["asset"] == "BNB":
                assets["BNB"] = b["total"]
                # BNB 价格估算
                try:
                    bnb_price = float(self.api_client.get_symbol_ticker("BNBUSDT")["price"])
                    total_value += b["total"] * bnb_price
                except:
                    pass

        return {
            "total_assets": len([b for b in balances if b["total"] > 0]),
            "stablecoin_balance": assets.get("USDT", 0) + assets.get("FDUSD", 0),
            "bnb_balance": assets.get("BNB", 0),
            "estimated_total_usdt": total_value
        }

    def _detect_account_type(self, balances: List[Dict], account: Dict) -> str:
        """检测账户类型（主账户 vs 子账户）"""
        # 通过账户权限特征判断
        permissions = account.get("permissions", [])

        if "SPOT" in permissions:
            # 如果余额较小，可能是子账户
            total_stable = sum(b["total"] for b in balances if b["asset"] in ["USDT", "FDUSD"])
            if total_stable < 1000:
                return "sub_account_recommended"
            elif total_stable > 10000:
                return "main_account_detected"

        return "sub_account"

    def _check_permissions(self, account: Dict) -> Dict:
        """检查 API 权限"""
        # 币安 API 不会直接返回权限信息
        # 我们需要通过尝试调用受限接口来判断

        permissions = ["SPOT"]  # 假设有现货权限（否则无法获取账户信息）
        dangerous = []

        # 检查是否有提现权限（通过接口尝试）
        # 注意：这里只是模拟检查，实际不应该调用提现接口
        # 实际情况需要用户手动配置时说明

        # 检查是否有合约权限
        try:
            # 尝试获取合约账户信息
            url = f"{self.api_client.base_url.replace('api', 'fapi')}/fapi/v2/account"
            response = self.api_client.session.get(url)
            if response.status_code == 200:
                permissions.append("FUTURES")
        except:
            pass

        # 标记危险权限
        for forbidden in self.config.forbidden_permissions:
            dangerous.append(forbidden)

        return {
            "all_permissions": permissions,
            "dangerous": dangerous
        }

    def _calculate_security_score(self, results: Dict) -> int:
        """计算安全评分 (0-100)"""
        score = 100

        # 账户类型扣分
        if results["account_type"] == "main_account_detected":
            score -= 40

        # 危险权限扣分
        if results["dangerous_permissions"]:
            score -= 50

        # 余额过大的子账户扣分
        if results["account_type"] == "sub_account":
            if results["balance_summary"].get("estimated_total_usdt", 0) > 2000:
                score -= 20

        return max(0, score)

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """生成安全建议"""
        recommendations = []

        if results["account_type"] == "main_account_detected":
            recommendations.append(
                "⚠️ 检测到主账户！为了安全，建议创建一个仅含 500-1000 USDT 的子账户，"
                "并为此子账户创建专用 API Key。"
            )

        if results["dangerous_permissions"]:
            recommendations.append(
                "🚨 您的 API Key 可能包含危险权限！请确保关闭以下权限：\n"
                + "\n".join([f"   - {p}" for p in results["dangerous_permissions"]])
            )

        if results["balance_summary"].get("estimated_total_usdt", 0) > 2000:
            recommendations.append(
                "💡 建议：子账户资金建议控制在 500-1000 USDT 以内，最大风险可控。"
            )

        recommendations.append(
            "🛡️ 建议为 API Key 绑定 IP 白名单，只允许运行 AI 的服务器访问。"
        )

        return recommendations

    def format_report(self, results: Dict) -> str:
        """格式化安全检查报告"""
        report = "🦞 金甲龙虾 - 安全围栏检查报告\n"
        report += "=" * 50 + "\n\n"

        # 连接状态
        if results["api_connection"]:
            report += "✅ API 连接成功\n\n"
        else:
            report += "❌ API 连接失败\n\n"
            return report

        # 账户类型
        account_type_map = {
            "sub_account": "✅ 子账户",
            "sub_account_recommended": "✅ 子账户（推荐配置）",
            "main_account_detected": "⚠️ 检测到主账户"
        }
        report += f"账户类型: {account_type_map.get(results['account_type'], results['account_type'])}\n\n"

        # 余额摘要
        summary = results["balance_summary"]
        report += "资产摘要:\n"
        report += f"  • 资产种类: {summary['total_assets']} 种\n"
        report += f"  • 稳定币: ${summary['stablecoin_balance']:.2f}\n"
        report += f"  • BNB: {summary['bnb_balance']:.4f}\n"
        if summary.get('estimated_total_usdt'):
            report += f"  • 估算总值: ${summary['estimated_total_usdt']:.2f}\n"
        report += "\n"

        # API 权限
        report += "API 权限:\n"
        if results["permissions"]:
            report += "  • 已启用: " + ", ".join(results["permissions"]) + "\n"
        if results["dangerous_permissions"]:
            report += f"  • 🚨 危险权限: {', '.join(results['dangerous_permissions'])}\n"
        report += "\n"

        # 安全评分
        score = results["security_score"]
        if score >= 80:
            score_emoji = "🟢"
        elif score >= 50:
            score_emoji = "🟡"
        else:
            score_emoji = "🔴"
        report += f"{score_emoji} 安全评分: {score}/100\n\n"

        # 警告
        if results["warnings"]:
            report += "⚠️ 警告:\n"
            for w in results["warnings"]:
                report += f"  {w}\n"
            report += "\n"

        # 建议
        if results["recommendations"]:
            report += "💡 建议:\n"
            for r in results["recommendations"]:
                report += f"  {r}\n"

        return report
