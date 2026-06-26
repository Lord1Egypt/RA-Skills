# Auto Proteomics

English | 中文

Auto Proteomics is a public OpenClaw skill for low-token routing and downstream analysis of processed DDA LFQ proteomics inputs.

Auto Proteomics 是一个公开的 OpenClaw skill，用于对 processed DDA LFQ 蛋白组学输入进行低 token 路由与 downstream 分析。

Author / 作者: Guo Xuan 郭轩  
Contact / 联系邮箱: xguo608@connect.hkust-gz.edu.cn

## What this release is

- one shipped runnable workflow: `dda-lfq-processed`
- one public input family: processed DDA LFQ protein-level tables
- one public comparison model: `group-a` vs `group-b`
- a release-oriented repository that keeps visible non-shipped branches for routing clarity: `dia-quant` as an internal prototype, plus `dda-identification` and `phospho-differential` as scaffold-only specs

## 当前版本是什么

- 一个已经随包提供并可运行的工作流：`dda-lfq-processed`
- 一类公开支持输入：processed DDA LFQ 蛋白层级定量表
- 一种公开比较模型：`group-a` vs `group-b`
- 仓库中也保留了可见但未随版本公开承诺的分支：`dia-quant` 仅为 internal prototype，`dda-identification` 与 `phospho-differential` 仍是 scaffold-only 规格

## What it does

Given processed inputs such as MaxQuant-style `proteinGroups.txt`, this release provides a clear public path for:
- matrix generation
- QC outputs
- two-group differential protein analysis
- report and run manifest generation

给定类似 MaxQuant `proteinGroups.txt` 的 processed 输入，本版本提供一条清晰的公开路径，用于生成：
- matrix
- QC 输出
- 双组差异蛋白分析
- report 和 run manifest

## What it is not

This first public release is intentionally narrow. It does not promise:
- raw-spectrum identification pipelines
- DIA execution
- phosphoproteomics execution
- enrichment execution
- multi-omics execution
- generalized complex study-design handling

这个首个公开版本刻意保持边界收束，不承诺：
- 原始谱图鉴定流程
- DIA 执行
- 磷酸化蛋白组执行
- 富集分析执行
- multi-omics 执行
- 更一般化的复杂实验设计处理

## Public entrypoint

```bash
bash scripts/workflows/dda_lfq_processed.sh \
  --input-dir <run_dir> \
  --protein-groups <proteinGroups.txt> \
  --summary <summary.txt> \
  --parameters <parameters.txt> \
  --output-dir <output_dir> \
  --group-a <condition_a> \
  --group-b <condition_b>
```

## Repository structure

- `SKILL.md`: public entry and release boundary
- `references/WORKFLOW_INDEX.yaml`: routing and shipped-vs-non-shipped boundary
- `references/RUNTIME_REQUIREMENTS.md`: runtime contract for the shipped DDA path
- `references/DEMO_INPUT_GUIDE.md`: demo/onboarding input guidance for the shipped DDA path
- `references/branches/`: internal branch specs for scaffold and prototype routes unless explicitly promoted
- `scripts/workflows/dda_lfq_processed.sh`: shipped execution path

## Release positioning

This repository is not presented as a full proteomics toolbox.
The shipped public surface is exactly one runnable processed DDA LFQ downstream path.
Visible DIA / DDA-identification / phospho materials remain internal prototype or scaffold context, not shipped support.

这个仓库并不是“蛋白组学全家桶”。
当前真正随版本公开交付的，只有一条可运行的 processed DDA LFQ downstream 路径。
仓库里可见的 DIA / DDA-identification / phospho 相关内容仍属于 internal prototype 或 scaffold context，不代表已经公开支持。
