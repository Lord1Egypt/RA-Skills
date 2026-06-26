# BLAST 物种注释工具技能

## 描述

提供BLAST物种注释工具的使用指南和快速调用功能。包含两个主要工具：
- `blast_annotation_tool.py` - 对指定FASTA序列进行BLAST注释
- `top_asv_blast.py` - 从OTU表提取Top ASV并进行BLAST注释

## 安装依赖

```bash
pip install biopython
```

## 工具一：blast_annotation_tool.py

### 基本用法
```bash
# 基本用法：输入FASTA文件和输出目录
python3 blast_annotation_tool.py sequences.fasta results/

# 使用序列ID到样本名的映射文件
python3 blast_annotation_tool.py sequences.fasta results/ --mapping mapping.csv

# 跳过已存在的结果（断点续传）
python3 blast_annotation_tool.py sequences.fasta results/ --skip-existing
```

### 参数说明
- `input`: 输入FASTA文件路径 (必填)
- `output`: 输出目录路径 (必填)
- `--mapping, -m`: 序列ID到样本名的映射文件 (CSV格式)
- `--delay, -d`: 每次BLAST请求之间的延迟秒数 (默认: 3)
- `--hits, -n`: 每个样本保留的BLAST hits数量 (默认: 10)
- `--skip-existing, -s`: 跳过已存在的结果文件 (默认: False)

## 工具二：top_asv_blast.py

### 基本用法
```bash
# 基本用法
python3 top_asv_blast.py taxa_table.xls rep.fasta results/

# 跳过已存在的结果（断点续传）
python3 top_asv_blast.py taxa_table.xls rep.fasta results/ --skip-existing

# 自定义参数
python3 top_asv_blast.py taxa_table.xls rep.fasta results/ --delay 5 --hits 20
```

### 参数说明
- `otu_table`: OTU表文件 (.xls, .tsv, .csv) (必填)
- `fasta`: 代表性序列FASTA文件 (必填)
- `output`: 输出目录路径 (必填)
- `--top-n, -n`: 每个样本提取前N个ASV (默认: 1)
- `--delay, -d`: 每次BLAST请求之间的延迟秒数 (默认: 3)
- `--hits`: 每个ASV保留的BLAST hits数量 (默认: 10)
- `--skip-existing, -s`: 跳过已存在的结果文件 (默认: False)

## 输入文件格式

### FASTA文件
```
>ASV1
TAGGGAATCTTCCGCAATGGACGAAAGTCTGACGGAGCAACGCCGCGTGAG...
>ASV2
TAGGGAATCTTCCGCAATGGACGAAAGTCTGACGGAGCAACGCCGCGTGAG...
```

### 映射文件 (可选)
CSV格式，第一列为序列ID，第二列为样本名：
```csv
ASV1,D1-8
ASV2,J2-8
ASV3,D3-8
```

### OTU表格式
- 第一列：ASV/OTU ID
- 中间列：样本序列计数（支持重复样本自动合并）
- 最后一列：Taxonomy注释

## 输出文件

- 每个样本的BLAST结果CSV文件
- 汇总表 (blast_summary.csv)
- Top ASV信息表 (top_asv_info.csv)

## 注意事项

1. 需要网络连接访问NCBI BLAST服务
2. 每次比对可能需要几秒到几十秒
3. 建议使用`--delay`参数避免请求过于频繁
4. 使用`--skip-existing`可实现断点续传

## 快速调用

当您需要进行BLAST物种注释时，只需说：
- "使用blast注释工具"
- "运行top asv blast"
- "BLAST物种注释指南"

我会为您提供详细的参数说明和使用方法。