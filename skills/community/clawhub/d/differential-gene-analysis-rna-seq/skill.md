# Differential Gene Expression Analysis (RNA-seq)
OpenCLAW Skill for bioinformatics data analysis.

## License
MIT-0

## Description
This skill performs differential gene analysis using DESeq2 with simulated expression data.

## Input
input/count_matrix.csv

## Output
- output/volcano.png
- output/pca.png
- output/heatmap.png
- output/diff_genes_significant.csv

## Code
```r
# ==============================
# OpenCLAW Skill Run Code
# ==============================

if (!require("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager", repos = "https://cloud.r-project.org/")
}

BiocManager::install(c("DESeq2", "ggplot2", "pheatmap"), update = FALSE, ask = FALSE)

library(DESeq2)
library(ggplot2)
library(pheatmap)

if (!dir.exists("output")) dir.create("output")

# Read input
count_df <- read.csv("input/count_matrix.csv", row.names = 1)
count_matrix <- as.matrix(count_df)
group <- factor(c("Control","Control","Control","Treat","Treat","Treat"))
colData <- data.frame(group = group)

# DESeq2
dds <- DESeqDataSetFromMatrix(round(count_matrix), colData, ~ group)
dds <- dds[rowSums(counts(dds)) > 3, ]
dds <- DESeq(dds)
res <- results(dds, contrast = c("group", "Treat", "Control"))
res_sig <- subset(res, padj < 0.05 & abs(log2FoldChange) > 1)
write.csv(as.data.frame(res_sig), "output/diff_genes_significant.csv")

# Volcano
res_df <- as.data.frame(res)
res_df$sig <- ifelse(res_df$padj < 0.05 & abs(res_df$log2FoldChange) > 1, "Sig", "NS")
p <- ggplot(res_df, aes(log2FoldChange, -log10(padj))) + geom_point(aes(color=sig)) + theme_bw()
ggsave("output/volcano.png", p, dpi=300)

# PCA
vsd <- vst(dds, blind=FALSE)
p_pca <- plotPCA(vsd, intgroup="group") + theme_bw()
ggsave("output/pca.png", p_pca)

# Heatmap
if(nrow(res_sig) > 0) {
  top <- head(rownames(res_sig), 10)
  mat <- t(scale(t(assay(vsd)[top,])))
  png("output/heatmap.png", width=800, height=600)
  pheatmap(mat, annotation_col=data.frame(group))
  dev.off()
}

cat("✅ Skill run successfully\n")