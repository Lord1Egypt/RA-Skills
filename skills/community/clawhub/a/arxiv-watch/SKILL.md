---
name: arxiv-watcher
description: Monitor new papers on arXiv by category. Use when user wants to check latest papers, track research topics, or manage reading lists. Trigger phrases: "check arxiv", "new papers", "arxiv category", "watch arxiv", "latest papers on".
---

# ArXiv Watcher

Monitor and track new papers on arXiv.org by category.

## Overview

This skill helps you:
- Fetch latest papers from specific arXiv categories
- Generate formatted Markdown summaries
- Star/bookmark papers for later reading

## Quick Start

```
# Check latest papers in a category
/arxiv-watcher cs.AI

# Multiple categories
/arxiv-watcher cs.AI cs.CL cs.LG

# View starred papers
/arxiv-watcher --starred
```

## Available Categories

### Computer Science (cs.*)
| Category | Description |
|----------|-------------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language |
| cs.CV | Computer Vision |
| cs.LG | Machine Learning |
| cs.NE | Neural and Evolutionary Computing |
| cs.RO | Robotics |
| cs.SE | Software Engineering |

### Physics (physics.*)
| Category | Description |
|----------|-------------|
| astro-ph | Astrophysics |
| cond-mat | Condensed Matter |
| hep-ex | High Energy Physics - Experiment |
| hep-th | High Energy Physics - Theory |
| quant-ph | Quantum Physics |

### Mathematics (math.*)
| Category | Description |
|----------|-------------|
| math.AG | Algebraic Geometry |
| math.CO | Combinatorics |
| math.DG | Differential Geometry |
| math.NT | Number Theory |
| math.ST | Statistics Theory |

### Statistics (stat.*)
| Category | Description |
|----------|-------------|
| stat.ML | Machine Learning |
| stat.TH | Statistics Theory |

Full category list: https://arxiv.org/category_taxonomy

## Commands

### Fetch Latest Papers

```bash
python scripts/arxiv_watcher.py fetch <category> [--limit N]
```

Fetches recent papers from arXiv. Outputs Markdown format with:
- Paper title and arXiv ID
- Authors
- Abstract preview (first 200 chars)
- Link to full paper

### Star Papers

```bash
python scripts/arxiv_watcher.py star <arxiv_id>
```

Adds a paper to starred list for later reference.

### Unstar Papers

```bash
python scripts/arxiv_watcher.py unstar <arxiv_id>
```

Removes a paper from starred list.

### View Starred Papers

```bash
python scripts/arxiv_watcher.py starred
```

Lists all starred papers with their details.

## Output Format

Papers are displayed in Markdown format:

```markdown
## [2403.12345] Paper Title Here

**Authors:** John Doe, Jane Smith
**Category:** cs.AI
**Submitted:** 2024-03-15

**Abstract:**
This paper presents a novel approach to...

**Links:**
- arXiv: https://arxiv.org/abs/2403.12345
- PDF: https://arxiv.org/pdf/2403.12345.pdf

---
```

Starred papers include a ⭐ marker for easy identification.

## Workflow

When user asks to check arXiv:

1. **Identify categories** - Parse user request for category names
2. **Fetch papers** - Run `arxiv_watcher.py fetch <category>`
3. **Format output** - Present papers in readable Markdown
4. **Offer actions** - Ask if user wants to star any papers

### Example Interactions

**User:** "check new papers in cs.AI"

**Assistant:** Runs fetch command, displays 5-10 recent papers, asks if any should be starred.

**User:** "star the second one"

**Assistant:** Parses the arxiv_id from previous output, runs star command, confirms action.

**User:** "show my starred papers"

**Assistant:** Runs starred command, displays list with details.

## Resources

### scripts/
- `arxiv_watcher.py` - Main CLI for fetching and managing papers

### assets/
- `starred.json` - Persistent storage for starred papers (auto-created)
