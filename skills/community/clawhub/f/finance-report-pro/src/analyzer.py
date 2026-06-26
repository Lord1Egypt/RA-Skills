#!/usr/bin/env python3
"""
財務分析器 - 分析個人財務狀況
功能：計算財務健康評分、儲蓄率、資產負債比
"""

from typing import Dict

class FinancialAnalyzer:
    """財務分析器"""
    
    def analyze(self, data: Dict) -> Dict:
        """
        分析財務狀況
        
        Args:
            data: 財務數據
                {
                    'monthly_income': 30000,
                    'monthly_expense': 20000,
                    'assets': {'cash': 100000, 'investment': 50000, 'property': 500000},
                    'liabilities': {'loan': 200000, 'credit_card': 10000}
                }
        
        Returns:
            Dict: 分析結果
        """
        # 計算總資產
        total_assets = sum(data.get('assets', {}).values())
        
        # 計算總負債
        total_liabilities = sum(data.get('liabilities', {}).values())
        
        # 計算淨資產
        net_worth = total_assets - total_liabilities
        
        # 計算儲蓄率
        monthly_income = data.get('monthly_income', 0)
        monthly_expense = data.get('monthly_expense', 0)
        savings_rate = (monthly_income - monthly_expense) / monthly_income * 100 if monthly_income > 0 else 0
        
        # 計算資產負債比
        debt_to_asset_ratio = total_liabilities / total_assets * 100 if total_assets > 0 else 0
        
        # 計算財務健康評分
        health_score = self.calculate_health_score(savings_rate, debt_to_asset_ratio, net_worth)
        
        # 生成評級
        rating = self.get_rating(health_score)
        
        return {
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'net_worth': net_worth,
            'monthly_income': monthly_income,
            'monthly_expense': monthly_expense,
            'savings_rate': savings_rate,
            'debt_to_asset_ratio': debt_to_asset_ratio,
            'health_score': health_score,
            'rating': rating
        }
    
    def calculate_health_score(self, savings_rate: float, debt_ratio: float, net_worth: float) -> int:
        """
        計算財務健康評分（0-100）
        
        評分標準：
        - 儲蓄率（40 分）：>50% 得 40 分，每少 10% 扣 8 分
        - 資產負債比（30 分）：<20% 得 30 分，每多 10% 扣 5 分
        - 淨資產（30 分）：>$100 萬得 30 分，每少 20 萬扣 6 分
        """
        score = 0
        
        # 儲蓄率評分（40 分）
        if savings_rate >= 50:
            score += 40
        elif savings_rate >= 40:
            score += 32
        elif savings_rate >= 30:
            score += 24
        elif savings_rate >= 20:
            score += 16
        elif savings_rate >= 10:
            score += 8
        
        # 資產負債比評分（30 分）
        if debt_ratio <= 20:
            score += 30
        elif debt_ratio <= 30:
            score += 25
        elif debt_ratio <= 40:
            score += 20
        elif debt_ratio <= 50:
            score += 15
        elif debt_ratio <= 60:
            score += 10
        
        # 淨資產評分（30 分）
        if net_worth >= 1000000:
            score += 30
        elif net_worth >= 800000:
            score += 24
        elif net_worth >= 600000:
            score += 18
        elif net_worth >= 400000:
            score += 12
        elif net_worth >= 200000:
            score += 6
        
        return min(100, score)
    
    def get_rating(self, score: int) -> str:
        """獲取評級"""
        if score >= 80:
            return "優秀 🟢"
        elif score >= 60:
            return "良好 🟡"
        elif score >= 40:
            return "一般 🟠"
        else:
            return "需改善 🔴"
    
    def get_recommendations(self, analysis: Dict) -> list:
        """獲取理財建議"""
        recommendations = []
        
        # 根據儲蓄率建議
        if analysis['savings_rate'] < 20:
            recommendations.append("儲蓄率較低，建議減少不必要支出")
        elif analysis['savings_rate'] >= 30:
            recommendations.append("儲蓄率良好，建議增加投資")
        
        # 根據資產負債比建議
        if analysis['debt_to_asset_ratio'] > 50:
            recommendations.append("負債比例過高，建議優先還債")
        elif analysis['debt_to_asset_ratio'] < 30:
            recommendations.append("資產負債比健康，可考慮增加投資")
        
        # 根據淨資產建議
        if analysis['net_worth'] < 200000:
            recommendations.append("建議建立應急基金（3-6 個月支出）")
        elif analysis['net_worth'] >= 500000:
            recommendations.append("建議配置部分資產到被動收入來源")
        
        return recommendations


# 測試
if __name__ == "__main__":
    analyzer = FinancialAnalyzer()
    
    test_data = {
        'monthly_income': 30000,
        'monthly_expense': 20000,
        'assets': {'cash': 100000, 'investment': 50000, 'property': 500000},
        'liabilities': {'loan': 200000, 'credit_card': 10000}
    }
    
    result = analyzer.analyze(test_data)
    
    print("📊 財務分析報告")
    print(f"淨資產：${result['net_worth']:,.0f}")
    print(f"儲蓄率：{result['savings_rate']:.1f}%")
    print(f"資產負債比：{result['debt_to_asset_ratio']:.1f}%")
    print(f"財務健康評分：{result['health_score']}/100 ({result['rating']})")
    print("\n💡 建議:")
    for rec in analyzer.get_recommendations(result):
        print(f"  • {rec}")
