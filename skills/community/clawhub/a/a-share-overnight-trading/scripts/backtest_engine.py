#!/usr/bin/env python3
"""
A股主板隔夜交易法回测引擎
模拟2025年3月1日至3月25日的每日选股和次日验证
"""

import sys
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

class OvernightBacktest:
    """隔夜交易回测引擎"""
    
    def __init__(self, start_date: str, end_date: str):
        """
        初始化回测引擎
        
        Args:
            start_date: 开始日期 '2025-03-01'
            end_date: 结束日期 '2025-03-25'
        """
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # 筛选标准（与skill保持一致）
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
        
        # 回测结果存储
        self.results = []
        self.trades = []
        
    def load_mock_data(self) -> pd.DataFrame:
        """
        加载模拟数据
        
        实际使用时应该替换为真实数据源，如：
        - tushare: pro.daily() + pro.daily_basic()
        - akshare: ak.stock_zh_a_hist()
        - 本地CSV文件
        """
        print("⚠️  注意: 使用模拟数据进行演示")
        print("实际使用时请修改load_mock_data()函数，连接真实数据源")
        
        # 生成模拟交易日历（去掉周末）
        dates = []
        current_date = self.start_date
        while current_date <= self.end_date:
            if current_date.weekday() < 5:  # 周一=0, 周五=4
                dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
        
        # 模拟股票池（20支主板股票）
        stock_pool = [
            {'code': '600030', 'name': '中信证券', 'sector': '券商'},
            {'code': '600036', 'name': '招商银行', 'sector': '银行'},
            {'code': '600519', 'name': '贵州茅台', 'sector': '消费'},
            {'code': '601012', 'name': '隆基绿能', 'sector': '新能源'},
            {'code': '601318', 'name': '中国平安', 'sector': '保险'},
            {'code': '601857', 'name': '中国石油', 'sector': '能源'},
            {'code': '601888', 'name': '中国国旅', 'sector': '消费'},
            {'code': '603259', 'name': '药明康德', 'sector': '医药'},
            {'code': '603501', 'name': '韦尔股份', 'sector': '半导体'},
            {'code': '603986', 'name': '兆易创新', 'sector': '半导体'},
            {'code': '000001', 'name': '平安银行', 'sector': '银行'},
            {'code': '000002', 'name': '万科A', 'sector': '房地产'},
            {'code': '000063', 'name': '中兴通讯', 'sector': '通信'},
            {'code': '000338', 'name': '潍柴动力', 'sector': '机械'},
            {'code': '000538', 'name': '云南白药', 'sector': '医药'},
            {'code': '000625', 'name': '长安汽车', 'sector': '汽车'},
            {'code': '000858', 'name': '五粮液', 'sector': '消费'},
            {'code': '000876', 'name': '新希望', 'sector': '农业'},
            {'code': '002024', 'name': '苏宁易购', 'sector': '零售'},
            {'code': '002594', 'name': '比亚迪', 'sector': '新能源'},
        ]
        
        # 生成模拟价格数据
        data = []
        base_prices = {
            '600030': 22.5, '600036': 35.0, '600519': 1700, '601012': 45.0,
            '601318': 45.0, '601857': 8.5, '601888': 120.0, '603259': 75.0,
            '603501': 90.0, '603986': 110.0, '000001': 15.0, '000002': 25.0,
            '000063': 30.0, '000338': 15.5, '000538': 55.0, '000625': 18.0,
            '000858': 150.0, '000876': 12.0, '002024': 8.0, '002594': 220.0
        }
        
        market_caps = {
            '600030': 3200, '600036': 9000, '600519': 21000, '601012': 3400,
            '601318': 8500, '601857': 15000, '601888': 2500, '603259': 2200,
            '603501': 1100, '603986': 750, '000001': 3000, '000002': 2800,
            '000063': 1400, '000338': 1300, '000538': 1000, '000625': 1800,
            '000858': 5800, '000876': 550, '002024': 750, '002594': 6400
        }
        
        for date in dates:
            for stock in stock_pool:
                code = stock['code']
                base_price = base_prices[code]
                
                # 生成随机但合理的价格变化
                daily_change = np.random.normal(0.002, 0.03)  # 均值0.2%，波动3%
                price = base_price * (1 + daily_change)
                price_change = daily_change * 100  # 转换为百分比
                
                # 生成其他指标
                turnover = market_caps[code] * np.random.uniform(0.001, 0.005)  # 成交额
                turnover_rate = np.random.uniform(2.0, 8.0)  # 换手率
                volume_ratio = np.random.uniform(0.7, 1.8)  # 量比
                
                data.append({
                    'date': date,
                    'code': code,
                    'name': stock['name'],
                    'sector': stock['sector'],
                    'price': round(price, 2),
                    'price_change': round(price_change, 2),
                    'turnover': round(turnover, 2),
                    'market_cap': market_caps[code],
                    'turnover_rate': round(turnover_rate, 2),
                    'volume_ratio': round(volume_ratio, 2),
                    'open_price': round(price * (1 + np.random.normal(-0.01, 0.01)), 2),
                    'high_price': round(price * (1 + abs(np.random.normal(0.02, 0.01))), 2),
                    'low_price': round(price * (1 - abs(np.random.normal(0.015, 0.01))), 2),
                })
        
        df = pd.DataFrame(data)
        
        # 生成次日开盘价（用于验证）
        next_day_data = []
        for idx, row in df.iterrows():
            # 次日开盘价：基于当日收盘价加上随机波动
            next_open = row['price'] * (1 + np.random.normal(0.001, 0.02))
            next_day_data.append({
                'date': row['date'],
                'code': row['code'],
                'next_open': round(next_open, 2),
                'next_open_change': round((next_open / row['price'] - 1) * 100, 2)
            })
        
        self.next_day_df = pd.DataFrame(next_day_data)
        return df
    
    def check_criteria(self, stock_data: pd.Series) -> Tuple[bool, List[str]]:
        """检查单支股票是否符合筛选标准"""
        reasons = []
        passed = True
        
        # 1. 检查代码（主板）
        code = str(stock_data['code'])
        if not (code.startswith('60') or code.startswith('00')):
            reasons.append("❌ 非主板股票")
            passed = False
        else:
            reasons.append("✅ 主板股票")
        
        # 2. 检查涨幅
        change = stock_data['price_change']
        if change < self.criteria['price_change_min']:
            reasons.append(f"❌ 涨幅{change:.2f}% < {self.criteria['price_change_min']}%")
            passed = False
        elif change > self.criteria['price_change_max']:
            reasons.append(f"❌ 涨幅{change:.2f}% > {self.criteria['price_change_max']}%")
            passed = False
        else:
            reasons.append(f"✅ 涨幅{change:.2f}% 在范围内")
        
        # 3. 检查成交额
        turnover = stock_data['turnover']
        if turnover < self.criteria['turnover_min']:
            reasons.append(f"❌ 成交额{turnover:.2f}亿 < {self.criteria['turnover_min']}亿")
            passed = False
        else:
            reasons.append(f"✅ 成交额{turnover:.2f}亿 > {self.criteria['turnover_min']}亿")
        
        # 4. 检查流通市值
        market_cap = stock_data['market_cap']
        if market_cap < self.criteria['market_cap_min']:
            reasons.append(f"❌ 流通市值{market_cap:.0f}亿 < {self.criteria['market_cap_min']}亿")
            passed = False
        elif market_cap > self.criteria['market_cap_max']:
            reasons.append(f"❌ 流通市值{market_cap:.0f}亿 > {self.criteria['market_cap_max']}亿")
            passed = False
        else:
            reasons.append(f"✅ 流通市值{market_cap:.0f}亿 在范围内")
        
        # 5. 检查换手率
        turnover_rate = stock_data['turnover_rate']
        if turnover_rate < self.criteria['turnover_rate_min']:
            reasons.append(f"❌ 换手率{turnover_rate:.2f}% < {self.criteria['turnover_rate_min']}%")
            passed = False
        elif turnover_rate > self.criteria['turnover_rate_max']:
            reasons.append(f"❌ 换手率{turnover_rate:.2f}% > {self.criteria['turnover_rate_max']}%")
            passed = False
        else:
            reasons.append(f"✅ 换手率{turnover_rate:.2f}% 在范围内")
        
        # 6. 检查股价
        price = stock_data['price']
        if price < self.criteria['price_min']:
            reasons.append(f"❌ 股价{price:.2f}元 < {self.criteria['price_min']}元")
            passed = False
        else:
            reasons.append(f"✅ 股价{price:.2f}元 > {self.criteria['price_min']}元")
        
        return passed, reasons
    
    def select_stock_for_date(self, date_data: pd.DataFrame) -> Optional[Dict]:
        """为特定交易日选择一支股票"""
        qualified_stocks = []
        
        for idx, stock in date_data.iterrows():
            passed, reasons = self.check_criteria(stock)
            if passed:
                qualified_stocks.append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'sector': stock['sector'],
                    'price': stock['price'],
                    'price_change': stock['price_change'],
                    'turnover': stock['turnover'],
                    'market_cap': stock['market_cap'],
                    'reasons': reasons,
                    'score': self.calculate_score(stock)
                })
        
        if not qualified_stocks:
            return None
        
        # 按得分排序，选择最高分
        qualified_stocks.sort(key=lambda x: x['score'], reverse=True)
        return qualified_stocks[0]
    
    def calculate_score(self, stock: pd.Series) -> float:
        """计算股票得分（用于排序）"""
        score = 0
        
        # 涨幅得分：接近3%得高分
        change = stock['price_change']
        optimal_change = 3.0
        change_score = 10 - abs(change - optimal_change) * 2
        score += max(0, change_score)
        
        # 成交额得分：越大越好
        turnover_score = min(10, stock['turnover'] / 5)  # 每5亿得1分，最高10分
        score += turnover_score
        
        # 换手率得分：接近5%得高分
        turnover_rate = stock['turnover_rate']
        optimal_tr = 5.0
        tr_score = 10 - abs(turnover_rate - optimal_tr) * 2
        score += max(0, tr_score)
        
        # 量比得分（如果可用）
        if 'volume_ratio' in stock:
            vr = stock['volume_ratio']
            if 0.8 <= vr <= 2.0:
                score += 5
        
        return round(score, 2)
    
    def run_backtest(self, data_df: pd.DataFrame):
        """运行回测"""
        dates = sorted(data_df['date'].unique())
        
        print(f"开始回测: {self.start_date.date()} 到 {self.end_date.date()}")
        print(f"交易日数量: {len(dates)}")
        print("=" * 80)
        
        for i, date in enumerate(dates):
            if i == len(dates) - 1:
                continue  # 最后一天没有次日数据
            
            date_data = data_df[data_df['date'] == date]
            selected = self.select_stock_for_date(date_data)
            
            if selected:
                # 获取次日开盘价
                next_day = self.next_day_df[
                    (self.next_day_df['date'] == date) & 
                    (self.next_day_df['code'] == selected['code'])
                ]
                
                if not next_day.empty:
                    next_open = next_day.iloc[0]['next_open']
                    next_change = next_day.iloc[0]['next_open_change']
                    
                    trade = {
                        'date': date,
                        'code': selected['code'],
                        'name': selected['name'],
                        'buy_price': selected['price'],
                        'sell_price': next_open,
                        'buy_change': selected['price_change'],
                        'sell_change': next_change,
                        'pnl': round((next_open / selected['price'] - 1) * 100, 2),
                        'sector': selected['sector'],
                        'score': selected['score']
                    }
                    
                    self.trades.append(trade)
                    
                    print(f"\n交易日: {date}")
                    print(f"选中股票: {selected['name']} ({selected['code']})")
                    print(f"买入价: {selected['price']:.2f}元 (涨幅: {selected['price_change']:.2f}%)")
                    print(f"次日开盘价: {next_open:.2f}元 (涨幅: {next_change:.2f}%)")
                    print(f"隔夜盈亏: {trade['pnl']:.2f}%")
                    print(f"得分: {selected['score']}")
                    print(f"板块: {selected['sector']}")
                    print("-" * 60)
                else:
                    print(f"\n交易日: {date}")
                    print(f"选中股票: {selected['name']} ({selected['code']})")
                    print("⚠️  警告: 无次日数据")
            else:
                print(f"\n交易日: {date}")
                print("❌ 未找到符合条件的股票")
                print("-" * 60)
        
        print("\n" + "=" * 80)
        print("回测完成!")
    
    def analyze_results(self):
        """分析回测结果"""
        if not self.trades:
            print("没有交易记录可分析")
            return
        
        # 转换为DataFrame便于分析
        trades_df = pd.DataFrame(self.trades)
        
        print("\n" + "=" * 80)
        print("回测结果分析")
        print("=" * 80)
        
        # 基本统计
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        even_trades = len(trades_df[trades_df['pnl'] == 0])
        
        win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
        
        print(f"总交易次数: {total_trades}")
        print(f"盈利交易: {winning_trades} ({win_rate:.1f}%)")
        print(f"亏损交易: {losing_trades} ({(losing_trades/total_trades*100):.1f}%)")
        print(f"持平交易: {even_trades} ({(even_trades/total_trades*100):.1f}%)")
        
        # 盈亏统计
        if total_trades > 0:
            avg_profit = trades_df['pnl'].mean()
            median_profit = trades_df['pnl'].median()
            max_profit = trades_df['pnl'].max()
            max_loss = trades_df['pnl'].min()
            std_profit = trades_df['pnl'].std()
            
            print(f"\n盈亏统计:")
            print(f"平均盈亏: {avg_profit:.2f}%")
            print(f"中位数盈亏: {median_profit:.2f}%")
            print(f"最大盈利: {max_profit:.2f}%")
            print(f"最大亏损: {max_loss:.2f}%")
            print(f"标准差: {std_profit:.2f}% (波动性)")
            
            # 盈亏比
            winning_pnl = trades_df[trades_df['pnl'] > 0]['pnl'].mean()
            losing_pnl = abs(trades_df[trades_df['pnl'] < 0]['pnl'].mean())
            
            if losing_pnl > 0:
                profit_ratio = winning_pnl / losing_pnl
                print(f"盈亏比: {profit_ratio:.2f} (盈利/亏损)")
            else:
                print("盈亏比: ∞ (无亏损交易)")
        
        # 板块分析
        print(f"\n板块分布:")
        sector_counts = trades_df['sector'].value_counts()
        for sector, count in sector_counts.items():
            percentage = count / total_trades * 100
            avg_pnl = trades_df[trades_df['sector'] == sector]['pnl'].mean()
            print(f"  {sector}: {count}次 ({percentage:.1f}%) 平均盈亏: {avg_pnl:.2f}%")
        
        # 时间序列分析
        print(f"\n时间序列表现:")
        trades_df['cumulative_pnl'] = trades_df['pnl'].cumsum()
        
        # 绘制累计盈亏曲线（如果可能）
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(range(len(trades_df)), trades_df['cumulative_pnl'], marker='o')
            plt.xlabel('交易序号')
            plt.ylabel('累计盈亏 (%)')
            plt.title('隔夜交易累计盈亏曲线')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # 保存图表
            chart_path = '/tmp/overnight_backtest_chart.png'
            plt.savefig(chart_path, dpi=150)
            print(f"📈 盈亏曲线图已保存: {chart_path}")
        except Exception as e:
            print(f"⚠️  无法生成图表: {e}")
        
        # 详细交易记录
        print(f"\n详细交易记录:")
        print(trades_df.to_string(index=False))
        
        # 保存结果到文件
        output_path = '/tmp/overnight_backtest_results.csv'
        trades_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\n📊 详细结果已保存: {output_path}")
        
        return trades_df

def main():
    parser = argparse.ArgumentParser(description='A股主板隔夜交易法回测引擎')
    parser.add_argument('--start', default='2025-03-01', help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end', default='2025-03-25', help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--data-file', help='CSV数据文件路径（如提供则使用真实数据）')
    
    args = parser.parse_args()
    
    # 创建回测引擎
    backtest = OvernightBacktest(args.start, args.end)
    
    # 加载数据
    if args.data_file:
        print(f"加载数据文件: {args.data_file}")
        try:
            data_df = pd.read_csv(args.data_file)
        except Exception as e:
            print(f"❌ 加载数据文件失败: {e}")
            return 1
    else:
        data_df = backtest.load_mock_data()
    
    # 运行回测
    backtest.run_backtest(data_df)
    
    # 分析结果
    backtest.analyze_results()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())