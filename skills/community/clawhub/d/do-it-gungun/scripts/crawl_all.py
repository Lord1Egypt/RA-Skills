#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
do-it 数据抓取主脚本
一键抓取所有数据：薪资 + 城市 + 案例

使用方法:
    python scripts/crawl_all.py
"""

import subprocess
import sys
import json
from datetime import datetime

def run_script(script_name: str):
    """运行抓取脚本"""
    print(f"\n{'='*60}")
    print(f"运行：{script_name}")
    print(f"{'='*60}\n")
    
    result = subprocess.run([sys.executable, script_name])
    
    if result.returncode != 0:
        print(f"⚠️  {script_name} 执行失败，继续下一个...")
    else:
        print(f"✓ {script_name} 执行完成")
    
    return result.returncode == 0


def generate_summary():
    """生成数据摘要报告"""
    print("\n" + "="*60)
    print("生成数据摘要报告")
    print("="*60)
    
    summary = {
        'report_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'data_files': {
            'salary': 'data/salary/finance_bp_salary.json',
            'city': 'data/city/city_comparison.json',
            'cases_manual': 'data/cases/case_records.json',
            'cases_web': 'data/cases/web_cases.json'
        },
        'statistics': {}
    }
    
    # 读取各数据文件统计
    try:
        with open('data/salary/finance_bp_salary.json', 'r', encoding='utf-8') as f:
            salary_data = json.load(f)
            summary['statistics']['salary_records'] = len(salary_data.get('data', []))
    except Exception as e:
        print(f"⚠️ 读取薪资数据失败：{e}")
        summary['statistics']['salary_records'] = 0
    
    try:
        with open('data/city/city_comparison.json', 'r', encoding='utf-8') as f:
            city_data = json.load(f)
            summary['statistics']['city_records'] = len(city_data.get('data', []))
    except Exception as e:
        print(f"⚠️ 读取城市数据失败：{e}")
        summary['statistics']['city_records'] = 0
    
    try:
        with open('data/cases/case_records.json', 'r', encoding='utf-8') as f:
            case_data = json.load(f)
            summary['statistics']['manual_cases'] = len(case_data.get('cases', []))
    except Exception as e:
        print(f"⚠️ 读取手动案例失败：{e}")
        summary['statistics']['manual_cases'] = 0
    
    try:
        with open('data/cases/web_cases.json', 'r', encoding='utf-8') as f:
            web_cases = json.load(f)
            summary['statistics']['web_cases'] = len(web_cases.get('cases', []))
    except Exception as e:
        print(f"⚠️ 读取网络案例失败：{e}")
        summary['statistics']['web_cases'] = 0
    
    # 总计
    summary['statistics']['total_cases'] = (
        summary['statistics'].get('manual_cases', 0) + 
        summary['statistics'].get('web_cases', 0)
    )
    
    # 保存摘要
    with open('data/DATA-SUMMARY.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 摘要已保存：data/DATA-SUMMARY.json")
    
    # 打印摘要
    print("\n" + "="*60)
    print("📊 do-it 数据库摘要")
    print("="*60)
    print(f"更新时间：{summary['report_date']}")
    print(f"\n数据统计:")
    print(f"  薪资记录：{summary['statistics'].get('salary_records', 0)} 条")
    print(f"  城市数据：{summary['statistics'].get('city_records', 0)} 个")
    print(f"  手动案例：{summary['statistics'].get('manual_cases', 0)} 个")
    print(f"  网络案例：{summary['statistics'].get('web_cases', 0)} 个")
    print(f"  案例总计：{summary['statistics'].get('total_cases', 0)} 个")
    print("="*60)
    
    return summary


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🌪️ do-it 数据抓取系统")
    print("="*60)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行各抓取脚本
    scripts = [
        'scripts/crawl_city_data.py',
        'scripts/crawl_cases.py',
    ]
    
    success_count = 0
    for script in scripts:
        if run_script(script):
            success_count += 1
    
    # 生成摘要
    generate_summary()
    
    # 完成提示
    print("\n" + "="*60)
    print("✅ 数据抓取完成！")
    print("="*60)
    print(f"成功：{success_count}/{len(scripts)} 个脚本")
    print(f"\n下一步:")
    print("  1. 查看数据：cat data/DATA-SUMMARY.json | jq")
    print("  2. 查看薪资：cat data/salary/finance_bp_salary.json | jq")
    print("  3. 查看城市：cat data/city/city_comparison.json | jq")
    print("  4. 查看案例：cat data/cases/*.json | jq")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
