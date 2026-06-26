#!/usr/bin/env python3
"""
AI 项目目录结构初始化脚本 v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
功能:
  - 新建项目（完整目录结构 + README 模板 + .gitignore + 配置模板）
  - 添加数据来源 / 分词方案 / 训练运行
  - 添加后训练 / RL 实验

用法:
  python3 init_ai_project.py --name MyProject
  python3 init_ai_project.py --name MyProject --add-source --source wikipedia_zh
  python3 init_ai_project.py --name MyProject --add-tokenizer --approach bpe_v2
  python3 init_ai_project.py --name MyProject --add-training --arch llama3 --run baseline_v1
  python3 init_ai_project.py --name MyProject --add-posttrain --method sft --run chat_v1
  python3 init_ai_project.py --name MyProject --add-rl --method ppo --run reward_v1
"""

import argparse
import os
import sys
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# 目录结构定义
# ═══════════════════════════════════════════════════════════════

DIRS = [
    # ── 01_data ──
    "01_data/01_raw",
    "01_data/02_qc/scripts",
    "01_data/02_qc/reports",
    "01_data/02_qc/cleaned",
    "01_data/03_processed/text",
    "01_data/03_processed/image",
    "01_data/03_processed/audio",
    # 多模态细化
    "01_data/03_processed/multimodal/image_text",
    "01_data/03_processed/multimodal/video_text",
    "01_data/03_processed/multimodal/audio_text",
    "01_data/03_processed/multimodal/interleaved",
    # ── 02_tokenization ──
    "02_tokenization/01_existing",
    "02_tokenization/02_custom",
    "02_tokenization/03_training",
    "02_tokenization/04_evaluation/intrinsic",
    "02_tokenization/04_evaluation/extrinsic",
    "02_tokenization/05_generated",
    # ── 03_models ──
    "03_models/01_pretraining",
    "03_models/02_post_training/sft",
    "03_models/02_post_training/dpo",
    "03_models/02_post_training/orpo",
    "03_models/02_post_training/kto",
    "03_models/02_post_training/simpo",
    "03_models/02_post_training/rlhf",
    "03_models/03_rl/ppo",
    "03_models/03_rl/grpo",
    "03_models/03_rl/reward_models",
    "03_models/04_evaluation/benchmarks",
    "03_models/04_evaluation/reports",
    "03_models/05_deployment",
    # ── 04_experiments ──
    "04_experiments/runs",
    # ── 05_docs ──
    "05_docs/design",
    "05_docs/meetings",
    "05_docs/references",
    # ── 06_shared ──
    "06_shared/scripts",
    "06_shared/configs/training",
    "06_shared/configs/data",
    "06_shared/configs/deployment",
]

# ═══════════════════════════════════════════════════════════════
# .gitignore 模板
# ═══════════════════════════════════════════════════════════════

GITIGNORE = """# ═══════════════════════════════════════════════
# AI 项目 .gitignore（自动生成 by ai-project-scaffold）
# ═══════════════════════════════════════════════

# ── Python ──
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
*.egg

# ── 模型文件（太大不进 git） ──
*.pth
*.pt
*.safetensors
*.bin
*.ckpt
*.h5
*.pb
*.onnx
**/checkpoints/
!**/checkpoints/.gitkeep

# ── 原始数据（太大 + 可能有版权问题） ──
01_data/01_raw/
!01_data/01_raw/**/metadata.yaml

# ── 日志 ──
*.log
**/logs/
!**/logs/.gitkeep

# ── 环境 & 密钥 ──
.env
.env.*
*.key
*.pem
secrets.yaml
credentials.json

# ── IDE ──
.vscode/
.idea/
*.swp
*.swo
*~

# ── OS ──
.DS_Store
Thumbs.db

# ── 临时文件 ──
tmp/
temp/
*.tmp
*.temp
.cache/

# ── 输出产物 ──
wandb/
outputs/
lightning_logs/
mlruns/
"""

# ═══════════════════════════════════════════════════════════════
# README 模板
# ═══════════════════════════════════════════════════════════════

README_ROOT = """# {project_name}

> 📅 创建时间: {date}
> 🛠 自动生成 by ai-project-scaffold v2.0

## 项目目标

<!-- 简要描述项目目标 -->

## 目录导航

| 目录 | 用途 |
|------|------|
| [01_data/](01_data/) | 📊 数据层：原始数据、质控、处理 |
| [02_tokenization/](02_tokenization/) | 🔤 分词层：tokenizer 选型与制作 |
| [03_models/](03_models/) | 🧠 模型层：预训练、后训练、RL |
| [04_experiments/](04_experiments/) | 🔬 实验管理 |
| [05_docs/](05_docs/) | 📚 文档与参考文献 |
| [06_shared/](06_shared/) | 🔧 共享脚本与配置 |

## 快速开始

```bash
# 检查项目健康状态
python3 scripts/check_project.py --name {project_name}

# 查看追踪链
python3 scripts/trace.py --name {project_name}

# 对比实验
python3 scripts/compare_runs.py --name {project_name}
```
"""

README_DATA = """# 📊 数据层

## 数据来源登记表

| 来源 | 类型 | 规模 | 获取方式 | 获取日期 | License | 质量评级 | 备注 |
|------|------|------|----------|----------|---------|----------|------|
|      |      |      |          |          |         |          |      |

## 数据流向

记录数据从原始 → QC → 处理 → 使用的完整链路。

> 💡 运行 `python3 scripts/trace.py --name <项目>` 自动生成追踪链。
"""

README_TOKEN = """# 🔤 分词层

## 分词策略决策

| 方案 | 类型 | 词表大小 | 训练语料 | 压缩率 | 下游任务 | 选用理由 |
|------|------|----------|----------|--------|----------|----------|
|      |      |          |          |        |          |          |

## 分词 → 模型 追踪

记录每个分词方案被哪些模型使用。

> 💡 运行 `python3 scripts/trace.py --name <项目> --layer tokenization` 查看分词追踪。
"""

README_MODEL = """# 🧠 模型层

## 架构选型决策

| 架构 | 参数量 | 选型理由 | 对比方案 | 决策日期 |
|------|--------|----------|----------|----------|
|      |        |          |          |          |

## 训练历史

| 运行 | 架构 | 数据 | Token | 状态 | Loss | 备注 |
|------|------|------|-------|------|------|------|
|      |      |      |       |      |      |      |

> 💡 运行 `python3 scripts/compare_runs.py --name <项目>` 自动对比实验。
"""

README_EXPERIMENT = """# 🔬 实验日志

## 实验时间线

按时间顺序记录每次实验：目的、配置、结果、结论。

---

### 模板

### YYYY-MM-DD: <实验名称>

- **目的:** 
- **涉及模块:** (数据/分词/预训练/后训练/RL)
- **关键配置:**
  - 
- **结果:**
  - 
- **结论/下一步:**
  - 

---

> 💡 运行 `python3 scripts/check_project.py --name <项目>` 检查是否有遗漏的实验记录。
"""

README_GENERATED_DATA = """# 🔄 分词过程中产生的新数据

记录分词/训练过程中自动生成的数据：
- 数据增强产物
- 重新采样数据
- 合成数据
- token 训练衍生物

| 来源实验 | 数据类型 | 规模 | 存放位置 | 用途 |
|----------|----------|------|----------|------|
|          |          |      |          |      |
"""

README_SHARED = """# 🔧 共享资源

跨模块通用的脚本和配置。

## scripts/
- 数据处理通用工具
- 评估指标计算
- 可视化工具

## configs/
- **training/** — DeepSpeed、LoRA、QLoRA 等训练配置模板
- **data/** — 数据加载、预处理配置模板
- **deployment/** — 模型部署配置模板

> 💡 初始化项目时会自动预置常用配置模板。
"""

QUALITY_LOG = """# 📋 数据质量追踪日志

> 持续更新，记录所有数据集的质量评估结果。

---

## 质量评级标准

| 评级 | 说明 |
|------|------|
| A | 高质量，可直接用于训练 |
| B | 需要轻度清洗 |
| C | 需要大量清洗，可能有噪音 |
| D | 质量差，仅作参考 |
| F | 不可用 |

## 质量记录

| 日期 | 数据集 | 评级 | 问题描述 | 处理方式 | 负责人 | QC 脚本 |
|------|--------|------|----------|----------|--------|---------|
|      |        |      |          |          |        |         |
"""

METADATA_TEMPLATE = """# 数据来源元信息

source_name: {source_name}
source_type:  # web_crawl / internal_db / public_dataset / api / manual
url: 
access_date: {date}
license: 
language: 
size:
  files: 
  tokens_estimate: 
format:  # jsonl / parquet / csv / txt / binary
description: >
  
quality_notes: >
  
contact: 
"""

PROJECT_CONFIG = """# ══════════════════════════════════
# 项目配置
# ══════════════════════════════════

project:
  name: {project_name}
  created: {date}
  description: >
    
  members: []
  repo: 

data:
  primary_language: 
  modalities: []  # text, image, audio, multimodal
  total_tokens_estimate: 

model:
  target_size: 
  architecture_candidates: []
  
training:
  framework:  # pytorch / jax / mindspore
  parallel_strategy:  # deepspeed_zero2 / zero3 / fsdp / ddp
  hardware:  # GPU型号和数量
  
goals:
  - 
"""

# ═══════════════════════════════════════════════════════════════
# 配置模板
# ═══════════════════════════════════════════════════════════════

DEEPSPEED_ZERO2 = """# DeepSpeed ZeRO-2 配置模板
# 适用: 中等规模模型，显存优化 + 梯度分片

{
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "zero_optimization": {
    "stage": 2,
    "offload_optimizer": {
      "device": "none"
    },
    "allgather_partitions": true,
    "allgather_bucket_size": 2e8,
    "reduce_scatter": true,
    "reduce_bucket_size": 2e8,
    "overlap_comm": true,
    "contiguous_gradients": true
  },
  "fp16": {
    "enabled": false
  },
  "bf16": {
    "enabled": true
  },
  "gradient_clipping": 1.0,
  "wall_clock_breakdown": false
}
"""

DEEPSPEED_ZERO3 = """# DeepSpeed ZeRO-3 配置模板
# 适用: 超大模型，参数 + 梯度 + 优化器全分片

{
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "offload_param": {
      "device": "cpu",
      "pin_memory": true
    },
    "overlap_comm": true,
    "contiguous_gradients": true,
    "sub_group_size": 1e9,
    "reduce_bucket_size": "auto",
    "stage3_prefetch_bucket_size": "auto",
    "stage3_param_persistence_threshold": "auto",
    "stage3_max_live_parameters": 1e9,
    "stage3_max_reuse_distance": 1e9,
    "stage3_gather_16bit_weights_on_model_save": true
  },
  "bf16": {
    "enabled": true
  },
  "gradient_clipping": 1.0,
  "wall_clock_breakdown": false
}
"""

LORA_CONFIG = """# LoRA (Low-Rank Adaptation) 配置模板
# 适用: 参数高效微调，冻结原模型，只训练低秩适配器

{
  "peft_type": "LORA",
  "r": 16,
  "lora_alpha": 32,
  "lora_dropout": 0.05,
  "target_modules": [
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj"
  ],
  "bias": "none",
  "task_type": "CAUSAL_LM"
}
"""

QLORA_CONFIG = """# QLoRA (Quantized LoRA) 配置模板
# 适用: 4-bit 量化 + LoRA，极低显存微调大模型

{
  "load_in_4bit": true,
  "bnb_4bit_compute_dtype": "bfloat16",
  "bnb_4bit_quant_type": "nf4",
  "bnb_4bit_use_double_quant": true,
  "peft_type": "LORA",
  "r": 16,
  "lora_alpha": 32,
  "lora_dropout": 0.05,
  "target_modules": [
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj"
  ],
  "bias": "none",
  "task_type": "CAUSAL_LM"
}
"""

WANDB_CONFIG = """# Weights & Biases 配置模板

wandb:
  project: "{project_name}"
  entity: ""
  mode: "online"  # online / offline / disabled
  tags: []
  notes: ""
  log_model: false
  settings:
    _disable_stats: false
"""

CONFIG_README = """# 配置模板

此目录包含常用训练/数据/部署配置模板。

## 使用方法

1. 复制需要的模板到对应实验目录
2. 修改其中的占位符（如 `{project_name}`）
3. 在启动脚本中引用

## 模板清单

### training/
| 模板 | 适用场景 |
|------|----------|
| `deepspeed_zero2.yaml` | 中等模型，ZeRO-2 优化 |
| `deepspeed_zero3.yaml` | 大模型，ZeRO-3 全分片 |
| `lora_config.yaml` | 参数高效微调 |
| `qlora_config.yaml` | 4-bit 量化微调 |
| `wandb_config.yaml` | 实验追踪配置 |
"""

# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

def create_dirs(base_path: str):
    for d in DIRS:
        os.makedirs(os.path.join(base_path, d), exist_ok=True)
    return base_path


def write_file(path: str, content: str):
    if os.path.exists(path):
        print(f"  ⏭  跳过（已存在）: {path}")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ 创建: {path}")


def force_write(path: str, content: str):
    """覆盖写入（用于配置模板等需要更新的文件）"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def init_project(project_name: str, output_dir: str = "."):
    """初始化完整的 AI 项目目录结构"""
    base = os.path.join(output_dir, project_name)
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"\n{'='*60}")
    print(f"🚀 初始化 AI 项目: {project_name}")
    print(f"📁 目标路径: {os.path.abspath(base)}")
    print(f"{'='*60}\n")

    # 1. 创建目录
    print("📂 创建目录结构...")
    create_dirs(base)

    # 2. README 模板
    print("\n📝 生成 README 模板...")
    readmes = {
        "README.md": README_ROOT.format(project_name=project_name, date=today),
        "01_data/README.md": README_DATA,
        "02_tokenization/README.md": README_TOKEN,
        "03_models/README.md": README_MODEL,
        "04_experiments/experiment_log.md": README_EXPERIMENT,
        "02_tokenization/05_generated/README.md": README_GENERATED_DATA,
        "06_shared/README.md": README_SHARED,
        "01_data/04_quality_log.md": QUALITY_LOG,
        "_project_config.yaml": PROJECT_CONFIG.format(project_name=project_name, date=today),
    }
    for rel_path, content in readmes.items():
        write_file(os.path.join(base, rel_path), content)

    # 3. .gitignore
    print("\n🔒 生成 .gitignore...")
    write_file(os.path.join(base, ".gitignore"), GITIGNORE)

    # 4. 配置模板
    print("\n⚙️  预置配置模板...")
    config_dir = os.path.join(base, "06_shared/configs")
    configs = {
        "README.md": CONFIG_README,
        "training/deepspeed_zero2.yaml": DEEPSPEED_ZERO2,
        "training/deepspeed_zero3.yaml": DEEPSPEED_ZERO3,
        "training/lora_config.yaml": LORA_CONFIG,
        "training/qlora_config.yaml": QLORA_CONFIG,
        "training/wandb_config.yaml": WANDB_CONFIG.format(project_name=project_name),
    }
    for rel_path, content in configs.items():
        force_write(os.path.join(config_dir, rel_path), content)
    print(f"  ✅ 预置 5 个配置模板到 06_shared/configs/")

    # 5. 复制管理脚本到项目
    print("\n🔧 复制管理脚本...")
    skill_scripts = os.path.dirname(os.path.abspath(__file__))
    mgmt_scripts = [
        "check_project.py",
        "trace.py",
        "compare_runs.py",
        "checkpoint_mgmt.py",
        "doc_lint.py",
    ]
    target_scripts_dir = os.path.join(base, "scripts")
    os.makedirs(target_scripts_dir, exist_ok=True)
    for script in mgmt_scripts:
        src = os.path.join(skill_scripts, script)
        if os.path.exists(src):
            import shutil
            shutil.copy2(src, os.path.join(target_scripts_dir, script))
            print(f"  ✅ 复制: scripts/{script}")
    if not mgmt_scripts or not any(os.path.exists(os.path.join(skill_scripts, s)) for s in mgmt_scripts):
        print(f"  ⚠️  管理脚本尚未就绪，稍后可用 --upgrade 补充")

    print(f"\n{'='*60}")
    print(f"✅ 项目初始化完成！")
    print(f"📁 {os.path.abspath(base)}")
    print(f"\n📋 已生成:")
    print(f"   • 30+ 目录      完整的三层管线结构")
    print(f"   • 9 个 README   各层级入口文档")
    print(f"   • .gitignore    自动忽略大文件/密钥/日志")
    print(f"   • 5 个配置模板   DeepSpeed/LoRA/QLoRA/WandB")
    print(f"\n💡 下一步:")
    print(f"   cd {os.path.abspath(base)}")
    print(f"   python3 scripts/check_project.py --name {project_name}  # 健康检查")
    print(f"   python3 scripts/trace.py --name {project_name}         # 追踪链")
    print(f"   编辑 01_data/README.md 登记数据来源")


def add_source(project_name: str, source_name: str, output_dir: str = "."):
    base = os.path.join(output_dir, project_name)
    source_dir = os.path.join(base, "01_data/01_raw", f"source_{source_name}")
    os.makedirs(os.path.join(source_dir, "data"), exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    meta = METADATA_TEMPLATE.format(source_name=source_name, date=today)
    write_file(os.path.join(source_dir, "metadata.yaml"), meta)
    print(f"✅ 数据来源已添加: source_{source_name}")


def add_tokenizer(project_name: str, approach: str, output_dir: str = "."):
    base = os.path.join(output_dir, project_name)
    approach_dir = os.path.join(base, "02_tokenization/02_custom", approach)
    for sd in ["scripts", "configs", "vocab_output"]:
        os.makedirs(os.path.join(approach_dir, sd), exist_ok=True)
    eval_md = f"# {approach} 评估\n\n## 内在评估\n\n| 指标 | 值 |\n|------|----|\n| 压缩率 |  |\n| 覆盖率 |  |\n| 词表大小 |  |\n\n## 下游评估\n\n| 下游任务 | 指标 | 值 |\n|----------|------|----|\n|          |      |    |\n"
    write_file(os.path.join(approach_dir, "eval.md"), eval_md)
    write_file(os.path.join(approach_dir, "README.md"),
               f"# {approach}\n\n## 方案说明\n\n## 技术细节\n\n## 决策记录\n")
    print(f"✅ 分词方案已添加: {approach}")


def add_training(project_name: str, arch: str, run_name: str, output_dir: str = "."):
    base = os.path.join(output_dir, project_name)
    run_dir = os.path.join(base, "03_models/01_pretraining", arch, run_name)
    for sd in ["configs", "scripts", "checkpoints", "logs", "eval"]:
        os.makedirs(os.path.join(run_dir, sd), exist_ok=True)
    print(f"✅ 预训练运行已添加: {arch}/{run_name}")


def add_posttrain(project_name: str, method: str, run_name: str, output_dir: str = "."):
    base = os.path.join(output_dir, project_name)
    run_dir = os.path.join(base, "03_models/02_post_training", method, run_name)
    for sd in ["data", "configs", "scripts", "checkpoints", "eval"]:
        os.makedirs(os.path.join(run_dir, sd), exist_ok=True)
    print(f"✅ 后训练运行已添加: {method}/{run_name}")


def add_rl(project_name: str, method: str, run_name: str, output_dir: str = "."):
    base = os.path.join(output_dir, project_name)
    run_dir = os.path.join(base, "03_models/03_rl", method, run_name)
    for sd in ["configs", "scripts", "checkpoints", "logs", "eval"]:
        os.makedirs(os.path.join(run_dir, sd), exist_ok=True)
    print(f"✅ RL 运行已添加: {method}/{run_name}")


def upgrade_project(project_name: str, output_dir: str = "."):
    """升级已有项目：补充 .gitignore、配置模板、管理脚本"""
    base = os.path.join(output_dir, project_name)
    if not os.path.isdir(base):
        print(f"❌ 项目不存在: {base}")
        sys.exit(1)

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n🔧 升级项目: {project_name}")

    # 补充缺失目录
    print("📂 补充目录...")
    create_dirs(base)

    # .gitignore
    gi_path = os.path.join(base, ".gitignore")
    if not os.path.exists(gi_path):
        print("🔒 生成 .gitignore...")
        write_file(gi_path, GITIGNORE)

    # 配置模板
    config_dir = os.path.join(base, "06_shared/configs")
    configs = {
        "README.md": CONFIG_README,
        "training/deepspeed_zero2.yaml": DEEPSPEED_ZERO2,
        "training/deepspeed_zero3.yaml": DEEPSPEED_ZERO3,
        "training/lora_config.yaml": LORA_CONFIG,
        "training/qlora_config.yaml": QLORA_CONFIG,
        "training/wandb_config.yaml": WANDB_CONFIG.format(project_name=project_name),
    }
    for rel_path, content in configs.items():
        write_file(os.path.join(config_dir, rel_path), content)

    # 管理脚本
    skill_scripts = os.path.dirname(os.path.abspath(__file__))
    mgmt_scripts = ["check_project.py", "trace.py", "compare_runs.py", "checkpoint_mgmt.py", "doc_lint.py"]
    target_scripts_dir = os.path.join(base, "scripts")
    os.makedirs(target_scripts_dir, exist_ok=True)
    for script in mgmt_scripts:
        src = os.path.join(skill_scripts, script)
        if os.path.exists(src):
            import shutil
            shutil.copy2(src, os.path.join(target_scripts_dir, script))
            print(f"  ✅ 更新: scripts/{script}")

    print(f"✅ 项目升级完成！")


def main():
    parser = argparse.ArgumentParser(
        description="AI 项目目录结构管理工具 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  init_ai_project.py --name MyLLM                     # 新建项目
  init_ai_project.py --name MyLLM --upgrade            # 升级已有项目
  init_ai_project.py --name MyLLM --add-source --source wiki
  init_ai_project.py --name MyLLM --add-tokenizer --approach bpe_v2
  init_ai_project.py --name MyLLM --add-training --arch llama3 --run v1
  init_ai_project.py --name MyLLM --add-posttrain --method sft --run chat_v1
  init_ai_project.py --name MyLLM --add-rl --method ppo --run reward_v1
        """)

    parser.add_argument("--name", type=str, help="项目名称")
    parser.add_argument("--output", type=str, default=".", help="输出父目录（默认当前目录）")
    parser.add_argument("--upgrade", action="store_true", help="升级已有项目（补充配置和管理脚本）")

    # 子命令
    parser.add_argument("--add-source", action="store_true", help="添加数据来源")
    parser.add_argument("--source", type=str, help="来源名称")
    parser.add_argument("--add-tokenizer", action="store_true", help="添加分词方案")
    parser.add_argument("--approach", type=str, help="分词方案名")
    parser.add_argument("--add-training", action="store_true", help="添加预训练运行")
    parser.add_argument("--arch", type=str, help="模型架构")
    parser.add_argument("--run", type=str, help="运行名称")
    parser.add_argument("--add-posttrain", action="store_true", help="添加后训练运行")
    parser.add_argument("--method", type=str, help="后训练方法 (sft/dpo/orpo/kto/simpo/rlhf)")
    parser.add_argument("--add-rl", action="store_true", help="添加 RL 运行")
    # --method 和 --run 共用

    args = parser.parse_args()

    if not args.name:
        parser.error("必须指定 --name")

    if args.upgrade:
        upgrade_project(args.name, args.output)
    elif args.add_source:
        if not args.source:
            parser.error("--add-source 需要 --source <名称>")
        add_source(args.name, args.source, args.output)
    elif args.add_tokenizer:
        if not args.approach:
            parser.error("--add-tokenizer 需要 --approach <方案名>")
        add_tokenizer(args.name, args.approach, args.output)
    elif args.add_training:
        if not args.arch or not args.run:
            parser.error("--add-training 需要 --arch <架构> --run <运行名>")
        add_training(args.name, args.arch, args.run, args.output)
    elif args.add_posttrain:
        if not args.method or not args.run:
            parser.error("--add-posttrain 需要 --method <方法> --run <运行名>")
        add_posttrain(args.name, args.method, args.run, args.output)
    elif args.add_rl:
        if not args.method or not args.run:
            parser.error("--add-rl 需要 --method <方法> --run <运行名>")
        add_rl(args.name, args.method, args.run, args.output)
    else:
        init_project(args.name, args.output)


if __name__ == "__main__":
    main()
