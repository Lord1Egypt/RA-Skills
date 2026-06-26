#!/usr/bin/env python3
"""
小黄鸭文献验证分析脚本
从 PDF 中提取共识序列，从 Step 3 开始运行分析流程
X 字符（非共有序列片段）直接跳过
"""

import os
import re
import zlib
import json
import pandas as pd
from datetime import datetime
from collections import defaultdict

# ============================================================
# 氨基酸分类体系（已确认，严格执行）
# ============================================================
FUNCTIONAL_CLASSES = {
    "Nucleophilic": ["S", "T", "C"],
    "Hydrophobic":  ["V", "L", "I", "M"],   # A/G/P 排除，不参与统计
    "Aromatic":     ["F", "Y", "W"],
    "Amide":        ["N", "Q"],
    "Acidic":       ["D", "E"],
    "Cationic":     ["H", "K", "R"]
}
# 注意：A(丙氨酸)、G(甘氨酸)、P(脯氨酸) 与 X 一样，不属于任何类别，不参与配对统计

AA_TO_CLASS = {
    aa: cls
    for cls, aas in FUNCTIONAL_CLASSES.items()
    for aa in aas
}

CHECKPOINT_FILE = "checkpoint.json"

# ============================================================
# 工具函数
# ============================================================

def log(log_file, message):
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{ts}] {message}"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(msg + "\n")
    print(msg)

def save_checkpoint(cp_path, cp):
    with open(cp_path, 'w', encoding='utf-8') as f:
        json.dump(cp, f, ensure_ascii=False, indent=2)

def load_checkpoint(cp_path):
    if os.path.exists(cp_path):
        with open(cp_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "pdf_parsed":        False,
        "consensus":         {},   # taxon_name -> sequence
        "pairs_done":        False,
        "formulations_done": False,
        "outputs_done":      False,
    }

# ============================================================
# Step 3: 从 PDF 提取共识序列
# ============================================================

def step3_parse_pdf(pdf_path, task_dir, log_file, cp, cp_path):
    log(log_file, "=== 步骤3: 从PDF提取共识序列 ===")

    if cp.get("pdf_parsed") and cp.get("consensus"):
        log(log_file, f"⏭️  已完成，共 {len(cp['consensus'])} 个类群，跳过")
        return cp["consensus"]

    with open(pdf_path, 'rb') as f:
        raw = f.read()

    # 解压所有 FlateDecode 流，提取 TJ 文本
    streams = re.findall(b'stream\r?\n(.*?)\r?\nendstream', raw, re.DOTALL)
    text_chunks = []
    for s in streams:
        for wbits in [15, -15, 47]:
            try:
                dec = zlib.decompress(s, wbits)
                t   = dec.decode('latin1', errors='replace')
                # 提取 TJ 操作符内的文本
                tjs = re.findall(r'\[([^\]]+)\]\s*TJ', t)
                for item in tjs:
                    chars = re.findall(r'\(([^)]*)\)', item)
                    text_chunks.append(''.join(chars))
                break
            except Exception:
                pass

    full_text = '\n'.join(text_chunks)
    log(log_file, f"📄 PDF文本提取完成，总字符数: {len(full_text):,}")

    # 按物种分割序列
    # 格式: ==> TaxonName.txt <== ... >MSA Consensus of N seqs, protein\nSEQUENCE
    sections = re.split(r'==> (.+?)\.txt <==', full_text)
    # sections[0] = 前缀, sections[1] = 名称, sections[2] = 内容, ...

    consensus_seqs = {}
    i = 1
    while i < len(sections) - 1:
        taxon_name = sections[i].strip()
        content    = sections[i + 1]

        # 提取序列（>MSA Consensus 之后的内容）
        seq_match = re.search(
            r'>MSA Consensus of \d+ seqs.*?\n([A-Za-zX\s]+)',
            content, re.DOTALL
        )
        if seq_match:
            raw_seq = seq_match.group(1).upper()
            # 剔除 X、A、G、P 及非氨基酸字符，拼接为新序列
            # X = 非共有位点；A/G/P = 用户指定排除
            cleaned = re.sub(r'[^CDEFHIKLMNQRSTVWY]', '', raw_seq)
            if len(cleaned) > 10:
                consensus_seqs[taxon_name] = cleaned

        i += 2

    log(log_file, f"✅ 成功提取 {len(consensus_seqs)} 个类群的共识序列")
    for name, seq in consensus_seqs.items():
        log(log_file, f"   {name}: {len(seq)} aa（已剔除X/A/G/P）")

    # 保存共识序列到文件（含X）
    species_dir = os.path.join(task_dir, 'species_analysis')
    os.makedirs(species_dir, exist_ok=True)
    for name, seq in consensus_seqs.items():
        safe_name = re.sub(r'[^\w\-]', '_', name)
        out_path  = os.path.join(species_dir, f"{safe_name}_consensus.fasta")
        with open(out_path, 'w') as f:
            f.write(f">{name}_consensus\n{seq}\n")

    cp["consensus"]   = consensus_seqs
    cp["pdf_parsed"]  = True
    save_checkpoint(cp_path, cp)
    return consensus_seqs

# ============================================================
# Step 4: 计算氨基酸对频率
# ============================================================

def step4_calculate_pair_frequencies(consensus_seqs, task_dir, log_file, cp, cp_path):
    log(log_file, "=== 步骤4: 计算氨基酸对频率 ===")

    pairs_file = os.path.join(task_dir, 'pair_analysis', 'all_species_pairs.json')
    os.makedirs(os.path.dirname(pairs_file), exist_ok=True)

    if cp.get("pairs_done") and os.path.exists(pairs_file):
        log(log_file, "⏭️  步骤4已完成，从文件加载结果")
        with open(pairs_file, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        return {
            sp: {
                'total_pairs': d['total_pairs'],
                'pair_frequencies': {
                    tuple(k.split('_', 1)): v
                    for k, v in d['pair_frequencies'].items()
                }
            }
            for sp, d in raw.items()
        }

    log(log_file, "    统计规则：剔除X/A/G/P后拼接为新序列，统计新序列中的相邻对")
    log(log_file, "         与文献方法一致（已验证Acanthomorphata 3175对完全吻合）")

    all_species_pairs = {}

    for taxon, seq in consensus_seqs.items():
        # seq 已在 Step3 剔除 X/A/G/P，直接统计相邻对
        pair_counts = defaultdict(int)
        total_pairs = 0
        for idx in range(len(seq) - 1):
            aa_i = seq[idx]
            aa_j = seq[idx + 1]
            if aa_i in AA_TO_CLASS and aa_j in AA_TO_CLASS:
                pair = (AA_TO_CLASS[aa_i], AA_TO_CLASS[aa_j])
                pair_counts[pair] += 1
                total_pairs += 1

        pair_frequencies = {
            pair: {'count': cnt,
                   'frequency': cnt / total_pairs if total_pairs else 0}
            for pair, cnt in pair_counts.items()
        }

        all_species_pairs[taxon] = {
            'total_pairs':     total_pairs,
            'pair_frequencies': pair_frequencies,
        }
        log(log_file, f"✅ {taxon}: {total_pairs} 个有效相邻对")

    # 序列化保存
    with open(pairs_file, 'w', encoding='utf-8') as f:
        json.dump(
            {
                sp: {
                    'total_pairs': d['total_pairs'],
                    'pair_frequencies': {
                        f"{k[0]}_{k[1]}": v
                        for k, v in d['pair_frequencies'].items()
                    }
                }
                for sp, d in all_species_pairs.items()
            },
            f, ensure_ascii=False, indent=2
        )

    cp["pairs_done"] = True
    save_checkpoint(cp_path, cp)
    log(log_file, f"📊 步骤4完成，共处理 {len(all_species_pairs)} 个类群")
    return all_species_pairs

# ============================================================
# Step 5: Top 5 氨基酸对 + 配方计算
# ============================================================

def step5_calculate_formulations(all_species_pairs, task_dir, log_file, cp, cp_path):
    log(log_file, "=== 步骤5: 选择Top 5氨基酸对并计算配方 ===")

    formulations_file = os.path.join(task_dir, 'formulations', 'species_formulations.json')
    os.makedirs(os.path.dirname(formulations_file), exist_ok=True)

    if cp.get("formulations_done") and os.path.exists(formulations_file):
        log(log_file, "⏭️  步骤5已完成，从文件加载结果")
        with open(formulations_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    species_formulations = {}

    # 生成所有21种对称对型标签（按字母排序，确保唯一性）
    _cls_list = sorted(FUNCTIONAL_CLASSES.keys())
    ALL_PAIR_TYPES = []
    for idx_a, cls_a in enumerate(_cls_list):
        for cls_b in _cls_list[idx_a:]:
            ALL_PAIR_TYPES.append(tuple(sorted([cls_a, cls_b])))

    for taxon, data in all_species_pairs.items():
        # 先合并对称对（A-B 与 B-A 合并），再选 Top5（与文献方法一致）
        sym_counts = defaultdict(int)
        for (ci, cj), freq in data['pair_frequencies'].items():
            sym_key = tuple(sorted([ci, cj]))
            sym_counts[sym_key] += freq['count']

        sorted_pairs = sorted(sym_counts.items(), key=lambda x: -x[1])
        top5 = sorted_pairs[:5]   # list of (sym_key, count)

        top5_total  = sum(cnt for _, cnt in top5)
        total_pairs = data['total_pairs']
        top5_pct    = (top5_total / total_pairs * 100) if total_pairs else 0

        class_counts = defaultdict(int)
        for (ci, cj), cnt in top5:
            class_counts[ci] += cnt
            class_counts[cj] += cnt

        total_ni = sum(class_counts.values())
        relative_composition = {
            cls: {
                'Ni': class_counts.get(cls, 0),
                'phi_percent': round(
                    class_counts.get(cls, 0) / total_ni * 100 if total_ni else 0,
                    2
                )
            }
            for cls in FUNCTIONAL_CLASSES
        }

        # 汇总所有21种对型的计数（合并对称对 A-B 和 B-A）
        sym_pair_counts = defaultdict(int)
        for (ci, cj), freq in data['pair_frequencies'].items():
            key = tuple(sorted([ci, cj]))
            sym_pair_counts[key] += freq['count']
        all_pair_counts = {pt: sym_pair_counts.get(pt, 0) for pt in ALL_PAIR_TYPES}

        species_formulations[taxon] = {
            'top_5_pairs': [
                {
                    'pair':      f"{ci}-{cj}",
                    'count':     cnt,
                    'frequency': round(cnt / total_pairs * 100, 2) if total_pairs else 0
                }
                for (ci, cj), cnt in top5
            ],
            'top_5_total_count': top5_total,
            'top_5_percentage':  round(top5_pct, 2),
            'relative_composition': relative_composition,
            'all_pair_counts': {f"{a}-{b}": cnt for (a, b), cnt in all_pair_counts.items()},
            'total_pairs': total_pairs
        }
        log(log_file, f"✅ {taxon}: Top5占 {top5_pct:.1f}%")

    with open(formulations_file, 'w', encoding='utf-8') as f:
        json.dump(species_formulations, f, ensure_ascii=False, indent=2)

    cp["formulations_done"] = True
    save_checkpoint(cp_path, cp)
    log(log_file, f"📊 步骤5完成，共生成 {len(species_formulations)} 个配方")
    return species_formulations

# ============================================================
# Step 6: 生成输出文件
# ============================================================

def step6_generate_outputs(species_formulations, task_dir, log_file, cp, cp_path):
    log(log_file, "=== 步骤6: 生成输出文件 ===")

    out_dir          = os.path.join(task_dir, 'output_files')
    os.makedirs(out_dir, exist_ok=True)
    formulations_csv = os.path.join(out_dir, 'species_formulations.csv')
    top_pairs_csv    = os.path.join(out_dir, 'top_5_pairs_details.csv')
    summary_csv      = os.path.join(out_dir, 'formulation_summary.csv')

    if (cp.get("outputs_done")
            and all(os.path.exists(p) for p in [formulations_csv, top_pairs_csv, summary_csv])):
        log(log_file, "⏭️  步骤6已完成，跳过")
        return formulations_csv, top_pairs_csv, summary_csv

    # species_formulations.csv
    rows = []
    for sp, fm in species_formulations.items():
        row = {
            'species':          sp,
            'total_pairs':      fm['total_pairs'],
            'top_5_pairs':      '; '.join(p['pair'] for p in fm['top_5_pairs']),
            'top_5_percentage': fm['top_5_percentage'],
        }
        for cls, comp in fm['relative_composition'].items():
            row[f'{cls}_Ni']  = comp['Ni']
            row[f'{cls}_phi'] = comp['phi_percent']
        # 追加所有21种对型的计数
        for pair_key, cnt in fm.get('all_pair_counts', {}).items():
            row[f'count_{pair_key}'] = cnt
        rows.append(row)
    pd.DataFrame(rows).to_csv(formulations_csv, index=False)

    # top_5_pairs_details.csv
    pair_rows = [
        {
            'species':           sp,
            'rank':              i + 1,
            'pair':              p['pair'],
            'count':             p['count'],
            'frequency_percent': p['frequency'],
        }
        for sp, fm in species_formulations.items()
        for i, p in enumerate(fm['top_5_pairs'])
    ]
    pd.DataFrame(pair_rows).to_csv(top_pairs_csv, index=False)

    # formulation_summary.csv
    sigs = {}
    for sp, fm in species_formulations.items():
        sig = tuple(sorted(
            (cls, round(comp['phi_percent'], 1))
            for cls, comp in fm['relative_composition'].items()
        ))
        sigs.setdefault(sig, []).append(sp)
    n_unique = len(sigs)
    n_dup    = len(species_formulations) - n_unique

    pd.DataFrame([{
        'total_species':         len(species_formulations),
        'unique_formulations':   n_unique,
        'duplicate_formulations': n_dup,
    }]).to_csv(summary_csv, index=False)

    cp["outputs_done"] = True
    save_checkpoint(cp_path, cp)

    log(log_file, "✅ 输出文件生成完成:")
    for p in [formulations_csv, top_pairs_csv, summary_csv]:
        log(log_file, f"   {p}")

    return formulations_csv, top_pairs_csv, summary_csv

# ============================================================
# 主流程
# ============================================================

def main():
    PDF_PATH  = '/home/lenovo/.openclaw/media/inbound/共同序列---6639c329-38a8-47d0-ad58-25f594a2c599.pdf'
    TASK_NAME = '小黄鸭文献验证'
    RESULTS_BASE = '/home/lenovo/.openclaw/workspace/analysis_results'

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_dir  = os.path.join(RESULTS_BASE, f"{TASK_NAME}_{timestamp}")
    os.makedirs(task_dir, exist_ok=True)

    log_dir  = os.path.join(task_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'analysis_log.txt')
    cp_path  = os.path.join(task_dir, CHECKPOINT_FILE)
    cp       = load_checkpoint(cp_path)

    log(log_file, f"=== 任务开始: {TASK_NAME} ===")
    log(log_file, f"任务目录: {task_dir}")
    log(log_file, f"PDF来源: {PDF_PATH}")
    log(log_file, "X字符（非共有序列片段）将被跳过")

    try:
        consensus_seqs       = step3_parse_pdf(PDF_PATH, task_dir, log_file, cp, cp_path)
        all_species_pairs    = step4_calculate_pair_frequencies(consensus_seqs, task_dir, log_file, cp, cp_path)
        species_formulations = step5_calculate_formulations(all_species_pairs, task_dir, log_file, cp, cp_path)
        formulations_csv, top_pairs_csv, summary_csv = step6_generate_outputs(
            species_formulations, task_dir, log_file, cp, cp_path
        )

        n_total  = len(consensus_seqs)
        n_done   = len(species_formulations)
        log(log_file, "=" * 60)
        log(log_file, f"✅ 分析完成! 成功处理: {n_done}/{n_total} 个类群")
        log(log_file, f"结果目录: {task_dir}")
        log(log_file, "=" * 60)

        # 输出续传命令（以防意外）
        print(f"\n💡 续传命令: python {__file__} --resume {task_dir}")

    except Exception as e:
        import traceback
        log(log_file, f"❌ 任务异常: {e}")
        log(log_file, traceback.format_exc())
        log(log_file, f"💡 续传命令: python {__file__} --resume {task_dir}")
        raise


if __name__ == "__main__":
    import sys
    if '--resume' in sys.argv:
        idx = sys.argv.index('--resume')
        resume_dir = sys.argv[idx + 1]
        # 从已有目录续传
        PDF_PATH  = '/home/lenovo/.openclaw/media/inbound/共同序列---6639c329-38a8-47d0-ad58-25f594a2c599.pdf'
        log_file  = os.path.join(resume_dir, 'logs', 'analysis_log.txt')
        cp_path   = os.path.join(resume_dir, CHECKPOINT_FILE)
        cp        = load_checkpoint(cp_path)
        print(f"[续传模式] 目录: {resume_dir}")
        consensus_seqs       = step3_parse_pdf(PDF_PATH, resume_dir, log_file, cp, cp_path)
        all_species_pairs    = step4_calculate_pair_frequencies(consensus_seqs, resume_dir, log_file, cp, cp_path)
        species_formulations = step5_calculate_formulations(all_species_pairs, resume_dir, log_file, cp, cp_path)
        step6_generate_outputs(species_formulations, resume_dir, log_file, cp, cp_path)
    else:
        main()
