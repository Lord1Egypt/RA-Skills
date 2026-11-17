"""
Step 2: Spec 推导引擎 —— 从用户需求推导内部规格。

借鉴 spec-kit 理念：
1. 从需求中提取功能范围、输入输出、边界条件、验收标准
2. 生成 plan.md 兼容的计划
3. 用户完全无感知，AI 内部完成
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from contracts.input_schema import ProjectType, AcceptanceCriterion


@dataclass
class FileSpec:
    """单个文件的规格"""
    path: str
    description: str
    is_entry: bool = False
    is_test: bool = False
    is_hard_gate: bool = False
    dependencies: List[str] = field(default_factory=list)


@dataclass
class SpecResult:
    """Spec 推导结果"""
    project_name: str = ""
    project_type: ProjectType = ProjectType.CLI_TOOL
    description: str = ""
    files: List[FileSpec] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    acceptance_criteria: List[Dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "project_type": self.project_type.value if isinstance(self.project_type, ProjectType) else self.project_type,
            "files": [
                {
                    "path": f.path,
                    "description": f.description,
                    "is_entry": f.is_entry,
                    "is_test": f.is_test,
                    "is_hard_gate": f.is_hard_gate,
                    "dependencies": f.dependencies,
                }
                for f in self.files
            ],
            "dependencies": self.dependencies,
            "acceptance_criteria": self.acceptance_criteria,
        }


class SpecEngine:
    """Spec 推导引擎"""

    def derive(
        self,
        description: str,
        project_type: ProjectType = ProjectType.CLI_TOOL,
        acceptance_criteria: Optional[List[AcceptanceCriterion]] = None,
    ) -> SpecResult:
        """
        从用户需求推导内部规格。

        这是 AI 辅助的核心环节 —— AI 根据 description 推导出文件列表、
        依赖关系、验收标准。但输出格式受 Schema 约束，不会变成自由文本。
        """
        spec = SpecResult(
            description=description,
            project_type=project_type,
        )

        # 标准化项目结构（所有项目都必须包含这些文件）
        spec.files = self._derive_file_structure(project_type, description)
        spec.dependencies = self._derive_dependencies(project_type, description)

        # 转换验收标准
        if acceptance_criteria:
            spec.acceptance_criteria = [
                {"given": ac.given, "when": ac.when, "then": ac.then, "priority": ac.priority}
                for ac in acceptance_criteria
            ]

        return spec

    def _derive_file_structure(
        self, project_type: ProjectType, description: str
    ) -> List[FileSpec]:
        """推导标准化文件结构"""
        files = [
            FileSpec(
                path="src/main.py",
                description=f"主程序入口 — {description[:50]}",
                is_entry=True,
                is_hard_gate=True,
            ),
            FileSpec(
                path="tests/test_main.py",
                description="pytest 单元测试",
                is_test=True,
                dependencies=["src/main.py"],
            ),
            FileSpec(
                path="docs/README.md",
                description="使用说明/安装/依赖文档",
            ),
            FileSpec(
                path="requirements.txt",
                description="Python 依赖清单",
            ),
            FileSpec(
                path="run.sh",
                description="一键运行脚本",
            ),
            FileSpec(
                path="SKILL.md",
                description="AI 技能元数据头",
            ),
            FileSpec(
                path="ASSET_MANIFEST.md",
                description="人类可读的资源地图表",
            ),
            FileSpec(
                path="manifest.json",
                description="机器可读的资产清单",
            ),
            FileSpec(
                path="environment.toml",
                description="环境隔离配置",
            ),
        ]

        # 根据项目类型添加特定文件
        if project_type == ProjectType.WEB_APP:
            files.append(FileSpec(
                path="src/app.py",
                description="Web 应用主模块",
                dependencies=["src/main.py"],
            ))
        elif project_type == ProjectType.API_SERVICE:
            files.append(FileSpec(
                path="src/api.py",
                description="API 路由定义",
                dependencies=["src/main.py"],
            ))

        return files

    def _derive_dependencies(
        self, project_type: ProjectType, description: str
    ) -> List[str]:
        """推导默认依赖"""
        deps = []
        if project_type == ProjectType.WEB_APP:
            deps.append("flask>=3.0")
        elif project_type == ProjectType.API_SERVICE:
            deps.append("fastapi>=0.100")
            deps.append("uvicorn>=0.23")
        return deps
