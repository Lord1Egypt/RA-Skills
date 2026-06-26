---
name: deeppurpose
description: Help install, inspect, run, troubleshoot, and adapt the DeepPurpose molecular modeling library for drug-target interaction prediction, compound property prediction, DDI, PPI, protein function prediction, drug repurposing, and virtual screening. Use when the user mentions DeepPurpose, `from DeepPurpose import`, `DTI`, `CompoundPred`, `DDI`, `PPI`, `ProteinPred`, `oneliner`, `data_process`, `generate_config`, DeepPurpose datasets, encodings, pretrained models, toy data, or demo notebooks.
license: BSD-3-Clause
---

# DeepPurpose

This skill is adapted from DeepPurpose, copyright (c) 2020 Kexin Huang,
Tianfan Fu, licensed under BSD 3-Clause.

Prefer a local DeepPurpose checkout over web summaries. Treat a directory as the
repo root when it contains `setup.py`, `requirements.txt`, `DeepPurpose/`,
`DEMO/`, and `toy_data/`.

## Workflow

1. Classify the request: environment/install, task pipeline, dataset format,
pretrained model, notebook/demo adaptation, or troubleshooting.
2. Read only the relevant reference file:
   - installation, dependency sanity, or smoke tests:
     `references/install-and-dependencies.md`
   - task/module selection, encodings, splits, and core APIs:
     `references/tasks-and-entrypoints.md`
   - dataset loaders, custom text formats, pretrained downloads, and result
     outputs: `references/data-and-pretrained.md`
3. Verify advice against local files before answering. Prefer `README.md`,
`DeepPurpose/utils.py`, `DeepPurpose/dataset.py`, and the task module the user
actually needs.
4. Reuse the upstream API shape instead of inventing wrappers. The maintained
paths are:
   - DTI: `DeepPurpose/DTI.py`
   - compound property prediction: `DeepPurpose/CompoundPred.py`
   - DDI: `DeepPurpose/DDI.py`
   - PPI: `DeepPurpose/PPI.py`
   - protein function prediction: `DeepPurpose/ProteinPred.py`
   - one-line repurposing and virtual screening:
     `DeepPurpose/oneliner.py`
5. Prefer the closest notebook in `DEMO/` when the user wants an example or a
starting point.

## Execution Rules

- Build datasets with `DeepPurpose.dataset` helpers or local text files in the
expected format.
- Encode and split with `data_process(...)`, then build a config with
`generate_config(...)`, then call `model_initialize(**config)` or
`model_pretrained(...)`.
- Keep the task/module aligned:
  - DTI uses both drug and target inputs
  - compound property uses drug-only inputs
  - DDI uses `X_drug` plus `X_drug_`
  - PPI uses `X_target` plus `X_target_`
  - protein function uses target-only inputs
- For repurposing or screening, prefer the existing helpers:
  `DTI.repurpose`, `DTI.virtual_screening`, `CompoundPred.repurpose`, and
  `oneliner.repurpose` or `oneliner.virtual_screening`.
- Warn when a step triggers network downloads. Dataset helpers and pretrained
  model helpers fetch remote files.
- Distinguish static validation from runtime validation. `DeepPurpose/utils.py`
  imports heavy dependencies immediately, so a real import needs RDKit, PyTorch,
  Descriptastorus, and related packages installed first.

## Source Files

Use these local files as the primary source of truth when present:

- `README.md`
- `requirements.txt`
- `environment.yml`
- `setup.py`
- `DeepPurpose/utils.py`
- `DeepPurpose/dataset.py`
- `DeepPurpose/oneliner.py`
- `DeepPurpose/DTI.py`
- `DeepPurpose/CompoundPred.py`
- `DeepPurpose/DDI.py`
- `DeepPurpose/PPI.py`
- `DeepPurpose/ProteinPred.py`
- `toy_data/`
- `DEMO/`
