#!/usr/bin/env python3
"""
智能数据分析处理器
支持多种数据源处理和报告生成
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
import csv
import io

class DataProcessor:
    """智能数据处理和分析类"""
    
    def __init__(self):
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, Any]:
        """加载报告模板"""
        return {
            "business_report": {
                "sections": ["执行摘要", "市场分析", "业绩表现", "财务分析", "风险识别", "建议和行动计划"]
            },
            "project_report": {
                "sections": ["项目概况", "进度分析", "成本分析", "质量评估", "风险管理", "总结和建议"]
            },
            "financial_report": {
                "sections": ["财务状况概览", "损益分析", "现金流分析", "资产负债分析", "财务比率", "风险预警"]
            }
        }
    
    def process_csv_data(self, file_path: str) -> Dict[str, Any]:
        """处理CSV数据并生成分析报告"""
        try:
            df = pd.read_csv(file_path)
            
            analysis = {
                "basic_stats": {
                    "row_count": len(df),
                    "column_count": len(df.columns),
                    "memory_usage": df.memory_usage(deep=True).sum(),
                    "dtypes": df.dtypes.to_dict()
                },
                "column_analysis": {},
                "quality_metrics": {
                    "missing_percentage": df.isnull().sum().to_dict(),
                    "duplicate_rows": df.duplicated().sum(),
                    "unique_counts": {}
                }
            }
            
            # 对每个列进行分析
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    analysis["column_analysis"][col] = {
                        "type": "numeric",
                        "min": float(df[col].min()),
                        "max": float(df[col].max()),
                        "mean": float(df[col].mean()),
                        "median": float(df[col].median()),
                        "std": float(df[col].std())
                    }
                    analysis["quality_metrics"]["unique_counts"][col] = df[col].nunique()
                elif df[col].dtype == 'object':
                    value_counts = df[col].value_counts()
                    analysis["column_analysis"][col] = {
                        "type": "categorical",
                        "unique_values": df[col].nunique(),
                        "top_values": value_counts.head(5).to_dict()
                    }
                    analysis["quality_metrics"]["unique_counts"][col] = df[col].nunique()
            
            # 检测异常值
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            outliers = {}
            for col in numeric_cols:
                mean = df[col].mean()
                std = df[col].std()
                upper = mean + 2 * std
                lower = mean - 2 * std
                outlier_count = ((df[col] > upper) | (df[col] < lower)).sum()
                outliers[col] = {
                    "count": int(outlier_count),
                    "percentage": float(round(outlier_count / len(df) * 100, 2)),
                    "upper_threshold": float(upper),
                    "lower_threshold": float(lower)
                }
            
            analysis["outliers"] = outliers
            
            return {
                "status": "success",
                "dataframe_shape": {"rows": len(df), "columns": len(df.columns)},
                "analysis": analysis,
                "preview": df.head(5).to_dict()
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def generate_data_insights(self, df: pd.DataFrame, target_column: Optional[str] = None) -> Dict[str, Any]:
        """生成数据洞察报告"""
        insights = {}
        
        # 相关性分析
        if len(df.select_dtypes(include=[np.number]).columns) > 1:
            corr_matrix = df.select_dtypes(include=[np.number]).corr()
            insights["correlations"] = {
                "matrix": corr_matrix.to_dict(),
                "high_correlations": []
            }
            
            # 找出高相关性的特征对
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = abs(corr_matrix.iloc[i, j])
                    if corr_value > 0.8:
                        insights["correlations"]["high_correlations"].append({
                            "feature1": corr_matrix.columns[i],
                            "feature2": corr_matrix.columns[j],
                            "correlation": float(corr_value)
                        })
        
        # 趋势分析
        date_columns = []
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                date_columns.append(col)
        
        if date_columns:
            insights["temporal_analysis"] = {
                "date_columns_found": date_columns,
                "trend_pattern": "需要进行时间序列分析"
            }
        
        # 分类数据分析
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            insights["categorical_analysis"] = {}
            for col in categorical_cols[:3]:  # 限制最多分析3个分类列
                value_dist = df[col].value_counts(normalize=True).head(5).to_dict()
                insights["categorical_analysis"][col] = {
                    "unique_values": df[col].nunique(),
                    "dominant_category": df[col].mode().iloc[0] if not df[col].mode().empty else None,
                    "value_distribution": value_dist
                }
        
        # 如果指定了目标列，进行目标分析
        if target_column and target_column in df.columns:
            target_analysis = {}
            
            if df[target_column].dtype in ['int64', 'float64']:
                # 数值型目标分析
                target_analysis["type"] = "numeric"
                target_analysis["distribution"] = {
                    "min": float(df[target_column].min()),
                    "max": float(df[target_column].max()),
                    "mean": float(df[target_column].mean()),
                    "median": float(df[target_column].median()),
                    "quantiles": df[target_column].quantile([0.25, 0.5, 0.75]).to_dict()
                }
            elif df[target_column].dtype == 'object':
                # 分类型目标分析
                target_analysis["type"] = "categorical"
                target_analysis["class_distribution"] = df[target_column].value_counts(normalize=True).to_dict()
            
            insights["target_analysis"] = target_analysis
        
        return insights
    
    def generate_markdown_report(self, df: pd.DataFrame, analysis_results: Dict[str, Any], 
                               report_type: str = "business") -> str:
        """生成Markdown格式的报告"""
        template = self.templates.get(report_type, self.templates["business_report"])
        
        report = f"# 数据分析报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"**数据概览**: {analysis_results.get('dataframe_shape', {})}\n\n"
        
        for section in template["sections"]:
            if section == "执行摘要":
                report += f"## {section}\n\n"
                report += f"本次分析共处理 {len(df)} 行数据，包含 {len(df.columns)} 个字段。\n\n"
                
                # 添加关键发现
                if "insights" in analysis_results:
                    report += "### 关键发现\n\n"
                    insights = analysis_results["insights"]
                    if "correlations" in insights:
                        high_corrs = insights["correlations"].get("high_correlations", [])
                        if high_corrs:
                            report += "#### 强相关性发现\n"
                            for corr in high_corrs[:3]:
                                report += f"- **{corr['feature1']}** 与 **{corr['feature2']}** 的相关系数为 {corr['correlation']:.3f}\n"
                            report += "\n"
                
            elif section == "数据质量分析":
                report += f"## {section}\n\n"
                if "analysis" in analysis_results and "quality_metrics" in analysis_results["analysis"]:
                    quality = analysis_results["analysis"]["quality_metrics"]
                    
                    total_cells = len(df) * len(df.columns)
                    missing_cells = sum(quality["missing_percentage"].values())
                    missing_percentage = (missing_cells / total_cells * 100) if total_cells > 0 else 0
                    
                    report += f"### 数据完整性\n"
                    report += f"- 数据表格: {len(df)}行 × {len(df.columns)}列\n"
                    report += f"- 缺失值比例: {missing_percentage:.2f}%\n"
                    report += f"- 重复行数: {quality['duplicate_rows']}\n\n"
                    
                    if quality.get("unique_counts"):
                        report += "### 唯一值分析\n"
                        for col, unique_count in list(quality["unique_counts"].items())[:5]:
                            if unique_count < 10:
                                report += f"- **{col}**: {unique_count}个唯一值 (可能为类别变量)\n"
                            elif unique_count > len(df) * 0.9:
                                report += f"- **{col}**: {unique_count}个唯一值 (接近全部唯一，可能为ID字段)\n"
                        report += "\n"
            
            elif section == "统计摘要":
                report += f"## {section}\n\n"
                if analysis_results.get("analysis", {}).get("column_analysis"):
                    report += "### 数值型字段统计\n\n"
                    report += "| 字段 | 类型 | 最小值 | 最大值 | 平均值 | 标准差 |\n"
                    report += "|------|------|--------|--------|--------|--------|\n"
                    
                    for col, stats in analysis_results["analysis"]["column_analysis"].items():
                        if stats["type"] == "numeric":
                            report += f"| {col} | 数值 | {stats['min']:.2f} | {stats['max']:.2f} | {stats['mean']:.2f} | {stats['std']:.2f} |\n"
                    report += "\n"
            
            else:
                # 为其他章节添加占位符
                report += f"## {section}\n\n"
                report += f"*更多分析内容将根据具体需求进行填充*\n\n"
        
        # 添加改进建议
        report += "## 改进建议\n\n"
        
        if "analysis" in analysis_results and "quality_metrics" in analysis_results["analysis"]:
            quality = analysis_results["analysis"]["quality_metrics"]
            missing_cells = sum(quality["missing_percentage"].values())
            
            if missing_cells > 0:
                report += "1. **数据清理建议**: 发现缺失值，建议进行数据清洗或插补处理\n"
            
            if quality["duplicate_rows"] > 0:
                report += f"2. **重复数据处理**: 检测到 {quality['duplicate_rows']} 条重复记录，建议进行去重处理\n"
        
        if "analysis" in analysis_results and "outliers" in analysis_results["analysis"]:
            outlier_summary = sum([v["count"] for v in analysis_results["analysis"]["outliers"].values()])
            if outlier_summary > 0:
                report += f"3. **异常值检测**: 发现 {outlier_summary} 个潜在异常值，建议进行核实或处理\n"
        
        # 添加技术说明
        report += "\n---\n"
        report += "**技术说明**: 本报告由智能数据分析报告生成器自动生成。\n"
        report += f"**处理算法**: Python + Pandas + NumPy\n"
        report += f"**报告模板**: {report_type}模板\n"
        
        return report

# 主函数测试
if __name__ == "__main__":
    # 创建示例数据
    data = {
        '日期': pd.date_range('2024-01-01', periods=100),
        '销售额': np.random.normal(1000, 200, 100),
        '客户数': np.random.randint(50, 200, 100),
        '产品类别': np.random.choice(['A', 'B', 'C', 'D'], 100),
        '地区': np.random.choice(['华东', '华南', '华北', '西南'], 100)
    }
    
    df = pd.DataFrame(data)
    
    # 测试处理器
    processor = DataProcessor()
    df.to_csv("test_data.csv", index=False)
    
    result = processor.process_csv_data("test_data.csv")
    insights = processor.generate_data_insights(df, target_column="销售额")
    
    result["insights"] = insights
    
    report = processor.generate_markdown_report(df, result, "business")
    
    print("数据处理结果概述:")
    print(f"- 数据形状: {len(df)}行 × {len(df.columns)}列")
    print(f"- 数值字段: {len([c for c in df.columns if df[c].dtype in ['int64', 'float64']])}")
    print(f"- 分类字段: {len([c for c in df.columns if df[c].dtype == 'object'])}")
    print(f"- 生成报告长度: {len(report)}字符")
    
    # 保存报告
    with open("data_analysis_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ 测试完成！报告已保存至 data_analysis_report.md")