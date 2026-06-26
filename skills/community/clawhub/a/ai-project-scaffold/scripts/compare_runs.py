#!/usr/bin/env python3
"""
AI 项目实验对比脚本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
自动扫描训练运行，汇总关键指标对比表。

支持:
  - 同一架构下多个运行的对比
  - 跨架构对比
  - 预训练 / 后训练 / RL 各阶段对比

用法:
  python3 compare_runs.py --name MyProject                     # 全部对比
  python3 compare_runs.py --name MyProject --arch llama3        # 指定架构
  python3 compare_runs.py --name MyProject --stage post_training # 只看后训练
"""

import argparse
import os
import sys
import json
from datetime import datetime


class RunComparator:
    def __init__(self, base: str, project_name: str):
        self.base = base
        self.name = project_name

    def run(self, arch: str = None, stage: str = None):
        print(f"\n{'='*60}")
        print(f"📊 AI 项目实验对比: {self.name}")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}")

        if stage is None or stage == "pretraining":
            self._compare_pretraining(arch)
        if stage is None or stage == "post_training":
            self._compare_post_training()
        if stage is None or stage == "rl":
            self._compare_rl()
        if stage is None or stage == "tokenization":
            self._compare_tokenization()

        print()

    def _scan_run_metrics(self, run_dir: str) -> dict:
        """扫描单个运行的目录，提取关键指标"""
        metrics = {}

        # 检查 configs 目录
        configs_dir = os.path.join(run_dir, "configs")
        if os.path.isdir(configs_dir):
            for f in os.listdir(configs_dir):
                if f.endswith(('.yaml', '.yml', '.json')):
                    metrics["has_config"] = True
                    break

        # 检查 logs 目录
        logs_dir = os.path.join(run_dir, "logs")
        if os.path.isdir(logs_dir):
            log_files = [f for f in os.listdir(logs_dir) if f.endswith(('.log', '.txt', '.out'))]
            metrics["log_files"] = len(log_files)
            # 尝试读取训练日志找 loss
            for lf in log_files:
                # 简单采样，不读全文件
                lf_path = os.path.join(logs_dir, lf)
                try:
                    with open(lf_path, errors='ignore') as f:
                        for line in f:
                            line = line.strip()
                            if 'loss' in line.lower() and ('=' in line or ':' in line):
                                metrics["has_loss_in_log"] = True
                                break
                except Exception:
                    pass

        # 检查 checkpoints
        ckpt_dir = os.path.join(run_dir, "checkpoints")
        if os.path.isdir(ckpt_dir):
            ckpt_files = [f for f in os.listdir(ckpt_dir) if not f.startswith('.')]
            metrics["checkpoint_count"] = len(ckpt_files)
            # 估算大小
            total_size = 0
            for f in ckpt_files:
                fpath = os.path.join(ckpt_dir, f)
                if os.path.isfile(fpath):
                    total_size += os.path.getsize(fpath)
            metrics["checkpoint_size_mb"] = round(total_size / (1024 * 1024), 1)

        # 检查 eval
        eval_dir = os.path.join(run_dir, "eval")
        if os.path.isdir(eval_dir):
            eval_files = [f for f in os.listdir(eval_dir) if not f.startswith('.')]
            metrics["eval_files"] = len(eval_files)

        return metrics

    def _compare_pretraining(self, arch_filter: str = None):
        print(f"\n🧠 ── 预训练对比 ──")

        pt_dir = os.path.join(self.base, "03_models/01_pretraining")
        if not os.path.isdir(pt_dir):
            print("  (尚无预训练运行)")
            return

        all_runs = []
        for arch in sorted(os.listdir(pt_dir)):
            arch_dir = os.path.join(pt_dir, arch)
            if not os.path.isdir(arch_dir):
                continue
            if arch_filter and arch != arch_filter:
                continue

            for run in sorted(os.listdir(arch_dir)):
                run_dir = os.path.join(arch_dir, run)
                if not os.path.isdir(run_dir):
                    continue
                metrics = self._scan_run_metrics(run_dir)
                all_runs.append({
                    "arch": arch,
                    "run": run,
                    "path": run_dir,
                    "metrics": metrics,
                })

        if not all_runs:
            print("  (无匹配的运行)")
            return

        # 打印对比表
        print(f"\n  {'架构':<15} {'运行':<20} {'配置':<8} {'日志':<8} {'Checkpoint':<12} {'评估':<8}")
        print(f"  {'─'*15} {'─'*20} {'─'*8} {'─'*8} {'─'*12} {'─'*8}")
        for r in all_runs:
            m = r["metrics"]
            has_config = "✅" if m.get("has_config") else "❌"
            log_info = f"{m.get('log_files', 0)}文件"
            ckpt_info = f"{m.get('checkpoint_count', 0)}个/{m.get('checkpoint_size_mb', 0)}MB"
            eval_info = f"{m.get('eval_files', 0)}文件"
            print(f"  {r['arch']:<15} {r['run']:<20} {has_config:<8} {log_info:<8} {ckpt_info:<12} {eval_info:<8}")

        print(f"\n  共 {len(all_runs)} 个预训练运行")

    def _compare_post_training(self):
        print(f"\n🔧 ── 后训练对比 ──")

        post_dir = os.path.join(self.base, "03_models/02_post_training")
        if not os.path.isdir(post_dir):
            print("  (无后训练运行)")
            return

        all_runs = []
        for method in sorted(os.listdir(post_dir)):
            method_dir = os.path.join(post_dir, method)
            if not os.path.isdir(method_dir):
                continue
            for run in sorted(os.listdir(method_dir)):
                run_dir = os.path.join(method_dir, run)
                if not os.path.isdir(run_dir):
                    continue
                metrics = self._scan_run_metrics(run_dir)
                all_runs.append({
                    "method": method,
                    "run": run,
                    "metrics": metrics,
                })

        if not all_runs:
            print("  (无匹配的运行)")
            return

        print(f"\n  {'方法':<12} {'运行':<20} {'配置':<8} {'日志':<8} {'Checkpoint':<12} {'评估':<8}")
        print(f"  {'─'*12} {'─'*20} {'─'*8} {'─'*8} {'─'*12} {'─'*8}")
        for r in all_runs:
            m = r["metrics"]
            has_config = "✅" if m.get("has_config") else "❌"
            log_info = f"{m.get('log_files', 0)}文件"
            ckpt_info = f"{m.get('checkpoint_count', 0)}个"
            eval_info = f"{m.get('eval_files', 0)}文件"
            print(f"  {r['method']:<12} {r['run']:<20} {has_config:<8} {log_info:<8} {ckpt_info:<12} {eval_info:<8}")

        print(f"\n  共 {len(all_runs)} 个后训练运行")

    def _compare_rl(self):
        print(f"\n🎮 ── RL 对比 ──")

        rl_dir = os.path.join(self.base, "03_models/03_rl")
        if not os.path.isdir(rl_dir):
            print("  (无 RL 运行)")
            return

        all_runs = []
        for method in sorted(os.listdir(rl_dir)):
            method_dir = os.path.join(rl_dir, method)
            if not os.path.isdir(method_dir):
                continue
            for run in sorted(os.listdir(method_dir)):
                run_dir = os.path.join(method_dir, run)
                if not os.path.isdir(run_dir):
                    continue
                metrics = self._scan_run_metrics(run_dir)
                all_runs.append({
                    "method": method,
                    "run": run,
                    "metrics": metrics,
                })

        if not all_runs:
            print("  (无匹配的运行)")
            return

        print(f"\n  {'方法':<16} {'运行':<20} {'配置':<8} {'日志':<8} {'Checkpoint':<12} {'评估':<8}")
        print(f"  {'─'*16} {'─'*20} {'─'*8} {'─'*8} {'─'*12} {'─'*8}")
        for r in all_runs:
            m = r["metrics"]
            has_config = "✅" if m.get("has_config") else "❌"
            log_info = f"{m.get('log_files', 0)}文件"
            ckpt_info = f"{m.get('checkpoint_count', 0)}个"
            eval_info = f"{m.get('eval_files', 0)}文件"
            print(f"  {r['method']:<16} {r['run']:<20} {has_config:<8} {log_info:<8} {ckpt_info:<12} {eval_info:<8}")

        print(f"\n  共 {len(all_runs)} 个 RL 运行")

    def _compare_tokenization(self):
        print(f"\n🔤 ── 分词对比 ──")

        custom_dir = os.path.join(self.base, "02_tokenization/02_custom")
        if not os.path.isdir(custom_dir):
            print("  (无分词方案)")
            return

        approaches = sorted([d for d in os.listdir(custom_dir)
                             if os.path.isdir(os.path.join(custom_dir, d))])
        if not approaches:
            print("  (无分词方案)")
            return

        print(f"\n  {'方案':<20} {'脚本':<8} {'词表':<8} {'评估':<8} {'README':<8}")
        print(f"  {'─'*20} {'─'*8} {'─'*8} {'─'*8} {'─'*8}")
        for app in approaches:
            app_dir = os.path.join(custom_dir, app)
            has_scripts = bool(os.path.isdir(os.path.join(app_dir, "scripts")) and
                               [f for f in os.listdir(os.path.join(app_dir, "scripts"))
                                if f.endswith(('.py', '.sh'))])
            has_vocab = bool(os.path.isdir(os.path.join(app_dir, "vocab_output")) and
                             os.listdir(os.path.join(app_dir, "vocab_output")))
            eval_path = os.path.join(app_dir, "eval.md")
            has_eval = os.path.isfile(eval_path) and os.path.getsize(eval_path) > 100
            readme_path = os.path.join(app_dir, "README.md")
            has_readme = os.path.isfile(readme_path) and os.path.getsize(readme_path) > 50

            print(f"  {app:<20} {'✅' if has_scripts else '❌':<8} "
                  f"{'✅' if has_vocab else '❌':<8} "
                  f"{'✅' if has_eval else '❌':<8} "
                  f"{'✅' if has_readme else '❌':<8}")

        print(f"\n  共 {len(approaches)} 个分词方案")


def main():
    parser = argparse.ArgumentParser(description="AI 项目实验对比工具")
    parser.add_argument("--name", type=str, required=True, help="项目名称")
    parser.add_argument("--output", type=str, default=".", help="项目父目录")
    parser.add_argument("--arch", type=str, help="只对比指定架构")
    parser.add_argument("--stage", type=str,
                        choices=["pretraining", "post_training", "rl", "tokenization"],
                        help="只对比指定阶段")
    args = parser.parse_args()

    base = os.path.join(args.output, args.name)
    if not os.path.isdir(base):
        print(f"❌ 项目不存在: {base}")
        sys.exit(1)

    comparator = RunComparator(base, args.name)
    comparator.run(arch=args.arch, stage=args.stage)


if __name__ == "__main__":
    main()
