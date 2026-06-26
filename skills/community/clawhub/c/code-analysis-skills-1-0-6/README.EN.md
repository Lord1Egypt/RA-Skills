# 📊 Code Analysis Skills

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-orange)](skill.yaml)

A comprehensive Git repository analysis tool that scans repositories and generates multi-dimensional developer insight reports — covering **commit patterns**, **work habits**, **development efficiency**, **code style**, **code quality**, **slacking index**, and **developer evaluations**. Supports Markdown, JSON, HTML, and PDF output formats.

---

## ✨ Features

- 🔍 **Repository Scanning** — Analyze a single Git repo or recursively discover all `.git` repos under a directory
- 📝 **Commit Patterns** — Frequency, size distribution, merge ratio, commit message quality
- ⏰ **Work Habits** — Working hours distribution, weekend/late-night coding ratio, consecutive coding streaks
- 🚀 **Dev Efficiency** — Code churn rate, rework ratio, Bus Factor, file ownership
- 🎨 **Code Style** — Language distribution, Conventional Commits compliance, file classification
- 🔎 **Code Quality** — Bug fix ratio, revert frequency, large commit ratio, test coverage, Python complexity (via radon)
- 🐟 **Slacking Index** — Composite score from 7 behavioral signals (sparsity, trivial commits, disappearance, low output, etc.)
- 🏆 **Developer Evaluation** — Weighted 6-dimension scoring (S/A/B/C/D/E/F grades), honest strengths/weaknesses, actionable suggestions
- 📊 **Leaderboards** — Developer score ranking + slacking index ranking
- 👥 **Multi-Developer Comparison** — Side-by-side comparison tables across all dimensions
- 📄 **Multiple Output Formats** — Markdown, JSON, styled HTML, and PDF reports (can generate multiple simultaneously)

## 📦 Installation

### Prerequisites

- Python 3.9+
- Git

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install gitpython pydriller radon tabulate jinja2 click pyyaml reportlab
```

For higher quality PDF output, optionally install:

```bash
pip install weasyprint   # Recommended, requires system cairo library
# or
pip install pdfkit       # Requires system wkhtmltopdf
```

## 🚀 Usage

### Basic Commands

```bash
# Analyze a single repository (all contributors)
python -m src.main -r /path/to/repo

# Recursively scan a directory for all Git repos
python -m src.main -r /path/to/projects --scan-all

# Compare specific developers
python -m src.main -r /path/to/repo -a "Alice" -a "Bob"

# Filter by date range
python -m src.main -r /path/to/repo -s 2024-01-01 -u 2024-12-31

# Generate HTML report
python -m src.main -r /path/to/repo -f html -o report.html

# Generate Markdown + HTML + PDF simultaneously
python -m src.main -r /path/to/repo -f "markdown,html,pdf" -o report

# Generate PDF report
python -m src.main -r /path/to/repo -f pdf -o report.pdf

# Save Markdown report to file
python -m src.main -r /path/to/repo -o report.md
```

### CLI Options

| Option | Description | Default |
|---|---|---|
| `-r, --repo` | Path to Git repo or parent directory | *(required)* |
| `--scan-all` | Recursively scan for all `.git` repos | `false` |
| `-a, --author` | Author name/email to analyze (repeatable) | All contributors |
| `-s, --since` | Start date (ISO format: `YYYY-MM-DD`) | — |
| `-u, --until` | End date (ISO format: `YYYY-MM-DD`) | — |
| `-b, --branch` | Branch to analyze | Current branch |
| `-f, --format` | Output format(s): `markdown`, `json`, `html`, `pdf` (comma-separated for multiple) | `markdown` |
| `-o, --output` | Output file path (base name for multiple formats) | stdout |

## 📁 Project Structure

```
code-analysis-skills/
├── src/
│   ├── main.py                 # CLI entry point
│   ├── scanner.py              # Repository scanner (single & recursive)
│   ├── analyzers/
│   │   ├── base_analyzer.py    # Base analyzer with Git traversal & author filtering
│   │   ├── commit_analyzer.py  # Commit pattern analysis
│   │   ├── work_habit_analyzer.py  # Work habit analysis
│   │   ├── efficiency_analyzer.py  # Development efficiency analysis
│   │   ├── code_style_analyzer.py  # Code style analysis
│   │   ├── code_quality_analyzer.py # Code quality analysis
│   │   └── slacking_analyzer.py # Slacking index analysis
│   ├── evaluator/
│   │   └── developer_evaluator.py  # Developer evaluation engine
│   ├── reporters/
│   │   ├── base_reporter.py    # Reporter base class
│   │   ├── markdown_reporter.py # Markdown report generator
│   │   ├── json_reporter.py    # JSON report generator
│   │   ├── html_reporter.py    # Styled HTML report generator
│   │   └── pdf_reporter.py     # PDF report generator
│   └── utils/
│       └── helpers.py          # Utility functions
├── tests/
│   ├── test_analyzers.py       # Analyzer unit tests
│   └── test_scanner.py         # Scanner unit tests
├── references/
│   └── metrics-guide.md        # Metrics definitions & healthy ranges
├── SKILL.md                    # ClawHub skill definition
├── skill.yaml                  # Skill configuration
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project metadata
└── pytest.ini                  # Test configuration
```

## 📊 Analysis Dimensions

### 1. 📝 Commit Patterns
- Commit frequency (daily/weekly)
- Commit size (lines added/deleted per commit)
- Merge commit ratio
- Commit message quality score

### 2. ⏰ Work Habits
- Working hours heatmap (hourly distribution)
- Weekend coding percentage
- Late-night coding percentage (22:00–06:00)
- Maximum consecutive coding days

### 3. 🚀 Development Efficiency
- Code churn rate (lines deleted / lines added)
- Rework ratio (changes to recently modified files)
- Bus Factor (how many developers own most of the codebase)
- File ownership distribution

### 4. 🎨 Code Style
- Programming language distribution
- Conventional Commits compliance rate
- File type classification (source / test / config / docs)

### 5. 🔍 Code Quality
- Bug fix commit ratio
- Revert commit frequency
- Large commit ratio (potential code smell)
- Test file coverage ratio
- Python code complexity (Cyclomatic Complexity via radon)

### 6. 🐟 Slacking Index
- Composite score (0-100) from 7 behavioral signals
- Signals: sparsity, trivial commits, disappearance, low output, non-code commits, procrastination, copy-paste
- Levels: 🔥 Workaholic → ✅ Normal → 😏 Suspicious → 🐟 Slacker → 🏆 Professional Slacker

### 7. 🏆 Developer Evaluation
- Weighted 6-dimension scoring (commit discipline 15% + work consistency 15% + efficiency 20% + code quality 25% + style 10% + engagement 15%)
- Grades: S / A / B / C / D / E / F
- Honest, blunt strengths and weaknesses
- Actionable improvement suggestions
- One-line verdict

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_analyzers.py
```

## ⚠️ Notes

- Analyzing large repositories (100K+ commits) may take a long time — consider limiting the date range
- Python complexity analysis requires `radon` and only applies to `.py` files
- Author matching supports fuzzy matching (name or email substring match)
- Directory scanning defaults to a maximum depth of 5 levels to avoid deep recursion
- PDF generation prioritizes weasyprint, falls back to pdfkit, then reportlab
- Evaluation results are based solely on Git commit history and do not represent a developer's full capabilities
- Slacking index is for reference only and should be understood in context

## ⚠️ Privacy & Data Security Notice

> **Important**: This tool extracts personal developer activity data from Git commit history, including timestamps, frequencies, and behavioral patterns.

**Before using, please ensure:**

- ✅ This tool runs **entirely locally** and does not transmit any data to external servers
- ⚠️ **Obtain informed consent** from relevant developers before analyzing their repositories
- 🚫 Analysis results **should not be directly used** for performance reviews, compensation decisions, or punitive management
- 🔒 Generated reports contain personal information — **store securely** and do not share publicly
- 📋 Ensure compliance with your organization's HR policies and local data protection regulations (e.g., GDPR)

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
