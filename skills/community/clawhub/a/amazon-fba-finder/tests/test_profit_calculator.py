"""
利润计算器单元测试
"""

import unittest
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from profit_calculator import ProfitCalculator, ProductDimensions


class TestProfitCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = ProfitCalculator(marketplace="US")
        self.sample_dimensions = ProductDimensions(
            length=12,
            width=9,
            height=1.5,
            weight=2.5
        )
    
    def test_basic_profit_calculation(self):
        """测试基本利润计算"""
        result = self.calculator.calculate_profit(
            selling_price=35.99,
            product_cost=8.50,
            dimensions=self.sample_dimensions,
            shipping_cost=2.0,
            monthly_sales=300
        )
        
        self.assertGreater(result.net_profit, 0)
        self.assertGreater(result.profit_margin, 15)
        self.assertIn('recommendation', result)
    
    def test_low_margin_product(self):
        """测试低利润产品"""
        result = self.calculator.calculate_profit(
            selling_price=20.00,
            product_cost=15.00,
            dimensions=self.sample_dimensions
        )
        
        self.assertLess(result.profit_margin, 20)
        self.assertIn('利润率过低', result.recommendation)
    
    def test_high_margin_product(self):
        """测试高利润产品"""
        result = self.calculator.calculate_profit(
            selling_price=50.00,
            product_cost=10.00,
            dimensions=self.sample_dimensions
        )
        
        self.assertGreater(result.profit_margin, 30)
        self.assertIn('优秀', result.recommendation)
    
    def test_fba_fee_calculation(self):
        """测试 FBA 费用计算"""
        # 小标准尺寸
        small = ProductDimensions(10, 8, 0.5, 0.8)
        fee_small = self.calculator._calculate_fba_fee(small)
        self.assertEqual(fee_small, 3.22)
        
        # 大标准尺寸
        large = ProductDimensions(12, 10, 2, 1.5)
        fee_large = self.calculator._calculate_fba_fee(large)
        self.assertGreater(fee_large, 3.22)
    
    def test_size_tier_determination(self):
        """测试尺寸分段判断"""
        small = ProductDimensions(10, 8, 0.5, 0.8)
        tier = self.calculator._determine_size_tier(small)
        self.assertEqual(tier.value, "small_standard")
    
    def test_break_even_analysis(self):
        """测试盈亏平衡分析"""
        result = self.calculator.calculate_profit(
            selling_price=30.00,
            product_cost=8.00,
            dimensions=self.sample_dimensions
        )
        
        self.assertGreater(result.breakeven_units, 0)
        self.assertLess(result.breakeven_units, 100000)
    
    def test_scenario_comparison(self):
        """测试场景对比"""
        scenarios = self.calculator.compare_scenarios(
            base_price=29.99,
            cost=7.50,
            dimensions=self.sample_dimensions
        )
        
        self.assertEqual(len(scenarios), 5)
        self.assertIn("0%", scenarios)
        self.assertIn("+5%", scenarios)
        self.assertIn("-5%", scenarios)


class TestProductDimensions(unittest.TestCase):
    
    def test_dimensions_creation(self):
        """测试尺寸对象创建"""
        dims = ProductDimensions(12, 9, 1.5, 2.5)
        
        self.assertEqual(dims.length, 12)
        self.assertEqual(dims.width, 9)
        self.assertEqual(dims.height, 1.5)
        self.assertEqual(dims.weight, 2.5)


if __name__ == '__main__':
    unittest.main()
