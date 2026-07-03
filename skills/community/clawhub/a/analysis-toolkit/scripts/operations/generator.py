"""
算子自动生成器 — 根据公式描述自动生成缺失算子的代码并注册。

工作流程：
1. 接收公式描述（如 "u = |bias| / sqrt(3)"）
2. 通过 LLM 或模板匹配识别算子结构
3. 生成 Python 代码
4. 写入 scripts/operations/ 下对应模块
5. 注册到算子注册表
"""
import os
import inspect
import importlib
from typing import Optional

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OPERATIONS_DIR = os.path.join(_SKILL_DIR, "operations")


# ═══════════════════════════════════════════════════════
# 算子代码模板
# ═══════════════════════════════════════════════════════

OPERATOR_TEMPLATE = '''"""
自动生成的算子: {name}
公式: {formula}
"""
import numpy as np


def {name}({params}) -> float:
    """
    {description}

    {param_doc}
    Returns
    -------
    float
    """
{passthrough}
'''


# ═══════════════════════════════════════════════════════
# 常用公式模式
# ═══════════════════════════════════════════════════════

FORMULA_PATTERNS = {
    "calc_{name}": {
        "template": '    return {expression}',
        "imports": "import numpy as np\n",
    },
}


# ═══════════════════════════════════════════════════════
# 向已有模块追加新的算子函数
# ═══════════════════════════════════════════════════════

def append_function_to_file(filename: str, func_code: str) -> dict:
    """
    向指定 Python 文件追加新的函数定义。

    Parameters
    ----------
    filename : str — 文件名（不含路径），如 "uncertainty.py"
    func_code : str — 完整的函数定义代码

    Returns
    -------
    dict — {"status": "ok"|"error", "message": str, "filepath": str}
    """
    filepath = os.path.join(_OPERATIONS_DIR, filename)
    if not os.path.exists(filepath):
        return {"status": "error", "message": f"文件不存在: {filepath}", "filepath": filepath}

    # 检查函数是否已存在
    mod_name = f"scripts.operations.{filename.replace('.py', '')}"
    try:
        mod = importlib.import_module(mod_name)
        func_name = _extract_func_name(func_code)
        if func_name and hasattr(mod, func_name):
            return {"status": "skipped", "message": f"函数 '{func_name}' 已存在于 {filename}", "filepath": filepath}
    except ImportError:
        pass

    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write("\n\n")
            f.write(func_code)
        return {"status": "ok", "message": f"已追加到 {filename}", "filepath": filepath}
    except IOError as e:
        return {"status": "error", "message": f"写入失败: {e}", "filepath": filepath}


def update_module_all(filepath: str, func_name: str) -> dict:
    """
    更新模块的 __all__ 列表，将新函数名加入其中。

    Parameters
    ----------
    filepath : str — Python 文件路径
    func_name : str — 新增的函数名

    Returns
    -------
    dict
    """
    if not os.path.exists(filepath):
        return {"status": "error", "message": f"文件不存在: {filepath}"}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if f'"{func_name}"' in content or f"'{func_name}'" in content:
        return {"status": "skipped", "message": f"'{func_name}' 已在 __all__ 中"}

    # 在 __all__ 的最后一个元素前插入
    import re
    # 找到 __all__ = [...] 的最后一个元素
    pattern = r'(__all__\s*=\s*\[)([^\]]*)(\])'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return {"status": "error", "message": "未找到 __all__ 定义"}

    prefix = match.group(1)
    body = match.group(2).strip()
    suffix = match.group(3)

    if body.endswith(","):
        new_body = body + f'\n    "{func_name}",'
    else:
        new_body = body + f',\n    "{func_name}",'

    new_content = content[:match.start()] + prefix + "\n" + new_body + "\n" + suffix + content[match.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return {"status": "ok", "message": f"已将 '{func_name}' 加入 __all__"}


# ═══════════════════════════════════════════════════════
# 从公式描述生成算子（供 LLM 调用）
# ═══════════════════════════════════════════════════════

def generate_operator_from_formula(
    formula: str,
    operator_name: str,
    description: str,
    parameters: list[dict],
    expression: str,
    target_file: str = "uncertainty.py",
) -> dict:
    """
    根据公式参数生成算子代码并注册。

    典型用法（由 LLM 解析标准公式后调用）：

        generate_operator_from_formula(
            formula="u_bias = |bias| / √3",
            operator_name="calc_ubias_rectangular",
            description="矩形分布偏倚不确定度",
            parameters=[
                {"name": "bias", "type": "float", "doc": "偏倚值"},
            ],
            expression="return abs(bias) / math.sqrt(3)",
            target_file="uncertainty.py",
        )

    Parameters
    ----------
    formula : str — 人可读的公式
    operator_name : str — 函数名
    description : str — 简短说明
    parameters : list[dict] — 参数列表 [{"name", "type", "doc"}, ...]
    expression : str — Python 表达式（不包含 def 行）
    target_file : str — 追加到哪个文件

    Returns
    -------
    dict
    """
    param_str = ", ".join(f"{p['name']}: {p['type']}" for p in parameters)
    param_doc_lines = []
    for p in parameters:
        param_doc_lines.append(f"    {p['name']} : {p['type']} — {p.get('doc', '')}")
    param_doc = "\n".join(param_doc_lines)

    func_code = (
        f"\n\n"
        f"def {operator_name}({param_str}) -> float:\n"
        f'    """\n'
        f"    {description}.\n"
        f"\n"
        f"    公式: {formula}\n"
        f"\n"
        f"    Parameters\n"
        f"    ----------\n"
        f"{param_doc}\n"
        f"\n"
        f"    Returns\n"
        f"    -------\n"
        f"    float\n"
        f'    """\n'
        f"    {expression}\n"
    )

    # 追加到文件
    result = append_function_to_file(target_file, func_code)
    if result["status"] == "ok":
        # 更新 __all__
        update_result = update_module_all(result["filepath"], operator_name)
        result["all_updated"] = (update_result["status"] == "ok")

        # 注册到算子注册表
        from scripts.operations.registry import get_operator_registry
        reg = get_operator_registry()
        cat = target_file.replace(".py", "")
        reg.register({
            "name": operator_name,
            "signature": f"({param_str})",
            "formula": formula,
            "description": description,
            "module": f"scripts.operations.{cat}",
            "category": cat,
            "required_params": [p["name"] for p in parameters],
        })

    return result


def _extract_func_name(func_code: str) -> Optional[str]:
    """从函数定义代码中提取函数名"""
    import re
    match = re.search(r"def\s+(\w+)\s*\(", func_code)
    return match.group(1) if match else None


# ═══════════════════════════════════════════════════════
# 自动追加自测试用例
# ═══════════════════════════════════════════════════════

def _add_self_test(func_name: str, args_expr: str, expected_expr: str,
                    filepath: str) -> dict:
    """
    在 self_test.py 的 _get_test_cases() 中追加一个测试用例。

    Parameters
    ----------
    func_name : str — 算子函数名
    args_expr : str — 参数的 Python 表达式，如 "([1,2,3],)"
    expected_expr : str — 预期值的 Python 表达式，如 "2.0"
    filepath : str — self_test.py 文件的路径

    Returns
    -------
    dict
    """
    if not os.path.exists(filepath):
        return {"status": "error", "message": f"文件不存在: {filepath}"}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 检查测试用例是否已存在
    if func_name in content:
        return {"status": "skipped", "message": f"测试用例 '{func_name}' 已存在"}

    # 在 _get_test_cases 最后追加新用例
    # 查找最后一个测试用例的结尾（即 return 之前的行）
    marker = "(te.calc_te_relative"  # 最后一个已有测试用例
    insert_pos = content.rfind(marker)
    if insert_pos == -1:
        # 备用：找最后一个 return 附近
        insert_pos = content.rfind("    return [")
        if insert_pos == -1:
            return {"status": "error", "message": "未找到测试用例插入位置"}

    # 找该行的末尾
    insert_pos = content.find("\n", insert_pos)
    if insert_pos == -1:
        return {"status": "error", "message": "无法定位插入位置"}

    new_test = f',\n        (ops.{func_name}, {args_expr}, {{}}, {expected_expr}, "{func_name} 自动生成验证"),'

    new_content = content[:insert_pos] + new_test + content[insert_pos:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return {"status": "ok", "message": f"已在 self_test.py 追加测试用例 '{func_name}'"}


__all__ = [
    "append_function_to_file", "update_module_all",
    "generate_operator_from_formula", "_add_self_test",
]
