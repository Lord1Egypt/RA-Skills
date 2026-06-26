#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
且慢 MCP 客户端 v2.0.0

集成 qieman-mcp 到 fund-analyzer-pro，实现模块 5-8：
- 模块 5：基金经理分析
- 模块 6：机会分析
- 模块 7：投资方式建议
- 模块 8：报告信号

数据源：且慢 MCP（持仓穿透/业绩归因/策略详情）
"""

import json
import os
import sys
import requests
import hashlib
import time
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

# 且慢 MCP 配置
MCP_CONFIG = {
    "url": "https://stargate.yingmi.com/mcp/v2",
    "headers": {
        "x-api-key": "rySVkZpwsubI_uExeTZuGg",
        "Accept": "application/json, text/event-stream"
    }
}

# 缓存目录
CACHE_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "fund-cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class QiemanClient:
    """且慢 MCP 客户端"""

    def __init__(self):
        self.url = MCP_CONFIG["url"]
        self.headers = MCP_CONFIG["headers"]

    def _get_cache_key(self, method: str, params: dict) -> str:
        """生成缓存 key"""
        key_str = f"{method}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_from_cache(self, key: str, ttl: int = 3600) -> Optional[dict]:
        """从缓存获取数据"""
        cache_file = CACHE_DIR / f"{key}.json"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if time.time() - data.get('_timestamp', 0) < ttl:
                    return data.get('result')
        except:
            pass
        return None

    def _save_to_cache(self, key: str, result: dict):
        """保存到缓存"""
        cache_file = CACHE_DIR / f"{key}.json"
        data = {'_timestamp': time.time(), 'result': result}
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _mcp_request(self, method: str, params: dict = None, use_cache: bool = True, ttl: int = 3600) -> dict:
        """发送 MCP 请求（带缓存）"""
        # 尝试从缓存获取
        cache_key = self._get_cache_key(method, params or {})
        if use_cache:
            cached = self._get_from_cache(cache_key, ttl)
            if cached:
                return {"result": cached, "from_cache": True}

        # 发送请求
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            if 'result' in data:
                result = data['result']
                self._save_to_cache(cache_key, result)
                return {"result": result, "from_cache": False}
            elif 'error' in data:
                return {"error": data['error']}
            else:
                return {"error": "未知响应格式"}

        except requests.RequestException as e:
            return {"error": f"请求失败：{str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"JSON 解析失败：{str(e)}"}

    # ============================================================
    # 模块 5：基金经理分析
    # ============================================================

    def analyze_manager(self, manager_name: str = None, fund_code: str = None) -> Dict:
        """基金经理分析

        Args:
            manager_name: 基金经理姓名
            fund_code: 基金代码（可选，用于获取当前管理基金）

        Returns:
            Dict: 基金经理分析报告
        """
        report = {
            'manager_name': manager_name,
            'analyze_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'basic_info': {},
            'managed_funds': [],
            'performance_summary': {},
            'style_analysis': {},
            'evaluation': {},
            'disclaimer': '以上分析仅供参考，不构成投资建议。'
        }

        # 通过且慢 MCP 获取基金经理数据
        # 注意：且慢 MCP 主要通过策略/基金代码获取数据
        if fund_code:
            # 获取基金详情（包含基金经理信息）
            result = self._mcp_request(
                'GetStrategyDetails',
                {'strategyCode': fund_code},
                ttl=86400  # 缓存 1 天
            )

            if 'result' in result:
                details = result['result']
                report['basic_info'] = {
                    'manager_name': details.get('managerName', manager_name or ''),
                    'manager_tenure': details.get('managerTenure', ''),
                    'managed_scale': details.get('managedScale', ''),
                    'fund_company': details.get('fundCompany', ''),
                }

                # 业绩摘要
                report['performance_summary'] = {
                    'annual_return': details.get('annualReturn', ''),
                    'max_drawdown': details.get('maxDrawdown', ''),
                    'sharpe_ratio': details.get('sharpeRatio', ''),
                    'win_rate': details.get('winRate', ''),
                }

                # 风格分析
                report['style_analysis'] = {
                    'investment_style': details.get('investmentStyle', ''),
                    'risk_level': details.get('riskLevel', ''),
                    'sector_focus': details.get('sectorFocus', ''),
                }

        # 综合评价
        report['evaluation'] = self._evaluate_manager(report)

        return report

    def _evaluate_manager(self, report: Dict) -> Dict:
        """评价基金经理"""
        perf = report.get('performance_summary', {})
        style = report.get('style_analysis', {})

        strengths = []
        risks = []

        # 基于业绩评价
        annual_return = perf.get('annual_return', '')
        if isinstance(annual_return, (int, float)) and annual_return > 15:
            strengths.append('年化收益优秀（>15%）')
        elif isinstance(annual_return, (int, float)) and annual_return > 10:
            strengths.append('年化收益良好（>10%）')

        max_drawdown = perf.get('max_drawdown', '')
        if isinstance(max_drawdown, (int, float)) and abs(max_drawdown) < 15:
            strengths.append('风险控制优秀（最大回撤<15%）')
        elif isinstance(max_drawdown, (int, float)) and abs(max_drawdown) > 30:
            risks.append('风险控制较差（最大回撤>30%）')

        # 基于风格评价
        investment_style = style.get('investment_style', '')
        if '价值' in str(investment_style):
            strengths.append('价值投资风格稳定')
        elif '成长' in str(investment_style):
            strengths.append('成长投资风格鲜明')

        return {
            'strengths': strengths if strengths else ['无明显优势'],
            'risks': risks if risks else ['无明显风险'],
        }

    # ============================================================
    # 模块 6：机会分析
    # ============================================================

    def analyze_opportunity(self, sector: str = None, fund_code: str = None) -> Dict:
        """机会分析

        Args:
            sector: 行业/板块名称
            fund_code: 基金代码（可选）

        Returns:
            Dict: 机会分析报告
        """
        report = {
            'sector': sector,
            'analyze_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'market_overview': {},
            'sector_analysis': {},
            'fund_analysis': {},
            'opportunity_score': 0,
            'recommendations': [],
            'disclaimer': '以上分析仅供参考，不构成投资建议。'
        }

        # 通过且慢 MCP 获取策略数据
        if sector:
            result = self._mcp_request(
                'StrategySearchByKeyword',
                {'keyword': sector},
                ttl=3600  # 缓存 1 小时
            )

            if 'result' in result:
                strategies = result['result']
                report['sector_analysis'] = {
                    'strategy_count': len(strategies) if isinstance(strategies, list) else 0,
                    'avg_return': '',
                    'avg_risk': '',
                }

        # 机会评分（0-100）
        report['opportunity_score'] = self._calculate_opportunity_score(report)

        # 生成建议
        report['recommendations'] = self._generate_opportunity_recommendations(report)

        return report

    def _calculate_opportunity_score(self, report: Dict) -> int:
        """计算机会评分"""
        score = 50  # 基础分

        sector = report.get('sector_analysis', {})
        strategy_count = sector.get('strategy_count', 0)

        if strategy_count > 10:
            score += 20  # 策略丰富
        elif strategy_count > 5:
            score += 10

        # 基于市场情绪调整（简化版）
        # 实际应接入市场数据

        return min(100, max(0, score))

    def _generate_opportunity_recommendations(self, report: Dict) -> List[str]:
        """生成机会建议"""
        recommendations = []
        score = report.get('opportunity_score', 50)

        if score >= 80:
            recommendations.append('机会明确，建议积极配置')
        elif score >= 60:
            recommendations.append('机会较好，建议适度配置')
        elif score >= 40:
            recommendations.append('机会一般，建议观望')
        else:
            recommendations.append('机会较差，建议回避')

        return recommendations

    # ============================================================
    # 模块 7：投资方式建议
    # ============================================================

    def suggest_investment_method(self, fund_code: str, amount: float, client_info: Dict = None) -> Dict:
        """投资方式建议

        Args:
            fund_code: 基金代码
            amount: 投资金额
            client_info: 客户信息（可选）

        Returns:
            Dict: 投资方式建议
        """
        report = {
            'fund_code': fund_code,
            'amount': amount,
            'suggest_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'investment_methods': [],
            'recommended_method': '',
            'reason': '',
            'disclaimer': '以上分析仅供参考，不构成投资建议。'
        }

        # 获取基金分析
        from fund_analyzer_pro import FundAnalyzerPro
        analyzer = FundAnalyzerPro()
        analysis = analyzer.analyze_fund(fund_code)

        risk_level = analysis.get('risk_metrics', {}).get('risk_level', '')
        recent_1y = analysis.get('performance', {}).get('recent_1y', '')

        # 基于风险等级推荐投资方式
        if risk_level == '高':
            # 高风险基金：建议定投
            report['investment_methods'] = [
                {
                    'method': '定期定额投资（定投）',
                    'description': '每月固定金额买入，分散择时风险',
                    'suitable_for': '高风险基金/长期投资',
                    'estimated_months': max(6, int(amount / 10000)),
                },
                {
                    'method': '分批买入',
                    'description': '分 3-5 批买入，每批间隔 1-2 周',
                    'suitable_for': '中高风险基金/中期投资',
                    'estimated_months': 3,
                },
            ]
            report['recommended_method'] = '定期定额投资（定投）'
            report['reason'] = '基金风险等级较高，定投可分散择时风险，适合长期投资'

        elif risk_level == '中':
            # 中风险基金：建议分批买入
            report['investment_methods'] = [
                {
                    'method': '分批买入',
                    'description': '分 3 批买入，每批间隔 1 周',
                    'suitable_for': '中风险基金/中期投资',
                    'estimated_months': 1,
                },
                {
                    'method': '一次性买入',
                    'description': '当前估值合理，可一次性买入',
                    'suitable_for': '中风险基金/当前估值偏低',
                    'estimated_months': 0,
                },
            ]
            report['recommended_method'] = '分批买入'
            report['reason'] = '基金风险等级中等，分批买入可平衡收益和风险'

        else:
            # 低风险基金：建议一次性买入
            report['investment_methods'] = [
                {
                    'method': '一次性买入',
                    'description': '当前估值合理，可一次性买入',
                    'suitable_for': '低风险基金/短期投资',
                    'estimated_months': 0,
                },
            ]
            report['recommended_method'] = '一次性买入'
            report['reason'] = '基金风险等级较低，波动小，适合一次性买入'

        return report

    # ============================================================
    # 模块 8：报告信号
    # ============================================================

    def generate_signal(self, fund_code: str) -> Dict:
        """报告信号

        Args:
            fund_code: 基金代码

        Returns:
            Dict: 报告信号（买入/持有/卖出/观察）
        """
        report = {
            'fund_code': fund_code,
            'signal_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'signal': '',
            'confidence': 0,
            'reason': '',
            'indicators': {},
            'disclaimer': '以上分析仅供参考，不构成投资建议。'
        }

        # 获取基金分析
        from fund_analyzer_pro import FundAnalyzerPro
        analyzer = FundAnalyzerPro()
        analysis = analyzer.analyze_fund(fund_code)

        perf = analysis.get('performance', {})
        risk = analysis.get('risk_metrics', {})
        holdings = analysis.get('holdings', {})

        # 信号评分（0-100）
        score = 50  # 基础分

        # 业绩评分
        recent_1y = perf.get('recent_1y', '')
        if isinstance(recent_1y, str) and '%' in recent_1y:
            try:
                ret = float(recent_1y.replace('%', '').replace('+', ''))
                if ret > 10:
                    score += 20
                elif ret > 0:
                    score += 10
                elif ret < -20:
                    score -= 20
                elif ret < -10:
                    score -= 10
            except:
                pass

        # 风险评分
        risk_level = risk.get('risk_level', '')
        if risk_level == '低':
            score += 10
        elif risk_level == '高':
            score -= 10

        # 持仓集中度评分
        top_10_weight = holdings.get('top_10_weight', '0%')
        try:
            weight = float(top_10_weight.replace('%', ''))
            if weight > 80:
                score -= 10  # 集中度过高
        except:
            pass

        # 生成信号
        if score >= 70:
            report['signal'] = '买入'
            report['confidence'] = min(100, score)
            report['reason'] = '基金业绩良好，风险可控，建议买入'
        elif score >= 50:
            report['signal'] = '持有'
            report['confidence'] = score
            report['reason'] = '基金表现平稳，建议继续持有'
        elif score >= 30:
            report['signal'] = '观察'
            report['confidence'] = 100 - score
            report['reason'] = '基金存在一定风险，建议观察后再决定'
        else:
            report['signal'] = '卖出'
            report['confidence'] = 100 - score
            report['reason'] = '基金风险较高，建议减仓或卖出'

        # 指标详情
        report['indicators'] = {
            'performance_score': score,
            'risk_level': risk_level,
            'top_10_weight': top_10_weight,
            'recent_1y': recent_1y,
        }

        return report

    # ============================================================
    # 格式化输出
    # ============================================================

    def format_report(self, report: Dict, module: str = 'manager') -> str:
        """格式化报告为 Markdown"""
        if module == 'manager':
            return self._format_manager_report(report)
        elif module == 'opportunity':
            return self._format_opportunity_report(report)
        elif module == 'investment':
            return self._format_investment_report(report)
        elif module == 'signal':
            return self._format_signal_report(report)
        else:
            return json.dumps(report, ensure_ascii=False, indent=2)

    def _format_manager_report(self, report: Dict) -> str:
        """格式化基金经理分析报告"""
        lines = []
        lines.append(f"# 基金经理分析报告：{report.get('manager_name', '')}")
        lines.append("")
        lines.append(f"**分析时间**：{report['analyze_time']}")
        lines.append("")

        basic = report.get('basic_info', {})
        if basic:
            lines.append("## 📊 基本信息")
            lines.append("")
            lines.append(f"- **基金经理**：{basic.get('manager_name', '')}")
            lines.append(f"- **从业年限**：{basic.get('manager_tenure', '')}")
            lines.append(f"- **管理规模**：{basic.get('managed_scale', '')}")
            lines.append(f"- **基金公司**：{basic.get('fund_company', '')}")
            lines.append("")

        perf = report.get('performance_summary', {})
        if perf:
            lines.append("## 📈 业绩摘要")
            lines.append("")
            lines.append(f"- **年化收益**：{perf.get('annual_return', '')}")
            lines.append(f"- **最大回撤**：{perf.get('max_drawdown', '')}")
            lines.append(f"- **夏普比率**：{perf.get('sharpe_ratio', '')}")
            lines.append(f"- **胜率**：{perf.get('win_rate', '')}")
            lines.append("")

        style = report.get('style_analysis', {})
        if style:
            lines.append("## 🎯 风格分析")
            lines.append("")
            lines.append(f"- **投资风格**：{style.get('investment_style', '')}")
            lines.append(f"- **风险等级**：{style.get('risk_level', '')}")
            lines.append(f"- **行业聚焦**：{style.get('sector_focus', '')}")
            lines.append("")

        eval = report.get('evaluation', {})
        if eval:
            lines.append("## 📋 综合评价")
            lines.append("")
            lines.append("**核心优势**：")
            for s in eval.get('strengths', []):
                lines.append(f"✅ {s}")
            lines.append("")
            lines.append("**主要风险**：")
            for r in eval.get('risks', []):
                lines.append(f"⚠️ {r}")
            lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append(report.get('disclaimer', ''))
        lines.append("")

        return '\n'.join(lines)

    def _format_opportunity_report(self, report: Dict) -> str:
        """格式化机会分析报告"""
        lines = []
        lines.append(f"# 机会分析报告：{report.get('sector', '')}")
        lines.append("")
        lines.append(f"**分析时间**：{report['analyze_time']}")
        lines.append(f"**机会评分**：{report['opportunity_score']}/100")
        lines.append("")

        sector = report.get('sector_analysis', {})
        if sector:
            lines.append("## 📊 行业分析")
            lines.append("")
            lines.append(f"- **策略数量**：{sector.get('strategy_count', 0)}")
            lines.append("")

        recs = report.get('recommendations', [])
        if recs:
            lines.append("## 💡 建议")
            lines.append("")
            for rec in recs:
                lines.append(f"- {rec}")
            lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append(report.get('disclaimer', ''))
        lines.append("")

        return '\n'.join(lines)

    def _format_investment_report(self, report: Dict) -> str:
        """格式化投资方式建议报告"""
        lines = []
        lines.append(f"# 投资方式建议：{report.get('fund_code', '')}")
        lines.append("")
        lines.append(f"**建议时间**：{report['suggest_time']}")
        lines.append(f"**投资金额**：{report['amount'] / 10000:.1f} 万" if report.get('amount') else "")
        lines.append("")

        methods = report.get('investment_methods', [])
        if methods:
            lines.append("## 📊 可选投资方式")
            lines.append("")
            for i, method in enumerate(methods, 1):
                lines.append(f"**方式{i}：{method.get('method', '')}**")
                lines.append(f"- **说明**：{method.get('description', '')}")
                lines.append(f"- **适合**：{method.get('suitable_for', '')}")
                lines.append(f"- **预计周期**：{method.get('estimated_months', 0)} 个月")
                lines.append("")

        lines.append(f"## 🎯 推荐方式")
        lines.append("")
        lines.append(f"**推荐**：{report.get('recommended_method', '')}")
        lines.append(f"**理由**：{report.get('reason', '')}")
        lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append(report.get('disclaimer', ''))
        lines.append("")

        return '\n'.join(lines)

    def _format_signal_report(self, report: Dict) -> str:
        """格式化报告信号"""
        lines = []
        lines.append(f"# 报告信号：{report.get('fund_code', '')}")
        lines.append("")
        lines.append(f"**信号时间**：{report['signal_time']}")
        lines.append("")

        lines.append(f"## 🎯 信号")
        lines.append("")
        lines.append(f"**信号**：{report.get('signal', '')}")
        lines.append(f"**置信度**：{report.get('confidence', 0)}%")
        lines.append(f"**理由**：{report.get('reason', '')}")
        lines.append("")

        indicators = report.get('indicators', {})
        if indicators:
            lines.append("## 📊 指标详情")
            lines.append("")
            lines.append(f"- **业绩评分**：{indicators.get('performance_score', '')}")
            lines.append(f"- **风险等级**：{indicators.get('risk_level', '')}")
            lines.append(f"- **前十大重仓**：{indicators.get('top_10_weight', '')}")
            lines.append(f"- **近 1 年收益**：{indicators.get('recent_1y', '')}")
            lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append(report.get('disclaimer', ''))
        lines.append("")

        return '\n'.join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python qieman_client.py <命令> [参数]")
        print("")
        print("命令：")
        print("  manager <经理姓名> [基金代码]  - 基金经理分析")
        print("  opportunity <行业>             - 机会分析")
        print("  investment <基金代码> <金额>    - 投资方式建议")
        print("  signal <基金代码>               - 报告信号")
        print("")
        print("示例：")
        print("  python qieman_client.py manager 张坤 005827")
        print("  python qieman_client.py opportunity 消费")
        print("  python qieman_client.py investment 005827 100000")
        print("  python qieman_client.py signal 005827")
        sys.exit(1)

    command = sys.argv[1]
    client = QiemanClient()

    if command == 'manager':
        if len(sys.argv) < 3:
            print("错误：请提供基金经理姓名")
            sys.exit(1)
        manager_name = sys.argv[2]
        fund_code = sys.argv[3] if len(sys.argv) > 3 else None
        report = client.analyze_manager(manager_name, fund_code)
        print(client.format_report(report, 'manager'))

    elif command == 'opportunity':
        if len(sys.argv) < 3:
            print("错误：请提供行业名称")
            sys.exit(1)
        sector = sys.argv[2]
        report = client.analyze_opportunity(sector)
        print(client.format_report(report, 'opportunity'))

    elif command == 'investment':
        if len(sys.argv) < 4:
            print("错误：请提供基金代码和投资金额")
            sys.exit(1)
        fund_code = sys.argv[2]
        amount = float(sys.argv[3])
        report = client.suggest_investment_method(fund_code, amount)
        print(client.format_report(report, 'investment'))

    elif command == 'signal':
        if len(sys.argv) < 3:
            print("错误：请提供基金代码")
            sys.exit(1)
        fund_code = sys.argv[2]
        report = client.generate_signal(fund_code)
        print(client.format_report(report, 'signal'))

    else:
        print(f"错误：未知命令 '{command}'")
        sys.exit(1)


if __name__ == '__main__':
    main()
