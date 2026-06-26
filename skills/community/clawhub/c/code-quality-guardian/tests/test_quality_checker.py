#!/usr/bin/env python3
"""
Code Quality Guardian - 单元测试
单元测试模块

运行测试:
    pytest tests/test_quality_checker.py -v
    pytest tests/test_quality_checker.py -v --cov=src
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from code_quality_guardian import (
    QualityAnalyzer,
    Config,
    AnalysisResult,
    Issue,
    Severity,
    Category,
)
from code_quality_guardian.tools import (
    Flake8Runner,
    PylintRunner,
    BanditRunner,
    RadonRunner,
)
from code_quality_guardian.reports import ConsoleReporter, JsonReporter, HtmlReporter


# ============= Fixtures =============

@pytest.fixture
def temp_project():
    """创建临时项目目录结构"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试文件
        (Path(tmpdir) / "src").mkdir()
        (Path(tmpdir) / "tests").mkdir()

        # 创建一个质量良好的 Python 文件
        good_file = Path(tmpdir) / "src" / "good_module.py"
        good_file.write_text('''
"""这是一个良好的模块示例"""


def calculate_sum(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b


class Calculator:
    """简单的计算器类"""
    
    def __init__(self):
        self.history = []
    
    def add(self, x: float, y: float) -> float:
        """加法运算"""
        result = x + y
        self.history.append(f"{x} + {y} = {result}")
        return result
''')

        # 创建一个有问题的 Python 文件
        bad_file = Path(tmpdir) / "src" / "bad_module.py"
        bad_file.write_text('''
import os,sys  # E401: 一行多个导入

def complex_function(n):  # 高复杂度函数
    if n > 0:
        if n % 2 == 0:
            if n % 3 == 0:
                return "divisible by 6"
            return "even"
        else:
            if n % 3 == 0:
                return "divisible by 3"
            return "odd"
    return "zero or negative"

x=1  # E225: 缺少空格
unused_var = 42  # 未使用的变量

eval("1 + 1")  # B307: 危险的 eval 使用
''')

        # 创建配置文件
        config_file = Path(tmpdir) / ".quality.yml"
        config_file.write_text('''
language: python
tools:
  - flake8
  - bandit
  - radon
thresholds:
  max_complexity: 10
  max_line_length: 100
''')

        yield tmpdir


@pytest.fixture
def sample_issue():
    """创建示例问题"""
    return Issue(
        tool="flake8",
        severity=Severity.HIGH,
        category=Category.STYLE,
        message="Line too long (120 > 100 characters)",
        file="src/module.py",
        line=10,
        column=1,
        code="E501",
    )


@pytest.fixture
def mock_analysis_result():
    """创建模拟分析结果"""
    return AnalysisResult(
        files_analyzed=10,
        lines_of_code=500,
        total_issues=25,
        issues_by_severity={
            Severity.CRITICAL: 0,
            Severity.HIGH: 2,
            Severity.MEDIUM: 5,
            Severity.LOW: 10,
            Severity.INFO: 8,
        },
        issues_by_category={
            Category.STYLE: 12,
            Category.COMPLEXITY: 3,
            Category.SECURITY: 2,
            Category.MAINTAINABILITY: 8,
        },
        complexity_score=7.5,
        maintainability_rank="A",
        security_score=95,
        issues=[],
    )


# ============= Config Tests =============

class TestConfig:
    """配置类测试"""

    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        assert config.language == "python"
        assert "flake8" in config.tools
        assert config.thresholds["max_complexity"] == 10

    def test_custom_config(self):
        """测试自定义配置"""
        config = Config(
            language="python",
            tools=["flake8", "bandit"],
            thresholds={"max_complexity": 8},
        )
        assert config.tools == ["flake8", "bandit"]
        assert config.thresholds["max_complexity"] == 8

    def test_config_from_file(self, temp_project):
        """测试从文件加载配置"""
        config_path = Path(temp_project) / ".quality.yml"
        config = Config.from_file(str(config_path))
        assert config.language == "python"
        assert "bandit" in config.tools


# ============= Issue Tests =============

class TestIssue:
    """问题类测试"""

    def test_issue_creation(self, sample_issue):
        """测试问题对象创建"""
        assert sample_issue.tool == "flake8"
        assert sample_issue.severity == Severity.HIGH
        assert sample_issue.code == "E501"
        assert sample_issue.file == "src/module.py"
        assert sample_issue.line == 10

    def test_issue_to_dict(self, sample_issue):
        """测试转换为字典"""
        data = sample_issue.to_dict()
        assert data["tool"] == "flake8"
        assert data["severity"] == "HIGH"
        assert data["code"] == "E501"


# ============= Tool Runner Tests =============

class TestFlake8Runner:
    """Flake8 工具运行器测试"""

    @patch("subprocess.run")
    def test_flake8_parsing(self, mock_run):
        """测试 Flake8 输出解析"""
        # 模拟 Flake8 输出
        mock_run.return_value = Mock(
            stdout="src/module.py:10:1: E501 line too long\nsrc/module.py:20:5: W291 trailing whitespace\n",
            returncode=1,
        )

        runner = Flake8Runner()
        issues = runner.run("/fake/path")

        assert len(issues) == 2
        assert issues[0].code == "E501"
        assert issues[0].line == 10
        assert issues[1].code == "W291"

    @patch("subprocess.run")
    def test_flake8_no_issues(self, mock_run):
        """测试无问题时的 Flake8 输出"""
        mock_run.return_value = Mock(stdout="", returncode=0)

        runner = Flake8Runner()
        issues = runner.run("/fake/path")

        assert len(issues) == 0


class TestBanditRunner:
    """Bandit 工具运行器测试"""

    @patch("subprocess.run")
    def test_bandit_parsing(self, mock_run):
        """测试 Bandit JSON 输出解析"""
        mock_run.return_value = Mock(
            stdout=json.dumps({
                "results": [
                    {
                        "test_id": "B307",
                        "issue_severity": "HIGH",
                        "issue_text": "Use of possibly insecure function",
                        "filename": "src/module.py",
                        "line_number": 15,
                        "line_range": [15],
                    }
                ]
            }),
            returncode=1,
        )

        runner = BanditRunner()
        issues = runner.run("/fake/path")

        assert len(issues) == 1
        assert issues[0].code == "B307"
        assert issues[0].severity == Severity.HIGH
        assert issues[0].category == Category.SECURITY


class TestRadonRunner:
    """Radon 工具运行器测试"""

    @patch("subprocess.run")
    def test_radon_cc_parsing(self, mock_run):
        """测试 Radon 圈复杂度解析"""
        mock_run.return_value = Mock(
            stdout=json.dumps({
                "src/complex.py": [
                    {
                        "type": "function",
                        "name": "complex_func",
                        "lineno": 10,
                        "rank": "C",
                        "complexity": 12,
                    }
                ]
            }),
            returncode=0,
        )

        runner = RadonRunner()
        metrics = runner.run("/fake/path")

        assert metrics["average_complexity"] > 0
        assert metrics["max_complexity"] == 12


# ============= AnalysisResult Tests =============

class TestAnalysisResult:
    """分析结果类测试"""

    def test_quality_gate_passed(self, mock_analysis_result):
        """测试质量门禁判断"""
        mock_analysis_result.thresholds = {"min_quality_score": 7.0}
        assert mock_analysis_result.quality_gate_passed is True

        mock_analysis_result.thresholds = {"min_quality_score": 8.0}
        mock_analysis_result.complexity_score = 6.0
        assert mock_analysis_result.quality_gate_passed is False

    def test_issues_by_severity(self, mock_analysis_result):
        """测试按严重程度分组"""
        assert mock_analysis_result.issues_by_severity[Severity.HIGH] == 2
        assert mock_analysis_result.issues_by_severity[Severity.MEDIUM] == 5

    def test_to_json(self, mock_analysis_result, tmp_path):
        """测试 JSON 导出"""
        output_file = tmp_path / "report.json"
        mock_analysis_result.to_json(str(output_file))

        assert output_file.exists()
        data = json.loads(output_file.read_text())
        assert data["files_analyzed"] == 10
        assert data["total_issues"] == 25


# ============= QualityAnalyzer Tests =============

class TestQualityAnalyzer:
    """质量分析器测试"""

    def test_analyzer_initialization(self):
        """测试分析器初始化"""
        analyzer = QualityAnalyzer()
        assert analyzer.config.language == "python"

    def test_analyzer_with_custom_config(self):
        """测试自定义配置初始化"""
        config = Config(tools=["flake8"])
        analyzer = QualityAnalyzer(config=config)
        assert analyzer.config.tools == ["flake8"]

    @patch("code_quality_guardian.QualityAnalyzer._run_tools")
    def test_analyze_method(self, mock_run_tools, temp_project):
        """测试分析方法"""
        # 模拟工具运行结果
        mock_run_tools.return_value = {
            "flake8": [],
            "bandit": [],
        }

        analyzer = QualityAnalyzer()
        result = analyzer.analyze(temp_project)

        assert isinstance(result, AnalysisResult)
        assert result.files_analyzed >= 0

    def test_analyze_single_file(self, temp_project):
        """测试单文件分析"""
        analyzer = QualityAnalyzer()
        file_path = Path(temp_project) / "src" / "good_module.py"
        
        result = analyzer.analyze_file(str(file_path))
        assert isinstance(result, AnalysisResult)


# ============= Reporter Tests =============

class TestConsoleReporter:
    """控制台报告器测试"""

    def test_console_output(self, mock_analysis_result, capsys):
        """测试控制台输出"""
        reporter = ConsoleReporter()
        reporter.render(mock_analysis_result)

        captured = capsys.readouterr()
        assert "Code Quality Guardian" in captured.out or len(captured.out) > 0


class TestJsonReporter:
    """JSON 报告器测试"""

    def test_json_output(self, mock_analysis_result, tmp_path):
        """测试 JSON 输出"""
        output_file = tmp_path / "report.json"
        reporter = JsonReporter()
        reporter.render(mock_analysis_result, str(output_file))

        assert output_file.exists()
        data = json.loads(output_file.read_text())
        assert "files_analyzed" in data
        assert "total_issues" in data


class TestHtmlReporter:
    """HTML 报告器测试"""

    def test_html_output(self, mock_analysis_result, tmp_path):
        """测试 HTML 输出"""
        output_file = tmp_path / "report.html"
        reporter = HtmlReporter()
        reporter.render(mock_analysis_result, str(output_file))

        assert output_file.exists()
        content = output_file.read_text()
        assert "<html>" in content.lower() or "<!doctype" in content.lower()


# ============= Integration Tests =============

class TestIntegration:
    """集成测试"""

    @pytest.mark.slow
    def test_full_analysis_workflow(self, temp_project):
        """测试完整分析工作流"""
        config = Config(
            language="python",
            tools=["flake8"],  # 只使用 flake8 避免其他依赖
            thresholds={"max_complexity": 10},
        )
        
        analyzer = QualityAnalyzer(config=config)
        result = analyzer.analyze(temp_project)

        # 验证结果结构
        assert hasattr(result, "files_analyzed")
        assert hasattr(result, "total_issues")
        assert hasattr(result, "issues_by_severity")
        assert hasattr(result, "complexity_score")

    def test_config_file_integration(self, temp_project):
        """测试配置文件集成"""
        config = Config.from_file(Path(temp_project) / ".quality.yml")
        analyzer = QualityAnalyzer(config=config)
        
        assert analyzer.config.thresholds["max_complexity"] == 10


# ============= Edge Cases =============

class TestEdgeCases:
    """边界情况测试"""

    def test_empty_project(self, tmp_path):
        """测试空项目"""
        analyzer = QualityAnalyzer()
        result = analyzer.analyze(str(tmp_path))
        
        assert result.files_analyzed == 0
        assert result.total_issues == 0

    def test_nonexistent_path(self):
        """测试不存在的路径"""
        analyzer = QualityAnalyzer()
        
        with pytest.raises(FileNotFoundError):
            analyzer.analyze("/nonexistent/path")

    def test_invalid_config(self):
        """测试无效配置"""
        with pytest.raises(ValueError):
            Config(language="unknown_language")

    def test_issue_comparison(self, sample_issue):
        """测试问题比较"""
        issue2 = Issue(
            tool="pylint",
            severity=Severity.MEDIUM,
            category=Category.STYLE,
            message="Another issue",
            file="src/module.py",
            line=20,
            code="C0301",
        )

        # 严重级别高的应该更大
        assert sample_issue.severity.value > issue2.severity.value


# ============= Performance Tests =============

class TestPerformance:
    """性能测试"""

    @pytest.mark.slow
    def test_large_project_analysis(self, tmp_path):
        """测试大项目分析性能"""
        # 创建大量测试文件
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        for i in range(50):
            (src_dir / f"module_{i}.py").write_text('''
def func():
    return 42
''')

        analyzer = QualityAnalyzer()
        import time
        
        start = time.time()
        result = analyzer.analyze(str(tmp_path))
        duration = time.time() - start

        # 应该在合理时间内完成
        assert duration < 30  # 30秒
        assert result.files_analyzed == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
