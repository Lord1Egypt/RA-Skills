#!/usr/bin/env python3
"""
報告生成器 - 生成理財報告
功能：生成 Markdown 報告、添加引流鏈接
"""

from datetime import datetime
from typing import Dict, List

class ReportGenerator:
    """報告生成器"""
    
    def generate(self, analysis: Dict, recommendations: List[str]) -> str:
        """
        生成理財報告
        
        Args:
            analysis: 財務分析結果
            recommendations: 理財建議列表
            
        Returns:
            str: Markdown 格式報告
        """
        report = f"""# 📊 個人理財報告

**生成日期：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 💰 財務健康評分：{analysis['health_score']}/100 ({analysis['rating']})

---

## 📈 收入支出分析

| 項目 | 金額 |
|------|------|
| **月收入** | ${analysis['monthly_income']:,.0f} |
| **月支出** | ${analysis['monthly_expense']:,.0f} |
| **月儲蓄** | ${analysis['monthly_income'] - analysis['monthly_expense']:,.0f} |
| **儲蓄率** | {analysis['savings_rate']:.1f}% |

"""
        
        # 根據儲蓄率添加評價
        if analysis['savings_rate'] >= 30:
            report += "**評價：** ✅ 儲蓄率良好，建議增加投資\n\n"
        elif analysis['savings_rate'] >= 20:
            report += "**評價：** ⚠️ 儲蓄率一般，建議優化支出\n\n"
        else:
            report += "**評價：** ❌ 儲蓄率較低，建議減少不必要支出\n\n"
        
        report += f"""---

## 🏦 資產負債評估

| 項目 | 金額 |
|------|------|
| **總資產** | ${analysis['total_assets']:,.0f} |
| **總負債** | ${analysis['total_liabilities']:,.0f} |
| **淨資產** | ${analysis['net_worth']:,.0f} |
| **資產負債比** | {analysis['debt_to_asset_ratio']:.1f}% |

"""
        
        # 根據資產負債比添加評價
        if analysis['debt_to_asset_ratio'] < 30:
            report += "**評價：** ✅ 資產負債比健康\n\n"
        elif analysis['debt_to_asset_ratio'] < 50:
            report += "**評價：** ⚠️ 資產負債比一般\n\n"
        else:
            report += "**評價：** ❌ 負債比例過高，建議優先還債\n\n"
        
        report += """---

## 💡 理財建議

"""
        
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += """
---

## 🎯 被動收入方案推薦

根據您的財務狀況，建議考慮以下被動收入方案：

| 方案 | 預期收益 | 風險 | 建議配置 |
|------|---------|------|---------|
| **股息投資** | $500-1000/月 | 中 | 20% 資產 |
| **房地產 REITs** | $300-800/月 | 低 | 15% 資產 |
| **P2P 借貸** | $200-500/月 | 中高 | 10% 資產 |
| **數字產品** | $1000-3000/月 | 中 | 時間投資 |
| **聯盟營銷** | $500-2000/月 | 低 | 時間投資 |

---

## 🚀 付費產品推薦

如需更專業的理財規劃，建議考慮以下服務：

### 1️⃣ FB Ads 代運營服務

**價格：** $199-799/月

**包含：**
- AI 廣告文案生成
- 廣告投放管理
- 數據分析優化
- 每週報告

**適合：** 想通過 FB Ads 增加收入的創業者

---

### 2️⃣ AI 電商實戰課程

**價格：** $997-2,997

**包含：**
- 10 小時視頻課程
- AI 工具包
- 實戰案例
- 社群支持

**適合：** 想建立電商業務的創業者

---

### 3️⃣ 1 對 1 理財諮詢

**價格：** $499/小時

**包含：**
- 個人財務分析
- 理財規劃建議
- 投資組合建議
- 跟進服務

**適合：** 需要個性化建議的專業人士

---

### 4️⃣ 全託管代運營服務

**價格：** $999/月

**包含：**
- 完整業務運營
- 財務管理
- 營銷策劃
- 每週會議

**適合：** 想完全放手的企业家

---

## 📞 聯絡我們

**Email:** mailtovicacompany.pay@gmail.com

**Telegram:** @VicAICompany

**預約諮詢:** [點擊此處](https://calendly.com/vicai)

---

**免責聲明：** 本報告僅供參考，不構成投資建議。投資涉及風險，決策需謹慎。

**生成時間：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report


# 測試
if __name__ == "__main__":
    from analyzer import FinancialAnalyzer
    
    analyzer = FinancialAnalyzer()
    generator = ReportGenerator()
    
    test_data = {
        'monthly_income': 30000,
        'monthly_expense': 20000,
        'assets': {'cash': 100000, 'investment': 50000, 'property': 500000},
        'liabilities': {'loan': 200000, 'credit_card': 10000}
    }
    
    analysis = analyzer.analyze(test_data)
    recommendations = analyzer.get_recommendations(analysis)
    report = generator.generate(analysis, recommendations)
    
    print(report)
