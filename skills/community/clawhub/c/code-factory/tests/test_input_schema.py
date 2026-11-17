"""
输入 Schema 边界条件测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from contracts.input_schema import ProjectRequest, ProjectType, AcceptanceCriterion


class TestProjectRequest:
    """ProjectRequest 输入校验"""

    # ── 正常情况 ──────────────────────────────────

    def test_valid_cli_project(self):
        req = ProjectRequest(
            project_name="my_tool",
            description="A file backup tool for developers",
        )
        assert req.project_name == "my_tool"
        assert req.project_type == ProjectType.CLI_TOOL
        assert req.target_python_version == "3.10"

    def test_valid_web_project(self):
        req = ProjectRequest(
            project_name="web_dashboard",
            description="A web dashboard for monitoring system health",
            project_type=ProjectType.WEB_APP,
        )
        assert req.project_type == ProjectType.WEB_APP

    def test_name_normalization(self):
        """项目名应该被标准化为小写"""
        req = ProjectRequest(
            project_name="MyTool",
            description="A file backup tool for developers",
        )
        assert req.project_name == "mytool"

    # ── 边界条件：project_name ────────────────────

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="project_name 不能为空"):
            ProjectRequest(project_name="", description="A test tool for developers")

    def test_name_starts_with_digit_raises(self):
        with pytest.raises(ValueError, match="必须以字母开头"):
            ProjectRequest(project_name="123tool", description="A test tool for developers")

    def test_name_with_special_chars_raises(self):
        with pytest.raises(ValueError, match="只能包含字母、数字和下划线"):
            ProjectRequest(project_name="my-tool", description="A test tool for developers")

    def test_reserved_name_raises(self):
        with pytest.raises(ValueError, match="保留字"):
            ProjectRequest(project_name="test", description="A test tool for developers")

    def test_name_too_long_raises(self):
        with pytest.raises(ValueError, match="不能超过"):
            ProjectRequest(
                project_name="a" * 65,
                description="A test tool for developers with long name",
            )

    def test_name_path_traversal_raises(self):
        """路径穿越检测：../../etc（先被字母开头检查拦截，这是正确的防御层级）"""
        with pytest.raises(ValueError):
            ProjectRequest(
                project_name="../../etc",
                description="A test tool with malicious name",
            )

    def test_name_with_slash_raises(self):
        """斜杠被特殊字符检查拦截"""
        with pytest.raises(ValueError):
            ProjectRequest(
                project_name="my/tool",
                description="A test tool with slash in name",
            )

    # ── 边界条件：description ─────────────────────

    def test_description_too_short_raises(self):
        with pytest.raises(ValueError, match="不能少于 10 个字符"):
            ProjectRequest(project_name="tool", description="short")

    def test_description_dangerous_chars(self):
        dangerous = ["; rm -rf /", "ls | cat", "$(whoami)"]
        for d in dangerous:
            with pytest.raises(ValueError, match="危险字符"):
                ProjectRequest(project_name="tool", description=f"test {d} hello world")

    # ── 边界条件：python_version ──────────────────

    def test_invalid_python_version_raises(self):
        with pytest.raises(ValueError, match="格式错误"):
            ProjectRequest(
                project_name="tool",
                description="A test tool for developers",
                target_python_version="3.x",
            )

    # ── 边界条件：target_directory ────────────────

    def test_target_directory_path_traversal_raises(self):
        with pytest.raises(ValueError, match="路径穿越"):
            ProjectRequest(
                project_name="tool",
                description="A test tool for developers",
                target_directory="../../../etc",
            )

    def test_target_directory_none_ok(self):
        req = ProjectRequest(
            project_name="tool",
            description="A test tool for developers",
            target_directory=None,
        )
        assert req.target_directory is None

    # ── 边界条件：数量上限 ────────────────────────

    def test_too_many_dependencies_raises(self):
        deps = [f"pkg{i}" for i in range(51)]
        with pytest.raises(ValueError, match="不能超过"):
            ProjectRequest(
                project_name="tool",
                description="A test tool for developers",
                dependencies=deps,
            )

    def test_too_many_acceptance_criteria_raises(self):
        acs = [
            AcceptanceCriterion(
                given="a file exists",
                when="backup is triggered",
                then="file is copied",
            )
            for _ in range(101)
        ]
        with pytest.raises(ValueError, match="不能超过"):
            ProjectRequest(
                project_name="tool",
                description="A test tool for developers",
                acceptance_criteria=acs,
            )

    # ── from_dict ─────────────────────────────────

    def test_from_dict_basic(self):
        req = ProjectRequest.from_dict({
            "project_name": "my_tool",
            "description": "A file backup tool for developers",
        })
        assert req.project_name == "my_tool"

    def test_from_dict_with_ac(self):
        req = ProjectRequest.from_dict({
            "project_name": "my_tool",
            "description": "A file backup tool for developers",
            "acceptance_criteria": [
                {
                    "given": "a file exists on disk",
                    "when": "backup is triggered",
                    "then": "file is copied to backup directory",
                    "priority": 1,
                }
            ],
        })
        assert len(req.acceptance_criteria) == 1


class TestAcceptanceCriterion:
    """验收标准校验"""

    def test_valid_criterion(self):
        ac = AcceptanceCriterion(
            given="a file exists",
            when="backup is triggered",
            then="file is copied to backup dir",
            priority=1,
        )
        assert ac.priority == 1

    def test_given_too_short_raises(self):
        with pytest.raises(ValueError, match="不能为空"):
            AcceptanceCriterion(given="ab", when="triggered", then="result")

    def test_invalid_priority_raises(self):
        with pytest.raises(ValueError, match="priority 必须是"):
            AcceptanceCriterion(
                given="a file exists",
                when="triggered",
                then="result",
                priority=99,
            )
