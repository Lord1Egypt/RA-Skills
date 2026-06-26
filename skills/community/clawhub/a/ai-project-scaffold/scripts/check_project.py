#!/usr/bin/env python3
"""
AI 项目健康检查脚本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
扫描项目目录，检查：
  - 数据来源是否都有 metadata.yaml
  - 分词方案是否都有 eval.md
  - 训练运行是否有日志
  - 实验日志是否更新
  - metadata.yaml 字段完整度
  - 目录结构完整性

用法:
  python3 check_project.py --name MyProject [--output .]
"""

import argparse
import os
import sys
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
# 检查规则
# ═══════════════════════════════════════════════════════════════

REQUIRED_DIRS = [
    "01_data", "02_tokenization", "03_models",
    "04_experiments", "05_docs", "06_shared",
]

REQUIRED_README = [
    "README.md", "_project_config.yaml", ".gitignore",
    "01_data/README.md", "01_data/04_quality_log.md",
    "02_tokenization/README.md",
    "03_models/README.md",
    "04_experiments/experiment_log.md",
]

METADATA_REQUIRED_FIELDS = [
    "source_name", "source_type", "url", "access_date",
    "license", "language", "description",
]

EVAL_REQUIRED_SECTIONS = [
    "内在评估", "下游评估",
]


def check_color(status: str) -> str:
    """简单的终端着色"""
    colors = {"OK": "✅", "WARN": "⚠️", "ERROR": "❌", "INFO": "ℹ️"}
    return colors.get(status, "  ")


class HealthChecker:
    def __init__(self, base: str, project_name: str):
        self.base = base
        self.name = project_name
        self.warnings = []
        self.errors = []
        self.passes = []

    def run_all(self):
        print(f"\n{'='*60}")
        print(f"🏥 AI 项目健康检查: {self.name}")
        print(f"📁 {os.path.abspath(self.base)}")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")

        self._check_dirs()
        self._check_readmes()
        self._check_gitignore()
        self._check_data_sources()
        self._check_quality_log()
        self._check_tokenizers()
        self._check_models()
        self._check_experiment_log()
        self._check_config_templates()

        self._print_summary()

    def _check_dirs(self):
        print("📂 目录结构 ...")
        for d in REQUIRED_DIRS:
            path = os.path.join(self.base, d)
            if os.path.isdir(path):
                self.passes.append(f"  目录存在: {d}/")
            else:
                self.errors.append(f"  缺少目录: {d}/")

    def _check_readmes(self):
        print("📝 README 文件 ...")
        for f in REQUIRED_README:
            path = os.path.join(self.base, f)
            if os.path.isfile(path):
                size = os.path.getsize(path)
                if size < 50:
                    self.warnings.append(f"  {f} 内容过少 ({size} bytes)，可能未填写")
                else:
                    self.passes.append(f"  README 正常: {f}")
            else:
                self.errors.append(f"  缺少文件: {f}")

    def _check_gitignore(self):
        gi_path = os.path.join(self.base, ".gitignore")
        if not os.path.isfile(gi_path):
            self.errors.append("  缺少 .gitignore！建议立即创建")
            return
        with open(gi_path) as f:
            content = f.read()
        checks = [
            ("checkpoints", "**/checkpoints/"),
            ("*.pth", "*.pth"),
            ("*.safetensors", "*.safetensors"),
            (".env", ".env"),
            ("logs", "*.log"),
        ]
        for name, pattern in checks:
            if pattern not in content:
                self.warnings.append(f"  .gitignore 可能缺少 {name} 的忽略规则")

    def _check_data_sources(self):
        print("📊 数据来源 ...")
        raw_dir = os.path.join(self.base, "01_data/01_raw")
        if not os.path.isdir(raw_dir):
            self.warnings.append("  01_data/01_raw/ 目录不存在")
            return

        sources = [d for d in os.listdir(raw_dir)
                   if os.path.isdir(os.path.join(raw_dir, d)) and d.startswith("source_")]
        if not sources:
            self.warnings.append("  尚未添加任何数据来源（01_data/01_raw/ 为空）")
            return

        self.passes.append(f"  发现 {len(sources)} 个数据来源")
        for src in sorted(sources):
            meta_path = os.path.join(raw_dir, src, "metadata.yaml")
            if not os.path.isfile(meta_path):
                self.errors.append(f"  {src}/ 缺少 metadata.yaml")
                continue

            with open(meta_path) as f:
                meta = f.read()

            missing_fields = []
            for field in METADATA_REQUIRED_FIELDS:
                if f"{field}:" not in meta:
                    missing_fields.append(field)
            # 检查字段是否为空值
            for line in meta.split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip()
                    if key in METADATA_REQUIRED_FIELDS and (not val or val == ""):
                        if key not in missing_fields:
                            missing_fields.append(f"{key}(空值)")

            if missing_fields:
                self.warnings.append(
                    f"  {src}/metadata.yaml 缺少或为空: {', '.join(missing_fields)}")
            else:
                self.passes.append(f"  ✅ source_{src} metadata 完整")

    def _check_quality_log(self):
        ql_path = os.path.join(self.base, "01_data/04_quality_log.md")
        if not os.path.isfile(ql_path):
            self.warnings.append("  缺少 01_data/04_quality_log.md")
            return
        with open(ql_path) as f:
            content = f.read()
        # 检查是否有实际的质量记录（至少一行表格数据）
        table_lines = [l for l in content.split("\n") if l.startswith("|") and "---" not in l and l.count("|") >= 3]
        data_lines = [l for l in table_lines if any(c.isalpha() for c in l)]
        if len(data_lines) <= 2:  # 只有表头
            self.warnings.append("  04_quality_log.md 尚无质量记录")

    def _check_tokenizers(self):
        print("🔤 分词方案 ...")
        custom_dir = os.path.join(self.base, "02_tokenization/02_custom")
        if not os.path.isdir(custom_dir):
            return

        approaches = [d for d in os.listdir(custom_dir)
                      if os.path.isdir(os.path.join(custom_dir, d))]
        if not approaches:
            self.warnings.append("  02_tokenization/02_custom/ 中尚无分词方案")
            return

        self.passes.append(f"  发现 {len(approaches)} 个分词方案")
        for app in sorted(approaches):
            app_dir = os.path.join(custom_dir, app)
            eval_path = os.path.join(app_dir, "eval.md")

            if not os.path.isfile(eval_path):
                self.warnings.append(f"  {app}/ 缺少 eval.md")
                continue

            with open(eval_path) as f:
                eval_content = f.read()

            if len(eval_content.strip()) < 100:
                self.warnings.append(f"  {app}/eval.md 内容过少，可能未填写评估结果")
            else:
                self.passes.append(f"  ✅ {app} eval 已填写")

    def _check_models(self):
        print("🧠 模型训练 ...")
        pt_dir = os.path.join(self.base, "03_models/01_pretraining")
        if not os.path.isdir(pt_dir):
            return

        archs = [d for d in os.listdir(pt_dir)
                 if os.path.isdir(os.path.join(pt_dir, d))]
        total_runs = 0
        for arch in sorted(archs):
            arch_dir = os.path.join(pt_dir, arch)
            runs = [d for d in os.listdir(arch_dir)
                    if os.path.isdir(os.path.join(arch_dir, d))]
            total_runs += len(runs)
            for run in sorted(runs):
                run_dir = os.path.join(arch_dir, run)
                # 检查是否有日志
                logs_dir = os.path.join(run_dir, "logs")
                if os.path.isdir(logs_dir) and os.listdir(logs_dir):
                    self.passes.append(f"  ✅ {arch}/{run} 有训练日志")
                else:
                    self.warnings.append(f"  {arch}/{run} logs/ 为空，训练可能未启动或无日志")
                # 检查 eval
                eval_dir = os.path.join(run_dir, "eval")
                if os.path.isdir(eval_dir) and os.listdir(eval_dir):
                    self.passes.append(f"  ✅ {arch}/{run} 有评估结果")
                else:
                    self.warnings.append(f"  {arch}/{run} eval/ 为空")

        if total_runs > 0:
            self.passes.append(f"  共 {total_runs} 个训练运行（{len(archs)} 个架构）")
        else:
            self.info = "  尚未开始模型训练"

        # 检查后训练
        post_dir = os.path.join(self.base, "03_models/02_post_training")
        if os.path.isdir(post_dir):
            post_methods = [d for d in os.listdir(post_dir)
                            if os.path.isdir(os.path.join(post_dir, d))]
            post_runs = 0
            for m in post_methods:
                m_dir = os.path.join(post_dir, m)
                post_runs += len([d for d in os.listdir(m_dir)
                                  if os.path.isdir(os.path.join(m_dir, d))])
            if post_runs > 0:
                self.passes.append(f"  后训练: {post_runs} 个运行")

    def _check_experiment_log(self):
        log_path = os.path.join(self.base, "04_experiments/experiment_log.md")
        if not os.path.isfile(log_path):
            self.errors.append("  缺少 04_experiments/experiment_log.md")
            return
        with open(log_path) as f:
            content = f.read()

        # 检查是否有实际记录（查找日期格式）
        import re
        dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)
        if len(dates) <= 1:  # 只有模板中的日期
            self.warnings.append("  experiment_log.md 尚无实验记录（无日期条目）")
        else:
            self.passes.append(f"  experiment_log.md 有 {len(set(dates))} 条日期记录")

        # 检查最近更新
        mtime = os.path.getmtime(log_path)
        days_ago = (datetime.now() - datetime.fromtimestamp(mtime)).days
        if days_ago > 7:
            self.warnings.append(f"  experiment_log.md 已 {days_ago} 天未更新")

    def _check_config_templates(self):
        config_dir = os.path.join(self.base, "06_shared/configs/training")
        if os.path.isdir(config_dir):
            templates = os.listdir(config_dir)
            if templates:
                self.passes.append(f"  配置模板: {len(templates)} 个")
            else:
                self.warnings.append("  06_shared/configs/training/ 无配置模板")

    def _print_summary(self):
        print(f"\n{'='*60}")
        print(f"📊 检查总结")
        print(f"{'='*60}")
        print(f"  ✅ 通过: {len(self.passes)}")
        print(f"  ⚠️  警告: {len(self.warnings)}")
        print(f"  ❌ 错误: {len(self.errors)}")

        if self.errors:
            print(f"\n❌ 错误（必须修复）:")
            for e in self.errors:
                print(f"  {e}")

        if self.warnings:
            print(f"\n⚠️  警告（建议修复）:")
            for w in self.warnings:
                print(f"  {w}")

        if self.passes and (self.errors or self.warnings):
            print(f"\n✅ 通过项 (共 {len(self.passes)} 项，用 --verbose 查看)")

        score = max(0, 100 - len(self.errors) * 15 - len(self.warnings) * 5)
        grade = "🏆" if score >= 90 else ("👍" if score >= 70 else ("⚠️" if score >= 50 else "🔴"))
        print(f"\n📈 健康评分: {score}/100 {grade}")


def main():
    parser = argparse.ArgumentParser(description="AI 项目健康检查工具")
    parser.add_argument("--name", type=str, required=True, help="项目名称")
    parser.add_argument("--output", type=str, default=".", help="项目父目录")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示全部通过项")
    args = parser.parse_args()

    base = os.path.join(args.output, args.name)
    if not os.path.isdir(base):
        print(f"❌ 项目不存在: {base}")
        sys.exit(1)

    checker = HealthChecker(base, args.name)
    checker.run_all()

    if args.verbose and checker.passes:
        print(f"\n✅ 全部通过项:")
        for p in checker.passes:
            print(f"  {p}")

    sys.exit(0 if not checker.errors else 1)


if __name__ == "__main__":
    main()
