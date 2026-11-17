"""
资产清单 Schema —— 锁定 manifest.json 和 ASSET_MANIFEST.md 的字段格式。

确保每次生成的资产清单具有一致的结构，可被工具链解析。
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AssetGenerationMethod(str, Enum):
    AUTO_GENERATED = "auto_generated"
    TEMPLATE = "template"
    USER_PROVIDED = "user_provided"


@dataclass
class AssetEntry:
    """单个资产文件描述"""
    path: str                     # 相对路径，如 "src/main.py"
    purpose: str                  # 用途说明
    generation_method: AssetGenerationMethod = AssetGenerationMethod.AUTO_GENERATED
    dependencies: List[str] = field(default_factory=list)  # 依赖的其他文件
    is_hard_gate: bool = False    # 是否为 HARD-GATE 关键文件


@dataclass
class AssetManifest:
    """资产清单 —— 机器可读 + 人类可读的统一结构"""

    project_name: str
    project_description: str
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    python_version: str = "3.10"
    assets: List[AssetEntry] = field(default_factory=list)

    # 运行环境
    os: str = ""
    environment_file: str = "requirements.txt"

    # 设计决策
    design_decisions: List[Dict[str, str]] = field(default_factory=list)

    # 已知局限
    known_limitations: List[Dict[str, str]] = field(default_factory=list)

    # 未来改进
    future_improvements: List[Dict[str, str]] = field(default_factory=list)

    def to_markdown(self) -> str:
        """生成人类可读的 ASSET_MANIFEST.md"""
        lines = [
            f"# 资源地图 — {self.project_name}",
            "",
            "## 项目目标",
            self.project_description,
            "",
            "## 资源清单",
            "",
            "| 文件 | 用途 | 生成方式 |",
            "|------|------|---------|",
        ]
        for a in self.assets:
            lines.append(f"| `{a.path}` | {a.purpose} | {a.generation_method.value} |")

        lines.extend([
            "",
            "## 运行环境",
            f"- Python版本：{self.python_version}",
            f"- 操作系统：{self.os or '跨平台'}",
            f"- 环境文件：{self.environment_file}",
            "",
        ])

        if self.design_decisions:
            lines.extend([
                "## 关键设计决策",
                "| 决策 | 理由 |",
                "|:-----|:-----|",
            ])
            for d in self.design_decisions:
                lines.append(f"| {d.get('decision', '')} | {d.get('reason', '')} |")

        if self.known_limitations:
            lines.extend([
                "",
                "## 已知局限",
                "| 局限 | 影响 |",
                "|:-----|:-----|",
            ])
            for l in self.known_limitations:
                lines.append(f"| {l.get('limitation', '')} | {l.get('impact', '')} |")

        if self.future_improvements:
            lines.extend([
                "",
                "## 未来改进方向",
                "| 方向 | 优先级 |",
                "|:-----|:------:|",
            ])
            for imp in self.future_improvements:
                lines.append(f"| {imp.get('direction', '')} | {imp.get('priority', '中')} |")

        return "\n".join(lines)

    def to_json_dict(self) -> Dict:
        """生成机器可读的 manifest.json"""
        return {
            "project_name": self.project_name,
            "description": self.project_description,
            "generated_at": self.generated_at,
            "python_version": self.python_version,
            "assets": [
                {
                    "path": a.path,
                    "purpose": a.purpose,
                    "generation_method": a.generation_method.value,
                    "dependencies": a.dependencies,
                    "is_hard_gate": a.is_hard_gate,
                }
                for a in self.assets
            ],
            "environment": {
                "os": self.os,
                "file": self.environment_file,
            },
            "design_decisions": self.design_decisions,
            "known_limitations": self.known_limitations,
            "future_improvements": self.future_improvements,
        }
