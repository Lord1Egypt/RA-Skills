---
name: document-workflow
description: Academic paper research workflow. Use when searching, downloading, or analyzing arXiv papers. Triggers: "search papers", "download paper", "arxiv", "latex source", "paper summary", "read paper".
---

# Document Workflow

Academic paper research: **Search → Download LaTeX → Read & Summarize**

---

## Quick Start

### 1. Search Papers
```bash
python -m skills.document-workflow.scripts.search_papers --query "world model" --max_results 5 --year_from 2024
```

### 2. Download LaTeX Source
```bash
python -m skills.document-workflow.scripts.latex_reader "2301.07088" --keep
```

### 3. Read & Summarize

```
Read the LaTeX source files and summarize following the reading guide below.
```

---

## Reading Guide

After downloading LaTeX source to `arxiv_{id}/`, read the `.tex` files in this order:

### Step 1: Get Metadata
Read the **main .tex file** (usually `main.tex`, `root.tex`, or `{paper-id}.tex`) for:
- `\title{}` - Paper title
- `\author{}` - Authors
- `\begin{abstract}...\end{abstract}` - Abstract

### Step 2: Understand the Problem
Read the **Introduction section** (usually `intro.tex`, `1-introduction.tex`, or first `\section`):
- What problem does this paper solve?
- What are the key contributions?
- How does it relate to prior work?

### Step 3: Understand the Method
Read the **Method/Approach section**:
- What is the proposed approach?
- Key equations in `\begin{equation}...\end{equation}` or `\begin{align}...\end{align}`
- Algorithm pseudocode in `\begin{algorithm}...\end{algorithm}`

### Step 4: Check Experiments
Read the **Experiments section**:
- Datasets used
- Baselines compared
- Metrics in `\begin{table}...\end{table}` with results
- Key findings

### Step 5: Check References

Read the `.bib` or `.bbl` file for:
- Related work citations
- Key papers in the field

---

## Output Schema

Summarize the paper in this JSON format(see more details in `./references/output_schema.json`):

```json
{
  "paper_title": "Full title",
  "authors": ["Author 1", "Author 2"],
  "source": "arXiv:XXXX.XXXXX",
  "task_definition": {
    "domain": "Research domain",
    "task": "Specific task",
    "problem_statement": "What problem this paper solves",
    "key_contributions": ["Contribution 1", "Contribution 2"]
  },
  "experiments": {
    "datasets": ["Dataset 1", "Dataset 2"],
    "baselines": ["Baseline 1", "Baseline 2"],
    "metrics": [
      {"name": "Metric name", "description": "What it measures","definition":"Mathematical definition or formula for the metric"}
    ],
    "results": [
      {"setting": "Dataset", "metric": "Metric", "proposed_method": "Score", "best_baseline": "Score"}
    ],
    "key_findings": ["Finding 1", "Finding 2"]
  }
}
```



---

## Scripts

| Script | Function |
|--------|----------|
| `search_papers.py` | Search papers (Tavily + Semantic Scholar) |
| `download_paper.py` | Download PDF (for human reading) |
| `latex_reader.py` | Download LaTeX source (for AI reading) |

---

## Tips for Reading LaTeX

| LaTeX Command | Meaning |
|---------------|---------|
| `\section{Title}` | Section heading |
| `\subsection{Title}` | Subsection heading |
| `\textbf{text}` | Bold text (often important) |
| `\cite{key}` | Citation reference |
| `\begin{equation}...\end{equation}` | Numbered equation |
| `\begin{table}...\end{table}` | Table |
| `\begin{figure}...\end{figure}` | Figure |
| `\input{file}` or `\subfile{file}` | Include another .tex file |

---

## Config

```bash
# Optional: Semantic Scholar API key
export SEMANTIC_SCHOLAR_API_KEY="your-key"

# Default download path
C:\Users\Lenovo\Desktop\papers
```