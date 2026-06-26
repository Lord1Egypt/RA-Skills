#!/usr/bin/env python3
"""
Code Quality Guardian - 使用示例
示例：分析项目代码质量

本示例展示如何使用 Code Quality Guardian API 分析项目代码质量
"""

import os
import sys
from pathlib import Path

# 将 src 目录添加到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from code_quality_guardian import QualityAnalyzer, Config


def example_1_basic_analysis():
    """示例 1: 基础项目分析"""
    print("=" * 60)
    print("示例 1: 基础项目分析")
    print("=" * 60)

    # 创建分析器实例
    analyzer = QualityAnalyzer()

    # 分析当前目录
    project_path = Path(__file__).parent.parent
    results = analyzer.analyze(str(project_path))

    # 输出结果摘要
    print(f"\n📊 分析完成!")
    print(f"   分析文件数: {results.files_analyzed}")
    print(f"   发现问题数: {results.total_issues}")
    print(f"   复杂度评分: {results.complexity_score}/10")
    print(f"   质量评级: {results.quality_rank}")

    # 输出到控制台
    results.to_console()


def example_2_custom_config():
    """示例 2: 使用自定义配置"""
    print("\n" + "=" * 60)
    print("示例 2: 使用自定义配置")
    print("=" * 60)

    # 创建自定义配置
    config = Config(
        language="python",
        tools=["flake8", "bandit", "radon"],  # 只使用这些工具
        thresholds={
            "max_complexity": 8,  # 最大复杂度
            "max_line_length": 88,  # 行长度限制
            "min_quality_score": 7.5,  # 最低质量分数
        },
        ignore_patterns=[
            "*/tests/*",
            "*/venv/*",
            "*/__pycache__/*",
            "*/migrations/*",
        ],
    )

    # 使用配置创建分析器
    analyzer = QualityAnalyzer(config=config)

    # 分析代码
    project_path = Path(__file__).parent.parent
    results = analyzer.analyze(str(project_path))

    print(f"\n📊 使用自定义配置分析完成!")
    print(f"   启用的工具: {', '.join(config.tools)}")
    print(f"   最大复杂度阈值: {config.thresholds['max_complexity']}")

    # 检查质量门禁
    if results.quality_gate_passed:
        print("   ✅ 质量门禁通过!")
    else:
        print("   ❌ 质量门禁未通过!")
        print(f"   需要改进的问题: {len(results.critical_issues)} 个严重问题")


def example_3_specific_tools():
    """示例 3: 使用特定工具进行分析"""
    print("\n" + "=" * 60)
    print("示例 3: 使用特定工具进行分析")
    print("=" * 60)

    # 只使用安全扫描工具
    analyzer = QualityAnalyzer(tools=["bandit"])

    project_path = Path(__file__).parent.parent
    results = analyzer.analyze(str(project_path))

    print(f"\n🔒 安全扫描结果:")
    print(f"   发现安全问题: {len(results.security_issues)} 个")

    for issue in results.security_issues[:5]:  # 显示前5个
        print(f"   - [{issue.severity}] {issue.message}")
        print(f"     位置: {issue.file}:{issue.line}")


def example_4_generate_reports():
    """示例 4: 生成不同格式的报告"""
    print("\n" + "=" * 60)
    print("示例 4: 生成不同格式的报告")
    print("=" * 60)

    analyzer = QualityAnalyzer()
    project_path = Path(__file__).parent.parent
    results = analyzer.analyze(str(project_path))

    # 创建输出目录
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # 生成 JSON 报告
    json_path = output_dir / "quality_report.json"
    results.to_json(str(json_path))
    print(f"\n📄 JSON 报告已生成: {json_path}")

    # 生成 HTML 报告
    html_path = output_dir / "quality_report.html"
    results.to_html(str(html_path))
    print(f"📄 HTML 报告已生成: {html_path}")

    # 生成 Markdown 报告
    md_path = output_dir / "quality_report.md"
    results.to_markdown(str(md_path))
    print(f"📄 Markdown 报告已生成: {md_path}")

    print(f"\n📊 报告摘要:")
    print(f"   总行数: {results.lines_of_code}")
    print(f"   文件数: {results.files_analyzed}")
    print(f"   问题分类:")
    for category, count in results.issues_by_category.items():
        print(f"     - {category}: {count} 个")


def example_5_ci_integration():
    """示例 5: CI/CD 集成示例"""
    print("\n" + "=" * 60)
    print("示例 5: CI/CD 集成示例")
    print("=" * 60)

    # CI 环境配置
    config = Config(
        language="python",
        tools=["flake8", "pylint", "bandit", "radon"],
        thresholds={
            "max_complexity": 10,
            "min_quality_score": 8.0,
        },
        fail_on="high",  # 发现 High 级别问题时失败
    )

    analyzer = QualityAnalyzer(config=config)
    project_path = Path(__file__).parent.parent
    results = analyzer.analyze(str(project_path))

    # CI 输出格式
    print("\n##vso[task.setvariable variable=qualityScore]" + str(results.quality_score))
    print(f"##vso[task.setvariable variable=totalIssues]{results.total_issues}")

    # 检查是否失败
    if results.has_failures:
        print("\n❌ 代码质量检查失败!")
        print(f"   失败原因: {results.failure_reason}")
        sys.exit(1)  # CI 失败
    else:
        print("\n✅ 代码质量检查通过!")
        print(f"   质量分数: {results.quality_score}/10")
        sys.exit(0)  # CI 通过


def example_6_incremental_analysis():
    """示例 6: 增量分析"""
    print("\n" + "=" * 60)
    print("示例 6: 增量分析 (只分析变更的文件)")
    print("=" * 60)

    # 获取变更的文件列表 (示例)
    changed_files = [
        "src/code_quality_guardian/analyzer.py",
        "src/code_quality_guardian/reports.py",
    ]

    analyzer = QualityAnalyzer()

    print(f"\n📝 分析变更的文件 ({len(changed_files)} 个):")
    for file in changed_files:
        print(f"   - {file}")
        # 分析单个文件
        if os.path.exists(file):
            result = analyzer.analyze_file(file)
            print(f"     问题数: {len(result.issues)}")


def main():
    """主函数：运行所有示例"""
    print("\n" + "🛡️ " * 20)
    print("   Code Quality Guardian - 使用示例")
    print("🛡️ " * 20 + "\n")

    # 运行示例
    examples = [
        ("基础分析", example_1_basic_analysis),
        ("自定义配置", example_2_custom_config),
        ("特定工具", example_3_specific_tools),
        ("生成报告", example_4_generate_reports),
        ("CI/CD 集成", example_5_ci_integration),
        ("增量分析", example_6_incremental_analysis),
    ]

    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n⚠️ 示例 '{name}' 运行出错: {e}")
            print("   (这可能是因为实际工具未安装，示例代码仍可参考)")

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
    print("\n提示: 实际使用前请确保已安装依赖:")
    print("   pip install -r requirements.txt")


if __name__ == "__main__":
    main()
