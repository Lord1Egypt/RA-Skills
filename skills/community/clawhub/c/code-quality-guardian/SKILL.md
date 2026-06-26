---
name: code-quality-guardian
description: 代码质量检测器 - 检测代码异味、复杂度、安全漏洞、风格规范等 | Code Quality Guardian - Detect code smells, complexity, security vulnerabilities and style issues
homepage: https://github.com/kaiyuelv/code-quality-guardian
category: devops
tags:
  - code-quality
  - linting
  - security
  - python
  - javascript
  - static-analysis
  - ci-cd
version: 1.0.0
---

# 🛡️ Code Quality Guardian (代码质量守护者)

## Metadata

| Field | Value |
|-------|-------|
| **Name** | code-quality-guardian |
| **Display Name** | 代码质量守护者 |
| **Version** | 1.0.0 |
| **Category** | Development Tools |
| **Author** | ClawHub |
| **License** | MIT |

## Description

A comprehensive code quality analysis tool supporting Python, JavaScript, and Go. It automatically detects code smells, complexity issues, security vulnerabilities, and style violations.

一款全面的代码质量分析工具，支持 Python、JavaScript 和 Go。自动检测代码异味、复杂度问题、安全漏洞和风格违规。

## Features

### English
- **Multi-language Support**: Python, JavaScript/TypeScript, Go
- **Code Smell Detection**: Identifies anti-patterns and design issues
- **Complexity Analysis**: Cyclomatic and maintainability metrics via Radon
- **Security Scanning**: Detect vulnerabilities with Bandit
- **Style Checking**: PEP8, ESLint, and Go fmt compliance
- **Comprehensive Reports**: JSON, HTML, and console output formats
- **CI/CD Integration**: Easy integration with pipelines
- **Configurable Rules**: Customizable thresholds and rule sets

### 中文
- **多语言支持**: Python、JavaScript/TypeScript、Go
- **代码异味检测**: 识别反模式和设计问题
- **复杂度分析**: 通过 Radon 进行圈复杂度和可维护性指标分析
- **安全扫描**: 使用 Bandit 检测安全漏洞
- **风格检查**: 符合 PEP8、ESLint 和 Go fmt 规范
- **综合报告**: JSON、HTML 和控制台输出格式
- **CI/CD 集成**: 易于集成到流水线
- **可配置规则**: 可自定义阈值和规则集

## Supported Languages

| Language | Tools Used | File Extensions |
|----------|------------|-----------------|
| Python | flake8, pylint, bandit, radon, mypy | .py |
| JavaScript/TypeScript | eslint, jshint | .js, .jsx, .ts, .tsx |
| Go | go vet, golint, staticcheck | .go |

## Usage

### Command Line Interface

```bash
# Analyze a Python project
code-quality-guardian analyze --path ./my-project --language python

# Analyze with specific tools only
code-quality-guardian analyze --path ./src --tools flake8,bandit

# Generate HTML report
code-quality-guardian analyze --path . --format html --output report.html

# Check specific complexity threshold
code-quality-guardian analyze --path . --max-complexity 10
```

### Python API

```python
from code_quality_guardian import QualityAnalyzer

# Initialize analyzer
analyzer = QualityAnalyzer(
    language='python',
    tools=['flake8', 'pylint', 'bandit'],
    config_path='.quality.yml'
)

# Run analysis
results = analyzer.analyze('./src')

# Generate report
report = results.to_json()
print(f"Issues found: {results.total_issues}")
print(f"Complexity score: {results.complexity_score}")
```

### Configuration File (.quality.yml)

```yaml
language: python
tools:
  - flake8
  - pylint
  - bandit
  - radon

thresholds:
  max_complexity: 10
  max_line_length: 100
  min_score: 8.0

ignore:
  - "*/tests/*"
  - "*/migrations/*"
  - "*/venv/*"

flake8:
  max_line_length: 100
  ignore: [E501, W503]

pylint:
  disable: [C0103, R0903]

bandit:
  severity: MEDIUM
  confidence: MEDIUM
```

## Installation

```bash
# Install from ClawHub
clawhub install code-quality-guardian

# Or install dependencies manually
pip install -r requirements.txt
```

## Requirements

- Python 3.8+
- flake8 >= 6.0.0
- pylint >= 2.17.0
- bandit >= 1.7.0
- radon >= 6.0.0
- mypy >= 1.0.0 (optional)

## Report Types

### Console Output (Default)
```
═══════════════════════════════════════════
   Code Quality Guardian v1.0.0
═══════════════════════════════════════════

📁 Project: my-project
🔤 Language: python
📊 Files analyzed: 42

┌─────────────────────────────────────────┐
│ Issues Summary                          │
├─────────────────────────────────────────┤
│ 🔴 Critical    0                        │
│ 🟠 High        2                        │
│ 🟡 Medium      8                        │
│ 🔵 Low         15                       │
│ 💡 Info        23                       │
├─────────────────────────────────────────┤
│ Total: 48                               │
└─────────────────────────────────────────┘

Complexity: 7.2/10 (Good)
Maintainability: A
Security Score: 95%
```

### JSON Output
```json
{
  "summary": {
    "files_analyzed": 42,
    "total_issues": 48,
    "critical": 0,
    "high": 2,
    "medium": 8,
    "low": 15,
    "info": 23
  },
  "metrics": {
    "complexity": 7.2,
    "maintainability": "A",
    "security_score": 95
  },
  "issues": [...]
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No issues found |
| 1 | Issues found but within thresholds |
| 2 | Threshold exceeded |
| 3 | Configuration error |
| 4 | Tool execution error |

## Integrations

### GitHub Actions
```yaml
- name: Code Quality Check
  uses: clawhub/code-quality-guardian@v1
  with:
    language: python
    path: ./src
    fail-on: high
```

### Pre-commit Hook
```yaml
repos:
  - repo: https://github.com/clawhub/code-quality-guardian
    rev: v1.0.0
    hooks:
      - id: quality-guardian
        args: ['--language', 'python']
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## Changelog

### v1.0.0
- Initial release
- Support for Python, JavaScript, Go
- Multi-format reporting
- CI/CD integration support
