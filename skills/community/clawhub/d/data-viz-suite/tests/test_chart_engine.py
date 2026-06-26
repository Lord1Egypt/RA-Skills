"""
Data Viz Suite - 单元测试
"""

import unittest
import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from chart_engine import ChartEngine, Theme
from dashboard import Dashboard
from report_generator import ReportGenerator


class TestChartEngine(unittest.TestCase):
    """测试图表引擎"""
    
    def setUp(self):
        self.data = {
            'x': ['A', 'B', 'C'],
            'y': [1, 2, 3]
        }
    
    def test_init(self):
        """测试初始化"""
        engine = ChartEngine(backend='plotly')
        self.assertEqual(engine.backend, 'plotly')
        
        engine = ChartEngine(backend='matplotlib')
        self.assertEqual(engine.backend, 'matplotlib')
    
    def test_line_chart(self):
        """测试折线图"""
        engine = ChartEngine(backend='plotly')
        fig = engine.line_chart(self.data, x='x', y='y', title='Test')
        self.assertIsNotNone(fig)
    
    def test_bar_chart(self):
        """测试柱状图"""
        engine = ChartEngine(backend='plotly')
        fig = engine.bar_chart(self.data, x='x', y='y', title='Test')
        self.assertIsNotNone(fig)
    
    def test_pie_chart(self):
        """测试饼图"""
        engine = ChartEngine(backend='plotly')
        fig = engine.pie_chart(self.data, values='y', names='x', title='Test')
        self.assertIsNotNone(fig)
    
    def test_scatter_chart(self):
        """测试散点图"""
        engine = ChartEngine(backend='plotly')
        scatter_data = {'a': [1, 2, 3], 'b': [4, 5, 6]}
        fig = engine.scatter_chart(scatter_data, x='a', y='b')
        self.assertIsNotNone(fig)
    
    def test_heatmap(self):
        """测试热力图"""
        engine = ChartEngine(backend='plotly')
        data = np.array([[1, 2], [3, 4]])
        fig = engine.heatmap(data, title='Test')
        self.assertIsNotNone(fig)


class TestDashboard(unittest.TestCase):
    """测试仪表盘"""
    
    def test_init(self):
        """测试初始化"""
        dash = Dashboard(title='Test', theme='light')
        self.assertEqual(dash.title, 'Test')
        self.assertEqual(dash.theme, 'light')
    
    def test_add_kpi(self):
        """测试添加KPI"""
        dash = Dashboard()
        dash.add_kpi('销售额', 1000, change=10)
        self.assertEqual(len(dash.kpis), 1)
        self.assertEqual(dash.kpis[0]['title'], '销售额')
    
    def test_add_chart(self):
        """测试添加图表"""
        dash = Dashboard()
        engine = ChartEngine(backend='plotly')
        fig = engine.line_chart({'x': [1], 'y': [2]}, x='x', y='y')
        dash.add_chart('test', fig, 'Test Chart')
        self.assertEqual(len(dash.charts), 1)


class TestReportGenerator(unittest.TestCase):
    """测试报表生成器"""
    
    def test_init(self):
        """测试初始化"""
        report = ReportGenerator(title='Test Report')
        self.assertEqual(report.title, 'Test Report')
    
    def test_add_section(self):
        """测试添加章节"""
        report = ReportGenerator()
        report.add_section('Section 1', text='Test content')
        self.assertEqual(len(report.sections), 1)
    
    def test_add_table(self):
        """测试添加表格"""
        report = ReportGenerator()
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        report.add_table('Test Table', df)
        self.assertEqual(len(report.sections), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
