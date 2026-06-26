<div align="center">

# 🧠 AI Academic Paper Researcher

**An intelligent, fully-automated arXiv research assistant designed for AI scientists and enthusiasts. Search, filter by top-tier conferences, download PDFs, and build your local library—all driven by natural language.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](https://choosealicense.com/licenses/mit-0/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-purple.svg)](#)

<br>

[**English**](./README.md) | [**简体中文**](./README_zh-CN.md)
</div>

---

## ✨ Why This Tool?

Navigating the ocean of daily arXiv submissions can be overwhelming. This tool acts as your personal academic scout. Whether you are a professional researcher tracking the latest advancements in specific subfields, or an enthusiast looking for foundational papers, this skill bridges the gap between raw arXiv data and curated, high-signal knowledge.

### 🚀 Key Features

- **🧠 Dual-Mode Intelligence**: 
  - **Broad Search**: Cast a wide net for the latest trends.
  - **Top-Tier Strict Filtering**: Uses LLM semantic verification to ensure papers were actually accepted to your target conferences (e.g., CVPR, NeurIPS, ICLR).
- **⏱️ Smart Sorting**: Automatically toggles between *Date* (for tracking new releases) and *Relevance* (for digging up classic/foundational algorithms).
- **🛡️ Domain Isolation**: Automatically appends AI-specific categories (`cs.CV`, `cs.LG`, `cs.AI`, etc.) to filter out noise from physics or biology.
- **📂 Local Library Management**: Silently downloads PDFs, standardizes file names, and logs everything into a local CSV to prevent duplicate downloads.
- **🛡️ Anti-Ban Protections**: Built-in exponential backoff and polite delays to handle arXiv's strict API rate limits (429 errors).

---

## 🧩 Architecture: How It Works

This skill is composed of several working parts that seamlessly integrate with your AI Agent (like OpenClaw):

| Component | Description | Role |
| :--- | :--- | :--- |
| **`SKILL.md`** | The "Brain" | Instructs the AI agent on how to interpret your queries, choose the right sorting strategy, and verify conference acceptances via the `comment` field. |
| **`arxiv_tool.py`** | The "Muscle" | A robust Python CLI tool that queries the arXiv API, handles HTTP streams, enforces rate limits, and downloads the PDFs. |
| **`target.csv`** | The "Filter" | A simple, user-defined list of top-tier venues you care about (e.g., `CVPR`, `ICCV`, `ICLR`). The LLM checks papers against this list. |
| **`paper_list.csv`** | The "Memory" | Automatically generated in your workspace. Tracks downloaded ArXiv IDs to ensure you never download the same paper twice. |

---

## 🛠️ Setup & Installation

**1. Install Dependencies**
Ensure you have the required Python packages installed in your environment:
```bash
pip install arxiv requests
```

**2. Directory Structure**
Ensure the files are placed correctly within your workspace:

```text
workspace/
├── paper_list/                  # Auto-generated: PDFs and paper_list.csv go here
└── skills/
    └── ai-paper-researcher/
        ├── SKILL.md             # The agent prompt
        ├── arxiv_tool.py        # The python script
        └── target.csv           # Your conference targets (e.g., CVPR, NeurIPS)
```

**3. Configure Targets**
Add your favorite conferences to `target.csv` (one per line):

```csv
target
CVPR
ICCV
NeurIPS
ICLR
```

---

## 🗣️ How to Use (Natural Language Prompting)

Once loaded into your AI agent, you can simply ask it to do the heavy lifting. Here are the best ways to prompt the system:

### 🔭 Scenario 1: Tracking the Latest Frontiers (Mode A)

*Perfect for weekly literature reviews in fast-moving domains.*

> "Invoke the `ai-paper-researcher` skill. Find the latest papers on **Agent security** from the past month. Sort by date, skip the top-tier conference filter, and download the most relevant ones to my workspace."

### 🏛️ Scenario 2: Deep Dive into Top-Tier Classics (Mode B)

*Perfect for finding foundational work that has been peer-reviewed and verified.*

> "Use the `ai-paper-researcher` skill. I want to research **Agent security**. Sort by relevance to find the most impactful papers. Strictly filter the results so you only download papers accepted to the venues listed in my `target.csv`. Give me a summary of what you downloaded."

### 🎯 Scenario 3: Precision Direct Download

*Perfect for grabbing specific papers you already know about without searching.*

> "Using the `ai-paper-researcher` skill, bypass the search and directly download the original Adam optimizer paper (ID: `1412.6980`) and the Focal Loss paper (ID: `1708.02002`)."

---

## 💻 CLI Usage (For Developers)

If you prefer to bypass the AI agent and use the terminal directly, the Python script is a fully functional standalone tool.

```bash
# Search for papers by relevance (returns JSON with comment fields)
python arxiv_tool.py search "diffusion models" --max 10 --sort relevance

# Search for the newest papers
python arxiv_tool.py search "diffusion models" --sort date

# Download a specific paper (handles naming and CSV logging automatically)
python arxiv_tool.py download 1412.6980
```

---

## 📜 Acknowledgments & License

This project was built upon the excellent foundational work from [Ractorrr/arxiv-mcp](https://github.com/Ractorrr/arxiv-mcp) (🔍 AI-powered arXiv research assistant). It has been heavily modified to remove database dependencies (MongoDB), introduce strict local file-system tracking, add LLM-driven semantic conference filtering, and implement robust streaming downloads to bypass arXiv API limitations.

**License:** [MIT License](https://choosealicense.com/licenses/mit/) - Free to use, modify, and distribute without attribution requirements.