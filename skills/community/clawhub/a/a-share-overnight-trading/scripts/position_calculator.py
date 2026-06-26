#!/usr/bin/env python3
"""
隔夜交易仓位计算器
根据资金总量、风险承受能力和股票价格计算合适的买入数量
"""

import sys
import argparse

class PositionCalculator:
    """仓位计算器"""
    
    def __init__(self, total_capital, risk_tolerance='medium'):
        """
        初始化计算器
        
        Args:
            total_capital: 总资金量（元）
            risk_tolerance: 风险承受能力 low/medium/high
        """
        self.total_capital = float(total_capital)
        self.risk_tolerance = risk_tolerance.lower()
        
        # 风险参数配置
        self.risk_params = {
            'low': {
                'max_single_position': 0.10,  # 单支股票最大仓位 10%
                'max_total_position': 0.30,   # 总仓位上限 30%
                'recommended_position': 0.05  # 推荐仓位 5%
            },
            'medium': {
                'max_single_position': 0.20,  # 单支股票最大仓位 20%
                'max_total_position': 0.50,   # 总仓位上限 50%
                'recommended_position': 0.12  # 推荐仓位 12%
            },
            'high': {
                'max_single_position': 0.30,  # 单支股票最大仓位 30%
                'max_total_position': 0.70,   # 总仓位上限 70%
                'recommended_position': 0.18  # 推荐仓位 18%
            }
        }
        
        if self.risk_tolerance not in self.risk_params:
            raise ValueError(f"风险承受能力必须是 low/medium/high 之一，当前为: {risk_tolerance}")
        
        self.params = self.risk_params[self.risk_tolerance]
    
    def calculate_position(self, stock_price, position_percent=None):
        """
        计算买入数量
        
        Args:
            stock_price: 股票价格（元）
            position_percent: 仓位百分比，如为None则使用推荐仓位
        
        Returns:
            dict: 包含各种仓位建议的计算结果
        """
        if position_percent is None:
            position_percent = self.params['recommended_position']
        
        # 确保仓位不超过单支股票最大限制
        position_percent = min(position_percent, self.params['max_single_position'])
        
        # 计算可投入金额
        capital_to_use = self.total_capital * position_percent
        
        # 计算可买入数量（取整，A股最小100股）
        shares = int(capital_to_use // stock_price)
        shares = (shares // 100) * 100  # 取整到100股的倍数
        
        # 实际投入金额
        actual_capital = shares * stock_price
        actual_percent = actual_capital / self.total_capital
        
        # 计算不同仓位级别的数量
        max_shares = int((self.total_capital * self.params['max_single_position']) // stock_price)
        max_shares = (max_shares // 100) * 100
        
        min_shares = 100  # 最小100股
        
        return {
            'total_capital': self.total_capital,
            'stock_price': stock_price,
            'requested_percent': position_percent,
            'requested_capital': capital_to_use,
            'actual_shares': shares,
            'actual_capital': actual_capital,
            'actual_percent': actual_percent,
            'max_single_position': self.params['max_single_position'],
            'max_single_capital': self.total_capital * self.params['max_single_position'],
            'max_shares': max_shares,
            'min_shares': min_shares,
            'risk_level': self.risk_tolerance
        }
    
    def calculate_multi_stock(self, stock_prices, position_percents=None):
        """
        计算多支股票的仓位
        
        Args:
            stock_prices: 股票价格列表
            position_percents: 每支股票的仓位百分比列表
        
        Returns:
            list: 每支股票的计算结果
        """
        if position_percents is None:
            # 如果没有指定，平均分配推荐仓位
            n = len(stock_prices)
            recommended_percent = self.params['recommended_position']
            position_percents = [recommended_percent / n] * n
        
        results = []
        for i, (price, percent) in enumerate(zip(stock_prices, position_percents)):
            result = self.calculate_position(price, percent)
            result['stock_index'] = i + 1
            results.append(result)
        
        return results
    
    def print_single_result(self, result):
        """打印单支股票计算结果"""
        print("=" * 60)
        print("仓位计算报告 - 单支股票")
        print("=" * 60)
        print(f"总资金: {result['total_capital']:,.2f} 元")
        print(f"股票价格: {result['stock_price']:.2f} 元/股")
        print(f"风险等级: {result['risk_level'].upper()}")
        print("-" * 60)
        
        print(f"\n风险参数 ({result['risk_level'].upper()}):")
        print(f"  单支股票最大仓位: {result['max_single_position']*100:.1f}%")
        print(f"  单支股票最大金额: {result['max_single_capital']:,.2f} 元")
        
        print(f"\n您的仓位设置:")
        print(f"  请求仓位: {result['requested_percent']*100:.1f}%")
        print(f"  请求金额: {result['requested_capital']:,.2f} 元")
        
        print(f"\n实际可买入:")
        print(f"  买入数量: {result['actual_shares']:,} 股")
        print(f"  买入金额: {result['actual_capital']:,.2f} 元")
        print(f"  实际仓位: {result['actual_percent']*100:.2f}%")
        
        print(f"\n其他参考:")
        print(f"  最大可买入: {result['max_shares']:,} 股")
        print(f"  最小可买入: {result['min_shares']:,} 股")
        
        # 风险提示
        print(f"\n⚠️  风险提示:")
        if result['actual_percent'] > 0.15:
            print("  当前仓位较重，请确保有严格止损纪律")
        elif result['actual_percent'] < 0.05:
            print("  当前仓位较轻，对总资金影响有限")
        else:
            print("  当前仓位适中")
        
        print("=" * 60)
    
    def print_multi_result(self, results):
        """打印多支股票计算结果"""
        print("=" * 60)
        print("仓位计算报告 - 多支股票")
        print("=" * 60)
        
        total_capital = results[0]['total_capital']
        total_actual_capital = sum(r['actual_capital'] for r in results)
        total_percent = total_actual_capital / total_capital
        
        print(f"总资金: {total_capital:,.2f} 元")
        print(f"风险等级: {results[0]['risk_level'].upper()}")
        print(f"股票数量: {len(results)} 支")
        print("-" * 60)
        
        # 每支股票详情
        for i, result in enumerate(results, 1):
            print(f"\n股票 #{i}:")
            print(f"  价格: {result['stock_price']:.2f} 元")
            print(f"  数量: {result['actual_shares']:,} 股")
            print(f"  金额: {result['actual_capital']:,.2f} 元")
            print(f"  仓位: {result['actual_percent']*100:.2f}%")
        
        print(f"\n汇总:")
        print(f"  总买入金额: {total_actual_capital:,.2f} 元")
        print(f"  总仓位: {total_percent*100:.2f}%")
        print(f"  剩余资金: {total_capital - total_actual_capital:,.2f} 元")
        
        # 风险检查
        max_total_percent = self.params['max_total_position']
        print(f"\n⚠️  风险检查:")
        print(f"  总仓位上限: {max_total_percent*100:.0f}%")
        
        if total_percent > max_total_percent:
            print(f"  ❌ 警告: 总仓位 {total_percent*100:.1f}% 超过上限 {max_total_percent*100:.0f}%")
            print("  建议: 减少买入数量或选择较少股票")
        elif total_percent > max_total_percent * 0.8:
            print(f"  ⚠️  注意: 总仓位 {total_percent*100:.1f}% 接近上限")
            print("  建议: 谨慎考虑是否继续加仓")
        else:
            print(f"  ✅ 安全: 总仓位 {total_percent*100:.1f}% 在安全范围内")
        
        print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='隔夜交易仓位计算器')
    parser.add_argument('--capital', type=float, required=True, help='总资金量（元）')
    parser.add_argument('--price', type=float, help='股票价格（元），单支股票模式')
    parser.add_argument('--prices', type=float, nargs='+', help='多支股票价格列表，多支股票模式')
    parser.add_argument('--percent', type=float, default=0.12, help='单支股票仓位百分比（默认12%%，即0.12）')
    parser.add_argument('--percents', type=float, nargs='+', help='多支股票仓位百分比列表')
    parser.add_argument('--risk', choices=['low', 'medium', 'high'], default='medium', 
                       help='风险承受能力 low/medium/high（默认medium）')
    
    args = parser.parse_args()
    
    # 验证输入
    if args.capital <= 0:
        print("错误: 总资金量必须大于0")
        return 1
    
    if args.price and args.prices:
        print("错误: 不能同时指定 --price 和 --prices")
        return 1
    
    if not args.price and not args.prices:
        print("错误: 必须指定 --price 或 --prices")
        return 1
    
    try:
        calculator = PositionCalculator(args.capital, args.risk)
        
        if args.price:
            # 单支股票模式
            if args.price <= 0:
                print("错误: 股票价格必须大于0")
                return 1
            
            result = calculator.calculate_position(args.price, args.percent)
            calculator.print_single_result(result)
            
        elif args.prices:
            # 多支股票模式
            if any(p <= 0 for p in args.prices):
                print("错误: 所有股票价格必须大于0")
                return 1
            
            if args.percents and len(args.percents) != len(args.prices):
                print("错误: 仓位百分比数量必须与股票价格数量一致")
                return 1
            
            results = calculator.calculate_multi_stock(args.prices, args.percents)
            calculator.print_multi_result(results)
    
    except ValueError as e:
        print(f"错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

# 使用示例:
# 单支股票:
# python position_calculator.py --capital 100000 --price 25.0 --percent 0.15 --risk medium
#
# 多支股票（平均分配）:
# python position_calculator.py --capital 100000 --prices 25.0 30.0 40.0 --risk medium
#
# 多支股票（指定仓位）:
# python position_calculator.py --capital 100000 --prices 25.0 30.0 --percents 0.1 0.15 --risk medium