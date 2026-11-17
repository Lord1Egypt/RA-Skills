"""
输入数据契约 —— 用户需求的形式化定义。

所有用户输入必须经过此 Schema 校验后才能进入编排流程。
"""

import os
import re
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, field


class ProjectType(str, Enum):
    CLI_TOOL = "cli_tool"
    WEB_APP = "web_app"
    LIBRARY = "library"
    API_SERVICE = "api_service"


@dataclass
class AcceptanceCriterion:
    """验收标准 —— Given/When/Then 结构化"""
    given: str
    when: str
    then: str
    priority: int = 2  # P1/P2/P3，默认 P2

    def __post_init__(self):
        if not self.given or len(self.given.strip()) < 5:
            raise ValueError("given 不能为空且至少 5 个字符")
        if not self.when or len(self.when.strip()) < 5:
            raise ValueError("when 不能为空且至少 5 个字符")
        if not self.then or len(self.then.strip()) < 5:
            raise ValueError("then 不能为空且至少 5 个字符")
        if self.priority not in (1, 2, 3):
            raise ValueError(f"priority 必须是 1/2/3，实际: {self.priority}")


_RESERVED_NAMES = {"test", "tmp", "temp", "src", "lib", "build", "dist"}


@dataclass
class ProjectRequest:
    """输入契约：用户需求的形式化定义"""

    project_name: str
    description: str
    project_type: ProjectType = ProjectType.CLI_TOOL
    target_python_version: str = "3.10"
    dependencies: List[str] = field(default_factory=list)
    target_directory: Optional[str] = None
    acceptance_criteria: List[AcceptanceCriterion] = field(default_factory=list)

    # 安全上限（防止恶意输入耗尽资源）
    MAX_PROJECT_NAME_LENGTH: int = 64
    MAX_DEPENDENCIES: int = 50
    MAX_ACCEPTANCE_CRITERIA: int = 100

    def __post_init__(self):
        # project_name 校验
        if not self.project_name or not self.project_name.strip():
            raise ValueError("project_name 不能为空")
        name = self.project_name.strip().lower()
        if len(name) > self.MAX_PROJECT_NAME_LENGTH:
            raise ValueError(
                f"project_name 不能超过 {self.MAX_PROJECT_NAME_LENGTH} 个字符: "
                f"'{name}' ({len(name)} 字符)"
            )
        if not name[0].isalpha():
            raise ValueError(f"project_name 必须以字母开头: '{name}'")
        if not all(c.isalnum() or c == "_" for c in name):
            raise ValueError(f"project_name 只能包含字母、数字和下划线: '{name}'")
        if name in _RESERVED_NAMES:
            raise ValueError(f"project_name 是保留字: '{name}'")
        # 路径穿越检测（防止 "../../etc" 之类的恶意名称）
        if ".." in name or "/" in name or "\\" in name:
            raise ValueError(
                f"project_name 包含非法路径字符: '{name}'，"
                f"可能存在路径穿越风险"
            )
        self.project_name = name

        # description 校验
        if not self.description or len(self.description.strip()) < 10:
            raise ValueError(f"description 不能少于 10 个字符: '{self.description}'")
        if len(self.description) > 2000:
            raise ValueError(f"description 不能超过 2000 个字符")
        # 危险字符过滤（防止 shell 注入等）
        dangerous_chars = [";", "|", "$(", "`", "&&", "||", ">", "<", "&"]
        for char in dangerous_chars:
            if char in self.description:
                raise ValueError(
                    f"description 包含危险字符: '{char}'，可能存在注入风险"
                )

        # python_version 校验
        if not re.match(r"^\d+\.\d+$", self.target_python_version):
            raise ValueError(f"target_python_version 格式错误: '{self.target_python_version}'，期望如 '3.10'")

        # dependencies 数量上限
        if len(self.dependencies) > self.MAX_DEPENDENCIES:
            raise ValueError(
                f"dependencies 不能超过 {self.MAX_DEPENDENCIES} 个: "
                f"当前 {len(self.dependencies)} 个"
            )

        # acceptance_criteria 数量上限
        if len(self.acceptance_criteria) > self.MAX_ACCEPTANCE_CRITERIA:
            raise ValueError(
                f"acceptance_criteria 不能超过 {self.MAX_ACCEPTANCE_CRITERIA} 个: "
                f"当前 {len(self.acceptance_criteria)} 个"
            )

        # target_directory 路径穿越检测
        if self.target_directory is not None:
            normalized = os.path.normpath(self.target_directory)
            if ".." in normalized.split(os.sep):
                raise ValueError(
                    f"target_directory 包含路径穿越: '{self.target_directory}'"
                )

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectRequest":
        """从字典构建，做类型转换"""
        ac_list = []
        for ac in data.get("acceptance_criteria", []):
            if isinstance(ac, dict):
                ac_list.append(AcceptanceCriterion(**ac))
            elif isinstance(ac, AcceptanceCriterion):
                ac_list.append(ac)

        return cls(
            project_name=data["project_name"],
            description=data["description"],
            project_type=ProjectType(data.get("project_type", "cli_tool")),
            target_python_version=data.get("target_python_version", "3.10"),
            dependencies=data.get("dependencies", []),
            target_directory=data.get("target_directory"),
            acceptance_criteria=ac_list,
        )
