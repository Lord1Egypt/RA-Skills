#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务数据可视化图表生成工具
根据解析的财务数据生成可视化图表
"""

import sys
import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from typing import Dict, List

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class ChartGenerator:
    """图表生成器"""
    
    def __init__(self, data: Dict, output_dir: str = "./charts"):
        self.data = data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.company_name = data.get('company_info', {}).get('company_name', 'Company')
        self.report_period = data.get('company_info', {}).get('report_period', '')
        
    def generate_all_charts(self) -> List[str]:
        """生成所有图表"""
        generated_files = []
        
        # 盈利能力图表
        if self._generate_profitability_chart():
            generated_files.append("profitability_chart.png")
        
        # 财务指标雷达图
        if self._generate_radar_chart():
            generated_files.append("financial_radar.png")
        
        # 关键指标摘要图
        if self._generate_summary_chart():
            generated_files.append("metrics_summary.png")
        
        return generated_files
    
    def _get_metric_value(self, metric_name: str) -> float:
        """获取指标数值"""
        metrics = self.data.get('financial_metrics', {})
        if metric_name in metrics:
            return metrics[metric_name].get('value', 0)
        return 0
    
    def _generate_profitability_chart(self) -> bool:
        """生成盈利能力图表"""
        try:
            metrics = self.data.get('financial_metrics', {})
            
            # 准备数据
            labels = []
            values = []
            
            profitability_metrics = ['毛利率', '净利率', 'ROE', 'ROA']
            for metric in profitability_metrics:
                if metric in metrics:
                    labels.append(metric)
                    values.append(metrics[metric]['value'])
            
            if not values:
                return False
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(labels, values, color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])
            
            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}%',
                       ha='center', va='bottom')
            
            ax.set_ylabel('百分比 (%)')
            ax.set_title(f'{self.company_name} {self.report_period} 盈利能力指标')
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'profitability_chart.png', dpi=150)
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"生成盈利能力图表失败: {e}")
            return False
    
    def _generate_radar_chart(self) -> bool:
        """生成财务指标雷达图"""
        try:
            import numpy as np
            
            metrics = self.data.get('financial_metrics', {})
            
            # 选择关键指标
            radar_metrics = {
                '毛利率': 30,  # 基准值
                '净利率': 15,
                'ROE': 15,
                '营收增长率': 20,
                '资产负债率': 50,  # 反向指标
            }
            
            values = []
            labels = []
            
            for metric, benchmark in radar_metrics.items():
                if metric in metrics:
                    value = metrics[metric]['value']
                    # 归一化到0-100
                    if metric == '资产负债率':
                        # 资产负债率越低越好，反向计算
                        normalized = max(0, min(100, (100 - value)))
                    else:
                        normalized = min(100, (value / benchmark) * 50)
                    values.append(normalized)
                    labels.append(metric)
            
            if len(values) < 3:
                return False
            
            # 创建雷达图
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            values += values[:1]  # 闭合图形
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            ax.plot(angles, values, 'o-', linewidth=2, color='#2E86AB')
            ax.fill(angles, values, alpha=0.25, color='#2E86AB')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            ax.set_ylim(0, 100)
            ax.set_title(f'{self.company_name} 财务健康度雷达图', pad=20)
            ax.grid(True)
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'financial_radar.png', dpi=150)
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"生成雷达图失败: {e}")
            return False
    
    def _generate_summary_chart(self) -> bool:
        """生成关键指标摘要图"""
        try:
            metrics = self.data.get('financial_metrics', {})
            
            # 创建摘要表格图
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.axis('off')
            
            # 准备表格数据
            table_data = []
            for metric_name, metric_info in metrics.items():
                value = metric_info['value']
                unit = metric_info['unit']
                
                # 格式化数值
                if '亿' in unit:
                    display_value = f"{value/100000000:.2f}亿"
                elif '万' in unit:
                    display_value = f"{value/10000:.2f}万"
                elif '%' in unit:
                    display_value = f"{value:.2f}%"
                else:
                    display_value = f"{value:.2f}"
                
                table_data.append([metric_name, display_value])
            
            if not table_data:
                return False
            
            # 创建表格
            table = ax.table(cellText=table_data,
                           colLabels=['财务指标', '数值'],
                           cellLoc='left',
                           loc='center',
                           colWidths=[0.4, 0.3])
            
            table.auto_set_font_size(False)
            table.set_fontsize(11)
            table.scale(1, 2)
            
            # 设置表头样式
            for i in range(2):
                table[(0, i)].set_facecolor('#2E86AB')
                table[(0, i)].set_text_props(weight='bold', color='white')
            
            # 设置标题
            plt.title(f'{self.company_name} {self.report_period} 财务指标摘要', 
                     fontsize=14, weight='bold', pad=20)
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'metrics_summary.png', dpi=150, bbox_inches='tight')
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"生成摘要图表失败: {e}")
            return False


def generate_charts_from_file(data_path: str, output_dir: str = "./charts") -> List[str]:
    """
    从数据文件生成图表
    
    Args:
        data_path: 解析后的数据文件路径(.json)
        output_dir: 图表输出目录
        
    Returns:
        List[str]: 生成的图表文件列表
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    generator = ChartGenerator(data, output_dir)
    return generator.generate_all_charts()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_charts.py <解析后的数据文件路径>")
        sys.exit(1)
    
    data_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./charts"
    
    try:
        print(f"正在生成图表: {data_file}")
        files = generate_charts_from_file(data_file, output_dir)
        
        if files:
            print(f"[OK] 图表生成完成")
            for f in files:
                print(f"  - {f}")
        else:
            print("[WARN] 未生成图表（可能缺少必要的财务数据）")
        
    except Exception as e:
        print(f"[ERROR] 图表生成失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
