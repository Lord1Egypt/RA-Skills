"""Cycle 5: PipelineState 중복 제거 테스트"""

import ast
from pathlib import Path
import pytest


def test_pipeline_state_defined_only_once():
    """builder.pipeline.PipelineState는 builder.models.PipelineState를 가리켜야 함"""
    import builder.models
    import builder.pipeline

    assert builder.pipeline.PipelineState is builder.models.PipelineState, (
        "builder.pipeline.PipelineState should be the same class as builder.models.PipelineState"
    )


def test_pipeline_imports_state_from_models():
    """pipeline.py에 PipelineState 클래스 정의가 없어야 함"""
    source = (Path(__file__).parents[2] / "builder" / "pipeline.py").read_text()
    tree = ast.parse(source)

    class_names = [
        node.name for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    ]

    assert "PipelineState" not in class_names, (
        "PipelineState class should not be defined in pipeline.py, only imported from builder.models"
    )


def test_pipeline_state_has_set_stage_method():
    """models.PipelineState가 set_stage 메서드를 가져야 함"""
    from builder.models import PipelineState
    state = PipelineState()
    assert hasattr(state, "set_stage")
    state.set_stage("building")
    assert state.stage == "building"


def test_pipeline_uses_models_pipeline_state():
    """pipeline.py의 import에 PipelineState가 있어야 함"""
    source = (Path(__file__).parents[2] / "builder" / "pipeline.py").read_text()
    tree = ast.parse(source)

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and "models" in node.module:
                for alias in node.names:
                    imports.append(alias.name)

    assert "PipelineState" in imports, (
        "pipeline.py should import PipelineState from builder.models"
    )
