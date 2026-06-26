"""
Command Line Interface for Code Quality Guardian
命令行接口
"""

import sys
from pathlib import Path
from typing import Optional

import click

from . import __version__
from .analyzer import QualityAnalyzer
from .config import Config
from .reports import ConsoleReporter, JsonReporter, HtmlReporter


@click.group()
@click.version_option(version=__version__, prog_name="code-quality-guardian")
def cli():
    """Code Quality Guardian - 代码质量守护者"""
    pass


@cli.command()
@click.option(
    "--path", "-p",
    default=".",
    help="要分析的代码路径",
)
@click.option(
    "--language", "-l",
    default="python",
    type=click.Choice(["python", "javascript", "typescript", "go"]),
    help="编程语言",
)
@click.option(
    "--tools", "-t",
    help="使用的工具（逗号分隔）",
)
@click.option(
    "--config", "-c",
    type=click.Path(exists=True),
    help="配置文件路径",
)
@click.option(
    "--format", "-f",
    default="console",
    type=click.Choice(["console", "json", "html"]),
    help="输出格式",
)
@click.option(
    "--output", "-o",
    help="输出文件路径",
)
@click.option(
    "--max-complexity",
    type=int,
    help="最大复杂度阈值",
)
@click.option(
    "--min-score",
    type=float,
    help="最低质量分数",
)
@click.option(
    "--ignore",
    help="忽略的文件模式（逗号分隔）",
)
@click.option(
    "--fail-on",
    default="high",
    type=click.Choice(["critical", "high", "medium", "low", "never"]),
    help="遇到何种级别问题时失败",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="详细输出",
)
@click.option(
    "--quiet", "-q",
    is_flag=True,
    help="静默模式",
)
def analyze(
    path: str,
    language: str,
    tools: Optional[str],
    config: Optional[str],
    format: str,
    output: Optional[str],
    max_complexity: Optional[int],
    min_score: Optional[float],
    ignore: Optional[str],
    fail_on: str,
    verbose: bool,
    quiet: bool,
):
    """分析代码质量"""
    
    # 加载配置
    if config:
        cfg = Config.from_file(config)
    else:
        # 检查默认配置文件
        default_configs = [".quality.yml", ".quality.yaml", ".quality.json"]
        cfg = None
        for cfg_file in default_configs:
            if Path(cfg_file).exists():
                cfg = Config.from_file(cfg_file)
                break
        
        if cfg is None:
            cfg = Config(language=language)
    
    # 覆盖配置选项
    if tools:
        cfg.tools = tools.split(",")
    if max_complexity:
        cfg.thresholds["max_complexity"] = max_complexity
    if min_score:
        cfg.thresholds["min_quality_score"] = min_score
    if ignore:
        cfg.ignore_patterns.extend(ignore.split(","))
    cfg.thresholds["fail_on"] = fail_on
    
    # 执行分析
    try:
        analyzer = QualityAnalyzer(config=cfg)
        result = analyzer.analyze(path)
        
        # 生成报告
        if format == "console":
            reporter = ConsoleReporter()
            reporter.render(result)
        elif format == "json":
            reporter = JsonReporter()
            output_path = output or "quality-report.json"
            reporter.render(result, output_path)
            if not quiet:
                click.echo(f"报告已保存: {output_path}")
        elif format == "html":
            reporter = HtmlReporter()
            output_path = output or "quality-report.html"
            reporter.render(result, output_path)
            if not quiet:
                click.echo(f"报告已保存: {output_path}")
        
        # 返回退出码
        if result.has_failures:
            sys.exit(2)
        elif result.total_issues > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except FileNotFoundError as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(3)
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(4)


@cli.command()
def init():
    """初始化配置文件"""
    config_content = '''# Code Quality Guardian 配置文件
language: python

tools:
  - flake8
  - pylint
  - bandit
  - radon

thresholds:
  max_complexity: 10
  max_line_length: 100
  min_quality_score: 8.0

ignore:
  - "*/tests/*"
  - "*/venv/*"
  - "*/__pycache__/*"

fail_on: high

# 工具特定配置
flake8:
  max_line_length: 100
  ignore: []

pylint:
  disable: []

bandit:
  severity: MEDIUM
  confidence: MEDIUM
'''
    
    config_path = Path(".quality.yml")
    if config_path.exists():
        click.confirm("配置文件已存在，是否覆盖？", abort=True)
    
    config_path.write_text(config_content, encoding="utf-8")
    click.echo(f"✅ 配置文件已创建: {config_path.absolute()}")


@cli.command()
@click.argument("tool_name")
def check(tool_name: str):
    """检查工具是否可用"""
    import shutil
    
    available = shutil.which(tool_name) is not None
    
    if available:
        click.echo(f"✅ {tool_name} 已安装")
        # 尝试获取版本
        import subprocess
        try:
            result = subprocess.run(
                [tool_name, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            version = result.stdout.strip() or result.stderr.strip()
            click.echo(f"   版本: {version}")
        except:
            pass
    else:
        click.echo(f"❌ {tool_name} 未安装")
        click.echo(f"   安装命令: pip install {tool_name}")


if __name__ == "__main__":
    cli()
