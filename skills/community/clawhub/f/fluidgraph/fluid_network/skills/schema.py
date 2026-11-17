# -*- coding: utf-8 -*-
"""机器可读的工具 Schema（JSON Schema 风格）。

这一层是**唯一真相**：Runner 的参数校验、``to_openai_tools()`` /
``to_anthropic_tools()`` / ``to_mcp_tools()`` 的转换都从这里读，
避免"文档写一套、代码是另一套"。

Schema 用的是 JSON Schema 的**子集**，且刻意保持在所有主流 tool-calling
格式都支持的交集内：

* ``type: "object"`` + ``properties`` + ``required``
* ``string`` / ``number`` / ``boolean`` / ``array`` / ``object``
* ``description`` / ``enum`` / ``default``

**不用** ``oneOf`` / ``$ref`` / ``anyOf`` —— OpenAI 与部分 MCP 实现对它们
的支持并不一致。需要"多种输入形态"时，用一个 ``string`` 参数配合
``description`` 说明，而不是上联合类型。
"""

from __future__ import annotations

__all__ = [
    "TOOL_SCHEMAS",
    "SCHEMA_BY_NAME",
    "get_schema",
    "validate_arguments",
    "describe_tools",
]

# --------------------------------------------------------------------------- #
# 可复用的片段
# --------------------------------------------------------------------------- #
_NETWORK_SOURCE = {
    "type": "string",
    "description": (
        "流体网络定义。可传三种形态之一："
        "(1) TOML 文件路径，如 'examples/example.toml'；"
        "(2) TOML 文本内容（需包含 [network] 段落）；"
        "(3) 上一轮 parse_network 的 data.summary 所属网络的原始来源。"
        "注意：不要传 AnalysisResult —— 那是 analyze_scenario 的输出，"
        "应交给 explain_load / compare_scenarios / render_report。"
    ),
}

_ANALYSIS_RESULT = {
    "type": "object",
    "description": (
        "analyze_scenario 返回的 data 字段（完整 AnalysisResult）。"
        "其中所有压力为 Pa、流量为 m3/s（SI 原值），"
        "不可达部件的数值为 null —— null 表示没有有效计算值，不是 0。"
    ),
}


TOOL_SCHEMAS: list[dict] = [
    # ------------------------------------------------------------------ #
    {
        "name": "parse_network",
        "description": (
            "解析并校验流体网络定义，返回网络摘要。"
            "当定义非法时返回全部问题的结构化诊断（每条含位置、字段与修复建议），"
            "可据此直接修正 TOML 后重试。"
            "在问任何物理问题之前先调用它，可以避免后续步骤白跑。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "network_source": _NETWORK_SOURCE,
                "strict": {
                    "type": "boolean",
                    "description": "未知字段是否视为错误。默认 true（推荐），设为 false 可容忍额外字段。",
                    "default": True,
                },
            },
            "required": ["network_source"],
        },
    },
    # ------------------------------------------------------------------ #
    {
        "name": "analyze_scenario",
        "description": (
            "对指定工况执行完整分析，返回 AnalysisResult。"
            "结果包含节点压力、管路流量与流速、压降、每条负载的流路、"
            "以及每个负载的可靠性状态（HEALTHY / ISOLATED / LOW_PRESSURE / "
            "LOW_FLOW / UNSUPPORTED / FAILED）。"
            "所有数值均由求解器计算，调用方不需要、也不应该自己算物理量。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "network_source": _NETWORK_SOURCE,
                "scenario_id": {
                    "type": "string",
                    "description": "工况 id，例如 'normal'、'v1_failure'。可用工况见 parse_network 的 summary.scenarios。",
                },
            },
            "required": ["network_source", "scenario_id"],
        },
    },
    # ------------------------------------------------------------------ #
    {
        "name": "analyze_all_scenarios",
        "description": (
            "一次分析网络里定义的全部工况，返回 {scenario_id: AnalysisResult}。"
            "这是 compare_scenarios 的常用前置 —— 比逐个调用 analyze_scenario 更省往返。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {"network_source": _NETWORK_SOURCE},
            "required": ["network_source"],
        },
    },
    # ------------------------------------------------------------------ #
    {
        "name": "explain_load",
        "description": (
            "解释单个负载为什么处于当前状态。"
            "返回状态、压力、流量、最低要求、流路、切断点与原因，"
            "并给出一句可直接转述给人的 explanation。"
            "当用户问「为什么 L1 挂了」「哪个负载还正常」时用它。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "analysis_result": _ANALYSIS_RESULT,
                "load_id": {
                    "type": "string",
                    "description": "负载节点 id，例如 'L1'。可用负载见 AnalysisResult 的 loads[].load_id。",
                },
            },
            "required": ["analysis_result", "load_id"],
        },
    },
    # ------------------------------------------------------------------ #
    {
        "name": "compare_scenarios",
        "description": (
            "按负载逐项对比两个或多个工况，给出压力/流量的变化与状态迁移。"
            "注意：某一侧为 null（负载不可达）时，delta 返回 null 而不是把差值算成负数 —— "
            "那种情况下数值根本不存在，报告里会在 notes 说明原因。"
            "当用户问「V1 故障造成了什么影响」「哪个负载变差了」时用它。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "analysis_results": {
                    "type": "array",
                    "description": "至少两个 AnalysisResult，顺序即对比顺序（通常是 正常 -> 故障）。",
                    "items": _ANALYSIS_RESULT,
                    "minItems": 2,
                },
            },
            "required": ["analysis_results"],
        },
    },
    # ------------------------------------------------------------------ #
    {
        "name": "render_report",
        "description": (
            "把一个 AnalysisResult 渲染成 Markdown 报告，"
            "包含工况、网络状态、流路分析、负载状态、管路状态、可靠性结论与警告。"
            "报告中的数值全部取自 AnalysisResult，只做单位换算（Pa->kPa、m3/s->L/s），"
            "不计算任何新的物理量。当用户要一份可直接阅读/粘贴的总结时用它。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {"analysis_result": _ANALYSIS_RESULT},
            "required": ["analysis_result"],
        },
    },
]

SCHEMA_BY_NAME: dict[str, dict] = {schema["name"]: schema for schema in TOOL_SCHEMAS}


def get_schema(name: str) -> dict:
    """按名字取 Schema。"""
    try:
        return SCHEMA_BY_NAME[name]
    except KeyError:
        available = ", ".join(sorted(SCHEMA_BY_NAME))
        raise KeyError(f"未知工具 '{name}'；可用：{available}") from None


def describe_tools() -> list[dict]:
    """给人类看的工具清单（名字 + 描述 + 参数名）。"""
    return [
        {
            "name": schema["name"],
            "description": schema["description"],
            "required": list(schema["input_schema"].get("required", [])),
            "properties": sorted(schema["input_schema"].get("properties", {})),
        }
        for schema in TOOL_SCHEMAS
    ]


# --------------------------------------------------------------------------- #
# 参数校验
# --------------------------------------------------------------------------- #
def validate_arguments(name: str, arguments: dict) -> list[str]:
    """按 Schema 校验参数，返回问题列表（空表示通过）。

    只实现本模块实际用到的 JSON Schema 子集：``type`` / ``required`` /
    ``enum`` / ``minItems``。刻意不引入 ``jsonschema`` 依赖 ——
    为了几个字段装一个库不划算，而且校验逻辑短到可以直接读。
    """
    schema = get_schema(name)
    spec = schema["input_schema"]
    problems: list[str] = []

    if not isinstance(arguments, dict):
        return [f"参数必须是对象，收到 {type(arguments).__name__}"]

    for key in spec.get("required", []):
        if key not in arguments or arguments[key] is None:
            problems.append(f"缺少必需参数 '{key}'")

    properties = spec.get("properties", {})
    for key, value in arguments.items():
        if key not in properties:
            problems.append(
                f"未知参数 '{key}'；可用：{', '.join(sorted(properties))}"
            )
            continue
        if value is None:
            continue
        problems.extend(_check_type(key, value, properties[key]))

    return problems


_TYPE_MAP = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def _check_type(key: str, value, spec: dict) -> list[str]:
    expected = spec.get("type")
    if not expected:
        return []

    python_type = _TYPE_MAP.get(expected)
    if python_type is None:
        return []

    # bool 是 int 的子类，得单独挡一下 —— 与 parser 里的处理保持一致
    if expected in ("number", "integer") and isinstance(value, bool):
        return [f"参数 '{key}' 应为 {expected}，收到 bool"]
    if expected == "boolean" and not isinstance(value, bool):
        return [f"参数 '{key}' 应为 boolean，收到 {type(value).__name__}"]
    if not isinstance(value, python_type):
        return [f"参数 '{key}' 应为 {expected}，收到 {type(value).__name__}"]

    problems: list[str] = []
    if "enum" in spec and value not in spec["enum"]:
        problems.append(
            f"参数 '{key}' 取值必须是 {spec['enum']} 之一，收到 {value!r}"
        )
    if expected == "array":
        min_items = spec.get("minItems")
        if min_items is not None and len(value) < min_items:
            problems.append(f"参数 '{key}' 至少需要 {min_items} 项，收到 {len(value)} 项")
    return problems
