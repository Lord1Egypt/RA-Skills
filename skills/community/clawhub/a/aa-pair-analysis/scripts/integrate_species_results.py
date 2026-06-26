#!/usr/bin/env python3
"""
联合分析结果整合工具（支持CSV格式）
将氨基酸对频率分析和关键片段预测结果按物种整合到一起

以后联合分析后运行此脚本，可将结果按物种整合
"""

import json
import shutil
import csv
from pathlib import Path
from datetime import datetime

def load_species_formulations(csv_file):
    """从CSV加载物种配方数据"""
    formulations = {}
    if not csv_file.exists():
        return formulations
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            species = row.get('species', '')
            if species:
                formulations[species] = {
                    'total_pairs': row.get('total_pairs', '0'),
                    'top_5_percentage': row.get('top_5_percentage', '0'),
                    'top_5_pairs': row.get('top_5_pairs', '').split('; '),
                    'formulation': row.get('top_5_pairs', ''),
                    'category_phi': {
                        'Nucleophilic': row.get('Nucleophilic_phi', '0'),
                        'Hydrophobic': row.get('Hydrophobic_phi', '0'),
                        'Aromatic': row.get('Aromatic_phi', '0'),
                        'Amide': row.get('Amide_phi', '0'),
                        'Acidic': row.get('Acidic_phi', '0'),
                        'Cationic': row.get('Cationic_phi', '0')
                    }
                }
    return formulations


def load_top5_pairs(csv_file):
    """从CSV加载Top5对型详情"""
    top5_data = {}
    if not csv_file.exists():
        return top5_data
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            species = row.get('species', '')
            if species not in top5_data:
                top5_data[species] = []
            top5_data[species].append({
                'rank': row.get('rank', ''),
                'pair': row.get('pair', ''),
                'count': row.get('count', '0'),
                'frequency': row.get('frequency_percent', '0')
            })
    return top5_data


def integrate_species_results(task_name, aa_pair_dir, fragment_dir, output_base):
    """整合单个任务的物种分析结果"""
    
    aa_pair_dir = Path(aa_pair_dir)
    fragment_dir = Path(fragment_dir)
    output_dir = Path(output_base) / f"{task_name}_物种整合结果"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"=== 整合分析结果: {task_name} ===")
    print(f"氨基酸对分析目录: {aa_pair_dir}")
    print(f"关键片段预测目录: {fragment_dir}")
    print(f"输出目录: {output_dir}")
    
    # 读取氨基酸对分析的CSV数据
    formulations = load_species_formulations(aa_pair_dir / "species_formulations.csv")
    top5_data = load_top5_pairs(aa_pair_dir / "top_5_pairs_details.csv")
    
    print(f"  📊 加载配方数据: {len(formulations)} 个物种")
    print(f"  📊 加载Top5数据: {len(top5_data)} 个物种")
    
    # 获取关键片段预测的所有物种目录
    fragment_species_dirs = [d for d in fragment_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]
    
    print(f"\n📁 发现 {len(fragment_species_dirs)} 个物种（关键片段预测）")
    
    integrated_count = 0
    
    for species_dir in sorted(fragment_species_dirs):
        species_name = species_dir.name
        print(f"\n🔬 整合物种: {species_name}")
        
        # 创建物种输出目录
        species_output = output_dir / species_name
        species_output.mkdir(exist_ok=True)
        
        # 1. 整合关键片段预测文件
        fragment_files = list(species_dir.glob("*_aligned.fasta"))
        consensus_files = list(species_dir.glob("*_consensus.fasta"))
        json_files = list(species_dir.glob("*_key_fragments.json"))
        report_files = list(species_dir.glob("*_分析报告.md"))
        
        # 复制关键片段预测文件到子目录
        fragment_output = species_output / "关键片段预测"
        fragment_output.mkdir(exist_ok=True)
        
        for f in fragment_files + consensus_files + json_files + report_files:
            shutil.copy2(f, fragment_output / f.name)
        
        print(f"  ✅ 关键片段预测: {len(fragment_files + consensus_files + json_files + report_files)} 个文件")
        
        # 2. 整合氨基酸对分析数据
        aa_output = species_output / "氨基酸对分析"
        aa_output.mkdir(exist_ok=True)
        
        # 保存该物种的氨基酸对数据
        species_formulation = formulations.get(species_name, {})
        species_top5 = top5_data.get(species_name, [])
        
        if species_formulation:
            # 保存JSON格式
            with open(aa_output / "formulation.json", 'w', encoding='utf-8') as f:
                json.dump(species_formulation, f, ensure_ascii=False, indent=2)
            
            # 生成文本格式的配方报告
            with open(aa_output / "formulation.txt", 'w', encoding='utf-8') as f:
                f.write(f"=== {species_name} 氨基酸对分析配方 ===\n\n")
                f.write(f"总对数: {species_formulation.get('total_pairs', 'N/A')}\n")
                f.write(f"Top 5 占比: {species_formulation.get('top_5_percentage', 'N/A')}%\n\n")
                
                f.write("各类别φ值:\n")
                for cat, phi in species_formulation.get('category_phi', {}).items():
                    f.write(f"  {cat}: {phi}%\n")
                
                f.write(f"\nTop 5 氨基酸对:\n")
                for pair in species_formulation.get('top_5_pairs', []):
                    f.write(f"  - {pair}\n")
                
                # 计算Top 5中各类氨基酸的比例
                f.write(f"\nTop 5 各类氨基酸比例:\n")
                class_counts = {}
                total_occurrences = 0
                
                for item in species_top5:
                    pair = item.get('pair', '')
                    count = int(item.get('count', 0))
                    classes = pair.split('-')
                    for cls in classes:
                        if cls:
                            class_counts[cls] = class_counts.get(cls, 0) + count
                            total_occurrences += 1
                
                # 按占比排序
                sorted_classes = sorted(class_counts.items(), key=lambda x: -x[1])
                for cls, cnt in sorted_classes:
                    pct = cnt / total_occurrences * 100 if total_occurrences > 0 else 0
                    f.write(f"  {cls}: {cnt}次 ({pct:.1f}%)\n")
                f.write(f"  总计: {total_occurrences}次\n")
                
                f.write(f"\n配方: {species_formulation.get('formulation', 'N/A')}\n")
            
            # 保存Top5详情
            with open(aa_output / "top5_details.json", 'w', encoding='utf-8') as f:
                json.dump(species_top5, f, ensure_ascii=False, indent=2)
            
            print(f"  ✅ 氨基酸对分析: Top5已保存")
        else:
            print(f"  ⚠️  无氨基酸对分析数据")
        
        # 3. 生成物种综合分析报告
        generate_integrated_report(species_name, species_output, species_formulation, species_top5)
        
        integrated_count += 1
    
    # 生成任务汇总报告
    generate_task_summary(output_dir, task_name, integrated_count)
    
    print(f"\n=== 整合完成 ===")
    print(f"成功整合: {integrated_count} 个物种")
    print(f"结果目录: {output_dir}")
    
    return str(output_dir)


def generate_integrated_report(species_name, species_dir, formulation, top5_list):
    """生成改进版物种综合分析报告"""

    report_path = species_dir / "物种综合分析报告.md"

    # 统计Top5中各类氨基酸比例
    class_counts = {}
    total_occurrences = 0
    for item in top5_list:
        pair = item.get('pair', '')
        count = int(item.get('count', 0))
        classes = pair.split('-')
        for cls in classes:
            if cls:
                class_counts[cls] = class_counts.get(cls, 0) + count
                total_occurrences += 1

    # 找出主导类别
    dominant_class = max(class_counts.items(), key=lambda x: x[1])[0] if class_counts else None
    dominant_count = class_counts.get(dominant_class, 0) if dominant_class else 0
    dominant_pct = dominant_count / total_occurrences * 100 if total_occurrences > 0 else 0

    # 读取关键片段数据（尝试空格和下划线两种命名）
    fragment_json = species_dir / "关键片段预测" / f"{species_name}_key_fragments.json"
    if not fragment_json.exists():
        # 尝试下划线命名
        safe_name = species_name.replace(' ', '_')
        fragment_json = species_dir / "关键片段预测" / f"{safe_name}_key_fragments.json"
    
    fragments = []
    fragment_count = 0
    if fragment_json.exists():
        with open(fragment_json, 'r', encoding='utf-8') as jf:
            fragment_data = json.load(jf)
        fragments = fragment_data.get('key_fragments', [])
        fragment_count = len(fragments)

    with open(report_path, 'w', encoding='utf-8') as f:
        # ========== 报告头部 ==========
        f.write(f"# {species_name} — 联合分析综合报告\n\n")
        f.write(f"**分析日期**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        if formulation:
            f.write(f"**配方**: `{formulation.get('formulation', 'N/A')}`  \n")
            f.write(f"**数据规模**: {formulation.get('total_pairs', 'N/A')} 对 / Top5 占 {formulation.get('top_5_percentage', 'N/A')}% / {fragment_count} 个关键片段\n\n")

        # ========== 执行摘要 ==========
        f.write("---\n\n")
        f.write("## 📋 执行摘要\n\n")

        # 关键数据卡片
        f.write("### 核心指标\n\n")
        f.write(f"| 指标 | 数值 |\n")
        f.write(f"|------|------|\n")
        if formulation:
            f.write(f"| 总对数 | {formulation.get('total_pairs', 'N/A')} |\n")
            f.write(f"| Top5占比 | {formulation.get('top_5_percentage', 'N/A')}% |\n")
            f.write(f"| 主导类别 | {dominant_class or 'N/A'} ({dominant_pct:.1f}%) |\n")
        f.write(f"| 关键片段 | {fragment_count} 个 |\n")
        f.write(f"\n")

        # ========== 氨基酸对分析 ==========
        if formulation:
            f.write("---\n\n")
            f.write("## 🧬 氨基酸对频率分析\n\n")

            # φ值总览
            f.write("### 各类别φ值分布\n\n")
            f.write("| 类别 | φ值 | 柱状图 |\n")
            f.write("|------|-----|--------|\n")
            for cat, phi in formulation.get('category_phi', {}).items():
                phi_val = float(phi or 0)
                bar_len = int(phi_val / 5)
                bar = "█" * bar_len + "░" * (20 - bar_len)
                f.write(f"| {cat} | {phi}% | {bar} |\n")

            # Top5对型
            f.write("\n### Top 5 氨基酸对\n\n")
            f.write("| 排名 | 对型 | 计数 | 频率 | 累计 |\n")
            f.write("|------|------|------|------|------|\n")
            cumulative = 0
            for item in top5_list:
                freq = float(item.get('frequency', 0))
                cumulative += freq
                f.write(f"| {item.get('rank', 'N/A')} | **{item.get('pair', 'N/A')}** | {item.get('count', 'N/A')} | {freq}% | {cumulative:.1f}% |\n")

            # 类别占比
            if class_counts:
                f.write("\n### Top 5 各类氨基酸组成\n\n")
                f.write("| 类别 | 出现次数 | 占比 | 可视化 |\n")
                f.write("|------|----------|------|--------|\n")
                sorted_classes = sorted(class_counts.items(), key=lambda x: -x[1])
                for cls, cnt in sorted_classes:
                    pct = cnt / total_occurrences * 100 if total_occurrences > 0 else 0
                    bar_len = int(pct / 5)
                    bar = "█" * bar_len + "░" * (20 - bar_len)
                    f.write(f"| {cls} | {cnt} | {pct:.1f}% | {bar} |\n")
                f.write(f"| **总计** | **{total_occurrences}** | **100%** | {'█' * 20} |\n")

            f.write("\n")

        # ========== 关键片段预测 ==========
        if fragments:
            f.write("---\n\n")
            f.write("## 🔬 关键片段预测\n\n")

            # 片段概览表
            f.write("### 片段总览\n\n")
            f.write("| # | 片段ID | 位置 | 长度 | 重要性 | 主导类别 | 保守率 |\n")
            f.write("|---|--------|------|------|--------|----------|--------|\n")

            for i, frag in enumerate(fragments[:15], 1):
                emoji = {"极关键": "🔴", "关键": "🟠", "结构关键": "🟡", "极高保守": "🔵", "高保守（功能待确认）": "🔵", "高保守": "🔵"}.get(
                    frag.get('criticality', ''), "⚪")
                frag_id = frag.get('fragment_id', 'N/A')[:25]
                pos = frag.get('position_in_consensus', 'N/A')
                length = frag.get('length', '-')
                crit = frag.get('criticality', 'N/A')
                comp = frag.get('composition', {})
                cat = f"{comp.get('dominant_category', '-')} ({comp.get('dominant_ratio', 0):.1f}%)" if comp else '-'
                cons = frag.get('avg_conservation', '-')
                f.write(f"| {i} | {emoji} {frag_id} | {pos} | {length} | {crit} | {cat} | {cons} |\n")

            if len(fragments) > 15:
                f.write(f"| ... | *共 {len(fragments)} 个片段* | - | - | - | - | - |\n")

            f.write(f"\n> **图例**: 🔴极关键 > 🟠关键 > 🟡结构关键 > 🔵高保守待确认\n\n")

            # Top 5 片段详细分析
            f.write("### Top 5 片段详细分析\n\n")

            # 按保守率排序取Top 5
            def get_conservation(x):
                cons = x.get('avg_conservation', 0)
                if isinstance(cons, str):
                    return float(cons.rstrip('%'))
                return float(cons)

            top_frags = sorted(fragments, key=get_conservation, reverse=True)[:5]

            for frag in top_frags:
                emoji = {"极关键": "🔴", "关键": "🟠", "结构关键": "🟡", "极高保守": "🔵", "高保守（功能待确认）": "🔵", "高保守": "🔵"}.get(
                    frag.get('criticality', ''), "⚪")
                f.write(f"#### {emoji} {frag.get('fragment_id', 'N/A')}\n\n")

                seq = frag.get('sequence', '')
                display_seq = seq[:50] + "..." if len(seq) > 50 else seq
                f.write(f"**序列**: `{display_seq}`  \n")
                f.write(f"**位置**: {frag.get('position_in_consensus', 'N/A')}  \n")
                f.write(f"**长度**: {frag.get('length', 'N/A')} aa，保守率: {frag.get('avg_conservation', 'N/A')}\n\n")

                comp = frag.get('composition', {})
                if comp:
                    ratios = comp.get('category_ratios', {})
                    counts = comp.get('category_counts', {})

                    f.write("**氨基酸类别组成**:\n\n")
                    sorted_cats = sorted(ratios.items(), key=lambda x: -x[1])
                    for cat, ratio in sorted_cats:
                        if ratio > 0:
                            count = counts.get(cat, 0)
                            bar_len = int(ratio / 5)
                            bar = "█" * bar_len + "░" * (20 - bar_len)
                            f.write(f"- {cat:15s}: {count:3d} ({ratio:5.1f}%) {bar}\n")

                    f.write(f"\n**主导类别**: {comp.get('dominant_category', 'N/A')} ({comp.get('dominant_ratio', 0):.1f}%)\n\n")

                func_pred = frag.get('function_prediction', '')
                if func_pred:
                    f.write(f"**功能预测**: {func_pred}\n\n")

                f.write("---\n\n")

        # ========== 文件清单 ==========
        f.write("## 📁 文件清单\n\n")
        f.write("| 目录 | 文件 | 说明 |\n")
        f.write("|------|------|------|\n")
        f.write("| 氨基酸对分析/ | formulation.json | 配方数据（JSON） |\n")
        f.write("| 氨基酸对分析/ | formulation.txt | 配方报告（文本） |\n")
        f.write("| 氨基酸对分析/ | top5_details.json | Top5对型详情 |\n")
        f.write("| 关键片段预测/ | *_consensus.fasta | 共识序列（FASTA） |\n")
        f.write("| 关键片段预测/ | *_key_fragments.json | 关键片段数据 |\n")
        f.write("| 关键片段预测/ | *_分析报告.md | 详细分析报告 |\n")

    print(f"  ✅ 综合报告已生成")
    return report_path


def generate_task_summary(output_dir, task_name, species_count):
    """生成改进版任务汇总报告"""

    summary_path = output_dir / "_任务汇总报告.md"

    # 统计物种完成状态
    species_dirs = sorted([d for d in output_dir.iterdir() if d.is_dir() and not d.name.startswith('_')])
    completed = sum(1 for d in species_dirs if (d / "物种综合分析报告.md").exists())

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"# 📊 {task_name} — 联合分析结果汇总\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        f.write(f"**物种总数**: {species_count}  \n")
        f.write(f"**报告完成**: {completed}/{species_count} ✅\n\n")

        f.write("---\n\n")

        # 快速统计
        f.write("## 📈 分析概览\n\n")
        f.write(f"| 物种数 | 完成报告 | 状态 |\n")
        f.write(f"|--------|----------|------|\n")
        status_icon = "✅ 全部完成" if completed == species_count else f"⚠️  {completed}/{species_count} 完成"
        f.write(f"| {species_count} | {completed} | {status_icon} |\n\n")

        # 物种列表（紧凑表格）
        f.write("---\n\n")
        f.write("## 📋 物种列表\n\n")
        f.write("| 序号 | 物种名 | 综合报告 | 氨基酸对 | 关键片段 |\n")
        f.write("|------|--------|----------|----------|----------|\n")

        for i, species_dir in enumerate(species_dirs, 1):
            report_exists = (species_dir / "物种综合分析报告.md").exists()
            aa_exists = (species_dir / "氨基酸对分析" / "formulation.json").exists()
            frag_exists = (species_dir / "关键片段预测" / f"{species_dir.name}_key_fragments.json").exists()

            report_icon = "✅" if report_exists else "❌"
            aa_icon = "✅" if aa_exists else "❌"
            frag_icon = "✅" if frag_exists else "❌"

            f.write(f"| {i} | **{species_dir.name}** | {report_icon} | {aa_icon} | {frag_icon} |\n")

        f.write("\n---\n\n")

        # 目录结构示例
        f.write("## 📂 目录结构\n\n")
        f.write("```\n")
        f.write(f"{task_name}_物种整合结果/\n")
        f.write("├── 物种A/\n")
        f.write("│   ├── 物种综合分析报告.md     ← 核心报告\n")
        f.write("│   ├── 氨基酸对分析/\n")
        f.write("│   │   ├── formulation.json    ← 配方数据\n")
        f.write("│   │   ├── formulation.txt     ← 配方文本\n")
        f.write("│   │   └── top5_details.json   ← Top5详情\n")
        f.write("│   └── 关键片段预测/\n")
        f.write("│       ├── *_consensus.fasta   ← 共识序列\n")
        f.write("│       ├── *_key_fragments.json\n")
        f.write("│       └── *_分析报告.md       ← 片段详情\n")
        f.write("├── 物种B/\n")
        f.write("│   └── ...\n")
        f.write("└── _任务汇总报告.md           ← 本文件\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 📝 使用指南\n\n")
        f.write("1. **快速概览**: 查看各物种的 `物种综合分析报告.md`\n")
        f.write("2. **氨基酸对分析**: 进入 `氨基酸对分析/` 目录查看配方和Top5数据\n")
        f.write("3. **关键片段详情**: 进入 `关键片段预测/` 目录查看完整片段分析\n")
        f.write("4. **批量处理**: 可使用 `formulation.json` 进行跨物种比较\n\n")

        f.write("---\n\n")
        f.write(f"*报告由联合分析整合工具自动生成 | {datetime.now().strftime('%Y-%m-%d')}*\n")

    print(f"📄 任务汇总报告: {summary_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 5:
        task_name = sys.argv[1]
        aa_pair_dir = sys.argv[2]
        fragment_dir = sys.argv[3]
        output_base = sys.argv[4]
        integrate_species_results(task_name, aa_pair_dir, fragment_dir, output_base)
    else:
        print("用法: python integrate_species_results.py <任务名> <aa_pair目录> <fragment目录> <输出目录>")
        print("\n或直接运行（处理默认任务）：")
        print("  python integrate_species_results.py")
