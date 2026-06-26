#!/usr/bin/env python3
"""
执行验证脚本
用于检查 financial-data-analyzer skill 是否正确完成了所有必需步骤
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def check_data_files(data_dir: str) -> dict:
    """检查数据文件是否存在"""
    data_path = Path(data_dir)
    
    results = {
        "total_files": 0,
        "csv_files": [],
        "xlsx_files": [],
        "json_files": [],
        "missing_types": []
    }
    
    if not data_path.exists():
        results["error"] = f"数据目录不存在: {data_dir}"
        return results
    
    # 统计文件
    for file in data_path.glob("**/*"):
        if file.is_file():
            results["total_files"] += 1
            if file.suffix == ".csv":
                results["csv_files"].append(str(file.name))
            elif file.suffix == ".xlsx":
                results["xlsx_files"].append(str(file.name))
            elif file.suffix == ".json":
                results["json_files"].append(str(file.name))
    
    # 检查必需的数据类型
    required_types = ["realtime", "history", "financial", "fundamental", "indicators", "risk_metrics"]
    
    for req_type in required_types:
        found = False
        for csv_file in results["csv_files"]:
            if req_type in csv_file:
                found = True
                break
        if not found:
            for json_file in results["json_files"]:
                if req_type in json_file:
                    found = True
                    break
        if not found:
            results["missing_types"].append(req_type)
    
    return results

def check_report_file(output_dir: str) -> dict:
    """检查是否生成了 HTML 报告"""
    output_path = Path(output_dir)
    
    results = {
        "html_reports": [],
        "md_reports": [],
        "has_html": False,
        "error_md_only": False
    }
    
    if not output_path.exists():
        results["error"] = f"输出目录不存在: {output_dir}"
        return results
    
    # 查找报告文件
    for file in output_path.glob("**/*"):
        if file.is_file():
            if file.suffix == ".html" and "report" in file.name.lower():
                results["html_reports"].append(str(file.name))
                results["has_html"] = True
            elif file.suffix == ".md" and "report" in file.name.lower():
                results["md_reports"].append(str(file.name))
    
    # 检查是否只有 MD 报告
    if results["md_reports"] and not results["html_reports"]:
        results["error_md_only"] = True
    
    return results

def check_chart_files(output_dir: str) -> dict:
    """检查是否生成了图表文件"""
    output_path = Path(output_dir)
    
    results = {
        "chart_files": [],
        "total_charts": 0
    }
    
    if not output_path.exists():
        results["error"] = f"输出目录不存在: {output_dir}"
        return results
    
    # 查找图表文件
    for file in output_path.glob("**/*"):
        if file.is_file():
            if file.suffix == ".html" and ("chart" in file.name.lower() or "echarts" in file.name.lower()):
                results["chart_files"].append(str(file.name))
                results["total_charts"] += 1
    
    return results

def generate_report(data_dir: str, output_dir: str) -> str:
    """生成执行验证报告"""
    report = []
    report.append("=" * 80)
    report.append("Financial Data Analyzer 执行验证报告")
    report.append("=" * 80)
    report.append(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"数据目录: {data_dir}")
    report.append(f"输出目录: {output_dir}")
    report.append("")
    
    # 检查数据文件
    report.append("【步骤1：数据文件检查】")
    data_results = check_data_files(data_dir)
    
    if "error" in data_results:
        report.append(f"❌ 错误: {data_results['error']}")
    else:
        report.append(f"✅ 总文件数: {data_results['total_files']}")
        report.append(f"   - CSV 文件: {len(data_results['csv_files'])} 个")
        report.append(f"   - XLSX 文件: {len(data_results['xlsx_files'])} 个")
        report.append(f"   - JSON 文件: {len(data_results['json_files'])} 个")
        
        if data_results["missing_types"]:
            report.append(f"⚠️  缺失的数据类型: {', '.join(data_results['missing_types'])}")
        else:
            report.append("✅ 所有必需的数据类型都已获取")
    
    report.append("")
    
    # 检查报告文件
    report.append("【步骤2：报告文件检查】")
    report_results = check_report_file(output_dir)
    
    if "error" in report_results:
        report.append(f"❌ 错误: {report_results['error']}")
    elif report_results["error_md_only"]:
        report.append(f"❌ 严重错误: 只生成了 Markdown 报告，未生成 HTML 报告！")
        report.append(f"   MD 报告: {', '.join(report_results['md_reports'])}")
        report.append("   【违反规则】: 必须输出 HTML 格式报告，不得输出 Markdown 格式")
    elif report_results["has_html"]:
        report.append(f"✅ 已生成 HTML 报告: {', '.join(report_results['html_reports'])}")
        if report_results["md_reports"]:
            report.append(f"⚠️  同时生成了 MD 报告: {', '.join(report_results['md_reports'])} (应删除)")
    else:
        report.append("❌ 错误: 未找到任何报告文件")
    
    report.append("")
    
    # 检查图表文件
    report.append("【步骤3：图表文件检查】")
    chart_results = check_chart_files(output_dir)
    
    if "error" in chart_results:
        report.append(f"❌ 错误: {chart_results['error']}")
    elif chart_results["total_charts"] >= 3:
        report.append(f"✅ 已生成 {chart_results['total_charts']} 个图表文件")
        for chart_file in chart_results["chart_files"]:
            report.append(f"   - {chart_file}")
    elif chart_results["total_charts"] > 0:
        report.append(f"⚠️  警告: 只生成了 {chart_results['total_charts']} 个图表（应至少 3 个）")
    else:
        report.append("❌ 错误: 未生成任何图表文件")
    
    report.append("")
    
    # 总结
    report.append("=" * 80)
    report.append("【总结】")
    
    success_count = 0
    total_checks = 3
    
    if not ("error" in data_results) and not data_results["missing_types"]:
        success_count += 1
        report.append("✅ 数据采集: 通过")
    else:
        report.append("❌ 数据采集: 失败")
    
    if report_results.get("has_html") and not report_results.get("error_md_only"):
        success_count += 1
        report.append("✅ 报告生成: 通过")
    else:
        report.append("❌ 报告生成: 失败")
    
    if chart_results["total_charts"] >= 3:
        success_count += 1
        report.append("✅ 图表生成: 通过")
    else:
        report.append("❌ 图表生成: 失败")
    
    report.append("")
    report.append(f"通过率: {success_count}/{total_checks} ({success_count/total_checks*100:.1f}%)")
    
    if success_count == total_checks:
        report.append("🎉 恭喜！所有检查都通过了！")
    else:
        report.append("⚠️  部分检查未通过，请检查上述错误并修正")
    
    report.append("=" * 80)
    
    return "\n".join(report)

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python validate_execution.py <data_dir> <output_dir>")
        print("示例: python validate_execution.py ./financial_data ./output")
        sys.exit(1)
    
    data_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    report = generate_report(data_dir, output_dir)
    print(report)
    
    # 保存报告到文件
    report_file = Path(output_dir) / f"execution_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(report, encoding='utf-8')
    print(f"\n验证报告已保存到: {report_file}")

if __name__ == "__main__":
    main()
