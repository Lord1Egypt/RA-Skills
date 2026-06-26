"""
Console reporter - 控制台彩色输出
"""

import sys
from typing import Optional

from .base import Reporter
from ..models import AnalysisResult, Severity, Category


try:
    from colorama import init, Fore, Style
    init()
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    class Fore:
        RED = ""
        YELLOW = ""
        GREEN = ""
        BLUE = ""
        CYAN = ""
        MAGENTA = ""
        WHITE = ""
        RESET = ""
    class Style:
        BRIGHT = ""
        RESET_ALL = ""


class ConsoleReporter(Reporter):
    """控制台报告生成器"""
    
    # 严重程度颜色
    SEVERITY_COLORS = {
        Severity.CRITICAL: Fore.RED + Style.BRIGHT,
        Severity.HIGH: Fore.RED,
        Severity.MEDIUM: Fore.YELLOW,
        Severity.LOW: Fore.BLUE,
        Severity.INFO: Fore.CYAN,
    }
    
    def render(self, result: AnalysisResult, output_path: Optional[str] = None) -> str:
        """
        渲染控制台报告
        
        Args:
            result: 分析结果
            output_path: 不使用
            
        Returns:
            报告字符串
        """
        lines = []
        
        # 标题
        lines.extend(self._render_header())
        
        # 摘要
        lines.extend(self._render_summary(result))
        
        # 问题统计
        lines.extend(self._render_issues_summary(result))
        
        # 质量指标
        lines.extend(self._render_metrics(result))
        
        # 质量门禁
        lines.extend(self._render_quality_gate(result))
        
        # 详细问题 (如果数量不多)
        if result.total_issues <= 20:
            lines.extend(self._render_issues_detail(result))
        
        output = "\n".join(lines)
        
        # 输出到控制台
        print(output)
        
        return output
    
    def _render_header(self) -> list:
        """渲染标题"""
        width = 60
        return [
            "",
            "═" * width,
            f"       {Fore.CYAN}🔍 Code Quality Guardian v1.0.0{Fore.RESET}",
            "═" * width,
            "",
        ]
    
    def _render_summary(self, result: AnalysisResult) -> list:
        """渲染摘要"""
        lines = [
            f"📁 Project: {result.files_analyzed} files analyzed",
            f"📊 Lines of code: {result.lines_of_code}",
            f"🔧 Tools used: flake8, pylint, bandit, radon",
            "",
        ]
        return lines
    
    def _render_issues_summary(self, result: AnalysisResult) -> list:
        """渲染问题统计"""
        width = 50
        lines = [
            "┌" + "─" * width + "┐",
            "│" + "📋 Issues Summary".center(width) + "│",
            "├" + "─" * width + "┤",
        ]
        
        # 各严重程度计数
        severity_icons = {
            Severity.CRITICAL: "🔴",
            Severity.HIGH: "🟠",
            Severity.MEDIUM: "🟡",
            Severity.LOW: "🔵",
            Severity.INFO: "💡",
        }
        
        for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
            count = result.issues_by_severity.get(sev, 0)
            name = sev.name.ljust(10)
            line = f"│ {severity_icons[sev]} {name} {str(count).rjust(width - 15)} │"
            lines.append(line)
        
        lines.extend([
            "├" + "─" * width + "┤",
            f"│ Total: {str(result.total_issues).rjust(width - 9)} │",
            "└" + "─" * width + "┘",
            "",
        ])
        
        return lines
    
    def _render_metrics(self, result: AnalysisResult) -> list:
        """渲染质量指标"""
        lines = [
            "📊 Quality Metrics",
            "━" * 50,
        ]
        
        # 复杂度分数
        cc_score = result.complexity_score
        cc_bar = self._render_bar(cc_score / 10)
        lines.append(f"  Complexity:     {cc_score:.1f}/10  {cc_bar}")
        
        # 质量分数
        q_score = result.quality_score
        q_bar = self._render_bar(q_score / 10)
        q_color = Fore.GREEN if q_score >= 7 else (Fore.YELLOW if q_score >= 5 else Fore.RED)
        lines.append(f"  Quality Score:  {q_score:.1f}/10  {q_bar} {q_color}{result.quality_rank}{Fore.RESET}")
        
        # 安全分数
        s_score = result.security_score
        s_bar = self._render_bar(s_score / 100)
        lines.append(f"  Security:       {s_score:.0f}%    {s_bar}")
        
        lines.extend([
            "━" * 50,
            "",
        ])
        
        return lines
    
    def _render_bar(self, ratio: float, width: int = 10) -> str:
        """渲染进度条"""
        filled = int(ratio * width)
        empty = width - filled
        return "●" * filled + "○" * empty
    
    def _render_quality_gate(self, result: AnalysisResult) -> list:
        """渲染质量门禁"""
        if result.quality_gate_passed:
            status = f"{Fore.GREEN}✅ PASSED{Fore.RESET}"
        else:
            status = f"{Fore.RED}❌ FAILED{Fore.RESET}"
        
        return [
            f"🔒 Quality Gate: {status}",
            f"   Score: {result.quality_score:.1f} (threshold: {result.thresholds.get('min_quality_score', 0)})",
            "",
        ]
    
    def _render_issues_detail(self, result: AnalysisResult) -> list:
        """渲染详细问题列表"""
        if not result.issues:
            return ["✨ No issues found!", ""]
        
        lines = [
            "📋 Detailed Issues",
            "─" * 60,
        ]
        
        # 按严重程度排序
        sorted_issues = sorted(
            result.issues,
            key=lambda x: x.severity.value,
            reverse=True
        )
        
        for issue in sorted_issues[:10]:  # 只显示前10个
            color = self.SEVERITY_COLORS.get(issue.severity, "")
            lines.append(f"{color}[{issue.code}]{Fore.RESET} {issue.message}")
            lines.append(f"   {Fore.CYAN}→{Fore.RESET} {issue.file}:{issue.line}")
            lines.append("")
        
        if len(sorted_issues) > 10:
            lines.append(f"... and {len(sorted_issues) - 10} more issues")
        
        return lines
