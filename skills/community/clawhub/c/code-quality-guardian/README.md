# 🛡️ Code Quality Guardian

> 自动化代码质量检测工具 | Automated Code Quality Analysis Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 目录 (Table of Contents)

- [功能特性](#功能特性-features)
- [快速开始](#快速开始-quick-start)
- [安装](#安装-installation)
- [使用方法](#使用方法-usage)
- [配置](#配置-configuration)
- [报告输出](#报告输出-reports)
- [API 文档](#api-文档-api-documentation)
- [CI/CD 集成](#cicd-集成)

---

## 功能特性 (Features)

### 🔍 多语言支持 (Multi-language)
- **Python**: flake8, pylint, bandit, radon, mypy
- **JavaScript/TypeScript**: eslint, jshint
- **Go**: go vet, golint, staticcheck

### 📊 检测维度 (Detection Dimensions)
| 维度 | 描述 | 工具 |
|------|------|------|
| 代码风格 | PEP8, ESLint, Go fmt 规范检查 | flake8, eslint |
| 代码异味 | 反模式、不良设计实践 | pylint, radon |
| 复杂度 | 圈复杂度、可维护性指数 | radon, xenon |
| 安全漏洞 | 常见安全问题扫描 | bandit, safety |
| 类型检查 | 静态类型分析 | mypy, pyright |

### 📈 报告格式 (Report Formats)
- 控制台彩色输出 (Console with colors)
- JSON 格式 (Machine readable)
- HTML 报告 (Interactive dashboard)
- Markdown 报告 (Documentation friendly)

---

## 快速开始 (Quick Start)

```bash
# 1. 克隆项目
cd /root/.openclaw/workspace/skills/code-quality-guardian

# 2. 安装依赖
pip install -r requirements.txt

# 3. 分析项目
python -m code_quality_guardian analyze --path /path/to/your/project --language python

# 4. 查看 HTML 报告
python -m code_quality_guardian analyze --path . --format html --output report.html
```

---

## 安装 (Installation)

### 从源码安装

```bash
git clone <repository-url>
cd code-quality-guardian
pip install -r requirements.txt
pip install -e .
```

### 作为 ClawHub Skill 安装

```bash
clawhub install code-quality-guardian
```

---

## 使用方法 (Usage)

### 命令行工具 (CLI)

#### 基础用法
```bash
# 分析当前目录的 Python 代码
quality-guardian analyze

# 分析指定路径
quality-guardian analyze --path ./src

# 指定语言
quality-guardian analyze --path ./src --language python

# 使用特定工具
quality-guardian analyze --tools flake8,bandit

# 生成 HTML 报告
quality-guardian analyze --format html --output report.html
```

#### 高级选项
```bash
# 设置复杂度阈值
quality-guardian analyze --max-complexity 10

# 忽略特定文件/目录
quality-guardian analyze --ignore "tests/*,migrations/*"

# 设置最低质量分数
quality-guardian analyze --min-score 8.0

# 详细输出
quality-guardian analyze --verbose

# 静默模式 (仅返回退出码)
quality-guardian analyze --quiet
```

### Python API

```python
from code_quality_guardian import QualityAnalyzer, Config

# 基础用法
analyzer = QualityAnalyzer()
results = analyzer.analyze('./my-project')
print(results.summary())

# 使用配置
config = Config(
    language='python',
    max_complexity=10,
    ignore_patterns=['tests/*', 'venv/*']
)
analyzer = QualityAnalyzer(config=config)
results = analyzer.analyze('./src')

# 自定义工具
analyzer = QualityAnalyzer(tools=['flake8', 'bandit'])
results = analyzer.analyze('./src')

# 生成不同格式报告
results.to_console()
results.to_json('report.json')
results.to_html('report.html')
```

---

## 配置 (Configuration)

### 配置文件 (.quality.yml)

在项目根目录创建 `.quality.yml`：

```yaml
# 语言设置
language: python

# 启用工具
tools:
  - flake8
  - pylint
  - bandit
  - radon

# 全局阈值
thresholds:
  max_complexity: 10
  max_line_length: 100
  min_quality_score: 8.0

# 忽略模式
ignore:
  - "*/tests/*"
  - "*/migrations/*"
  - "*/venv/*"
  - "*/__pycache__/*"

# 工具特定配置
flake8:
  max_line_length: 100
  ignore:
    - E501  # Line too long
    - W503  # Line break before binary operator
  select:
    - E
    - W
    - F

pylint:
  disable:
    - C0103  # Invalid name
    - R0903  # Too few public methods
  enable:
    - W0614  # Unused import

bandit:
  severity: MEDIUM  # LOW, MEDIUM, HIGH
  confidence: MEDIUM
  skips:
    - B101  # Use of assert

radon:
  cc_min: A  # Cyclomatic complexity minimum rank
  mi_min: B  # Maintainability index minimum rank
```

### 环境变量

```bash
export QUALITY_GUARDIAN_CONFIG=/path/to/config.yml
export QUALITY_GUARDIAN_LOG_LEVEL=DEBUG
export QUALITY_GUARDIAN_PARALLEL=true
```

---

## 报告输出 (Reports)

### 控制台输出示例

```
═══════════════════════════════════════════════════
       🔍 Code Quality Guardian v1.0.0
═══════════════════════════════════════════════════

📁 Project: my-awesome-project
🔤 Language: python
📊 Files analyzed: 42
🔧 Tools used: flake8, pylint, bandit, radon

┌─────────────────────────────────────────────────┐
│              📋 Issues Summary                   │
├─────────────────────────────────────────────────┤
│ 🔴 Critical (安全漏洞)         0                │
│ 🟠 High (严重问题)             2                │
│ 🟡 Medium (中等问题)           8                │
│ 🔵 Low (轻微问题)             15                │
│ 💡 Info (建议)                23                │
├─────────────────────────────────────────────────┤
│ Total Issues: 48                                │
└─────────────────────────────────────────────────┘

📊 Quality Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Complexity Score:     7.2/10  ●●●●●●●○○○  Good
  Maintainability:      A       ●●●●●●●●●●  Excellent
  Security Score:       95%     ●●●●●●●●●●  Safe
  Style Compliance:     87%     ●●●●●●●●○○  Good
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Quality Gate: PASSED
```

### JSON 输出示例

```json
{
  "meta": {
    "version": "1.0.0",
    "timestamp": "2026-03-20T16:45:00Z",
    "duration_ms": 2456
  },
  "summary": {
    "project_name": "my-awesome-project",
    "language": "python",
    "files_analyzed": 42,
    "lines_of_code": 3847,
    "tools_used": ["flake8", "pylint", "bandit", "radon"]
  },
  "issues": {
    "total": 48,
    "by_severity": {
      "critical": 0,
      "high": 2,
      "medium": 8,
      "low": 15,
      "info": 23
    },
    "by_category": {
      "style": 25,
      "complexity": 8,
      "security": 2,
      "maintainability": 13
    }
  },
  "metrics": {
    "complexity": {
      "average": 7.2,
      "max": 18,
      "score": 72
    },
    "maintainability": {
      "index": 85.3,
      "rank": "A"
    },
    "security": {
      "score": 95,
      "vulnerabilities": 2
    }
  },
  "quality_gate": {
    "status": "PASSED",
    "threshold": 8.0,
    "actual": 8.4
  }
}
```

---

## API 文档 (API Documentation)

### QualityAnalyzer 类

```python
class QualityAnalyzer:
    """
    代码质量分析器主类
    
    Args:
        language: 目标语言 ('python', 'javascript', 'go')
        tools: 要使用的工具列表
        config: 配置对象或配置文件路径
    """
    
    def analyze(self, path: str) -> AnalysisResult:
        """
        分析指定路径的代码
        
        Args:
            path: 要分析的目录或文件路径
            
        Returns:
            AnalysisResult: 分析结果对象
        """
        pass
```

### AnalysisResult 类

```python
class AnalysisResult:
    """分析结果类"""
    
    @property
    def total_issues(self) -> int:
        """返回总问题数"""
        pass
    
    @property
    def complexity_score(self) -> float:
        """返回复杂度评分 (0-10)"""
        pass
    
    def to_json(self, path: str = None) -> str:
        """导出为 JSON 格式"""
        pass
    
    def to_html(self, path: str = None) -> str:
        """导出为 HTML 格式"""
        pass
    
    def to_console(self) -> None:
        """输出到控制台"""
        pass
```

---

## CI/CD 集成

### GitHub Actions

```yaml
name: Code Quality Check

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Code Quality Guardian
        run: |
          pip install -r requirements.txt
      
      - name: Run Quality Check
        run: |
          python -m code_quality_guardian analyze \
            --path ./src \
            --format json \
            --output quality-report.json
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.json
```

### GitLab CI

```yaml
quality_check:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python -m code_quality_guardian analyze --path . --format json
  artifacts:
    reports:
      codequality: quality-report.json
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: code-quality-guardian
        name: Code Quality Guardian
        entry: python -m code_quality_guardian analyze
        language: python
        pass_filenames: false
        always_run: true
```

---

## 📚 示例代码

详见 `examples/` 目录：

- `analyze_project.py` - 基础项目分析
- `custom_config.py` - 自定义配置
- `ci_integration.py` - CI/CD 集成示例

---

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

感谢以下开源项目：
- [flake8](https://flake8.pycqa.org/)
- [pylint](https://pylint.pycqa.org/)
- [bandit](https://bandit.readthedocs.io/)
- [radon](https://radon.readthedocs.io/)
