"""
步骤注册表（StepRegistry）—— 声明式步骤定义。

消除 Orchestrator._commit_step_output() 中的硬编码 if-elif 路由链。
每个步骤声明：名称、依赖、输出提交函数、输出类型，新增步骤只需注册，无需修改 Orchestrator。

v2.5 增强：引入 output_type，PipelineGuard 可据此进行输出类型校验。
"""

from typing import Dict, List, Optional, Callable, Any, NamedTuple
from contracts.step_context import StepContext
from contracts.step_outputs import (
    PreflightOutput,
    EnvironmentSnapshotOutput,
    SpecOutput,
    AssetOutput,
    VerificationOutput,
    RetryOutput,
    DeliveryOutput,
)

# 步骤输出类型联合：所有可能的步骤输出 TypedDict
StepOutput = (
    PreflightOutput | EnvironmentSnapshotOutput | SpecOutput |
    AssetOutput | VerificationOutput | RetryOutput | DeliveryOutput |
    Dict[str, Any]
)

# commit_fn 类型标注：接收 StepContext 和步骤输出，无返回值
CommitFn = Callable[[StepContext, Dict[str, Any]], None]


class StepDefinition(NamedTuple):
    """步骤定义"""
    name: str                          # 步骤名称（如 "Phase0"）
    depends_on: Optional[str]          # 依赖的前置步骤（None 表示无依赖）
    commit_fn: Optional[CommitFn] = None
    # commit_fn: 将步骤输出写入 StepContext 的回调函数
    # 若为 None，则步骤输出不写入 StepContext（如 Step6 交付步骤）
    output_type: Optional[type] = None
    # output_type: 步骤输出的 TypedDict 类型（用于文档和运行时校验）
    has_side_effects: bool = False
    # has_side_effects: 步骤是否产生磁盘副作用（需要 Saga 补偿）


def _commit_preflight(ctx: StepContext, output: Dict[str, Any]) -> None:
    """Phase 0 → StepContext"""
    preflight_data = output.get("preflight", output)
    ctx.update_preflight(preflight_data)


def _commit_snapshot(ctx: StepContext, output: Dict[str, Any]) -> None:
    """Step 1 → StepContext"""
    ctx.update_snapshot(output)


def _commit_spec(ctx: StepContext, output: Dict[str, Any]) -> None:
    """Step 2 → StepContext"""
    ctx.update_spec(output)


def _commit_assets(ctx: StepContext, output: Dict[str, Any]) -> None:
    """Step 3 → StepContext"""
    assets = output.get("generated_files", [])
    ctx.update_assets(assets)


def _commit_verification(ctx: StepContext, output: Dict[str, Any]) -> None:
    """Step 4 → StepContext"""
    ctx.update_verification(output)


def _commit_retry(ctx: StepContext, output: Dict[str, Any]) -> None:
    """Step 5 → StepContext（v2.4：重试成功后写入 updated_assets 和 updated_verification）"""
    if output.get("success"):
        updated_assets = output.get("updated_assets")
        updated_verification = output.get("updated_verification")
        if updated_assets:
            ctx.update_assets(updated_assets)
        if updated_verification:
            ctx.update_verification(updated_verification)


# ── 注册表 ────────────────────────────────────────

STEP_REGISTRY: List[StepDefinition] = [
    StepDefinition(name="Phase0", depends_on=None,       commit_fn=_commit_preflight,   output_type=PreflightOutput,           has_side_effects=False),
    StepDefinition(name="Step1",  depends_on="Phase0",   commit_fn=_commit_snapshot,    output_type=EnvironmentSnapshotOutput, has_side_effects=False),
    StepDefinition(name="Step2",  depends_on="Step1",    commit_fn=_commit_spec,        output_type=SpecOutput,                has_side_effects=False),
    StepDefinition(name="Step3",  depends_on="Step2",    commit_fn=_commit_assets,      output_type=AssetOutput,               has_side_effects=True),
    StepDefinition(name="Step4",  depends_on="Step3",    commit_fn=_commit_verification, output_type=VerificationOutput,        has_side_effects=False),
    StepDefinition(name="Step5",  depends_on="Step4",    commit_fn=_commit_retry,       output_type=RetryOutput,               has_side_effects=True),
    StepDefinition(name="Step6",  depends_on="Step5",    commit_fn=None,                output_type=DeliveryOutput,            has_side_effects=False),
]


def get_step_definition(step_name: str) -> Optional[StepDefinition]:
    """按名称查找步骤定义"""
    for sd in STEP_REGISTRY:
        if sd.name == step_name:
            return sd
    return None


def validate_pipeline() -> List[str]:
    """
    启动时校验管道完整性。

    Returns:
        错误列表（空列表表示管道有效）
    """
    errors: List[str] = []
    names = {sd.name for sd in STEP_REGISTRY}

    for sd in STEP_REGISTRY:
        if sd.depends_on and sd.depends_on not in names:
            errors.append(f"步骤 '{sd.name}' 依赖未知步骤 '{sd.depends_on}'")

    # 检查循环依赖
    for sd in STEP_REGISTRY:
        visited = set()
        current = sd.name
        while current:
            if current in visited:
                errors.append(f"检测到循环依赖，涉及步骤: {current}")
                break
            visited.add(current)
            dep = get_step_definition(current)
            current = dep.depends_on if dep and dep.depends_on else ""

    return errors
