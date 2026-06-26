#!/usr/bin/env python3
"""
批量更新20260319整合分析结果中所有物种的综合分析报告
"""

import sys
import json
import csv
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from integrate_species_results import generate_integrated_report

BASE_DIR = Path('/home/lenovo/.openclaw/workspace/analysis_results/20260319_整合分析结果')
CSV_FILE = BASE_DIR / '_所有物种配方总览.csv'

def load_formulations_from_csv(csv_path, category_filter=None):
    """从CSV加载配方数据，可选按分类筛选"""
    formulations = {}
    top5_data = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row.get('分类', '')
            species = row.get('物种名', '')
            
            if category_filter and category_filter not in category:
                continue
            
            if species:
                formulations[species] = {
                    'total_pairs': row.get('总对数', '0'),
                    'top_5_percentage': '0',  # CSV中没有这个字段
                    'top_5_pairs': row.get('配方', '').split('; '),
                    'formulation': row.get('配方', ''),
                    'category_phi': {}  # CSV中没有φ值数据
                }
    
    return formulations, top5_data

def update_integration_dir(integration_dir, all_formulations):
    """更新单个整合目录下所有物种的综合报告"""
    print(f"\n{'='*60}")
    print(f"更新: {integration_dir.name}")
    print(f"{'='*60}")
    
    # 根据目录名确定分类筛选
    category_filter = None
    if 'PKC' in integration_dir.name:
        category_filter = 'PKC'
    elif '电荷模式' in integration_dir.name:
        category_filter = '电荷模式'
    elif '贻贝' in integration_dir.name:
        category_filter = '贻贝'
    elif '阳离子' in integration_dir.name:
        category_filter = '阳离子'
    
    # 筛选该分类的配方数据
    formulations = {k: v for k, v in all_formulations.items() 
                    if category_filter and category_filter in k}
    
    # 遍历所有物种子目录
    species_dirs = [d for d in integration_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]
    updated = 0
    
    for species_dir in species_dirs:
        species_name = species_dir.name
        
        # 检查是否有关键片段数据
        frag_json = species_dir / "关键片段预测" / f"{species_name}_key_fragments.json"
        if not frag_json.exists():
            # 尝试下划线命名
            safe_name = species_name.replace(' ', '_')
            frag_json = species_dir / "关键片段预测" / f"{safe_name}_key_fragments.json"
        
        if not frag_json.exists():
            print(f"  ⚠ {species_name}: 未找到关键片段JSON")
            continue
        
        # 获取氨基酸对数据
        species_formulation = formulations.get(species_name, {})
        
        # 生成更新后的综合报告
        generate_integrated_report(species_name, species_dir, species_formulation, [])
        print(f"  ✅ {species_name}")
        updated += 1
    
    print(f"\n  完成: {updated}/{len(species_dirs)} 个物种")
    return updated

def main():
    """批量更新所有整合目录"""
    if not BASE_DIR.exists():
        print(f"错误: 目录不存在 {BASE_DIR}")
        return
    
    if not CSV_FILE.exists():
        print(f"错误: CSV文件不存在 {CSV_FILE}")
        return
    
    # 加载所有配方数据
    print(f"加载配方数据: {CSV_FILE}")
    all_formulations, _ = load_formulations_from_csv(CSV_FILE)
    print(f"  共 {len(all_formulations)} 个物种")
    
    # 查找所有按物种整合的目录
    integration_dirs = sorted([d for d in BASE_DIR.iterdir() if d.is_dir() and '按物种整合' in d.name])
    
    if not integration_dirs:
        print(f"错误: 未找到整合目录")
        return
    
    print(f"\n发现 {len(integration_dirs)} 个整合目录")
    
    total_updated = 0
    for integration_dir in integration_dirs:
        count = update_integration_dir(integration_dir, all_formulations)
        total_updated += count
    
    print(f"\n{'='*60}")
    print(f"🎉 全部完成！共更新 {total_updated} 个物种的综合报告")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
