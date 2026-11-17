# -*- coding: utf-8 -*-
"""流体网络求解与 Agent Skill。

已完成阶段
----------
* 第一阶段：流体网络基础数据模型 + TOML Schema + Parser + 基础稳态求解器。
* 第二阶段：流路分析 + 工况分析 + 功能可靠性 + 标准 JSON 输出。
* 第三阶段：纯静态 HTML + JavaScript 可视化页面。
* 第四阶段：Agent Skill 层 —— 5 个可调用、可测试的原子工具 + JSON Schema。

快速上手::

    from fluid_network import FluidConfigParser, AnalysisBuilder

    network, scenarios = FluidConfigParser().load("examples/example.toml")
    builder = AnalysisBuilder()

    analysis = builder.build(network, scenarios[0])
    print(analysis.to_json())            # 稳定 schema 的 JSON
    print(analysis.summary.functional_loads)

只想拿内部数值时，也可以直接用 :class:`Solver`::

    from fluid_network import Solver, Analyzer

    result = Solver().solve(network, scenarios[0])
    print(Analyzer().render(network, scenarios[0], result))

物理模型（严格按需求文档，未引入额外公式）::

    ΔP = R · Q²         管路压力损失
    V  = Q / A          流速
    A  = π · D² / 4     圆管截面积
    ΣQ_in = ΣQ_out      节点流量守恒

SI 单位约定（求解器内部一律使用，不做任何隐式换算）::

    pressure   Pa        flow    m³/s
    diameter   m         length  m
    velocity   m/s       resistance  Pa·s²/m⁶   (使 ΔP = R·Q² 量纲成立)

展示层负责 Pa -> kPa、m³/s -> L/s 的换算。
"""

from .analysis import AnalysisBuilder
from .analyzer import Analyzer
from .exceptions import (
    ConfigError,
    FluidNetworkError,
    NotFoundError,
    ParseError,
    SolverError,
    TopologyError,
    ValidationError,
)
from .models import (
    LOAD_STATUS_LABELS,
    LOAD_STATUS_PRIORITY,
    AnalysisLoad,
    AnalysisNode,
    AnalysisPipe,
    AnalysisResult,
    AnalysisSummary,
    AnalysisValve,
    LoadResult,
    LoadStatus,
    Network,
    Node,
    NodeResult,
    NodeType,
    PathResult,
    Pipe,
    PipeResult,
    Scenario,
    ScenarioInfo,
    SolverResult,
    TopologySummary,
    Valve,
    ValveResult,
)
from .diagnostics import Diagnostic, DiagnosticCollector
from .parser import FluidConfigParser, load_network, load_scenarios
from .paths import FlowPathAnalyzer
from .reliability import ReliabilityAnalyzer, ReliabilityVerdict, evaluate_load_reliability
from .solver import Solver, evaluate_load
from .skills import (
    SkillResult,
    analyze_all_scenarios,
    analyze_scenario,
    compare_scenarios,
    explain_load,
    parse_network,
    render_report,
    summarize_network,
)
from .topology import Topology, TopologyViolation, build_topology, has_cycle

__version__ = "0.3.0"

__all__ = [
    "__version__",
    # 数据模型
    "Network",
    "Node",
    "NodeType",
    "Pipe",
    "Valve",
    "Scenario",
    # 结果模型
    "NodeResult",
    "PipeResult",
    "ValveResult",
    "LoadResult",
    "SolverResult",
    "LoadStatus",
    "LOAD_STATUS_LABELS",
    "LOAD_STATUS_PRIORITY",
    # 第二阶段：分析结果模型
    "AnalysisResult",
    "AnalysisLoad",
    "AnalysisNode",
    "AnalysisPipe",
    "AnalysisValve",
    "AnalysisSummary",
    "PathResult",
    "ScenarioInfo",
    "TopologySummary",
    # 组件
    "FluidConfigParser",
    "load_network",
    "load_scenarios",
    "Solver",
    "evaluate_load",
    "Analyzer",
    "AnalysisBuilder",
    "FlowPathAnalyzer",
    "ReliabilityAnalyzer",
    "ReliabilityVerdict",
    "evaluate_load_reliability",
    "Topology",
    "TopologyViolation",
    "build_topology",
    "has_cycle",
    # 第四阶段：Agent Skill 层
    "SkillResult",
    "parse_network",
    "analyze_scenario",
    "analyze_all_scenarios",
    "explain_load",
    "compare_scenarios",
    "render_report",
    "summarize_network",
    "Diagnostic",
    "DiagnosticCollector",
    # 异常
    "FluidNetworkError",
    "ConfigError",
    "ParseError",
    "ValidationError",
    "SolverError",
    "TopologyError",
    "NotFoundError",
]
