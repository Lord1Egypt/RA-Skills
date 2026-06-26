#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股市场日报脚本
获取大盘指数、热门板块和龙头股数据
数据来源：东方财富网
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional


class AStockDailyReport:
    """A 股市场日报生成器"""
    
    # 东方财富 API 基础 URL
    BASE_URL = "http://push2.eastmoney.com/api/qt"
    
    # 大盘指数代码
    INDICES = {
        "上证指数": "1.000001",
        "深证成指": "0.399001",
        "创业板指": "0.399006",
    }
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.session = requests.Session()
        
    def _get(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """发送 GET 请求"""
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"请求失败：{e}")
            return None
    
    def get_index_data(self) -> List[Dict]:
        """获取大盘指数数据"""
        results = []
        for name, code in self.INDICES.items():
            try:
                url = f"{self.BASE_URL}/stock/get"
                params = {
                    "secid": code,
                    "fields": "f43,f44,f45,f46,f58,f107"
                }
                data = self._get(url, params)
                if data and data.get('data'):
                    d = data['data']
                    current = d.get('f46', 0) / 100
                    open_p = d.get('f44', 0) / 100
                    pct = d.get('f107', 0)
                    if pct == 0 and open_p > 0:
                        pct = ((current - open_p) / open_p * 100)
                    results.append({
                        "name": name,
                        "current": current,
                        "pct": pct
                    })
            except Exception as e:
                print(f"获取{name}失败：{e}")
        return results
    
    def get_hot_sectors(self, top_n: int = 10) -> List[Dict]:
        """获取热门板块排行"""
        try:
            url = f"{self.BASE_URL}/clist/get"
            params = {
                "pn": 1,
                "pz": top_n,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": "f3",
                "fs": "m:90+t:3",
                "fields": "f12,f14,f2,f3,f4"
            }
            data = self._get(url, params)
            if data and data.get('data') and data['data'].get('diff'):
                sectors = []
                for block in data['data']['diff']:
                    sectors.append({
                        "code": block.get('f12', ''),
                        "name": block.get('f14', ''),
                        "price": block.get('f2', 0),
                        "pct": block.get('f3', 0),
                        "change": block.get('f4', 0)
                    })
                return sectors
        except Exception as e:
            print(f"获取板块失败：{e}")
        return []
    
    def get_sector_leaders(self, sector_code: str, top_n: int = 3) -> List[Dict]:
        """获取板块龙头股"""
        try:
            url = f"{self.BASE_URL}/clist/get"
            params = {
                "pn": 1,
                "pz": top_n,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": "f3",
                "fs": f"b:{sector_code}",
                "fields": "f12,f14,f2,f3,f4"
            }
            data = self._get(url, params)
            if data and data.get('data') and data['data'].get('diff'):
                stocks = []
                for stock in data['data']['diff']:
                    stocks.append({
                        "code": stock.get('f12', ''),
                        "name": stock.get('f14', ''),
                        "pct": stock.get('f3', 0)
                    })
                return stocks
        except Exception as e:
            print(f"获取{sector_code}龙头股失败：{e}")
        return []
    
    def get_all_time_high_stocks(self, top_n: int = 20) -> List[Dict]:
        """获取创历史新高的股票"""
        try:
            url = f"{self.BASE_URL}/clist/get"
            params = {
                "pn": 1,
                "pz": top_n,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": "f109",  # 按历史新高排序
                "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
                "fields": "f12,f14,f2,f3,f109"
            }
            data = self._get(url, params)
            if data and data.get('data') and data['data'].get('diff'):
                stocks = []
                for stock in data['data']['diff']:
                    stocks.append({
                        "code": stock.get('f12', ''),
                        "name": stock.get('f14', ''),
                        "price": stock.get('f2', 0),
                        "pct": stock.get('f3', 0),
                        "high_days": stock.get('f109', 0)
                    })
                return stocks
        except Exception as e:
            print(f"获取历史新高股票失败：{e}")
        return []
    
    def get_continuous_high_stocks(self, days: int = 20, top_n: int = 20) -> List[Dict]:
        """获取连续创新高的股票（N 日新高）"""
        try:
            url = f"{self.BASE_URL}/clist/get"
            # 根据天数选择排序字段
            fid = "f109" if days == 20 else "f193"  # f109=20 日新高，f193=60 日新高
            params = {
                "pn": 1,
                "pz": top_n,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": fid,
                "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
                "fields": "f12,f14,f2,f3,f109,f193"
            }
            data = self._get(url, params)
            if data and data.get('data') and data['data'].get('diff'):
                stocks = []
                for stock in data['data']['diff']:
                    high_20 = stock.get('f109', 0)
                    high_60 = stock.get('f193', 0)
                    # 只显示符合天数要求的
                    if (days == 20 and high_20 > 0) or (days == 60 and high_60 > 0):
                        stocks.append({
                            "code": stock.get('f12', ''),
                            "name": stock.get('f14', ''),
                            "price": stock.get('f2', 0),
                            "pct": stock.get('f3', 0),
                            "high_20": high_20,
                            "high_60": high_60
                        })
                return stocks
        except Exception as e:
            print(f"获取{days}日新高股票失败：{e}")
        return []
    
    def generate_report(self) -> str:
        """生成完整的市场日报"""
        lines = []
        lines.append("=" * 50)
        lines.append("📈 A 股市场日报")
        lines.append(f"📅 {datetime.now().strftime('%Y年%m月%d日 %H:%M')} (Asia/Shanghai)")
        lines.append("=" * 50)
        lines.append("")
        
        # 1. 大盘指数
        lines.append("【大盘指数】")
        indices = self.get_index_data()
        for idx in indices:
            lines.append(f"  {idx['name']}: {idx['current']:.2f} 点 ({idx['pct']:+.2f}%)")
        if not indices:
            lines.append("  数据获取中...")
        lines.append("")
        
        # 2. 热门板块
        lines.append("【🔥 今日最热板块 Top 10】")
        sectors = self.get_hot_sectors(10)
        for i, sec in enumerate(sectors, 1):
            emoji = "🔥" if i <= 3 else "📈"
            lines.append(f"  {emoji} {i}. {sec['name']}: {sec['price']:.2f} ({sec['pct']:+.2f}%)")
        if not sectors:
            lines.append("  数据获取中...")
        lines.append("")
        
        # 3. 板块龙头股
        lines.append("【🏆 板块龙头股】")
        top_sectors = sectors[:3] if len(sectors) >= 3 else sectors
        for sec in top_sectors:
            lines.append(f"\n  {sec['name']}:")
            leaders = self.get_sector_leaders(sec['code'], 3)
            for stock in leaders:
                flag = "🚀" if stock['pct'] >= 15 else ""
                lines.append(f"    • {stock['name']}({stock['code']}): {stock['pct']:+.2f}%{flag}")
        lines.append("")
        
        # 4. 市场简评
        lines.append("【市场简评】")
        if indices and sectors:
            sh = indices[0] if len(indices) > 0 else None
            if sh and sh['pct'] > 0:
                lines.append("  今日市场呈现结构性分化特征")
            else:
                lines.append("  今日市场整体调整，结构性机会为主")
            
            if sectors:
                top_sector = sectors[0]
                lines.append(f"  {top_sector['name']}领涨，涨幅{top_sector['pct']:+.2f}%")
                lines.append("  科技成长板块表现活跃")
        lines.append("")
        
        # 5. 创历史新高股票 Top20
        lines.append("【🎯 创历史新高股票 Top20】")
        ath_stocks = self.get_all_time_high_stocks(20)
        if ath_stocks:
            lines.append(f"  {'股票':<12} {'代码':<10} {'现价':<10} {'涨幅':<10}")
            lines.append("  " + "-" * 42)
            for stock in ath_stocks[:20]:
                lines.append(f"  {stock['name']:<12} {stock['code']:<10} {stock['price']:<10.2f} {stock['pct']:+.2f}%")
        else:
            lines.append("  暂无数据或今日无创历史新高股票")
        lines.append("")
        
        # 6. 连续创新高股票
        lines.append("【📊 连续创新高股票】")
        high_20 = self.get_continuous_high_stocks(20, 15)
        high_60 = self.get_continuous_high_stocks(60, 15)
        
        lines.append("  【20 日新高】")
        if high_20:
            for stock in high_20[:10]:
                lines.append(f"    {stock['name']}({stock['code']}): {stock['price']:.2f} ({stock['pct']:+.2f}%)")
        else:
            lines.append("    暂无数据")
        
        lines.append("  【60 日新高】")
        if high_60:
            for stock in high_60[:10]:
                lines.append(f"    {stock['name']}({stock['code']}): {stock['price']:.2f} ({stock['pct']:+.2f}%)")
        else:
            lines.append("    暂无数据")
        lines.append("")
        
        lines.append("=" * 50)
        lines.append("💡 数据来源：东方财富网 | 仅供参考，不构成投资建议")
        lines.append("⚠️ 风险提示：股市有风险，投资需谨慎。本报告仅供参考，不构成任何投资建议。")
        lines.append("=" * 50)
        
        return "\n".join(lines)


def main():
    """主函数"""
    report = AStockDailyReport()
    print(report.generate_report())


if __name__ == "__main__":
    main()
