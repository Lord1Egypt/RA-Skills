# arXiv Survey

🔍 **Automatically Generate Survey Reports on arXiv Papers** | 自动生成arXiv论文调查报告

## Project Overview

arXiv Survey is an automated tool for retrieving, categorizing, and summarizing academic papers from the arXiv repository on specified topics and time ranges. The tool automatically:

- 🔎 Searches for relevant papers via arXiv API
- 📊 Categorizes papers by theme
- 🌐 Translates paper abstracts to Chinese
- 📝 Generates structured Markdown reports

## Features

✅ **Automatic Search**: Retrieve papers from arXiv API based on keywords  
✅ **Smart Categorization**: Automatically classify papers by title and abstract  
✅ **Chinese Translation**: Translate paper abstracts to fluent Chinese  
✅ **Structured Output**: Generate professional Markdown format reports  
✅ **Flexible Time Range**: Support time range from any year to present  

## Quick Start

### Basic Usage

```bash
./scripts/survey_arxiv.sh <year> <theme> [output_dir]
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `<year>` | Starting year | `2026` |
| `<theme>` | Research theme (English or Chinese) | `AI assisted open source contribution` |
| `[output_dir]` | Output directory (optional, default current dir) | `.` or `./reports` |

### Usage Examples

```bash
# Search for papers on AI-assisted open source contribution from 2026
./scripts/survey_arxiv.sh 2026 "AI assisted open source contribution"

# Search for papers on RAG from 2024
./scripts/survey_arxiv.sh 2024 "RAG retrieval augmented generation"

# Search for multimodal learning papers from 2025, output to reports directory
./scripts/survey_arxiv.sh 2025 "multimodal learning" ./reports
```

## Workflow

```
1. Search
   └─ Query arXiv API for papers matching the theme

2. Filter
   └─ Collect 10-50 relevant papers (more for popular topics)

3. Categorize
   └─ Automatically classify papers by title and abstract

4. Translate
   └─ Translate abstracts to Chinese

5. Generate Report
   └─ Create structured Markdown file
```

## Output Format

The script generates a Markdown file named `arxiv-survey-<year>-<theme-slug>.md`.

### Report Structure Example

```markdown
# ArXiv Survey: <Theme> (<Year>-Present)

## Table of Contents

### Category 1
- Paper Title 1
- Paper Title 2

### Category 2
- Paper Title 3

---

## Detailed Papers

### Category 1

#### Paper Title 1
**Authors**: Author List
**arXiv**: [Link](https://arxiv.org/abs/xxxx.xxxxx)
**Abstract (中文)**: Translated abstract...

#### Paper Title 2
...
```

## Project Structure

```
arxiv-survey/
├── README.md                    # English documentation (this file)
├── README.en.md                 # English version
├── README.zh.md                 # Chinese version
├── SKILL.md                     # Skill description
├── _meta.json                   # Project metadata
└── scripts/
    └── survey_arxiv.sh          # Main survey and report generation script
```

## System Requirements

- **Bash** shell environment
- **curl**: For HTTP requests to arXiv API
- **iconv**: For character encoding conversion
- **grep/sed**: For text processing

## Installation & Setup

1. **Clone or download the project**
   ```bash
   cd arxiv-survey
   ```

2. **Make script executable**
   ```bash
   chmod +x scripts/survey_arxiv.sh
   ```

3. **Verify dependencies**
   ```bash
   which curl iconv grep sed
   ```

## Usage Guide

### Basic Example

```bash
# Navigate to project directory
cd arxiv-survey

# Execute search
./scripts/survey_arxiv.sh 2026 "large language models"

# View generated report
cat arxiv-survey-2026-large-language-models.md
```

### Multiple Searches

```bash
# Create output directory
mkdir -p reports

# Survey multiple topics
./scripts/survey_arxiv.sh 2026 "large language models" ./reports
./scripts/survey_arxiv.sh 2025 "diffusion models" ./reports
./scripts/survey_arxiv.sh 2024 "graph neural networks" ./reports

# View all reports
ls -la reports/
```

## Paper Collection Range

- **Niche Topics**: ~10-20 papers
- **General Topics**: ~20-40 papers
- **Popular Topics**: May exceed 50 papers

Actual numbers depend on arXiv inventory and search keyword matching.

## Feature Details

### Automatic Categorization

The script automatically groups papers into related research domains or sub-topics based on titles and abstracts.

### Chinese Translation

All paper abstracts are translated to Chinese for quick understanding by Chinese-speaking users. If full paper access is available, translations may include additional contextual information.

### File Naming Convention

All output file names use English without Chinese characters for compatibility across operating systems.

## Troubleshooting

### curl: command not found
Install curl:
```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS
brew install curl

# Windows (with WSL)
sudo apt-get install curl
```

### iconv: command not found
Install iconv tools:
```bash
# Ubuntu/Debian
sudo apt-get install libc-bin

# macOS
brew install libiconv
```

### No search results
- Check network connection
- Try modifying search keywords with more common terms
- Ensure year setting is correct

## Related Resources

- **arXiv API Documentation**: https://arxiv.org/help/api/
- **arXiv Classification System**: https://arxiv.org/archive/
- **Search Syntax**: https://arxiv.org/help/arxiv-search

## License

MIT License - See LICENSE file in project root

## Author

OpenClaw Workspace

## Version

v1.0.0

## Changelog

### v1.0.0 (Initial Release)
- ✨ Implement basic paper search and categorization
- ✨ Support Chinese abstract translation
- ✨ Generate structured Markdown reports
- ✨ Support custom output directory

## Contributing

Issues and feature requests are welcome!

## Notes

1. **API Rate Limiting**: The arXiv API has rate limits; avoid excessively frequent requests
2. **Translation Quality**: Automatic translations may require manual review
3. **Paper Freshness**: Reports reflect the latest published papers at generation time

---

**Need help?** Check SKILL.md for detailed skill description and workflow information.
