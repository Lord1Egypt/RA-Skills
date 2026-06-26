#!/usr/bin/env python3
"""
酒店P&L分析计算器
Hotel P&L Analysis Calculator

功能：
- 财务指标计算
- 保本点分析
- 敏感性分析
- 行业对标
"""

import json
from typing import Dict, List, Optional, Tuple

class HotelPLCalculator:
    """酒店P&L计算器"""
    
    def __init__(self, 
                 rooms: int = 0,
                 occ: float = 0.0,
                 adr: float = 0.0,
                 total_revenue: float = 0.0,
                 room_revenue: float = 0.0,
                 fB_revenue: float = 0.0,
                 other_revenue: float = 0.0,
                 labor_cost: float = 0.0,
                 utility_cost: float = 0.0,
                 marketing_cost: float = 0.0,
                 admin_cost: float = 0.0,
                 maintenance_cost: float = 0.0,
                 other_cost: float = 0.0,
                 fixed_cost: float = 0.0,
                 fB_cost: float = 0.0):
        """
        初始化酒店P&L计算器
        
        Args:
            rooms: 房间数
            occ: 出租率 (0-1)
            adr: 平均房价
            total_revenue: 总营收
            room_revenue: 客房收入
            fB_revenue: 餐饮收入
            other_revenue: 其他收入
            labor_cost: 人工成本
            utility_cost: 能耗成本
            marketing_cost: 市场营销费
            admin_cost: 行政管理费
            maintenance_cost: 维修维护费
            other_cost: 其他费用
            fixed_cost: 固定费用(租金/折旧/利息)
            fB_cost: 餐饮成本
        """
        self.rooms = rooms
        self.occ = occ
        self.adr = adr
        self.total_revenue = total_revenue
        self.room_revenue = room_revenue
        self.fB_revenue = fB_revenue
        self.other_revenue = other_revenue
        self.labor_cost = labor_cost
        self.utility_cost = utility_cost
        self.marketing_cost = marketing_cost
        self.admin_cost = admin_cost
        self.maintenance_cost = maintenance_cost
        self.other_cost = other_cost
        self.fixed_cost = fixed_cost
        self.fB_cost = fB_cost
        
        # 计算衍生指标
        self._calculate_derived_metrics()
    
    def _calculate_derived_metrics(self):
        """计算衍生指标"""
        # 出租率转为百分比
        self.occ_pct = self.occ * 100 if self.occ <= 1 else self.occ
        
        # 如果没有直接提供总营收，则计算
        if self.total_revenue == 0:
            self.total_revenue = self.room_revenue + self.fB_revenue + self.other_revenue
        
        # RevPAR
        self.revpar = self.adr * (self.occ / 100) if self.occ > 1 else self.adr * self.occ
        
        # 可售客房夜次 (假设30天)
        self.available_room_nights = self.rooms * 30
        
        # 已售客房夜次
        self.sold_room_nights = self.available_room_nights * (self.occ / 100) if self.occ > 1 else self.available_room_nights * self.occ
        
    def calculate_revenue_metrics(self) -> Dict:
        """计算收入相关指标"""
        return {
            "总收入": f"¥{self.total_revenue:,.0f}",
            "客房收入": f"¥{self.room_revenue:,.0f}",
            "客房收入占比": f"{self.room_revenue/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
            "餐饮收入": f"¥{self.fB_revenue:,.0f}",
            "餐饮收入占比": f"{self.fB_revenue/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
            "其他收入": f"¥{self.other_revenue:,.0f}",
            "RevPAR": f"¥{self.revpar:,.0f}",
            "已售客房夜次": f"{self.sold_room_nights:,.0f}",
        }
    
    def calculate_cost_metrics(self) -> Dict:
        """计算成本相关指标"""
        total_cost = (self.labor_cost + self.utility_cost + self.marketing_cost + 
                     self.admin_cost + self.maintenance_cost + self.other_cost)
        
        return {
            "总成本": f"¥{total_cost:,.0f}",
            "总成本率": f"{total_cost/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
            "人工成本": f"¥{self.labor_cost:,.0f}",
            "人工成本率": f"{self.labor_cost/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
            "能耗成本": f"¥{self.utility_cost:,.0f}",
            "能耗占比": f"{self.utility_cost/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
            "市场营销费": f"¥{self.marketing_cost:,.0f}",
            "营销费用率": f"{self.marketing_cost/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
            "餐饮成本": f"¥{self.fB_cost:,.0f}",
            "餐饮成本率": f"{self.fB_cost/self.fB_revenue*100:.1f}%" if self.fB_revenue else "N/A",
        }
    
    def calculate_profit_metrics(self) -> Dict:
        """计算利润相关指标"""
        # GOP计算
        total_cost = (self.labor_cost + self.utility_cost + self.marketing_cost + 
                     self.admin_cost + self.maintenance_cost + self.other_cost)
        gop = self.total_revenue - total_cost
        
        # 餐饮部利润
        fB_profit = self.fB_revenue - self.fB_cost
        
        # 客房部利润 (假设客房成本主要是人工和客房消耗品)
        room_cost = self.labor_cost * 0.4  # 假设40%人工用于客房
        room_profit = self.room_revenue - room_cost
        
        # NOI
        noi = gop - self.fixed_cost
        
        # 净利润
        net_profit = noi * 0.8  # 假设税率20%
        
        return {
            "GOP": f"¥{gop:,.0f}",
            "GOP Margin": f"{gop/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
            "客房部利润": f"¥{room_profit:,.0f}",
            "客房利润率": f"{room_profit/self.room_revenue*100:.1f}%" if self.room_revenue else "N/A",
            "餐饮部利润": f"¥{fB_profit:,.0f}",
            "餐饮利润率": f"{fB_profit/self.fB_revenue*100:.1f}%" if self.fB_revenue else "N/A",
            "NOI": f"¥{noi:,.0f}",
            "NOI Margin": f"{noi/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
            "净利润": f"¥{net_profit:,.0f}",
            "净利润率": f"{net_profit/self.total_revenue*100:.1f}%" if self.total_revenue else "N/A",
        }
    
    def calculate_breakeven(self, days: int = 30) -> Dict:
        """计算保本点"""
        # 变动成本
        variable_cost = (self.utility_cost + self.marketing_cost + 
                        self.maintenance_cost + self.other_cost)
        
        # 固定成本 = 人工成本 + 行政管理费 + 固定费用
        fixed_cost_total = (self.labor_cost + self.admin_cost + self.fixed_cost)
        
        # 贡献边际
        contribution_margin = self.adr - (variable_cost / self.sold_room_nights) if self.sold_room_nights > 0 else 0
        
        # 保本出租率
        available_nights = self.rooms * days
        breakeven_occ = fixed_cost_total / (self.adr * available_nights * 0.33) if self.adr > 0 else 0
        
        # 安全边际
        current_occ = self.occ / 100 if self.occ > 1 else self.occ
        safety_margin = (current_occ - breakeven_occ) * 100
        
        return {
            "固定成本总额": f"¥{fixed_cost_total:,.0f}",
            "变动成本/间夜": f"¥{variable_cost/self.sold_room_nights:,.0f}" if self.sold_room_nights > 0 else "N/A",
            "贡献边际/间夜": f"¥{contribution_margin:,.0f}",
            "贡献边际率": f"{contribution_margin/self.adr*100:.1f}%" if self.adr > 0 else "N/A",
            "保本出租率": f"{breakeven_occ*100:.1f}%",
            "当前出租率": f"{self.occ_pct:.1f}%",
            "安全边际": f"{safety_margin:.1f}pp",
        }
    
    def sensitivity_analysis(self) -> List[Dict]:
        """敏感性分析"""
        scenarios = []
        
        # ADR变化分析
        for adr_change in [-10, 10]:
            new_adr = self.adr * (1 + adr_change/100)
            new_revpar = new_adr * (self.occ / 100) if self.occ > 1 else new_adr * self.occ
            scenarios.append({
                "情景": f"ADR {adr_change:+d}%",
                "新ADR": f"¥{new_adr:,.0f}",
                "新RevPAR": f"¥{new_revpar:,.0f}",
                "收入变化": f"¥{self.total_revenue * adr_change/100:+,,.0f}",
            })
        
        # 出租率变化分析
        for occ_change in [-5, 5]:
            new_occ = self.occ_pct + occ_change
            new_sold = self.available_room_nights * new_occ/100
            new_revenue = new_sold * self.adr
            scenarios.append({
                "情景": f"OCC {occ_change:+d}pp",
                "新出租率": f"{new_occ:.1f}%",
                "新增收入": f"¥{new_revenue - self.total_revenue * 0.65:+,,.0f}",
            })
        
        return scenarios
    
    def get_full_report(self) -> str:
        """生成完整报告"""
        report = []
        report.append("=" * 50)
        report.append("        酒店P&L分析报告")
        report.append("=" * 50)
        
        report.append("\n【一、收入分析】")
        for k, v in self.calculate_revenue_metrics().items():
            report.append(f"  {k}: {v}")
        
        report.append("\n【二、成本分析】")
        for k, v in self.calculate_cost_metrics().items():
            report.append(f"  {k}: {v}")
        
        report.append("\n【三、利润分析】")
        for k, v in self.calculate_profit_metrics().items():
            report.append(f"  {k}: {v}")
        
        report.append("\n【四、保本点分析】")
        for k, v in self.calculate_breakeven().items():
            report.append(f"  {k}: {v}")
        
        report.append("\n【五、敏感性分析】")
        for s in self.sensitivity_analysis():
            report.append(f"  {s['情景']}: {s.get('新ADR', s.get('新出租率', ''))}")
        
        report.append("\n" + "=" * 50)
        return "\n".join(report)


def demo():
    """演示示例"""
    # 创建示例酒店数据 (300间客房的中高端酒店)
    hotel = HotelPLCalculator(
        rooms=300,
        occ=72.5,
        adr=658,
        total_revenue=21850000,
        room_revenue=14200000,
        fB_revenue=5800000,
        other_revenue=1850000,
        labor_cost=6120000,
        utility_cost=870000,
        marketing_cost=980000,
        admin_cost=650000,
        maintenance_cost=440000,
        other_cost=980000,
        fixed_cost=3800000,
        fB_cost=2030000,
    )
    
    print(hotel.get_full_report())
    
    return hotel


if __name__ == "__main__":
    demo()
