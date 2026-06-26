# 分析脚本模板

## 标准项目目录结构

```
PROJECT_NAME/
├── README.md                    # 项目说明
├── CONFIG.sh                     # 全局配置（路径、参数）
├── logs/                         # 执行日志
│   ├── 01_qc.log
│   ├── 02_alignment.log
│   └── ...
├── raw_data/                     # 原始数据（只读）
│   ├── sample1_R1.fastq.gz
│   └── sample1_R2.fastq.gz
├── qc_results/                   # 质控结果
├── trimmed/                      # 过滤后数据
├── alignment/                    # 比对结果
├── counts/                       # 表达矩阵
│   └── all_samples_counts.txt
├── results/                      # 差异分析结果
├── figures/                      # 图片
└── reports/                      # Rmarkdown报告
    └── analysis_report.html
```

## CONFIG.sh 模板

```bash
#!/bin/bash
# =====================================================================
# 全局配置文件
# =====================================================================

# 项目根目录
PROJECT_ROOT="/path/to/project"
cd $PROJECT_ROOT

# 参考基因组
REF_GENOME="/path/to/ref/genome.fa"
REF_INDEX="/path/to/ref/star_index"
ANNOTATION_GTF="/path/to/annotation.gtf"

# 数据目录
RAW_DIR="raw_data"
TRIMMED_DIR="trimmed"
ALIGN_DIR="alignment"
COUNTS_DIR="counts"
RESULTS_DIR="results"
FIGURES_DIR="figures"

# 分析参数
THREADS=8
ADAPTER_FILE="/path/to/adapters.fa"

# 样本列表（空格分隔）
SAMPLES=("control_1" "control_2" "treatment_1" "treatment_2")

# Mamba环境名
BIOINFO_ENV="bioinfo"
```

## 完整RNA-seq分析流程脚本

### 01_qc.sh

```bash
#!/bin/bash
# =====================================================================
# Step 1: 原始数据质量控制
# =====================================================================
source CONFIG.sh
set -e

LOG="logs/01_qc.log"
echo "[$(date)] 开始QC分析" | tee $LOG

# 激活环境
eval "$(conda shell.bash hook)"
conda activate $BIOINFO_ENV

mkdir -p $QC_DIR

for sample in "${SAMPLES[@]}"; do
    echo "[$(date)] Processing $sample" | tee -a $LOG
    fastqc -o $QC_DIR -t $THREADS \
        ${RAW_DIR}/${sample}_R1.fastq.gz \
        ${RAW_DIR}/${sample}_R2.fastq.gz \
        2>> $LOG
done

multiqc $QC_DIR -o $QC_DIR/summary 2>> $LOG
echo "[$(date)] QC完成" | tee -a $LOG
```

### 02_trimming.sh

```bash
#!/bin/bash
# =====================================================================
# Step 2: 数据过滤
# =====================================================================
source CONFIG.sh
set -e

LOG="logs/02_trimming.log"
echo "[$(date)] 开始过滤" | tee $LOG

mkdir -p $TRIMMED_DIR

for sample in "${SAMPLES[@]}"; do
    echo "[$(date)] Trimming $sample" | tee -a $LOG
    trimmomatic PE -phred33 \
        ${RAW_DIR}/${sample}_R1.fastq.gz \
        ${RAW_DIR}/${sample}_R2.fastq.gz \
        ${TRIMMED_DIR}/${sample}_R1.fq.gz \
        ${TRIMMED_DIR}/${sample}_R1_unpaired.fq.gz \
        ${TRIMMED_DIR}/${sample}_R2.fq.gz \
        ${TRIMMED_DIR}/${sample}_R2_unpaired.fq.gz \
        ILLUMINACLIP:$ADAPTER_FILE:2:30:10 \
        LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 \
        2>> $LOG
done

echo "[$(date)] 过滤完成" | tee -a $LOG
```

### 03_alignment.sh

```bash
#!/bin/bash
# =====================================================================
# Step 3: 序列比对
# =====================================================================
source CONFIG.sh
set -e

LOG="logs/03_alignment.log"
echo "[$(date)] 开始比对" | tee $LOG

mkdir -p $ALIGN_DIR

for sample in "${SAMPLES[@]}"; do
    echo "[$(date)] Aligning $sample" | tee -a $LOG
    STAR --genomeDir $REF_INDEX \
         --readFilesIn ${TRIMMED_DIR}/${sample}_R1.fq.gz \
                       ${TRIMMED_DIR}/${sample}_R2.fq.gz \
         --readFilesCommand zcat \
         --outSAMtype BAM SortedByCoordinate \
         --outFileNamePrefix ${ALIGN_DIR}/${sample}_ \
         --runThreadN $THREADS \
         --quantMode GeneCounts \
         2>> $LOG
done

echo "[$(date)] 比对完成" | tee -a $LOG
```

### 04_counting.sh

```bash
#!/bin/bash
# =====================================================================
# Step 4: 表达定量
# =====================================================================
source CONFIG.sh
set -e

LOG="logs/04_counting.log"
echo "[$(date)] 开始定量" | tee $LOG

mkdir -p $COUNTS_DIR

# 合并所有样本的bam文件进行定量
BAM_FILES=""
for sample in "${SAMPLES[@]}"; do
    BAM_FILES="$BAM_FILES ${ALIGN_DIR}/${sample}_Aligned.sortedByCoord.out.bam"
done

featureCounts -T $THREADS -t exon -g gene_id \
    -a $ANNOTATION_GTF \
    -o ${COUNTS_DIR}/all_samples.counts.txt \
    $BAM_FILES \
    2>> $LOG

echo "[$(date)] 定量完成" | tee -a $LOG
```

## Rmarkdown 差异分析报告模板

```yaml
---
title: "RNA-seq 差异表达分析报告"
author: "Hurry Botter"
date: "`r Sys.Date()`"
output:
  html_document:
    toc: true
    code_folding: hide
params:
  count_file: "counts/all_samples.counts.txt"
  metadata: "metadata.txt"
  comparison: "treatment_vs_control"
---

```{r setup, include=FALSE}
library(DESeq2)
library(ggplot2)
library(pheatmap)
library(clusterProfiler)
library(EnhancedVolcano)
library(org.Hs.eg.db)
library(tidyverse)
```

```{r load-data}
# 读取计数矩阵
count_df <- read.table(params$count_file, header=TRUE, row.names=1)
coldata <- read.table(params$metadata, header=TRUE, row.names=1)

# 过滤低表达基因（至少在3个样本中表达>1）
keep <- rowSums(count_df > 1) >= 3
count_df <- count_df[keep, ]
```

```{r deseq2}
dds <- DESeqDataSetFromMatrix(countData=count_df,
                               colData=coldata,
                               design=~condition)
dds <- DESeq(dds)

# 保存标准化后的数据
norm_counts <- counts(dds, normalized=TRUE)
write.table(norm_counts, "results/normalized_counts.txt",
            sep="\t", quote=FALSE)
```

```{r pca}
rld <- rlog(dds)
pcaData <- plotPCA(rld, intgroup="condition", returnData=TRUE)
ggplot(pcaData, aes(PC1, PC2, color=condition)) +
    geom_point(size=3) +
    geom_text_repel(aes(label=name)) +
    theme_bw()
```

```{r differential}
results <- results(dds, contrast=c("condition", "treatment", "control"))
summary(results)
write.table(as.data.frame(results),
            "results/differential_genes.txt",
            sep="\t", quote=FALSE)
```

```{r volcano}
EnhancedVolcano(results,
    lab=rownames(results),
    x='log2FoldChange',
    y='padj',
    pCutoff=0.05,
    FCcutoff=1.5)
```

```{r top-genes-heatmap}
top_genes <- rownames(head(results[order(results$padj),], 30))
mat <- assay(rld)[top_genes, ]
pheatmap(mat, scale="row", show_rownames=FALSE)
```

```{r enrichment}
# 获取差异基因
sig_genes <- rownames(subset(results, padj < 0.05 & abs(log2FoldChange) > 1))

# GO富集分析
go_bp <- enrichGO(gene=sig_genes, OrgDb=org.Hs.eg.db, ont="BP")
dotplot(go_bp, showCategory=15)
```
