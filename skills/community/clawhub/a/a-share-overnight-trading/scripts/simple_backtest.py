#!/usr/bin/env python3
"""
A股主板隔夜交易法简易回测（无外部依赖）
模拟2025年3月1日至3月25日的每日选股和次日验证
"""

import sys
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

class SimpleBacktest:
    """简易隔夜交易回测引擎"""
    
    def __init__(self, start_date: str, end_date: str):
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # 筛选标准
        self.criteria = {
            'price_change_min': 1.0,    # 最小涨幅%
            'price_change_max': 5.0,    # 最大涨幅%
            'turnover_min': 1.0,        # 最小成交额(亿元)
            'market_cap_min': 50.0,     # 最小流通市值(亿元)
            'market_cap_max': 500.0,    # 最大流通市值(亿元)
            'turnover_rate_min': 3.0,   # 最小换手率%
            'turnover_rate_max': 10.0,  # 最大换手率%
            'price_min': 5.0,           # 最低股价(元)
        }
        
        # 模拟股票池（20支主板股票）
        self.stock_pool = [
            {'code': '600030', 'name': '中信证券', 'sector': '券商', 'base_price': 22.5, 'market_cap': 3200},
            {'code': '600036', 'name': '招商银行', 'sector': '银行', 'base_price': 35.0, 'market_cap': 9000},
            {'code': '600519', 'name': '贵州茅台', 'sector': '消费', 'base_price': 1700, 'market_cap': 21000},
            {'code': '601012', 'name': '隆基绿能', 'sector': '新能源', 'base_price': 45.0, 'market_cap': 3400},
            {'code': '601318', 'name': '中国平安', 'sector': '保险', 'base_price': 45.0, 'market_cap': 8500},
            {'code': '601857', 'name': '中国石油', 'sector': '能源', 'base_price': 8.5, 'market_cap': 15000},
            {'code': '601888', 'name': '中国国旅', 'sector': '消费', 'base_price': 120.0, 'market_cap': 2500},
            {'code': '603259', 'name': '药明康德', 'sector': '医药', 'base_price': 75.0, 'market_cap': 2200},
            {'code': '603501', 'name': '韦尔股份', 'sector': '半导体', 'base_price': 90.0, 'market_cap': 1100},
            {'code': '603986', 'name': '兆易创新', 'sector': '半导体', 'base_price': 110.0, 'market_cap': 750},
            {'code': '000001', 'name': '平安银行', 'sector': '银行', 'base_price': 15.0, 'market_cap': 3000},
            {'code': '000002', 'name': '万科A', 'sector': '房地产', 'base_price': 25.0, 'market_cap': 2800},
            {'code': '000063', 'name': '中兴通讯', 'sector': '通信', 'base_price': 30.0, 'market_cap': 1400},
            {'code': '000338', 'name': '潍柴动力', 'sector': '机械', 'base_price': 15.5, 'market_cap': 1300},
            {'code': '000538', 'name': '云南白药', 'sector': '医药', 'base_price': 55.0, 'market_cap': 1000},
            {'code': '000625', 'name': '长安汽车', 'sector': '汽车', 'base_price': 18.0, 'market_cap': 1800},
            {'code': '000858', 'name': '五粮液', 'sector': '消费', 'base_price': 150.0, 'market_cap': 5800},
            {'code': '000876', 'name': '新希望', 'sector': '农业', 'base_price': 12.0, 'market_cap': 550},
            {'code': '002024', 'name': '苏宁易购', 'sector': '零售', 'base_price': 8.0, 'market_cap': 750},
            {'code': '002594', 'name': '比亚迪', 'sector': '新能源', 'base_price': 220.0, 'market_cap': 6400},
        ]
        
        self.trades = []
        self.random_seed = 42  # 固定随机种子，使结果可重复
        random.seed(self.random_seed)
    
    def generate_trading_dates(self) -> List[str]:
        """生成交易日历（去掉周末）"""
        dates = []
        current = self.start_date
        while current <= self.end_date:
            if current.weekday() < 5:  # 周一=0, 周五=4
                dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)
        return dates
    
    def generate_stock_data(self, date: str) -> List[Dict]:
        """为特定日期生成股票数据"""
        data = []
        
        for stock in self.stock_pool:
            # 生成随机但合理的价格变化
            daily_change = random.uniform(-0.04, 0.06)  # -4%到+6%
            price = stock['base_price'] * (1 + daily_change)
            price_change = daily_change * 100
            
            # 生成其他指标
            turnover = stock['market_cap'] * random.uniform(0.001, 0.005)
            turnover_rate = random.uniform(2.0, 8.0)
            volume_ratio = random.uniform(0.7, 1.8)
            
            # 生成次日开盘价（用于验证）
            next_open_change = random.uniform(-0.05, 0.05)
            next_open = price * (1 + next_open_change)
            
            data.append({
                'date': date,
                'code': stock['code'],
                'name': stock['name'],
                'sector': stock['sector'],
                'price': round(price, 2),
                'price_change': round(price_change, 2),
                'turnover': round(turnover, 2),
                'market_cap': stock['market_cap'],
                'turnover_rate': round(turnover_rate, 2),
                'volume_ratio': round(volume_ratio, 2),
                'next_open': round(next_open, 2),
                'next_open_change': round(next_open_change * 100, 2)
            })
        
        return data
    
    def check_criteria(self, stock: Dict) -> Tuple[bool, List[str]]:
        """检查股票是否符合筛选标准"""
        reasons = []
        passed = True
        
        # 1. 检查代码（主板）
        code = stock['code']
        if not (code.startswith('60') or code.startswith('00')):
            reasons.append("❌ 非主板股票")
            passed = False
        else:
            reasons.append("✅ 主板股票")
        
        # 2. 检查涨幅
        change = stock['price_change']
        if change < self.criteria['price_change_min']:
            reasons.append(f"❌ 涨幅{change:.2f}% < {self.criteria['price_change_min']}%")
            passed = False
        elif change > self.criteria['price_change_max']:
            reasons.append(f"❌ 涨幅{change:.2f}% > {self.criteria['price_change_max']}%")
            passed = False
        else:
            reasons.append(f"✅ 涨幅{change:.2f}% 在范围内")
        
        # 3. 检查成交额
        turnover = stock['turnover']
        if turnover < self.criteria['turnover_min']:
            reasons.append(f"❌ 成交额{turnover:.2f}亿 < {self.criteria['turnover_min']}亿")
            passed = False
        else:
            reasons.append(f"✅ 成交额{turnover:.2f}亿 > {self.criteria['turnover_min']}亿")
        
        # 4. 检查流通市值
        market_cap = stock['market_cap']
        if market_cap < self.criteria['market_cap_min']:
            reasons.append(f"❌ 流通市值{market_cap:.0f}亿 < {self.criteria['market_cap_min']}亿")
            passed = False
        elif market_cap > self.criteria['market_cap_max']:
            reasons.append(f"❌ 流通市值{market_cap:.0f}亿 > {self.criteria['market_cap_max']}亿")
            passed = False
        else:
            reasons.append(f"✅ 流通市值{market_cap:.0f}亿 在范围内")
        
        # 5. 检查换手率
        turnover_rate = stock['turnover_rate']
        if turnover_rate < self.criteria['turnover_rate_min']:
            reasons.append(f"❌ 换手率{turnover_rate:.2f}% < {self.criteria['turnover_rate_min']}%")
            passed = False
        elif turnover_rate > self.criteria['turnover_rate_max']:
            reasons.append(f"❌ 换手率{turnover_rate:.2f}% > {self.criteria['turnover_rate_max']}%")
            passed = False
        else:
            reasons.append(f"✅ 换手率{turnover_rate:.2f}% 在范围内")
        
        # 6. 检查股价
        price = stock['price']
        if price < self.criteria['price_min']:
            reasons.append(f"❌ 股价{price:.2f}元 < {self.criteria['price_min']}元")
            passed = False
        else:
            reasons.append(f"✅ 股价{price:.2f}元 > {self.criteria['price_min']}元")
        
        return passed, reasons
    
    def calculate_score(self, stock: Dict) -> float:
        """计算股票得分"""
        score = 0
        
        # 涨幅得分：接近3%得高分
        change = stock['price_change']
        optimal_change = 3.0
        change_score = 10 - abs(change - optimal_change) * 2
        score += max(0, change_score)
        
        # 成交额得分
        turnover_score = min(10, stock['turnover'] / 5)
        score += turnover_score
        
        # 换手率得分
        turnover_rate = stock['turnover_rate']
        optimal_tr = 5.0
        tr_score = 10 - abs(turnover_rate - optimal_tr) * 2
        score += max(0, tr_score)
        
        # 量比得分
        vr = stock.get('volume_ratio', 1.0)
        if 0.8 <= vr <= 2.0:
            score += 5
        
        return round(score, 2)
    
    def run_backtest(self):
        """运行回测"""
        dates = self.generate_trading_dates()
        
        print("=" * 80)
        print("A股主板隔夜交易法回测报告")
        print(f"时间范围: {self.start_date.date()} 到 {self.end_date.date()}")
        print(f"交易日数量: {len(dates)}")
        print(f"股票池: {len(self.stock_pool)}支主板股票")
        print("=" * 80)
        
        for i, date in enumerate(dates):
            if i == len(dates) - 1:
                continue  # 最后一天没有次日数据
            
            # 生成当日数据
            daily_data = self.generate_stock_data(date)
            
            # 筛选符合条件的股票
            qualified = []
            for stock in daily_data:
                passed, reasons = self.check_criteria(stock)
                if passed:
                    stock['score'] = self.calculate_score(stock)
                    stock['reasons'] = reasons
                    qualified.append(stock)
            
            # 选择得分最高的股票
            if qualified:
                qualified.sort(key=lambda x: x['score'], reverse=True)
                selected = qualified[0]
                
                # 计算盈亏
                pnl = (selected['next_open'] / selected['price'] - 1) * 100
                
                trade = {
                    'date': date,
                    'code': selected['code'],
                    'name': selected['name'],
                    'sector': selected['sector'],
                    'buy_price': selected['price'],
                    'buy_change': selected['price_change'],
                    'sell_price': selected['next_open'],
                    'sell_change': selected['next_open_change'],
                    'pnl': round(pnl, 2),
                    'score': selected['score']
                }
                
                self.trades.append(trade)
                
                print(f"\n📅 交易日: {date}")
                print(f"  选中股票: {selected['name']} ({selected['code']})")
                print(f"  板块: {selected['sector']}")
                print(f"  买入价: {selected['price']:.2f}元 (涨幅: {selected['price_change']:.2f}%)")
                print(f"  次日开盘: {selected['next_open']:.2f}元 (涨跌: {selected['next_open_change']:.2f}%)")
                print(f"  隔夜盈亏: {trade['pnl']:.2f}%")
                print(f"  得分: {selected['score']}")
                print(f"  符合条件数: {len(qualified)}/{len(daily_data)}")
            else:
                print(f"\n📅 交易日: {date}")
                print("  ❌ 未找到符合条件的股票")
                print("  (原因: 无股票满足所有筛选条件)")
        
        print("\n" + "=" * 80)
        print("回测完成!")
    
    def analyze_results(self):
        """分析回测结果"""
        if not self.trades:
            print("没有交易记录可分析")
            return
        
        print("\n" + "=" * 80)
        print("详细数据分析")
        print("=" * 80)
        
        # 基本统计
        total_trades = len(self.trades)
        winning_trades = sum(1 for t in self.trades if t['pnl'] > 0)
        losing_trades = sum(1 for t in self.trades if t['pnl'] < 0)
        even_trades = sum(1 for t in self.trades if t['pnl'] == 0)
        
        win_rate = winning_trades / total_trades * 100
        
        print(f"📊 交易统计:")
        print(f"  总交易次数: {total_trades}")
        print(f"  盈利交易: {winning_trades}次 ({win_rate:.1f}%)")
        print(f"  亏损交易: {losing_trades}次 ({losing_trades/total_trades*100:.1f}%)")
        print(f"  持平交易: {even_trades}次 ({even_trades/total_trades*100:.1f}%)")
        
        # 盈亏统计
        pnls = [t['pnl'] for t in self.trades]
        avg_pnl = sum(pnls) / total_trades
        max_profit = max(pnls)
        max_loss = min(pnls)
        
        # 计算标准差
        variance = sum((p - avg_pnl) ** 2 for p in pnls) / total_trades
        std_pnl = variance ** 0.5
        
        print(f"\n💰 盈亏统计:")
        print(f"  平均盈亏: {avg_pnl:.2f}%")
        print(f"  最大盈利: {max_profit:.2f}%")
        print(f"  最大亏损: {max_loss:.2f}%")
        print(f"  标准差: {std_pnl:.2f}% (波动性)")
        
        # 盈亏比
        winning_pnls = [t['pnl'] for t in self.trades if t['pnl'] > 0]
        losing_pnls = [abs(t['pnl']) for t in self.trades if t['pnl'] < 0]
        
        if winning_pnls and losing_pnls:
            avg_win = sum(winning_pnls) / len(winning_pnls)
            avg_loss = sum(losing_pnls) / len(losing_pnls)
            profit_ratio = avg_win / avg_loss
            print(f"  平均盈利: {avg_win:.2f}%")
            print(f"  平均亏损: {avg_loss:.2f}%")
            print(f"  盈亏比: {profit_ratio:.2f}")
        elif winning_pnls:
            print(f"  🎉 所有交易都盈利!")
        elif losing_pnls:
            print(f"  😢 所有交易都亏损!")
        
        # 板块分析
        print(f"\n🏢 板块分布:")
        sector_stats = {}
        for trade in self.trades:
            sector = trade['sector']
            if sector not in sector_stats:
                sector_stats[sector] = {'count': 0, 'total_pnl': 0}
            sector_stats[sector]['count'] += 1
            sector_stats[sector]['total_pnl'] += trade['pnl']
        
        for sector, stats in sector_stats.items():
            count = stats['count']
            avg_sector_pnl = stats['total_pnl'] / count
            percentage = count / total_trades * 100
            print(f"  {sector}: {count}次 ({percentage:.1f}%) 平均盈亏: {avg_sector_pnl:.2f}%")
        
        # 累计盈亏
        print(f"\n📈 累计盈亏曲线:")
        cumulative = 0
        cumulative_data = []
        print(f"  交易序号 | 当日盈亏 | 累计盈亏")
        print(f"  {'-'*30}")
        for i, trade in enumerate(self.trades, 1):
            cumulative += trade['pnl']
            cumulative_data.append(cumulative)
            print(f"  {i:2d}      | {trade['pnl']:7.2f}% | {cumulative:7.2f}%")
        
        print(f"\n  🔚 最终累计盈亏: {cumulative:.2f}%")
        
        # 胜率分析
        print(f"\n🎯 胜率分析:")
        if win_rate >= 60:
            print(f"  ✅ 优秀! 胜率{win_rate:.1f}% > 60%")
        elif win_rate >= 50:
            print(f"  👍 良好! 胜率{win_rate:.1f}% > 50%")
        elif win_rate >= 40:
            print(f"  ⚠️  一般! 胜率{win_rate:.1f}% 在40-50%之间")
        else:
            print(f"  ❌ 较差! 胜率{win_rate:.1f}% < 40%")
        
        # 风险评估
        print(f"\n⚠️  风险评估:")
        if std_pnl > 3.0:
            print(f"  波动性较高 (标准差: {std_pnl:.2f}%)，建议降低仓位")
        elif std_pnl > 2.0:
            print(f"  波动性适中 (标准差: {std_pnl:.2f}%)，风险可控")
        else:
            print(f"  波动性较低 (标准差: {std_pnl:.2f}%)，策略稳定")
        
        if max_loss < -5:
            print(f"  最大亏损{max_loss:.2f}%较大，需注意止损纪律")
        else:
            print(f"  最大亏损{max_loss:.2f}%在可接受范围内")
        
        # 策略评价
        print(f"\n📋 策略评价:")
        if avg_pnl > 0.5 and win_rate > 50:
            print(f"  🎉 策略表现优秀! 建议继续使用")
        elif avg_pnl > 0:
            print(f"  👍 策略表现良好，可以继续使用但需监控")
        elif avg_pnl > -0.5:
            print(f"  ⚠️  策略表现一般，建议优化筛选条件")
        else:
            print(f"  ❌ 策略表现较差，建议重新评估")
        
        # 详细交易记录
        print(f"\n" + "=" * 80)
        print("详细交易记录表")
        print("=" * 80)
        print("日期       | 股票代码 | 股票名称   | 板块   | 买入价 | 买入涨幅 | 卖出价 | 卖出涨跌 | 盈亏%   | 得分")
        print("-" * 100)
        for trade in self.trades:
            print(f"{trade['date']} | {trade['code']:6s} | {trade['name']:8s} | "
                  f"{trade['sector']:4s} | {trade['buy_price']:6.2f} | "
                  f"{trade['buy_change']:7.2f}% | {trade['sell_price']:6.2f} | "
                  f"{trade['sell_change']:7.2f}% | {trade['pnl']:7.2f}% | {trade['score']:.1f}")
        
        # 保存结果
        self.save_results()
        
        return self.trades
    
    def save_results(self):
        """保存结果到文件"""
        try:
            with open('/tmp/overnight_backtest_simple.txt', 'w', encoding='utf-8') as f:
                f.write("A股主板隔夜交易法回测报告\n")
                f.write(f"时间范围: {self.start_date.date()} 到 {self.end_date.date()}\n")
                f.write(f"交易日数量: {len(self.generate_trading_dates())}\n")
                f.write(f"随机种子: {self.random_seed}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("详细交易记录:\n")
                f.write("日期,股票代码,股票名称,板块,买入价,买入涨幅%,卖出价,卖出涨跌%,隔夜盈亏%,得分\n")
                for trade in self.trades:
                    f.write(f"{trade['date']},{trade['code']},{trade['name']},{trade['sector']},"
                           f"{trade['buy_price']:.2f},{trade['buy_change']:.2f},"
                           f"{trade['sell_price']:.2f},{trade['sell_change']:.2f},"
                           f"{trade['pnl']:.2f},{trade['score']:.1f}\n")
                
                # 统计信息
                f.write("\n" + "=" * 80 + "\n")
                f.write("统计摘要:\n")
                total_trades = len(self.trades)
                winning_trades = sum(1 for t in self.trades if t['pnl'] > 0)
                win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
                avg_pnl = sum(t['pnl'] for t in self.trades) / total_trades if total_trades > 0 else 0
                
                f.write(f"总交易次数: {total_trades}\n")
                f.write(f"胜率: {win_rate:.1f}%\n")
                f.write(f"平均盈亏: {avg_pnl:.2f}%\n")
                
            print(f"\n💾 详细结果已保存: /tmp/overnight_backtest_simple.txt")
        except Exception as e:
            print(f"⚠️  保存结果失败: {e}")

def main():
    """主函数"""
    print("A股主板隔夜交易法回测开始...")
    print("注意: 使用模拟数据进行演示")
    print("如需真实数据，请修改代码连接tushare/akshare等数据源")
    
    # 创建并运行回测
    backtest = SimpleBacktest('2025-03-01', '2025-03-25')
    backtest.run_backtest()
    backtest.analyze_results()
    
    print("\n" + "=" * 80)
    print("回测完成!")
    print("=" * 80)
    print("\n注意事项:")
    print("1. 本回测使用模拟数据，实际效果可能不同")
    print("2. 建议使用真实历史数据重新运行")
    print("3. 策略参数可根据实际表现调整")
    print("4. 股市有风险，投资需谨慎")

if __name__ == "__main__":
    main()