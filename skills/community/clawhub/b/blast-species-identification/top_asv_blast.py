#!/usr/bin/env python3
"""
Top ASV BLAST 注释工具
从 OTU 表中提取每个样本序列数最多的 ASV 并进行 BLAST 物种注释

用法:
    python top_asv_blast.py otu_table.xls rep.fasta output_dir/

输入:
    - OTU 表 (支持 .xls, .tsv, .csv 格式)
    - 代表性序列 FASTA 文件 (rep.fasta)
"""

import os
import sys
import csv
import argparse
import time
import re
from collections import defaultdict

try:
    from Bio import SeqIO
    from Bio.Blast import NCBIWWW
    from Bio.Blast import NCBIXML
except ImportError:
    print("错误: 需要安装 biopython")
    print("请运行: pip install biopython")
    sys.exit(1)


def parse_otu_table(otu_file):
    """
    解析 OTU 表，返回样本组信息
    自动检测样本重复并合并（如 D1-8-1, D1-8-2, D1-8-3 -> D1-8）
    """
    # 检测文件格式
    delimiter = '\t'
    if otu_file.endswith('.csv'):
        delimiter = ','

    with open(otu_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        header = next(reader)

        # 找到样本列（排除 SAMPLE ID 和 taxonomy）
        sample_cols = []
        for i, col in enumerate(header):
            col_lower = col.strip().lower()
            if col_lower not in ['sample id', 'sample_id', 'taxonomy', 'asv', 'otuid', 'otu_id']:
                sample_cols.append((i, col.strip()))

        # 检测样本组（合并重复）
        sample_groups = defaultdict(list)
        for col_idx, col_name in sample_cols:
            # 尝试匹配样本组名（如 D1-8-1 -> D1-8）
            match = re.match(r'^([A-Za-z]+\d+-\d+)(-\d+)?$', col_name)
            if match:
                group_name = match.group(1)
                sample_groups[group_name].append((col_idx, col_name))
            else:
                # 如果无法匹配，直接使用列名作为组名
                sample_groups[col_name].append((col_idx, col_name))

        # 读取 ASV 数据
        asv_data = {}
        taxonomy_col = len(header) - 1  # 假设最后一列是 taxonomy

        for row in reader:
            if not row or not row[0]:
                continue
            asv_id = row[0].strip()
            taxonomy = row[taxonomy_col].strip() if taxonomy_col < len(row) else ''

            asv_data[asv_id] = {
                'taxonomy': taxonomy,
                'counts': {}
            }

            for group_name, cols in sample_groups.items():
                total_count = sum(float(row[col_idx]) for col_idx, _ in cols if col_idx < len(row) and row[col_idx])
                asv_data[asv_id]['counts'][group_name] = total_count

        return asv_data, list(sample_groups.keys())


def find_top_asv_per_sample(asv_data, sample_groups):
    """找到每个样本组中序列数最多的 ASV"""
    top_asvs = {}

    for group in sample_groups:
        max_count = 0
        max_asv = None

        for asv_id, data in asv_data.items():
            count = data['counts'].get(group, 0)
            if count > max_count:
                max_count = count
                max_asv = asv_id

        if max_asv:
            top_asvs[group] = {
                'asv_id': max_asv,
                'count': max_count,
                'taxonomy': asv_data[max_asv]['taxonomy']
            }

    return top_asvs


def extract_sequences(fasta_file, asv_ids):
    """从 FASTA 文件提取指定 ASV 的序列"""
    sequences = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        if record.id in asv_ids:
            sequences[record.id] = str(record.seq)
    return sequences


def run_blast(sequence, hitlist_size=10):
    """运行 NCBI BLAST 比对"""
    try:
        result_handle = NCBIWWW.qblast(
            program="blastn",
            database="nt",
            sequence=sequence,
            expect=0.001,
            hitlist_size=hitlist_size,
            entrez_query="16S ribosomal RNA[Title] OR 16S rRNA[Title]",
            format_type="XML"
        )
        return result_handle
    except Exception as e:
        print(f"BLAST 错误: {e}")
        return None


def parse_blast_results(result_handle, output_csv, sample_name):
    """解析 BLAST 结果并保存为 CSV"""
    if result_handle is None:
        return None

    blast_records = NCBIXML.parse(result_handle)
    top_hit = None

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
                    if 'strain' in alignment.hit_def:
                        parts = alignment.hit_def.split(' strain ')[0]
                        sci_name = parts.strip()

                    query_cover = f"{hsp.query_end - hsp.query_start + 1}/{blast_record.query_length}"
                    per_ident = round(hsp.identities / hsp.align_length * 100, 1)

                    row = [
                        alignment.hit_def,
                        sci_name,
                        round(hsp.score, 1),
                        round(hsp.score, 1),
                        query_cover,
                        hsp.expect,
                        per_ident,
                        alignment.length,
                        alignment.accession
                    ]
                    writer.writerow(row)

                    if top_hit is None:
                        top_hit = {
                            'sample': sample_name,
                            'description': alignment.hit_def,
                            'scientific_name': sci_name,
                            'max_score': round(hsp.score, 1),
                            'e_value': hsp.expect,
                            'per_ident': per_ident,
                            'accession': alignment.accession
                        }

    return top_hit


def create_summary(summary_file, top_hits, top_asvs):
    """创建汇总表"""
    with open(summary_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Sample', 'ASV', 'Count', 'Original_Taxonomy',
            'BLAST_Top_Hit', 'Scientific_Name', 'Max_Score',
            'E_value', 'Per_ident', 'Accession'
        ])

        for hit in top_hits:
            sample = hit['sample']
            asv_info = top_asvs.get(sample, {})
            writer.writerow([
                sample,
                asv_info.get('asv_id', ''),
                asv_info.get('count', ''),
                asv_info.get('taxonomy', ''),
                hit['description'],
                hit['scientific_name'],
                hit['max_score'],
                hit['e_value'],
                hit['per_ident'],
                hit['accession']
            ])


def main():
    parser = argparse.ArgumentParser(
        description='Top ASV BLAST 注释工具 - 从 OTU 表提取最丰富的 ASV 进行物种鉴定',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s taxa_table.xls rep.fasta results/
  %(prog)s taxa_table.xls rep.fasta results/ --top-n 2
  %(prog)s taxa_table.xls rep.fasta results/ --skip-existing

输出:
  - 每个样本的 BLAST 结果 CSV 文件
  - 汇总表 blast_summary.csv
  - ASV 信息表 top_asv_info.csv
        """
    )
    parser.add_argument('otu_table', help='OTU 表文件 (.xls, .tsv, .csv)')
    parser.add_argument('fasta', help='代表性序列 FASTA 文件 (rep.fasta)')
    parser.add_argument('output', help='输出目录')
    parser.add_argument('--top-n', '-n', type=int, default=1, help='每个样本提取前 N 个 ASV (默认: 1)')
    parser.add_argument('--delay', '-d', type=int, default=3, help='每次 BLAST 请求之间的延迟秒数 (默认: 3)')
    parser.add_argument('--hits', type=int, default=10, help='每个 ASV 保留的 BLAST hits 数量 (默认: 10)')
    parser.add_argument('--skip-existing', '-s', action='store_true', help='跳过已存在的结果文件')

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.otu_table):
        print(f"错误: OTU 表文件不存在: {args.otu_table}")
        sys.exit(1)
    if not os.path.exists(args.fasta):
        print(f"错误: FASTA 文件不存在: {args.fasta}")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)

    # 解析 OTU 表
    print("解析 OTU 表...")
    asv_data, sample_groups = parse_otu_table(args.otu_table)
    print(f"发现 {len(asv_data)} 个 ASV, {len(sample_groups)} 个样本组")

    # 找到每个样本的 Top ASV
    print("查找每个样本的 Top ASV...")
    top_asvs = find_top_asv_per_sample(asv_data, sample_groups)

    # 保存 ASV 信息
    asv_info_file = os.path.join(args.output, "top_asv_info.csv")
    with open(asv_info_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Sample', 'ASV', 'Count', 'Taxonomy'])
        for sample in sorted(top_asvs.keys()):
            info = top_asvs[sample]
            writer.writerow([sample, info['asv_id'], info['count'], info['taxonomy']])
    print(f"ASV 信息保存至: {asv_info_file}")

    # 提取序列
    unique_asvs = set(info['asv_id'] for info in top_asvs.values())
    print(f"需要提取 {len(unique_asvs)} 条唯一序列...")
    sequences = extract_sequences(args.fasta, unique_asvs)
    print(f"成功提取 {len(sequences)} 条序列")

    # 进行 BLAST 比对
    top_hits = []
    for i, (sample, info) in enumerate(sorted(top_asvs.items()), 1):
        asv_id = info['asv_id']
        output_csv = os.path.join(args.output, f"{sample}.csv")

        # 检查是否已有结果
        if args.skip_existing and os.path.exists(output_csv):
            print(f"[{i}/{len(top_asvs)}] {sample}: 已存在，跳过")
            with open(output_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                first_row = next(reader, None)
                if first_row:
                    top_hits.append({
                        'sample': sample,
                        'description': first_row['Description'],
                        'scientific_name': first_row['Scientific Name'],
                        'max_score': first_row['Max Score'],
                        'e_value': first_row['E value'],
                        'per_ident': first_row['Per. ident'],
                        'accession': first_row['Accession']
                    })
            continue

        if asv_id not in sequences:
            print(f"[{i}/{len(top_asvs)}] {sample}: 序列 {asv_id} 不存在，跳过")
            continue

        print(f"[{i}/{len(top_asvs)}] 正在比对 {sample} ({asv_id})...")

        result = run_blast(sequences[asv_id], args.hits)

        if result:
            top_hit = parse_blast_results(result, output_csv, sample)
            result.close()
            if top_hit:
                top_hits.append(top_hit)
                print(f"    -> {top_hit['scientific_name']} ({top_hit['per_ident']}%)")
        else:
            print(f"    -> 比对失败")

        if i < len(top_asvs):
            time.sleep(args.delay)

    # 创建汇总表
    summary_file = os.path.join(args.output, "blast_summary.csv")
    create_summary(summary_file, top_hits, top_asvs)
    print(f"\n完成! 汇总表保存至: {summary_file}")


if __name__ == "__main__":
    main()
