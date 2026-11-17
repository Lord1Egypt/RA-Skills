"""
步骤输出数据契约 —— TypedDict 形式定义。

替代裸 Dict[str, Any]，提供编译期可检查的类型定义。
所有步骤处理器和防腐层校验器应引用此模块中的类型。

注意：TypedDict 仅用于类型标注和 IDE 提示，运行时仍是普通 dict。
"""

from typing import TypedDict, List, NotRequired, Dict


# ── Phase 0: 环境预检输出 ─────────────────────────

class PreflightOutput(TypedDict):
    python_ok: bool
    dir_writable: bool
    disk_sufficient: bool
    deps_available: bool
    issues: List[str]


class PreflightWrappedOutput(TypedDict):
    """Phase 0 步骤函数的实际返回格式（包含 preflight 包装键）"""
    preflight: PreflightOutput


# ── Step 1: 环境快照输出 ──────────────────────────

class EnvironmentSnapshotOutput(TypedDict):
    python_version: str
    installed_packages: List[str]
    target_directory: str


# ── Step 2: Spec 推导输出 ─────────────────────────

class FileSpecDict(TypedDict):
    path: str
    description: str
    is_entry: bool
    is_test: bool
    is_hard_gate: bool
    dependencies: List[str]


class AcceptanceCriterionDict(TypedDict):
    given: str
    when: str
    then: str
    priority: int


class SpecOutput(TypedDict):
    description: str
    project_type: str
    files: List[FileSpecDict]
    dependencies: List[str]
    acceptance_criteria: List[AcceptanceCriterionDict]


# ── Step 3: 资产生成输出 ──────────────────────────

class AssetOutput(TypedDict):
    generated_files: List[str]


# ── Step 4: 验证输出 ──────────────────────────────

class TestResultsDict(TypedDict, total=False):
    passed: bool
    output: str
    returncode: int
    summary: str


class VerificationOutput(TypedDict):
    all_passed: bool
    test_passed: bool
    dependency_ok: bool
    hard_gate_ok: bool
    test_output: str
    test_results: TestResultsDict
    issues: List[str]
    dependency_graph: List[Dict]
    suggestions: List[str]


# ── Step 5: 重试输出 ──────────────────────────────

class RetryOutput(TypedDict):
    retried: bool
    attempts: int
    success: bool
    updated_assets: NotRequired[List[str]]
    updated_verification: NotRequired[Dict]
    failure_pattern: NotRequired[str]
    reason: NotRequired[str]


# ── Step 6: 交付输出 ──────────────────────────────

class DeliveryOutput(TypedDict):
    project_path: str
    readme_preview: str
    manifest_summary: str
    manifest_json_summary: str
    test_summary: str
