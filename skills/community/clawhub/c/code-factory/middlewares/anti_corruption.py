"""
防腐层（Anti-Corruption Layer）—— 步骤间数据格式校验与转换。

每个步骤的输入/输出必须经过此层校验，杜绝"自然语言猜测"式数据传递。
任何不符合 Schema 的数据都会被拦截并报告明确的 ContractViolationError。
"""

from typing import Any, Dict, Type, Optional
from dataclasses import dataclass


class ContractViolationError(Exception):
    """契约违规异常 —— 携带明确的违规信息"""

    def __init__(
        self,
        step: str,
        field: str,
        expected: str,
        got: str,
        detail: str = "",
    ):
        self.step = step
        self.field = field
        self.expected = expected
        self.got = got
        self.detail = detail
        super().__init__(
            f"[{step}] 契约违规 @ {field}: 期望 {expected}, 实际 {got}"
            + (f" ({detail})" if detail else "")
        )


@dataclass
class ValidationResult:
    """校验结果"""
    is_valid: bool
    errors: list[ContractViolationError]
    sanitized_data: Dict[str, Any]


class AntiCorruptionLayer:
    """
    防腐层 —— 在步骤间建立数据格式壁垒。

    每个 validate_* 方法对应一个步骤间接口。
    输入是上一步的原始输出，输出是校验后的结构化数据。
    """

    # ── Phase 0 → Step 1 ──────────────────────────

    @staticmethod
    def validate_preflight_output(raw: Dict[str, Any]) -> ValidationResult:
        """
        校验 Phase 0 环境预检输出。
        期望字段：python_ok, dir_writable, disk_sufficient, issues
        """
        errors: list[ContractViolationError] = []
        step = "Phase0"

        required = {
            "python_ok": bool,
            "dir_writable": bool,
            "disk_sufficient": bool,
        }
        sanitized: Dict[str, Any] = {}

        for field, expected_type in required.items():
            if field not in raw:
                errors.append(ContractViolationError(
                    step=step, field=field,
                    expected=str(expected_type.__name__), got="缺失",
                    detail=f"Phase 0 必须输出 '{field}' 字段"
                ))
            elif not isinstance(raw[field], expected_type):
                errors.append(ContractViolationError(
                    step=step, field=field,
                    expected=str(expected_type.__name__),
                    got=type(raw[field]).__name__
                ))
            else:
                sanitized[field] = raw[field]

        # issues 是可选的
        sanitized["issues"] = raw.get("issues", [])

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_data=sanitized,
        )

    # ── Step 1 → Step 2 ───────────────────────────

    @staticmethod
    def validate_environment_snapshot(raw: Dict[str, Any]) -> ValidationResult:
        """
        校验 Step 1 环境快照输出。
        期望字段：python_version, installed_packages
        """
        errors: list[ContractViolationError] = []
        step = "Step1"
        sanitized: Dict[str, Any] = {}

        if "python_version" not in raw or not isinstance(raw["python_version"], str):
            errors.append(ContractViolationError(
                step=step, field="python_version",
                expected="str", got=type(raw.get("python_version")).__name__ if "python_version" in raw else "缺失"
            ))
        else:
            sanitized["python_version"] = raw["python_version"]

        if "installed_packages" not in raw:
            errors.append(ContractViolationError(
                step=step, field="installed_packages",
                expected="list[dict]", got="缺失"
            ))
        elif not isinstance(raw["installed_packages"], list):
            errors.append(ContractViolationError(
                step=step, field="installed_packages",
                expected="list", got=type(raw["installed_packages"]).__name__
            ))
        else:
            sanitized["installed_packages"] = raw["installed_packages"]

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_data=sanitized,
        )

    # ── Step 2 → Step 3 ───────────────────────────

    @staticmethod
    def validate_spec_output(raw: Dict[str, Any]) -> ValidationResult:
        """
        校验 Step 2 Spec 推导输出。
        期望字段：files (list), dependencies (list), acceptance_criteria (list), description (str)
        """
        errors: list[ContractViolationError] = []
        step = "Step2"
        sanitized: Dict[str, Any] = {}

        required_lists = ["files", "dependencies", "acceptance_criteria"]
        for field in required_lists:
            if field not in raw:
                errors.append(ContractViolationError(
                    step=step, field=field,
                    expected="list", got="缺失"
                ))
            elif not isinstance(raw[field], list):
                errors.append(ContractViolationError(
                    step=step, field=field,
                    expected="list", got=type(raw[field]).__name__
                ))
            else:
                sanitized[field] = raw[field]

        # description 字段（v2.5 新增校验）
        if "description" in raw and isinstance(raw["description"], str):
            sanitized["description"] = raw["description"]
        else:
            # description 缺失时不报错，但记录为空字符串
            sanitized["description"] = ""

        # files 中每个元素必须有 path 和 description
        if "files" in sanitized:
            for i, f in enumerate(sanitized["files"]):
                if not isinstance(f, dict) or "path" not in f:
                    errors.append(ContractViolationError(
                        step=step, field=f"files[{i}]",
                        expected="dict with 'path'", got=str(type(f).__name__)
                    ))
                elif isinstance(f, dict) and "path" in f:
                    path_val = f["path"]
                    if not isinstance(path_val, str) or path_val.strip() == "":
                        errors.append(ContractViolationError(
                            step=step, field=f"files[{i}].path",
                            expected="非空字符串", got=f"'{path_val}'"
                        ))

        # files 列表不能为空（至少需要 main.py）
        if "files" in sanitized and len(sanitized["files"]) == 0:
            errors.append(ContractViolationError(
                step=step, field="files",
                expected="非空列表（至少包含 src/main.py）", got="空列表",
                detail="Spec 推导未生成任何文件，请检查项目类型和描述"
            ))

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_data=sanitized,
        )

    # ── Step 4 → Step 5 ───────────────────────────

    @staticmethod
    def validate_verification_output(raw: Dict[str, Any]) -> ValidationResult:
        """
        校验 Step 4 验证输出。
        期望字段：all_passed (bool), test_results (dict), issues (list)
        """
        errors: list[ContractViolationError] = []
        step = "Step4"
        sanitized: Dict[str, Any] = {}

        if "all_passed" not in raw or not isinstance(raw["all_passed"], bool):
            errors.append(ContractViolationError(
                step=step, field="all_passed",
                expected="bool", got=type(raw.get("all_passed")).__name__ if "all_passed" in raw else "缺失"
            ))
        else:
            sanitized["all_passed"] = raw["all_passed"]

        sanitized["test_results"] = raw.get("test_results", {})
        sanitized["issues"] = raw.get("issues", [])

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_data=sanitized,
        )

    # ── Step 3 → Step 4 ───────────────────────────

    @staticmethod
    def validate_asset_output(raw: Dict[str, Any]) -> ValidationResult:
        """
        校验 Step 3 资产生成输出。
        期望字段：generated_files (非空 list)
        """
        errors: list[ContractViolationError] = []
        step = "Step3"
        sanitized: Dict[str, Any] = {}

        if "generated_files" not in raw:
            errors.append(ContractViolationError(
                step=step, field="generated_files",
                expected="list[str]", got="缺失",
                detail="Step 3 必须输出 generated_files 字段"
            ))
        elif not isinstance(raw["generated_files"], list):
            errors.append(ContractViolationError(
                step=step, field="generated_files",
                expected="list[str]", got=type(raw["generated_files"]).__name__
            ))
        elif len(raw["generated_files"]) == 0:
            errors.append(ContractViolationError(
                step=step, field="generated_files",
                expected="非空列表", got="空列表",
                detail="未生成任何文件，Spec 推导结果可能为空或生成过程异常"
            ))
        else:
            # 校验每个文件路径不包含路径穿越、空字符串
            for i, f in enumerate(raw["generated_files"]):
                if not isinstance(f, str):
                    errors.append(ContractViolationError(
                        step=step, field=f"generated_files[{i}]",
                        expected="str", got=type(f).__name__
                    ))
                elif f.strip() == "":
                    errors.append(ContractViolationError(
                        step=step, field=f"generated_files[{i}]",
                        expected="非空字符串", got="空字符串",
                        detail="文件路径不能为空"
                    ))
                elif ".." in f or f.startswith("/") or f.startswith("\\"):
                    errors.append(ContractViolationError(
                        step=step, field=f"generated_files[{i}]",
                        expected="安全路径", got=f"'{f}'",
                        detail="文件路径包含 .. 或绝对路径，可能存在路径穿越风险"
                    ))
            sanitized["generated_files"] = raw["generated_files"]

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_data=sanitized,
        )

    # ── Step 5 → Step 6 ───────────────────────────

    @staticmethod
    def validate_retry_output(raw: Dict[str, Any]) -> ValidationResult:
        """
        校验 Step 5 重试输出。
        期望字段：retried (bool), attempts (int)
        """
        errors: list[ContractViolationError] = []
        step = "Step5"
        sanitized: Dict[str, Any] = {}

        if "retried" not in raw:
            errors.append(ContractViolationError(
                step=step, field="retried",
                expected="bool", got="缺失"
            ))
        elif not isinstance(raw["retried"], bool):
            errors.append(ContractViolationError(
                step=step, field="retried",
                expected="bool", got=type(raw["retried"]).__name__
            ))
        else:
            sanitized["retried"] = raw["retried"]

        if "attempts" not in raw:
            errors.append(ContractViolationError(
                step=step, field="attempts",
                expected="int", got="缺失"
            ))
        elif not isinstance(raw["attempts"], int):
            errors.append(ContractViolationError(
                step=step, field="attempts",
                expected="int", got=type(raw["attempts"]).__name__
            ))
        else:
            sanitized["attempts"] = raw["attempts"]

        sanitized["success"] = raw.get("success", False)
        sanitized["failure_pattern"] = raw.get("failure_pattern", "")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_data=sanitized,
        )

    # ── Step 6 → 出口 ──────────────────────────────

    @staticmethod
    def validate_delivery_output(raw: Dict[str, Any]) -> ValidationResult:
        """
        校验 Step 6 交付输出。
        期望字段：project_path (str), readme_preview (str),
                  manifest_summary (str), manifest_json_summary (str),
                  test_summary (str)
        """
        errors: list[ContractViolationError] = []
        step = "Step6"
        sanitized: Dict[str, Any] = {}

        required_strings = [
            "project_path",
            "readme_preview",
            "manifest_summary",
            "manifest_json_summary",
            "test_summary",
        ]
        for field in required_strings:
            if field not in raw:
                errors.append(ContractViolationError(
                    step=step, field=field,
                    expected="str", got="缺失",
                    detail=f"交付输出必须包含 '{field}' 字段"
                ))
            elif not isinstance(raw[field], str):
                errors.append(ContractViolationError(
                    step=step, field=field,
                    expected="str", got=type(raw[field]).__name__
                ))
            else:
                sanitized[field] = raw[field]

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            sanitized_data=sanitized,
        )

    @classmethod
    def validate_step_transition(
        cls,
        from_step: str,
        raw_data: Dict[str, Any],
    ) -> ValidationResult:
        """
        根据来源步骤选择对应的校验器。

        Raises:
            ValueError: 未知步骤名
        """
        validators: Dict[str, callable] = {
            "Phase0": cls.validate_preflight_output,
            "Step1": cls.validate_environment_snapshot,
            "Step2": cls.validate_spec_output,
            "Step3": cls.validate_asset_output,
            "Step4": cls.validate_verification_output,
            "Step5": cls.validate_retry_output,
            "Step6": cls.validate_delivery_output,
        }

        validator = validators.get(from_step)
        if validator is None:
            raise ValueError(f"未知步骤 '{from_step}'，无法选择防腐层校验器")

        return validator(raw_data)
