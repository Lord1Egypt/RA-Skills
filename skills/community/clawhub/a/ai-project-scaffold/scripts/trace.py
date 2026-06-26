#!/usr/bin/env python3
"""
AI 项目追踪链自动生成脚本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
扫描项目目录，自动推导并可视化：
  - 数据 → 分词 → 模型 的完整追踪链
  - 每层的输入/输出关系
  - 未连接的孤立组件

用法:
  python3 trace.py --name MyProject [--output .]
  python3 trace.py --name MyProject --layer tokenization   # 只看分词层
  python3 trace.py --name MyProject --full                  # 包含所有文件详情
"""

import argparse
import os
import sys
from datetime import datetime


class TraceGenerator:
    def __init__(self, base: str, project_name: str):
        self.base = base
        self.name = project_name

    def run(self, layer: str = None, full: bool = False):
        print(f"\n{'='*60}")
        print(f"🔗 AI 项目追踪链: {self.name}")
        print(f"📁 {os.path.abspath(self.base)}")
        print(f"{'='*60}\n")

        if layer is None or layer == "data":
            self._trace_data()
        if layer is None or layer == "tokenization":
            self._trace_tokenization()
        if layer is None or layer == "models":
            self._trace_models()

        print(f"\n{'='*60}")
        print(f"📋 全局追踪链")
        print(f"{'='*60}")
        self._trace_full_chain()

        if full:
            self._trace_files()

    def _trace_data(self):
        print("📊 ── 数据层 ──")

        raw_dir = os.path.join(self.base, "01_data/01_raw")
        sources = []
        if os.path.isdir(raw_dir):
            sources = [d for d in sorted(os.listdir(raw_dir))
                       if os.path.isdir(os.path.join(raw_dir, d)) and d.startswith("source_")]

        if not sources:
            print("  (尚无数据来源)\n")
            return

        for src in sources:
            meta_path = os.path.join(raw_dir, src, "metadata.yaml")
            source_type = "?"
            language = "?"
            if os.path.isfile(meta_path):
                with open(meta_path) as f:
                    for line in f:
                        if line.startswith("source_type:"):
                            source_type = line.split(":", 1)[1].strip().strip("#").strip()
                        if line.startswith("language:"):
                            language = line.split(":", 1)[1].strip().strip("#").strip()

            data_dir = os.path.join(raw_dir, src, "data")
            file_count = 0
            if os.path.isdir(data_dir):
                file_count = sum(1 for _ in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, _)))

            print(f"  📦 {src}")
            print(f"     类型: {source_type}  语言: {language}  文件数: {file_count}")

        # QC
        qc_scripts = []
        qc_scripts_dir = os.path.join(self.base, "01_data/02_qc/scripts")
        if os.path.isdir(qc_scripts_dir):
            qc_scripts = [f for f in os.listdir(qc_scripts_dir) if f.endswith(('.py', '.sh', '.ipynb'))]
        qc_reports = []
        qc_reports_dir = os.path.join(self.base, "01_data/02_qc/reports")
        if os.path.isdir(qc_reports_dir):
            qc_reports = os.listdir(qc_reports_dir)

        print(f"\n  🔍 QC 脚本: {len(qc_scripts)} 个")
        for s in qc_scripts:
            print(f"     • {s}")
        print(f"  📄 QC 报告: {len(qc_reports)} 个")
        print()

    def _trace_tokenization(self):
        print("🔤 ── 分词层 ──")

        custom_dir = os.path.join(self.base, "02_tokenization/02_custom")
        approaches = []
        if os.path.isdir(custom_dir):
            approaches = sorted([d for d in os.listdir(custom_dir)
                                 if os.path.isdir(os.path.join(custom_dir, d))])

        # 现成 tokenizer
        existing_dir = os.path.join(self.base, "02_tokenization/01_existing")
        existing = []
        if os.path.isdir(existing_dir):
            existing = sorted([d for d in os.listdir(existing_dir)
                               if os.path.isdir(os.path.join(existing_dir, d))])

        if existing:
            print("  📋 现成 tokenizer:")
            for e in existing:
                notes_path = os.path.join(existing_dir, e, "notes.md")
                has_notes = os.path.isfile(notes_path) and os.path.getsize(notes_path) > 20
                print(f"     • {e} {'✅ 有记录' if has_notes else '⚠️ 无记录'}")

        if not approaches:
            if not existing:
                print("  (尚无分词方案)\n")
            return

        print(f"  🛠 自制 tokenizer ({len(approaches)} 个):")
        for app in approaches:
            app_dir = os.path.join(custom_dir, app)
            eval_path = os.path.join(app_dir, "eval.md")
            has_eval = os.path.isfile(eval_path) and os.path.getsize(eval_path) > 100
            has_scripts = False
            scripts_dir = os.path.join(app_dir, "scripts")
            if os.path.isdir(scripts_dir):
                has_scripts = bool([f for f in os.listdir(scripts_dir) if f.endswith(('.py', '.sh'))])
            has_vocab = False
            vocab_dir = os.path.join(app_dir, "vocab_output")
            if os.path.isdir(vocab_dir):
                has_vocab = bool(os.listdir(vocab_dir))

            status = []
            if has_scripts:
                status.append("📝脚本")
            if has_vocab:
                status.append("📖词表")
            if has_eval:
                status.append("📊评估")
            status_str = " ".join(status) if status else "🕐 空"

            print(f"     • {app} [{status_str}]")

        # token 训练
        train_dir = os.path.join(self.base, "02_tokenization/03_training")
        train_runs = []
        if os.path.isdir(train_dir):
            train_runs = sorted([d for d in os.listdir(train_dir)
                                 if os.path.isdir(os.path.join(train_dir, d))])
        if train_runs:
            print(f"\n  🏋️ Token 训练 ({len(train_runs)} 个):")
            for t in train_runs:
                print(f"     • {t}")

        # 评估
        for eval_type in ["intrinsic", "extrinsic"]:
            eval_dir = os.path.join(self.base, f"02_tokenization/04_evaluation/{eval_type}")
            if os.path.isdir(eval_dir):
                files = [f for f in os.listdir(eval_dir) if not f.startswith('.')]
                if files:
                    print(f"  📊 {eval_type} 评估: {len(files)} 个文件")

        # 生成数据
        gen_dir = os.path.join(self.base, "02_tokenization/05_generated")
        if os.path.isdir(gen_dir):
            gen_files = [f for f in os.listdir(gen_dir)
                         if os.path.isfile(os.path.join(gen_dir, f)) and f != "README.md"]
            if gen_files:
                print(f"  🔄 分词产生的新数据: {len(gen_files)} 个文件")
        print()

    def _trace_models(self):
        print("🧠 ── 模型层 ──")

        # 预训练
        pt_dir = os.path.join(self.base, "03_models/01_pretraining")
        if os.path.isdir(pt_dir):
            archs = sorted([d for d in os.listdir(pt_dir)
                            if os.path.isdir(os.path.join(pt_dir, d))])
            if archs:
                print(f"  🏗 预训练架构 ({len(archs)} 个):")
                for arch in archs:
                    arch_dir = os.path.join(pt_dir, arch)
                    runs = sorted([d for d in os.listdir(arch_dir)
                                   if os.path.isdir(os.path.join(arch_dir, d))])
                    print(f"     • {arch}/ ({len(runs)} 个运行)")
                    for run in runs:
                        run_dir = os.path.join(arch_dir, run)
                        has_log = False
                        logs_dir = os.path.join(run_dir, "logs")
                        if os.path.isdir(logs_dir) and os.listdir(logs_dir):
                            has_log = True
                        has_eval = False
                        eval_dir = os.path.join(run_dir, "eval")
                        if os.path.isdir(eval_dir) and os.listdir(eval_dir):
                            has_eval = True
                        status = []
                        if has_log:
                            status.append("📋日志")
                        if has_eval:
                            status.append("📊评估")
                        status_str = " ".join(status) if status else "🕐 空"
                        print(f"       └─ {run} [{status_str}]")

        # 后训练
        post_dir = os.path.join(self.base, "03_models/02_post_training")
        if os.path.isdir(post_dir):
            methods = sorted([d for d in os.listdir(post_dir)
                              if os.path.isdir(os.path.join(post_dir, d))])
            post_runs = []
            for m in methods:
                m_dir = os.path.join(post_dir, m)
                runs = sorted([d for d in os.listdir(m_dir)
                               if os.path.isdir(os.path.join(m_dir, d))])
                if runs:
                    post_runs.append((m, runs))

            if post_runs:
                print(f"\n  🔧 后训练:")
                for method, runs in post_runs:
                    print(f"     • {method}/ ({len(runs)} 个运行)")
                    for run in runs:
                        print(f"       └─ {run}")

        # RL
        rl_dir = os.path.join(self.base, "03_models/03_rl")
        if os.path.isdir(rl_dir):
            rl_methods = sorted([d for d in os.listdir(rl_dir)
                                 if os.path.isdir(os.path.join(rl_dir, d))])
            rl_runs = []
            for m in rl_methods:
                m_dir = os.path.join(rl_dir, m)
                runs = sorted([d for d in os.listdir(m_dir)
                               if os.path.isdir(os.path.join(m_dir, d))])
                if runs:
                    rl_runs.append((m, runs))

            if rl_runs:
                print(f"\n  🎮 强化学习:")
                for method, runs in rl_runs:
                    print(f"     • {method}/ ({len(runs)} 个运行)")
                    for run in runs:
                        print(f"       └─ {run}")
        print()

    def _trace_full_chain(self):
        """生成完整的端到端追踪链"""
        raw_dir = os.path.join(self.base, "01_data/01_raw")
        custom_dir = os.path.join(self.base, "02_tokenization/02_custom")
        pt_dir = os.path.join(self.base, "03_models/01_pretraining")
        post_dir = os.path.join(self.base, "03_models/02_post_training")

        sources = []
        if os.path.isdir(raw_dir):
            sources = sorted([d for d in os.listdir(raw_dir)
                              if os.path.isdir(os.path.join(raw_dir, d)) and d.startswith("source_")])

        approaches = []
        if os.path.isdir(custom_dir):
            approaches = sorted([d for d in os.listdir(custom_dir)
                                 if os.path.isdir(os.path.join(custom_dir, d))])

        arch_runs = []
        if os.path.isdir(pt_dir):
            for arch in sorted(os.listdir(pt_dir)):
                arch_dir = os.path.join(pt_dir, arch)
                if os.path.isdir(arch_dir):
                    for run in sorted(os.listdir(arch_dir)):
                        if os.path.isdir(os.path.join(arch_dir, run)):
                            arch_runs.append(f"{arch}/{run}")

        post_runs = []
        if os.path.isdir(post_dir):
            for m in sorted(os.listdir(post_dir)):
                m_dir = os.path.join(post_dir, m)
                if os.path.isdir(m_dir):
                    for run in sorted(os.listdir(m_dir)):
                        if os.path.isdir(os.path.join(m_dir, run)):
                            post_runs.append(f"{m}/{run}")

        # 构建 ASCII 链路图
        chain_parts = []

        if sources:
            chain_parts.append(f"📦 {' → '.join(sources)}")
        if approaches:
            chain_parts.append(f"🔤 {' → '.join(approaches)}")
        if arch_runs:
            chain_parts.append(f"🧠 {' → '.join(arch_runs)}")
        if post_runs:
            chain_parts.append(f"🔧 {' → '.join(post_runs)}")

        if chain_parts:
            for part in chain_parts:
                print(f"  {part}")
        else:
            print("  🕐 项目尚未填充内容，追踪链为空")

        # 统计
        print(f"\n  📈 统计: {len(sources)} 数据源 → {len(approaches)} 分词方案 → {len(arch_runs)} 预训练 → {len(post_runs)} 后训练")

    def _trace_files(self):
        """列出所有非空文件"""
        print(f"\n{'='*60}")
        print(f"📄 文件详情")
        print(f"{'='*60}")
        for root, dirs, files in os.walk(self.base):
            # 跳过一些目录
            if any(skip in root for skip in ['.git', '__pycache__', 'checkpoints', 'logs']):
                continue
            for f in sorted(files):
                if f.startswith('.'):
                    continue
                fpath = os.path.join(root, f)
                rel = os.path.relpath(fpath, self.base)
                size = os.path.getsize(fpath)
                if size > 0:
                    print(f"  {rel} ({size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(description="AI 项目追踪链生成工具")
    parser.add_argument("--name", type=str, required=True, help="项目名称")
    parser.add_argument("--output", type=str, default=".", help="项目父目录")
    parser.add_argument("--layer", type=str, choices=["data", "tokenization", "models"],
                        help="只追踪指定层级")
    parser.add_argument("--full", "-f", action="store_true", help="显示所有文件详情")
    args = parser.parse_args()

    base = os.path.join(args.output, args.name)
    if not os.path.isdir(base):
        print(f"❌ 项目不存在: {base}")
        sys.exit(1)

    tracer = TraceGenerator(base, args.name)
    tracer.run(layer=args.layer, full=args.full)


if __name__ == "__main__":
    main()
