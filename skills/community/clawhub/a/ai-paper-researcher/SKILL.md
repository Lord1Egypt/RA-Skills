---
name: ai-paper-researcher
description: An arXiv paper search engine designed specifically for scientific researchers. Supports dual modes: "Broad Search" and "Top-Tier Strict Filtering", along with relevance and date sorting. Automatically checks for duplicates, downloads PDFs, and maintains a local CSV paper library.
---

# AI Academic Paper Researcher

## 1. Skill Positioning & Core Objective
This skill aims to assist researchers in the AI field by searching for arXiv literature and automating PDF downloads and local file management.
**Core Principle:** All download records must rely on the local `workspace/paper_list/paper_list.csv` for deduplication to prevent repeated downloads.

## 2. Tools & Dependencies
- **Execution Script:** `python arxiv_tool.py`
- **Target Conference List:** The `target.csv` file located in the same directory as this skill (contains the names of top-tier conferences or journals the user follows, e.g., CVPR, NeurIPS, ICLR).

## 3. Sorting Strategy Selection
Before executing any search, you must decide which sorting parameter (`--sort`) to use based on the user's intent:
- **Searching for Classic Theories / Well-known Algorithms (Classic/Influential):** If the user searches for specific well-known algorithms (e.g., "Adam", "ResNet") or foundational papers in core fields, you **MUST use `--sort relevance`**. Otherwise, because arXiv defaults to returning a large number of newly submitted papers, classic older papers will be pushed out of the search results.
- **Tracking Latest Frontiers (Latest Trends):** If the user explicitly requests "latest", "this year", or "recent weeks" papers, please use `--sort date`.

## 4. Two Retrieval Modes
Infer the required mode based on the user's query:

### Mode A: Broad Search (All Relevant Mode)
**Trigger Condition:** The user only provides a research direction without restricting the papers to be published in top-tier conferences.
**Execution Logic:**
1. Run `python arxiv_tool.py search "[query]" --max 15 --sort [selected sorting strategy]`.
2. Ignore the `comment` field in the JSON response.
3. Exclude papers where `is_downloaded: true` in the results.
4. Select the papers most relevant to the user's needs and proceed directly to the download process.

### Mode B: Top-Tier Conference/Journal Strict Filtering (Top-Tier Verification Mode)
**Trigger Condition:** The user explicitly requests "top-tier conferences", "top journals", or specifies certain conferences (e.g., "Help me find Adam-related papers from past ICLR conferences").
**Execution Logic:**
1. **Read Target List:** Use the file reading tool to view the contents of `target.csv` to get the list of target conferences/journals.
2. **Initial Search:** Run `python arxiv_tool.py search "[query]" --max 30 --sort [selected sorting strategy]`. *(Note: The script automatically fetches the latest version of the paper, so if it has been accepted by a top conference, the comment will contain the relevant information.)*
3. **LLM Semantic Verification (CRITICAL):**
   - Carefully review the `comment` field in the JSON of each candidate paper.
   - Determine whether any conference listed in `target.csv` is present in the `comment`.
   - **Note on Variations:** Be tolerant of abbreviations, year suffixes, or non-standard formatting of conference names when matching (e.g., `Accepted to ICLR 2015`, `NeurIPS'23`, `Appears in CVPR`). As long as it semantically refers to the target conference, consider it a successful match.
   - If the `comment` is empty, or does not contain a publication statement for the target conference, you **MUST exclude** the paper.
4. Exclude already downloaded papers (`is_downloaded: true`).
5. Proceed to the download process for the successfully verified papers.

## 5. Download & File Persistence
1. For the filtered papers, execute the download command one by one: `python arxiv_tool.py download [arxiv_id]`.
2. Collect the script's return results.

## 6. Reporting Standard
After completing the search and download, report the final results to the user:
- Explicitly state which retrieval mode was used (Mode A/B) and which sorting method (Date/Relevance).
- List the successfully downloaded papers (Format: `[ArXiv ID] Title - (Matched conference, if any)`).