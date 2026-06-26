---
name: bioinformatics-analysis
description: 标准化生物信息学分析流程。当用户提出以下任务时激活：(1) 测序数据分析（RNA-seq、ChIP-seq、WGS等），(2) 差异表达分析，(3) 通路/富集分析，(4) 组学数据可视化，(5) 统计检验，(6) 任何需要调用成熟生信工具而非编写Python/R算法代码的分析任务。核心原则：优先调用工具，记录shell脚本过程，结果用Rmarkdown统计可视化，确保分析可重复。
---

# Bioinformatics Analysis - 标准化生信分析

## 核心原则

**工具 > 代码**：优先使用成熟的生信工具，绝不自己写算法代码。
**过程记录**：每一步都写 shell 脚本并执行，而非在对话中描述。
**可重复性**：所有分析必须可以通过脚本重现。

## 工作流程

### 1. 环境准备

```bash
# 读取 ~/.bashrc 中的环境配置
source ~/.bashrc

# 激活或创建 mamba 环境
mamba activate <env_name>      # 已有环境
mamba create -n <env_name> -c <channels> <packages>  # 创建新环境

# 常用生信环境示例
mamba create -n bioinfo -c conda-forge -c bioconda \
  fastqc trimmomatic star featurecounts deseq2 \
  samtools bedtools homer meme
```

### 2. 原始数据质量控制

```bash
# FastQC 质控
fastqc -o <output_dir> -f fastq <raw_data>/*.fastq.gz

# 批量处理脚本模板
cat > 01_qc.sh << 'EOF'
#!/bin/bash
set -e
RAW_DIR="raw_data"
QC_DIR="qc_results"
mkdir -p $QC_DIR

for fq in $RAW_DIR/*.fastq.gz; do
    echo "Processing: $fq"
    fastqc -o $QC_DIR "$fq"
done
echo "QC completed"
EOF
bash 01_qc.sh
```

### 3. 序列比对/定量

```bash
# RNA-seq: STAR 比对 + featureCounts 定量
cat > 02_alignment.sh << 'EOF'
#!/bin/bash
set -e
REF="genome/GRCh38"
SAMPLE="sample1"
GTF="annotation/gencode.v38.annotation.gtf"

mkdir -p alignment/$SAMPLE

star --genomeDir $REF \
     --readFilesIn reads/$SAMPLE.fastq.gz \
     --readFilesCommand zcat \
     --outSAMtype BAM SortedByCoordinate \
     --outFileNamePrefix alignment/$SAMPLE/

featureCounts -T 4 -t exon -g gene_id \
  -a $GTF \
  -o counts/$SAMPLE.counts \
  alignment/$SAMPLE/Aligned.sortedByCoord.out.bam
EOF
bash 02_alignment.sh
```

### 4. 差异分析（Rmarkdown）

```bash
cat > 03_differential_analysis.Rmd << 'EOF'
---
title: "差异表达分析报告"
author: "Bioinformatics Pipeline"
date: "`r Sys.Date()`"
output:
  html_document:
    toc: true
    theme: united
---

```{r setup, message=FALSE}
library(DESeq2)
library(ggplot2)
library(pheatmap)
library(clusterProfiler)
```

```{r load-data}
# 读取计数矩阵
count_matrix <- read.table("counts/matrix.txt", header=TRUE, row.names=1)
coldata <- read.table("metadata.txt", header=TRUE, row.names=1)
```

```{r deseq2}
dds <- DESeqDataSetFromMatrix(countData=count_matrix,
                               colData=coldata,
                               design=~condition)
dds <- DESeq(dds)
results <- results(dds)
```

```{r visualization}
# MA plot
plotMA(results)
# 热图
top_genes <- rownames(head(results[order(results$padj),], 20))
pheatmap(assay(vst(dds))[top_genes,])
```
EOF
Rscript -e "rmarkdown::render('03_differential_analysis.Rmd')"
```

### 5. 富集分析

```bash
cat > 04_enrichment.sh << 'EOF'
#!/bin/bash
set -e
GENELIST="differential_genes.txt"
OUTPUT="enrichment_results"

# GO富集
 enrichment.sh $GENELIST BP CC MF BP
clusterProfiler --dotplot --gseGO

# KEGG通路
enrichment.sh $GENELIST KEGG

# Reactome
enrichment.sh $GENELIST Reactome
EOF
bash 04_enrichment.sh
```

## 工具优先级

1. **QC**: FastQC, MultiQC, Trimmomatic, Cutadapt
2. **比对**: STAR, BWA, Bowtie2, HISAT2
3. **定量**: featureCounts, htseq-count, Salmon, kallisto
4. **差异分析**: DESeq2, edgeR, limma（仅用已有R包，不写算法）
5. **富集分析**: clusterProfiler, GSEA, Enrichr
6. **可视化**: ggplot2, pheatmap, Gviz, IGV
7. **基因组操作**: BEDTools, SAMtools, BCFtools

## 关键规则

- **绝不写Python脚本做已有的生信工具能做的事**
- **每一步都写 .sh 脚本并执行**，记录到 `logs/` 目录
- **原始数据不修改**，所有处理脚本化
- **输出结构标准化**：
  ```
  project/
  ├── raw_data/        # 原始数据（只读）
  ├── qc_results/      # 质控结果
  ├── alignment/       # 比对结果
  ├── counts/          # 表达矩阵
  ├── results/         # 差异分析结果
  ├── figures/         # 图片
  ├── scripts/         # 所有分析脚本
  └── logs/            # 执行日志
  ```
- **Rmarkdown 报告包含**：方法描述、统计结果、可视化图表

## 常用工具速查

详见 [references/tools.md](references/tools.md)

## 分析脚本模板

详见 [references/templates.md](references/templates.md)
