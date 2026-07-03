"""
Pipeline 钩子系统 — 保证正确执行，LLM 可自动修正。

三个钩子点：
  pipeline:pre   — 运行前校验引用、函数、报告完整性
  step:post       — 每步后检查输出合理性（None/NaN/类型）
  report:auto     — Pipeline.run() 末尾自动渲染 HTML 报告

失败时返回 {block, reason, details, suggestion}，LLM 据此修正重试。
"""
import importlib
import inspect
import os

_HOOKS = {
    "pipeline:pre": [],
    "step:post": [],
}


def register(hook_point: str, func):
    """注册钩子到指定点"""
    if hook_point not in _HOOKS:
        _HOOKS[hook_point] = []
    _HOOKS[hook_point].append(func)


def run(hook_point: str, context: dict) -> dict:
    """
    执行指定点的所有钩子。

    Returns
    -------
    dict — {"block": False} 或 {"block": True, "reason": str, "details": str, "suggestion": str}
    """
    for hook in _HOOKS.get(hook_point, []):
        try:
            result = hook(context)
            if result and result.get("block"):
                return result
        except Exception as e:
            return {"block": True, "reason": f"钩子异常: {hook.__name__}",
                    "details": str(e), "suggestion": "检查钩子实现"}
    return {"block": False}


# ═══════════════════════════════════════════════════════
# 内置钩子实现
# ═══════════════════════════════════════════════════════

# ── pipeline:pre 钩子 ──


def _check_step_references(context):
    """检查所有 %xxx% 引用是否指向已定义的步骤或 %input%"""
    pipe = context.get("_pipeline")
    if not pipe:
        return None

    step_names = {s.name for s in pipe.steps}
    errors = []

    for step in pipe.steps:
        for param_key, param_val in step.params.items():
            if isinstance(param_val, str) and param_val.startswith("%") and param_val.endswith("%"):
                ref = param_val[1:-1]
                if ref == "input" or ref == step.name:
                    continue
                if ref.startswith("input."):
                    continue
                if "." in ref:
                    step_ref = ref.split(".")[0]
                    if step_ref not in step_names:
                        errors.append(f"步骤「{step.name}」引用了不存在的步骤「{step_ref}」（参数 {param_key}={param_val}）")
                else:
                    if ref not in step_names and ref != "input":
                        errors.append(f"步骤「{step.name}」引用了不存在的步骤或输入「{ref}」（参数 {param_key}={param_val}）")

    # 检查步骤顺序依赖：被引用的步骤应在引用之前
    executed = set()
    for step in pipe.steps:
        for param_val in step.params.values():
            if isinstance(param_val, str) and param_val.startswith("%") and param_val.endswith("%"):
                ref = param_val[1:-1]
                if "." in ref:
                    ref = ref.split(".")[0]
                if ref in step_names and ref not in executed and ref != step.name:
                    errors.append(f"步骤「{step.name}」引用了尚未执行的步骤「{ref}」（顺序错误）")
        executed.add(step.name)

    if errors:
        return {
            "block": True,
            "reason": "步骤引用校验失败",
            "details": "\n".join(errors),
            "suggestion": "修正 Pipeline steps 中的引用路径或调整步骤顺序",
        }
    return None


def _check_target_functions(context):
    """检查所有 target 函数是否可正常导入"""
    pipe = context.get("_pipeline")
    if not pipe:
        return None

    errors = []
    for step in pipe.steps:
        target = step.target
        try:
            mod_path, func_name = target.rsplit(".", 1)
            mod = importlib.import_module(f"scripts.{mod_path}")
            func = getattr(mod, func_name, None)
            if func is None:
                errors.append(f"步骤「{step.name}」目标函数不存在: {target}")
        except ImportError as e:
            errors.append(f"步骤「{step.name}」目标模块导入失败: {target} → {e}")
        except ValueError:
            errors.append(f"步骤「{step.name}」目标格式错误: {target}（应为 module.func_name）")

    if errors:
        return {
            "block": True,
            "reason": "目标函数校验失败",
            "details": "\n".join(errors),
            "suggestion": "修正 Pipeline steps 中的 target 路径",
        }
    return None


def _check_default_report(context):
    """检查 default_report 对应的报告模板文件是否存在"""
    pipe = context.get("_pipeline")
    if not pipe or not pipe.default_report:
        return None

    # 直接检查文件是否存在（不通过 Pipeline.load_template 解析）
    report_base = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "pipeline", "templates"
    )
    for subdir in ["reports", "user"]:
        path = os.path.join(report_base, subdir, f"{pipe.default_report}.json")
        if os.path.exists(path):
            return None

    return {
        "block": True,
        "reason": "默认报告模板不存在",
        "details": f"场景「{pipe.name}」配置的 default_report 为「{pipe.default_report}」，但未找到对应模板",
        "suggestion": f"在 templates/reports/ 下创建 {pipe.default_report}.json，或修改 default_report 字段",
    }
    return None


# ── step:post 钩子 ──


def _guard_numeric_output(context):
    """每步后检查数值输出的合理性"""
    step = context.get("_current_step")
    result = context.get("_current_result")

    if result is None:
        return {
            "block": True,
            "reason": f"步骤「{step.name}」返回 None",
            "details": f"函数 {step.target} 返回了 None",
            "suggestion": "检查该函数的参数是否正确，特别是数据引用是否有效",
        }

    # 字典输出：检查关键字段
    if isinstance(result, dict):
        for k, v in result.items():
            if isinstance(v, float):
                if v != v:  # NaN
                    return {
                        "block": False,
                        "reason": f"步骤「{step.name}」字段 {k}=NaN",
                        "details": "检测到 NaN 值，后续步骤可能出错",
                        "suggestion": "检查输入数据是否包含空值或零值",
                    }

    # 数值输出：检查 NaN / Inf
    if isinstance(result, (int, float)):
        if result != result:  # NaN
            return {
                "block": True,
                "reason": f"步骤「{step.name}」结果为 NaN",
                "details": f"函数 {step.target} 返回了 NaN",
                "suggestion": "检查输入数据是否包含空值或除数为零",
            }
        if result == float("inf") or result == float("-inf"):
            return {
                "block": True,
                "reason": f"步骤「{step.name}」结果为无穷大",
                "details": f"函数 {step.target} 返回了 {result}",
                "suggestion": "检查是否存在除零或溢出",
            }

    return None


# ═══════════════════════════════════════════════════════
# 注册内置钩子
# ═══════════════════════════════════════════════════════

register("pipeline:pre", _check_step_references)
register("pipeline:pre", _check_target_functions)
register("pipeline:pre", _check_default_report)
register("step:post", _guard_numeric_output)
