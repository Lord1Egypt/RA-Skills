# -*- coding: utf-8 -*-
"""流体网络的数据模型。

设计要点
--------
1. **纯标准库**：使用 ``dataclasses``，不引入 Pydantic / attrs，保证零依赖可跑。
2. **不可变**：网络定义（:class:`Network` 及其成员）在解析完成后即视为只读，
   因为求解器可能有多个、会并发跑不同工况。可变状态全部放在 :class:`Scenario`
   与求解结果里。
3. **校验分两层**：
   - 字段级校验在 ``__post_init__`` 中完成（正数、非空 id……）；
   - 跨对象校验（id 唯一、引用存在）需要看到整个网络，放在 :class:`Network`
     的 ``__post_init__`` 与 parser 里，错误信息更上下文相关。
4. **单位约定**（SI，全局统一）::

      压力      Pa
      流量      m3/s
      直径      m
      流阻 R    Pa·s^2/m^6   (使 ΔP = R·Q^2 量纲成立)
      流速      m/s
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .diagnostics import Diagnostic, DiagnosticCollector
from .exceptions import NotFoundError, TopologyError, ValidationError

# 纯水密度，仅用于报告展示（当前物理模型不使用密度）。
WATER_DENSITY = 1000.0


class NodeType(str, Enum):
    """节点类型。

    ``Pump`` / ``Junction`` / ``Load`` 是当前支持的三种。
    由于继承 ``str``，可以直接与字符串比较（``node.type == "pump"``）。
    """

    PUMP = "pump"
    JUNCTION = "junction"
    LOAD = "load"


class LoadStatus(str, Enum):
    """负载的功能状态。

    判定优先级（自上而下，命中即止）::

        1. 不可达                    -> ISOLATED
        2. 可达但 pressure < 阈值     -> LOW_PRESSURE
        3. 可达、压力达标，流量不足    -> LOW_FLOW
        4. 两项都达标                -> HEALTHY
        5. 拓扑不支持，无法判定       -> UNSUPPORTED

    ``FAILED`` 是兜底值，不属于上述优先级链 —— 它表示"求解过程本身出了
    意料之外的问题"。除异常路径外不会出现。

    ``HEALTHY`` 是唯一 ``functional == True`` 的状态。
    """

    HEALTHY = "HEALTHY"
    ISOLATED = "ISOLATED"
    LOW_PRESSURE = "LOW_PRESSURE"
    LOW_FLOW = "LOW_FLOW"
    UNSUPPORTED = "UNSUPPORTED"
    FAILED = "FAILED"

    @property
    def functional(self) -> bool:
        """该状态是否算"功能正常"。"""
        return self is LoadStatus.HEALTHY

    @property
    def zh(self) -> str:
        """中文标签，供文本报告使用。"""
        return LOAD_STATUS_LABELS[self]


# 中文标签（文本报告用）
LOAD_STATUS_LABELS: dict["LoadStatus", str] = {
    LoadStatus.HEALTHY: "正常",
    LoadStatus.ISOLATED: "不可达",
    LoadStatus.LOW_PRESSURE: "压力不足",
    LoadStatus.LOW_FLOW: "流量不足",
    LoadStatus.UNSUPPORTED: "拓扑不支持",
    LoadStatus.FAILED: "失败",
}

# 功能判定优先级（数值越小越优先）
LOAD_STATUS_PRIORITY: dict["LoadStatus", int] = {
    LoadStatus.ISOLATED: 0,
    LoadStatus.UNSUPPORTED: 1,
    LoadStatus.LOW_PRESSURE: 2,
    LoadStatus.LOW_FLOW: 3,
    LoadStatus.HEALTHY: 4,
    LoadStatus.FAILED: 5,
}


def _numeric_error(
    code: str,
    label: str,
    field: str,
    value: float,
    *,
    positive: bool,
) -> ValidationError:
    """构造一条带修复建议的数值校验错误。

    ``label`` 形如 ``"负载节点 'L1' 的 min_pressure"`` —— 元素名与字段名都在里面，
    这里把它拆出来是为了能给出**具体的**建议（"改成大于 0 的数" vs "补上这个字段"）。
    """
    requirement = "正数" if positive else "非负数"
    if value is None:
        suggestion = f"补上 {field} 字段，取值必须是{requirement}"
        reason = "缺失"
    elif isinstance(value, str):
        suggestion = f"给 {field} 去掉引号，改成一个{requirement}"
        reason = "类型不对"
    else:
        suggestion = f"把 {field} 改成一个{'大于 0' if positive else '大于等于 0'}的数"
        reason = "取值越界"

    return ValidationError(
        f"{label} 必须为{requirement}，当前值 {value!r}",
        diagnostics=[
            Diagnostic(
                code=code,
                message=f"{label} 必须为{requirement}，当前值 {value!r}",
                field=field,
                suggestion=suggestion,
                context={"actual_value": repr(value), "reason": reason, "requirement": requirement},
            )
        ],
    )


def _require_positive(value: float, label: str, field: str = "") -> float:
    if value is None or not math.isfinite(float(value)) or float(value) <= 0.0:
        raise _numeric_error("invalid_numeric_range", label, field, value, positive=True)
    return float(value)


def _require_non_negative(value: float, label: str, field: str = "") -> float:
    if value is None or not math.isfinite(float(value)) or float(value) < 0.0:
        raise _numeric_error("invalid_numeric_range", label, field, value, positive=False)
    return float(value)


# --------------------------------------------------------------------------- #
# 网络元件
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Node:
    """网络节点。

    - ``pump``     : 压力边界，必须提供 ``pressure``（泵出口设定压力）。
    - ``junction`` : 三通/分叉点，无附加属性。
    - ``load``     : 需液点，必须提供 ``min_pressure`` 与 ``min_flow``。

    负载的两个流量概念**必须区分开**（第二阶段引入）：

    - ``min_flow``        最低工作流量阈值 —— **只用于功能判定**。
    - ``required_flow``   当前工况下该负载实际需要的流量 —— **用于求解**。
      缺省时等于 ``min_flow``（第一阶段的等价行为）。
    - ``supply_limit``    可选。该负载在当前工况下**最多**能接收到的流量。
      缺省不限制。这是"供液受限"场景的建模入口 —— 也是 ``LOW_FLOW``
      状态在正常树状网络里唯一可能真实出现的来源。
    """

    id: str
    type: NodeType
    pressure: float | None = None         # 仅 pump
    min_pressure: float | None = None     # 仅 load
    min_flow: float | None = None         # 仅 load —— 阈值
    required_flow: float | None = None    # 仅 load —— 求解需求，缺省 = min_flow
    supply_limit: float | None = None     # 仅 load —— 供液上限，缺省不限制

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValidationError(f"节点 id 必须是非空字符串，当前值 {self.id!r}")
        if not isinstance(self.type, NodeType):
            object.__setattr__(self, "type", NodeType(str(self.type).lower()))

        if self.type is NodeType.PUMP:
            object.__setattr__(self, "pressure", _require_positive(self.pressure, f"泵节点 '{self.id}' 的 pressure", "pressure"))
        else:
            if self.pressure is not None:
                raise ValidationError(f"节点 '{self.id}' 类型为 {self.type.value}，不允许设置 pressure 字段")

        if self.type is NodeType.LOAD:
            object.__setattr__(
                self, "min_pressure", _require_positive(self.min_pressure, f"负载节点 '{self.id}' 的 min_pressure", "min_pressure")
            )
            object.__setattr__(
                self, "min_flow", _require_non_negative(self.min_flow, f"负载节点 '{self.id}' 的 min_flow", "min_flow")
            )
            if self.required_flow is not None:
                object.__setattr__(
                    self,
                    "required_flow",
                    _require_non_negative(self.required_flow, f"负载节点 '{self.id}' 的 required_flow", "required_flow"),
                )
            if self.supply_limit is not None:
                object.__setattr__(
                    self,
                    "supply_limit",
                    _require_non_negative(self.supply_limit, f"负载节点 '{self.id}' 的 supply_limit", "supply_limit"),
                )
        else:
            extra = (
                ("min_pressure", self.min_pressure),
                ("min_flow", self.min_flow),
                ("required_flow", self.required_flow),
                ("supply_limit", self.supply_limit),
            )
            for name, value in extra:
                if value is not None:
                    raise ValidationError(f"节点 '{self.id}' 类型为 {self.type.value}，不允许设置 {name} 字段")

    @property
    def is_source(self) -> bool:
        """是否为压力边界（压力源）。"""
        return self.type is NodeType.PUMP

    @property
    def demand(self) -> float:
        """求解时该节点向网络索取的目标流量（m³/s）。

        非负载节点恒为 0。这是 Solver 唯一读取的"需求"字段 ——
        与用于功能判定的 :attr:`min_flow` 相互独立。
        """
        if self.type is not NodeType.LOAD:
            return 0.0
        return float(self.required_flow if self.required_flow is not None else (self.min_flow or 0.0))

    def supplied_flow(self, demanded: float | None = None) -> float:
        """给定管路能送到的流量，返回该负载**实际**能取用的流量。

        ``实际取用 = min(需求, 供液上限)``。缺省不设上限时即为需求本身。
        """
        target = self.demand if demanded is None else float(demanded)
        if self.supply_limit is None:
            return target
        return min(target, float(self.supply_limit))


@dataclass(frozen=True)
class Pipe:
    """圆管。压力损失遵循简化经验公式 ``ΔP = R · Q²``。"""

    id: str
    from_node: str
    to_node: str
    resistance: float
    diameter: float
    length: float | None = None   # 可选，仅供展示

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValidationError(f"管路 id 必须是非空字符串，当前值 {self.id!r}")
        if self.from_node == self.to_node:
            raise ValidationError(f"管路 '{self.id}' 的 from 与 to 不能是同一个节点")
        object.__setattr__(
            self, "resistance", _require_positive(self.resistance, f"管路 '{self.id}' 的 resistance", "resistance")
        )
        object.__setattr__(self, "diameter", _require_positive(self.diameter, f"管路 '{self.id}' 的 diameter", "diameter"))
        if self.length is not None:
            object.__setattr__(self, "length", _require_positive(self.length, f"管路 '{self.id}' 的 length", "length"))

    @property
    def area(self) -> float:
        """圆管截面积 A = π·D²/4（m²）。"""
        return math.pi * self.diameter**2 / 4.0


@dataclass(frozen=True)
class Valve:
    """理想阀：只通断，不产生压力损失（R = 0）。

    开关状态属于工况（:class:`Scenario`），因此不保存在这里。
    """

    id: str
    from_node: str
    to_node: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValidationError(f"阀门 id 必须是非空字符串，当前值 {self.id!r}")
        if self.from_node == self.to_node:
            raise ValidationError(f"阀门 '{self.id}' 的 from 与 to 不能是同一个节点")


# --------------------------------------------------------------------------- #
# 工况
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Scenario:
    """一个运行工况。

    - ``valve_states`` : 阀门 id -> 开/关。**未列出的阀门默认开启**（见 ``valve_open``）。
    - ``failures``     : 预留字段，一阶段不参与计算，仅原样保留以便后续扩展
                         （例如管道破裂、泵停机）。
    - ``actions``      : 预留字段，同上（例如调节泵压、临时增开阀门）。
    """

    id: str
    name: str = ""
    valve_states: Mapping[str, bool] = field(default_factory=dict)
    failures: tuple[Mapping[str, Any], ...] = ()
    actions: tuple[Mapping[str, Any], ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValidationError(f"工况 id 必须是非空字符串，当前值 {self.id!r}")
        # 冻结成普通 dict，避免外部持有的 Mapping 在求解过程中被改动。
        normalised = {str(k): bool(v) for k, v in dict(self.valve_states).items()}
        object.__setattr__(self, "valve_states", normalised)

    @property
    def display_name(self) -> str:
        return self.name or self.id

    def valve_open(self, valve_id: str) -> bool:
        """阀门在本次工况下是否开启。未显式列出的阀门视为开启。"""
        return self.valve_states.get(valve_id, True)


# --------------------------------------------------------------------------- #
# 网络
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Network:
    """一张完整的流体网络定义（不含工况）。"""

    id: str
    name: str = ""
    nodes: tuple[Node, ...] = ()
    pipes: tuple[Pipe, ...] = ()
    valves: tuple[Valve, ...] = ()

    # 派生索引，解析后由 __post_init__ 填充，不参与相等性比较。
    _node_index: Mapping[str, Node] = field(default_factory=dict, repr=False, compare=False)
    _nodes_by_type: Mapping[NodeType, tuple[Node, ...]] = field(
        default_factory=dict, repr=False, compare=False
    )
    _diagnostics: tuple[Diagnostic, ...] = field(default=(), repr=False, compare=False)

    def __post_init__(self) -> None:
        collector = DiagnosticCollector()

        if not isinstance(self.id, str) or not self.id.strip():
            collector.error(
                "invalid_network_id",
                f"网络 id 必须是非空字符串，当前值 {self.id!r}",
                location="[network]",
                field="id",
                suggestion='在 [network] 段落里补上 id = "your-network-id"',
            )

        nodes = tuple(self.nodes)
        pipes = tuple(self.pipes)
        valves = tuple(self.valves)

        if not nodes:
            collector.error(
                "no_nodes",
                "网络必须至少包含一个节点",
                location="[[nodes]]",
                suggestion="至少添加一个 [[nodes]] 段落（通常是 pump 与 load）",
            )
        if not pipes:
            collector.error(
                "no_pipes",
                "网络必须至少包含一条管路",
                location="[[pipes]]",
                suggestion="至少添加一个 [[pipes]] 段落把节点连起来",
            )

        self._check_unique_ids(collector, nodes, pipes, valves)
        node_index = {n.id: n for n in nodes}

        # 逐个元件收集引用错误 —— 不要在第一条就中断，
        # 否则 Agent 改一个跑一次，体验很差。
        for index, pipe in enumerate(pipes):
            site = f"[[pipes]][{index}]"
            self._check_endpoint(collector, pipe.id, "管路", "from", pipe.from_node, site, node_index)
            self._check_endpoint(collector, pipe.id, "管路", "to", pipe.to_node, site, node_index)
        for index, valve in enumerate(valves):
            site = f"[[valves]][{index}]"
            self._check_endpoint(collector, valve.id, "阀门", "from", valve.from_node, site, node_index)
            self._check_endpoint(collector, valve.id, "阀门", "to", valve.to_node, site, node_index)

        if collector.has_errors:
            raise ValidationError.from_collector(
                f"网络 '{self.id}' 定义有 {len(collector.errors)} 处问题", collector
            )

        by_type: dict[NodeType, list[Node]] = {t: [] for t in NodeType}
        for node in nodes:
            by_type[node.type].append(node)

        object.__setattr__(self, "nodes", nodes)
        object.__setattr__(self, "pipes", pipes)
        object.__setattr__(self, "valves", valves)
        object.__setattr__(self, "_node_index", node_index)
        object.__setattr__(self, "_nodes_by_type", {t: tuple(v) for t, v in by_type.items()})
        object.__setattr__(self, "_diagnostics", collector.items)

    @property
    def diagnostics(self) -> tuple[Diagnostic, ...]:
        """构建过程中产生的警告（非致命）。"""
        return getattr(self, "_diagnostics", ())

    # -- 校验辅助 ---------------------------------------------------------- #
    @staticmethod
    def _check_unique_ids(collector: DiagnosticCollector, nodes, pipes, valves) -> None:
        seen: dict[str, tuple[str, str]] = {}
        kinds = (("节点", "[[nodes]]", nodes), ("管路", "[[pipes]]", pipes), ("阀门", "[[valves]]", valves))
        for kind, section, items in kinds:
            for index, item in enumerate(items):
                if item.id in seen:
                    first_kind, first_site = seen[item.id]
                    collector.error(
                        "duplicate_id",
                        f"id '{item.id}' 重复：已用作{first_kind}（{first_site}），此处又被声明为{kind}",
                        location=f"{section}[{index}].id",
                        field="id",
                        suggestion=f"把其中一个 '{item.id}' 改成未使用过的名字；"
                                   "节点 / 管路 / 阀门的 id 共用同一个命名空间",
                        duplicate_id=item.id,
                        first_declared_as=first_kind,
                    )
                else:
                    seen[item.id] = (kind, f"{section}[{index}]")

    @staticmethod
    def _check_endpoint(
        collector: DiagnosticCollector,
        element_id: str,
        kind: str,
        field: str,
        node_id: str,
        site: str,
        node_index: Mapping[str, Node],
    ) -> None:
        if node_id in node_index:
            return
        available = sorted(node_index)
        preview = ", ".join(available[:8]) + ("…" if len(available) > 8 else "")
        collector.error(
            "unknown_endpoint",
            f"{kind} '{element_id}' 的 {field} 引用了不存在的节点 '{node_id}'",
            location=f"{site}.{field}",
            field=field,
            suggestion=(
                f"把 {field} 改成已存在的节点 id；当前可用节点：{preview or '（无）'}"
            ),
            element_id=element_id,
            referenced_node=node_id,
            available_nodes=available,
        )

    # -- 查询接口 ---------------------------------------------------------- #
    @property
    def node_index(self) -> Mapping[str, Node]:
        return self._node_index

    @property
    def node_ids(self) -> tuple[str, ...]:
        return tuple(self._node_index)

    @property
    def element_ids(self) -> frozenset[str]:
        """所有元件 id（节点 + 管路 + 阀门）。"""
        return frozenset(self._node_index) | {p.id for p in self.pipes} | {v.id for v in self.valves}

    def node(self, node_id: str) -> Node:
        try:
            return self._node_index[node_id]
        except KeyError:
            raise NotFoundError(f"网络中不存在节点 '{node_id}'") from None

    def nodes_of_type(self, node_type: NodeType | str) -> tuple[Node, ...]:
        if not isinstance(node_type, NodeType):
            node_type = NodeType(str(node_type).lower())
        return self._nodes_by_type.get(node_type, ())

    def pipe(self, pipe_id: str) -> Pipe:
        for pipe in self.pipes:
            if pipe.id == pipe_id:
                return pipe
        raise NotFoundError(f"网络中不存在管路 '{pipe_id}'")

    def valve(self, valve_id: str) -> Valve:
        for valve in self.valves:
            if valve.id == valve_id:
                return valve
        raise NotFoundError(f"网络中不存在阀门 '{valve_id}'")

    # -- 拓扑 -------------------------------------------------------------- #
    @property
    def pump(self) -> Node:
        """返回唯一压力源。多泵/无泵在一阶段均不支持。"""
        pumps = self.nodes_of_type(NodeType.PUMP)
        if not pumps:
            raise TopologyError("网络中没有泵（pump）节点，一阶段模型需要至少一个压力源")
        if len(pumps) > 1:
            ids = ", ".join(p.id for p in pumps)
            raise TopologyError(f"一阶段模型只支持单泵，当前发现 {len(pumps)} 个：{ids}")
        return pumps[0]

    @property
    def loads(self) -> tuple[Node, ...]:
        return self.nodes_of_type(NodeType.LOAD)

    @property
    def total_demand(self) -> float:
        """所有负载的求解需求之和（m³/s）。"""
        return sum(load.demand for load in self.loads)

    @property
    def total_min_flow(self) -> float:
        """所有负载的最低工作流量阈值之和（m³/s）。"""
        return sum(load.min_flow or 0.0 for load in self.loads)


# --------------------------------------------------------------------------- #
# 求解结果
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class NodeResult:
    node_id: str
    pressure: float | None   # 隔离节点为 None
    status: str              # "ok" | "isolated"
    node_type: NodeType | None = None
    inflow: float = 0.0
    outflow: float = 0.0
    demand: float = 0.0      # 该节点自身消耗的流量（仅负载非零）

    @property
    def residual(self) -> float:
        """流量守恒残差 ``ΣQ_in − ΣQ_out − demand``，理想情况下为 0。"""
        return self.inflow - self.outflow - self.demand

    @property
    def is_isolated(self) -> bool:
        return self.status == "isolated"


@dataclass(frozen=True)
class PipeResult:
    pipe_id: str
    from_node: str
    to_node: str
    flow: float                  # m³/s，流向为声明的 from -> to
    velocity: float              # m/s
    pressure_drop: float         # Pa，恒等于 R·Q²
    active: bool = True          # 是否参与本次工况计算
    from_pressure: float | None = None
    to_pressure: float | None = None


@dataclass(frozen=True)
class ValveResult:
    valve_id: str
    is_open: bool
    flow: float = 0.0            # 关闭或未导通时为 0
    pressure_drop: float = 0.0   # 理想阀恒为 0
    active: bool = False

    @property
    def status(self) -> str:
        return "open" if self.is_open else "closed"


@dataclass(frozen=True)
class LoadResult:
    load_id: str
    pressure: float | None
    flow: float | None           # m³/s；不可达时为 None（不是 0）
    functional: bool             # 等价于 status is HEALTHY
    status: LoadStatus = LoadStatus.HEALTHY
    min_pressure: float | None = None
    min_flow: float | None = None
    required_flow: float | None = None
    reason: str = ""

    @property
    def demanded(self) -> float:
        """求解时该负载向网络索取的目标流量（m³/s）。"""
        if self.required_flow is not None:
            return float(self.required_flow)
        return float(self.min_flow or 0.0)

    @property
    def supplied(self) -> float | None:
        """实际送达该负载的流量（m³/s），即 :attr:`flow` 的别名。

        不可达时返回 ``None`` —— "没有有效计算值"和"零流量"是两回事。
        """
        return self.flow

    @property
    def is_isolated(self) -> bool:
        return self.status is LoadStatus.ISOLATED

    @property
    def supplied_or_zero(self) -> float:
        """供液量的数值形式，不可达时按 0 计。仅用于**聚合求和**。

        展示层应该用 :attr:`flow`（可空），这样才能如实呈现"无有效值"。
        """
        return float(self.flow) if self.flow is not None else 0.0


@dataclass(frozen=True)
class SolverResult:
    network_id: str
    scenario_id: str
    scenario_name: str
    node_results: Mapping[str, NodeResult] = field(default_factory=dict)
    pipe_results: Mapping[str, PipeResult] = field(default_factory=dict)
    valve_results: Mapping[str, ValveResult] = field(default_factory=dict)
    load_results: Mapping[str, LoadResult] = field(default_factory=dict)
    paths: Mapping[str, "PathResult"] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    # -- 便捷访问 ---------------------------------------------------------- #
    def pressure(self, node_id: str) -> float | None:
        return self._get(self.node_results, node_id, "节点结果").pressure

    def path(self, load_id: str) -> "PathResult":
        return self._get(self.paths, load_id, "流路结果")

    def flow(self, element_id: str) -> float:
        if element_id in self.pipe_results:
            return self.pipe_results[element_id].flow
        if element_id in self.valve_results:
            return self.valve_results[element_id].flow
        raise NotFoundError(f"结果中不存在管路/阀门 '{element_id}'")

    def load(self, load_id: str) -> LoadResult:
        return self._get(self.load_results, load_id, "负载结果")

    def all_loads_functional(self) -> bool:
        return all(r.functional for r in self.load_results.values())

    def functional_loads(self) -> tuple[LoadResult, ...]:
        return tuple(r for r in self.load_results.values() if r.functional)

    def internal_nodes(self) -> tuple[NodeResult, ...]:
        """非泵、非隔离的节点 —— 这些节点必须严格满足流量守恒。"""
        return tuple(
            r for r in self.node_results.values()
            if r.node_type is not NodeType.PUMP and not r.is_isolated
        )

    def supply_flow(self) -> float:
        """泵向网络补充的总流量（m³/s）。压力边界节点的残差即供液量。"""
        return sum(
            r.outflow - r.inflow
            for r in self.node_results.values()
            if r.node_type is NodeType.PUMP and not r.is_isolated
        )

    def demand_flow(self) -> float:
        """所有负载实际获得的流量之和（m³/s）。

        不可达负载没有有效流量值，在**求和**语境下按 0 计 —— 求和需要一个数，
        而展示层应当读 :attr:`LoadResult.flow`（可空）以如实呈现"无有效值"。
        """
        return sum(r.supplied_or_zero for r in self.load_results.values())

    def max_conservation_residual(self) -> float:
        """内部节点守恒残差绝对值的最大值（m³/s）。

        泵是压力边界，其"残差"等于供液量而非误差，故不纳入统计。
        """
        return max((abs(r.residual) for r in self.internal_nodes()), default=0.0)

    @staticmethod
    def _get(mapping: Mapping[str, Any], key: str, label: str):
        try:
            return mapping[key]
        except KeyError:
            raise NotFoundError(f"{label}中不存在 '{key}'") from None


__all__ = [
    "WATER_DENSITY",
    "NodeType",
    "LoadStatus",
    "LOAD_STATUS_LABELS",
    "LOAD_STATUS_PRIORITY",
    "Node",
    "Pipe",
    "Valve",
    "Scenario",
    "Network",
    "NodeResult",
    "PipeResult",
    "ValveResult",
    "LoadResult",
    "SolverResult",
    # 第二阶段：统一分析结果
    "ScenarioInfo",
    "TopologySummary",
    "PathResult",
    "AnalysisLoad",
    "AnalysisNode",
    "AnalysisPipe",
    "AnalysisValve",
    "AnalysisSummary",
    "AnalysisResult",
]


# =========================================================================== #
# 第二阶段：统一分析结果模型
#
# 设计原则
# --------
# 1. **扁平、稳定、可序列化**。全部是 dataclass 的标量 / 列表字段，
#    不含任何计算逻辑，``to_dict()`` 的结果就是最终 JSON 结构。
# 2. **不直接 dump 内部对象**。``SolverResult`` 里带了 ``NodeType`` 枚举、
#    ``frozenset`` 等，直接序列化会产生不可控结构；这里全部转成基本类型。
# 3. **缺失值一律用 ``None``**，不用 0 冒充。被切断的负载压力是 ``None``
#    而不是 0 Pa —— 前端能一眼区分"没有值"和"值为零"。
# =========================================================================== #
@dataclass(frozen=True)
class ScenarioInfo:
    """工况标识。"""

    id: str
    name: str

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}


@dataclass(frozen=True)
class TopologySummary:
    """当前工况下的拓扑概况。"""

    connected: bool                        # 是否所有节点都从泵可达
    supported: bool                        # 拓扑是否在本模型能力范围内
    isolated_nodes: tuple[str, ...] = ()   # 不可达节点
    unsupported_elements: tuple[str, ...] = ()   # 位于环上、导致不支持的元件
    unsupported_reason: str = ""

    def to_dict(self) -> dict:
        return {
            "connected": self.connected,
            "supported": self.supported,
            "isolated_nodes": list(self.isolated_nodes),
            "unsupported_elements": list(self.unsupported_elements),
            "unsupported_reason": self.unsupported_reason,
        }


@dataclass(frozen=True)
class PathResult:
    """一个负载的流路分析结果。"""

    load_id: str
    reachable: bool
    path: tuple[str, ...] = ()               # 元件 id，按泵 -> 负载顺序
    node_path: tuple[str, ...] = ()          # 节点 id，按泵 -> 负载顺序
    isolation_point: str | None = None       # 导致切断的元件（通常是关闭的阀门）
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "load_id": self.load_id,
            "reachable": self.reachable,
            "path": list(self.path),
            "node_path": list(self.node_path),
            "isolation_point": self.isolation_point,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class AnalysisNode:
    """分析结果里的节点条目。"""

    node_id: str
    node_type: NodeType
    pressure: float | None
    status: str                    # "ok" | "isolated"
    inflow: float = 0.0
    outflow: float = 0.0
    demand: float = 0.0

    @property
    def residual(self) -> float:
        """流量守恒残差 ``ΣQ_in − ΣQ_out − demand``。"""
        return self.inflow - self.outflow - self.demand

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "type": self.node_type.value,
            "pressure": self.pressure,
            "status": self.status,
            "inflow": self.inflow,
            "outflow": self.outflow,
            "demand": self.demand,
            "residual": self.residual,
        }


@dataclass(frozen=True)
class AnalysisPipe:
    """分析结果里的管路条目。

    ``flow`` / ``velocity`` / ``pressure_drop`` 在管路未参与计算时为 ``None``
    —— 与 :class:`AnalysisLoad` 一致，不用 0 冒充"没有有效计算值"。
    """

    pipe_id: str
    from_node: str
    to_node: str
    flow: float | None
    velocity: float | None
    pressure_drop: float | None
    resistance: float = 0.0
    diameter: float = 0.0
    active: bool = True
    from_pressure: float | None = None
    to_pressure: float | None = None

    def to_dict(self) -> dict:
        return {
            "pipe_id": self.pipe_id,
            "from": self.from_node,
            "to": self.to_node,
            "flow": self.flow,
            "velocity": self.velocity,
            "pressure_drop": self.pressure_drop,
            "resistance": self.resistance,
            "diameter": self.diameter,
            "active": self.active,
            "from_pressure": self.from_pressure,
            "to_pressure": self.to_pressure,
        }


@dataclass(frozen=True)
class AnalysisLoad:
    """分析结果里的负载条目 —— 求解数值 + 流路 + 功能状态三者的汇总。"""

    load_id: str
    pressure: float | None
    flow: float | None
    functional: bool
    status: LoadStatus
    min_pressure: float | None = None
    min_flow: float | None = None
    required_flow: float | None = None
    reason: str = ""
    reachable: bool = True
    path: tuple[str, ...] = ()
    node_path: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "load_id": self.load_id,
            "pressure": self.pressure,
            "flow": self.flow,
            "min_pressure": self.min_pressure,
            "min_flow": self.min_flow,
            "required_flow": self.required_flow,
            "functional": self.functional,
            "status": self.status.value,
            "reason": self.reason,
            "reachable": self.reachable,
            "path": list(self.path),
            "node_path": list(self.node_path),
        }


@dataclass(frozen=True)
class AnalysisValve:
    """分析结果里的阀门条目。

    阀门不是管路，没有流速与沿程压降；它只有"通 / 断"和流经它的流量。
    单独建模而不是塞进 ``pipes``，是为了让前端不必猜哪条是阀。
    """

    valve_id: str
    from_node: str
    to_node: str
    is_open: bool
    flow: float | None = None
    active: bool = False
    pressure_drop: float = 0.0   # 理想阀恒为 0

    def to_dict(self) -> dict:
        return {
            "valve_id": self.valve_id,
            "from": self.from_node,
            "to": self.to_node,
            "is_open": self.is_open,
            "flow": self.flow,
            "active": self.active,
            "pressure_drop": self.pressure_drop,
        }


@dataclass(frozen=True)
class AnalysisSummary:
    """整体统计。"""

    total_loads: int = 0
    functional_loads: int = 0
    failed_loads: int = 0
    isolated_loads: int = 0
    status_counts: Mapping[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "total_loads": self.total_loads,
            "functional_loads": self.functional_loads,
            "failed_loads": self.failed_loads,
            "isolated_loads": self.isolated_loads,
            "status_counts": dict(self.status_counts),
        }


@dataclass(frozen=True)
class AnalysisResult:
    """一次完整分析的结果 —— 这是对外（尤其对前端）的唯一契约。

    字段划分刻意保持"一个对象一件事"：拓扑归拓扑、流路归流路、
    数值归数值、判定归判定。任何一层出问题都能被独立观察。
    """

    scenario: ScenarioInfo
    topology: TopologySummary
    paths: Mapping[str, PathResult] = field(default_factory=dict)
    nodes: tuple[AnalysisNode, ...] = ()
    pipes: tuple[AnalysisPipe, ...] = ()
    valves: tuple[AnalysisValve, ...] = ()
    loads: tuple[AnalysisLoad, ...] = ()
    warnings: tuple[str, ...] = ()
    summary: AnalysisSummary = field(default_factory=AnalysisSummary)

    # 供调试 / 溯源，不参与 JSON 输出的主体结构
    network_id: str = ""
    schema_version: str = "2.0"
    # 主干管 id，由**后端**判定后提供；前端一律直接采用，不自行重算。
    main_pipe_id: str = ""

    # -- 便捷访问（不进 JSON） ------------------------------------------- #
    def load(self, load_id: str) -> AnalysisLoad:
        for item in self.loads:
            if item.load_id == load_id:
                return item
        raise NotFoundError(f"分析结果中不存在负载 '{load_id}'")

    def pipe(self, pipe_id: str) -> AnalysisPipe:
        for item in self.pipes:
            if item.pipe_id == pipe_id:
                return item
        raise NotFoundError(f"分析结果中不存在管路 '{pipe_id}'")

    def path(self, load_id: str) -> PathResult:
        try:
            return self.paths[load_id]
        except KeyError:
            raise NotFoundError(f"分析结果中不存在负载 '{load_id}' 的流路") from None

    # -- 序列化 ---------------------------------------------------------- #
    def to_dict(self) -> dict:
        """转成纯基本类型的字典 —— 结果可直接被 ``json.dump`` 或前端读取。"""
        return {
            "schema_version": self.schema_version,
            "network_id": self.network_id,
            "scenario": self.scenario.to_dict(),
            "topology": self.topology.to_dict(),
            "paths": {key: value.to_dict() for key, value in self.paths.items()},
            "nodes": [node.to_dict() for node in self.nodes],
            "pipes": [pipe.to_dict() for pipe in self.pipes],
            "valves": [valve.to_dict() for valve in self.valves],
            "loads": [load.to_dict() for load in self.loads],
            "summary": self.summary.to_dict(),
            "warnings": list(self.warnings),
            # 主干管由后端判定，前端直接采用（缺失时为空串）
            "main_pipe_id": self.main_pipe_id or None,
        }

    def to_json(self, *, indent: int | None = 2, ensure_ascii: bool = False) -> str:
        """转成 JSON 文本。

        ``ensure_ascii=False`` 让中文以原字符输出，文件更可读；只要文件以
        UTF-8 保存，任何标准 JSON 解析器都能正确读回。
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=ensure_ascii)
