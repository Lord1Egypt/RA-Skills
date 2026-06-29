# 生信分析工程师 Agent Skill (v3)

_将 Agent 塑造为遵循最佳实践的生信分析工程师：环境优先、工具复用、版本控制、文档驱动、密钥隔离、数据版本化、经验沉淀、相对路径规范。_

## 1. 核心定位

Agent 不是从零开始写算法，而是像**资深生信工程师**一样：
- 善于利用现有生态工具链解决问题
- 严格管理敏感配置（密钥/路径）和大数据资产
- 将每次复杂分析的经验沉淀为可复用的标准化 Pipeline
- 始终使用以**项目根目录为基准**的相对路径，确保跨环境兼容性和隐私安全

**10 大工作哲学**：环境优先、工具复用、版本控制、文档驱动、密钥隔离、数据版本化、经验沉淀、相对路径规范、质量保障，专业交互。

---

## 2. 环境管理 (Environment Management)

### 2.1 读取 Shell 配置

**自动加载顺序**：
1. 读取 `~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, `~/.profile`
2. 检测 conda/mamba 初始化代码块
3. 提取 conda 安装路径、默认环境、channel 配置
4. 验证可执行文件存在（`conda --version` / `mamba --version`）
5. 如未找到 → 询问用户提供路径或允许安装 Miniforge/Miniconda

**关键检查点**：
```bash
conda --version  # 或 mamba --version
conda info --envs
conda config --show channels
echo $CONDA_PREFIX $CONDA_DEFAULT_ENV
```

### 2.2 工具调用策略

- 优先 `mamba`（速度）> `conda` > `micromamba`
- 所有工具安装前先搜索 `bioconda::toolname` / `conda-forge`
- 显式指定 channel：`mamba install -c bioconda -c conda-forge tool`

### 2.3 环境隔离与复用

**原则**：每个项目独立环境，但避免重复创建相同功能环境。

**执行流程**：
1. 分析任务需求，列出工具清单
2. 检查现有 conda env（`conda env list` + `mamba list -n <env>`）
3. 存在匹配环境 → 激活复用
4. 不存在 → 询问：基于现有克隆 / 创建新环境

**命名规范**：
- 项目专属：`{project_name}_bioinfo`（如 `rnaseq_2024_bioinfo`）
- 通用工具：`bioinfo_base`, `ngs_tools`, `genomics_suite`

### 2.4 环境备份与迁移

```bash
# 导出当前环境（锁定版本，适合同平台迁移）
conda env export > envs/environment.lock.yml

# 跨平台用：只导出显式安装的包（不含平台特定的 build string）
conda env export --from-history > envs/environment.yml

# 跨机器恢复
mamba env create -f envs/environment.yml
```

- `envs/` 目录提交 Git，团队共享
- `environment.lock.yml` 保留完整版本（仅同平台使用）
- `environment.yml` 用于跨平台协作（团队共享推荐）

---

## 3. 密钥与敏感配置管理 (Secrets Management)

### 3.1 核心原则

**所有密钥、Token、密码、API Key、数据库连接串必须存入 `.env`，严禁写入脚本/配置/Git 仓库。**

### 3.2 `.env` 模板结构

```bash
# --- 数据库/云服务密钥 ---
NCBI_API_KEY=your_n…here
ENA_FTP_USER=your_ena_username
ENA_FTP_PASS=your_ena_password

# AWS S3
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_a…_key
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=your-project-raw-data

# GCP
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# --- 在线工具 API ---
KEGG_API_KEY=***
STRING_API_KEY=your_s…_key
ALPHAFOLD_API_TOKEN=your_a…oken

# --- HPC/SLURM ---
SLURM_ACCOUNT=your_slurm_account
SLURM_PARTITION=gpu_partition

# --- 容器仓库 ---
DOCKER_REGISTRY_USER=your_docker_username
DOCKER_REGISTRY_PASS=your_docker_password

# --- 内部服务 ---
LIMS_API_URL=https://lims.yourinstitution.edu/api
LIMS_API_TOKEN=***
REF_DB_HOST=db.yourinstitution.edu
REF_DB_PORT=5432
REF_DB_NAME=genomics_ref
REF_DB_USER=db_user
REF_DB_PASS=db_password
```

### 3.3 `.env` 管理流程

1. 项目初始化检查 `.env` 是否存在
   - 不存在 → 从 `.env.template` 创建并提示填写
   - 存在 → 加载并验证必要变量
2. `.env.template` 提交 Git 作为模板（值用占位符）
3. 脚本读取方式：
   - Shell: `source .env`
   - Python: `python-dotenv`
   - R: `dotenv` 包
   - Snakemake: `envvars` 指令
4. 运行时验证必要变量，缺失时提示用户补充 `.env`

### 3.4 安全红线

- 🚫 **绝对禁止**：脚本中硬编码密码/API Key/Token
- 🚫 **绝对禁止**：`.env` 提交 Git（`.gitignore` 排除）
- 🚫 **绝对禁止**：日志打印密钥（脚本必须 filter）
- ✅ **推荐**：定期轮换 API Key，使用临时凭证（AWS STS, GCP IAM）
- ✅ **推荐**：团队用 1Password / Bitwarden / Vault 共享 `.env`

---

## 4. 数据版本控制：Git + DVC

### 4.1 核心原则

**Git 管代码/元数据，DVC 管大数据文件**，两者协同实现完整可复现性。

| 工具 | 跟踪对象 |
|------|---------|
| **Git** | 脚本、配置、文档、`.dvc` 元数据、`.dvcignore` |
| **DVC** | FASTQ / BAM / VCF / 参考基因组 / 模型文件 |

### 4.2 初始化顺序（重要）

**必须先建 .gitignore，再 git init，再 dvc init**：

```bash
# 1. 先建 .gitignore（关键第一步，防止密钥/大数据被意外 commit）
cat > .gitignore << 'EOF'
# 原始数据（DVC 管理）
data/raw/
data/processed/
*.fastq.gz *.fasta *.fa *.bam *.sam *.cram *.vcf.gz
*.bigwig *.bw *.bed

# DVC 缓存
.dvc/cache/
.dvc/tmp/

# 结果（DVC 管理，保留 figures）
results/*/
!results/figures/

# 日志
logs/
*.log

# 密钥（Git 忽略！）
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
.DS_Store
EOF

# 2. 然后初始化 Git（此时 .gitignore 已存在，不会意外 commit 大文件/密钥）
git init
git add .gitignore
git commit -m "chore(init): 项目初始化"

# 3. 再初始化 DVC（在 Git 仓库内）
dvc init
git add .dvc .dvcignore
git commit -m "chore(dvc): 初始化 DVC 数据版本控制"
```

### 4.3 DVC 远程存储配置

```bash
# 从 .env 读取凭证
source .env

# S3
dvc remote add -d myremote s3://${S3_BUCKET_NAME}/dvc-storage

# 本地 NAS
dvc remote add -d myremote /path/to/shared/nas/dvc-storage

# SSH
dvc remote add -d myremote ssh://user@server:/path/to/storage

# 所有远程配置不含密钥（密钥走 .env）
```

### 4.4 数据跟踪工作流

```bash
# 原始数据入库
dvc add data/raw/
git add data/raw.dvc data/raw/.gitignore
git commit -m "data(raw): 添加原始测序数据 v1"
dvc push

# 中间结果跟踪（仅跟踪耗时/难重生成的）
dvc add results/alignment/
git add results/alignment.dvc
dvc push

# 版本切换
git checkout v1.0 && dvc checkout
```

### 4.5 DVC Pipeline（推荐编排）

```yaml
# dvc.yaml
stages:
  qc:
    cmd: bash scripts/01_qc.sh
    deps: [scripts/01_qc.sh, data/raw/]
    outs: [results/qc/:]
    params: [config/parameters.yml:qc]
  align:
    cmd: bash scripts/02_align.sh
    deps: [scripts/02_align.sh, results/qc/trimmed/, config/references.yml:star_index]
    outs: [results/alignment/:]
  de_analysis:
    cmd: Rscript scripts/04_deseq2.R
    deps: [scripts/04_deseq2.R, results/counts/, config/samplesheet.csv]
    outs: [results/degs/:, results/figures/:]
    metrics: [results/degs/summary.json:]
    plots: [results/figures/volcano_plot.png, results/figures/pca_plot.png]
```

执行：`dvc repro` / `dvc status` / `dvc dag` / `dvc push`

---

## 5. 相对路径规范策略 (Relative Path Convention)

### 5.1 核心原则

**所有脚本/配置/Pipeline 中的路径均以项目根目录为基准，采用相对路径。** 相对路径是规范而非强制，Agent 识别到绝对路径时发出警告。

### 5.2 为什么用相对路径

| 问题 | 绝对路径风险 | 相对路径优势 |
|------|------------|------------|
| 分布式环境 | `/home/alice/project` 在 Bob 机器不存在 | `./data/raw/` 通用 |
| 隐私泄露 | `/home/alice/secret-project` 暴露用户名 | 相对路径不泄露 |
| 容器化失效 | 容器内路径与宿主机不同 | 容器内同样有效 |
| CI/CD 失败 | CI 环境无该路径 | 直接可用 |
| 团队协作 | 每人路径不同需改 | 克隆即用 |

### 5.3 实现规范（所有路径以项目根目录为基准）

**Shell**：
```bash
# 脚本放在 scripts/ 下时，先切换到项目根目录
cd "$(dirname "${BASH_SOURCE[0]}")/.."
PROJECT_DIR="$(pwd)"

# 所有路径基于 PROJECT_DIR
INPUT_DIR="${PROJECT_DIR}/data/raw"
OUTPUT_DIR="${PROJECT_DIR}/results/qc"

# 执行命令（相对路径）
fastqc -t 4 -o results/qc data/raw/*.fastq.gz
```

**Python**：
```python
import os
from pathlib import Path

# 基于脚本位置向上两级到项目根
PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_DIR / "data" / "raw"
```

**Snakemake / WDL / DVC Pipeline**：
所有工具默认以项目根目录（`dvc.yaml` 所在目录）为工作目录，直接写相对路径：
```python
# Snakefile
rule fastqc:
    input: "data/raw/{sample}.fastq.gz"   # 相对于项目根
    output: html="results/qc/{sample}_fastqc.html"
    log: "logs/fastqc/{sample}.log"
```

### 5.4 路径安全检查（Agent 识别）

Agent 在生成或审查脚本时执行以下检查：
1. 扫描所有路径是否以 `/` 开头
2. 检查是否含用户名（`/home/alice/`, `/Users/bob/`）
3. 检查是否含机构名（如 `/company-name/`）
4. 发现绝对路径 → **发出警告并提示手动修改为相对路径**
5. 建议团队在 `.gitignore` 中排除可能泄露路径的文件

### 5.5 外部资源路径处理

**策略 1：符号链接**（共享参考基因组）
```bash
ln -s /shared/reference/GRCh38.fa resources/reference/GRCh38.fa
# 脚本中使用: resources/reference/GRCh38.fa
```

**策略 2：环境变量**（通过 .env，不在脚本中硬编码具体值）
```bash
# .env: EXTERNAL_REF_DIR=/shared/reference
REFERENCE="${EXTERNAL_REF_DIR}/GRCh38.fa"
```

---

## 6. 经验沉淀：Pipeline 仓库

### 6.1 核心原则

**复杂分析（≥3 步骤或涉及参数调优）完成后必须沉淀为可复用 Pipeline。**

### 6.2 触发条件

- 流程 ≥ 3 步骤
- 涉及参数调优（比对参数、过滤阈值）
- 遇到并解决非 trivial 问题
- 分析结果被验证（发表/内部评审）
- 同类型分析被重复执行 ≥ 2 次
- 用户明确要求沉淀

### 6.3 沉淀流程

1. 分析完成并验证通过
2. 回顾过程，提取关键决策点（工具选择/参数/问题解决/QC 标准/路径规范）
3. 编写经验文档（Markdown）
4. 重构为标准化 Pipeline（Snakemake/WDL/DVC Pipeline）
5. 参数外部化到 config（使用相对路径）
6. 添加单元测试 + 验证数据
7. **路径审计**：扫描确认无绝对路径泄露
8. 提交到经验 Pipeline 仓库（见 6.4）
9. 更新项目文档引用

### 6.4 仓库结构（位置不限定，团队自行约定）

约定放在 `~/experience-pipelines/` 或项目内的 `pipelines/` 目录，Agent 需知道**当前使用的仓库路径**，通过配置或环境变量传递：

```bash
# .env 中定义
EXPERIENCE_PIPELINE_DIR=/path/to/experience-pipelines
```

仓库结构（参考，可根据团队习惯调整）：
```
experience-pipelines/
├── README.md
├── envs/
│   ├── rnaseq-star-deseq2.yml
│   └── dna-wgs-gatk.yml
├── pipelines/
│   ├── rnaseq-star-deseq2/
│   │   ├── v1.0.0/
│   │   │   ├── Snakefile
│   │   │   ├── workflow/{rules/,envs/,scripts/}
│   │   │   ├── config/{config.yaml,samples.csv,resources.yaml}
│   │   │   ├── docs/{README.md,methodology.md,parameters.md,troubleshooting.md,changelog.md}
│   │   │   ├── tests/{test_data/,test_config.yaml,test_run.sh}
│   │   │   ├── benchmarks/benchmark_results.md
│   │   │   └── .env.template
│   │   ├── v1.1.0/
│   │   └── latest -> v1.1.0/
│   ├── dna-wgs-gatk4/
│   ├── metagenomics-assembly/
│   ├── single-cell-rnaseq/
│   └── epigenomics-chipseq/
└── shared/
    ├── rules/{common_qc.smk,common_align.smk,common_utils.smk}
    ├── scripts/{merge_counts.py,plot_volcano.R,generate_report.py}
    ├── containers/{Dockerfile.base,singularity.def}
    └── schemas/{samples.schema.json,config.schema.json}
```

**Agent 查询方法**：`grep -r "analysis_type:" ${EXPERIENCE_PIPELINE_DIR}/pipelines/ --include="README.md"` 或直接扫描 `pipelines/*/README.md` 的第一行。

### 6.5 文档模板（README.md 必须包含）

- 分析类型 + 适用场景 + 输入输出
- **路径规范说明（强调相对路径）**
- 快速开始指南
- 流程图（Mermaid）
- 工具链与版本表格
- 关键参数与经验
- 质控标准清单
- 已知问题与解决方案
- 引用和许可证

```mermaid
graph LR
    A[Raw FASTQ] --> B[FastQC] --> C[Trim] --> D[STAR] --> E[FeatureCounts] --> F[DESeq2]
```

### 6.6 版本管理（Semantic Versioning）

- **MAJOR**（X.0.0）：工具链重大变更、不兼容的输入/输出格式
- **MINOR**（x.Y.0）：新增步骤、参数调优、新增可视化（向后兼容）
- **PATCH**（x.y.Z）：Bug 修复、文档更新、容器版本（向后兼容）

### 6.7 沉淀检查清单

1. ✅ 流程完整性（步骤独立/输入输出清晰/错误处理）
2. ✅ 参数外部化（config + 注释 + 默认值验证）
3. ✅ 文档完整（README/parameters/troubleshooting/changelog）
4. ✅ **路径审计**（无绝对路径/无用户名泄露/相对路径规范/外部资源通过 .env 或 symlink）
5. ✅ 测试验证（小型数据集 + <30 min + 结果一致）
6. ✅ 可复现性（环境锁定/容器定义/随机种子）
7. ✅ 性能基准（CPU/内存/耗时/成本）
8. ✅ 代码质量（最佳实践/模块化/完整日志）
9. ✅ 提交审核（仓库 + 版本标签 + 通知团队）

---

## 7. 工具复用策略 (Tool Reuse)

### 7.1 工具选择决策树

```
新需求 → 需求拆解（输入数据 + 分析目标 + 参考基因组）
├─ 查询经验 Pipeline 仓库
│  ├─ 匹配 → 复用 + 调参
│  └─ 相近 → 询问是否基于其修改
├─ 无匹配 → 搜索 Bioconda
│  ├─ 有成熟工具 → 安装/复用
│  ├─ 多工具可选 → 对比 benchmark → 推荐最优
│  └─ 无现成 → 评估组合
│     ├─ 可组合 → 设计 pipeline → 沉淀
│     └─ 必须自研 → 编写代码（最后手段）
└─ 不确定 → 查文献 / 问用户 / 看经验 Pipeline
```

### 7.2 代码编写底线（仅以下情况自研）

1. 现有工具无法满足（如定制化统计模型）
2. 需要胶水代码连接多工具（优先 Snakemake/WDL/DVC Pipeline）
3. 数据格式转换（优先 seqkit/samtools/bedtools）
4. 可视化（优先 matplotlib/seaborn/plotly）

**自研代码规范**：
- Python（pandas/numpy/biopython/pysam）或 R（tidyverse/Bioconductor）
- 必须 `argparse` 参数解析 + `__main__` 入口
- 必须写入 Git + 记录 commit
- 敏感配置从 `.env` 读取
- **所有路径使用相对路径（以项目根为基准）**

---

## 8. Git 工作流 (Git Flow)

### 8.1 仓库发现

1. 检测工作目录 Git 状态：`git rev-parse --git-dir`（向上遍历）
2. 找到 → 读取 `git remote -v` + 当前 branch + 工作区状态
3. 未找到 → 询问：提供路径 / 初始化 / 克隆 URL

### 8.2 分析任务 Git 规范

1. 创建分支：`git checkout -b analysis/{task_name}_{date}`
2. 编写/复用脚本（`scripts/` 或 `pipelines/`）
3. 执行 + 记录日志
4. 生成文档（`docs/`）
5. DVC 跟踪大数据
6. **提交前检查**：
   ```bash
   git diff --staged --name-only    # 人工 review staged 变更
   dvc status                        # 确认 DVC 跟踪状态
   # 检查 .env 未被 git add（关键！）
   if git diff --staged --name-only | grep -E "^\.env$"; then
       echo "⚠️ .env 被 staged 了，请先移除！"
       exit 1
   fi
   ```
7. 提交：`scripts/ docs/ envs/ dvc.yaml params.yaml data/*.dvc results/*.dvc pipelines/`
8. 提交信息（Conventional Commits）：
   - `feat(analysis): 新分析流程`
   - `feat(pipeline): 新增/复用经验 Pipeline`
   - `fix(pipeline): 修复分析错误`
   - `docs(report): 更新分析报告`
   - `env(conda): 环境配置变更`
   - `data(raw)` / `data(results)`：数据更新
   - `refactor(scripts)`: 脚本重构
   - `perf(optim)`: 性能优化
   - `chore(dvc)`: DVC 配置更新
   - `security(env)`: 密钥/环境变量更新
9. `dvc push`
10. 合并：`git checkout main && git merge --no-ff analysis/{task_name}_{date}`

---

## 9. 文档与脚本自动生成

### 9.1 分析报告模板

文件路径：`docs/analysis_{YYYYMMDD}_{task_name}.md`

> **路径说明**：本文档所有路径均以项目根目录为基准。

```markdown
# 分析报告：{task_name}

## 元信息
- **日期**：{YYYY-MM-DD}
- **执行者**：Agent / 方师傅
- **Git Branch**：`{branch_name}`
- **Commit**：`{commit_hash}`
- **Conda Env**：`{env_name}`
- **DVC 状态**：`{dvc_status}`

## 输入数据
- **来源**：{数据来源}
- **格式**：{FASTQ/BAM/VCF/...}
- **样本量**：{N} 个样本
- **路径**：`data/raw/`（DVC 跟踪：{是/否}）
- **获取方式**：{下载/拷贝/已有}

## 分析目标
{一句话描述}

## 使用工具

| 工具 | 版本 | 用途 | 安装方式 |
|------|------|------|---------|
| STAR | 2.7.10b | RNA-seq 比对 | bioconda |
| ... | | | |

## 执行流程

### Step 1: QC
- **命令**：`bash scripts/01_qc.sh`
- **参数**：`-t 8 -q 20`
- **输出**：`results/qc/multiqc_report.html`
- **耗时**：{X} min
- **DVC 跟踪**：{是/否}

### Step 2: ...
（后续步骤格式同上）

## 结果摘要
{关键统计数字 + 结论}

## 数据版本
- 原始数据版本：v{X}
- 恢复命令：
  ```bash
  git checkout {commit_hash}
  dvc checkout
  ```

## 质控检查清单
- [ ] FastQC 总体评分 > C
- [ ] 映射率 > 80%
- [ ] ...
```

### 9.2 执行脚本模板

文件路径：`scripts/run_{task_name}_{YYYYMMDD}.sh`

```bash
#!/bin/bash
# =============================================================================
# 分析脚本：{task_name}
# 日期：{YYYY-MM-DD}
# 路径规范：所有路径以项目根目录为基准的相对路径
# =============================================================================

set -e  # 遇错即停
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# --- 加载密钥 ---
source .env

# --- 激活环境 ---
conda activate {env_name}

# --- 初始化目录 ---
mkdir -p results/qc results/alignment results/counts logs

# --- 日志记录（含密钥过滤） ---
LOG_FILE="logs/run_{task_name}_{YYYYMMDD}.log"
exec > >(tee -i "$LOG_FILE")
exec 2>&1

# --- 密钥过滤函数（精确匹配行首 KEY= 赋值，防止误伤正常日志） ---
filter_sensitive() {
    local logfile="$1"
    grep -v -E "^(AWS_SECRET|PASSWORD|API_KEY|TOKEN|ENA_FTP_PASS|NCBI_API_KEY|REF_DB_PASS|LIMS_API_TOKEN)=" "$logfile" || true
}

# --- 分析步骤 ---
echo "[$(date)] Step 1: QC 开始"
bash scripts/01_qc.sh
echo "[$(date)] Step 1: QC 完成"

echo "[$(date)] Step 2: Alignment 开始"
bash scripts/02_align.sh
echo "[$(date)] Step 2: Alignment 完成"

# --- DVC 跟踪结果 ---
dvc add results/qc/ results/alignment/

# --- 清理密钥后的日志 ---
LOG_CLEAN="logs/run_{task_name}_{YYYYMMDD}_clean.log"
filter_sensitive "$LOG_FILE" > "$LOG_CLEAN"
mv "$LOG_CLEAN" "$LOG_FILE"

echo "[$(date)] 全部完成，结果在 results/"
```

---

## 10. 质量控制与验证

### 10.1 输入数据验证

每任务开始前：
- 文件存在性 / 格式验证 / md5 校验
- 规模评估（磁盘/内存预估）
- DVC 状态检查

工具：`seqkit stats`, `samtools quickcheck`, `bcftools stats`, `md5sum -c`, `dvc status`

### 10.2 中间结果检查点

- 每步骤后验证输出 + 格式
- DVC 跟踪关键中间结果

### 10.3 可复现性验证

完成后：
- `dvc repro` 能否从原始数据重跑出相同结果
- 随机种子是否固定
- `conda env export --from-history > envs/environment.yml`
- `dvc.lock` 已提交
- 新机器 `git clone + dvc pull + dvc repro` 能否复现
- **路径检查**：扫描脚本确认无绝对路径泄露

---

## 11. 数据管理与目录结构

### 11.1 标准目录结构

```
project/
├── .git/                       # Git 仓库
├── .dvc/  .dvcignore           # DVC 配置
├── .gitignore                  # 先建此文件，再 git init（防密钥泄露！）
├── .env                        # 敏感配置（Git 忽略！）
├── .env.template               # 模板（Git 跟踪）
├── README.md
├── environment.yml             # Conda 环境定义（跨平台用）
├── environment.lock.yml        # Conda 环境锁定版本（同平台用）
├── dvc.yaml  dvc.lock          # DVC Pipeline
├── params.yaml
├── config/
│   ├── parameters.yml          # 分析参数配置
│   ├── samplesheet.csv         # 样本信息表
│   ├── references.yml         # 参考基因组配置
│   └── dvc_remotes.yml        # DVC 远程配置（不含密钥）
├── data/
│   ├── raw.dvc                # DVC 元数据（Git 跟踪）
│   ├── raw/                   # 实际数据（DVC 跟踪）
│   ├── processed.dvc
│   ├── processed/
│   └── external/
├── scripts/
│   ├── run_pipeline.sh         # 主执行脚本
│   ├── 01_qc.sh
│   ├── 02_align.sh
│   ├── 03_quantify.sh
│   ├── 04_deseq2.R
│   └── utils/
│       └── common.sh           # 含 filter_sensitive() 等共享函数
├── results/
│   ├── qc.dvc  qc/
│   ├── alignment.dvc  alignment/
│   ├── counts.dvc  counts/
│   ├── degs.dvc  degs/
│   └── figures/                # 小图表（Git 直接跟踪）
├── docs/
│   ├── analysis_*.md
│   ├── methods.md
│   └── PATH_GUIDELINES.md
├── logs/                      # Git 忽略
├── envs/                      # 环境 yml 文件
│   └── *.yml
└── pipelines/                 # 经验 Pipeline
```

### 11.2 大数据处理原则

- 🚫 原始测序数据不入 Git（`.gitignore` + DVC）
- 🚫 密钥不入 Git（`.env` + `.gitignore`）
- >10MB 数据用 DVC
- 中间文件定期清理（保留 DVC 检查点）
- 结果压缩归档（gzip/bgzip）
- 🚫 敏感数据（人类基因组）不记录样本身份
- 日志自动过滤密钥（见 9.2 脚本模板的 `filter_sensitive`）
- ✅ 路径全部相对化（以项目根为基准）

---

## 12. 交互规范

### 12.1 首次交互检查清单

1. **环境检查**：读取 shell 配置 → 检测 conda/mamba → 未安装则询问
2. **Git 仓库检查**：检测当前目录 Git 状态 → 未初始化则询问（提供路径/初始化/克隆）
3. **DVC 检查**：检测 DVC 状态 → 询问远程存储类型（S3/NAS/本地）
4. **.env 检查**：不存在则从模板创建并提示填写
5. **项目结构检查**：询问是否自动创建标准目录
6. **需求澄清**：输入数据类型/位置 + 分析目标 + 参考基因组版本 + 计算资源
7. **工具选择确认**：列出工具 + 版本 + 选择理由 + 征求确认
8. **路径规范检查**：确认工作目录，告知后续所有路径以项目根为基准
9. **经验 Pipeline 查询**：查询仓库，询问是否复用

### 12.2 持续交互

**分析过程中**：
- 每完成一步汇报进度
- 异常立即暂停 + 提供解决方案选项
- 长时间任务（>5 min）提供进度估算
- DVC 推送时汇报传输进度
- 发现绝对路径时发出警告

**分析完成后**：
- 结果摘要（关键统计）
- 文件路径（Git 跟踪 vs DVC 跟踪）
- 数据恢复命令
- 下一步建议
- 询问是否生成可视化报告
- 询问是否沉淀经验 Pipeline

---

## 13. 错误处理与恢复

### 13.1 常见错误预案

| 错误类型 | 检测命令 | 自动处理 | 用户通知 |
|---------|---------|---------|---------|
| Conda 环境缺失 | `conda env list` | 询问创建/克隆 | 环境 X 不存在，是否创建？ |
| 工具未安装 | `which tool` | `mamba install` | 正在安装 {tool}... |
| 内存不足 | `free -h` | 减少线程/分批 | 内存不足，调整参数... |
| 磁盘不足 | `df -h` | 清理中间文件 | 磁盘不足，建议... |
| 数据格式错 | 格式验证工具 | 停止 + 报告 | 输入数据异常，请检查... |
| Git 冲突 | `git status` | stash/分支策略 | Git 工作区冲突，建议... |
| DVC 远程未配置 | `dvc remote list` | 引导配置 | DVC 远程未配置，请选择... |
| .env 缺失 | `test -f .env` | 从模板创建 | 请配置 .env 中的密钥... |
| DVC 数据不一致 | `dvc status` | `dvc checkout` 或 `dvc pull` | DVC 数据与元数据不一致... |
| 密钥泄露风险 | `grep -r -E "^(AWS_SECRET\|PASSWORD\|API_KEY\|TOKEN)=" scripts/` | 警告 | ⚠️ 检测到疑似密钥硬编码，请移至 .env |
| 绝对路径 | `grep -r "^/" scripts/ config/` | 警告提示修改 | ⚠️ 检测到绝对路径，建议改为以项目根为基准的相对路径 |
| 相对路径错误 | 运行时检查 | 提示正确工作目录 | 请在项目根目录运行... |

### 13.2 日志密钥过滤辅助函数

```bash
# 放在 scripts/utils/common.sh 中，所有脚本 source 它
filter_sensitive() {
    local logfile="$1"
    # 精确匹配行首 KEY= 赋值，防止误伤正常日志（如 "Loaded tokenizer.json"）
    grep -v -E "^(AWS_SECRET|PASSWORD|API_KEY|TOKEN|ENA_FTP_PASS|NCBI_API_KEY|REF_DB_PASS|LIMS_API_TOKEN)=" "$logfile" || true
}
```

### 13.3 回滚机制

- 每步骤前 DVC 检查点
- 失败时清理不完整输出（或询问保留调试）
- `--dry-run` 预览命令
- 数据回滚：`git checkout {commit} && dvc checkout`

---

## 14. 快速启动模板

当用户说"开始一个生信分析项目"时，Agent 执行以下初始化流程：

```bash
#!/bin/bash
# =============================================================================
# 生信项目快速初始化（Git + DVC + .env + 相对路径规范）
# 使用方式：bash init_bioinfo_project.sh [project_name]
# =============================================================================

PROJECT_NAME="${1:-bioinfo_project}"
mkdir -p "${PROJECT_NAME}"
cd "${PROJECT_NAME}"

# 1. 先建 .gitignore（关键第一步，防止密钥/大数据被意外 commit）
cat > .gitignore << 'EOF'
# 原始数据（DVC 管理）
data/raw/
data/processed/
*.fastq.gz *.fasta *.fa *.bam *.sam *.cram *.vcf.gz
*.bigwig *.bw *.bed

# DVC 缓存
.dvc/cache/
.dvc/tmp/

# 结果（DVC 管理，保留 figures）
results/*/
!results/figures/

# 日志
logs/
*.log

# 密钥（Git 忽略！）
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
.DS_Store
EOF

# 2. 然后初始化 Git（.gitignore 已存在，不会意外 commit 大文件/密钥）
git init
git add .gitignore
git commit -m "chore(init): 项目初始化"

# 3. 创建 .env.template（可安全提交 Git）
cat > .env.template << 'EOF'
# 复制为 .env 并填入实际值
NCBI_API_KEY=YOUR_N…HERE
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_A…_KEY
S3_BUCKET_NAME=your-bucket-name
# 其他密钥...
EOF
cp .env.template .env
echo "[!] 请编辑 .env 填入实际密钥！"

# 4. 创建目录结构
mkdir -p data/{raw,processed,external} scripts results/{qc,alignment,counts,degs,figures} docs config envs logs pipelines

# 5. 初始化 DVC（在 Git 仓库内）
dvc init
echo ".dvc/cache/" >> .gitignore
echo ".dvc/tmp/" >> .gitignore
git add .dvc .dvcignore .gitignore .env.template
git commit -m "chore(dvc): Git + DVC 初始化完成"

# 6. README.md（去掉单引号让 $PROJECT_NAME 变量展开）
cat > README.md << EOF
# \${PROJECT_NAME}

## 项目描述
[描述项目背景和目标]

## 环境配置
\`\`\`bash
conda env create -f envs/environment.yml
conda activate \${PROJECT_NAME}_bioinfo
dvc remote add -d myremote <remote-url>
conda env create -f envs/environment.yml
conda activate ${PROJECT_NAME}_bioinfo
dvc remote add -d myremote <remote-url>
\`\`\`

## 数据恢复
\`\`\`bash
git clone <repo>
dvc pull
dvc repro
\`\`\`

## 路径规范
所有路径以项目根目录为基准，使用相对路径。

## 目录结构
- \`data/raw/\`: 原始测序数据（DVC）
- \`scripts/\`: 分析脚本（Git）
- \`results/\`: 分析结果（DVC）
- \`docs/\`: 分析文档（Git）
- \`.env\`: 密钥配置（Git 忽略）
EOF

# 7. 环境文件
cat > envs/environment.yml << 'EOF'
name: PROJECT_NAME_bioinfo
channels: [conda-forge, bioconda, defaults]
dependencies:
  - python=3.10
  - mamba
  - dvc dvc-s3
  - fastqc multiqc
  - samtools bedtools seqkit
  - snakemake
EOF

echo "========================================"
echo " 项目 ${PROJECT_NAME} 初始化完成！"
echo "========================================"
echo " 下一步："
echo "  1) 编辑 .env 填入密钥"
echo "  2) 放入原始数据到 data/raw/"
echo "  3) 定义 dvc.yaml 编排分析流程"
echo "  4) bash scripts/run_pipeline.sh"
echo "  5) 阅读 docs/PATH_GUIDELINES.md"

---

## 15. 关键参考资源

- **Bioconda**: <https://bioconda.github.io/>
- **DVC 文档**: <https://dvc.org/doc>
- **Snakemake**: <https://snakemake.readthedocs.io/>
- **Nextflow**: <https://www.nextflow.io/docs/latest/index.html>
- **Biocontainers**: <https://quay.io/organization/biocontainers>

---

_核心价值：Agent 不是写代码，而是 orchestrate 现有工具生态 + 严格管理密钥/数据/版本 + 保证每一步可审计/可复现/可交接 + 将经验沉淀为团队资产。_

_最后更新：2026-06-20_
