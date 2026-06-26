---
name: ai-project-scaffold
description: "为 AI 模型项目创建标准化目录结构：覆盖数据→分词→模型→实验全链路，支持多方案并行、来源追踪、质量记录。内置健康检查、追踪链、实验对比、checkpoint管理。严格文档规范防止 AI 生成冗余文档。"
---

# AI 项目目录结构管理 v2.0

适用于涉及数据清洗、分词/Tokenization、模型训练、后训练、强化学习等完整 AI 管线的项目。

## 🔴 文档铁律（AI 助手必须遵守）

> ⚠️ 这是本 skill 最重要的部分。违反任何一条都应被视为严重错误。

### 原则

1. **表 > 文** — 能用表格记录的，不写段落。表格可扫描、可对比、不冗余。
2. **记录决策，不写教程** — 文档回答"做了什么选择、为什么"，不写"怎么用、是什么"。
3. **一处一真理** — 同一信息绝不出现在两个文件里。信息有且仅有一个权威位置。
4. **日志即文档** — `experiment_log.md` 是唯一持续增长的文档。其他 README 只在结构变化时更新。
5. **写完删一半** — 写完任何文档后，删掉至少一半字数。留下的才是精华。

### 禁止清单

| ❌ 绝对禁止 | ✅ 应该做 |
|-------------|----------|
| 写超过 200 字的段落说明 | 用表格或列表，每行 ≤ 一行 |
| 在 README 里粘贴代码 | 代码放在 scripts/，README 只写脚本名+用途 |
| 创建 `GUIDE.md`、`TUTORIAL.md`、`NOTES.md` 等随意命名的文档 | 只使用约定文件名 |
| 重复其他文件已有的信息 | 用链接引用（如 `详见 01_data/README.md`） |
| 自动生成"项目概述""背景介绍"等水字数的章节 | 空着也比写废话强 |
| 写 `detailed_explanation_v2_final.md` | 一个主题一个文件，版本在文件名里（如 `token_eval_v2.md`） |
| 用 `final`、`new`、`latest` 等模糊后缀 | 用数字版本号 v1, v2, v3 |

### 文档命名规范

```
✅ 好命名:
  architecture_decision_001_transformer.md  # ADR 风格
  qc_report_wikipedia_zh_2024-03-15.md      # 数据集_日期
  eval_benchmark_mmlu_v2.md                 # 主题_版本

❌ 坏命名:
  notes.md                                  # 太模糊
  final_report.md                           # 哪个 final？
  test.md                                   # 测什么？
  new_doc_v3_final_revised.md               # 💀
```

### 允许的文档类型及字数上限

| 文档 | 最大字数 | 更新频率 | 说明 |
|------|---------|---------|------|
| 各层 `README.md` | 300 字 | 结构变化时 | 表格为主，不写段落 |
| `experiment_log.md` | 不限（按条目追加） | 每次实验 | 唯一允许持续增长的文件 |
| `metadata.yaml` | 不限 | 数据源变更时 | 结构化数据，不是散文 |
| `eval.md`（分词方案下） | 500 字 | 评估完成后 | 表格 + 关键数字 |
| `architecture_decision_*.md` | 500 字 | 做决策时 | 背景+选项+决策+后果 |
| `qc_report_*.md` | 300 字 | 每次 QC | 数据集+问题+处理+结果 |
| `meeting_*.md` | 200 字 | 每次会议 | 日期+议题+结论，不要流水账 |

超过字数上限的文档应拆分为多个文件，或用表格代替段落。

---

## 设计理念

1. **分层管理** — 数据层 / 分词层 / 模型层 各自独立，互不污染
2. **多方案并行** — 每层支持多种技术方案/尝试并存，各自有独立空间
3. **来源可追溯** — 数据从哪来、经过什么处理、用到了哪个模型，全程可追踪
4. **质量可见** — 数据质量、分词效果、模型评估都有独立的记录空间
5. **文档极简** — 遵循上方🔴铁律，拒绝 AI 生成冗余文档

---

## 目录结构

```
<project_name>/
├── README.md                          # 项目总览（≤300字）
├── _project_config.yaml               # 项目元信息
├── .gitignore                         # 自动生成，忽略 checkpoints/logs/数据/.env
├── scripts/                           # 管理脚本（自动复制）
│   ├── check_project.py               # 健康检查
│   ├── trace.py                       # 追踪链生成
│   ├── compare_runs.py                # 实验对比
│   └── checkpoint_mgmt.py             # Checkpoint 管理
│
├── 01_data/                           # 📊 数据层
│   ├── README.md                      # 数据来源登记表（表格，≤300字）
│   ├── 01_raw/                        # 原始数据（按来源分目录）
│   │   └── source_<name>/
│   │       ├── metadata.yaml          # 结构化元信息
│   │       └── data/
│   ├── 02_qc/                         # 质量控制
│   │   ├── scripts/                   # QC 脚本
│   │   ├── reports/                   # QC 报告（命名: qc_report_<dataset>_YYYY-MM-DD.md）
│   │   └── cleaned/                   # 清洗后数据
│   ├── 03_processed/                  # 处理后
│   │   ├── text/
│   │   ├── image/
│   │   ├── audio/
│   │   └── multimodal/                # 多模态细化
│   │       ├── image_text/
│   │       ├── video_text/
│   │       ├── audio_text/
│   │       └── interleaved/
│   └── 04_quality_log.md              # 数据质量追踪日志（表格追加）
│
├── 02_tokenization/                   # 🔤 分词层
│   ├── README.md                      # 分词策略总览（表格，≤300字）
│   ├── 01_existing/                   # 现成 tokenizer
│   │   └── <tokenizer_name>/
│   │       ├── config.yaml
│   │       └── notes.md               # 选用理由（≤150字）
│   ├── 02_custom/                     # 自制
│   │   └── <approach_name>/
│   │       ├── README.md              # 方案说明（≤200字）
│   │       ├── scripts/
│   │       ├── configs/
│   │       ├── vocab_output/
│   │       └── eval.md                # 评估结果（表格，≤500字）
│   ├── 03_training/                   # token 相关训练
│   ├── 04_evaluation/                 # 内在 + 下游评估
│   │   ├── intrinsic/
│   │   └── extrinsic/
│   └── 05_generated/                  # 分词产生的新数据记录
│
├── 03_models/                         # 🧠 模型层
│   ├── README.md                      # 架构选型决策（表格，≤300字）
│   ├── 01_pretraining/
│   │   └── <arch_name>/<run_name>/
│   │       ├── configs/               # 训练配置
│   │       ├── scripts/               # 训练脚本
│   │       ├── checkpoints/           # gitignored
│   │       ├── logs/                  # gitignored
│   │       └── eval/
│   ├── 02_post_training/
│   │   ├── sft/                       # 监督微调
│   │   ├── dpo/                       # DPO
│   │   ├── orpo/                      # ORPO
│   │   ├── kto/                       # KTO
│   │   ├── simpo/                     # SimPO
│   │   └── rlhf/                      # RLHF 流程
│   ├── 03_rl/
│   │   ├── ppo/
│   │   ├── grpo/
│   │   └── reward_models/
│   ├── 04_evaluation/
│   │   ├── benchmarks/
│   │   └── reports/
│   └── 05_deployment/
│
├── 04_experiments/                    # 🔬 实验管理
│   ├── experiment_log.md              # 时间线日志（唯一可无限增长的文件）
│   └── runs/
│
├── 05_docs/                           # 📚 文档（严格遵守铁律）
│   ├── design/                        # 架构决策记录（ADR 风格）
│   ├── meetings/                      # 会议记录（命名: meeting_YYYY-MM-DD_主题.md）
│   └── references/                    # 外部参考文献
│
└── 06_shared/                         # 🔧 共享资源
    ├── scripts/                       # 通用脚本
    └── configs/
        ├── training/                  # DeepSpeed/LoRA/QLoRA/WandB 模板
        ├── data/                      # 数据处理配置模板
        └── deployment/                # 部署配置模板
```

---

## 🛠 管理工具

### 新建项目

```bash
python3 init_ai_project.py --name "MyLLM" [--output /path/to/parent]
```
自动生成：完整目录 + 各层 README 模板 + `.gitignore` + 5 个配置模板 + 管理脚本副本

### 添加组件

```bash
# 数据来源（自动生成 metadata.yaml）
--add-source --source <名称>

# 分词方案（自动创建 scripts/configs/vocab/eval）
--add-tokenizer --approach <方案名>

# 预训练运行
--add-training --arch <架构> --run <运行名>

# 后训练运行
--add-posttrain --method <sft/dpo/orpo/kto/simpo/rlhf> --run <运行名>

# RL 运行
--add-rl --method <ppo/grpo/...> --run <运行名>
```

### 升级已有项目

```bash
python3 init_ai_project.py --name "MyLLM" --upgrade
# 补充缺失目录 + .gitignore + 配置模板 + 管理脚本
```

### 健康检查

```bash
python3 check_project.py --name "MyLLM"
# 扫描: 目录完整度 / metadata 字段 / eval 是否填写 / 日志是否更新
# 输出: 健康评分 0-100 + 具体问题清单
```

### 追踪链

```bash
python3 trace.py --name "MyLLM"                    # 全局追踪
python3 trace.py --name "MyLLM" --layer models      # 只看模型层
python3 trace.py --name "MyLLM" --full              # 含文件详情
```

### 实验对比

```bash
python3 compare_runs.py --name "MyLLM"                          # 全部对比
python3 compare_runs.py --name "MyLLM" --arch llama3             # 指定架构
python3 compare_runs.py --name "MyLLM" --stage post_training     # 只看后训练
```

### Checkpoint 管理

```bash
python3 checkpoint_mgmt.py --name "MyLLM" list                      # 列出所有
python3 checkpoint_mgmt.py --name "MyLLM" clean --keep 3 --dry-run  # 预览清理
python3 checkpoint_mgmt.py --name "MyLLM" clean --keep 3            # 每运行保留3个最新
python3 checkpoint_mgmt.py --name "MyLLM" archive --to /backup/     # 归档
python3 checkpoint_mgmt.py --name "MyLLM" stats                     # 磁盘统计
```

---

## 命名规范

| 层级 | 目录命名 | 示例 |
|------|---------|------|
| 数据来源 | `source_<描述>` | `source_wikipedia_zh`, `source_internal_docs` |
| QC 报告 | `qc_report_<dataset>_YYYY-MM-DD.md` | `qc_report_wikipedia_2024-03-15.md` |
| 分词方案 | `<方法>_v<版本>` | `bpe_v1`, `unigram_v2`, `sentencepiece_v1` |
| 模型架构 | `<架构名>` | `llama3`, `qwen2`, `custom_moe` |
| 训练运行 | `<描述>_v<版本>` | `baseline_v1`, `lr_3e4_v2`, `wd_0.1_v1` |
| 后训练方法 | `<缩写>` | `sft`, `dpo`, `ppo`, `grpo` |
| 会议记录 | `meeting_YYYY-MM-DD_<主题>.md` | `meeting_2024-03-15_arch_review.md` |
| 设计决策 | `architecture_decision_<序号>_<主题>.md` | `architecture_decision_001_transformer.md` |

---

## 追踪链

每个阶段记录输入/输出依赖，形成完整链路：

```
source_wikipedia_zh (01_data/01_raw/)
  → qc_report_wikipedia_2024-03-15.md (01_data/02_qc/reports/)
    → bpe_v1 (02_tokenization/02_custom/)
      → eval.md 评估通过
        → llama3/baseline_v1 (03_models/01_pretraining/)
          → sft/chat_v1 (03_models/02_post_training/)
            → ppo/reward_v2 (03_models/03_rl/)
```

> 💡 运行 `python3 scripts/trace.py --name <项目>` 自动生成追踪链。

---

## AI 助手行为准则

使用本 skill 时，AI 助手必须:

1. **初始化项目时** — 只生成模板骨架，不填充假数据。空表格比假数据好。
2. **写 README 时** — 表格 > 列表 > 段落。默认用表格。
3. **记录实验时** — 追加到 `experiment_log.md`，用模板格式，不要新建文件。
4. **写评估报告时** — 数字和表格是主角，文字只是表头。
5. **不要做的事**:
   - ❌ 不要创建 `05_docs/` 下的随意命名的 `.md` 文件
   - ❌ 不要在多个 README 里重复同一段话
   - ❌ 不要写"本项目旨在..."这种水字数开头
   - ❌ 不要生成超过 300 字的 README
   - ❌ 不要用 `final`、`new`、`latest`、`updated` 命名文件
