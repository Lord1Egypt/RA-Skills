# Biomni Data Lake Usage Guide

**Version:** v2.0
**Updated:** 2026-03-13

---

## ⚠️ Storage Path Rules (Mandatory)

### Root Directory `/` - Critically Low Space

```
/dev/mapper/ubuntu--vg-ubuntu--lv   98G   85G  8.5G  91% /
```

**❌ Strictly Prohibited:**
- ❌ Installing any software packages to the root directory
- ❌ Downloading large data files to the root directory
- ❌ Generating temporary files in the root directory
- ❌ Any file cleanup without explicit user permission

### Data Lake Path - Only Recommended Location

**✅ Data Lake:** `/home/data/biomni_data_lake/` (7.2TB, 13% used)

**✅ Temporary Output:** `/home/data/biomni_data_lake/temp/`

**✅ Workspace:** `/home/biolims/.openclaw/workspace/` (config files and small scripts only)

---

## Core Principles

1. **Use Biomni Agent first** → `agent.go("task description")`
2. **Fall back on failure** → Read from local data lake directly
3. **External API last** → UniProt/NCBI etc.

**❌ Prohibited:** Skipping Biomni and querying external sources directly

---

## Official Usage

```python
from biomni.agent import A1

agent = A1(
    path='/home/data/biomni_data_lake',
    llm='qwen3.5-plus',
    source='Custom',
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    api_key='your-api-key',
    timeout_seconds=1800
)

# Execute task
agent.go("Analyze HER2 gene expression in breast cancer")
```

---

## Space Monitoring

**Check commands:**
```bash
# Root directory (should stay <90%)
df -h /

# Data lake (ample space)
df -h /home/data

# Data lake file count
ls /home/data/biomni_data_lake/ | wc -l
```

**Alert thresholds:**
- Root directory > 90%: 🚨 Stop writing immediately
- Root directory > 95%: 🔥 Emergency cleanup

---

## API Failure Handling Strategy

| Failure Type | Affected Databases | Action |
|-------------|-------------------|--------|
| API auth failure | ChEMBL, STRING | Skip, try other databases |
| Parameter error | UniProt, cBioPortal | Remove parameters and retry |
| Missing module | PubMed | Install or skip |
| Network unreachable | Google Search | Use local data lake |

---

## Local Data Lake Files (Fallback)

```python
import pandas as pd
DATA_LAKE = '/home/data/biomni_data_lake'

# Disease - Gene associations
disgenet = pd.read_parquet(f'{DATA_LAKE}/DisGeNET.parquet')

# Tissue expression
gtex = pd.read_parquet(f'{DATA_LAKE}/gtex_tissue_gene_tpm.parquet')

# CRISPR dependency
depmap = pd.read_csv(f'{DATA_LAKE}/DepMap_CRISPRGeneDependency.csv')

# GWAS associations
gwas = pd.read_pickle(f'{DATA_LAKE}/gwas_catalog.pkl')

# Knowledge graph
kg = pd.read_csv(f'{DATA_LAKE}/kg.csv')

# Drug binding
bindingdb = pd.read_csv(f'{DATA_LAKE}/BindingDB_All_202409.tsv', sep='\t')
```

---

## Main Data Files

| File | Size | Purpose |
|------|------|---------|
| genebass_*.pkl | ~4.7GB | Variant population frequency |
| kg.csv | 937MB | Knowledge graph |
| DepMap_*.csv | ~900MB | Gene expression/CRISPR |
| sgRNA_*.txt | ~720MB | sgRNA library |
| BindingDB_*.tsv | 122MB | Compound - Target |
| gwas_catalog.pkl | 174MB | GWAS |
| DisGeNET.parquet | 3MB | Disease - Gene |

---

**Back to:** `../MEMORY.md`
