#!/usr/bin/env python3
"""
行业对比分析模块 - 与同行业公司对比分析
用于判断公司在行业中的竞争地位
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 尝试导入 akshare
try:
    import akshare as ak
    import pandas as pd
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    print("⚠️ AKShare 未安装，部分功能不可用")


# 行业映射表（股票名称关键词 -> 行业）
INDUSTRY_MAP = {
    # 银行
    "银行": "银行",
    
    # 电动两轮车
    "爱玛": "电动两轮车",
    "雅迪": "电动两轮车",
    "小牛": "电动两轮车",
    "新日": "电动两轮车",
    "绿源": "电动两轮车",
    
    # 智能家居/扫地机器人
    "科沃斯": "智能家居",
    "石头": "智能家居",
    "云鲸": "智能家居",
    "追觅": "智能家居",
    
    # 白酒
    "茅台": "白酒",
    "五粮液": "白酒",
    "泸州老窖": "白酒",
    "洋河": "白酒",
    "汾酒": "白酒",
    
    # 新能源汽车
    "比亚迪": "新能源汽车",
    "蔚来": "新能源汽车",
    "小鹏": "新能源汽车",
    "理想": "新能源汽车",
    
    # 家电
    "美的": "家电",
    "格力": "家电",
    "海尔": "家电",
    "海信": "家电",
    
    # 家用轻工/户外休闲
    "浙江永强": "家用轻工",
    "永强": "家用轻工",
    
    # 科技
    "腾讯": "互联网",
    "阿里": "互联网",
    "百度": "互联网",
    "京东": "互联网",
    "美团": "互联网",
    
    # 半导体
    "中芯": "半导体",
    "韦尔": "半导体",
    "兆易": "半导体",
    "北方华创": "半导体",
    
    # 医药
    "恒瑞": "医药",
    "药明": "医药",
    "迈瑞": "医药",
    "片仔癀": "医药",
    
    # 食品饮料
    "伊利": "乳制品",
    "蒙牛": "乳制品",
    "双汇": "肉制品",
    "海天": "调味品",
}

# 行业龙头股映射
INDUSTRY_LEADERS = {
    "银行": ["601398", "601288", "601939", "600036"],  # 工商银行、农业银行、建设银行、招商银行
    "电动两轮车": ["01585", "603529", "NIU"],  # 雅迪控股、爱玛科技、小牛电动
    "智能家居": ["603486", "688169", "石头科技"],  # 科沃斯、石头科技
    "白酒": ["600519", "000858", "000568", "000596"],  # 贵州茅台、五粮液、泸州老窖、古井贡酒
    "新能源汽车": ["002594", "NIO", "XPEV", "LI"],  # 比亚迪、蔚来、小鹏、理想
    "家电": ["000333", "000651", "600690"],  # 美的集团、格力电器、海尔智家
    "互联网": ["00700", "BABA", "BIDU", "JD"],  # 腾讯、阿里巴巴、百度、京东
    "半导体": ["688981", "603501", "603986"],  # 中芯国际、韦尔股份、兆易创新
    "医药": ["600276", "603259", "300760"],  # 恒瑞医药、药明康德、迈瑞医疗
    "乳制品": ["600887", "02319"],  # 伊利股份、蒙牛乳业
    "调味品": ["603288"],  # 海天味业
    "家用轻工": ["002489", "603833"],  # 浙江永强、欧派家居
}


class IndustryComparisonAnalyzer:
    """行业对比分析器"""
    
    def __init__(self, stock_code: str, stock_name: str = ""):
        """
        初始化
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称（可选）
        """
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.industry = None
        self.peers = []
        
    def identify_industry(self) -> Optional[str]:
        """
        识别所属行业
        
        Returns:
            行业名称
        """
        # 1. 根据股票名称识别
        for keyword, industry in INDUSTRY_MAP.items():
            if keyword in self.stock_name:
                self.industry = industry
                return industry
        
        # 2. 尝试从AKShare获取行业信息
        if HAS_AKSHARE:
            try:
                df = ak.stock_individual_info_em(symbol=self.stock_code)
                if df is not None and not df.empty:
                    for _, row in df.iterrows():
                        if "行业" in str(row.get("item", "")):
                            self.industry = row.get("value", "")
                            return self.industry
            except Exception:
                pass
        
        return None
    
    def get_industry_peers(self) -> List[str]:
        """
        获取同行业公司列表
        
        Returns:
            同行业公司代码列表
        """
        if not self.industry:
            self.identify_industry()
        
        if self.industry and self.industry in INDUSTRY_LEADERS:
            self.peers = INDUSTRY_LEADERS[self.industry]
            return self.peers
        
        return []
    
    def fetch_peer_data(self, peer_codes: List[str]) -> List[Dict]:
        """
        获取同行业公司数据
        
        Args:
            peer_codes: 同行业公司代码列表
            
        Returns:
            公司数据列表
        """
        if not HAS_AKSHARE:
            return []
        
        peers_data = []
        
        for code in peer_codes:
            try:
                # 跳过港股和美股代码
                if code.startswith("0") and len(code) == 5:
                    continue  # 港股
                if code.isalpha():
                    continue  # 美股
                
                print(f"   ⏳ 获取 {code} 数据...")
                
                # 获取实时行情
                df = ak.stock_zh_a_spot_em()
                stock = df[df['代码'] == code]
                
                if stock.empty:
                    continue
                
                row = stock.iloc[0]
                
                peer_data = {
                    "code": code,
                    "name": row['名称'],
                    "price": float(row['最新价']) if pd.notna(row['最新价']) else 0,
                    "market_cap": float(row['总市值']) if pd.notna(row['总市值']) else 0,
                    "pe_ratio": float(row['市盈率-动态']) if pd.notna(row['市盈率-动态']) else 0,
                    "pb_ratio": float(row['市净率']) if pd.notna(row['市净率']) else 0,
                }
                
                # 获取财务数据
                try:
                    df_income = ak.stock_financial_report_sina(stock=code, symbol="利润表")
                    df_balance = ak.stock_financial_report_sina(stock=code, symbol="资产负债表")
                    
                    if not df_income.empty and not df_balance.empty:
                        income_row = df_income.iloc[0]
                        balance_row = df_balance.iloc[0]
                        
                        revenue = float(income_row['营业收入']) / 1e8 if pd.notna(income_row['营业收入']) else 0
                        cost = float(income_row['营业成本']) / 1e8 if pd.notna(income_row['营业成本']) else 0
                        net_profit = float(income_row['归属于母公司所有者的净利润']) / 1e8 if pd.notna(income_row['归属于母公司所有者的净利润']) else 0
                        equity = float(balance_row['归属于母公司股东权益合计']) / 1e8 if pd.notna(balance_row['归属于母公司股东权益合计']) else 0
                        
                        peer_data["revenue"] = revenue
                        peer_data["net_profit"] = net_profit
                        peer_data["gross_margin"] = (revenue - cost) / revenue * 100 if revenue > 0 else 0
                        peer_data["roe"] = net_profit / equity * 100 if equity > 0 else 0
                except Exception:
                    peer_data["revenue"] = 0
                    peer_data["net_profit"] = 0
                    peer_data["gross_margin"] = 0
                    peer_data["roe"] = 0
                
                peers_data.append(peer_data)
                
            except Exception as e:
                print(f"   ⚠️ 获取 {code} 数据失败: {e}")
                continue
        
        return peers_data
    
    def calculate_ranking(self, target_data: Dict, peers_data: List[Dict]) -> Dict:
        """
        计算行业排名
        
        Args:
            target_data: 目标公司数据
            peers_data: 同行业公司数据
            
        Returns:
            排名结果
        """
        ranking = {
            "market_cap": {"rank": 0, "total": 0, "percentile": 0},
            "pe_ratio": {"rank": 0, "total": 0, "percentile": 0},
            "roe": {"rank": 0, "total": 0, "percentile": 0},
            "gross_margin": {"rank": 0, "total": 0, "percentile": 0},
        }
        
        if not peers_data:
            return ranking
        
        # 添加目标公司到列表
        all_data = peers_data + [target_data]
        total = len(all_data)
        
        # 市值排名（从大到小）
        sorted_by_cap = sorted(all_data, key=lambda x: x.get("market_cap", 0), reverse=True)
        for i, item in enumerate(sorted_by_cap):
            if item["code"] == target_data["code"]:
                ranking["market_cap"]["rank"] = i + 1
                ranking["market_cap"]["total"] = total
                ranking["market_cap"]["percentile"] = (total - i) / total * 100
                break
        
        # PE排名（从小到大，越低越好）
        sorted_by_pe = sorted([x for x in all_data if x.get("pe_ratio", 0) > 0], 
                             key=lambda x: x.get("pe_ratio", 0))
        for i, item in enumerate(sorted_by_pe):
            if item["code"] == target_data["code"]:
                ranking["pe_ratio"]["rank"] = i + 1
                ranking["pe_ratio"]["total"] = len(sorted_by_pe)
                ranking["pe_ratio"]["percentile"] = (len(sorted_by_pe) - i) / len(sorted_by_pe) * 100
                break
        
        # ROE排名（从大到小）
        sorted_by_roe = sorted([x for x in all_data if x.get("roe", 0) > 0], 
                              key=lambda x: x.get("roe", 0), reverse=True)
        for i, item in enumerate(sorted_by_roe):
            if item["code"] == target_data["code"]:
                ranking["roe"]["rank"] = i + 1
                ranking["roe"]["total"] = len(sorted_by_roe)
                ranking["roe"]["percentile"] = (len(sorted_by_roe) - i) / len(sorted_by_roe) * 100
                break
        
        # 毛利率排名（从大到小）
        sorted_by_margin = sorted([x for x in all_data if x.get("gross_margin", 0) > 0], 
                                  key=lambda x: x.get("gross_margin", 0), reverse=True)
        for i, item in enumerate(sorted_by_margin):
            if item["code"] == target_data["code"]:
                ranking["gross_margin"]["rank"] = i + 1
                ranking["gross_margin"]["total"] = len(sorted_by_margin)
                ranking["gross_margin"]["percentile"] = (len(sorted_by_margin) - i) / len(sorted_by_margin) * 100
                break
        
        return ranking
    
    def generate_comparison_report(self, target_data: Dict, peers_data: List[Dict], 
                                   ranking: Dict) -> str:
        """
        生成行业对比报告
        
        Args:
            target_data: 目标公司数据
            peers_data: 同行业公司数据
            ranking: 排名结果
            
        Returns:
            报告文本
        """
        lines = []
        lines.append("=" * 70)
        lines.append("📊 行业对比分析报告")
        lines.append("=" * 70)
        
        # 行业信息
        lines.append(f"\n🏭 所属行业: {self.industry or '未知'}")
        
        # 行业公司对比表
        if peers_data:
            lines.append("\n📊 行业公司对比（按市值排序）")
            lines.append("-" * 70)
            lines.append(f"{'公司':<10} {'市值(亿)':<12} {'PE':<8} {'ROE':<8} {'毛利率':<8} {'排名':<6}")
            lines.append("-" * 70)
            
            # 合并目标公司和同行数据
            all_data = peers_data + [target_data]
            all_data_sorted = sorted(all_data, key=lambda x: x.get("market_cap", 0), reverse=True)
            
            for i, item in enumerate(all_data_sorted, 1):
                name = item.get("name", "")[:8]
                market_cap = item.get("market_cap", 0)
                pe = item.get("pe_ratio", 0)
                roe = item.get("roe", 0)
                margin = item.get("gross_margin", 0)
                
                # 标记目标公司
                is_target = item["code"] == target_data["code"]
                marker = " ★" if is_target else ""
                
                lines.append(f"{name:<10} {market_cap:<12.1f} {pe:<8.1f} {roe:<8.1f}% {margin:<8.1f}% {i:<6}{marker}")
        
        # 行业地位分析
        lines.append("\n📈 行业地位分析")
        lines.append("-" * 70)
        
        target_name = target_data.get("name", self.stock_code)
        
        # 市值排名
        cap_rank = ranking.get("market_cap", {})
        if cap_rank.get("total", 0) > 0:
            lines.append(f"市值排名: 第{cap_rank['rank']}/{cap_rank['total']}名")
            if cap_rank["rank"] == 1:
                lines.append("  ✅ 行业龙头")
            elif cap_rank["percentile"] >= 75:
                lines.append("  ✅ 行业前列")
            elif cap_rank["percentile"] >= 50:
                lines.append("  ⚠️ 行业中游")
            else:
                lines.append("  ❌ 行业后排")
        
        # PE排名
        pe_rank = ranking.get("pe_ratio", {})
        if pe_rank.get("total", 0) > 0:
            lines.append(f"\n估值排名: 第{pe_rank['rank']}/{pe_rank['total']}名（PE从低到高）")
            if pe_rank["rank"] == 1:
                lines.append("  ✅ 行业估值最低")
            elif pe_rank["percentile"] <= 25:
                lines.append("  ✅ 估值偏低")
            elif pe_rank["percentile"] <= 75:
                lines.append("  ⚠️ 估值合理")
            else:
                lines.append("  ❌ 估值偏高")
        
        # ROE排名
        roe_rank = ranking.get("roe", {})
        if roe_rank.get("total", 0) > 0:
            lines.append(f"\nROE排名: 第{roe_rank['rank']}/{roe_rank['total']}名")
            if roe_rank["rank"] == 1:
                lines.append("  ✅ 行业盈利能力最强")
            elif roe_rank["percentile"] >= 75:
                lines.append("  ✅ 盈利能力优秀")
            elif roe_rank["percentile"] >= 50:
                lines.append("  ⚠️ 盈利能力中等")
            else:
                lines.append("  ❌ 盈利能力较弱")
        
        # 毛利率排名
        margin_rank = ranking.get("gross_margin", {})
        if margin_rank.get("total", 0) > 0:
            lines.append(f"\n毛利率排名: 第{margin_rank['rank']}/{margin_rank['total']}名")
            if margin_rank["rank"] == 1:
                lines.append("  ✅ 行业毛利率最高")
            elif margin_rank["percentile"] >= 75:
                lines.append("  ✅ 毛利率优秀")
            elif margin_rank["percentile"] >= 50:
                lines.append("  ⚠️ 毛利率中等")
            else:
                lines.append("  ❌ 毛利率较低")
        
        # 投资建议
        lines.append("\n💡 行业投资建议")
        lines.append("-" * 70)
        
        suggestions = []
        
        # ROE优秀 + 估值低
        if roe_rank.get("percentile", 0) >= 75 and pe_rank.get("percentile", 0) <= 25:
            suggestions.append(f"✅ {target_name}ROE行业领先，估值偏低，具备投资价值")
        
        # ROE优秀 + 估值高
        elif roe_rank.get("percentile", 0) >= 75 and pe_rank.get("percentile", 0) >= 75:
            suggestions.append(f"⚠️ {target_name}盈利能力强，但估值偏高，需关注业绩增长")
        
        # ROE一般 + 估值低
        elif roe_rank.get("percentile", 0) <= 50 and pe_rank.get("percentile", 0) <= 25:
            suggestions.append(f"⚠️ {target_name}估值低但盈利能力一般，需关注基本面改善")
        
        # ROE一般 + 估值高
        else:
            suggestions.append(f"❌ {target_name}盈利能力和估值均无优势，建议谨慎")
        
        for suggestion in suggestions:
            lines.append(suggestion)
        
        lines.append("\n" + "=" * 70)
        
        return "\n".join(lines)
    
    def analyze(self) -> Dict:
        """
        执行完整分析
        
        Returns:
            分析结果字典
        """
        if not HAS_AKSHARE:
            return {"error": "AKShare 未安装"}
        
        # 识别行业
        self.identify_industry()
        if not self.industry:
            return {"error": "无法识别行业"}
        
        # 获取同行业公司
        peers = self.get_industry_peers()
        if not peers:
            return {"error": f"未找到 {self.industry} 行业的公司数据"}
        
        print(f"📊 正在分析 {self.industry} 行业...")
        
        # 获取目标公司数据
        print(f"   ⏳ 获取目标公司 {self.stock_code} 数据...")
        target_data = self.fetch_peer_data([self.stock_code])
        if not target_data:
            return {"error": "获取目标公司数据失败"}
        target_data = target_data[0]
        
        # 获取同行公司数据
        print(f"   ⏳ 获取同行业公司数据...")
        peers_data = self.fetch_peer_data([p for p in peers if p != self.stock_code])
        
        # 计算排名
        ranking = self.calculate_ranking(target_data, peers_data)
        
        # 生成报告
        report = self.generate_comparison_report(target_data, peers_data, ranking)
        
        return {
            "stock_code": self.stock_code,
            "stock_name": target_data.get("name", ""),
            "industry": self.industry,
            "peers": peers_data,
            "target": target_data,
            "ranking": ranking,
            "report": report,
        }


def analyze_industry_comparison(stock_code: str, stock_name: str = "") -> Dict:
    """
    分析股票行业地位
    
    Args:
        stock_code: 股票代码
        stock_name: 股票名称
        
    Returns:
        分析结果
    """
    analyzer = IndustryComparisonAnalyzer(stock_code, stock_name)
    return analyzer.analyze()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 industry_comparison.py <股票代码> [股票名称]")
        print("示例: python3 industry_comparison.py 603529 爱玛科技")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    stock_name = sys.argv[2] if len(sys.argv) > 2 else ""
    
    result = analyze_industry_comparison(stock_code, stock_name)
    
    if "error" in result:
        print(f"❌ {result['error']}")
        sys.exit(1)
    
    print(result["report"])
    
    # 保存结果
    output_dir = f"/root/.openclaw/workspace/investment/industry"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/{stock_code}_industry.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 分析结果已保存: {output_file}")
