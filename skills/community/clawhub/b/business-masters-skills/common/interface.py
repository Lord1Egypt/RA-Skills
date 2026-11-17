# -*- coding: utf-8 -*-
"""
common/interface.py
商业管理大师技能矩阵 · 公共接口契约 (Common Interface Contract)
版本: 1.0.0

职责：
  - 定义所有技能模块统一的输入/输出数据结构与参数契约
  - 提供参数校验函数，保证模块间松耦合、仅通过约定接口交互
  - 任何模块都不依赖其他模块的内部实现，只依赖本契约

版本信息：
  v1.0.0  初始版本，定义 SkillResult / ParameterSpec / SkillContract / validate_params
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# 输出结果定义 (Output Result Definition)
# ---------------------------------------------------------------------------
@dataclass
class SkillResult:
    """所有技能统一返回结构。模块间交互只通过该结构，不暴露内部状态。"""
    module_id: str
    module_name: str
    status: str                      # "success" | "invalid_input" | "error"
    data: Dict[str, Any] = field(default_factory=dict)        # 结构化业务数据
    insights: List[str] = field(default_factory=list)         # 关键洞察
    recommendations: List[str] = field(default_factory=list)  # 行动建议
    warnings: List[str] = field(default_factory=list)         # 预警/假设提示

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_id": self.module_id,
            "module_name": self.module_name,
            "status": self.status,
            "data": self.data,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "warnings": self.warnings,
        }


# ---------------------------------------------------------------------------
# 输入参数定义 (Input Parameter Definition)
# ---------------------------------------------------------------------------
@dataclass
class ParameterSpec:
    """
    单个输入参数的声明式定义。
    - name:        参数名
    - type:        "str" | "int" | "float" | "bool" | "list" | "dict" | "enum"
    - required:    是否必填
    - constraints: 约束说明（取值范围 / 枚举值 / 格式要求），人类可读 + 校验依据
    - default:     默认值（仅 optional 生效）
    - description: 业务含义
    """
    name: str
    type: str
    required: bool
    constraints: str
    default: Any = None
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "required": self.required,
            "constraints": self.constraints,
            "default": self.default,
            "description": self.description,
        }


# ---------------------------------------------------------------------------
# 技能契约 (Skill Contract)
# ---------------------------------------------------------------------------
@dataclass
class SkillContract:
    """模块的对外契约：标识、职责描述、参数清单、输出字段说明。"""
    module_id: str
    module_name: str
    description: str
    parameters: List[ParameterSpec]
    outputs: List[Dict[str, str]]   # [{"field": "", "type": "", "description": ""}]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_id": self.module_id,
            "module_name": self.module_name,
            "description": self.description,
            "parameters": [p.to_dict() for p in self.parameters],
            "outputs": self.outputs,
        }


# ---------------------------------------------------------------------------
# 参数校验 (Parameter Validation) —— 模块松耦合调用的前置关卡
# ---------------------------------------------------------------------------
def _check_type(value: Any, expected: str) -> bool:
    if expected == "str":
        return isinstance(value, str)
    if expected == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "float":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "bool":
        return isinstance(value, bool)
    if expected == "list":
        return isinstance(value, list)
    if expected == "dict":
        return isinstance(value, dict)
    if expected == "enum":
        return isinstance(value, str)
    return True


def validate_params(contract: SkillContract, params: Dict[str, Any]) -> List[str]:
    """
    依据契约校验入参，返回错误列表（空列表表示通过）。
    约定：
      - 必填缺省 -> 报错
      - 可选缺省 -> 自动填充 default
      - 类型不符 / 超范围 -> 报错（范围由 constraints 文本约定，此处做基础类型与枚举校验）
    """
    errors: List[str] = []
    for spec in contract.parameters:
        if spec.name not in params or params[spec.name] is None:
            if spec.required:
                errors.append("缺少必填参数: %s" % spec.name)
                continue
            params[spec.name] = spec.default
            continue
        value = params[spec.name]
        if not _check_type(value, spec.type):
            errors.append("参数 %s 类型应为 %s，实际为 %s" % (spec.name, spec.type, type(value).__name__))
            continue
        # 枚举约束
        if spec.type == "enum" and spec.constraints:
            allowed = [v.strip() for v in spec.constraints.split("|")]
            if value not in allowed:
                errors.append("参数 %s 取值 '%s' 不在允许范围 %s" % (spec.name, value, allowed))
    # 未知参数提示（不阻断）
    known = {p.name for p in contract.parameters}
    for extra in params:
        if extra not in known:
            errors.append("警告: 未声明参数将被忽略: %s" % extra)
    return errors
