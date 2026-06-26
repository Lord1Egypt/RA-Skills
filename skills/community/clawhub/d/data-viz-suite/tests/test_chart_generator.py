"""
图表生成器单元测试
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.chart_generator import ChartGenerator
import pandas as pd


class TestChartGenerator(unittest.TestCase):
    """测试 ChartGenerator 类"""
    
    def setUp(self):
        """测试前准备"""
        self.gen = ChartGenerator(theme='corporate')
        self.sample_data = {
            '月份': ['1月', '2月', '3月'],
            '销售额': [100, 150, 200],
            '利润': [30, 45, 60]
        }
    
    def test_init_default_theme(self):
        """测试默认主题初始化"""
        gen = ChartGenerator()
        self.assertEqual(gen.theme['primary'], '#1f77b4')
    
    def test_init_custom_theme(self):
        """测试自定义主题初始化"""
        gen = ChartGenerator(theme='dark')
        self.assertEqual(gen.theme['bg'], '#1a1a1a')
    
    def test_line_chart(self):
        """测试折线图生成"""
        fig = self.gen.line_chart(self.sample_data, x='月份', y='销售额', title='测试')
        self.assertIsNotNone(fig)
        self.assertEqual(fig.layout.title.text, '测试')
    
    def test_line_chart_multi_y(self):
        """测试多Y轴折线图"""
        fig = self.gen.line_chart(self.sample_data, x='月份', 
                                 y=['销售额', '利润'], title='多轴测试')
        self.assertIsNotNone(fig)
    
    def test_bar_chart_vertical(self):
        """测试垂直柱状图"""
        fig = self.gen.bar_chart(self.sample_data, x='月份', y='销售额', title='测试')
        self.assertIsNotNone(fig)
    
    def test_bar_chart_horizontal(self):
        """测试水平柱状图"""
        fig = self.gen.bar_chart(self.sample_data, x='月份', y='销售额', 
                                title='测试', orientation='h')
        self.assertIsNotNone(fig)
    
    def test_pie_chart(self):
        """测试饼图"""
        data = {'类别': ['A', 'B', 'C'], '值': [30, 40, 30]}
        fig = self.gen.pie_chart(data, names='类别', values='值', title='测试')
        self.assertIsNotNone(fig)
    
    def test_scatter_chart(self):
        """测试散点图"""
        data = {'x': [1, 2, 3], 'y': [4, 5, 6], 'c': ['A', 'B', 'A']}
        fig = self.gen.scatter_chart(data, x='x', y='y', color='c', title='测试')
        self.assertIsNotNone(fig)
    
    def test_heatmap(self):
        """测试热力图"""
        data = [[1, 0.5], [0.5, 1]]
        fig = self.gen.heatmap(data, title='测试')
        self.assertIsNotNone(fig)
    
    def test_dataframe_input(self):
        """测试 DataFrame 输入"""
        df = pd.DataFrame(self.sample_data)
        fig = self.gen.line_chart(df, x='月份', y='销售额')
        self.assertIsNotNone(fig)


if __name__ == '__main__':
    print("🧪 运行 Data Viz Suite 单元测试...\n")
    unittest.main(verbosity=2)
