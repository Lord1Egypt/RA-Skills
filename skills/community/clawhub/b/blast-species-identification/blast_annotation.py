#!/usr/bin/env python3
"""
NCBI BLAST 自动比对脚本
从 rep.fasta 提取 Top ASV 序列并进行在线 BLAST 比对
"""

import os
import csv
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import time

# 定义每个样本的 Top 1 ASV
SAMPLE_TOP_ASV = {
    'D1-8': 'ASV1',
    'D2-8': 'ASV4',
    'D3-8': 'ASV3',
    'J1-8': 'ASV1',
    'J2-8': 'ASV2',
    'J3-8': 'ASV2',
    'J4-8': 'ASV6',
    'L1-8': 'ASV4',
    'L2-8': 'ASV3',
    'L3-8': 'ASV1',
    'N1-8': 'ASV7',
    'N2-8': 'ASV1',
    'N3-8': 'ASV2',
}

# 获取需要比对的唯一 ASV 列表
UNIQUE_ASVS = sorted(set(SAMPLE_TOP_ASV.values()))

def extract_sequences(fasta_file, asv_list):
    """从 FASTA 文件提取指定 ASV 的序列"""
    sequences = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        if record.id in asv_list:
            sequences[record.id] = str(record.seq)
    return sequences

def run_blast(sequence, asv_name):
    """运行 NCBI BLAST 比对"""
    print(f"正在比对 {asv_name}...")
    try:
        # 使用 BLASTn，针对 16S ribosomal RNA sequences
        result_handle = NCBIWWW.qblast(
            program="blastn",
            database="nt",
            sequence=sequence,
            expect=0.001,
            hitlist_size=10,
            entrez_query="16S ribosomal RNA[Title] OR 16S rRNA[Title]",
            format_type="XML"
        )
        return result_handle
    except Exception as e:
        print(f"BLAST 错误 ({asv_name}): {e}")
        return None

def parse_blast_results(result_handle, output_csv, asv_name):
    """解析 BLAST 结果并保存为 CSV"""
    if result_handle is None:
        return False

    blast_records = NCBIXML.parse(result_handle)

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Description', 'Scientific Name', 'Max Score', 'Total Score',
            'Query Cover', 'E value', 'Per. ident', 'Acc. Len', 'Accession'
        ])

        for blast_record in blast_records:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    # 提取科学名称
                    sci_name = alignment.hit_def.split(' ')[0] if alignment.hit_def else ''
                    # 尝试从描述中提取更准确的名字
                    if 'strain' in alignment.hit_def:
                        parts = alignment.hit_def.split(' strain ')[0]
                        sci_name = parts.strip()

                    writer.writerow([
                        alignment.hit_def,
                        sci_name,
                        round(hsp.score, 1),
                        round(hsp.score, 1),
                        f"{hsp.query_end - hsp.query_start + 1}/{blast_record.query_length}",
                        hsp.expect,
                        round(hsp.identities / hsp.align_length * 100, 1),
                        alignment.length,
                        alignment.accession
                    ])
    return True

def main():
    fasta_file = "rep.fasta"
    output_dir = "blast_results"

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"需要比对的 ASV: {UNIQUE_ASVS}")

    # 提取序列
    print("提取序列...")
    sequences = extract_sequences(fasta_file, UNIQUE_ASVS)
    print(f"成功提取 {len(sequences)} 条序列")

    # 检查缺失的 ASV
    missing = set(UNIQUE_ASVS) - set(sequences.keys())
    if missing:
        print(f"警告: 未找到以下 ASV: {missing}")

    # 逐个进行 BLAST 比对
    for asv in UNIQUE_ASVS:
        if asv not in sequences:
            print(f"跳过 {asv} (序列不存在)")
            continue

        output_csv = os.path.join(output_dir, f"{asv}_blast.csv")

        # 检查是否已有结果
        if os.path.exists(output_csv):
            print(f"{asv} 已有比对结果，跳过")
            continue

        # 运行 BLAST
        result = run_blast(sequences[asv], asv)

        if result:
            parse_blast_results(result, output_csv, asv)
            result.close()
            print(f"{asv} 比对完成，结果保存至 {output_csv}")
        else:
            print(f"{asv} 比对失败")

        # 添加延迟以避免请求过于频繁
        time.sleep(3)

    # 生成汇总表
    print("\n生成汇总表...")
    summary_file = os.path.join(output_dir, "blast_summary.csv")
    with open(summary_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Sample', 'ASV', 'Top_Hit_Description', 'Top_Hit_Species',
                        'Max_Score', 'E_value', 'Per_ident', 'Accession'])

        for sample, asv in sorted(SAMPLE_TOP_ASV.items()):
            blast_file = os.path.join(output_dir, f"{asv}_blast.csv")
            if os.path.exists(blast_file):
                with open(blast_file, 'r', encoding='utf-8') as bf:
                    reader = csv.DictReader(bf)
                    first_hit = next(reader, None)
                    if first_hit:
                        writer.writerow([
                            sample, asv,
                            first_hit['Description'],
                            first_hit['Scientific Name'],
                            first_hit['Max Score'],
                            first_hit['E value'],
                            first_hit['Per. ident'],
                            first_hit['Accession']
                        ])
                    else:
                        writer.writerow([sample, asv, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
            else:
                writer.writerow([sample, asv, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])

    print(f"汇总表保存至 {summary_file}")
    print("\n完成!")

if __name__ == "__main__":
    main()
