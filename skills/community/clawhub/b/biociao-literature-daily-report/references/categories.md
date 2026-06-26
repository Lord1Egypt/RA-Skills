# 领域分类标准

本文档定义了科研日报中使用的领域分类体系和关键词。

## 分类体系

### 1. 单细胞组学 (`单细胞组学`)
- **定义**: 在单细胞分辨率下研究生物样本的技术和方法
- **关键词**: `single-cell`, `scRNA-seq`, `scATAC-seq`, `spatial transcriptomics`, `空间转录组`
- **典型应用**: 细胞类型鉴定、发育轨迹分析、疾病异质性研究

### 2. 宏基因组学 (`宏基因组学`)
- **定义**: 直接对环境样本中所有微生物的基因组进行研究
- **关键词**: `metagenomics`, `microbiome`, `16S`, `metatranscriptomics`, `宏基因组`, `微生物组`
- **典型应用**: 肠道菌群分析、环境微生物探测、病原检测

### 3. 病原真菌 (`病原真菌`)
- **定义**: 引起人类或植物疾病的真菌病原体研究
- **关键词**: `fungal`, `fungus`, `pathogen`, `Candida`, `Aspergillus`, `Cryptococcus`, `镰刀菌`, `真菌`
- **典型应用**: 抗真菌药物开发、感染机制、耐药性研究

### 4. 生物信息方法 (`生信方法`)
- **定义**: 用于处理和分析生物数据的计算方法和工具开发
- **关键词**: `bioinformatics`, `algorithm`, `pipeline`, `tool`, `method`, `computational`, `算法`, `流程`
- **典型应用**: 序列比对、结构预测、变异检测、功能注释

### 5. AI/机器学习 (`AI/ML`)
- **定义**: 人工智能和机器学习技术在生物学中的应用
- **关键词**: `artificial intelligence`, `machine learning`, `deep learning`, `neural network`, `transformer`, `LLM`, `AI`, `ML`
- **典型应用**: 蛋白质结构预测、药物发现、基因调控网络推断

### 6. 基因组学 (`基因组学`)
- **定义**: 全基因组范围的研究，包括结构和功能
- **关键词**: `genomics`, `genome`, `pan-genome`, `structural variation`, `基因组`, `泛基因组`
- **典型应用**: 群体遗传学、进化分析、比较基因组

### 7. 蛋白质组学 (`蛋白质组学`)
- **定义**: 大规模研究蛋白质的结构、功能和相互作用
- **关键词**: `proteomics`, `mass spectrometry`, `peptide`, `protein structure`, `蛋白质组`
- **典型应用**: 表达谱分析、翻译后修饰、蛋白互作网络

### 8. 表观遗传 (`表观遗传`)
- **定义**: 不涉及 DNA 序列变化的基因表达调控
- **关键词**: `epigenetics`, `methylation`, `chromatin`, `ATAC-seq`, `ChIP-seq`, `染色质`, `甲基化`
- **典型应用**: 基因表达调控、细胞分化、疾病标志物

---

## 关键词匹配策略

### 优先级规则
1. **标题优先**: 先匹配标题中的关键词
2. **摘要补充**: 再匹配摘要中的关键词
3. **多标签支持**: 一篇文章可以有多个分类标签

### 大小写不敏感
所有匹配均为大小写不敏感，如 `Single-cell` 和 `single-cell` 同等对待。

### 短语匹配
支持完整短语匹配，如 `deep learning` 会匹配整个短语而不仅仅是单个词。

