#!/usr/bin/env python3
"""
隔夜交易法快速检查脚本
用于快速验证一支股票是否符合隔夜交易筛选条件

注意：需要配置数据源（如tushare、akshare等API）
"""

import sys
import argparse
from datetime import datetime

class OvernightStockChecker:
    """隔夜交易股票检查器"""
    
    def __init__(self):
        """初始化筛选标准"""
        self.criteria = {
            # 主板代码范围
            'valid_prefixes': ['60', '00'],  # 沪市主板60, 深市主板00
            
            # 量化指标
            'price_change_min': 1.0,    # 最小涨幅%
            'price_change_max': 5.0,    # 最大涨幅%
            'turnover_min': 1.0,        # 最小成交额(亿元)
            'market_cap_min': 50.0,     # 最小流通市值(亿元)
            'market_cap_max': 500.0,    # 最大流通市值(亿元)
            'turnover_rate_min': 3.0,   # 最小换手率%
            'turnover_rate_max': 10.0,  # 最大换手率%
            'price_min': 5.0,           # 最低股价(元)
            'volume_ratio_min': 0.8,    # 最小量比
            'volume_ratio_max': 2.0,    # 最大量比
        }
        
    def check_stock_code(self, code):
        """检查股票代码是否符合主板要求"""
        if not code:
            return False, "股票代码为空"
        
        # 标准化代码格式（去除交易所前缀）
        if code.startswith('sh') or code.startswith('sz'):
            pure_code = code[2:]
        else:
            pure_code = code
            
        # 检查前缀
        prefix = pure_code[:2]
        if prefix not in self.criteria['valid_prefixes']:
            return False, f"代码{pure_code}不属于主板(60/00开头)"
            
        return True, f"代码{pure_code}符合主板要求"
    
    def check_quantitative_indicators(self, stock_data):
        """
        检查量化指标
        
        stock_data需要包含以下字段：
        - price_change: 涨幅(%)
        - turnover: 成交额(亿元)
        - market_cap: 流通市值(亿元)
        - turnover_rate: 换手率(%)
        - price: 当前价格(元)
        - volume_ratio: 量比
        """
        results = []
        all_pass = True
        
        # 1. 检查涨幅
        change = stock_data.get('price_change', 0)
        if change < self.criteria['price_change_min']:
            results.append(f"❌ 涨幅{change:.2f}% < {self.criteria['price_change_min']}%")
            all_pass = False
        elif change > self.criteria['price_change_max']:
            results.append(f"❌ 涨幅{change:.2f}% > {self.criteria['price_change_max']}%")
            all_pass = False
        else:
            results.append(f"✅ 涨幅{change:.2f}% 在{self.criteria['price_change_min']}%-{self.criteria['price_change_max']}%范围内")
        
        # 2. 检查成交额
        turnover = stock_data.get('turnover', 0)
        if turnover < self.criteria['turnover_min']:
            results.append(f"❌ 成交额{turnover:.2f}亿元 < {self.criteria['turnover_min']}亿元")
            all_pass = False
        else:
            results.append(f"✅ 成交额{turnover:.2f}亿元 > {self.criteria['turnover_min']}亿元")
        
        # 3. 检查流通市值
        market_cap = stock_data.get('market_cap', 0)
        if market_cap < self.criteria['market_cap_min']:
            results.append(f"❌ 流通市值{market_cap:.2f}亿元 < {self.criteria['market_cap_min']}亿元")
            all_pass = False
        elif market_cap > self.criteria['market_cap_max']:
            results.append(f"❌ 流通市值{market_cap:.2f}亿元 > {self.criteria['market_cap_max']}亿元")
            all_pass = False
        else:
            results.append(f"✅ 流通市值{market_cap:.2f}亿元 在{self.criteria['market_cap_min']}-{self.criteria['market_cap_max']}亿元范围内")
        
        # 4. 检查换手率
        turnover_rate = stock_data.get('turnover_rate', 0)
        if turnover_rate < self.criteria['turnover_rate_min']:
            results.append(f"❌ 换手率{turnover_rate:.2f}% < {self.criteria['turnover_rate_min']}%")
            all_pass = False
        elif turnover_rate > self.criteria['turnover_rate_max']:
            results.append(f"❌ 换手率{turnover_rate:.2f}% > {self.criteria['turnover_rate_max']}%")
            all_pass = False
        else:
            results.append(f"✅ 换手率{turnover_rate:.2f}% 在{self.criteria['turnover_rate_min']}%-{self.criteria['turnover_rate_max']}%范围内")
        
        # 5. 检查股价
        price = stock_data.get('price', 0)
        if price < self.criteria['price_min']:
            results.append(f"❌ 股价{price:.2f}元 < {self.criteria['price_min']}元")
            all_pass = False
        else:
            results.append(f"✅ 股价{price:.2f}元 > {self.criteria['price_min']}元")
        
        # 6. 检查量比（可选）
        volume_ratio = stock_data.get('volume_ratio', 1.0)
        if volume_ratio < self.criteria['volume_ratio_min']:
            results.append(f"⚠️  量比{volume_ratio:.2f} < {self.criteria['volume_ratio_min']}（成交量偏低）")
        elif volume_ratio > self.criteria['volume_ratio_max']:
            results.append(f"⚠️  量比{volume_ratio:.2f} > {self.criteria['volume_ratio_max']}（成交量异常）")
        else:
            results.append(f"✅ 量比{volume_ratio:.2f} 在{self.criteria['volume_ratio_min']}-{self.criteria['volume_ratio_max']}范围内")
        
        return all_pass, results
    
    def get_mock_data(self, code):
        """
        获取模拟数据（实际使用时替换为真实数据源）
        
        真实数据源示例（使用tushare）：
        import tushare as ts
        pro = ts.pro_api('your_token')
        
        # 获取实时行情
        df = pro.daily(ts_code=code+'.SH' if code.startswith('60') else code+'.SZ')
        # 获取市值数据
        df_basic = pro.daily_basic(ts_code=code+'.SH' if code.startswith('60') else code+'.SZ')
        """
        # 模拟数据 - 实际使用时请替换
        mock_data = {
            '600030': {  # 中信证券
                'price_change': 2.3,
                'turnover': 25.8,
                'market_cap': 3200.0,
                'turnover_rate': 4.2,
                'price': 22.5,
                'volume_ratio': 1.2
            },
            '601012': {  # 隆基绿能
                'price_change': 3.1,
                'turnover': 18.3,
                'market_cap': 2200.0,
                'turnover_rate': 3.8,
                'price': 45.6,
                'volume_ratio': 1.5
            },
            '000001': {  # 平安银行
                'price_change': 1.2,
                'turnover': 12.5,
                'market_cap': 2800.0,
                'turnover_rate': 2.9,
                'price': 15.8,
                'volume_ratio': 0.9
            }
        }
        
        # 提取纯数字代码
        pure_code = code[2:] if code.startswith(('sh', 'sz')) else code
        
        return mock_data.get(pure_code, {
            'price_change': 2.0,
            'turnover': 5.0,
            'market_cap': 200.0,
            'turnover_rate': 5.0,
            'price': 20.0,
            'volume_ratio': 1.0
        })
    
    def print_summary(self, code, code_check_result, quant_check_result, quant_results):
        """打印检查结果摘要"""
        print("=" * 60)
        print(f"股票代码: {code}")
        print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # 代码检查结果
        code_pass, code_msg = code_check_result
        print(f"代码检查: {'✅ 通过' if code_pass else '❌ 失败'} - {code_msg}")
        
        # 量化指标检查结果
        quant_pass, _ = quant_check_result
        print(f"量化指标: {'✅ 通过' if quant_pass else '❌ 失败'}")
        
        print("-" * 60)
        print("详细检查结果:")
        for result in quant_results:
            print(f"  {result}")
        
        print("-" * 60)
        
        # 总体结论
        if code_pass and quant_pass:
            print("🎉 总体结论: 符合隔夜交易筛选条件")
            print("建议: 可进入人工复核阶段（技术面、消息面等）")
        else:
            print("❌ 总体结论: 不符合隔夜交易筛选条件")
            print("建议: 放弃或寻找其他标的")
        
        print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='隔夜交易法股票检查工具')
    parser.add_argument('code', help='股票代码（如600030或sh600030）')
    parser.add_argument('--mock', action='store_true', help='使用模拟数据')
    
    args = parser.parse_args()
    
    checker = OvernightStockChecker()
    
    # 1. 检查股票代码
    code_check_result = checker.check_stock_code(args.code)
    
    # 2. 获取数据并检查量化指标
    if args.mock:
        stock_data = checker.get_mock_data(args.code)
    else:
        print("注意: 当前使用模拟数据。请配置真实数据源后重试。")
        print("在quick_check.py中修改get_mock_data()函数，添加tushare/akshare等数据源。")
        stock_data = checker.get_mock_data(args.code)
    
    quant_check_result = checker.check_quantitative_indicators(stock_data)
    quant_pass, quant_results = quant_check_result
    
    # 3. 打印结果
    checker.print_summary(args.code, code_check_result, quant_check_result, quant_results)
    
    # 返回退出码
    code_pass, _ = code_check_result
    if code_pass and quant_pass:
        return 0  # 通过
    else:
        return 1  # 不通过

if __name__ == "__main__":
    sys.exit(main())