#!/usr/bin/env python3
"""
氨基酸序列分析工作流程 - 按物种单独分析
支持断点续传：任意步骤中断后，重新运行可从断点继续

断点续传机制：
- 每完成一个物种的比对，立即写入 checkpoint.json
- 重启时读取 checkpoint，跳过已完成的物种/步骤
- 通过 --resume <task_dir> 参数指定续传目录
"""

import os
import shutil
import subprocess
import pandas as pd
from datetime import datetime
import json
from collections import defaultdict
import argparse
import sys


# ============================================================
# 氨基酸分类体系（已由用户确认，严格执行，不得修改）
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


class SpeciesLevelAnalysisWorkflow:
    """
    物种级别的氨基酸序列分析工作流（含断点续传）

    分析步骤：
    1. 环境检查 & 扫描输入文件
    2. 多序列比对（clustalo，按物种，逐个保存checkpoint）
    3. 提取共识序列
    4. 计算氨基酸对频率
    5. 选择Top 5氨基酸对并计算配方
    6. 生成输出文件
    """

    CHECKPOINT_FILE = "checkpoint.json"

    def __init__(self, task_name, data_dir, resume_dir=None, consensus_threshold=0.5):
        """
        初始化

        Args:
            task_name            (str):   任务名称
            data_dir             (str):   原始数据目录
            resume_dir           (str):   若指定，则从该目录续传；否则新建目录
            consensus_threshold  (float): 共识序列保守性阈值（默认0.5）
                                          某位置最高频氨基酸占比 >= 该值 → 写入残基
                                          否则标记为 X（低保守，后续被剔除）
        """
        self.consensus_threshold = consensus_threshold
        self.task_name = task_name
        self.data_dir  = data_dir

        # 氨基酸分类
        self.functional_classes = FUNCTIONAL_CLASSES
        self.aa_to_class = {
            aa: cls
            for cls, aas in self.functional_classes.items()
            for aa in aas
        }

        # 目录初始化
        if resume_dir and os.path.isdir(resume_dir):
            self.task_dir = resume_dir
            print(f"[续传模式] 使用已有目录: {self.task_dir}")
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.task_dir = (
                f"/home/lenovo/.openclaw/workspace/analysis_results"
                f"/{task_name}_{timestamp}"
            )
            os.makedirs(self.task_dir, exist_ok=True)

        self.subdirs = {
            'aligned_sequences': f"{self.task_dir}/aligned_sequences",
            'species_analysis':  f"{self.task_dir}/species_analysis",
            'pair_analysis':     f"{self.task_dir}/pair_analysis",
            'formulations':      f"{self.task_dir}/formulations",
            'output_files':      f"{self.task_dir}/output_files",
            'logs':              f"{self.task_dir}/logs",
        }
        for subdir in self.subdirs.values():
            os.makedirs(subdir, exist_ok=True)

        # 日志文件
        self.log_file = f"{self.subdirs['logs']}/analysis_log.txt"

        # 加载或初始化 checkpoint
        self.checkpoint_path = os.path.join(self.task_dir, self.CHECKPOINT_FILE)
        self.checkpoint = self._load_checkpoint()

    # ----------------------------------------------------------
    # Checkpoint 读写
    # ----------------------------------------------------------

    def _load_checkpoint(self):
        """加载已有 checkpoint；不存在则返回初始结构"""
        if os.path.exists(self.checkpoint_path):
            with open(self.checkpoint_path, 'r', encoding='utf-8') as f:
                cp = json.load(f)
            self.log(f"📂 加载断点记录，已完成物种: "
                     f"{list(cp.get('aligned', {}).keys())}")
            return cp
        return {
            "aligned":    {},   # species_name -> aligned_fasta_path
            "consensus":  {},   # species_name -> consensus_seq (str)
            "pairs_done": False,
            "formulations_done": False,
            "outputs_done": False,
        }

    def _save_checkpoint(self):
        """将当前进度写入 checkpoint.json"""
        with open(self.checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(self.checkpoint, f, ensure_ascii=False, indent=2)

    # ----------------------------------------------------------
    # 日志
    # ----------------------------------------------------------

    def log(self, message):
        ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{ts}] {message}"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(msg + "\n")
        print(msg)

    # ----------------------------------------------------------
    # Step 1: 环境检查
    # ----------------------------------------------------------

    def step1_environment_check(self):
        self.log(f"=== 开始任务: {self.task_name} ===")
        self.log(f"任务目录: {self.task_dir}")
        self.log(f"原始数据目录: {self.data_dir}")

        for tool in ['clustalo', 'python3']:
            try:
                subprocess.run([tool, '--version'], capture_output=True, check=True)
                self.log(f"✅ {tool} 可用")
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.log(f"❌ {tool} 不可用")
                raise RuntimeError(f"{tool} 不可用")

        species_files = {
            os.path.splitext(f)[0]: os.path.join(self.data_dir, f)
            for f in os.listdir(self.data_dir)
            if f.endswith(('.fasta', '.fa', '.fas'))
        }

        if not species_files:
            raise FileNotFoundError("未找到序列文件")

        self.log(f"📁 找到 {len(species_files)} 个物种文件")
        for name in sorted(species_files):
            self.log(f"  - {name}")

        return species_files

    # ----------------------------------------------------------
    # Step 2: 多序列比对（含断点续传：逐个物种保存）
    # ----------------------------------------------------------

    def step2_multiple_sequence_alignment(self, species_files):
        self.log("=== 步骤2: 多序列比对 (按物种) ===")

        already_done = self.checkpoint.get("aligned", {})
        aligned_files = dict(already_done)  # 已完成的直接带入

        skipped = [s for s in species_files if s in already_done]
        if skipped:
            self.log(f"⏭️  跳过已完成比对的物种 ({len(skipped)} 个): {skipped}")

        pending = {s: p for s, p in species_files.items() if s not in already_done}
        self.log(f"🔄 待比对物种: {len(pending)} 个")

        for species_name, input_path in pending.items():
            output_path = os.path.join(
                self.subdirs['aligned_sequences'],
                f"{species_name}_aligned.fasta"
            )
            self.log(f"正在比对物种: {species_name}")

            try:
                subprocess.run(
                    ['clustalo', '-i', input_path, '-o', output_path,
                     '--outfmt=fasta', '--force'],
                    check=True, capture_output=True
                )
                aligned_files[species_name] = output_path
                # ✅ 立即写 checkpoint
                self.checkpoint["aligned"][species_name] = output_path
                self._save_checkpoint()
                self.log(f"✅ 比对完成: {species_name}")

            except subprocess.CalledProcessError as e:
                err = e.stderr.decode() if e.stderr else "未知错误"
                self.log(f"❌ 比对失败: {species_name} — {err}")
                # 失败不中断，继续下一个物种

        self.log(f"📊 成功比对 {len(aligned_files)}/{len(species_files)} 个物种")
        return aligned_files

    # ----------------------------------------------------------
    # Step 3: 提取共识序列（含断点续传）
    # ----------------------------------------------------------

    def step3_extract_consensus_sequence(self, aligned_files):
        self.log("=== 步骤3: 提取共识序列 ===")

        already_done = self.checkpoint.get("consensus", {})
        consensus_sequences = dict(already_done)

        skipped = [s for s in aligned_files if s in already_done]
        if skipped:
            self.log(f"⏭️  跳过已完成共识提取的物种 ({len(skipped)} 个): {skipped}")

        for species_name, aligned_path in aligned_files.items():
            if species_name in already_done:
                continue

            self.log(f"正在提取 {species_name} 的共识序列")
            sequences = self._parse_fasta(aligned_path)

            if not sequences:
                self.log(f"⚠️  {species_name} 无序列数据，跳过")
                continue

            consensus = self._calculate_consensus(sequences, threshold=self.consensus_threshold)
            consensus_sequences[species_name] = consensus

            # 保存共识序列文件
            out = os.path.join(
                self.subdirs['species_analysis'],
                f"{species_name}_consensus.fasta"
            )
            with open(out, 'w') as f:
                f.write(f">{species_name}_consensus\n{consensus}\n")

            # ✅ 写 checkpoint
            self.checkpoint["consensus"][species_name] = consensus
            self._save_checkpoint()
            self.log(f"✅ {species_name}: 共识序列长度 {len(consensus)}")

        self.log(f"📊 成功提取 {len(consensus_sequences)} 个共识序列")
        return consensus_sequences

    def _parse_fasta(self, file_path):
        sequences, current = [], []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if current:
                        sequences.append(''.join(current))
                        current = []
                else:
                    current.append(line)
        if current:
            sequences.append(''.join(current))
        return sequences

    def _calculate_consensus(self, sequences, threshold=0.5):
        """
        生成共识序列。
        threshold: 保守性阈值（默认0.5）。
            某位置最高频氨基酸的出现比例 >= threshold → 写入该氨基酸
            否则 → 标记为 'X'（低保守位点，后续分析中将被剔除）
        """
        if not sequences:
            return ""
        length    = len(sequences[0])
        consensus = []
        for i in range(length):
            counts = defaultdict(int)
            for seq in sequences:
                if i < len(seq):
                    counts[seq[i]] += 1
            # 忽略 gap，只统计真实氨基酸
            valid = {aa: c for aa, c in counts.items() if aa != '-'}
            if not valid:
                consensus.append('-')
                continue
            best_aa    = max(valid, key=valid.get)
            total_valid = sum(valid.values())
            # 保守性阈值判断
            if valid[best_aa] / total_valid >= threshold:
                consensus.append(best_aa)
            else:
                consensus.append('X')   # 低保守位点 → X
        return ''.join(consensus).replace('-', '')

    # ----------------------------------------------------------
    # Step 4: 计算氨基酸对频率（整体步骤，含续传检查）
    # ----------------------------------------------------------

    def step4_calculate_pair_frequencies(self, consensus_sequences):
        self.log("=== 步骤4: 计算氨基酸对频率 ===")
        self.log("    统计规则：剔除X/A/G/P后拼接为新序列，统计新序列中的相邻对")

        # 如果已有保存的结果，直接加载
        pairs_file = os.path.join(self.subdirs['pair_analysis'], 'all_species_pairs.json')
        if self.checkpoint.get("pairs_done") and os.path.exists(pairs_file):
            self.log("⏭️  步骤4已完成，从文件加载结果")
            with open(pairs_file, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            # 反序列化 key 为 tuple
            all_species_pairs = {}
            for species, data in raw.items():
                all_species_pairs[species] = {
                    'total_pairs': data['total_pairs'],
                    'pair_frequencies': {
                        tuple(k.split('_', 1)): v
                        for k, v in data['pair_frequencies'].items()
                    }
                }
            return all_species_pairs

        all_species_pairs = {}

        EXCLUDE = set('XAGP')

        for species_name, consensus_seq in consensus_sequences.items():
            self.log(f"正在分析 {species_name} 的氨基酸对")

            # 剔除 X/A/G/P 后拼接为新序列，再统计相邻对（与文献方法一致）
            filtered_seq = ''.join(aa for aa in consensus_seq if aa not in EXCLUDE)

            pair_counts = defaultdict(int)
            total_pairs = 0
            for i in range(len(filtered_seq) - 1):
                aa_i = filtered_seq[i]
                aa_j = filtered_seq[i + 1]
                if aa_i in self.aa_to_class and aa_j in self.aa_to_class:
                    pair = (self.aa_to_class[aa_i], self.aa_to_class[aa_j])
                    pair_counts[pair] += 1
                    total_pairs += 1

            pair_frequencies = {
                pair: {'count': cnt,
                       'frequency': cnt / total_pairs if total_pairs else 0}
                for pair, cnt in pair_counts.items()
            }

            all_species_pairs[species_name] = {
                'total_pairs': total_pairs,
                'pair_frequencies': pair_frequencies,
            }
            self.log(f"✅ {species_name}: {total_pairs} 个有效相邻对")

        # 保存（JSON key 转为 str）
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

        self.checkpoint["pairs_done"] = True
        self._save_checkpoint()
        return all_species_pairs

    # ----------------------------------------------------------
    # Step 5: Top 5 配方计算（含续传检查）
    # ----------------------------------------------------------

    def step5_select_top_pairs_and_calculate_formulation(self, all_species_pairs):
        self.log("=== 步骤5: 选择Top 5氨基酸对并计算配方 ===")

        formulations_file = os.path.join(self.subdirs['formulations'], 'species_formulations.json')
        if self.checkpoint.get("formulations_done") and os.path.exists(formulations_file):
            self.log("⏭️  步骤5已完成，从文件加载结果")
            with open(formulations_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        species_formulations = {}

        # 生成所有21种对称对型标签
        all_pair_types = []
        cls_list = list(self.functional_classes.keys())  # dict→list，支持切片
        for idx_a, cls_a in enumerate(cls_list):
            for cls_b in cls_list[idx_a:]:
                all_pair_types.append(tuple(sorted([cls_a, cls_b])))

        for species_name, data in all_species_pairs.items():
            self.log(f"正在计算 {species_name} 的配方")

            # 先合并对称对（A-B 与 B-A 合并），再选 Top5（与文献方法一致）
            sym_counts = defaultdict(int)
            for (ci, cj), freq in data['pair_frequencies'].items():
                sym_key = tuple(sorted([ci, cj]))
                sym_counts[sym_key] += freq['count']

            sorted_pairs = sorted(sym_counts.items(), key=lambda x: -x[1])
            top5 = sorted_pairs[:5]   # list of (sym_key, count)

            top5_total = sum(cnt for _, cnt in top5)
            total_pairs = data['total_pairs']
            top5_pct = (top5_total / total_pairs * 100) if total_pairs else 0

            class_counts = defaultdict(int)
            for (ci, cj), cnt in top5:
                class_counts[ci] += cnt
                class_counts[cj] += cnt

            total_ni = sum(class_counts.values())
            relative_composition = {
                cls: {
                    'Ni': class_counts.get(cls, 0),
                    'phi_percent': round(
                        class_counts.get(cls, 0) / total_ni * 100
                        if total_ni else 0, 2
                    )
                }
                for cls in self.functional_classes
            }

            # 汇总所有21种对型的计数（合并对称对 A-B 和 B-A）
            sym_pair_counts = defaultdict(int)
            for (ci, cj), freq in data['pair_frequencies'].items():
                key = tuple(sorted([ci, cj]))
                sym_pair_counts[key] += freq['count']
            all_pair_counts = {f"{a}-{b}": sym_pair_counts.get((a, b), 0)
                               for (a, b) in all_pair_types}

            species_formulations[species_name] = {
                'top_5_pairs': [
                    {
                        'pair': f"{ci}-{cj}",
                        'count': cnt,
                        'frequency': round(cnt / total_pairs * 100, 2) if total_pairs else 0
                    }
                    for (ci, cj), cnt in top5
                ],
                'top_5_total_count': top5_total,
                'top_5_percentage': round(top5_pct, 2),
                'relative_composition': relative_composition,
                'all_pair_counts': all_pair_counts,
                'total_pairs': total_pairs
            }
            self.log(f"✅ {species_name}: Top 5占 {top5_pct:.1f}%")

        with open(formulations_file, 'w', encoding='utf-8') as f:
            json.dump(species_formulations, f, ensure_ascii=False, indent=2)

        self.checkpoint["formulations_done"] = True
        self._save_checkpoint()
        return species_formulations

    # ----------------------------------------------------------
    # Step 6: 生成输出文件（含续传检查）
    # ----------------------------------------------------------

    def step6_generate_output_files(self, species_formulations):
        self.log("=== 步骤6: 生成输出文件 ===")

        out_dir = self.subdirs['output_files']
        formulations_csv = os.path.join(out_dir, 'species_formulations.csv')
        top_pairs_csv    = os.path.join(out_dir, 'top_5_pairs_details.csv')
        summary_csv      = os.path.join(out_dir, 'formulation_summary.csv')

        if (self.checkpoint.get("outputs_done")
                and all(os.path.exists(p) for p in [formulations_csv, top_pairs_csv, summary_csv])):
            self.log("⏭️  步骤6已完成，跳过")
            return formulations_csv, top_pairs_csv, summary_csv

        # species_formulations.csv
        rows = []
        for sp, fm in species_formulations.items():
            row = {
                'species': sp,
                'total_pairs': fm['total_pairs'],
                'top_5_pairs': '; '.join(p['pair'] for p in fm['top_5_pairs']),
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
                'species': sp,
                'rank': i + 1,
                'pair': p['pair'],
                'count': p['count'],
                'frequency_percent': p['frequency'],
            }
            for sp, fm in species_formulations.items()
            for i, p in enumerate(fm['top_5_pairs'])
        ]
        pd.DataFrame(pair_rows).to_csv(top_pairs_csv, index=False)

        # formulation_summary.csv
        unique = self._identify_unique_formulations(species_formulations)
        pd.DataFrame([{
            'total_species': len(species_formulations),
            'unique_formulations': len(unique),
            'duplicate_formulations': len(species_formulations) - len(unique),
        }]).to_csv(summary_csv, index=False)

        self.log("✅ 输出文件生成完成:")
        for path in [formulations_csv, top_pairs_csv, summary_csv]:
            self.log(f"  - {path}")

        self.checkpoint["outputs_done"] = True
        self._save_checkpoint()
        return formulations_csv, top_pairs_csv, summary_csv

    def _identify_unique_formulations(self, species_formulations):
        seen = {}
        for sp, fm in species_formulations.items():
            sig = tuple(sorted(
                (cls, round(comp['phi_percent'], 1))
                for cls, comp in fm['relative_composition'].items()
            ))
            seen.setdefault(sig, []).append(sp)
        return seen

    # ----------------------------------------------------------
    # 主入口
    # ----------------------------------------------------------

    def run_complete_analysis(self):
        try:
            species_files       = self.step1_environment_check()
            aligned_files       = self.step2_multiple_sequence_alignment(species_files)

            if not aligned_files:
                self.log("❌ 没有成功比对的文件，退出")
                return None

            consensus_sequences = self.step3_extract_consensus_sequence(aligned_files)

            if not consensus_sequences:
                self.log("❌ 没有共识序列，退出")
                return None

            all_species_pairs   = self.step4_calculate_pair_frequencies(consensus_sequences)
            species_formulations = self.step5_select_top_pairs_and_calculate_formulation(all_species_pairs)
            formulations_csv, top_pairs_csv, summary_csv = \
                self.step6_generate_output_files(species_formulations)

            self.log("=" * 60)
            self.log(f"分析完成! 成功分析: {len(species_formulations)}/{len(species_files)} 个物种")
            self.log(f"结果目录: {self.task_dir}")
            self.log("=" * 60)

            return {
                'task_dir':          self.task_dir,
                'species_count':     len(species_files),
                'formulations_count': len(species_formulations),
                'formulations_csv':  formulations_csv,
                'top_pairs_csv':     top_pairs_csv,
                'summary_csv':       summary_csv,
            }

        except Exception as e:
            import traceback
            self.log(f"❌ 任务异常中断: {e}")
            self.log(traceback.format_exc())
            self.log(f"💡 续传命令: python {__file__} --resume {self.task_dir} {self.task_name} {self.data_dir}")
            raise


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="爬行动物氨基酸对分析（支持断点续传）"
    )
    parser.add_argument("task_name", help="任务名称")
    parser.add_argument("data_dir",  help="原始FASTA数据目录")
    parser.add_argument(
        "--resume", metavar="TASK_DIR",
        help="指定已有任务目录，从断点继续（省略则新建）"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.5, metavar="FLOAT",
        help="共识序列保守性阈值（默认0.5）：某位置最高频氨基酸占比>=该值时写入，否则标记X"
    )
    args = parser.parse_args()

    workflow = SpeciesLevelAnalysisWorkflow(
        task_name            = args.task_name,
        data_dir             = args.data_dir,
        resume_dir           = args.resume,
        consensus_threshold  = args.threshold,
    )
    result = workflow.run_complete_analysis()
    if result:
        print(f"\n✅ 完成！结果: {result['task_dir']}")


# 向后兼容的函数接口
def run_species_analysis(task_name, data_directory, resume_dir=None):
    workflow = SpeciesLevelAnalysisWorkflow(task_name, data_directory, resume_dir)
    return workflow.run_complete_analysis()


if __name__ == "__main__":
    main()
