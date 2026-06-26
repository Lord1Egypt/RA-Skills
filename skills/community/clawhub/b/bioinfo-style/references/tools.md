# 常用生信工具速查

## 测序数据质控

| 工具 | 用途 | 常用命令 |
|------|------|----------|
| FastQC | 原始数据质量评估 | `fastqc -o qc/ sample.fastq.gz` |
| MultiQC | 批量汇总QC报告 | `multiqc . -o report/` |
| Trimmomatic | 过滤低质量reads | `trimmomatic PE input_R1.fastq.gz input_R2.fastq.gz out_R1.fastq.gz out_R2.fastq.gz ILLUMINACLIP:adapters.fa:2:30:10` |
| Cutadapt | 去除接头/低质量序列 | `cutadapt -a AGATCGGAAGAGC -o trimmed.fastq.gz input.fastq.gz` |

## 序列比对

| 工具 | 用途 | 常用命令 |
|------|------|----------|
| STAR | RNA-seq比对（金标准） | `star --genomeDir ref --readFilesIn R1.fq.gz --readFilesCommand zcat` |
| BWA | DNA比对 | `bwa mem ref.fa reads.fq.gz > aln.sam` |
| HISAT2 | RNA-seq（快速） | `hisat2 -x ref -U reads.fq.gz | samtools view -Sb` |
| Bowtie2 | 小基因组/短序列 | `bowtie2 -x ref -U reads.fq.gz` |

## 表达定量

| 工具 | 用途 | 常用命令 |
|------|------|----------|
| featureCounts | 基于注释定量 | `featureCounts -a annotation.gtf -o counts.txt alignments.bam` |
| htseq-count | 计数定量 | `htseq-count -f bam -s reverse alignment.bam annotation.gtf` |
| Salmon | 伪定量（快速） | `salmon quant -i index -l IU -r reads.fq.gz -o output` |
| kallisto | 伪定量 | `kallisto quant -i index -o output reads.fq.gz` |

## 差异分析

| 工具 | 用途 | R包 |
|------|------|-----|
| DESeq2 | 标准化计数差异分析 | `DESeq2` |
| edgeR | 计数数据差异分析 | `edgeR` |
| limma-voom | 微阵列/RNA-seq | `limma` |

## 富集分析

| 工具 | 用途 | 常用命令 |
|------|------|----------|
| clusterProfiler | GO/KEGG富集 | R包 |
| GSEA | 基因集富集分析 | R包 |
| Enrichr | 在线富集分析 | 网页版 |
| Metascape | 一站式富集分析 | 网页版 |

## 基因组操作

| 工具 | 用途 | 常用命令 |
|------|------|----------|
| BEDTools |基因组区间操作 | `bedtools intersect -a a.bed -b b.bed` |
| SAMtools | SAM/BAM处理 | `samtools sort -o sorted.bam input.bam` |
| BCFtools | VCF/BCF处理 | `bcftools call -v variants.bcf` |
| GATK | 变异检测（金标准） | `gatk HaplotypeCaller -R ref.fa -I sample.bam -O variants.vcf` |

## 可视化

| 工具 | 用途 | 示例 |
|------|------|------|
| ggplot2 | 通用绘图 | `ggplot(df, aes(x,y)) + geom_point()` |
| pheatmap | 热图 | `pheatmap(mat)` |
| ggrepel | 添加标签 | `geom_text_repel()` |
| EnhancedVolcano | 火山图 | `EnhancedVolcano()` |

## 安装命令（mamba）

```bash
# 创建生信环境
mamba create -n bioinfo \
  -c conda-forge -c bioconda \
  fastqc multiqc trimmomatic \
  star bwa bowtie2 hisat2 \
  samtools bedtools bcftools \
  featurecounts htseq \
  salmon kallisto \
  -y

# R生信包
mamba install -n bioinfo -c conda-forge -c bioconda \
  r-deseq2 r-edger r-limma r-clusterprofiler \
  bioconductor-deseq2 bioconductor-edger -y
```
