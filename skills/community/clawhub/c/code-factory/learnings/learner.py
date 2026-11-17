"""
失败模式学习器 —— 加载历史失败模式，辅助决策。

职责：
1. 在每次执行前加载 .learnings/ 中的历史失败模式
2. 识别已知会导致失败的路径，提前跳过或降级
3. 为 RetryController 提供历史经验参考
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class FailurePattern:
    """单条失败模式"""
    error_type: str
    step: str
    project_name: str
    timestamp: str
    retry_count: int = 0
    strategy_used: str = ""
    error_summary: str = ""


@dataclass
class LearningReport:
    """学习报告"""
    total_patterns: int = 0
    known_failures: List[FailurePattern] = field(default_factory=list)
    should_skip_known_failures: bool = False
    recommendations: List[str] = field(default_factory=list)


class Learner:
    """失败模式学习器"""

    def __init__(self, learnings_dir: Path):
        self.learnings_dir = Path(learnings_dir)
        self.patterns: List[FailurePattern] = []

    def load(self) -> LearningReport:
        """
        加载所有历史失败模式。

        Returns:
            LearningReport 包含已知失败模式和建议
        """
        self.patterns = []
        report = LearningReport()

        if not self.learnings_dir.exists():
            return report

        # 加载 failure_patterns.json（聚合记录）
        patterns_file = self.learnings_dir / "failure_patterns.json"
        if patterns_file.exists():
            try:
                data = json.loads(patterns_file.read_text(encoding="utf-8"))
                for p in data.get("patterns", []):
                    self.patterns.append(FailurePattern(
                        error_type=p.get("error_type", ""),
                        step=p.get("step", ""),
                        project_name=p.get("project_name", ""),
                        timestamp=p.get("timestamp", ""),
                    ))
            except (json.JSONDecodeError, KeyError):
                pass

        # 加载独立的 failure_*.json 文件
        for f in sorted(self.learnings_dir.glob("failure_*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                retry_history = data.get("retry_history", [])
                fp = FailurePattern(
                    error_type=data.get("error_type", "unknown"),
                    step=data.get("step", ""),
                    project_name=data.get("project_name", ""),
                    timestamp=data.get("timestamp", ""),
                    retry_count=len(retry_history),
                    strategy_used=retry_history[-1]["strategy"] if retry_history else "",
                    error_summary=retry_history[-1]["error"] if retry_history else "",
                )
                self.patterns.append(fp)
            except (json.JSONDecodeError, KeyError):
                continue

        report.total_patterns = len(self.patterns)
        report.known_failures = self.patterns

        # 生成建议
        report.recommendations = self._generate_recommendations()
        report.should_skip_known_failures = self._has_recurring_failures()

        return report

    def is_known_failure(self, project_name: str, step: str) -> bool:
        """
        检查某个项目/步骤组合是否在历史上失败过。

        Args:
            project_name: 项目名称
            step: 步骤名称

        Returns:
            True 如果该组合在历史中多次失败
        """
        matches = [
            p for p in self.patterns
            if p.project_name == project_name and p.step == step
        ]
        return len(matches) >= 2  # 至少 2 次才算已知失败

    def _generate_recommendations(self) -> List[str]:
        """基于历史模式生成建议"""
        recs = []
        if not self.patterns:
            return recs

        # 统计最常见失败步骤
        from collections import Counter
        step_counts = Counter(p.step for p in self.patterns)
        most_common_step = step_counts.most_common(1)
        if most_common_step:
            recs.append(
                f"最常见失败步骤: {most_common_step[0][0]}"
                f" ({most_common_step[0][1]} 次)，建议优先检查该步骤的输入校验"
            )

        # 统计最常见错误类型
        error_counts = Counter(p.error_type for p in self.patterns)
        most_common_error = error_counts.most_common(1)
        if most_common_error:
            recs.append(
                f"最常见错误类型: {most_common_error[0][0]}"
                f" ({most_common_error[0][1]} 次)"
            )

        if len(self.patterns) > 10:
            recs.append("历史失败模式较多（>10），建议检查环境配置或依赖版本")

        return recs

    def _has_recurring_failures(self) -> bool:
        """是否存在重复出现的失败模式"""
        if len(self.patterns) < 3:
            return False

        from collections import Counter
        # 检查同一 project + step 组合是否重复出现
        combos = [(p.project_name, p.step) for p in self.patterns]
        combo_counts = Counter(combos)
        return any(c >= 3 for c in combo_counts.values())
