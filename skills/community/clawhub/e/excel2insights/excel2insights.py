#!/usr/bin/env python3
"""
Excel2Insights - Excel数据分析工具 (增强版)
版本: v1.1.0 (增强版)
描述: 基于v1.0.8 HIGH CONFIDENCE安全架构，添加详细统计分析、数据可视化和增强报告功能
安全原则: 纯本地处理，无网络功能，数据安全
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import sys
from datetime import datetime

class EnhancedExcelAnalyzer:
    """增强版Excel数据分析器"""
    
    def __init__(self):
        self.data = None
        self.analysis_results = {}
    
    def load_data(self, file_path):
        """加载Excel数据"""
        try:
            print(f"📂 加载文件: {file_path}")
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            else:
                self.data = pd.read_excel(file_path)
            print(f"✅ 加载成功: {len(self.data)} 行 × {len(self.data.columns)} 列")
            return True
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return False
    
    def basic_analysis(self):
        """基础数据分析"""
        if self.data is None:
            print("请先加载数据")
            return
        
        print("\n📊 基础数据分析")
        print("=" * 40)
        print(f"数据行数: {len(self.data)}")
        print(f"数据列数: {len(self.data.columns)}")
        print(f"内存使用: {self.data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # 数据类型概览
        print("\n📋 数据类型分布:")
        dtypes_counts = self.data.dtypes.value_counts()
        for dtype, count in dtypes_counts.items():
            print(f"  {dtype}: {count} 列")
        
        # 保存结果
        self.analysis_results['basic'] = {
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'memory_mb': self.data.memory_usage(deep=True).sum() / 1024 / 1024,
            'dtypes': dtypes_counts.to_dict()
        }
    
    def detailed_statistics(self):
        """详细统计分析"""
        if self.data is None:
            return
        
        print("\n🔢 详细统计分析")
        print("=" * 40)
        
        numeric_stats = {}
        
        # 数值列统计
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"数值列数量: {len(numeric_cols)}")
            print(f"数值列: {', '.join(numeric_cols[:3])}{'...' if len(numeric_cols) > 3 else ''}")
            
            for col in numeric_cols:
                try:
                    mean_val = self.data[col].mean()
                    median_val = self.data[col].median()
                    std_val = self.data[col].std()
                    min_val = self.data[col].min()
                    max_val = self.data[col].max()
                    q1 = self.data[col].quantile(0.25)
                    q3 = self.data[col].quantile(0.75)
                    iqr = q3 - q1
                    missing = self.data[col].isna().sum()
                    missing_pct = missing / len(self.data) * 100
                    
                    # 显示前3列的详细统计
                    if col in numeric_cols[:3]:
                        print(f"\n{col}:")
                        print(f"  平均值: {mean_val:.2f}")
                        print(f"  中位数: {median_val:.2f}")
                        print(f"  标准差: {std_val:.2f}")
                        print(f"  范围: {min_val:.2f} - {max_val:.2f}")
                        print(f"  缺失值: {missing} ({missing_pct:.1f}%)")
                    
                    numeric_stats[col] = {
                        'mean': float(mean_val),
                        'median': float(median_val),
                        'std': float(std_val),
                        'min': float(min_val),
                        'max': float(max_val),
                        'q1': float(q1),
                        'q3': float(q3),
                        'iqr': float(iqr),
                        'missing': int(missing),
                        'missing_pct': float(missing_pct)
                    }
                    
                except Exception as e:
                    print(f"  统计 {col} 时出错: {e}")
        
        # 分类列统计
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            print(f"\n分类列数量: {len(categorical_cols)}")
            for col in categorical_cols[:2]:  # 显示前2个
                try:
                    unique_count = self.data[col].nunique()
                    top_value = self.data[col].mode().iloc[0] if not self.data[col].mode().empty else "N/A"
                    top_count = (self.data[col] == top_value).sum()
                    top_pct = top_count / len(self.data) * 100
                    missing = self.data[col].isna().sum()
                    
                    print(f"\n{col}:")
                    print(f"  唯一值数量: {unique_count}")
                    print(f"  最常见值: {top_value} ({top_pct:.1f}%)")
                    print(f"  缺失值: {missing}")
                    
                except Exception as e:
                    print(f"  统计 {col} 时出错: {e}")
        
        # 保存结果
        self.analysis_results['detailed'] = {
            'numeric_stats': numeric_stats,
            'numeric_cols_count': len(numeric_cols),
            'categorical_cols_count': len(categorical_cols)
        }
    
    def missing_value_analysis(self):
        """缺失值分析"""
        if self.data is None:
            return
        
        print("\n⚠️  缺失值分析")
        print("=" * 40)
        
        missing_counts = self.data.isna().sum()
        missing_cols = missing_counts[missing_counts > 0]
        
        if len(missing_cols) == 0:
            print("✅ 无缺失值")
        else:
            print(f"有缺失值的列: {len(missing_cols)}")
            missing_info = {}
            
            for col, count in missing_cols.items():
                pct = count / len(self.data) * 100
                print(f"  {col}: {count} 个缺失值 ({pct:.1f}%)")
                
                missing_info[col] = {
                    'missing_count': int(count),
                    'missing_pct': float(pct)
                }
            
            # 总体缺失情况
            total_missing = missing_counts.sum()
            total_cells = len(self.data) * len(self.data.columns)
            missing_rate = total_missing / total_cells * 100
            
            print(f"\n📋 总体缺失情况:")
            print(f"  总缺失值: {total_missing}")
            print(f"  总数据单元: {total_cells}")
            print(f"  缺失率: {missing_rate:.2f}%")
            
            # 保存结果
            self.analysis_results['missing'] = {
                'missing_info': missing_info,
                'total_missing': int(total_missing),
                'total_cells': int(total_cells),
                'missing_rate': float(missing_rate)
            }
    
    def create_visualizations(self, output_dir):
        """创建可视化图表"""
        if self.data is None:
            return
        
        print("\n🎨 创建可视化图表")
        print("=" * 40)
        
        viz_dir = os.path.join(output_dir, "visualizations")
        os.makedirs(viz_dir, exist_ok=True)
        
        charts_created = []
        
        # 1. 数值列分布直方图
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols[:3]:  # 为前3个数值列创建直方图
            try:
                plt.figure(figsize=(10, 6))
                
                # 清理数据，移除NaN
                clean_data = self.data[col].dropna()
                
                if len(clean_data) > 0:
                    plt.hist(clean_data, bins=30, edgecolor='black', alpha=0.7)
                    plt.title(f'{col} 分布直方图', fontsize=14, fontweight='bold')
                    plt.xlabel(col, fontsize=12)
                    plt.ylabel('频数', fontsize=12)
                    plt.grid(True, alpha=0.3)
                    
                    # 添加统计信息
                    mean_val = clean_data.mean()
                    median_val = clean_data.median()
                    plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'平均值: {mean_val:.2f}')
                    plt.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'中位数: {median_val:.2f}')
                    plt.legend()
                    
                    plt.tight_layout()
                    
                    hist_path = os.path.join(viz_dir, f'histogram_{col}.png')
                    plt.savefig(hist_path, dpi=100, bbox_inches='tight')
                    plt.close()
                    
                    print(f"✅ 创建直方图: {col}")
                    charts_created.append(f'histogram_{col}.png')
                else:
                    print(f"⚠️  {col} 列无有效数据，跳过图表创建")
                    
            except Exception as e:
                print(f"❌ 创建 {col} 直方图失败: {e}")
        
        # 2. 缺失值热力图
        try:
            missing_matrix = self.data.isna().astype(int)
            
            if missing_matrix.sum().sum() > 0:
                plt.figure(figsize=(12, 8))
                
                # 限制显示的行数（避免图表过大）
                max_rows = min(100, len(missing_matrix))
                display_matrix = missing_matrix.iloc[:max_rows, :]
                
                plt.imshow(display_matrix, aspect='auto', cmap='viridis')
                plt.title('缺失值热力图', fontsize=14, fontweight='bold')
                plt.xlabel('列', fontsize=12)
                plt.ylabel('行 (前100行)', fontsize=12)
                plt.colorbar(label='缺失 (1) / 非缺失 (0)')
                
                # 添加列名
                plt.xticks(range(len(display_matrix.columns)), display_matrix.columns, rotation=45, ha='right')
                
                plt.tight_layout()
                
                heatmap_path = os.path.join(viz_dir, 'missing_heatmap.png')
                plt.savefig(heatmap_path, dpi=100, bbox_inches='tight')
                plt.close()
                
                print(f"✅ 创建缺失值热力图")
                charts_created.append('missing_heatmap.png')
            else:
                print("✅ 无缺失值，跳过热力图创建")
                
        except Exception as e:
            print(f"❌ 创建缺失值热力图失败: {e}")
        
        print(f"📁 图表保存到: {viz_dir}")
        print(f"📊 共创建 {len(charts_created)} 个图表")
        
        # 保存结果
        self.analysis_results['visualizations'] = {
            'charts_created': charts_created,
            'visualization_dir': viz_dir
        }
    
    def generate_enhanced_report(self, output_dir):
        """生成增强版分析报告"""
        if self.data is None:
            return None
        
        print("\n📝 生成分析报告")
        print("=" * 40)
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(output_dir, f"analysis_report_{timestamp}.md")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                # 报告头部
                f.write("# Excel数据分析报告 (v1.1.0增强版)\n\n")
                f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("## 📊 数据概览\n\n")
                f.write(f"- **数据文件**: {os.path.basename(sys.argv[1]) if len(sys.argv) > 1 else '未知'}\n")
                f.write(f"- **数据行数**: {len(self.data)}\n")
                f.write(f"- **数据列数**: {len(self.data.columns)}\n")
                
                if 'basic' in self.analysis_results:
                    f.write(f"- **内存使用**: {self.analysis_results['basic']['memory_mb']:.2f} MB\n")
                
                f.write("\n### 数据类型分布\n")
                if 'basic' in self.analysis_results and 'dtypes' in self.analysis_results['basic']:
                    for dtype, count in self.analysis_results['basic']['dtypes'].items():
                        f.write(f"- `{dtype}`: {count} 列\n")
                
                # 详细统计信息
                if 'detailed' in self.analysis_results and 'numeric_stats' in self.analysis_results['detailed']:
                    numeric_stats = self.analysis_results['detailed']['numeric_stats']
                    if numeric_stats:
                        f.write("\n## 🔢 数值列统计\n\n")
                        f.write("| 列名 | 平均值 | 中位数 | 标准差 | 最小值 | 最大值 | 缺失值 |\n")
                        f.write("|------|--------|--------|--------|--------|--------|--------|\n")
                        
                        for col, stats in list(numeric_stats.items())[:10]:  # 最多显示10列
                            f.write(f"| {col} | {stats['mean']:.2f} | {stats['median']:.2f} | {stats['std']:.2f} | "
                                  f"{stats['min']:.2f} | {stats['max']:.2f} | {stats['missing']} ({stats['missing_pct']:.1f}%) |\n")
                
                # 缺失值分析
                if 'missing' in self.analysis_results and 'missing_info' in self.analysis_results['missing']:
                    missing_info = self.analysis_results['missing']['missing_info']
                    if missing_info:
                        f.write("\n## ⚠️  缺失值分析\n\n")
                        f.write("| 列名 | 缺失值数量 | 缺失率 |\n")
                        f.write("|------|------------|--------|\n")
                        
                        for col, info in missing_info.items():
                            f.write(f"| {col} | {info['missing_count']} | {info['missing_pct']:.1f}% |\n")
                        
                        f.write(f"\n**总体缺失情况**:\n")
                        f.write(f"- 总缺失值: {self.analysis_results['missing']['total_missing']}\n")
                        f.write(f"- 总数据单元: {self.analysis_results['missing']['total_cells']}\n")
                        f.write(f"- 缺失率: {self.analysis_results['missing']['missing_rate']:.2f}%\n")
                
                # 可视化图表信息
                if 'visualizations' in self.analysis_results:
                    f.write("\n## 🎨 可视化图表\n\n")
                    charts = self.analysis_results['visualizations'].get('charts_created', [])
                    if charts:
                        f.write("生成的图表文件:\n")
                        for chart in charts:
                            f.write(f"- `{chart}`\n")
                    else:
                        f.write("本次分析未生成图表。\n")
                
                # 分析建议
                f.write("\n## 💡 分析建议\n\n")
                
                suggestions = []
                
                # 基于数据类型给出建议
                numeric_cols_count = self.analysis_results.get('detailed', {}).get('numeric_cols_count', 0)
                categorical_cols_count = self.analysis_results.get('detailed', {}).get('categorical_cols_count', 0)
                
                if numeric_cols_count > 0:
                    suggestions.append(f"**数据包含 {numeric_cols_count} 个数值列**，适合进行以下分析:")
                    suggestions.append("  - 描述性统计分析（已完成）")
                    suggestions.append("  - 相关性分析（建议后续版本添加）")
                    suggestions.append("  - 趋势分析和预测（建议后续版本添加）")
                
                if categorical_cols_count > 0:
                    suggestions.append(f"**数据包含 {categorical_cols_count} 个分类列**，适合进行以下分析:")
                    suggestions.append("  - 频率分布分析")
                    suggestions.append("  - 交叉表分析")
                    suggestions.append("  - 分组对比分析")
                
                # 基于缺失情况给出建议
                if 'missing' in self.analysis_results:
                    missing_rate = self.analysis_results['missing']['missing_rate']
                    if missing_rate > 0:
                        suggestions.append(f"**数据缺失率: {missing_rate:.2f}%**")
                        if missing_rate < 5:
                            suggestions.append("  - 缺失率较低，可以考虑删除缺失行")
                        elif missing_rate < 20:
                            suggestions.append("  - 缺失率适中，建议使用均值/中位数填充")
                        else:
                            suggestions.append("  - 缺失率较高，需要谨慎处理或考虑删除该列")
                
                for suggestion in suggestions:
                    f.write(f"{suggestion}\n")
                
                f.write("\n---\n")
                f.write("**分析工具**: Excel2Insights v1.1.0 (增强版)\n")
                f.write("**安全原则**: 纯本地处理，数据安全，无网络功能\n")
                f.write("**架构基础**: 基于v1.0.8 HIGH CONFIDENCE安全架构\n")
                f.write(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"✅ 报告已生成: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ 生成报告失败: {e}")
            return None

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Excel数据分析工具 v1.1.0 (增强版)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  基础分析: python excel2insights.py data.xlsx
  详细分析: python excel2insights.py data.csv --detailed
  可视化分析: python excel2insights.py data.xlsx --detailed --visualize
  指定输出: python excel2insights.py data.xlsx --output ./results/

增强功能说明:
  1. 📊 详细统计分析: 数值列详细统计、缺失值分析
  2. 🎨 数据可视化: 直方图、缺失值热力图
  3. 📝 增强报告: Markdown格式详细报告
  4. 🔧 用户体验: 改进的命令行界面和反馈
  5. 🔒 安全保持: 基于v1.0.8 HIGH CONFIDENCE安全架构
        """
    )
    
    parser.add_argument('file', help='Excel文件路径 (.xlsx, .xls, .csv)')
    parser.add_argument('--output', default='./output', help='输出目录 (默认: ./output)')
    parser.add_argument('--detailed', action='store_true', help='执行详细统计分析')
    parser.add_argument('--visualize', action='store_true', help='创建可视化图表')
    parser.add_argument('--quiet', action='store_true', help='安静模式，减少输出')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        print(f"💡 当前目录: {os.getcwd()}")
        return
    
    # 显示启动信息
    if not args.quiet:
        print("=" * 60)
        print("Excel数据分析工具 v1.1.0 (增强版)")
        print("=" * 60)
        print("安全原则: 纯本地处理 | 数据安全 | 无网络功能")
        print("架构基础: 基于v1.0.8 HIGH CONFIDENCE安全架构")
        print("-" * 60)
    
    # 创建分析器
    analyzer = EnhancedExcelAnalyzer()
    
    # 加载数据
    if not analyzer.load_data(args.file):
        return
    
    # 基础分析（始终执行）
    analyzer.basic_analysis()
    
    # 详细统计分析（可选）
    if args.detailed:
        analyzer.detailed_statistics()
        analyzer.missing_value_analysis()
    
    # 可视化分析（可选）
    if args.visualize:
        analyzer.create_visualizations(args.output)
    
    # 生成报告
    report_path = analyzer.generate_enhanced_report(args.output)
    
    # 显示完成信息
    if not args.quiet:
        print("\n" + "=" * 60)
        print("✅ 分析完成")
        if report_path:
            print(f"📄 报告位置: {report_path}")
        
        # 显示增强功能使用情况
        print(f"📊 增强功能使用:")
        if args.detailed:
            print(f"  ✅ 详细统计分析")
        if args.visualize:
            print(f"  ✅ 数据可视化")
        
        print("=" * 60)

if __name__ == "__main__":
    main()