#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stock-decision Skill - A 股投资决策助手
从共享记忆读取持仓，生成投资决策报告
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# 添加工作目录到路径
sys.path.insert(0, str(Path.home() / ".openclaw" / "workspace"))

# 导入共享记忆加载器
from shared_memory_loader import get_latest_holdings


class Config:
    """配置管理"""
    
    RISK_CONFIG = {
        "max_position": 20.0,
        "max_total_position": 80.0,
        "max_loss_per_stock": 8.0,
        "max_daily_loss": 5.0
    }


class MarketData:
    """行情数据"""
    
    @staticmethod
    def get_stock_price(code: str) -> dict:
        """获取股票实时价格"""
        try:
            import requests
            
            if code.startswith('6'):
                symbol = f"sh{code}"
            else:
                symbol = f"sz{code}"
            
            url = f"https://qt.gtimg.cn/q={symbol}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            response.encoding = 'gbk'
            
            if response.status_code == 200 and '"' in response.text:
                parts = response.text.split('"')[1].split('~')
                if len(parts) >= 50:
                    current = float(parts[3])
                    close = float(parts[4])
                    change = ((current - close) / close) * 100 if close != 0 else 0
                    
                    return {
                        "code": code,
                        "price": round(current, 2),
                        "change": round(change, 2),
                        "prev_close": close
                    }
        except Exception as e:
            pass
        
        # 备用数据
        base_prices = {
            "300570": 112.51,
            "300054": 49.75,
            "603398": 11.64,
            "688262": 31.26,
            "300342": 56.47,
            "688472": 12.59,
            "000711": 4.13
        }
        
        return {
            "code": code,
            "price": base_prices.get(code, 100),
            "change": 0,
            "prev_close": base_prices.get(code, 100)
        }


class DecisionEngine:
    """决策引擎"""
    
    def __init__(self, config: Config):
        self.config = config
        self.market_data = MarketData()
    
    def analyze_stock(self, code: str, holding: dict) -> dict:
        """分析单只股票"""
        market = self.market_data.get_stock_price(code)
        cost = holding["cost"]
        profit_pct = ((market["price"] - cost) / cost) * 100
        position = holding.get("position", 10.0)
        
        signal = self.generate_signal(holding, profit_pct, position)
        
        return {
            "code": code,
            "name": holding["name"],
            "market": market,
            "holding": holding,
            "profit_pct": round(profit_pct, 2),
            "signal": signal
        }
    
    def generate_signal(self, holding: dict, profit_pct: float, position: float) -> dict:
        """生成买卖信号"""
        signal = {
            "action": "持有",
            "strength": "neutral",
            "reason": "",
            "stop_loss": holding["cost"] * (1 - 0.08),
            "stop_profit": holding["cost"] * (1 + 0.15)
        }
        
        if profit_pct <= -8:
            signal["action"] = "减仓/止损"
            signal["strength"] = "strong_sell"
            signal["reason"] = f"触及止损线 (-8%)"
        elif profit_pct >= 15:
            signal["action"] = "分批止盈"
            signal["strength"] = "sell"
            signal["reason"] = f"触及止盈线 (+15%)"
        elif position > self.config.RISK_CONFIG["max_position"]:
            signal["action"] = "降仓"
            signal["strength"] = "sell"
            signal["reason"] = f"仓位超标 ({position:.2f}% > 20%)"
        else:
            signal["action"] = "持有观望"
            signal["strength"] = "neutral"
            signal["reason"] = "无明显信号"
        
        return signal
    
    def analyze_all(self, holdings: dict) -> list:
        """分析所有持仓股"""
        return [self.analyze_stock(code, holding) for code, holding in holdings.items()]


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def generate_report(self, results: list) -> str:
        """生成投资决策报告"""
        report = f"""# 📊 A 股投资决策报告

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**持仓数量**：{len(results)} 只  
**数据来源**：SHARED_MEMORY.md

---

## 🚨 紧急操作

"""
        urgent = [r for r in results if r['signal']['strength'] in ['strong_sell', 'sell']]
        if urgent:
            for stock in urgent:
                report += f"### {stock['name']}({stock['code']}) {stock['signal']['strength']}\n\n"
                report += f"- **操作**：{stock['signal']['action']}\n"
                report += f"- **理由**：{stock['signal']['reason']}\n"
                report += f"- **止损价**：{stock['signal']['stop_loss']:.2f}元\n"
                report += f"- **止盈价**：{stock['signal']['stop_profit']:.2f}元\n\n"
        else:
            report += "✅ 无紧急操作\n\n"
        
        report += "---\n\n## 📈 持仓详情\n\n"
        report += "| 代码 | 名称 | 现价 | 成本 | 盈亏% | 操作 |\n"
        report += "|------|------|------|------|-------|------|\n"
        
        for stock in results:
            icon = "🔴" if stock['signal']['strength'] == 'strong_sell' else "🟡" if stock['signal']['strength'] == 'sell' else "⚪"
            report += f"| {stock['code']} | {stock['name']} | {stock['market']['price']:.2f} | {stock['holding']['cost']:.2f} | {stock['profit_pct']:+.2f}% | {icon} {stock['signal']['action']} |\n"
        
        report += "\n---\n\n**免责声明**：本报告仅供参考，不构成投资建议。\n"
        
        return report


def execute(query: str = "") -> str:
    """执行 Skill"""
    print("🚀 开始生成投资决策报告...")
    
    # 读取持仓
    holdings = get_latest_holdings()
    if not holdings:
        return "❌ 读取持仓失败！请检查 SHARED_MEMORY.md"
    
    # 分析持仓
    config = Config()
    engine = DecisionEngine(config)
    results = engine.analyze_all(holdings)
    
    # 生成报告
    reporter = ReportGenerator(config)
    report = reporter.generate_report(results)
    
    # 保存报告
    output_dir = Path.home() / ".openclaw" / "decisions"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ 报告已保存：{output_file}")
    return report


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    result = execute(query)
    print(result[:500])  # 打印前 500 字符
